from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ExtractionResult:
    sections: list[dict[str, str]] = field(default_factory=list)
    page_count: int | None = None
    slide_count: int | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def total_chars(self) -> int:
        return sum(len(s.get("content", "")) for s in self.sections)


class BaseProcessor(ABC):
    @abstractmethod
    def extract(self, file_path: Path) -> ExtractionResult:
        """
        Extract text, structure, and metadata from the document file.
        Raises DocumentProcessingError on failure.
        """
        pass


class DocumentProcessingError(Exception):
    def __init__(self, message: str, details: str | None = None):
        super().__init__(message)
        self.message = message
        self.details = details
