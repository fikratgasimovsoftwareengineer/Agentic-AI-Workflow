
from ..tools.get_weather_info import ImposeWeatherInfo
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


class WeatherAgent(LlmAgent):

    def __init__(self):
        

        
        super().__init__(
                name="weather_aware_planner",
                model=LiteLlm(model="ollama_chat/qwen3.5:9b"),
                description="A trip planner that checks the real-time weather before making suggestions.",
                instruction="You are a cautious trip planner. Before suggesting any outdoor activities, you MUST use the `get_live_weather_forecast` tool to check conditions. Incorporate the live weather details into your recommendation.",
                tools=[ImposeWeatherInfo.get_live_weather_forecast]
            )

    print(f"🌦️ Weather Agent is created and can now call a live weather API!")