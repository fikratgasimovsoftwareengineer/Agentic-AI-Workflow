# =============================================================
# agents/sentiment_agent.py — Agente per analisi del sentiment
# =============================================================
# Tool disponibili:
#   - detect_sentiment_signals(text) : rileva segnali lessicali
#     di sentiment (parole positive/negative/neutre) nel testo
#     come base per l'analisi più profonda del modello
# =============================================================

import re
from agents.base_agent import BaseAgent


# Dizionari lessicali leggeri per rilevamento segnali
_POSITIVE_WORDS = {
    "ottimo", "eccellente", "bravo", "felice", "bello", "fantastico",
    "perfetto", "buono", "meraviglioso", "positivo", "grande", "amore",
    "gioia", "successo", "vincere", "bene", "contento", "soddisfatto",
    "good", "great", "excellent", "happy", "love", "wonderful", "amazing",
    "perfect", "best", "awesome", "fantastic", "brilliant", "superb",
}

_NEGATIVE_WORDS = {
    "male", "pessimo", "terribile", "triste", "brutto", "orribile",
    "fallimento", "perdere", "peggio", "odio", "paura", "ansia",
    "problema", "errore", "sbagliato", "negativo", "deluso", "arrabbiato",
    "bad", "terrible", "awful", "hate", "sad", "horrible", "worst",
    "failure", "wrong", "ugly", "angry", "disappointed", "disgusting",
}

_INTENSIFIERS = {
    "molto", "troppo", "assolutamente", "completamente", "totalmente",
    "estremamente", "incredibilmente", "davvero", "proprio",
    "very", "extremely", "absolutely", "completely", "totally", "really",
}


class SentimentAgent(BaseAgent):

    @property
    def name(self) -> str:
        return "sentiment"

    @property
    def system_prompt(self) -> str:
        return (
            "Sei un agente specializzato nell'analisi del sentiment, delle emozioni "
            "e dell'intento comunicativo nei testi. "
            "Per ogni testo analizzato fornisci: "
            "1) Sentiment generale (positivo/negativo/neutro/misto) con intensità "
            "2) Emozioni principali rilevate (gioia, rabbia, tristezza, paura, sorpresa, disgusto) "
            "3) Intento comunicativo (informare, persuadere, lamentarsi, elogiare, chiedere aiuto, ecc.) "
            "4) Tono (formale, informale, sarcastico, ironico, neutro) "
            "5) Parole o frasi chiave che guidano l'analisi. "
            "Usa sempre il tool 'detect_sentiment_signals' prima di analizzare."
        )

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "detect_sentiment_signals",
                    "description": (
                        "Analizza il testo a livello lessicale e rileva segnali "
                        "di sentiment: conta parole positive, negative, intensificatori, "
                        "punteggiatura emotiva e stima un sentiment score grezzo."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Il testo da analizzare per il sentiment.",
                            },
                        },
                        "required": ["text"],
                    },
                },
            }
        ]

    def _execute_tool(self, tool_name: str, tool_args: dict) -> str:
        if tool_name == "detect_sentiment_signals":
            return self._detect_sentiment_signals(tool_args.get("text", ""))
        return f"Tool '{tool_name}' non riconosciuto."

    # ----------------------------------------------------------
    # Implementazione tool detect_sentiment_signals
    # ----------------------------------------------------------

    def _detect_sentiment_signals(self, text: str) -> str:
        """
        Analisi lessicale leggera basata su dizionari.
        Conta segnali positivi/negativi e produce un sentiment score grezzo
        che il modello usa come base per l'analisi semantica profonda.
        """
        if not text.strip():
            return "Testo vuoto — nessun segnale rilevabile."

        words_raw = re.findall(r"\b\w+\b", text.lower())
        words     = set(words_raw)

        positive_hits    = words & _POSITIVE_WORDS
        negative_hits    = words & _NEGATIVE_WORDS
        intensifier_hits = words & _INTENSIFIERS

        pos_count = len(positive_hits)
        neg_count = len(negative_hits)
        int_count = len(intensifier_hits)

        # Punteggio grezzo: positivi - negativi, amplificato dagli intensificatori
        raw_score = (pos_count - neg_count) * (1 + 0.3 * int_count)

        # Segnali punteggiatura
        exclamations    = text.count("!")
        question_marks  = text.count("?")
        caps_words      = len(re.findall(r"\b[A-Z]{2,}\b", text))  # parole in MAIUSCOLO

        # Sentiment label grezza
        if raw_score > 1:
            raw_label = "POSITIVO"
        elif raw_score < -1:
            raw_label = "NEGATIVO"
        elif pos_count > 0 and neg_count > 0:
            raw_label = "MISTO"
        else:
            raw_label = "NEUTRO"

        return (
            f"SEGNALI LESSICALI RILEVATI\n"
            f"  Parole totali         : {len(words_raw)}\n"
            f"  Segnali positivi ({pos_count})  : {', '.join(positive_hits) or 'nessuno'}\n"
            f"  Segnali negativi ({neg_count})  : {', '.join(negative_hits) or 'nessuno'}\n"
            f"  Intensificatori ({int_count})   : {', '.join(intensifier_hits) or 'nessuno'}\n"
            f"  Punti esclamativi     : {exclamations}\n"
            f"  Punti interrogativi   : {question_marks}\n"
            f"  Parole in MAIUSCOLO   : {caps_words}\n"
            f"  Score grezzo          : {raw_score:+.2f}\n"
            f"  Sentiment lessicale   : {raw_label}\n\n"
            f"Istruzione: usa questi segnali come base per la tua analisi "
            f"semantica profonda di sentiment, emozioni e intento."
        )