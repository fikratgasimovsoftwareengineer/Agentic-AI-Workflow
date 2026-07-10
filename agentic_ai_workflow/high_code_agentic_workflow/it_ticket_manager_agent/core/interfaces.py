from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from core.models import Ticket, TicketPriority,TicketCategory,TicketEvent

## va implementato in db ###
class ITicketRepository(ABC):
    
    @abstractmethod
    def create_ticket(self, ticket:Ticket)->Ticket:
        pass
    
    @abstractmethod
    def update_ticket(self, ticket_id:str, **fields)->Optional[Ticket]:
        pass
    
    @abstractmethod
    def get_ticket(self, ticket_id:str)->Optional[Ticket]:
        pass
    
    @abstractmethod
    def list_all_tickets(self)->list[Ticket]:
        pass
    
    @abstractmethod
    def get_similar_resolved_tickets(self, category:TicketCategory, limit:int)->list[Ticket]:
        pass
    
    @abstractmethod
    def log_event(self, event:TicketEvent):
        pass
    
### va implementato in tools ##
class INotificationService(ABC):
    
    @abstractmethod
    def notify_opened(self,ticket:Ticket):
        pass
    
    @abstractmethod
    def notify_resolved(self, ticket:Ticket):
        pass
    
    @abstractmethod
    def notify_escalated(self, ticket:Ticket):
        pass
    
## va implementato in tools ##
class IJiraService(ABC):
    
    @abstractmethod
    def create_issue(self,ticket:Ticket):
        pass
    
    @abstractmethod
    def update_issue(self, jira_key:str, status:str, comment:str):
        pass
    
    @abstractmethod
    def close_issue(self, jira_key:str, resolution:str):
        pass
    
class IMlFlowTracker(ABC):
    
    @abstractmethod
    def log_ticket(self, ticket:Ticket):
        pass
    
    @abstractmethod
    def log_tool_result(self, tool_name:str, result:dict):
        pass
    
    @abstractmethod
    def log_metrics(self, key:str, value:float):
        pass