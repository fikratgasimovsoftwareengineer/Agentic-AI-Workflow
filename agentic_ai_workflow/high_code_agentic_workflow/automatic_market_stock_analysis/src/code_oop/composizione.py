
class Motore:
    def __init__(self, cilindrata):
        self.cilindrata = cilindrata
        self.acceso = False

    def avvia(self):
        self.acceso = True
        print("Vroooom! 🔥")

class Auto:
    def __init__(self, modello):
        self.modello = modello
        self.motore = Motore(1600)   # ← creato DENTRO (composizione!)
                                     #   nessuno lo passa da fuori

    def parti(self):
        self.motore.avvia()
        print(f"{self.modello} è partita! 🚗")


auto = Auto("Fiat Panda")
auto.parti()
# Vroooom! 🔥
# Fiat Panda è partita! 🚗


# AGGREGAZIONE → il figlio ARRIVA da fuori
class Universita:
    def __init__(self, nome, rettore):      # rettore passato dall'esterno
        self.nome = nome
        self.rettore = rettore              # esiste anche senza l'università

class Docente:
    def __init__(self, nome):
        self.nome = nome

d = Docente("Prof. Verdi")
uni = Universita("Politecnico", d)          # il Docente resta mio anche se l'uni chiude ✅

# COMPOSIZIONE → il figlio NASCE dentro
class Ufficio:
    def __init__(self, numero):
        self.numero = numero
        self.scrivania = Scrivania()        # creata QUI: muore con l'ufficio

class Scrivania:
    pass