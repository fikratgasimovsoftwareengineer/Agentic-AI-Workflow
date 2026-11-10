from google.adk.agents import LlmAgent
from climate_ai_management.tools.human_in_loop import request_report_approval



def build_human_approval_agent(model:str)->LlmAgent:
    
    return LlmAgent(
        name = "HumanApprovalAgent",
        model=model,
        description="Request human approval before the pubblishing the carbon footprint report.",
        instruction= ("Your role is to manage human review process \n"
                    "The report draft is available in session state\n"
                    "You MUST call function request_report_approval  to request the reviewier's decision\n"
                    "Never approve or reject on your own or by yourself\n"
                    "Never publish report without approval\n"
                    "After the tool returns, report its status\n"),
        tools=[request_report_approval]
        
    )