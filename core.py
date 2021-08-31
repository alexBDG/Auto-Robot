# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 10:45:00 2021

@author: Alexandre
"""

from time import sleep
from copy import deepcopy
import pygame
try:
    import RPi.GPIO as GPIO
    # Set Pins number config
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
except ImportError:
    print("Not in Raspberry Pi environment!")
    pass


class Motor:

    def __init__(self, ena, in1, in2, verbose=0):

        # Set Pinss
        self.ena = ena
        self.in1 = in1
        self.in2 = in2

        # Setup GPIO
        GPIO.setup(self.ena, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        self.pwm = GPIO.PWM(self.ena, 100) # frequence (Hz)

        # Other
        self.pwm.start(0)
        self.verbose = verbose

    def moveF(self, x=100, t=0):
        if self.verbose>0:
            print("[INFO] moveB - {:.2f}s - {:3}%".format(t, x))
        self.pwm.ChangeDutyCycle(x) # 0. <= x <= 100.
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        sleep(t)

    def moveB(self, x=100, t=0):
        if self.verbose>0:
            print("[INFO] moveB - {:.2f}s - {:3}%".format(t, x))
        self.pwm.ChangeDutyCycle(x) # 0. <= x <= 100.
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        sleep(t)

    def stop(self, t=0):
        if self.verbose>0:
            print("[INFO] stop - {:.2f}s".format(t))
        self.pwm.ChangeDutyCycle(0) # 0. <= x <= 100.
        sleep(t)



def test1():
    print("#"*80, "{:^80}".format('Test #1'), "#"*80, sep="\n")
    # Define motors
    m1 = Motor(21, 20, 16)
    m2 = Motor(18, 23, 24)

    try:
        m2.moveF(x=30, t=0)
        # Infinite loop
        while True:
            m1.moveF(x=30, t=2)
            m1.stop(t=1)
            m1.moveB(t=2)
            m1.stop(t=1)

    except InterruptedError:
        print("[INFO] end of test #1")
        m1.stop(0)
        m2.stop(0)
        pass
    print("#"*80, sep="\n\n")



def bornSpeed(s):
    if s > 100:
        return 100
    elif s < -100:
        return -100
    else:
        return s



class RobotMotors():

    def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B, verbose=0):

        # Set Pins
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B

        # Setup GPIO
        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100)
        self.pwmB = GPIO.PWM(self.EnaB, 100)

        # Other
        self.pwmA.start(0)
        self.pwmB.start(0)
        self.verbose = verbose



    def move(self, speed=0.5, turn=0.):
        if self.verbose>0:
            print("[INFO] move - speed={:d}% & turn={:d}%".format(
                speed*100, turn*100
            ))

        # Input values are normalized
        speed *=100
        turn *=100
        # Compute motors speeds
        leftSpeed = bornSpeed(speed - turn)
        rightSpeed = bornSpeed(speed + turn)

        # Apply speeds
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))

        if leftSpeed>0:
            GPIO.output(self.In1A, GPIO.HIGH)
            GPIO.output(self.In2A, GPIO.LOW)
        else:
            GPIO.output(self.In1A, GPIO.LOW)
            GPIO.output(self.In2A, GPIO.HIGH)

        if rightSpeed>0:
            GPIO.output(self.In1B, GPIO.HIGH)
            GPIO.output(self.In2B, GPIO.LOW)
        else:
            GPIO.output(self.In1B, GPIO.LOW)
            GPIO.output(self.In2B, GPIO.HIGH)



    def stop(self):
        if self.verbose>0:
            print("[INFO] stop")
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)



def test2():
    print("#"*80, "{:^80}".format('Test #2'), "#"*80, sep="\n")
    motor = RobotMotors(21, 20, 16, 18, 23, 24)
    motor.move(speed=0.6, turn=0)
    sleep(1)
    motor.stop()
    sleep(2)
    motor.move(speed=-0.5, turn=0.2)
    sleep(1)
    motor.stop()
    sleep(2)
    print("#"*80, sep="\n\n")



def keybordCMD(factor=0.1):
    speed = 0.
    turn = 0.

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN: #pygame.KEYUP:

            # # Going left
            # if (event.key == pygame.K_LEFT) or (event.key == pygame.K_q):
            #     turn -= 0.1

            # # Going right
            # if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
            #     turn += 0.1

            # # Going forward
            # if (event.key == pygame.K_UP) or (event.key == pygame.K_z):
            #     speed += 0.1

            # # Going backward
            # if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
            #     speed -= 0.1

            # To quit
            if ((event.mod & pygame.KMOD_CTRL) and (event.key == pygame.K_c)):
                raise KeyboardInterrupt

        elif event.type == pygame.QUIT: # If user clicked close
            raise KeyboardInterrupt

    pressed_events = pygame.key.get_pressed()

    # Going left
    if pressed_events[pygame.K_LEFT] or pressed_events[pygame.K_q]:
        turn += factor

    # Going right
    if pressed_events[pygame.K_RIGHT] or pressed_events[pygame.K_d]:
        turn -= factor

    # Going forward
    if pressed_events[pygame.K_UP] or pressed_events[pygame.K_z]:
        speed += factor

    # Going backward
    if pressed_events[pygame.K_DOWN] or pressed_events[pygame.K_s]:
        speed -= factor

    return {"speed": speed, "turn": turn}



def sign(x):
    if x<0:
        return -1.
    else:
        return 1.



class CarPosition:

    def __init__(self, size=[400, 300], verbose=0):
        # Initialize pygame
        pygame.init()

        # Set the height and width of the screen
        self.screen = pygame.display.set_mode(size)

        # Define the colors we will use in RGB format
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.RED   = (255,   0,   0)

        # Clear the screen and set the screen background
        self.screen.fill(self.BLACK)

        # Initialize car coordinates
        self.car_width, self.car_height = size[1]//50, size[1]//40
        self.position = pygame.math.Vector2(
            size[0]//2-self.car_width//2, size[1]-self.car_height-5
        )
        self.velocity = pygame.math.Vector2(0, 0)

        # Create the list of car's path
        self.path = []
        self.verbose = verbose

        # Initialize the first screen
        self.draw()



    def draw(self):
        # Clear the screen and set the screen background
        self.screen.fill(self.BLACK)

        # Draw the car
        pygame.draw.rect(
            self.screen, self.WHITE,
            [
                round(self.position[0]), round(self.position[1]),
                self.car_width,    self.car_height
            ]
        )

        if len(self.path)>1:
            # Draw the path
            pygame.draw.lines(self.screen, self.RED, False, self.path, 2)

        pygame.display.flip()



    def update(self, dt=0., speed=0., turn=0.):
        if abs(speed)>0.:
            pass
        else:
            # No speed
            return 0.

        # Compute motors speeds
        speed *= 100
        turn *= 50
        leftSpeed = bornSpeed(speed - turn)
        rightSpeed = bornSpeed(speed + turn)
        vel = min(abs(leftSpeed), abs(rightSpeed))
        r = vel*dt*sign(speed)
        theta = turn*0.9*sign(speed)-90 # Portion of a 90° angle
        if self.verbose>1:
            print("[INFO]", "r={}".format(r), "theta={}".format(theta))

        # Compute cartesian velocity from polar one
        self.velocity.from_polar((r, theta))
        self.position += self.velocity
        self.path.append(list(self.position))

        # Draw
        self.draw()



def test3():
    print("#"*80, "{:^80}".format('Test #3'), "#"*80, sep="\n")

    # Initialize display
    car = CarPosition()

    # Frames per seconds
    fps = 30

    try:
        while True:
            cmd = keybordCMD(factor=1.)
            print("[INFO]", cmd, car.position)
            car.update(dt=1./fps, **cmd)
            sleep(1./fps)
    except KeyboardInterrupt:
        pass
    print("#"*80, sep="\n\n")



if __name__ == "__main__":
    # Run tests
    test1()
    test2()
    test3()

