
import unittest

from app.agents.ranking import rank_trends


class TestRankingLive(unittest.TestCase):

    def test_ranking_with_gpt6(self):

        state = {
            "verified_trends": [
                {
                    "topic": "Polemiche arbitrali in Serie A",
                    "description": (
                        "Un gol viene annullato dopo una revisione VAR, "
                        "generando proteste e discussioni tra tifosi."
                    ),
                    "category": "controversies",
                    "content_type": "current",
                    "published_date": "2026-11-19",
                    "verified": True,
                    "confidence": 9
                },
                {
                    "topic": "Rivalità storiche tra tifoserie",
                    "description": (
                        "Le rivalità tra tifoserie rappresentano "
                        "una componente storica della cultura calcistica."
                    ),
                    "category": "football_culture",
                    "content_type": "evergreen",
                    "verified": True,
                    "confidence": 9
                }
            ]
        }

        result = rank_trends(state)

        self.assertEqual(len(result), 2)

        for trend in result:
            self.assertGreaterEqual(trend["actuality"], 1)
            self.assertLessEqual(trend["actuality"], 10)

            self.assertGreaterEqual(trend["interest"], 1)
            self.assertLessEqual(trend["interest"], 10)

            self.assertGreaterEqual(trend["humor"], 1)
            self.assertLessEqual(trend["humor"], 10)

            expected_score = round(
                trend["actuality"] * 0.4 +
                trend["interest"] * 0.3 +
                trend["humor"] * 0.3,
                2
            )

            self.assertEqual(trend["score"], expected_score)
            self.assertTrue(trend["reasoning"])

        self.assertGreaterEqual(
            result[0]["score"],
            result[1]["score"]
        )

        print("\n--- RANKING CON GPT-6.1 SOL ---")

        for trend in result:
            print("\nArgomento:", trend["topic"])
            print("Attualità:", trend["actuality"])
            print("Interesse:", trend["interest"])
            print("Potenziale umoristico:", trend["humor"])
            print("Score:", trend["score"])
            print("Motivazione:", trend["reasoning"])


if __name__ == "__main__":
    unittest.main()
