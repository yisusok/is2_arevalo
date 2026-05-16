from abc import ABC, abstractmethod

class TrenLaminador(ABC):
    @abstractmethod
    def producir(self, espesor: float, ancho: float) -> str:
        pass

class TrenCincoMetros(TrenLaminador):
    def producir(self, espesor: float, ancho: float) -> str:
        return f"Plancha de {espesor}\" x {ancho}m con largo de 5 metros."

class TrenDiezMetros(TrenLaminador):
    def producir(self, espesor: float, ancho: float) -> str:
        return f"Plancha de {espesor}\" x {ancho}m con largo de 10 metros."

class LaminaAcero:
    def __init__(self, espesor: float, ancho: float, tren: TrenLaminador):
        self.espesor = espesor
        self.ancho = ancho
        self.tren = tren 

    def set_tren(self, tren: TrenLaminador):
        self.tren = tren

    def enviar_a_producir(self):
        resultado = self.tren.producir(self.espesor, self.ancho)
        print(f"Fabricando Lámina Genérica -> {resultado}")

if __name__ == "__main__":
    tren_5m = TrenCincoMetros()
    tren_10m = TrenDiezMetros()

    lamina = LaminaAcero(espesor=0.5, ancho=1.5, tren=tren_5m)
    
    print("Producción Inicial:")
    lamina.enviar_a_producir()

    print("\nCambiando de línea de producción:")
    lamina.set_tren(tren_10m)
    lamina.enviar_a_producir()