from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

from langchain_ollama import ChatOllama


llm = ChatOllama(model="qwen3:8b", temperature=0)
# Graph state
class State(TypedDict):
    topic: str
    joke: str
    story: str
    poem:str
    combined_output: str

def call_llm_1(state:State):
    msg = llm.invoke(f"write joke about {state['topic']}")
    return {"joke":msg.content}

def call_llm_2(state:State):
    msg = llm.invoke(f"write story about {state['topic']}")
    
    return {"story":msg.content}

def call_llm_3(state:State):
    msg = llm.invoke(f"write a poem about {state['topic']}")
    
    return {"poem":msg.content}

def aggregator(state:State):
    #"combine jokes"
    
    combined = f"Here's a Joke, Story, and Poem about {state['topic']}!\n\n"
    
    combined += f"JOKE:\n{state['joke']}\n\n"
    combined += f"STORY:\n{state['story']}\n\n"
   
    combined += f"POEM:\n{state['poem']}"
    return {"combined_output":combined}

#build workflow
parallel_workflow = StateGraph(State)

parallel_workflow.add_node("call_llm_1",call_llm_1)
parallel_workflow.add_node("call_llm_2", call_llm_2)
parallel_workflow.add_node("call_llm_3",call_llm_3)
parallel_workflow.add_node("aggregator",aggregator)

#add edges to nodes
parallel_workflow.add_edge(START, "call_llm_1")
parallel_workflow.add_edge(START, "call_llm_2")
parallel_workflow.add_edge(START, "call_llm_3")
parallel_workflow.add_edge("call_llm_1", "aggregator")
parallel_workflow.add_edge("call_llm_2", "aggregator")
parallel_workflow.add_edge("call_llm_3", "aggregator")

parallel_workflow.add_edge("aggregator", END)
parallel_flow = parallel_workflow.compile()

image_bytes = parallel_flow.get_graph().draw_mermaid_png()

with open('parallel_executuin.png', 'wb') as draw_img:
    draw_img.write(image_bytes)
    
    
### invokation ##
state = parallel_flow.invoke({"topic":"cats"})
print(state['combined_output'])