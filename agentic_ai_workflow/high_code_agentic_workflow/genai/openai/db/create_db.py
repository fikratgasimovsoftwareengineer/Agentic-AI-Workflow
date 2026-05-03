import sqlite3
import random
from dataclasses import dataclass, field


@dataclass
class DatabaseManager:
    
    
    name_db:str
    conn:sqlite3.Connection = field(init=False)
  

    def __post_init__(self):
        self.conn = sqlite3.connect(self.name_db)
        self.cursor = self.conn.cursor()
    
    def close(self):
        if self.conn:
            self.conn.close()
            
            
    def create_table(self):
        
        self.cursor.execute('''                 
                            CREATE TABLE IF NOT EXISTS toys 
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                price REAL
                            )''')
        
        self.conn.commit()
        
        print(f"Database '{self.name_db}' and table 'toys' created successfully with 100 toy entries.")
            
        
    
        
    def seed_if_empty(self):
        
        prefixes = ['Magic', 'Super', 'Ultra', 'Mega', 'Power', 'Wonder']
        suffixes = ['Bear', 'Doll', 'Car', 'Robot', 'Puzzle', 'Game']
        
        for i in range(1, 101):
            toy_name = random.choice(prefixes) + ' ' + random.choice(suffixes)
            toy_price = round(random.uniform(5, 20), 2) #prezzo causale tra 5 e 20
            self.cursor.execute(
                
                'INSERT INTO toys (name, price) VALUES (?,?)', (toy_name, toy_price)
            )
            
    
        
        ### subito dopi, execute commnad per esaminare il contenuto del db
        self.cursor.execute('SELECT * from toys')
        
        print('Toys in database: ')
        
        for row in self.cursor.fetchall():
            print(row)
            
        #self.conn.close() 
        
    def connect_db(self):
        return sqlite3.connect(self.name_db)
       

@dataclass  
class ToyRepository:
    
    db:DatabaseManager
    
    
    def list_toys(self):
        return self.db.conn.execute('SELECT * FROM toys').fetchall()
        
        
    def find_by_prefix(self, prefix:str):
        query = 'SELECT * FROM toys WHERE name LIKE ?'
        cursor = self.db.cursor.execute(query, (prefix + '%',))
     
        return cursor.fetchall()    
    
    # Find toys in a price range
    def find_toys_in_price_range(self, low_price, high_price):
      
        query = 'SELECT * FROM toys WHERE price BETWEEN ? AND ?'
        cursor = self.db.conn.execute(query, (low_price, high_price))
        return cursor.fetchall()
    

    def get_random_toys(self, count:int=5):

        cursor = self.db.conn.execute('SELECT * FROM toys')
        all_toys = cursor.fetchall()
        return random.sample(all_toys, min(count, len(all_toys)))
        

    def get_most_expensive_toy(self, count=1):
      
            cursor = self.db.conn.execute(f'SELECT * FROM toys ORDER BY price DESC LIMIT {count}')
            return cursor.fetchone()
        
    # Function to get the cheapest toy
    def get_cheapest_toy(self, count:int=1):
       
            cursor = self.db.conn.execute(f'SELECT * FROM toys ORDER BY price ASC LIMIT {count}')
            return cursor.fetchone()

""" def main():
    db_manager = DatabaseManager()
    db_manager.create_table()
    
    
if __name__ =="__main__":
    main() """