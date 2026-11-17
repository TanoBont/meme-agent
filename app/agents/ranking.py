
def rank_trends(state):
    """
    Assegna un punteggio ai trend verificati
    in base a tre criteri.
    """

    ranked_trends = []

    for trend in state["verified_trends"]:

        # Punteggi simulati, da 1 a 10
        actuality = 8
        interest = 7
        humor = 9

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
            "score": round(score, 2)
        }

        ranked_trends.append(ranked_trend)

    # Ordiniamo i trend dal punteggio più alto al più basso
    ranked_trends.sort(
        key=lambda trend: trend["score"],
        reverse=True
    )

    # Aggiorniamo lo State
    state["ranked_trends"] = ranked_trends

    return ranked_trends
