from pydantic import BaseModel, Field
from typing import Annotated, List, TypedDict
import operator
from langchain.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.types import Send
from langgraph.graph import StateGraph, START, END

################################################################
llm = ChatOllama(model="qwen3:8b", temperature=0)

class Section(BaseModel):
    name:str = Field(
        description="Name for this section of the report"
    )
    description:str = Field(
        "brief overview of the main topics and concepts"
    )
    
    
class Sections(BaseModel):
    sections:List[Section] = Field(
        description="sections of the report"
    )
    
planner = llm.with_structured_output(Sections)


###################################################################
class State(TypedDict):
    topic:str
    session:List[Section]
    completed_section:Annotated[list, operator.add]
    final_report:str
    

class WorkerState(TypedDict):
    section:Section
    completed_sections:Annotated[list, operator.add]
    
    
def orchestrator(state:State):
    
    report_sections=planner.invoke(
        
        [
            SystemMessage(content="Generate a plan for the work report"),
            HumanMessage(content=f"here is the report topic : {state['topic']}"),
        ]
    )
    return {"sections":report_sections.sections}


def llm_call(state: WorkerState):
    """Worker writes a section of the report"""

    # Generate section
    section = llm.invoke(
        [
            SystemMessage(
                content="Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting."
            ),
            HumanMessage(
                content=f"Here is the section name: {state['section'].name} and description: {state['section'].description}"
            ),
        ]
    )

    # Write the updated section to completed sections
    return {"completed_sections": [section.content]}


def synthesizer(state: State):
    """Synthesize full report from sections"""

    # List of completed sections
    completed_sections = state["completed_sections"]

    # Format completed section to str to use as context for final sections
    completed_report_sections = "\n\n---\n\n".join(completed_sections)

    return {"final_report": completed_report_sections}


# Conditional edge function to create llm_call workers that each write a section of the report
def assign_workers(state: State):
    """Assign a worker to each section in the plan"""

    # Kick off section writing in parallel via Send() API
    return [Send("llm_call", {"section": s}) for s in state["sections"]]

# Build workflow
orchestrator_worker_builder = StateGraph(State)

# Add the nodes
orchestrator_worker_builder.add_node("orchestrator", orchestrator)
orchestrator_worker_builder.add_node("llm_call", llm_call)
orchestrator_worker_builder.add_node("synthesizer", synthesizer)

# Add edges to connect nodes
orchestrator_worker_builder.add_edge(START, "orchestrator")
orchestrator_worker_builder.add_conditional_edges(
    "orchestrator", assign_workers, ["llm_call"]
)
orchestrator_worker_builder.add_edge("llm_call", "synthesizer")
orchestrator_worker_builder.add_edge("synthesizer", END)

# Compile the workflow
orchestrator_worker = orchestrator_worker_builder.compile()

# Show the workflow
img = orchestrator_worker.get_graph().draw_mermaid_png()

with open("multi_worker.png", 'wb') as f:
    f.write(img)

# Invoke
state = orchestrator_worker.invoke({"topic": "Create a report on LLM scaling laws"})
