from abc import ABC, abstractmethod

class Componente(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def mostrar(self, nivel: int = 0):
        pass

class Pieza(Componente):
    def mostrar(self, nivel: int = 0):
        print("  " * nivel + f"- Pieza: {self.nombre}")

class SubConjunto(Componente):
    def __init__(self, nombre: str):
        super().__init__(nombre)
        self._hijos = []

    def agregar(self, componente: Componente):
        self._hijos.append(componente)

    def mostrar(self, nivel: int = 0):
        print("  " * nivel + f"+ Sub-conjunto: {self.nombre}")
        for hijo in self._hijos:
            hijo.mostrar(nivel + 1)

if __name__ == "__main__":
    producto_principal = SubConjunto("Producto Principal")

    for i in range(1, 4):
        sub_combo = SubConjunto(f"SC-{i}")
        for j in range(1, 5):
            sub_combo.agregar(Pieza(f"Pz-{i}.{j}"))
        producto_principal.agregar(sub_combo)

    print("--- Configuración Estándar Inicial ---")
    producto_principal.mostrar()

    sub_opcional = SubConjunto("SC-Opcional Extra")
    for j in range(1, 5):
        sub_opcional.agregar(Pieza(f"Pz-Opt.{j}"))
    
    producto_principal.agregar(sub_opcional)

    print("\n--- Configuración con Sub-conjunto Opcional Añadido ---")
    producto_principal.mostrar()