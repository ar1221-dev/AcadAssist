from pathlib import Path
from pypdf import PdfReader
from pypdf.errors import PyPdfError

from app.services.processors.base import (
    BaseProcessor,
    DocumentProcessingError,
    ExtractionResult,
)


class PDFProcessor(BaseProcessor):
    def extract(self, file_path: Path) -> ExtractionResult:
        if not file_path.exists():
            raise DocumentProcessingError(f"PDF file not found at {file_path}")

        try:
            reader = PdfReader(str(file_path))
            if reader.is_encrypted:
                try:
                    # Attempt empty password decrypt
                    reader.decrypt("")
                except Exception:
                    raise DocumentProcessingError("PDF is encrypted with an unsupported password.")

            page_count = len(reader.pages)
            sections: list[dict[str, str]] = []

            for idx, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text() or ""
                sections.append({
                    "label": f"Page {idx}",
                    "content": page_text.strip(),
                })

            doc_meta: dict[str, str] = {}
            if reader.metadata:
                for k, v in reader.metadata.items():
                    if v and isinstance(v, str):
                        clean_key = k.lstrip("/")
                        doc_meta[clean_key] = v

            return ExtractionResult(
                sections=sections,
                page_count=page_count,
                slide_count=None,
                metadata=doc_meta,
            )
        except DocumentProcessingError:
            raise
        except PyPdfError as e:
            raise DocumentProcessingError(f"Corrupted or invalid PDF file: {str(e)}", details=str(e))
        except Exception as e:
            raise DocumentProcessingError(f"Failed to process PDF: {str(e)}", details=str(e))
