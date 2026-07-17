

from ..agents.base_agent import BaseAgent



### Report generator ###

## LO agent dovrebbe accettare le risposta delle Agente Logical and Syntax Analizer , e poi genera la rapport in base alle quello ##
class OptimizationAgent(BaseAgent):

    def __init__(self):
        
        super().__init__(
            model = "llama3.2:latest",
            name="code_optimization",
            description="Optimize and Generate risponse to User",
            instructions=("Your task is read and understand Optimization techniques based on given report from ReportAgent\n"
                "Based on this report:\n{code_report_generator_result}\n\n"  # ← output_key di ReportAgent
                "Provide clear optimization techniques. Be friendly and encouraging."
                "Conclude your response with encouraging statements"),
            tools=[]
        )

    def _execute_tools(self, tool_name:str, tools_args:str):
        return f"{tool_name} e {tools_args}"
   
