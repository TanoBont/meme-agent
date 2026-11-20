# 08 — Operations e deployment

## 1. Ambienti
- Dev e Test iniziali.
- Staging e Production introdotti prima della beta/pubblicazione.
- Database isolati per ambiente.
- Configurazione per environment.
- Segreti fuori dal repository e secret manager in ambienti gestiti.
- Dati di test non reali o adeguatamente anonimizzati.

## 2. Container e deploy
- Docker Compose per sviluppo e primi ambienti controllati.
- GitHub Actions per CI/CD.
- Deploy progressivo e health check.
- Migrazioni Alembic eseguite in modo controllato prima/durante il rilascio.
- Rollback applicativo documentato.
- Roll-forward o restore per migrazioni non reversibili.
- Nessun Kubernetes/Microservices MVP.

## 3. Release management
- SemVer.
- Tag Git e GitHub Releases.
- Changelog.
- Compatibilità API documentata.
- Migrazioni e breaking change pianificate.
- La versione Python esistente resta distinta dal nuovo prodotto web.

## 4. Dependency management
- Lockfile per dipendenze Python e frontend.
- Aggiornamenti controllati.
- Dependabot e alert GitHub.
- Scansione vulnerabilità con strumenti appropriati (es. pip-audit, npm audit).
- Verifica licenze dipendenze.
- Test di regressione dopo gli aggiornamenti.
- SBOM nelle fasi successive o dove richiesto.

## 5. Logging e osservabilità
- Log strutturati JSON.
- Livelli DEBUG/INFO/WARNING/ERROR/CRITICAL.
- correlation_id e trace_id end-to-end.
- OpenTelemetry per tracing e metriche.
- Redazione di segreti e dati personali.
- Tassonomia errori condivisa e risposta API coerente.
- Retry solo su errori temporanei e operazioni idempotenti.
- Nessuna entità ApplicationLog generica.

Separazione:
| Sistema | Scopo |
|---|---|
| Application logging | Diagnostica tecnica |
| AuditLog | Operazioni rilevanti |
| SecurityIncident | Incidenti di sicurezza |
| GenerationRun | Invocazioni AI e costi |
| BackgroundJob | Stato processi asincroni |
| OpenTelemetry | Trace e metriche |

## 6. Backup e recovery
Nessuna entità ER dedicata. Definire:
- policy e frequenza backup;
- cifratura e accessi;
- retention e copie separate;
- RPO e RTO realistici;
- backup DB e asset storage coerenti;
- restore test periodici;
- runbook e responsabilità;
- verifica integrità dopo ripristino.

I valori RPO/RTO vanno scelti in base a impatto, costi e infrastruttura reale, non inventati in fase di design.

## 7. Scalabilità e risorse
- Backend stateless e scalabile orizzontalmente quando necessario.
- Pool connessioni DB.
- Worker separati dal traffico HTTP.
- Code con priorità, timeout, retry e idempotenza.
- Rate limit per utente/endpoint/provider.
- Quote AI e limiti di concorrenza.
- Backpressure e limiti CPU/RAM/upload.
- Redis/Celery solo se misure lo giustificano.
- Object storage quando il filesystem locale non è adeguato.
- Monitorare latenza, code, errori, CPU/RAM, DB, provider e costi per utente/workflow.

## 8. UX e accessibilità
Riferimento WCAG 2.2 AA come obiettivo. Responsive desktop/tablet/mobile; Meme Studio inizialmente desktop-first. Tastiera, focus, contrasto, label, semantica, alternative testuali e stati UI coerenti.
