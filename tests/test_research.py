
import unittest
from unittest.mock import patch

from app.agents.research import research_trends


class TestResearch(unittest.TestCase):

    @patch("app.agents.research.search_web")
    def test_research_trends(self, mock_search):

        mock_search.side_effect = [
            [
                {
                    "title": "Risultati Serie A",
                    "content": "Risultati dell'ultima giornata.",
                    "url": "https://example.com/serie-a",
                    "published_date": "2026-11-19"
                },
                {
                    "title": "Articolo incompleto",
                    "content": "",
                    "url": "https://example.com/incompleto"
                }
            ],
            [
                {
                    "title": "Calciomercato",
                    "content": "Ultime trattative di mercato.",
                    "url": "https://example.com/mercato"
                }
            ],
            [
                {
                    "title": "Champions League",
                    "content": "Notizie sulle competizioni europee.",
                    "url": "https://example.com/champions"
                }
            ],
            [
                {
                    "title": "Polemiche VAR",
                    "content": "Discussioni sulle decisioni arbitrali.",
                    "url": "https://example.com/var"
                }
            ],
            [
                {
                    "title": "Momenti virali",
                    "content": "Meme e rivalità calcistiche.",
                    "url": "https://example.com/virali"
                },
                {
                    "title": "Risultati Serie A",
                    "content": "Risultato duplicato.",
                    "url": "https://example.com/serie-a"
                }
            ]
        ]

        trends = research_trends()

        # Verifica risultati validi e unici
        self.assertEqual(len(trends), 5)

        urls = [trend["url"] for trend in trends]
        self.assertEqual(len(urls), len(set(urls)))

        # Verifica le categorie
        self.assertEqual(
            [trend["category"] for trend in trends],
            [
                "serie_a",
                "calciomercato",
                "champions_league",
                "controversies",
                "football_culture"
            ]
        )

        # Verifica le tipologie di contenuto
        self.assertEqual(
            [trend["content_type"] for trend in trends],
            [
                "current",
                "current",
                "current",
                "current",
                "evergreen"
            ]
        )

        # Verifica i campi dei risultati
        for trend in trends:
            self.assertTrue(trend["topic"])
            self.assertTrue(trend["description"])
            self.assertTrue(trend["url"])
            self.assertEqual(trend["source"], trend["url"])
            self.assertIn("category", trend)
            self.assertIn("content_type", trend)
            self.assertIn("published_date", trend)

        # Verifica la data di pubblicazione
        self.assertEqual(
            trends[0]["published_date"],
            "2026-11-19"
        )

        # Verifica che le ricerche siano cinque
        self.assertEqual(mock_search.call_count, 5)

        # Verifica il numero massimo di risultati per query
        for call in mock_search.call_args_list:
            self.assertEqual(call.kwargs["max_results"], 1)

    @patch("app.agents.research.search_web")
    @patch("app.agents.research.MAX_TRENDS", 3)
    def test_max_trends_limit(self, mock_search):

        mock_search.side_effect = [
            [
                {
                    "title": f"Trend {i}",
                    "content": f"Descrizione del trend {i}",
                    "url": f"https://example.com/{i}"
                }
            ]
            for i in range(1, 6)
        ]

        trends = research_trends()

        # Verifica il limite massimo configurato
        self.assertEqual(len(trends), 3)

        self.assertEqual(
            [trend["topic"] for trend in trends],
            ["Trend 1", "Trend 2", "Trend 3"]
        )

        @patch("app.agents.research.search_web")
        def test_search_queries(self, mock_search):

            mock_search.return_value = []

            research_trends()

            queries = [
                call.args[0]
                for call in mock_search.call_args_list
            ]

            expected_keywords = [
                "serie a",
                "calciomercato",
                "champions league",
                "var",
                "meme"
            ]

            self.assertEqual(len(queries), 5)

            for query, keyword in zip(queries, expected_keywords):
                self.assertIn(keyword, query.lower())

if __name__ == "__main__":
    unittest.main()
