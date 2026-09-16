"""RAG Pipeline coordinating retrieval, context construction, answer generation, and citations."""

from typing import List, Optional, Set, Tuple

from app.rag.context_builder import ContextBuilder
from app.rag.models import RetrievedChunk, SourceReference, StudyResponse
from app.rag.provider import BaseAIProvider, MockAIProvider
from app.rag.retriever import BaseRetriever, MockRetriever


class RAGPipeline:
    """Orchestrates the end-to-end RAG workflow for academic study assistance."""

    def __init__(
        self,
        retriever: BaseRetriever,
        context_builder: ContextBuilder,
        ai_provider: BaseAIProvider,
    ) -> None:
        self.retriever = retriever
        self.context_builder = context_builder
        self.ai_provider = ai_provider

    @classmethod
    def create_mock_pipeline(
        cls, corpus: Optional[List[RetrievedChunk]] = None
    ) -> "RAGPipeline":
        """Factory method to construct a mock RAG pipeline for local testing and development."""
        retriever = MockRetriever(corpus=corpus)
        context_builder = ContextBuilder()
        ai_provider = MockAIProvider()
        return cls(
            retriever=retriever,
            context_builder=context_builder,
            ai_provider=ai_provider,
        )

    def _create_source_references(
        self, chunks: List[RetrievedChunk]
    ) -> List[SourceReference]:
        """Map retrieved chunks into SourceReference citation objects."""
        sources: List[SourceReference] = []
        seen: Set[Tuple[str, Optional[int], Optional[str]]] = set()

        for chunk in chunks:
            key = (chunk.source, chunk.page, chunk.chunk_id)
            if key not in seen:
                seen.add(key)
                snippet = (
                    chunk.content[:100] + "..."
                    if len(chunk.content) > 100
                    else chunk.content
                )
                sources.append(
                    SourceReference(
                        source=chunk.source,
                        page=chunk.page,
                        chunk_id=chunk.chunk_id,
                        snippet=snippet,
                    )
                )
        return sources

    def run(self, question: str, top_k: int = 3) -> StudyResponse:
        """Execute the end-to-end RAG pipeline for a given academic question.

        Args:
            question: The academic question asked by the student.
            top_k: Maximum number of relevant chunks to retrieve.

        Returns:
            StudyResponse containing the generated answer, citations, and metadata.
        """
        # 1. Retrieve relevant chunks
        chunks = self.retriever.retrieve(query=question, top_k=top_k)

        # 2. Build structured context
        context = self.context_builder.build_context(chunks)

        # 3. Generate answer via AI provider
        answer = self.ai_provider.generate_response(question=question, context=context)

        # 4. Extract source references
        sources = self._create_source_references(chunks) if chunks else []

        return StudyResponse(
            question=question,
            answer=answer,
            sources=sources,
            context_used=context,
            confidence=1.0 if chunks else 0.0,
        )
