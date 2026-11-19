
from app.llms import get_openai_model
from app.agents.schemas import TrendVerification


def verify_trends(state):
    """
    Verifica i trend calcistici raccolti dal Research Agent
    utilizzando OpenAI.
    """

    model = get_openai_model(temperature=0.1)
    structured_model = model.with_structured_output(TrendVerification)

    verified_trends = []

    for trend in state["trends"]:

        
        prompt = f"""
        Sei un analista specializzato nel calcio italiano ed europeo.

        Il tuo compito è effettuare una valutazione preliminare
        dei contenuti raccolti da un sistema di ricerca online.

        Non devi certificare la veridicità delle notizie,
        poiché non puoi consultare direttamente le pagine web.
        Devi stabilire se le informazioni disponibili sono
        sufficientemente credibili, pertinenti e utilizzabili
        per le successive fasi di generazione dei meme.

        TITOLO:
        {trend["topic"]}

        DESCRIZIONE:
        {trend["description"]}

        FONTE:
        {trend.get("source", "Non disponibile")}

        URL:
        {trend.get("url", "Non disponibile")}

        CATEGORIA:
        {trend.get("category", "Non specificata")}

        TIPOLOGIA:
        {trend.get("content_type", "Non specificata")}

        DATA DI PUBBLICAZIONE:
        {trend.get("published_date") or "Non disponibile"}

        CRITERI DI VALUTAZIONE:

        1. ATTENDIBILITÀ
        - Valuta la presenza di informazioni concrete e verificabili.
        - Controlla la coerenza tra titolo e descrizione.
        - Non confondere opinioni, supposizioni e fatti.
        - Non considerare automaticamente vera un'informazione
          soltanto perché viene presentata come una notizia.

        2. ATTUALITÀ
        Se il contenuto è CURRENT:
        - Valuta quanto le informazioni siano recenti.
        - Una data mancante riduce la certezza sull'attualità,
          ma non determina automaticamente un esito negativo.
        - Un contenuto chiaramente datato e non più attuale
          deve essere penalizzato.
        - Non dedurre la data di pubblicazione dal momento
          in cui stai effettuando la verifica.

        Se il contenuto è EVERGREEN:
        - Non richiedere necessariamente una data recente.
        - Valuta la rilevanza per la cultura calcistica,
          le rivalità, i momenti iconici e gli sfottò.
        - Considera se il contenuto può ancora essere interessante
          per un pubblico appassionato di calcio.

        3. QUALITÀ DELLA FONTE
        - Valuta il tipo di fonte e la sua riconoscibilità.
        - Distingui testate giornalistiche, siti ufficiali,
          piattaforme social e contenuti generati dagli utenti.
        - Una fonte social non è automaticamente falsa,
          ma richiede maggiore cautela.
        - Una singola fonte non garantisce la veridicità
          dell'informazione.

        4. COERENZA DELLA CATEGORIA
        - Verifica che il contenuto corrisponda alla categoria assegnata.
        - Un contenuto generico non deve essere considerato pertinente
          soltanto perché contiene riferimenti al calcio.
        - Valuta la reale utilità del contenuto per la categoria.

        REGOLE GENERALI:
        - Utilizza esclusivamente le informazioni fornite.
        - Non inventare fatti, date o conferme esterne.
        - Non dichiarare verificata una notizia soltanto
          perché il titolo sembra plausibile.
        - Distingui l'attendibilità del contenuto dalla sua attualità.
        - Considera sia l'affidabilità sia l'utilizzabilità
          del contenuto per il progetto.

        Assegna una confidenza da 1 a 10.

        Imposta verified=True quando:

        - Il contenuto presenta informazioni plausibili e coerenti.
        - Non emergono contraddizioni evidenti tra titolo e descrizione.
        - La fonte non presenta elementi che ne compromettano
          chiaramente l'attendibilità.
        - Il contenuto è pertinente alla categoria assegnata.
        - Sono presenti elementi sufficienti per sviluppare
          un'idea di meme senza inventare fatti.

        Non richiedere una certezza assoluta sulla veridicità
        della notizia, poiché questa fase rappresenta
        uno screening preliminare e non una verifica definitiva.

        Imposta verified=False quando il contenuto è incompleto,
        poco pertinente, incoerente o presenta evidenti problemi
        di attendibilità.

        Motiva brevemente la valutazione, indicando
        eventuali limiti o elementi di incertezza.
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
