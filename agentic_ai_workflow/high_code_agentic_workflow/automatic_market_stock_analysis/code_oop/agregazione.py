class Giocatore:
    
    def __init__(self, name):
        self.name = name
        
        
class Squadra:
    def __init__(self, name):
        self.name = name    
        self.giocatori = []
        
    def setGiocatori(self, giocatori:Giocatore): ## aggregazione
        self.giocatori.append(giocatori.name)
    
    def getGiocatori(self):
        return self.giocatori
    
def main():
    fikrat = Giocatore("Fikrat")
    hikmat = Giocatore("Hikmat")

    squadra = Squadra("Squadra Principale")
    squadra.setGiocatori(fikrat)
    squadra.setGiocatori(hikmat)

    print(squadra.getGiocatori())
    
if __name__ == "__main__":
    main()