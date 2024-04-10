#!/bin/python3


import RPi.GPIO as GPIO

class OutputGpio:
    def __init__(self, channel):
        self.channel = channel
        self.gpioStatus = 1

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(self.channel, 1)

    def setGpio(self, out):
        GPIO.output(self.channel, out)

    def deSetup(self):
        GPIO.setup(self.channel, GPIO.IN)
