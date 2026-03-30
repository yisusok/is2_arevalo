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


# ✔ NUEVO: pedir input si no hay argumento
if len(sys.argv) < 2:
    num = int(input("Ingrese un número: "))
else:
    num = int(sys.argv[1])

print(f"Factorial {num}! es {factorial(num)}")