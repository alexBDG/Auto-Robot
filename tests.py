# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 10:20:52 2021

@author: alspe
"""


import time
import cv2
import unittest
from autorobot.hardware.camera import Camera


class TestHardware(unittest.TestCase):
    verbose = 1

    def test_camera(self):
        ca = Camera(fps=30, width=1920, height=1080, verbose=self.verbose).start()
        
        start = time.time()
        while (time.time()-start)<10:
            frame = ca.read()
            cv2.imshow('webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        ca.stop()
        cv2.destroyAllWindows()
        

if __name__ == '__main__':
    unittest.main()


