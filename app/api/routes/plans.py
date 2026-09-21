"""API routes for Study Plans and Tasks (Person 4)."""

from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.study_plan import StudyPlan, StudyTask
from app.schemas.study import (
    StudyPlanCreateRequest,
    StudyPlanResponse,
    StudyTaskResponse,
    TaskUpdateRequest,
    TodayPlanResponse,
)
from app.services.planner import create_study_plan, get_today_plan, update_task_status

router = APIRouter(prefix="/plans", tags=["Study Plans"])
tasks_router = APIRouter(prefix="/tasks", tags=["Study Tasks"])


@router.post("", response_model=StudyPlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(
    payload: StudyPlanCreateRequest,
    db: Session = Depends(get_db),
):
    """Generate and store a new exam-aware study plan."""
    try:
        plan = create_study_plan(
            user_id=payload.user_id,
            start_date=payload.start_date,
            end_date=payload.end_date,
            available_minutes_per_day=payload.available_minutes_per_day,
            db=db,
        )
        return plan
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create study plan: {str(e)}",
        )


@router.get("", response_model=List[StudyPlanResponse])
def list_plans(
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db),
):
    """List all study plans for the user."""
    plans = (
        db.query(StudyPlan)
        .filter(StudyPlan.user_id == user_id)
        .order_by(StudyPlan.created_at.desc())
        .all()
    )
    return plans


@router.get("/today", response_model=TodayPlanResponse)
def get_today_study_plan(
    user_id: str = Query(..., description="User ID"),
    target_date: Optional[date] = Query(None, description="Optional target date (defaults to today)"),
    db: Session = Depends(get_db),
):
    """Retrieve today's scheduled study tasks."""
    try:
        plan_data = get_today_plan(user_id=user_id, target_date=target_date, db=db)
        return TodayPlanResponse(**plan_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve today's plan: {str(e)}",
        )


@router.get("/{plan_id}", response_model=StudyPlanResponse)
def get_plan_by_id(
    plan_id: str,
    user_id: str = Query(..., description="User ID required for user isolation"),
    db: Session = Depends(get_db),
):
    """Retrieve a specific study plan and its tasks scoped to user_id."""
    plan = (
        db.query(StudyPlan)
        .filter(StudyPlan.study_plan_id == plan_id, StudyPlan.user_id == user_id)
        .first()
    )

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study plan '{plan_id}' not found or access unauthorized for user '{user_id}'",
        )
    return plan


@tasks_router.patch("/{task_id}", response_model=StudyTaskResponse)
def patch_task(
    task_id: str,
    payload: TaskUpdateRequest,
    user_id: str = Query(..., description="User ID required for authorization check"),
    db: Session = Depends(get_db),
):
    """Update study task completion status or reschedule time scoped to user_id."""
    try:
        task = update_task_status(
            task_id=task_id,
            status=payload.status,
            user_id=user_id,
            rescheduled_date=payload.rescheduled_date,
            rescheduled_time=payload.rescheduled_time,
            db=db,
        )
        return task
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}",
        )
