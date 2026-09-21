"""AcadAssist Knowledge Base & RAG main application entrypoint.

Integrates document processing and knowledge retrieval subsystem into the shared AcadAssist backend.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.config import settings
from app.database.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan managing database table initialization."""
    init_db()
    yield


app = FastAPI(
    title="AcadAssist Knowledge & RAG API",
    description="Full Document Processing, Knowledge Base, and Hybrid RAG subsystem.",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes under /api
app.include_router(api_router)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint confirming subsystem readiness."""
    return {
        "status": "ok",
        "subsystem": "knowledge-rag-v2",
        "version": "2.0.0",
        "embedding_model": settings.EMBEDDING_MODEL,
        "embedding_dimensions": settings.EMBEDDING_DIMENSIONS,
    }


def main() -> None:
    """Entry point to run the server."""
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
