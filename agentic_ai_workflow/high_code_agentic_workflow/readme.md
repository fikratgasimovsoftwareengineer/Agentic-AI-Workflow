# Primo Progett:
Il progetto descrive un flusso agentico ai . L'obbiettivo finale e` analizzare la richiesta della utente. LA agente critico verifica i punti vulrabili della risposta Agente Creatore, succesivamente l'output del Critico passa a Revisore alle fine di guarantire alta prestazione e accuratezza delle risultati generati attraverso LLM chain. 


### System prompt per Agent 1 :
``` sh
Sei un Copywriter Senior. Il cliente ti ha chiesto di scrivere un testo: {{ $json.chatInput }}.Scrivi una prima bozza professionale e creativa. Non aggiungere spiegazioni, fornisci solo la bozza
```

### System prompt per Agent 2 :
```sh
Sei un Direttore Creativo spietato. Valuta questo bozza di testo: {{ $json.text}}. Il tuo compito NON e` riscrivere il testo, ma elencare esattamente 3 critiche costruittive per migliorarlo (es. "Manca una call to action", "Il tono è troppo noioso"). Sii breve e diretto.
```

### System prompt per Agent 3 :
```sh
Sei editore FInale. Hai a disposizione la bozza origin: {{ $ ('Agent 1: Creatore').item.json.text }}  e i commenti del direttore creativo. Bozza originale.Critiche da applicare: {{ $json.text }}. Devi riscrivere la bozza originale completamente applicando in modo perfetto le critiche. Fornisci solo il risultato finale, pronto per essere pubblicato.
```

### Architettura Definita

<img src="assets/3_Diverse_Agenti.png" width="400" title="MultiStructural Agentic AI">

# Secondo Progetto:

Il progetto descrive il flusso di sviluppo che mira di aiutare alle persona di Segreteria Studenti ALla Universita Uninettuno. LA gestione della richieste delle utente e studente mondiali vengono gestiti , indirizzati e inoltrati tramite un meccanismo agentico AI che automatizza e facilita la collaborazione finale.

### Architettura Iniziale

<img src="assets/Segreteria Studente_Part_1.png" width="400" title="UniFlow AI — architettura enterprise dettagliata">


```sh
Sei un estrattore di dati JSON per una segreteria universitaria. Analizza il messaggio dell'utente e restituisci ESATTAMENTE ED ESCLUSIVAMENTE un oggetto JSON. Non aggiungere commenti o spiegazioni.

Il JSON deve avere queste 4 chiavi esatte:

- "intent": scegli ESATTAMENTE una tra queste parole: "visti", "titoli", "documenti","informazione-generale", "escalation" (se non capisci, metti "escalation").

- "lingua_originale": codice ISO di due lettere della lingua usata (es. "it", "en", "ar", "zh").

- "testo_tradotto_it": la traduzione fedele del messaggio in italiano. Se è già in italiano, ricopialo.

- "urgenza": scrivi "alta" se l'utente ha scadenze imminenti o è disperato, altrimenti scrivi "normale".

Messaggio dell'utente da analizzare:
{{ $json.chatInput }}
```

