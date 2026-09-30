class Animale:
    
    def __init__(self, nome, legs):
        self.nome = nome
        self.legs = legs
        self.eyes = 2
        
        
    def run_observe(self):
        return f"legs"+{self.legs}, "eyes"+{self.eyes}
    
    
    
class Gatto(Animale):
  
    def __init__(self, nome):
        super().__init__(nome, legs=4)

    def run_observe(self):
        return f"{self.nome} : {self.legs}" 
    
class Cane(Animale):
    

    def __init__(self, nome):
        super().__init__(nome,legs=4)
    
        
    def run_observe(self):
        return f"{self.nome}:{self.legs}"
    
def main():

    gatto = Gatto("irish cat")
    cane = Cane("dog")
    print(gatto.run_observe())
    print(cane.run_observe())
    
if __name__ == "__main__":
    main()