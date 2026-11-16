
from app.agents.research import research_trends
from app.agents.verification import verify_trends
from app.agents.ranking import rank_trends
from app.agents.creative import generate_meme_ideas
from app.agents.evaluator import evaluate_meme_ideas
from app.graph.state import MemeAgentState

# Creiamo lo State iniziale
state: MemeAgentState = {
    "trends": [],
    "verified_trends": [],
    "ranked_trends": [],
    "meme_ideas": []
}

# Fase 1: ricerca
state["trends"] = research_trends()

# Fase 2: verifica
state = verify_trends(state)

# Fase 3: classificazione
state = rank_trends(state)

# Fase 4: generazione delle idee
state = generate_meme_ideas(state)

# Fase 5: valutazione delle idee
state = evaluate_meme_ideas(state)

# Visualizziamo i risultati finali
print("\nVALUTAZIONE DELLE IDEE:\n")

for idea in state["meme_ideas"]:
    print(f"Argomento: {idea['topic']}")
    print(f"Testo: {idea['text_top']}")
    print(f"Valutazione: {idea['evaluation_score']}/10")
    print(f"Approvata: {idea['approved']}")
    print("-" * 50)
