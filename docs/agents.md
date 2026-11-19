# Agenti del sistema

## 1. Panoramica

Meme Agent utilizza sei agenti specializzati, ciascuno responsabile di una fase specifica del processo di individuazione e trasformazione dei trend calcistici in idee per meme.

Gli agenti sono implementati in moduli Python indipendenti all'interno della directory `app/agents/` e vengono coordinati dal workflow LangGraph.

La comunicazione tra gli agenti avviene attraverso lo stato condiviso del sistema.

## 2. Research Agent

**Modulo:** `research.py`

Il Research Agent si occupa di individuare trend e notizie relativi al mondo del calcio attraverso ricerche online effettuate con Tavily.

Le principali responsabilità sono:

- Eseguire ricerche utilizzando diverse query.
- Raccogliere informazioni e metadati dai risultati.
- Organizzare i contenuti individuati.
- Evitare la presenza di risultati duplicati.

I risultati vengono inseriti nello stato condiviso e passati alla fase successiva.

Il modulo `football_keywords.py` fornisce supporto attraverso parole chiave specifiche del dominio calcistico.

## 3. Verification Agent

**Modulo:** `verification.py`

Il Verification Agent effettua una valutazione preliminare dei trend raccolti durante la fase di ricerca.

Utilizza un modello linguistico per analizzare le informazioni disponibili e stimare la plausibilità dei contenuti.

Le sue responsabilità comprendono:

- Analizzare i trend raccolti.
- Valutare la plausibilità delle informazioni.
- Produrre un esito strutturato per ciascun trend.

La verifica rappresenta un primo filtro di attendibilità basato sulle informazioni recuperate, non una certificazione definitiva della veridicità delle notizie.

## 4. Ranking Agent

**Modulo:** `ranking.py`

Il Ranking Agent assegna un punteggio ai trend che hanno superato la fase di verifica.

La classificazione considera tre dimensioni:

| Criterio | Peso |
|---|---:|
| Attualità | 40% |
| Interesse | 30% |
| Potenziale umoristico | 30% |

I punteggi vengono combinati per ottenere una valutazione complessiva.

I trend vengono quindi ordinati e viene selezionato un numero massimo di elementi, configurabile attraverso `MAX_TRENDS`.

## 5. Creative Agent

**Modulo:** `creative.py`

Il Creative Agent trasforma i trend selezionati in idee per meme.

Per ogni trend elabora un contenuto strutturato che comprende:

- Argomento di riferimento.
- Testo superiore.
- Testo inferiore.
- Descrizione dell'idea.

L'obiettivo è produrre idee coerenti con il contesto calcistico e con il potenziale umoristico del trend, evitando di introdurre informazioni non supportate dai dati disponibili.

## 6. Evaluator Agent

**Modulo:** `evaluator.py`

L'Evaluator Agent valuta la qualità delle idee generate dal Creative Agent.

La valutazione combina controlli deterministici implementati in Python e una valutazione effettuata tramite modello linguistico.

### 6.1 Valutazione basata su regole

**Modulo di supporto:** `evaluation_rules.py`

I controlli Python analizzano quattro aspetti:

- Completezza.
- Pertinenza.
- Leggibilità.
- Struttura.

Questi controlli permettono di verificare caratteristiche oggettive e requisiti minimi delle idee generate.

### 6.2 Valutazione AI

Il modello linguistico contribuisce alla valutazione di aspetti qualitativi e creativi, tra cui:

- Creatività.
- Umorismo.
- Originalità.

### 6.3 Punteggio complessivo

Il punteggio finale combina le due valutazioni:

| Componente | Peso |
|---|---:|
| Regole Python | 60% |
| Valutazione AI | 40% |

Le idee che raggiungono la soglia di approvazione vengono contrassegnate come approvate. Le altre possono essere inviate al processo di revisione.

## 7. Revision Agent

**Modulo:** `revision.py`

Il Revision Agent interviene sulle idee che non hanno superato la valutazione.

Utilizza il risultato dell'Evaluator Agent per individuare gli aspetti da migliorare e generare una versione aggiornata dell'idea.

La nuova versione viene sottoposta nuovamente alla valutazione.

Il numero massimo di revisioni è configurabile tramite `MAX_REVISIONS`.

## 8. Schemi degli output

**Modulo di supporto:** `schemas.py`

Il modulo contiene gli schemi utilizzati per strutturare gli output prodotti dai modelli linguistici.

L'utilizzo di output strutturati permette di mantenere uniformi i dati restituiti dagli agenti e facilita la loro integrazione nel workflow.

## 9. Collaborazione tra gli agenti

I sei agenti collaborano secondo una sequenza coordinata da LangGraph:

1. Il Research Agent raccoglie i trend.
2. Il Verification Agent ne valuta la plausibilità.
3. Il Ranking Agent seleziona i trend più interessanti.
4. Il Creative Agent genera le idee per meme.
5. L'Evaluator Agent valuta le idee.
6. Il Revision Agent interviene sulle idee non approvate, che vengono nuovamente valutate.

Il processo di revisione può essere ripetuto fino al raggiungimento della soglia di approvazione o del limite massimo di tentativi configurato.