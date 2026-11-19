
from app.tools.search import search_web
from app.config import MAX_TRENDS


def research_trends():
    """
    Ricerca trend calcistici italiani ed europei.
    Distingue contenuti attuali ed evergreen,
    elimina risultati incompleti e duplicati.
    """

    search_queries = [
        {
            "category": "serie_a",
            "content_type": "current",
            "query": "ultime notizie Serie A risultati partite giocatori allenatori"
        },
        {
            "category": "calciomercato",
            "content_type": "current",
            "query": "ultime notizie calciomercato italiano ed europeo"
        },
        {
            "category": "champions_league",
            "content_type": "current",
            "query": "ultime notizie Champions League Europa League calcio europeo"
        },
        {
            "category": "controversies",
            "content_type": "current",
            "query": "polemiche arbitrali VAR dichiarazioni controverse calcio"
        },
        {
            "category": "football_culture",
            "content_type": "evergreen",
            "query": "meme calcio momenti virali rivalità sfottò tifoserie"
        }
    ]

    trends = []
    seen_urls = set()

    for search in search_queries:

        results = search_web(search["query"], max_results=1)

        for result in results:

            title = result.get("title", "").strip()
            description = result.get("content", "").strip()
            url = result.get("url", "").strip()

            # Scartiamo i risultati incompleti
            if not title or not description or not url:
                continue

            # Evitiamo i duplicati
            if url in seen_urls:
                continue

            seen_urls.add(url)

            trends.append({
                "topic": title,
                "description": description,
                "url": url,
                "source": url,
                "category": search["category"],
                "content_type": search["content_type"],
                "published_date": result.get("published_date")
            })

    return trends[:MAX_TRENDS]
