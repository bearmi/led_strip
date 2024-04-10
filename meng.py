#!/bin/python3

import time

from rpi_ws281x import ws, Color, Adafruit_NeoPixel
from led_obj import Abdomen, LedStrip, Breast, Head, Ear, Hair, Arm, BaseLedObj
from led_effect import WalkOut, FadeOut, FadeIn, BuildUp, TearDown, Convert, BlackOut

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
    abd3 = strip.getLedObjByName("head3")
    e = FadeIn(0, 255, 0)
    e.setSpeed(3, True).setConditions({"brst":{"WalkOut":BaseLedObj.EventEffectComplete}})
    abd3.appendEffect(e)

    e = FadeOut(0, 255, 0)
    e.setSpeed(3, True)
    abd3.appendEffect(e)

    abd3 = strip.getLedObjByName("head2")
    e = FadeIn(255, 255, 255)
    e.setSpeed(3, True).setConditions({"head3":{"FadeOut":BaseLedObj.EventEffectComplete}})
    abd3.appendEffect(e)

    e = FadeOut(255, 255, 255)
    e.setSpeed(3, True)
    abd3.appendEffect(e)

    abd3 = strip.getLedObjByName("head1")
    e = FadeIn(255, 0, 0)
    e.setSpeed(3, True).setConditions({"head2":{"FadeOut":BaseLedObj.EventEffectComplete}})
    abd3.appendEffect(e)

    e = FadeOut(255, 0, 0)
    e.setSpeed(3, True)
    abd3.appendEffect(e)



    abd3 = strip.getLedObjByName("ear1")
    e = WalkOut([Color(255,255,255), DOT_COLORS[1], DOT_COLORS[7]])
    e.setSpeed(8, True).setRevert(True).setConditions({"brst":{"WalkOut":BaseLedObj.EventEffectComplete}})
    abd3.appendEffect(e)
    
    abd3 = strip.getLedObjByName("ear2")
    e = WalkOut([Color(255,255,255), DOT_COLORS[1], DOT_COLORS[7]])
    e.setSpeed(8, True).setConditions({"brst":{"WalkOut":BaseLedObj.EventEffectComplete}})
    abd3.appendEffect(e)
    
    abd3 = strip.getLedObjByName("ear3")
    e = WalkOut([Color(255,255,255), DOT_COLORS[1], DOT_COLORS[7]])
    e.setSpeed(8, True).setRevert(True).setConditions({"brst":{"WalkOut":BaseLedObj.EventEffectComplete}})
    abd3.appendEffect(e)


    abd3 = strip.getLedObjByName("hair")
    e = WalkOut([Color(255,255,255), DOT_COLORS[1], DOT_COLORS[7]])
    e.setSpeed(8, True).setConditions({"ear2":{"WalkOut":BaseLedObj.EventEffectComplete}})
    abd3.appendEffect(e)

def appendBodyEffect(strip):
    abd3 = strip.getLedObjByName("brst")
    e = WalkOut([Color(255,255,255), DOT_COLORS[1], DOT_COLORS[7]])
    e.setSpeed(5).setConditions({"abd3":{"FadeOut":BaseLedObj.EventEffectComplete}})
    abd3.appendEffect(e)

    abd3 = strip.getLedObjByName("arm")
    e = WalkOut([Color(255,255,255), DOT_COLORS[1], DOT_COLORS[7]])
    e.setSpeed(5).setConditions({"abd3":{"FadeOut":BaseLedObj.EventEffectComplete}})
    abd3.appendEffect(e)

    abd3 = strip.getLedObjByName("abd1")
    e = FadeIn(0, 255, 0)
    e.setSpeed(6, True)
    abd3.appendEffect(e)

    e = FadeOut(0, 255, 0)
    e.setSpeed(6, True)
    abd3.appendEffect(e)

    e = BlackOut()
    e.setSpeed(30).setRepeat(10)
    abd3.appendEffect(e)

    abd3 = strip.getLedObjByName("abd2")
    e = FadeIn(255, 255, 255)
    e.setSpeed(6, True).setConditions({"abd1":{"FadeOut":BaseLedObj.EventEffectComplete}})
    abd3.appendEffect(e)

    e = FadeOut(255, 255, 255)
    e.setSpeed(6, True)
    abd3.appendEffect(e)

    abd3 = strip.getLedObjByName("abd3")
    e = FadeIn(255, 0, 0)
    e.setSpeed(6, True).setConditions({"abd2":{"FadeOut":BaseLedObj.EventEffectComplete}})
    abd3.appendEffect(e)

    e = FadeOut(255, 0, 0)
    e.setSpeed(6, True)
    abd3.appendEffect(e)

def main():
    # Create NeoPixel objects with appropriate configuration for each strip.
    strip_body = LedStrip()
    strip_body.add("abd1", Abdomen(2))
    strip_body.add("abd2", Abdomen(3))
    strip_body.add("abd3", Abdomen(4))

    strip_body.add("brst", Breast(13))   # *3
    strip_body.add("arm", Arm(8))    # *3

    strip_head = LedStrip()
    strip_head.add("head1", Head(2))
    strip_head.add("head2", Head(3))
    strip_head.add("head3", Head(4))

    strip_head.add("ear1", Ear(3))   # *3
    strip_head.add("ear2", Ear(6))   # *3
    strip_head.add("ear3", Ear(5))   # *3

    strip_head.add("hair", Hair(20))   # *3

    strip_body.setStrip(Adafruit_NeoPixel(strip_body.getTotalLedNum(), LED_2_PIN, LED_2_FREQ_HZ,
                               LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS,
                               LED_2_CHANNEL, LED_2_STRIP))

    strip_head.setStrip(Adafruit_NeoPixel(strip_head.getTotalLedNum(), LED_1_PIN, LED_1_FREQ_HZ,
                               LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS,
                               LED_1_CHANNEL, LED_1_STRIP))

    print('Press Ctrl-C to quit.')

    strip_body.initStrip()
    strip_head.initStrip()

    appendBodyEffect(strip_body)
    appendHeadEffect(strip_head)

    strip_body.printLinks()
    strip_head.printLinks()
    while True:
        strip_events = strip_body.show()
        if len(strip_events) != 0:
            print ("strip event +++++", str(strip_events))
           
        if strip_events.get("brst") != None and strip_events["brst"].get("WalkOut") != None and strip_events["brst"]["WalkOut"] & BaseLedObj.EventEffectComplete:
            strip_head.appendEvents("brst", "WalkOut", BaseLedObj.EventEffectComplete)
        strip_head.show()
        time.sleep(5/1000)

# Main program logic follows:
if __name__ == '__main__':
    main()
