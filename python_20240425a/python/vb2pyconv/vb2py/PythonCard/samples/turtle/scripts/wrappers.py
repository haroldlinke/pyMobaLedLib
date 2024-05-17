
"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/05/11 01:12:51 $"
"""

# by referring to the Turtle class in this
# module rather than PythonCard.turtle.BitmapTurtle
# directly in scripts, the script can be run in
# a different turtle environment such as LegoTurtle
# by simply changing the import line below
# of course, I haven't written those other
# turtle wrappers, but it never hurts to plan ahead <wink>

# i'm open to suggestions for another way of achieving
# the same result, namely not needing to change myriads
# of turtle scripts in order to run them in a different
# graphics environment (BitmapTurtle, LegoTurtle, etc.)

from PythonCard import turtle

class Turtle(turtle.BitmapTurtle):
    pass


# examples derived from
# Visual Modeling with Logo: A Structural Approach to Seeing
# by James Clayson
# and
# Turtle Geometry: The Computer as a Medium for Exploring Mathematics
# by Harold Abelson and Andrea diSessa

class CurvesTurtle(Turtle):
    # TG p. 92
    def cCurve(self, size, level):
        if level == 0:
            self.forward(size)
            return
        self.cCurve(size, level - 1)
        self.right(90)
        self.cCurve(size, level - 1)
        self.left(90)

    # TG p. 93
    def lDragon(self, size, level):
        if level == 0:
            self.forward(size)
            return
        self.lDragon(size, level - 1)
        self.left(90)
        self.rDragon(size, level - 1)

    # TG p. 93
    def rDragon(self, size, level):
        if level == 0:
            self.forward(size)
            return
        self.lDragon(size, level - 1)
        self.right(90)
        self.rDragon(size, level - 1)

    # example derived from
    # Turtle Geometry: The Computer as a Medium for Exploring Mathematics
    # by Harold Abelson and Andrea diSessa
    # p. 96-98
    def hilbert(self, size, level, parity):
        if level == 0:
            return
        # rotate and draw first subcurve with opposite parity to big curve
        self.left(parity * 90)
        self.hilbert(size, level - 1, -parity)
        # interface to and draw second subcurve with same parity as big curve
        self.forward(size)
        self.right(parity * 90)
        self.hilbert(size, level - 1, parity)
        # third subcurve
        self.forward(size)
        self.hilbert(size, level - 1, parity)
        # fourth subcurve
        self.right(parity * 90)
        self.forward(size)
        self.hilbert(size, level - 1, -parity)
        # a final turn is needed to make the turtle
        # end up facing outward from the large square
        self.left(parity * 90)

    # Visual Modeling with Logo: A Structural Approach to Seeing
    # by James Clayson
    # Koch curve, after Helge von Koch who introduced this geometric figure in 1904
    # p. 146
    def fractalgon(self, n, rad, lev, dir):
        import math
        
        # if dir = 1 turn outward
        # if dir = -1 turn inward
        edge = 2 * rad * math.sin(math.pi / n) # logo uses sin(180 / n); Python uses radians
        self.pu()
        self.fd(rad)
        self.pd()
        self.rt(180 - (90 * (n - 2) / n))
        for i in range(n):
            self.fractal(edge, lev, dir)
            self.rt(360 / n)
        self.lt(180 - (90 * (n - 2) / n))
        self.pu()
        self.bk(rad)
        self.pd()

    # p. 146
    def fractal(self, dist, depth, dir):
        if depth < 1:
            self.fd(dist)
            return
        self.fractal(dist / 3, depth - 1, dir)
        self.lt(60 * dir)
        self.fractal(dist / 3, depth - 1, dir)
        self.rt(120 * dir)
        self.fractal(dist / 3, depth - 1, dir)
        self.lt(60 * dir)
        self.fractal(dist / 3, depth - 1, dir)
