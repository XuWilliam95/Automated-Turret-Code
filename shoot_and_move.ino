#include <Servo.h>

Servo servo_hor;
Servo servo_vert;// create servo object to control a servo
// twelve servo objects can be created on most boards

int pos_hor = 90;
int pos_vert = 90;// variable to store the servo position
int d;
int x;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);
  servo_hor.attach(9);
  servo_vert.attach(7);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  d = Serial.readString().toInt();
  servo_hor.write(pos_hor);
  servo_vert.write(pos_vert);
  
  if (d == 2) {
    pos_vert += 3;
    servo_vert.write(pos_vert);
  }
  if (d == -2) {
    pos_vert -= 3;
    servo_vert.write(pos_vert);
  }
  
  if (d == 3) {
    pos_hor += 3;
    servo_hor.write(pos_hor);
  }
  
  if (d == -3) {
    pos_hor -= 3;
    servo_hor.write(pos_hor);
  }

  if (x == 1){
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level
  }
  else {
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  }
  
  }
