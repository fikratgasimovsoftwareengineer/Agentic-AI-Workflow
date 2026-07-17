# =============================================================
# agents/base_agent.py
# =============================================================

from interfaces.i_base_agent import IBaseAgent

#from tracking.ml_flow_tracker import AgentRunTracker


class BaseAgent(IBaseAgent):
    """
    Classe base astratta per tutti gli agenti di ReasonerHub.

    Flusso per ogni query:
        1. Chiamata iniziale al modello  →  risposta + confidence
        2. Se tool call rilevata         →  esegui tool → reinvia
        3. Se confidence < soglia        →  loop self-reflection
        4. Log tutto su MLflow
    """

    def __init__(self, model, name, instructions, description, tools):
        self._model  = model
        self._name = name
        self._instructions:list[str] = instructions
        self._description = description
        self._tools = tools


    ### Property ###
    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, agent_name:str)->None:
        if not agent_name:
            raise ValueError("Agent name is not setted")
        self._name = agent_name
        

    #### model ####
    @property
    def model(self) -> str:
        return self._model
    @model.setter
    def model(self, llm_agent:str)->None:
        if not llm_agent:
            raise ValueError("LLM Agent is not setted")
        self._model = llm_agent
        
    #### INTRUCTTIONS ###
    @property
    def instructions(self)->str:
        return self._instructions
    @instructions.setter
    def instructions(self, instructions:list[str])->None:
        if not instructions:
            raise ValueError("Instructions is not setted")
        self.instructions = instructions
        
        
        
    @property
    def description(self)->str:
        return self._description
    @description.setter
    def description(self, description)->None:
        if not description:
            raise ValueError("Il Modello ha bisogno di descrizione")
        
        self._description = description
        

    @property
    def tools(self) -> list:
        return self._tools                         
    @tools.setter
    def tools(self, list_of_tools:list):
        if not isinstance(list_of_tools, list):
            raise TypeError("Tools should be List type")
        self._tools = list_of_tools
        
        return self._tools


    
    
    
    
    """ 
    # ── Entry point pubblico ───────────────────────────────────

    def run(self, query: str) -> dict:
        with AgentRunTracker(
            agent_name=self.name,
            query=query,
            model=self.model
        ) as tracker:
            reasoning_chain = []
            result = self._run_with_reflection(query, reasoning_chain, tracker)
            tracker.log_reasoning_chain(reasoning_chain)
            tracker.log_final_answer(result["answer"])
            return result

    # ── Loop self-reflection ───────────────────────────────────

    def _run_with_reflection(self, query, reasoning_chain, tracker) -> dict:

        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user",   "content": query},
        ]

        reflection_rounds = 0
        self_corrected    = False
        tool_called       = None

        # Step 1 — risposta iniziale
        raw, tool_called = self._call_model(messages)
        answer, confidence = self._parse_response(raw)
        reasoning_chain.append({
            "step": "initial_response", "content": raw, "confidence": confidence
        })

        # Step 2 — tool call
        if tool_called:
            tool_result = self._execute_tool(tool_called["name"], tool_called["args"])
            tracker.log_tool_call(tool_called["name"])
            reasoning_chain.append({
                "step": "tool_call", "tool": tool_called["name"],
                "args": tool_called["args"], "result": tool_result,
            })
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "tool",      "content": tool_result})
            raw, _ = self._call_model(messages)
            answer, confidence = self._parse_response(raw)
            reasoning_chain.append({
                "step": "post_tool_response", "content": raw, "confidence": confidence
            })

        # Step 3 — self-reflection loop
        while confidence < CONFIDENCE_THRESHOLD and reflection_rounds < MAX_REFLECTION_ROUNDS:
            reflection_rounds += 1
            prev_answer = answer

            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": (
                f"Il tuo confidence score era {confidence:.2f}, "
                f"sotto la soglia {CONFIDENCE_THRESHOLD}. "
                f"Rifletti criticamente e rispondi con più accuratezza."
            )})

            raw, _ = self._call_model(messages)
            answer, confidence = self._parse_response(raw)

            if answer.strip() != prev_answer.strip():
                self_corrected = True

            reasoning_chain.append({
                "step": f"self_reflection_round_{reflection_rounds}",
                "content": raw, "confidence": confidence,
                "self_corrected": self_corrected,
            })

        tracker.log_confidence(confidence)
        tracker.log_reflection(rounds=reflection_rounds, corrected=self_corrected)

        return {
            "answer":            answer,
            "confidence":        confidence,
            "reflection_rounds": reflection_rounds,
            "self_corrected":    self_corrected,
            "tool_called":       tool_called["name"] if tool_called else None,
        }

    # ── Helpers ────────────────────────────────────────────────

    def _build_system_prompt(self) -> str:
        return self.system_prompt + """
    """
---
ISTRUZIONE OBBLIGATORIA:
Alla fine di ogni risposta aggiungi SEMPRE questa riga:
CONFIDENCE: <numero tra 0.0 e 1.0>

Esempi:
CONFIDENCE: 0.95   ← molto sicuro
CONFIDENCE: 0.60   ← incerto
CONFIDENCE: 0.30   ← molto incerto

NON omettere mai questa riga.
"""

    """ def _call_model(self, messages: list[dict]) -> tuple[str, dict | None]:
        kwargs = {"model": self.model, "messages": messages}
        if self.tools:
            kwargs["tools"] = self.tools

        response = self.client.chat(**kwargs)
        message  = response.message

        if hasattr(message, "tool_calls") and message.tool_calls:
            tc = message.tool_calls[0]
            return message.content or "", {
                "name": tc.function.name,
                "args": dict(tc.function.arguments),
            }
        return message.content or "", None

    def _parse_response(self, raw: str) -> tuple[str, float]:
        confidence = 0.5
        answer     = raw

        match = re.search(r"CONFIDENCE:\s*([\d.]+)", raw, re.IGNORECASE)
        if match:
            try:
                confidence = float(match.group(1))
                confidence = max(0.0, min(1.0, confidence))
            except ValueError:
                pass
            answer = re.sub(r"\nCONFIDENCE:\s*[\d.]+", "", raw).strip()

        return answer, confidence """