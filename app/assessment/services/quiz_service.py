"""High-level quiz orchestration service for Person 3 Assessment Subsystem.

Implements core service contracts for quiz generation, submission, performance analytics,
weak-topic detection, and exam retrieval, callable by FastAPI routes and Foundry Agent tools.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.assessment.models import Quiz, Question, generate_uuid, utc_now
from app.assessment.schemas import (
    QuizCreateRequest,
    QuizResponse,
    QuestionOut,
    SubmittedAnswer,
    QuizSubmissionResponse,
    PerformanceMetricsResponse,
    WeakTopicsResponse,
    ExamResponse,
)
from app.assessment.exceptions import QuizNotFoundError, QuizAccessDeniedError
from app.assessment.services.question_generator import (
    BaseQuestionGenerator,
    DeterministicQuestionGenerator,
)
from app.assessment.services.no_repeat_service import NoRepeatService
from app.assessment.services.adaptive_difficulty_service import AdaptiveDifficultyService
from app.assessment.services.scoring_service import ScoringService
from app.assessment.services.performance_service import PerformanceService
from app.assessment.services.exam_service import ExamService


class QuizService:
    """Core Assessment orchestrator coordinating all assessment sub-services."""

    def __init__(self, question_generator: Optional[BaseQuestionGenerator] = None):
        self.question_generator = question_generator or DeterministicQuestionGenerator()

    def generate_quiz(
        self,
        db: Session,
        user_id: str,
        subject_id: str,
        topic_ids: Optional[List[str]] = None,
        difficulty: Optional[str] = None,
        count: int = 10,
        course_id: Optional[str] = None,
        title: Optional[str] = None,
    ) -> QuizResponse:
        """Generate an adaptive, non-repeating quiz tailored for a student.

        Args:
            db: Database session
            user_id: Target student ID
            subject_id: Academic subject
            topic_ids: Optional specific topics within subject
            difficulty: Optional explicit difficulty ('easy', 'medium', 'hard')
            count: Number of questions (default 10)
            course_id: Optional course ID
            title: Optional custom quiz title

        Returns:
            QuizResponse with generated questions
        """
        # 1. Resolve adaptive difficulty if not explicitly forced
        resolved_difficulty = AdaptiveDifficultyService.get_recommended_difficulty(
            db=db,
            user_id=user_id,
            subject_id=subject_id,
            explicit_difficulty=difficulty,
        )

        # 2. Generate candidate questions via modular generator
        candidates = self.question_generator.generate_candidate_questions(
            subject_id=subject_id,
            topic_ids=topic_ids,
            difficulty=resolved_difficulty,
            count=count,
        )

        # 3. Apply deterministic per-user no-repeat filter
        primary_topic = topic_ids[0] if topic_ids else subject_id
        selected_candidates = NoRepeatService.filter_candidate_questions(
            db=db,
            user_id=user_id,
            candidates=candidates,
            count=count,
            topic=primary_topic,
        )

        # 4. Create Quiz entity
        quiz_id = generate_uuid()
        quiz_title = title or f"{subject_id.replace('_', ' ').title()} Quiz ({resolved_difficulty.capitalize()})"

        quiz = Quiz(
            quiz_id=quiz_id,
            user_id=user_id,
            course_id=course_id,
            subject_id=subject_id,
            title=quiz_title,
            difficulty=resolved_difficulty,
            question_count=len(selected_candidates),
            created_at=utc_now(),
        )
        db.add(quiz)
        db.flush()

        # 5. Create Question entities
        questions_out: List[QuestionOut] = []
        for cand in selected_candidates:
            q_id = cand.get("question_id") or generate_uuid()
            question = Question(
                question_id=q_id,
                quiz_id=quiz_id,
                subject_id=cand.get("subject_id", subject_id),
                topic_id=cand.get("topic_id", primary_topic),
                question_text=cand["question_text"],
                question_type=cand.get("question_type", "multiple_choice"),
                difficulty=cand.get("difficulty", resolved_difficulty),
                options=cand["options"],
                correct_answer=cand["correct_answer"],
                explanation=cand.get("explanation"),
                source_chunk_id=cand.get("source_chunk_id"),
            )
            db.add(question)
            questions_out.append(
                QuestionOut(
                    question_id=q_id,
                    quiz_id=quiz_id,
                    subject_id=question.subject_id,
                    topic_id=question.topic_id,
                    question_text=question.question_text,
                    question_type=question.question_type,
                    difficulty=question.difficulty,
                    options=question.options,
                    explanation=question.explanation,
                    source_chunk_id=question.source_chunk_id,
                )
            )

        db.commit()
        db.refresh(quiz)

        return QuizResponse(
            quiz_id=quiz.quiz_id,
            user_id=quiz.user_id,
            course_id=quiz.course_id,
            subject_id=quiz.subject_id,
            title=quiz.title,
            difficulty=quiz.difficulty,
            question_count=quiz.question_count,
            created_at=quiz.created_at,
            questions=questions_out,
        )

    def get_quiz_by_id(self, db: Session, user_id: str, quiz_id: str) -> QuizResponse:
        """Retrieve an existing quiz enforcing user ownership."""
        quiz = db.execute(select(Quiz).where(Quiz.quiz_id == quiz_id)).scalar_one_or_none()
        if not quiz:
            raise QuizNotFoundError(quiz_id)

        if quiz.user_id != user_id:
            raise QuizAccessDeniedError(quiz_id=quiz_id, user_id=user_id)

        questions_out = [
            QuestionOut(
                question_id=q.question_id,
                quiz_id=q.quiz_id,
                subject_id=q.subject_id,
                topic_id=q.topic_id,
                question_text=q.question_text,
                question_type=q.question_type,
                difficulty=q.difficulty,
                options=q.options,
                explanation=q.explanation,
                source_chunk_id=q.source_chunk_id,
            )
            for q in quiz.questions
        ]

        return QuizResponse(
            quiz_id=quiz.quiz_id,
            user_id=quiz.user_id,
            course_id=quiz.course_id,
            subject_id=quiz.subject_id,
            title=quiz.title,
            difficulty=quiz.difficulty,
            question_count=quiz.question_count,
            created_at=quiz.created_at,
            questions=questions_out,
        )

    def submit_quiz(
        self,
        db: Session,
        user_id: str,
        quiz_id: str,
        answers: List[SubmittedAnswer],
    ) -> QuizSubmissionResponse:
        """Evaluate submitted answers and record evaluation."""
        return ScoringService.evaluate_and_submit_quiz(
            db=db,
            user_id=user_id,
            quiz_id=quiz_id,
            submitted_answers=answers,
        )

    def get_performance(
        self,
        db: Session,
        user_id: str,
        subject_id: Optional[str] = None,
    ) -> PerformanceMetricsResponse:
        """Retrieve student performance metrics."""
        return PerformanceService.get_performance_metrics(
            db=db,
            user_id=user_id,
            subject_id=subject_id,
        )

    def get_weak_topics(
        self,
        db: Session,
        user_id: str,
        subject_id: Optional[str] = None,
    ) -> WeakTopicsResponse:
        """Retrieve student weak topics."""
        return PerformanceService.get_weak_topics(
            db=db,
            user_id=user_id,
            subject_id=subject_id,
        )

    def get_upcoming_exams(
        self,
        db: Session,
        user_id: str,
        subject_id: Optional[str] = None,
    ) -> List[ExamResponse]:
        """Retrieve student upcoming exams."""
        return ExamService.get_upcoming_exams(
            db=db,
            user_id=user_id,
            subject_id=subject_id,
        )


# Global singleton instance for easy import across Agent tools and routers
quiz_service = QuizService()
