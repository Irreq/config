from continuous_rectifier import continuous_rectifier

import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5,
              min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()

        if not success:  # ignore empty frame
            continue

        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
