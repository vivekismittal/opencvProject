#include<Servo.h>
Servo X ;
Servo Y;
char x;
long int v;
void setup() {
X.attach(9);
Y.attach(3);

 Serial.begin(9600);
   X.write(90);
}

void loop() {
if(Serial.available()>2){
  x =Serial.read();
  v =Serial.parseInt();
 if(x =='a'){
    X.write(v); 
    Y.write(0); 
  }
 else if(x=='b'){
    X.write(90);
    Y.write(180);
  }
  delay(10);
  }
  
}
