"""Mock academic questions and quiz loaders for Checkpoint 1 testing."""

from typing import List, Optional
from app.contracts.models import Quiz, QuizQuestion

# Curated academic question bank for deterministic testing and local flow
MOCK_QUESTIONS: List[QuizQuestion] = [
    QuizQuestion(
        id="q_ds_01",
        text="What is the time complexity of binary search on a sorted array of n elements?",
        options=[
            "A. O(n)",
            "B. O(log n)",
            "C. O(n^2)",
            "D. O(1)",
        ],
        correct_answer="B",
        explanation="Binary search halves the search space at each step, yielding O(log n) time complexity.",
        topic="Data Structures & Algorithms",
        difficulty="easy",
    ),
    QuizQuestion(
        id="q_ds_02",
        text="Which data structure operates on a First-In-First-Out (FIFO) principle?",
        options=[
            "A. Stack",
            "B. Queue",
            "C. Binary Tree",
            "D. Hash Table",
        ],
        correct_answer="B",
        explanation="A Queue operates on the FIFO principle where the first element added is the first one removed.",
        topic="Data Structures & Algorithms",
        difficulty="easy",
    ),
    QuizQuestion(
        id="q_os_01",
        text="Which of the following is NOT one of Coffman's four necessary conditions for deadlock?",
        options=[
            "A. Mutual Exclusion",
            "B. Hold and Wait",
            "C. Preemption",
            "D. Circular Wait",
        ],
        correct_answer="C",
        explanation="The condition is 'No Preemption', meaning resources cannot be forcibly seized.",
        topic="Operating Systems",
        difficulty="medium",
    ),
    QuizQuestion(
        id="q_os_02",
        text="What mechanism does an operating system use to switch the CPU from one process to another?",
        options=[
            "A. Paging",
            "B. Context Switching",
            "C. Thrashing",
            "D. Polling",
        ],
        correct_answer="B",
        explanation="Context switching saves the state of the current process and restores the state of the next process.",
        topic="Operating Systems",
        difficulty="medium",
    ),
    QuizQuestion(
        id="q_cn_01",
        text="Which layer of the OSI model is responsible for end-to-end reliability and flow control?",
        options=[
            "A. Network Layer",
            "B. Transport Layer",
            "C. Data Link Layer",
            "D. Session Layer",
        ],
        correct_answer="B",
        explanation="The Transport Layer (Layer 4) handles end-to-end communication, segmentation, flow control, and error recovery (e.g., TCP).",
        topic="Computer Networks",
        difficulty="easy",
    ),
    QuizQuestion(
        id="q_cn_02",
        text="What is the default port number used by the HTTPS protocol?",
        options=[
            "A. 80",
            "B. 21",
            "C. 443",
            "D. 8080",
        ],
        correct_answer="C",
        explanation="HTTPS uses TCP port 443 by default for encrypted web traffic.",
        topic="Computer Networks",
        difficulty="easy",
    ),
]


def get_mock_questions(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
) -> List[QuizQuestion]:
    """Retrieve filtered mock questions from the bank.

    Args:
        topic: Optional topic filter (case-insensitive substring match).
        difficulty: Optional difficulty filter ('easy', 'medium', 'hard').

    Returns:
        List of matching QuizQuestion instances.
    """
    filtered = MOCK_QUESTIONS
    if topic:
        filtered = [q for q in filtered if topic.lower() in q.topic.lower()]
    if difficulty:
        filtered = [q for q in filtered if q.difficulty.lower() == difficulty.lower()]
    return list(filtered)


def load_mock_quiz(
    quiz_id: str = "mock_quiz_01",
    title: str = "Computer Science Core Fundamentals",
    topic: str = "Computer Science",
    difficulty: str = "medium",
    questions: Optional[List[QuizQuestion]] = None,
) -> Quiz:
    """Load or construct a mock quiz for local demonstration and testing.

    Args:
        quiz_id: Unique identifier for the quiz.
        title: Quiz title.
        topic: Subject or topic area.
        difficulty: Overall difficulty level.
        questions: Optional list of questions; defaults to all mock questions.

    Returns:
        A Quiz instance populated with questions.
    """
    selected_questions = questions if questions is not None else list(MOCK_QUESTIONS)
    return Quiz(
        id=quiz_id,
        title=title,
        subject="Computer Science",
        topic=topic,
        difficulty=difficulty,
        questions=selected_questions,
        created_at="2026-09-16T10:00:00Z",
    )
