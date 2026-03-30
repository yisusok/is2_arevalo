#!/usr/bin/python
# *-------------------------------------------------------------------------*
# * factorial.py                                                            *
# * Calcula factorial de número o rango                                     *
# * TP1 - Ingeniería de Software II                                         *
# *-------------------------------------------------------------------------*

import sys

# Calcula el factorial de un número
def factorial(num):
    if num < 0:
        print("No existe factorial de negativos")
        return 0

    if num == 0:
        return 1

    fact = 1
    while num > 1:
        fact *= num
        num -= 1

    return fact


# Interpreta la entrada del usuario
def procesar_entrada(entrada):

    # Detecta rango
    if "-" in entrada:
        partes = entrada.split("-")

        # Caso "-10"
        if partes[0] == "":
            inicio = 1
            fin = int(partes[1])

        # Caso "5-"
        elif partes[1] == "":
            inicio = int(partes[0])
            fin = 60

        # Caso "4-8"
        else:
            inicio = int(partes[0])
            fin = int(partes[1])

    else:
        # Número único
        inicio = int(entrada)
        fin = int(entrada)

    return inicio, fin


# Programa principal
if len(sys.argv) < 2:
    entrada = input("Ingrese número o rango: ")
else:
    entrada = sys.argv[1]

inicio, fin = procesar_entrada(entrada)

if inicio > fin:
    print("Rango inválido")
    sys.exit()

# Calcula y muestra resultados
for i in range(inicio, fin + 1):
    print(f"Factorial {i}! es {factorial(i)}")