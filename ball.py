#!/bin/python3

import time

from rpi_ws281x import ws, Color, Adafruit_NeoPixel
from led_obj import Abdomen, LedStrip, Breast, Head, Ear, Hair, Arm, BaseLedObj
from led_effect import WalkOut, FadeOut, FadeIn, BuildUp, TearDown, Convert, Wave, BlackOut
from inputGpio import InputGpio




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

DOT_COLORS = [0x002000,   # red
              0x102000,   # orange
              0x202000,   # yellow
              0x200000,   # green
              0x200020,   # lightblue
              0x000020,   # blue
              0x001010,   # purple
              0x002010]   # pink

BALL_COLORS = [0xff0000,   # red
              0x00ff00,   # orange
              0x0000ff,   # yellow
              0xffff00]
#actual cplor patten is GRB

def appendPrepareEffect(strip):
    abd3 = strip.getLedObjByName("ball1")
    e = FadeIn(0, 255, 0)
    e.setColor(BALL_COLORS[0]).setSpeed(6, True)
    abd3.appendEffect(e)
            
    e = FadeOut(0, 255, 0)
    e.setColor(BALL_COLORS[0]).setSpeed(6, True)
    abd3.appendEffect(e)

    e = BlackOut()                                                                                                                                                                                    
    e.setSpeed(30).setRepeat(10)
    abd3.appendEffect(e)


    abd3 = strip.getLedObjByName("ball2")
    e = FadeIn( 255, 0, 0)
    e.setColor(BALL_COLORS[1]).setSpeed(6, True)
    abd3.appendEffect(e)

    e = FadeOut( 255, 0, 0)
    e.setColor(BALL_COLORS[1]).setSpeed(6, True)
    abd3.appendEffect(e)

    e = BlackOut()                                                                                                                                                                                    
    e.setSpeed(30).setRepeat(10)
    abd3.appendEffect(e)


    abd3 = strip.getLedObjByName("ball3")
    e = FadeIn(0, 0, 255)
    e.setColor(BALL_COLORS[2]).setSpeed(6, True)
    abd3.appendEffect(e)

    e = FadeOut(0, 0, 255)
    e.setColor(BALL_COLORS[2]).setSpeed(6, True)
    abd3.appendEffect(e)

    e = BlackOut()                                                                                                                                                                                    
    e.setSpeed(30).setRepeat(10)
    abd3.appendEffect(e)


    abd3 = strip.getLedObjByName("ball4")
    e = FadeIn( 255, 255, 0)
    e.setColor(BALL_COLORS[3]).setSpeed(6, True)
    abd3.appendEffect(e)

    e = FadeOut( 255, 255, 0)
    e.setColor(BALL_COLORS[3]).setSpeed(6, True)
    abd3.appendEffect(e)

    e = BlackOut()                                                                                                                                                                                    
    e.setSpeed(30).setRepeat(10)
    abd3.appendEffect(e)

def appendBlinkEffect(strip):
    abd3 = strip.getLedObjByName("ball1")
    e = FadeIn(0, 255, 0)
    e.setColor(BALL_COLORS[0]).setSpeed(6, True)
    abd3.appendEffect(e)

    e = FadeOut(0, 255, 0)
    e.setColor(BALL_COLORS[0]).setSpeed(6, True)
    abd3.appendEffect(e)
                                                                                                                                                                                                      
    abd3 = strip.getLedObjByName("ball2")
    e = FadeIn( 255, 0, 0)
    e.setColor(BALL_COLORS[1]).setSpeed(6, True)
    abd3.appendEffect(e)

    e = FadeOut( 255, 0, 0)
    e.setColor(BALL_COLORS[1]).setSpeed(6, True)
    abd3.appendEffect(e)

    abd3 = strip.getLedObjByName("ball3")
    e = FadeIn(0, 0, 255)
    e.setColor(BALL_COLORS[2]).setSpeed(6, True)
    abd3.appendEffect(e)

    e = FadeOut(0, 0, 255)
    e.setColor(BALL_COLORS[2]).setSpeed(6, True)
    abd3.appendEffect(e)
    
    abd3 = strip.getLedObjByName("ball4")
    e = FadeIn( 255, 255, 0)
    e.setColor(BALL_COLORS[3]).setSpeed(6, True)
    abd3.appendEffect(e)

    e = FadeOut( 255, 255, 0)
    e.setColor(BALL_COLORS[3]).setSpeed(6, True)
    abd3.appendEffect(e)

def appendLight(i):
    global strip_ball

    abd3 = strip_ball.getLedObjByName("ball"+ str(i+1))
    e = FadeIn( 255, 255, 0)
    e.setColor(BALL_COLORS[i]).setSpeed(20, True)
    abd3.appendEffect(e)

    e = FadeOut( 255, 255, 0)
    e.setColor(BALL_COLORS[i]).setSpeed(20, True)
    abd3.appendEffect(e)

def process1Click():
    global strip_ball, rmtCtrl
    global cntr

    while True:
        time.sleep(5/1000)
        rmtEvent = rmtCtrl.gpioPoll()
        if rmtEvent != InputGpio.EventNone:
            print("remote event ====== ", str(rmtEvent))

        if rmtEvent & InputGpio.EventPullDown:
            break

        strip_ball.show()     
        cntr += 1

def process4Lights():
    global strip_ball
    global rmtCtrl, cntr

    strip_ball.clearAllEffect()
    for i in range(0, 4):
        cntr += 1
        process1Click()
        appendLight(i)

        time.sleep(5/1000)

    # all lights on, blink and wait
    strip_ball.clearAllEffect()
    appendBlinkEffect(strip_ball)    

    process1Click()

def main():
    # Create NeoPixel objects with appropriate configuration for each strip.
    global strip_ball

    strip_ball.add("ball1", BaseLedObj(8))
    strip_ball.add("ball2", BaseLedObj(8))
    strip_ball.add("ball3", BaseLedObj(8))
    strip_ball.add("ball4", BaseLedObj(8))

    strip_ball.setStrip(Adafruit_NeoPixel(strip_ball.getTotalLedNum(), LED_2_PIN, LED_2_FREQ_HZ,
                               LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS,
                               LED_2_CHANNEL, LED_2_STRIP))

    print('Press Ctrl-C to quit.')

    strip_ball.initStrip()



    rmtCtrl = InputGpio(16)

    appendPrepareEffect(strip_ball)
    process1Click()
    
    process4Lights()

    process4Lights()

# Main program logic follows:
if __name__ == '__main__':
    cntr = 0
    rmtCtrl = InputGpio(14)
    strip_ball = LedStrip()

    while True:
        main()
