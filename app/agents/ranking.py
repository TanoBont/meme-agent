
from app.llms import get_openai_model
from app.agents.schemas import TrendRanking
from app.config import MAX_TRENDS


def rank_trends(state):
    """
    Valuta e ordina i trend calcistici verificati utilizzando OpenAI.
    """

    model = get_openai_model(temperature=0.2)
    structured_model = model.with_structured_output(TrendRanking)

    ranked_trends = []

    for trend in state["verified_trends"]:

        # Ignoriamo i trend non verificati
        if not trend["verified"]:
            continue

        
        prompt = f"""
        Sei un esperto di calcio italiano ed europeo,
        social media e creazione di meme calcistici.

        Il tuo compito è individuare i trend con il maggiore
        potenziale per diventare meme sui social.

        Analizza il seguente trend e assegna tre punteggi
        da 1 a 10.

        ARGOMENTO:
        {trend["topic"]}

        DESCRIZIONE:
        {trend["description"]}

        CATEGORIA:
        {trend.get("category", "Non specificata")}

        TIPOLOGIA:
        {trend.get("content_type", "Non specificata")}

        DATA DI PUBBLICAZIONE:
        {trend.get("published_date") or "Non disponibile"}

        CONFIDENZA DELLA VERIFICA:
        {trend.get("confidence", "Non disponibile")}

        CRITERI DI VALUTAZIONE:

        1. ATTUALITÀ:
        Per i contenuti CURRENT valuta quanto il trend sia
        recente e collegato a eventi attuali.

        Per i contenuti EVERGREEN valuta quanto il trend
        sia ancora riconoscibile e rilevante nella cultura calcistica.
        Non penalizzarlo soltanto perché non è recente.

        2. INTERESSE:
        Valuta quanto il trend potrebbe attirare l'attenzione
        degli appassionati di calcio italiani ed europei.

        Considera:
        - Importanza dell'evento o del personaggio.
        - Coinvolgimento delle tifoserie.
        - Possibilità di generare discussioni e reazioni sui social.
        - Rilevanza per il pubblico calcistico.

        3. POTENZIALE UMORISTICO:
        Valuta quanto il trend si presta alla creazione
        di meme divertenti, battute, sfottò e situazioni ironiche.

        Considera:
        - Presenza di situazioni paradossali o divertenti.
        - Possibilità di creare battute riconoscibili.
        - Potenziale di condivisione sui social.
        - Disponibilità di elementi concreti da utilizzare
          per costruire un meme.

        REGOLE:
        - Valuta i criteri in modo realistico e differenziato.
        - Non assegnare automaticamente punteggi elevati.
        - Non inventare informazioni non presenti nel contenuto.
        - Non confondere l'importanza giornalistica
          con il potenziale di creare un meme.
        - Non penalizzare automaticamente un trend
          soltanto perché proviene da una categoria evergreen.
        - Utilizza la confidenza della verifica come elemento
          di contesto, non come punteggio automatico.

        Assegna un punteggio da 1 a 10 per ciascun criterio.

        Fornisci anche una breve motivazione che spieghi
        perché il trend merita il punteggio assegnato.
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

    return ranked_trends[:MAX_TRENDS]
