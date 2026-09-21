from collections.abc import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.knowledge_base import KnowledgeBaseService, knowledge_base_service


def get_kb_service() -> KnowledgeBaseService:
    return knowledge_base_service
