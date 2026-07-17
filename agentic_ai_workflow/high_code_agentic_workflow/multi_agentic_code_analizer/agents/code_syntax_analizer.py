

from agents.base_agent import BaseAgent



### CODE LOGICAL ANALYSIZE ###
class CodeSyntaxAnalyzerAgent(BaseAgent):

    def __init__(self):
        
        super().__init__(
            model = "qwen3.5:9b",
            name="code_syntax_analizer",
            description="Analze given code and find out possible logical errors",
            instructions=["Your task is to analyze the syntax of the given code "
                "and identify any syntax errors or flaws in reasoning.\n"
                "Provide the syntax errors found in clear bullet points.\n"
                "If no syntax errors are found, state that explicitly."],
            tools=[]
        )

    def _execute_tools(self, tool_name:str, tools_args:str):
        return f"{tool_name} e {tools_args}"
   
