"""Retriever interfaces and mock implementation for academic study material."""

from abc import ABC, abstractmethod
import re
from typing import List, Optional, Set

from app.rag.models import RetrievedChunk


class BaseRetriever(ABC):
    """Abstract base retriever interface."""

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 3) -> List[RetrievedChunk]:
        """Retrieve relevant document chunks given a query string."""
        pass


class MockRetriever(BaseRetriever):
    """Mock retriever searching an in-memory academic sample corpus using keyword/token overlap."""

    DEFAULT_CORPUS: List[RetrievedChunk] = [
        RetrievedChunk(
            chunk_id="chunk_ml_01",
            content=(
                "Supervised learning is a machine learning paradigm where models are trained "
                "on labeled datasets containing both input features and corresponding ground truth targets. "
                "Common algorithms include linear regression, logistic regression, support vector machines, "
                "and decision trees."
            ),
            source="Introduction to Machine Learning.pdf",
            page=12,
            metadata={"topic": "Machine Learning", "subtopic": "Supervised Learning"},
        ),
        RetrievedChunk(
            chunk_id="chunk_ml_02",
            content=(
                "Unsupervised learning deals with unlabeled data where the goal is to discover underlying "
                "patterns, groupings, or representations. Key methods include clustering (e.g., K-Means, DBSCAN) "
                "and dimensionality reduction (e.g., Principal Component Analysis)."
            ),
            source="Introduction to Machine Learning.pdf",
            page=25,
            metadata={"topic": "Machine Learning", "subtopic": "Unsupervised Learning"},
        ),
        RetrievedChunk(
            chunk_id="chunk_ml_03",
            content=(
                "Overfitting occurs when a machine learning model learns the training data too well, "
                "capturing noise and specific idiosyncrasies rather than generalizing to unseen data. "
                "Techniques to mitigate overfitting include regularization (L1/L2), cross-validation, "
                "pruning, and dropout."
            ),
            source="Introduction to Machine Learning.pdf",
            page=48,
            metadata={"topic": "Machine Learning", "subtopic": "Model Evaluation"},
        ),
        RetrievedChunk(
            chunk_id="chunk_db_01",
            content=(
                "Database normalization is the process of structuring a relational database to minimize "
                "redundancy and avoid anomalies during insert, update, and delete operations. Normal forms "
                "include 1NF, 2NF, 3NF, and Boyce-Codd Normal Form (BCNF)."
            ),
            source="Database Systems Concepts.pdf",
            page=104,
            metadata={"topic": "Databases", "subtopic": "Normalization"},
        ),
        RetrievedChunk(
            chunk_id="chunk_os_01",
            content=(
                "An operating system process is an instance of a computer program being executed. "
                "Each process contains program code, current activity, memory segments (stack, heap, data), "
                "and associated system resources managed by the kernel scheduler."
            ),
            source="Modern Operating Systems.pdf",
            page=34,
            metadata={"topic": "Operating Systems", "subtopic": "Processes"},
        ),
    ]

    STOP_WORDS = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
        "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
        "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down",
        "during", "each", "explain", "few", "for", "from", "further", "had", "has",
        "have", "having", "he", "her", "here", "hers", "herself", "him", "himself",
        "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just",
        "me", "more", "most", "my", "myself", "no", "nor", "not", "of", "off", "on",
        "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over",
        "own", "same", "she", "should", "so", "some", "such", "than", "that", "the",
        "their", "theirs", "them", "themselves", "then", "there", "these", "they",
        "this", "those", "through", "to", "too", "under", "until", "up", "very",
        "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom",
        "why", "with", "would", "you", "your", "yours", "yourself", "yourselves",
    }

    def __init__(self, corpus: Optional[List[RetrievedChunk]] = None) -> None:
        self._corpus = list(corpus) if corpus is not None else list(self.DEFAULT_CORPUS)

    def _tokenize(self, text: str, filter_stopwords: bool = True) -> Set[str]:
        """Tokenize text into lowercase alphanumeric tokens."""
        tokens = set(re.findall(r"\b[a-zA-Z0-9_]+\b", text.lower()))
        if filter_stopwords:
            content_tokens = {t for t in tokens if t not in self.STOP_WORDS}
            return content_tokens if content_tokens else tokens
        return tokens

    def retrieve(self, query: str, top_k: int = 3) -> List[RetrievedChunk]:
        """Retrieve top_k chunks based on token overlap between query and chunk content/source."""
        query_tokens = self._tokenize(query, filter_stopwords=True)
        if not query_tokens:
            return []

        scored_chunks: List[RetrievedChunk] = []
        for chunk in self._corpus:
            target_text = f"{chunk.content} {chunk.source}"
            target_tokens = self._tokenize(target_text, filter_stopwords=False)
            overlap = query_tokens.intersection(target_tokens)
            if overlap:
                score = len(overlap) / len(query_tokens)
                scored_chunk = RetrievedChunk(
                    chunk_id=chunk.chunk_id,
                    content=chunk.content,
                    source=chunk.source,
                    page=chunk.page,
                    score=round(score, 4),
                    metadata=dict(chunk.metadata),
                )
                scored_chunks.append(scored_chunk)

        # Sort descending by score, then ascending by chunk_id for determinism
        scored_chunks.sort(key=lambda c: (-c.score, c.chunk_id))
        return scored_chunks[:top_k]
