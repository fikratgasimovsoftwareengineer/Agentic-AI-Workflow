from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent #An agent that can represent a human user through an input function.)
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

from autogen_agentchat.ui import Console
from autogen_agentchat.messages import ToolCallSummaryMessage
import asyncio

import aiohttp

from azure.core.credentials import AzureKeyCredential


import os



# --------------------------------------------------------------------------
# 1. SETUP DELLE VARIABILI D'AMBIENTE
# --------------------------------------------------------------------------
# Assicurati che queste variabili siano impostate nel tuo terminale
# Esempio:
# Set the environment variable
os.environ["AZURE_OPENAI_ENDPOINT"] ="https://custom-gpt-dev.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] ="91d6e2b0a02f47589001d909039cda77"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "gpt-4o"
os.environ["AZURE_OPENAI_API_VERSION"]= "2024-12-01-preview"
# --------------------------------------------------------------------------
def get_env_variable(name: str) -> str:
    """Funzione di utilità per leggere le variabili d'ambiente."""
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"La variabile d'ambiente '{name}' non è impostata.")
    return value

try:

    client = AzureOpenAIChatCompletionClient(
        azure_endpoint=get_env_variable("AZURE_OPENAI_ENDPOINT"),
        model="gpt-4o",
        api_key=get_env_variable("AZURE_OPENAI_API_KEY"),
        azure_deployment=get_env_variable("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version="2024-05-01-preview",
    )
except ValueError as e:
    print(f"Errore: {e}")
    exit()



async def get_weather(city:str)->str:
    print(f"--- ⚙️ ESECUZIONE STRUMENTO: get_weather(city='{city}') ---")
    test_weather_data = {
        "city":"Roma",
        "temperature":"28C"
    }
    
    return  f"{test_weather_data.get('city','')}: {test_weather_data.get('temperature','')}"


async def get_jokes(joke_type:str, joke:str):
    print(f"Joke type {joke_type} and joke {joke}")
    
    messages = {
        "joke_t":joke_type,
        "joke":"lets create small car for toy purpose."
    }
    return f"{messages.get('joke_t', '')} : {messages.get('joke', '')}"

user_proxy = UserProxyAgent(
    
    name="user_proxy"
)
gpt4o_agent = AssistantAgent(
    name = "assistant_agent",
    model_client=client,
    tools=[get_weather, get_jokes],
    description = 'An Agent that can provide weather information and joke information',
    model_client_stream=True,
    reflect_on_tool_use=False
)


# Run the agent and stream the messages to the console.
async def main() -> None:
    
    try:
        # Use asyncio.run(agent.run(...)) when running in a script.
        #result = await gpt4o_agent.run(task="what is the weather in Rome")
        result = await gpt4o_agent.run(task="can you tell me joke?")
        
        result_summary = [summary.content for summary in reversed(result.messages) if isinstance(summary, ToolCallSummaryMessage)]
        print(result_summary)
        
        
        """   await user_proxy.chat(
            recipient = gpt4o_agent,
            max_turns = 6,
            message = "What is the weather in Rome?"
        )  """
                
        """ response = await asyncio.create_task(
            user_proxy.on_messages(
                [TextMessage(content="What is your name? ", source="user")],
                cancellation_token=CancellationToken(),
            )
        ) """
    finally:    
        
        await client.close()
        
        
        """ #await Console(gpt4o_agent.run_stream(task="What is the weather in New York?"))
        stream = gpt4o_agent.run_stream(task="What is the weather in Rome?")
        
        async for message in stream:
            
            #print(message)
            if hasattr(message, 'type'):
                if message.type=="ToolCallRequestEvent" and message.source == "weather_agent":
                    
                    #message.content[0].name
                    print("Received final response from the agent. Exiting...")
                    print(message.content)
                    print(message.content[0].name)
                    print(message.content[0].arguments)
                    print("=======================================================")
            else:
             pass """


if __name__== "__main__":
# NOTE: if running this inside a Python script you'll need to use asyncio.run(main()).
    asyncio.run(main())