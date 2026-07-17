# =============================================================
# config.py — Configurazione centrale ReasonerHub
# =============================================================
 
OLLAMA_API_BASE = "http://localhost:11434"
CODICE_OLLAMA_MODEL = "qwen3.5:9b"
## REPORT GENERATOR
REPORT_OLLAMA_MODEL = "llama3.2:latest",

# --- Self-reflection ---
# Soglia minima di confidenza (0.0 → 1.0)
# Se un agente scende sotto questa soglia, attiva un secondo giro di riflessione
CONFIDENCE_THRESHOLD=0.75

MAX_REFLECTION_ROUNDS=2

# MLFLOW #
MLFLOW_TRACKING_URI="http://localhost:5000"
MLFLOW_EXPERIMENT_NAME="ReasonerHub"

