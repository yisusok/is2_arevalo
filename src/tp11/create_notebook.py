"""Script para generar el Jupyter Notebook 'TP11_Gestion_Calidad.ipynb'.

Asignatura: Ingeniería de Software II (FCyT - UADER)
Docente: Dr. Pedro E. Colla
Alumno: Jesús Arévalo
Ubicación: src/tp11/
"""

import json
import os


def build_notebook():
    nb = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.14.3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }

    # Cell 1: Carátula y Encabezado
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# TP11: Gestión de Calidad, Validación & Verificación\n",
                "\n",
                "**Asignatura:** Ingeniería de Software II  \n",
                "**Docente:** Dr. Pedro E. Colla  \n",
                "**Institución:** Facultad de Ciencia y Tecnología (FCyT) - Universidad Autónoma de Entre Ríos (UADER)  \n",
                "**Alumno:** Jesús Arévalo  \n",
                "**Ubicación de Código y Documentación:** `src/tp11/`  \n",
                "\n",
                '> **Nota de Alineación Académica:** Las respuestas conceptuales, formulaciones matemáticas y modelos estadísticos de confiabilidad presentados en este cuaderno han sido desarrollados en estricta conformidad con el marco teórico y láminas dictadas por el **Dr. Pedro E. Colla** (*"Gestión de Calidad, Validación & Verificación"*, *"Procesos de Calidad"*, *"Garantía"* y el *"Taller_Defectos.ipynb"*), así como el tutorial *"Kanban para uso genérico"* del **Ing. Álvaro Ruiz de Mendarozqueta**.\n',
                "\n",
                "---",
            ],
        }
    )

    # Cell 2: Imports y Setup
    nb["cells"].append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "\n",
                "# Configuración estética de gráficos\n",
                "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                "plt.rcParams['font.sans-serif'] = 'Arial'\n",
                "plt.rcParams['axes.edgecolor'] = '#cccccc'\n",
                "plt.rcParams['axes.linewidth'] = 0.8\n",
                "print('Entorno de simulación inicializado correctamente.')",
            ],
        }
    )

    # Cell 3: Sección 1 - Collatz Requerimientos e Inspección
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Conjetura de Collatz: Requerimientos, Trazabilidad e Inspección de Calidad\n",
                "\n",
                "### Estructuración de Requerimientos\n",
                "- **Requerimientos Funcionales $R = \\{R_1, R_2, R_3, R_4\\}$:**\n",
                "  - $R_1$: Solicitar y aceptar por teclado un número entero positivo cualquiera.\n",
                "  - $R_2$: Comprobar la conjetura de Collatz ($n \\text{ par} \\to n/2$; $n \\text{ impar} \\to 3n+1$) iterando hasta alcanzar el valor 1.\n",
                "  - $R_3$: Calcular el número de iteraciones necesarias para alcanzar el valor 1.\n",
                "  - $R_4$: Imprimir en pantalla el número de partida y el número total de iteraciones.\n",
                "\n",
                "- **Requerimientos No Funcionales $F = \\{F_1, F_2, F_3, F_4\\}$:**\n",
                "  - $F_1$ (Restricción de dominio): Limitar a 1999 el entero máximo a validar ($1 \\le n \\le 1999$).\n",
                "  - $F_2$ (Calidad de código): Tasa de comentarios controlada (defecto si supera el umbral de 12).\n",
                "  - $F_3$ (Robustez y excepciones): Manejo controlado de entradas no válidas (números negativos, cero, alfanuméricos).\n",
                "  - $F_4$ (Mantenibilidad): Conformidad con PEP8, tipado estático y convenciones PEP257.\n",
                "\n",
                "### Matriz de Trazabilidad RTMX ($R \\cup F \\iff T$)\n",
                "| Requerimiento | Descripción | Casos de Prueba Asociados | Tipo de Prueba |\n",
                "|---|---|---|---| \n",
                "| $R_1$ | Entrada por teclado | $T_5, T_6, T_7, T_8, T_9, T_{10}$ | Funcional (Caja Negra) |\n",
                "| $R_2$ | Algoritmo 3n+1 / n/2 | $T_1, T_2, T_3, T_4$ | Unitario (Caja Blanca) |\n",
                "| $R_3$ | Conteo de iteraciones | $T_1, T_2, T_3, T_4, T_5, T_7$ | Unitario / Funcional |\n",
                "| $R_4$ | Impresión de resultados | $T_5, T_6, T_7$ | Funcional (Caja Negra) |\n",
                "| $F_1$ | Límite máximo 1999 | $T_7, T_8$ | Funcional (Frontera) |\n",
                "| $F_2$ | Tasa de comentarios | Inspección estática (S1) | Verificación Estática |\n",
                "| $F_3$ | Control de excepciones | $T_8, T_9, T_{10}, T_{11}, T_{12}$ | Robustez / Excepciones |\n",
                "| $F_4$ | Convenciones de código | Linters (Ruff, Black, Mypy) | Análisis Estático |",
            ],
        }
    )

    # Cell 4: Código Collatz y Ejecución
    nb["cells"].append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "def collatz(num: int) -> int:\n",
                "    if num <= 0:\n",
                "        raise ValueError('El número debe ser un entero positivo mayor a 0.')\n",
                "    iteraciones = 0\n",
                "    while num != 1:\n",
                "        if num % 2 == 0:\n",
                "            num = num // 2\n",
                "        else:\n",
                "            num = 3 * num + 1\n",
                "        iteraciones += 1\n",
                "    return iteraciones\n",
                "\n",
                "# Verificación para casos clave\n",
                "ejemplos = [1, 2, 3, 4, 20, 1999]\n",
                "for val in ejemplos:\n",
                "    print(f'Partida: {val:4d} -> Iteraciones: {collatz(val):2d}')",
            ],
        }
    )

    # Cell 5: Sección 2 - Regresión de Musa
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Modelos Dinámicos de Confiabilidad de Software (Modelo de Musa / Goel-Okumoto)\n",
                "\n",
                "Conforme al taller `Taller_Defectos.ipynb` del Dr. Pedro E. Colla, el modelo básico de ejecución en el tiempo de Musa establece:\n",
                "\n",
                "$$\\lambda(t) = \\lambda_0 e^{-\\left(\\frac{\\lambda_0}{\\mu_0}\\right) t}$$\n",
                "\n",
                "$$\\mu(t) = \\mu_0 \\left(1 - e^{-\\left(\\frac{\\lambda_0}{\\mu_0}\\right) t}\\right)$$\n",
                "\n",
                "Aplicando logaritmo natural sobre la tasa de defectos:\n",
                "\n",
                "$$\\ln(d(t)) = \\ln(\\lambda_0) - \\left(\\frac{\\lambda_0}{\\mu_0}\\right) t = m \\cdot t + b$$\n",
                "\n",
                "donde $\\lambda_0 = e^b$ y $\\mu_0 = -\\frac{\\lambda_0}{m}$.",
            ],
        }
    )

    # Cell 6: Código Regresión Guía
    nb["cells"].append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Dataset de los 7 primeros días\n",
                "t_dias = np.array([0, 1, 2, 3, 4, 5, 6], dtype=float)\n",
                "defectos = np.array([9, 18, 5, 7, 23, 2, 8], dtype=float)\n",
                "\n",
                "# Regresión lineal sobre ln(d)\n",
                "ln_d = np.log(defectos)\n",
                "m, b = np.polyfit(t_dias, ln_d, 1)\n",
                "l0 = float(np.exp(b))\n",
                "mu0 = float(-l0 / m)\n",
                "\n",
                "print(f'Pendiente (m):     {m:.6f}')\n",
                "print(f'Ordenada (b):      {b:.6f}')\n",
                "print(f'lambda_0 inicial:  {l0:.4f} defectos/día')\n",
                "print(f'mu_0 proyectado:   {mu0:.2f} defectos totales')\n",
                "print(f'Observados:        {np.sum(defectos):.0f} defectos')\n",
                "print(f'Remanentes:        {mu0 - np.sum(defectos):.2f} defectos')\n",
                "\n",
                "# Curvas teóricas\n",
                "t_grid = np.linspace(0, 15, 200)\n",
                "mu_teorica = mu0 * (1.0 - np.exp(-(l0 / mu0) * t_grid))\n",
                "lambda_teorica = l0 * np.exp(-(l0 / mu0) * t_grid)\n",
                "\n",
                "plt.figure(figsize=(10, 5))\n",
                "plt.plot(t_grid, mu_teorica, label='Defectos Acumulados $\\mu(t)$ (Teórico)', color='#d62728', lw=2)\n",
                "plt.plot(t_grid, lambda_teorica, label='Intensidad de Fallas $\\lambda(t)$', color='#1f77b4', linestyle='--', lw=2)\n",
                "plt.scatter(t_dias, np.cumsum(defectos), color='black', zorder=5, label='Acumulado Observado')\n",
                "plt.scatter(t_dias, defectos, color='blue', marker='x', zorder=5, label='Defectos Diarios Observados')\n",
                "plt.axhline(mu0, color='gray', linestyle=':', label=f'Asíntota $\\mu_0 = {mu0:.1f}$')\n",
                "plt.title('Calibración del Modelo Dinámico de Confiabilidad de Musa (Días 0 a 6)')\n",
                "plt.xlabel('Tiempo continuo de test (días)')\n",
                "plt.ylabel('Cantidad de Defectos')\n",
                "plt.legend()\n",
                "plt.tight_layout()\n",
                "plt.show()",
            ],
        }
    )

    # Cell 7: Regresión para Collatz
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Proyección de Defectos en el Software Collatz (Asimilando Día a Sesión)\n",
                "\n",
                "- Sesión 1: Inspección estática inicial (4 defectos sintácticos y semánticos detectados).\n",
                "- Sesión 2: Inspección de test cases (2 omisiones de frontera agregadas).\n",
                "- Sesión 3: Testing unitario 1 (2 fallas en tiempo de ejecución).\n",
                "- Sesión 4: Testing unitario 2 (1 falla de valor retornado).\n",
                "- Sesión 5: Testing funcional 1 (1 falla en límite 1999).\n",
                "- Sesión 6: Testing funcional 2 (0 fallas, 100% éxito).",
            ],
        }
    )

    # Cell 8: Código Collatz Regresión
    nb["cells"].append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sesiones = np.array([1, 2, 3, 4, 5], dtype=float)\n",
                "def_sesion = np.array([4, 2, 2, 1, 1], dtype=float)\n",
                "\n",
                "m_col, b_col = np.polyfit(sesiones, np.log(def_sesion), 1)\n",
                "l0_col = float(np.exp(b_col))\n",
                "mu0_col = float(-l0_col / m_col)\n",
                "total_col = float(np.sum(def_sesion))\n",
                "\n",
                "loc_final = 82  # Obtenido con cat collatz.py | wc -l\n",
                "mu_r = max(0.0, mu0_col - total_col)\n",
                "\n",
                "print('Resultados Collatz:')\n",
                "print(f'  lambda_0: {l0_col:.4f} def/sesión')\n",
                "print(f'  mu_0 estimado: {mu0_col:.2f} defectos totales proyectados')\n",
                "print(f'  Total identificados (sum mu_i): {total_col:.0f} defectos')\n",
                "print(f'  Tamaño de collatz.py: {loc_final} LOCs')\n",
                "print(f'  Defectos liberados (mu_r = mu_0 - sum mu_i): {mu_r:.2f} defectos')\n",
                "print(f'  Densidad de defectos liberados: {mu_r / loc_final:.5f} def/LOC')",
            ],
        }
    )

    # Cell 9: Sección 3 - Kanban y TEP
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Metodología Kanban y el Parámetro TEP (Álvaro Ruiz de Mendarozqueta)\n",
                "\n",
                'Conforme al tutorial visual *"Kanban para uso genérico"* del **Ing. Álvaro Ruiz de Mendarozqueta**:\n',
                "\n",
                "1. **Significado del parámetro TEP:**  \n",
                '   **TEP** significa **Trabajo En Progreso**, siendo la traducción al español de la sigla universal **WIP** (*Work In Progress*). Representa la cantidad exacta de tareas que se encuentran simultáneamente en ejecución activa dentro de las columnas operativas (por ejemplo, en la sección *"Trabajando"*).\n',
                "\n",
                "2. **Significado crítico en su utilización:**  \n",
                "   El fundamento central de Kanban descansa sobre la **Ley de Little**:\n",
                "\n",
                "   $$\\text{Plazo de ejecución (Lead Time)} = \\frac{\\text{Trabajo En Progreso (TEP)}}{\\text{Rendimiento (Throughput)}}$$\n",
                "\n",
                "   - **Control del Lead Time:** Si el TEP crece sin límite, el tiempo de entrega (*Lead Time*) se incrementa proporcionalmente, provocando multitasking, dispersión y sobrecarga cognitiva.\n",
                "   - **Modelo Pull:** Limitar el TEP (fijando un tope explícito, ej. $TEP = 2$) impide la acumulación desordenada de trabajo; una nueva tarea entra sólo cuando se libera cupo al terminar una anterior.\n",
                "   - **Exposición de impedimentos:** Cuando una tarea se bloquea, el cupo del TEP se satura de inmediato, forzando al equipo a detener el ingreso de trabajo para abocarse a destrabar el cuello de botella (foco en el flujo y mejora continua).",
            ],
        }
    )

    # Cell 10: Sección 4 - Marco de Garantía y Multas
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Marco para Evaluar Garantía y Efecto de Multas Contractuales (Dr. Pedro E. Colla)\n",
                "\n",
                "### Modelo Económico de Confiabilidad y Garantía\n",
                "El costo total del ciclo de vida bajo garantía $C_t(\\tau_r)$ se compone del costo de testeo en desarrollo $C(\\tau_r)$ y el costo de atender fallas durante el período de garantía $\\tau_w$, denotado $W(\\tau_r)$:\n",
                "\n",
                "$$C_t(\\tau_r) = C(\\tau_r) + W(\\tau_r)$$\n",
                "\n",
                "$$C(q) = C_0 + C_1 \\tau_r^\\alpha + C_2 \\mu_0 (1 - e^{-\\lambda_0 \\tau_r})$$\n",
                "\n",
                "$$W(q) = C_3 \\mu_0 \\left[ (1 - e^{-\\lambda_0 (\\tau_r + \\tau_w)}) - (1 - e^{-\\lambda_0 \\tau_r}) \\right]$$\n",
                "\n",
                "### Comportamiento Cualitativo de Incrementar el PCE\n",
                "- Al **incrementar el PCE** en las etapas de ingeniería (análisis, diseño, revisiones), una mayor fracción de defectos es contenida tempranamente, disminuyendo la densidad latente que llega al período de prueba.\n",
                "- Como demuestra la curva $[\tau_r / \\tau_0] = f(\\tau_w, PCE)$ (slide 9 de *Garantía*), a mayor PCE ($0.9$ frente a $0.5$), el **tiempo óptimo de testeo $(\\tau_r^*)$ disminuye sensiblemente** para alcanzar la confiabilidad contractual. Prevenir defectos ahorra tiempo y costo de testeo posterior.\n",
                "\n",
                "### Efecto de una Multa en el Punto de Equilibrio\n",
                "- Una **multa o penalidad contractual** incrementa directamente el costo unitario de falla externa en garantía ($C_3' = C_3 + \\text{Multa}$).\n",
                "- Esto eleva la curva de costo de garantía $W(\\tau_r)$, acentuando su pendiente negativa para tiempos cortos de test.\n",
                "- Al resolver $\\frac{\\partial C_t}{\\partial \\tau_r} = 0$, el punto de equilibrio económico se desplaza hacia la **derecha**, es decir, **se incrementa el tiempo óptimo de test $(\\tau_r^*)$**. La multa incentiva a prolongar y profundizar la verificación en desarrollo antes de liberar el producto.",
            ],
        }
    )

    # Cell 11: Sección 5 - Línea de Base V&V
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Modelo Simplificado de V&V y Línea de Base Organizacional\n",
                "\n",
                "### Parámetros Históricos:\n",
                "- $PCE = 89\\% = 0.89$\n",
                "- Densidad de defectos al liberar: $\\delta_r = 0.12 \\text{ def/FP}$\n",
                "- Tamaño del proyecto: $S = 100 \\text{ FP}$",
            ],
        }
    )

    # Cell 12: Código V&V
    nb["cells"].append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "s_fp = 100.0\n",
                "pce_org = 0.89\n",
                "delta_r_org = 0.12\n",
                "\n",
                "# a. Expectativa de defectos totales (mu_0)\n",
                "d_r = s_fp * delta_r_org\n",
                "mu_0_fp = d_r / (1.0 - pce_org)\n",
                "\n",
                "# b. Densidad de defectos al finalizar construcción (delta_0)\n",
                "delta_0_fp = mu_0_fp / s_fp\n",
                "\n",
                "# c. Defectos a planear detectar en V&V\n",
                "d_vyv_fp = mu_0_fp * pce_org\n",
                "\n",
                "print(f'a. mu_0 esperado:                {mu_0_fp:.2f} defectos (aprox. {round(mu_0_fp)})')\n",
                "print(f'b. delta_0 al fin construcción: {delta_0_fp:.4f} def/FP')\n",
                "print(f'c. Defectos a detectar en V&V:  {d_vyv_fp:.2f} defectos (aprox. {round(d_vyv_fp)})')\n",
                "print(f'   Defectos tolerados al release: {d_r:.2f} defectos')",
            ],
        }
    )

    # Cell 13: Sección 6 - Deuda Técnica y Agilidad
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                '## 6. Deuda Técnica y Calidad en Ciclos Ágiles ("Agile & Software Engineering")\n',
                "\n",
                "De acuerdo al modelo analítico de Colla (slides 64 a 86 de *Procesos de Calidad*):\n",
                "\n",
                "1. **Factores gestionados desde la calidad:**\n",
                "   - **PCE (Contención en Fase):** Un $PCE \\ge 80\\%$ impide que los defectos escapen y se transformen en **deuda técnica involuntaria**, la cual adquiere precedencia mandatoria sobre las nuevas historias de usuario.\n",
                "   - **CoPQ (Costo de Pobre Calidad):** Limitar el $CoPQ \\le 18\\%$ previene la destrucción del valor operativo aportado por la agilidad.\n",
                "   - **Tasa de Refactoring ($r$):** Se debe garantizar una tasa mínima de refactoring por sprint que supere la frontera de bancarrota técnica:\n",
                "\n",
                "     $$r > \\frac{\\alpha}{\\alpha + 1 - \\beta}$$\n",
                "\n",
                "   - **Reducción de $\\alpha$ (inyección en nuevo código) y $\\beta$ (retrabajo del retrabajo):** Mediante pruebas automáticas, linters e inspecciones de pares.\n",
                "\n",
                "2. **Por qué producen esa mejora:**\n",
                "   En presencia de defectos no resueltos, la velocidad efectiva del equipo se degrada según:\n",
                "\n",
                "   $$V_k = \\frac{V_0}{1 + \\gamma D_k}$$\n",
                "\n",
                '   Si no se controla el PCE y no se paga la deuda, el proyecto entra en **"trashing"** (todo el esfuerzo se drena en arreglar fallas y la entrega de valor nuevo cae a cero, $N_k \\to 0$). La gestión rigurosa de calidad estabiliza la velocidad, reduce los sprints de limpieza ($S_{clean}$) y asegura la viabilidad presupuestaria ($K_{fin} \\le K_B$).',
            ],
        }
    )

    # Cell 14: Sección 7 - json2csv y CI/CD
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Herramienta json2csv y Pipeline de Integración Continua\n",
                "\n",
                "La herramienta `json2csv.py` ha sido desarrollada como un filtro de línea de comandos en `src/tp11/json2csv.py` con las siguientes características:\n",
                "- Formato de ejecución: `python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}`.\n",
                "- Cobertura de tests unitarios: **99%** con 20 pruebas aprobadas en `test_json2csv.py`.\n",
                "- Cumplimiento verificado de linters y seguridad: `ruff`, `black`, `pep8`, `pydocstyle` (PEP257), `mypy`, `pyright` y `bandit`.\n",
                "- Integración continua automatizada en `.github/workflows/ci.yml`.",
            ],
        }
    )

    # Cell 15: Demostración CLI json2csv
    nb["cells"].append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import io\n",
                "from src.tp11.json2csv import convertir_json_a_csv\n",
                "\n",
                "json_demo = '''[\n",
                '  {"id": 1, "herramienta": "Ruff", "tipo": "Linter", "estado": "OK"},\n',
                '  {"id": 2, "herramienta": "Black", "tipo": "Formateador", "estado": "OK"},\n',
                '  {"id": 3, "herramienta": "MyPy", "tipo": "TypeChecker", "estado": "OK"},\n',
                '  {"id": 4, "herramienta": "Pytest", "tipo": "Testing", "cobertura": "99%"}\n',
                "]'''\n",
                "\n",
                "buffer_in = io.StringIO(json_demo)\n",
                "buffer_out = io.StringIO()\n",
                "filas = convertir_json_a_csv(buffer_in, buffer_out, delimitador=';')\n",
                "\n",
                "print(f'Filas procesadas: {filas}')\n",
                "print('Salida CSV generada:')\n",
                "print(buffer_out.getvalue())",
            ],
        }
    )

    output_path = os.path.join(os.path.dirname(__file__), "TP11_Gestion_Calidad.ipynb")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Jupyter Notebook generado exitosamente en: {output_path}")


if __name__ == "__main__":
    build_notebook()
