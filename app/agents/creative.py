
from app.llms import get_openai_model
from app.agents.schemas import MemeIdeas


def generate_meme_ideas(state):
    """
    Genera idee per meme utilizzando un modello linguistico.
    """

    model = get_openai_model(temperature=0.9)

    structured_model = model.with_structured_output(MemeIdeas)

    trends = state["ranked_trends"]

    prompt = f"""
    Sei un creativo specializzato nella realizzazione di meme per i social.

    Il tuo compito è generare un'idea di meme per ciascuno dei seguenti trend.

    TREND:
    {trends}

    Per ogni idea:
    - Mantieni il contenuto pertinente al trend.
    - Utilizza un tono ironico e divertente.
    - Scrivi testi brevi e adatti a un meme.
    - Il testo superiore deve introdurre una situazione.
    - Il testo inferiore deve contenere una conclusione ironica.
    - Non ripetere sempre la stessa struttura.

    Restituisci un'idea per ogni trend.
    """

    result = structured_model.invoke(prompt)

    meme_ideas = []

    for trend, idea in zip(trends, result.ideas):
        meme_idea = idea.model_dump()
        meme_idea["score"] = trend["score"]

        meme_ideas.append(meme_idea)

    return meme_ideas
