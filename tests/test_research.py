
import unittest
from unittest.mock import patch

from app.agents.research import research_trends


class TestResearch(unittest.TestCase):

    @patch("app.agents.research.search_web")
    def test_research_trends(self, mock_search):

        mock_search.side_effect = [
            [
                {
                    "title": "Nuovi sviluppi AI",
                    "content": "Nuovi strumenti di intelligenza artificiale.",
                    "url": "https://example.com/ai"
                },
                {
                    "title": "Articolo senza descrizione",
                    "content": "",
                    "url": "https://example.com/incompleto"
                }
            ],
            [
                {
                    "title": "Ultime notizie calcio",
                    "content": "Discussioni sul campionato.",
                    "url": "https://example.com/calcio"
                },
                {
                    "title": "Nuovi sviluppi AI",
                    "content": "Nuovi strumenti di intelligenza artificiale.",
                    "url": "https://example.com/ai"
                }
            ],
            [
                {
                    "title": "Trend social",
                    "content": "Nuovi argomenti virali.",
                    "url": "https://example.com/social"
                },
                {
                    "title": "",
                    "content": "Descrizione senza titolo.",
                    "url": "https://example.com/senza-titolo"
                }
            ]
        ]

        trends = research_trends()

        # Verifica che siano rimasti solo i risultati validi e unici
        self.assertEqual(len(trends), 3)

        # Verifica i titoli
        self.assertEqual(
            [trend["topic"] for trend in trends],
            [
                "Nuovi sviluppi AI",
                "Ultime notizie calcio",
                "Trend social"
            ]
        )

        # Verifica che non esistano URL duplicati
        urls = [trend["url"] for trend in trends]
        self.assertEqual(len(urls), len(set(urls)))

        # Verifica che ogni risultato contenga i campi richiesti
        for trend in trends:
            self.assertTrue(trend["topic"])
            self.assertTrue(trend["description"])
            self.assertTrue(trend["url"])
            self.assertEqual(trend["source"], trend["url"])

        # Verifica che siano state effettuate tre ricerche simulate
        self.assertEqual(mock_search.call_count, 3)


if __name__ == "__main__":
    unittest.main()
