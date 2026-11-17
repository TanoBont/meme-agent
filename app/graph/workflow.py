
from langgraph.graph import StateGraph, START, END

from app.graph.state import MemeAgentState
from app.agents.research import research_trends
from app.agents.verification import verify_trends
from app.agents.ranking import rank_trends
from app.agents.creative import generate_meme_ideas
from app.agents.evaluator import evaluate_meme_ideas


def research_node(state: MemeAgentState):
    """
    Nodo che si occupa di individuare i trend.
    """

    trends = research_trends()

    return {
        "trends": trends
    }

def verification_node(state: MemeAgentState):
    verified_trends = verify_trends(state)

    return {
        "verified_trends": verified_trends
    }

def ranking_node(state: MemeAgentState):
    """
    Nodo che classifica i trend verificati.
    """

    ranked_trends = rank_trends(state)

    return {
        "ranked_trends": ranked_trends
    }

def creative_node(state: MemeAgentState):
    """
    Nodo che genera idee per meme dai trend classificati.
    """

    meme_ideas = generate_meme_ideas(state)

    return {
        "meme_ideas": meme_ideas
    }

def evaluator_node(state: MemeAgentState):
    """
    Nodo che valuta le idee generate dal Creative Agent.
    """

    evaluated_ideas = evaluate_meme_ideas(state)

    return {
        "meme_ideas": evaluated_ideas
    }


# Creiamo il grafo utilizzando il nostro State
builder = StateGraph(MemeAgentState)

# Registriamo il Research Agent come nodo
builder.add_node("research", research_node)
builder.add_node("verification", verification_node)
builder.add_node("ranking", ranking_node)
builder.add_node("creative", creative_node)
builder.add_node("evaluator", evaluator_node)

# Definiamo il punto di partenza
builder.add_edge(START, "research")
builder.add_edge("research", "verification")
builder.add_edge("verification", "ranking")
builder.add_edge("ranking", "creative")
builder.add_edge("creative", "evaluator")
builder.add_edge("evaluator", END)


# Compiliamo il grafo
graph = builder.compile()
