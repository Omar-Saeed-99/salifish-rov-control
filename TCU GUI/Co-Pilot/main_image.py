#!/usr/bin/python3

# built in
import sys
import os
import time
from matplotlib.pyplot import text
import mss 
# pip installed
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2 as cv
import socket
import numpy 
import pickle,struct,imutils
# co_pilot
from co_pilot_ui import *
from vedio_player import VideoPlayerThread
from co_pilot_cv import MapProcessingThread


host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
class socketconnection(QThread):
    def __init__(self, ):
        super(socketconnection,self).__init__()
    def run(self):

        try:
            server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            socket_address = (host_ip,port)
            server_socket.bind(socket_address)
            server_socket.listen(5)
            print("LISTENING AT:",socket_address)
        except:
            print("establishing socket connection")
            return

        try:
            while True:
             client_socket,addr = server_socket.accept()
             print('GOT CONNECTION FROM:',addr)
             if client_socket:
              vid = cv.VideoCapture(0)
    
              while(vid.isOpened()):
               img,frame = vid.read()
               frame = imutils.resize(frame,width=320)
               a = pickle.dumps(frame)
               message = struct.pack("Q",len(a))+a
               client_socket.sendall(message)
        except:
            print ("writing to serial")



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.input_1.setPlaceholderText("Inter input(2)")
        self.ui.input_2.setPlaceholderText("Inter input(1)")
        self.ui.input_3.setPlaceholderText("Inter input(3)")
        self.ui.input_n.setPlaceholderText("inter(n) value")
        self.ui.input_a.setPlaceholderText("inter(a) value")
        self.ui.input_l.setPlaceholderText("inter(L) value")
        self.ui.biomass_b.setPlaceholderText("inter(b) value")

        socket = socketconnection ()
        socket.start()
        


        self.active_thread_pool: [[QThread, QLabel]] = []  # for future stopping
        self.video_player_thread: VideoPlayerThread
        self.map_processing_thread: MapProcessingThread

        self.ui.pb_videoBrowse.clicked.connect(lambda: self.browse_file(self.ui.video_path))
        self.ui.pb_run_2.clicked.connect(self.play_video)

        
        self.ui.pb_ai.clicked.connect(lambda: self.AI_Fish_Detector(1))
        self.ui.pb_fishlength.clicked.connect(lambda: self.Measure_fish_length(2))
        self.ui.pb_capture.clicked.connect(lambda: self.photo_capture(3))
        self.ui.pb_mosaic.clicked.connect(lambda: self.Photo_Mosaic(4))
        self.ui.pb_shipwreck.clicked.connect(lambda: self.Measure_ship_wreck(5))
        self.ui.pb_Mapping.clicked.connect(lambda: self.Mapping(6))

        
        self.ui.pb_mapBrowse.clicked.connect(lambda: self.browse_file(self.ui.map_png_path))
        self.ui.map_png_path.textChanged.connect(self.map_selected)
        self.ui.pb_processMap.clicked.connect(self.process_map)

        self.ui.avreg.clicked.connect(self.calcutaions)
        self.ui.avreg_mass.clicked.connect(self.avg_mass)
        self.ui.tab_copilot.currentChanged.connect(self.tab_changed)
        
        self.handle_keyboard_shortcuts()
      
    
    #Switch Between tabs
    def handle_keyboard_shortcuts(self):
        self.sc_cam1 = QShortcut(QKeySequence('Alt+1'), self)
        self.sc_cam2 = QShortcut(QKeySequence('Alt+2'), self)
        self.sc_cam3 = QShortcut(QKeySequence('Alt+3'), self)
        self.sc_cam4 = QShortcut(QKeySequence('alt+4'), self)
        self.sc_cam1.activated.connect(lambda: self.ui.tab_copilot.setCurrentIndex(0))
        self.sc_cam2.activated.connect(lambda: self.ui.tab_copilot.setCurrentIndex(1))
        self.sc_cam3.activated.connect(lambda: self.ui.tab_copilot.setCurrentIndex(2))  
        self.sc_cam4.activated.connect(lambda: self.ui.tab_copilot.setCurrentIndex(3))
    
    ###############################################################################################
    #NEW2022/Randa 
    #Task (2)

    def AI_Fish_Detector (self, index: int) -> None:
       monitor = 'fish_practice_video_12 (1080p).mp4' # المفروض ياخد من بروز :)
       if self.ui.pb_ai.isChecked():
            self.ui.pb_ai.setStyleSheet("background-color: green;color: rgb(255, 255, 255)")
            self.video_player_thread= VideoPlayerThread(monitor,index)
            self.video_player_thread.pix_sig.connect(lambda ret, qpix: self.ui.lb_video.setPixmap(qpix) if ret == 0 else self.ui.lb_video.setText("Video Ended"))
            self.video_player_thread.start()
            self.active_thread_pool.append([self.video_player_thread, self.ui.lb_video])
       else:
            self.ui.pb_ai.setStyleSheet("background-color: rgb(116, 0, 0); color: rgb(255, 255, 255)")
            self.video_player_thread.stop()
            self.ui.lb_video.setText('No Signal')
    def Measure_fish_length (self, index: int) -> None:
        monitor = "FISH_Trim.mp4"#'rtsp://admin:sailfish1234@192.168.1.108:554/cam/realmonitor?channel=0&subtype=0'
        if self.ui.pb_fishlength.isChecked():
            self.ui.pb_fishlength.setStyleSheet("background-color: green;color: rgb(255, 255, 255)")
            self.video_player_thread= VideoPlayerThread(monitor,index)
            self.video_player_thread.pix_sig.connect(lambda ret, qpix: self.ui.lb_video.setPixmap(qpix) if ret == 0 else self.ui.lb_video.setText("Video Ended"))
            self.video_player_thread.start()
            self.active_thread_pool.append([self.video_player_thread, self.ui.lb_video])
        else:
            self.ui.pb_fishlength.setStyleSheet("background-color: rgb(116, 0, 0); color: rgb(255, 255, 255)")
            self.video_player_thread.stop()
            self.ui.lb_video.setText('No Signal')


    ####################################################################################################

    def calcutaions(self):
      
        input1 = self.ui.input_1.text()
        
        input2 = self.ui.input_2.text()
       
        input3 = self.ui.input_3.text()
        
    
        avreg_length = (float(input1) + float(input2) + float(input3)) / 3
        ave_len = QMessageBox(1, "Average Length", f"Avarge Length = {avreg_length} cm", QMessageBox.Ok)
        ave_len.setStyleSheet("QLabel { font-size: 24pt;}")
        ave_len.exec()
    
    def avg_mass(self):
        a = self.ui.input_a.text()
        b = self.ui.biomass_b.text()
        l = self.ui.input_l.text()
        n = self.ui.input_n.text()
        bio_mass = float(n) * float(a) * float(l)**float(b)
        biomass = QMessageBox(0, "BioMass", f"Biomass = {bio_mass} Kg", QMessageBox.Ok)
        biomass.setStyleSheet("QLabel { font-size: 24pt;}")
        biomass.exec() 

    ################################################################################################
    #Task(3)
  #Task(3)
    def photo_capture(self, index: int) -> None:
        monitor = 0
        if self.ui.pb_capture.isChecked():
            self.ui.pb_capture.setStyleSheet("background-color: green;color: rgb(255, 255, 255)")
            self.video_player_thread= VideoPlayerThread(monitor,index)
            self.video_player_thread.pix_sig.connect(lambda ret, qpix: self.ui.lb_origMap.setPixmap(qpix) if ret == 0 else self.ui.lb_origMap.setText("Video Ended"))
            self.video_player_thread.start()
            self.active_thread_pool.append([self.video_player_thread, self.ui.lb_origMap])
        else:
            self.ui.pb_capture.setStyleSheet("background-color: rgb(116, 0, 0); color: rgb(255, 255, 255)")
            self.video_player_thread.stop()
            self.ui.lb_origMap.setText('No Signal')
    
    def Photo_Mosaic(self, index: int) -> None:
        monitor = ["videoplayback.mp4",]
        if self.ui.pb_mosaic.isChecked():
            self.ui.pb_mosaic.setStyleSheet("background-color: green;color: rgb(255, 255, 255)")
            self.video_player_thread= VideoPlayerThread(monitor[index])
            self.video_player_thread.pix_sig.connect(lambda ret, qpix: self.ui.lb_origMap.setPixmap(qpix) if ret == 0 else self.ui.lb_origMap.setText("Video Ended"))
            self.video_player_thread.start()
            self.active_thread_pool.append([self.video_player_thread, self.ui.lb_origMap])
        else:
            self.ui.pb_mosaic.setStyleSheet("background-color: rgb(116, 0, 0); color: rgb(255, 255, 255)")
            self.video_player_thread.stop()
            self.ui.lb_origMap.setText('No Signal')

    def Measure_ship_wreck(self, index: int) -> None:
        monitor =  "wrick.mp4"#'rtsp://admin:sailfish1234@192.168.1.108:554/cam/realmonitor?channel=0&subtype=0'
                #'rtsp://admin:sailfish1234@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0
        print(index)
        if self.ui.pb_shipwreck.isChecked():
            self.ui.pb_shipwreck.setStyleSheet("background-color: green;color: rgb(255, 255, 255)")
            self.video_player_thread= VideoPlayerThread(monitor,index)
            self.video_player_thread.pix_sig.connect(lambda ret, qpix: self.ui.lb_origMap.setPixmap(qpix) if ret == 0 else self.ui.lb_origMap.setText("Video Ended"))
            self.video_player_thread.start()
            self.active_thread_pool.append([self.video_player_thread, self.ui.lb_origMap])
        else:
            self.ui.pb_shipwreck.setStyleSheet("background-color: rgb(116, 0, 0); color: rgb(255, 255, 255)")
            self.video_player_thread.stop()
            self.ui.lb_origMap.setText('No Signal')

    def Mapping(self, index: int) -> None:
        #print(index)
        monitor =  "mapping.mp4"#'rtsp://admin:sailfish1234@192.168.1.108:554/cam/realmonitor?channel=0&subtype=0'
        if self.ui.pb_Mapping.isChecked():
            self.ui.pb_Mapping.setStyleSheet("background-color: green;color: rgb(255, 255, 255)")
            self.video_player_thread= VideoPlayerThread(monitor,index)
            self.video_player_thread.pix_sig.connect(lambda ret, qpix: self.ui.lb_origMap.setPixmap(qpix) if ret == 0 else self.ui.lb_origMap.setText("Video Ended"))
            self.video_player_thread.start()
            self.active_thread_pool.append([self.video_player_thread, self.ui.lb_origMap])
        else:
            self.ui.pb_Mapping.setStyleSheet("background-color: rgb(116, 0, 0); color: rgb(255, 255, 255)")
            self.video_player_thread.stop()
            self.ui.lb_origMap.setText('No Signal')
        


    #####################################################################################################

    def browse_file(self, te: QTextEdit):
        path = QFileDialog.getOpenFileName(self, 'Open File')
        te.setText(path[0])

    def play_video(self) -> None:
        file = self.ui.video_path.toPlainText()
        if os.path.exists(file):
            if hasattr(self, 'video_player_thread'):
                if self.video_player_thread.isRunning():
                    self.video_player_thread.stop()

            self.video_player_thread = VideoPlayerThread(file)
            self.video_player_thread.pix_sig.connect(lambda qpix: self.ui.lb_video.setPixmap(qpix) if qpix else self.ui.lb_video.setText("Video Ended"))
            self.video_player_thread.start()
            self.active_thread_pool.append([self.video_player_thread, self.ui.lb_video])
        else:
            msg = QMessageBox()
            msg.setWindowTitle("File Not Found")
            msg.setText("Please provide a file path")
            msg.setIcon(QMessageBox.critical)
            msg.setStyleSheet(self.styleSheet())
            msg.exec_()

    def map_selected(self):
        file: str = self.ui.map_png_path.toPlainText()
        if os.path.exists(file):
            if file.endswith('.png'):
                self.ui.lb_origMap.setPixmap(QPixmap(file).scaled(self.ui.lb_origMap.size()))
            else:
                msg = QMessageBox()
                msg.setWindowTitle("File Type Not PNG")
                msg.setText("Please provide a png file")
                msg.setIcon(QMessageBox.Critical)
                msg.setStyleSheet(self.styleSheet())
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("File Not Found")
            msg.setText("Please provide a file path")
            msg.setIcon(QMessageBox.critical)
            msg.setStyleSheet(self.styleSheet())
            msg.exec_()


    def process_map(self):
        file: str = self.ui.map_png_path.toPlainText()
        if os.path.exists(file):
            if file.endswith('.png'):
                self.ui.lb_origMap.setPixmap(QPixmap(file).scaled(self.ui.lb_origMap.size()))
            else:
                msg = QMessageBox()
                msg.setWindowTitle("File Type Not PNG")
                msg.setText("Please provide a png file")
                msg.setIcon(QMessageBox.Critical)
                msg.setStyleSheet(self.styleSheet())
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("File Not Found")
            msg.setText("Please provide a file path")
            msg.setIcon(QMessageBox.critical)
            msg.setStyleSheet(self.styleSheet())
            msg.exec_()

        self.map_processing_thread = MapProcessingThread(file, self.ui.pb_processMap.size())
        self.map_processing_thread.start()
        self.map_processing_thread.pix_sig.connect(lambda qpix: self.ui.pb_processMap.setPixmap(qpix))

     

    def tab_changed(self, index: int):
        for entry in self.active_thread_pool:
            if entry:
                entry[0].stop()
                entry[1].setText("No Signal")
                self.active_thread_pool.remove(entry)

    def closeEvent(self, event: QCloseEvent):
        for entry in self.active_thread_pool:
            if entry:
                entry[0].stop()
                self.active_thread_pool.remove(entry)
        QMainWindow.closeEvent(self, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
