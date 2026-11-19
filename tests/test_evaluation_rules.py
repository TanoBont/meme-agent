
import unittest

from app.agents.evaluation_rules import (
    evaluate_completeness,
    evaluate_relevance,
    evaluate_readability,
    evaluate_structure
)


class TestEvaluationRules(unittest.TestCase):

    def setUp(self):
        self.valid_idea = {
            "topic": "Calcio",
            "text_top": "QUANDO LA TUA SQUADRA VINCE",
            "text_bottom": "MA IL VAR ANNULLA IL GOL",
            "description": "Meme ironico sulle polemiche arbitrali."
        }

    def test_completeness_valid_idea(self):
        score = evaluate_completeness(self.valid_idea)
        self.assertEqual(score, 10.0)

    def test_completeness_missing_field(self):
        idea = self.valid_idea.copy()
        idea["text_bottom"] = ""

        score = evaluate_completeness(idea)

        self.assertEqual(score, 7.5)

    def test_relevance_matching_topic(self):
        score = evaluate_relevance(self.valid_idea)

        self.assertEqual(score, 10.0)

    def test_relevance_empty_topic(self):
        idea = self.valid_idea.copy()
        idea["topic"] = ""

        score = evaluate_relevance(idea)

        self.assertEqual(score, 1)

    def test_readability_short_texts(self):
        score = evaluate_readability(self.valid_idea)

        self.assertEqual(score, 10.0)

    def test_readability_missing_text(self):
        idea = self.valid_idea.copy()
        idea["text_top"] = ""

        score = evaluate_readability(idea)

        self.assertLess(score, 10.0)

    def test_structure_valid_idea(self):
        score = evaluate_structure(self.valid_idea)

        self.assertEqual(score, 10)

    def test_structure_empty_field(self):
        idea = self.valid_idea.copy()
        idea["text_bottom"] = ""

        score = evaluate_structure(idea)

        self.assertEqual(score, 1)

    def test_structure_identical_texts(self):
        idea = self.valid_idea.copy()
        idea["text_top"] = "STESSO TESTO"
        idea["text_bottom"] = "STESSO TESTO"

        score = evaluate_structure(idea)

        self.assertEqual(score, 3)


if __name__ == "__main__":
    unittest.main()
