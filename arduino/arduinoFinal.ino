#include <Wire.h>
#include <Servo.h>
#include <UIPEthernet.h>

// thrusters pins decleration

byte thruster1servoPin =A3; // 7*****                        **** 5
byte thruster2servoPin =A2; //   Horzontal thrusters         
byte thruster3servoPin =4; //                                
byte thruster4servoPin =A0; // ****6                           4****

byte thruster5servoPin =1; //                               
byte thruster6servoPin =2; // 1***   Vertical thrusters *** 2  

byte thruster7servoPin =3; //             ***3

// servo pin decleration

byte servo_ = 0; 
int servo_ange = 84;


// thrusters objects

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
Servo servo7;
Servo real;



uint8_t flags ;
uint8_t V_diection ;
uint32_t speed_of_vertical ;
uint8_t H_diection ;
uint32_t speed_of_horzontal ;
byte servo;
uint8_t on_off ;




// solnoids and led pins declrations

#define p_grip 6 // peimry gripper
bool p_grip_state = false;

#define S_grip 7 // secondry gripper
bool S_grip_state = false;

#define R_grip 9 // rotinal gripper
bool R_grip_state = false;

//#define sol4 9 // idk
//bool state_4 = false;


#define led 5
bool led_state = false;


char *splitings[8]; // an array of pointers to the pieces of the above array after strtok()
char *ptr = NULL;
bool imu_state = false;


EthernetServer server = EthernetServer(8000);




void forward(int i)
{

int v = map(i,0,100,1500,1850);
servo5.writeMicroseconds(v); // Send signal to ESC.
servo7.writeMicroseconds(v); // Send signal to ESC.
servo2.writeMicroseconds(v); // Send signal to ESC.

 v = map( i,0,100,1500,1150);
servo1.writeMicroseconds(v); // Send signal to ESC.

//servo3.writeMicroseconds(v); // Send signal to ESC.
//servo4.writeMicroseconds(v); // Send signal to ESC.
//servo6.writeMicroseconds(v); // Send signal to ESC.


}


void backward(int i)
{
int v = map(i,0,100,1500,1850);

servo1.writeMicroseconds(v); // Send signal to ESC.
 v = map( i,0,100,1500,1150);
servo7.writeMicroseconds(v); // Send signal to ESC.
servo5.writeMicroseconds(v); // Send signal to ESC.
servo2.writeMicroseconds(v); // Send signal to ESC.


}


int right(int i)
{
  
int v = map(i,0,100,1500,1850);
servo1.writeMicroseconds(v); // Send signal to ESC.
servo2.writeMicroseconds(v); // Send signal to ESC.
servo5.writeMicroseconds(v); // Send signal to ESC.

//
v = map( i,0,100,1500,1150);
servo7.writeMicroseconds(v); // Send signal to ESC.



}


int left(int i)
{
int v = map(i,0,100,1500,1850);

servo7.writeMicroseconds(v); // Send signal to ESC.

//
v = map( i,0,100,1500,1150);
servo1.writeMicroseconds(v); // Send signal to ESC.
servo2.writeMicroseconds(v); // Send signal to ESC.
servo5.writeMicroseconds(v); // Send signal to ESC.

}

int R_left(int i)
{
int v = map( i,0,100,1500,1850);
//   Serial.print("l with speed: ");
//   Serial.println(v);
servo5.writeMicroseconds(v); // Send signal to ESC.

 v = map(i,0,100,1500,1150);
servo1.writeMicroseconds(v); // Send signal to ESC.
servo2.writeMicroseconds(v); // Send signal to ESC.
servo7.writeMicroseconds(v); // Send signal to ESC.


}

int R_right(int i)
{
int v = map( i,0,100,1500,1850);
//   Serial.print("l with speed: ");
//   Serial.println(v);
servo1.writeMicroseconds(v); // Send signal to ESC.
servo2.writeMicroseconds(v); // Send signal to ESC.
servo7.writeMicroseconds(v); // Send signal to ESC.

 v = map(i,0,100,1500,1150);
servo5.writeMicroseconds(v); // Send signal to ESC.

}

void up(int i)
{

  int v = map(i,0,100,1500,1150);   
//  Serial.print("up with speed: ");
//  Serial.println(v);

servo6.writeMicroseconds(v); // Send signal to ESC.
servo4.writeMicroseconds(v); // Send signal to ESC.

}

int down(int i)
{
int  v = map( i,0,100,1500,1850);
// Serial.print("down with speed: ");
// Serial.println(v);
servo6.writeMicroseconds(v); // Send signal to ESC.
servo4.writeMicroseconds(v); // Send signal to ESC.

}
void h_stop()
{
//    Serial.print("h stop ");

servo3.writeMicroseconds(1500); // Send signal to ESC.
servo5.writeMicroseconds(1500); // Send signal to ESC.
servo2.writeMicroseconds(1500); // Send signal to ESC.
servo7.writeMicroseconds(1500); // Send signal to ESC.
}

void v_stop()
{
//     Serial.print("v stop  ");

servo6.writeMicroseconds(1500); // Send signal to ESC.
servo4.writeMicroseconds(1500); // Send signal to ESC.
}
void roll_right(int i)
      {

//       Serial.print("ho.rse right with speed: ");
       
         int  v = map( i,0,100,1500,1150);
//         Serial.println(v);
         servo6.writeMicroseconds(v);
         v = map( i,0,100,1500,1850);
         servo4.writeMicroseconds(v);
         
     }
