# Meme Agent

![CI](https://github.com/TanoBont/meme-agent/actions/workflows/ci.yml/badge.svg)

Meme Agent è un progetto personale basato su un'architettura multi-agente che utilizza l'intelligenza artificiale per individuare trend calcistici online e trasformarli in idee per meme.

Il sistema automatizza le diverse fasi del processo, dalla ricerca delle notizie alla valutazione delle idee creative, attraverso agenti specializzati coordinati da un workflow realizzato con **LangGraph**.

## Obiettivi

- Ricercare notizie e trend relativi al mondo del calcio.
- Analizzare e valutare preliminarmente le informazioni raccolte.
- Classificare i trend in base ad attualità, interesse e potenziale umoristico.
- Generare idee creative per meme utilizzando modelli linguistici.
- Valutare automaticamente la qualità delle idee generate.
- Migliorare le idee che non superano la fase di valutazione.

## Architettura

Il sistema è composto da sei agenti specializzati, coordinati attraverso un workflow basato su LangGraph.

### Agenti

**1. Research Agent**

Si occupa della ricerca online di notizie e trend calcistici tramite Tavily. Raccoglie i risultati e gestisce i relativi metadati, occupandosi anche della rimozione dei duplicati.

**2. Verification Agent**

Analizza le informazioni raccolte e ne valuta la plausibilità sulla base dei contenuti restituiti dalla ricerca, effettuando una prima verifica dei trend individuati.

**3. Ranking Agent**

Assegna un punteggio ai trend considerando tre fattori:

- Attualità: 40%
- Interesse: 30%
- Potenziale umoristico: 30%

I trend vengono ordinati in base al punteggio complessivo e vengono selezionati quelli più rilevanti.

**4. Creative Agent**

Genera idee per meme a partire dai trend selezionati, utilizzando output strutturati per mantenere organizzati i contenuti creativi.

**5. Evaluator Agent**

Valuta le idee generate combinando controlli basati su regole Python e valutazioni effettuate tramite un modello linguistico.

La valutazione combina:

- Controlli basati su regole: 60%
- Valutazione AI: 40%

Le idee che raggiungono la soglia di approvazione prevista vengono accettate.

**6. Revision Agent**

Si occupa di migliorare le idee che non superano la valutazione. Le versioni revisionate vengono sottoposte nuovamente all'Evaluator Agent, entro un numero massimo di tentativi configurabile.

## Workflow

Gli agenti sono coordinati da LangGraph attraverso uno stato condiviso che permette di trasferire i dati tra le diverse fasi.

Il processo segue queste fasi:

1. Ricerca dei trend online.
2. Verifica preliminare delle informazioni raccolte.
3. Classificazione e selezione dei trend.
4. Generazione delle idee per meme.
5. Valutazione delle idee.
6. Revisione delle idee non approvate, con una nuova valutazione.

Il workflow gestisce automaticamente il ciclo di revisione e interrompe i tentativi al raggiungimento del limite configurato.

## Tecnologie utilizzate

| Tecnologia | Utilizzo |
|---|---|
| Python | Linguaggio principale |
| LangGraph | Orchestrazione del workflow multi-agente |
| LangChain | Integrazione con i modelli linguistici |
| OpenAI API | Generazione e valutazione dei contenuti |
| Tavily API | Ricerca online dei trend |
| unittest | Test automatici |

## Installazione

Clonare il repository:

```bash
git clone https://github.com/TanoBont/meme-agent.git
cd meme-agent
```

Creare un ambiente virtuale:

```bash
python -m venv .venv
```

Attivarlo su Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Installare le dipendenze:

```bash
pip install -r requirements.txt
```

## Configurazione

Creare un file `.env` nella directory principale del progetto, utilizzando `.env.example` come riferimento.

Configurare le proprie chiavi API:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Le altre impostazioni disponibili sono:

```env
OPENAI_MODEL=gpt-6.1-sol
MAX_REVISIONS=2
MAX_TRENDS=5
```

- `OPENAI_MODEL`: modello OpenAI utilizzato dal sistema.
- `MAX_REVISIONS`: numero massimo di revisioni consentite per le idee non approvate.
- `MAX_TRENDS`: numero massimo di trend selezionati nella fase di classificazione.

## Esecuzione

Per avviare il sistema:

```bash
python main.py
```

Al termine dell'esecuzione vengono mostrati i trend individuati, quelli verificati e classificati, le idee generate e le relative valutazioni, insieme a un riepilogo dell'esecuzione.

## Test

Il progetto include test automatici realizzati con `unittest`, che verificano il comportamento dei singoli agenti, delle regole di valutazione e del workflow.

Per eseguire la suite:

```bash
python -m unittest discover -s tests -v
```

I test che richiedono chiamate a servizi esterni vengono eseguiti separatamente.

## Stato del progetto

Il progetto è attualmente in fase di sviluppo.

La pipeline multi-agente è stata implementata e comprende ricerca, verifica preliminare, classificazione, generazione, valutazione e revisione delle idee.

Tra i possibili sviluppi futuri rientrano la generazione automatica delle immagini dei meme, l'integrazione di ulteriori fonti di ricerca e lo sviluppo di un'interfaccia utente.