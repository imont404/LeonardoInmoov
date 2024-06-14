#include <Servo.h>
Servo tiltServo; //y
Servo panServo; //x


void setup()
{
  Serial.begin(9600);
  tiltServo.attach(9); // Vertical
  panServo.attach(10); // Horizontal 
  panServo.write(90);
  tiltServo.write(40);
}



void loop() {
  if (Serial.available() > 0) {
    int angle = Serial.parseInt();
    if (angle >= 45 && angle <= 135) {
      panServo.write(angle); 

   
   // tiltServo.write(angle);
    }
  }
}
