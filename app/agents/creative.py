
def generate_meme_ideas(state):
    """
    Genera idee per meme partendo dai trend classificati.
    Per ora utilizza regole predefinite.
    """

    meme_ideas = []

    for trend in state["ranked_trends"]:

        idea = {
            "topic": trend["topic"],
            "score": trend["score"],
            "text_top": f"QUANDO PENSI DI AVER CAPITO {trend['topic'].upper()}",
            "text_bottom": "MA SCOPRI CHE C'È ANCORA TANTO DA IMPARARE",
            "description": f"Meme ironico sul tema {trend['topic']}"
        }

        meme_ideas.append(idea)

    return meme_ideas
