
from abc import ABC, abstractmethod


class IDentifiable(ABC):
 
    ## MODEL ##
    @property
    @abstractmethod
    def model(self)->str:
        pass
    
    @model.setter
    @abstractmethod
    def model(self, agent_name:str):
        pass
            
    ## NAME ##
    @property
    @abstractmethod
    def name(self) -> str: pass

    @name.setter
    @abstractmethod
    def name(self, value: str): pass
    
    ## DESCRIPTION ##
    @property
    @abstractmethod
    def description(self)->str:
        pass
    
    @description.setter
    @abstractmethod
    def description(self, description:str):
        pass

 
    ## instruction ##
    @property
    @abstractmethod
    def instructions(self)->str:
        pass
    
    @instructions.setter
    @abstractmethod
    def instructions(self, instructions:str):
        pass

class IExecutable(ABC):
    @abstractmethod
    def _run(self, query:str):
        pass
    
class IToolable(ABC):
    ## tools ##
    """     @property
    @abstractmethod
    def tools(self)->list:
        pass
    
    @tools.setter
    @abstractmethod
    def tools(self, list_of_tools:list):
        pass """
    
    @abstractmethod
    def _execute_tools(self, tool_name:str, tools_args:str):
        pass
    
class IBaseAgents(IToolable):
    pass # composizion della interfaccia
    