
def evaluate_completeness(idea):
    """
    Valuta la completezza di un'idea per meme.
    """

    required_fields = [
        "topic",
        "text_top",
        "text_bottom",
        "description"
    ]

    completed_fields = 0

    for field in required_fields:
        value = idea.get(field)

        if isinstance(value, str) and value.strip():
            completed_fields += 1

    score = (completed_fields / len(required_fields)) * 10

    return round(score, 2)


def evaluate_relevance(idea):
    """
    Valuta la pertinenza tra l'argomento e il contenuto del meme.
    """

    topic = idea.get("topic", "").lower()

    content = " ".join([
        idea.get("text_top", ""),
        idea.get("text_bottom", ""),
        idea.get("description", "")
    ]).lower()

    topic_words = topic.split()

    if not topic_words:
        return 1

    matching_words = sum(
        1 for word in topic_words
        if word in content
    )

    relevance_ratio = matching_words / len(topic_words)

    score = 1 + relevance_ratio * 9

    return round(score, 2)


def evaluate_readability(idea):
    """
    Valuta la leggibilità dei testi del meme
    in base alla loro lunghezza.
    """

    text_top = idea.get("text_top", "")
    text_bottom = idea.get("text_bottom", "")
    description = idea.get("description", "")

    limits = {
        "text_top": 100,
        "text_bottom": 100,
        "description": 200
    }

    fields = {
        "text_top": text_top,
        "text_bottom": text_bottom,
        "description": description
    }

    scores = []

    for field, value in fields.items():

        if not isinstance(value, str) or not value.strip():
            scores.append(1)
            continue

        length = len(value)

        if length <= limits[field]:
            scores.append(10)
        elif length <= limits[field] * 1.5:
            scores.append(7)
        else:
            scores.append(4)

    return round(sum(scores) / len(scores), 2)


def evaluate_structure(idea):
    """
    Valuta la struttura dell'idea del meme.
    """

    topic = idea.get("topic", "")
    text_top = idea.get("text_top", "")
    text_bottom = idea.get("text_bottom", "")
    description = idea.get("description", "")

    fields = [topic, text_top, text_bottom, description]

    if not all(isinstance(value, str) and value.strip() for value in fields):
        return 1

    if text_top.strip().lower() == text_bottom.strip().lower():
        return 3

    if text_top.strip().lower() == description.strip().lower():
        return 5

    return 10
