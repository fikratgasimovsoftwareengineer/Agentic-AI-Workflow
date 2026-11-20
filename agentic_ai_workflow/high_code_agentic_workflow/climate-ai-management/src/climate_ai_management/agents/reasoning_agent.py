from google.adk.agents import LlmAgent
from climate_ai_management.schemas.reasoning_model_schema import ReasoningAction
def reasoning_on_human_feedback(model_reasoning:str)->LlmAgent:
    
    return LlmAgent(
        name = "ReasoningAction",
        model=model_reasoning,
        description = ("Think and analyze human revision feedback and prepare "
        "a grounded revision plan for ReportWriterAgent"),
        
        instruction = (
            "Your task is analize human feedback and prepare structured revision plan"
            "Identify which sections needs revision"
            "Propose changes based on the part that needs revision"
            "Prepare Revision instructions for ReportWriterAgent"
            "Use Human Feedback: \n"
            "{revision_feedback}\n\n"
            "Use Extracted Data:\n" 
            "{extracted_data}\n\n"
            
            "Use final report \n"
            "{final_report}\n\n"
            "Return a structured revision plan matching "
            "the required output schema."
                        
        ),
        
      output_schema=ReasoningAction,
      output_key = "revision_plan"
        
    )