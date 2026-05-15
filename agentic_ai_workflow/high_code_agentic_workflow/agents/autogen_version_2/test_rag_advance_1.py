import os
from autogen import AssistantAgent, UserProxyAgent
import asyncio
from typing import Annotated
import pathlib
from dotenv import load_dotenv
import sys


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

if not all([azure_endpoint, api_key, model_name]):
    raise ValueError(
        "Assicurati di aver impostato le variabili d'ambiente: "
        "AZURE_OPENAI_API_BASE, AZURE_OPENAI_API_KEY, e AZURE_OPENAI_DEPLOYMENT_NAME"
    )

# Creazione dell'Agente Assistente (il "cervello" basato su GPT-4o)
# Questo agente decide quale strumento usare o se rispondere direttamente.
assistant = AssistantAgent(
    name="Assistant_GPT4o",
    llm_config={
        "config_list": [{
            "model": model_name,
            "api_type": "azure",
            "api_version": api_version,
            "base_url": azure_endpoint,
            "api_key": api_key
        }],
        "temperature": 0.4,
    },
    # Stop as soon as the assistant emits TERMINATE
    is_termination_msg=lambda msg: isinstance(msg, dict) and 
        isinstance(msg.get("content"), str) and "TERMINATE" in msg["content"],
    system_message="""
        You are a helpful and friendly AI Assistant.
        Answer the user's question in ONE turn. If a tool is helpful, call AT MOST ONE tool.
        If the question is ambiguous, make a reasonable assumption and answer once.
        Do NOT ask follow-up questions.
        End your final message with a friendly emoji, then on a new line write: TERMINATE
        """
)

# Creazione dell'Agente Proxy Utente (l'"esecutore")
# Questo agente esegue il codice e le funzioni che l'assistente gli fornisce.
user_proxy = UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    # 2 is enough for single-turn: (1) initial user message, (2) tool execution
    max_consecutive_auto_reply=2,
    # If the assistant ever asks something back, cut the loop
    default_auto_reply="TERMINATE",
    # Stop when we see the termination token from the assistant
    is_termination_msg=lambda msg: isinstance(msg, dict) and 
        isinstance(msg.get("content"), str) and "TERMINATE" in msg["content"],
        
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

@user_proxy.register_for_execution(name="get_weather")
@assistant.register_for_llm(description="Provide Weather information for a request city.")
async def get_weather(city: Annotated[str, "City for which you need to provide weather condition es. 'Roma'."]) -> str:
    """Ottiene il meteo per una data città (dati simulati)."""
  
    test_weather_data = {
        "Roma": "28°C, Sunny",
        "Milano": "24°C, Cloudy",
        "Napoli": "30°C, Clear"
    }
  
    weather = test_weather_data.get(city, "Meteo non disponibile")
    return f"Il meteo a {city} è: {weather}"





@user_proxy.register_for_execution(name="get_jokes")
@assistant.register_for_llm(description="Provide an insteresting joke via this function.")
async def get_jokes(joke_type: Annotated[str, "There are types of jokes such as  'tech', 'animali'."], 
                  joke_topic: Annotated[str, "this is topic of joke"]) -> str:

   
    return f"Type of joke is '{joke_type}' on topic '{joke_topic}'"

# --- 3. IMPLEMENTAZIONE DELLA FUNZIONALITÀ RAG (SIMULATA) ---
# In un sistema reale, questa funzione si collegherebbe a un database vettoriale
# come Azure AI Search, ChromaDB, o Pinecone.
def retrieve_from_vector_db(query: str) -> str:
    """
    SIMULAZIONE di una ricerca in un database vettoriale.
    Cerca documenti pertinenti in base a una query dell'utente.
    """
    print(f"--- ⚙️ ESECUZIONE RAG: Ricerca nella knowledge base per '{query}' ---")
    
    # Simula una knowledge base
    knowledge_base = {
        "policy rimborsi spese": "La policy aziendale prevede il rimborso delle spese di viaggio e alloggio presentando le ricevute entro 15 giorni dalla trasferta.",
        "configurazione vpn": "Per configurare la VPN, scarica il client dal portale aziendale, installalo e usa le tue credenziali di dominio per l'accesso.",
        "ferie": "Le richieste di ferie devono essere inviate tramite il portale HR con almeno 10 giorni lavorativi di preavviso.",
    }

    # Logica di ricerca semplificata (keyword matching)
    for key, value in knowledge_base.items():
        if all(word in query.lower() for word in key.split()):
            return value
    
    return "Mi dispiace, non ho trovato informazioni pertinenti nella mia base di conoscenza."




# Registriamo la funzione RAG come uno strumento per gli agenti
@user_proxy.register_for_execution(name="retrieve_knowledge")
@assistant.register_for_llm(description="Usa questa funzione per rispondere a domande che richiedono conoscenza specifica interna, come policy aziendali, procedure tecniche o documentazione di prodotto.")
def retrieve_knowledge(query: Annotated[str, "La domanda specifica dell'utente a cui trovare risposta nella base di conoscenza."]) -> str:
    """Funzione wrapper per la ricerca RAG."""
    return retrieve_from_vector_db(query)


# --- 4. ESECUZIONE DELLE CONVERSAZIONI DI TEST ---
async def main():
    
    
    user_question = ""
    while True:
        user_question = input("\n your question : ")
        print("\n********* TEST 1: Domanda semplice (risposta diretta da GPT-4o) *******")
        await user_proxy.a_initiate_chat(
            assistant,
            message=user_question.strip()
        )
        
        if user_question.lower() == "exit":
            break
    """ print("\n--- TEST 2: Domanda che richiede lo strumento 'get_weather' ---")
    await user_proxy.a_initiate_chat(
        assistant,
        #message="Potresti dirmi che tempo fa a Milano?",
    )

    print("\n--- TEST 3: Domanda che richiede lo strumento RAG ---")
    await user_proxy.a_initiate_chat(
        assistant,
       # message="Come funziona la policy per i rimborsi spese in azienda?",
    )

    print("\n--- TEST 4: Domanda che richiede un altro strumento ('get_jokes') ---")
    await user_proxy.a_initiate_chat(
        assistant,
        #message="Raccontami una barzelletta di tipo 'tech' sui programmatori.",
    )
    
    print("\n *** TEST 5: Domanda ambigua dove l'LLM deve scegliere tra RAG e risposta diretta ***-")
    await user_proxy.a_initiate_chat(
        assistant,
        #message="Come si chiedono le ferie?",
    ) """


if __name__ == "__main__":
    asyncio.run(main())