from langchain.tools import tool
from abc import ABC, abstractmethod
["technology", "economics", "jobs", "sport", "scientific_research"]

class SearchWikipedia(ABC):
    @tool
    @abstractmethod
    def search_wikipedia(self, query:str):
        """Search wikipedia"""
        pass
    
class SearchSport(ABC):
    @tool
    @abstractmethod
    def get_sport_news(self, tipo_di_sport:str):
        """get sport information"""
        pass
    
class SearchTechnology(ABC):
    @tool
    @abstractmethod
    def get_technology_news(self, query:str):
        """get tech news"""
        pass

class SearchEconomics(ABC):
    @tool
    @abstractmethod
    def get_economy_new(self, query:str):
        """get economoy news"""
        pass
    
class SearchScience(ABC):
    @tool
    @abstractmethod
    def get_scientific_research(self, query:str):
        """scientific research"""
        pass
    
class SearchJobs(ABC):
    @tool
    @abstractmethod
    def get_jobs(self, query:str):
        """job search"""
        pass
    
    