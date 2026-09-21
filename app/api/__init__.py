"""API router consolidating Person 2 Knowledge Base & RAG routes."""

from fastapi import APIRouter
from app.api.routes.documents import router as documents_router
from app.api.routes.knowledge import router as knowledge_router

api_router = APIRouter(prefix="/api")
api_router.include_router(documents_router)
api_router.include_router(knowledge_router)

__all__ = ["api_router"]
