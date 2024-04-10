
import math
from wrappers import Turtle

def draw(canvas):
    t1 = Turtle(canvas)
    t1.cls()

    """
    # test towards (towardsXY)
    # these kinds of tests should be done using pyunit
    tt = Turtle(canvas)
    for i in range(0, 370, 10):
        tt.pu()
        tt.lt(i)
        tt.fd(100)
        print "angle: %f, t1 towards tt: %f, tt towards t1: %f" % (i, t1.towards(tt), tt.towards(t1))
        tt.bk(100)
        tt.rt(i)
    """

    # test the distance calculation
    t1.left(45)
    t1.forward(100 * math.sqrt(2))

    t2 = Turtle(canvas)
    t2.forward(100)
    d = t2.distance(t1)
    # should display 100
    t2.write("%f" % d)

    # test the odometer reading
    t1.resetOdometer()
    t1.resumeOdometer()
    t1.polygon(4, 100)
    t1.write("odometer: %f" % t1.getOdometer())
