from pydantic import BaseModel,ConfigDict,Field

class ExtractionSchema(BaseModel):
    
    ## dont allow user to parse input ##
    model_config = ConfigDict(extra="forbid")
    
    ## define model llm ###
    ## output json structure ##
    company:str | None = Field(
        
        description="Company name extracted from the document"
    )
    
    year:int | None = Field(
        description= "The reporting the year"
    )
    
    scope_1_tco2e:float | None = Field(
        ge=0,
        description="Scope 1 emissions in the tonnes of CO2 equivalent"
    )
    
    scope_2_tco2e:float | None = Field(
        ge=0,
        description="Scope 2 emissions in tonnes of CO2 equivalent"
    )
    
    scope_3_tco2e: float | None = Field(
        default=None,
        ge=0,
        description="Scope 3 emissions in tonnes of CO2 equivalent"
    )
    
    declared_total_tco2:float | None = Field(
        ge=0,
        description="Total emissions explicitly declared in the document"
    )
    
    evidence:list[str] | None = Field(
        description="Supporting evidence extracted from the document"
    )
    
    missing_fields:list[str] | None = Field(
        description="Information missing from the document"
    )