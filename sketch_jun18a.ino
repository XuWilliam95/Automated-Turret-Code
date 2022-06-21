int x;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  if (x == 1){
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(0.1);                       // wait for a second
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
      delay(0.1);
      }
  }
  
