"""FastAPI router exposing AcadAssist backend tools for Microsoft Foundry OpenAPI integration."""

import logging
from typing import Any, Dict
from fastapi import APIRouter, HTTPException, status

from app.schemas.tools import (
    SearchKnowledgeParams,
    SummarizeDocumentParams,
    GenerateQuizParams,
    SubmitQuizParams,
    GetPerformanceParams,
    GetWeakTopicsParams,
    GetProgressParams,
    GetUpcomingExamsParams,
    CreateStudyPlanParams,
    GetTodayPlanParams,
    GenerateWeeklyReportParams,
)
from app.schemas.search import SearchKnowledgeResponse
from app.azure.adapters import ToolDispatcher

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tools", tags=["Tools"])

_dispatcher: ToolDispatcher | None = None


def get_dispatcher() -> ToolDispatcher:
    """Retrieve or initialize the ToolDispatcher instance."""
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = ToolDispatcher()
    return _dispatcher


@router.post(
    "/search_knowledge",
    response_model=SearchKnowledgeResponse,
    status_code=status.HTTP_200_OK,
    operation_id="search_knowledge",
    summary="Search student academic knowledge base",
    description="Search academic materials using hybrid retrieval. Requires user_id and query.",
)
def search_knowledge(params: SearchKnowledgeParams) -> SearchKnowledgeResponse:
    if not params.user_id or not params.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    if not params.query or not params.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'query' field must not be empty.",
        )
    dispatcher = get_dispatcher()
    return dispatcher.kb_adapter.search_knowledge(
        user_id=params.user_id.strip(),
        query=params.query.strip(),
        course_id=params.course_id.strip() if params.course_id else None,
        subject_id=params.subject_id.strip() if params.subject_id else None,
        top_k=params.top_k,
    )


@router.post(
    "/summarize_document",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    operation_id="summarize_document",
    summary="Summarize an academic document",
    description="Summarize a specific academic document or textbook chapter in the knowledge base.",
)
def summarize_document(params: SummarizeDocumentParams) -> Dict[str, Any]:
    if not params.user_id or not params.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    if not params.document_id or not params.document_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'document_id' field is mandatory.",
        )
    dispatcher = get_dispatcher()
    return dispatcher.kb_adapter.summarize_document(
        user_id=params.user_id.strip(),
        document_id=params.document_id.strip(),
        mode=params.mode.strip() if params.mode else "concise",
    )


@router.post(
    "/generate_quiz",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    operation_id="generate_quiz",
    summary="Generate an practice quiz",
    description="Generate practice quiz questions on a specified academic subject or topic.",
)
def generate_quiz(params: GenerateQuizParams) -> Dict[str, Any]:
    if not params.user_id or not params.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    dispatcher = get_dispatcher()
    return dispatcher.assessment_adapter.generate_quiz(
        user_id=params.user_id.strip(),
        subject_id=params.subject_id.strip() if params.subject_id else None,
        topic_ids=params.topic_ids,
        difficulty=params.difficulty.strip() if params.difficulty else "medium",
        count=params.count,
    )


@router.post(
    "/submit_quiz",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    operation_id="submit_quiz",
    summary="Submit student quiz answers",
    description="Submit answers for a previously generated quiz, calculate score, and record history.",
)
def submit_quiz(params: SubmitQuizParams) -> Dict[str, Any]:
    if not params.user_id or not params.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    if not params.quiz_id or not params.quiz_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'quiz_id' field is mandatory.",
        )
    dispatcher = get_dispatcher()
    try:
        return dispatcher.assessment_adapter.submit_quiz(
            user_id=params.user_id.strip(),
            quiz_id=params.quiz_id.strip(),
            answers=params.answers,
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc).strip("'"),
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc).strip("'"),
        )


