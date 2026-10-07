from src.domain.models import RouterState
from langgraph.graph import END


def routing_validator_node(route:RouterState):
    
    if route['grade']=='approved':
        return END
    if route['grade'] == 'needs_revision':
        return "final_response_aggregator"
    if route.get("revision_count", 0 ) > 2:
        return END 