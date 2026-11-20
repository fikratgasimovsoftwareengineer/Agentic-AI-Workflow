from google.adk import Workflow
from google.adk.workflow import START
from climate_ai_management.agents.extraction_agent import build_extraction_agent
from climate_ai_management.agents.analysis_agent import build_analysis_agent
from climate_ai_management.agents.report_agent import build_report_agent
from climate_ai_management.tools.human_in_loop import request_report_approval
from climate_ai_management.agents.reasoning_agent import reasoning_on_human_feedback
from climate_ai_management.tools.review_routing import (
    route_review_decision,
    publish_final_report,
    reject_report,
    prepare_revision,
)



#from climate_ai_management.agents.human_approval_agent import build_human_approval_agent

def build_workflow(model:str)->Workflow:
    
    extraction_agent = build_extraction_agent(model=model)
    analysis_agent = build_analysis_agent(model=model)
    report_agent = build_report_agent(model=model)
    reasoning_agent = reasoning_on_human_feedback(model_reasoning=model)
    #human_approval_agent = build_human_approval_agent(model=model)
    return Workflow(
        name = "CarbonFootprintAnalsysisWorkflow",
        description="Extract, analysis and generate report on carbon footprint data",
        edges=[(
            START,
            ### agentts ### 
            extraction_agent,
            analysis_agent,
            report_agent,
            ## tools ### 
            request_report_approval,
            route_review_decision
        ),
        #COnditional edges
        (
            route_review_decision,
            {
                "approve":publish_final_report,
                "reject":reject_report,
                "request_revision":prepare_revision
            },
        ),
        (
            
           prepare_revision,
           reasoning_agent,
           report_agent
        ),
    
        
        ## revision loop
               
        
    ],
)