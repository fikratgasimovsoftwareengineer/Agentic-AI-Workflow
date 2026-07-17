from google.adk.agents.llm_agent import Agent
import ollama
from config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    CONFIDENCE_THRESHOLD,
    MAX_REFLECTION_ROUNDS,
)

root_agent = Agent(
    model='<FILL_IN_MODEL>',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[..,...]
)

