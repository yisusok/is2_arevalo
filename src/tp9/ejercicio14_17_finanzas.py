"""
TP9 - Ejercicios 14 a 17: Evaluaciones Financieras y de Riesgo en Proyectos
"""


def ejercicio_14():
    print("=== Ejercicio 14: Esperanza de Apuesta en Ruleta ===")
    ficha = 1000.0
    p_ganar = 18.0 / 37.0
    p_perder = 19.0 / 37.0

    ev = (ficha * p_ganar) + (-ficha * p_perder)
    print(f"Probabilidad de Ganar (P_g): {p_ganar:.4f} ({p_ganar*100:.2f}%)")
    print(f"Probabilidad de Perder (P_p): {p_perder:.4f} ({p_perder*100:.2f}%)")
    print(f"Esperanza Matemática E(X): ${ev:.2f}")
    print(f"Ventaja de la casa: {abs(ev/ficha)*100:.2f}%\n")


def ejercicio_15():
    print("=== Ejercicio 15: Telar de los Colores (Esquema Ponzi) ===")
    inversion = 1000.0
    rendimiento_mensual = 0.07
    ganancia = inversion * rendimiento_mensual  # +70
    perdida = -inversion  # -1000

    # Para E(X) <= 0: 70 * Pg - 1000 * (1 - Pg) = 0 => 1070 * Pg = 1000
    p_ganar_limite = 1000.0 / 1070.0
    p_perder_limite = 1.0 - p_ganar_limite

    print(f"Ganancia esperada en caso de éxito: +${ganancia:.2f}")
    print(f"Pérdida en caso de colapso: -${inversion:.2f}")
    print(f"Probabilidad de ganar máxima para E(X) <= 0: {p_ganar_limite:.4f} ({p_ganar_limite*100:.2f}%)")
    print(f"Probabilidad de perder mínima para E(X) <= 0: {p_perder_limite:.4f} ({p_perder_limite*100:.2f}%)")
    print("Conclusión: Para que la esperanza neta sea nula o negativa, la probabilidad de perder el total del capital")
    print("debe ser de al menos un 6.54% por período. En esquemas piramidales reales, la pérdida final supera el 90%.\n")


def ejercicio_16():
    print("=== Ejercicio 16: Valor Presente (VP) ===")
    fv = 1000.0
    r_mensual = 0.07
    n_meses = 12

    vp = fv / ((1.0 + r_mensual) ** n_meses)
    print(f"Monto Futuro (FV): ${fv:.2f} en {n_meses} meses")
    print(f"Tasa de Costo de Oportunidad Mensual (r): {r_mensual*100:.1f}%")
    print(f"Factor de Descuento (1+r)^12: {(1.0 + r_mensual)**n_meses:.6f}")
    print(f"Valor Presente (VP): ${vp:.2f}\n")


def ejercicio_17():
    print("=== Ejercicio 17: Tasa Efectiva Anual (TEA) e Impacto en Camino Crítico ===")
    r_mensual = 0.07
    tea = ((1.0 + r_mensual) ** 12) - 1.0

    print(f"Tasa Efectiva Anual (TEA): {tea*100:.2f}%")

    # Verificación
    fv = 1000.0
    vp = fv / (1.0 + tea)
    print(f"Verificación VP con TEA: ${vp:.2f}")
    print("\nImpacto en Duración y Camino Crítico Financiero:")
    print("1. Duración del proyecto: 12 meses.")
    print("2. Tasa de descuento extremadamente alta (TEA = 125.22% anual):")
    print("   - Los flujos de fondos lejanos pierden casi todo su valor presente.")
    print("   - En la programación financiera de proyectos (CPM/PERT Financiero), el camino crítico")
    print("     se desplaza hacia las actividades que liberan ingresos o reducen egresos en las primeras fases,")
    print("     penalizando fuertemente la holgura de actividades con alto flujo monetario tardío.")


def main():
    ejercicio_14()
    ejercicio_15()
    ejercicio_16()
    ejercicio_17()


if __name__ == '__main__':
    main()
