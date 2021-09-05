"""
Created on Sun Aug 15 15:51:28 2021

@author: Alexandre
"""

import sys
import argparse

from autorobot.gui.game import Game
from autorobot.hardware.motor import RobotMotors, IS_GPIO_AVAILABLE


def parseTuple(arg):
    try:
        # Should be a list
        return eval(arg)
    except:
        err = "You do not gave a tuple!"
        argparse.ArgumentTypeError()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Auto-Robot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''
        Welcome with Auto-Robot program!
        --------------------------------
            
        You need to turn on the raspberry
        and to be sure to have a motor power
        supply.
        
        '''
    )

    parser.add_argument(
        '-s', '--speed',
        type=float, default=0.5,
        help='Speed ratio of the car. Should be between 0 and 1.'
    )

    parser.add_argument(
        '-r', '--resolution',
        type=parseTuple, default=(1280, 720),
        help='Windows resolution.'
    )

    parser.add_argument(
        '-f', '--fps',
        type=int, default=50,
        help='Frame per seconds.'
    )

    parser.add_argument(
        '-v', '--verbose',
        type=float, default=0,
        help='Display informations if non null.'
    )

    args = vars(parser.parse_args())

    if IS_GPIO_AVAILABLE:
        rm = RobotMotors(
            21, 20, 16, # Left motor
            18, 23, 24, # Right motor
            verbose = args['verbose']
        )
    else:
        rm = None

    print("#"*78, "{:^78}".format('Start'), "#"*78, sep="\n")
    g = Game(args['resolution'], args['fps'], args['speed'], args['speed'], rm)
    g.start()
    print("#"*78, sep="\n\n")


