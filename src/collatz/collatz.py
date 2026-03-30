#!/usr/bin/python
# *-------------------------------------------------------------------------*
# * collatz.py                                                              *
# * Calcula la conjetura de Collatz para números entre 1 y 10000            *
# * Genera un gráfico de iteraciones                                        *
# * TP1 - Ingeniería de Software II                                         *
# *-------------------------------------------------------------------------*

import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# Función: collatz
# Calcula la cantidad de pasos hasta llegar a 1
# --------------------------------------------------------------------------
def collatz(n):
    pasos = 0

    while n != 1:
        # Si es par
        if n % 2 == 0:
            n = n // 2
        else:
            # Si es impar → 3n + 1
            n = 3 * n + 1
        
        pasos += 1

    return pasos


# --------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# --------------------------------------------------------------------------

x = []  # número inicial
y = []  # cantidad de iteraciones

# Calcular para valores entre 1 y 10000
for i in range(1, 10001):
    x.append(i)
    y.append(collatz(i))

# Crear gráfico
plt.plot(x, y)

# Etiquetas
plt.xlabel("Número inicial (n)")
plt.ylabel("Iteraciones hasta converger")
plt.title("Conjetura de Collatz")

# Mostrar gráfico
plt.show()