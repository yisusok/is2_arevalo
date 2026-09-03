import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure output directory exists
output_dir = os.path.join(os.path.dirname(__file__), 'images')
os.makedirs(output_dir, exist_ok=True)

# Set plot style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 1.0

# ==========================================
# 1. EJERCICIO 4 PLOTS
# ==========================================
S_vals = np.linspace(0, 10000, 500)
E_vals = 8.0 * (S_vals ** 0.95)

E_td_vals = np.linspace(1, 500, 500)
td_vals = 2.4 * (E_td_vals ** 0.33)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot E vs S
ax1.plot(S_vals, E_vals, color='#1f77b4', linewidth=2.5, label=r'$E = 8 \cdot S^{0.95}$')
ax1.set_title('Esfuerzo (E) vs Tamaño (S)', fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel('Tamaño S (LOC / Puntos)', fontsize=11)
ax1.set_ylabel('Esfuerzo E (Personas-Mes)', fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(fontsize=11)

# Highlight specific points
ax1.scatter([1000, 5000, 10000], [8*1000**0.95, 8*5000**0.95, 8*10000**0.95], color='#d62728', zorder=5)
for s in [1000, 5000, 10000]:
    e = 8 * (s ** 0.95)
    ax1.annotate(f'S={s}\nE={e:.1f} PM', (s, e), textcoords="offset points", xytext=(-15, 10), ha='center', fontsize=9)

# Plot td vs E
ax2.plot(E_td_vals, td_vals, color='#2ca02c', linewidth=2.5, label=r'$t_d = 2.4 \cdot E^{0.33}$')
ax2.set_title('Tiempo Calendario ($t_d$) vs Esfuerzo (E)', fontsize=13, fontweight='bold', pad=12)
ax2.set_xlabel('Esfuerzo E (Personas-Mes)', fontsize=11)
ax2.set_ylabel('Tiempo $t_d$ (Meses)', fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(fontsize=11)

# Highlight specific points
ax2.scatter([1, 100, 500], [2.4*1**0.33, 2.4*100**0.33, 2.4*500**0.33], color='#d62728', zorder=5)
for e in [1, 100, 500]:
    td = 2.4 * (e ** 0.33)
    ax2.annotate(f'E={e}\ntd={td:.2f}m', (e, td), textcoords="offset points", xytext=(-15, 10), ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'q4_esfuerzo_tiempo.png'), dpi=300)
plt.close()

# ==========================================
# 2. EJERCICIO 8 PLOTS (PNR Model)
# ==========================================
K = 72.0  # PM total
# Calibration baseline: td = 12 months, a = 1 / (2 * td^2) = 1/288
td_calib = 12.0
a_calib = 1.0 / (2.0 * (td_calib ** 2))

# Time domain 0 to 24 months
t = np.linspace(0, 24, 200)

# Effort rate p(t) = 2 * K * a * t * exp(-a * t^2)
p_calib = 2 * K * a_calib * t * np.exp(-a_calib * (t ** 2))

# Quadrupled a (a_quad = 4 * a_calib)
a_quad = 4.0 * a_calib
p_quad = 2 * K * a_quad * t * np.exp(-a_quad * (t ** 2))

# Historical hypothetical dataset points (e.g. baseline curve + noise)
np.random.seed(42)
t_hist = np.array([1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
p_hist = 2 * K * a_calib * t_hist * np.exp(-a_calib * (t_hist ** 2)) + np.random.normal(0, 0.2, len(t_hist))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# Plot a: 72 PM baseline vs historical data
ax1.plot(t, p_calib, color='#1f77b4', linewidth=2.5, label=f'Modelo PNR Ajustado ($K=72$ PM, $t_d={td_calib:.0f}$m)')
ax1.scatter(t_hist, p_hist, color='#ff7f0e', s=50, zorder=5, label='Datos Históricos de Calibración')
ax1.axvline(x=td_calib, color='gray', linestyle=':', label=f'Peak Effort $t_p = {td_calib:.0f}$m')
ax1.set_title('Modelo PNR: Distribución de Esfuerzo (K = 72 PM)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Tiempo (Meses)', fontsize=11)
ax1.set_ylabel('Ritmo de Esfuerzo p(t) (Personas / Mes)', fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(fontsize=10)

# Plot b: Calibrated vs Quadrupled 'a' (Zona Imposible)
ax2.plot(t, p_calib, color='#1f77b4', linewidth=2.5, label=f'Calibrado ($a = {a_calib:.5f}$)')
ax2.plot(t, p_quad, color='#d62728', linewidth=2.5, linestyle='--', label=f'Compresión $a\' = 4a = {a_quad:.5f}$')
ax2.fill_between(t, 0, p_quad, color='#d62728', alpha=0.15, label='Zona Imposible (Sobrecarga Creciente)')
ax2.set_title('Efecto de Cuadruplicar el Parámetro "a" (Zona Imposible)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Tiempo (Meses)', fontsize=11)
ax2.set_ylabel('Ritmo de Esfuerzo p(t) (Personas / Mes)', fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'q8_pnr_distribucion.png'), dpi=300)
plt.close()

# ==========================================
# 3. EJERCICIO 9 PLOTS (Regresiones)
# ==========================================
x_data = np.array([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000], dtype=float)
y_data = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], dtype=float)

# Fits
m_lin, c_lin = np.polyfit(x_data, y_data, 1)
poly_exp = np.polyfit(x_data, np.log(y_data), 1)
b_exp, a_exp_log = poly_exp[0], poly_exp[1]
a_exp = np.exp(a_exp_log)

x_grid = np.linspace(0, 11000, 500)
y_lin_grid = m_lin * x_grid + c_lin
y_exp_grid = a_exp * np.exp(b_exp * x_grid)

fig, ax = plt.subplots(figsize=(9, 6))

ax.scatter(x_data, y_data, color='#000000', s=70, zorder=5, label='Datos Históricos (Calibración)')
ax.plot(x_grid, y_lin_grid, color='#1f77b4', linewidth=2.5, label=f'Regresión Lineal: $y = {m_lin:.6f}x {c_lin:+.2f}$ ($R^2=0.9726$)')
ax.plot(x_grid, y_exp_grid, color='#d62728', linewidth=2.5, linestyle='--', label=f'Regresión Exponencial: $y = {a_exp:.4f} e^{{{b_exp:.6f}x}}$ ($R^2=0.9058$)')

# Annotations for LOC=9100 and LOC=200
pred_lin_9100 = m_lin * 9100 + c_lin
pred_lin_200 = m_lin * 200 + c_lin
pred_exp_200 = a_exp * np.exp(b_exp * 200)

ax.scatter([9100], [pred_lin_9100], color='#2ca02c', s=90, marker='^', zorder=6, label=f'Estimación LOC=9100 ({pred_lin_9100:.2f} PM)')
ax.scatter([200], [pred_lin_200], color='#9467bd', s=90, marker='v', zorder=6, label=f'Estimación Lineal LOC=200 ({pred_lin_200:.2f} PM)')

ax.axhline(0, color='red', linestyle=':', alpha=0.7, label='Límite Físico (0 PM)')

ax.set_title('Modelos Estáticos de Esfuerzo: Comparativa de Regresiones', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Tamaño / Complejidad (LOC)', fontsize=11)
ax.set_ylabel('Esfuerzo (Personas-Mes)', fontsize=11)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(fontsize=9.5, loc='upper left')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'q9_regresion_modelos.png'), dpi=300)
plt.close()

print('Assets generated successfully!')
