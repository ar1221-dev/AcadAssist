"""FastAPI dependencies for Person 2 routes."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.processing.pipeline import DocumentProcessingService
from app.services.rag.embedding import EmbeddingService
from app.services.rag.knowledge import get_embedding_service, get_search_service, set_search_service
from app.services.rag.search import AzureSearchService
from app.services.storage.azure_storage import AzureStorageService

_storage_service: AzureStorageService | None = None


def get_storage() -> AzureStorageService:
    global _storage_service
    if _storage_service is None:
        _storage_service = AzureStorageService()
    return _storage_service


def set_storage_service(service: AzureStorageService) -> None:
    """Override storage service (e.g. for testing)."""
    global _storage_service
    _storage_service = service


def get_search() -> AzureSearchService:
    return get_search_service()


def get_embedding() -> EmbeddingService:
    return get_embedding_service()


def get_processing_service(
    storage: AzureStorageService = Depends(get_storage),
    embedding: EmbeddingService = Depends(get_embedding),
    search: AzureSearchService = Depends(get_search),
) -> DocumentProcessingService:
    return DocumentProcessingService(
        storage_service=storage,
        embedding_service=embedding,
        search_service=search,
    )
