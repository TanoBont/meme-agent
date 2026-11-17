
from app.tools.search import search_web


def research_trends():
    """
    Ricerca trend attuali sul web utilizzando Tavily.
    """

    search_queries = [
        "ultime tendenze intelligenza artificiale tecnologia",
        "ultime notizie di calcio e argomenti discussi",
        "trend virali e argomenti popolari sui social"
    ]

    trends = []

    for query in search_queries:

        results = search_web(query, max_results=3)

        for result in results:
            trends.append({
                "topic": result.get("title", ""),
                "description": result.get("content", ""),
                "url": result.get("url", ""),
                "source": result.get("url", "")
            })

    return trends
