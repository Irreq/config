import pygame, sys, math

class Cam:
    def __init__(self,pos=(0,0,0),rot=(0,0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def update(self,dt,key):

        s = dt*10
        if key[pygame.K_LEFT]: self.pos[0] +=s
        if key[pygame.K_RIGHT]: self.pos[0] -=s
        if key[pygame.K_DOWN]: self.pos[1] -=s
        if key[pygame.K_UP]: self.pos[1] +=s

        #x,y = s*math.sin(self.rot[1]), s*math.cos(self.rot[1])
        if key[pygame.K_w]: self.pos[2] +=s
        if key[pygame.K_s]: self.pos[2] -=s
        # if key[pygame.K_a]: self.pos[0] -=s
        # if key[pygame.K_d]: self.pos[0] +=s

pygame.init()
w,h = 1000,1000;cx,cy = w//2,h//2
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

b = w/2

verts = (-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)
edges = (0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)

cam = Cam((0,0,-5))




from continuous_rectifier import continuous_rectifier
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
                xPos, yPos, zPos = int(landMark.x * imgW), int(landMark.y * imgH), landMark.z
                landMarkList.append([id, xPos, yPos, zPos])

        return landMarkList

handDetector = HandDetector(min_detection_confidence=0.7)

webcamFeed = cv2.VideoCapture(2)


while webcamFeed.isOpened():
    success, image = webcamFeed.read()

    if not success:  # Empty frame
        continue
    handLandmarks = handDetector.findHandLandMarks(image=image)

    dt = clock.tick()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()

    screen.fill((0,0,0))

    for edge in edges:
        points = []
        for x,y,z in (verts[edge[0]],verts[edge[1]]):
            x-=cam.pos[0]
            y-=cam.pos[1]
            z-=cam.pos[2]

            f = b/z
            x,y = x*f,y*f
            points += [(cx+int(x),cy+int(y))]
        pygame.draw.line(screen,(250,0,250),points[0],points[1],1)


    pygame.display.flip()

    key = pygame.key.get_pressed()
    cam.update(dt,key)


    if(len(handLandmarks) != 0):
        #for volume control we need 4th and 8th landmark
        #details: https://google.github.io/mediapipe/solutions/hands

        (_, x1, y1, z1) = handLandmarks[4]
        (_, x2, y2, z2) = handLandmarks[8]

        length = int(math.hypot(x2-x1, y2-y1))

        length = abs(int(continuous_rectifier(20, length, 120)-20))

        length = 101 - length
        cam.pos[2] = length



webcamFeed.release()
