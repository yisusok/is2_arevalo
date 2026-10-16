#!/usr/bin/env python3
"""Módulo de conversión de archivos JSON a formato CSV con estrategia de filtro.

Este programa forma parte del TP11 de Ingeniería de Software II (FCyT UADER).
Permite la conversión de datos JSON a formato CSV recibiendo datos desde
archivos o flujos estándar (stdin/stdout), soportando delimitadores configurables
y manejo robusto de excepciones de entrada/salida y decodificación.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from typing import Any, Sequence, TextIO

__version__ = "1.0.0"


def obtener_version() -> str:
    """Devuelve la versión actual del módulo.

    Returns:
        Cadena con el número de versión semántica.
    """
    return __version__


def aplanar_valor(valor: Any) -> Any:
    """Normaliza un valor para su correcta escritura en formato CSV.

    Si el valor es una estructura anidada (dict o list), lo serializa
    a una representación JSON compacta. En otro caso, retorna el valor
    directo o cadena vacía si es None.

    Args:
        valor: Elemento a normalizar.

    Returns:
        Valor listo para serializar en el registro CSV.
    """
    if valor is None:
        return ""
    if isinstance(valor, (dict, list)):
        return json.dumps(valor, ensure_ascii=False)
    return valor


def transformar_json_a_filas(
    datos: Any,
) -> tuple[list[str], list[dict[str, Any]]]:
    """Valida y transforma la estructura de datos JSON en encabezados y registros.

    Args:
        datos: Estructura decodificada desde el JSON de entrada.

    Returns:
        Tupla compuesta por:
            - Lista de nombres de columnas (encabezados únicos).
            - Lista de diccionarios que representan cada fila.

    Raises:
        ValueError: Si los datos no corresponden a una colección o diccionario.
    """
    if isinstance(datos, dict):
        filas = [datos]
    elif isinstance(datos, list):
        if not datos:
            return [], []
        if not all(isinstance(item, dict) for item in datos):
            raise ValueError(
                "La lista JSON debe contener únicamente objetos (diccionarios)."
            )
        filas = datos
    else:
        raise ValueError(
            "El JSON de entrada debe ser un objeto o una lista de objetos."
        )

    # Identificar todas las columnas únicas preservando el orden de aparición
    encabezados: list[str] = []
    for fila in filas:
        for clave in fila.keys():
            if clave not in encabezados:
                encabezados.append(clave)

    return encabezados, filas


def convertir_json_a_csv(
    flujo_entrada: TextIO,
    flujo_salida: TextIO,
    delimitador: str = ",",
) -> int:
    """Convierte el flujo de texto JSON en un flujo de texto CSV.

    Args:
        flujo_entrada: Stream de texto desde donde leer el JSON.
        flujo_salida: Stream de texto hacia donde escribir el CSV.
        delimitador: Carácter delimitador de campos CSV (por defecto ',').

    Returns:
        Cantidad de filas de datos procesadas y emitidas.

    Raises:
        ValueError: Si el delimitador es inválido o el JSON está mal formado.
        json.JSONDecodeError: Si el contenido no cumple con la sintaxis JSON.
    """
    if len(delimitador) != 1:
        raise ValueError(
            f"El delimitador debe ser un único carácter, se recibió: '{delimitador}'"
        )

    contenido = flujo_entrada.read()
    if not contenido.strip():
        return 0

    datos = json.loads(contenido)
    encabezados, filas = transformar_json_a_filas(datos)

    if not encabezados:
        return 0

    escritor = csv.writer(
        flujo_salida,
        delimiter=delimitador,
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\n",
    )

    escritor.writerow(encabezados)

    contador_filas = 0
    for fila in filas:
        registro = [aplanar_valor(fila.get(col, "")) for col in encabezados]
        escritor.writerow(registro)
        contador_filas += 1

    flujo_salida.flush()
    return contador_filas


def construir_parser() -> argparse.ArgumentParser:
    """Construye y configura el parser de argumentos de línea de comandos.

    Returns:
        Instancia de ArgumentParser configurada para el programa.
    """
    parser = argparse.ArgumentParser(
        prog="json2csv",
        description="Herramienta de filtro para convertir archivos JSON a formato CSV.",
        epilog="Ejemplo: python json2csv.py -i datos.json -o salida.csv -d ';'",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="archivo_entrada",
        default=None,
        help="Ruta al archivo JSON de entrada (opcional; por defecto stdin).",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="archivo_salida",
        default=None,
        help="Ruta al archivo CSV de salida (opcional; por defecto stdout).",
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        dest="delimitador",
        default=",",
        help="Carácter delimitador de campos para el archivo CSV (por defecto ',').",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Muestra la versión del programa y finaliza.",
    )
    return parser


def ejecutar_filtro(args_linea: Sequence[str] | None = None) -> int:
    """Punto de entrada principal para ejecutar la conversión CLI.

    Gestiona la apertura y cierre de flujos de archivos o estándar,
    y captura todas las excepciones controladas retornando códigos de salida estándar.

    Args:
        args_linea: Argumentos manuales de línea de comandos (opcional).

    Returns:
        Código entero de salida del proceso (0 éxito, != 0 error).
    """
    parser = construir_parser()
    args = parser.parse_args(args_linea)

    flujo_in: TextIO = sys.stdin
    flujo_out: TextIO = sys.stdout
    archivo_in_abierto = False
    archivo_out_abierto = False

    try:
        # Apertura de entrada
        if args.archivo_entrada is not None:
            if not os.path.exists(args.archivo_entrada):
                sys.stderr.write(
                    f"Error: El archivo de entrada '{args.archivo_entrada}' no existe.\n"
                )
                return 1
            flujo_in = open(args.archivo_entrada, "r", encoding="utf-8")
            archivo_in_abierto = True

        # Apertura de salida
        if args.archivo_salida is not None:
            flujo_out = open(args.archivo_salida, "w", encoding="utf-8")
            archivo_out_abierto = True

        # Ejecución de la conversión
        convertir_json_a_csv(flujo_in, flujo_out, args.delimitador)
        return 0

    except json.JSONDecodeError as err:
        sys.stderr.write(f"Error de formato JSON: {err}\n")
        return 2
    except ValueError as err:
        sys.stderr.write(f"Error de validación: {err}\n")
        return 3
    except OSError as err:
        sys.stderr.write(f"Error de entrada/salida: {err}\n")
        return 4
    finally:
        if archivo_in_abierto:
            flujo_in.close()
        if archivo_out_abierto:
            flujo_out.close()


def main() -> None:
    """Función de arranque del script CLI."""
    sys.exit(ejecutar_filtro())


if __name__ == "__main__":
    main()
