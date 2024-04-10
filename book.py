#!/bin/python3

import time

from rpi_ws281x import ws, Color, Adafruit_NeoPixel
from led_obj import Abdomen, LedStrip, Breast, Head, Ear, Hair, Arm, BaseLedObj
from led_effect import WalkOut, FadeOut, FadeIn, BuildUp, TearDown, Convert, BlackOut
from inputGpio import InputGpio
from outputGpio import OutputGpio


# LED strip configuration:                                                                                                                                                                          
LED_1_PIN = 18          # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA = 10          # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 128  # Set to 0 for darkest and 255 for brightest
LED_1_INVERT = 0    # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL = 0       # 0 or 1
LED_1_STRIP = ws.WS2811_STRIP_RGB

LED_2_PIN = 19          # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA = 9          # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 128  # Set to 0 for darkest and 255 for brightest
LED_2_INVERT = 0    # True to invert the signal (when using NPN transistor level shift)
LED_2_CHANNEL = 1       # 0 or 1
LED_2_STRIP = ws.WS2811_STRIP_RGB

BOOK_MT_PIN = 23
BALL_MT_PIN = 24

DOT_COLORS = [0x002000,   # red
              0x102000,   # orange
              0x202000,   # yellow
              0x200000,   # green
              0x200020,   # lightblue
              0x000020,   # blue
              0x001010,   # purple
              0x002010]   # pink
#actual cplor patten is GRB
def appendHeadEffect(strip):
    abd3 = strip.getLedObjByName("head1")
    e = FadeIn(0, 255, 255)
    e.setSpeed(5, True)
    abd3.appendEffect(e)

    e = FadeOut(0, 255, 255)
    e.setSpeed(2, True)
    abd3.appendEffect(e)

def appendBookEffect1(strip):
    abd3 = strip.getLedObjByName("face")
    e = FadeIn(0, 0, 255)
    e.setSpeed(60, True)
    abd3.appendEffect(e)

    e = FadeOut(0, 0, 255)
    e.setSpeed(60, True)
    abd3.appendEffect(e)

    e = BlackOut()
    e.setSpeed(60).setRepeat(10)
    abd3.appendEffect(e)

