"""Deterministic quiz evaluator for AcadAssist assessment module."""

import re
from typing import Dict, List, Optional
from app.contracts.models import Mistake, Quiz, QuizAttempt, QuizQuestion, QuizResult


def normalize_answer(answer: Optional[str]) -> str:
    """Normalize a quiz answer string for reliable deterministic comparison.

    Strips leading/trailing whitespace, converts to uppercase, and extracts
    the option key if formatted like 'B. Queue' or '(B)'.

    Args:
        answer: Raw answer string from student or model.

    Returns:
        Normalized answer string (e.g., 'B').
    """
    if not answer:
        return ""
    cleaned = answer.strip().upper()
    # Match patterns like 'B.', 'B)', '(B)', or simply 'B'
    match = re.match(r"^\(?([A-D])[\.\)]?.*$", cleaned)
    if match:
        return match.group(1)
    return cleaned


def is_answer_correct(student_answer: str, correct_answer: str) -> bool:
    """Check if a student's answer matches the correct answer.

    Args:
        student_answer: Answer provided by the student.
        correct_answer: Canonical correct answer.

    Returns:
        True if normalized answers match, False otherwise.
    """
    norm_student = normalize_answer(student_answer)
    norm_correct = normalize_answer(correct_answer)
    return bool(norm_student and norm_student == norm_correct)


def evaluate_quiz(quiz: Quiz, attempt: QuizAttempt) -> QuizResult:
    """Deterministically evaluate a student's quiz attempt.

    Compares submitted answers against correct answers for all questions
    in the quiz, calculates scores and percentages, and logs all mistakes.

    Args:
        quiz: The Quiz definition containing questions and correct answers.
        attempt: The student's QuizAttempt containing submitted answers.

    Returns:
        A QuizResult with total questions, correct/incorrect counts,
        percentage score, and mistake records.
    """
    total_questions = len(quiz.questions)
    if total_questions == 0:
        return QuizResult(
            quiz_id=quiz.id,
            attempt_id=attempt.id,
            total_questions=0,
            correct_count=0,
            incorrect_count=0,
            score=0.0,
            percentage=0.0,
            mistakes=[],
        )

    correct_count = 0
    mistakes: List[Mistake] = []
    answers: Dict[str, str] = attempt.submitted_answers or {}

    for question in quiz.questions:
        student_ans = answers.get(question.id, "")
        if is_answer_correct(student_ans, question.correct_answer):
            correct_count += 1
        else:
            mistakes.append(
                Mistake(
                    question_id=question.id,
                    question_text=question.text,
                    student_answer=student_ans if student_ans else "[No Answer]",
                    correct_answer=question.correct_answer,
                    explanation=question.explanation,
                    topic=question.topic,
                )
            )

    incorrect_count = total_questions - correct_count
    score = float(correct_count)
    percentage = round((correct_count / total_questions) * 100.0, 2)

    return QuizResult(
        quiz_id=quiz.id,
        attempt_id=attempt.id,
        total_questions=total_questions,
        correct_count=correct_count,
        incorrect_count=incorrect_count,
        score=score,
        percentage=percentage,
        mistakes=mistakes,
    )
