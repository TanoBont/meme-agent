# 03 — Modello di dominio ed entità ER

**Nota:** questo è un inventario concettuale consolidato, non ancora uno schema SQL definitivo. Tipi, nullabilità, cardinalità e vincoli fisici dovranno essere specificati nel diagramma ER e nelle migrazioni.

## 1. Identity & Access
Entità:
- `User`
- `UserCredential`
- `UserSession`
- `UserActionToken`
- `ExternalIdentity`
- `Role`, `Permission`, `RolePermission`, `UserRole`, `UserRoleHistory`
- `UserPreference`, `UserCreativePreference`
- `UserFavoriteTeam`, `UserFavoritePlayer`, `UserFavoriteCompetition`

Regole:
- Email memorizzata in un solo campo; unicità case-insensitive tramite indice su `lower(email)`, senza colonna email_normalized.
- Password con Argon2id.
- Refresh token rotation, family ID, reuse detection e revoca della famiglia.
- `UserActionToken` con purpose esplicito per verifica email/reset password.
- RBAC combinato con ownership e contesto della risorsa.
- API key provider non sono credenziali degli utenti.

## 2. Asset Management
Entità:
- `Asset`: UUID, owner nullable per asset di piattaforma, tipo, titolo/descrizione, visibilità, stato, current version, timestamps e deleted_at.
- `AssetVersion`: immutabile; unique(asset_id, version_number), metadata file, checksum SHA-256, dimensioni/durata e JSONB validato.
- `AssetStorageObject`: uno o più oggetti storage per versione, ruolo, provider/key/stato; un solo primary attivo per versione.
- `AssetSource`: USER_UPLOAD, AI_GENERATED, PLATFORM_CREATED, EXTERNAL_SOURCE, DERIVED; provenienza e riferimento.
- `License`, `AssetLicense`, `AssetUsagePermission`: diritti, attribuzione, evidenze e stato verifica.
- `AssetDerivation`: relazioni tra versioni sorgente e destinazione, tipo derivazione; prevenire cicli.

Regole:
- FK composta per assicurare che `Asset.current_version_id` appartenga allo stesso asset.
- Non inferire diritti automaticamente.
- Cancellazione coordinata con domini e account.
- Upload: MIME reale, limiti, malware scan, storage privato, chiavi non prevedibili, autorizzazione backend, URL firmati, checksum e backup.

## 3. Football Catalog
Entità:
- `Team`, `TeamAlias`
- `FootballPerson`, `PersonAlias`
- `Player` (sottotipo one-to-one), `Coach` (sottotipo one-to-one)
- `PlayerTeamMembership`, `CoachTeamMembership`
- `Competition`, `CompetitionEdition`
- `TeamExternalId`, `PersonExternalId`, `CompetitionExternalId`
- `EventTeam`, `EventPerson`, `EventCompetition` (associazioni con FootballEvent, nel dominio Discover)

Attributi/semantica:
- Team: country_code, city, founded_year, logo_asset_id, status ACTIVE/INACTIVE/DISSOLVED, team_type CLUB/NATIONAL_TEAM/OTHER, gender_category MEN/WOMEN/MIXED/UNKNOWN, age_category SENIOR/U21/U19/YOUTH/OTHER.
- Player: position GK/DEF/MID/FWD; preferred_foot LEFT/RIGHT/BOTH/UNKNOWN.
- Coach: coaching_level.
- Persona può essere sia Player sia Coach.
- Membership con date e tipo/ruolo; niente numero maglia generale (stagionale) né contratto legale.
- Competition type LEAGUE/CUP/TOURNAMENT/FRIENDLY/OTHER; scope NATIONAL/CONTINENTAL/INTERNATIONAL/LOCAL.
- CompetitionEdition unique(competition_id, season_label), date e stato.
- External ID unique(provider, external_id); dedup prudente, merge reversibile e audit.
- Non modellare ora calendari completi, statistiche, contratti o trasferimenti.

## 4. Discover
Entità:
- `NewsSource`, `Article`
- `FootballEvent`
- `EventType`
- `ArticleEvent`
- `EventTeam`, `EventPerson`, `EventCompetition`
- `MemeOpportunity`
- `UserOpportunityInteraction`
- `AcquisitionRecord`
- `DiscoverProcessingRun`
- `MemeProjectSourceReference` (nel dominio Meme Studio)

