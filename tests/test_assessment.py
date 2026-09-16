"""Comprehensive unit tests for the AcadAssist assessment module."""

import unittest
from app.assessment.evaluator import evaluate_quiz, is_answer_correct, normalize_answer
from app.assessment.mistakes import (
    count_mistakes_by_topic,
    extract_mistakes,
    filter_mistakes_by_topic,
)
from app.assessment.mock_data import (
    MOCK_QUESTIONS,
    get_mock_questions,
    load_mock_quiz,
)
from app.assessment.progress import calculate_progress, calculate_topic_progress
from app.assessment.question_history import QuestionHistory, normalize_question_text
from app.contracts.models import (
    Mistake,
    Progress,
    Quiz,
    QuizAttempt,
    QuizQuestion,
    QuizResult,
)


class TestMockData(unittest.TestCase):
    """Test mock question loading and filtering."""

    def test_mock_questions_exist(self) -> None:
        self.assertGreater(len(MOCK_QUESTIONS), 0)

    def test_get_mock_questions_filter_by_topic(self) -> None:
        questions = get_mock_questions(topic="Operating Systems")
        self.assertTrue(all("Operating Systems" in q.topic for q in questions))
        self.assertGreater(len(questions), 0)

    def test_get_mock_questions_filter_by_difficulty(self) -> None:
        questions = get_mock_questions(difficulty="easy")
        self.assertTrue(all(q.difficulty == "easy" for q in questions))

    def test_load_mock_quiz(self) -> None:
        quiz = load_mock_quiz(quiz_id="test_quiz_01", title="Test Quiz")
        self.assertEqual(quiz.id, "test_quiz_01")
        self.assertEqual(quiz.title, "Test Quiz")
        self.assertEqual(len(quiz.questions), len(MOCK_QUESTIONS))


class TestEvaluator(unittest.TestCase):
    """Test deterministic evaluation and scoring."""

    def setUp(self) -> None:
        self.q1 = QuizQuestion(
            id="q1",
            text="What is 2+2?",
            options=["A. 3", "B. 4", "C. 5", "D. 6"],
            correct_answer="B",
            explanation="2+2 equals 4.",
            topic="Math",
            difficulty="easy",
        )
        self.q2 = QuizQuestion(
            id="q2",
            text="Which planet is known as the Red Planet?",
            options=["A. Venus", "B. Mars", "C. Jupiter", "D. Saturn"],
            correct_answer="B",
            explanation="Mars appears red due to iron oxide.",
            topic="Science",
            difficulty="easy",
        )
        self.quiz = Quiz(
            id="quiz_test",
            title="General Knowledge",
            questions=[self.q1, self.q2],
        )

    def test_normalize_answer(self) -> None:
        self.assertEqual(normalize_answer("b"), "B")
        self.assertEqual(normalize_answer(" B "), "B")
        self.assertEqual(normalize_answer("B."), "B")
        self.assertEqual(normalize_answer("(B)"), "B")
        self.assertEqual(normalize_answer("B. Option text"), "B")
        self.assertEqual(normalize_answer(""), "")
        self.assertEqual(normalize_answer(None), "")

    def test_is_answer_correct(self) -> None:
        self.assertTrue(is_answer_correct("b", "B"))
        self.assertTrue(is_answer_correct(" B ", "B"))
        self.assertTrue(is_answer_correct("B. Mars", "B"))
        self.assertFalse(is_answer_correct("A", "B"))
        self.assertFalse(is_answer_correct("", "B"))

    def test_evaluate_all_correct(self) -> None:
        attempt = QuizAttempt(
            id="att_01",
            quiz_id="quiz_test",
            submitted_answers={"q1": "B", "q2": "B"},
        )
        result = evaluate_quiz(self.quiz, attempt)
        self.assertEqual(result.total_questions, 2)
        self.assertEqual(result.correct_count, 2)
        self.assertEqual(result.incorrect_count, 0)
        self.assertEqual(result.score, 2.0)
        self.assertEqual(result.percentage, 100.0)
        self.assertEqual(len(result.mistakes), 0)

    def test_evaluate_partial_correct(self) -> None:
        attempt = QuizAttempt(
            id="att_02",
            quiz_id="quiz_test",
            submitted_answers={"q1": "B", "q2": "A"},  # q2 incorrect
        )
        result = evaluate_quiz(self.quiz, attempt)
        self.assertEqual(result.total_questions, 2)
        self.assertEqual(result.correct_count, 1)
        self.assertEqual(result.incorrect_count, 1)
        self.assertEqual(result.score, 1.0)
        self.assertEqual(result.percentage, 50.0)
        self.assertEqual(len(result.mistakes), 1)
        mistake = result.mistakes[0]
        self.assertEqual(mistake.question_id, "q2")
        self.assertEqual(mistake.student_answer, "A")
        self.assertEqual(mistake.correct_answer, "B")
        self.assertEqual(mistake.topic, "Science")

    def test_evaluate_all_incorrect_or_unanswered(self) -> None:
        attempt = QuizAttempt(
            id="att_03",
            quiz_id="quiz_test",
            submitted_answers={},  # no answers provided
        )
        result = evaluate_quiz(self.quiz, attempt)
        self.assertEqual(result.total_questions, 2)
        self.assertEqual(result.correct_count, 0)
        self.assertEqual(result.incorrect_count, 2)
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.percentage, 0.0)
        self.assertEqual(len(result.mistakes), 2)
        self.assertEqual(result.mistakes[0].student_answer, "[No Answer]")

    def test_evaluate_empty_quiz_edge_case(self) -> None:
        empty_quiz = Quiz(id="empty", title="Empty Quiz", questions=[])
        attempt = QuizAttempt(id="att_empty", quiz_id="empty", submitted_answers={})
        result = evaluate_quiz(empty_quiz, attempt)
        self.assertEqual(result.total_questions, 0)
        self.assertEqual(result.correct_count, 0)
        self.assertEqual(result.incorrect_count, 0)
        self.assertEqual(result.percentage, 0.0)
        self.assertEqual(len(result.mistakes), 0)


