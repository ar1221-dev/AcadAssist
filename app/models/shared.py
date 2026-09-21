"""Shared AcadAssist application entities.

These entities map directly to the single shared application database tables.
All models use extend_existing=True to guarantee no duplicate tables are created.
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

    user_id = Column(String(64), primary_key=True, default=generate_uuid)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class Course(Base):
    """Academic Course entity in shared database."""

    __tablename__ = "courses"
    __table_args__ = {"extend_existing": True}

    course_id = Column(String(64), primary_key=True, default=generate_uuid)
    name = Column(String(128), nullable=False)
    code = Column(String(32), nullable=True)


class Subject(Base):
    """Academic Subject entity within a Course in shared database."""

    __tablename__ = "subjects"
    __table_args__ = {"extend_existing": True}

    subject_id = Column(String(64), primary_key=True, default=generate_uuid)
    course_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)


class Topic(Base):
    """Topic entity within a Subject in shared database."""

    __tablename__ = "topics"
    __table_args__ = {"extend_existing": True}

    topic_id = Column(String(64), primary_key=True, default=generate_uuid)
    subject_id = Column(String(64), nullable=False, index=True)
    course_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    difficulty = Column(String(32), nullable=False, default="medium")
    estimated_minutes = Column(Integer, nullable=False, default=60)


from app.assessment.models import Exam

__all__ = ["User", "Course", "Subject", "Topic", "Exam"]

