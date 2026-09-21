from pathlib import Path
import pytest
from fastapi.testclient import TestClient

SAMPLE_DIR = Path("sample_data")


def test_upload_pdf(client: TestClient):
    pdf_path = SAMPLE_DIR / "trees.pdf"
    with open(pdf_path, "rb") as f:
        response = client.post(
            "/materials",
            files={"file": ("trees.pdf", f, "application/pdf")},
            data={"subject": "Data Structures", "course": "CS101", "title": "Trees & BST"},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["subject"] == "Data Structures"
    assert data["course"] == "CS101"
    assert data["title"] == "Trees & BST"
    assert data["file_type"] == "pdf"
    assert data["processing_status"] == "PROCESSED"
    assert data["page_count"] == 2
    assert data["content_length"] > 50


def test_upload_pptx(client: TestClient):
    pptx_path = SAMPLE_DIR / "networks.pptx"
    with open(pptx_path, "rb") as f:
        response = client.post(
            "/materials",
            files={"file": ("networks.pptx", f, "application/vnd.openxmlformats-officedocument.presentationml.presentation")},
            data={"subject": "Computer Networks", "course": "CS301"},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["file_type"] == "pptx"
    assert data["processing_status"] == "PROCESSED"
    assert data["slide_count"] == 2


def test_upload_docx(client: TestClient):
    docx_path = SAMPLE_DIR / "normalization.docx"
    with open(docx_path, "rb") as f:
        response = client.post(
            "/materials",
            files={"file": ("normalization.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            data={"subject": "DBMS", "course": "CS202"},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["file_type"] == "docx"
    assert data["processing_status"] == "PROCESSED"
    assert data["content_length"] > 100


def test_upload_txt(client: TestClient):
    txt_path = SAMPLE_DIR / "linear_algebra.txt"
    with open(txt_path, "rb") as f:
        response = client.post(
            "/materials",
            files={"file": ("linear_algebra.txt", f, "text/plain")},
            data={"subject": "Mathematics", "course": "MATH101"},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["file_type"] == "txt"
    assert data["processing_status"] == "PROCESSED"


def test_upload_legacy_ppt_and_doc(client: TestClient):
    ppt_path = SAMPLE_DIR / "os_scheduling.ppt"
    with open(ppt_path, "rb") as f:
        resp1 = client.post(
            "/materials",
            files={"file": ("os_scheduling.ppt", f, "application/vnd.ms-powerpoint")},
            data={"subject": "Operating Systems"},
        )
    assert resp1.status_code == 201
    assert resp1.json()["file_type"] == "ppt"
    assert resp1.json()["processing_status"] == "PROCESSED"

    doc_path = SAMPLE_DIR / "software_eng.doc"
    with open(doc_path, "rb") as f:
        resp2 = client.post(
            "/materials",
            files={"file": ("software_eng.doc", f, "application/msword")},
            data={"subject": "Software Engineering"},
        )
    assert resp2.status_code == 201
    assert resp2.json()["file_type"] == "doc"
    assert resp2.json()["processing_status"] == "PROCESSED"


def test_validation_unsupported_file_type(client: TestClient):
    response = client.post(
        "/materials",
        files={"file": ("malware.exe", b"executable bytes", "application/octet-stream")},
        data={"subject": "Security"},
    )
    assert response.status_code == 400
    assert "unsupported" in response.json()["detail"].lower()


def test_validation_empty_file(client: TestClient):
    response = client.post(
        "/materials",
        files={"file": ("empty.pdf", b"", "application/pdf")},
        data={"subject": "Data Structures"},
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_validation_unsafe_filename(client: TestClient):
    response = client.post(
        "/materials",
        files={"file": ("../../evil.pdf", b"%PDF-1.4 dummy", "application/pdf")},
        data={"subject": "Data Structures"},
    )
    assert response.status_code == 400
    assert "unsafe" in response.json()["detail"].lower()


def test_validation_missing_subject(client: TestClient):
    response = client.post(
        "/materials",
        files={"file": ("test.txt", b"Hello world", "text/plain")},
        data={"subject": "   "},
    )
    assert response.status_code == 400
    assert "subject" in response.json()["detail"].lower()


def test_duplicate_handling(client: TestClient):
    content = b"Exact duplicate test content"
    # First upload
    r1 = client.post(
        "/materials",
        files={"file": ("doc1.txt", content, "text/plain")},
        data={"subject": "Physics"},
    )
    assert r1.status_code == 201

    # Second upload with same content and same subject -> 409 Conflict
    r2 = client.post(
        "/materials",
        files={"file": ("doc2.txt", content, "text/plain")},
        data={"subject": "Physics"},
    )
    assert r2.status_code == 409
    assert "duplicate" in r2.json()["error_code"].lower()

    # Same content under different subject should succeed
    r3 = client.post(
        "/materials",
        files={"file": ("doc3.txt", content, "text/plain")},
        data={"subject": "Chemistry"},
    )
    assert r3.status_code == 201


def test_get_material_and_content_and_status(client: TestClient):
    txt_path = SAMPLE_DIR / "linear_algebra.txt"
    with open(txt_path, "rb") as f:
        upload_resp = client.post(
            "/materials",
            files={"file": ("linear_algebra.txt", f, "text/plain")},
            data={"subject": "Mathematics", "course": "MATH101", "title": "Linear Algebra"},
        )
    mat_id = upload_resp.json()["id"]

    # 1. GET /materials/{id}
    get_resp = client.get(f"/materials/{mat_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == mat_id
    assert get_resp.json()["title"] == "Linear Algebra"

    # 2. GET /materials/{id}/content
    content_resp = client.get(f"/materials/{mat_id}/content")
    assert content_resp.status_code == 200
    content_data = content_resp.json()
    assert content_data["id"] == mat_id
    assert "=== ACADASSIST KNOWLEDGE BASE METADATA ===" in content_data["processed_content"]
    assert "Linear Algebra" in content_data["processed_content"]

    # 3. GET /materials/{id}/status
    status_resp = client.get(f"/materials/{mat_id}/status")
    assert status_resp.status_code == 200
    assert status_resp.json()["processing_status"] == "PROCESSED"
    assert status_resp.json()["processing_error"] is None

    # 4. GET non-existent
    not_found = client.get("/materials/non-existent-id")
    assert not_found.status_code == 404


def test_list_materials_and_filtering(client: TestClient):
    # Upload 2 materials in different subjects
    client.post(
        "/materials",
        files={"file": ("file1.txt", b"Content for Subject A", "text/plain")},
        data={"subject": "SubjectA", "course": "CRS100"},
    )
    client.post(
        "/materials",
        files={"file": ("file2.txt", b"Content for Subject B", "text/plain")},
        data={"subject": "SubjectB", "course": "CRS200"},
    )

    # List all
    all_resp = client.get("/materials")
    assert all_resp.status_code == 200
    all_data = all_resp.json()
    assert all_data["total"] >= 2

    # Filter by subject
    sub_resp = client.get("/materials?subject=SubjectA")
    assert sub_resp.status_code == 200
    sub_data = sub_resp.json()
    assert all(item["subject"] == "SubjectA" for item in sub_data["items"])
    assert sub_data["total"] >= 1

    # Filter by course
    crs_resp = client.get("/materials?course=CRS200")
    assert crs_resp.status_code == 200
    crs_data = crs_resp.json()
    assert all(item["course"] == "CRS200" for item in crs_data["items"])


def test_delete_material(client: TestClient):
    upload_resp = client.post(
        "/materials",
        files={"file": ("to_delete.txt", b"Disposable content", "text/plain")},
        data={"subject": "Temporary"},
    )
    mat_id = upload_resp.json()["id"]

    # Delete
    del_resp = client.delete(f"/materials/{mat_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["status"] == "success"

    # Confirm it's gone from GET /materials/{id}
    get_resp = client.get(f"/materials/{mat_id}")
    assert get_resp.status_code == 404

    # Confirm DELETE on non-existent returns 404
    del_again = client.delete(f"/materials/{mat_id}")
    assert del_again.status_code == 404


def test_api_v1_prefix_compatibility(client: TestClient):
    # Verify routes work under /api/v1/materials as well
    resp = client.get("/api/v1/materials")
    assert resp.status_code == 200


def test_upload_corrupted_file_results_in_failed_status(client: TestClient):
    # Corrupted PDF with .pdf extension
    corrupted_bytes = b"Not a valid PDF file at all"
    upload_resp = client.post(
        "/materials",
        files={"file": ("corrupted.pdf", corrupted_bytes, "application/pdf")},
        data={"subject": "Robotics"},
    )
    assert upload_resp.status_code == 201
    data = upload_resp.json()
    assert data["processing_status"] == "FAILED"
    assert data["processing_error"] is not None
    assert len(data["processing_error"]) > 0

    # Getting content of failed file should return 409 Conflict
    content_resp = client.get(f"/materials/{data['id']}/content")
    assert content_resp.status_code == 409

