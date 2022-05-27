from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from typing import List, Dict, Optional
import pygame
import sys
import time
import cv2 as cv   
import mss 
import queue
import re

import numpy
import serial
import socket

# Local Modules
from sf_message import SFMessage
from sf_logger import SFLogger  

logger = SFLogger(level=SFLogger.INFO, name="pilot")

HOST = '192.168.1.80'  # The server's hostname or IP address
PORT = 8000        # The port used by the server

def Socket_try():
    global sock
    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.settimeout(1)
    except:
        logger.error("establishing serial connection!")
Socket_try()

# def serial_try():

#     try:
#        global srl
#        srl = serial.Serial('COM5', 57600,parity='E', stopbits=2, timeout=0.01)
#     except:
#         logger.error("establitiong serial connection!")
    
# serial_try()  

#Camera_thread
class ImageThread(QThread):
    q_img_sig = pyqtSignal(QPixmap)

    def __init__(self, vid_path: dict):
        super(ImageThread, self).__init__()
        self.__monitor = vid_path

    def run(self):
        self.__thread_active = True
        with mss.mss() as sct:

            while self.__thread_active:
                image = numpy.asarray(sct.grab(self.__monitor))
                image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                height, width, _ = image.shape
                bytesPerLine = 3 * width
                #Convert Numpy materix to QImage: QImage >> QPixman
                q_img = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888) #*** BgR
                #To Deal with gui using signal
                self.q_img_sig.emit(QPixmap.fromImage(q_img))
                self.usleep(16)
  
    
    def stop(self):
        self.__thread_active = False
        self.wait(20)
        self.quit()
        self.exit()

        
class CamLabWorker:
    def __init__(self, mon: Dict[str, int], lb: QLabel) -> None:
        self.mon = mon
        self.lb = lb
        self.__th: Optional[ImageThread] = None

    def start(self):
        self.__th = ImageThread(self.mon)
        self.__th.q_img_sig.connect(lambda qimg: self.lb.setPixmap(qimg))
        self.__th.start()
        logger.debug(10 * "=" + f"Thread [{self.__th}] started for Lebel [{self.lb}]" + 10 * "=")

    def stop(self):
        if self.__th != None:
            self.__th.stop()
        self.lb.setText("No Signal")





