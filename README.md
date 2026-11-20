# Meme Agent

![CI](https://github.com/TanoBont/meme-agent/actions/workflows/ci.yml/badge.svg)

Meme Agent è un progetto personale basato sull'intelligenza artificiale, nato con l'obiettivo di individuare trend e notizie dal mondo del calcio e trasformarli in idee creative per meme.

Il progetto è attualmente composto da un prototipo Python multi-agente e da una progettazione più ampia per una futura piattaforma web AI-powered.

L'obiettivo è sviluppare un sistema che supporti l'intero processo creativo: dalla scoperta degli eventi calcistici alla generazione, modifica e condivisione dei meme, mantenendo l'utente al centro delle decisioni.

## Indice

- [Progetto](#progetto)
- [Stato attuale](#stato-attuale)
- [Prototipo multi-agente](#prototipo-multi-agente)
- [Tecnologie utilizzate](#tecnologie-utilizzate)
- [Installazione e configurazione](#installazione-e-configurazione)
- [Esecuzione](#esecuzione)
- [Test](#test)
- [Progettazione della piattaforma](#progettazione-della-piattaforma)
- [Documentazione](#documentazione)
- [Roadmap](#roadmap)

## Progetto

Meme Agent nasce come esperimento di applicazione pratica dei sistemi multi-agente e dei Large Language Models alla creazione di contenuti umoristici legati al calcio.

Il progetto si è evoluto verso una piattaforma più articolata, che prevede:

- **Discover:** ricerca e analisi di notizie ed eventi calcistici con potenziale creativo.
- **Meme Studio:** ambiente assistito dall'AI per ideare e realizzare meme.
- **Library:** raccolta personale per organizzare e conservare i contenuti.
- **Knowledge Base & RAG:** gestione e recupero di informazioni per migliorare il contesto delle generazioni AI.

La piattaforma è progettata per essere estendibile e modulare, con particolare attenzione a sicurezza, privacy, qualità del software e gestione dei costi dei servizi AI.

## Stato attuale

Il progetto si trova in una fase di evoluzione tra prototipazione e progettazione architetturale.

| Componente | Stato |
|---|---|
| Prototipo Python multi-agente | Implementato |
| Ricerca e analisi dei trend calcistici | Implementata nel prototipo |
| Generazione e valutazione delle idee | Implementata nel prototipo |
| Revisione automatica delle idee | Implementata nel prototipo |
| Progettazione della piattaforma web | In progettazione |
| Modello dati e architettura target | Progettati a livello concettuale |
| Implementazione della piattaforma web | Da avviare |

Le funzionalità descritte nella progettazione della piattaforma non devono essere considerate già disponibili nel prototipo.

## Prototipo multi-agente

Il prototipo attuale è sviluppato in Python e utilizza LangGraph per coordinare sei agenti specializzati attraverso un workflow condiviso.

### Agenti

**1. Research Agent**

Ricerca online notizie e trend calcistici tramite Tavily. Raccoglie i risultati, gestisce i metadati e contribuisce alla rimozione dei duplicati.

**2. Verification Agent**

Analizza le informazioni raccolte e ne valuta la plausibilità sulla base dei contenuti disponibili.

**3. Ranking Agent**

Assegna un punteggio ai trend considerando tre fattori:

- Attualità: 40%
- Interesse: 30%
- Potenziale umoristico: 30%

I trend vengono ordinati in base al punteggio complessivo e vengono selezionati quelli più rilevanti.

**4. Creative Agent**

Genera idee per meme a partire dai trend selezionati, utilizzando output strutturati per organizzare i contenuti creativi.

**5. Evaluator Agent**

Valuta le idee generate combinando controlli basati su regole Python e valutazioni effettuate tramite un modello linguistico:

- Controlli basati su regole: 60%
- Valutazione AI: 40%

**6. Revision Agent**

Migliora le idee che non superano la valutazione. Le versioni revisionate vengono sottoposte nuovamente all'Evaluator Agent, entro un numero massimo di tentativi configurabile.

### Workflow

Il processo è coordinato da LangGraph attraverso uno stato condiviso che permette il trasferimento delle informazioni tra le diverse fasi.

Le principali fasi sono:

1. Ricerca dei trend online.
2. Verifica preliminare delle informazioni.
3. Classificazione e selezione dei trend.
4. Generazione delle idee per meme.
5. Valutazione delle idee.
6. Revisione delle idee non approvate e nuova valutazione.

Il workflow gestisce il ciclo di revisione e interrompe i tentativi al raggiungimento del limite configurato.

## Tecnologie utilizzate

| Tecnologia | Utilizzo |
|---|---|
| Python | Linguaggio principale del prototipo |
| LangGraph | Orchestrazione del workflow multi-agente |
| LangChain | Integrazione con i modelli linguistici |
| OpenAI API | Generazione e valutazione dei contenuti |
| Tavily API | Ricerca online dei trend |
| unittest | Test automatici |

## Installazione e configurazione

### Prerequisiti

- Python
- Git
- Chiavi API per i servizi esterni utilizzati

### Clonazione del repository

```bash
git clone https://github.com/TanoBont/meme-agent.git
cd meme-agent
```

### Creazione dell'ambiente virtuale

```bash
python -m venv .venv
```

Su Windows, attivazione dell'ambiente:

```powershell
.venv\Scripts\Activate.ps1
```

### Installazione delle dipendenze

```bash
pip install -r requirements.txt
```

### Configurazione delle variabili d'ambiente

Creare un file `.env` nella directory principale del progetto, utilizzando `.env.example` come riferimento.

Le principali variabili utilizzate sono:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Le altre impostazioni, come modello AI, numero massimo di revisioni e numero di trend da selezionare, possono essere configurate in base alle variabili supportate dal progetto.

**Nota:** il file `.env` contiene credenziali private e non deve essere pubblicato o incluso nei commit Git.

## Esecuzione

Per avviare il prototipo:

```bash
python main.py
```

Al termine dell'esecuzione vengono mostrati i trend individuati, quelli verificati e classificati, le idee generate e le relative valutazioni, insieme a un riepilogo del processo.

## Test

Il progetto include test automatici realizzati con `unittest`, che verificano il comportamento dei singoli agenti, delle regole di valutazione e del workflow.

Per eseguire la suite:

```bash
python -m unittest discover -s tests -v
```

I test che richiedono chiamate a servizi esterni vengono gestiti separatamente.

## Progettazione della piattaforma

L'evoluzione prevista consiste nella realizzazione di una piattaforma web modulare, multiutente e assistita dall'intelligenza artificiale.

### Architettura target

La progettazione prevede l'utilizzo delle seguenti tecnologie:

| Tecnologia | Responsabilità prevista |
|---|---|
| Next.js, React e TypeScript | Frontend web |
| FastAPI | Backend e API REST |
| Python e LangGraph | Orchestrazione dei workflow AI |
| OpenAI API | Servizi di intelligenza artificiale |
| PostgreSQL e pgvector | Database e ricerca vettoriale |
| Pillow | Elaborazione e composizione delle immagini |
| Docker | Containerizzazione e ambiente di sviluppo |

Queste tecnologie rappresentano l'architettura target e non descrivono lo stack già implementato nel prototipo.

### Domini funzionali

La piattaforma è stata suddivisa nei seguenti domini:

1. Identity & Access
2. Asset Management
3. Football Catalog
4. Discover
5. Meme Studio
6. Library
7. Knowledge Base & RAG
8. AI Usage
9. Governance & Protection

Sono inoltre previste funzionalità trasversali per notifiche, moderazione, processi asincroni, configurazione e osservabilità.

### Principi architetturali

La progettazione segue alcuni principi fondamentali:

- Modular Monolith come architettura iniziale.
- Separazione delle responsabilità tra domini.
- API REST versionate.
- Gestione centralizzata degli asset.
- Isolamento dei dati tra utenti.
- Sicurezza e privacy integrate fin dalla progettazione.
- Monitoraggio dell'utilizzo e dei costi dei servizi AI.
- Test automatici e qualità del codice.
- Possibilità di evoluzione progressiva senza introdurre complessità prematura.

## Documentazione

La documentazione tecnica è organizzata in due aree.

### Prototipo attuale

I documenti nella cartella `docs/` descrivono il funzionamento dell'applicazione Python già sviluppata:

- `agents.md`
- `architecture.md`
- `configuration.md`
- `workflow.md`

### Progettazione della piattaforma

La cartella `docs/platform/` contiene la documentazione architetturale e progettuale della futura piattaforma web:

| Documento | Contenuto |
|---|---|
| `00-overview.md` | Panoramica e obiettivi |
| `01-requirements.md` | Requisiti funzionali e non funzionali |
| `02-architecture.md` | Architettura software |
| `03-domain-model.md` | Modello concettuale dei dati |
| `04-workflows.md` | Workflow applicativi |
| `05-security-privacy-governance.md` | Sicurezza, privacy e governance |
| `06-data-integrity.md` | Integrità e gestione dei dati |
| `07-testing-quality.md` | Testing e qualità |
| `08-operations.md` | Aspetti operativi |
| `09-roadmap.md` | Roadmap evolutiva |
| `10-decisions-register.md` | Registro delle decisioni architetturali |
| `11-open-items.md` | Questioni ancora aperte |

La documentazione distingue le funzionalità implementate da quelle progettate o pianificate.

## Roadmap

Lo sviluppo futuro è organizzato per fasi:

**Fase 1 – Progettazione tecnica**

- Consolidamento del modello ER.
- Definizione dello schema PostgreSQL.
- Progettazione delle API REST.
- Definizione dettagliata dell'architettura applicativa.
- Delimitazione delle funzionalità MVP.

**Fase 2 – MVP**

- Setup dell'architettura applicativa.
- Implementazione di autenticazione e gestione utenti.
- Gestione centralizzata degli asset.
- Prime funzionalità Discover.
- Prime funzionalità Meme Studio.
- Libreria personale ed esportazione dei meme.

**Fase 3 – Beta ed evoluzione**

- Miglioramento delle funzionalità AI.
- Evoluzione del sistema RAG.
- Miglioramento dell'editor.
- Funzionalità avanzate e personalizzazione.
- Test, sicurezza e ottimizzazione.

**Fase 4 – Release pubblica**

- Consolidamento operativo.
- Scalabilità e affidabilità.
- Funzionalità community e servizi aggiuntivi.
- Valutazione di ulteriori integrazioni.

La roadmap è indicativa e potrà essere aggiornata durante lo sviluppo.

---

## Obiettivo finale

Realizzare una piattaforma che unisca intelligenza artificiale, automazione e creatività, offrendo agli appassionati di calcio uno strumento per trasformare eventi e notizie in contenuti originali e divertenti.