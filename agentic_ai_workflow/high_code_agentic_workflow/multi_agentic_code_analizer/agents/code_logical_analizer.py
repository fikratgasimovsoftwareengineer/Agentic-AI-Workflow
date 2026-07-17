

from agents.base_agent import BaseAgent



### CODE LOGICAL ANALYSIZE ###
class CodeLogicAnalyzerAgent(BaseAgent):

    def __init__(self):
        
        super().__init__(
            model = "qwen3.5:9b",
            name="code_logic_analizer",
            description="Analze given code and find out possible logical errors",
            instructions=["Your task is to analyze the logic of the given code "
                "and identify any logical errors or flaws in reasoning.\n"
                "Provide the logical errors found in clear bullet points.\n"
                "If no logical errors are found, state that explicitly."],
            tools=[]
        )

    def _execute_tools(self, tool_name:str, tools_args:str):
        return f"{tool_name} e {tools_args}"
    
    

"""     @property
    def system_prompt(self) -> str:
        return (
            "Sei un agente specializzato in analisi, review e spiegazione del codice. "
            "Puoi lavorare con Python, JavaScript, TypeScript, Java, C++, Bash e altri linguaggi. "
            "Per ogni pezzo di codice che analizzi: "
            "1) Spiega cosa fa il codice ad alto livello "
            "2) Identifica eventuali bug, vulne rabilità o code smell "
            "3) Suggerisci miglioramenti concreti "
            "4) Valuta la qualità complessiva (leggibilità, manutenibilità, performance). "
            "Usa il tool 'analyze_code_structure' per ottenere metriche strutturali prima di rispondere."
        )

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "analyze_code_structure",
                    "description": (
                        "Analizza la struttura statica di un frammento di codice: "
                        "conta linee, funzioni/metodi, classi, commenti e stima "
                        "la complessità ciclomatica approssimativa."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Il codice sorgente da analizzare.",
                            },
                            "language": {
                                "type": "string",
                                "description": "Linguaggio di programmazione del codice.",
                                "enum": ["python", "javascript", "typescript", "java", "cpp", "bash", "other"],
                            },
                        },
                        "required": ["code", "language"],
                    },
                },
            }
        ]

    def _execute_tool(self, tool_name: str, tool_args: dict) -> str:
        if tool_name == "analyze_code_structure":
            return self._analyze_code_structure(
                tool_args.get("code", ""),
                tool_args.get("language", "other"),
            )
        return f"Tool '{tool_name}' non riconosciuto."
    """