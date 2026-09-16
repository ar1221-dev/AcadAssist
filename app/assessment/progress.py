"""Deterministic progress calculation and tracking for AcadAssist assessment."""

from typing import Dict, List, Optional
from app.contracts.models import Progress, Quiz, QuizResult


def calculate_progress(
    results: List[QuizResult],
    topic: str = "Overall",
) -> Progress:
    """Calculate aggregate progress metrics across a collection of quiz results.

    Args:
        results: List of QuizResult objects to aggregate.
        topic: Topic or category name for this progress record.

    Returns:
        A Progress instance summarizing total attempts, correct/incorrect, and accuracy.
    """
    if not results:
        return Progress(
            topic=topic,
            quizzes_attempted=0,
            questions_attempted=0,
            correct_count=0,
            incorrect_count=0,
            accuracy_percentage=0.0,
        )

    quizzes_attempted = len(results)
    questions_attempted = sum(r.total_questions for r in results)
    correct_count = sum(r.correct_count for r in results)
    incorrect_count = sum(r.incorrect_count for r in results)

    accuracy_percentage = (
        round((correct_count / questions_attempted) * 100.0, 2)
        if questions_attempted > 0
        else 0.0
    )

    return Progress(
        topic=topic,
        quizzes_attempted=quizzes_attempted,
        questions_attempted=questions_attempted,
        correct_count=correct_count,
        incorrect_count=incorrect_count,
        accuracy_percentage=accuracy_percentage,
    )


def calculate_topic_progress(
    results: List[QuizResult],
    quiz_map: Dict[str, Quiz],
) -> Dict[str, Progress]:
    """Calculate breakdown of progress metrics grouped by topic.

    Args:
        results: List of QuizResult objects.
        quiz_map: Dictionary mapping quiz_id to Quiz object to resolve topics.

    Returns:
        Dictionary mapping topic name to its corresponding Progress summary.
    """
    topic_results: Dict[str, List[QuizResult]] = {}

    for res in results:
        quiz = quiz_map.get(res.quiz_id)
        topic_name = quiz.topic if quiz and quiz.topic else "General"
        if topic_name not in topic_results:
            topic_results[topic_name] = []
        topic_results[topic_name].append(res)

    progress_by_topic: Dict[str, Progress] = {}
    for topic_name, res_list in topic_results.items():
        progress_by_topic[topic_name] = calculate_progress(res_list, topic=topic_name)

    return progress_by_topic
