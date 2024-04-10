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
#actual cplor patten is GRB
def appendHeadEffect(strip):
    handler = strip.getLedObjByName("head1")
    e = FadeIn(128, 255, 0)
    e.setSpeed(5, True)
    handler.appendEffect(e)

    e = FadeOut(128, 255, 0)
    e.setSpeed(2, True)
    handler.appendEffect(e)

def appendEffects(strip):
    # handler
    handler = strip.getLedObjByName("handler")

    e = WalkOut([Color(255,255,255), Color(255,255,255), DOT_COLORS[1], DOT_COLORS[1], DOT_COLORS[7], DOT_COLORS[7]], True)
    e.setSpeed(10, True).setRevert(False)
    e.setAccRate(0.96)
    handler.appendEffect(e)

    e = BlackOut()
    e.setSpeed(30).setRepeat(4)
    handler.appendEffect(e)

    e = WalkOut([Color(255,255,255), Color(255,255,255), Color(0,255,0), Color(0,255,0) ], True)
    e.setSpeed(6, True).setRevert(False).setBg(0x200000)
    e.setAccRate(0.96)
    handler.appendEffect(e, 1)

    #  head
    handler = strip.getLedObjByName("head")

    e = Wave()
    e.setSpeed(2)
    e.appendColor((255,0,0), 30)
    e.appendColor((0,255,0), 30)
    e.appendColor((128,255,0), 30)
    e.appendColor((0, 255,255), 30)
    e.setRevert(False)
    handler.appendEffect(e)

    e = BlackOut()
    handler.appendEffect(e, 1)

    e = BuildUp(0x80ff00)
    e.setSpeed(9, True).setConditions({"handler":{"WalkOut":BaseLedObj.EventEffectComplete}})
    e.setAccRate(0.96)
    handler.appendEffect(e, 1)

    e = FadeOut(0x80, 255, 0)
    e.setSpeed(30, True)
    handler.appendEffect(e, 1)

    e = BlackOut()
    e.setRepeat(15)
    handler.appendEffect(e, 1)


def handleSig(signum, frame, ask=True):
    print("recerived sig--------------------")

def main():
    # Create NeoPixel objects with appropriate configuration for each strip.
    strip_body = LedStrip()
    strip_body.add("handler", BaseLedObj(50))
    strip_body.add("head", BaseLedObj(92))


    strip_body.setStrip(Adafruit_NeoPixel(strip_body.getTotalLedNum(), LED_2_PIN, LED_2_FREQ_HZ,
                               LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS,
                               LED_2_CHANNEL, LED_2_STRIP))


    print('Press Ctrl-C to quit.')

    strip_body.initStrip()

    appendEffects(strip_body)

    strip_body.printLinks()


    ctrlBtn = InputGpio(26)

    btn_show = False
    while True:
        btn_events = ctrlBtn.gpioPoll()
        if btn_events != InputGpio.EventNone:
            print("Btn event ====== ", str(btn_events))
        if btn_events & InputGpio.EventDoubleClickDown:
            handler = strip_body.getLedObjByName("handler")
            handler.setActiveEffects(1)
            handler.setLoop(False)

            handler = strip_body.getLedObjByName("head")
            handler.setActiveEffects(1)
            handler.setLoop(False)
            
            btn_show = True

        strip_events = strip_body.show()

        if len(strip_events) != 0:
            print ("strip event +++++", str(strip_events), str(btn_show))

        if btnShowOffCheck(btn_show, strip_events):
            handler = strip_body.getLedObjByName("handler")
            handler.setActiveEffects(0)
            handler.setLoop(True)

            handler = strip_body.getLedObjByName("head")
            handler.setActiveEffects(0)
            handler.setLoop(True)

            btn_show = False
            
            
        time.sleep(5/1000)


def btnShowOffCheck(btn_show, strip_events):
    if not btn_show:
        return False

    if len(strip_events) == 0:
        return False
    print ("btn show done2")
    if strip_events.get("head") == None:
        return False
    print ("btn show done3")
    if strip_events["head"].get("BlackOut") == None:
        return False
    print ("btn show done4")
    if strip_events["head"]["BlackOut"] & BaseLedObj.EventLoopComplete:
        print ("btn show done")
        return True

    return False

# Main program logic follows:
if __name__ == '__main__':
    main()
