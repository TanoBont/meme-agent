
import unittest
from unittest.mock import patch, MagicMock

from app.tools.search import search_web


class TestSearch(unittest.TestCase):

    @patch("app.tools.search.get_tavily_client")
    def test_search_web_success(self, mock_get_client):

        mock_client = MagicMock()

        mock_client.search.return_value = {
            "results": [
                {
                    "title": "Serie A",
                    "content": "Ultime notizie calcistiche.",
                    "url": "https://example.com/serie-a"
                }
            ]
        }

        mock_get_client.return_value = mock_client

        results = search_web("ultime notizie Serie A", max_results=2)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Serie A")

        mock_client.search.assert_called_once_with(
            query="ultime notizie Serie A",
            search_depth="basic",
            max_results=2
        )

    @patch("app.tools.search.get_tavily_client")
    def test_search_web_connection_error(self, mock_get_client):

        mock_client = MagicMock()
        mock_client.search.side_effect = ConnectionError(
            "Errore di connessione"
        )

        mock_get_client.return_value = mock_client

        results = search_web("ultime notizie Serie A")

        self.assertEqual(results, [])

    @patch("app.tools.search.get_tavily_client")
    def test_search_web_missing_results(self, mock_get_client):

        mock_client = MagicMock()
        mock_client.search.return_value = {}

        mock_get_client.return_value = mock_client

        results = search_web("ultime notizie Serie A")

        self.assertEqual(results, [])

    @patch("app.tools.search.get_tavily_client")
    def test_search_web_missing_api_key(self, mock_get_client):

        mock_get_client.side_effect = ValueError(
            "TAVILY_API_KEY non configurata"
        )

        results = search_web("ultime notizie Serie A")

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
