
import unittest
from unittest.mock import patch

from app.agents.research import research_trends


class TestResearch(unittest.TestCase):

    @patch("app.agents.research.search_web")
    def test_research_trends(self, mock_search):

        # Simula i risultati restituiti da Tavily
        mock_search.side_effect = [
            [
                {
                    "title": "Nuovi sviluppi AI",
                    "content": "Nuovi strumenti di intelligenza artificiale.",
                    "url": "https://example.com/ai"
                }
            ],
            [
                {
                    "title": "Ultime notizie calcio",
                    "content": "Discussioni sul campionato.",
                    "url": "https://example.com/calcio"
                }
            ],
            [
                {
                    "title": "Trend social",
                    "content": "Nuovi argomenti virali.",
                    "url": "https://example.com/social"
                }
            ]
        ]

        trends = research_trends()

        # Verifica che siano stati raccolti tre risultati
        self.assertEqual(len(trends), 3)

        # Verifica il contenuto dei risultati
        self.assertEqual(trends[0]["topic"], "Nuovi sviluppi AI")
        self.assertEqual(trends[1]["topic"], "Ultime notizie calcio")
        self.assertEqual(trends[2]["topic"], "Trend social")

        # Verifica che ogni risultato contenga una fonte
        for trend in trends:
            self.assertIn("url", trend)
            self.assertIn("source", trend)
            self.assertIn("description", trend)

        # Verifica che Tavily sia stato chiamato tre volte
        self.assertEqual(mock_search.call_count, 3)


if __name__ == "__main__":
    unittest.main()
