"""Suite de pruebas unitarias y de integración para la lógica del TP12.

Asignatura: Ingeniería de Software II (FCyT - UADER)
Docente: Dr. Pedro E. Colla
Alumno: Jesús Arévalo
Ubicación: src/tp12/
"""

import pytest
from simulador_embebido import (
    CircuitConfig,
    EmuladorArduinoTP12,
    adc_to_voltage,
    voltage_to_adc,
)


def test_adc_quantization_limits():
    """Verifica los límites de cuantización del ADC de 10 bits (0 a 1023)."""
    assert voltage_to_adc(0.0) == 0
    assert voltage_to_adc(5.0) == 1023
    assert voltage_to_adc(-1.0) == 0  # Clamp inferior
    assert voltage_to_adc(6.0) == 1023  # Clamp superior


def test_adc_quantization_midpoints():
    """Verifica la cuantización para tensiones intermedias (50% y 25%)."""
    # 50% de 5V = 2.5V -> 1023 * 0.5 = 511.5 -> redondeo a 511 o 512
    adc_mid = voltage_to_adc(2.5)
    assert adc_mid in (511, 512)

    # 25% de 5V = 1.25V -> 1023 * 0.25 = 255.75 -> 256
    adc_quarter = voltage_to_adc(1.25)
    assert adc_quarter in (255, 256)


def test_adc_voltage_reconstruction():
    """Verifica la conversión inversa de cuentas a voltios."""
    assert pytest.approx(adc_to_voltage(0), abs=1e-3) == 0.0
    assert pytest.approx(adc_to_voltage(1023), abs=1e-3) == 5.0
    assert pytest.approx(adc_to_voltage(511), abs=0.01) == 2.50
    assert pytest.approx(adc_to_voltage(255), abs=0.01) == 1.25


def test_circuit_config_lsb_resolution():
    """Verifica la resolución por LSB del convertidor (aprox 4.88 mV)."""
    cfg = CircuitConfig()
    expected_lsb = 5.0 / 1023.0
    assert pytest.approx(cfg.lsb_voltage, abs=1e-5) == expected_lsb
    assert 0.0048 < cfg.lsb_voltage < 0.0049


def test_emulador_modo_base_boton_presionado():
    """Verifica la lógica en Modo Base (Umbral 50% = 2.5V, ADC <= 511)."""
    cfg = CircuitConfig(umbral_ratio=0.50)
    emu = EmuladorArduinoTP12(cfg)

    # Caso 1: Tensión 1.0 V (<= 2.5V) -> Debe activar LED permanente
    res1 = emu.evaluar_ciclo(button_pressed=True, pot_voltage=1.0)
    assert res1["activado"] is True
    assert res1["led_modo"] == "PERMANENTE_ON"

    # Caso 2: Tensión 2.5 V (límite exacto de 50%) -> Activado
    res2 = emu.evaluar_ciclo(button_pressed=True, pot_voltage=2.5)
    assert res2["activado"] is True
    assert res2["led_modo"] == "PERMANENTE_ON"

    # Caso 3: Tensión 3.5 V (> 2.5V) -> No activado, LED debe parpadear
    res3 = emu.evaluar_ciclo(button_pressed=True, pot_voltage=3.5)
    assert res3["activado"] is False
    assert res3["led_modo"] == "PARPADEO"

    # Caso 4: Tensión 5.0 V -> No activado, LED parpadea
    res4 = emu.evaluar_ciclo(button_pressed=True, pot_voltage=5.0)
    assert res4["activado"] is False
    assert res4["led_modo"] == "PARPADEO"


def test_emulador_modo_base_boton_en_reposo():
    """Verifica que si el botón no está presionado, el LED parpadea independientemente del potenciómetro."""
    cfg = CircuitConfig(umbral_ratio=0.50)
    emu = EmuladorArduinoTP12(cfg)

    for v in [0.0, 1.25, 2.50, 4.0, 5.0]:
        res = emu.evaluar_ciclo(button_pressed=False, pot_voltage=v)
        assert res["activado"] is False
        assert res["led_modo"] == "PARPADEO"


def test_emulador_modificacion_c_25pct():
    """Verifica la Modificación (c): Umbral al 25% de la tensión total (<= 1.25V)."""
    cfg_c = CircuitConfig(umbral_ratio=0.25)
    emu_c = EmuladorArduinoTP12(cfg_c)

    assert cfg_c.umbral_adc == 255
    assert pytest.approx(cfg_c.umbral_voltage, abs=1e-2) == 1.25

    # Tensión 0.8 V (<= 1.25V) -> Activa LED
    res1 = emu_c.evaluar_ciclo(button_pressed=True, pot_voltage=0.8)
    assert res1["activado"] is True
    assert res1["led_modo"] == "PERMANENTE_ON"

    # Tensión 1.24 V (<= 1.25V) -> Activa LED
    res2 = emu_c.evaluar_ciclo(button_pressed=True, pot_voltage=1.24)
    assert res2["activado"] is True

    # Tensión 2.0 V (> 1.25V, aunque menor al 50%) -> NO debe activar en Mod C
    res3 = emu_c.evaluar_ciclo(button_pressed=True, pot_voltage=2.0)
    assert res3["activado"] is False
    assert res3["led_modo"] == "PARPADEO"

    # Tensión 2.5 V (era activa en modo base, ahora NO debe activar)
    res4 = emu_c.evaluar_ciclo(button_pressed=True, pot_voltage=2.5)
    assert res4["activado"] is False
    assert res4["led_modo"] == "PARPADEO"


def test_cronogramas_temporales():
    """Verifica los períodos y ciclo de trabajo de los parpadeos en Mod A y Mod B."""
    # Mod A: Parpadeo cada 5 segundos (período = 5000 ms)
    cfg_a = CircuitConfig(periodo_parpadeo_ms=5000.0)
    emu_a = EmuladorArduinoTP12(cfg_a)
    t_a, onda_a = emu_a.generar_cronograma_parpadeo(duracion_total_s=10.0, paso_ms=10.0)
    assert len(t_a) == len(onda_a)
    # Ciclo de trabajo aproximado 50%
    duty_a = onda_a.mean()
    assert pytest.approx(duty_a, abs=0.05) == 0.50

    # Mod B: Parpadeo cada 1 segundo (período = 1000 ms)
    cfg_b = CircuitConfig(periodo_parpadeo_ms=1000.0)
    emu_b = EmuladorArduinoTP12(cfg_b)
    _, onda_b = emu_b.generar_cronograma_parpadeo(duracion_total_s=10.0, paso_ms=10.0)
    duty_b = onda_b.mean()
    assert pytest.approx(duty_b, abs=0.05) == 0.50
