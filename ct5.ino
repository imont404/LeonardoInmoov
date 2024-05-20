#include <Servo.h>

Servo servoX;
Servo servoY;

int targetX = 90;
int currentX = 90;
int stepX = 7;
int targetY = 30;
int currentY = 30; //20 a 100 grados
int stepY = 7;
unsigned long lastMoveTime = 0;
unsigned long wait = 2;

void setup() {
  Serial.begin(9600);
  servoX.attach(10); //x
  servoY.attach(9); //y
  servoX.write(currentX);
  servoY.write(currentY);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    //X
    if (command == "XFL") {
      targetX = max(0, currentX - 20);
    } else if (command == "XFR") {
      targetX = min(180, currentX + 20);
    } else if (command == "XL") {
      targetX = max(0, currentX - stepX);
    } else if (command == "XR") {
      targetX = min(180, currentX + stepX);
    } else if (command == "CX") {
      targetX = 90;
    }

    //Y
    if (command == "YFU") {
      targetY = max(20, currentY - 20);
    } else if (command == "YFD") {
      targetY = min(100, currentY + 20);
    } else if (command == "YU") {
      targetY = max(20, currentY - stepY);
    } else if (command == "YD") {
      targetY = min(100, currentY + stepY);
    } else if (command == "CY") {
      targetY = 30;
    }
  }

  unsigned long currentTime = millis();
  if (currentTime - lastMoveTime > wait) {
    // X
    if (currentX < targetX) {
      currentX = min(targetX, currentX + stepX);
      servoX.write(currentX);
    } else if (currentX > targetX) {
      currentX = max(targetX, currentX - stepX);
      servoX.write(currentX);
    }
    // Y
    if (currentY < targetY) {
      currentY = min(targetY, currentY + stepY);
      servoY.write(currentY);
    } else if (currentY > targetY) {
      currentY = max(targetY, currentY - stepY);
      servoY.write(currentY);
    }
    lastMoveTime = currentTime;
  }
}
