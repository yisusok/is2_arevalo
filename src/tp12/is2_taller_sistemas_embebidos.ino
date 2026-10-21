//*------------------------------------------------------------------
//* UADER - FCyT
//* Ingeniería de Software II
//* Dr. Pedro E. Colla
//*
//* TP12: Sistemas Embebidos - Arduino Uno
//* Alumno: Jesús Arévalo
//*
//* Archivo: is2_taller_sistemas_embebidos.ino
//* Descripción: Firmware corregido y parametrizado para la evaluación
//*              del circuito con potenciómetro, pulsador y LED integrado.
//*------------------------------------------------------------------

// ==================================================================
// CONFIGURACIÓN DE PINES (MAPPING DE HARDWARE)
// ==================================================================
const int PIN_BUTTON = 2;          // Entrada digital: Pulsador en D2
const int PIN_POT    = A0;         // Entrada analógica: Potenciómetro en A0 (Corregido respecto al original)
const int PIN_LED    = LED_BUILTIN;// Salida digital: LED onboard en D13

// ==================================================================
// SELECCIÓN DE PERFIL / MODALIDAD DE EJECUCIÓN
// ------------------------------------------------------------------
// Descomente únicamente UNA de las siguientes directivas:
#define MODO_BASE       // Consigna Base: Umbral 50% (<= 511), parpadeo cada 1 s
// #define MODO_A_5S    // Modificación (a): Ritmo de parpadeo cada 5 s
// #define MODO_B_1S    // Modificación (b): Ritmo de parpadeo cada 1 s
// #define MODO_C_25PCT // Modificación (c): Umbral al 25% (<= 255)

// ==================================================================
// PARÁMETROS DEL SISTEMA SEGÚN MODO SELECCIONADO
// ==================================================================
#if defined(MODO_A_5S)
    const int    UMBRAL_ADC          = 511;   // 50% de 1023 (2.50V)
    const float  UMBRAL_PORCENTAJE   = 50.0;
    const unsigned long TIEMPO_ON_MS = 2500;  // Parpadeo cada 5 s (semi-período ON)
    const unsigned long TIEMPO_OFF_MS= 2500;  // Semi-período OFF
    const char*  MODO_NOMBRE         = "Modificación (a): Parpadeo cada 5 segundos";

#elif defined(MODO_B_1S)
    const int    UMBRAL_ADC          = 511;   // 50% de 1023 (2.50V)
    const float  UMBRAL_PORCENTAJE   = 50.0;
    const unsigned long TIEMPO_ON_MS = 500;   // Parpadeo cada 1 s (semi-período ON)
    const unsigned long TIEMPO_OFF_MS= 500;   // Semi-período OFF
    const char*  MODO_NOMBRE         = "Modificación (b): Parpadeo cada 1 segundo";

#elif defined(MODO_C_25PCT)
    const int    UMBRAL_ADC          = 255;   // 25% de 1023 (1.25V)
    const float  UMBRAL_PORCENTAJE   = 25.0;
    const unsigned long TIEMPO_ON_MS = 500;   // Parpadeo nominal 1 s
    const unsigned long TIEMPO_OFF_MS= 500;
    const char*  MODO_NOMBRE         = "Modificación (c): Umbral de activación al 25%";

#else // MODO_BASE por defecto
    const int    UMBRAL_ADC          = 511;   // 50% de 1023 (2.50V)
    const float  UMBRAL_PORCENTAJE   = 50.0;
    const unsigned long TIEMPO_ON_MS = 500;   // 500 ms ON
    const unsigned long TIEMPO_OFF_MS= 500;   // 500 ms OFF
    const char*  MODO_NOMBRE         = "Consigna Base: Umbral 50%, Parpadeo 1 s";
#endif

// ==================================================================
// CONFIGURACIÓN DE POLARIDAD DEL PULSADOR
// ------------------------------------------------------------------
// En el circuito estándar de TinkerCad con resistor pull-down a GND,
// el pulsador entrega HIGH (1) al presionarse.
// Si se utiliza pull-up (o pulsador conectado a GND con pull-up interno),
// cambiar a LOW (0).
const int BUTTON_PRESSED = HIGH; 

