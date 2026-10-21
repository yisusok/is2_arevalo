//*------------------------------------------------------------------
//* UADER - FCyT | Ingeniería de Software II
//* Dr. Pedro E. Colla
//* TP12: Sistemas Embebidos - Arduino Uno
//* Alumno: Jesús Arévalo
//*
//* Firmware Base: Umbral al 50% de Vcc y parpadeo de 1 segundo
//*------------------------------------------------------------------

const int PIN_BUTTON = 2;          // Pulsador en pin digital 2
const int PIN_POT    = A0;         // Potenciómetro en pin analógico A0
const int PIN_LED    = LED_BUILTIN;// LED onboard (pin digital 13)

// Constantes de operación
const int UMBRAL_ADC = 511;        // 50% de 1023 (aprox 2.5V sobre 5V de Vcc)
const int BUTTON_PRESSED = HIGH;   // Estado al presionar con pull-down
const unsigned long DELAY_500MS = 500;

void setup() {
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_POT, INPUT);
  pinMode(PIN_BUTTON, INPUT);

  Serial.begin(9600);
  Serial.println(F("--- TP12: Firmware Base (Umbral 50%, Parpadeo 1s) ---"));
}

void loop() {
  int estadoBoton = digitalRead(PIN_BUTTON);

  if (estadoBoton == BUTTON_PRESSED) {
    // Si se presiona el botón, se lee el valor analógico del potenciómetro
    int valorADC = analogRead(PIN_POT);
    float tension = (valorADC * 5.0) / 1023.0;

    // Si la tensión es la mitad que la de la fuente o menor (ADC <= 511)
    if (valorADC <= UMBRAL_ADC) {
      digitalWrite(PIN_LED, HIGH); // LED permanente encendido
      Serial.print(F("Boton Presionado | ADC: "));
      Serial.print(valorADC);
      Serial.print(F(" | Tension: "));
      Serial.print(tension, 2);
      Serial.println(F(" V (<= 50%) -> LED ON PERMANENTE"));
    } else {
      // Caso contrario: apaga el LED onboard y sigue parpadeando
      Serial.print(F("Boton Presionado | ADC: "));
      Serial.print(valorADC);
      Serial.print(F(" | Tension: "));
      Serial.print(tension, 2);
      Serial.println(F(" V (> 50%) -> LED PARPADEANDO"));

      digitalWrite(PIN_LED, LOW);
      delay(DELAY_500MS);
      digitalWrite(PIN_LED, HIGH);
      delay(DELAY_500MS);
      digitalWrite(PIN_LED, LOW);
    }
  } else {
    // En reposo (sin presionar): LED parpadea periódicamente
    digitalWrite(PIN_LED, LOW);
    delay(DELAY_500MS);
    digitalWrite(PIN_LED, HIGH);
    delay(DELAY_500MS);
    digitalWrite(PIN_LED, LOW);
  }

  // Espera de 500 ms al finalizar la lectura para repetir el ciclo
  delay(DELAY_500MS);
}
