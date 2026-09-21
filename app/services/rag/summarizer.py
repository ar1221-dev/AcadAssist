"""Document summarization contract supporting multiple academic study modes."""

from typing import Any
from sqlalchemy.orm import Session

from app.models.document import Chunk, Document


VALID_SUMMARY_MODES = {"quick", "detailed", "exam", "revision"}


def summarize_document(
    document_id: str,
    user_id: str,
    mode: str = "quick",
    db: Session | None = None,
) -> dict[str, Any]:
    """Retrieve document content, enforce user ownership, and prepare context for summarization.

    Supported modes:
        - quick: High-level overview and main concepts (concise).
        - detailed: Comprehensive breakdown section-by-section.
        - exam: High-yield concepts, definitions, and key exam questions/topics.
        - revision: Bullet-point formula/keyword quick reference.

    Returns:
        Structured context and summary payload integration-ready for downstream AI.
    """
    if mode not in VALID_SUMMARY_MODES:
        raise ValueError(f"Invalid mode '{mode}'. Supported modes: {', '.join(sorted(VALID_SUMMARY_MODES))}")

    if db is None:
        raise ValueError("Database session is required to retrieve document.")

    # 1. Ownership enforcement
    doc = db.query(Document).filter(Document.document_id == document_id).first()
    if not doc:
        raise FileNotFoundError(f"Document '{document_id}' not found.")
    if doc.user_id != user_id:
        raise PermissionError("Access denied: You do not own this document.")

    # 2. Retrieve chunks
    chunks = (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id, Chunk.user_id == user_id)
        .order_by(Chunk.chunk_index)
        .all()
    )

    if not chunks:
        # Document not yet processed or empty
        return {
            "document_id": document_id,
            "title": doc.title,
            "filename": doc.filename,
            "mode": mode,
            "status": doc.status,
            "summary": f"Document '{doc.title}' is currently {doc.status}. Please process the document first.",
            "sections": [],
            "key_points": [],
        }

    # Extract distinct sections and key excerpts
    sections: list[dict[str, Any]] = []
    seen_sections = set()
    key_points: list[str] = []

    for c in chunks:
        sec_name = c.section_title or f"Page {c.page_number}" if c.page_number else f"Chunk {c.chunk_index + 1}"
        if sec_name not in seen_sections:
            seen_sections.add(sec_name)
            first_sentence = c.content.split(". ")[0].strip()
            sections.append({
                "section": sec_name,
                "page": c.page_number,
                "slide": c.slide_number,
                "overview": first_sentence[:200],
            })

    # Prepare structured summary text based on mode
    if mode == "quick":
        summary_text = (
            f"Overview of '{doc.title}': Covers {len(sections)} main sections across "
            f"{len(chunks)} chunks. Main themes include {', '.join([s['section'] for s in sections[:4]])}."
        )
    elif mode == "exam":
        summary_text = (
            f"Exam High-Yield Review for '{doc.title}': Focus on key concepts in "
            f"{', '.join([s['section'] for s in sections[:5]])}. Pay attention to core definitions and mechanisms."
        )
    elif mode == "revision":
        summary_text = (
            f"Quick Revision Sheet for '{doc.title}': Key points and definitions organized by section."
        )
    else:  # detailed
        summary_text = (
            f"Detailed Analysis of '{doc.title}': Full breakdown of {len(chunks)} chunks across "
            f"{len(sections)} sections, preserving page/slide boundaries."
        )

    return {
        "document_id": document_id,
        "title": doc.title,
        "filename": doc.filename,
        "mode": mode,
        "status": doc.status,
        "total_chunks": len(chunks),
        "sections": sections,
        "summary": summary_text,
    }
