"""
Resolución analítica y numérica del ejercicio de Línea de Base Organizacional
y Modelo Simplificado de V&V (Ingeniería de Software II - FCyT UADER).

Parámetros históricos:
- PCE = 89% (0.89)
- Densidad de defectos al liberar (delta_r) = 0.12 def/FP
- Tamaño del proyecto construido (S) = 100 FP
"""


def main():
    pce = 0.89
    delta_r = 0.12  # def/FP
    s = 100.0  # FP

    print("=" * 65)
    print("EJERCICIO DE ESTIMACIÓN Y LÍNEA DE BASE DE V&V")
    print("=" * 65)

    # 1. Defectos liberados esperados al momento de la entrega
    # D_r = S * delta_r
    d_r = s * delta_r

    # 2. Expectativa de defectos totales (mu_0)
    # PCE = D_detectados / mu_0 = (mu_0 - D_r) / mu_0 = 1 - (D_r / mu_0)
    # 1 - PCE = D_r / mu_0 => mu_0 = D_r / (1 - PCE)
    mu_0 = d_r / (1.0 - pce)

    # 3. Densidad de defectos al finalizar la construcción (delta_0)
    # delta_0 = mu_0 / S
    delta_0 = mu_0 / s

    # 4. Defectos que se deben planear detectar durante el período de V&V
    # D_vyv = mu_0 * PCE = mu_0 - D_r
    d_vyv = mu_0 * pce

    print("a. Expectativa de defectos totales (mu_0):")
    print(
        f"   D_r (liberados) = S * delta_r = {s:.0f} * {delta_r:.2f} = {d_r:.2f} defectos"
    )
    print(
        f"   mu_0 = D_r / (1 - PCE) = {d_r:.2f} / (1 - {pce:.2f}) = {mu_0:.2f} defectos (aprox. {round(mu_0)} defectos)"
    )
    print()

    print("b. Densidad de defectos al finalizar construcción (delta_0):")
    print(f"   delta_0 = mu_0 / S = {mu_0:.2f} / {s:.0f} = {delta_0:.4f} def/FP")
    print()

    print("c. Defectos a planear detectar durante el período de V&V:")
    print(
        f"   D_vyv = mu_0 * PCE = {mu_0:.2f} * {pce:.2f} = {d_vyv:.2f} defectos (aprox. {round(d_vyv)} defectos)"
    )
    print()

    print(
        "d. Análisis ante detección de 60 defectos en los primeros 3 días (20 def/día):"
    )
    porcentaje_detectado = (60.0 / d_vyv) * 100.0
    print(
        f"   En solo 3 días ya se detectó el {porcentaje_detectado:.1f}% de todos los defectos previstos para V&V."
    )
    print("   Fundamentación técnica:")
    print(
        "   1) La tasa de inyección de defectos durante el desarrollo superó ampliamente"
    )
    print("      la línea de base histórica (delta_0 > 1.09 def/FP).")
    print(
        "   2) Si se asume que aún no se alcanzó la asíntota de la curva de confiabilidad,"
    )
    print(
        "      el universo real de defectos totales mu_0 es sustancialmente mayor al previsto."
    )
    print(
        "   3) Mantener el plan de V&V original provocaría un desborde de defectos escapados"
    )
    print("      superando el límite de liberación delta_r = 0.12 def/FP.")
    print(
        "   4) Acción correctiva: Reestimar mu_0 mediante modelo dinámico (Musa/Goel-Okumoto)"
    )
    print(
        "      y extender el horizonte y esfuerzo de testeo antes de autorizar el release."
    )
    print("=" * 65)


if __name__ == "__main__":
    main()
