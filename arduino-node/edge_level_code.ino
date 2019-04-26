#include <avr/sleep.h>
#define interruptPin 2

#define FASTADC 1
long tim = 0;
int inputPin = A2;

// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

void setup() {
  // put your setup code here, to run once:
pinMode(inputPin,INPUT);
Serial.begin(230400);

 #if FASTADC
 // set prescale to 16
   sbi(ADCSRA,ADPS2) ;
   cbi(ADCSRA,ADPS1) ;
   cbi(ADCSRA,ADPS0) ;
  #endif

pinMode(interruptPin,INPUT_PULLUP);
}

void loop() {
  Going_To_Sleep();
}

void Going_To_Sleep() {
  sleep_enable();
  attachInterrupt(0, wakeUp, LOW);
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_cpu();
}

void wakeUp(){
  tim = millis();
  Serial.println("Data from room no. L1: ");
  while ((millis() - tim)<10000) {
    double input = map(analogRead(inputPin), 0, 1023, -1000, 1000);
    Serial.print((int)input);
    Serial.print(",");
  }
  delay(1000);
  Serial.println(" ");
  tim=0;
  sleep_disable();
  detachInterrupt(0); 
}
