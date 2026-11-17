from google.adk import Context, Event
from typing import Any
from climate_ai_management.services.report_manager_identity import generate_report_id
from climate_ai_management.schemas.decision_model_validator import ModelValidator

def route_review_decision(
    context: Context,
    node_input: Any,
) -> Event:

    # Validate human response
    decision = ModelValidator.model_validate(node_input)

    report = context.state.get("final_report")

    if not report:
        raise ValueError("Final report is missing.")

    report_id = generate_report_id(report)

    review_data = {
        "report_id": report_id,
        "decision": decision.decision,
        "comment": decision.comment,
    }

    return Event(
        output=review_data,
        state={
            "report_approval": review_data,
        },
        route=decision.decision,
    )

  
def elaborate_output_format(output:dict)->list:
    
    output_population = []
    for keys, values in output.items():
        title = keys.replace("_", " ").upper()
        
        if isinstance(values, str):
                
            output_population.append(f"{title}: \n{values}\n")
        elif isinstance (values, list):
            body = "\n".join(f"- {v}" for v in values)
            
            output_population.append({
                    (f"{title} \n{body}\n")
                })

    return ", ".join(map(str, output_population))


def publish_final_report(context:Context)->Event:

    
   
    final_report = context.state.get("final_report")
    approval = context.state.get("report_approval")
    
    text_output = elaborate_output_format(final_report)
    #output_format = elaborate_output_format(final_report)
    
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
        
    
    """print(f"Approved : {approved_report_id}")
    print(f"reportID : {report_id}")
    print(f"decision : {decision}") """
    if approved_report_id != report_id:
        return {
            "status": "BLOCKED",
            "reason": "REPORT_ID_MISMATCH",
            "message": "Approval does not match the current report."
        }
    
    return Event( 
        output={
            "status": "PUBLISHED",
            "report_id": report_id,
        },
        state={
                "published_report":final_report,
                "published_report_id":report_id,
                "publication_status":"published",
            
            },
     
        message = ("Carbon footprint report approved and published.\n"
                   f"Report ID: {report_id}"
                   f"Last Output : {text_output}")
    )              


def reject_report(context:Context)->Event:
    
    approval = context.state.get("report_approval")
    
    if not approval:
        raise ValueError("Human approval is missing")
    
    if approval.get("decision") != "reject":
        raise ValueError("Invalid rejection decision")
    
    return Event(
        output = {
            "status":"REJECTED",
        },
        state={
        
            "published_report":None,
            "published_report_id":None,
            "publication_status":"rejected"
        },
        message = ("Carbon footprint was rejected"
                "and has not been published")
    )

def prepare_revision(context:Context)->Event:
    
    
    approval = context.state.get("report_approval")
    if not approval:
        raise ValueError("Human decision is missing")
    
    
    if approval.get("decision") != "request_revision":
        raise ValueError("Revision was not requested")
    
    print()
    
    comment = approval.get("comment", "").strip()
    
    return Event(
        output = {
            "revision_feedback":comment
        },
        
        state= {
            "revision_feedback":comment,
            "report_approval":None,
            "published_report":None,
            "published_report_id":None,
            "publication_status":"revision_required",
        },
        
    )