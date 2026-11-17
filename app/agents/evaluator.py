
from app.agents.evaluation_rules import (
    evaluate_completeness,
    evaluate_relevance,
    evaluate_readability,
    evaluate_structure
)


def evaluate_meme_ideas(state):
    """
    Valuta le idee generate dal Creative Agent
    attraverso diversi criteri.
    """

    evaluated_ideas = []

    for idea in state["meme_ideas"]:

        # Valutazione dei singoli criteri
        evaluation = {
            "completeness": evaluate_completeness(idea),
            "relevance": evaluate_relevance(idea),
            "readability": evaluate_readability(idea),
            "structure": evaluate_structure(idea)
        }

        # Pesi assegnati ai criteri
        score = (
            evaluation["completeness"] * 0.25 +
            evaluation["relevance"] * 0.30 +
            evaluation["readability"] * 0.25 +
            evaluation["structure"] * 0.20
        )

        evaluation_score = round(score, 2)

        evaluated_idea = {
            **idea,
            "evaluation": evaluation,
            "evaluation_score": evaluation_score,
            "approved": evaluation_score >= 7
        }

        evaluated_ideas.append(evaluated_idea)

    return evaluated_ideas
