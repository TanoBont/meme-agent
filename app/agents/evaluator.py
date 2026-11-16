
def evaluate_meme_ideas(state):
    """
    Valuta le idee generate dal Creative Agent.
    Per ora utilizza una valutazione simulata.
    """

    evaluated_ideas = []

    for idea in state["meme_ideas"]:

        # Punteggio simulato
        evaluation_score = 8

        evaluated_idea = {
            **idea,
            "evaluation_score": evaluation_score,
            "approved": evaluation_score >= 7
        }

        evaluated_ideas.append(evaluated_idea)

    # Aggiorniamo lo State
    state["meme_ideas"] = evaluated_ideas

    return state
