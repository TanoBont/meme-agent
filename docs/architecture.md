# Architettura del sistema

## 1. Panoramica

Meme Agent è un sistema multi-agente sviluppato in Python, progettato per ricercare trend calcistici online e trasformarli in idee per meme.

L'architettura è organizzata in componenti indipendenti, ciascuno responsabile di una specifica fase del processo. Gli agenti collaborano attraverso uno stato condiviso e sono coordinati da un workflow realizzato con **LangGraph**.

Il sistema integra servizi esterni per la ricerca online e modelli linguistici per l'analisi, la generazione e la valutazione dei contenuti.

## 2. Architettura logica

L'architettura può essere suddivisa in quattro livelli principali:

- **Orchestrazione:** gestisce l'esecuzione degli agenti e il flusso dei dati attraverso LangGraph.
- **Agenti:** implementano le diverse fasi del processo, dalla ricerca alla revisione delle idee.
- **Servizi e integrazioni:** forniscono l'accesso ai modelli linguistici e agli strumenti di ricerca esterni.
- **Configurazione e stato:** gestiscono i parametri applicativi e i dati condivisi durante l'esecuzione.

## 3. Componenti principali

### 3.1 Orchestrazione

Il workflow è implementato tramite LangGraph e definisce l'ordine di esecuzione degli agenti, le transizioni tra le diverse fasi e le condizioni che determinano il proseguimento o l'interruzione del processo.

Il grafo utilizza uno stato condiviso, definito in `app/graph/state.py`, che permette agli agenti di leggere i dati prodotti dalle fasi precedenti e aggiornare le informazioni necessarie a quelle successive.

La definizione e la compilazione del workflow sono gestite in `app/graph/workflow.py`.

### 3.2 Agenti

Gli agenti sono organizzati nella directory `app/agents/`.

Ogni agente implementa una responsabilità specifica:

- Ricerca dei trend.
- Verifica preliminare delle informazioni.
- Classificazione dei trend.
- Generazione delle idee per meme.
- Valutazione delle idee.
- Revisione dei contenuti non approvati.

La separazione in moduli indipendenti facilita la manutenzione, il testing e l'evoluzione delle singole funzionalità.

### 3.3 Modelli linguistici

L'integrazione con i modelli OpenAI è centralizzata in `app/llms.py`.

La funzione `get_openai_model()` inizializza il modello configurato e restituisce un'istanza di `ChatOpenAI`.

La configurazione supporta il modello specificato tramite la variabile d'ambiente `OPENAI_MODEL`. Per i modelli della famiglia GPT-6 viene utilizzata la Responses API con livello di reasoning `low`.

### 3.4 Strumenti esterni

La directory `app/tools/` contiene i componenti dedicati all'interazione con servizi esterni.

Attualmente il sistema utilizza Tavily per effettuare ricerche online e raccogliere informazioni sui trend calcistici.

L'integrazione è separata dalla logica degli agenti, così da mantenere indipendenti la ricerca dei dati e la loro elaborazione.

### 3.5 Configurazione

Il modulo `app/config.py` centralizza il caricamento delle variabili d'ambiente attraverso `python-dotenv`.

Le principali impostazioni riguardano:

- Chiave API OpenAI.
- Modello linguistico da utilizzare.
- Numero massimo di revisioni.
- Numero massimo di trend selezionati.

Le credenziali e i parametri personalizzati vengono definiti nel file `.env`, escluso dal repository. Il file `.env.example` fornisce un modello di configurazione.

## 4. Stato condiviso

Lo stato del sistema è definito in `app/graph/state.py` attraverso il tipo `MemeAgentState`.

Durante l'esecuzione vengono condivise le informazioni prodotte dai diversi agenti.

Tra i principali campi utilizzati:

| Campo | Descrizione |
|---|---|
| `trends` | Trend raccolti durante la ricerca |
| `verified_trends` | Trend sottoposti alla verifica preliminare |
| `ranked_trends` | Trend classificati e selezionati |
| `meme_ideas` | Idee per meme generate e valutate |
| `revision_count` | Numero di revisioni effettuate |

Lo stato condiviso consente di mantenere il contesto dell'esecuzione e di gestire il ciclo di valutazione e revisione.

## 5. Struttura del progetto

La struttura principale del repository è organizzata nel seguente modo:

```text
meme-agent/
│
├── app/
│   ├── agents/
│   ├── graph/
│   │   ├── state.py
│   │   └── workflow.py
│   ├── tools/
│   ├── config.py
│   └── llms.py
│
├── data/
│
├── docs/
│   ├── agents.md
│   ├── architecture.md
│   ├── configuration.md
│   └── workflow.md
│
├── tests/
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Descrizione delle directory

- `app/`: contiene la logica applicativa e i componenti del sistema.
- `app/agents/`: contiene le implementazioni dei singoli agenti.
- `app/graph/`: contiene la definizione dello stato condiviso e del workflow LangGraph.
- `app/tools/`: contiene gli strumenti per l'interazione con servizi esterni.
- `data/`: directory dedicata ai dati del progetto.
- `docs/`: raccoglie la documentazione tecnica.
- `tests/`: contiene i test automatici.
- `main.py`: punto di ingresso dell'applicazione.

## 6. Avvio dell'applicazione

L'esecuzione del sistema parte da `main.py`.

Il modulo inizializza lo stato, invoca il grafo tramite `graph.invoke()` e raccoglie il risultato dell'intero workflow.

Al termine vengono visualizzati i trend individuati, le idee generate, le relative valutazioni e un riepilogo dell'esecuzione.