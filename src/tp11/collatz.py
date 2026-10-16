#!/usr/bin/env python3
"""
Módulo para el cálculo y comprobación de la Conjetura de Collatz.

TP11 - Gestión de Calidad (Ingeniería de Software II - FCyT UADER)
Requerimiento:
- Solicitar y aceptar un número entero positivo cualquiera por teclado.
- Limitar a 1999 el entero máximo a validar.
- Comprobar la conjetura de Collatz calculando el número de iteraciones
  necesarias para alcanzar el valor 1.
- Imprimir el número de partida y el número de iteraciones calculadas.
"""

import sys


def collatz(num: int) -> int:
    """Calcula la cantidad de iteraciones de la sucesión de Collatz hasta llegar a 1.

    Args:
        num: Número entero positivo inicial.

    Returns:
        Número entero con la cantidad de iteraciones realizadas.

    Raises:
        ValueError: Si el número no es un entero positivo mayor que cero.
    """
    if num <= 0:
        raise ValueError("El número debe ser un entero positivo mayor a 0.")

    iteraciones = 0
    while num != 1:
        if num % 2 == 0:
            num = num // 2
        else:
            num = 3 * num + 1
        iteraciones += 1

    return iteraciones


def solicitar_numero() -> int:
    """Solicita y valida un número entero positivo por teclado entre 1 y 1999.

    Returns:
        Número entero positivo validado dentro del rango [1, 1999].
    """
    while True:
        try:
            entrada = input("Ingrese un número entero positivo (máximo 1999): ").strip()
            valor = int(entrada)
            if valor <= 0:
                print("Error: El número debe ser mayor que cero. Intente nuevamente.")
                continue
            if valor > 1999:
                print(
                    "Error: El número supera el límite máximo permitido (1999). Intente nuevamente."
                )
                continue
            return valor
        except ValueError:
            print(
                "Error: Debe ingresar un valor numérico entero válido. Intente nuevamente."
            )
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada por el usuario.")
            sys.exit(0)


def main() -> None:
    """Función principal de ejecución del programa."""
    print("=" * 60)
    print("Comprobación de la Conjetura de Collatz (TP11 - Calidad)")
    print("=" * 60)

    numero_partida = solicitar_numero()
    iteraciones = collatz(numero_partida)

    print(f"\nNúmero de partida: {numero_partida}")
    print(f"Número de iteraciones necesarias para alcanzar 1: {iteraciones}")
    print("=" * 60)


if __name__ == "__main__":
    main()
