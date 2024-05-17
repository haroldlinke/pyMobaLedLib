# examples derived from
# Visual Modeling with Logo: A Structural Approach to Seeing
# by James Clayson

from wrappers import Turtle
import math
from math import pi, sin

class GonTurtle(Turtle):
    # same as polygon, but without the efficiency ;-)
    def ngon(self, n, edge):
        for i in range(n):
            self.fd(edge)
            self.rt(360.0 / n)

    # draw a n-sided polygon with radius rad
    # p. 30
    def cngon(self, n, rad):
        self.pu()
        self.fd(rad)
        angle = 180 - (90 * (n - 2) / n)
        self.rt(angle)
        self.pd()
        edge = 2 * rad * sin(pi / n) # logo uses sin(180 / n); Python uses radians
        self.ngon(n, edge)
        self.left(angle)
        self.pu()
        self.bk(rad)
        self.pd()

    # p. 22
    def spingon(self, n, edge, angle, growth, times):
        if times < 1:
            return
        self.ngon(n, edge)
        self.rt(angle)
        self.spingon(n, edge * growth, angle, growth, times - 1)

    # another way to do recursion, though the way above seems best
    """
    def spingon(self, n, edge, angle, growth, times):
        if times > 0:
            self.ngon(n, edge)
            self.rt(angle)
            self.spingon(n, edge * growth, angle, growth, times - 1)
    """

def draw(canvas):
    t = GonTurtle(canvas)
    t.cls()

    # check that variations of plot works
    """
    t.plot() # uses current x, y #t.plot(375, 300)
    t.plot(None,10)
    t.plot(10,None)
    """
    # p. 21
    #t.spingon(50, 3, 10, 1.02, 95)


    radius = 150

    # check the radius by uncommenting this
    """
    t.color('blue')
    for i in range(36):
        t.fd(radius)
        t.bk(radius)
        t.rt(10)
    """

    """
    # show that as the number of sides increases
    # the distance traveled approaches the circumference
    # of the circle
    # use the built-in cPolygon (centered-Polygon aTurtle class method)
    # output is sent to the console window
    print "circumference: %f" % (2 * pi * radius)
    for i in range(3, 30):
        t.resetOdometer()
        t.resumeOdometer()
        t.cPolygon(i, radius)
        dist = t.getOdometer() - (2 * radius)
        print "sides: %d, distance: %f" % (i, dist)
    t.suspendOdometer()
    """
    
    # same as t.color('black')
    t.color(0, 0, 0)
    # any r, g, b values between 0 - 255 are valid
    t.color(50, 100, 200)

    """"""
    for i in range(10):
        t.cngon(8, radius)
        #t.cngon(6, radius)
        #t.cngon(5, radius)
        #t.cngon(4, radius)
        #t.cngon(3, radius)
        t.rt(5)
        radius = radius - 5
    """"""
