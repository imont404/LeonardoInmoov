#include <Servo.h>
Servo servoVer; //Vertical Servo
Servo servoHor; //Horizontal Servo
int x;
int y;
int prevX;
int prevY;
void setup()
{
  Serial.begin(9600);
  servoVer.attach(9); // Vertical
  servoHor.attach(10); // Horizontal 
  servoVer.write(90);
  servoHor.write(40);
}
void Pos()
{
  if(prevX != x || prevY != y)
  {
    int servoX = map(x, -320, 320, 0, 80);
    int servoY = map(y, 450, 0, 80, 0);
    servoX = min(servoX, 80);
    servoX = max(servoX, 0);
    servoY = min(servoY, 80);
    servoY = max(servoY, 0);
    
    servoHor.write(servoX);
    servoVer.write(servoY);
  }
}
void loop()
{
  if(Serial.available() > 0)
  {
    if(Serial.read() == 'X')
    {
      x = Serial.parseInt();
      if(Serial.read() == 'Y')
      {
        y = Serial.parseInt();
       Pos();
      }
    }
    while(Serial.available() > 0)
    {
      Serial.read();
    }
  }
}



