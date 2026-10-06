""" from src.interfaces.i_tools import (
    ISearchEconomics)
from src.domain.models import AgentInput


class SearchEconomics(ISearchEconomics):

    def get_economy_new(self, query:str)->str:
          return f"[economics] Notizie per: {query}"    
    

def main():
    tool = SearchEconomics()
    risultato = tool.get_economy_new("tell me about economics")
    print(risultato)

if __name__ == "__main__":
    main()
        
 """