
import unittest
from unittest.mock import patch, MagicMock

from app.agents.verification import verify_trends


class TestVerification(unittest.TestCase):

    @patch("app.agents.verification.get_openai_model")
    def test_verify_trends(self, mock_get_model):

        mock_model = MagicMock()
        mock_structured_model = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.with_structured_output.return_value = mock_structured_model

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
                    "topic": "Risultati Serie A",
                    "description": "Risultati dell'ultima giornata.",
                    "url": "https://example.com/serie-a",
                    "source": "https://example.com/serie-a",
                    "category": "serie_a",
                    "content_type": "current",
                    "published_date": "2026-11-19"
                },
                {
                    "topic": "Momento virale del calcio",
                    "description": "Un episodio diventato virale.",
                    "url": "https://example.com/viral",
                    "source": "https://example.com/viral",
                    "category": "football_culture",
                    "content_type": "evergreen",
                    "published_date": None
                }
            ]
        }

        verified_trends = verify_trends(state)

        # Numero di trend restituiti
        self.assertEqual(len(verified_trends), 2)

        # Verifica primo risultato
        self.assertTrue(verified_trends[0]["verified"])
        self.assertEqual(verified_trends[0]["confidence"], 9)

        # Verifica secondo risultato
        self.assertFalse(verified_trends[1]["verified"])
        self.assertEqual(verified_trends[1]["confidence"], 3)

        # Verifica conservazione dei metadati
        self.assertEqual(
            verified_trends[0]["category"],
            "serie_a"
        )
        self.assertEqual(
            verified_trends[0]["content_type"],
            "current"
        )
        self.assertEqual(
            verified_trends[0]["published_date"],
            "2026-11-19"
        )

        self.assertEqual(
            verified_trends[1]["content_type"],
            "evergreen"
        )

        # Verifica configurazione modello
        mock_get_model.assert_called_once_with(temperature=0.1)

        # Verifica schema strutturato
        mock_model.with_structured_output.assert_called_once()

        # Verifica chiamate
        self.assertEqual(mock_structured_model.invoke.call_count, 2)

        # Verifica contenuto dei prompt
        prompts = [
            call.args[0]
            for call in mock_structured_model.invoke.call_args_list
        ]

        # Verifica nuovo ruolo del Verification Agent
        self.assertIn("valutazione preliminare", prompts[0])
        self.assertIn("Non devi certificare la veridicità", prompts[0])

        # Verifica criteri di approvazione
        self.assertIn("Non richiedere una certezza assoluta", prompts[0])
        self.assertIn("verified=True", prompts[0])

        self.assertIn("serie_a", prompts[0])
        self.assertIn("current", prompts[0])
        self.assertIn("2026-11-19", prompts[0])

        self.assertIn("football_culture", prompts[1])
        self.assertIn("evergreen", prompts[1])
        self.assertIn("Non disponibile", prompts[1])


if __name__ == "__main__":
    unittest.main()
