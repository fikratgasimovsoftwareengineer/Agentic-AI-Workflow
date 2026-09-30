```sh
IntentAnalyzer  → Routing (+ Planning in v2)
Research        → ReAct + Tool Use (+ Parallelization via Send)
DataAnalysis    → Tool Use (+ Parallelization per i grafici)
Writer          → Prompt chaining con contesto accumulato
Critic↔Editor   → Reflection / Evaluator-Optimizer (con guardrail)
FinalAnswer     → Human-in-the-Loop (interrupt) + output strutturato
Supervisor      → Orchestrator-Workers + Routing vincolato
Trasversale     → Guardrails, Strategy, Factory, Template Method, DI, Observer
```


```sh
market-research-agent/
├── .env                          # variabili d'ambiente (chiavi, URL)
├── requirements.txt              # dipendenze pinnate
├── main.py                       # entry point
├── src/
│   ├── config/
│   │   └── settings.py           # configurazione centralizzata
│   ├── domain/
│   │   └── models.py             # contratti dati tra agenti (Pydantic)
│   ├── agents/
│   │   ├── llm_provider.py       # astrazione LLM (Strategy)
│   │   ├── base.py               # classe base nodi (Template Method)
│   │   ├── intent_analyzer.py
│   │   ├── researcher.py
│   │   ├── data_analyst.py
│   │   ├── writer.py
│   │   ├── critic.py
│   │   ├── editor.py
│   │   └── final_answer.py
│   ├── infrastructure/
│   │   ├── ollama_provider.py    # adapter Ollama
│   │   ├── tools.py              # tool per il ReAct
│   │   └── chart_generator.py    # grafici deterministici
│   └── graph/
│       ├── state.py              # stato condiviso
│       ├── supervisor.py         # routing
│       └── builder.py            # assemblaggio del grafo
└── tests/
```


```sh
query
						  │
						  ▼
						┌──────────────────┐  PATTERN 1: ROUTER
						│  INTENT ROUTER   │  "di cosa parla questa richiesta?"
						│  (ResearchPlan)  │  -> categories + search_queries
						└────────┬─────────┘
						         │
						         ▼           PATTERN 2: ORCHESTRATOR-WORKERS
						┌──────────────────┐  il ResearchPlan E' il piano dell'orchestratore:
						│  Send fan-out    │  una ricerca per query (i sotto-task non erano
						└────────┬─────────┘  predefiniti: li ha generati il Router a runtime)
						         │
						    ┌────┼────┐
						    ▼    ▼    ▼      WORKERS: i rami di ricerca Tavily (paralleli)
						  [search][search][search]
						    │    │    │
						    └────┼────┘
						         ▼
						┌──────────────────┐  SYNTHESIZER: fonde i risultati in UN output
						│  FINAL ANSWER    │  (results accumulati via operator.add)
						└──────────────────┘
```