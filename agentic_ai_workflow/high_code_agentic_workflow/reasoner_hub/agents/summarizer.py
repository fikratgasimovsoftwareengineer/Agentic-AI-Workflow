# =============================================================
# agents/summarizer_agent.py — Agente per sintesi di testi
# =============================================================
# Tool disponibili:
#   - extract_keypoints(text, max_points) : estrae i punti
#     chiave da un testo come lista strutturata, che il modello
#     usa come base per costruire la sintesi finale
# =============================================================

from agents.base_agent import BaseAgent


class SummarizerAgent(BaseAgent):

    @property
    def name(self) -> str:
        return "summarizer"

    @property
    def system_prompt(self) -> str:
        return (
            "Sei un agente specializzato nella sintesi e comprensione di testi. "
            "Il tuo compito è estrarre l'essenza di qualsiasi testo: "
            "identifica il tema centrale, i punti chiave, le conclusioni principali "
            "e le informazioni più rilevanti. "
            "Produci sintesi chiare, concise e fedeli all'originale. "
            "Distingui sempre tra informazioni esplicite nel testo e tue inferenze. "
            "Se il testo è lungo, usa il tool 'extract_keypoints' prima di sintetizzare."
        )

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "extract_keypoints",
                    "description": (
                        "Estrae i punti chiave da un testo e li struttura "
                        "come lista numerata per facilitare la sintesi."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Il testo da cui estrarre i punti chiave.",
                            },
                            "max_points": {
                                "type": "integer",
                                "description": "Numero massimo di punti chiave da estrarre (default: 5).",
                            },
                        },
                        "required": ["text"],
                    },
                },
            }
        ]

    def _execute_tool(self, tool_name: str, tool_args: dict) -> str:
        if tool_name == "extract_keypoints":
            return self._extract_keypoints(
                tool_args.get("text", ""),
                tool_args.get("max_points", 5),
            )
        return f"Tool '{tool_name}' non riconosciuto."

    # ----------------------------------------------------------
    # Implementazione tool extract_keypoints
    # ----------------------------------------------------------

    def _extract_keypoints(self, text: str, max_points: int = 5) -> str:
        """
        Analisi statistica leggera del testo:
        conta parole, frasi, stima lunghezza —
        fornisce metadati strutturali che aiutano il modello
        a tarare la profondità della sintesi.
        """
        if not text.strip():
            return "Testo vuoto — nessun punto chiave estraibile."

        sentences  = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
        word_count = len(text.split())
        char_count = len(text)

        # Stima densità informativa: parole per frase
        avg_words_per_sentence = word_count / max(len(sentences), 1)

        # Scegli le frasi più lunghe come proxy di maggiore contenuto
        ranked = sorted(sentences, key=lambda s: len(s.split()), reverse=True)
        top_sentences = ranked[:max_points]

        keypoints_str = "\n".join(
            f"  {i+1}. {s}" for i, s in enumerate(top_sentences)
        )

        return (
            f"METADATI TESTO\n"
            f"  Parole totali     : {word_count}\n"
            f"  Caratteri         : {char_count}\n"
            f"  Frasi identificate: {len(sentences)}\n"
            f"  Media parole/frase: {avg_words_per_sentence:.1f}\n\n"
            f"FRASI PIÙ DENSE (candidate punti chiave):\n"
            f"{keypoints_str}\n\n"
            f"Istruzione: usa questi elementi per costruire "
            f"una sintesi coerente e fedele al testo originale."
        )