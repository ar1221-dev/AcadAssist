"""Knowledge retrieval API routes."""

from fastapi import APIRouter, HTTPException
from app.schemas.knowledge import KnowledgeSearchRequest, KnowledgeSearchResponse
from app.services.rag.knowledge import search_knowledge

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])


@router.post("/search", response_model=KnowledgeSearchResponse)
def search_knowledge_endpoint(request: KnowledgeSearchRequest):
    """Hybrid search endpoint retrieving knowledge chunks for student questions.

    Enforces server-side user isolation, ensuring students only retrieve their own chunks.
    """
    try:
        results_dict = search_knowledge(
            user_id=request.user_id,
            query=request.query,
            course_id=request.course_id,
            subject_id=request.subject_id,
            top_k=request.top_k,
        )
        return KnowledgeSearchResponse(**results_dict)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge search failed: {e}")
