# =============================================================
# agents/code_analyzer_agent.py — Agente per analisi del codice
# =============================================================
# Tool disponibili:
#   - analyze_code_structure(code, language) : analizza
#     metriche strutturali del codice (linee, funzioni,
#     complessità stimata) come base per la review
# =============================================================

import re
from agents.base_agent import BaseAgent


class CodeAnalyzerAgent(BaseAgent):

    @property
    def name(self) -> str:
        return "code_analyzer"

    @property
    def system_prompt(self) -> str:
        return (
            "Sei un agente specializzato in analisi, review e spiegazione del codice. "
            "Puoi lavorare con Python, JavaScript, TypeScript, Java, C++, Bash e altri linguaggi. "
            "Per ogni pezzo di codice che analizzi: "
            "1) Spiega cosa fa il codice ad alto livello "
            "2) Identifica eventuali bug, vulnerabilità o code smell "
            "3) Suggerisci miglioramenti concreti "
            "4) Valuta la qualità complessiva (leggibilità, manutenibilità, performance). "
            "Usa il tool 'analyze_code_structure' per ottenere metriche strutturali prima di rispondere."
        )

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "analyze_code_structure",
                    "description": (
                        "Analizza la struttura statica di un frammento di codice: "
                        "conta linee, funzioni/metodi, classi, commenti e stima "
                        "la complessità ciclomatica approssimativa."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Il codice sorgente da analizzare.",
                            },
                            "language": {
                                "type": "string",
                                "description": "Linguaggio di programmazione del codice.",
                                "enum": ["python", "javascript", "typescript", "java", "cpp", "bash", "other"],
                            },
                        },
                        "required": ["code", "language"],
                    },
                },
            }
        ]

    def _execute_tool(self, tool_name: str, tool_args: dict) -> str:
        if tool_name == "analyze_code_structure":
            return self._analyze_code_structure(
                tool_args.get("code", ""),
                tool_args.get("language", "other"),
            )
        return f"Tool '{tool_name}' non riconosciuto."

    # ----------------------------------------------------------
    # Implementazione tool analyze_code_structure
    # ----------------------------------------------------------

    def _analyze_code_structure(self, code: str, language: str) -> str:
        """
        Analisi statica leggera basata su regex.
        Non esegue il codice — solo analisi strutturale testuale.
        """
        if not code.strip():
            return "Codice vuoto — nessuna analisi possibile."

        lines       = code.splitlines()
        total_lines = len(lines)
        blank_lines = sum(1 for l in lines if not l.strip())
        code_lines  = total_lines - blank_lines

        # Pattern per linguaggio
        patterns = {
            "python": {
                "function": r"^\s*def\s+\w+",
                "class":    r"^\s*class\s+\w+",
                "comment":  r"^\s*#",
                "branch":   r"\b(if|elif|for|while|except|with)\b",
            },
            "javascript": {
                "function": r"(function\s+\w+|=>\s*\{|^\s*\w+\s*\(.*\)\s*\{)",
                "class":    r"^\s*class\s+\w+",
                "comment":  r"^\s*(//|/\*)",
                "branch":   r"\b(if|else|for|while|catch|switch)\b",
            },
            "typescript": {
                "function": r"(function\s+\w+|=>\s*\{|^\s*\w+\s*\(.*\)\s*\{)",
                "class":    r"^\s*class\s+\w+",
                "comment":  r"^\s*(//|/\*)",
                "branch":   r"\b(if|else|for|while|catch|switch)\b",
            },
        }

        # Usa python come fallback per linguaggi non specificati
        p = patterns.get(language, patterns["python"])

        func_count    = sum(1 for l in lines if re.search(p["function"], l))
        class_count   = sum(1 for l in lines if re.search(p["class"], l))
        comment_count = sum(1 for l in lines if re.search(p["comment"], l))
        branch_count  = sum(1 for l in lines if re.search(p["branch"], l))

        # Complessità ciclomatica approssimativa: 1 + branch_count
        cyclomatic = 1 + branch_count

        complexity_label = (
            "Bassa (buona)"    if cyclomatic <= 5  else
            "Media"            if cyclomatic <= 10 else
            "Alta (attenzione)" if cyclomatic <= 20 else
            "Molto alta (refactoring consigliato)"
        )

        return (
            f"ANALISI STRUTTURALE — {language.upper()}\n"
            f"  Linee totali          : {total_lines}\n"
            f"  Linee di codice       : {code_lines}\n"
            f"  Linee vuote           : {blank_lines}\n"
            f"  Funzioni/metodi       : {func_count}\n"
            f"  Classi                : {class_count}\n"
            f"  Righe di commento     : {comment_count}\n"
            f"  Branch (if/for/while) : {branch_count}\n"
            f"  Complessità stimata   : {cyclomatic} → {complexity_label}\n\n"
            f"Istruzione: usa queste metriche come contesto per la tua review dettagliata."
        )