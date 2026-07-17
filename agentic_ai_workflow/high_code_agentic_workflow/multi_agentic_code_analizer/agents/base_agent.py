# =============================================================
# agents/base_agent.py
# =============================================================

from ..interfaces.i_base_agent import IBaseAgents
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


#from tracking.ml_flow_tracker import AgentRunTracker


class BaseAgent(LlmAgent, IBaseAgents):
    """
    Classe base astratta per tutti gli agenti di ReasonerHub.

    Flusso per ogni query:
        1. Chiamata iniziale al modello  →  risposta + confidence
        2. Se tool call rilevata         →  esegui tool → reinvia
        3. Se confidence < soglia        →  loop self-reflection
        4. Log tutto su MLflow
    """

    def __init__(self, model: str, name: str, instructions: str,
             description: str, tools: list):
        """    self._model  = model
        self._name = name
        self._instructions:str = instructions
        self._description = description
        self._tools = tools """
        
        super().__init__(
                model=LiteLlm(model=f"ollama_chat/{model}"),
                name=name,
                instruction=instructions,
                description=description,
                tools=tools,
                output_key=f"{name}_result",
            )
        
    def _execute_tools(self, tool_name:str, tools_args:str):
        """Default — agenti figli sovrascrivono se hanno tool propri."""
        return f"Tool '{tool_name}' non disponibile in BaseAgent."


"""     ### Property ###
    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, agent_name:str)->None:
        if not agent_name:
            raise ValueError("Agent name is not setted")
        self._name = agent_name
        

    #### model ####
    @property
    def model(self) -> str:
        return self._model
    @model.setter
    def model(self, llm_agent:str)->None:
        if not llm_agent:
            raise ValueError("LLM Agent is not setted")
        self._model = llm_agent
        
    #### INTRUCTTIONS ###
    @property
    def instructions(self)->str:
        return self._instructions
    @instructions.setter
    def instructions(self, instructions:str)->None:
        if not instructions:
            raise ValueError("Instructions is not setted")
        self._instructions = instructions
        
        
        
    @property
    def description(self)->str:
        return self._description
    @description.setter
    def description(self, description)->None:
        if not description:
            raise ValueError("Il Modello ha bisogno di descrizione")
        
        self._description = description
        

    @property
    def tools(self) -> list:
        return self._tools                         
    @tools.setter
    def tools(self, list_of_tools:list):
        if not isinstance(list_of_tools, list):
            raise TypeError("Tools should be List type")
        self._tools = list_of_tools
        
        
 """