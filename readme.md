# 🤖 Multi-Agent AI Orchestration (100% Local & Private)

Questo repository dimostra la costruzione di un'infrastruttura AI locale (Self-Hosted) e l'orchestrazione di un sistema Multi-Agente per l'automazione aziendale. 

Il progetto applica il pattern cognitivo **"Reflection & Self-Correction"** (Creatore -> Critico -> Revisore) per generare output di altissima qualità senza l'intervento umano, mantenendo i costi operativi a zero e garantendo la totale privacy dei dati aziendali.

## 🏗 Architettura del Sistema
L'infrastruttura è costruita e deployata tramite Docker Compose:
- **Orchestratore:** [n8n](https://n8n.io/) (Self-hosted)
- **LLM Engine:** [Ollama](https://ollama.ai/) (Esecuzione locale)
- **Modello AI:** Meta LLaMA 3.1 / 3.2 (Integrazione diretta tramite Docker Networking)

![Architettura del Flusso](assets/architecture_screenshot.png) *(Nota: aggiungi qui il tuo screenshot!)*

## 🧠 Il Pattern Agentico: Copywriting Automation
Il flusso `Multi_Agentic_AI_Orchestration.json` simula un'agenzia di marketing a ciclo chiuso:
1. **Agente 1 (Drafting):** Analizza il prompt dell'utente e genera una bozza iniziale.
2. **Agente 2 (Critique):** Ispeziona la bozza come un Direttore Creativo, identificando debolezze (es. tono errato, mancanza di Call to Action).
3. **Agente 3 (Revision):** Applica le correzioni dell'Agente 2 alla bozza originale, producendo la versione finale ottimizzata.

### 💡 Valore di Business (Perché adottare questa soluzione)
- **Privacy Totale:** I dati aziendali sensibili non vengono mai inviati a server esterni (come OpenAI o Anthropic).
- **Costi Zero (No API Fees):** L'inferenza avviene localmente sull'hardware aziendale.
- **Scalabilità:** Facilmente integrabile con database interni, CRM (HubSpot, Salesforce) e canali di comunicazione (Slack, Email) grazie all'approccio Low-Code di n8n.

## 🚀 Come testarlo localmente
1. Clona il repository: `git clone https://github.com/tuo-utente/Agentic-AI-Workflow.git`
2. Avvia l'infrastruttura: `docker compose up -d`
3. Scarica il modello AI: `docker exec -it ollama ollama pull llama3.1`
4. Accedi a n8n su `http://localhost:5678` e importa il workflow dalla cartella `low_code_agentic_ai/`.
