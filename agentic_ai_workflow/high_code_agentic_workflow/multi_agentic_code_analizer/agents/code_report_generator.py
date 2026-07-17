

from agents.base_agent import BaseAgent



### Report generator ###

## LO agent dovrebbe accettare le risposta delle Agente Logical and Syntax Analizer , e poi genera la rapport in base alle quello ##
class ReportGeneratorAgent(BaseAgent):

    def __init__(self):
        
        super().__init__(
            model = "llama3.2:latest",
            name="code_report_generator",
            description="generate technical short report about given sysntax and logical errors",
            instructions=["Your task is to prepare report based on logical and syntax errors"
                "Provide report and mention which parts of code needs to be fixed and handled and optimized. \n"
                "Provide also optimization techniques based on software engineering knowledge\n",
                "Be clear and concise and clear out your answer using also bullet points.\n"
                "Report should be between around 400 characters."],
            tools=[]
        )

    def _execute_tools(self, tool_name:str, tools_args:str):
        return f"{tool_name} e {tools_args}"
   
