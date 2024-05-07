#include <Servo.h>
#define fps 23
Servo servoHor;
int position = 40;
int step = 2;

void setup() {
  Serial.begin(9600);
  servoHor.attach(10);
  servoHor.write(position);
}

void loop() {
  while (Serial.available() > 0) {
    String commandStr = Serial.readStringUntil('\n');
    commandStr.trim();

    if (commandStr.length() > 0) {
      if (commandStr == "1" && position < 80) {
        position += step;
        position = min(position, 80);
        servoHor.write(position);
      } else if (commandStr == "-1" && position > 0) {
        position -= step;
        position = max(position, 0);
        servoHor.write(position);
      } 
    }
    Serial.flush();
  }
  delay(1000/fps);
}