Regole:
- NewsSource è la fonte editoriale; provider acquisizione è il mezzo tecnico, concetti distinti.
- Article ed evento non sono la stessa cosa: più articoli possono riferirsi a un evento.
- EventType: MATCH, TRANSFER, STATEMENT, INJURY, CONTROVERSY, REFEREE_DECISION, RECORD, VIRAL_MOMENT, OTHER.
- FootballEvent status DETECTED, UNDER_REVIEW, CONFIRMED, DISPUTED, ARCHIVED, MERGED; merge reversibile tramite merged_into_event_id.
- MemeOpportunity è condivisa globalmente; un evento può avere più opportunità.
- Separare factual_context da creative_direction; includere potenziale, rilevanza, confidence, score, valid_from, expires_at, last_evaluated_at e status DRAFT/ACTIVE/EXPIRED/DISMISSED/ARCHIVED.
- UserOpportunityInteraction registra VIEW/OPEN/SAVE/UNSAVE/CREATE/DISMISS. `LibraryItem` conserva lo stato corrente del salvataggio; SAVE/UNSAVE transazionali e DISMISS distinto.
- AcquisitionRecord registra provider, query, external_result_id, retrieved_at, raw_metadata, status e article_id opzionale.
- DiscoverProcessingRun registra stato, retry ed errori con riferimenti tipizzati.
- Deduplicazione articoli separata da deduplicazione eventi.
- Non memorizzare integralmente gli articoli in automatico: preferire metadata, link e sintesi compatibili con licenze.

Ranking iniziale da calibrare:
- meme potential 30%;
- recency 20%;
- creative potential 20%;
- football context 15%;
- confidence 15%.
Personalizzazione separata dal ranking generale.

## 5. Meme Studio
Entità:
- `MemeProject`
- `MemeProjectSourceReference`
- `MemeConcept`
- `MemeVersion`
- `Composition`
- `CompositionRevision`
- `CanvasElement`
- `CompositionApproval`
- `MemeExport`
- `CompositionFormatPreset`
- `MemeProjectAIWorkflow`
- `MemeVersionGeneration`

Regole:
- SourceReference usa FK tipizzate e snapshot, non FK polimorfica; esattamente un tipo di riferimento valorizzato.
- Max un concept selezionato per progetto.
- MemeVersion con parent_version_id, version_number, snapshot creativo/testo, selected_image_asset_version_id e stato.
- Composition MASTER o FORMAT_VARIANT; una composizione per MemeVersion; varianti con provenienza.
- CompositionRevision immutabile, snapshot completo, revision number, parent revision, autore e change summary.
- CanvasElement riferito a CompositionRevision, tipo TEXT/IMAGE/SHAPE, coordinate/dimensioni/rotazione/z-index e properties JSONB.
- CompositionApproval riferita alla revisione esatta; APPROVED/REJECTED/CHANGES_REQUESTED. Nuova revisione richiede nuova approvazione.
- MemeExport riferito alla revisione approvata esatta e a un nuovo Asset finale; PNG/JPG/WEBP.
- CompositionFormatPreset: nome, platform, format_code, width/height/aspect_ratio, safe_area_config, export_config, active, version_number; unique(format_code, version_number), versionato e non sovrascritto.
- Editor: canvas, livelli, testo, immagini, forme, allineamento, crop, resize, rotazione, font, colori, contorni, undo/redo.
- Pillow per rendering backend; Fabric.js/Konva da valutare per frontend.

## 6. Library
Entità:
- `LibraryItem`
- `LibraryCollection`
- `LibraryCollectionItem`

Regole:
- LibraryItem contiene user_id, item_type, riferimenti tipizzati nullable a MemeProject/MemeVersion/Asset/MemeOpportunity e pinned AssetVersion opzionale.
- Esattamente un riferimento coerente con item_type.
- Indici unique parziali per utente e target per tipo.
- Rimuovere un item elimina il collegamento, non la risorsa.
- LibraryCollection e LibraryCollectionItem con vincoli composti per ownership; user_id ridondante nella tabella associativa ammesso per enforcement.
- Unicità collection/item e position.
- favorite/archive timestamps nullable e indipendenti.
- Privata nell'MVP; niente condivisione pubblica.

## 7. Knowledge Base & RAG
Entità:
- `KnowledgeDocument`, `KnowledgeDocumentVersion`
- `KnowledgeChunkSet`, `KnowledgeChunk`, `ChunkEmbedding`
- `ChunkingConfiguration`, `EmbeddingConfiguration`, `IndexingProfile`
- `KnowledgeIndexingJob`
- `MemeTemplate`, `MemeExample`
- `KnowledgeContribution` (futura)
- `RAGEvaluationDataset`, `RAGEvaluationCase`, `RAGEvaluationRun`, `RAGEvaluationResult`, `EvaluationBaseline`
- `RAGRetrievalRun`, `RAGRetrievalResult`

