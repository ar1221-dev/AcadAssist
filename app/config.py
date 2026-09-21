from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AcadAssist Knowledge Base (Person 2 Checkpoint 1)"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./knowledge_base.db"
    
    # Storage directories (resolved relative to workspace or absolute)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    STORAGE_RAW_DIR: Path = BASE_DIR / "storage" / "raw"
    STORAGE_PROCESSED_DIR: Path = BASE_DIR / "storage" / "processed"
    
    # Upload limits
    MAX_FILE_SIZE_BYTES: int = 50 * 1024 * 1024  # 50 MB
    ALLOWED_EXTENSIONS: set[str] = {"pdf", "pptx", "ppt", "docx", "doc", "txt"}
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
