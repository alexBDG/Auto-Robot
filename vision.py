# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 10:37:07 2021

@author: Alexandre
"""

import time
import cv2
import numpy as np

from autorobot.gui.game import RealFPS

# used to record the time when we processed last frame
prev_frame_time = 0

# used to record the time at which we processed current frame
new_frame_time = 0

# Asked frames per seconds
FPS = 30

# Set resolution
RESOLUTION = (600, 400)

# Get camera
cap = cv2.VideoCapture(0)
real_fps = RealFPS(100)

print("FPS :", cap.get(cv2.CAP_PROP_FPS))
cap.set(cv2.CAP_PROP_FPS, FPS)
print("FPS :", cap.get(cv2.CAP_PROP_FPS))

print("IMG - width : ", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("    - height :", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  RESOLUTION[0]);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1]);
print("IMG - width : ", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("    - height :", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # ======================= #
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    vertical_separator = np.full(
        shape=(frame.shape[0], 2),#, frame.shape[-1]), 
        fill_value=255,
        dtype=np.uint8
    )
    horizontal_separator = np.full(
        shape=(2, 2*frame.shape[1]+2),#, frame.shape[-1]), 
        fill_value=255,
        dtype=np.uint8
    )
    
    # Apply identity kernel
    kernel1 = np.array([[-1,  0,  1],
                        [-2,  0,  2],
                        [-1,  0,  1]])
    kernel2 = np.array([[-1, -2, -1],
                        [ 0,  0,  0],
                        [ 1,  2,  1]])
    kernel3 = np.array([[-1,  1, -1],
                        [ 1,  0,  1],
                        [-1,  1, -1]])
    kernel3 = np.array([[-1, -1,  1,  1, -1, -1],
                        [-1, -1,  1,  1, -1, -1],
                        [ 1,  1,  0,  0,  1,  1],
                        [ 1,  1,  0,  0,  1,  1],
                        [-1, -1,  1,  1, -1, -1],
                        [-1, -1,  1,  1, -1, -1]])
    frame1 = cv2.filter2D(
        src=frame, ddepth=-1, kernel=kernel1
    )
    frame2 = cv2.filter2D(
        src=frame, ddepth=-1, kernel=kernel2
    )
    frame3 = cv2.filter2D(
        src=frame, ddepth=-1, kernel=kernel3
    )
    
    
    # frame3 = cv2.addWeighted(frame1, .5, frame2, .5, 0)
    
    # frame4 = cv2.GaussianBlur(frame3, (0, 0), cv2.BORDER_DEFAULT)
    # frame3 = cv2.addWeighted(frame3, 1.5, frame4, -0.5, 0)
    
    frame_top = np.concatenate(
        (frame, vertical_separator, frame1), 
        axis=1
    )
    frame_bottom = np.concatenate(
        (frame2, vertical_separator, frame3), 
        axis=1
    )
    frame_final = np.concatenate(
        (frame_top, horizontal_separator, frame_bottom), 
        axis=0
    )
    # ======================= #

    # compute and get the FPS
    real_fps.update()
    fps = "{:<3d} FPS".format(real_fps.get_value())

    # puting the FPS count on the frame
    cv2.putText(frame_final, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('frame', frame_final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
