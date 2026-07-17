```sh
reasonerhub/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── math_agent.py
│   ├── fact_checker_agent.py
│   ├── summarizer_agent.py
│   ├── code_analyzer_agent.py
│   └── sentiment_agent.py        # ← 5° agente
├── tools/
│   ├── __init__.py
│   ├── math_tools.py
│   ├── text_tools.py
│   └── code_tools.py
├── orchestrator/
│   ├── __init__.py
│   └── root_orchestrator.py
├── tracking/
│   ├── __init__.py
│   └── mlflow_tracker.py
├── config.py
├── main.py
└── requirements.txt
```
```sh
mlflow server --host 127.0.0.1 --port 5000
```