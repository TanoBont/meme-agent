
import unittest
from unittest.mock import patch, MagicMock

from app.agents.creative import generate_meme_ideas


class TestCreativeAgent(unittest.TestCase):

    @patch("app.agents.creative.get_openai_model")
    def test_generate_meme_ideas(self, mock_get_model):

        mock_model = MagicMock()
        mock_structured_model = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.with_structured_output.return_value = mock_structured_model

        mock_idea = MagicMock()
        mock_idea.model_dump.return_value = {
            "topic": "Calcio",
            "text_top": "QUANDO LA TUA SQUADRA SEGNA",
            "text_bottom": "MA L'ARBITRO ANNULLA IL GOL",
            "description": "Meme sulle delusioni calcistiche"
        }

        mock_result = MagicMock()
        mock_result.ideas = [mock_idea]

        mock_structured_model.invoke.return_value = mock_result

        state = {
            "ranked_trends": [
                {
                    "topic": "Calcio",
                    "score": 8.5
                }
            ]
        }

        result = generate_meme_ideas(state)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["topic"], "Calcio")
        self.assertEqual(result[0]["score"], 8.5)
        self.assertIn("text_top", result[0])
        self.assertIn("text_bottom", result[0])

        mock_get_model.assert_called_once_with(temperature=0.9)
        mock_structured_model.invoke.assert_called_once()


if __name__ == "__main__":
    unittest.main()
