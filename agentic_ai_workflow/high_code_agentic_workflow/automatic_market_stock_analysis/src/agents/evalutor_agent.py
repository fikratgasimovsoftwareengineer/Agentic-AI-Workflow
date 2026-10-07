from src.domain.models import RouterState
from src.interfaces.i_evaluator import IEvaluator
from src.domain.models import Feedback
    

class EvaluatorAgent:
    
    name="evaluator_agent"
    
    def __init__(self, validator:IEvaluator):
        self._validator=validator
    
        
    def __call__(self, state:RouterState):
        
           
        prompt = (
            "Sei un revisore rigoroso. Valuta la risposta rispetto alla domanda.\n"
            f"DOMANDA: ```{state['query']}```\n"
            f"RISPOSTA DA VALUTARE: ```{state['final_answer']}```\n"   # ← LEI deve esserci!
            "Criteri: 1) risponde alla domanda? 2) cita le fonti? 3) è coerente?\n"
            "Dai 'approved' solo se TUTTI i criteri sono soddisfatti."
        )
        

        validate_output = self._validator.invoke_evaluator(prompt, Feedback)
        
        return {"feedback": validate_output.feedback,
                "needs_revision":state.get('revision_count', 0) + 1,
                "grade": validate_output.grade
                }
    
        