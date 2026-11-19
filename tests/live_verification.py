
import unittest

from app.agents.verification import verify_trends
from app.agents.research import research_trends


class TestVerificationLive(unittest.TestCase):

    def test_verification_with_gpt6(self):

        state = {
            "trends": [
                {
                    "topic": "Polemiche arbitrali durante una partita di Serie A",
                    "description": (
                        "L'arbitro annulla un gol dopo aver consultato "
                        "il monitor VAR. L'episodio genera proteste "
                        "da parte dei giocatori e dei tifosi."
                    ),
                    "source": "Test di verifica",
                    "url": "https://example.com/test",
                    "category": "controversies",
                    "content_type": "current",
                    "published_date": "2026-11-19"
                }
            ]
        }

        result = verify_trends(state)

        self.assertEqual(len(result), 1)

        trend = result[0]

        self.assertIsInstance(trend["verified"], bool)
        self.assertGreaterEqual(trend["confidence"], 1)
        self.assertLessEqual(trend["confidence"], 10)
        self.assertTrue(trend["reasoning"])

        self.assertEqual(trend["category"], "controversies")
        self.assertEqual(trend["content_type"], "current")

        print("\n--- VERIFICATION CON GPT-6.1 SOL ---")
        print("Argomento:", trend["topic"])
        print("Verificato:", trend["verified"])
        print("Confidenza:", trend["confidence"])
        print("Motivazione:", trend["reasoning"])

    def test_verification_with_tavily(self):

        trends = research_trends()

        self.assertGreater(len(trends), 0)

        state = {
            "trends": trends
        }

        result = verify_trends(state)

        self.assertEqual(len(result), len(trends))

        print("\n--- VERIFICATION DEI TREND REALI ---")

        for index, trend in enumerate(result, start=1):

            self.assertIsInstance(trend["verified"], bool)
            self.assertGreaterEqual(trend["confidence"], 1)
            self.assertLessEqual(trend["confidence"], 10)
            self.assertTrue(trend["reasoning"])

            print(f"\nTrend {index}")
            print("Argomento:", trend["topic"])
            print("Categoria:", trend["category"])
            print("Verificato:", trend["verified"])
            print("Confidenza:", trend["confidence"])
            print("Motivazione:", trend["reasoning"])


if __name__ == "__main__":
    unittest.main()
