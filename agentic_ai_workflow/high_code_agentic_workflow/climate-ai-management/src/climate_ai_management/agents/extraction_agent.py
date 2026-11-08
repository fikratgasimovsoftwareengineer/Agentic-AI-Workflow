from google.adk.agents import LlmAgent
from climate_ai_management.schemas.extration_schema import ExtractionSchema


def build_extraction_agent(model:str)->LlmAgent:

    return LlmAgent(
        name="ExtractionAgent",
        model=model,
        description="Extract Carbon footprint information from documents",
        
        instruction=(
            "You are a carbon footprint data extraction specialist. "
            "Analyze the document supplied by the user. "
            "Extract company name, year, emission values, evidence "
            "and missing information. "
            "Use null when information is absent. "
            "Never fabricate information. "
            "Only report values supported by the source document. "
            "Return data matching the required output schema."
        ),
        output_schema=ExtractionSchema,
        output_key="extracted_data"
    )