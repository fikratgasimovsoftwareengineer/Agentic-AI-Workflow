from src.infrastructure.llm import OllamaRouter
from src.domain.models import RouterState
from src.config.app_settings import AppSettings
from src.infrastructure.tavily_search import TavilySearch
from langgraph.graph import StateGraph, START, END

### agenti

from src.agents.intent_router_node import IntentRouterNode
from src.agents.tavil_research_node import TavilyResearchNode
from src.agents.final_response_aggregator import FinalResponseAggre
def main():
    
    appsettings = AppSettings()
    
    ## 1. composition 
    intent_router = IntentRouterNode(OllamaRouter(appsettings))    
    research_agent = TavilyResearchNode(TavilySearch(appsettings))

    aggregator_agent = FinalResponseAggre(OllamaRouter(appsettings))

    # 2 grafo
    builder = StateGraph(RouterState)
    
    
    #### 3 construzione dei node
    builder.add_node("intent_router",intent_router)
    builder.add_node("research_agent",research_agent)
    builder.add_node("aggregator_agent", aggregator_agent)
    
    
    ### 4. construzione dei edge
    builder.add_edge(START, "intent_router")
    builder.add_edge("intent_router", "research_agent")
    builder.add_edge("research_agent", "aggregator_agent")
    builder.add_edge("aggregator_agent", END)
    
    graph = builder.compile()
        
    """         
    ### salvataggio del grafo
    png_bytes = graph.get_graph().draw_mermaid_png()
    with open('graph.png', 'wb') as f:
        f.write(png_bytes)
        
    """
    while True:
        domanda =  input("\nInserisci la domanda (o 'exit'): ").strip()
        if domanda.lower() == 'exit':
            break
        if not domanda:
            continue
        
        result = graph.invoke({"query":domanda})
        print(f"La risposta \n")
        print(result['final_answer'])
        
        
        
        """    print(f"{result.}")
        for r in result['results']:
            print(f"- {r['output'][:120]}...\n") """
            
    

        #"query":"Come sta evolvendo il mercato del lavoro tech in Europe
        
if __name__ == "__main__":
    main()
    
    
""" 
while True:
    question = input("Inserisce la domanda: \n")
    
    if question == 'exit':
        break
        
    
    prompt = (
        "Classifica la richiesta in UNA categoria tra: technology, "
        "economics, jobs, sport, scientific_research.\n\n"
        "then create related questions from 1 to 2 for advance web search in english,"
        f"RICHIESTA: {question}"
    
    )
    plan = router.invoke_structured(prompt, Classification)
    
    print(f"\nCategoria: {plan.type_of_request}")
    print(f"Query generate: {plan.query_reformulate}")
    try:
        for query in plan.query_reformulate:
            results = search.search_invoke(query)
            for r in results:
                print(f"- {r.title}\n  {r.content}\n {r.url}\n")
        
    except AttributeError as e :
        print(f"errore from tavily search {e}") """