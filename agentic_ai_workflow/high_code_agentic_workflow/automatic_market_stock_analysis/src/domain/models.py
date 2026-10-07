from typing import Annotated, TypedDict,Literal, List
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



## send worker
class SendTask(TypedDict):
    search_query:str
    intent_type:Category
    
class RouterState(TypedDict, total=False):
    query:str
    classification:Classification
    results: Annotated[list[AgentOutput], operator.add]
    final_answer:str
    # feedback #
    grade:str
    feedback:str
    revision_count:int # guardrails antiloop infinito!



## SRP: sintetizzare l'ultima risposta
class FinalReport(BaseModel):
    final_answer:str = Field(..., description="Risposta sintetica e strutturale ai risultati della ricerca")
    
    
    
### Feedback ###
class Feedback(BaseModel):
    grade:Literal["approved", "needs_revision"] = Field(
        description="approved se la risposta e` completa, accurata e cita la fonte; needs_revision altrimenti"
    )
    feedback:str=Field(
        description="Se needs_revision, cosa manca e come migliorare la risposta"
    )
   
