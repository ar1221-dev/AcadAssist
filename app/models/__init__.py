"""Models package exposing all entities for AcadAssist."""

from app.models.academic import *  # fallback if named academic
from app.models.shared import Course, Exam, QuizAttempt, Subject, Topic, TopicMastery, User
from app.models.study_plan import StudyPlan, StudyTask
from app.models.weekly_report import WeeklyReport

__all__ = [
    "User",
    "Course",
    "Subject",
    "Topic",
    "Exam",
    "TopicMastery",
    "QuizAttempt",
    "StudyPlan",
    "StudyTask",
    "WeeklyReport",
]
