"""
Comprehensive automated test suite for MindMesh AI.
Validates all AI generation functions, document parsing, and edge cases.
"""

import sys
import unittest
from config import SAMPLE_OS_NOTES, SAMPLE_DSA_NOTES
from ai.gemma import (
    local_engine_generate_summary,
    local_engine_generate_mcqs,
    local_engine_generate_flashcards,
    local_engine_generate_exam_questions,
    local_engine_generate_revision_plan,
    local_engine_ask_ai,
    clean_json_response,
    check_ollama_status
)
from utils.text_processor import clean_text, get_text_stats, truncate_text_for_ai

class TestMindMeshAI(unittest.TestCase):
    def test_clean_text_and_stats(self):
        sample = "  This is an operating system note.   \n\n\n\nIt handles processes.  "
        cleaned = clean_text(sample)
        self.assertNotIn("   ", cleaned)
        stats = get_text_stats(cleaned)
        self.assertGreater(stats["word_count"], 0)
        self.assertGreater(stats["char_count"], 0)
        self.assertGreater(stats["est_tokens"], 0)

    def test_summary_generation(self):
        summary = local_engine_generate_summary(SAMPLE_OS_NOTES, "Operating Systems")
        self.assertIn("quick_summary", summary)
        self.assertIn("detailed_summary", summary)
        self.assertIn("important_points", summary)
        self.assertIn("key_terms", summary)
        self.assertGreaterEqual(len(summary["important_points"]), 3)
        self.assertGreaterEqual(len(summary["key_terms"]), 3)

    def test_mcq_generation(self):
        mcqs = local_engine_generate_mcqs(SAMPLE_OS_NOTES, number=5, difficulty="Medium")
        self.assertIn("questions", mcqs)
        questions = mcqs["questions"]
        self.assertEqual(len(questions), 5)
        for q in questions:
            self.assertIn("question", q)
            self.assertEqual(len(q["options"]), 4)
            self.assertIn(q["correct_answer"], q["options"])
            self.assertIn("explanation", q)

    def test_flashcards_generation(self):
        fc = local_engine_generate_flashcards(SAMPLE_OS_NOTES, number=6)
        self.assertIn("flashcards", fc)
        cards = fc["flashcards"]
        self.assertEqual(len(cards), 6)
        for c in cards:
            self.assertIn("question", c)
            self.assertIn("answer", c)
            self.assertIn("category", c)

    def test_exam_questions_generation(self):
        eq = local_engine_generate_exam_questions(SAMPLE_OS_NOTES)
        self.assertIn("very_short_questions", eq)
        self.assertIn("short_questions", eq)
        self.assertIn("long_questions", eq)
        self.assertGreaterEqual(len(eq["very_short_questions"]), 2)
        self.assertGreaterEqual(len(eq["short_questions"]), 2)
        self.assertGreaterEqual(len(eq["long_questions"]), 1)

    def test_revision_plan_generation(self):
        plan = local_engine_generate_revision_plan(
            subject="Operating Systems",
            exam_date="2026-10-10",
            study_time="2 hours/day",
            level="Beginner"
        )
        self.assertIn("plan_overview", plan)
        self.assertIn("daily_schedule", plan)
        self.assertGreaterEqual(len(plan["daily_schedule"]), 3)
        for day in plan["daily_schedule"]:
            self.assertIn("day", day)
            self.assertIn("topic", day)
            self.assertIn("duration", day)
            self.assertIn("tasks", day)

    def test_ask_ai_grounding(self):
        # Test specific deadlock question
        reply1 = local_engine_ask_ai("Explain deadlock in simple terms", SAMPLE_OS_NOTES)
        self.assertIn("Deadlock", reply1)
        self.assertIn("Coffman", reply1)

        # Test process vs thread
        reply2 = local_engine_ask_ai("What is the difference between process and thread?", SAMPLE_OS_NOTES)
        self.assertIn("Process", reply2)
        self.assertIn("Thread", reply2)

    def test_json_cleaner(self):
        dirty = '```json\n{"status": "ok", "value": 42}\n```'
        cleaned = clean_json_response(dirty)
        self.assertEqual(cleaned, '{"status": "ok", "value": 42}')

    def test_ollama_graceful_check(self):
        # Should gracefully return (False, [], message) without unhandled exception
        is_up, models, msg = check_ollama_status("http://127.0.0.1:11434")
        self.assertIsInstance(is_up, bool)

if __name__ == "__main__":
    unittest.main()
