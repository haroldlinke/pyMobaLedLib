
# another example that doesn't actually use the turtle for drawing

import math
import sys
from wrappers import Turtle

class ChaosTurtle(Turtle):
    def chaos(self, a=1.5732, xOrig=0.0, yOrig=0.0, endRange=38, 
        xOffset=250, yOffset=250, scale=200.0):

        mult = 1.2 / endRange
        
        tempAutoRefresh = self.canvas.autoRefresh
        self.canvas.autoRefresh = False
        for j in range(1, endRange + 1):
            x = xOrig + mult * j
            y = yOrig + mult * j
            for i in range(1000):
                temp = x * math.cos(a) - (y - (x * x)) * math.sin(a)
                y = x * math.sin(a) + (y - (x * x)) * math.cos(a)
                x = temp
                try:
                    self.canvas.drawPoint((xOffset + scale * x, yOffset + scale * y))
                except OverflowError:
                    pass
            self.canvas.refresh()
        self.canvas.autoRefresh = tempAutoRefresh

    # this is an alternate implementation of the method above, 
    # but it uses drawPointList instead. in order to avoid 
    # an OverflowError exception in drawPointList an explicit
    # check that x1 and y1 are in the maxint conversion range
    # must be done. at least on my machine the need to create
    # the temporary variables x1, y1 and the conversion check
    # ends up making this method slower that the method above
    def chaosWithList(self, a=1.5732, xOrig=0.0, yOrig=0.0, endRange=38, 
        xOffset=250, yOffset=250, scale=200.0):

        mult = 1.2 / endRange
        
        points = []
        maxint = sys.maxint
        for j in range(1, endRange + 1):
            x = xOrig + mult * j
            y = yOrig + mult * j
            for i in range(1000):
                temp = x * math.cos(a) - (y - (x * x)) * math.sin(a)
                y = x * math.sin(a) + (y - (x * x)) * math.cos(a)
                x = temp
                x1 = xOffset + scale * x
                y1 = yOffset + scale * y
                if x1 > -maxint and x1 < maxint and y1 > -maxint and y1 < maxint:
                    points.append((x1, y1))
            self.canvas.drawPointList(points)

def draw(canvas):
    t = ChaosTurtle(canvas)
    t.cls()
    #t.chaos(1.5732, 0.0, 0.0, 38, 250, 250, 200)
    t.chaos(1.1111, 0.0, 0.0, 38, 250, 250, 200)
    # zoom in on one section of the same set as above
    #t.chaos(1.1111, 0.74, 0.27, 500, 0, 0, 500)
