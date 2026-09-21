from pathlib import Path

from app.services.processors.base import (
    BaseProcessor,
    DocumentProcessingError,
    ExtractionResult,
)


class TXTProcessor(BaseProcessor):
    SUPPORTED_ENCODINGS = ["utf-8", "utf-8-sig", "utf-16", "latin-1", "cp1252"]

    def extract(self, file_path: Path) -> ExtractionResult:
        if not file_path.exists():
            raise DocumentProcessingError(f"Text file not found at {file_path}")

        raw_bytes = file_path.read_bytes()
        text_content: str | None = None
        used_encoding = "unknown"

        for enc in self.SUPPORTED_ENCODINGS:
            try:
                text_content = raw_bytes.decode(enc)
                used_encoding = enc
                break
            except (UnicodeDecodeError, LookupError):
                continue

        if text_content is None:
            text_content = raw_bytes.decode("latin-1", errors="replace")
            used_encoding = "latin-1 (fallback)"

        # Normalize carriage returns and clean extra whitespace
        normalized_text = text_content.replace("\r\n", "\n").replace("\r", "\n").strip()

        # Split into logical sections if delimiters exist (e.g., "---" or "===" or "# ")
        lines = normalized_text.split("\n")
        sections: list[dict[str, str]] = []
        current_label = "Section 1"
        current_chunk: list[str] = []
        sec_num = 1

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("---") and len(stripped) > 3 and stripped.endswith("---"):
                if current_chunk:
                    sections.append({
                        "label": current_label,
                        "content": "\n".join(current_chunk).strip(),
                    })
                    sec_num += 1
                    current_chunk = []
                current_label = stripped.strip("- ")
                current_chunk.append(current_label)
            elif stripped.startswith("# ") and len(current_chunk) > 5:
                if current_chunk:
                    sections.append({
                        "label": current_label,
                        "content": "\n".join(current_chunk).strip(),
                    })
                    sec_num += 1
                    current_chunk = []
                current_label = stripped.lstrip("# ").strip()
                current_chunk.append(stripped)
            else:
                current_chunk.append(line)

        if current_chunk or not sections:
            sections.append({
                "label": current_label,
                "content": "\n".join(current_chunk).strip(),
            })

        return ExtractionResult(
            sections=sections,
            page_count=None,
            slide_count=None,
            metadata={"format": "TXT", "encoding": used_encoding},
        )
