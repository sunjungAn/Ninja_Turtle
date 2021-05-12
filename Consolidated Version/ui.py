import numpy as np
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot

from run import VideoThread

class Ui_Ninja_Turtle(QWidget):
    def setupUi(self, Ninja_Turtle):
        Ninja_Turtle.setObjectName("Ninja_Turtle")
        Ninja_Turtle.resize(412, 294)

        self.pushButton = QtWidgets.QPushButton(Ninja_Turtle)
        self.pushButton.setGeometry(QtCore.QRect(20, 70, 112, 61))
        font = QtGui.QFont()
        font.setFamily("Bodoni MT Black")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Ninja_Turtle)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 140, 112, 61))
        font = QtGui.QFont()
        font.setFamily("Bodoni MT Black")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Ninja_Turtle)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 210, 112, 61))
        self.label = QtWidgets.QLabel(Ninja_Turtle)

        self.label.setPixmap(QtGui.QPixmap("Ninja_Turtle.png").scaled(225, 220))
        self.label.setGeometry(QtCore.QRect(160, 70, 225, 200))

        font = QtGui.QFont()
        font.setFamily("Bodoni MT Black")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.frame = QtWidgets.QFrame(Ninja_Turtle)
        self.frame.setGeometry(QtCore.QRect(150, 30, 231, 241))
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # self.graphicsView.setObjectName("graphicsView")

        # create the video capture thread

        self.retranslateUi(Ninja_Turtle)
        QtCore.QMetaObject.connectSlotsByName(Ninja_Turtle)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(225, 220)  # , Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def retranslateUi(self, Ninja_Turtle):
        _translate = QtCore.QCoreApplication.translate
        Ninja_Turtle.setWindowTitle(_translate("Ninja_Turtle", "Ninja_Turtle"))
        self.pushButton.setText(_translate("Ninja_Turtle", "Exit"))
        self.pushButton.clicked.connect(self.exit)

        self.pushButton_2.setText(_translate("Ninja_Turtle", "Start"))
        self.pushButton_2.clicked.connect(self.start_webcam)

        self.pushButton_3.setText(_translate("Ninja_Turtle", "Stop"))
        self.pushButton_3.clicked.connect(self.stop)

    def exit(self):  # 나가기
        quit()

    def start_webcam(self):
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        self.thread.flag = 1

    def stop(self):
        self.thread.stop()
        self.label.setPixmap(QtGui.QPixmap("Ninja_Turtle.png").scaled(225, 220))
        self.thread.flag = -1  # 캠이 꺼짐을 의미
