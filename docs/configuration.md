# Configurazione del progetto

## 1. Panoramica

Meme Agent utilizza variabili d'ambiente per gestire le credenziali dei servizi esterni e i parametri di configurazione del workflow.

Le impostazioni vengono caricate all'avvio dell'applicazione tramite `python-dotenv` e centralizzate nel modulo `app/config.py`.

Le credenziali personali non devono essere inserite direttamente nel codice sorgente né pubblicate nel repository.

## 2. File di configurazione

Il progetto utilizza due file distinti:

- `.env`: contiene le credenziali e le configurazioni locali dell'utente. Non deve essere versionato.
- `.env.example`: fornisce un esempio delle variabili necessarie per configurare il progetto.

Per iniziare, creare un file `.env` nella directory principale, prendendo come riferimento `.env.example`.

## 3. Variabili d'ambiente

### 3.1 OpenAI

| Variabile | Descrizione |
|---|---|
| `OPENAI_API_KEY` | Chiave API necessaria per accedere ai modelli OpenAI |
| `OPENAI_MODEL` | Identificativo del modello linguistico utilizzato |

Il progetto utilizza OpenAI per le attività di verifica, classificazione, generazione, valutazione e revisione.

Il modello viene inizializzato attraverso la funzione `get_openai_model()`, definita in `app/llms.py`.

Per i modelli della famiglia GPT-6 viene utilizzata la Responses API con livello di reasoning `low`.

### 3.2 Tavily

| Variabile | Descrizione |
|---|---|
| `TAVILY_API_KEY` | Chiave API necessaria per effettuare ricerche online |

Tavily viene utilizzato dal Research Agent per raccogliere informazioni e risultati relativi ai trend calcistici.

### 3.3 Parametri del workflow

| Variabile | Valore predefinito | Descrizione |
|---|---:|---|
| `MAX_REVISIONS` | `2` | Numero massimo di revisioni delle idee non approvate |
| `MAX_TRENDS` | `5` | Numero massimo di trend selezionati nella fase di classificazione |

Questi parametri permettono di modificare il comportamento del workflow senza intervenire direttamente sul codice.

## 4. Esempio di configurazione

Un esempio di file `.env` è il seguente:

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-6.1-sol

# Tavily
TAVILY_API_KEY=your_tavily_api_key

# Configurazione workflow
MAX_REVISIONS=2
MAX_TRENDS=5
```

I valori mostrati sono indicativi. Le chiavi API devono essere sostituite con le proprie credenziali.

## 5. Caricamento della configurazione

Il modulo `app/config.py` utilizza `load_dotenv()` per caricare le variabili definite nel file `.env`.

Le impostazioni vengono poi rese disponibili agli altri componenti del progetto attraverso variabili Python.

Per i parametri numerici vengono utilizzati valori predefiniti nel caso in cui non siano specificati nel file di configurazione.

## 6. Sicurezza delle credenziali

Per evitare la pubblicazione accidentale di informazioni riservate:

- Il file `.env` deve essere escluso dal controllo versione tramite `.gitignore`.
- Le chiavi API non devono essere inserite direttamente nei file Python.
- Il repository deve contenere esclusivamente `.env.example`, senza credenziali reali.
- Prima di ogni commit è opportuno verificare che non siano presenti file contenenti segreti.

## 7. Riferimenti al codice

I principali moduli coinvolti nella configurazione sono:

- `app/config.py`: caricamento delle variabili d'ambiente.
- `app/llms.py`: inizializzazione dei modelli linguistici.
- `app/tools/search.py`: integrazione con Tavily.
- `.env.example`: esempio delle variabili di configurazione.