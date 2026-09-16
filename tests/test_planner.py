"""Comprehensive unit tests for the AcadAssist planner module."""

import unittest
from app.contracts.models import StudyPlan, StudyTask
from app.planner.planning import (
    add_task_to_plan,
    complete_task,
    create_study_plan,
    create_study_task,
    filter_tasks_by_status,
    get_plan_completion_stats,
    load_mock_study_plan,
)


class TestPlanner(unittest.TestCase):
    """Test study plan and task management."""

    def test_create_study_task(self) -> None:
        task = create_study_task(
            task_id="t1",
            title="Read Chapter 3",
            topic="Operating Systems",
            planned_date="2026-09-18",
            is_completed=False,
        )
        self.assertEqual(task.id, "t1")
        self.assertEqual(task.title, "Read Chapter 3")
        self.assertEqual(task.topic, "Operating Systems")
        self.assertFalse(task.is_completed)

    def test_create_study_plan_and_add_task(self) -> None:
        plan = create_study_plan(
            plan_id="plan_01",
            title="OS Exam Prep",
            subject="Operating Systems",
        )
        self.assertEqual(len(plan.tasks), 0)

        task = create_study_task("t1", "Process Synchronization")
        add_task_to_plan(plan, task)
        self.assertEqual(len(plan.tasks), 1)
        self.assertEqual(plan.tasks[0].id, "t1")

    def test_complete_task(self) -> None:
        task1 = create_study_task("t1", "Task 1", is_completed=False)
        task2 = create_study_task("t2", "Task 2", is_completed=False)
        plan = create_study_plan("plan_01", "Plan", tasks=[task1, task2])

        # Mark t1 as complete
        success = complete_task(plan, "t1")
        self.assertTrue(success)
        self.assertTrue(task1.is_completed)
        self.assertFalse(task2.is_completed)

        # Attempt to complete non-existent task
        not_found = complete_task(plan, "non_existent_id")
        self.assertFalse(not_found)

    def test_plan_completion_stats(self) -> None:
        # Empty plan stats
        empty_plan = create_study_plan("empty", "Empty")
        empty_stats = get_plan_completion_stats(empty_plan)
        self.assertEqual(empty_stats["total_tasks"], 0)
        self.assertEqual(empty_stats["completion_percentage"], 0.0)

        # Plan with mixed completion
        t1 = create_study_task("t1", "T1", is_completed=True)
        t2 = create_study_task("t2", "T2", is_completed=True)
        t3 = create_study_task("t3", "T3", is_completed=False)
        t4 = create_study_task("t4", "T4", is_completed=False)
        plan = create_study_plan("plan_02", "Plan", tasks=[t1, t2, t3, t4])

        stats = get_plan_completion_stats(plan)
        self.assertEqual(stats["total_tasks"], 4)
        self.assertEqual(stats["completed_tasks"], 2)
        self.assertEqual(stats["pending_tasks"], 2)
        self.assertEqual(stats["completion_percentage"], 50.0)

    def test_filter_tasks_by_status(self) -> None:
        t1 = create_study_task("t1", "T1", is_completed=True)
        t2 = create_study_task("t2", "T2", is_completed=False)
        plan = create_study_plan("plan_03", "Plan", tasks=[t1, t2])

        completed = filter_tasks_by_status(plan, completed=True)
        pending = filter_tasks_by_status(plan, completed=False)

        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].id, "t1")
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].id, "t2")

    def test_load_mock_study_plan(self) -> None:
        plan = load_mock_study_plan()
        self.assertIsInstance(plan, StudyPlan)
        self.assertGreater(len(plan.tasks), 0)
        stats = get_plan_completion_stats(plan)
        self.assertGreater(stats["total_tasks"], 0)


if __name__ == "__main__":
    unittest.main()
