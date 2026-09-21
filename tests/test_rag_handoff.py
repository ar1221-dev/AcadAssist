from app.utils.normalizer import build_rag_document


def test_rag_handoff_document_structure():
    material_id = "test-uuid-999"
    title = "Binary Search Trees"
    subject = "Data Structures"
    course = "CS101"
    file_type = "pdf"
    sections = [
        {"label": "Page 1", "content": "Root, left and right subtrees."},
        {"label": "Page 2", "content": "In-order traversal yields sorted order."},
    ]

    doc = build_rag_document(
        material_id=material_id,
        title=title,
        subject=subject,
        course=course,
        file_type=file_type,
        sections=sections,
        extra_metadata={"Author": "Prof. Smith"},
    )

    # Verify RAG markers
    assert "=== ACADASSIST KNOWLEDGE BASE METADATA ===" in doc
    assert f"Material ID: {material_id}" in doc
    assert f"Title: {title}" in doc
    assert f"Subject: {subject}" in doc
    assert f"Course: {course}" in doc
    assert "File Type: PDF" in doc
    assert "Author: Prof. Smith" in doc
    assert "=== DOCUMENT CONTENT ===" in doc
    assert "--- Page 1 ---" in doc
    assert "Root, left and right subtrees." in doc
    assert "--- Page 2 ---" in doc
    assert "In-order traversal yields sorted order." in doc
