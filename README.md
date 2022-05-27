# controlling rov using arduino

## rov spacifcations:
the rov has 2 leds 2 neumatic grippers and 7 thrusters, with depth and imu sensor 


The system is composed of Arduino UNO connected using Ethernet communication, as the Arduino receives the commands from the top side through ENC28J60 module. 
The Arduino takes signals from IMU sensor and emit digital signals for mechanisms, gripper, and LEDs, also it emits PWM signals for ESCs to move thrusters (t100) and servo.
Arduino is also responsible for sending data or feedback to the GUI such as the determined distance and the readings that token from the IMU sensor as well as the used sensors.
