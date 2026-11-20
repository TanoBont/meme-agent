# 00 — Visione e contesto

## 1. Visione
Meme Agent è concepito come piattaforma web AI-powered per appassionati di calcio e creator. Aiuta a individuare notizie, episodi e trend con potenziale umoristico e a trasformarli in meme attraverso un ambiente creativo assistito dall'AI.

Non è un semplice aggregatore di notizie e non genera automaticamente un meme per ogni notizia: l'utente guida la scoperta, sceglie cosa esplorare e mantiene il controllo creativo e l'approvazione finale.

## 2. Ambito
- Dominio iniziale: calcio.
- Target: applicazione web multiutente.
- Primo utilizzo: ambiente locale.
- Evoluzione: beta privata e successiva pubblicazione.
- Community interna: futura, non MVP.
- Pubblicazione social diretta: futura, non MVP.
- Animazioni e video: futuri, non MVP.

## 3. Principi
1. Human-in-the-loop e approvazione manuale.
2. Distinzione tra fatti, informazioni incerte e direzione creativa.
3. Provenienza verificabile di notizie e asset.
4. Privacy e sicurezza by design.
5. Modularità con confini di dominio espliciti.
6. Evoluzione incrementale senza infrastruttura prematura.
7. Documentazione versionata e sincronizzata con il codice.

## 4. Stato del prodotto
Il repository preesistente contiene un'applicazione Python multi-agent con LangGraph, agenti di ricerca/verifica/ranking/creatività/valutazione/revisione e test. La piattaforma web descritta nei documenti è un target futuro, non una funzionalità già disponibile.

La release esistente deve restare identificabile e distinta dalla futura applicazione web. Non riutilizzare tag o versioni in modo ambiguo.

## 5. Glossario
- **Discover:** area per esplorare notizie, eventi e opportunità creative.
- **Article:** contenuto editoriale esterno identificato tramite fonte e metadati.
- **FootballEvent:** evento calcistico normalizzato.
- **MemeOpportunity:** opportunità creativa derivata da uno o più eventi.
- **Meme Studio:** ambiente di ideazione, composizione, modifica e approvazione.
- **Asset:** risorsa digitale centralizzata.
- **AssetVersion:** versione immutabile di un asset.
- **GenerationRun:** singola invocazione AI.
- **AIWorkflowRun:** workflow AI composto da più invocazioni.
- **OutboxEvent:** evento persistito atomicamente con una modifica di dominio.
- **RAG:** retrieval-augmented generation.
- **MVP:** prima versione utilizzabile a perimetro limitato.
