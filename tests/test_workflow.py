
import unittest

from langgraph.graph import StateGraph, START, END

from app.graph.state import MemeAgentState

from app.graph.workflow import (
    graph,
    evaluator_node,
    revision_node,
    should_revise
)


def creative_node_problematic(state: MemeAgentState):
    """
    Genera intenzionalmente un meme incompleto
    per verificare il ciclo di revisione.
    """
    return {
        "meme_ideas": [
            {
                "topic": "Calcio",
                "text_top": "QUANDO VINCI",
                "text_bottom": "",
                "description": "Meme sulla tecnologia"
            }
        ]
    }


class TestWorkflow(unittest.TestCase):

    def test_workflow_completo(self):
        initial_state = {
            "trends": [],
            "verified_trends": [],
            "ranked_trends": [],
            "meme_ideas": [],
            "revision_count": 0
        }

        result = graph.invoke(initial_state)

        self.assertGreater(len(result["meme_ideas"]), 0)

        for idea in result["meme_ideas"]:
            self.assertTrue(idea["approved"])

        self.assertLessEqual(result["revision_count"], 2)

    def test_workflow_con_revisione(self):

        builder = StateGraph(MemeAgentState)

        builder.add_node("creative", creative_node_problematic)
        builder.add_node("evaluator", evaluator_node)
        builder.add_node("revision", revision_node)

        builder.add_edge(START, "creative")
        builder.add_edge("creative", "evaluator")

        builder.add_conditional_edges(
            "evaluator",
            should_revise,
            {
                "revise": "revision",
                "end": END
            }
        )

        builder.add_edge("revision", "evaluator")

        test_graph = builder.compile()

        initial_state = {
            "trends": [],
            "verified_trends": [],
            "ranked_trends": [],
            "meme_ideas": [],
            "revision_count": 0
        }

        result = test_graph.invoke(initial_state)

        self.assertEqual(result["revision_count"], 1)
        self.assertTrue(result["meme_ideas"][0]["approved"])
        self.assertEqual(result["meme_ideas"][0]["evaluation_score"], 10.0)


if __name__ == "__main__":
    unittest.main()
