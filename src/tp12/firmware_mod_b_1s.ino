//*------------------------------------------------------------------
//* UADER - FCyT | Ingeniería de Software II
//* Dr. Pedro E. Colla
//* TP12: Sistemas Embebidos - Arduino Uno
//* Alumno: Jesús Arévalo
//*
//* Modificación (b): Ritmo de parpadeo a una vez cada 1 segundo
//*------------------------------------------------------------------

const int PIN_BUTTON = 2;          // Pulsador en pin digital 2
const int PIN_POT    = A0;         // Potenciómetro en pin analógico A0
const int PIN_LED    = LED_BUILTIN;// LED onboard (pin digital 13)

const int UMBRAL_ADC = 511;        // 50% de 1023 (2.5V)
const int BUTTON_PRESSED = HIGH;

// Temporización para parpadeo de 1 segundo de período (500 ms ON / 500 ms OFF)
const unsigned long TIEMPO_SEMI_PERIODO = 500; 
const unsigned long DELAY_500MS = 500;

void setup() {
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_POT, INPUT);
  pinMode(PIN_BUTTON, INPUT);

  Serial.begin(9600);
  Serial.println(F("--- TP12: Modificacion (b) - Ritmo de parpadeo cada 1s ---"));
}

void loop() {
  int estadoBoton = digitalRead(PIN_BUTTON);

  if (estadoBoton == BUTTON_PRESSED) {
    int valorADC = analogRead(PIN_POT);
    float tension = (valorADC * 5.0) / 1023.0;

    if (valorADC <= UMBRAL_ADC) {
      digitalWrite(PIN_LED, HIGH); // LED permanente encendido
      Serial.print(F("Boton Presionado | ADC: "));
      Serial.print(valorADC);
      Serial.print(F(" | Tension: "));
      Serial.print(tension, 2);
      Serial.println(F(" V (<= 50%) -> LED ON PERMANENTE"));
    } else {
      Serial.print(F("Boton Presionado | ADC: "));
      Serial.print(valorADC);
      Serial.print(F(" | Tension: "));
      Serial.print(tension, 2);
      Serial.println(F(" V (> 50%) -> PARPADEO 1s"));

      // Parpadeo con ritmo de 1 segundo (500ms OFF / 500ms ON)
      digitalWrite(PIN_LED, LOW);
      delay(TIEMPO_SEMI_PERIODO);
      digitalWrite(PIN_LED, HIGH);
      delay(TIEMPO_SEMI_PERIODO);
      digitalWrite(PIN_LED, LOW);
    }
  } else {
    // Parpadeo con ritmo de 1 segundo en espera
    digitalWrite(PIN_LED, LOW);
    delay(TIEMPO_SEMI_PERIODO);
    digitalWrite(PIN_LED, HIGH);
    delay(TIEMPO_SEMI_PERIODO);
    digitalWrite(PIN_LED, LOW);
  }

  delay(DELAY_500MS);
}
