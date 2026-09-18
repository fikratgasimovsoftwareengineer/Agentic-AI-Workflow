from abc import ABC, abstractmethod
from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T", BaseModel)

class LLMRouter(ABC):
    
    @abstractmethod
    def invoke_qwen(self, prompt:str, schema:type[T]):
        "Invocare il modello forzando l'output sulla schema dato"
    
    