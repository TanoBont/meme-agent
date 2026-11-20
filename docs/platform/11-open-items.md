# 11 — Elementi da definire prima dell'implementazione

Questi punti non contraddicono le decisioni approvate: sono dettagli che richiedono specifiche, prove o informazioni aggiornate.

## 1. Modello ER
- Diagramma ER completo con cardinalità e optionalità.
- Tipi PostgreSQL, enum, check, unique e indici.
- Definizione esatta di tutte le FK composte e vincoli cross-domain.
- Politiche ON DELETE per ogni relazione.
- Schema fisico e migrazioni Alembic.
- Verifica dei vincoli di esclusività/one-of e degli indici parziali.

## 2. API e contratti
- Elenco endpoint `/api/v1`, request/response schema.
- Error code e formato error response.
- Paginazione, filtri, ordinamento.
- Idempotency key per operazioni sensibili.
- Autenticazione, refresh, CSRF/CORS e session policy.
- Rate limit e quote numeriche.

## 3. Provider e costi
- Modelli AI e provider immagini effettivi.
- Prezzi, rate limits, retention, data processing e region.
- Fallback e policy provider.
- Soglie budget e quote.
- Licenze e condizioni d'uso dei provider.
- Tavily e fonti editoriali: accesso, caching, attribution e termini.

## 4. Immagini e UX
- Dimensioni e safe area social aggiornate.
- Formati export, qualità, trasparenza e profili colore.
- Scelta editor React tra Fabric/Konva o alternative dopo proof of concept.
- Font e licenze.
- Test di usabilità e accessibilità.

## 5. Sicurezza e privacy
- Data inventory e record of processing.
- Base giuridica per ciascuna finalità.
- Retention per categoria, backup e log.
- DPIA screening e necessità effettiva.
- Ruoli privacy, DPA, sub-responsabili e trasferimenti.
- Procedure data breach e tempi di notifica.
- Verifica aggiornata GDPR, AI Act e altra normativa applicabile.
- Copyright/takedown e gestione reclami.

## 6. Operazioni
- Hosting e region.
- RPO/RTO e frequenza backup.
- Monitoring stack e soglie alert.
- Runbook incidenti, deploy e rollback.
- Strategia secrets management.
- Capacità e load test.

## 7. Decisioni non da anticipare
- Redis/Celery.
- Kubernetes/microservizi.
- Billing e abbonamenti.
- Community e condivisione pubblica.
- Social publishing, video e animazioni.
- Organization/Workspace e API client.

Queste scelte restano fuori dall'MVP finché non emergono requisiti e benefici concreti.
