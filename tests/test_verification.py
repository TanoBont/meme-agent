
import unittest
from unittest.mock import patch, MagicMock

from app.agents.verification import verify_trends


class TestVerification(unittest.TestCase):

    @patch("app.agents.verification.get_openai_model")
    def test_verify_trends(self, mock_get_model):

        # Simula il modello OpenAI
        mock_model = MagicMock()
        mock_structured_model = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.with_structured_output.return_value = mock_structured_model

        # Simula le risposte del modello
        first_result = MagicMock()
        first_result.verified = True
        first_result.confidence = 9
        first_result.reasoning = "Informazioni sufficientemente supportate."

        second_result = MagicMock()
        second_result.verified = False
        second_result.confidence = 3
        second_result.reasoning = "Informazioni insufficienti."

        mock_structured_model.invoke.side_effect = [
            first_result,
            second_result
        ]

        state = {
            "trends": [
                {
                    "topic": "Intelligenza artificiale",
                    "description": "Nuovi strumenti AI.",
                    "url": "https://example.com/ai",
                    "source": "https://example.com/ai"
                },
                {
                    "topic": "Calcio",
                    "description": "Discussioni sul campionato.",
                    "url": "https://example.com/calcio",
                    "source": "https://example.com/calcio"
                }
            ]
        }

        verified_trends = verify_trends(state)

        # Verifica il numero di trend restituiti
        self.assertEqual(len(verified_trends), 2)

        # Verifica il primo trend
        self.assertTrue(verified_trends[0]["verified"])
        self.assertEqual(verified_trends[0]["confidence"], 9)
        self.assertEqual(
            verified_trends[0]["reasoning"],
            "Informazioni sufficientemente supportate."
        )

        # Verifica il secondo trend
        self.assertFalse(verified_trends[1]["verified"])
        self.assertEqual(verified_trends[1]["confidence"], 3)

        # Verifica che le informazioni originali siano conservate
        self.assertEqual(
            verified_trends[0]["url"],
            "https://example.com/ai"
        )

        # Verifica le chiamate al modello
        mock_get_model.assert_called_once_with(temperature=0.1)
        self.assertEqual(mock_structured_model.invoke.call_count, 2)


if __name__ == "__main__":
    unittest.main()
