# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 22:32:50 2018

@author: AMarda
"""

import cv2

initial_frame = None
frame_Count = 0
while True:
    frame_Count = frame_Count +1
    # Capturing video from webcam
    video = cv2.VideoCapture(0)
    isReadSuccessFul, frame =video.read();
    
    if(isReadSuccessFul):
        grayedFrame =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        grayedFrame = cv2.GaussianBlur(grayedFrame,(21,21),0)
    
    if (initial_frame is  None):
        initial_frame = grayedFrame
        continue
    
    frame_diff = cv2.absdiff(initial_frame,grayedFrame)
    thresholdFrame = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)[1]
    thresholdFrame = cv2.dilate(thresholdFrame,None,iterations=2)
    
    #Retrieving countours
    image ,contours, hierarchy =cv2.findContours(thresholdFrame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    for con in contours:
        if(cv2.contourArea(con) < 1000):
            continue
        (x,y,w,h)=cv2.boundingRect(con)
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),3)
    
    cv2.imshow("Current", grayedFrame)
    cv2.imshow("Diff to first", frame_diff)
    cv2.imshow("Threshold frame",thresholdFrame)
    
    key = cv2.waitKey(1)
    
    if(key == ord('q') or frame_Count == 100):
        break

# Releasing video cature object after everything is done
video.release()

#Destroyng all windows
cv2.destroyAllWindows()