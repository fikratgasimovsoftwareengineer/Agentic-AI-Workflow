from src.domain.models import RouterState
from src.interfaces.i_tavily_search import ITavilySearch


class TavilyResearchNode:
    
    name = "tavily_research_node"
    
    def __init__(self, tavil_search:ITavilySearch):
        self._tavil_search = tavil_search
        
    def __call__(self, state:RouterState):
        
        results = []
        for query in state['classification'].query_reformulate:
            for r in self._tavil_search.search_invoke(query):
                results.append({
                    "intent_type":state['classification'].type_of_request,
                    "output": f"{r.title} — {r.url}\n{r.content}",
                })
                
        return {"results":results}
    
    