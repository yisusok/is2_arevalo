"""Simulador del comportamiento de hardware y firmware para Arduino Uno (TP12).

Asignatura: Ingeniería de Software II (FCyT - UADER)
Docente: Dr. Pedro E. Colla
Alumno: Jesús Arévalo
Ubicación: src/tp12/
"""

import os
from dataclasses import dataclass
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np


class LedState(Enum):
    """Estados discretos del LED onboard."""

    LOW = 0
    HIGH = 1


class SystemMode(Enum):
    """Modos operativos contemplados en el TP12."""

    BASE = "Consigna Base (Umbral 50%, Parpadeo 1s)"
    MOD_A_5S = "Modificación A (Parpadeo cada 5s)"
    MOD_B_1S = "Modificación B (Parpadeo cada 1s)"
    MOD_C_25PCT = "Modificación C (Umbral 25%, Parpadeo 1s)"


@dataclass(frozen=True)
class CircuitConfig:
    """Configuración de parámetros eléctricos y temporales del sistema."""

    v_ref: float = 5.0  # Tensión de referencia ADC (Voltios)
    adc_resolution_bits: int = 10  # Resolución del ADC del ATmega328P
    umbral_ratio: float = 0.50  # Fracción de Vcc (0.50 = 50%, 0.25 = 25%)
    periodo_parpadeo_ms: float = 1000.0  # Período completo de parpadeo (ms)
    delay_ciclo_ms: float = 500.0  # Retardo entre lecturas (ms)

    @property
    def max_adc_counts(self) -> int:
        """Cantidad máxima de cuentas del ADC (2^10 - 1 = 1023)."""
        return (1 << self.adc_resolution_bits) - 1

    @property
    def lsb_voltage(self) -> float:
        """Resolución de tensión por LSB (V_ref / 1023)."""
        return self.v_ref / float(self.max_adc_counts)

    @property
    def umbral_adc(self) -> int:
        """Valor umbral entero del ADC."""
        return int(np.floor(self.max_adc_counts * self.umbral_ratio))

    @property
    def umbral_voltage(self) -> float:
        """Tensión umbral analógica en voltios."""
        return self.v_ref * self.umbral_ratio


def voltage_to_adc(voltage: float, v_ref: float = 5.0, bits: int = 10) -> int:
    """Convierte una tensión continua al valor cuantizado de ADC de 10 bits.

    Args:
        voltage: Tensión analógica de entrada (V).
        v_ref: Tensión de referencia (5.0 V).
        bits: Número de bits de cuantización.

    Returns:
        Valor entero entre 0 y 2^bits - 1.
    """
    max_counts = (1 << bits) - 1
    clamped_voltage = max(0.0, min(voltage, v_ref))
    return int(np.floor((clamped_voltage / v_ref) * max_counts))


def adc_to_voltage(adc_val: int, v_ref: float = 5.0, bits: int = 10) -> float:
    """Convierte cuentas de ADC a tensión analógica equivalente.

    Args:
        adc_val: Cuentas enteras de ADC.
        v_ref: Tensión de referencia (V).
        bits: Número de bits de cuantización.

    Returns:
        Tensión analógica estimada en voltios.
    """
    max_counts = (1 << bits) - 1
    clamped_adc = max(0, min(adc_val, max_counts))
    return (clamped_adc * v_ref) / float(max_counts)


class EmuladorArduinoTP12:
    """Emulador de la lógica del firmware Arduino Uno para el TP12."""

    def __init__(self, config: CircuitConfig):
        """Inicializa el emulador con la configuración provista."""
        self.config = config

    def evaluar_ciclo(
        self, button_pressed: bool, pot_voltage: float
    ) -> dict[str, object]:
        """Evalúa un ciclo de ejecución de la función loop().

        Args:
            button_pressed: Booleano indicando si el pulsador está presionado.
            pot_voltage: Tensión analógica presente en el cursor del potenciómetro (A0).

        Returns:
            Diccionario con las variables de estado y la acción tomada.
        """
        adc_val = voltage_to_adc(
            pot_voltage, self.config.v_ref, self.config.adc_resolution_bits
        )
        tension_calc = adc_to_voltage(
            adc_val, self.config.v_ref, self.config.adc_resolution_bits
        )

        if button_pressed:
            activado = adc_val <= self.config.umbral_adc
            if activado:
                led_modo = "PERMANENTE_ON"
                consola_msg = (
                    f"[ACTIVADO] ADC={adc_val} ({tension_calc:.2f}V) "
                    f"<= Umbral ({self.config.umbral_voltage:.2f}V) -> LED SOLID HIGH"
                )
            else:
                led_modo = "PARPADEO"
                consola_msg = (
                    f"[ALERTA] ADC={adc_val} ({tension_calc:.2f}V) "
                    f"> Umbral ({self.config.umbral_voltage:.2f}V) -> LED BLINK"
                )
        else:
            activado = False
            led_modo = "PARPADEO"
            consola_msg = "Boton en reposo -> LED BLINK"

        return {
            "button_pressed": button_pressed,
            "pot_voltage_in": pot_voltage,
            "adc_val": adc_val,
            "tension_calc": tension_calc,
            "umbral_adc": self.config.umbral_adc,
            "umbral_voltage": self.config.umbral_voltage,
            "activado": activado,
            "led_modo": led_modo,
            "consola_msg": consola_msg,
        }

    def generar_cronograma_parpadeo(
        self, duracion_total_s: float = 12.0, paso_ms: float = 20.0
    ) -> tuple[np.ndarray, np.ndarray]:
        """Genera la forma de onda temporal del LED en modo parpadeo."""
        t_arr = np.arange(0, duracion_total_s * 1000.0, paso_ms)
        periodo = self.config.periodo_parpadeo_ms
        semi_periodo = periodo / 2.0

        # En la implementación: LOW durante semi_periodo, luego HIGH durante semi_periodo
        onda_led = np.array(
            [1.0 if (t % periodo) >= semi_periodo else 0.0 for t in t_arr]
        )
        return t_arr / 1000.0, onda_led


