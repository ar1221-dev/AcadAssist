"""AcadAssist FastAPI Application Entrypoint.

Provides the REST API server for the React frontend, orchestrating interactions
with the ONE AcadAssist Agent powered by Microsoft Foundry.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from app.api.chat import router as chat_router
from app.api.knowledge import router as knowledge_router
from app.api.tools import router as tools_router

# Configure root logger
settings = get_settings()
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("acadassist")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler for the FastAPI application."""
    logger.info("Starting AcadAssist API (Environment: %s)", settings.environment)
    logger.info("Foundry Agent: %s, Model: %s", settings.foundry_agent_name, settings.foundry_model_deployment)
    logger.info("Search Index: %s, Storage Container: %s", settings.azure_search_index, settings.azure_storage_container)
    yield
    logger.info("Shutting down AcadAssist API")


# Create core FastAPI application
app = FastAPI(
    title="AcadAssist API",
    version="1.0.0",
    description="Backend API powering the AcadAssist AI Study Assistant via Microsoft Foundry.",
    lifespan=lifespan,
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(chat_router)
app.include_router(knowledge_router)
app.include_router(tools_router)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring and readiness probes."""
    return {
        "status": "healthy",
        "service": "AcadAssist API",
        "version": "1.0.0",
        "environment": settings.environment,
        "foundry_configured": settings.is_foundry_configured,
        "search_configured": settings.is_search_configured,
        "storage_configured": settings.is_storage_configured,
    }


def main() -> None:
    """Run server via uvicorn for development."""
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
