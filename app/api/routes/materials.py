import logging
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_kb_service
from app.database.session import get_db
from app.models.material import ProcessingStatus
from app.schemas.material import (
    MaterialContentResponse,
    MaterialListResponse,
    MaterialResponse,
    MaterialStatusResponse,
)
from app.services.knowledge_base import (
    ContentNotReadyError,
    KnowledgeBaseService,
    MaterialNotFoundError,
)
from app.services.validator import (
    DuplicateMaterialError,
    MaterialValidationError,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/materials", tags=["Materials"])


@router.post(
    "",
    response_model=MaterialResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload an academic material",
    description="Accepts PDF, PPT, PPTX, DOC, DOCX, and TXT files. Validates, stores raw file, extracts content, and prepares normalized RAG text.",
)
async def upload_material(
    file: UploadFile = File(..., description="The academic document to upload"),
    subject: str = Form(..., description="Academic subject/course (e.g., 'Data Structures & Algorithms')"),
    course: str | None = Form(None, description="Course code or identifier (e.g., 'CS201')"),
    title: str | None = Form(None, description="Optional custom title for the document"),
    description: str | None = Form(None, description="Optional document notes or description"),
    db: Session = Depends(get_db),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    # Read file content safely
    try:
        content_bytes = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded file: {str(e)}",
        )

    original_filename = file.filename or "unnamed_document"

    try:
        material = kb_service.upload_material(
            db=db,
            file_bytes=content_bytes,
            original_filename=original_filename,
            subject=subject,
            course=course,
            title=title,
            description=description,
            process_immediately=True,
        )
        return material
    except (DuplicateMaterialError, MaterialValidationError):
        raise
    except Exception as e:
        logger.error("Unhandled error uploading material: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while uploading the document.",
        )


@router.get(
    "",
    response_model=MaterialListResponse,
    summary="List academic materials",
    description="Retrieve materials with optional filtering by subject, course, or processing status.",
)
def list_materials(
    subject: str | None = Query(None, description="Filter by subject"),
    course: str | None = Query(None, description="Filter by course code"),
    status_filter: ProcessingStatus | None = Query(None, alias="status", description="Filter by processing status"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of items to return"),
    db: Session = Depends(get_db),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    total, items = kb_service.list_materials(
        db=db,
        subject=subject,
        course=course,
        status=status_filter,
        skip=skip,
        limit=limit,
    )
    return MaterialListResponse(total=total, items=items)


@router.get(
    "/{material_id}",
    response_model=MaterialResponse,
    summary="Get material metadata",
    description="Retrieve full metadata for a specific material by its ID.",
)
def get_material(
    material_id: str,
    db: Session = Depends(get_db),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    try:
        return kb_service.get_material(db=db, material_id=material_id)
    except MaterialNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{material_id}/content",
    response_model=MaterialContentResponse,
    summary="Get extracted and normalized content",
    description="Retrieve normalized text content prepared for future RAG chunking and embedding.",
)
def get_material_content(
    material_id: str,
    db: Session = Depends(get_db),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    try:
        return kb_service.get_material_content(db=db, material_id=material_id)
    except MaterialNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ContentNotReadyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get(
    "/{material_id}/status",
    response_model=MaterialStatusResponse,
    summary="Get material processing status",
    description="Check processing state (UPLOADED, PROCESSING, PROCESSED, FAILED) and error details if any.",
)
def get_material_status(
    material_id: str,
    db: Session = Depends(get_db),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    try:
        material = kb_service.get_material(db=db, material_id=material_id)
        return MaterialStatusResponse(
            id=material.id,
            title=material.title,
            processing_status=material.processing_status,
            processing_error=material.processing_error,
            uploaded_at=material.uploaded_at,
            updated_at=material.updated_at,
        )
    except MaterialNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{material_id}",
    summary="Delete material",
    description="Delete material record from the database and remove raw and processed storage files from disk.",
)
def delete_material(
    material_id: str,
    db: Session = Depends(get_db),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    try:
        kb_service.delete_material(db=db, material_id=material_id)
        return {
            "status": "success",
            "message": f"Material '{material_id}' and all associated files deleted successfully.",
            "id": material_id,
        }
    except MaterialNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
