import cv2
import mediapipe as mp
import os
import csv
EPOCH = 5000

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
f1 = open('gooddata.csv','w', newline='')
f2 = open('goodweight.csv', 'w', newline='')

wr1 = csv.writer(f1)
wr2 = csv.writer(f2)
wr1.writerow(['nose length', 'right_ear length', 'left_ear length'])
wr2.writerow(['weight'])
epoch = 0

def dist(P, A, B):
    area = abs((A.x - P.x) * (B.y - P.y) - (A.y - P.y) * (B.x - P.x))
    AB = ((A.x - B.x) ** 2 + (A.y - B.y) ** 2) ** 0.5
    return (area / AB)

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

    nose_length = dist(nose, left_shoulder, right_shoulder) / shoulder_length
    rear_length = dist(right_ear, left_shoulder, right_shoulder) / shoulder_length
    lear_length = dist(left_ear, left_shoulder, right_shoulder) / shoulder_length
    wr1.writerow([nose_length, rear_length, lear_length])
       
    cv2.putText(image, "Good Pose",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    cv2.putText(image, "nose length: {}".format(nose_length),(10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    cv2.putText(image, "right_ear length: {}".format(rear_length),(10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    cv2.putText(image, "left_ear length: {}".format(lear_length),(10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)   
    wr2.writerow([0])
    epoch += 1

    cv2.imshow('Good Pose', image)
      
    if (cv2.waitKey(5) & 0xFF == 27) or epoch == EPOCH:
        f1.close()
        f2.close()
        break
cap.release()
