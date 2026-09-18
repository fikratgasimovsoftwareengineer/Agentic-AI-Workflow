from typing import Annotated, TypedDict,Literal
import operator
import json
from pydantic import BaseModel,Field

Category = Literal["technology", "economics", "jobs", "sport", "scientific_research"]

class AgentInput(TypedDict):    
    """Svolgersi nella gestione della domanda"""
    query:str
    
class AgentOutput(TypedDict):
    """risultati prodotti da un ramo di ricerca"""
    intent_type: Category
    output:str

class Classification(BaseModel):
    """Output validato del classificatore """
    type_of_request: Category
    reasoning:str = Field(...,description="Perche` questa categoria")


class RouterState(TypedDict):
    query:str
    classification:list[Classification]
    results: Annotated[list[AgentOutput], operator.add]
    final_answer:str