from imp import IMP_HOOK
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QPixmap, QImage
import cv2 
import mss 
import numpy
import math as m  
from draw2 import lenght
from vid import yolo
import numpy as np
from mapping import mapping
from ship_wrick import lenght2
class VideoPlayerThread(QThread):
    """
    Processes the video file or display it as it (if so,
    use media player insteed of cv2 (faster))
    """
    pix_sig = pyqtSignal(int,QPixmap)

    def __init__(self, img_dim,task ) :  #farmers code change str to dirc 
        self.__img_dim = img_dim
        self.task = task 
        super().__init__()
    def run(self) -> None:
        self.__thread_active = True
        capture = cv2.VideoCapture(self.__img_dim)
        qimg: QImage
        if self.task == 1:
                
            while self.__thread_active and capture.isOpened():
                ret, frame = capture.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    #print(type(frame))
                    # START_OF(Image Team) Process your frame here into qimg

                    # Code !!!
                    frame = yolo(frame)
                   # frame = np.array([frame])
                   # print(frame[0].shape)
                    frame = np.array(frame)
                    # END_OF(Image Team)
                    qimg = QImage(frame.data, frame.shape[1], frame.shape[0],
                                QImage.Format_RGB888)
                    self.pix_sig.emit(0,QPixmap.fromImage(qimg))
                    self.msleep(1000 // 30) # Lower CPU than cv2.waitKey (WTF!!)
            self.pix_sig.emit(1,QPixmap.fromImage(qimg))
            



        if self.task == 2:
                
            while self.__thread_active and capture.isOpened():
                ret, frame = capture.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # START_OF(Image Team) Process your frame here into qimg

                    # Code !!!
                    

                    # END_OF(Image Team)
                    qimg = QImage(frame.data, frame.shape[1], frame.shape[0],
                                QImage.Format_RGB888)
                    self.pix_sig.emit(0,QPixmap.fromImage(qimg))
                    self.msleep(1000 // 30) # Lower CPU than cv2.waitKey (WTF!!)
            self.pix_sig.emit(1,QPixmap.fromImage(qimg))
            lenght(frame)

        if self.task == 6:
                
            while self.__thread_active and capture.isOpened():
                ret, frame = capture.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # START_OF(Image Team) Process your frame here into qimg

                    # Code !!!
                    

                    # END_OF(Image Team)
                    qimg = QImage(frame.data, frame.shape[1], frame.shape[0],
                                QImage.Format_RGB888)
                    self.pix_sig.emit(0,QPixmap.fromImage(qimg))
                    self.msleep(1000 // 30) # Lower CPU than cv2.waitKey (WTF!!)
            self.pix_sig.emit(1,QPixmap.fromImage(qimg))
            mapping()
            #self.pix_sig.emit(1,QPixmap.fromImage(qimg))

        if self.task == 5:
                
            while self.__thread_active and capture.isOpened():
                ret, frame = capture.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # START_OF(Image Team) Process your frame here into qimg

                    # Code !!!
                    

                    # END_OF(Image Team)
                    qimg = QImage(frame.data, frame.shape[1], frame.shape[0],
                                QImage.Format_RGB888)
                    self.pix_sig.emit(0,QPixmap.fromImage(qimg))
                    self.msleep(1000 // 30) # Lower CPU than cv2.waitKey (WTF!!)
            self.pix_sig.emit(1,QPixmap.fromImage(qimg))
            lenght2(frame)
        


        # with mss.mss() as sct:
        #     monitor = self.__img_dim
        #     while "Screen capturing":
        #         image = numpy.asarray(sct.grab(monitor))
        #         image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        #         height, width, channel = image.shape
        #         bytesPerLine = 3 * width
        #         #Convert Numpy materix to QImage: QImage >> QPixman 
        #         q_img = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888) #*** BgR
        #         #To Deal with gui using signal
        #         self.pix_sig.emit(QPixmap.fromImage(q_img))
        #         self.wait(5)  

    def stop(self):
        self.__thread_active = False
        self.quit()