
from app.tools.search import search_web


def research_trends():
    """
    Ricerca trend attuali sul web utilizzando Tavily.
    Valida i risultati ed elimina eventuali duplicati.
    """

    search_queries = [
        "ultime tendenze intelligenza artificiale tecnologia",
        "ultime notizie di calcio e argomenti discussi",
        "trend virali e argomenti popolari sui social"
    ]

    trends = []
    seen_urls = set()

    for query in search_queries:

        results = search_web(query, max_results=3)

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
                "source": url
            })

    return trends
