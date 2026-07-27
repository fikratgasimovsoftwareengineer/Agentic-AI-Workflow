# google_adk_labs/agent.py

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from .agents.day_trip_agent import DayTripAgent
from .agents.weather_agent import WeatherAgent
from .tools.duck_web_search import DuckWebSearch



web_search_tool = DuckWebSearch()

day_trip_agent = DayTripAgent(web_search_tool)
weather_agent = WeatherAgent()

root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/qwen3.5:9b"),
    name="RouterAgent",
    description="Router che smista tra pianificazione gite e meteo.",
    instruction=(
        "You are a router. Delegate based on user intent:\n"
        "- If the user asks about weather, forecast, rain, temperature, or hiking conditions "
        "→ delegate to weather_aware_planner\n"
        "- If the user asks to plan a day trip, itinerary, or activities "
        "→ delegate to day_trip_agent\n"
        "Always delegate — do not answer directly."
    ),
    sub_agents=[day_trip_agent, weather_agent],
)