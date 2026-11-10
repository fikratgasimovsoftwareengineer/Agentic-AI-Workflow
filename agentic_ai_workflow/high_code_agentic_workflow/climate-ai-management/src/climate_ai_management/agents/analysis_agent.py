from google.adk.agents import LlmAgent
from climate_ai_management.schemas.analysis_schema import AnalysisSchema
from climate_ai_management.schemas.extration_schema import ExtractionSchema
from climate_ai_management.callbacks.validation_callbacks import validate_state

from climate_ai_management.tools.math_operations import find_difference_coe2, find_total
from google.adk.tools import FunctionTool

def build_analysis_agent(model:str)->LlmAgent:
    

    
    return LlmAgent(
        name="AnalysisAgent",
        model=model,
        description="Analysis carbon emissions and detect inconsistencies",
        instruction=(
            "You are the environmental data analysis specialist. "
            "Analyze the following extracted information:\n "
            "Extracted Emissions data: \n"
            "{extracted_data}\n\n"
            "You have two python function tools to calculate total of carbon emission and difference between them\n"
            "1. find_total: calculates the sum of the Scope 1, 2 and 3 \n"
            "2. find_difference_coe2: calculates the difference  between calculated and declared totals \n"
            "You must call find_total before reporting a calculated total\n"
            "Then call find_difference_coe2 to calculate the numerical discrepancy.\n"    
            "Do not perform these calculations mentally.\n"
            "Do not treat missing emission values as zero.\n"
            "If any required value is missing, state that the comparions can not be completed!\n"
            "Use the results in your final analysis \n"
            "Return data matching the required schema."
        ),
        tools=[find_total, find_difference_coe2],
        
        output_schema=AnalysisSchema,
        output_key="analysis_result",
        before_agent_callback=validate_state({
                "extracted_data":ExtractionSchema
            }),
        after_agent_callback=validate_state({
            "analysis_result":AnalysisSchema,
        })
        
    
    
    )
  