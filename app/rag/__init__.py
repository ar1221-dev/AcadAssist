"""RAG module package for AcadAssist.

Provides retrieval-augmented generation pipelines, context construction,
retrievers, and AI provider interfaces for academic study assistance.
"""

from app.rag.context_builder import ContextBuilder
from app.rag.models import RetrievedChunk, SourceReference, StudyResponse
from app.rag.pipeline import RAGPipeline
from app.rag.provider import BaseAIProvider, MockAIProvider
from app.rag.retriever import BaseRetriever, MockRetriever

__all__ = [
    "BaseAIProvider",
    "BaseRetriever",
    "ContextBuilder",
    "MockAIProvider",
    "MockRetriever",
    "RAGPipeline",
    "RetrievedChunk",
    "SourceReference",
    "StudyResponse",
]
