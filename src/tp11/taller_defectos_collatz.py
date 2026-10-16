#!/usr/bin/env python3
"""
Modelos Dinámicos de Confiabilidad y Proyección de Defectos (Modelo Básico de Musa).

Basado en el marco teórico de la cátedra y el notebook Taller_Defectos.ipynb
del Dr. Pedro E. Colla (Ingeniería de Software II - FCyT UADER).

Ecuaciones fundamentales:
- Intensidad de fallas: lambda(t) = lambda_0 * exp(-(lambda_0 / mu_0) * t)
- Defectos acumulados: mu(t) = mu_0 * (1 - exp(-(lambda_0 / mu_0) * t))
- Linealización: ln(d(t)) = ln(lambda_0) - (lambda_0 / mu_0) * t
  y = m * t + b
  lambda_0 = exp(b)
  mu_0 = -lambda_0 / m
"""

import math
import os


def regresion_musa(t_datos, d_datos):
    """Calcula los parámetros lambda_0 y mu_0 mediante el modelo de regresión de Musa.

    Args:
        t_datos: Lista con los tiempos (días o sesiones).
        d_datos: Lista con la cantidad de defectos observados por intervalo.

    Returns:
        Tupla (m, b, lambda_0, mu_0, r2)
    """
    n = len(t_datos)
    ln_d = [math.log(max(d, 1e-6)) for d in d_datos]

    sum_t = sum(t_datos)
    sum_y = sum(ln_d)
    sum_tt = sum(t * t for t in t_datos)
    sum_ty = sum(t * y for t, y in zip(t_datos, ln_d))

    # Coeficientes m y b (mínimos cuadrados)
    denom = n * sum_tt - sum_t * sum_t
    m = (n * sum_ty - sum_t * sum_y) / denom
    b = (sum_y - m * sum_t) / n

    lambda_0 = math.exp(b)
    mu_0 = -lambda_0 / m if m != 0 else float("inf")

    # Coeficiente de determinación R^2
    y_mean = sum_y / n
    ss_tot = sum((y - y_mean) ** 2 for y in ln_d)
    ss_res = sum((y - (m * t + b)) ** 2 for t, y in zip(t_datos, ln_d))
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 0.0

    return m, b, lambda_0, mu_0, r2


def mu_smooth(t, lambda_0, mu_0):
    """Calcula los defectos acumulados teóricos."""
    return mu_0 * (1.0 - math.exp(-(lambda_0 / mu_0) * t))


def lambda_smooth(t, lambda_0, mu_0):
    """Calcula la intensidad de defectos teórica instantánea."""
    return lambda_0 * math.exp(-(lambda_0 / mu_0) * t)


def main():
    print("=" * 70)
    print("TP11 - GESTIÓN DE CALIDAD: PROYECCIÓN DE DEFECTOS (MODELO DE MUSA)")
    print("=" * 70)

    # --------------------------------------------------------------------------
    # 1. Dataset de prueba de la guía (Días 0 a 6)
    # --------------------------------------------------------------------------
    dias = [0, 1, 2, 3, 4, 5, 6]
    defectos_guia = [9, 18, 5, 7, 23, 2, 8]

    m1, b1, l0_1, mu0_1, r2_1 = regresion_musa(dias, defectos_guia)
    total_observado_1 = sum(defectos_guia)

    print("\n[EJERCICIO 1] Dataset de la guía de trabajos prácticos (7 primeros días):")
    print("Día:      ", dias)
    print("Defectos: ", defectos_guia)
    print(f"Total de defectos observados (sum mu_i): {total_observado_1}")
    print("\nResultados de la regresión lineal sobre ln(Defectos):")
    print(f"  Pendiente (m)   = {m1:.6f}")
    print(f"  Ordenada (b)    = {b1:.6f}")
    print(f"  R^2             = {r2_1:.4f}")
    print(f"  lambda_0        = {l0_1:.4f} def/día (intensidad inicial)")
    print(f"  mu_0 estimado   = {mu0_1:.2f} defectos totales proyectados")
    print(
        f"  Defectos remanentes estimados = mu_0 - sum(mu_i) = {mu0_1 - total_observado_1:.2f}"
    )

    # --------------------------------------------------------------------------
    # 2. Dataset de Sesiones del ejercicio de Collatz (asimilando Día a Sesión)
    # --------------------------------------------------------------------------
    # Sesiones de test del programa Collatz:
    # S1 (Insp. estática inicial): 4 defectos
    # S2 (Validación de tests):    2 defectos
    # S3 (Test unitario 1):        2 defectos sintácticos/runtime
    # S4 (Test unitario 2):        1 defecto (return iter)
    # S5 (Test funcional 1):       1 defecto (límite 1999)
    # S6 (Test funcional 2):       0 defectos (100% éxito)
    # Tomamos las sesiones con defectos observados para la regresión
    sesiones = [1, 2, 3, 4, 5]
    defectos_collatz = [4, 2, 2, 1, 1]

    m2, b2, l0_2, mu0_2, r2_2 = regresion_musa(sesiones, defectos_collatz)
    total_observado_2 = sum(defectos_collatz)

    # Cálculo de LOCs de collatz.py
    collatz_file = os.path.join(os.path.dirname(__file__), "collatz.py")
    try:
        with open(collatz_file, "r", encoding="utf-8") as f:
            loc_final = len(f.readlines())
    except Exception:
        loc_final = 82

    # Defectos liberados: mu_r = mu_0 - sum(mu_i)
    # En caso de que sum(mu_i) alcance o supere la estimación discreta, mu_r tiende a 0.
    mu_r = max(0.0, mu0_2 - total_observado_2)

    print("\n" + "-" * 70)
    print("[EJERCICIO 2] Dataset de Sesiones de Collatz (asimilando Día a Sesiones):")
    print("Sesión:   ", sesiones)
    print("Defectos: ", defectos_collatz)
    print(f"Total de defectos identificados (sum mu_i): {total_observado_2}")
    print("\nResultados de la regresión de Musa para Collatz:")
    print(f"  Pendiente (m)   = {m2:.6f}")
    print(f"  Ordenada (b)    = {b2:.6f}")
    print(f"  R^2             = {r2_2:.4f}")
    print(f"  lambda_0        = {l0_2:.4f} def/sesión")
    print(f"  mu_0 estimado   = {mu0_2:.2f} defectos totales estadísticos")
    print(
        f"\nTamaño final del código collatz.py (cat collatz.py | wc -l): {loc_final} LOCs"
    )
    print(
        f"Defectos liberados al finalizar test (mu_r = mu_0 - sum mu_i): {mu_r:.2f} defectos"
    )
    print(
        f"Densidad final de defectos liberados (mu_r / LOC): {mu_r / loc_final:.5f} def/LOC"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()