// Retardo de estabilización de ciclo de lectura especificado en la consigna
const unsigned long DELAY_CICLO_MS = 500;

// ==================================================================
// INICIALIZACIÓN (SETUP)
// ==================================================================
void setup()
{
  // Configuración de direcciones de puertos
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_POT, INPUT);
  pinMode(PIN_BUTTON, INPUT);

  // Inicialización de la interfaz de comunicaciones serie
  Serial.begin(9600);
  while (!Serial) {
    ; // Espera para puertos nativos USB (Arduino Leonardo/Micro, compatible Uno)
  }

  // Banner informativo del sistema
  Serial.println(F("=================================================="));
  Serial.println(F("   UADER - FCyT | Ingenieria de Software II"));
  Serial.println(F("   TP12: Taller de Sistemas Embebidos (Arduino Uno)"));
  Serial.println(F("   Alumno: Jesus Arevalo"));
  Serial.println(F("=================================================="));
  Serial.print(F("Modo activo: "));
  Serial.println(MODO_NOMBRE);
  Serial.print(F("Umbral ADC de activacion: <= "));
  Serial.print(UMBRAL_ADC);
  Serial.print(F(" ("));
  Serial.print(UMBRAL_PORCENTAJE, 1);
  Serial.print(F("% de Vcc = "));
  Serial.print((UMBRAL_PORCENTAJE * 5.0) / 100.0, 2);
  Serial.println(F(" V)"));
  Serial.print(F("Periodo de parpadeo: "));
  Serial.print(TIEMPO_ON_MS + TIEMPO_OFF_MS);
  Serial.println(F(" ms"));
  Serial.println(F("Sistema iniciado y en espera de eventos..."));
  Serial.println(F("--------------------------------------------------"));
}

// ==================================================================
// CICLO PRINCIPAL (LOOP)
// ==================================================================
void loop()
{
  // 1. Lectura del estado del pulsador físico
  int estadoBoton = digitalRead(PIN_BUTTON);

  // 2. Evaluación: ¿Se encuentra presionado el pulsador?
  if (estadoBoton == BUTTON_PRESSED) {
    // Lectura analógica de la tensión en el potenciómetro (canal A0, 10 bits: 0-1023)
    int valorADC = analogRead(PIN_POT);
    float tensionVoltios = (valorADC * 5.0) / 1023.0;
    float porcentaje = (valorADC / 1023.0) * 100.0;

    // Condición: Tensión menor o igual a la tensión umbral (50% o 25% según modo)
    if (valorADC <= UMBRAL_ADC) {
      // Estado Activo: LED permanente encendido
      digitalWrite(PIN_LED, HIGH);

      // Exhibición del valor medido en la consola serie
      Serial.print(F("[ACTIVADO] Boton PRESIONADO | ADC: "));
      Serial.print(valorADC);
      Serial.print(F(" / 1023 | Tension: "));
      Serial.print(tensionVoltios, 2);
      Serial.print(F(" V ("));
      Serial.print(porcentaje, 1);
      Serial.println(F("% de Vcc) -> LED ENCENDIDO PERMANENTE"));
    } else {
      // Condición no cumplida (tensión superior al umbral):
      // El LED onboard se apaga y continúa su ciclo de parpadeo
      Serial.print(F("[ALERTA] Boton PRESIONADO pero Tension > Umbral | ADC: "));
      Serial.print(valorADC);
      Serial.print(F(" ("));
      Serial.print(tensionVoltios, 2);
      Serial.println(F(" V) -> Parpadeando LED..."));

      ejecutarCicloParpadeo();
    }
  } else {
    // Si el pulsador NO está presionado:
    // El sistema mantiene el LED parpadeando en estado de espera (idle)
    ejecutarCicloParpadeo();
  }

  // Retardo de ciclo especificado en la consigna (500 ms)
  delay(DELAY_CICLO_MS);
}

// ==================================================================
// SUBRUTINA DE PARPADEO DEL LED
// ==================================================================
void ejecutarCicloParpadeo()
{
  digitalWrite(PIN_LED, LOW);
  delay(TIEMPO_OFF_MS);
  digitalWrite(PIN_LED, HIGH);
  delay(TIEMPO_ON_MS);
  digitalWrite(PIN_LED, LOW);
}