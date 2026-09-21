"""Tests for hybrid knowledge search, ranking, and filtering."""

from datetime import datetime, timezone
from app.models.document import Chunk
from app.services.rag.embedding import EmbeddingService
from app.services.rag.knowledge import search_knowledge
from app.services.rag.search import AzureSearchService, LocalHybridSearchIndex


def test_hybrid_search_ranking_and_top_k(search_service):
    embedding_service = EmbeddingService()

    # Index 3 chunks
    chunks = [
        Chunk(
            chunk_id="chunk-os-1",
            document_id="doc-os",
            user_id="user-alice",
            course_id="cs-101",
            subject_id="os-1",
            content="Deadlock prevention eliminates mutual exclusion or hold and wait conditions.",
            title="Deadlocks",
            section_title="Prevention",
            document_title="Operating Systems",
            filename="OS.pdf",
            page_number=12,
            chunk_index=0,
            total_chunks=3,
            created_at=datetime.now(timezone.utc),
        ),
        Chunk(
            chunk_id="chunk-os-2",
            document_id="doc-os",
            user_id="user-alice",
            course_id="cs-101",
            subject_id="os-1",
            content="CPU Scheduling uses Round Robin, Priority, and Shortest Job First algorithms.",
            title="Scheduling",
            section_title="Algorithms",
            document_title="Operating Systems",
            filename="OS.pdf",
            page_number=5,
            chunk_index=1,
            total_chunks=3,
            created_at=datetime.now(timezone.utc),
        ),
        Chunk(
            chunk_id="chunk-os-3",
            document_id="doc-os",
            user_id="user-alice",
            course_id="cs-101",
            subject_id="os-1",
            content="Virtual memory paging uses TLB and page tables for address translation.",
            title="Memory",
            section_title="Paging",
            document_title="Operating Systems",
            filename="OS.pdf",
            page_number=20,
            chunk_index=2,
            total_chunks=3,
            created_at=datetime.now(timezone.utc),
        ),
    ]

    vectors = embedding_service.embed_texts([c.content for c in chunks])
    search_service.index_chunks(chunks, vectors)

    # Search for deadlock
    res = search_knowledge(
        user_id="user-alice",
        query="Explain deadlock prevention",
        top_k=2,
    )

    results = res["results"]
    assert len(results) <= 2
    assert len(results) > 0

    top_result = results[0]
    assert top_result["chunk_id"] == "chunk-os-1"
    assert top_result["page_number"] == 12
    assert "Deadlock prevention" in top_result["content"]
    assert top_result["document_title"] == "Operating Systems"
    assert top_result["score"] > 0.0


def test_search_course_and_subject_filtering(search_service):
    embedding_service = EmbeddingService()

    chunks = [
        Chunk(
            chunk_id="c-cs101",
            document_id="doc-1",
            user_id="user-alice",
            course_id="cs-101",
            subject_id="os-1",
            content="Algorithms in operating systems.",
            document_title="OS",
            filename="os.pdf",
            page_number=1,
            chunk_index=0,
            total_chunks=1,
            created_at=datetime.now(timezone.utc),
        ),
        Chunk(
            chunk_id="c-ee201",
            document_id="doc-2",
            user_id="user-alice",
            course_id="ee-201",
            subject_id="signals-1",
            content="Digital signal processing algorithms.",
            document_title="DSP",
            filename="dsp.pdf",
            page_number=1,
            chunk_index=0,
            total_chunks=1,
            created_at=datetime.now(timezone.utc),
        ),
    ]
    vectors = embedding_service.embed_texts([c.content for c in chunks])
    search_service.index_chunks(chunks, vectors)

    # Search with course filter cs-101
    res_cs = search_knowledge(
        user_id="user-alice",
        query="algorithms",
        course_id="cs-101",
    )
    assert len(res_cs["results"]) == 1
    assert res_cs["results"][0]["course_id"] == "cs-101"

    # Search with course filter ee-201
    res_ee = search_knowledge(
        user_id="user-alice",
        query="algorithms",
        course_id="ee-201",
    )
    assert len(res_ee["results"]) == 1
    assert res_ee["results"][0]["course_id"] == "ee-201"
