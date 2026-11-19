
import unittest

from app.agents.revision import revise_meme_ideas


class TestRevisionLive(unittest.TestCase):

    def test_revision_with_gpt6(self):

        original_idea = {
            "topic": "Polemiche arbitrali",
            "text_top": "QUANDO LA TUA SQUADRA SEGNA",
            "text_bottom": "MA IL VAR HA ALTRI PROGRAMMI",
            "description": (
                "Un tifoso esulta per un gol che viene "
                "successivamente annullato dal VAR."
            ),
            "score": 8.5,
            "category": "controversies",
            "content_type": "current",
            "approved": False,
            "evaluation_score": 5.8,
            "evaluation": {
                "creativity": 4,
                "humor": 5,
                "originality": 3,
                "feedback": (
                    "Il meme è troppo generico e prevedibile. "
                    "La battuta non presenta un elemento "
                    "particolarmente originale."
                )
            }
        }

        state = {
            "meme_ideas": [original_idea]
        }

        result = revise_meme_ideas(state)

        self.assertEqual(len(result), 1)

        revised_idea = result[0]

        # Verifica la struttura della revisione
        self.assertTrue(revised_idea["text_top"])
        self.assertTrue(revised_idea["text_bottom"])
        self.assertTrue(revised_idea["description"])

        # Verifica la conservazione dei metadati
        self.assertEqual(revised_idea["topic"], original_idea["topic"])
        self.assertEqual(revised_idea["category"], "controversies")
        self.assertEqual(revised_idea["content_type"], "current")
        self.assertEqual(revised_idea["score"], 8.5)

        # Verifica che la revisione abbia modificato almeno un campo
        self.assertTrue(
            revised_idea["text_top"] != original_idea["text_top"]
            or revised_idea["text_bottom"] != original_idea["text_bottom"]
            or revised_idea["description"] != original_idea["description"]
        )

        print("\n--- REVISION CON GPT-6.1 SOL ---")
        print("Argomento:", revised_idea["topic"])
        print("Testo originale:", original_idea["text_top"])
        print("Conclusione originale:", original_idea["text_bottom"])
        print("\nTesto revisionato:", revised_idea["text_top"])
        print("Conclusione revisionata:", revised_idea["text_bottom"])
        print("Descrizione:", revised_idea["description"])


if __name__ == "__main__":
    unittest.main()
