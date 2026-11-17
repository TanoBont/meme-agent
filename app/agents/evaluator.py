
from app.llms import get_openai_model

from app.agents.schemas import MemeEvaluation

from app.agents.evaluation_rules import (
    evaluate_completeness,
    evaluate_relevance,
    evaluate_readability,
    evaluate_structure
)


def evaluate_meme_ideas(state):
    """
    Valuta le idee generate dal Creative Agent
    combinando regole Python e valutazione AI.
    """

    model = get_openai_model(temperature=0.2)

    structured_model = model.with_structured_output(MemeEvaluation)

    evaluated_ideas = []

    for idea in state["meme_ideas"]:

        # Valutazione tramite regole Python
        rule_evaluation = {
            "completeness": evaluate_completeness(idea),
            "relevance": evaluate_relevance(idea),
            "readability": evaluate_readability(idea),
            "structure": evaluate_structure(idea)
        }

        rule_score = (
            rule_evaluation["completeness"] * 0.25 +
            rule_evaluation["relevance"] * 0.30 +
            rule_evaluation["readability"] * 0.25 +
            rule_evaluation["structure"] * 0.20
        )

        rule_score = round(rule_score, 2)

        # Valutazione tramite AI
        prompt = f"""
        Sei un esperto nella valutazione di meme per i social.

        Valuta il seguente meme considerando:
        - Creatività
        - Potenziale umoristico
        - Originalità

        Assegna a ciascun criterio un punteggio da 1 a 10.

        ARGOMENTO: {idea["topic"]}
        TESTO SUPERIORE: {idea["text_top"]}
        TESTO INFERIORE: {idea["text_bottom"]}
        DESCRIZIONE: {idea["description"]}

        Valuta il meme in modo critico e imparziale.
        """

        ai_result = structured_model.invoke(prompt)

        ai_evaluation = ai_result.model_dump()

        ai_score = (
            ai_evaluation["creativity"] * 0.4 +
            ai_evaluation["humor"] * 0.4 +
            ai_evaluation["originality"] * 0.2
        )

        ai_score = round(ai_score, 2)

        # Combinazione dei punteggi
        final_score = round(
            rule_score * 0.6 + ai_score * 0.4,
            2
        )

        evaluation = {
            **rule_evaluation,
            **ai_evaluation,
            "rule_score": rule_score,
            "ai_score": ai_score
        }

        evaluated_idea = {
            **idea,
            "evaluation": evaluation,
            "evaluation_score": final_score,
            "approved": final_score >= 7
        }

        evaluated_ideas.append(evaluated_idea)

    return evaluated_ideas
