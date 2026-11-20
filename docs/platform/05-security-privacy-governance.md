# 05 — Sicurezza, privacy e governance

## 1. Security by design
Threat modeling STRIDE per asset, trust boundary, entry point e flussi dati. Il modello minacce dovrà essere mantenuto in `docs/security/threat-model.md` quando la documentazione verrà integrata nel repository.

Controlli:
- autenticazione robusta e sessioni sicure;
- Argon2id per password;
- refresh token rotation e reuse detection;
- rate limiting login, token e API;
- autorizzazione backend e ownership su ogni risorsa;
- protezione CSRF dove applicabile, CORS restrittivo, CSP e security headers;
- validazione input/output e protezione da injection;
- upload sicuro, MIME sniffing reale, limiti, malware scan;
- storage privato e URL firmati con scadenza;
- segreti server-side e secret manager;
- dipendenze scansionate e aggiornate;
- incident response e audit.

## 2. Multi-tenancy e access control
Shared database con isolamento logico per utente. Verifiche ownership in use case e query; foreign key composte dove necessario. RLS può essere aggiunta come defense-in-depth. Non assumere che UUID non prevedibili sostituiscano l'autorizzazione.

## 3. Privacy e GDPR
Progettare i trattamenti secondo finalità, minimizzazione, trasparenza, accuratezza, limitazione conservazione, integrità e riservatezza.
- Mappare categorie di dati, finalità, base giuridica, destinatari e trasferimenti.
- Privacy notice chiara e aggiornata.
- Gestione richieste accesso, rettifica, cancellazione, portabilità, limitazione e opposizione.
- Consensi registrati solo quando il consenso è la base appropriata; non usare un consenso generico per tutto.
- Retention per categoria e finalità, cancellazione/anonymizzazione verificabile.
- Data deletion orchestrata e propagata ai sistemi collegati.
- Valutare necessità di DPIA e ruoli titolare/responsabile con consulenza competente.
- Verificare hosting, sub-responsabili, trasferimenti internazionali e accordi.

La conformità effettiva non può essere dichiarata dalla sola progettazione: richiede verifica normativa e legale aggiornata prima di beta/pubblicazione.

## 4. AI governance e normativa
- Documentare scopo, capacità, limiti e supervisione umana.
- Distinguere output AI da fatti e fonti.
- Proteggere contro prompt injection e data leakage.
- Tracciare provider, modello, configurazione, input/output metadata e costi con minimizzazione.
- Verificare policy provider, retention, uso dati, localizzazione e DPA.
- Valutare obblighi applicabili del quadro normativo UE sull'AI e relative scadenze prima del rilascio; non presumere classificazioni o esenzioni senza analisi.

## 5. Proprietà intellettuale e licenze
- Ogni asset ha provenienza e licenza/evidenza d'uso.
- Template originali o con licenza verificata.
- Non assumere che immagini reperite sul web siano riutilizzabili.
- Verificare termini e policy dei provider immagini AI.
- Gestire attribuzione e limitazioni d'uso.
- Definire procedura per segnalazioni copyright e rimozione.
- Conservare evidenze e audit delle verifiche.
- Evitare di replicare integralmente articoli; usare metadati/link/sintesi nel rispetto dei diritti.

## 6. Logging e audit
Non registrare password, token, API key o segreti. Minimizzare e redigere dati personali e contenuti sensibili. Accesso ai log limitato e retention definita.
Distinguere:
- application logs: diagnostica tecnica;
- AuditLog: azioni rilevanti;
- SecurityIncident: incidenti;
- GenerationRun: invocazioni AI;
- BackgroundJob: esecuzione tecnica asincrona.

## 7. Incident management
Definire rilevazione, classificazione, contenimento, investigazione, comunicazione, remediation e post-mortem. Valutare gli obblighi di notifica entro i termini previsti dalla normativa applicabile, con supporto legale/DPO se presente.
