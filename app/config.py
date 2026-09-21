"""Centralized configuration for AcadAssist Study Intelligence (Person 4)."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings with environment override support."""

    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Database: single shared database for AcadAssist
    DATABASE_URL: str = "sqlite:///./data/acadassist.db"

    # Study time defaults (minutes per day)
    DEFAULT_STUDY_TIME_MINUTES: int = 120

    # Topic mastery thresholds (percentages 0.0 - 100.0)
    STRONG_MASTERY_THRESHOLD: float = 75.0
    WEAK_MASTERY_THRESHOLD: float = 60.0
    MASTERY_COMPLETION_THRESHOLD: float = 70.0

    # Exam proximity rules (days before exam)
    # <= 2 days: revision + targeted weak-topic focus
    # 3–7 days: targeted weak-topic preparation
    # 7–14 days: increased preparation
    # > 14 days: normal study
    EXAM_PROXIMITY_URGENT_DAYS: int = 2
    EXAM_PROXIMITY_WEAK_PRIORITY_DAYS: int = 7
    EXAM_PROXIMITY_PREP_DAYS: int = 14

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

# Ensure the SQLite directory exists if using local sqlite file
if settings.DATABASE_URL.startswith("sqlite:///"):
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    if db_path and not db_path.startswith(":memory:"):
        db_dir = Path(db_path).parent
        if db_dir and not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)
