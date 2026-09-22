"""Unit tests for Azure AI Search infrastructure and index schema."""

import pytest
from app.azure.search import (
    INDEX_NAME,
    VECTOR_DIMENSIONS,
    AzureSearchManager,
    build_acadassist_index_schema,
)
from azure.search.documents.indexes.models import VectorSearchAlgorithmMetric


def test_search_index_schema_fields():
    """Verify all 18 required fields exist in the index schema."""
    index = build_acadassist_index_schema()
    assert index.name == INDEX_NAME

    field_names = [f.name for f in index.fields]
    expected_fields = [
        "id",
        "chunk_id",
        "user_id",
        "course_id",
        "subject_id",
        "document_id",
        "content",
        "title",
        "section_title",
        "document_title",
        "filename",
        "page_number",
        "slide_number",
        "chunk_index",
        "total_chunks",
        "content_type",
        "created_at",
        "content_vector",
    ]

    assert len(field_names) == 18
    for expected in expected_fields:
        assert expected in field_names, f"Missing expected field: {expected}"


def test_search_index_vector_configuration():
    """Verify vector search dimensions and cosine metric."""
    index = build_acadassist_index_schema()
    vector_field = next(f for f in index.fields if f.name == "content_vector")

    assert vector_field.vector_search_dimensions == VECTOR_DIMENSIONS
    assert vector_field.vector_search_dimensions == 1536
    assert vector_field.vector_search_profile_name == "acadassist-vector-profile"

    assert index.vector_search is not None
    algorithm = index.vector_search.algorithms[0]
    assert algorithm.parameters.metric == VectorSearchAlgorithmMetric.COSINE


def test_search_manager_missing_endpoint():
    """Verify error when attempting client initialization without endpoint."""
    manager = AzureSearchManager(endpoint=None)
    with pytest.raises(ValueError, match="Azure Search endpoint not configured"):
        manager.get_index_client()


def test_search_mandatory_user_id():
    """Verify that user_id filtering is mandatory for search_knowledge."""
    manager = AzureSearchManager(endpoint="https://test.search.windows.net")
    with pytest.raises(ValueError, match="user_id filter is mandatory"):
        manager.search(user_id="", query="test query")


def test_search_execution_with_user_filter(monkeypatch):
    """Verify search builds the correct user_id filter expression."""
    from unittest.mock import MagicMock
    manager = AzureSearchManager(endpoint="https://test.search.windows.net")
    mock_search_client = MagicMock()
    mock_search_client.search.return_value = [{"id": "chunk-1", "content": "Paging"}]
    monkeypatch.setattr(manager, "get_search_client", lambda: mock_search_client)

    res = manager.search(
        user_id="user-123",
        query="paging",
        course_id="cs301",
        subject_id="os",
        top_k=3,
    )
    assert len(res) == 1
    mock_search_client.search.assert_called_once()
    _, kwargs = mock_search_client.search.call_args
    assert kwargs["search_text"] == "paging"
    assert "user_id eq 'user-123'" in kwargs["filter"]
    assert "course_id eq 'cs301'" in kwargs["filter"]
    assert "subject_id eq 'os'" in kwargs["filter"]
    assert kwargs["top"] == 3
