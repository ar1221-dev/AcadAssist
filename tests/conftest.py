import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.api.deps import get_kb_service
from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.services.knowledge_base import KnowledgeBaseService
from app.services.storage import StorageService


@pytest.fixture(scope="session")
def temp_dir():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


@pytest.fixture
def test_storage(temp_dir):
    raw_dir = temp_dir / "raw"
    processed_dir = temp_dir / "processed"
    return StorageService(raw_base_dir=raw_dir, processed_base_dir=processed_dir)


@pytest.fixture
def db_session(temp_dir):
    # Use file-based SQLite in temp dir so connection is shared cleanly
    db_file = temp_dir / "test.db"
    test_engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        test_engine.dispose()
        if db_file.exists():
            db_file.unlink(missing_ok=True)


@pytest.fixture
def kb_service(test_storage):
    return KnowledgeBaseService(storage=test_storage)


@pytest.fixture
def client(db_session: Session, kb_service: KnowledgeBaseService):
    def override_get_db():
        yield db_session

    def override_get_kb_service():
        return kb_service

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_kb_service] = override_get_kb_service

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
