"""Question history and exact duplicate detection for assessment module."""

import re
from typing import List, Set
from app.contracts.models import QuizQuestion


def normalize_question_text(text: str) -> str:
    """Normalize question text for deterministic exact duplicate detection.

    Converts to lowercase, removes leading/trailing whitespace, collapses
    internal whitespace, and strips standard punctuation. No hashing is used.

    Args:
        text: Raw question text.

    Returns:
        Normalized plain string representation.
    """
    if not text:
        return ""
    # Convert to lowercase
    normalized = text.lower().strip()
    # Replace all punctuation characters with space
    normalized = re.sub(r"[^\w\s]", "", normalized)
    # Collapse multiple spaces into a single space
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


class QuestionHistory:
    """Tracks seen questions to prevent exact duplicate repeats in quizzes."""

    def __init__(self) -> None:
        self.seen_ids: Set[str] = set()
        self.seen_texts: Set[str] = set()

    def is_duplicate(self, question: QuizQuestion) -> bool:
        """Check if a question has already been seen by ID or normalized text.

        Args:
            question: The QuizQuestion to check.

        Returns:
            True if previously seen, False if new.
        """
        if question.id and question.id in self.seen_ids:
            return True
        norm_text = normalize_question_text(question.text)
        if norm_text and norm_text in self.seen_texts:
            return True
        return False

    def record(self, question: QuizQuestion) -> None:
        """Record a question as seen.

        Args:
            question: The QuizQuestion to record.
        """
        if question.id:
            self.seen_ids.add(question.id)
        norm_text = normalize_question_text(question.text)
        if norm_text:
            self.seen_texts.add(norm_text)

    def record_many(self, questions: List[QuizQuestion]) -> None:
        """Record multiple questions as seen.

        Args:
            questions: List of QuizQuestion instances to record.
        """
        for q in questions:
            self.record(q)

    def filter_new_questions(self, questions: List[QuizQuestion]) -> List[QuizQuestion]:
        """Filter a list of questions, keeping only those that have not been seen.

        Args:
            questions: Candidate list of QuizQuestions.

        Returns:
            List of new, unseen QuizQuestions.
        """
        return [q for q in questions if not self.is_duplicate(q)]

    def reset(self) -> None:
        """Clear all question history records."""
        self.seen_ids.clear()
        self.seen_texts.clear()
