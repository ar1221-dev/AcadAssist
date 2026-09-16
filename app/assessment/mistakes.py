"""Mistake representation and review helpers for the assessment module."""

from typing import Dict, List
from app.assessment.evaluator import evaluate_quiz
from app.contracts.models import Mistake, Quiz, QuizAttempt


def extract_mistakes(quiz: Quiz, attempt: QuizAttempt) -> List[Mistake]:
    """Extract all mistake records from a quiz attempt.

    Args:
        quiz: The quiz definition.
        attempt: The student's attempt.

    Returns:
        List of Mistake objects for all incorrectly answered questions.
    """
    result = evaluate_quiz(quiz, attempt)
    return result.mistakes


def filter_mistakes_by_topic(mistakes: List[Mistake], topic: str) -> List[Mistake]:
    """Filter mistake records by topic name (case-insensitive substring match).

    Args:
        mistakes: List of Mistake objects.
        topic: Topic string to filter by.

    Returns:
        Filtered list of Mistake objects.
    """
    if not topic:
        return list(mistakes)
    target = topic.lower()
    return [m for m in mistakes if target in m.topic.lower()]


def count_mistakes_by_topic(mistakes: List[Mistake]) -> Dict[str, int]:
    """Count number of mistakes per topic for weakness analysis.

    Args:
        mistakes: List of Mistake objects.

    Returns:
        Dictionary mapping topic name to count of mistakes.
    """
    counts: Dict[str, int] = {}
    for m in mistakes:
        topic_name = m.topic or "Uncategorized"
        counts[topic_name] = counts.get(topic_name, 0) + 1
    return counts
