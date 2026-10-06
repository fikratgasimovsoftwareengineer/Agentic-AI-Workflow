from abc import ABC, abstractmethod
from src.domain.search import SearchResults
class ITavilySearch(ABC):
    
    @abstractmethod
    def search_invoke(self, prompt:str, max_results:int)->list[SearchResults]:
        """Cerca sul web e restituisce risultati tipizzati."""
        pass