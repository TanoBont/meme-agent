
import unittest
from unittest.mock import patch, MagicMock

from app.agents.evaluator import evaluate_meme_ideas


class TestEvaluator(unittest.TestCase):

    @patch("app.agents.evaluator.get_openai_model")
    def test_idea_valida(self, mock_get_model):

        mock_model = MagicMock()
        mock_structured_model = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.with_structured_output.return_value = mock_structured_model

        mock_result = MagicMock()
        mock_result.model_dump.return_value = {
            "creativity": 9,
            "humor": 9,
            "originality": 8,
            "feedback": "Meme creativo e divertente"
        }

        mock_structured_model.invoke.return_value = mock_result

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

        self.assertEqual(result[0]["evaluation"]["rule_score"], 10.0)
        self.assertEqual(result[0]["evaluation"]["ai_score"], 8.8)
        self.assertEqual(result[0]["evaluation_score"], 9.52)
        self.assertTrue(result[0]["approved"])

        mock_get_model.assert_called_once_with(temperature=0.2)
        mock_structured_model.invoke.assert_called_once()

    @patch("app.agents.evaluator.get_openai_model")
    def test_idea_problematic(self, mock_get_model):

        mock_model = MagicMock()
        mock_structured_model = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.with_structured_output.return_value = mock_structured_model

        mock_result = MagicMock()
        mock_result.model_dump.return_value = {
            "creativity": 2,
            "humor": 2,
            "originality": 3,
            "feedback": "Meme poco originale e poco divertente"
        }

        mock_structured_model.invoke.return_value = mock_result

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

        mock_structured_model.invoke.assert_called_once()


if __name__ == "__main__":
    unittest.main()
