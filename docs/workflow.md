# Workflow di esecuzione

## 1. Panoramica

Il workflow di Meme Agent è realizzato utilizzando **LangGraph** e coordina l'esecuzione dei sei agenti che compongono il sistema.

Il grafo definisce la sequenza delle operazioni, gestisce il trasferimento dei dati attraverso uno stato condiviso e controlla il ciclo di valutazione e revisione delle idee generate.

L'esecuzione parte dal nodo di ricerca e termina quando tutte le idee risultano approvate oppure viene raggiunto il numero massimo di revisioni consentite.

## 2. Definizione del grafo

**Modulo:** `app/graph/workflow.py`

Il grafo viene costruito utilizzando `StateGraph`, associato al tipo `MemeAgentState`.

Ogni agente viene registrato come nodo attraverso `add_node()`. I collegamenti tra i nodi vengono definiti tramite `add_edge()`, mentre le transizioni condizionali vengono gestite con `add_conditional_edges()`.

Il grafo viene infine compilato tramite `builder.compile()`.

## 3. Sequenza di esecuzione

Il workflow segue una sequenza iniziale composta da cinque fasi.

### 3.1 Ricerca

**Nodo:** `research`

Il nodo richiama `research_trends()` e inserisce i trend individuati nel campo `trends` dello stato condiviso.

### 3.2 Verifica

**Nodo:** `verification`

Il nodo richiama `verify_trends()` e aggiorna il campo `verified_trends` con gli esiti della valutazione preliminare.

### 3.3 Classificazione

**Nodo:** `ranking`

Il nodo richiama `rank_trends()` e aggiorna `ranked_trends` con i trend ordinati e selezionati.

### 3.4 Generazione

**Nodo:** `creative`

Il nodo richiama `generate_meme_ideas()` e produce le idee per meme a partire dai trend classificati.

I risultati vengono inseriti nel campo `meme_ideas`.

### 3.5 Valutazione

**Nodo:** `evaluator`

Il nodo richiama `evaluate_meme_ideas()` e aggiorna le idee con i relativi punteggi e risultati della valutazione.

Al termine della valutazione viene eseguita una funzione di controllo che determina il passaggio successivo.

## 4. Ciclo di valutazione e revisione

Il workflow utilizza la funzione `should_revise()` per decidere se terminare l'esecuzione oppure procedere con una revisione.

La funzione considera due condizioni:

1. Tutte le idee devono risultare approvate.
2. Non deve essere stato raggiunto il numero massimo di revisioni configurato.

Se tutte le idee sono approvate, il workflow termina.

Se il numero massimo di revisioni è stato raggiunto, il workflow termina anche in presenza di idee non approvate.

Negli altri casi viene eseguito il Revision Agent.

### 4.1 Revisione

**Nodo:** `revision`

Il nodo richiama `revise_meme_ideas()` per migliorare le idee non approvate.

Al termine aggiorna:

- `meme_ideas`, con le versioni revisionate.
- `revision_count`, incrementando il numero di revisioni effettuate.

### 4.2 Nuova valutazione

Dopo la revisione, il workflow torna direttamente al nodo `evaluator`.

Le idee aggiornate vengono quindi sottoposte nuovamente alla valutazione, senza ripetere le fasi di ricerca, verifica, classificazione e generazione.

Il ciclo può ripetersi fino all'approvazione di tutte le idee o al raggiungimento del limite configurato.

## 5. Condizioni di terminazione

Il workflow termina in due situazioni:

- Tutte le idee generate risultano approvate.
- Il numero di revisioni effettuate raggiunge `MAX_REVISIONS`.

Il limite massimo viene letto dalla configurazione applicativa.

Se non viene specificato diversamente, il valore predefinito è pari a 2.

## 6. Schema del flusso

```text
START
  |
  v
Research
  |
  v
Verification
  |
  v
Ranking
  |
  v
Creative
  |
  v
Evaluator
  |
  v
should_revise()
  |
  +---- Tutte approvate ----> END
  |
  +---- Limite raggiunto ---> END
  |
  +---- Da revisionare
              |
              v
           Revision
              |
              v
           Evaluator
```

## 7. Stato condiviso

Il trasferimento dei dati tra i nodi avviene attraverso `MemeAgentState`, definito in `app/graph/state.py`.

Ogni nodo riceve lo stato corrente e restituisce un dizionario contenente i campi da aggiornare.

Questo approccio consente di mantenere separata la logica dei singoli agenti dalla gestione del flusso di esecuzione.