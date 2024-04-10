# test coordinate system

from wrappers import Turtle

class CoordinatesTurtle(Turtle):
    def doTick(self, n):
        self.right(90)
        self.forward(5)
        self.write("%d" % n)
        self.back(10)
        self.forward(5)
        self.left(90)

def draw(canvas):
    t = CoordinatesTurtle(canvas)
    t.cls

    t.plot() # "0, 0" in Logo space, but "windowWidth / 2, windowHeight / 2" in Guido space
    # in Guido space (turtle.py from Python standard library)
    t.color('green')
    for i in range(4):
        t.fd(250)
        t.doTick(250)
        t.fd(250)
        t.bk(500)
        t.lt(90)
    # note that the lines are not perfectly straight above which indicates a truncation or
    # rounding bug. since i have yet to mess with the coordinate system or keeping a high-precision
    # virtual turtle that is only converted to integer coordinates when drawing i haven't
    # traced out the problem

    """
    t.plot(10, 10)
    t.plot(10, 500)
    t.plot(500, 500)
    t.plot(500, 10)
    """

    
    t.color('gray')
    for i in (10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180):
        t.lt(i)
        t.fd(i * 2)
        #print t._angle
        # change this to write on screen, DrawText or something
        t.write("%d" % t._angle)
        t.bk(i * 2)
        t.rt(i)
    
