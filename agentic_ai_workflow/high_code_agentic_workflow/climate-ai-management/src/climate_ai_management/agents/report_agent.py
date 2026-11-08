from google.adk.agents import LlmAgent
from climate_ai_management.schemas.reporting_schema import ReportSchema

def build_report_agent(model:str)->LlmAgent:
    
    return LlmAgent(
        name="ReportWriterAgent",
        model=model,
        description="Generate a structured carbon footprint audit report for end user",
        instruction=(
            "You are report write about environmental carbon footprint and emissions\n"
            "Use extracted information:\n"
            "{extracted_data}\n\n"
            
            "Use analysis results:\n" 
            "{analysis_result}\n\n"
            
            "Produce and generate professional report in English Language."
            "Include executive summary, emissions overview, anomalies, limitations and recommendations."
            "Do not invent information or claim that which are not written or provided"
            "This is a preliminary, non-certified result."
            "Return data matching the required output schema"
            
            ),
        output_schema=ReportSchema,
        output_key="final_report"
    )

