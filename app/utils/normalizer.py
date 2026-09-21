from datetime import datetime, timezone


def build_rag_document(
    material_id: str,
    title: str,
    subject: str,
    course: str | None,
    file_type: str,
    sections: list[dict[str, str]],
    extra_metadata: dict[str, str] | None = None,
) -> str:
    """
    Produce a deterministic, clean, human- and machine-readable text representation
    specifically structured for downstream chunking, embedding, and vector storage (Person 4 RAG).
    
    sections: list of dicts with {"label": "Page 1" / "Slide 2" / "Section 1", "content": "..."}
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    lines: list[str] = [
        "=== ACADASSIST KNOWLEDGE BASE METADATA ===",
        f"Material ID: {material_id}",
        f"Title: {title}",
        f"Subject: {subject}",
        f"Course: {course or 'N/A'}",
        f"File Type: {file_type.upper()}",
        f"Normalized At: {now_iso}",
    ]

    if extra_metadata:
        for k, v in extra_metadata.items():
            lines.append(f"{k}: {v}")

    lines.append("=== DOCUMENT CONTENT ===")
    lines.append("")

    for sec in sections:
        label = sec.get("label", "Section").strip()
        text = sec.get("content", "").strip()
        lines.append(f"--- {label} ---")
        if text:
            lines.append(text)
        else:
            lines.append("[Empty Section]")
        lines.append("")

    return "\n".join(lines).strip()
