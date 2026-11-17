
from app.llms import get_openai_model
from app.agents.schemas import TrendRanking


def rank_trends(state):
    """
    Valuta e ordina i trend verificati utilizzando OpenAI.
    """

    model = get_openai_model(temperature=0.2)
    structured_model = model.with_structured_output(TrendRanking)

    ranked_trends = []

    for trend in state["verified_trends"]:

        # Ignoriamo i trend non verificati
        if not trend["verified"]:
            continue

        prompt = f"""
        Sei un esperto di social media e creazione di meme.

        Analizza il seguente trend e assegna tre punteggi
        da 1 a 10.

        ARGOMENTO:
        {trend["topic"]}

        DESCRIZIONE:
        {trend["description"]}

        CRITERI:

        1. ATTUALITÀ:
        Quanto il trend è attuale e legato a eventi recenti?

        2. INTERESSE:
        Quanto potrebbe attirare l'attenzione degli utenti?

        3. POTENZIALE UMORISTICO:
        Quanto si presta alla creazione di meme divertenti?

        Valuta i criteri in modo realistico e differenziato.
        Non assegnare automaticamente punteggi elevati.

        Fornisci anche una breve motivazione.
        """

        result = structured_model.invoke(prompt)

        actuality = result.actuality
        interest = result.interest
        humor = result.humor

        # Calcolo del punteggio complessivo
        score = (
            actuality * 0.4 +
            interest * 0.3 +
            humor * 0.3
        )

        ranked_trend = {
            **trend,
            "actuality": actuality,
            "interest": interest,
            "humor": humor,
            "reasoning": result.reasoning,
            "score": round(score, 2)
        }

        ranked_trends.append(ranked_trend)

    # Ordiniamo i trend dal punteggio più alto al più basso
    ranked_trends.sort(
        key=lambda trend: trend["score"],
        reverse=True
    )

    return ranked_trends
