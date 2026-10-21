//*------------------------------------------------------------------
//* UADER - FCyT | Ingeniería de Software II
//* Dr. Pedro E. Colla
//* TP12: Sistemas Embebidos - Arduino Uno
//* Alumno: Jesús Arévalo
//*
//* Modificación (c): Umbral de activación al 25% de la tensión total
//*------------------------------------------------------------------

const int PIN_BUTTON = 2;          // Pulsador en pin digital 2
const int PIN_POT    = A0;         // Potenciómetro en pin analógico A0
const int PIN_LED    = LED_BUILTIN;// LED onboard (pin digital 13)

// Cálculo del umbral al 25%:
// Tensión nominal de alimentación: Vcc = 5.0 V
// Tensión umbral: 25% de 5.0 V = 1.25 V
// Cuantización ADC de 10 bits: 1023 * 0.25 = 255.75 -> 255 cuentas
const int UMBRAL_ADC = 255;        
const int BUTTON_PRESSED = HIGH;

const unsigned long TIEMPO_SEMI_PERIODO = 500; // Parpadeo de 1s
const unsigned long DELAY_500MS = 500;

void setup() {
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_POT, INPUT);
  pinMode(PIN_BUTTON, INPUT);

  Serial.begin(9600);
  Serial.println(F("--- TP12: Modificacion (c) - Umbral de activacion al 25% (<= 1.25V / ADC <= 255) ---"));
}

void loop() {
  int estadoBoton = digitalRead(PIN_BUTTON);

  if (estadoBoton == BUTTON_PRESSED) {
    int valorADC = analogRead(PIN_POT);
    float tension = (valorADC * 5.0) / 1023.0;

    // Si la tensión es el 25% o menor de la tensión total (ADC <= 255)
    if (valorADC <= UMBRAL_ADC) {
      digitalWrite(PIN_LED, HIGH); // LED permanente encendido
      Serial.print(F("Boton Presionado | ADC: "));
      Serial.print(valorADC);
      Serial.print(F(" | Tension: "));
      Serial.print(tension, 2);
      Serial.println(F(" V (<= 25% de Vcc) -> LED ON PERMANENTE"));
    } else {
      Serial.print(F("Boton Presionado | ADC: "));
      Serial.print(valorADC);
      Serial.print(F(" | Tension: "));
      Serial.print(tension, 2);
      Serial.println(F(" V (> 25% de Vcc) -> LED PARPADEANDO"));

      digitalWrite(PIN_LED, LOW);
      delay(TIEMPO_SEMI_PERIODO);
      digitalWrite(PIN_LED, HIGH);
      delay(TIEMPO_SEMI_PERIODO);
      digitalWrite(PIN_LED, LOW);
    }
  } else {
    // Parpadeo en reposo
    digitalWrite(PIN_LED, LOW);
    delay(TIEMPO_SEMI_PERIODO);
    digitalWrite(PIN_LED, HIGH);
    delay(TIEMPO_SEMI_PERIODO);
    digitalWrite(PIN_LED, LOW);
  }

  delay(DELAY_500MS);
}
