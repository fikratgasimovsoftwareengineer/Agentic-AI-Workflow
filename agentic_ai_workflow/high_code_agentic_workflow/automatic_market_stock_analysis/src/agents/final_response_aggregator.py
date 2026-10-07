from src.domain.models import RouterState, FinalReport
from src.interfaces.i_ollama import ILLMRouter

class FinalResponseAggre:
    name = "final_response_aggregator"
    
    def __init__(self, router:ILLMRouter):
        self._router=router
        
    def __call__(self, state:RouterState):
       

        materiali = "\n\n".join(res['output'] for res in state['results'])
        
        feedback_section_prompt =  "" 
        if state.get("feedback") and state.get("grade") != "approved":
            feedback_section_prompt = (
                f"Last response ```{state['final_answer']}``` is not approved by validator\n"
                f"feedback: ```{state['feedback']}```"
                f"query: ```{state['query']}```"
                "Correct your answer based on the question and provided the feedback, "
            )
            
        prompt = (
                    "il tuo ruolo e` di unire le risultati avvenuti in base alle domanda seguente\n"
                    f"DOMANDA: ```{state['query']}```\n"
                    f"RISULTATI DELLA RICERCA: ```{materiali}```\n"
                    f"{feedback_section_prompt}"
                    "Scrivi una risposta unificata, chiara e strutturata, "
                    "citando le fonti (URL) alla fine."
                )
        
        report = self._router.invoke_structured(prompt, FinalReport)
        return {"final_answer":report.final_answer}
        