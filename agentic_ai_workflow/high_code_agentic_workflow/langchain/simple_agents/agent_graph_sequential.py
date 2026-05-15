from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage,BaseMessage,HumanMessage
from agent_static import base_agent, agent_explanair


class GraphState(TypedDict):
    messages:List[BaseMessage]
    intermediate_result:str 
    


### NODE DEL GRAFO
def calculator_node(state:GraphState)->GraphState:
    # ultimo
    user_query = state["messages"][-1].content
    
    # risultati
    result = base_agent.invoke({"messages":[("user", user_query)]})
    
    # estrai la risposta tecnica
    risposta_tecnia = result["messages"][-1].content.strip()
    
    print(f"📊 Calculator output: {risposta_tecnia}")
    
    return {
        "messages":[AIMessage(content=risposta_tecnia)],
        "intermediate_result":risposta_tecnia
        
    
    }
### NODE DI SPIEGATORE 
def explainer_node(state:GraphState)->GraphState:
    
    # acquistare il risultato numerico dal nodo precedente
    numeric_result = state["intermediate_result"]
    # Invoca l'agente spiegatore
    result = agent_explanair.invoke({"messages":[("user", numeric_result)]})
    
    final_msg = result["messages"][-1].content.strip()
    
    print(f"Explainer output: {final_msg}")
    return {"messages":[AIMessage(content = final_msg)]}

## builder
builder = StateGraph(GraphState)

builder.add_node("calculator", calculator_node)
builder.add_node("explainer", explainer_node)

# definisce il flusso
# set entry point
builder.set_entry_point("calculator")
builder.add_edge("calculator", "explainer")
builder.add_edge("explainer", END)

graph = builder.compile()

# ---------- Esecuzione ----------
if __name__ == "__main__":
    user_query = (
        "I have 150 euros and today 1 EURO = 1.17 dollars. "
        "How much dollars i will get if i convert all my euros to dollars?"
    )
    print("🤖 LangGraph pipeline starting...")
    # Stato iniziale
    initial_state = {"messages": [HumanMessage(content=user_query)]}
    # Esegui il grafo
    final_state = graph.invoke(initial_state)
    print("\n✅ Risposta finale dell'intero flusso:")
    print(final_state["messages"][-1].content)