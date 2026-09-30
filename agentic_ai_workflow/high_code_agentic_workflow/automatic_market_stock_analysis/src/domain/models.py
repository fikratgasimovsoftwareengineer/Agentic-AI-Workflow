from typing import Annotated, TypedDict,Literal
import operator

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
    query_reformulate: list[str] = Field(
        min_length=1,
        max_length=2,
        description = "Query created for advance web search in english"
    )
    reasoning:str = Field(...,description="Perche` questa categoria")



class RouterState(TypedDict, total=False):
    query:str
    classification:Classification
    results: Annotated[list[AgentOutput], operator.add]
    final_answer:str
    
