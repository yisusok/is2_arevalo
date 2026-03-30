

import sys

class Factorial:

    def __init__(self):
        pass

    def calcular(self, num):
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

    def run(self, minimo, maximo):
        if minimo > maximo:
            print("Rango inválido")
            return

        for i in range(minimo, maximo + 1):
            print(f"Factorial {i}! es {self.calcular(i)}")


def procesar_entrada(entrada):

    if "-" in entrada:
        partes = entrada.split("-")

        if partes[0] == "":
            inicio = 1
            fin = int(partes[1])

        elif partes[1] == "":
            inicio = int(partes[0])
            fin = 60

        else:
            inicio = int(partes[0])
            fin = int(partes[1])

    else:
        inicio = int(entrada)
        fin = int(entrada)

    return inicio, fin


if len(sys.argv) < 2:
    entrada = input("Ingrese número o rango (ej: 5, 4-8, -10, 5-): ")
else:
    entrada = sys.argv[1]

inicio, fin = procesar_entrada(entrada)

f = Factorial()

f.run(inicio, fin)