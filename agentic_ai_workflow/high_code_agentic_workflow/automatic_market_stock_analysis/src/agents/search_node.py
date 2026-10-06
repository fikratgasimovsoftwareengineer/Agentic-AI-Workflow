from src.domain.models import  SendTask
from src.interfaces.i_tavily_search import ITavilySearch

class SearchWorkerNode:
    
    name = "search_worker"
    
    def __init__(self, tavil_search:ITavilySearch):
        self._tavil_search = tavil_search
        
    def __call__(self, task:SendTask):
        
        results = [
            {
                 "intent_type":task['intent_type'],
                 "output":f"{r.url} - r{r.content}"
            }
            for r in self._tavil_search.search_invoke(task['search_query'])
        ]

    
        return {"results":results}
    
    