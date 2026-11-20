# 02 — Architettura target

## 1. Stile
Modular Monolith multiutente. Un'unica applicazione backend organizzata in domini con ownership e interfacce esplicite. L'estrazione futura di servizi sarà valutata solo sulla base di esigenze misurate.

## 2. Stack previsto
| Livello | Tecnologia | Uso |
|---|---|---|
| Frontend | Next.js, React, TypeScript | UI e routing |
| Backend | FastAPI, Python | API e casi d'uso |
| AI | LangGraph | workflow multi-agent |
| LLM | OpenAI tramite adapter | analisi e generazione |
| Search | Tavily tramite adapter | ricerca esterna |
| Database | PostgreSQL | persistenza transazionale |
| Vector | pgvector | embedding/retrieval |
| RAG | LangChain e servizi applicativi | retrieval/context assembly |
| Image | Pillow | rendering/export |
| Editor | React; valutazione Fabric.js/Konva | canvas interattivo |
| Container | Docker/Compose | ambienti riproducibili |
| Migration | Alembic | schema versionato |

Librerie, provider immagini, hosting e storage definitivo richiedono verifica di manutenzione, licenze, costi e proof of concept.

## 3. Componenti
- Frontend web.
- Backend/API.
- AI engine.
- Worker per processi asincroni e rendering.
- PostgreSQL/pgvector.
- Storage adapter: filesystem locale iniziale, object storage in seguito.
- Adapter provider esterni.

Redis/Celery solo se esigenze reali lo giustificano. Nessun Kubernetes o microservizio nell'MVP.

## 4. Domini
1. Identity & Access
2. Asset Management
3. Football Catalog
4. Discover
5. Meme Studio
6. Library
7. Knowledge Base & RAG
8. AI Usage
9. Governance & Protection

Componenti trasversali: Trust & Safety, Notifications, Background Jobs, Application Configuration, Generation Feedback. Billing futuro.

## 5. Domain ownership
- Ogni dominio possiede regole e repository interni.
- Gli altri domini usano interfacce pubbliche.
- Vietato l'accesso diretto ai repository interni altrui.
- Vietate dipendenze circolari.
- Operazioni sincrone tramite casi d'uso/interfacce.
- Operazioni asincrone tramite Outbox e consumer idempotenti.
- Foreign key tra domini consentite per integrità referenziale, senza trasferire ownership.

## 6. API
REST `/api/v1`, OpenAPI, errori coerenti, validazione e autorizzazione backend. Nessuna entità ApiClient/ApiClientCredential nell'MVP; Developer Platform futura.

## 7. Multi-tenancy
Database condiviso con isolamento logico per `user_id`. Query e use case verificano ownership; foreign key composte proteggono i collegamenti tra risorse. RLS PostgreSQL opzionale come difesa aggiuntiva dopo verifica del modello di connessione. Nessuna Organization/Workspace MVP.

## 8. Provider e segreti
Adapter per provider AI, search e immagini. Nessuna entità generica ExternalServiceProvider. Chiavi API solo backend, in secret store per ambienti gestiti; `.env` locale ignorato da Git. Non esporre chiavi al browser.

## 9. Outbox e job
`OutboxEvent` scritto nella stessa transazione del cambiamento di dominio. Consegna at-least-once; consumer idempotenti. `BackgroundJob` governa l'esecuzione tecnica, mentre i record di dominio mantengono lo stato funzionale.

## 10. Versioni e release
SemVer, tag Git, GitHub Releases, changelog, compatibilità API documentata, migrazioni e procedure di rollback. La release Python preesistente resta distinta dalla futura web platform.
