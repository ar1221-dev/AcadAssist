"""End-to-End integration test for the AcadAssist Operating Systems demo scenario.

Validates the full pipeline flow:
React Client
    ↓
POST /api/chat
    ↓
FastAPI Router
    ↓
AcadAssist Agent Service
    ↓
search_knowledge tool
    ↓
Knowledge Base / AI Search chunks
    ↓
Grounded Answer & Citation Construction
    ↓
FastAPI
    ↓
React Client
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_e2e_explain_paging_demo():
    """Verify complete end-to-end OS demo scenario for 'Explain paging.'"""
    payload = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "message": "Explain paging.",
    }

    # 1. React sends POST request to FastAPI
    response = client.post("/api/chat", json=payload)

    # 2. FastAPI returns 200 OK
    assert response.status_code == 200
    data = response.json()

    # 3. Verify grounded message content
    message = data.get("message", "")
    assert len(message) > 0
    assert "paging" in message.lower()
    assert "memory" in message.lower()
    assert "frame" in message.lower() or "page" in message.lower()

    # 4. Verify source citation preservation
    sources = data.get("sources", [])
    assert len(sources) >= 1

    primary_source = sources[0]
    assert primary_source["document_title"] == "Operating Systems Concepts: Virtual Memory"
    assert primary_source["filename"] == "os_concepts_ch8_paging.pdf"
    assert primary_source["page_number"] == 324
    assert primary_source["score"] >= 0.8
    assert "paging" in primary_source["content_snippet"].lower()

    # 5. Verify action items structure
    assert isinstance(data.get("actions"), list)
