"""Shared data contracts package for AcadAssist."""

from app.contracts.models import (
    AgentResponse,
    Document,
    DocumentChunk,
    Mistake,
    Progress,
    Quiz,
    QuizAttempt,
    QuizQuestion,
    QuizResult,
    RetrievedChunk,
    SourceReference,
    StudyPlan,
    StudyResponse,
    StudyTask,
)

__all__ = [
    "QuizQuestion",
    "Quiz",
    "QuizAttempt",
    "QuizResult",
    "Mistake",
    "Progress",
    "StudyTask",
    "StudyPlan",
    "Document",
    "DocumentChunk",
    "RetrievedChunk",
    "SourceReference",
    "StudyResponse",
    "AgentResponse",
]
