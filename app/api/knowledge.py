"""Knowledge API Router.

Provides POST /api/knowledge/search as an API boundary for knowledge retrieval.
Does NOT duplicate Person 2's actual RAG implementation.
"""

import logging
from fastapi import APIRouter, HTTPException, status

from app.schemas.search import SearchKnowledgeRequest, SearchKnowledgeResponse
from app.azure.adapters import KnowledgeBaseAdapter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge"])

_kb_adapter: KnowledgeBaseAdapter | None = None


def get_kb_adapter() -> KnowledgeBaseAdapter:
    """Get or initialize the KnowledgeBaseAdapter."""
    global _kb_adapter
    if _kb_adapter is None:
        _kb_adapter = KnowledgeBaseAdapter()
    return _kb_adapter


@router.post(
    "/search",
    response_model=SearchKnowledgeResponse,
    status_code=status.HTTP_200_OK,
    summary="Search the student academic knowledge base",
    description="API boundary for Person 2 knowledge search. Filters by user_id and optionally course_id/subject_id.",
)
def search_knowledge_endpoint(request: SearchKnowledgeRequest) -> SearchKnowledgeResponse:
    """Execute knowledge search."""
    if not request.user_id or not request.user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field is mandatory.",
        )
    if not request.query or not request.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'query' field must not be empty.",
        )

    try:
        adapter = get_kb_adapter()
        response = adapter.search_knowledge(
            user_id=request.user_id.strip(),
            query=request.query.strip(),
            course_id=request.course_id,
            subject_id=request.subject_id,
            top_k=request.top_k,
        )
        return response
    except Exception as exc:
        logger.error("Error executing knowledge search: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during knowledge search: {str(exc)}",
        )
