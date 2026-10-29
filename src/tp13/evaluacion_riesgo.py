"""Módulo de Evaluación de Riesgos y Generación de Mapa de Calor.

Asignatura: Ingeniería de Software II
Docente: Dr. Pedro E. Colla
Institución: Facultad de Ciencia y Tecnología (FCyT) - UADER
Alumno: Jesús Arévalo
Módulo: TP13 - Estándar ISO 27000
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class RiesgoFactor:
    """Representa un escenario de riesgo tecnológico o de seguridad."""

    id_riesgo: str
    activo_proceso: str
    amenaza: str
    vulnerabilidad: str
    prob_inherente: int
    imp_inherente: int
    salvaguardas_notas: str
    prob_residual: int
    imp_residual: int

    @property
    def riesgo_inherente(self) -> int:
        """Calcula el riesgo inherente (P * I)."""
        return self.prob_inherente * self.imp_inherente

    @property
    def riesgo_residual(self) -> int:
        """Calcula el riesgo residual tras salvaguardas (Pres * Ires)."""
        return self.prob_residual * self.imp_residual

    @classmethod
    def clasificar_nivel(cls, valor_riesgo: int) -> str:
        """Clasifica el nivel de riesgo según los umbrales de apetito de riesgo."""
        if valor_riesgo <= 6:
            return "Aceptable"
        elif 7 <= valor_riesgo <= 12:
            return "Tolerable con PTR"
        else:
            return "Inaceptable (Accionar Inmediato)"


class MatrizRiesgo:
    """Gestiona el conjunto de riesgos evaluados y la generación del mapa de calor."""

    def __init__(self, riesgos: List[RiesgoFactor]) -> None:
        """Inicializa la matriz con una lista de factores de riesgo."""
        self.riesgos = riesgos

    @classmethod
    def obtener_riesgos_consigna(cls) -> MatrizRiesgo:
        """Construye los 5 factores de riesgo especificados en la consigna del TP13."""
        riesgos = [
            RiesgoFactor(
                id_riesgo="R-01",
                activo_proceso="DB alumnos",
                amenaza="Ransomware",
                vulnerabilidad="Parches atrasados",
                prob_inherente=4,
                imp_inherente=5,
                salvaguardas_notas="Crítico; planes BRS/backup inmutable + gestión de parches",
                prob_residual=2,
                imp_residual=3,
            ),
            RiesgoFactor(
                id_riesgo="R-02",
                activo_proceso="LMS (Campus Virtual)",
                amenaza="DDoS",
                vulnerabilidad="Sin Firewall",
                prob_inherente=4,
                imp_inherente=4,
                salvaguardas_notas="Mitigar con Firewall / WAF perimetral + Anti-DDoS + Rate Limiting",
                prob_residual=2,
                imp_residual=2,
            ),
            RiesgoFactor(
                id_riesgo="R-03",
                activo_proceso="Email Institucional",
                amenaza="Phishing",
                vulnerabilidad="Conciencia baja",
                prob_inherente=5,
                imp_inherente=3,
                salvaguardas_notas="Campañas de concientización + 2FA obligatorio + DMARC/SPF/DKIM",
                prob_residual=2,
                imp_residual=2,
            ),
            RiesgoFactor(
                id_riesgo="R-04",
                activo_proceso="SIU Guaraní",
                amenaza="Interrupción eléctrica",
                vulnerabilidad="Redundancia limitada",
                prob_inherente=3,
                imp_inherente=3,
                salvaguardas_notas="UPS online de doble conversión + Grupo electrógeno de arranque automático",
                prob_residual=2,
                imp_residual=1,
            ),
            RiesgoFactor(
                id_riesgo="R-05",
                activo_proceso="Doc repositorio",
                amenaza="Fuga PII",
                vulnerabilidad="Acceso laxo",
                prob_inherente=4,
                imp_inherente=4,
                salvaguardas_notas="RBAC (Control por roles) + DLP (Prevención de fuga) + Clasificación formal",
                prob_residual=2,
                imp_residual=2,
            ),
        ]
        return cls(riesgos)

    def generar_reporte_texto(self) -> str:
        """Genera un reporte formateado en texto plano/Markdown."""
        lineas = []
        lineas.append("=" * 115)
        lineas.append(
            f"{'ID':<6} | {'Activo/Proceso':<20} | {'Amenaza':<15} | {'Vuln.':<18} | {'P':<3} | {'I':<3} | {'R_Inh':<6} | {'Nivel Inh.':<18} | {'R_Res':<6} | {'Nivel Res.'}"
        )
        lineas.append("=" * 115)
        for r in self.riesgos:
            lineas.append(
                f"{r.id_riesgo:<6} | {r.activo_proceso:<20} | {r.amenaza:<15} | {r.vulnerabilidad:<18} | "
                f"{r.prob_inherente:<3} | {r.imp_inherente:<3} | {r.riesgo_inherente:<6} | {r.clasificar_nivel(r.riesgo_inherente):<18} | "
                f"{r.riesgo_residual:<6} | {r.clasificar_nivel(r.riesgo_residual)}"
            )
        lineas.append("=" * 115)
        return "\n".join(lineas)

    def exportar_mapa_calor(self, output_path: str = "mapa_calor_riesgos.png") -> str:
        """Genera un gráfico del mapa de calor de riesgos 5x5 con trazabilidad antes/después."""
        fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

        # Matriz 5x5: eje Y = Probabilidad (1 a 5), eje X = Impacto (1 a 5)
        # Se genera matriz numérica de valores de riesgo R = P * I
        valores = np.zeros((5, 5), dtype=int)
        for p in range(1, 6):
            for i in range(1, 6):
                # Matriz con Y invertido para plot (Fila 0 = Probabilidad 5, Fila 4 = Probabilidad 1)
                valores[5 - p, i - 1] = p * i

        # Mapa de colores personalizado según apetito de riesgo:
        # <= 6: Verde suave (#a8e6cf)
        # 7-12: Amarillo / Naranja suave (#ffd3b6)
        # >= 15: Rojo suave (#ffaaa5)
        color_matrix = np.zeros((5, 5, 4))
        for r_idx in range(5):
            for c_idx in range(5):
                val = valores[r_idx, c_idx]
                if val <= 6:
                    color_matrix[r_idx, c_idx] = [0.45, 0.82, 0.55, 0.85]  # Verde
                elif 7 <= val <= 12:
                    color_matrix[r_idx, c_idx] = [0.98, 0.78, 0.35, 0.85]  # Amarillo/Naranja
                else:
                    color_matrix[r_idx, c_idx] = [0.94, 0.42, 0.42, 0.85]  # Rojo

        ax.imshow(color_matrix, origin="upper", extent=[0.5, 5.5, 0.5, 5.5])

        # Agregar los valores numéricos y texto en cada celda
        for p in range(1, 6):
            for i in range(1, 6):
                val = p * i
                ax.text(
                    i,
                    p,
                    f"{val}",
                    ha="center",
                    va="center",
                    color="#1a1a1a",
                    fontsize=13,
                    fontweight="bold",
                    alpha=0.6,
                )

        # Plotear los puntos de riesgo inherente y residual con flechas
        # Para evitar superposiciones si coinciden coordenadas, aplicamos un leve jitter visual
        jitter_map: Dict[str, Tuple[float, float]] = {
            "R-01": (0.0, 0.0),
            "R-02": (-0.12, 0.08),
            "R-03": (0.0, 0.0),
            "R-04": (0.0, 0.0),
            "R-05": (0.12, -0.08),
        }

        for r in self.riesgos:
            jx, jy = jitter_map.get(r.id_riesgo, (0.0, 0.0))
            x_inh, y_inh = r.imp_inherente + jx, r.prob_inherente + jy
            x_res, y_res = r.imp_residual + jx, r.prob_residual + jy

            # Punto Inherente (Círculo rojo relleno con borde oscuro)
            ax.scatter(
                x_inh,
                y_inh,
                color="#c0392b",
                s=200,
                edgecolors="#2c3e50",
                linewidths=2,
                zorder=5,
            )
            ax.annotate(
                f"{r.id_riesgo} (Inh)",
                (x_inh, y_inh),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
                fontsize=9,
                fontweight="bold",
                color="#78281f",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#c0392b", alpha=0.9),
                zorder=6,
            )

            # Punto Residual (Cuadrado verde con borde oscuro)
            ax.scatter(
                x_res,
                y_res,
                color="#27ae60",
                s=180,
                marker="s",
                edgecolors="#196f3d",
                linewidths=2,
                zorder=5,
            )
            ax.annotate(
                f"{r.id_riesgo} (Res)",
                (x_res, y_res),
                textcoords="offset points",
                xytext=(0, -15),
                ha="center",
                fontsize=9,
                fontweight="bold",
                color="#145a32",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#27ae60", alpha=0.9),
                zorder=6,
            )

            # Flecha de transición de tratamiento de riesgo
            ax.annotate(
                "",
                xy=(x_res, y_res),
                xytext=(x_inh, y_inh),
                arrowprops=dict(
                    arrowstyle="->",
                    color="#2c3e50",
                    lw=2,
                    ls="--",
                    shrinkA=10,
                    shrinkB=10,
                ),
                zorder=4,
            )

        # Configuraciones de ejes y etiquetas
        ax.set_xticks(range(1, 6))
        ax.set_yticks(range(1, 6))
        ax.set_xticklabels(
            [
                "1: Menor\n(Sin impacto)",
                "2: Bajo\n(<1 día)",
                "3: Moderado\n(1-2 días)",
                "4: Mayor\n(3-6 días)",
                "5: Catastrófico\n(≥1 sem.)",
            ],
            fontsize=9,
        )
        ax.set_yticklabels(
            [
                "1: Muy baja\n(≤1/5 años)",
                "2: Baja\n(1/2-3 años)",
                "3: Media\n(1/año)",
                "4: Alta\n(1/trimestre)",
                "5: Crítica\n(≥1/mes)",
            ],
            fontsize=9,
        )

        ax.set_xlabel("Impacto (I)", fontsize=12, fontweight="bold", labelpad=10)
        ax.set_ylabel("Probabilidad (P)", fontsize=12, fontweight="bold", labelpad=10)
        ax.set_title(
            "TP13: Mapa de Calor de Evaluación de Riesgos (ISO 27000 / SGSI)\nTrazabilidad de Riesgo Inherente a Residual tras Salvaguardas",
            fontsize=13,
            fontweight="bold",
            pad=18,
        )

        # Leyenda de Apetito de Riesgo
        from matplotlib.patches import Patch

        legend_elements = [
            Patch(facecolor="#73d28c", edgecolor="#27ae60", label="Riesgo Aceptable (R ≤ 6)"),
            Patch(facecolor="#f9c759", edgecolor="#d68910", label="Riesgo Tolerable con PTR (7 ≤ R ≤ 12)"),
            Patch(facecolor="#f06b6b", edgecolor="#c0392b", label="Riesgo Inaceptable (R ≥ 15)"),
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor="#c0392b",
                markersize=10,
                label="Riesgo Inherente (Inicial)",
            ),
            plt.Line2D(
                [0],
                [0],
                marker="s",
                color="w",
                markerfacecolor="#27ae60",
                markersize=10,
                label="Riesgo Residual (Mitigado)",
            ),
            plt.Line2D([0], [0], color="#2c3e50", lw=2, ls="--", label="Mitigación con Salvaguarda"),
        ]
        ax.legend(
            handles=legend_elements,
            loc="upper left",
            bbox_to_anchor=(1.02, 1),
            borderaxespad=0.0,
            frameon=True,
            fontsize=9,
        )

        ax.grid(color="white", linestyle="-", linewidth=1.5, alpha=0.7)
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()
        return output_path


def main() -> None:
    """Punto de entrada para ejecución directa."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_png = os.path.join(base_dir, "mapa_calor_riesgos.png")
    matriz = MatrizRiesgo.obtener_riesgos_consigna()
    print(matriz.generar_reporte_texto())
    grafico = matriz.exportar_mapa_calor(output_png)
    print(f"\n[OK] Mapa de calor exportado exitosamente en: {grafico}")


if __name__ == "__main__":
    main()
