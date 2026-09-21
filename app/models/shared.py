"""Shared AcadAssist models and Person 3 integration contracts.

These entities map directly to the single shared application database tables.
Person 4 consumes these tables (TopicMastery, QuizAttempt, Exam, Topic, Course, Subject, User)
as read/integration mappings, using extend_existing to guarantee no duplicate tables are created.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Date, DateTime, Float, Integer, String, Text

from app.database.base import Base


def generate_uuid() -> str:
    """Generate a UUID4 string."""
    return str(uuid.uuid4())


class User(Base):
    """User entity in shared database."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    user_id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class Course(Base):
    """Academic Course entity in shared database."""

    __tablename__ = "courses"
    __table_args__ = {"extend_existing": True}

    course_id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    code = Column(String(32), nullable=True)


class Subject(Base):
    """Academic Subject entity within a Course in shared database."""

    __tablename__ = "subjects"
    __table_args__ = {"extend_existing": True}

    subject_id = Column(String(64), primary_key=True)
    course_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)


class Topic(Base):
    """Topic entity within a Subject in shared database."""

    __tablename__ = "topics"
    __table_args__ = {"extend_existing": True}

    topic_id = Column(String(64), primary_key=True)
    subject_id = Column(String(64), nullable=False, index=True)
    course_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    difficulty = Column(String(32), nullable=False, default="medium")  # easy, medium, hard
    estimated_minutes = Column(Integer, nullable=False, default=60)


class Exam(Base):
    """Exam entity owned by Person 3 / shared database."""

    __tablename__ = "exams"
    __table_args__ = {"extend_existing": True}

    exam_id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(64), nullable=False, index=True)
    course_id = Column(String(64), nullable=False, index=True)
    subject_id = Column(String(64), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    exam_date = Column(Date, nullable=False, index=True)
    target_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class TopicMastery(Base):
    """Authoritative topic mastery records produced by Person 3."""

    __tablename__ = "topic_mastery"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(64), nullable=False, index=True)
    topic_id = Column(String(64), nullable=False, index=True)
    mastery_percentage = Column(Float, nullable=False, default=0.0)
    quizzes_attempted = Column(Integer, nullable=False, default=0)
    quizzes_passed = Column(Integer, nullable=False, default=0)
    is_weak = Column(Boolean, nullable=False, default=False)
    is_completed = Column(Boolean, nullable=False, default=False)
    last_assessed_at = Column(DateTime, nullable=True)


class QuizAttempt(Base):
    """Authoritative quiz attempt scores produced by Person 3."""

    __tablename__ = "quiz_attempts"
    __table_args__ = {"extend_existing": True}

    attempt_id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(64), nullable=False, index=True)
    topic_id = Column(String(64), nullable=False, index=True)
    score_percentage = Column(Float, nullable=False)
    total_questions = Column(Integer, nullable=False, default=5)
    correct_answers = Column(Integer, nullable=False, default=0)
    completed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
