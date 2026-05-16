from abc import ABC, abstractmethod

class ComponenteNumero(ABC):
    @abstractmethod
    def obtener_valor(self) -> float:
        pass

class Numero(ComponenteNumero):
    def __init__(self, valor: float):
        self._valor = valor

    def obtener_valor(self) -> float:
        return self._valor

class OperacionDecorator(ComponenteNumero):
    def __init__(self, componente: ComponenteNumero):
        self._componente = componente

class SumarDos(OperacionDecorator):
    def obtener_valor(self) -> float:
        return self._componente.obtener_valor() + 2

class MultiplicarPorDos(OperacionDecorator):
    def obtener_valor(self) -> float:
        return self._componente.obtener_valor() * 2

class DividirPorTres(OperacionDecorator):
    def obtener_valor(self) -> float:
        return self._componente.obtener_valor() / 3

if __name__ == "__main__":
    numero_base = Numero(10)
    print(f"Valor base inicial: {numero_base.obtener_valor()}") # 10

    numero_decorado = DividirPorTres(
        MultiplicarPorDos(
            SumarDos(numero_base)
        )
    )

    print(f"Valor con operaciones anidadas: {numero_decorado.obtener_valor()}") # 8.0