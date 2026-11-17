
import unittest
from unittest.mock import patch, MagicMock

from app.graph.workflow import (
    evaluator_node,
    revision_node,
    should_revise
)

from app.agents.revision import revise_meme_ideas


class TestRevision(unittest.TestCase):

    def test_max_revisions(self):
        state = {
            "revision_count": 2,
            "meme_ideas": [
                {
                    "approved": False
                }
            ]
        }

        self.assertEqual(should_revise(state), "end")

    @patch("app.agents.revision.get_openai_model")
    @patch("app.agents.evaluator.get_openai_model")
    def test_revision_cycle(self, mock_evaluator_model, mock_revision_model):

        # Mock dell'Evaluator
        evaluator = MagicMock()
        structured_evaluator = MagicMock()

        mock_evaluator_model.return_value = evaluator
        evaluator.with_structured_output.return_value = structured_evaluator

        evaluation_result = MagicMock()
        evaluation_result.model_dump.return_value = {
            "creativity": 9,
            "humor": 9,
            "originality": 9,
            "feedback": "Meme creativo e divertente"
        }

        structured_evaluator.invoke.return_value = evaluation_result

        # Mock del Revision Agent
        revision = MagicMock()
        structured_revision = MagicMock()

        mock_revision_model.return_value = revision
        revision.with_structured_output.return_value = structured_revision

        revision_result = MagicMock()
        revision_result.model_dump.return_value = {
            "text_top": "QUANDO LA TUA SQUADRA SEGNA",
            "text_bottom": "MA L'ARBITRO ANNULLA IL GOL",
            "description": "Meme ironico sulle partite di calcio"
        }

        structured_revision.invoke.return_value = revision_result

        state = {
            "trends": [],
            "verified_trends": [],
            "ranked_trends": [],
            "revision_count": 0,
            "meme_ideas": [
                {
                    "topic": "Calcio",
                    "score": 8.5,
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
        self.assertEqual(
            state["meme_ideas"][0]["text_top"],
            "QUANDO LA TUA SQUADRA SEGNA"
        )

        state.update(evaluator_node(state))

        self.assertTrue(state["meme_ideas"][0]["approved"])
        self.assertEqual(should_revise(state), "end")

        structured_revision.invoke.assert_called_once()
        self.assertEqual(structured_evaluator.invoke.call_count, 2)

    @patch("app.agents.revision.get_openai_model")
    def test_revision_relevance(self, mock_get_model):

        mock_model = MagicMock()
        mock_structured_model = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.with_structured_output.return_value = mock_structured_model

        mock_result = MagicMock()
        mock_result.model_dump.return_value = {
            "text_top": "QUANDO LA TUA SQUADRA SEGNA",
            "text_bottom": "MA IL VAR ANNULLA TUTTO",
            "description": "Meme ironico sul calcio"
        }

        mock_structured_model.invoke.return_value = mock_result

        state = {
            "meme_ideas": [
                {
                    "topic": "Calcio",
                    "score": 8.5,
                    "text_top": "QUANDO PENSI AL METEO",
                    "text_bottom": "MA PIOVE",
                    "description": "Meme sul tempo atmosferico",
                    "evaluation": {
                        "completeness": 10,
                        "relevance": 4,
                        "readability": 10,
                        "structure": 10,
                        "feedback": "Il meme non è pertinente"
                    },
                    "evaluation_score": 8.2,
                    "approved": False
                }
            ]
        }

        revised_ideas = revise_meme_ideas(state)
        revised_idea = revised_ideas[0]

        self.assertIn("calcio", revised_idea["description"])
        self.assertEqual(revised_idea["score"], 8.5)
        self.assertFalse(revised_idea["approved"])

        mock_structured_model.invoke.assert_called_once()

    @patch("app.agents.revision.get_openai_model")
    def test_approved_idea_unchanged(self, mock_get_model):

        idea = {
            "topic": "Calcio",
            "text_top": "TESTO SUPERIORE",
            "text_bottom": "TESTO INFERIORE",
            "description": "Meme sul calcio",
            "approved": True
        }

        state = {
            "meme_ideas": [idea]
        }

        result = revise_meme_ideas(state)

        self.assertEqual(result[0], idea)
        mock_get_model.assert_not_called()

if __name__ == "__main__":
    unittest.main()
