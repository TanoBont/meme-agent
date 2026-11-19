
import unittest

from app.agents.research import research_trends
from app.config import MAX_TRENDS


class TestResearchLive(unittest.TestCase):

    def test_research_with_tavily(self):

        result = research_trends()

        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), MAX_TRENDS)

        urls = []

        for trend in result:
            self.assertTrue(trend["topic"])
            self.assertTrue(trend["description"])
            self.assertTrue(trend["url"])
            self.assertIn(
                trend["content_type"],
                ["current", "evergreen"]
            )

            urls.append(trend["url"])

        # Verifica che non ci siano URL duplicati
        self.assertEqual(len(urls), len(set(urls)))

        print("\n--- RESEARCH CON TAVILY ---")
        print("Trend raccolti:", len(result))

        for index, trend in enumerate(result, start=1):
            print(f"\nTrend {index}")
            print("Argomento:", trend["topic"])
            print("Categoria:", trend["category"])
            print("Tipologia:", trend["content_type"])
            print("Data:", trend["published_date"])
            print("Fonte:", trend["source"])
            print("Descrizione:", trend["description"][:250])


if __name__ == "__main__":
    unittest.main()
