from pathlib import Path
from app.services.processors.base import (
    BaseProcessor,
    DocumentProcessingError,
    ExtractionResult,
)
from app.services.processors.docx import DOCXProcessor
from app.services.processors.pdf import PDFProcessor
from app.services.processors.pptx import PPTProcessor
from app.services.processors.txt import TXTProcessor

_PROCESSORS: dict[str, BaseProcessor] = {
    "pdf": PDFProcessor(),
    "pptx": PPTProcessor(),
    "ppt": PPTProcessor(),
    "docx": DOCXProcessor(),
    "doc": DOCXProcessor(),
    "txt": TXTProcessor(),
}


def get_processor_for_extension(ext: str) -> BaseProcessor:
    clean_ext = ext.lstrip(".").lower()
    processor = _PROCESSORS.get(clean_ext)
    if not processor:
        raise DocumentProcessingError(f"No processor registered for extension '.{clean_ext}'")
    return processor


__all__ = [
    "BaseProcessor",
    "ExtractionResult",
    "DocumentProcessingError",
    "PDFProcessor",
    "PPTProcessor",
    "DOCXProcessor",
    "TXTProcessor",
    "get_processor_for_extension",
]
