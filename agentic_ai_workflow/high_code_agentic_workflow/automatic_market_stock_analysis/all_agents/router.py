from typing_extensions import Literal
from typing_extensions import TypedDict
from langchain.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END

from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3:8b", temperature=0)


class Router(BaseModel):
    """ step:Literal["poem", "story", "joke"] = Field(
        None, description="The next step in the routing process"
    ) """
    step:Literal["llm_call_1", "llm_call_2", "llm_call_3"] = Field(
        description="llm_call_1=story, llm_call_2=joke, llm_call_3=poem"
    )
    
    
router = llm.with_structured_output(Router)

##### STATE ####
class State(TypedDict):
    input:str
    decision:str
    output:str
    
##########################################################  
def llm_call_1(state:State):
    "write story"
    
    result = llm.invoke(state["input"])
    
    return {"output":result.content}

##########################################################
def llm_call_2(state:State):
    
    "write a joke"
    
    result = llm.invoke(state["input"])
    
    return {"output":result.content}

###########################################################
def llm_call_3(state:State):
    "write a poem"
    result = llm.invoke(state["input"])
    
    return {"output":result.content}


def llm_call_router(state:State):
    
    "route input to specific node"
    
    decision = router.invoke(
        [
            SystemMessage(
                content = "Router input to story, joke and poem based on user's request"
            ),
            HumanMessage(content=state['input'])
        ]
    )

    return {"decision":decision.step}


def router_decision(state:State):
    
    """    if state["decision"]=="story":
        return "llm_call_1"
    elif state["decision"]=="joke":
        return "llm_call_2"
    elif state["decision"]=="poem":
        return "llm_call_3" """
    return state['decision']
    
### router ###   
router_builder = StateGraph(State)

router_builder.add_node("llm_call_1", llm_call_1)
router_builder.add_node("llm_call_2", llm_call_2)
router_builder.add_node("llm_call_3", llm_call_3)

router_builder.add_node("llm_call_router", llm_call_router)

# add edges
router_builder.add_edge(START, "llm_call_router")
router_builder.add_conditional_edges(
    "llm_call_router",
    router_decision,
    {
        "llm_call_1":"llm_call_1",
        "llm_call_2":"llm_call_2",
        "llm_call_3":"llm_call_3",
    },
)


router_builder.add_edge("llm_call_1", END)
router_builder.add_edge("llm_call_2", END)
router_builder.add_edge("llm_call_3", END)

router_worflow = router_builder.compile()

msg_image= router_worflow.get_graph().draw_mermaid_png()

with open('router_flow.png', 'wb') as image:
    image.write(msg_image)
    
state = router_worflow.invoke({'input':'write me joke about cats'})
print(state['output'])