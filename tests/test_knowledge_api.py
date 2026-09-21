"""Integration tests for POST /api/knowledge/search API endpoint."""

import io


def test_knowledge_search_api_endpoint(client, sample_academic_entities):
    entities = sample_academic_entities
    user_id = entities["user_a"].user_id
    course_id = entities["course"].course_id
    subject_id = entities["subject_os"].subject_id

    # 1. Upload and process a document first
    content = (
        "Operating Systems Unit 3\n\n"
        "Deadlock Prevention\n"
        "Deadlock prevention conditions: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait.\n\n"
        "Banker's Algorithm\n"
        "Banker's algorithm ensures resource allocation never enters an unsafe state."
    )
    upload_resp = client.post(
        "/api/documents",
        data={
            "user_id": user_id,
            "course_id": course_id,
            "subject_id": subject_id,
            "title": "Operating Systems Unit 3",
        },
        files={"file": ("OS_Unit_3.txt", io.BytesIO(content.encode("utf-8")), "text/plain")},
    )
    doc_id = upload_resp.json()["document_id"]
    client.post(f"/api/documents/{doc_id}/process?user_id={user_id}")

    # 2. Search knowledge API
    search_payload = {
        "user_id": user_id,
        "query": "Explain deadlock prevention",
        "course_id": course_id,
        "subject_id": subject_id,
        "top_k": 3,
    }
    search_resp = client.post("/api/knowledge/search", json=search_payload)
    assert search_resp.status_code == 200

    data = search_resp.json()
    assert "results" in data
    results = data["results"]
    assert len(results) >= 1

    top_chunk = results[0]
    assert top_chunk["document_id"] == doc_id
    assert top_chunk["course_id"] == course_id
    assert top_chunk["subject_id"] == subject_id
    assert "Deadlock prevention" in top_chunk["content"]
    assert top_chunk["score"] > 0.0


def test_knowledge_search_api_validation(client):
    # Empty query should return empty results
    resp = client.post(
        "/api/knowledge/search",
        json={"user_id": "user-123", "query": "   ", "top_k": 5},
    )
    assert resp.status_code == 422 or (resp.status_code == 200 and resp.json()["results"] == [])

    # Missing user_id should fail validation
    resp_no_user = client.post("/api/knowledge/search", json={"query": "test query"})
    assert resp_no_user.status_code == 422
