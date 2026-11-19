
from app.llms import get_openai_model
from app.agents.schemas import MemeIdeas


def generate_meme_ideas(state):
    """
    Genera idee per meme calcistici utilizzando OpenAI.
    """

    trends = state["ranked_trends"]

    # Evitiamo chiamate inutili se non ci sono trend
    if not trends:
        return []

    model = get_openai_model(temperature=0.9)
    structured_model = model.with_structured_output(MemeIdeas)

    prompt = f"""
    Sei un creativo specializzato nella realizzazione di meme
    sul calcio italiano ed europeo.

    Il tuo compito è generare un'idea di meme per ciascuno
    dei seguenti trend, rispettando il contesto fornito.

    TREND:
    {trends}

    REGOLE GENERALI:

    - Scrivi esclusivamente in italiano.
    - Utilizza un tono ironico, divertente e riconoscibile
      dagli appassionati di calcio.
    - Mantieni ogni meme pertinente al trend di riferimento.
    - Utilizza testi brevi, immediati e adatti ai social.
    - Il testo superiore deve introdurre una situazione.
    - Il testo inferiore deve contenere una conclusione ironica.
    - Evita di ripetere la stessa struttura narrativa.
    - Non inventare risultati, dichiarazioni o episodi
      che non siano presenti nelle informazioni fornite.

    STILI CREATIVI:

    Puoi utilizzare, alternandoli quando opportuno:
    - Sfottò tra squadre e tifoserie.
    - Situazioni paradossali legate alle partite.
    - Ironia su allenatori, giocatori e arbitri.
    - Battute sul calciomercato.
    - Rivalità e luoghi comuni del mondo calcistico.
    - Situazioni tipiche vissute dai tifosi.

    ATTUALITÀ ED EVERGREEN:

    - Per i trend CURRENT, sfrutta gli elementi legati
      agli eventi recenti.
    - Per i trend EVERGREEN, utilizza situazioni e dinamiche
      riconoscibili della cultura calcistica.

    Restituisci esattamente un'idea per ciascun trend,
    mantenendo lo stesso ordine dei trend ricevuti.
    """

    result = structured_model.invoke(prompt)

    # Controlliamo che sia stata generata un'idea per ogni trend
    if len(result.ideas) != len(trends):
        raise ValueError(
            "Il numero di idee generate non corrisponde "
            "al numero di trend ricevuti."
        )

    meme_ideas = []

    for trend, idea in zip(trends, result.ideas):
        meme_idea = idea.model_dump()

        meme_idea["score"] = trend["score"]
        meme_idea["category"] = trend.get("category", "serie_a")
        meme_idea["content_type"] = trend.get("content_type", "current")

        meme_ideas.append(meme_idea)

    return meme_ideas
