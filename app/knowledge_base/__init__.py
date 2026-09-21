"""Knowledge base module package for AcadAssist (Person 2).

Provides document ingestion, multi-format text extraction (PDF, PPTX, PPT, DOCX, DOC, TXT),
safe storage segregation, metadata indexing, and deterministic normalized text formatting
for downstream RAG consumption.
"""

from app.database.session import SessionLocal, get_db, init_db
from app.models.material import Material, ProcessingStatus
from app.schemas.material import (
    MaterialCreate,
    MaterialListResponse,
    MaterialResponse,
    MaterialStatusResponse,
    ProcessedContentResponse,
)
from app.services.knowledge_base import (
    ContentNotReadyError,
    KnowledgeBaseService,
    MaterialNotFoundError,
    knowledge_base_service,
)
from app.services.processors.base import BaseProcessor, ExtractionResult
from app.services.storage import StorageService, storage_service
from app.services.validator import (
    DocumentValidator,
    DuplicateMaterialError,
    MaterialValidationError,
    validator,
)
from app.utils.normalizer import build_rag_document
from app.utils.security import compute_sha256, sanitize_filename

__all__ = [
    "BaseProcessor",
    "ContentNotReadyError",
    "DocumentValidator",
    "DuplicateMaterialError",
    "ExtractionResult",
    "KnowledgeBaseService",
    "Material",
    "MaterialCreate",
    "MaterialListResponse",
    "MaterialNotFoundError",
    "MaterialResponse",
    "MaterialStatusResponse",
    "MaterialValidationError",
    "ProcessedContentResponse",
    "ProcessingStatus",
    "SessionLocal",
    "StorageService",
    "build_rag_document",
    "compute_sha256",
    "get_db",
    "init_db",
    "knowledge_base_service",
    "sanitize_filename",
    "storage_service",
    "validator",
]
