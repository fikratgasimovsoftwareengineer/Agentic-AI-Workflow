from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# ── TOOLS ──────────────────────────────────────────────

def get_current_datetime() -> dict:
    """Restituisce data e ora corrente."""
    from datetime import datetime
    now = datetime.now()
    return {
        "status": "success",
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M"),
        "weekday": now.strftime("%A")
    }

def calculate(expression: str) -> dict:
    """Esegue calcoli matematici. Esempio: '2 + 2', '15 * 4', '100 / 5'."""
    try:
        allowed = set("0123456789+-*/()., ")
        if not all(c in allowed for c in expression):
            return {"status": "error", "message": "Espressione non valida"}
        result = eval(expression)
        return {"status": "success", "expression": expression, "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_wikipedia(topic: str) -> dict:
    """Cerca informazioni su un argomento su Wikipedia."""
    import urllib.request
    import json
    try:
        topic_encoded = urllib.parse.quote(topic)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic_encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": "ADK-Chatbot/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            return {
                "status": "success",
                "title": data.get("title", ""),
                "summary": data.get("extract", "")[:500],
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
            }
    except Exception as e:
        return {"status": "error", "message": f"Ricerca fallita: {str(e)}"}

def get_weather_info(city: str) -> dict:
    """Fornisce informazioni meteo generali per una città (simulato)."""
    # In produzione: integra OpenWeatherMap API
    return {
        "status": "success",
        "city": city,
        "note": f"Per meteo in tempo reale su {city}, visita: https://wttr.in/{city}",
        "suggestion": "Integra una API meteo reale per dati live"
    }

# ── AGENTE ROOT ────────────────────────────────────────

import urllib.parse

root_agent = Agent(
    #model=LiteLlm(model="ollama_chat/llama3.2:latest"),
    model=LiteLlm(model="ollama_chat/gemma4:latest"),
    
    name="generic_chatbot",
    description="Chatbot generico con capacità agentiche.",
    instruction="""
    Sei un assistente AI avanzato, intelligente e disponibile.
    Rispondi in modo chiaro e preciso in qualsiasi lingua l'utente utilizzi.

    Hai accesso a questi tool — usali SEMPRE quando appropriato:

    - get_current_datetime: quando chiedono data, ora, giorno
    - calculate: quando chiedono calcoli matematici
    - search_wikipedia: quando chiedono informazioni su persone, luoghi, eventi, concetti
    - get_weather_info: quando chiedono del meteo

    Regole importanti:
    1. Se la domanda richiede un tool, usalo — non inventare dati
    2. Dopo aver usato un tool, spiega il risultato in modo naturale
    3. Per domande generali di conoscenza, rispondi direttamente
    4. Sii conciso ma completo
    """,
    tools=[
        get_current_datetime,
        calculate,
        search_wikipedia,
        get_weather_info,
    ],
)