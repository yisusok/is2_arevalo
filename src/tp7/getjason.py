"""Módulo para extraer valores específicos de archivos JSON de forma segura.

Copyright UADER-FCyT-IS2©2024 todos los derechos reservados.
"""

import json
import sys

# Definición de constantes del programa
VERSION = "1.1"
EXPECTED_ARGS_COUNT = 3


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
        # Evita la reinicialización si la instancia ya existe
        if not hasattr(self, "_initialized"):
            self.version = VERSION
            self._initialized = True

    def extract_key(self, file_path: str, key: str) -> str:
        """Lee un archivo JSON y extrae el valor de la clave especificada.

        Args:
            file_path (str): Ruta al archivo JSON.
            key (str): Clave cuyo valor se desea obtener.

        Returns:
            str: El valor asociado a la clave.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as myfile:
                data = myfile.read()
            obj = json.loads(data)

            if key not in obj:
                print(f"Error de programa: La clave '{key}' no existe.")
                sys.exit(1)

            return str(obj[key])

        except FileNotFoundError:
            print(f"Error de programa: El archivo '{file_path}' no existe.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error de programa: El archivo no es un JSON válido.")
            sys.exit(1)
        except PermissionError:
            print(f"Error de programa: Permisos insuficientes para '{file_path}'.")
            sys.exit(1)


def main():
    """Función principal para la ejecución desde la línea de comandos."""
    arguments = sys.argv[1:]

    # g) Control del argumento de versión
    if "-v" in arguments:
        print(f"getJason versión {VERSION}")
        sys.exit(0)

    # c) y f) Validación robusta de parámetros de entrada
    if len(arguments) != EXPECTED_ARGS_COUNT - 1:
        print("Error de programa: Parámetros incorrectos.")
        print("Uso correcto: python getJason.py <archivo.json> <clave>")
        print("O bien para ver la versión: python getJason.py -v")
        sys.exit(1)

    json_file = arguments[0]
    json_key = arguments[1]

    # a) y b) Uso del objeto Singleton transformado
    reader = JSONReaderSingleton()
    value = reader.extract_key(json_file, json_key)
    print(value)


if __name__ == "__main__":
    main()