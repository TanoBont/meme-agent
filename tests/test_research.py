
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
                    "url": "https://EXAMPLE.com/serie-a/"
                }
            ]
        ]

        trends = research_trends()

        # Verifica risultati validi e unici
        self.assertEqual(len(trends), 5)

        urls = [trend["url"] for trend in trends]
        self.assertEqual(len(urls), len(set(urls)))

        # Verifica categorie
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

        # Verifica tipologie di contenuto
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

        # Verifica campi dei risultati
        for trend in trends:
            self.assertTrue(trend["topic"])
            self.assertTrue(trend["description"])
            self.assertTrue(trend["url"])
            self.assertEqual(trend["source"], trend["url"])
            self.assertIn("category", trend)
            self.assertIn("content_type", trend)
            self.assertIn("published_date", trend)

        # Verifica data di pubblicazione
        self.assertEqual(
            trends[0]["published_date"],
            "2026-11-19"
        )

        # Verifica numero di ricerche
        self.assertEqual(mock_search.call_count, 5)

        # Verifica numero massimo di risultati per query
        for call in mock_search.call_args_list:
            self.assertEqual(call.kwargs["max_results"], 2)

    @patch("app.agents.research.search_web")
    def test_collects_up_to_ten_trends(self, mock_search):

        mock_search.side_effect = [
            [
                {
                    "title": f"Trend {category}_{i}",
                    "content": f"Descrizione {category}_{i}",
                    "url": f"https://example.com/{category}_{i}"
                }
                for i in range(2)
            ]
            for category in range(5)
        ]

        trends = research_trends()

        # Verifica raccolta di 10 trend
        self.assertEqual(len(trends), 10)
        self.assertEqual(mock_search.call_count, 5)

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
            "sfottò"
        ]

        self.assertEqual(len(queries), 5)

        for query, keyword in zip(queries, expected_keywords):
            self.assertIn(keyword, query.lower())

        # Verifica che le query contengano un riferimento temporale
        for query in queries[:4]:
            self.assertTrue(any(char.isdigit() for char in query))

    @patch("app.agents.research.search_web")
    def test_search_removes_incomplete_results(self, mock_search):

        mock_search.side_effect = [
            [
                {
                    "title": "Trend valido",
                    "content": "Descrizione valida.",
                    "url": "https://example.com/valid"
                },
                {
                    "title": "Trend senza descrizione",
                    "content": "",
                    "url": "https://example.com/incomplete"
                },
                {
                    "title": "Trend senza URL",
                    "content": "Descrizione disponibile."
                }
            ],
            [],
            [],
            [],
            []
        ]

        trends = research_trends()

        self.assertEqual(len(trends), 1)
        self.assertEqual(trends[0]["topic"], "Trend valido")


if __name__ == "__main__":
    unittest.main()
