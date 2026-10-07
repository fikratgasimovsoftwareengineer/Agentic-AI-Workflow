from abc import ABC, abstractmethod
from typing import TypeVar
from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class IEvaluator(ABC):
    
    @abstractmethod
    def invoke_evaluator(self, response_aggregator:str, schema:type[T])->T:
        pass