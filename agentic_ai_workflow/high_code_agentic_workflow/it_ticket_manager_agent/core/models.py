from __future__ import annotations
from enum import Enum
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class TicketCategory(Enum):
    NETWORK="network"
    SERVER = "server"
    SOFTWARE = "software"
    ACCESS = "access"
    HARDWARE = "hardware"
    OTHER = "other"
    
class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

class TicketPriority(Enum):
    CRITICAL="critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    
class Ticket(BaseModel):
    id: str
    title: str
    description:str
    ### enum 
    category:TicketCategory
    status:TicketStatus
    priority:TicketPriority
    ## date time ###
    created_at:datetime
    updated_at:datetime
    resolved_at:Optional[datetime]  
    
class TicketEvent(BaseModel):
    ticket_id:str
    event_type:str
    description:str
    agent:str = "system"
    created_at:datetime = Field(default_factory=datetime.now)
    
    
class ToolResult(BaseModel):
    status:str
    message: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    
    def to_dict(self)->dict:
        return self.model_dump()
    
    