@router.post(
    "/get_performance",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    operation_id="get_performance",
    summary="Retrieve historical student performance metrics",
    description="Retrieve historical assessment scores, quiz statistics, and performance trends.",
)
def get_performance(params: GetPerformanceParams) -> Dict[str, Any]:
    if not params.user_id or not params.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    dispatcher = get_dispatcher()
    return dispatcher.assessment_adapter.get_performance(
        user_id=params.user_id.strip(),
        subject_id=params.subject_id.strip() if params.subject_id else None,
    )


@router.post(
    "/get_weak_topics",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    operation_id="get_weak_topics",
    summary="Identify student weak topics",
    description="Identify topics where the student has struggled based on quiz and assessment history.",
)
def get_weak_topics(params: GetWeakTopicsParams) -> Dict[str, Any]:
    if not params.user_id or not params.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    dispatcher = get_dispatcher()
    return dispatcher.assessment_adapter.get_weak_topics(
        user_id=params.user_id.strip(),
        subject_id=params.subject_id.strip() if params.subject_id else None,
    )


@router.post(
    "/get_progress",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    operation_id="get_progress",
    summary="Retrieve course completion progress",
    description="Retrieve current course completion percentage, reading milestone progress, and study streaks.",
)
def get_progress(params: GetProgressParams) -> Dict[str, Any]:
    if not params.user_id or not params.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    dispatcher = get_dispatcher()
    return dispatcher.study_adapter.get_progress(
        user_id=params.user_id.strip(),
        course_id=params.course_id.strip() if params.course_id else None,
        subject_id=params.subject_id.strip() if params.subject_id else None,
    )


@router.post(
    "/get_upcoming_exams",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    operation_id="get_upcoming_exams",
    summary="Retrieve upcoming exams and deadlines",
    description="Retrieve scheduled exams, tests, and assignment deadlines.",
)
def get_upcoming_exams(params: GetUpcomingExamsParams) -> Dict[str, Any]:
    if not params.user_id or not params.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    dispatcher = get_dispatcher()
    return dispatcher.study_adapter.get_upcoming_exams(
        user_id=params.user_id.strip(),
    )


@router.post(
    "/create_study_plan",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    operation_id="create_study_plan",
    summary="Create an optimized study plan",
    description="Create an optimized daily study plan tailored to weak topics and available study hours.",
)
def create_study_plan(params: CreateStudyPlanParams) -> Dict[str, Any]:
    if not params.user_id or not params.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    dispatcher = get_dispatcher()
    raw_dict = params.model_dump()
    duration = raw_dict.get("duration_days") or raw_dict.get("days")
    return dispatcher.study_adapter.create_study_plan(
        user_id=params.user_id.strip(),
        start_date=params.start_date.strip() if params.start_date else None,
        end_date=params.end_date.strip() if params.end_date else None,
        duration_days=duration,
        current_date=raw_dict.get("current_date"),
    )


@router.post(
    "/get_today_plan",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    operation_id="get_today_plan",
    summary="Retrieve today's study schedule",
    description="Retrieve the student's scheduled study sessions and practice tasks for today.",
)
def get_today_plan(params: GetTodayPlanParams) -> Dict[str, Any]:
    if not params.user_id or not params.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    dispatcher = get_dispatcher()
    return dispatcher.study_adapter.get_today_plan(
        user_id=params.user_id.strip(),
    )


@router.post(
    "/generate_weekly_report",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    operation_id="generate_weekly_report",
    summary="Generate a weekly learning summary",
    description="Generate a weekly learning summary including hours studied, concepts mastered, and streak status.",
)
def generate_weekly_report(params: GenerateWeeklyReportParams) -> Dict[str, Any]:
    if not params.user_id or not params.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    if not params.week_start or not params.week_start.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'week_start' field is mandatory.",
        )
    if not params.week_end or not params.week_end.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'week_end' field is mandatory.",
        )
    dispatcher = get_dispatcher()
    return dispatcher.study_adapter.generate_weekly_report(
        user_id=params.user_id.strip(),
        week_start=params.week_start.strip(),
        week_end=params.week_end.strip(),
    )
