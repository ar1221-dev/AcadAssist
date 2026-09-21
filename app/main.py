"""AcadAssist main application entrypoint and FastAPI router registration."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.assessment.api.router import assessment_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for startup and shutdown events."""
    init_db()
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AcadAssist - AI-Powered Personalized Academic Study Assistant Backend",
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

    # Mount Assessment API router under /api
    app.include_router(assessment_router, prefix="/api")

    @app.get("/health", tags=["Health"])
    def health_check():
        return {
            "status": "healthy",
            "app": settings.app_name,
            "version": settings.app_version,
            "subsystems": {
                "assessment": "operational",
            },
        }

    return app


app = create_app()


def main() -> None:
    """Entry point to launch the development server."""
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
