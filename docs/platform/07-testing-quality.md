# 07 — Testing e qualità

## 1. Livelli
- Unit test: logica di dominio e funzioni pure.
- Integration test: PostgreSQL, pgvector, storage adapter, provider mock.
- Contract test: API OpenAPI e interfacce tra domini.
- Architecture test: dipendenze, ownership e assenza cicli.
- End-to-end: flussi utente critici con Playwright.
- Security test: autorizzazione, isolamento, upload, sessioni, rate limit e input malevoli.
- Performance/load test: API, query, code, rendering e concorrenza.
- Migration test: upgrade da versioni precedenti e integrità.
- Accessibility test: automatizzati e manuali.
- AI Evaluation: suite distinta dai test software deterministici.

## 2. Tooling previsto
- pytest per nuovo backend Python; mantenere unittest per test legacy finché necessario.
- Playwright per E2E.
- Ruff e mypy per qualità Python.
- GitHub Actions per CI.
- Test DB separato e dati sintetici/anonymized.
- Test che invocano API live separati, esplicitamente opt-in e mai requisito della CI standard.

## 3. AI Evaluation
Dataset versionati e casi rappresentativi. Metriche:
- factuality e supporto alle fonti;
- pertinenza del contesto;
- qualità e varietà creativa;
- umorismo e leggibilità;
- aderenza alle istruzioni;
- tasso di allucinazioni;
- sicurezza e contenuti non consentiti;
- costo e latenza.

Combinare controlli deterministici, LLM-as-judge calibrato e valutazione umana. Non usare feedback utente per modificare automaticamente modelli/prompt o addestrare senza processo e base appropriati.

## 4. CI
Pipeline:
1. installazione da lockfile;
2. lint e type check;
3. unit test;
4. integration test;
5. contract e architecture test;
6. migration/integrity test;
7. security/dependency scan;
8. E2E selettivi;
9. AI evaluation non-live o con fixture controllate.

Le suite live con costi provider sono separate e protette da segreti/limiti.

## 5. Criteri di qualità
Bloccare merge per regressioni critiche, violazioni dei confini di dominio, vulnerabilità elevate non accettate, migrazioni non testate o regressioni nei flussi di approvazione/export e isolamento utente.
