"""AcadAssist main application entrypoint and FastAPI router registration.

Consolidates Knowledge Base, Assessment, and Study Intelligence subsystems into the shared AcadAssist backend.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.assessment.api.router import assessment_router
from app.config import settings
from app.database.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan managing database table initialization."""
    init_db()
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="AcadAssist API",
        description="AI-Powered Personalized Academic Study Assistant Backend",
        version="2.0.0",
        lifespan=lifespan,
    )

    # Configure CORS for React frontend integration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routes under /api
    app.include_router(api_router)
    app.include_router(assessment_router, prefix="/api")

    @app.get("/health", tags=["Health"])
    def health_check():
        """Unified health check endpoint confirming subsystem readiness."""
        return {
            "status": "healthy",
            "app": "AcadAssist",
            "version": "2.0.0",
            "subsystems": {
                "knowledge_rag": "operational",
                "assessment": "operational",
            },
            "embedding_model": settings.EMBEDDING_MODEL,
            "embedding_dimensions": settings.EMBEDDING_DIMENSIONS,
        }

    return app


app = create_app()


def main() -> None:
    """Entry point to launch the development server."""
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
