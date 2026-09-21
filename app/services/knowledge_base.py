import logging
import uuid
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.material import Material, ProcessingStatus
from app.services.processors import DocumentProcessingError, get_processor_for_extension
from app.services.storage import StorageService, storage_service
from app.services.validator import MaterialValidator
from app.utils.normalizer import build_rag_document
from app.utils.security import compute_sha256, extract_extension, sanitize_filename

logger = logging.getLogger(__name__)


class MaterialNotFoundError(Exception):
    def __init__(self, material_id: str):
        super().__init__(f"Material with ID '{material_id}' was not found.")
        self.material_id = material_id


class ContentNotReadyError(Exception):
    def __init__(self, material_id: str, status: str):
        super().__init__(
            f"Content for material '{material_id}' is not ready yet. Current status: '{status}'"
        )
        self.material_id = material_id
        self.status = status


class KnowledgeBaseService:
    def __init__(self, storage: StorageService | None = None):
        self.storage = storage or storage_service

    def upload_material(
        self,
        db: Session,
        file_bytes: bytes,
        original_filename: str,
        subject: str,
        course: str | None = None,
        title: str | None = None,
        description: str | None = None,
        process_immediately: bool = True,
    ) -> Material:
        """
        Ingest, validate, store, and process an academic document.
        """
        # 1. Validation
        clean_subject = MaterialValidator.validate_subject(subject)
        MaterialValidator.validate_filename(original_filename)
        file_type = MaterialValidator.validate_file_type(original_filename)
        MaterialValidator.validate_file_content(file_bytes)

        # 2. Duplicate Detection
        content_hash = compute_sha256(file_bytes)
        MaterialValidator.check_duplicate(db, content_hash=content_hash, subject=clean_subject)

        # 3. Identifiers & Filenames
        material_id = str(uuid.uuid4())
        safe_filename = sanitize_filename(original_filename)

        # Default title if not specified
        if not title or not title.strip():
            derived_title = Path(safe_filename).stem.replace("_", " ").title()
        else:
            derived_title = title.strip()

        # 4. Raw Storage
        saved_raw_path = self.storage.save_raw_file(
            material_id=material_id,
            filename=safe_filename,
            content=file_bytes,
        )

        # 5. Database Record Creation
        material = Material(
            id=material_id,
            title=derived_title,
            original_filename=original_filename,
            filename=safe_filename,
            file_type=file_type,
            file_size=len(file_bytes),
            content_hash=content_hash,
            subject=clean_subject,
            course=course.strip() if course and course.strip() else None,
            description=description.strip() if description and description.strip() else None,
            storage_path=str(saved_raw_path.resolve()),
            processing_status=ProcessingStatus.UPLOADED,
        )
        db.add(material)
        db.commit()
        db.refresh(material)

        logger.info("Material %s (%s) registered under subject '%s'", material_id, safe_filename, clean_subject)

        # 6. Processing
        if process_immediately:
            self.process_material(db, material_id)
            db.refresh(material)

        return material

    def process_material(self, db: Session, material_id: str) -> Material:
        """
        Run document extraction and store normalized content.
        """
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            raise MaterialNotFoundError(material_id)

        material.processing_status = ProcessingStatus.PROCESSING
        material.processing_error = None
        db.commit()
        db.refresh(material)

        raw_file_path = self.storage.get_raw_file_path(material_id, material.filename)

        try:
            processor = get_processor_for_extension(material.file_type)
            extraction_result = processor.extract(raw_file_path)

            # Build normalized output for Person 4 RAG
            rag_content = build_rag_document(
                material_id=material.id,
                title=material.title,
                subject=material.subject,
                course=material.course,
                file_type=material.file_type,
                sections=extraction_result.sections,
                extra_metadata=extraction_result.metadata,
            )

            # Store processed output
            processed_file = self.storage.save_processed_content(material_id, rag_content)

            material.processed_path = str(processed_file.resolve())
            material.page_count = extraction_result.page_count
            material.slide_count = extraction_result.slide_count
            material.content_length = len(rag_content)
            material.processing_status = ProcessingStatus.PROCESSED
            material.processing_error = None

            logger.info("Material %s processed successfully (%d chars)", material_id, len(rag_content))

        except Exception as exc:
            logger.error("Error processing material %s: %s", material_id, str(exc), exc_info=True)
            material.processing_status = ProcessingStatus.FAILED
            material.processing_error = str(exc)

        db.commit()
        db.refresh(material)
        return material

    def get_material(self, db: Session, material_id: str) -> Material:
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            raise MaterialNotFoundError(material_id)
        return material

    def list_materials(
        self,
        db: Session,
        subject: str | None = None,
        course: str | None = None,
        status: ProcessingStatus | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[int, list[Material]]:
        query = db.query(Material)

        if subject:
            query = query.filter(Material.subject == subject.strip())
        if course:
            query = query.filter(Material.course == course.strip())
        if status:
            query = query.filter(Material.processing_status == status)

        total = query.count()
        items = query.order_by(Material.uploaded_at.desc()).offset(skip).limit(limit).all()
        return total, items

    def get_material_content(self, db: Session, material_id: str) -> dict:
        material = self.get_material(db, material_id)

        if material.processing_status == ProcessingStatus.FAILED:
            raise ContentNotReadyError(
                material_id, f"Processing failed: {material.processing_error}"
            )
        elif material.processing_status != ProcessingStatus.PROCESSED:
            raise ContentNotReadyError(material_id, material.processing_status.value)

        content = self.storage.read_processed_content(material_id)
        if content is None:
            raise ContentNotReadyError(
                material_id, "Processed file missing from storage disk."
            )

        return {
            "id": material.id,
            "title": material.title,
            "subject": material.subject,
            "course": material.course,
            "file_type": material.file_type,
            "processing_status": material.processing_status,
            "content_length": material.content_length or len(content),
            "page_count": material.page_count,
            "slide_count": material.slide_count,
            "processed_content": content,
        }

    def delete_material(self, db: Session, material_id: str) -> None:
        material = self.get_material(db, material_id)

        # 1. Delete stored disk files
        self.storage.delete_material_storage(material_id)

        # 2. Delete database record
        db.delete(material)
        db.commit()
        logger.info("Material %s and its storage artifacts deleted.", material_id)


knowledge_base_service = KnowledgeBaseService()
