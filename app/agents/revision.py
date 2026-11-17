
def revise_meme_ideas(state):
    """
    Rivede le idee non approvate utilizzando
    i risultati dei singoli criteri di valutazione.
    """

    revised_ideas = []

    for idea in state["meme_ideas"]:

        if idea["approved"]:
            revised_ideas.append(idea)
            continue

        revised_idea = idea.copy()
        evaluation = idea["evaluation"]

        # Correzione della completezza
        if evaluation["completeness"] < 7:
            if not revised_idea.get("text_top"):
                revised_idea["text_top"] = (
                    f"QUANDO PENSI A {idea['topic'].upper()}"
                )

            if not revised_idea.get("text_bottom"):
                revised_idea["text_bottom"] = (
                    "MA LE COSE NON VANNO COME PREVISTO"
                )

            if not revised_idea.get("description"):
                revised_idea["description"] = (
                    f"Meme ironico sul tema {idea['topic']}"
                )

        # Correzione della pertinenza
        if evaluation["relevance"] < 7:
            revised_idea["text_top"] = (
                f"QUANDO TI CONFRONTI CON {idea['topic'].upper()}"
            )

            revised_idea["description"] = (
                f"Meme ironico e pertinente al tema {idea['topic']}"
            )

        # Correzione della leggibilità
        if evaluation["readability"] < 7:
            revised_idea["text_top"] = (
                f"QUANDO PROVI {idea['topic'].upper()}"
            )

            revised_idea["text_bottom"] = (
                "MA NON È FACILE"
            )

        # Correzione della struttura
        if evaluation["structure"] < 7:
            revised_idea["text_top"] = (
                f"QUANDO SCOPRI {idea['topic'].upper()}"
            )

            revised_idea["text_bottom"] = (
                "E NON SAI COSA ASPETTARTI"
            )

        revised_ideas.append(revised_idea)

    return revised_ideas
