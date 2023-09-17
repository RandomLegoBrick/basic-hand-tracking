import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import mediapipe
import mouse
from math import hypot

 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

def lerp(value1, value2, amt):
    return ((value2 - value1) * amt) + value1


capture = cv2.VideoCapture(0)

def clamp(n, minimum, maximum):
    return max(minimum, min(n, maximum))

def dist(x1, y1, x2, y2):
    return hypot(x1-x2, y1-y2)

x = 1920/2
y = 1080/2
thumbX = 0
timeout = 0
thumbY = 0
mousePressed = False

with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1) as hands:
    while True:
 
        ret, frame = capture.read()
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks != None:
    
            
            handLandmarks = results.multi_hand_landmarks[0]
            
            indexFinger = (handLandmarks.landmark[8].x, handLandmarks.landmark[8].y)
            thumb = (handLandmarks.landmark[4].x, handLandmarks.landmark[4].y)

            if dist(indexFinger[0], indexFinger[1], thumb[0], thumb[1]) < 0.02:
               mouse.press()
            else:
                mouse.release()
            
            x = lerp(x, (handLandmarks.landmark[0].x * 2) - 0.5, 0.5)
            y = lerp(y, (handLandmarks.landmark[0].y * 2) - 0.5, 0.5)
            
            mouseX = 1920-(x*1920)
            mouseY = (y*1080)

            mouseX = clamp(mouseX, 0, 1920)
            mouseY = clamp(mouseY, 0, 1920)
            
            mouse.move(mouseX, mouseY)

        
        if cv2.waitKey(1) == 27:
            break
 
cv2.destroyAllWindows()
capture.release()
