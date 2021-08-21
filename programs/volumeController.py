from continuous_rectifier import continuous_rectifier
# from handDetector import HandDetector
import cv2
import math
import numpy as np
import os

import mediapipe as mp

mpHands = mp.solutions.hands

class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        # Media pipe will first detect hands and then continue to track, if it cannot track anymore
        # it will go back to detecting even though it is more time consuming
        self.hands = mpHands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence,
                                   min_tracking_confidence=min_tracking_confidence)

    def findHandLandMarks(self, image, handNumber=0, draw=False):
        originalImage = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        landMarkList = []

        if results.multi_hand_landmarks:  # Will return None if no hands are found
            hand = results.multi_hand_landmarks[handNumber]

            for id, landMark in enumerate(hand.landmark):
                imgH, imgW, imgC = originalImage.shape  # Height, width and channel for image
                xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
                landMarkList.append([id, xPos, yPos])

        return landMarkList

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
if webcamFeed is None:
    print("no camera was found")
    exit()

#!/usr/local/bin/python3
#import cv2
import numpy as np
import random
# Make empty black image
# background=np.zeros((1000,1000,3),np.uint8)

# while True:
#    # Make one pixel red
#    #
#    point = [random.randrange(0,100), random.randrange(0,100)]
#    image[point[0], point[1]]=[0,0,255]
#
#    cv2.imshow('image',image)
#    cv2.waitKey(1)
#
#    time.sleep(0.01)
#    image[point[0], point[1]]=[0,0,0]

# oldx2, oldy2 = 0, 0
while webcamFeed.isOpened():
    success, image = webcamFeed.read()
    
    if not success:  # Empty frame
        continue
    handLandmarks = handDetector.findHandLandMarks(image=image)

    if(len(handLandmarks) != 0):
        #for volume control we need 4th and 8th landmark
        #details: https://google.github.io/mediapipe/solutions/hands
        x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
        x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
        
        #oldx2, oldy2 = (oldx2 + x2) // 2, (oldy2 + y2) // 2
        #print(oldx2, oldy2, end="                 \r")

        #try:
        #    background[oldy2, -oldx2] = [0,0,255]
        #except:
        #    pass
        #cv2.imshow('image',background)
        #cv2.waitKey(1)

        #try:
        #    background[oldy2, -oldx2] = [0,0,0]
        #except:
        #    pass
        #continue
        length = math.hypot(x2-x1, y2-y1) // 1
        print(length)
        continue
        length = abs(int(continuous_rectifier(0, length, 110)) - 10)

        if abs(length-previous_length) > 5:
            previous_length = length
            print("Volume: {}% {}                                     ".format(length, "="*(length//10)), end="\r")
            os.system("amixer -q sset Master {}%".format(length))

    #if cv2.waitKey(5) & 0xFF == 27:
    #    break


webcamFeed.release()

