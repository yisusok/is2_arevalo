"""
TP9 - Ejercicio 8: Modelo Dinámico de Esfuerzo (PNR - Putnam-Norden-Rayleigh)
Evaluación de la distribución de esfuerzo en el tiempo para K = 72 PM
y análisis del impacto de la variación del parámetro 'a' (Zona Imposible).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def modelo_pnr_ritmo(t: np.ndarray, K: float, a: float) -> np.ndarray:
    """Calcula el ritmo de esfuerzo p(t) = 2 * K * a * t * exp(-a * t^2) [Personas/Mes]."""
    return 2.0 * K * a * t * np.exp(-a * (t ** 2))


def modelo_pnr_acumulado(t: np.ndarray, K: float, a: float) -> np.ndarray:
    """Calcula el esfuerzo acumulado E(t) = K * (1 - exp(-a * t^2)) [Personas-Mes]."""
    return K * (1.0 - np.exp(-a * (t ** 2)))


def main():
    print("=== Ejercicio 8: Modelo Dinámico PNR (Putnam-Norden-Rayleigh) ===")

    K = 72.0  # Esfuerzo total en Personas-Mes
    td_calib = 12.0  # Tiempo de entrega / pico de calibración baseline (12 meses)

    # Parámetro a de calibración baseline: a = 1 / (2 * td^2)
    a_calib = 1.0 / (2.0 * (td_calib ** 2))

    print(f"\nEsfuerzo Total Aceptado (K): {K} PM")
    print(f"Tiempo Calendario Baseline (td): {td_calib} meses")
    print(f"Parámetro de Calibración Obtenido (a): {a_calib:.6f} 1/mes^2")

    # Ritmo de esfuerzo pico
    p_max_calib = 2 * K * a_calib * (1 / np.sqrt(2 * a_calib)) * np.exp(-0.5)
    print(f"Personal Máximo en el Pico (p_max): {p_max_calib:.2f} Personas/Mes")

    # Caso C: a quadrupled
    a_quad = 4.0 * a_calib
    td_quad = 1.0 / np.sqrt(2.0 * a_quad)
    p_max_quad = 2 * K * a_quad * td_quad * np.exp(-0.5)

    print("\n--- Efecto de Cuadruplicar el Parámetro 'a' ---")
    print(f"Nuevo Parámetro a': {a_quad:.6f} 1/mes^2")
    print(f"Nuevo Tiempo de Pico td': {td_quad:.2f} meses (Compresión del 50%)")
    print(f"Nuevo Personal Máximo Requerido: {p_max_quad:.2f} Personas/Mes (4x sobrecarga)")

    # Graficación
    t = np.linspace(0, 24, 200)
    p_calib = modelo_pnr_ritmo(t, K, a_calib)
    p_quad_curve = modelo_pnr_ritmo(t, K, a_quad)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, p_calib, label=f'Modelo Calibrado ($a={a_calib:.5f}$, $t_d=12$m)', color='#1f77b4', linewidth=2.5)
    ax.plot(t, p_quad_curve, label=f'Modelo Compresivo ($a\'=4a={a_quad:.5f}$, $t_d=6$m)', color='#d62728', linestyle='--', linewidth=2.5)

    ax.fill_between(t, 0, p_quad_curve, color='#d62728', alpha=0.15, label='Zona Imposible (Imposible Staffing)')
    ax.set_title('Ejercicio 8: Curva Rayleigh PNR (K = 72 PM)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Tiempo (Meses)', fontsize=11)
    ax.set_ylabel('Ritmo de Esfuerzo p(t) (Personas/Mes)', fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
