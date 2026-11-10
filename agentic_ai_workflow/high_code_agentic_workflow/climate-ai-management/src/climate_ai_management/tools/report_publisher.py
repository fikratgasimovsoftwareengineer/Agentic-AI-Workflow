from google.adk.tools.tool_context import ToolContext

from climate_ai_management.services.report_manager_identity import generate_report_id


def publish_final_report(tool_context:ToolContext):
    

    final_report = tool_context.state.get("final_report")
    approval = tool_context.state.get("report_approval")
    
    if not final_report:
        return {
            "status": "BLOCKED",
            "reason": "MISSING_REPORT",
            "message": "Final report is missing."
        }
    # 2. Check human approval
    if not approval:
        return {
            "status": "BLOCKED",
            "reason": "MISSING_APPROVAL",
            "message": "Human approval is missing."
        }


    report_id = generate_report_id(final_report)
   
    approved_report_id = approval.get("report_id")
    decision = approval.get("decision")
    
    if decision != "approve":
        return {
            "status": "BLOCKED",
            "reason": "NOT_APPROVED",
            "decision": decision,
            "message": "The human reviewer did not approve the report."
        }
        
    
    print(f"Approved : {approved_report_id}")
    print(f"reportID : {report_id}")
    print(f"decision : {decision}")
    if approved_report_id != report_id:
        return {
            "status": "BLOCKED",
            "reason": "REPORT_ID_MISMATCH",
            "message": "Approval does not match the current report."
        }
    tool_context.state["published_report"] = final_report
    tool_context.state["publication_status"] = "published"
    
    return {
        "status":"PUBLISHED",
        "report_id": report_id,
        "message":"The approved report has been published successfully."
    }                