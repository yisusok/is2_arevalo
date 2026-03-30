import sys

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


# ✔ Función para procesar entrada
def procesar_entrada(entrada):

    if "-" in entrada:
        partes = entrada.split("-")

        # "-10" → 1 a 10
        if partes[0] == "":
            inicio = 1
            fin = int(partes[1])

        # "5-" → 5 a 60
        elif partes[1] == "":
            inicio = int(partes[0])
            fin = 60

        # "4-8"
        else:
            inicio = int(partes[0])
            fin = int(partes[1])
    else:
        inicio = int(entrada)
        fin = int(entrada)

    return inicio, fin


# Entrada
if len(sys.argv) < 2:
    entrada = input("Ingrese número o rango: ")
else:
    entrada = sys.argv[1]

inicio, fin = procesar_entrada(entrada)

# Validación
if inicio > fin:
    print("Rango inválido")
    sys.exit()

# Mostrar
for i in range(inicio, fin + 1):
    print(f"Factorial {i}! es {factorial(i)}")