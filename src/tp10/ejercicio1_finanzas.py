"""
Ejercicio 1: Ingeniería Financiera de un Proyecto de Software
Asignatura: Ingeniería de Software II (FCyT - UADER)
Docente: Dr. Pedro E. Colla
Alumno: Estudiante de Ingeniería de Software

Este script resuelve las preguntas financieras a, b, c, d, e, f del Ejercicio 1.
"""

import math

def calcular_ejercicio_1():
    r = 0.01  # Tasa efectiva mensual 1%
    costo_mensual_base = 1000.0

    print("=" * 70)
    print("EJERCICIO 1: ANÁLISIS FINANCIERO DE PROYECTO DE SOFTWARE")
    print("=" * 70)

    # a. Caso base (12 meses)
    n_a = 12
    pv_costos_a = sum(costo_mensual_base / ((1 + r)**t) for t in range(1, n_a + 1))
    pv_beneficio_a = 18000.0 / ((1 + r)**n_a)
    npv_a = pv_beneficio_a - pv_costos_a
    rent_a = npv_a / pv_costos_a

    print("\na. Ejecución según el plan original (12 meses):")
    print(f"   - Valor Presente de Costos (PV_costos): ${pv_costos_a:.2f}")
    print(f"   - Valor Presente de Beneficios (PV_beneficio): ${pv_beneficio_a:.2f}")
    print(f"   - Valor Presente Neto (NPV): ${npv_a:.2f}")
    print(f"   - Rentabilidad (NPV / PV_costos): {rent_a * 100:.2f}%")

    # b. Extensión por 3 meses (15 meses)
    n_b = 15
    pv_costos_b = sum(costo_mensual_base / ((1 + r)**t) for t in range(1, n_b + 1))
    pv_beneficio_b = 18000.0 / ((1 + r)**n_b)
    npv_b = pv_beneficio_b - pv_costos_b
    rent_b = npv_b / pv_costos_b

    print("\nb. Extensión del proyecto por 3 meses (15 meses total):")
    print(f"   - Valor Presente de Costos (PV_costos): ${pv_costos_b:.2f}")
    print(f"   - Valor Presente de Beneficios (PV_beneficio): ${pv_beneficio_b:.2f}")
    print(f"   - Valor Presente Neto (NPV): ${npv_b:.2f}")
    print(f"   - Rentabilidad (NPV / PV_costos): {rent_b * 100:.2f}%")

    # c. Comparación de Rentabilidad
    print("\nc. Resumen de Rentabilidades:")
    print(f"   - Caso Planificado (12 meses): {rent_a * 100:.2f}%")
    print(f"   - Caso Retrasado (15 meses): {rent_b * 100:.2f}%")
    print(f"   - Caída de Rentabilidad: {(rent_a - rent_b) * 100:.2f} puntos porcentuales")

    # d. Impacto de retraso de 6 meses (18 meses total)
    n_d = 18
    pv_costos_d = sum(costo_mensual_base / ((1 + r)**t) for t in range(1, n_d + 1))
    pv_beneficio_d = 18000.0 / ((1 + r)**n_d)
    npv_d = pv_beneficio_d - pv_costos_d
    rent_d = npv_d / pv_costos_d

    print("\nd. Impacto de un retraso de 6 meses (18 meses total):")
    print(f"   - Valor Presente de Costos (PV_costos): ${pv_costos_d:.2f}")
    print(f"   - Valor Presente de Beneficios (PV_beneficio): ${pv_beneficio_d:.2f}")
    print(f"   - Valor Presente Neto (NPV): ${npv_d:.2f}")
    print(f"   - Rentabilidad: {rent_d * 100:.2f}%")
    print(f"   - Destrucción absoluta de valor vs Plan: ${npv_a - npv_d:.2f}")

    # e. Esquema de Gestión Profesional (+5% costo mensual = $1050/mes)
    costo_mensual_pm = 1000.0 * 1.05
    pv_costos_e = sum(costo_mensual_pm / ((1 + r)**t) for t in range(1, 12 + 1))
    pv_beneficio_e = pv_beneficio_a
    npv_e = pv_beneficio_e - pv_costos_e
    rent_e = npv_e / pv_costos_e

    print("\ne. Esquema de Gestión Profesional con PMs certificados (+5% costo, 12 meses):")
    print(f"   - Nuevo costo mensual: ${costo_mensual_pm:.2f}")
    print(f"   - Valor Presente de Costos (PV_costos): ${pv_costos_e:.2f}")
    print(f"   - Valor Presente Neto (NPV): ${npv_e:.2f}")
    print(f"   - Rentabilidad: {rent_e * 100:.2f}%")
    print(f"   - Ganancia neta de contratar PM vs Retraso de 3 meses: ${npv_e - npv_b:.2f}")
    print("   - Conclusión: Es ALTAMENTE CONVENIENTE la gestión profesional.")

    # f. [Desafío] Máximo costo mensual aceptable para 15 meses manteniendo el NPV deseado ($4719.01)
    npv_deseado = npv_a
    pv_costos_f_permitido = pv_beneficio_b - npv_deseado
    factor_descuento_15 = sum(1.0 / ((1 + r)**t) for t in range(1, 15 + 1))
    c_max = pv_costos_f_permitido / factor_descuento_15

    print("\nf. [Desafío] Máximo costo mensual aceptable en 15 meses para conservar el NPV objetivo:")
    print(f"   - NPV objetivo a conservar: ${npv_deseado:.2f}")
    print(f"   - PV máximo de costos permitido: ${pv_costos_f_permitido:.2f}")
    print(f"   - Factor de descuento acumulado (15 meses): {factor_descuento_15:.6f}")
    print(f"   - Costo mensual máximo aceptable (C_max): ${c_max:.2f}")
    print(f"   - Reducción presupuestaria mensual requerida: {((1000.0 - c_max) / 1000.0) * 100:.2f}%")
    print("=" * 70)

if __name__ == "__main__":
    calcular_ejercicio_1()
