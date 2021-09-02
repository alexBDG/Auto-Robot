"""
Created on Sun Aug 15 15:51:28 2021

@author: Alexandre
"""

import sys

from gui.game import Game
from hardware.motor import RobotMotors, IS_GPIO_AVAILABLE



if __name__ == '__main__':
    if len(sys.argv)>1:
        factor = float(sys.argv[1])
        
    VERBOSE = 1
        
    if IS_GPIO_AVAILABLE:
        rm = RobotMotors(
            21, 20, 16, # Left motor
            18, 23, 24, # Right motor
            verbose = VERBOSE
        )
    else:
        rm = None
        
    RESOLUTION = (1280, 720)
    FPS = 50
    SPEED = 2.
    ROTATION_SPEED = 1.
    
    g = Game(RESOLUTION, FPS, SPEED, ROTATION_SPEED, rm)
    
    print("#"*78, "{:^78}".format('Start'), "#"*78, sep="\n")
    g.start()
    print("#"*78, sep="\n\n")
