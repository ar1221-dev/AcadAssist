# Assessment and Planning Module (Person 3)

## 1. Overview & Purpose
The **Assessment + Planning** module (`app/assessment` and `app/planner`) forms the core practice, evaluation, mistake tracking, and study management foundation of **AcadAssist**.

In the full AcadAssist lifecycle:
$$\text{Learn} \longrightarrow \text{Practice} \longrightarrow \text{Evaluate} \longrightarrow \text{Identify Weakness} \longrightarrow \text{Plan} \longrightarrow \text{Revise}$$

Person 3 provides the deterministic application layer for the **Practice**, **Evaluate**, **Mistakes**, **Progress**, and **Plan** steps.

---

## 2. Checkpoint 1 Scope (Foundation Only)

For Checkpoint 1, the module implements a fully offline, deterministic, mock-driven pipeline:
- **Zero Cloud / Azure dependencies** (No Azure AI Search, No Cosmos DB, No Blob Storage).
- **Zero LLM dependencies** (No OpenAI/Foundry API calls).
- **Deterministic logic** for scoring, percentage calculations, mistake logging, and progress metrics.
- **Single authoritative models** under `app/contracts/models.py`.
- **Strict module separation**: Assessment logic in `app/assessment/`, Study Planning logic in `app/planner/`.

---

## 3. Architecture & Data Contracts

All data contracts are standard Python dataclasses in `app/contracts/models.py`:

```
┌─────────────────────────────────────────────────────────────┐
│                      app/contracts/                         │
│  QuizQuestion  │  Quiz  │  QuizAttempt  │  QuizResult       │
│  Mistake       │  Progress  │  StudyTask │  StudyPlan       │
└──────────────────────────────┬──────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
     ┌───────────────────┐           ┌───────────────────┐
     │  app/assessment/  │           │   app/planner/    │
     │  - mock_data.py   │           │  - planning.py    │
     │  - evaluator.py   │           └───────────────────┘
     │  - mistakes.py    │
     │  - progress.py    │
     │  - question_      │
     │    history.py     │
     └───────────────────┘
```

### Core Models
- **`QuizQuestion`**: Question ID, text, options list, correct answer, explanation, topic, and difficulty.
- **`Quiz`**: Quiz ID, title, subject, topic, difficulty, questions list, and timestamp.
- **`QuizAttempt`**: Attempt ID, quiz ID reference, student/user ID, submitted answers map (`question_id -> answer`).
- **`QuizResult`**: Total questions, correct count, incorrect count, numeric score, percentage, and list of `Mistake` objects.
- **`Mistake`**: Question ID, question text, student's answer, correct answer, explanation, and topic.
- **`Progress`**: Total quizzes attempted, questions attempted, correct count, incorrect count, and accuracy percentage.
- **`StudyTask`**: Task ID, title, topic, planned date, and boolean completion status.
- **`StudyPlan`**: Plan ID, title, subject, list of `StudyTask` instances, and creation timestamp.

---

## 4. Workflows & Usage

### 4.1 Mock Quiz Flow & Evaluation
```python
from app.assessment import load_mock_quiz, evaluate_quiz, extract_mistakes
from app.contracts.models import QuizAttempt

# 1. Load a mock quiz
quiz = load_mock_quiz()

# 2. Capture student answers
attempt = QuizAttempt(
    id="attempt_01",
    quiz_id=quiz.id,
    submitted_answers={
        "q_ds_01": "B",  # Correct
        "q_ds_02": "A",  # Incorrect (Queue is FIFO, student chose Stack)
    }
)

# 3. Evaluate attempt deterministically
result = evaluate_quiz(quiz, attempt)
print(f"Score: {result.correct_count}/{result.total_questions} ({result.percentage}%)")

# 4. Review mistakes
for mistake in result.mistakes:
    print(f"Question: {mistake.question_text}")
    print(f"Your Answer: {mistake.student_answer} | Correct: {mistake.correct_answer}")
    print(f"Explanation: {mistake.explanation}")
```

### 4.2 Progress Tracking
```python
from app.assessment import calculate_progress

# Aggregate multiple quiz results into overall progress
overall_progress = calculate_progress([result])
print(f"Overall Accuracy: {overall_progress.accuracy_percentage}%")
```

### 4.3 Question Duplicate Prevention
```python
from app.assessment import QuestionHistory

history = QuestionHistory()

# Check and record seen questions
for question in quiz.questions:
    if not history.is_duplicate(question):
        history.record(question)
```

### 4.4 Study Planning & Tasks
```python
from app.planner import load_mock_study_plan, complete_task, get_plan_completion_stats

# 1. Load or create a study plan
plan = load_mock_study_plan()

# 2. Complete a task
complete_task(plan, task_id="t_02")

# 3. Check stats
stats = get_plan_completion_stats(plan)
print(f"Progress: {stats['completed_tasks']}/{stats['total_tasks']} ({stats['completion_percentage']}%)")
```

---

## 5. Running Tests

Run the test suite using `pytest`:

```bash
python -m pytest
```

Or using standard `unittest`:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 6. Future Scope (Checkpoint 2 & Beyond)
The following are intentionally **deferred** to subsequent checkpoints:
- Dynamic quiz generation using Azure OpenAI / Microsoft Foundry.
- Semantic duplicate detection using embeddings and vector search.
- Adaptive study plan generation based on real-time performance analytics.
- Integration with Azure Cosmos DB / PostgreSQL for persistence.
- Streamlit UI components (Person 5 responsibility).
