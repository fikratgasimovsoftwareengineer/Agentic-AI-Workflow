from src.interfaces.i_evaluator import IEvaluator
from pydantic import BaseModel
from typing import TypeVar
from src.interfaces.i_ollama import ILLMRouter

T = TypeVar("T", bound=BaseModel)

class Evaluator(IEvaluator):
    
    def __init__(self, llm:ILLMRouter):
        self._llm = llm 
    
    def invoke_evaluator(self, response_aggregator:str, schema:type[T]):
        
        return self._llm.invoke_structured(response_aggregator, schema)
        
        