Regole:
- Document status DRAFT/PENDING_REVIEW/APPROVED/REJECTED/ARCHIVED.
- Versioni approvate conservate; una nuova versione non disattiva quella corrente finché non approvata.
- Index status NOT_INDEXED/QUEUED/PROCESSING/READY/FAILED/OUTDATED.
- Retry 3 tentativi con backoff 30/60/120 secondi; distinguere errori temporanei e permanenti.
- Switch atomico dell'indice.
- Configurazioni chunking/embedding immutabili e versionate dopo l'uso.
- MemeTemplate/MemeExample usano Asset centrale e non duplicano licenze.
- KnowledgeContribution futura: ownership utente, licenza piattaforma versionata accettata, moderazione.
- Retrieval ibrido pgvector + PostgreSQL FTS + filtri metadata + reranking.
- Valutazione: Precision@K, Recall@K, MRR, nDCG, rilevanza, copertura, ridondanza, faithfulness, hallucination, qualità contesto/umorismo.
- RAGRetrievalRun/Result tracciano query, chunk/versione, score, model/config, timing e collegamento a GenerationRun.

## 8. AI Usage
Entità:
- `GenerationRun`
- `AIWorkflowRun`
- `AIProvider`
- `AIModelConfiguration`
- `AIModelPricing`
- `UsagePolicy`
- `UserUsageAllocation`
- `GenerationKnowledgeReference`
- `GenerationFeedback`
- collegamenti Meme Studio `MemeProjectAIWorkflow`, `MemeVersionGeneration`

Regole:
- GenerationRun è la singola invocazione, con user_id nullable solo per invocazioni di sistema, domain, operation, provider/model/version, status, input/output metadata, token, costo stimato/effettivo, timestamps, error, parent_run_id, correlation_id, retry_count e config snapshot.
- AIWorkflowRun è il workflow complessivo; GenerationRun.workflow_run_id nullable.
- No AIUsageLedger duplicato.
- Quota verificata prima della chiamata; prenotazione temporanea e contabilizzazione effettiva concorrente-safe.
- GenerationKnowledgeReference conserva i chunk realmente inviati, con ruolo CONTEXT/EXAMPLE/TEMPLATE_REFERENCE/HUMOR_GUIDANCE/OTHER.
- GenerationFeedback: rating opzionale, tipo POSITIVE/NEGATIVE/INACCURATE/NOT_RELEVANT/NOT_FUNNY/POOR_QUALITY/OTHER, commento; non modifica automaticamente prompt o training.

## 9. Governance & Protection e componenti trasversali
Entità:
- `PrivacyRequest`
- `ConsentRecord`
- `AccountDeletionRequest`
- `DataDeletionJob`
- `AuditLog`
- `SecurityIncident`
- `IncidentAction`
- `ContentReport`, `ModerationReview`, `ModerationAction` (Trust & Safety, futura community/beta)
- `Notification`, `NotificationPreference`, `NotificationDelivery`
- `BackgroundJob`
- `ApplicationConfiguration`, `ApplicationConfigurationVersion`, `SecretReference`

Regole:
- PrivacyRequest: accesso, rettifica, cancellazione, portabilità, limitazione, opposizione.
- ConsentRecord solo per consensi realmente necessari e dimostrabili.
- AccountDeletionRequest/DataDeletionJob coordinano cancellazione e anonimizzazione.
- AuditLog per operazioni rilevanti; non sostituisce log tecnico.
- SecurityIncident e IncidentAction per incident response.
- Moderazione: report, decisione e azione sono concetti distinti; riferimenti tipizzati, no polymorphic FK.
- Notification MVP in-app; email beta, push successivo. Notifiche di sicurezza non disattivabili come marketing.
- BackgroundJob: stato, priorità, payload, schedule/start/end, attempts/max, last error, idempotency key, lock, next retry, timeout. Non sostituisce i record di esecuzione del dominio.
- ApplicationConfiguration e versioni; SecretReference contiene solo riferimenti a secret store, mai segreti.
- Nessuna entità generica ApplicationLog, SearchQueryHistory, SearchIndex, RetentionPolicy o Backup.

## 10. Entità future non MVP
- `SubscriptionPlan`, `UserSubscription`, `PaymentTransaction`, `SubscriptionPlanVersion`.
- Community/contributi pubblici e moderazione estesa.
- API client/developer platform.
- Organization/Workspace.
