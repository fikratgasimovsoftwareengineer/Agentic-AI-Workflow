```sh
it_ticket_agent/
│
├── config.py                        ← configurazione centralizzata (D)
│
├── main.py                          ← entry point, avvia il sistema
│
├── data/
│   ├── __init__.py
│   └── db.py                        ← unico punto di accesso al database (S)
│
├── core/
│   ├── __init__.py
│   ├── interfaces.py                ← astrazioni / contratti (D + L)
│   └── models.py                    ← dataclass Ticket, TicketEvent (S)    
│
├── tools/
│   ├── __init__.py
│   ├── diagnostic_tools.py          ← classify, urgency, similar (S + I)
│   ├── resolution_tools.py          ← propose, resolve, escalate (S + I)
│   ├── notification_tools.py        ← email apertura/risoluzione/SLA (S + I)
│   └── jira_tools.py                ← MCP Jira create/update/close (S + I)
│
├── agents/
│   ├── __init__.py
│   ├── diagnostic_agent.py          ← analisi ticket (S + I)
│   ├── resolution_agent.py          ← risoluzione ticket (S + I)
│   ├── notification_agent.py        ← notifiche email (S + I)
│   ├── jira_agent.py                ← sincronizzazione Jira (S + I)
│   └── root_agent.py                ← orchestratore principale (S)
│
├── monitoring/
│   ├── __init__.py
│   └── mlflow_tracker.py            ← MLflow layer trasversale (O)
│
├── mcp_servers/
│   ├── __init__.py
│   └── jira_mock.py                 ← mock MCP server locale per test
│
└── requirements.txt
```

### Ordine 
```sh
core/models.py        ✓  fatto
core/interfaces.py    ✓  fatto
data/db.py            ← adesso
config.py             ← poi
tools/                ← poi
agents/               ← poi
knowledge_base/       ← qui va il RAG
    indexer.py        ← indicizza i documenti
    retriever.py      ← cerca nei documenti
monitoring/           ← MLflow per ultimo
```