"""Centralized configuration for AcadAssist Knowledge Base & RAG subsystem (Person 2).

Integrates with the single shared application database and supports both production
Azure integrations and explicit local testing providers.
"""

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings with environment override support."""

    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Database: single shared database for AcadAssist
    DATABASE_URL: str = "sqlite:///./data/acadassist.db"

    # General Azure credentials (from .env.example)
    AZURE_ENDPOINT: str | None = None
    AZURE_API_KEY: str | None = None

    # Azure Blob Storage Configuration
    AZURE_STORAGE_CONNECTION_STRING: str | None = None
    AZURE_STORAGE_CONTAINER: str = "acadassist-documents"
    STORAGE_LOCAL_DIR: str = "./data/storage"

    # Azure AI Search Configuration
    AZURE_SEARCH_ENDPOINT: str | None = None
    AZURE_SEARCH_KEY: str | None = None
    AZURE_SEARCH_INDEX_NAME: str = "acadassist-knowledge-index"

    # Embedding Service Configuration (Required: text-embedding-3-small, 1536 dimensions)
    AZURE_OPENAI_ENDPOINT: str | None = None
    AZURE_OPENAI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSIONS: int = 1536

    # Document Chunking Configuration
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    MAX_UPLOAD_SIZE_BYTES: int = 50 * 1024 * 1024  # 50 MB
    ALLOWED_EXTENSIONS: list[str] = Field(
        default_factory=lambda: [".pdf", ".ppt", ".pptx", ".docx", ".txt"]
    )

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def is_production(self) -> bool:
        """Check if currently running in production environment."""
        return self.ENVIRONMENT.lower() in ("production", "prod")

    def validate_production_azure(self) -> None:
        """Ensure all required Azure credentials are provided when running in production."""
        if not self.is_production():
            return
        missing = []
        if not self.AZURE_STORAGE_CONNECTION_STRING:
            missing.append("AZURE_STORAGE_CONNECTION_STRING")
        if not self.AZURE_SEARCH_ENDPOINT:
            missing.append("AZURE_SEARCH_ENDPOINT")
        if not self.AZURE_SEARCH_KEY:
            missing.append("AZURE_SEARCH_KEY")
        if not (self.AZURE_OPENAI_API_KEY or self.OPENAI_API_KEY):
            missing.append("AZURE_OPENAI_API_KEY / OPENAI_API_KEY")

        if missing:
            raise ValueError(
                f"Production environment requires Azure credentials. Missing: {', '.join(missing)}"
            )


settings = Settings()

# Ensure local directories exist if running locally
if settings.DATABASE_URL.startswith("sqlite:///"):
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    if db_path and not db_path.startswith(":memory:"):
        db_dir = Path(db_path).parent
        if db_dir and not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)

local_storage_path = Path(settings.STORAGE_LOCAL_DIR)
if not local_storage_path.exists():
    local_storage_path.mkdir(parents=True, exist_ok=True)
