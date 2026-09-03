"""
TP9 - Ejercicio 9: Modelos Estáticos de Regresión para Estimación de Esfuerzo
Dataset histórico: LOC vs Esfuerzo (PM)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    # Dataset histórico
    loc = np.array([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000], dtype=float)
    esfuerzo_pm = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], dtype=float)

    print("=== Ejercicio 9: Evaluación de Modelos de Regresión Estáticos ===")

    # 1. Regresión Lineal: y = m * x + c
    m_lin, c_lin = np.polyfit(loc, esfuerzo_pm, 1)
    y_pred_lin = m_lin * loc + c_lin
    ss_tot = np.sum((esfuerzo_pm - np.mean(esfuerzo_pm)) ** 2)
    ss_res_lin = np.sum((esfuerzo_pm - y_pred_lin) ** 2)
    r2_lin = 1.0 - (ss_res_lin / ss_tot)

    # 2. Regresión Exponencial: y = a * exp(b * x) -> ln(y) = ln(a) + b * x
    poly_exp = np.polyfit(loc, np.log(esfuerzo_pm), 1)
    b_exp, ln_a_exp = poly_exp[0], poly_exp[1]
    a_exp = np.exp(ln_a_exp)
    y_pred_exp = a_exp * np.exp(b_exp * loc)
    ss_res_exp = np.sum((esfuerzo_pm - y_pred_exp) ** 2)
    r2_exp = 1.0 - (ss_res_exp / ss_tot)

    print("\n--- Resultados de Regresión ---")
    print(f"Modelo Lineal:      E(PM) = {m_lin:.6f} * LOC + ({c_lin:.4f})  | R² = {r2_lin:.4f}")
    print(f"Modelo Exponencial: E(PM) = {a_exp:.4f} * exp({b_exp:.6f} * LOC) | R² = {r2_exp:.4f}")

    # Selección
    mejor_modelo = "Lineal" if r2_lin > r2_exp else "Exponencial"
    print(f"\nModelo Seleccionado (mayor R²): Modelo {mejor_modelo}")

    # Estimación para LOC = 9100
    loc_9100 = 9100
    e_lin_9100 = m_lin * loc_9100 + c_lin
    e_exp_9100 = a_exp * np.exp(b_exp * loc_9100)
    print(f"\n--- Estimación para LOC = 9100 ---")
    print(f"Modelo Lineal:      {e_lin_9100:.2f} PM")
    print(f"Modelo Exponencial: {e_exp_9100:.2f} PM")

    # Estimación para LOC = 200
    loc_200 = 200
    e_lin_200 = m_lin * loc_200 + c_lin
    e_exp_200 = a_exp * np.exp(b_exp * loc_200)
    print(f"\n--- Estimación para LOC = 200 ---")
    print(f"Modelo Lineal:      {e_lin_200:.2f} PM (¡Valor negativo físicamente imposible!)")
    print(f"Modelo Exponencial: {e_exp_200:.2f} PM")

    print("\nPrecauciones con LOC = 200:")
    print("1. El valor de LOC=200 se encuentra muy por debajo del rango de calibración del dataset [1000, 10000].")
    print("2. La extrapolación lineal genera un resultado absurdo de esfuerzo negativo (-2.68 PM).")
    print("3. En proyectos pequeños (LOC=200), existen costos fijos no escalables (setup, ambiente, overhead).")

    # Graficación
    x_grid = np.linspace(0, 11000, 500)
    plt.figure(figsize=(9, 6))
    plt.scatter(loc, esfuerzo_pm, color='black', label='Datos Históricos (Calibración)', zorder=5)
    plt.plot(x_grid, m_lin * x_grid + c_lin, label=f'Lineal ($R^2={r2_lin:.4f}$)', color='#1f77b4', linewidth=2)
    plt.plot(x_grid, a_exp * np.exp(b_exp * x_grid), label=f'Exponencial ($R^2={r2_exp:.4f}$)', color='#d62728', linestyle='--', linewidth=2)

    plt.scatter([loc_9100], [e_lin_9100], color='green', marker='^', s=100, label=f'Predicción LOC=9100 ({e_lin_9100:.2f} PM)', zorder=6)
    plt.scatter([loc_200], [e_lin_200], color='purple', marker='v', s=100, label=f'Predicción LOC=200 ({e_lin_200:.2f} PM)', zorder=6)

    plt.axhline(0, color='gray', linestyle=':', alpha=0.7)
    plt.title('Ejercicio 9: Comparativa de Regresiones Estáticas')
    plt.xlabel('Tamaño / Complejidad (LOC)')
    plt.ylabel('Esfuerzo (Personas-Mes)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
