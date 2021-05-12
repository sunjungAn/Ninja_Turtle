# GUI를 위한 import
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import cam

# Media PipePose를 위한 import
import numpy as np
import sys
import cv2
import mediapipe as mp
import joblib

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pkl_file = 'SVM.pkl'
estimator = joblib.load(pkl_file)
warning = cv2.imread("./warning.jpg")


# 수선의 발 길이를 구하는 함수
def dist(P, A, B):
    area = abs((A.x - P.x) * (B.y - P.y) - (A.y - P.y) * (B.x - P.x))
    AB = ((A.x - B.x) ** 2 + (A.y - B.y) ** 2) ** 0.5
    return (area / AB)

class VideoThread(QThread):
    
    change_pixmap_signal = pyqtSignal(np.ndarray)
    flag = -1

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        with mp_pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as pose:
            while self._run_flag:
                success, image = cap.read()

                image_height, image_width, _ = image.shape

                # Flip the image horizontally for a later selfie-view display, and convert
                # the BGR image to RGB.
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                results = pose.process(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.pose_landmarks is None:
                    print("no landmark")
                    continue

                nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
                left_mouth = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT]
                right_mouth = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT]
                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                left_ear = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR]
                right_ear = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR]
                shoulder_length = ((left_shoulder.x - right_shoulder.x) ** 2 + (left_shoulder.y - right_shoulder.y) ** 2) ** 0.5

                nose_length = dist(nose, left_shoulder, right_shoulder) / shoulder_length
                rear_length = dist(right_ear, left_shoulder, right_shoulder) / shoulder_length
                lear_length = dist(left_ear, left_shoulder, right_shoulder) / shoulder_length

                test_data = [[nose_length, rear_length, lear_length]]
                pred = estimator.predict(test_data)
                
                if success:
                    self.change_pixmap_signal.emit(image)

                if (pred == 1):
                    cv2.namedWindow('Warning')
                    cv2.imshow('Warning', warning)
                else:
                    cv2.destroyWindow("Warning")
                    
                if cv2.waitKey(5) & 0xFF == 27:
                    break        
            cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


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
        #self.thread.flag = -1  # 캠이 꺼짐을 의미


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Ninja_Turtle = QtWidgets.QDialog()
    ui = Ui_Ninja_Turtle()
    ui.setupUi(Ninja_Turtle)
    Ninja_Turtle.show()
    sys.exit(app.exec_())
