
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
            "topic": "Polemiche arbitrali",
            "text_top": "QUANDO LA TUA SQUADRA SEGNA",
            "text_bottom": "MA IL VAR HA ALTRI PROGRAMMI",
            "description": "Meme sulle polemiche arbitrali."
        }

        mock_result = MagicMock()
        mock_result.ideas = [mock_idea]

        mock_structured_model.invoke.return_value = mock_result

        state = {
            "ranked_trends": [
                {
                    "topic": "Polemiche arbitrali",
                    "description": "Discussioni sulle decisioni VAR.",
                    "category": "controversies",
                    "content_type": "current",
                    "score": 8.5
                }
            ]
        }

        result = generate_meme_ideas(state)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["topic"], "Polemiche arbitrali")
        self.assertEqual(result[0]["score"], 8.5)
        self.assertIn("text_top", result[0])
        self.assertIn("text_bottom", result[0])

        mock_get_model.assert_called_once_with(temperature=0.9)
        mock_model.with_structured_output.assert_called_once_with(
            unittest.mock.ANY
        )
        mock_structured_model.invoke.assert_called_once()

        prompt = mock_structured_model.invoke.call_args.args[0]

        self.assertIn("calcio italiano ed europeo", prompt)
        self.assertIn("controversies", prompt)
        self.assertIn("current", prompt)
        self.assertIn("esattamente un'idea", prompt)

    @patch("app.agents.creative.get_openai_model")
    def test_empty_trends(self, mock_get_model):

        state = {
            "ranked_trends": []
        }

        result = generate_meme_ideas(state)

        self.assertEqual(result, [])
        mock_get_model.assert_not_called()

    @patch("app.agents.creative.get_openai_model")
    def test_mismatched_number_of_ideas(self, mock_get_model):

        mock_model = MagicMock()
        mock_structured_model = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.with_structured_output.return_value = mock_structured_model

        mock_result = MagicMock()
        mock_result.ideas = []

        mock_structured_model.invoke.return_value = mock_result

        state = {
            "ranked_trends": [
                {
                    "topic": "Calcio",
                    "score": 8.5
                }
            ]
        }

        with self.assertRaises(ValueError):
            generate_meme_ideas(state)


if __name__ == "__main__":
    unittest.main()
