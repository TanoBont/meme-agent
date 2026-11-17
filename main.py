
from app.graph.workflow import graph
from app.graph.state import MemeAgentState


initial_state: MemeAgentState = {
    "trends": [],
    "verified_trends": [],
    "ranked_trends": [],
    "meme_ideas": [],
    "revision_count": 0
}

# Eseguiamo il grafo
result = graph.invoke(initial_state)

# Visualizziamo i trend individuati
print("\nTREND INDIVIDUATI\n")

for trend in result["trends"]:
    print(f"Argomento: {trend['topic']}")
    print(f"Descrizione: {trend['description']}")
    print("-" * 40)


# Visualizziamo i trend verificati
print("\nTREND VERIFICATI\n")

for trend in result["verified_trends"]:
    print(f"Argomento: {trend['topic']}")
    print(f"Verificato: {trend['verified']}")
    print("-" * 40)

# Visualizziamo i trend classificati
print("\nTREND CLASSIFICATI\n")

for trend in result["ranked_trends"]:
    print(f"Argomento: {trend['topic']}")
    print(f"Attualità: {trend['actuality']}/10")
    print(f"Interesse: {trend['interest']}/10")
    print(f"Potenziale umoristico: {trend['humor']}/10")
    print(f"Punteggio complessivo: {trend['score']}/10")
    print("-" * 40)
    
# Visualizziamo le idee generate
print("\nIDEE PER I MEME\n")

for idea in result["meme_ideas"]:
    print(f"Argomento: {idea['topic']}")
    print(f"Testo superiore: {idea['text_top']}")
    print(f"Testo inferiore: {idea['text_bottom']}")
    print(f"Descrizione: {idea['description']}")
    print("-" * 40)
    

print("\nVALUTAZIONE DELLE IDEE\n")

for idea in result["meme_ideas"]:
    print(f"Argomento: {idea['topic']}")

    evaluation = idea["evaluation"]

    print(f"Completezza: {evaluation['completeness']}/10")
    print(f"Pertinenza: {evaluation['relevance']}/10")
    print(f"Leggibilità: {evaluation['readability']}/10")
    print(f"Struttura: {evaluation['structure']}/10")

    print(f"Punteggio complessivo: {idea['evaluation_score']}/10")
    print(f"Approvata: {idea['approved']}")

    print("----------------------------------------")



# Riepilogo dell'esecuzione
print("\nRIEPILOGO ESECUZIONE\n")

total_ideas = len(result["meme_ideas"])

approved_ideas = sum(
    1 for idea in result["meme_ideas"]
    if idea["approved"]
)

rejected_ideas = total_ideas - approved_ideas

print(f"Trend individuati: {len(result['trends'])}")
print(f"Idee generate: {total_ideas}")
print(f"Idee approvate: {approved_ideas}")
print(f"Idee non approvate: {rejected_ideas}")
print(f"Revisioni effettuate: {result['revision_count']}")

print("----------------------------------------")
