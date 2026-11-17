
import unittest
from unittest.mock import patch, MagicMock

from app.agents.ranking import rank_trends


class TestRanking(unittest.TestCase):

    @patch("app.agents.ranking.get_openai_model")
    def test_rank_trends(self, mock_get_model):

        # Simuliamo il modello OpenAI
        mock_model = MagicMock()
        mock_structured_model = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.with_structured_output.return_value = mock_structured_model

        # Simuliamo le risposte del modello
        first_result = MagicMock()
        first_result.actuality = 9
        first_result.interest = 8
        first_result.humor = 10
        first_result.reasoning = "Trend attuale e con alto potenziale umoristico."

        second_result = MagicMock()
        second_result.actuality = 6
        second_result.interest = 7
        second_result.humor = 5
        second_result.reasoning = "Trend interessante ma meno adatto ai meme."

        mock_structured_model.invoke.side_effect = [
            first_result,
            second_result
        ]

        state = {
            "verified_trends": [
                {
                    "topic": "Intelligenza artificiale",
                    "description": "Nuovi strumenti AI.",
                    "verified": True
                },
                {
                    "topic": "Calcio",
                    "description": "Discussioni sul campionato.",
                    "verified": True
                }
            ]
        }

        ranked_trends = rank_trends(state)

        # Verifica il numero di trend
        self.assertEqual(len(ranked_trends), 2)

        # Verifica il calcolo dei punteggi
        self.assertEqual(ranked_trends[0]["score"], 9.0)
        self.assertEqual(ranked_trends[1]["score"], 6.0)

        # Verifica l'ordinamento
        self.assertGreaterEqual(
            ranked_trends[0]["score"],
            ranked_trends[1]["score"]
        )

        # Verifica la presenza dei criteri
        for trend in ranked_trends:
            self.assertIn("actuality", trend)
            self.assertIn("interest", trend)
            self.assertIn("humor", trend)
            self.assertIn("reasoning", trend)

        # Verifica le chiamate al modello
        mock_get_model.assert_called_once_with(temperature=0.2)
        self.assertEqual(mock_structured_model.invoke.call_count, 2)


if __name__ == "__main__":
    unittest.main()
