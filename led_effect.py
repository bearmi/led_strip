#!/bin/python3
import led_obj
from rpi_ws281x import ws, Color, Adafruit_NeoPixel

class BaseEffect:
    def __init__(self, speed = 5, repeat = 1):
        self.speed = speed
        self.repeat = repeat
        self.times = 0
        self.nextCnt = 0
        self.cntr = 0
        self.accRate = 4/5
        self.stepsPerOnce = 0
        self.name = None
        self.firstPos = 0
        self.ledNum = 0
        self.revert = False
        self.conditions = []
        self.isSatConditions = False
        self.strip_events = []
        self.acc = False
        self.ledObjName = ""

    def setAccRate(self, rate):
        self.accRate = rate
        return self

    def checkConditions(self):
        if len(self.conditions) == 0:
            return True
        for k, v in self.conditions.items():
            tmp = self.strip_events.get(k)
            if tmp != None:
                for k1, v1 in v.items():
                    tmp1 = tmp.get(k1)
                    if tmp1 != None and tmp1 & v1:
                        self.isSatConditions = True
                        return True
        return False
                            

    def setConditions(self, conditions):
        self.conditions = conditions
        return self

    def checkSpeed(self, counter):
        if not self.isSatConditions and not self.checkConditions():
            return False
        else:
            self.isSatConditions = True
        self.cntr = counter
        if not self.acc:
            if counter % self.speed == 0:
                return True
        else:
            if self.nextCnt <= counter:
                self.nextCnt = counter + self.stepsPerOnce
                self.stepsPerOnce = int(self.stepsPerOnce * self.accRate)
                if self.stepsPerOnce < 1:
                    self.stepsPerOnce = 1

                return True
        return False

    def resetOnce(self):
        print("-------=======", self.ledObjName, " ", self.name, "=======------")
        if self.acc == True:
            self.stepsPerOnce = self.speed
            self.nextCnt = self.cntr + self.speed

    def show(self, counter):
        if self.checkSpeed(counter):
            return False   # move to the next, since it's a base effect
        return False

    def isInLedRange(self, pos):
        num = self.ledNum
        if pos < 0:
            return False
        if pos > num -1:
            return False
        return True

    def fillColor(self, color, pos, count = 1):
        i = 0
        while True:
            if self.isInLedRange(pos):
                self.strip.setPixelColor(self.firstPos + pos + i, color)
            i += 1
            if i>= count:
                break

    def reset(self, cntr = 0):
        self.isSatConditions = False

    def setSpeed(self, speed, acc = False):
        self.speed = speed
        self.acc = acc
        return self

    def getSpeed(self):
        return self.speed

    def setRepeat(self, repeat):
        self.repeat = repeat
        return self

    def getRepeat(self):
        return self.repeat

    def setAccelerate(self, acc):
        self.acc = acc
        return self

    def getAccelerate(self):
        return self.acc

    def clear(self):
        self.fillColor(Color(0, 0, 0), 0, self.ledNum)

    def getSteps(self):
        return self.ledNum

    def getName(self):
        return self.name

    def setInitCntr(self, cntr):
        self.cntr = cntr

    def setFirstPos(self, pos):
        self.firstPos = pos
        return self

    def setLedNum(self, num):
        self.ledNum = num
        return self

    def setStrip(self, strip):
        self.strip = strip
        return self

    def setLedObjName(self, name):
        self.ledObjName = name
        return self

    def setRevert(self, revert):
        self.revert = revert
        return self

    def setStripEvents(self, strip_events):
        self.strip_events = strip_events
        return self

    def debug(self, head, strings):
        strings.insert(0, self.name)
        strings.insert(0, head)
        print(strings)

class FadeOut(BaseEffect):
    def __init__(self, colorG, colorR, colorB):
        self.colorG = colorG
        self.colorR = colorR
        self.colorB = colorB
        self.decG = colorG >> 5  # 16 steps to fade out
        self.decR = colorR >> 5
        self.decB = colorB >> 5
        BaseEffect.__init__(self)
        self.name = __class__.__name__

    def setColor(self, color):
        self.colorG = color >> 16
        self.colorR = (color & 0xff00) >> 8
        self.colorB = (color & 0xff)
        self.decG = self.colorG >> 5  # 16 steps to fade out
        self.decR = self.colorR >> 5
        self.decB = self.colorB >> 5
        return self

    def getSteps(self):
        return 32

    def reset(self):
        self.times = 0
        self.resetOnce()
        BaseEffect.reset(self)
        
    def resetOnce(self):
        self.g = self.colorG
        self.r = self.colorR
        self.b = self.colorB
        BaseEffect.resetOnce(self)
    
    def decColor(self, color, dec):
        color -= dec
        if color < 0:
            return 0
        return color

    def showOnce(self):
        self.fillColor(Color(self.g, self.r, self.b), 0, self.ledNum)
        self.g = self.decColor(self.g, self.decG)
        self.r = self.decColor(self.r, self.decR)
        self.b = self.decColor(self.b, self.decB)

    def isFinishedOnce(self):
        if self.g <= 0 and self.r <= 0 and self.b <= 0:
            return True
        return False
                
    def show(self, counter):
        if not self.checkSpeed(counter):
            return True
        self.showOnce()
        if self.isFinishedOnce():
            self.showOnce()
            self.times += 1
            if self.times == self.repeat:
                return False
            self.resetOnce()
   
        return True


