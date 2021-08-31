# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 10:37:07 2021

@author: Alexandre
"""

import time
import cv2

# used to record the time when we processed last frame
prev_frame_time = 0

# used to record the time at which we processed current frame
new_frame_time = 0

# Asked frames per seconds
new_fps = 30


cap = cv2.VideoCapture(-1)
print("FPS initial :", cap.get(cv2.CAP_PROP_FPS))
cap.set(cv2.CAP_PROP_FPS, new_fps)
print("FPS demandés :", new_fps)
print("FPS actuels :", cap.get(cv2.CAP_PROP_FPS))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time = time.time()

    # Calculating the fps

    # fps will be number of frame processed in given time frame
    # since their will be most of time error of 0.001 second
    # we will be subtracting it to get more accurate result
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time

    # converting the fps into integer then to string
    fps = str(int(fps))

    # puting the FPS count on the frame
    cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
