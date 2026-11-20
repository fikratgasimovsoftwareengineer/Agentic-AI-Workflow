from pydantic import Field,BaseModel, ConfigDict

class ReasoningAction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    feedback_summary:str = Field(
        description="Summary of the human revision request"
    )
    
    proposed_changes:list[str] = Field(
        description="Specific changes required in the next report"
    )
    
    revision_instructions:str = Field(
        description="Details instruction for ReportWriterAgent"
    )
    
    human_comment:str