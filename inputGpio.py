#!/bin/python3


import RPi.GPIO as GPIO

class InputGpio:
    EventNone = 0
    EventPullDown = 1
    EventPullUp = 2
    EventDoubleClickDown = 4
    EventDoubleClickUp = 8
    EventLongPress = 16

    def __init__(self, channel):
        self.channel = channel
        self.gpioStatus = 1
        self.countLimit = 5
        self.gpioCounter = 0
        self.lastStatus = 1
        self.counter = 0
        self.longPressLimit = 140
                
        self.doubltClickLimit = 100
        self.doubleClickHighCounter = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def gpioChanged(self):
        if self.gpioStatus == 1:
            # button released, and if click again, would be regarded as double click
            self.doubleClickHighCounter = self.counter
            print ("bear11h", str(self.counter), str(self.longPressCntr))
            if self.counter - self.longPressCntr >= self.longPressLimit:
                return InputGpio.EventPullUp | InputGpio.EventLongPress
            return InputGpio.EventPullUp
        else:
            tmp = InputGpio.EventPullDown
            self.longPressCntr = self.counter
            print ("bear11f", str(self.counter), "-", str(self.doubleClickHighCounter))
            if self.counter - self.doubleClickHighCounter < self.doubltClickLimit:
                print ("bear11g double clicked")
                tmp |= InputGpio.EventDoubleClickDown
                print("bear11g1", str(tmp))
            return tmp


    def gpioPoll(self):
        self.counter += 1
        tmp = GPIO.input(self.channel)
        # print("bear11 ====== ", str(tmp))
        if tmp != self.gpioStatus:
            if tmp == self.lastStatus:
                self.gpioCounter += 1
                if self.gpioCounter == self.countLimit:  # filter out switch jump
                    print("bear11a became", str(tmp), str(self.gpioCounter))
                    self.gpioStatus = tmp
                    return self.gpioChanged()

            else:
                self.gpioCounter = 0
                self.lastStatus = tmp
        return InputGpio.EventNone
