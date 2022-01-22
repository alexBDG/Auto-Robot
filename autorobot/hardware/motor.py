# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 10:45:00 2021

@author: Alexandre
"""

from time import sleep
IS_GPIO_AVAILABLE = True
try:
    import RPi.GPIO as GPIO
    # Set Pins number config
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
except ImportError:
    print("Not in Raspberry Pi environment!")
    IS_GPIO_AVAILABLE = False
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
            print("[INFO] move - speed={:.0f}% & turn={:.0f}%".format(
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



if __name__ == "__main__":
    # Run tests
    if IS_GPIO_AVAILABLE:
        test1()
        test2()