class TestMistakes(unittest.TestCase):
    """Test mistake tracking, extraction, and filtering."""

    def test_extract_and_filter_mistakes(self) -> None:
        quiz = load_mock_quiz()
        # Answer only the first question correctly, leave the rest unanswered
        first_q = quiz.questions[0]
        attempt = QuizAttempt(
            id="att_mistake_test",
            quiz_id=quiz.id,
            submitted_answers={first_q.id: first_q.correct_answer},
        )
        mistakes = extract_mistakes(quiz, attempt)
        expected_mistakes_count = len(quiz.questions) - 1
        self.assertEqual(len(mistakes), expected_mistakes_count)

        # Filter by Operating Systems
        os_mistakes = filter_mistakes_by_topic(mistakes, "Operating Systems")
        self.assertTrue(all("Operating Systems" in m.topic for m in os_mistakes))

        # Count by topic
        counts = count_mistakes_by_topic(mistakes)
        self.assertIsInstance(counts, dict)
        self.assertGreater(sum(counts.values()), 0)


class TestProgress(unittest.TestCase):
    """Test deterministic progress aggregation."""

    def test_empty_results_progress(self) -> None:
        prog = calculate_progress([])
        self.assertEqual(prog.quizzes_attempted, 0)
        self.assertEqual(prog.questions_attempted, 0)
        self.assertEqual(prog.accuracy_percentage, 0.0)

    def test_aggregate_progress(self) -> None:
        res1 = QuizResult(
            quiz_id="q1",
            total_questions=10,
            correct_count=8,
            incorrect_count=2,
            score=8.0,
            percentage=80.0,
        )
        res2 = QuizResult(
            quiz_id="q2",
            total_questions=10,
            correct_count=6,
            incorrect_count=4,
            score=6.0,
            percentage=60.0,
        )
        prog = calculate_progress([res1, res2])
        self.assertEqual(prog.quizzes_attempted, 2)
        self.assertEqual(prog.questions_attempted, 20)
        self.assertEqual(prog.correct_count, 14)
        self.assertEqual(prog.incorrect_count, 6)
        self.assertEqual(prog.accuracy_percentage, 70.0)

    def test_topic_progress_breakdown(self) -> None:
        quiz_ds = Quiz(id="quiz_ds", title="DS Quiz", topic="Data Structures")
        quiz_os = Quiz(id="quiz_os", title="OS Quiz", topic="Operating Systems")
        quiz_map = {"quiz_ds": quiz_ds, "quiz_os": quiz_os}

        res_ds = QuizResult(quiz_id="quiz_ds", total_questions=5, correct_count=5, incorrect_count=0)
        res_os = QuizResult(quiz_id="quiz_os", total_questions=5, correct_count=2, incorrect_count=3)

        breakdown = calculate_topic_progress([res_ds, res_os], quiz_map)
        self.assertIn("Data Structures", breakdown)
        self.assertIn("Operating Systems", breakdown)
        self.assertEqual(breakdown["Data Structures"].accuracy_percentage, 100.0)
        self.assertEqual(breakdown["Operating Systems"].accuracy_percentage, 40.0)


class TestQuestionHistory(unittest.TestCase):
    """Test duplicate question prevention and history tracking."""

    def test_normalize_question_text(self) -> None:
        t1 = "What is the time complexity of Binary Search?"
        t2 = "  what is the time complexity of binary search?   "
        self.assertEqual(normalize_question_text(t1), normalize_question_text(t2))

    def test_duplicate_detection_by_id_and_text(self) -> None:
        history = QuestionHistory()
        q1 = QuizQuestion(id="q_01", text="What is FIFO?", correct_answer="B")
        q2 = QuizQuestion(id="q_02", text="What is FIFO?", correct_answer="B")  # Same text, diff id
        q3 = QuizQuestion(id="q_01", text="Different text", correct_answer="A")  # Same id, diff text
        q4 = QuizQuestion(id="q_03", text="What is LIFO?", correct_answer="A")  # Completely new

        self.assertFalse(history.is_duplicate(q1))
        history.record(q1)

        # q1 is now duplicate
        self.assertTrue(history.is_duplicate(q1))
        # q2 is duplicate by normalized text
        self.assertTrue(history.is_duplicate(q2))
        # q3 is duplicate by id
        self.assertTrue(history.is_duplicate(q3))
        # q4 is not duplicate
        self.assertFalse(history.is_duplicate(q4))

    def test_filter_new_questions(self) -> None:
        history = QuestionHistory()
        q1 = QuizQuestion(id="q1", text="Question 1")
        q2 = QuizQuestion(id="q2", text="Question 2")
        q3 = QuizQuestion(id="q3", text="Question 3")

        history.record(q1)
        filtered = history.filter_new_questions([q1, q2, q3])
        self.assertEqual(len(filtered), 2)
        self.assertEqual([q.id for q in filtered], ["q2", "q3"])


if __name__ == "__main__":
    unittest.main()
