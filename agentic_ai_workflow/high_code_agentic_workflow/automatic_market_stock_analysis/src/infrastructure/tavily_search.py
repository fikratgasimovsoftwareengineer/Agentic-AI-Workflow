from src.interfaces.i_tavily_search import ITavilySearch
from src.domain.search import SearchResults
from dataclasses import dataclass

# To install: pip install tavily-python
from tavily import TavilyClient
from src.config.app_settings import AppSettings
from src.domain.search import SearchResults

@dataclass
class TavilySearch(ITavilySearch):
    
    
    def __init__(self, settings:AppSettings):
        self._client = TavilyClient(settings.tavily_api)
    

        
    def search_invoke(self, prompt:str, max_results=2)->list[SearchResults]:
        results_search =  self._client.search(
            query= prompt,
            max_results=max_results
        )
    
        return [
            SearchResults(
                title=r['title'],
                url = r['url'],
                content = r['content']
            )
            for r in results_search.get("results", [])
        ]