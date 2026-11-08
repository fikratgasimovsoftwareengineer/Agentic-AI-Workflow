from pydantic import BaseModel, Field, ConfigDict

class ReportSchema(BaseModel):

    model_config = ConfigDict(extra="forbid")

    executive_summary: str = Field(
        description="Executive summary of the carbon footprint analysis"
    )

    emissions_overview: str = Field(
        description="Overview of extracted emissions data"
    )

    anomalies: list[str] = Field(
        description="Detected anomalies and inconsistencies"
    )

    limitations: list[str] = Field(
        description="Limitations and missing information"
    )

    recommendations: list[str] = Field(
        description="Recommended corrective and verification actions"
    )

    disclaimer: str = Field(
        description="Statement that this is a preliminary non-certified audit"
    )