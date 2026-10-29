"""Módulo de Modelado y Simulación del Caso de Estudio TIC (ISO 27000 / SGSI).

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
class ProyectoMejora:
    """Representa uno de los 13 proyectos de mejora del Caso de Estudio TIC."""

    id_proyecto: str
    nombre: str
    coste_implementacion: float
    coste_mantenimiento: float
    duracion_semanas: int
    fecha_inicio: str
    fecha_fin: str

    @property
    def porcentaje_capex(self) -> float:
        """Porcentaje relativo sobre el CAPEX total de 401.760 €."""
        return (self.coste_implementacion / 401760.0) * 100.0

    @property
    def porcentaje_opex(self) -> float:
        """Porcentaje relativo sobre el OPEX total de 167.000 €."""
        return (self.coste_mantenimiento / 167000.0) * 100.0


class CasoEstudioTIC:
    """Modela y analiza los indicadores técnicos y financieros del Caso TIC."""

    def __init__(self) -> None:
        """Inicializa la cartera de proyectos y los datos de cumplimiento diferencial."""
        self.proyectos: List[ProyectoMejora] = [
            ProyectoMejora(
                "PR01",
                "Copias de Seguridad",
                34640.0,
                10440.0,
                8,
                "01/09/2016",
                "26/10/2016",
            ),
            ProyectoMejora(
                "PR02",
                "Organización y Clasificación de Información",
                2480.0,
                4000.0,
                8,
                "15/09/2016",
                "09/11/2016",
            ),
            ProyectoMejora(
                "PR03",
                "Baseline Software y Hardware",
                4640.0,
                6400.0,
                12,
                "15/11/2016",
                "06/02/2017",
            ),
            ProyectoMejora(
                "PR04",
                "Plan de Continuidad de Negocio",
                16000.0,
                7200.0,
                24,
                "15/02/2017",
                "01/08/2017",
            ),
            ProyectoMejora(
                "PR05",
                "Política de Seguridad de la Información",
                4560.0,
                9600.0,
                10,
                "01/12/2016",
                "08/02/2017",
            ),
            ProyectoMejora(
                "PR06",
                "Política de Control de Acceso",
                36200.0,
                6240.0,
                20,
                "01/05/2017",
                "15/09/2017",
            ),
            ProyectoMejora(
                "PR07",
                "Políticas de Actualización",
                3200.0,
                4640.0,
                4,
                "15/02/2017",
                "14/03/2017",
            ),
            ProyectoMejora(
                "PR08",
                "Programa de Formación Continua",
                27280.0,
                27280.0,
                8,
                "01/09/2016",
                "26/10/2016",
            ),
            ProyectoMejora(
                "PR09",
                "Seguridad en Recursos Humanos (RRHH)",
                3200.0,
                4800.0,
                8,
                "02/10/2017",
                "24/11/2017",
            ),
            ProyectoMejora(
                "PR10",
                "Gestión Incidentes, SIEM, Logs & Threat Intel",
                251000.0,
                69600.0,
                60,
                "03/04/2017",
                "25/05/2018",
            ),
            ProyectoMejora(
                "PR11",
                "Gestión de Activos Empresa y Empleados",
                9600.0,
                8800.0,
                20,
                "01/03/2017",
                "18/07/2017",
            ),
            ProyectoMejora(
                "PR12",
                "Gestión de Proveedores",
                7360.0,
                6400.0,
                12,
                "01/05/2018",
                "23/07/2018",
            ),
            ProyectoMejora(
                "PR13",
                "Cumplimiento Legal y Propiedad Intelectual",
                1600.0,
                1600.0,
                4,
                "02/05/2017",
                "29/05/2017",
            ),
        ]

        # Datos del Análisis Diferencial ISO 27002 (Dominios A.5 a A.18)
        self.dominios_iso27002: List[str] = [
            "A.5 Políticas",
            "A.6 Organización",
            "A.7 RRHH",
            "A.8 Activos",
            "A.9 Accesos",
            "A.10 Cripto",
            "A.11 Física",
            "A.12 Operaciones",
            "A.13 Comunicaciones",
            "A.14 Desarrollo",
            "A.15 Proveedores",
            "A.16 Incidentes",
            "A.17 Continuidad",
            "A.18 Cumplimiento",
        ]

        self.cumplimiento_ex_ante: List[float] = [
            0.10,
            0.15,
            0.20,
            0.25,
            0.15,
            0.05,
            0.35,
            0.08,
            0.25,
            0.70,
            0.10,
            0.05,
            0.02,
            0.30,
        ]

        self.cumplimiento_ex_post: List[float] = [
            0.95,
            0.90,
            0.92,
            0.90,
            0.95,
            0.88,
            0.90,
            0.92,
            0.94,
            0.98,
            0.88,
            0.92,
            0.85,
            0.95,
        ]

    @property
    def total_capex(self) -> float:
        """Suma de los costos de implementación de todos los proyectos."""
        return sum(p.coste_implementacion for p in self.proyectos)

    @property
    def total_opex(self) -> float:
        """Suma de los costos anuales de mantenimiento de todos los proyectos."""
        return sum(p.coste_mantenimiento for p in self.proyectos)

    def generar_reporte_proyectos(self) -> str:
        """Genera una tabla en texto plano del desglose financiero de proyectos."""
        lineas = []
        lineas.append("=" * 110)
        lineas.append(
            f"{'ID':<6} | {'Proyecto':<42} | {'Coste Impl. (€)':<16} | {'% CAPEX':<9} | {'Coste Mant. (€)':<16} | {'% OPEX'}"
        )
        lineas.append("=" * 110)
        for p in self.proyectos:
            lineas.append(
                f"{p.id_proyecto:<6} | {p.nombre:<42} | {p.coste_implementacion:>14,.2f} € | "
                f"{p.porcentaje_capex:>7.2f}% | {p.coste_mantenimiento:>14,.2f} € | {p.porcentaje_opex:>6.2f}%"
            )
        lineas.append("=" * 110)
        lineas.append(
            f"{'TOTAL':<6} | {'INVERSIÓN TOTAL DE LA CARTERA TIC':<42} | {self.total_capex:>14,.2f} € | "
            f"{'100.00%':<9} | {self.total_opex:>14,.2f} € | {'100.00%'}"
        )
        lineas.append("=" * 110)
        return "\n".join(lineas)

    def exportar_grafico_costes(self, output_path: str = "costes_proyectos_tic.png") -> str:
        """Genera un gráfico comparativo de barras apiladas o agrupadas para CAPEX vs OPEX."""
        fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

        ids = [p.id_proyecto for p in self.proyectos]
        capex = [p.coste_implementacion for p in self.proyectos]
        opex = [p.coste_mantenimiento for p in self.proyectos]

        x = np.arange(len(ids))
        width = 0.38

        rects1 = ax.bar(x - width / 2, capex, width, label="Coste Implementación (CAPEX)", color="#2980b9")
        rects2 = ax.bar(x + width / 2, opex, width, label="Coste Mantenimiento Anual (OPEX)", color="#e67e22")

        ax.set_ylabel("Costo en Euros (€)", fontsize=11, fontweight="bold")
        ax.set_title(
            "Caso de Estudio TIC: Desglose Económico de Proyectos (PR01 - PR13)\nInversión Total: 401.760 € CAPEX | 167.000 € OPEX",
            fontsize=12,
            fontweight="bold",
            pad=14,
        )
        ax.set_xticks(x)
        ax.set_xticklabels(ids, fontsize=10, fontweight="bold")
        ax.legend(fontsize=10, loc="upper right")
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        # Destacar PR10 con una anotación
        pr10_idx = ids.index("PR10")
        ax.annotate(
            f"PR10: SIEM, Incidentes & Threat Intel\n{capex[pr10_idx]:,.0f} € (62.5% del CAPEX)",
            xy=(pr10_idx - width / 2, capex[pr10_idx]),
            xytext=(pr10_idx - 3.2, capex[pr10_idx] * 0.85),
            arrowprops=dict(facecolor="#c0392b", shrink=0.05, width=1.5, headwidth=8),
            fontsize=9,
            fontweight="bold",
            color="#922b21",
            bbox=dict(boxstyle="round,pad=0.3", fc="#fadbd8", ec="#c0392b", alpha=0.9),
        )

        plt.tight_layout()
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()
        return output_path

    def exportar_grafico_radar(self, output_path: str = "radar_cumplimiento_tic.png") -> str:
        """Genera el gráfico Radar / Araña comparativo Ex-Ante vs Ex-Post."""
        num_vars = len(self.dominios_iso27002)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Cerrar el círculo del radar
        angles += angles[:1]
        ex_ante = self.cumplimiento_ex_ante + self.cumplimiento_ex_ante[:1]
        ex_post = self.cumplimiento_ex_post + self.cumplimiento_ex_post[:1]
        deseado = [1.0] * num_vars + [1.0]

        fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True), dpi=300)

        # Ajuste visual
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        plt.xticks(angles[:-1], self.dominios_iso27002, fontsize=9, fontweight="bold", color="#2c3e50")
        ax.set_rlabel_position(0)
        plt.yticks(
            [0.2, 0.4, 0.6, 0.8, 1.0],
            ["20%", "40%", "60%", "80%", "100%"],
            color="#7f8c8d",
            size=8,
        )
        plt.ylim(0, 1.05)

        # Curva Deseada (Línea punteada azul suave)
        ax.plot(angles, deseado, linewidth=1.5, linestyle=":", color="#3498db", label="Nivel Deseado (100%)")

        # Curva Ex-Ante (Negro / Gris oscuro con sombreado tenue)
        ax.plot(
            angles,
            ex_ante,
            linewidth=2,
            linestyle="solid",
            color="#2c3e50",
            label="Ex-Ante (Diagnóstico Inicial)",
        )
        ax.fill(angles, ex_ante, color="#2c3e50", alpha=0.15)

        # Curva Ex-Post (Rojo carmesí / Burdeos con sombreado)
        ax.plot(
            angles,
            ex_post,
            linewidth=2.5,
            linestyle="solid",
            color="#e74c3c",
            label="Ex-Post (Tras Implementación SGSI)",
        )
        ax.fill(angles, ex_post, color="#e74c3c", alpha=0.25)

        plt.title(
            "Caso de Estudio TIC: Análisis Diferencial Ex-Ante / Ex-Post (ISO 27002)\nEvolución de Conformidad por Dominio",
            fontsize=12,
            fontweight="bold",
            pad=25,
        )
        plt.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), fontsize=9, frameon=True)

        plt.tight_layout()
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()
        return output_path


def main() -> None:
    """Punto de entrada de prueba."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caso = CasoEstudioTIC()
    print(caso.generar_reporte_proyectos())

    costes_path = os.path.join(base_dir, "costes_proyectos_tic.png")
    radar_path = os.path.join(base_dir, "radar_cumplimiento_tic.png")

    g1 = caso.exportar_grafico_costes(costes_path)
    g2 = caso.exportar_grafico_radar(radar_path)
    print(f"\n[OK] Gráfico de costes exportado en: {g1}")
    print(f"[OK] Gráfico radar exportado en: {g2}")


if __name__ == "__main__":
    main()
