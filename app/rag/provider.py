"""AI Provider interfaces and deterministic mock implementation."""

from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    """Abstract interface for AI/LLM providers."""

    @abstractmethod
    def generate_response(self, question: str, context: str) -> str:
        """Generate an answer given a user question and retrieved study context."""
        pass


class MockAIProvider(BaseAIProvider):
    """Deterministic local AI provider without external API calls."""

    INSUFFICIENT_MATERIAL_MESSAGE = (
        "I could not find sufficient study material to answer this question. "
        "Please refer to your course materials or upload relevant notes."
    )

    def generate_response(self, question: str, context: str) -> str:
        """Produce a deterministic answer grounded in the retrieved context."""
        if not context or not context.strip():
            return self.INSUFFICIENT_MATERIAL_MESSAGE

        # Extract textual passages from formatted context
        passages = [
            line.strip()
            for line in context.splitlines()
            if line.strip() and not line.strip().startswith("---")
        ]
        grounded_text = " ".join(passages)

        return (
            f"Based on your study materials, here is the relevant concept for '{question.strip()}':\n\n"
            f"{grounded_text}"
        )
