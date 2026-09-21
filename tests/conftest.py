"""Pytest configuration, shared fixtures, and database setup for testing."""

import os
import shutil
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.api.deps import get_db, set_search_service, set_storage_service
from app.config import settings
from app.database.base import Base
from app.main import app
from app.models.document import Chunk, Document
from app.models.shared import Course, Subject, User
from app.services.rag.knowledge import set_search_service as set_rag_search_service
from app.services.rag.search import AzureSearchService, LocalHybridSearchIndex
from app.services.storage.azure_storage import AzureStorageService
from app.services.storage.local_storage import LocalStorageService


@pytest.fixture(scope="session", autouse=True)
def test_environment():
    """Ensure tests run with test environment variables."""
    settings.ENVIRONMENT = "test"
    temp_dir = tempfile.mkdtemp(prefix="acadassist_test_storage_")
    settings.STORAGE_LOCAL_DIR = temp_dir
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


from sqlalchemy.pool import StaticPool


@pytest.fixture
def db_engine():
    """Create in-memory SQLite engine for isolated test runs."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    """Yield a transactional database session for tests."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def local_storage(test_environment):
    """Local storage service fixture."""
    storage = LocalStorageService(base_dir=test_environment)
    return storage


@pytest.fixture
def search_service():
    """Clean hybrid search service with isolated local in-memory index."""
    service = AzureSearchService()
    service.local_index = LocalHybridSearchIndex()
    set_search_service(service)
    set_rag_search_service(service)
    return service


@pytest.fixture
def client(db_session, local_storage, search_service):
    """FastAPI TestClient with overridden dependencies."""
    azure_storage = AzureStorageService()
    azure_storage.fallback_storage = local_storage
    set_storage_service(azure_storage)

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_academic_entities(db_session):
    """Seed sample User, Course, and Subject records for testing."""
    user_a = User(user_id="user-alice-001", name="Alice Student", email="alice@test.edu")
    user_b = User(user_id="user-bob-002", name="Bob Student", email="bob@test.edu")
    course = Course(course_id="course-cs-101", name="Computer Science", code="CS101")
    subject_os = Subject(subject_id="subj-os-201", course_id="course-cs-101", name="Operating Systems")
    subject_db = Subject(subject_id="subj-db-202", course_id="course-cs-101", name="Database Systems")

    db_session.add_all([user_a, user_b, course, subject_os, subject_db])
    db_session.commit()

    return {
        "user_a": user_a,
        "user_b": user_b,
        "course": course,
        "subject_os": subject_os,
        "subject_db": subject_db,
    }
