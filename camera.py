# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 09:53:13 2021

@author: alspe
"""

import time
import cv2
from threading import Thread, Lock
from ..gui.game import RealFPS


class Camera:

    def __init__(self, src=0, width=None, height=None, fps=30, verbose=0):
        """Manage the camera stream.

        Parameters
        ----------
        src : int, default=0
            OpenCV's index of the camera.
            
        width : int, default=None
            Frame's width. If `None`, default width of the camera will be used.
            
        height : int, default=None
            Frame's height. If `None`, default height of the camera will be 
            used.
            
        fps : int, default=None
            How many frame per seconds need to be acquired. If `None`, default 
            FPS of the camera will be used.
            
        verbose : int, default=0
            Display information if set more than `0`.
        """

        # Get the camera
        self.camera = cv2.VideoCapture(src)

        # Set resolution
        if verbose>0:
            print("[CAMERA] initial width:", 
                  self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        if width is not None:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            if verbose>0:
                print("[CAMERA] asked width:", width)
                print("[CAMERA] current width:", 
                      self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        if verbose>0:
            print("[CAMERA] initial height:", 
                  self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if height is not None:
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            if verbose>0:
                print("[CAMERA] asked height:", height)
                print("[CAMERA] current height:", 
                      self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Set FPS
        if verbose>0:
            print("[CAMERA] initial FPS:", 
                  self.camera.get(cv2.CAP_PROP_FPS))
        if fps is not None:
            self.camera.set(cv2.CAP_PROP_FPS, fps)
            if verbose>0:
                print("[CAMERA] asked FPS:", fps)
                print("[CAMERA] current FPS:", 
                      self.camera.get(cv2.CAP_PROP_FPS))

        # Create a FPS tracer
        self.real_fps = RealFPS(10)
        # font which we will be using to display FPS
        self.fps_font = cv2.FONT_HERSHEY_SIMPLEX

        (self.grabbed, self.frame) = self.camera.read()
        self.started = False
        self.read_lock = Lock()


    def start(self) :
        if self.started :
            print("[CAMERA] Acquisition thread already started!")
            return None
        
        # In other case, start a thread with update function as target
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        
        return self


    def update(self) :
        # Main loop
        while self.started:
            (grabbed, frame) = self.camera.read()
            
            # Apply color
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Put the FPS count on the frame
            fps = "{:<3d} FPS".format(self.real_fps.get_value())
            cv2.putText(
                frame, fps, (7, 70), self.fps_font, 3, 
                (100, 255, 0), 3, cv2.LINE_AA
            )
            
            # Save the frame
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()
            
            # Update FPS
            self.real_fps.update()


    def read(self) :
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame


    def stop(self) :
        self.started = False
        self.thread.join()


    def __exit__(self, exc_type, exc_value, traceback) :
        self.stream.release()



if __name__ == "__main__":
    ca = Camera(fps=30, width=1920, height=1080, verbose=1).start()
    while True:
        frame = ca.read()
        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    ca.stop()
    cv2.destroyAllWindows()


