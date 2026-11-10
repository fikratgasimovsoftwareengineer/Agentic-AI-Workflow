from google.adk.agents import LlmAgent
from climate_ai_management.tools.human_in_loop import request_report_approval
from climate_ai_management.tools.report_publisher import publish_final_report



def build_human_approval_agent(model:str)->LlmAgent:
    
    return LlmAgent(
        name = "HumanApprovalAgent",
        model=model,
        description="Request human approval before the pubblishing the carbon footprint report.",
        instruction= ("Your role is to manage human review process \n"
                    "The report draft is available in session state\n"
                    "You MUST call function request_report_approval  to request the reviewier's decision\n"
                    "Never approve or reject on your own or by yourself\n"
                    "ONLY after explicit human approval, call publish_final_report to publish final report\n"
                    "Never publish a rejected or unapproved report.\n"
                    "When publication succeeds, present the report "
                    "to the user."),
        tools=[request_report_approval, 
               publish_final_report]
        
    )