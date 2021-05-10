from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler


#시각화를 위한 import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#데이터 불러오기
data = pd.read_csv("gooddata.csv")
col = list(map(str,data.columns))
x = data[col[:-1]]
print(x)
y = data[col[-1]]

#PipeLine
scaler = StandardScaler()
base_model = SVC(kernel='rbf')
pipe = Pipeline([('scaler', scaler), ('base_model', base_model)])



# data split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

# grid search을 통한 svm 파라미터 결정시 필요한 요소 설정
parameters = {'base_model__C': [  1000],
          'base_model__gamma': [ 0.01]}
# grid search Part
grid = GridSearchCV(estimator=pipe, param_grid=parameters, cv=5, n_jobs=-1)
grid.fit(X_train, y_train)

# grid search 결과 출력
print(grid)
print(grid.best_score_)
print(grid.best_estimator_)
print(grid.predict(X_test))
print("학습 결과", grid.score(X_train, y_train))
print("테스트 결과", grid.score(X_test, y_test))



#시각화
scores = grid.cv_results_['mean_test_score']
scores = np.array(scores).reshape(len(parameters['base_model__C']), len(parameters['base_model__gamma']))
for ind, i in enumerate(parameters['base_model__C']):
    plt.plot(parameters['base_model__gamma'], scores[ind], label='C: ' + str(i))

plt.legend()
plt.xlabel('Gamma')
plt.ylabel('Mean score')
plt.show()

estimator = grid.best_estimator_
import cv2
import mediapipe as mp
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
neckslice = cv2.imread("./neckslice.jpg")


def dist(P, A, B):
    area = abs((A.x - P.x) * (B.y - P.y) - (A.y - P.y) * (B.x - P.x))
    AB = ((A.x - B.x) ** 2 + (A.y - B.y) ** 2) ** 0.5
    return (area / AB)


def cal_rate(nose, left_mouth, right_mouth, left_shoulder, right_shoulder):
    a = dist(nose, left_shoulder, right_shoulder)
    b = dist(nose, left_mouth, right_mouth)
    r = a / b
    return r



# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        image_height, image_width, _ = image.shape

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if results.pose_landmarks is None:
            print("no landmark")
            continue

        nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        right_ear = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR]
        left_ear = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        shoulder_length = ((left_shoulder.x - right_shoulder.x) ** 2 + (left_shoulder.y - right_shoulder.y) ** 2) ** 0.5

        nose_length = float(dist(nose, left_shoulder, right_shoulder) / shoulder_length)
        rear_length = float(dist(right_ear, left_shoulder, right_shoulder) / shoulder_length)
        lear_length = float(dist(left_ear, left_shoulder, right_shoulder) / shoulder_length)

        test_data = [[nose_length, rear_length, lear_length]]


        cv2.imshow('NeckSlice', image)

        pred = estimator.predict(test_data)

        if (pred == 1):
            cv2.namedWindow('Neck Slice!!')
            cv2.imshow('Neck Slice!!', neckslice)
        else:
            cv2.destroyWindow("Neck Slice!!")

        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
