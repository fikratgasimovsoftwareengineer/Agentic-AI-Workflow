from google.adk.tools.tool_context import ToolContext
import json
import hashlib

def publish_final_report(tool_context:ToolContext):
    

    final_report = tool_context.state.get("final_report")
    approval = tool_context.state.get("report_approval")
    
    if not final_report or not approval:
        return {
            "status":"BLOCKED",
            "message": "Report or human message is missing"
        }
        
    report_id = hashlib.sha256(json.dumps(
        final_report,
        sort_keys=True,
        ensure_ascii=False
    ).encode("utf-8")).hexdigest()
    
    if ( approval.get("report_id") != report_id
    or
        approval.get("decision") != "approve"
    ):
        return {
                "status":"BLOCKED",
                "message": "Report or human message is missing"
            }
        
    tool_context.state["published_report"] = final_report
    tool_context.state["publication_status"] = "publised"
    
    return {
        "status":"PUBLISHED",
        "report_id": report_id,
        "report":final_report
    }                