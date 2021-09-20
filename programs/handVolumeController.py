#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Usage:
Pinch your index-finger and thumb to adjust the audio level
"""

import cv2
import math
import os, time

from continuous_rectifier import continuous_rectifier


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
                xPos, yPos, zPos = int(landMark.x * imgW), int(landMark.y * imgH), landMark.z
                landMarkList.append([id, xPos, yPos, zPos])

        return landMarkList

handDetector = HandDetector(min_detection_confidence=0.7)



def capture(duration=10, verbose=False):
    previous_length = 50
    for i in range(1,9):
        try:
            webcamFeed = cv2.VideoCapture(i)
            break
        except:
            webcamFeed = None

    if webcamFeed is None:
        return

    webcamFeed = cv2.VideoCapture(2)
    launch_time = time.time()
    while webcamFeed.isOpened():
        success, image = webcamFeed.read()

        if not success:  # Empty frame
            continue
        handLandmarks = handDetector.findHandLandMarks(image=image)

        if(len(handLandmarks) != 0):
            # details: https://google.github.io/mediapipe/solutions/hands
            (_, x1, y1, z1) = handLandmarks[4]
            (_, x2, y2, z2) = handLandmarks[8]

            length = int(math.hypot(x2-x1, y2-y1))

            length = abs(int(continuous_rectifier(20, length, 120)-20))

            if abs(length-previous_length) > 5:
                previous_length = length
                os.system("amixer -q sset Master {}%".format(length))

                if verbose:
                    print("Volume: {}% {}                                     ".format(length, "="*(length//3)), end="\r")

        if time.time() - launch_time > duration:
            webcamFeed.release()


if __name__ == "__main__":

    capture()
