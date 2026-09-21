from langchain.tools import tool
from typing_extensions import Literal
from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from langgraph.graph import MessagesState
from langchain.messages import SystemMessage, HumanMessage, ToolMessage

llm = ChatOllama(model="llama3.2:latest", temperature=0)

@tool
def multiply(a:int, b:int):
    """multiply two numbers and return the product"""
    return a*b
@tool
def add(a:int, b:int):
    """Add two numbers and return sum"""
    return a+b

@tool
def divide(a:int,b:int): 
    """Divide the first number by the second and return the result."""   
    return a/b

tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)


def llm_call(state:MessagesState):
    return {
        "messages":[
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                    )
                ]
                + state["messages"]
            )
        ]
    }
def tool_node(state: MessagesState):
    """Performs the tool call"""

    result = []
    
    for tool_call in state["messages"][-1].tool_calls:
        
        tool = tools_by_name[tool_call["name"]]
        
        observation = tool.invoke(tool_call["args"])
        
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
        
    return {"messages": result}

def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    messages = state["messages"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return "tool_node"
    
    return END

agent_build = StateGraph(MessagesState)
agent_build.add_node("llm_call", llm_call)
agent_build.add_node("tool_node", tool_node)

agent_build.add_edge(START, "llm_call")
agent_build.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node",END]
)

agent_build.add_edge("tool_node", "llm_call")
agent = agent_build.compile()
mg = agent.get_graph(xray=True).draw_mermaid_png()

with open ("multi_agentic.png", "wb") as f:
    f.write(mg)
    
    
messages = [HumanMessage(content="Add 3 and 4.")]
messages = agent.invoke({"messages":messages})
    