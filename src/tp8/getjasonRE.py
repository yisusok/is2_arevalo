"""Módulo para gestionar pagos automáticos y extracción segura de claves JSON.

Aplica patrones de diseño: Singleton, Chain of Responsibility e Iterator.
Copyright UADER-FCyT-IS2©2026 todos los derechos reservados.
"""

import json
import sys
from typing import List, Optional

# Definición de constantes del programa
VERSION = "1.2"


class JSONReaderSingleton:
    """Clase Singleton para gestionar la lectura y extracción de datos JSON."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Garantiza la existencia de una única instancia de la clase."""
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Inicializa los atributos de la instancia de forma segura."""
        if not hasattr(self, "_initialized"):
            self.version = VERSION
            self._initialized = True

    @staticmethod
    def extract_key(file_path: str, key: str) -> str:
        """Lee un archivo JSON y extrae el valor de la clave especificada."""
        try:
            with open(file_path, "r", encoding="utf-8") as myfile:
                data = myfile.read()
            obj = json.loads(data)

            if key not in obj:
                print(f"Error: La clave '{key}' no existe.")
                sys.exit(1)

            return str(obj[key])

        except FileNotFoundError:
            print(f"Error: El archivo '{file_path}' no existe.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: El archivo no es un JSON válido.")
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permisos insuficientes para '{file_path}'.")
            sys.exit(1)


class Pago:
    """Representa una entidad de pago procesada por el sistema."""

    def __init__(self, numero_pedido: int, token: str, monto: float):
        self.numero_pedido = numero_pedido
        self.token = token
        self.monto = monto

    def __str__(self) -> str:
        return (f"Pedido: {self.numero_pedido} | "
                f"Banco (Token): {self.token} | "
                f"Monto: ${self.monto:.2f}")


class PagoIterator:
    """Iterador personalizado para recorrer cronológicamente los pagos."""

    def __init__(self, pagos: List[Pago]):
        self._pagos = pagos
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Pago:
        if self._index < len(self._pagos):
            resultado = self._pagos[self._index]
            self._index += 1
            return resultado
        raise StopIteration


class HistorialPagos:
    """Colección iterable que almacena el registro histórico de pagos."""

    def __init__(self):
        self._registro: List[Pago] = []

    def agregar_pago(self, pago: Pago):
        """Añade un pago de forma cronológica al historial."""
        self._registro.append(pago)

    def __iter__(self) -> PagoIterator:
        return PagoIterator(self._registro)


class AccountHandler:
    """Manejador base para el patrón Cadena de Responsabilidad con prevención de ciclos."""

    def __init__(self, token: str, saldo_inicial: float, file_path: str = "sitedata.json"):
        self.token = token
        self.saldo = saldo_inicial
        self.file_path = file_path
        self.next_handler: Optional['AccountHandler'] = None

        reader = JSONReaderSingleton()
        self.api_key = reader.extract_key(self.file_path, self.token)

    def set_next(self, handler: 'AccountHandler') -> 'AccountHandler':
        """Define el siguiente eslabón de la cadena."""
        self.next_handler = handler
        return handler

    def procesar_pago(self, numero_pedido: int, monto: float, 
                      historial: HistorialPagos, visitados: Optional[list] = None) -> bool:
        """Procesa el pago de forma balanceada controlando no caer en recursión infinita."""
        if visitados is None:
            visitados = []

        # Control de parada: si ya evaluamos esta cuenta en este intento de pago, salimos
        if self.token in visitados:
            return False

        # Si tiene saldo, se procesa inmediatamente
        if self.saldo >= monto:
            self.saldo -= monto
            nuevo_pago = Pago(numero_pedido, self.token, monto)
            historial.agregar_pago(nuevo_pago)
            print(f"[PROCESADO] {nuevo_pago} (Clave Aut.: {self.api_key[:8]}...)")
            return True

        # Si no tiene saldo, se registra que ya pasó por acá y delega al siguiente
        visitados.append(self.token)
        if self.next_handler:
            return self.next_handler.procesar_pago(numero_pedido, monto, historial, visitados)

        return False


def ejecutar_simulacion():
    """Configura el entorno y simula las transacciones automáticas sin desbordamiento."""
    print("--- Inicializando Sistema de Re-ingeniería de Pagos ---")
    historial = HistorialPagos()

    # Configuración de cuentas y saldos iniciales (Total sistema = $3000)
    cuenta1 = AccountHandler(token="token1", saldo_inicial=1000.0)
    cuenta2 = AccountHandler(token="token2", saldo_inicial=2000.0)

    # Conexión circular para balanceo alternado
    cuenta1.set_next(cuenta2)
    cuenta2.set_next(cuenta1)

    # 7 pedidos de $500 (Total requerido = $3500, debe fallar el último)
    pedidos_montos = [500.0] * 7  
    manejador_actual = cuenta1

    for idx, monto in enumerate(pedidos_montos, start=1):
        print(f"\nProcesando pedido N° {idx} por ${monto}...")
        
        # Pasamos un arreglo de visitados vacío para cada nueva transacción
        exito = manejador_actual.procesar_pago(idx, monto, historial, visitados=None)

        if exito:
            # Si se cobró con éxito, avanzamos el puntero para alternar la carga en el próximo turno
            manejador_actual = manejador_actual.next_handler
        else:
            print(f"[RECHAZADO] Pedido N° {idx}: Fondos insuficientes en todo el sistema.")

    # Listado cronológico usando el patrón Iterator
    print("\n" + "="*50)
    print("LISTADO CRONOLÓGICO DE PAGOS EFECTUADOS (Iterator)")
    print("="*50)
    for pago in historial:
        print(pago)

    print("\nSaldos finales:")
    print(f"Cuenta 1 ({cuenta1.token}): ${cuenta1.saldo:.2f}")
    print(f"Cuenta 2 ({cuenta2.token}): ${cuenta2.saldo:.2f}")

def main():
    """Función principal para la ejecución desde la línea de comandos."""
    arguments = sys.argv[1:]

    if "-v" in arguments:
        print(f"getJason versión {VERSION}")
        sys.exit(0)

    # Si no se pasan argumentos, corre la simulación automática solicitada
    if not arguments:
        ejecutar_simulacion()
    else:
        # Mantiene compatibilidad hacia atrás con la versión 1.1
        if len(arguments) != 2:
            print("Uso correcto: python getJason.py <archivo.json> <clave>")
            print("O ejecute sin parámetros para iniciar la simulación de pagos.")
            sys.exit(1)
        reader = JSONReaderSingleton()
        print(reader.extract_key(arguments[0], arguments[1]))


if __name__ == "__main__":
    main()