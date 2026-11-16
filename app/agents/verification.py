
def verify_trends(state):
    """
    Analizza i trend individuati dal Research Agent
    e simula una verifica delle informazioni.
    """

    verified_trends = []

    for trend in state["trends"]:

        verified_trend = {
            "topic": trend["topic"],
            "description": trend["description"],
            "verified": True
        }

        verified_trends.append(verified_trend)

    return verified_trends
