import json
import time
import mlflow
from config import MLFLOW_EXPERIMENT_NAME,MLFLOW_TRACKING_URI


"""_summary_ : tutoraggio :[tutoraggio mlflow](https://mlflow.org/docs/latest/ml/tracking/tracking-api/)
"""


def init_mlflow():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

class AgentRunTracker:
    
    """
    Context manager per tracciare una singola elaborazione di un agente.
 
    Uso tipico:
        with AgentRunTracker(agent_name="math", query="2+2") as tracker:
            # ... logica agente ...
            tracker.log_confidence(0.95)
            tracker.log_reflection(rounds=1, corrected=False)
            tracker.log_tool_call("calculate")
            tracker.log_reasoning_chain(chain)
            tracker.log_final_answer(answer)
    """
    
    def __init__(self,agent_name:str, query:str, model:str):
        self.agent_name = agent_name
        self.query = query
        self.model = model
        
        self._run = None
        self._start_ts = None
        
        
    # The __enter__ method is part of Python's context manager protocol. It defines what happens at the start of a with statement block.
    def __enter__(self):
        self._run = mlflow.start_run(run_name=f"{self.agent_name}__run")
        self._start_ts = time.time()
        
        #Data Logging
        mlflow.log_param("agent_name", self.agent_name)
        mlflow.log_param("model", self.model)
        mlflow.log_param("query", self.query[:500]) #trocnare
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # --- Metric: latenza totale calcolata in uscita ---
        latency_ms = (time.time() - self._start_ts) * 1000
        mlflow.log_metric("latency_ms", round(latency_ms, 2))
 
        if exc_type is not None:
            mlflow.set_tag("error", str(exc_val)[:500])
 
        mlflow.end_run()
        return False  # non sopprime eccezioni
        
    def log_confidence(self, score:float):
        mlflow.log_metric("confidence_score", round(score, 4))
        
    def log_reflection(self, rounds:int, corrected:bool):
        mlflow.log_metric("reflection_rounds", rounds)
        mlflow.set_tag("self_corrected", str(corrected))
        
    def log_tool_call(self, tool_name:str):
        mlflow.set_tag("tool_used", "True")
        mlflow.set_tag("tool_name", tool_name)
        
    def log_reasoning_chain(self, chain:list[dict]):
        
        """
        Salva l'intero reasoning chain come artifact JSON.
        Questo è il log più ricco: contiene ogni step di pensiero dell'agente.
 
        chain esempio:
            [
              {"step": "initial_response", "content": "..."},
              {"step": "self_reflection",  "content": "..."},
              {"step": "final_answer",     "content": "..."}
            ]
        """
        artifact_path = f"/tmp/{self.agent_name}_reasoning_chain.json"
        with open(artifact_path, 'w', encoding="utf-8") as f:
            json.dump({
                "agent":self.agent_name,
                "query":self.query,
                "chain":chain
            },
            
            f,
            ensure_ascii=False,
            indent=2
            )
        mlflow.log_artifact(artifact_path, artifact_path=self.agent_name)


    def log_final_answer(self, answer: str):
        """
        Logga la risposta finale come tag (troncata a 500 chars).
        La risposta completa è nell'artifact del reasoning chain.
        """
        mlflow.set_tag("final_answer_preview", answer[:500])