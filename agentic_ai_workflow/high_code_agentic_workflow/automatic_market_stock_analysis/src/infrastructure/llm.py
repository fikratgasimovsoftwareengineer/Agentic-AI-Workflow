from src.interfaces.i_ollama import ILLMRouter
from typing import TypeVar
from src.config.app_settings import AppSettings
from pydantic import BaseModel
from langchain_ollama import ChatOllama

T = TypeVar("T", bound=BaseModel)

class OllamaRouter(ILLMRouter):
    
    
    def __init__(self,settings:AppSettings):
        
        self._chat = ChatOllama(
            base_url = settings.ollama_base_url,
            model = settings.ollama_model,
            temperature=0.0
        )
    
    def invoke_structured(self, prompt:str, schema:type[T]):
        
        structured  = self._chat.with_structured_output(schema)
        return structured.invoke(prompt)
    
    
    
