
import re
import unicodedata

from app.agents.football_keywords import FOOTBALL_KEYWORDS

def normalize_text(text):
    """
    Normalizza il testo per facilitare il confronto delle parole.
    """

    text = unicodedata.normalize("NFKD", text.lower())

    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )

    return text


def count_keyword_matches(text, keywords):
    """
    Conta le parole chiave presenti nel testo,
    evitando corrispondenze parziali.
    """

    matches = 0

    for keyword in keywords:
        normalized_keyword = normalize_text(keyword)

        pattern = (
            r"(?<!\w)"
            + re.escape(normalized_keyword)
            + r"(?!\w)"
        )

        if re.search(pattern, text):
            matches += 1

    return matches

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
    Valuta la pertinenza tra l'argomento e il contenuto del meme,
    considerando topic, categoria e contesto calcistico.
    """

    topic = idea.get("topic", "")
    category = idea.get("category")

    content = " ".join([
        idea.get("text_top", ""),
        idea.get("text_bottom", ""),
        idea.get("description", "")
    ])

    topic = normalize_text(topic)
    content = normalize_text(content)

    if not topic:
        return 1

    # Parole chiave generali del mondo calcistico
    general_keywords = [
        "calcio", "football", "squadra", "partita",
        "gol", "rete", "giocatore", "calciatore",
        "allenatore", "arbitro", "var", "tifoso",
        "tifoseria", "campionato", "derby",
        "portiere", "attaccante", "difensore",
        "centrocampista", "rigore"
    ]

    # 1. Pertinenza diretta rispetto al topic
    topic_words = topic.split()

    matching_topic_words = sum(
        1 for word in topic_words
        if count_keyword_matches(content, [word]) > 0
    )

    topic_score = (
        matching_topic_words / len(topic_words)
    ) * 10

    # 2. Pertinenza rispetto alla categoria
    category_score = None

    if category in FOOTBALL_KEYWORDS:
        category_keywords = FOOTBALL_KEYWORDS[category]

        category_matches = count_keyword_matches(
            content,
            category_keywords
        )

        category_score = min(category_matches / 2, 1) * 10

    # 3. Pertinenza calcistica generale
    general_matches = count_keyword_matches(
        content,
        general_keywords
    )

    general_score = min(general_matches / 3, 1) * 10

    # Se il topic è semplicemente "calcio",
    # valutiamo la pertinenza attraverso il contesto calcistico.
    if topic in ["calcio", "football"]:
        topic_score = general_score

    # Combinazione dei punteggi
    if category_score is not None:
        score = (
            topic_score * 0.4 +
            category_score * 0.4 +
            general_score * 0.2
        )
    else:
        # Se manca la categoria, redistribuiamo i pesi.
        score = (
            topic_score * (0.4 / 0.6) +
            general_score * (0.2 / 0.6)
        )

    # Riportiamo il risultato nell'intervallo 1-10
    score = max(1, min(score, 10))

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