def appendBookEffect1a(book):
    # face slow blink
    abd3 = book.getLedObjByName("face")
    e = FadeIn(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

    e = FadeOut(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

def appendBookEffect2(book):
    # face slow blink
    abd3 = book.getLedObjByName("face")
    e = FadeIn(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)
    
    e = FadeOut(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)
    
    abd3 = book.getLedObjByName("p1a")
    e = FadeIn(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)
    
    e = FadeOut(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)
    
    abd3 = book.getLedObjByName("p1b")
    e = FadeIn(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

    e = FadeOut(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

    abd3 = book.getLedObjByName("p1c")
    e = FadeIn(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

    e = FadeOut(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

    abd3 = book.getLedObjByName("p1d")
    e = FadeIn(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

    e = FadeOut(0, 255, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

def appendBookEffect4(book):

    abd3 = book.getLedObjByName("p2a")
    e = FadeIn(255, 0, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

    e = FadeOut(255, 0, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

    abd3 = book.getLedObjByName("p2b")
    e = FadeIn(255, 0, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

    e = FadeOut(255, 0, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

    abd3 = book.getLedObjByName("p2c")
    e = FadeIn(255, 0, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)

    e = FadeOut(255, 0, 0)
    e.setSpeed(5)
    abd3.appendEffect(e)    

def main():
    # Create NeoPixel objects with appropriate configuration for each strip.
    strip_book = LedStrip()
    strip_book.add("face", BaseLedObj(4))
    strip_book.add("p2a", BaseLedObj(5))
    strip_book.add("p2b", BaseLedObj(4))
    strip_book.add("p2c", BaseLedObj(4))   # *3

    strip_book.add("p1a", BaseLedObj(3))  # *3
    strip_book.add("p1b", BaseLedObj(3))  # *3
    strip_book.add("p1c", BaseLedObj(5))  # *3
    strip_book.add("p1d", BaseLedObj(5))    # *3

    strip_head = LedStrip()
    strip_head.add("head1", BaseLedObj(100))
    strip_head.add("ear1", BaseLedObj(10))   # *3   #  !!!! remove them may cause trouble

    strip_head.add("hair", BaseLedObj(20))   # *3  #  !!!! remove them may cause trouble

    strip_book.setStrip(Adafruit_NeoPixel(strip_book.getTotalLedNum(), LED_1_PIN, LED_1_FREQ_HZ,
                               LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS,
                               LED_1_CHANNEL, LED_1_STRIP))

    strip_head.setStrip(Adafruit_NeoPixel(strip_head.getTotalLedNum(), LED_2_PIN, LED_2_FREQ_HZ,
                               LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS,
                               LED_2_CHANNEL, LED_2_STRIP))

    print('Press Ctrl-C to quit.')

    strip_book.initStrip()
    strip_head.initStrip()

    appendBookEffect1(strip_book)
    appendHeadEffect(strip_head)

    bookMotor = OutputGpio(BOOK_MT_PIN)
    bookMotor.deSetup()

    ballMotor = OutputGpio(BALL_MT_PIN)
    ballMotor.deSetup()

    # 1. idle, face led slow blink
    # 1a. quick blink, and book down
    # 2. [remote click] face led on, and open the 1st page
    # 3. castle led on
    # 4. [remote click] open the 2nd page
    # 5. dragon led on, ball driver on


    strip_book.printLinks()
    strip_head.printLinks()
    rmtCtl = InputGpio(14)  # remote controller

    while True:    # S1
        time.sleep(5/1000)
        rmtEvent = rmtCtl.gpioPoll()
        if rmtEvent != InputGpio.EventNone:
            print("remote event ====== ", str(rmtEvent))

        if rmtEvent & InputGpio.EventLongPress:
            break

        strip_book.show()        

    strip_book.clearAllEffect()
    appendBookEffect1a(strip_book)
    while True:   # s1a
        time.sleep(5/1000)
        rmtEvent = rmtCtl.gpioPoll()
        if rmtEvent != InputGpio.EventNone:
            print("remote event ====== ", str(rmtEvent))

        if rmtEvent & InputGpio.EventLongPress:
            break

        strip_book.show()

    strip_book.clearAllEffect()
    appendBookEffect2(strip_book)
    print("~~~~~~~ Step 2 ~~~~")
    cnt = 1350
    print(">>>>>  open book  P1>>>>")
    bookMotor = OutputGpio(BOOK_MT_PIN)
    bookMotor.setGpio(0)
    while True:    # S2
        time.sleep(5/1000)
        if cnt <= 0:
            bookMotor.setGpio(1)  # stop book motor
            bookMotor.deSetup()
            print(">>>>>  open book P1 : stop>>>>")
            break
        else:
            cnt -= 1

        strip_book.show()


    #### s3: show page 1, till next click
    print("~~~~~~~ Step 3 ~~~~")
    while True:    # S3
        time.sleep(5/1000)
        rmtEvent = rmtCtl.gpioPoll()
        if rmtEvent != InputGpio.EventNone:
            print("remote event ====== ", str(rmtEvent))

        if rmtEvent & InputGpio.EventLongPress:
            break

        strip_book.show()        

    strip_book.clearAllEffect()
    appendBookEffect4(strip_book)
    print("~~~~~~~ Step 4 ~~~~")
    cnt = 1200
    bookMotor = OutputGpio(BOOK_MT_PIN)
    bookMotor.setGpio(0)
    print(">>>>>  open book p2>>>>")
    while True:
        time.sleep(5/1000)
        if cnt <= 0:
            bookMotor.setGpio(1)  # stop book motor
            bookMotor.deSetup()
            print(">>>>>  open book : stop>>>>")
            break
        else:
            print(">>> ", str(cnt))
            cnt -= 1

        strip_book.show()

    ### S5
    ballMotor = OutputGpio(BALL_MT_PIN)
    ballMotor.setGpio(0)
    print("~~~~~~~ Step 5 ~~~~")
    while True:    # S5
        time.sleep(5/1000)
        rmtEvent = rmtCtl.gpioPoll()
        if rmtEvent != InputGpio.EventNone:
            print("remote event ====== ", str(rmtEvent))

        if rmtEvent & InputGpio.EventLongPress:
            ballMotor.setGpio(1)  # stop ball motor
            ballMotor.deSetup()
            break

        strip_book.show()
        


# Main program logic follows:
if __name__ == '__main__':
    while True:
        main()
