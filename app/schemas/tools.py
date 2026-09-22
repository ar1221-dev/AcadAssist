"""Shared contract schemas for all 11 AcadAssist Agent tools.

Defines the parameter and response structures for tools invoked by the ONE AcadAssist Agent.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class SearchKnowledgeParams(BaseModel):
    user_id: str
    query: str
    course_id: Optional[str] = None
    subject_id: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=50)


class SummarizeDocumentParams(BaseModel):
    user_id: str
    document_id: str
    mode: str = Field(..., description="Summary mode (e.g. concise, detailed, bullet_points)")


class GenerateQuizParams(BaseModel):
    user_id: str
    subject_id: Optional[str] = None
    topic_ids: Union[List[str], Any] = Field(default_factory=list)
    difficulty: str = Field(..., description="Quiz difficulty (easy, medium, hard)")
    count: int = Field(default=5, ge=1, le=20, description="Number of questions")


class SubmitQuizParams(BaseModel):
    user_id: str
    quiz_id: str
    answers: Union[List[Any], Dict[str, Any], Any] = Field(..., description="Student's chosen answers")


class GetPerformanceParams(BaseModel):
    user_id: str
    subject_id: Optional[str] = None


class GetWeakTopicsParams(BaseModel):
    user_id: str
    subject_id: Optional[str] = None


class GetProgressParams(BaseModel):
    user_id: str
    course_id: Optional[str] = None
    subject_id: Optional[str] = None


class GetUpcomingExamsParams(BaseModel):
    user_id: str


class CreateStudyPlanParams(BaseModel):
    user_id: str
    start_date: Optional[str] = Field(default=None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(default=None, description="End date (YYYY-MM-DD)")
    duration_days: Optional[Union[int, str]] = Field(default=None, description="Plan duration in days (e.g. 7)")
    current_date: Optional[str] = Field(default=None, description="Optional current date reference (YYYY-MM-DD)")

    model_config = {"extra": "allow"}


class GetTodayPlanParams(BaseModel):
    user_id: str


class GenerateWeeklyReportParams(BaseModel):
    user_id: str
    week_start: str = Field(..., description="Week start date (YYYY-MM-DD)")
    week_end: str = Field(..., description="Week end date (YYYY-MM-DD)")
