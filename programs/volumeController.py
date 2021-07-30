from continuous_rectifier import continuous_rectifier
from handDetector import HandDetector
import cv2
import math
import numpy as np
import os

handDetector = HandDetector(min_detection_confidence=0.7)

webcamFeed = None

for i in range(5):
    try:
        webcamFeed = cv2.VideoCapture(i)
        break
    except:
        webcamFeed = None

previous_length=50

print("\n\n")
while True:
    status, image = webcamFeed.read()
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)

    if(len(handLandmarks) != 0):
        #for volume control we need 4th and 8th landmark
        #details: https://google.github.io/mediapipe/solutions/hands
        x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
        x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
        length = math.hypot(x2-x1, y2-y1)
        length = abs(int(continuous_rectifier(0, length, 110)) - 10)

        if abs(length-previous_length) > 5:
            previous_length = length
            print("Volume: {}% {}                                     ".format(length, "="*(length//10)), end="\r")
            os.system("amixer -q sset Master {}%".format(length))

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
webcamFeed.release()

