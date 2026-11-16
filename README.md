# Meme Agent

**Meme Agent** è un progetto personale sviluppato con l'obiettivo di realizzare un sistema multi-agente basato su intelligenza artificiale, capace di individuare trend online, analizzarli e trasformarli in contenuti creativi sotto forma di meme.

Il sistema è progettato per automatizzare le diverse fasi del processo, dalla ricerca degli argomenti alla generazione e valutazione delle idee, fino alla creazione dell'immagine finale.

## Obiettivi del progetto

- Ricercare trend e argomenti di attualità online.
- Analizzare e verificare le informazioni raccolte.
- Classificare i trend in base a rilevanza, interesse e potenziale umoristico.
- Generare idee creative per meme attraverso modelli di intelligenza artificiale.
- Valutare le idee generate e selezionare quelle più adatte.
- Automatizzare il processo di creazione dei contenuti.

## Architettura prevista

Il progetto prevede diversi agenti specializzati, ognuno responsabile di una specifica fase del processo:

| Agente | Responsabilità |
|---|---|
| Research Agent | Ricerca dei trend online |
| Verification Agent | Verifica delle informazioni |
| Ranking Agent | Classificazione dei trend |
| Creative Agent | Generazione di idee per meme |
| Evaluator Agent | Valutazione delle idee generate |

## Tecnologie

- Python
- LangGraph
- OpenAI API
- Google Gemini
- Tavily
- Reddit API

## Stato del progetto

**In sviluppo.**

È stata realizzata una prima versione della pipeline, con agenti Python separati e uno stato condiviso per gestire i dati tra le diverse fasi.

Le attività successive prevedono l'integrazione di LangGraph, dei servizi di ricerca online e dei modelli di intelligenza artificiale, oltre alla realizzazione della generazione automatica delle immagini.

## Installazione

1. Clonare il repository:

   ```bash
   git clone https://github.com/TanoBont/meme-agent.git
   ```

2. Entrare nella cartella del progetto:

   ```bash
   cd meme-agent
   ```

3. Creare e attivare un ambiente virtuale:

   ```bash
   python -m venv .venv
   ```

4. Installare le dipendenze:

   ```bash
   pip install -r requirements.txt
   ```

5. Creare il file `.env` partendo da `.env.example` e inserire le proprie chiavi API quando necessarie.


*Progetto personale in continuo sviluppo.*