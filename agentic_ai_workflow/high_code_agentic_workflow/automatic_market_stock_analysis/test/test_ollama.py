from src.infrastructure.llm import OllamaRouter
from src.domain.models import RouterState
from src.config.app_settings import AppSettings
from src.infrastructure.tavily_search import TavilySearch
from src.infrastructure.evaluator import Evaluator
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
load_dotenv()          # ←
### agenti

from src.agents.intent_router_node import IntentRouterNode
from src.agents.search_node import SearchWorkerNode
from src.agents.dispatcher_agent import DispatcherAgent
from src.agents.final_response_aggregator import FinalResponseAggre

from src.agents.routing import routing_validator_node
from src.agents.evalutor_agent import EvaluatorAgent



def main():
    
    appsettings = AppSettings()
    
    ## 1. composition 
    intent_router = IntentRouterNode(OllamaRouter(appsettings))  
    
    
    #2. qui dispatche agent legge dal intent router: intent type e search_query
    
    dispatcher_agent = DispatcherAgent() 
    
    search_worker = SearchWorkerNode(TavilySearch(appsettings))
    

    #worker_agents = 
    
    aggregator_agent = FinalResponseAggre(OllamaRouter(appsettings))
    
    evaluator_agent = EvaluatorAgent(Evaluator(OllamaRouter(appsettings)))

    # 2 grafo
    builder = StateGraph(RouterState)
    
    
    #### 3 construzione dei node
    builder.add_node("intent_router",intent_router)
    builder.add_node("search_worker",search_worker)
    builder.add_node("aggregator_agent", aggregator_agent)
    builder.add_node("evaluator_agent", evaluator_agent)
    
    
    
    ### 4. construzione dei edge
    builder.add_edge(START, "intent_router")
    builder.add_conditional_edges("intent_router", 
                                    dispatcher_agent,   
                                    ["search_worker"])
    
    builder.add_edge("search_worker", "aggregator_agent")
    builder.add_edge("aggregator_agent", "evaluator_agent")
    builder.add_conditional_edges(
        "evaluator_agent",
        routing_validator_node,
        {"final_response_aggregator":"aggregator_agent", END:END}
    )
    #builder.add_edge("aggregator_agent", END)  
    
    graph = builder.compile()
        
             
    ### salvataggio del grafo
    png_bytes = graph.get_graph().draw_mermaid_png()
    with open('graph_orhestratore.png', 'wb') as f:
        f.write(png_bytes)
         
    
    while True:
        domanda =  input("\nInserisci la domanda (o 'exit'): ").strip()
        if domanda.lower() == 'exit':
            break
        if not domanda:
            continue
        
        result = graph.invoke({"query":domanda})
        print(f"La risposta \n")
        print(result['final_answer'])
        
        


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