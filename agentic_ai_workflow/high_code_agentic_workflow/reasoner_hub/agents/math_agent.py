# =============================================================
# agents/math_agent.py — Agente per ragionamento matematico
# =============================================================
# Tool disponibili:
#   - calculate(expression) : valuta espressioni matematiche
#                             usando eval() su un sottoinsieme
#                             sicuro di operatori Python
# =============================================================

import math
from agents.base_agent import BaseAgent


class MathAgent(BaseAgent):

    @property
    def name(self) -> str:
        return "math"

    @property
    def system_prompt(self) -> str:
        return (
            "Sei un agente specializzato in matematica e ragionamento numerico. "
            "Puoi risolvere equazioni, calcoli aritmetici, problemi di algebra, "
            "geometria, statistica e logica matematica. "
            "Mostra sempre i passaggi del ragionamento prima della risposta finale. "
            "Se hai un tool 'calculate' disponibile, usalo per verificare i calcoli numerici."
        )

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": (
                        "Valuta un'espressione matematica Python e ritorna il risultato numerico. "
                        "Supporta: +, -, *, /, **, sqrt(), sin(), cos(), log(), pi, e."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Espressione matematica da calcolare. Es: '2 ** 10', 'sqrt(144)', '3.14 * 5**2'",
                            }
                        },
                        "required": ["expression"],
                    },
                },
            }
        ]

    def _execute_tool(self, tool_name: str, tool_args: dict) -> str:
        if tool_name == "calculate":
            return self._calculate(tool_args.get("expression", ""))
        return f"Tool '{tool_name}' non riconosciuto."

    # ----------------------------------------------------------
    # Implementazione tool calculate
    # ----------------------------------------------------------

    def _calculate(self, expression: str) -> str:
        """
        Valuta l'espressione matematica in un namespace sicuro.
        Espone solo funzioni math — nessun accesso a builtins pericolosi.
        """
        safe_namespace = {
            "__builtins__": {},           # blocca tutti i builtins
            "sqrt":  math.sqrt,
            "sin":   math.sin,
            "cos":   math.cos,
            "tan":   math.tan,
            "log":   math.log,
            "log10": math.log10,
            "exp":   math.exp,
            "abs":   abs,
            "round": round,
            "pi":    math.pi,
            "e":     math.e,
        }
        try:
            result = eval(expression, safe_namespace)           # noqa: S307
            return f"Risultato di '{expression}' = {result}"
        except ZeroDivisionError:
            return f"Errore: divisione per zero nell'espressione '{expression}'"
        except Exception as ex:
            return f"Errore nel calcolo di '{expression}': {ex}"