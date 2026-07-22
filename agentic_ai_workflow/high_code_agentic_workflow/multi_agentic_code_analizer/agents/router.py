from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm

class Router(LlmAgent):
    
    def __init__(self, sub_agents=None):
        super().__init__(
            model=LiteLlm(model="ollama_chat/qwen3.5:9b"),
            name = "RouterAgent",
            description="Verify and Find out User intention and Target\n",
            instruction=(
                "Your task is to identify what user wants on her/his request.\n"
                "RULE 1 - RESPOND DIRECTLY when:\n"
                "- User sends a greeting (hi, hello, ciao, etc.)\n"
                "- User asks a general question about programming concepts\n"
                "- User asks who you are or what you can do\n"
                "- User's message does NOT contain actual source code\n"
                "In these cases, respond naturally and mention you can help analyze code.\n\n"
                "RULE 2 - DELEGATE to CodePipelineAgent ONLY when:\n"
                "- User provides actual source code (with def, class, for, if, etc.)\n"
                "- User explicitly asks to analyze, debug, or optimize specific code\n"
                "- User pastes a code snippet and asks for review\n\n"
                "IMPORTANT: If there is NO CODE in the message, do NOT delegate. "
                "Respond yourself."
                ),
            sub_agents=sub_agents or [],
        )
        
    
    
    def _execute_tools(self, tool_name:str, tools_args:str):
        return f"{tool_name} e {tools_args}"
   