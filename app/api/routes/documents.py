"""Document management and processing API routes."""

import logging
from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from app.api.deps import get_db, get_processing_service, get_search, get_storage
from app.config import settings
from app.models.document import Chunk, Document
from app.schemas.document import (
    DocumentListResponse,
    DocumentProcessResponse,
    DocumentResponse,
    DocumentSummaryRequest,
    DocumentSummaryResponse,
)
from app.services.processing.pipeline import DocumentProcessingService
from app.services.rag.search import AzureSearchService
from app.services.rag.summarizer import summarize_document
from app.services.storage.azure_storage import AzureStorageService

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    course_id: str = Form(...),
    subject_id: str = Form(...),
    title: str | None = Form(None),
    description: str | None = Form(None),
    db: Session = Depends(get_db),
    storage: AzureStorageService = Depends(get_storage),
):
    """Upload and record a new academic document."""
    raw_name = file.filename or ""
    safe_filename = Path(raw_name).name.strip()
    if not safe_filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    ext = Path(safe_filename).suffix.lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(settings.ALLOWED_EXTENSIONS)}",
        )

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty (0 bytes).")
    if len(file_bytes) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(status_code=400, detail=f"File exceeds max size of {settings.MAX_UPLOAD_SIZE_BYTES} bytes.")

    # Save to storage (Azure Blob or local fallback)
    try:
        storage_path = storage.save_file(file_bytes, safe_filename, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save document to storage: {e}")

    doc_title = title or Path(safe_filename).stem

    doc = Document(
        user_id=user_id,
        course_id=course_id,
        subject_id=subject_id,
        filename=safe_filename,
        file_type=ext.replace(".", ""),
        title=doc_title,
        description=description,
        storage_path=storage_path,
        status="uploaded",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return doc


@router.get("", response_model=DocumentListResponse)
def list_documents(
    user_id: str = Query(..., description="Mandatory requesting user ID"),
    course_id: str | None = Query(None, description="Optional course filter"),
    subject_id: str | None = Query(None, description="Optional subject filter"),
    db: Session = Depends(get_db),
):
    """List documents strictly isolated to the requesting user."""
    query = db.query(Document).filter(Document.user_id == user_id)
    if course_id:
        query = query.filter(Document.course_id == course_id)
    if subject_id:
        query = query.filter(Document.subject_id == subject_id)

    docs = query.order_by(Document.uploaded_at.desc()).all()
    return DocumentListResponse(documents=docs, total=len(docs))


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    user_id: str = Query(..., description="Requesting user ID to verify ownership"),
    db: Session = Depends(get_db),
):
    """Retrieve metadata for a specific document with user ownership verification."""
    doc = db.query(Document).filter(Document.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    if doc.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this document.")
    return doc


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    user_id: str = Query(..., description="Requesting user ID to verify ownership"),
    db: Session = Depends(get_db),
    storage: AzureStorageService = Depends(get_storage),
    search: AzureSearchService = Depends(get_search),
):
    """Delete document from storage, search index, and database, verifying ownership."""
    doc = db.query(Document).filter(Document.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    if doc.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this document.")

    # 1. Clean up storage
    try:
        storage.delete_file(doc.storage_path)
    except Exception as e:
        logger.warning(f"Storage file cleanup exception for document {document_id}: {e}")

    # 2. Clean up search index
    search.delete_chunks_by_document(document_id, user_id)

    # 3. Clean up DB chunks and document record
    db.query(Chunk).filter(Chunk.document_id == document_id).delete()
    db.delete(doc)
    db.commit()

    return {"status": "success", "message": f"Document '{document_id}' and all associated chunks deleted."}


@router.post("/{document_id}/process", response_model=DocumentProcessResponse)
def process_document_endpoint(
    document_id: str,
    user_id: str = Query(..., description="Requesting user ID to verify ownership"),
    db: Session = Depends(get_db),
    pipeline: DocumentProcessingService = Depends(get_processing_service),
):
    """Run full parsing, chunking, embedding, and indexing pipeline on an uploaded document."""
    try:
        doc = pipeline.process_document(document_id, user_id, db)
        return DocumentProcessResponse(
            document_id=doc.document_id,
            status=doc.status,
            message="Document successfully processed and indexed into knowledge base.",
            processed_at=doc.processed_at,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found.")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this document.")
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Processing error: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {e}")


@router.post("/{document_id}/summarize", response_model=DocumentSummaryResponse)
def summarize_document_endpoint(
    document_id: str,
    body: DocumentSummaryRequest,
    user_id: str = Query(..., description="Requesting user ID to verify ownership"),
    db: Session = Depends(get_db),
):
    """Prepare structured document summary context according to requested mode."""
    try:
        summary_data = summarize_document(
            document_id=document_id,
            user_id=user_id,
            mode=body.mode,
            db=db,
        )
        return DocumentSummaryResponse(**summary_data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found.")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this document.")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization preparation failed: {e}")
