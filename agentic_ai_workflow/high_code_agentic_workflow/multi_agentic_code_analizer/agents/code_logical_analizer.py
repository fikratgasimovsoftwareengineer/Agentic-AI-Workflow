

from ..agents.base_agent import BaseAgent



### CODE LOGICAL ANALYSIZE ###
class CodeLogicAnalyzerAgent(BaseAgent):

    def __init__(self):
        
        super().__init__(
            model = "qwen3.5:9b",
            name="code_logic_analizer",
            description="Analze given code and find out possible logical errors",
            instructions=("Your task is to analyze the logic of the given code "
                "and identify any logical errors or flaws in reasoning.\n"
                "Provide the logical errors found in clear bullet points.\n"
                "If no logical errors are found, state that explicitly."),
            tools=[],
           
        )

    def _execute_tools(self, tool_name:str, tools_args:str):
        return f"{tool_name} e {tools_args}"
   
