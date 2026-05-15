from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from enum import Enum

from utils.classes import Operation, CalculatorInput, CurrencyConverterInput

llm = ChatOllama(
    model="llama3.2",
    temperature=0.0

)
##################################################33
############## CalculatorInput TOOL ##############
@tool(args_schema=CalculatorInput)
def precise_calculator(a:int, b:int, operation:Operation)->str:
    """
    A precise calculator that can perform complex calculations and provide accurate results. 
    It can handle a wide range of mathematical operations, including basic arithmetic, algebra, calculus, and more. 
    The precise calculator is designed to provide quick and reliable answers to mathematical queries, making it an essential tool for students, professionals, and anyone in need of accurate calculations.
    """
    if operation == Operation.addition:
        return str(a+b)
    elif operation == Operation.substraction:
        return str(a-b)
    elif operation == Operation.multiplication:
        return str(a*b)
    elif operation == Operation.division:
        return str(a/b) if b != 0 else "Error: Division by zero is not allowed."
    else:
        return "Operation not supported"

@tool(args_schema=CurrencyConverterInput)
def convert_currency(amount:float, rate:float)->str:
    """
    Convert an amount from EURO TO another currency given the exchange rate

    Args:
        amount (float): the amount in EURO to be converted
        rate (float): exchange rate to target currency

    Returns:
        str: the converted amount in the target curreny as a string
    """
    return str(round(amount*rate, 2))
    


##############################################################################
############## AGENT 1 CREATION ################################################

base_agent = create_agent(llm, tools=[precise_calculator, convert_currency], system_prompt=
                    "You are precise calculator and currency converter agent. Use tools for every arithmetic calculation and currency conversion."
                    "Output ONLY the final number, no extra cost" 
                    )

##################################################################################333
################ AGENT 2 SPIEGATORE ################################################
agent_explanair = create_agent(
    llm,
    tools=[],
    system_prompt = "You are a friendly financial assistant"
    "given a numerical result, explain it   in human readable form, providing context and insights to help the user understand the significance of the result. "
    "add context, like 'that means you will receive ... dollars' "
    "keep the tone warm and professional"
)
""" if __name__ == "__main__":
     
    print("Match Agent starting...")
    user_query  = "I have 150 euros and today 1 EURO = 1.17 dollars. How much dollars i will get if i convert all my euros to dollars?"
    # Invoke the agent passing the initial user message
    result = base_agent.invoke({"messages": [("user", user_query)]})
    
    print("Agent response:")
    technical_conversation = result["messages"][-1].content.strip()
    print(technical_conversation)
    
    
    
    print("\n\nNow let's ask the explainer agent to explain the result in human readable form")
    final_answer = agent_explanair.invoke({"messages":[("user", technical_conversation)]})
    
    print("Explainer Agent response:",final_answer["messages"][-1].content.strip())
    print("✅ Risposta finale:")
    print(final_answer["messages"][-1].content.strip())
    
"""