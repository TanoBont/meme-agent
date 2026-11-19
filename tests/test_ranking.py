
import unittest
from unittest.mock import patch, MagicMock

from app.agents.ranking import rank_trends


class TestRanking(unittest.TestCase):

    @patch("app.agents.ranking.get_openai_model")
    def test_rank_trends(self, mock_get_model):

        mock_model = MagicMock()
        mock_structured_model = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.with_structured_output.return_value = mock_structured_model

        first_result = MagicMock()
        first_result.actuality = 9
        first_result.interest = 8
        first_result.humor = 10
        first_result.reasoning = "Trend attuale e divertente."

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
                    "topic": "Polemiche arbitrali",
                    "description": "Discussioni sulle decisioni VAR.",
                    "verified": True,
                    "confidence": 9,
                    "category": "controversies",
                    "content_type": "current",
                    "published_date": "2026-11-19"
                },
                {
                    "topic": "Rivalità calcistiche",
                    "description": "Storiche rivalità tra tifoserie.",
                    "verified": True,
                    "confidence": 8,
                    "category": "football_culture",
                    "content_type": "evergreen",
                    "published_date": None
                },
                {
                    "topic": "Notizia non verificata",
                    "description": "Informazioni insufficienti.",
                    "verified": False,
                    "confidence": 2,
                    "category": "serie_a",
                    "content_type": "current"
                }
            ]
        }

        ranked_trends = rank_trends(state)

        # Verifica che vengano classificati solo i trend verificati
        self.assertEqual(len(ranked_trends), 2)

        # Verifica il calcolo dei punteggi
        self.assertEqual(ranked_trends[0]["score"], 9.0)
        self.assertEqual(ranked_trends[1]["score"], 6.0)

        # Verifica l'ordinamento decrescente
        self.assertGreaterEqual(
            ranked_trends[0]["score"],
            ranked_trends[1]["score"]
        )

        # Verifica i criteri di valutazione
        for trend in ranked_trends:
            self.assertIn("actuality", trend)
            self.assertIn("interest", trend)
            self.assertIn("humor", trend)
            self.assertIn("reasoning", trend)

        # Verifica la conservazione dei metadati
        self.assertEqual(
            ranked_trends[0]["category"],
            "controversies"
        )
        self.assertEqual(
            ranked_trends[0]["content_type"],
            "current"
        )
        self.assertEqual(
            ranked_trends[1]["category"],
            "football_culture"
        )
        self.assertEqual(
            ranked_trends[1]["content_type"],
            "evergreen"
        )

        # Verifica configurazione del modello
        mock_get_model.assert_called_once_with(temperature=0.2)
        mock_model.with_structured_output.assert_called_once()

        # Verifica che OpenAI venga chiamato solo per i trend verificati
        self.assertEqual(mock_structured_model.invoke.call_count, 2)

        # Verifica il contenuto dei prompt
        prompts = [
            call.args[0]
            for call in mock_structured_model.invoke.call_args_list
        ]

        self.assertIn("controversies", prompts[0])
        self.assertIn("current", prompts[0])
        self.assertIn("2026-11-19", prompts[0])
        self.assertIn("9", prompts[0])

        self.assertIn("football_culture", prompts[1])
        self.assertIn("evergreen", prompts[1])
        self.assertIn("Non disponibile", prompts[1])


if __name__ == "__main__":
    unittest.main()
