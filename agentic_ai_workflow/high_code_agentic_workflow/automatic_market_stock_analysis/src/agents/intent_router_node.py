from src.domain.models import Classification, RouterState
from src.interfaces.i_ollama import ILLMRouter

class IntentRouterNode:
    
    name="intent_router"
    
    
    def __init__(self, llm:ILLMRouter):
        self._llm = llm
        
    def __call__(self, state:RouterState):
        prompt = (
                "Classifica la richiesta in UNA categoria tra: technology, "
                "economics, jobs, sport, scientific_research.\n\n"
                "then create related questions from 1 to 2 for advance web search in english,"
                f"RICHIESTA: {state['query']}"
            
            )
        
        plan = self._llm.invoke_structured(prompt, Classification)
        return {'classification':plan}