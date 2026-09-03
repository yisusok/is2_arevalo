"""
TP9 - Ejercicio 4: Modelo de Estimación de Esfuerzo y Tiempo Calendario
Relaciones:
    E = 8 * S^0.95
    td = 2.4 * E^0.33
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def calcular_esfuerzo(s: float) -> float:
    """Calcula el esfuerzo E (en Personas-Mes) dado el tamaño S."""
    return 8.0 * (s ** 0.95)


def calcular_tiempo_calendario(e: float) -> float:
    """Calcula el tiempo calendario td (en meses) dado el esfuerzo E."""
    return 2.4 * (e ** 0.33)


def main():
    print("=== Ejercicio 4: Estimación de Esfuerzo y Tiempo Calendario ===")

    # Tabla de valores representativos
    tamanos = [10, 50, 100, 500, 1000, 5000, 10000]
    print("\n--- Relación Tamaño (S) vs Esfuerzo (E) ---")
    print(f"{'Tamaño S':>10} | {'Esfuerzo E (PM)':>18} | {'Tiempo td (Meses)':>20}")
    print("-" * 55)

    for s in tamanos:
        e = calcular_esfuerzo(s)
        td = calcular_tiempo_calendario(e)
        print(f"{s:10d} | {e:18.2f} | {td:20.2f}")

    print("\n--- Relación Esfuerzo (E) vs Tiempo td ---")
    esfuerzos = [1, 10, 50, 100, 250, 500]
    print(f"{'Esfuerzo E (PM)':>15} | {'Tiempo td (Meses)':>20}")
    print("-" * 40)

    for e in esfuerzos:
        td = calcular_tiempo_calendario(e)
        print(f"{e:15d} | {td:20.2f}")

    # Graficación
    S_vals = np.linspace(0, 10000, 500)
    E_vals = calcular_esfuerzo(S_vals)

    E_td_vals = np.linspace(1, 500, 500)
    td_vals = calcular_tiempo_calendario(E_td_vals)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(S_vals, E_vals, color='#1f77b4', linewidth=2, label=r'$E = 8 S^{0.95}$')
    ax1.set_title('Esfuerzo (E) vs Tamaño (S)')
    ax1.set_xlabel('Tamaño S')
    ax1.set_ylabel('Esfuerzo E (PM)')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()

    ax2.plot(E_td_vals, td_vals, color='#2ca02c', linewidth=2, label=r'$t_d = 2.4 E^{0.33}$')
    ax2.set_title('Tiempo Calendario ($t_d$) vs Esfuerzo (E)')
    ax2.set_xlabel('Esfuerzo E (PM)')
    ax2.set_ylabel('Tiempo $t_d$ (Meses)')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
