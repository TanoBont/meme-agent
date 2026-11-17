
import unittest

from app.graph.workflow import (
    evaluator_node,
    revision_node,
    should_revise
)

from app.agents.revision import revise_meme_ideas


class TestRevision(unittest.TestCase):

    def test_revision_cycle(self):
        state = {
            "trends": [],
            "verified_trends": [],
            "ranked_trends": [],
            "revision_count": 0,
            "meme_ideas": [
                {
                    "topic": "Calcio",
                    "text_top": "QUANDO VINCI",
                    "text_bottom": "",
                    "description": "Meme sulla tecnologia"
                }
            ]
        }

        state.update(evaluator_node(state))

        self.assertFalse(state["meme_ideas"][0]["approved"])
        self.assertEqual(should_revise(state), "revise")

        state.update(revision_node(state))

        self.assertEqual(state["revision_count"], 1)

        state.update(evaluator_node(state))

        self.assertTrue(state["meme_ideas"][0]["approved"])
        self.assertEqual(should_revise(state), "end")

    def test_revision_relevance(self):
        state = {
            "meme_ideas": [
                {
                    "topic": "Calcio",
                    "text_top": "QUANDO PENSI AL METEO",
                    "text_bottom": "MA PIOVE",
                    "description": "Meme sul tempo atmosferico",
                    "evaluation": {
                        "completeness": 10,
                        "relevance": 4,
                        "readability": 10,
                        "structure": 10
                    },
                    "evaluation_score": 8.2,
                    "approved": False
                }
            ]
        }

        revised_ideas = revise_meme_ideas(state)
        revised_idea = revised_ideas[0]

        self.assertIn("CALCIO", revised_idea["text_top"])
        self.assertIn("Calcio", revised_idea["description"])


if __name__ == "__main__":
    unittest.main()
