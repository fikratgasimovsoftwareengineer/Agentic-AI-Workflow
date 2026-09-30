from src.domain.models import AgentInput

def test_agent_input(agent_input:AgentInput)->str:
    
    return f"Elaboro : {agent_input['query']}"

input_test:AgentInput = {"query":"come sta il mercato EV?"}

print(input_test)