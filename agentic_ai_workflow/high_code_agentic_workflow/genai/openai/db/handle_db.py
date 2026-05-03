import sqlite3
import random
import sys
import pathlib

env_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(env_path))
from db.create_db import DatabaseManager,ToyRepository
from dataclasses import dataclass, field

@dataclass
class HandleDB:
    
    
    name_db:str = 'toy_database.db'

    
    db:DatabaseManager = field(init=False)
    repo:ToyRepository = field(init=False)    
        
    
    def __post_init__(self):
        # open connection to db
        self.db = DatabaseManager(self.name_db)
        
        # creare tabella se non esiste
        self.db.create_table()
        
        # seed table :
        self.db.seed_if_empty()
        
        ### pass il ogetto della database manager al repository
        self.repo = ToyRepository(self.db)
        
    
    def close(self):
        self.db.close()
        
    ### call list
    
    def list_all_toys(self):
        return self.repo.list_toys()
    
    def find_toys_by_prefix(self, prefix:str):
        return self.repo.find_by_prefix(prefix)
    
    def find_toys_by_range(self,low_price, high_price):
        return self.repo.find_toys_in_price_range(low_price=low_price, high_price=high_price)
    
    def sort_random_toys(self, count:int):
        return self.repo.get_random_toys(count=count)
    
    def sort_most_expensive_toy(self, count:int):
        return self.repo.get_most_expensive_toy(count=count)
    
    def sort_cheapest_toy(self, count:int):
        return self.repo.get_cheapest_toy(count=count)
    
    
def main():
    handle_db = HandleDB()
    
    try:
        print(handle_db.list_all_toys())
        
        print(handle_db.find_toys_by_prefix('Toy 1'))
        
        print(handle_db.find_toys_by_range(10, 20))
        
        print(handle_db.sort_random_toys(3))
        
        print(handle_db.sort_most_expensive_toy(2))
        
        print(handle_db.sort_cheapest_toy(2))
        
    finally:
        handle_db.close()
        
if __name__ == "__main__":
    main()