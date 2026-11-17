
import unittest

from app.agents.evaluator import evaluate_meme_ideas


class TestEvaluator(unittest.TestCase):

    def test_idea_valida(self):
        state = {
            "meme_ideas": [
                {
                    "topic": "Calcio",
                    "text_top": "QUANDO VINCI LA PARTITA",
                    "text_bottom": "MA L'ARBITRO FISCHIA FUORIGIOCO",
                    "description": "Meme ironico sul calcio"
                }
            ]
        }

        result = evaluate_meme_ideas(state)

        self.assertEqual(result[0]["evaluation_score"], 10.0)
        self.assertTrue(result[0]["approved"])

    def test_idea_problematic(self):
        state = {
            "meme_ideas": [
                {
                    "topic": "Calcio",
                    "text_top": "QUANDO VINCI",
                    "text_bottom": "",
                    "description": "Meme sulla tecnologia"
                }
            ]
        }

        result = evaluate_meme_ideas(state)

        self.assertLess(result[0]["evaluation_score"], 7)
        self.assertFalse(result[0]["approved"])


if __name__ == "__main__":
    unittest.main()
