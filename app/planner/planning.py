"""Study plan and task management foundation for AcadAssist planner module."""

from typing import Any, Dict, List, Optional
from app.contracts.models import StudyPlan, StudyTask


def create_study_task(
    task_id: str,
    title: str,
    topic: str = "",
    planned_date: str = "",
    is_completed: bool = False,
) -> StudyTask:
    """Create a new study task instance.

    Args:
        task_id: Unique identifier for the task.
        title: Task description or title.
        topic: Topic or subject domain.
        planned_date: ISO date string for when the task is scheduled.
        is_completed: Initial completion status.

    Returns:
        A populated StudyTask instance.
    """
    return StudyTask(
        id=task_id,
        title=title,
        topic=topic,
        planned_date=planned_date,
        is_completed=is_completed,
    )


def create_study_plan(
    plan_id: str,
    title: str,
    subject: str = "",
    tasks: Optional[List[StudyTask]] = None,
    created_at: str = "2026-09-16T10:00:00Z",
) -> StudyPlan:
    """Create a new study plan instance with a collection of tasks.

    Args:
        plan_id: Unique plan identifier.
        title: Name of the study plan.
        subject: Academic subject.
        tasks: Optional initial list of tasks.
        created_at: ISO timestamp of creation.

    Returns:
        A populated StudyPlan instance.
    """
    return StudyPlan(
        id=plan_id,
        title=title,
        subject=subject,
        tasks=tasks if tasks is not None else [],
        created_at=created_at,
    )


def add_task_to_plan(plan: StudyPlan, task: StudyTask) -> None:
    """Add a task to an existing study plan.

    Args:
        plan: The target StudyPlan.
        task: The StudyTask to add.
    """
    plan.tasks.append(task)


def complete_task(plan: StudyPlan, task_id: str) -> bool:
    """Mark a specific task in the study plan as completed.

    Args:
        plan: The study plan containing the task.
        task_id: ID of the task to mark completed.

    Returns:
        True if the task was found and updated, False otherwise.
    """
    for task in plan.tasks:
        if task.id == task_id:
            task.is_completed = True
            return True
    return False


def get_plan_completion_stats(plan: StudyPlan) -> Dict[str, Any]:
    """Calculate task completion metrics for a study plan.

    Args:
        plan: The target StudyPlan.

    Returns:
        Dictionary containing total_tasks, completed_tasks, and completion_percentage.
    """
    total = len(plan.tasks)
    if total == 0:
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "completion_percentage": 0.0,
        }

    completed = sum(1 for t in plan.tasks if t.is_completed)
    pending = total - completed
    percentage = round((completed / total) * 100.0, 2)

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_percentage": percentage,
    }


def filter_tasks_by_status(
    plan: StudyPlan,
    completed: bool,
) -> List[StudyTask]:
    """Filter study plan tasks by their completion status.

    Args:
        plan: The study plan.
        completed: True for completed tasks, False for pending tasks.

    Returns:
        List of matching StudyTask instances.
    """
    return [t for t in plan.tasks if t.is_completed == completed]


def load_mock_study_plan(
    plan_id: str = "plan_mock_01",
    title: str = "Computer Science Fundamentals Study Roadmap",
    subject: str = "Computer Science",
) -> StudyPlan:
    """Load a sample mock study plan for local testing and demonstration.

    Args:
        plan_id: Plan identifier.
        title: Plan title.
        subject: Academic subject.

    Returns:
        A sample StudyPlan with predefined study tasks.
    """
    sample_tasks = [
        create_study_task("t_01", "Study Data Structures: Trees and Queues", "Data Structures", "2026-09-17", True),
        create_study_task("t_02", "Study Operating Systems: Deadlocks & Process Management", "Operating Systems", "2026-09-18", False),
        create_study_task("t_03", "Study Computer Networks: OSI Model & TCP/IP", "Computer Networks", "2026-09-19", False),
        create_study_task("t_04", "Complete Core CS Practice Quiz", "Assessment", "2026-09-20", False),
        create_study_task("t_05", "Review Incorrect Questions & Mistakes", "Review", "2026-09-21", False),
    ]
    return create_study_plan(
        plan_id=plan_id,
        title=title,
        subject=subject,
        tasks=sample_tasks,
    )
