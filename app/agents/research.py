
from datetime import date

from app.tools.search import search_web


def research_trends():
    """
    Ricerca trend calcistici italiani ed europei.
    Distingue contenuti attuali ed evergreen,
    elimina risultati incompleti e duplicati.
    """

    today = date.today().strftime("%d %B %Y")

    search_queries = [
        {
            "category": "serie_a",
            "content_type": "current",
            "query": (
                f"Serie A ultime notizie calcio {today} "
                "infortuni ufficiali risultati partite "
                "prestazioni giocatori allenatori"
            )
        },
        {
            "category": "calciomercato",
            "content_type": "current",
            "query": (
                f"calciomercato {today} trattative "
                "aggiornamenti trasferimenti ufficiali "
                "Serie A Premier League Liga"
            )
        },
        {
            "category": "champions_league",
            "content_type": "current",
            "query": (
                f"UEFA Champions League {today} "
                "ultime partite risultati gol "
                "prestazioni giocatori notizie"
            )
        },
        {
            "category": "controversies",
            "content_type": "current",
            "query": (
                f"Serie A {today} episodi arbitrali "
                "controversi VAR rigori espulsioni "
                "decisioni arbitrali partite recenti"
            )
        },
        {
            "category": "football_culture",
            "content_type": "evergreen",
            "query": (
                "calcio italiano rivalità storiche "
                "tifoserie sfottò derby momenti iconici "
                "episodi memorabili cultura calcistica"
            )
        }
    ]

    trends = []
    seen_urls = set()

    for search in search_queries:

        results = search_web(
            search["query"],
            max_results=2
        )

        for result in results:

            title = result.get("title", "").strip()
            description = result.get("content", "").strip()
            url = result.get("url", "").strip()

            # Scartiamo i risultati incompleti
            if not title or not description or not url:
                continue

            # Normalizziamo l'URL per evitare duplicati
            normalized_url = url.lower().rstrip("/")

            if normalized_url in seen_urls:
                continue

            seen_urls.add(normalized_url)

            trends.append({
                "topic": title,
                "description": description,
                "url": url,
                "source": url,
                "category": search["category"],
                "content_type": search["content_type"],
                "published_date": result.get("published_date")
            })

    return trends
