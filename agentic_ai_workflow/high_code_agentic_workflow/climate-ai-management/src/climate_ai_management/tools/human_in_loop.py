
from climate_ai_management.services.report_manager_identity import generate_report_id
from climate_ai_management.schemas.decision_model_validator import ModelValidator
from google.adk import Event, Context
from google.adk.workflow import node
from google.adk.events import RequestInput
from typing import Any

""" 

def request_report_approval(tool_context:ToolContext):
    
Request human approval before publishing  a carbon footprint report.
        The reviewer must explicity approve or reject the draft.
    
    report = tool_context.state.get("final_report")
    if not report:
        return {
            "status":"Error",
            "message":"No report available for review"
        }
        
    ## convert report to json  to convert to json string ##
    report_id = generate_report_id(report)
    
 
    tool_confirmation = tool_context.tool_confirmation
    
    # request human approval
    if not tool_confirmation:
        tool_context.request_confirmation(
            hint=("Please Review the Carbon Footprint report before pubblication. "
                  f"Report ID {report_id[:12]}\n"
                  "Available decisions:\n"
                  "- approve\n"
                  "- reject\n"
                  "- request_revision (provide a comment)\n"
                  ),
            payload={
                "report_id":report_id,
                "decision":"pending",
                "comment":""
            } 
        )
        
        return {
            "status":"PENDING_APPROVAL",
            "report_id":report_id   
        }
        
  
    
    if not tool_confirmation.confirmed:
        raw_decision = {
            "report_id": report_id,
            "decision": "reject",
            "comment": ""
        }
    else:   
         # process human approval or reject
        raw_decision = tool_confirmation.payload or {}
    
    try:
            
        decision = ModelValidator.validate_review(raw_decision)
    except ValueError as exc:
        
        return {
            "status":"INVALID_REVIEW",
            "message":str(exc)
        }
        
        
    if decision.report_id != report_id:
        return {
            "status":"BLOCKED",
            "reason":"REPORT_ID_MISMATCH"
        }
         
    tool_context.state["report_approval"] = {
        decision.model_dump(mode="json")
    }
    
    if decision.decision == "request_revision":
        tool_context.state["revision_feedback"] =(decision.comment)
    
    
    return {
       "status":decision.decision,
       "report_id":report_id,
       "comment":decision.comment
    }
        
"""

        
        
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
    
    
        
  
""" 
try:
    decision = ModelValidator.validate_review(response)
except ValueError as exc:
    
    return {
        "status":"INVALID_REVIEW",
        "message":str(exc)
    }
    
    
if decision.report_id != report_id:
    return ValueError("Report ID Mismatch")

yield Event(
    output=decision.model_dump(mode="json"),
    state={
        "report_approval":decision.model_dump(mode="json"),
        "revision_feedback":(
            decision.comment
            if decision.decision == "request_revision"
            else ""
        )
    },
    route = decision.decision
    
) """