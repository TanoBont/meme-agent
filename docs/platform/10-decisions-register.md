# 10 — Registro delle decisioni

Questo registro riassume le decisioni progettuali approvate nella conversazione. Le verifiche 8.14–8.32 sono state considerate approvate secondo l'opzione standard A; ciò non sostituisce la successiva validazione implementativa.

## Prodotto
- Piattaforma web per meme calcistici, calcio-only iniziale.
- Discover generale e personalizzato; non semplice news aggregator.
- Creazione da Discover o idea personale.
- AI assistiva; utente mantiene controllo.
- Rigenerazione separata di testo/immagine/composizione.
- Approvazione manuale obbligatoria.
- Pipeline immagini ibrida: template originali/licenziati e immagini AI.
- Export Instagram/TikTok MVP, formati da verificare.
- Community interna, video/animazioni e social publishing futuri.

## Architettura
- Modular Monolith, multi-user dall'inizio.
- Next.js/React/TypeScript, FastAPI/Python, LangGraph, OpenAI adapter, Tavily adapter.
- PostgreSQL + pgvector; LangChain/RAG; Pillow.
- Docker/Compose; filesystem locale iniziale, object storage futuro.
- Redis/Celery solo se giustificati; niente Kubernetes/microservizi MVP.
- REST `/api/v1`, OpenAPI.
- Provider abstraction; no ExternalServiceProvider.
- Shared DB + logical multi-tenancy; no Organization/Workspace MVP.
- No ApiClient/ApiClientCredential MVP.

## Modello e domini
- Nove domini: Identity & Access, Asset Management, Football Catalog, Discover, Meme Studio, Library, Knowledge Base & RAG, AI Usage, Governance & Protection.
- Asset Management centralizzato.
- GenerationRun singola invocazione; AIWorkflowRun workflow complessivo.
- Nessun AIUsageLedger duplicato.
- OutboxEvent transactional outbox, at-least-once, consumer idempotenti.
- BackgroundJob non sostituisce i record di dominio.
- State machine per dominio, no entità generica.
- Library salva riferimenti, non duplica contenuti.
- No generic SearchQueryHistory/SearchIndex/ApplicationLog.
- Billing futuro, non MVP.
- Backup e retention documentati operativamente, non entità ER.
- Import/export central service senza nuova entità generica.
- Optimistic locking default, pessimistic per casi specifici.
- Revisioni e versioni immutabili.

## Verifiche trasversali 8.14–8.32
- **8.14 Backup & Recovery:** procedure, RPO/RTO e restore test, nessuna entità ER.
- **8.15 Provider integrations:** Provider Abstraction, no ExternalServiceProvider.
- **8.16 REST API:** `/api/v1`, OpenAPI; Developer Platform futura.
- **8.17 Import/Export:** servizio centrale, progressivo, no nuove entità.
- **8.18 Outbox:** OutboxEvent atomico, at-least-once, consumer idempotenti.
- **8.19 Concorrenza:** optimistic default, pessimistic selettivo.
- **8.20 State machines:** specifiche per dominio, documentate.
- **8.21 PostgreSQL:** vincoli rigorosi, indici mirati, Alembic, integrity test.
- **8.22 Testing:** unit/integration/contract/E2E/security/performance; CI; AI Evaluation separata.
- **8.23 Domain boundaries:** Modular Monolith, ownership rigorosa, no repo interni altrui, no cicli.
- **8.24 Threat modeling:** STRIDE e revisione periodica.
- **8.25 Deployment:** Dev/Test iniziali, Staging/Prod per beta, Docker, CI/CD, rollback.
- **8.26 Release:** SemVer, tag, changelog, compatibilità API e migrazioni.
- **8.27 Dependencies:** lockfile, Dependabot, vulnerability scan, licenze, SBOM successivo.
- **8.28 Logging:** JSON strutturato, correlation/trace ID, OpenTelemetry, redazione PII/segreti; no ApplicationLog entity.
- **8.29 Scalabilità:** backend stateless, worker/code, quote, rate limit, backpressure, scaling progressivo.
- **8.30 UX/accessibilità:** responsive, obiettivo WCAG 2.2 AA, editor desktop-first.
- **8.31 Dipendenze domini:** ownership, interfacce pubbliche, no cicli, Outbox per asincrono.
- **8.32 Revisione ER:** modello concettualmente coerente; nessuna nuova entità approvata; schema SQL/diagramma fisico ancora da validare.

## Principi di governance
- Nessuna nuova entità ER senza responsabilità e necessità dimostrata.
- Nessuna tecnologia infrastrutturale prematura.
- Distinguere sempre progettato, implementato e verificato.
- Privacy, sicurezza, GDPR, AI regulation, licenze e proprietà intellettuale incluse fin dall'inizio.