def generar_graficos_tp12(output_dir: str) -> list[str]:
    """Genera y guarda gráficos técnicos demostrativos del comportamiento del TP12."""
    os.makedirs(output_dir, exist_ok=True)
    rutas_generadas = []

    # 1. Curva de Transferencia ADC y Zonas de Operación
    fig, ax = plt.subplots(figsize=(9, 5.5))
    v_in = np.linspace(0.0, 5.0, 500)
    adc_curve = [voltage_to_adc(v) for v in v_in]

    ax.plot(
        v_in,
        adc_curve,
        label="Conversión ADC 10-bits ($V_{ref} = 5.0$ V)",
        color="#1f77b4",
        linewidth=2,
    )

    # Umbral 50% (Base, Mod A, Mod B)
    ax.axvline(
        2.5,
        color="#2ca02c",
        linestyle="--",
        linewidth=1.8,
        label="Umbral Base/Mod A/B: 50% ($V_{th}=2.50$ V, ADC=511)",
    )
    ax.axhline(511, color="#2ca02c", linestyle=":", alpha=0.7)

    # Umbral 25% (Mod C)
    ax.axvline(
        1.25,
        color="#d62728",
        linestyle="--",
        linewidth=1.8,
        label="Umbral Mod C: 25% ($V_{th}=1.25$ V, ADC=255)",
    )
    ax.axhline(255, color="#d62728", linestyle=":", alpha=0.7)

    # Regiones coloreadas para Mod C
    ax.axvspan(
        0.0,
        1.25,
        alpha=0.15,
        color="#d62728",
        label="Zona Activa Mod C (LED Fijo si botón presionado)",
    )
    ax.axvspan(
        1.25,
        2.50,
        alpha=0.12,
        color="#2ca02c",
        label="Zona Activa adicional en Modo Base (25% - 50%)",
    )
    ax.axvspan(2.50, 5.0, alpha=0.08, color="#7f7f7f", label="Zona Parpadeo (>50%)")

    ax.set_title(
        "TP12: Curva de Transferencia del ADC y Regiones de Activación del LED",
        fontsize=12,
        fontweight="bold",
    )
    ax.set_xlabel("Tensión de Entrada en Potenciómetro $V_{in}$ [V]", fontsize=11)
    ax.set_ylabel("Cuentas del ADC (10 bits, 0-1023)", fontsize=11)
    ax.set_xlim(0, 5.0)
    ax.set_ylim(0, 1024)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left", fontsize=9)

    ruta_adc = os.path.join(output_dir, "curva_transferencia_adc.png")
    fig.tight_layout()
    fig.savefig(ruta_adc, dpi=200)
    plt.close(fig)
    rutas_generadas.append(ruta_adc)

    # 2. Cronogramas Comparativos de Parpadeo (Mod A: 5s vs Mod B: 1s)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    cfg_mod_a = CircuitConfig(periodo_parpadeo_ms=5000.0)
    emu_mod_a = EmuladorArduinoTP12(cfg_mod_a)
    t_s, onda_a = emu_mod_a.generar_cronograma_parpadeo(
        duracion_total_s=15.0, paso_ms=10.0
    )

    cfg_mod_b = CircuitConfig(periodo_parpadeo_ms=1000.0)
    emu_mod_b = EmuladorArduinoTP12(cfg_mod_b)
    _, onda_b = emu_mod_b.generar_cronograma_parpadeo(
        duracion_total_s=15.0, paso_ms=10.0
    )

    ax1.step(t_s, onda_a, where="post", color="#ff7f0e", linewidth=2, label="LED State")
    ax1.set_title(
        "Modificación (a): Ritmo de Parpadeo cada 5 Segundos ($T = 5.0$ s, $f = 0.2$ Hz)",
        fontsize=11,
        fontweight="bold",
    )
    ax1.set_ylabel("Estado LED (0/1)", fontsize=10)
    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(["LOW (0)", "HIGH (1)"])
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.axvspan(
        2.5,
        5.0,
        alpha=0.15,
        color="#ff7f0e",
        label="Semi-período HIGH (2500 ms)",
    )
    ax1.legend(loc="upper right", fontsize=9)

    ax2.step(t_s, onda_b, where="post", color="#2ca02c", linewidth=2, label="LED State")
    ax2.set_title(
        "Modificación (b) / Base: Ritmo de Parpadeo cada 1 Segundo ($T = 1.0$ s, $f = 1.0$ Hz)",
        fontsize=11,
        fontweight="bold",
    )
    ax2.set_xlabel("Tiempo [segundos]", fontsize=11)
    ax2.set_ylabel("Estado LED (0/1)", fontsize=10)
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(["LOW (0)", "HIGH (1)"])
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.axvspan(
        0.5,
        1.0,
        alpha=0.15,
        color="#2ca02c",
        label="Semi-período HIGH (500 ms)",
    )
    ax2.legend(loc="upper right", fontsize=9)

    ruta_cronograma = os.path.join(output_dir, "cronogramas_parpadeo.png")
    fig.tight_layout()
    fig.savefig(ruta_cronograma, dpi=200)
    plt.close(fig)
    rutas_generadas.append(ruta_cronograma)

    return rutas_generadas


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("Ejecutando simulación y generación de gráficos para TP12...")
    archivos = generar_graficos_tp12(current_dir)
    for a in archivos:
        print(f" -> Generado: {a}")
