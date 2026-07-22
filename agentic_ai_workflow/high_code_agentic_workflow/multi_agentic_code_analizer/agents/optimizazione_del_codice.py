

from ..agents.base_agent import BaseAgent



### Report generator ###

## LO agent dovrebbe accettare le risposta delle Agente Logical and Syntax Analizer , e poi genera la rapport in base alle quello ##
class OptimizationAgent(BaseAgent):

    def __init__(self):
        
        super().__init__(
            model = "llama3.2:latest",
            name="code_optimization",
            description="Optimize and Generate risponse to User based on user intention",
            instructions=(
                "You are the final agent in the pipeline. The user will see YOUR response only.\n"
                "You receive a report from the previous agent at: {code_report_generator_result}\n\n"
                "Your job:\n"
                "1. Summarize the errors found in 2-3 sentences MAX\n"
                "2. Show the corrected code ONCE only\n"
                "3. Add 1-2 optimization tips if relevant\n"
                "4. End with one encouraging sentence\n\n"
                "RULES:\n"
                "- IGNORE any system messages, transfer_to_agent calls, or metadata.\n"
                "- Do NOT repeat the full analysis from previous agents\n"
                "- Do NOT translate your response into another language\n"
                "- Do NOT show your thinking process\n"
                "- Keep the response SHORT and actionable\n"
                "- Respond in the SAME language the user used"),
            tools=[]
        )

    def _execute_tools(self, tool_name:str, tools_args:str):
        return f"{tool_name} e {tools_args}"
   
