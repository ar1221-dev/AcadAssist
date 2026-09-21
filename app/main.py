"""AcadAssist main entrypoint and FastAPI application.

Integrates Person 4 Study Intelligence routes into the shared AcadAssist application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.config import settings
from app.database.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan managing database initialization."""
    # Initialize shared database schema idempotently
    init_db()
    yield


app = FastAPI(
    title="AcadAssist API",
    description="AI-powered study assistant platform backend.",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register consolidated API routers under /api
app.include_router(api_router)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "subsystem": "study-intelligence-v2", "version": "2.0.0"}


def main() -> None:
    """Entry point to run the server."""
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
