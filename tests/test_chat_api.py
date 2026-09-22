"""Integration tests for the FastAPI application and POST /api/chat endpoint."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    """Verify health probe returns status 200 and metadata."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "AcadAssist API"
    assert "environment" in data


def test_chat_endpoint_valid_request():
    """Verify POST /api/chat processes valid request and returns response schema."""
    payload = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "message": "What should I study today?",
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "sources" in data
    assert "actions" in data
    assert isinstance(data["sources"], list)
    assert isinstance(data["actions"], list)


def test_chat_endpoint_empty_message_validation():
    """Verify POST /api/chat rejects empty message string with 400."""
    payload = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "message": "   ",
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 400
    assert "message" in response.json()["detail"].lower()


def test_chat_endpoint_empty_user_id_validation():
    """Verify POST /api/chat rejects empty user_id string with 400."""
    payload = {
        "user_id": "",
        "message": "Explain paging.",
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 400
    assert "user_id" in response.json()["detail"].lower()


def test_chat_endpoint_missing_fields_validation():
    """Verify POST /api/chat rejects missing body fields with 422."""
    response = client.post("/api/chat", json={})
    assert response.status_code == 422
