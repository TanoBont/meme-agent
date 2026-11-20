# 06 — Integrità dati e persistenza

## 1. Database
PostgreSQL come database transazionale e pgvector per embedding. Alembic per migrazioni versionate.

## 2. Vincoli
- PK UUID dove appropriato.
- FK esplicite.
- UNIQUE semplici/composte e indici parziali.
- CHECK per enum e invarianti locali.
- NOT NULL quando l'assenza non è semanticamente valida.
- FK composte per ownership e coerenza tra risorsa/versione.
- Vincoli condizionali per riferimenti tipizzati (es. LibraryItem).
- JSONB solo per strutture variabili con validazione schema.
- Indici motivati da query e pattern di accesso.

## 3. Versionamento e immutabilità
AssetVersion, CompositionRevision, configurazioni di indicizzazione e prezzi/modelli versionati non si sovrascrivono dopo l'uso. Le modifiche creano nuove versioni. I record storici necessari ad audit e provenienza sono preservati secondo retention.

## 4. Concorrenza
- Optimistic locking come default.
- Pessimistic locking per sezioni critiche e prenotazioni quota.
- Quote AI riservate e contabilizzate in transazioni concorrenti-safe.
- Job con lock, idempotency key e lease/timeout.
- Outbox atomica con il cambiamento di dominio.
- Consumer idempotenti per consegna at-least-once.

## 5. Cancellazioni
Definire esplicitamente CASCADE, RESTRICT e SET NULL per ogni relazione. Cancellazione account coordinata per dati utente, asset, versioni, Library, sessioni, job e riferimenti esterni. Separare cancellazione logica, archiviazione e cancellazione fisica. Le esigenze di audit, obblighi legali e retention devono essere bilanciati e documentati.

## 6. Migrazioni
- Ogni modifica schema tramite Alembic.
- Migrazioni revisionate e testate su DB vuoto e su dati realistici.
- Backfill separati quando necessario.
- Strategie expand/contract per cambi compatibili.
- Rollback documentato; non presumere che ogni migrazione dati sia reversibile.
- Nessuna modifica manuale non tracciata allo schema.

## 7. Integrità da testare
- Asset.current_version appartiene allo stesso asset.
- LibraryItem ha esattamente il riferimento coerente con item_type.
- Collection item e risorsa appartengono allo stesso utente.
- Export punta alla revisione approvata esatta.
- Una nuova revisione invalida la possibilità di usare un'approvazione precedente.
- Unique partial index e vincoli di deduplicazione.
- Stato e transizioni consentiti.
- Nessun riferimento cross-user.
- Idempotenza Outbox/job e concorrenza quote.
