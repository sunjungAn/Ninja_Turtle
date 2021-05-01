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

# For static images:
with mp_pose.Pose(
    static_image_mode=True, min_detection_confidence=0.5) as pose:
    image = cv2.imread("./origin.jpg")
    image_height, image_width, _ = image.shape
    # Convert the BGR image to RGB before processing.
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Draw pose landmarks on the image.
    annotated_image = image.copy()
    # Use mp_pose.UPPER_BODY_POSE_CONNECTIONS for drawing below when
    # upper_body_only is set to True.
    mp_drawing.draw_landmarks(
        annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    n = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
    lm = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT]
    rm = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT]
    ls = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    rs = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    r = cal_rate(n, lm, rm, ls, rs) - 0.3
    cv2.imwrite('./result.jpg', annotated_image)

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
    left_mouth = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT]
    right_mouth = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT]
    left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    rate = cal_rate(nose, left_mouth, right_mouth, left_shoulder, right_shoulder)

    cv2.putText(image, "TurtleNeck Ratio : {}".format(r),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)    
    cv2.putText(image, "Current Ratio : {}".format(rate),(10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    cv2.imshow('NeckSlice', image)
        
    if(rate<r):
      cv2.namedWindow('Neck Slice!!')
      cv2.imshow('Neck Slice!!',neckslice)
    else:
        cv2.destroyWindow("Neck Slice!!")
      
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
