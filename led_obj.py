#!/bin/python3


from rpi_ws281x import ws, Color, Adafruit_NeoPixel
import led_effect

class BaseLedObj:
    EventNone = 0
    EventEffectComplete = 1
    EventLoopComplete = 2

    def __init__(self, num, direction = True):
        self.ledNum = num
        self.direction = direction
        self.firstPos = 0
        self.effects = []
        self.currentEffect = 0
        self.strip = None
        self.name = None
        self.ActiveEffects = 0
        self.loop = True

    def getLedNum(self):
        return self.ledNum

    def setStrip(self, strip):
        self.strip = strip

    def getStrip(self):
        return self.strip

    def getDir(self):
        return self.direction

    def setFirstPos(self, pos):
        self.firstPos = pos

    def clearEffects(self):
        self.effects = []
        self.currentEffect = 0

    def getFirstPos(self):
        return self.firstPos

    def show(self, counter, strip_events):
        if self.ActiveEffects > len(self.effects) -1:
            #print("No effect found for " + self.name)
            return

        effects = self.effects[self.ActiveEffects]
        if len(effects) == 0:
            return None
        if self.currentEffect >= len(effects):
            return None

        effect = effects[self.currentEffect]

        event = BaseLedObj.EventNone
        if effect.setStripEvents(strip_events).show(counter) == False:
        # no next, move to the next effect
            event |= BaseLedObj.EventEffectComplete
            if self.currentEffect +1 == len(effects):
                event |= BaseLedObj.EventLoopComplete
                if self.loop == False:
                    self.currentEffect += 1
                    return { effect.getName() :event}
                else:
                    self.currentEffect = 0
            else:
                self.currentEffect += 1

            effect = effects[self.currentEffect]
            effect.setInitCntr(counter)
            effect.reset()
            effect.setStripEvents(strip_events)
            effect.show(counter)

        if event != BaseLedObj.EventNone:
            return { effect.getName() :event}
        else:
            return None

    def appendEffect(self, effect, index = 0):
        if index == len(self.effects):
            self.effects.append([])

        if index < len(self.effects):
            effects = self.effects[index]
        else:
            print("ERR: index out of range")

        effects = self.effects[index]
        effects.append(effect)
        effect.setFirstPos(self.getFirstPos())
        effect.setLedNum(self.ledNum)
        effect.setLedObjName(self.name)
        effect.setStrip(self.strip)
        effect.reset()
        
    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setLoop(self, loop):
        self.loop = loop
        return self

    def setActiveEffects(self, index):
        if index < len(self.effects):
            self.ActiveEffects = index
            self.currentEffect = 0
            for effect in self.effects[self.ActiveEffects]:
                effect.reset()
        else:
            print("ERR: index out of range", index)
        return self

class Abdomen(BaseLedObj):
    def __init__(self, num):
        BaseLedObj.__init__(self, num)

class Breast(BaseLedObj):
    def __init__(self, num):
        BaseLedObj.__init__(self, num)

class Arm(BaseLedObj):
    def __init__(self, num):
        BaseLedObj.__init__(self, num)

class Head(BaseLedObj):
    def __init__(self, num):
        BaseLedObj.__init__(self, num)

class Ear(BaseLedObj):
    def __init__(self, num):
        BaseLedObj.__init__(self, num)

class Hair(BaseLedObj):
    def __init__(self, num):
        BaseLedObj.__init__(self, num)

class LedStrip:
    def __init__(self):
        self.links = {}
        self.strip = None
        self.counter = 0

        self.ledOn = True
        self.events = {}

    def add(self, name, obj):
        self.links[name] = obj
        obj.setName(name)

    def getTotalLedNum(self):
        n = 0
        for k,v in self.links.items():
            print("bear3", k, v.getFirstPos(), str(v.getLedNum()))
            n += v.getLedNum()

        print("Total led num " + str(n))
        return n

    def setStrip(self, strip):
        self.strip = strip

    def getStrip(self):
        return self.strip

    def getLedObjByName(self, name):
        for k,v in self.links.items():
            print("bear3a "+ k + " " + name)
            if k == name:
                return v
        print("No obj with name "+ name)
        return None

    def show(self):
        events_tmp = {}
        for k,v in self.links.items():
            event = v.show(self.counter, self.events)
            if event != None:
                events_tmp[k] = event
        self.strip.show()
        self.counter += 1
        self.events = events_tmp
        return self.events

    def appendEvents(self, idx1, idx2, value):
        t = {idx2: value}
        self.events[idx1] = t

    def printLinks(self):
        for k,v in self.links.items():
            print(k, v.getFirstPos(), str(v.getLedNum()))

    def blackout(self):
        strip = self.strip
        for i in range(max(strip.numPixels(), strip.numPixels())):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()

    def initStrip(self):
        num = 0
        for k,obj in self.links.items():
            obj.setFirstPos(num)
            obj.setStrip(self.strip)
            num += obj.getLedNum()

        self.strip.begin()
        self.blackout()

    def clearAllEffect(self):
        self.blackout()
        for k,obj in self.links.items():
            obj.clearEffects()
