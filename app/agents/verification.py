
from app.llms import get_openai_model
from app.agents.schemas import TrendVerification


def verify_trends(state):
    """
    Verifica i trend raccolti dal Research Agent
    utilizzando un modello linguistico.
    """

    model = get_openai_model(temperature=0.1)

    structured_model = model.with_structured_output(TrendVerification)

    verified_trends = []

    for trend in state["trends"]:

        prompt = f"""
        Sei un analista specializzato nella verifica delle informazioni online.

        Devi valutare l'attendibilità del seguente trend utilizzando
        esclusivamente le informazioni fornite.

        TITOLO:
        {trend["topic"]}

        DESCRIZIONE:
        {trend["description"]}

        FONTE:
        {trend.get("source", "Non disponibile")}

        URL:
        {trend.get("url", "Non disponibile")}

        VALUTA:
        - Attendibilità delle informazioni.
        - Presenza di elementi concreti a supporto.
        - Coerenza tra titolo e descrizione.

        Considera che una singola fonte non garantisce la veridicità
        di un'informazione.

        Assegna un livello di confidenza da 1 a 10.

        Imposta verified=True soltanto se le informazioni sono
        sufficientemente supportate.

        Motiva brevemente la tua valutazione.
        """

        result = structured_model.invoke(prompt)

        verified_trend = {
            **trend,
            "verified": result.verified,
            "confidence": result.confidence,
            "reasoning": result.reasoning
        }

        verified_trends.append(verified_trend)

    return verified_trends
