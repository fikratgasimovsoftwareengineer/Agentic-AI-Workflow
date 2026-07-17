

from ..agents.base_agent import BaseAgent



### Report generator ###

## LO agent dovrebbe accettare le risposta delle Agente Logical and Syntax Analizer , e poi genera la rapport in base alle quello ##
class CodeReportGeneratorAgent(BaseAgent):

    def __init__(self):
        
        super().__init__(
            model = "llama3.2:latest",
            name="code_report_generator",
            description="generate technical short report about given sysntax and logical errors",
            
            instructions=(
                    "Your task is to prepare a report based on logical and syntax errors.\n"
                    "SYNTAX ERRORS:\n{code_syntax_analizer_result}\n\n"
                    "LOGICAL ERRORS:\n{code_logic_analizer_result}\n\n"
                    "Generate a concise technical report under 400 characters."
                ),
            tools=[])

    def _execute_tools(self, tool_name:str, tools_args:str):
        return f"{tool_name} e {tools_args}"
   
