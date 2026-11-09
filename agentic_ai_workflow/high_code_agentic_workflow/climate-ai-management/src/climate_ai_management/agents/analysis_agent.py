from google.adk.agents import LlmAgent
from climate_ai_management.schemas.analysis_schema import AnalysisSchema
from climate_ai_management.schemas.extration_schema import ExtractionSchema
from climate_ai_management.callbacks.validation_callbacks import validate_state
def build_analysis_agent(model:str)->LlmAgent:
    
    return LlmAgent(
        name="AnalysisAgent",
        model=model,
        description="Analysis carbon emissions and detect inconsistencies",
        instruction=(
            "You are the environmental data analysis specialist. "
            "Analyze the following extracted information:\n "
            "{extracted_data}\n\n"
            "Check consistency of emissions data,missing values and declare totals.\n "
            "Calculate differences only when the values are comparable and total covers the same scopes\n "
            "Never interpret missing emissions as zero.\n "
            "Identify limitations and recommed verification actions.\n"
            "Return data matching the required schema "
        ),
        output_schema=AnalysisSchema,
        output_key="analysis_result",
        before_agent_callback=validate_state({
                "extracted_data":ExtractionSchema
            }
            ),
        after_agent_callback=({
            "analysis_result":AnalysisSchema,
        }),
        
    
    
    )
  