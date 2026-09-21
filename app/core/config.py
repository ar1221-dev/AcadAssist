"""AcadAssist core configuration.

Centralizes all settings, database URLs, and configurable business rule thresholds
for adaptive difficulty, weak-topic detection, and exam-aware assessment.
"""

from os import getenv
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load .env file if available
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


class AssessmentSettings(BaseModel):
    """Configurable settings and thresholds for Person 3 Assessment Subsystem."""

    # Adaptive Difficulty Thresholds (percentages 0 - 100)
    adaptive_easy_threshold: float = Field(
        default=float(getenv("ADAPTIVE_EASY_THRESHOLD", "50.0")),
        description="Percentage below which difficulty adapts to easy / revision",
    )
    adaptive_hard_threshold: float = Field(
        default=float(getenv("ADAPTIVE_HARD_THRESHOLD", "75.0")),
        description="Percentage above which difficulty adapts to hard",
    )
    default_difficulty: str = Field(
        default=getenv("DEFAULT_DIFFICULTY", "medium"),
        description="Default quiz difficulty if no performance history exists",
    )

    # Mastery / Weak Topic Thresholds (ratios 0.0 - 1.0)
    weak_topic_threshold: float = Field(
        default=float(getenv("WEAK_TOPIC_THRESHOLD", "0.60")),
        description="Mastery ratio below which a topic is classified as weak",
    )
    strong_topic_threshold: float = Field(
        default=float(getenv("STRONG_TOPIC_THRESHOLD", "0.75")),
        description="Mastery ratio at or above which a topic is classified as strong",
    )

    # Exam Proximity Windows (in days)
    exam_normal_days: int = Field(
        default=int(getenv("EXAM_NORMAL_DAYS", "14")),
        description="Days threshold beyond which normal assessment is applied",
    )
    exam_increased_days: int = Field(
        default=int(getenv("EXAM_INCREASED_DAYS", "7")),
        description="Days threshold (7-14d) for increased assessment focus",
    )
    exam_weak_topic_days: int = Field(
        default=int(getenv("EXAM_WEAK_TOPIC_DAYS", "3")),
        description="Days threshold (3-7d) for targeted weak-topic assessment",
    )
    exam_revision_days: int = Field(
        default=int(getenv("EXAM_REVISION_DAYS", "2")),
        description="Days threshold (<=2d) for revision + targeted assessment",
    )


class Settings(BaseModel):
    """Global application settings."""

    app_name: str = "AcadAssist"
    app_version: str = "1.0.0"
    environment: str = getenv("ENVIRONMENT", "development")
    log_level: str = getenv("LOG_LEVEL", "INFO")

    # Shared Application Database
    database_url: str = getenv(
        "DATABASE_URL", f"sqlite:///{DATA_DIR / 'acadassist.db'}"
    )

    # Assessment Specific Settings
    assessment: AssessmentSettings = Field(default_factory=AssessmentSettings)


settings = Settings()
