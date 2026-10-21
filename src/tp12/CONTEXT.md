# CONTEXT.md: Registro de Contexto, Especificación y Trazabilidad del TP12

**Asignatura:** Ingeniería de Software II  
**Docente:** Dr. Pedro E. Colla  
**Institución:** Facultad de Ciencia y Tecnología (FCyT) - Universidad Autónoma de Entre Ríos (UADER)  
**Alumno:** Jesús Arévalo  
**Módulo:** TP12 Sistemas Embebidos  
**Ubicación:** `src/tp12/`  

---

## 1. Alcance y Objetivos de Ingeniería

El presente Trabajo Práctico tiene como objetivo el modelado, construcción, auditoría de software de firmware, corrección y verificación experimental de un sistema embebido basado en el microcontrolador **ATmega328P** sobre la plataforma **Arduino Uno**.

El sistema interactúa con:
1. **Entrada Digital (D2):** Pulsador físico con resistencia pull-down externa (o pull-up interna) para sensar la interacción del usuario.
2. **Entrada Analógica (A0):** Potenciómetro lineal de 10 kΩ conectado entre Vcc (5V) y GND, cuyo cursor entrega una tensión variable continua $V_{in} \in [0.0, 5.0]\text{ V}$.
3. **Salida Digital (D13 / `LED_BUILTIN`):** LED integrado en la placa Arduino Uno para señalización óptica de estados.
4. **Salida Serie (UART / USB):** Puerto serie a 9600 baudios para emisión y registro de telemetría y diagnósticos.

---

## 2. Auditoría de Calidad del Sketch Original (`is2_taller_sistemas_embebidos.ino`)

De acuerdo con la consigna: *"Cargue el programa utilizado para la emulación en plataforma TinkerCad (así como todas las modificaciones que le hubiera hecho para que funcionare)..."*, se realizó una inspección formal de código sobre la versión preliminar provista por la cátedra, identificándose los siguientes defectos:

| ID Defecto | Ubicación | Código Original | Defecto Detectado | Acción Correctiva Aplicada |
| :--- | :--- | :--- | :--- | :--- |
| **DEF-01** | `loop()`, línea 27 | `int a=analogRead(2);` | Lectura de canal analógico A2 en lugar de A0 (el cursor del circuito está cableado al pin A0). | Se reemplazó por `analogRead(PIN_POT)` asignado a `A0`. |
| **DEF-02** | `loop()`, línea 25 | `if (pin2 == 0) { ... }` | Falta de evaluación de la condición de tensión analógica ($\le 50\%$ de Vcc). Encendía el LED sólo con el botón. | Se incorporó la condición anidada `if (valorADC <= UMBRAL_ADC)` para discriminar la tensión. |
| **DEF-03** | `setup()`, línea 17 | `digitalWrite(3,HIGH);` | Escritura en pin D3 sin previa configuración de `pinMode(3, OUTPUT)` y sin propósito en el circuito. | Se eliminó la instrucción espuria y se concentró la configuración en pines asignados. |
| **DEF-04** | `setup()` / `loop()` | `pin2 == 0` | Asunción rígida de lógica activa-baja (pull-up) sin contemplar el esquemático de TinkerCad con resistor pull-down. | Se parametrizó mediante la constante `BUTTON_PRESSED = HIGH` con soporte configurable para ambas topologías. |
| **DEF-05** | General | Números mágicos (`2`, `3`, `500`) | Falta de encapsulamiento y modularidad. | Se introdujeron constantes descriptivas (`PIN_BUTTON`, `PIN_POT`, `PIN_LED`, `UMBRAL_ADC`). |

---

## 3. Especificación de Requerimientos y Casos de Prueba

### Requerimientos Funcionales (RF):
- **RF-01:** Cuando el pulsador NO esté presionado, el LED integrado debe parpadear cíclicamente con el ritmo configurado.
- **RF-02:** Cuando el pulsador se presione, el microcontrolador debe leer inmediatamente el canal analógico A0.
- **RF-03:** Si el valor analógico leído es menor o igual al umbral configurado (50% en modo Base, 25% en Modificación C), el LED debe permanecer encendido en estado fijo (`HIGH`) y debe emitirse por puerto serie el valor ADC y la tensión calculada.
- **RF-04:** Si el valor analógico supera dicho umbral estando el botón presionado, el LED debe apagarse y reanudar el ciclo de parpadeo.
- **RF-05:** Al finalizar cada ciclo de evaluación se debe intercalar un retardo de estabilización de 500 ms antes de la siguiente iteración.

### Requerimientos de Modificación (Página 2 del TP):
- **MOD-A:** Ritmo de parpadeo configurado a un ciclo cada 5 segundos ($T = 5000\text{ ms}$, semiperíodo de 2500 ms).
- **MOD-B:** Ritmo de parpadeo configurado a un ciclo cada 1 segundo ($T = 1000\text{ ms}$, semiperíodo de 500 ms).
- **MOD-C:** Umbral de activación reducido al 25% de la tensión de la fuente ($V_{th} = 1.25\text{ V}$, cuentas ADC $\le 255$).

---

## 4. Trazabilidad de Artefactos Desarrollados

- [is2_taller_sistemas_embebidos.ino](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp12/is2_taller_sistemas_embebidos.ino): Firmware maestro multipropósito con selección de perfiles por directivas preprocesador.
- [firmware_base.ino](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp12/firmware_base.ino): Firmware autocontenido para la Consigna Base.
- [firmware_mod_a_5s.ino](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp12/firmware_mod_a_5s.ino): Firmware para la Modificación (a) (5 segundos).
- [firmware_mod_b_1s.ino](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp12/firmware_mod_b_1s.ino): Firmware para la Modificación (b) (1 segundo).
- [firmware_mod_c_25pct.ino](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp12/firmware_mod_c_25pct.ino): Firmware para la Modificación (c) (25% umbral).
- [simulador_embebido.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp12/simulador_embebido.py): Emulador matemático del ADC de 10 bits y generador de gráficos.
- [test_firmware.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp12/test_firmware.py): Suite de pruebas unitarias ejecutadas con `pytest` (100% passed).
- [TP12_Sistemas_Embebidos.ipynb](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp12/TP12_Sistemas_Embebidos.ipynb): Jupyter Notebook interactivo de simulación y gráficos.
- [README.md](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp12/README.md): Informe universitario completo y detallado.
