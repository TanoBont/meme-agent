
import os

from tavily import TavilyClient


def get_tavily_client():
    """
    Crea e restituisce un client Tavily.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("TAVILY_API_KEY non configurata")

    return TavilyClient(api_key=api_key)


def search_web(query: str, max_results: int = 5):
    """
    Esegue una ricerca web tramite Tavily.
    Gestisce eventuali errori senza interrompere il workflow.
    """

    try:
        client = get_tavily_client()

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=max_results
        )

        return response.get("results", [])

    except Exception as error:
        print(f"Errore durante la ricerca Tavily: {error}")
        return []
