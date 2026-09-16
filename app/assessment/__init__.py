"""Assessment and quiz module for AcadAssist.

Provides deterministic quiz loading, evaluation, scoring, mistake tracking,
progress calculations, and exact duplicate prevention.
"""

from app.assessment.evaluator import (
    evaluate_quiz,
    is_answer_correct,
    normalize_answer,
)
from app.assessment.mistakes import (
    count_mistakes_by_topic,
    extract_mistakes,
    filter_mistakes_by_topic,
)
from app.assessment.mock_data import (
    MOCK_QUESTIONS,
    get_mock_questions,
    load_mock_quiz,
)
from app.assessment.progress import (
    calculate_progress,
    calculate_topic_progress,
)
from app.assessment.question_history import (
    QuestionHistory,
    normalize_question_text,
)

__all__ = [
    "MOCK_QUESTIONS",
    "get_mock_questions",
    "load_mock_quiz",
    "evaluate_quiz",
    "is_answer_correct",
    "normalize_answer",
    "extract_mistakes",
    "filter_mistakes_by_topic",
    "count_mistakes_by_topic",
    "calculate_progress",
    "calculate_topic_progress",
    "QuestionHistory",
    "normalize_question_text",
]
