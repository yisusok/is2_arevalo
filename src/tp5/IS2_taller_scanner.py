import os

#*--------------------------------------------------------------------
#* Ejemplo de design pattern de tipo state (Modificado para memorias)
#*--------------------------------------------------------------------
"""State class: Base State class"""
class State:

    def scan(self):
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print("Sintonizando... Estación {} {}".format(self.stations[self.pos], self.name))

class AmState(State):

    def __init__(self, radio):
        self.radio = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos = 0
        self.name = "AM"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate

"""Separate class for FM state"""
class FmState(State):

    def __init__(self, radio):
        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos = 0
        self.name = "FM"

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.state = self.radio.amstate

class Radio:

    def __init__(self):
        self.fmstate = FmState(self)
        self.amstate = AmState(self)

        self.state = self.fmstate

        self.memories = {
            "M1": ("950", "AM"),
            "M2": ("94.3", "FM"),
            "M3": ("1310", "AM"),
            "M4": ("101.5", "FM")
        }

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()
        
        print("--- Barrido de Memorias sintonizadas ---")
        for label, (freq, band) in self.memories.items():
            print("Memoria {} -> {} {}".format(label, freq, band))
        print("----------------------------------------")


if __name__ == "__main__":
    os.system("clear")
    print("\nCrea un objeto radio y almacena las siguientes acciones")
    radio = Radio()
    actions = [radio.scan] * 3 + [radio.toggle_amfm] + [radio.scan] * 3
    actions *= 2

    print("Recorre las acciones ejecutando la acción, el objeto cambia la interfaz según el estado")
    for action in actions:
        action()