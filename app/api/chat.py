"""Chat API Endpoint Router.

Provides POST /api/chat for student interactions.
React communicates solely through this endpoint.
"""

import logging
from fastapi import APIRouter, HTTPException, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.azure.agent import AcadAssistAgentService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Chat"])

# Singleton agent service instance for request handling
_agent_service: AcadAssistAgentService | None = None


def get_agent_service() -> AcadAssistAgentService:
    """Retrieve or initialize the AcadAssistAgentService instance."""
    global _agent_service
    if _agent_service is None:
        _agent_service = AcadAssistAgentService()
    return _agent_service


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Interact with the AcadAssist Study Assistant",
    description=(
        "Processes student queries through the ONE AcadAssist Agent on Microsoft Foundry. "
        "The agent orchestrates tool selection, retrieves grounded academic source materials, "
        "and returns structured responses with citations."
    ),
)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Process incoming chat messages from React frontend."""
    # Validate request payload
    clean_message = request.message.strip()
    if not clean_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'message' field must not be empty.",
        )

    clean_user_id = request.user_id.strip()
    if not clean_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'user_id' field must not be empty.",
        )

    try:
        agent_service = get_agent_service()
        response = agent_service.chat(
            user_id=clean_user_id,
            message=clean_message,
        )
        return response
    except Exception as exc:
        logger.error("Error processing chat message: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while communicating with AcadAssist: {str(exc)}",
        )
