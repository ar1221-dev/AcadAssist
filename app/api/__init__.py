"""API router consolidating Person 2 Knowledge Base & Person 4 Study Intelligence routes."""

from fastapi import APIRouter

from app.api.routes.documents import router as documents_router
from app.api.routes.knowledge import router as knowledge_router
from app.api.routes.plans import router as plans_router, tasks_router
from app.api.routes.progress import router as progress_router
from app.api.routes.reports import router as reports_router

api_router = APIRouter(prefix="/api")

# Person 2 Knowledge Base routes
api_router.include_router(documents_router)
api_router.include_router(knowledge_router)

# Person 4 Study Intelligence routes
api_router.include_router(progress_router)
api_router.include_router(plans_router)
api_router.include_router(tasks_router)
api_router.include_router(reports_router)

__all__ = ["api_router"]
