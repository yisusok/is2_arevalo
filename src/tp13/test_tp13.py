"""Suite de Pruebas Automatizadas para el TP13 (ISO 27000 / SGSI).

Asignatura: Ingeniería de Software II
Docente: Dr. Pedro E. Colla
Institución: Facultad de Ciencia y Tecnología (FCyT) - UADER
Alumno: Jesús Arévalo
Módulo: TP13 - Estándar ISO 27000
"""

import os
import pytest
from src.tp13.evaluacion_riesgo import RiesgoFactor, MatrizRiesgo
from src.tp13.caso_estudio_tic import CasoEstudioTIC, ProyectoMejora


def test_clasificacion_apetito_riesgo():
    """Valida los umbrales de apetito de riesgo según la consigna."""
    # Aceptable <= 6
    assert RiesgoFactor.clasificar_nivel(1) == "Aceptable"
    assert RiesgoFactor.clasificar_nivel(4) == "Aceptable"
    assert RiesgoFactor.clasificar_nivel(6) == "Aceptable"

    # Tolerable con PTR: 7 a 12
    assert RiesgoFactor.clasificar_nivel(7) == "Tolerable con PTR"
    assert RiesgoFactor.clasificar_nivel(9) == "Tolerable con PTR"
    assert RiesgoFactor.clasificar_nivel(10) == "Tolerable con PTR"
    assert RiesgoFactor.clasificar_nivel(12) == "Tolerable con PTR"

    # Inaceptable >= 15
    assert RiesgoFactor.clasificar_nivel(15) == "Inaceptable (Accionar Inmediato)"
    assert RiesgoFactor.clasificar_nivel(16) == "Inaceptable (Accionar Inmediato)"
    assert RiesgoFactor.clasificar_nivel(20) == "Inaceptable (Accionar Inmediato)"
    assert RiesgoFactor.clasificar_nivel(25) == "Inaceptable (Accionar Inmediato)"


def test_matriz_particion_matematica():
    """Demuestra que la escala 5x5 no posee productos en el rango hueco {13, 14}."""
    productos_posibles = set()
    for p in range(1, 6):
        for i in range(1, 6):
            prod = p * i
            productos_posibles.add(prod)
            # Todo valor debe pertenecer a uno de los tres intervalos
            assert prod <= 6 or (7 <= prod <= 12) or prod >= 15

    # 13 y 14 no son factorizables por factores enteros en [1, 5]
    assert 13 not in productos_posibles
    assert 14 not in productos_posibles


def test_riesgos_factores_consigna():
    """Verifica los valores asignados a los 5 riesgos R-01 a R-05."""
    matriz = MatrizRiesgo.obtener_riesgos_consigna()
    assert len(matriz.riesgos) == 5

    r_map = {r.id_riesgo: r for r in matriz.riesgos}

    # R-01 DB alumnos Ransomware
    assert r_map["R-01"].riesgo_inherente == 20
    assert r_map["R-01"].clasificar_nivel(r_map["R-01"].riesgo_inherente) == "Inaceptable (Accionar Inmediato)"
    assert r_map["R-01"].riesgo_residual == 6
    assert r_map["R-01"].clasificar_nivel(r_map["R-01"].riesgo_residual) == "Aceptable"

    # R-02 LMS DDoS
    assert r_map["R-02"].riesgo_inherente == 16
    assert r_map["R-02"].clasificar_nivel(r_map["R-02"].riesgo_inherente) == "Inaceptable (Accionar Inmediato)"
    assert r_map["R-02"].riesgo_residual == 4
    assert r_map["R-02"].clasificar_nivel(r_map["R-02"].riesgo_residual) == "Aceptable"

    # R-03 Email Phishing
    assert r_map["R-03"].riesgo_inherente == 15
    assert r_map["R-03"].clasificar_nivel(r_map["R-03"].riesgo_inherente) == "Inaceptable (Accionar Inmediato)"
    assert r_map["R-03"].riesgo_residual == 4
    assert r_map["R-03"].clasificar_nivel(r_map["R-03"].riesgo_residual) == "Aceptable"

    # R-04 SIU Interrupción eléctrica
    assert r_map["R-04"].riesgo_inherente == 9
    assert r_map["R-04"].clasificar_nivel(r_map["R-04"].riesgo_inherente) == "Tolerable con PTR"
    assert r_map["R-04"].riesgo_residual == 2
    assert r_map["R-04"].clasificar_nivel(r_map["R-04"].riesgo_residual) == "Aceptable"

    # R-05 Doc repositorio Fuga PII
    assert r_map["R-05"].riesgo_inherente == 16
    assert r_map["R-05"].clasificar_nivel(r_map["R-05"].riesgo_inherente) == "Inaceptable (Accionar Inmediato)"
    assert r_map["R-05"].riesgo_residual == 4
    assert r_map["R-05"].clasificar_nivel(r_map["R-05"].riesgo_residual) == "Aceptable"


def test_caso_estudio_tic_totales():
    """Verifica la coherencia financiera y de proyectos del Caso TIC."""
    caso = CasoEstudioTIC()
    assert len(caso.proyectos) == 13

    # Total CAPEX: 401.760 €
    assert caso.total_capex == pytest.approx(401760.0, rel=1e-4)

    # Total OPEX: 167.000 €
    assert caso.total_opex == pytest.approx(167000.0, rel=1e-4)

    # PR10 debe ser el mayor proyecto
    pr10 = next(p for p in caso.proyectos if p.id_proyecto == "PR10")
    assert pr10.coste_implementacion == 251000.0
    assert pr10.coste_mantenimiento == 69600.0
    assert pr10.duracion_semanas == 60
    assert pr10.porcentaje_capex > 62.0


def test_generacion_reportes_y_graficos(tmp_path):
    """Valida la generación de reportes de texto y renderizado de gráficos."""
    matriz = MatrizRiesgo.obtener_riesgos_consigna()
    reporte_riesgo = matriz.generar_reporte_texto()
    assert "R-01" in reporte_riesgo
    assert "Ransomware" in reporte_riesgo

    img_riesgo = tmp_path / "test_heatmap.png"
    matriz.exportar_mapa_calor(str(img_riesgo))
    assert img_riesgo.exists()
    assert img_riesgo.stat().st_size > 10000

    caso = CasoEstudioTIC()
    reporte_tic = caso.generar_reporte_proyectos()
    assert "401,760.00" in reporte_tic
    assert "PR10" in reporte_tic

    img_costes = tmp_path / "test_costes.png"
    caso.exportar_grafico_costes(str(img_costes))
    assert img_costes.exists()
    assert img_costes.stat().st_size > 10000

    img_radar = tmp_path / "test_radar.png"
    caso.exportar_grafico_radar(str(img_radar))
    assert img_radar.exists()
    assert img_radar.stat().st_size > 10000
