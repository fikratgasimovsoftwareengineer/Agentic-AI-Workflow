# =============================================================
# agents/fact_checker_agent.py — Agente per verifica dei fatti
# =============================================================
# Tool disponibili:
#   - check_claim(claim, domain) : struttura una verifica
#     epistemica della affermazione, valutando certezza,
#     fonti attendibili e possibili controesempi
# =============================================================

from agents.base_agent import BaseAgent


class FactCheckerAgent(BaseAgent):

    @property
    def name(self) -> str:
        return "fact_checker"

    @property
    def system_prompt(self) -> str:
        return (
            "Sei un agente specializzato nella verifica epistemica delle affermazioni. "
            "Il tuo compito è analizzare ogni affermazione con rigore critico: "
            "distingui fatti verificabili da opinioni, identifica affermazioni dubbie, "
            "segnala possibili bias o errori logici, e valuta il grado di certezza. "
            "Struttura sempre la risposta in: "
            "1) Analisi dell'affermazione "
            "2) Evidenze a supporto "
            "3) Evidenze contrarie o dubbi "
            "4) Verdetto finale con grado di certezza."
        )

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "check_claim",
                    "description": (
                        "Struttura una verifica epistemica formale di un'affermazione. "
                        "Ritorna un framework di analisi con dominio, tipo di claim e criteri di verifica."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "claim": {
                                "type": "string",
                                "description": "L'affermazione da verificare.",
                            },
                            "domain": {
                                "type": "string",
                                "description": "Dominio dell'affermazione: 'science', 'history', 'math', 'current_events', 'general'",
                                "enum": ["science", "history", "math", "current_events", "general"],
                            },
                        },
                        "required": ["claim", "domain"],
                    },
                },
            }
        ]

    def _execute_tool(self, tool_name: str, tool_args: dict) -> str:
        if tool_name == "check_claim":
            return self._check_claim(
                tool_args.get("claim", ""),
                tool_args.get("domain", "general"),
            )
        return f"Tool '{tool_name}' non riconosciuto."

    # ----------------------------------------------------------
    # Implementazione tool check_claim
    # ----------------------------------------------------------

    def _check_claim(self, claim: str, domain: str) -> str:
        """
        Costruisce un framework di verifica strutturato.
        Non fa ricerca esterna — fornisce criteri epistemici
        che il modello userà nella sua analisi.
        """
        domain_criteria = {
            "science": (
                "Verifica: peer review, riproducibilità, consenso scientifico, "
                "metodologia degli studi citati, possibili bias di pubblicazione."
            ),
            "history": (
                "Verifica: fonti primarie vs secondarie, contesto storico, "
                "storiografia moderna, documenti d'archivio, revisione accademica."
            ),
            "math": (
                "Verifica: dimostrazione formale, controesempi, assiomi utilizzati, "
                "validità logica della prova."
            ),
            "current_events": (
                "Verifica: fonti multiple indipendenti, data dell'evento, "
                "possibile disinformazione, contesto politico/economico."
            ),
            "general": (
                "Verifica: logica interna, coerenza con fatti noti, "
                "presenza di generalizzazioni indebite, fonti citabili."
            ),
        }

        criteria = domain_criteria.get(domain, domain_criteria["general"])

        return (
            f"FRAMEWORK DI VERIFICA\n"
            f"Affermazione: '{claim}'\n"
            f"Dominio: {domain}\n"
            f"Criteri da applicare: {criteria}\n"
            f"Istruzione: usa questo framework per strutturare "
            f"la tua analisi epistemica completa."
        )