void roll_left(int i)
      {
//   Serial.print("horse left with speed: ");
      int  v = map( i,0,100,1500,1150);
//       Serial.println(v);
       servo4.writeMicroseconds(v);
       v = map( i,0,100,1500,1850);
       servo6.writeMicroseconds(v);
        }
void horse_up(int i)
      {
//      Serial.print("horse up with speed: ");
     int  v = map( i,0,100,1500,1850);

        servo3.writeMicroseconds(v);

      }
void horse_down(int i)
      {

//      Serial.print("horse down with speed: ");

      int  v = map( i,0,100,1500,1150);

        servo3.writeMicroseconds(v);

//         Serial.println(v);
      }
    
void setup() {

//  Serial.begin(9600); // for depuging

servo1.attach(thruster1servoPin);
servo1.writeMicroseconds(1500); // send "stop" signal to ESC. Also necessary to arm the ESC.
servo2.attach(thruster2servoPin);
servo2.writeMicroseconds(1500); // send "stop" signal to ESC. Also necessary to arm the ESC.
servo3.attach(thruster3servoPin);
servo3.writeMicroseconds(1500); // send "stop" signal to ESC. Also necessary to arm the ESC.
servo4.attach(thruster4servoPin);
servo4.writeMicroseconds(1500); // send "stop" signal to ESC. Also necessary to arm the ESC.
servo5.attach(thruster5servoPin);
servo5.writeMicroseconds(1500); // send "stop" signal to ESC. Also necessary to arm the ESC.
servo6.attach(thruster6servoPin);
servo6.writeMicroseconds(1500); // send "stop" signal to ESC. Also necessary to arm the ESC.
servo7.attach(thruster7servoPin);
servo7.writeMicroseconds(1500); // send "stop" signal to ESC. Also necessary to arm the ESC.

real.attach(servo_);
real.write(servo_ange);

  pinMode(p_grip, OUTPUT);
  pinMode(S_grip, OUTPUT);
  pinMode(R_grip, OUTPUT);
  pinMode(led, OUTPUT);

  uint8_t mac[6] = {0x00,0x01,0x02,0x03,0x04,0x05};
  IPAddress myIP(192,168,1,80);

  Ethernet.begin(mac,myIP);

  server.begin();


  Wire.begin(); // join i2c bus (address optional for master)
}





void loop() {


  byte index = 0;


   size_t size;
uint8_t* msg;
  if (EthernetClient client = server.available())
    {
      while((size = client.available()) > 0)
        {
          uint8_t* msg = (uint8_t*)malloc(size);
          size = client.read(msg,size);
          
//          Serial.write(msg,size);
//          Serial.println();      
//          client.write(msg,size);

ptr = strtok(msg, ",");

    while (ptr != NULL)
    {
    splitings[index] = ptr;
      index++;


      
      ptr = strtok(NULL, ",");
    }

    
    flags = atoi(splitings[0]);
   on_off = atoi(splitings[1]);
    V_diection = atoi(splitings[2]);
    speed_of_vertical = atoi (splitings[3]);
    H_diection =  atoi(splitings[4]);
    speed_of_horzontal = atoi(splitings[5]);
    servo = atoi(splitings[6]);

      if (on_off == 16) {
        p_grip_state = not p_grip_state;
        if (p_grip_state == true) {
          digitalWrite(p_grip, HIGH);
        } else {
          digitalWrite(p_grip, LOW);
        }
      }
      else if (on_off == 8) {
        S_grip_state = not S_grip_state;
        if (S_grip_state == true) {
          digitalWrite(S_grip, HIGH);
        } else {
          digitalWrite(S_grip, LOW);
        }
      }
      else if (on_off == 4) {
        R_grip_state = not R_grip_state;

        if (R_grip_state == true) {
          digitalWrite(R_grip, HIGH);
        } else {
          digitalWrite(R_grip, LOW);
        }

      }
      else if (on_off == 1) {
        imu_state = not imu_state;
      }

      else if (on_off == 2) {
        led_state = not led_state;

        if (led_state == true) {
          digitalWrite(led, HIGH);

          
        } else {
          digitalWrite(led, LOW);

        }
      }


  if(V_diection != 0){
   if (V_diection == 1){
   up(speed_of_vertical);
   }else if (V_diection == 2){
      down(speed_of_vertical);
   }else if (V_diection == 3){
   horse_up(speed_of_vertical);
   }else if (V_diection == 4){
      horse_down(speed_of_vertical);
   }else if (V_diection ==5){
   roll_left(speed_of_vertical);
   }else if (V_diection == 6){
      roll_right(speed_of_vertical);
   }
   
   }

      if(H_diection != 0){
  if (H_diection == 1){
   forward(speed_of_horzontal);
   }else if (H_diection == 2){
      backward(speed_of_horzontal);
   }else if (H_diection == 3){
      right(speed_of_horzontal);
   }else if (H_diection == 4){
      left(speed_of_horzontal);
   }else if (H_diection == 6){
    if (speed_of_horzontal==0){
      speed_of_horzontal = 30;
    }
      R_right(speed_of_horzontal);
   }else if (H_diection == 5){
        if (speed_of_horzontal==0){
      speed_of_horzontal = 30;
    }
      R_left(speed_of_horzontal);
   }
   }

if (servo == 1){
  servo_ange = servo_ange + 10;
  servo = 0;
  real.write(servo_ange);
  Serial.print("servo angle= ");
  
}else if (servo == 2){
    servo = 0;
 servo_ange = servo_ange - 10;
 real.write(servo_ange);
  Serial.print("servo angle= ");
   Serial.println(servo_ange);

 }

            free(msg);

    }
delay(10);
        }

     
}

 
