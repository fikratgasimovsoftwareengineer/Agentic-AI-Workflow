import os
import asyncio
from openai import AsyncAzureOpenAI
from openai import OpenAIError
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, WebSearchTool, function_tool
import pathlib
from dotenv import load_dotenv
import sys
import datetime

env_path = pathlib.Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(env_path ))
load_dotenv(dotenv_path=env_path / 'genai/openai' / '.env')


# --- 1. CONFIGURAZIONE DEGLI AGENTI E DELL'LLM ---

# Leggi le credenziali di Azure OpenAI dalle variabili d'ambiente
# Assicurati di averle impostate nel tuo sistema!

api_version:str = os.getenv("OPENAI_VERSION")
azure_endpoint:str = os.getenv("OPENAI_ENDPOINT")
deployment:str = os.getenv("OPENAI_DEPLOYMENT")
api_key:str = os.getenv("OPENAI_KEY")
model_name:str = os.getenv("OPENAI_MODEL_NAME2")



# Disable tracing since we're using Azure OpenAI
set_tracing_disabled(disabled=True)

@function_tool
def save_results(output):
    print(f"Saving results: {output}, timestamp:{datetime.time()}")

async def main():
    try:
        # Create the Async Azure OpenAI client
        client = AsyncAzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint,
        )

        # Configure the agent with Azure OpenAI
        agent = Agent(
            name="Assistant",
            instructions="You are a helpful assistant. Help user to find answers related to questions",
            model=OpenAIChatCompletionsModel(
                model=model_name,
                openai_client=client,
            ),
            tools=[WebSearchTool(), save_results]
        )
        
        while True:
            user_input = input("Enter your question (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break

            print(f"User Input: {user_input}")

            result = await Runner.run(agent, input=user_input)
            print(result.final_output)

    except OpenAIError as e:
        print(f"OpenAI API Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())