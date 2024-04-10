# examples derived from
# Visual Modeling with Logo: A Structural Approach to Seeing
# by James Clayson
# p. 146
# and
# Turtle Geometry: The Computer as a Medium for Exploring Mathematics
# by Harold Abelson and Andrea diSessa
# p. 91
# see http://physics.hallym.ac.kr/education/chaos/ncsa/Fgeom.html
# for some more explanation of fractals

from wrappers import CurvesTurtle

def draw(canvas):
    t = CurvesTurtle(canvas)
    t.cls()
    t.pu()
    t.lt(90)
    t.fd(50)
    t.rt(90)
    t.pd()
    
    # VM p. 146
    t.fractalgon(3, 200, 4, -1)
    t.fractalgon(3, 250, 4, 1)

    # if you turn on the odometer you should see the total distance
    # the turle has gone, so you can compare a level 1 curve to
    # level 2, 3, etc.
    # but you will need to subtract the radius (rad) distance * 2
    # to compensate for the forward() and back() calls in fractalgon
    # the same distance measurements can be done with other curves:
    # cCurves, dragon, hilbert, or any drawing commands
    # for example as the number of sides increases in a polygon
    # the distance traveled will approach the 2 * pi * r (the radius)
    # (circumference) of the circle bounded by the polygon
    #
    # odometer commands
    # t.getOdometer()
    # t.resumeOdometer()
    # t.resetOdometer()
    # t.suspendOdometer()

