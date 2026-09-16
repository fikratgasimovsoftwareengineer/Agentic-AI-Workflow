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