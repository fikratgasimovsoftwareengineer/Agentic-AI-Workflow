from pydantic import Field, ConfigDict, BaseModel


class AnalysisSchema(BaseModel):
    
    model_config = ConfigDict(extra="forbid")
    
    calculated_total_toco2e:float | None = Field(
        description="Calculate total emission when comparable data is available"
    )
    
    declared_total_toco2e:float | None = Field(
        description="Total emission declared in the document"
    )
    
    difference_tco2e:float | None = Field(
        description="Calculate total minus declared total"
    )
    
    findings:list[str] | None = Field(
        description="Detected inconsistency and relevant findings"
    )
    
    limitations: list[str] = Field(
        description="Limitations of the analysis"
    )
    recommended_actions:list[str] = Field(
        description="Recommend verification actions"
    )