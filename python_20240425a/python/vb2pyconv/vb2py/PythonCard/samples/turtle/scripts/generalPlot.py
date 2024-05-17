# this is the beginnings of a generalized set of plotting
# methods for drawing graphs where x and y can be described
# by an equation such as x = t, y = cos(t)
# where t is the iteration value over some low to high range
# and a step value

# since Python can be handed a couple of strings that
# are then have eval() applied to them in the loop
# generalPlot allows any equation to be passed in as long
# as it can be defined in terms of t

# the tschirnhausen curve is shown as its own method and
# defined in terms of generalPlot for comparison

import math
from math import cos, pi, sin, sqrt, tan
from wrappers import Turtle

# wrapper for any additional drawing routines
# that need to know about each other
class PlotTurtle(Turtle):
    def doTick(self, n):
        self.right(90)
        self.forward(5)
        self.write("%d" % n)
        self.back(10)
        self.forward(5)
        self.left(90)

    def coordinateLines(self, x0, y0, xScale, yScale, xLow, xHigh):
        self.moveTo(0, y0)
        self.color('blue')
        self.lineTo(1000, y0)
        self.moveTo(x0, 0)
        self.lineTo(x0, 1000)
        self.moveTo(x0, y0)

        """        
        for i in range(10):
            self.moveTo(i * xLow * xScale + x0, y0)
            self.doTick(i * xLow)
            self.moveTo(i * xHigh * xScale + x0, y0)
            self.doTick(i * xHigh)
        self.lt(90)
        """
        self.color('black')

    def generalPlot(self, xOffset, yOffset, xScale, yScale,
                    xEquation, yEquation, low, high, stepSize):
        # the units of t are radians

        print "xEquation:", xEquation
        print "yEquation:", yEquation
        
        steps = int((high - low) / stepSize) + 2   # low to high inclusive

        # moveTo the first point to avoid an extra line
        t = low
        x = eval(xEquation)
        y = eval(yEquation)
        self.moveTo(x * xScale + xOffset, y * yScale + yOffset)
        for j in range(steps):
            t += stepSize
            x = eval(xEquation)
            y = eval(yEquation)
            # self.plot(x * xScale + xOffset, y * yScale + yOffset)
            self.lineTo(x * xScale + xOffset, y * yScale + yOffset)
            #self.write("%f, %f" % (x, y))
            #break

    def tschirnhausen2(self, xOffset, yOffset, xScale, yScale, a, low, high, stepSize):
        # the units of t are radians
        
        steps = int((high - low) / stepSize) + 2   # low to high inclusive

        # moveTo the first point to avoid an extra line
        t = low - stepSize
        x = 3 * a * (pow(t, 2) - 3)
        y = a * t * (pow(t, 2) - 3)
        self.moveTo(x * xScale + xOffset, y * yScale + yOffset)
        for j in range(steps):
            t += stepSize
            temp = a * (pow(t, 2) - 3)
            x = 3 * temp
            y = t * temp
            # self.plot(x * xScale + xOffset, y * yScale + yOffset)
            self.lineTo(x * xScale + xOffset, y * yScale + yOffset)

    """
    based on the Tschirnhausen algorithm
    presented in the May 1988 Scientific American
    Computer Recreations column by A. K. Dewdney
    algorithm starts on page 121
    """
    def tschirnhausen(self, xOffset, yOffset, xScale, yScale, low, high, stepSize):
        # the units of t are radians
        
        a = 1.0
        # a = 0.3
        steps = int(high - low) / stepSize

        aSteps = int((2 - 0.1) / 0.1)
        a = 0.1
        for i in range(aSteps):
            # moveTo the first point to avoid an extra line
            t = low
            x = 3 * a * (pow(t, 2) - 3)
            y = t * a * (pow(t, 2) - 3)
            self.moveTo(x * xScale + xOffset, y * yScale + yOffset)
            for j in range(steps):
                t += stepSize
                x = 3 * a * (pow(t, 2) - 3)
                y = a * t * (pow(t, 2) - 3)
                # self.plot(x * xScale + xOffset, y * yScale + yOffset)
                self.lineTo(x * xScale + xOffset, y * yScale + yOffset)
            a += .1

def draw(canvas):
    t1 = PlotTurtle(canvas)
    t1.cls()

    t1.coordinateLines(300, 250, 100, 100, -10, 10)

    # plot sin, cos, and tan
    t1.color('red')
    t1.generalPlot(300, 250, 100, 100, "t", "sin(t)", -pi, pi, .01)   
    t1.color('green')
    t1.generalPlot(300, 250, 100, 100, "t", "cos(t)", -pi, pi, .01)   
    t1.color('purple')
    t1.generalPlot(300, 250, 100, 100, "t", "tan(t)", -pi, pi, .01)
    
    # generalPlot takes an equation for x and an equation for y
    # and iterates over a range with a step value
    # t is the value of each iteration

    # hippopede    
    t1.color('black')
    for a in range(20, 50, 5):
        b = 20
        t1.generalPlot(300, 250, 2, 2,
                   "2*cos(t)*sqrt("+str(a)+"*"+str(b)+"-"+"pow("+str(b)+",2)*pow(sin(t), 2))",
                   "2*sin(t)*sqrt("+str(a)+"*"+str(b)+"-"+"pow("+str(b)+",2)*pow(sin(t), 2))",
                   -pi, pi, pi/180)    


    t1.tschirnhausen(200, 250, 5, 3, -4.4, 4.4, .01)
    #t1.tschirnhausen2(200, 250, 5, 3, 1.0, -4.4, 4.4, .01)

    """
    aLow = .1
    aHigh = 2
    aStepSize = .1    
    aSteps = ((aHigh - aLow) / aStepSize) + 2   # aLow to aHigh inclusive
    a = aLow - aStepSize
    for i in range(aSteps):
        a += .1
        # a stepSize of .01 gives pretty smooth curves
        t1.generalPlot(200, 250, 5, 3,
                       "3*" + str(a) + "*(pow(t,2)-3)", "t*" + str(a) + "*(pow(t, 2)-3)",
                       -4.4, 4.4, .01)
    """
