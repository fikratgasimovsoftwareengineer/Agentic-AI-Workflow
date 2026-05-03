from openai import AzureOpenAI
from dataclasses import dataclass, field
import os
import requests
import pathlib
from dotenv import load_dotenv
import sys
import openai
import json
import time
import logging
import jsonify
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
env_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(env_path))
load_dotenv(dotenv_path=env_path / '.env')

from utils.joke_handle import get_joke

@dataclass
class InferenceGpt4o:
    
    api_version:str = os.getenv("OPENAI_VERSION")
    azure_endpoint:str = os.getenv("OPENAI_ENDPOINT")
    subscription_key:str = os.getenv("OPENAI_KEY")
    deployment:str = os.getenv("OPENAI_DEPLOYMENT")
    
        
    system_prompt:str = """
        You are a helpful assistant
    """
    
    url:str="https://sv443.net/jokeapi/v2/joke/Any"
    
    def __post_init__(self):
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint= self.azure_endpoint,
            api_key=self.subscription_key,
        )
        
        self.available_tools = {
            "get_joke":get_joke 
        }
        
    
    conversation_history:list = field(default_factory=list)



    # ... all'interno della tua classe InferenceGpt4o ...
    
    
    def get_completion(self, input_user: str):
        """_summary_
        la questo funziona assorba la funziona get completion che invece ritira 
        le informazione dalla terzo party.

        Args:
            input_user (str): _description_
        """
        
        # 1. CORREGGI LA DEFINIZIONE DELLO STRUMENTO!
        # Questo è il passo più importante. I parametri devono corrispondere a quelli della tua funzione get_joke.
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_joke",
                    "description": "Ritorna una barzelletta divertente. Supporta categorie come Any, Programming, Pun, Christmas.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "La categoria della barzelletta, es. 'Programming', 'Christmas'",
                                "enum": ["Any", "Programming", "Pun", "Christmas", "Spooky"],
                            }
                        },
                        "required": ["category"],
                    },
                },
            }
        ]

        if not self.conversation_history:
            self.conversation_history.append({"role": "system", "content": self.system_prompt})

        self.conversation_history.append({"role": "user", "content": input_user})
        

        response = self.client.chat.completions.create(
            messages=self.conversation_history,
            model=self.deployment,
            tools=tools,
            tool_choice="auto",
        )
        
        response_message = response.choices[0].message
        # 2. ASSEMBLA CORRETTAMENTE I PEZZI DALLO STREAM
     
        
        if response_message.tool_calls:
         
            
            function_name = response_message.tool_calls[0].function.name
            function_to_call = self.available_tools.get(function_name)
        
        
            if function_to_call:
                
                # Ora il parsing JSON funzionerà perché `arguments` è una stringa JSON completa
                function_args = json.loads(response_message.tool_calls[0].function.arguments)
              
                
                if function_args:
                
                    # Chiama la funzione Python
                    function_response = function_to_call(**function_args)
                    
                    self.conversation_history.append({"role":"assistant", "content":function_response})
                    print("Output of function call:")
                    print(function_response)
        
        else:
            self.conversation_history.append({"role":"assistant", "content":response.choices[0].message.content})
            print(f"**Model own response**: {response.choices[0].message.content}")
    
    
    def get_completion_by_stream(self, input_user:str):
        
        """_summary_
        Questa funziona genera il testo in base al streaming.
        **PERO NON si prende in conto che tool_calls viene integrato!**
        Returns:
            _type_: _description_

        Yields:
            _type_: _description_
        """
         
        # 1. CORREGGI LA DEFINIZIONE DELLO STRUMENTO!
        # Questo è il passo più importante. I parametri devono corrispondere a quelli della tua funzione get_joke.
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_joke",
                    "description": "Talk about jokes",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string", "joke can be divided according to categories"
                                "description": "Categories can be divided such as 'Programming', 'Christmas'",
                                "enum": ["Any", "Programming", "Pun", "Christmas", "Spooky"],
                            }
                        },
                        "required": ["category"],
                    },
                },
            }
        ] 

        if not self.conversation_history:
            self.conversation_history.append({"role": "system", "content": self.system_prompt})

        self.conversation_history.append({"role": "user", "content": input_user})
        print(f"User question: {input_user}")

        try:
            response_stream = self.client.chat.completions.create(
                stream=True,
                messages=self.conversation_history,
                model=self.deployment,
                tools=tools,
                tool_choice="auto",
                )
        
            ## 
            collected_chunks = []
            batch = ""
            try:
                for chunk in response_stream:
                    if hasattr(chunk, 'choices') and chunk.choices:
                        piece = chunk.choices[0].delta.content  
                        if piece:
                            collected_chunks.append(piece)
                            batch += piece
                            while " " in batch:
                                word, _, batch = batch.partition(" ")
                                logging.debug(f"Yielding word{word}")
                                yield word + " "
                                
                                time.sleep(0.01)
                if batch:
                    logging.debug(f"Yielding remaining batch")
                    yield batch
                    
            finally:
                full_response = ''.join(collected_chunks)
                self.conversation_history.append({"role":"assistant","content":full_response})
                
                
        except openai.BadRequestError as e:
            status_code = getattr(e.response, 'status_code', None)
        
            if status_code==400:
                return jsonify({"error":"Ups,la richiesta non e` andata a buon fine, per favore ripeti ancora"}), 500
        

            
def main():
    
    inference = InferenceGpt4o()
    
    k = 'exit'
    while True:
    
        user_prompt = input('\n Enter Prompt: ').lower()
        print("====MODEL ANSWER========")
        
        if user_prompt == k:
            break
        
        response_generator = inference.get_completion_by_stream(user_prompt)
        
        for chunk in response_generator:
            print(chunk, end='', flush=True)
            
            
        
  
    
if __name__ == "__main__":
    main()