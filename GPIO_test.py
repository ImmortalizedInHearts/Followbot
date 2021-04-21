#!/usr/bin/env python
# -*- coding: utf-8 -*-

import OPi.GPIO as GPIO
from time import sleep          # this lets us have a time delay

GPIO.setboard(GPIO.PCPCPLUS)    # Orange Pi PC board
GPIO.setmode(GPIO.BOARD)        # set up BOARD BCM numbering
GPIO.setup(7, GPIO.OUT)         # set BCM7 (pin 26) as an output (LED)
GPIO.setup(8, GPIO.OUT)         # set BCM7 (pin 26) as an output (LED)
GPIO.setup(9, GPIO.OUT)         # set BCM7 (pin 26) as an output (LED)
GPIO.setup(10, GPIO.OUT)         # set BCM7 (pin 26) as an output (LED)


try:
    print ("Press CTRL+C to exit")
    while True:
        GPIO.output(7, 1)       # set port/pin value to 1/HIGH/True
        GPIO.output(9, 1)       # set port/pin value to 1/HIGH/True
        sleep(0.1)
        GPIO.output(7, 0)       # set port/pin value to 0/LOW/False
        GPIO.output(9, 0)       # set port/pin value to 0/LOW/False
        sleep(2)

        GPIO.output(8, 1)       # set port/pin value to 1/HIGH/True
        GPIO.output(10, 1)       # set port/pin value to 1/HIGH/True
        sleep(0.1)
        GPIO.output(8, 0)       # set port/pin value to 0/LOW/False
        GPIO.output(10, 0)       # set port/pin value to 0/LOW/False
        sleep(0.1)

        sleep(0.5)

except KeyboardInterrupt:
    GPIO.output(7, 0)       # set port/pin value to 0/LOW/False
    GPIO.output(9, 0)       # set port/pin value to 0/LOW/False
    GPIO.output(8, 0)       # set port/pin value to 0/LOW/False
    GPIO.output(10, 0)       # set port/pin value to 0/LOW/False
    GPIO.cleanup()              # Clean GPIO
    print ("Bye.")