
import unittest

from app.agents.creative import generate_meme_ideas


class TestCreativeLive(unittest.TestCase):

    def test_creative_with_gpt6(self):

        state = {
            "ranked_trends": [
                {
                    "topic": "Polemiche arbitrali",
                    "description": (
                        "Il VAR annulla un gol durante una partita "
                        "dopo una revisione al monitor."
                    ),
                    "category": "controversies",
                    "content_type": "current",
                    "score": 8.5
                }
            ]
        }

        result = generate_meme_ideas(state)

        self.assertEqual(len(result), 1)

        idea = result[0]

        self.assertTrue(idea["topic"])
        self.assertTrue(idea["text_top"])
        self.assertTrue(idea["text_bottom"])
        self.assertTrue(idea["description"])

        self.assertEqual(idea["category"], "controversies")
        self.assertEqual(idea["content_type"], "current")

        print("\n--- MEME GENERATO CON GPT-6.1 SOL ---")
        print("Argomento:", idea["topic"])
        print("Testo superiore:", idea["text_top"])
        print("Testo inferiore:", idea["text_bottom"])
        print("Descrizione:", idea["description"])
        print("Categoria:", idea["category"])
        print("Punteggio trend:", idea["score"])


if __name__ == "__main__":
    unittest.main()
