
from app.llms import get_openai_model
from app.agents.schemas import MemeRevision


def revise_meme_ideas(state):
    """
    Rivede le idee non approvate utilizzando un modello linguistico.
    """

    structured_model = None

    revised_ideas = []

    for idea in state["meme_ideas"]:

        if idea["approved"]:
            revised_ideas.append(idea)
            continue

        if structured_model is None:
            model = get_openai_model(temperature=0.8)
            structured_model = model.with_structured_output(MemeRevision)

        evaluation = idea["evaluation"]

        prompt = f"""
        Sei un esperto creativo specializzato nella realizzazione di meme.

        Il tuo compito è migliorare il seguente meme, che non ha superato
        la valutazione qualitativa.

        ARGOMENTO: {idea["topic"]}
        TESTO SUPERIORE: {idea["text_top"]}
        TESTO INFERIORE: {idea["text_bottom"]}
        DESCRIZIONE: {idea["description"]}

        VALUTAZIONE:
        {evaluation}

        FEEDBACK:
        {evaluation.get("feedback", "Nessun feedback disponibile")}

        ISTRUZIONI:
        - Mantieni il collegamento con l'argomento originale.
        - Migliora creatività, umorismo e originalità.
        - Utilizza testi brevi e immediati.
        - Il testo superiore deve introdurre una situazione.
        - Il testo inferiore deve contenere una conclusione ironica.
        - Evita ripetizioni e formulazioni generiche.

        Restituisci una versione migliorata del meme.
        """

        result = structured_model.invoke(prompt)

        revised_idea = idea.copy()

        revised_idea.update(result.model_dump())

        # L'idea dovrà essere valutata nuovamente
        revised_ideas.append(revised_idea)

    return revised_ideas
