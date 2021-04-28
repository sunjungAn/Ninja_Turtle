# NeckSlice(ver.1.0)

`거북목 예방 프로그램 연습 구현`

<br>

### 01. Implement NeckSlice

`앞에서 공부한 MediaPipe Pose를 사용하고 비율을 계산하여 NeckSlice 프로그램 구현` 

* 코의 y 좌표

  ```python
  ny = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height
  ```

* 양쪽 입과 어깨의 중앙점 y 좌표 계산

  ```
  my = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT].y + results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT].y)/2 * image_height
  sy = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y + results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)/2 * image_height
  ```

* 어깨의 중앙점과 입의 중앙점 길이 그리고 코와 입의 중앙점의 길이를 구하여 비율 계산

  ```python
  r = (my-sy)/(ny-my)
  ```

  ![image01.PNG](https://github.com/hyunmin0317/OpenCV_Study/blob/master/NeckSlice/NeckSlice(ver.1.0)/Github/image01.PNG?raw=true)

* 영상에서의 비율아 기준(사진에서의 비율 - 0.5)보다 작으면 현재 비율을 출력하고 'neckslice.jpg' 사진을 보여줌

  ```python
  if(rate<r-0.5):
        print("Neck Slice!! - 현재 비율: ", rate)
        cv2.namedWindow('Neck Slice')
        cv2.imshow('Neck Slice',neckslice)
  else:
      cv2.destroyWindow("Neck Slice")
  ```

* 거북목 판정 비율과 현재 비율을 화면에 출력

<br>

### 02. Whole Code

```python
import cv2
import mediapipe as mp
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
neckslice = cv2.imread("./neckslice.jpg")

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
    ny = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height
    my = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT].y + results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT].y)/2 * image_height 
    sy = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y + results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)/2 * image_height
    r = (my-sy)/(ny-my)
    cv2.imwrite('./result.jpg', annotated_image)
    print("평소 비율: ",r)

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

    ny = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height
    my = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT].y + results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT].y)/2 * image_height 
    sy = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y + results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)/2 * image_height
    rate = (my-sy)/(ny-my)
    
    cv2.imshow('MediaPipe Pose', image)
    
    if(rate<r-0.5):
      print("Neck Slice!! - 현재 비율: ", rate)
      cv2.namedWindow('Neck Slice')
      cv2.imshow('Neck Slice',neckslice)
    else:
        cv2.destroyWindow("Neck Slice")
      
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
```

<br>

###  03. NeckSlice Result

![result.PNG](https://github.com/hyunmin0317/Ninja_Turtle/blob/master/NeckSlice/Github/result.PNG?raw=true)