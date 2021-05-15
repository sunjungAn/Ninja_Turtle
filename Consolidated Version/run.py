import mediapipe as mp
import numpy as np
import cv2
import sys
import joblib
from PyQt5.QtCore import QThread, pyqtSignal

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pkl_file = 'SVM.pkl'
estimator = joblib.load(pkl_file)
warning = cv2.imread("./warning.jpg")
warning = cv2.resize(warning, None, fx = 0.5, fy = 0.5, interpolation=cv2.INTER_AREA)
loading = cv2.imread("./loading.png")
loading = cv2.resize(loading, None, fx = 0.7, fy = 0.7, interpolation=cv2.INTER_AREA)

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
                    cv2.destroyWindow("Warning")
                    cv2.namedWindow('Loading')
                    cv2.moveWindow('Loading', 750, 300)
                    cv2.imshow('Loading', loading)
                    if cv2.waitKey(5) & 0xFF == 27:
                        break
                    continue        
                cv2.destroyWindow("Loading")

                nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
                left_mouth = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT]
                right_mouth = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT]
                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                left_ear = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR]
                right_ear = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR]
                shoulder_length = ((left_shoulder.x - right_shoulder.x) ** 2 + (left_shoulder.y - right_shoulder.y) ** 2) ** 0.5

                nose_length = float(dist(nose, left_shoulder, right_shoulder) / shoulder_length)
                rear_length = float(dist(right_ear, left_shoulder, right_shoulder) / shoulder_length)
                lear_length = float(dist(left_ear, left_shoulder, right_shoulder) / shoulder_length)

                test_data = [[nose_length, rear_length, lear_length]]
                pred = estimator.predict(test_data)

                if success:
                    self.change_pixmap_signal.emit(image)

                if (pred == 1):
                    cv2.namedWindow('Warning')
                    cv2.moveWindow('Warning', 750, 300)
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
