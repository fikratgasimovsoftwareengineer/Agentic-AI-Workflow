
from climate_ai_management.services.report_manager_identity import generate_report_id
from climate_ai_management.schemas.decision_model_validator import ModelValidator
from google.adk import Event, Context
from google.adk.workflow import node
from google.adk.events import RequestInput
from typing import Any


       
        
@node(rerun_on_resume=False)
async def request_report_approval(context:Context):
    
    """Request human approval before publishing  a carbon footprint report.
        The reviewer must explicity approve or reject the draft.
    """
    report = context.state.get("final_report")
    if not report:
        raise ValueError("Final report is missing")
        
    ## convert report to json  to convert to json string ##
    report_id = generate_report_id(report)
    
    # request human approval

    yield RequestInput(

        message=("Please Review the Carbon Footprint report before pubblication. "
                f"Interrupt ID {report_id[:12]}\n"
                "Available decisions:\n"
                "- approve\n"
                "- reject\n"
                "- request_revision (provide a comment)\n"
                ),
        payload={
            "report_id":report_id,
            "report":report
        } ,
        response_schema=ModelValidator,
        
    )
    
    
        
