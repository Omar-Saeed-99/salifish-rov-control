# controlling rov using arduino

## rov spacifcations:
the rov has 2 leds 2 neumatic grippers and 7 thrusters, with depth and imu sensor 


The system is composed of Arduino UNO connected using Ethernet communication, as the Arduino receives the commands from the top side through ENC28J60 module. 
The Arduino takes signals from IMU sensor and emit digital signals for mechanisms, gripper, and LEDs, also it emits PWM signals for ESCs to move thrusters (t100) and servo.
Arduino is also responsible for sending data or feedback to the GUI such as the determined distance and the readings that token from the IMU sensor as well as the used sensors.

## ROV GUI

The top side control unit provides 2 screens of GUI to provide intuitive and fast control over ROV crucial functions. 
The GUI is the general interface for the software, from which the pilot and co-pilot control the movement of the ROV and receive feedback from it.
It consists of the front end and back end using a QT designernapplication framework and python.
QT Designer is providing us with a what you see is what you get user interface, and it is an independent programming language.
It doesn’t produce code in any particular programming language, so, we use python programming language as it is the best choice for the GUI back-end because it offers
substantial support libraries which contains also the PYQT5 library, reduces latency achieves real-time control, and was implemented to construct all missionspecific algorithms.

![pilot GUI](https://user-images.githubusercontent.com/87039861/170713315-ed918054-4738-46cb-975c-759c9c0af79f.png)


The GUI's main purposes are activating the different functionalities, like taking a photo, concatenating photos, finding differences in photos, switching the mode to the
autonomous, making some calculations, and mapping.
In addition to these, it can illustrate some data like the connection status of the ROV and the joystick. 
To achieve these purposes, we created two different user interfaces for the pilot and the co-pilot.

![CO-Pilot-GUI](https://user-images.githubusercontent.com/87039861/170714034-40dd71e7-d050-429d-8982-d395e1585aee.png)
![CO-Pilot-GUI](https://user-images.githubusercontent.com/87039861/170714047-da5c4a86-fa54-4be2-bf0d-ba50b1c7cb16.png)

