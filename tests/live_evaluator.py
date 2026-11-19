
import unittest

from app.agents.evaluator import evaluate_meme_ideas


class TestEvaluatorLive(unittest.TestCase):

    def test_evaluator_with_gpt6(self):

        state = {
            "meme_ideas": [
                {
                    "topic": "Polemiche arbitrali",
                    "text_top": "QUANDO LA TUA SQUADRA SEGNA",
                    "text_bottom": "MA IL VAR HA ALTRI PROGRAMMI",
                    "description": (
                        "Un tifoso esulta per il gol della propria "
                        "squadra, ma l'arbitro viene richiamato "
                        "al monitor VAR e annulla la rete."
                    ),
                    "score": 8.5,
                    "category": "controversies",
                    "content_type": "current"
                }
            ]
        }

        result = evaluate_meme_ideas(state)

        self.assertEqual(len(result), 1)

        idea = result[0]
        evaluation = idea["evaluation"]

        # Verifica punteggi AI
        for criterion in ["creativity", "humor", "originality"]:
            self.assertGreaterEqual(evaluation[criterion], 1)
            self.assertLessEqual(evaluation[criterion], 10)

        # Verifica punteggi delle regole
        for criterion in [
            "completeness",
            "relevance",
            "readability",
            "structure"
        ]:
            self.assertGreaterEqual(evaluation[criterion], 1)
            self.assertLessEqual(evaluation[criterion], 10)

        # Verifica calcolo AI
        expected_ai_score = round(
            evaluation["creativity"] * 0.4 +
            evaluation["humor"] * 0.4 +
            evaluation["originality"] * 0.2,
            2
        )

        self.assertEqual(evaluation["ai_score"], expected_ai_score)

        # Verifica calcolo finale
        expected_final_score = round(
            evaluation["rule_score"] * 0.6 +
            evaluation["ai_score"] * 0.4,
            2
        )

        self.assertEqual(
            idea["evaluation_score"],
            expected_final_score
        )

        self.assertEqual(
            idea["approved"],
            expected_final_score >= 7
        )

        print("\n--- EVALUATOR CON GPT-6.1 SOL ---")
        print("Argomento:", idea["topic"])
        print("Creatività:", evaluation["creativity"])
        print("Umorismo:", evaluation["humor"])
        print("Originalità:", evaluation["originality"])
        print("Rule score:", evaluation["rule_score"])
        print("AI score:", evaluation["ai_score"])
        print("Punteggio finale:", idea["evaluation_score"])
        print("Approvato:", idea["approved"])


if __name__ == "__main__":
    unittest.main()
