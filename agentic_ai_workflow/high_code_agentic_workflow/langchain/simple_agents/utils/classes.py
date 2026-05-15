from pydantic import BaseModel, Field
from enum import Enum



# -------------------------------
# Agente 1: Calcolatore + Convertitore Valuta
# -------------------------------
### Operation Class
class Operation(str, Enum):
    addition:str = "addition"
    substraction:str = "subtraction"
    multiplication:str = "multiplication"
    division:str = "division"
    
class CalculatorInput(BaseModel):
    a:float = Field(description="First Number")
    b:float = Field(description="Second Number")
    operation:Operation = Field(description="The operation to perform. Must be one of: addition, subtraction, multiplication, division.")    
    
    

class CurrencyConverterInput(BaseModel):
    amount:float = Field(description="The amount In EURO.")
    rate:float = Field(description="Exchange rate to target currency")
    

    