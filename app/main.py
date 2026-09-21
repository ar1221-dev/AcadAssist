from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.materials import router as materials_router
from app.config import settings
from app.database.session import init_db
from app.services.knowledge_base import (
    ContentNotReadyError,
    MaterialNotFoundError,
)
from app.services.validator import (
    DuplicateMaterialError,
    MaterialValidationError,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Safe database initialization (creates tables if not exist, does NOT drop data)
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AcadAssist Person 2 Checkpoint 1: Knowledge Base and Document Ingestion Foundation",
    lifespan=lifespan,
)

# Enable CORS for local testing or future frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(MaterialNotFoundError)
async def material_not_found_handler(request: Request, exc: MaterialNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.material_id, "message": str(exc)},
    )


@app.exception_handler(DuplicateMaterialError)
async def duplicate_material_handler(request: Request, exc: DuplicateMaterialError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(MaterialValidationError)
async def validation_error_handler(request: Request, exc: MaterialValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(ContentNotReadyError)
async def content_not_ready_handler(request: Request, exc: ContentNotReadyError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc), "status": exc.status},
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "AcadAssist Knowledge Base",
        "version": settings.VERSION,
    }


# Mount materials routes directly at /materials and under /api/v1/materials
app.include_router(materials_router)
app.include_router(materials_router, prefix=settings.API_V1_PREFIX)
