from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from pydantic import BaseModel, Field
from typing_extensions import Literal
from langchain_ollama import ChatOllama


llm = ChatOllama(model="llama3.2:latest", temperature=0)


class State(TypedDict):
    joke:str
    topic:str
    feedback:str
    funny_or_not:str
    
class FeedBack(BaseModel):
    
    grade:Literal["funny", "not_funny"] = Field(
        description="decide if the joke is funny or not"
    )
    feedback:str=Field(
        description="If the joke is not funny, provide feedback on how to improve"
    )
    
    
evaluator = llm.with_structured_output(FeedBack)

# node
def llm_call_generator(state:State):
    if state.get("feedback"):
        msg = llm.invoke(f"write a joke about {state['topic']} but take into account the feedback {state['feedback']}")
        
    else:
        msg = llm.invoke(f"write a joke about {state['topic']}")
        
    return {"joke":msg.content}

# node evalutor
def llm_call_evaluator(state:State):
    """LLM evaluate the joke"""

    grade = evaluator.invoke(f"grade a joke {state['joke']}")

    return {"funny_or_not": grade.grade, "feedback":grade.feedback}


def route_joke(state:State):
    """route back to generator or end based on up the feedback"""
    if state['funny_or_not']=="funny":
        return "Accepted"
    elif state["funny_or_not"]=="not_funny":
        return "Rejected + Feedback"

#### llm call generator-evaluator ###
optimizer_build = StateGraph(State)
optimizer_build.add_node("llm_call_generator", llm_call_generator)
optimizer_build.add_node("llm_call_evaluator", llm_call_evaluator)


optimizer_build.add_edge(START, "llm_call_generator")
optimizer_build.add_edge("llm_call_generator", "llm_call_evaluator")
optimizer_build.add_conditional_edges(
    "llm_call_evaluator",
    route_joke,
    {
        "Accepted":END,
        "Rejected + Feedback":"llm_call_generator"
    },
)
optimizer_workflow = optimizer_build.compile()


img = optimizer_workflow.get_graph().draw_mermaid_png()
with open('evalutor_optimizer.png', 'wb') as f:
    f.write(img)

state = optimizer_workflow.invoke({"topic":"Cats"})
print(state["joke"])