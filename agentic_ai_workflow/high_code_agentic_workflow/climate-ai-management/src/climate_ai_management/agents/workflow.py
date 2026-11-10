from google.adk import Workflow
from google.adk.workflow import START
from climate_ai_management.agents.extraction_agent import build_extraction_agent
from climate_ai_management.agents.analysis_agent import build_analysis_agent
from climate_ai_management.agents.report_agent import build_report_agent
from climate_ai_management.agents.human_approval_agent import build_human_approval_agent

def build_workflow(model:str)->Workflow:
    
    extraction_agent = build_extraction_agent(model=model)
    analysis_agent = build_analysis_agent(model=model)
    report_agent = build_report_agent(model=model)
    human_approval_agent = build_human_approval_agent(model=model)
    return Workflow(
        name = "CarbonFootprintAnalsysisWorkflow",
        description="Extract, analysis and generate report on carbon footprint data",
        edges=[(
            START,
            extraction_agent,
            analysis_agent,
            report_agent,
            human_approval_agent
        )
    ],
)