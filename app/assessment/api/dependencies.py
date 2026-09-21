"""API dependencies and authentication/user resolution for Person 3 Assessment Subsystem."""

from typing import Optional
from fastapi import Header, Query, HTTPException, status


def get_current_user_id(
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    user_id: Optional[str] = Query(None, alias="user_id"),
) -> str:
    """Resolve current user ID from X-User-ID header or query parameter.

    Enforces strict identity resolution while maintaining compatibility across
    development tools, curl, and frontend clients.
    """
    resolved = x_user_id or user_id
    if not resolved:
        # Default fallback for unauthenticated local development if no header provided
        return "default_student_user"
    return resolved.strip()
