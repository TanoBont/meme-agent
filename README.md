# Meme Agent

![CI](https://github.com/TanoBont/meme-agent/actions/workflows/ci.yml/badge.svg)

Meme Agent è un progetto personale sviluppato in Python con l'obiettivo di semplificare e supportare la creazione di contenuti meme legati al mondo del calcio.

Il progetto si basa su un sistema multi-agente, orchestrato tramite LangGraph, in cui ogni agente svolge un compito specifico: dalla ricerca di notizie e trend calcistici alla generazione, valutazione e revisione di idee creative per meme.

## Funzionalità

- **Ricerca dei trend:** individua notizie e argomenti di attualità calcistica tramite Tavily.
- **Verifica delle informazioni:** analizza i risultati della ricerca e ne valuta l'attendibilità.
- **Classificazione:** assegna un punteggio ai trend in base ad attualità, interesse e potenziale umoristico.
- **Generazione delle idee:** crea proposte di meme a partire dai trend selezionati.
- **Valutazione:** analizza la qualità delle idee generate combinando controlli basati su regole e valutazioni AI.
- **Revisione automatica:** migliora le idee che non superano la valutazione, attraverso un ciclo di revisione controllato.

## Architettura

Il sistema è organizzato in sei agenti:

| Agente | Responsabilità |
|---|---|
| Research Agent | Ricerca notizie e trend calcistici |
| Verification Agent | Verifica e analizza le informazioni raccolte |
| Ranking Agent | Classifica i trend in base al punteggio |
| Creative Agent | Genera idee per meme |
| Evaluator Agent | Valuta la qualità delle idee |
| Revision Agent | Migliora le idee che necessitano di revisione |

Gli agenti collaborano attraverso un workflow orchestrato da LangGraph e condividono uno stato comune, che consente di trasferire le informazioni tra le diverse fasi.

### Sistema di ranking

I trend vengono classificati utilizzando tre criteri:

- Attualità: 40%
- Interesse: 30%
- Potenziale umoristico: 30%

### Sistema di valutazione

Le idee generate vengono valutate combinando due approcci:

- Controlli basati su regole Python: 60%
- Valutazione tramite modello AI: 40%

Le idee che non raggiungono la soglia prevista possono essere inviate al Revision Agent, che prova a migliorarle. Il processo viene ripetuto fino al raggiungimento dei criteri di valutazione o del numero massimo di tentativi configurato.

## Tecnologie utilizzate

- Python
- LangGraph
- LangChain
- OpenAI API
- Tavily API
- unittest

## Installazione

Clona il repository:

```bash
git clone https://github.com/TanoBont/meme-agent.git
cd meme-agent
```

Crea e attiva un ambiente virtuale:

```bash
python -m venv .venv
```

Su Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Installa le dipendenze:

```bash
pip install -r requirements.txt
```

## Configurazione

Crea un file `.env` nella directory principale del progetto, prendendo come riferimento `.env.example`.

Inserisci le chiavi API necessarie:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Le altre impostazioni del sistema, come il modello AI e i parametri del workflow, possono essere configurate attraverso le variabili d'ambiente previste dal progetto.

**Nota:** non condividere il file `.env` e non inserirlo nel repository, perché contiene credenziali private.

## Esecuzione

Per avviare il progetto:

```bash
python main.py
```

## Test

Il progetto include test automatici realizzati con `unittest`.

Per eseguire tutti i test:

```bash
python -m unittest discover -s tests -v
```

## Documentazione

La documentazione tecnica del progetto è disponibile nella cartella `docs/`:

- `agents.md`: descrizione dei singoli agenti.
- `architecture.md`: architettura e organizzazione del sistema.
- `configuration.md`: configurazione e variabili d'ambiente.
- `workflow.md`: descrizione del workflow multi-agente.

## Sviluppi futuri

Tra i possibili sviluppi del progetto:

- Generazione automatica delle immagini dei meme.
- Miglioramento della selezione e della qualità delle fonti.
- Ulteriore ottimizzazione dei prompt e del processo di valutazione.
- Interfaccia grafica per interagire con il sistema.