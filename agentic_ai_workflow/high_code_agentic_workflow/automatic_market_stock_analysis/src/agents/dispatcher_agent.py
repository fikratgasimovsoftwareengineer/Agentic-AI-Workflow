from src.domain.models import RouterState
from langgraph.types import Send

class DispatcherAgent:

    name="dispatcher_agent"

        
    def __call__(self, stato:RouterState)->list[Send]:
        
        classification = stato['classification']
        
      
        return [
            Send("search_worker", {
                "search_query":query,
                "intent_type":classification.type_of_request
            })
            for query in classification.query_reformulate
        ]