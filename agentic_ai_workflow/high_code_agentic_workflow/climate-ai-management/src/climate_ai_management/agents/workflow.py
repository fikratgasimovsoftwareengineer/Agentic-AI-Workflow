from google.adk.agents import Workflows
from climate_ai_management.agents.extraction_agent import build_extraction_agent
from climate_ai_management.agents.analysis_agent import build_analysis_agent
from climate_ai_management.agents.report_agent import build_report_agent


def build_workflow(model:str)->Workflows:
    return Workflows(
        name = "CarbonFootprintAnalsysisWorkflow",
        description="Extract, analysis and generate report on carbon footprint data",
        sub_agents=[
            build_extraction_agent(),
            build_analysis_agent(),
            build_extraction_agent()
        ]
    )