"""
based on the "madness" algorithm by Stanley S. Miller
presented in the May 1988 Scientific American
Computer Recreations column by A. K. Dewdney
algorithm starts on page 121
"""
import math
from math import cos, sin
from wrappers import Turtle

class MadnessTurtle(Turtle):
    def madness(self, xOffset, yOffset, scale, n, stepSize):
        # in the article, the equations were
        # x = sin(.99 * t) - .7 * cos(3.01 * t)
        # y = cos(1.01 * t) + .1 * sin(15.03 * t)
        # the units of t are radians
        
        a = 1.0     # a = 0.3
        b = 0.99
        c = -0.7
        d = 3.01
        e = 1.0     # e = 0.9
        f = 1.01
        g = 0.1
        h = 15.03

        # moveTo the first point to avoid a line from
        # the center position
        t = -n * stepSize
        x = a * sin(b * t) + c * cos(d * t)
        y = e * cos(f * t) + g * sin(h * t)
        self.moveTo(x * scale + xOffset, y * scale + yOffset)
        for t in range(-n, n):
            t *= stepSize
            x = a * sin(b * t) + c * cos(d * t)
            y = e * cos(f * t) + g * sin(h * t)
            #self.plot(x * scale + xOffset, y * scale + yOffset)
            self.lineTo(x * scale + xOffset, y * scale + yOffset)

def draw(canvas):
    t1 = MadnessTurtle(canvas)
    t1.cls()
    
    # a stepSize of .01 gives pretty smooth curves
    t1.madness(350, 250, 200, 40000, .01)
