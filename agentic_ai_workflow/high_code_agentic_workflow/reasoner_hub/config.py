# =============================================================
# config.py — Configurazione centrale ReasonerHub
# =============================================================
 
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen3.5:9b"

# --- Self-reflection ---
# Soglia minima di confidenza (0.0 → 1.0)
# Se un agente scende sotto questa soglia, attiva un secondo giro di riflessione
CONFIDENCE_THRESHOLD=0.75

MAX_REFLECTION_ROUNDS=2

# MLFLOW #
MLFLOW_TRACKING_URI="http://localhost:5000"
MLFLOW_EXPERIMENT_NAME="ReasonerHub"

# --- Agenti disponibili ---
# Usato dall'orchestrator per il routing
AGENT_REGISTRY = [
    "math",
    "fact_checker",
    "summarizer",
    "code_analyzer",
    "sentiment",
]
 