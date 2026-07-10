# =============================================================
# orchestrator/root_orchestrator.py — Orchestratore principale
# =============================================================
# Responsabilità:
#   1. Riceve la query dell'utente
#   2. Classifica il tipo di query (quale agente è più adatto)
#   3. Delega all'agente specializzato corretto
#   4. Ritorna il risultato strutturato
#
# La classificazione avviene in due modi:
#   A. Keyword-based (veloce, nessuna chiamata LLM)
#   B. LLM-based    (più accurata, usata se A non è sicura)
# =============================================================

import re
import ollama

from config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    AGENT_REGISTRY,
)


from agents.fact_checker import FactCheckerAgent
from agents.math_agent import MathAgent
from agents.summarizer import SummarizerAgent
from agents.code_analyzer import CodeAnalyzerAgent
from agents.sentiment_agent import SentimentAgent


# ----------------------------------------------------------
# Keyword map: pattern → agent name
# Usato per routing veloce senza chiamata LLM
# ----------------------------------------------------------
_KEYWORD_MAP = {
    "math": [
        r"\b(calcola|calcolare|quanto\s+fa|risolvi|equazione|integrale|derivata"
        r"|somma|prodotto|divisione|radice|logaritmo|percentuale"
        r"|calculate|solve|equation|integral|derivative|sqrt|math)\b",
    ],
    "fact_checker": [
        r"\b(vero|falso|verifica|è\s+vero\s+che|conferma|smentisci|fact.?check"
        r"|affermazione|claim|true|false|verify|confirm|debunk|is\s+it\s+true)\b",
    ],
    "summarizer": [
        r"\b(riassumi|riassunto|sintesi|sintetizza|punti\s+chiave|riepiloga"
        r"|summarize|summary|key\s+points|tldr|tl;dr|main\s+points)\b",
    ],
    "code_analyzer": [
        r"\b(codice|code|bug|funzione|function|classe|class|python|javascript"
        r"|typescript|review|analizza\s+il\s+codice|refactor|debug|script)\b",
    ],
    "sentiment": [
        r"\b(sentiment|emozione|emozioni|tono|umore|positivo|negativo|analizza\s+il\s+testo"
        r"|feeling|emotion|mood|tone|opinion|opinione|review\s+prodotto)\b",
    ],
}


class RootOrchestrator:
    """
    Orchestratore principale di ReasonerHub.

    Istanzia tutti gli agenti una volta sola all'avvio
    e li riutilizza per ogni query (stateless per design).
    """

    def __init__(self):
        # Istanza unica di ogni agente
        self._agents = {
            "math":          MathAgent(),
            "fact_checker":  FactCheckerAgent(),
            "summarizer":    SummarizerAgent(),
            "code_analyzer": CodeAnalyzerAgent(),
            "sentiment":     SentimentAgent(),
        }
        self._llm_client = ollama.Client(host=OLLAMA_BASE_URL)

    # ----------------------------------------------------------
    # Entry point pubblico
    # ----------------------------------------------------------

    def run(self, query: str) -> dict:
        """
        Processa una query end-to-end:
            1. Classifica → trova l'agente giusto
            2. Delega     → l'agente elabora con self-reflection + MLflow
            3. Ritorna    → risultato arricchito con metadati di routing

        Ritorna:
            {
                "query":          str,
                "routed_to":      str,
                "routing_method": "keyword" | "llm",
                "answer":         str,
                "confidence":     float,
                "reflection_rounds": int,
                "self_corrected": bool,
                "tool_called":    str | None,
            }
        """
        agent_name, routing_method = self._classify(query)
        agent  = self._agents[agent_name]
        result = agent.run(query)

        return {
            "query":             query,
            "routed_to":         agent_name,
            "routing_method":    routing_method,
            **result,
        }

    # ----------------------------------------------------------
    # Classificazione query
    # ----------------------------------------------------------

    def _classify(self, query: str) -> tuple[str, str]:
        """
        Prova prima il routing keyword-based (veloce).
        Se non trova un match con abbastanza confidenza,
        usa il LLM per classificare (più lento ma accurato).

        Ritorna: (agent_name, routing_method)
        """
        # Tentativo A: keyword routing
        agent_name = self._keyword_routing(query)
        if agent_name:
            return agent_name, "keyword"

        # Tentativo B: LLM routing
        agent_name = self._llm_routing(query)
        return agent_name, "llm"

    def _keyword_routing(self, query: str) -> str | None:
        """
        Cerca pattern regex nella query.
        Ritorna il nome dell'agente con più match, o None se ambiguo.
        """
        query_lower = query.lower()
        scores      = {name: 0 for name in _KEYWORD_MAP}

        for agent_name, patterns in _KEYWORD_MAP.items():
            for pattern in patterns:
                matches = re.findall(pattern, query_lower, re.IGNORECASE)
                scores[agent_name] += len(matches)

        best_agent = max(scores, key=lambda k: scores[k])
        best_score = scores[best_agent]

        # Ritorna solo se c'è almeno 1 match chiaro
        if best_score >= 1:
            return best_agent

        return None  # nessun match → fallback a LLM

    def _llm_routing(self, query: str) -> str:
        """
        Usa il modello LLM per classificare la query
        quando il routing keyword non è sufficiente.
        Chiede una risposta strutturata con solo il nome dell'agente.
        """
        agents_list = "\n".join(f"- {name}" for name in AGENT_REGISTRY)

        classification_prompt = f"""Sei un classificatore di query. 
Devi scegliere ESATTAMENTE UNO dei seguenti agenti specializzati in base alla query dell'utente:

{agents_list}

Descrizione degli agenti:
- math          : calcoli, equazioni, problemi numerici, matematica
- fact_checker  : verifica affermazioni, fatti, claim da confermare o smentire
- summarizer    : riassunti, sintesi, estrazione punti chiave da testi
- code_analyzer : analisi codice, bug, review, spiegazione di codice sorgente
- sentiment     : analisi emozioni, tono, sentiment di testi o frasi

Query da classificare: "{query}"

Rispondi con UNA SOLA PAROLA: il nome esatto dell'agente scelto.
Non aggiungere spiegazioni. Solo il nome."""

        response = self._llm_client.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": classification_prompt}],
        )

        raw_answer = response.message.content.strip().lower()

        # Cerca il nome dell'agente nella risposta
        for agent_name in AGENT_REGISTRY:
            if agent_name in raw_answer:
                return agent_name

        # Fallback sicuro: summarizer gestisce query generiche
        return "summarizer"