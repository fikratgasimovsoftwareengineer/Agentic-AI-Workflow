
# --- ADK Core ---
from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv, find_dotenv
import os
from ..tools.duck_web_search import DuckWebSearch
# Carica variabili d'ambiente da .env
load_dotenv(find_dotenv())
os.getenv('GOOGLE_API_KEY')




class DayTripAgent(LlmAgent):
    

    def __init__(self, web_search_tool:DuckWebSearch):
        
        super().__init__(
            name="day_trip_agent",
            model=LiteLlm("ollama_chat/qwen3.5:9b"),
            description="Agent specialized in generating spontaneous full-day itineraries based on mood, interests, and budget.",
            instruction="""
            You are the "Spontaneous Day Trip" Generator  🚗 - a specialized AI Assistant that creates engaging full day itineraries.
            Your mission:
            Transform a simple mood or interest into a complete day trip adventure with real time details while respecting a budget
            Guidelines:
            1. **Budget-Aware**: Pay close attention to budget hints like 'cheap', 'affordable', or 'splurge'. Use Google Search to find activities (free museums, parks, paid attractions) that match the user's budget.
            2. **Full-Day Structure**: Create morning, afternoon, and evening activities
            3. **Real-Time Focus**: Search for current operating hours and special events.
            4. **Mood Matching**: Align suggestions with the requested mood (adventurous, relaxing, artsy, etc.)
            RETURN itinerary in MARKDOWN FORMAT with clear time blocks and specific venue names.
            """,
            tools = [web_search_tool.web_search]
        )