class FadeIn(BaseEffect):
    def __init__(self, colorG, colorR, colorB):
        self.colorG = colorG
        self.colorR = colorR
        self.colorB = colorB
        self.incG = colorG >> 5  # 16 steps to fade out
        self.incR = colorR >> 5
        self.incB = colorB >> 5
        BaseEffect.__init__(self)
        self.name = __class__.__name__

    def setColor(self, color):
        self.colorG = color >> 16
        self.colorR = (color & 0xff00) >> 8
        self.colorB = (color & 0xff)
        self.incG = self.colorG >> 5  # 16 steps to fade out
        self.incR = self.colorR >> 5
        self.incB = self.colorB >> 5
        return self

    def reset(self):
        self.times = 0
        self.resetOnce()
        BaseEffect.reset(self)
        
    def resetOnce(self):
        self.g = 0
        self.r = 0
        self.b = 0
        BaseEffect.resetOnce(self)
    
    def incColor(self, color, inc, targetColor):
        color += inc
        if color > targetColor:
            return targetColor
        return color

    def showOnce(self):
        self.fillColor(Color(self.g, self.r, self.b), 0, self.ledNum)
        self.g = self.incColor(self.g, self.incG, self.colorG)
        self.r = self.incColor(self.r, self.incR, self.colorR)
        self.b = self.incColor(self.b, self.incB, self.colorB)

    def isFinishedOnce(self):
        if self.g >= self.colorG and self.r >= self.colorR and self.b >= self.colorB:
            return True
        return False
                
    def show(self, counter):
        if not self.checkSpeed(counter):
            return True
        if not self.isFinishedOnce():
            self.showOnce()
        else:
            self.times += 1
            if self.times == self.repeat:
                return False
            self.resetOnce()                                                                                                                                                                          

        return True

class Convert(BaseEffect):
    def __init__(self, colorFrom, colorTo):
        self.colorFrom = colorFrom
        self.colorTo = colorTo
        BaseEffect.__init__(self)
        self.name = __class__.__name__

    def reset(self):
        self.times = 0
        self.resetOnce()
        BaseEffect.reset(self)
        
    def resetOnce(self):
        self.stepCount = 9  # 9 steps to convert to new color
        BaseEffect.resetOnce(self)
    
    def computeColor(self, colorIndex):
        if self.stepCount == 1:
            return self.colorTo[colorIndex]

        if self.stepCount == 9:
            return self.colorFrom[colorIndex]        
        f = self.colorFrom[colorIndex]
        t = self.colorTo[colorIndex]
        f = f - f * (9 - self.stepCount) /9
        f = int(f)
        t = t * (9 - self.stepCount)/9
        t = int(t)
        t = f + t
        return t

    def showOnce(self):
        self.fillColor(Color(self.computeColor(0), self.computeColor(1), self.computeColor(2)), 0, self.ledNum)

    def isFinishedOnce(self):
        return self.stepCount == 0
                
    def show(self, counter):
        if not self.checkSpeed(counter):
            return True
        if not self.isFinishedOnce():
            self.showOnce()
            self.stepCount -= 1
        else:
            self.times += 1
            if self.times == self.repeat:                                                                                                                                                             
                return False
            self.resetOnce()

        return True

class WalkOut(BaseEffect):
    def __init__(self, colors, revert = False):
        BaseEffect.__init__(self)
        self.revert = revert
        self.colors = colors
        self.name = __class__.__name__
        self.bg = Color(0,0,0)

    def reset(self):
        self.times = 0
        self.resetOnce()
        BaseEffect.reset(self)

    def setBg(self, bg):
        self.bg = bg
        return self

    def resetOnce(self):
        if self.revert:
            self.curPos = self.ledNum - 1
        else:
            self.curPos = 0
        BaseEffect.resetOnce(self)

    def showOnce(self):
        if self.revert:
            i = self.curPos
            for c in self.colors:
                self.fillColor(c, i)
                i += 1

            self.curPos -= 1
        else:
            i = self.curPos
            for c in self.colors:
                self.fillColor(c, i)
                i -= 1

            self.curPos += 1

    def isFinishedOnce(self):
        if self.revert:
            return not self.isInLedRange(self.curPos) and not self.isInLedRange(self.curPos + len(self.colors) -1)
        else:
            return not self.isInLedRange(self.curPos) and not self.isInLedRange(self.curPos - len(self.colors) +1)
                
    def show(self, counter):
        if not self.checkSpeed(counter):
            return True
        self.fillColor(self.bg, 0, self.ledNum)
        if not self.isFinishedOnce():     
            self.showOnce()
        else:
            self.times += 1
            if self.times == self.repeat:
                return False
            self.resetOnce()
        
        return True