class UI(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.ui.Joystick.setAlignment(Qt.AlignCenter)
        

       # Cam threads initialization
        mon = mss.mss().monitors[1]
        monitor1 = {
            "top": mon["top"] +  15,  # 15px from the top
            "left": mon["left"] +1,  # 1px from the left
            "width": 958,
            "height": 525,
            "mon": 2
        }
        monitor2 = {
            "top": mon["top"] +  15,  
            "left": mon["left"] +960,  
            "width": 958,
            "height": 525,
            "mon": 2
        }
        monitor3 = {
            "top": mon["top"] +  550,  
            "left": mon["left"] +10, 
            "width": 945,
            "height": 525,
            "mon": 2
        }
        monitor4 = {
            "top": mon["top"] +  550,  
            "left": mon["left"] +960, 
            "width": 958,
            "height": 525,
            "mon": 2
        }
        self.cam_tab_list: List[List[CamLabWorker]] = [
                [
                    CamLabWorker(monitor1, self.ui.AllCam1),
                    CamLabWorker(monitor2, self.ui.Allcam2),
                    CamLabWorker(monitor3, self.ui.Allcam3),
                    CamLabWorker(monitor4, self.ui.Allcam4),
                ],
                [
                    CamLabWorker(monitor1, self.ui.Maincamera)
                ],
                [
                    CamLabWorker(monitor4, self.ui.GripperCam),
                    CamLabWorker(monitor1, self.ui.MainCam)
                ]
        ]
        self.ui.tabWidget.currentChanged.connect(self.tab_change_cb)
        # Start cam threads for the startup tab
        for cam_worker in self.cam_tab_list[self.ui.tabWidget.currentIndex()]:
            cam_worker.start()
        
    
        self.handle_joystick_events()
        self.handle_keyboard_shortcuts()

    # Tab change callback
    def tab_change_cb(self, index: int) -> None:
        logger.debug(5 * "=" + f"Tab Change [{index}]" + 5 * "=")
        for tab in self.cam_tab_list:
            for cam_worker in tab:
                cam_worker.stop()
        for cam_worker in self.cam_tab_list[index]:
            cam_worker.start()
            

    #Switch Between tabs
    def handle_keyboard_shortcuts(self):
        self.sc_cam1 = QShortcut(QKeySequence('Alt+1'), self)
        self.sc_cam2 = QShortcut(QKeySequence('Alt+2'), self)
        self.sc_cam3 = QShortcut(QKeySequence('Alt+3'), self)
        self.sc_cam1.activated.connect(lambda: self.ui.tabWidget.setCurrentIndex(0))
        self.sc_cam2.activated.connect(lambda: self.ui.tabWidget.setCurrentIndex(1))
        self.sc_cam3.activated.connect(lambda: self.ui.tabWidget.setCurrentIndex(2))      
    
   
    def handle_joystick_events(self):


        pygame.init()
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        hsped = 0
        vsped = 0

        
        datar = ""
        while True:

                state1=0          
                state2=0
                state3=0
                state4=0
                state5=0

                
                servo = 0

                x = 0
            
                ver_horse_ = None
                Forw_back_Axis= None
                Hor_rotation_axis= None
                Hor_letrals = None
                roll_horse_ = None
                up_down_axis = None

                servosend = 0

                p_gripper = False
                S_gripper = False
                R_gripper = False
                Led = False
                Imu = False

                if x == 3:
                    x == 0 
                    #joysticks motions with deadzones
                
                pygame.event.pump()
                x_axis = int(joystick.get_axis(1)*90)      #for forward/backward
                y_axis = int(joystick.get_axis(0)*90)      #for left/right
                z_axis = int(joystick.get_axis(2)*90)      #for up/down
                # w_axis = int(5)      #for rotate.// left/right 
                w_axis = int(joystick.get_axis(5)*90)      #for rotate left/right
                h_axis = int(joystick.get_axis(3)*90)      #for horse 
                # r_axis = int(50)      #for rol/ 
                r_axis = int(joystick.get_axis(4)*90)      #for roll 
 
                c_axis = joystick.get_hat(0)               #for servo


                if (x_axis <= -5) & (y_axis in range (-5,5)) & (w_axis in range (-5,5)) :
                    Forw_back_Axis = x_axis
                    hsped = abs(x_axis)
                    self.ui.lcdForward.display(x_axis)

                elif x_axis > 5 & (y_axis in range (-5,5)) & (w_axis in range (-5,5)):
                    Forw_back_Axis = x_axis
                    hsped = abs(x_axis)
                    self.ui.lcdForward.display(x_axis)

                elif (y_axis >= 5) & (x_axis in range (-5,5)) & (w_axis in range (-5,5)):
                    Hor_letrals = y_axis
                    hsped = abs(y_axis)
                    self.ui.lcdLateral.display(y_axis)

                elif y_axis < -5  & (x_axis in range (-5,5)) & (w_axis in range (-5,5)):
                    Hor_letrals = y_axis
                    hsped = abs(y_axis)
                    self.ui.lcdLateral.display(y_axis)

                elif (w_axis >= 5) & (y_axis in range (-5,5)) & (x_axis in range (-5,5)):
                    Hor_rotation_axis  = w_axis
                    hsped = abs(w_axis)
                    self.ui.lcdRotaion.display(2*w_axis)

                elif w_axis < -5 & (y_axis in range (-5,5)) & (x_axis in range (-5,5)) :
                    Hor_rotation_axis  = w_axis
                    hsped = abs(w_axis)
                    self.ui.lcdRotaion.display(2*w_axis)

                 elif (w_axis in range (-5,5)) & (x_axis in range (-10,10)) & (y_axis in range (-5,5)) :
                    Hor_rotation_axis= 0
                    Hor_letrals = 0
                    Forw_back_Axis = 0
                else:
                    Hor_rotation_axis= 0
                    Hor_letrals = 0
                    Forw_back_Axis = 0



                if (z_axis != 0) :  #up/down 
                    if (abs(z_axis) >10):
                        self.ui.lcdVertical.display(z_axis)
                        vsped = z_axis
                        up_down_axis = z_axis
                    else:
                        up_down_axis = 0
                        self.ui.lcdVertical.display(0)

                elif (h_axis != 0) : 
                    if (abs(h_axis) >10):
                        vsped = h_axis
                        self.ui.lcdHorse.display(h_axis)
                        ver_horse_ = h_axis
                    else:
                        ver_horse_ = 0
                        self.ui.lcdHorse.display(0)

                elif (r_axis != 0) : 
                    if (abs(r_axis) >10):
                        vsped = r_axis
                        self.ui.lcdRoll.display(r_axis)
                        roll_horse_ = r_axis
                    else:
                        roll_horse_ = 0 
                        self.ui.lcdRoll.display(0)
                else:
                    up_down_axis= 0
                    roll_horse_ = 0
                    ver_horse_ = 0


        
                p_grip  = joystick.get_button(0)
                s_grip  = joystick.get_button(4)
                r_grip  = joystick.get_button(3)
                led  = joystick.get_button(11)
                tabs = joystick.get_button(5)
                mech_4 = joystick.get_button(9)

                    
                if p_grip == True :
                    time.sleep(0.3)
                    p_gripper = not p_gripper
                    state1 = not state1
                    self.ui.PrimGripper.setText('ON' if state1 else 'OFF')
                    self.ui.PrimGripper.setAlignment(Qt.AlignCenter)
                    self.ui.PrimGripper.setStyleSheet(f'QLabel {{ background-color : {"green" if state1 else "red"} ; }}')
                


                if s_grip  == True:
                    time.sleep(0.3)
                    state3 = not state3
                    S_gripper = not S_gripper
                    self.ui.SecondaryGripper.setText('ON'if state3 else 'OFF')
                    self.ui.SecondaryGripper.setAlignment(Qt.AlignCenter)
                    self.ui.SecondaryGripper.setStyleSheet(f'QLabel {{ background-color : {"green" if state3 else "Red"}; }}')
            

                    
                    #print("Event")

                    if r_grip == True:    
                    time.sleep(0.3)     
                    state2 = not state2
                    R_gripper = not R_gripper
        
                    self.ui.GripperRotaion.setText('+90' if state2 else '-90')
                    self.ui.GripperRotaion.setAlignment(Qt.AlignCenter)
                    self.ui.GripperRotaion.setStyleSheet(f'QLabel {{ background-color : {"green" if state2 else "Red"}; }}')

                

                # # #LED 
                if led == True:
                    time.sleep(0.3)
                    state4 = not state4
                    Led = not Led                            
                    self.ui.LED.setText('ON' if state4 else 'OFF')
                    self.ui.LED.setAlignment(Qt.AlignCenter)
                    self.ui.LED.setStyleSheet(f'QLabel {{ background-color : {"green" if state4 else "Red"}; }}')


                if tabs == True:
                        time.sleep(0.3)
                        x = x +1
                        if x == 3:
                            x=0
                        self.ui.tabWidget.setCurrentIndex(x)


                # #####################################################################################################  
                #for imu
                if mech_4 == 9:
                        time.sleep(0.3)
                        state5 = not state5
                        Imu = not Imu
                        self.ui.imu.setText('ON' if state5 else 'OFF')
                        self.ui.imu.setAlignment(Qt.AlignCenter)
                        self.ui.imu.setStyleSheet(f'QLabel {{ background-color : {"green" if state5 else "Red"}; }}')

                if c_axis[1] == 1:
                    time.sleep(0.3)
                    servo += 10
                    servosend = 2
                if servo > 90:
                    servo = 90
                
                elif c_axis[1] == -1:
                    time.sleep(0.3)
                    servosend = 1
                    servo -= 10
                if servo < -90:
                    servo = -90

                self.ui.stepper_dial.setValue(servo)
                self.ui.stepper_lcd.display(servo)
                

                    #print(event)
                
                on_off = int("".join(str(x) for x in [int(p_gripper),
                        int(S_gripper),
                        int(R_gripper),
                        int(Led),
                        int(Imu)]), 2)
                
                #  for event in pygame.event.get():
                
                # if abs(hsped-hsped_old)>1 or abs(vsped-vspeed_old)>1 or on_off!= on_off_old or servosend!=servosend_old:
                # time.sleep(0.05) 
                data=  SFMessage(For_back= Forw_back_Axis,
                                        RR_RL= Hor_rotation_axis,
                                        right_left=Hor_letrals,
                                        roll_horse=roll_horse_,
                                        up_down=up_down_axis,
                                        ver_horse= ver_horse_,
                                        servo_=servosend,
                                        switches=on_off)
                    
                # for event in pygame.event.get():
                try:    
                        send_msg = (str(data))
                        #send_msg = self.data_q.ge
                        sock.sendall(str(send_msg).encode('utf-8'))
                        logger.info(f"sending {send_msg} to serial")
                        self.ui.ROV.setText("Connected") 
                        self.ui.ROV.setStyleSheet("QLabel { background-color : green;}")
                        #self.__sock.flushOutput

                except:
                        logger.warning("writing to serial!")
                        self.ui.ROV.setText("Disconnected") 
                        self.ui.ROV.setStyleSheet("QLabel { background-color : red;}")
                        Socket_try()

                try:
                        sock.settimeout(0.02)
                        datar = sock.recv(1024)
                        datar = datar.decode()
                        logger.info(f"received {datar}")  

                                
                except:
                        Socket_try()
                        pass

                readings = datar.split(',') 

                        #print(msg)
                try:
                            yaw = int(readings[0])
                            pitch = int(readings[1])
                            roll = int(readings[2])
                            self.ui.lcdYaw.display(yaw)
                            self.ui.lcdPitch.display(pitch)
                            self.ui.lcdRoll.display(roll)
                except:
                            pass  
                # time.sleep(0.01)
                hsped_old = hsped
                vspeed_old = vsped
                on_off =0
                servosend = 0

        


    
             

                            
                            
                        
                            
                                
                    
      
def main():

    app = QApplication(sys.argv)
    win = UI()
    app.exec_()

if __name__ == "__main__":
    main()
