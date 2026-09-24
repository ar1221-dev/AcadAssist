"""Context builder for formulating structured prompts from retrieved chunks."""

from typing import List

from app.rag.models import RetrievedChunk


class ContextBuilder:
    """Formats retrieved chunks into a clean, structured context string."""

    def build_context(self, chunks: List[RetrievedChunk]) -> str:
        """Convert a list of RetrievedChunk objects into formatted context.

        Returns an empty string if chunks is empty.
        """
        if not chunks:
            return ""

        formatted_sections: List[str] = []
        for idx, chunk in enumerate(chunks, start=1):
            source_info = f"Source: {chunk.source}"
            if chunk.page is not None:
                source_info += f", Page: {chunk.page}"

            section = f"--- [Document Passage {idx}] ({source_info}) ---\n{chunk.content.strip()}"
            formatted_sections.append(section)

        return "\n\n".join(formatted_sections)
