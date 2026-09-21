"""Shared application database configuration and session management.

Provides SQLAlchemy declarative base, session factories, and database initializers
for the single shared AcadAssist application database.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

# Engine configuration with SQLite thread safety support if sqlite is used
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize all registered SQLAlchemy database tables."""
    # Ensure all models are imported prior to creating tables
    import app.assessment.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