class Wave(BaseEffect):
    def __init__(self, revert = False):
        BaseEffect.__init__(self)
        self.revert = revert
        self.colors = []
        self.name = __class__.__name__

    def appendBuffer(self, preColor, color):
        steps = 3
        tmp = [0,0,0]
        for i in range(1,steps):
            for j in range (0,3):
                f = preColor[j]
                t = color[j]
                f = f * (steps - i) /steps
                f = int(f)
                t = t - t * (steps - i)/steps
                t = int(t)
                t = f + t
                tmp[j] = t
            self.colors.append(tmp.copy())
        return t 

    def appendColor(self, color, lenth):
        if len(self.colors) != 0:
            preColor = self.colors[len(self.colors)-1]
            self.appendBuffer(preColor, color)
        else:
            self.appendBuffer((0,0,0), color)
        for i in range(0, lenth):
            self.colors.append(color)
        print(str(self.colors))
        return self

    def reset(self):
        self.times = 0
        self.resetOnce()
        BaseEffect.reset(self)

    def resetOnce(self):
        if self.revert:
            self.curPos = self.ledNum - 1
        else:
            self.curPos = 0
        BaseEffect.resetOnce(self)

    def showOnce(self):
        if self.revert:
            p = self.curPos
            total = len(self.colors)
            j = 0
            for i in range(0, self.ledNum):
                c = self.colors[j%total]
                self.fillColor(Color(c[0],c[1], c[2]), p%self.ledNum)
                p -= 1
                j += 1
            self.curPos -= 1
        else:
            p = self.curPos
            total = len(self.colors)
            j = 0
            for i in range(0, self.ledNum):
                c = self.colors[j%total]
                self.fillColor(Color(c[0],c[1], c[2]), p%self.ledNum)
                p += 1
                j += 1
            self.curPos += 1

    def isFinishedOnce(self):
        return not self.isInLedRange(self.curPos)
                
    def show(self, counter):
        if not self.checkSpeed(counter):
            return True
        if not self.isFinishedOnce():     
            self.showOnce()
        else:
            self.times += 1
            if self.times == self.repeat:
                return False
            self.resetOnce()
        
        return True

class TearDown(BaseEffect):
    def __init__(self, color, revert = False):
        BaseEffect.__init__(self)
        self.revert = revert                                                                                                                                                                          
        self.color = color
        self.name = __class__.__name__

    def reset(self):
        self.times = 0
        self.resetOnce()
        BaseEffect.reset(self)

    def resetOnce(self):
        self.fillColor(self.color, 0, self.ledNum)
        if self.revert:
            self.curPos = self.ledNum - 1
        else:
            self.curPos = 0
        BaseEffect.resetOnce(self)

    def showOnce(self):
        self.fillColor(Color(0,0,0), self.curPos)
        if self.revert:
            self.curPos -= 1
        else:
            self.curPos += 1

    def isFinishedOnce(self):
        if self.revert:
            return not self.isInLedRange(self.curPos)
        else:
            return not self.isInLedRange(self.curPos)
                
    def show(self, counter):
        if not self.checkSpeed(counter):
            return True
        if not self.isFinishedOnce():     
            self.showOnce()
        else:                                                                                                                                                                                         
            self.times += 1
            if self.times == self.repeat:
                return False
            self.resetOnce()

        return True
        
class BuildUp(BaseEffect):
    def __init__(self, color, revert = False):
        BaseEffect.__init__(self)
        self.revert = revert
        self.color = color
        self.name = __class__.__name__

    def reset(self):
        self.times = 0
        self.resetOnce()
        BaseEffect.reset(self)

    def resetOnce(self):
        self.clear()
        if self.revert:
            self.curPos = self.ledNum - 1
        else:
            self.curPos = 0
        BaseEffect.resetOnce(self)

    def showOnce(self):
        self.fillColor(self.color, self.curPos)
        if self.revert:
            self.curPos -= 1
        else:
            self.curPos += 1

    def isFinishedOnce(self):
        if self.revert:
            return not self.isInLedRange(self.curPos)
        else:
            return not self.isInLedRange(self.curPos)
                
    def show(self, counter):
        if not self.checkSpeed(counter):
            return True
        if not self.isFinishedOnce():     
            self.showOnce()
        else:                                                                                                                                                                                         
            self.times += 1
            if self.times == self.repeat:
                return False
            self.resetOnce()

        return True

class BlackOut(BaseEffect):
    def __init__(self):
        BaseEffect.__init__(self)
        self.name = __class__.__name__

    def reset(self):
        self.done = False
        self.times = self.repeat
        BaseEffect.reset(self)

    def show(self, counter):
        if not self.checkSpeed(counter):
            return True
        if not self.done:
            self.clear()
            self.times -= 1
            if self.times ==0:
                self.done = True
                return True
        else:
            return False

