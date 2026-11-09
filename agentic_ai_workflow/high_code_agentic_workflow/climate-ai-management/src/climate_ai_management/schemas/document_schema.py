from pydantic import BaseModel, Field, ConfigDict
from typing import Any

class PageData(BaseModel):  
    model_config = ConfigDict(extra="forbid")
    page_number:int = Field(ge=1)
    page_text:str
    layout:dict[str, Any]

class DocumentHandler(BaseModel):
    
    model_config = ConfigDict(extra="forbid")
    
    document_id: str
    filename: str
    page_count: int = Field(ge=1)
    page_block: list[PageData]
    