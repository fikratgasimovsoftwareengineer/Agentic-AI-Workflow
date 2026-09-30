from langchain.tools import tool
from abc import ABC, abstractmethod

class ISearchWikipedia(ABC):

    @abstractmethod
    def search_wikipedia(self, query:str):
        pass
    
class ISearchSport(ABC):

    @abstractmethod
    def get_sport_news(self, tipo_di_sport:str):
        pass
    
class ISearchTechnology(ABC):

    @abstractmethod
    def get_technology_news(self, query:str):
        pass

class ISearchEconomics(ABC):

    @abstractmethod
    def get_economy_new(self, query:str):
        pass
    
class ISearchScience(ABC):

    @abstractmethod
    def get_scientific_research(self, query:str):
        pass
    
class ISearchJobs(ABC):

    @abstractmethod
    def get_jobs(self, query:str):
        pass
    
     