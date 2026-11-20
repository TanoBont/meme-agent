# 04 — Workflow applicativi

## 1. Discover pipeline
1. Definizione query e fonti ammesse.
2. Acquisition tramite provider.
3. Normalizzazione dei metadati.
4. Deduplicazione degli articoli.
5. Verifica preliminare e valutazione attendibilità.
6. Rilevamento FootballEvent.
7. Collegamento a squadre, persone e competizioni.
8. Analisi potenziale creativo.
9. Creazione/aggiornamento MemeOpportunity.
10. Ranking generale e personalizzazione feed.

Contenuti esterni sono input non attendibili: prompt injection e istruzioni presenti nelle pagine non devono essere eseguite o considerate policy. Conservare riferimenti, non copiare integralmente contenuti protetti senza base giuridica/licenza.

## 2. Interazione opportunità
- VIEW/OPEN registrano interazione.
- SAVE/UNSAVE aggiornano LibraryItem in modo transazionale.
- DISMISS è distinto dal semplice unsave.
- CREATE avvia un MemeProject e conserva la provenienza tramite riferimenti tipizzati e snapshot.

## 3. Meme Studio
1. Creazione da Discover o idea personale.
2. Raccolta del contesto e delle fonti.
3. Generazione di concept e direzione creativa.
4. Selezione/modifica del concept.
5. Generazione o scelta asset.
6. Composizione e rendering anteprima.
7. Modifiche manuali e rigenerazioni indipendenti.
8. Creazione di revisioni immutabili.
9. Approvazione manuale della revisione.
10. Export legato esattamente alla revisione approvata.

Una modifica dopo approvazione crea una nuova revisione e richiede una nuova approvazione.

## 4. AI workflow
- AIWorkflowRun rappresenta il processo coordinato.
- GenerationRun rappresenta ogni chiamata.
- Controllo quota prima dell'invocazione.
- Prenotazione quota sotto transazione/controllo concorrenza.
- Retry solo per errori temporanei e idempotenti.
- Persistenza di modello, configurazione, token, costo e risultato.
- Feedback raccolto senza addestramento o modifica automatica non autorizzata.
- Riferimenti RAG indicano quali chunk sono stati effettivamente passati al modello.

## 5. RAG
- Revisione/approvazione documento.
- Creazione versione.
- Chunking con configurazione versionata.
- Embedding e indexing job.
- Validazione indice.
- Switch atomico verso la nuova versione indicizzata.
- Retrieval ibrido, reranking e context assembly.
- Logging di retrieval e collegamento a GenerationRun.
- Evaluation su dataset versionati.

## 6. State machines
Le macchine a stati sono specifiche per dominio e documentate. Per ogni macchina definire:
- stati ammessi;
- transizioni;
- ruolo autorizzato;
- precondizioni;
- effetti collaterali;
- eventi Outbox;
- comportamento su errore/retry;
- transizioni terminali e riapertura, se ammessa.

Non introdurre una generica entità StateMachine.
