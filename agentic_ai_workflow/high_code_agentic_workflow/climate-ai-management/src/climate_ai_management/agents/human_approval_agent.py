from google.adk.agents import LlmAgent
from climate_ai_management.tools.human_in_loop import request_report_approval
from climate_ai_management.tools.report_publisher import publish_final_report



def build_human_approval_agent(model:str)->LlmAgent:
    
    return LlmAgent(
        name = "HumanApprovalAgent",
        model=model,
        description="Request human approval before the pubblishing the carbon footprint report.",
        instruction=(
            "You manage the human approval and publication process.\n\n"

            "STEP 1 — HUMAN REVIEW\n"
            "Call request_report_approval to obtain explicit human approval.\n"
            "Never approve a report yourself.\n\n"

            "STEP 2 — PUBLICATION\n"
            "If the report is approved, call publish_final_report.\n"
            "If rejected, do not publish the report.\n\n"

            "STEP 3 — FINAL RESPONSE\n"
            "Use the actual status returned by publish_final_report.\n"
            "If the tool returns PUBLISHED, state clearly that the report "
            "has been published successfully.\n"
            "If the tool returns BLOCKED, explain why publication was blocked.\n"
            "If approval is pending, request human confirmation.\n\n"

            "IMPORTANT:\n"
            "Never ask the user to approve a report that has already "
            "been approved and published.\n"
            "Never describe a published report as a draft awaiting review.\n"
            "Never claim publication succeeded unless the publication tool "
            "explicitly confirms it."
        ),
        tools=[request_report_approval, 
               publish_final_report]
        
    )