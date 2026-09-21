from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings
from app.database.base import Base

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Initialize database tables idempotently without dropping existing data."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Provide a transactional database session scope."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
