# 01 — Requisiti di prodotto

## 1. Utenti e valore
La piattaforma si rivolge ad appassionati di calcio e creator che desiderano:
- scoprire spunti calcistici con potenziale meme;
- comprendere il contesto e risalire alle fonti;
- creare partendo da Discover o da un'idea autonoma;
- usare l'AI come assistente, non come decisore finale;
- modificare separatamente testo, immagini e composizione;
- salvare, organizzare ed esportare le proprie creazioni.

## 2. Requisiti funzionali

### 2.1 Identity & Access
- Registrazione, autenticazione, logout, sessioni.
- Verifica email e recupero password.
- Preferenze di interfaccia, lingua, locale e fuso orario.
- Preferenze creative e squadre/persone/competizioni preferite.
- RBAC e controlli contestuali di ownership.
- Predisposizione per identità esterne, non essenziale per MVP.

### 2.2 Discover
- Feed generale e personalizzato.
- Acquisizione da fonti compatibili con termini e licenze.
- Normalizzazione e deduplicazione degli articoli.
- Identificazione e collegamento di eventi, squadre, persone e competizioni.
- Analisi del potenziale creativo e generazione di MemeOpportunity.
- Ranking generale e personalizzazione separata.
- Interazioni VIEW, OPEN, SAVE, UNSAVE, CREATE, DISMISS.
- Nessuna generazione automatica per ogni notizia.

### 2.3 Meme Studio
- Creazione da opportunità Discover o idea personale.
- Concept AI modificabile dall'utente.
- Direzione visiva e tono ironico facoltativi.
- Rigenerazione indipendente di testo, immagine e composizione.
- Editor con testo, immagini, forme, livelli, visibilità, blocco, crop, resize, rotazione, font, colori, contorni e allineamento.
- Revisioni immutabili della composizione.
- Approvazione manuale riferita alla revisione esatta.
- Export solo della revisione approvata.

### 2.4 Pipeline visuale
- Modello ibrido: template originali/licenziati e immagini AI originali.
- Asset Management centralizzato.
- Tracciamento di provenienza, licenza, attribuzione e derivazioni.
- Rendering backend con Pillow.
- Formati social principali per Instagram e TikTok nell'MVP; dimensioni e safe area da verificare prima dello sviluppo.

### 2.5 Library
- Salvataggio di progetti, versioni, asset e opportunità.
- Raccolte private.
- Salvataggio senza duplicare il contenuto originale.
- Rimozione del collegamento dalla Library senza cancellare la risorsa sorgente.
- Nessuna condivisione pubblica nell'MVP.

### 2.6 Knowledge Base & RAG
- Conoscenza dedicata alla cultura dei meme, non archivio delle news correnti.
- Documenti con workflow di revisione e approvazione.
- Chunking, embedding, indicizzazione e retrieval.
- Ricerca ibrida semantica + full-text + filtri metadati.
- Reranking e tracciamento dei chunk effettivamente forniti al modello.

### 2.7 AI Usage
- Tracciamento invocazioni e workflow.
- Provider, modello, versione, token, costi, durata, errori e retry.
- Quote e limiti verificati prima delle chiamate.
- Prenotazione temporanea e contabilizzazione effettiva sotto concorrenza.
- API key dei provider condivise lato servizio, mai chiavi individuali degli utenti.

## 3. Requisiti non funzionali
- Sicurezza: autorizzazione backend, isolamento utenti, rate limiting, gestione sicura dei segreti.
- Privacy: minimizzazione, finalità, retention, accesso, rettifica e cancellazione.
- Affidabilità: vincoli DB, idempotenza, retry controllati, backup e restore testati.
- Usabilità: responsive, accessibilità, feedback chiari, stati vuoti/caricamento/errore.
- Manutenibilità: modular monolith, API versionate, migrazioni Alembic, CI e documentazione.
- Osservabilità: log strutturati, metriche, tracing e audit distinti.
- Cost control: limiti provider, quote, budget e monitoraggio costi AI.

## 4. Fuori scope MVP
- Community interna e feed social.
- Pubblicazione social diretta.
- Video e animazioni.
- Altri sport.
- Abbonamenti, pagamenti e billing.
- Developer Platform e API client.
- Organization e Workspace.
- Microservizi e Kubernetes.
- Generazione automatica indiscriminata a partire dalle notizie.

## 5. Criteri di accettazione MVP
1. Un utente può registrarsi e gestire in sicurezza la sessione.
2. Può consultare Discover e risalire alle fonti.
3. Può creare da opportunità o idea personale.
4. Può generare e modificare concept e composizioni.
5. Solo la revisione approvata esattamente può essere esportata.
6. Può salvare e ritrovare i propri contenuti.
7. Quote, costi, errori e job sono tracciati.
8. Test di isolamento, sicurezza, integrità e flussi principali superati.
9. Privacy notice, termini, backup e procedure operative pronti per il rilascio.

## 6. Metriche da definire
Tempo di completamento creazione, tasso di approvazione, uso dell'editor, feedback sulle generazioni, latenza/errori, costi per workflow e utilizzo di Discover/Library. Definire soglie solo dopo una baseline misurata.
