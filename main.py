"""
Created on Sun Aug 15 15:51:28 2021

@author: Alexandre
"""

import sys
from time import sleep
import pygame
from core import keybordCMD, RobotMotors


class Robot:

    def __init__(self, factor=0.2, size=[400, 300], verbose=0):
        # Initialize video system
        pygame.init()

        # Set the height and width of the screen
        self.screen = pygame.display.set_mode(size)

        self.factor = factor
        self.verbose = verbose
        self.rm = RobotMotors(
            21, 20, 16, # Left motor
            18, 23, 24, # Right motor
            verbose=self.verbose
        )

    def start(self):
        print("#"*78, "{:^78}".format('Start'), "#"*78, sep="\n")
        try:
            while True:
                cmd = keybordCMD(self.factor)
                print("[INFO]", cmd)
                self.rm.move(**cmd)
                sleep(1./30)
        except KeyboardInterrupt:
            pass
        print("#"*78, sep="\n\n")



if __name__ == '__main__':
    if len(sys.argv)>1:
        factor = float(sys.argv[1])

    # Initialization
    rbt = Robot(factor=factor)

    # Start the routine
    rbt.start()
