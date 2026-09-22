"""Integration tests for POST /api/knowledge/search endpoint."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_knowledge_search_valid_request():
    """Verify POST /api/knowledge/search returns 200 and valid schema."""
    payload = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "query": "Explain deadlock prevention",
        "course_id": "course-cs-301",
        "subject_id": "subject-os",
        "top_k": 5,
    }
    response = client.post("/api/knowledge/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    if data["results"]:
        first = data["results"][0]
        assert "chunk_id" in first
        assert "document_id" in first
        assert "content" in first
        assert "document_title" in first
        assert "filename" in first
        assert "score" in first


def test_knowledge_search_paging_demo():
    """Verify POST /api/knowledge/search returns expected OS paging mock results."""
    payload = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "query": "Explain paging in operating systems",
        "top_k": 3,
    }
    response = client.post("/api/knowledge/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) >= 1
    assert "paging" in data["results"][0]["content"].lower()
    assert data["results"][0]["filename"] == "os_concepts_ch8_paging.pdf"


def test_knowledge_search_missing_user_id():
    """Verify POST /api/knowledge/search rejects missing user_id."""
    payload = {
        "user_id": "",
        "query": "Explain deadlock prevention",
    }
    response = client.post("/api/knowledge/search", json=payload)
    assert response.status_code == 400
    assert "user_id" in response.json()["detail"].lower()


def test_knowledge_search_missing_query():
    """Verify POST /api/knowledge/search rejects missing query."""
    payload = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "query": "   ",
    }
    response = client.post("/api/knowledge/search", json=payload)
    assert response.status_code == 400
    assert "query" in response.json()["detail"].lower()
