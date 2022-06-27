#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 90;    // variable to store the servo position
int d;
int x;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  myservo.attach(9);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  d = Serial.readString().toInt();
  myservo.write(pos);
  
  if (d == 2) {
    pos += 1;
    myservo.write(pos);
  }
  if (d == -2) {
    pos -= 1;
    myservo.write(pos);
  }

  if (x == 1){
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level
  }
  else {
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  }
  
  }
