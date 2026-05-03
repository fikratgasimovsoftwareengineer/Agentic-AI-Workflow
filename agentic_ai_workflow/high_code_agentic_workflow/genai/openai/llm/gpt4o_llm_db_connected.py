from openai import AzureOpenAI
from dataclasses import dataclass, field
import os
import pathlib
from dotenv import load_dotenv
import sys
import json

env_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(env_path))
load_dotenv(dotenv_path=env_path / '.env')

from utils.joke_handle import get_joke
from db.handle_db import HandleDB


@dataclass
class InferenceGpt4o:
    
    api_version:str = os.getenv("OPENAI_VERSION")
    azure_endpoint:str = os.getenv("OPENAI_ENDPOINT")
    subscription_key:str = os.getenv("OPENAI_KEY")
    deployment:str = os.getenv("OPENAI_DEPLOYMENT")
    
        
    system_prompt:str = """
        You are a helpful assistant. 
        You can use tools to fetch data from SqLite database, whenever needed
    """
    

    
    input_user:str=''
   
    
    conversation_history:list = field(default_factory=list)
    def __post_init__(self):
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint= self.azure_endpoint,
            api_key=self.subscription_key,
        )
      
        handle_db = HandleDB()
        
        self.available_tools = {
            "list_all_toys":handle_db.list_all_toys,
            "find_toys_by_prefix":handle_db.find_toys_by_prefix,
            "find_toys_by_range":handle_db.find_toys_by_range,
            "sort_random_toys":handle_db.sort_random_toys,
            "sort_most_expensive_toy":handle_db.sort_most_expensive_toy,
            "sort_cheapest_toy":handle_db.sort_cheapest_toy 
        }

        # modello leggere questo descrizione per capira quando e cosa deve chiamare
        self.tools = [
            {
                
                "type":"function",
                "function":{
                    
                    "name":"list_all_toys",
                    "description":"Retrieves all toys from the database",
                    "parameters":{"type":"object", 
                                  "properties":{},
                                  "required":[]},
                                  },
                },
                

            {
                "type":"function",
                "function":{
                    "name":"find_toys_by_prefix",
                    "description":"Find toys by name prefix",
                    "parameters":{
                        "type":"object",
                        "properties":{
                            "prefix":{"type":"string", "description":"The prefix of the toy name to search for"}
                        },
                        
                    },
                    "required":["prefix"],
                },
                
            },
            
            {
                "type": "function",
                
                "function": {
                    "name": "find_toys_by_range",
                    
                    "description": "Finds toys within a specific price range.",
                    
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "low_price": {"type": "number", "description": "The minimum price."},
                            "high_price": {"type": "number", "description": "The maximum price."}
                        },
                        "required": ["low_price", "high_price"],
                    },
                },
            },
                
            {
                "type": "function",
                "function":{
                    "name":"sort_most_expensive_toy",
                    "description":"Get the most expensive toy from the database",
                    "parameters":{
                        "type":"object",
                        "properties":{
                            "count":{"type":"integer", "description":"The number of most expensive toys to retrieve"}
                        },
                        "required":["count"]
                    }
                }
            },
            
            {
                "type":"function",
                "function":{
                    "name":"sort_cheapest_toy",
                    "description":"Get the cheapest toy from the database",
                    "parameters":{
                        "type":"object",
                        "properties":{
                            "count":{"type":"integer","description":"The number of the cheapest toys to retrieve"}
                        },
                        "required":["count"]
                    }
                }
            }
               
            
            
        ]
      
    # ... all'interno della tua classe InferenceGpt4o ...
    def get_completion(self, input_user: str):
      

        if not self.conversation_history:
            self.conversation_history.append({"role": "system", "content": self.system_prompt})

        self.conversation_history.append({"role": "user", "content": input_user})
        

        # Chiediamo al modello di rispondere o di scegliere un tool.
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=self.conversation_history,
            tools=self.tools,
            tool_choice="auto",
        )

        response_msg = response.choices[0].message
      
        if response_msg.tool_calls:
            
            self.conversation_history.append(response_msg)
            
            for tool_call in response_msg.tool_calls:
                # get function name
                function_name = tool_call.function.name
                # mapp function name to available functions
                function_to_call = self.available_tools.get(function_name)
                if not function_to_call:
                    print(f"Errore: Funzione '{function_name}' non trovata .")
                    continue
                # get arguments of functions 
                function_args =json.loads(tool_call.function.arguments) 
                print(f"Calling the function name {function_name} with args :{function_args}")
                
                # function response
                function_response = function_to_call(**function_args)
                
                ## quam praticamente il modello osserva il output della funzione e la domanda della utente
                self.conversation_history.append({
                    "role":"tool",
                    "name":function_name,
                    "tool_call_id":tool_call.id,
                    "content":json.dumps(function_response)
                })
                
         

         
            
            final_response = self.client.chat.completions.create(
                model = self.deployment,
                messages = self.conversation_history
            )
            self.conversation_history.append(final_response.choices[0].message)
            
            return final_response.choices[0].message.content
        
        else:
            final_response = response_msg.content
            self.conversation_history.append({"role":"assistant", "content":final_response})
            return final_response
              
def main():
    inference = InferenceGpt4o()
    

    k = 'exit'
    while True:
        user_prompt = input('\nEnter Prompt (or "exit" to quit): ').lower()
        if user_prompt == k:
            break
        
        print("====MODEL IS THINKING...========")
        output_db = inference.get_completion(user_prompt)
        print("===MODEL RESPONSE===='\n")
        print(output_db)
            

if __name__ == "__main__":
    main()
        
