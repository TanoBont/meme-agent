
import unittest
from unittest.mock import patch

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
                "description": "Meme sulla tecnologia",
                "score": 8.5
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

        generated_ideas = [
            {
                "topic": "Calcio",
                "text_top": "QUANDO LA TUA SQUADRA SEGNA",
                "text_bottom": "MA IL VAR ANNULLA TUTTO",
                "description": "Meme ironico sul calcio",
                "score": 9.0
            }
        ]

        evaluated_ideas = [
            {
                **generated_ideas[0],
                "evaluation_score": 9.5,
                "approved": True
            }
        ]

        # Simula Creative ed Evaluator senza chiamare OpenAI
        with patch(
            "app.graph.workflow.generate_meme_ideas",
            return_value=generated_ideas
        ), patch(
            "app.graph.workflow.evaluate_meme_ideas",
            return_value=evaluated_ideas
        ):

            result = graph.invoke(initial_state)

        self.assertGreater(len(result["meme_ideas"]), 0)

        for idea in result["meme_ideas"]:
            self.assertTrue(idea["approved"])

        self.assertEqual(result["revision_count"], 0)

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

        # Prima valutazione: meme non approvato
        first_evaluation = [
            {
                "topic": "Calcio",
                "text_top": "QUANDO VINCI",
                "text_bottom": "",
                "description": "Meme sulla tecnologia",
                "score": 8.5,
                "evaluation_score": 5.0,
                "approved": False
            }
        ]

        # Seconda valutazione: meme approvato
        second_evaluation = [
            {
                "topic": "Calcio",
                "text_top": "QUANDO LA TUA SQUADRA SEGNA",
                "text_bottom": "MA IL VAR ANNULLA TUTTO",
                "description": "Meme ironico sul calcio",
                "score": 8.5,
                "evaluation_score": 10.0,
                "approved": True
            }
        ]

        revised_ideas = [
            {
                **first_evaluation[0],
                "text_top": "QUANDO LA TUA SQUADRA SEGNA",
                "text_bottom": "MA IL VAR ANNULLA TUTTO",
                "description": "Meme ironico sul calcio"
            }
        ]

        # Simula Evaluator e Revision
        with patch(
            "app.graph.workflow.evaluate_meme_ideas",
            side_effect=[first_evaluation, second_evaluation]
        ) as mock_evaluator, patch(
            "app.graph.workflow.revise_meme_ideas",
            return_value=revised_ideas
        ) as mock_revision:

            result = test_graph.invoke(initial_state)

        self.assertEqual(result["revision_count"], 1)
        self.assertTrue(result["meme_ideas"][0]["approved"])
        self.assertEqual(result["meme_ideas"][0]["evaluation_score"], 10.0)

        self.assertEqual(mock_evaluator.call_count, 2)
        mock_revision.assert_called_once()


if __name__ == "__main__":
    unittest.main()
