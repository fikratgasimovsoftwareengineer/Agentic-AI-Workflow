from google.adk.tools.tool_context import ToolContext
import json
import hashlib

def request_report_approval(tool_context:ToolContext):
    
    """Request human approval before publishing  a carbon footprint report.
        The reviewer must explicity approve or reject the draft.
    """
    report = tool_context.state.get("final_report")
    if not report:
        return {
            "status":"Error",
            "message":"No report available for review"
        }
        
    ## convert report to json  to convert to json string ##
    report_json = json.dumps(report)
    report_id = hashlib.sha256(report_json.encode("utf-8")).hexdigest()
    
 
    tool_confirmation = tool_context.tool_confirmation

    # request human approval
    if not tool_confirmation:
        tool_context.request_confirmation(
            hint=("Please Review the Carbon Footprint report before pubblication. "
                  f"Report ID {report_id[:12]}"
                  "approve or reject the report."
                  ),
            payload={
                "report_id":report_id,
                "decision":"approve",
                "comment":""
            }
        )
        
        return {
            "status":"PENDING_APPROVAL",
            "report_id":report_id   
        }
        
    # process human approval or reject
    payload = tool_confirmation.payload or {}
    
    if not tool_confirmation.confirmed:
        decision = "reject"
    else:
        decision = payload.get("decision", "reject")
        
    if (
    payload.get("report_id") != report_id
        or
    decision not in ("approve", "reject")
    ):
         decision = "reject"
         
    tool_context.state["report_approval"] = {
        "report_id":report_id,
        "decision":decision,
        "comment": payload.get("comment", "")
    }
    
    return {
        "status": (
            "APPROVED"  if decision == "approve" else "REJECTED"
        ),
        "report_id":report_id
    }
        