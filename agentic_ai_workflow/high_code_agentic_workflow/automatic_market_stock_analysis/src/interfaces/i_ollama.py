from abc import ABC, abstractmethod
from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class ILLMRouter(ABC):
    
    @abstractmethod
    def invoke_structured(self, prompt:str, schema:type[T])->T:
        "Invocare il modello forzando l'output sulla schema dato"
        pass
    
    