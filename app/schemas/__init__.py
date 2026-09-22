"""Schemas package exports."""

from app.schemas.chat import ActionItem, ChatRequest, ChatResponse, SourceItem
from app.schemas.search import ChunkResult, SearchKnowledgeRequest, SearchKnowledgeResponse
from app.schemas.tools import (
    CreateStudyPlanParams,
    GenerateQuizParams,
    GenerateWeeklyReportParams,
    GetPerformanceParams,
    GetProgressParams,
    GetTodayPlanParams,
    GetUpcomingExamsParams,
    GetWeakTopicsParams,
    SubmitQuizParams,
    SummarizeDocumentParams,
)

__all__ = [
    "ActionItem",
    "ChatRequest",
    "ChatResponse",
    "ChunkResult",
    "CreateStudyPlanParams",
    "GenerateQuizParams",
    "GenerateWeeklyReportParams",
    "GetPerformanceParams",
    "GetProgressParams",
    "GetTodayPlanParams",
    "GetUpcomingExamsParams",
    "GetWeakTopicsParams",
    "SearchKnowledgeRequest",
    "SearchKnowledgeResponse",
    "SourceItem",
    "SubmitQuizParams",
    "SummarizeDocumentParams",
]
