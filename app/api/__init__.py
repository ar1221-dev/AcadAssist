"""API package initialization and router aggregation."""

from fastapi import APIRouter

from app.api.routes.plans import router as plans_router, tasks_router
from app.api.routes.progress import router as progress_router
from app.api.routes.reports import router as reports_router

api_router = APIRouter(prefix="/api")

api_router.include_router(progress_router)
api_router.include_router(plans_router)
api_router.include_router(tasks_router)
api_router.include_router(reports_router)

__all__ = ["api_router"]
