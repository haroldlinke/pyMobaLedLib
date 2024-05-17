# examples derived from
# Turtle Geometry: The Computer as a Medium for Exploring Mathematics
# by Harold Abelson and Andrea diSessa

from wrappers import Turtle

class SunTurtle(Turtle):
    # p. 10
    def arcr(self, r, deg):
        for i in range(deg):
            self.forward(r)
            self.right(1)

    # p. 11
    def arcl(self, r, deg):
        for i in range(deg):
            self.forward(r)
            self.left(1)

    # p. 12
    def ray(self, r):
        for i in range(2):
            self.arcr(r, 90)
            self.arcl(r, 90)
        """
        self.arcl(r, 90)
        self.arcr(r, 90)
        self.arcl(r, 90)
        self.arcr(r, 90)
        """

    # p. 12
    def circles(self):
        for i in range(9):
            self.arcr(1, 360)
            self.right(40)

    # p. 12
    def petal(self, size):
        self.arcr(size, 60)
        self.right(120)
        self.arcr(size, 60)
        self.right(120)

    # p. 12
    def flower(self, size):
        for i in range(6):
            self.petal(size)
            self.right(60)

    # p. 12
    def sun(self, size):
        for i in range(9):
            self.ray(size)
            self.rt(160)


def draw(canvas):
    t = SunTurtle(canvas)
    t.cls()
    #t.circles()
    #t.flower(3)
    
    # simplify coding below by mapping the object methods
    pu = t.pu
    pd = t.pd
    rt = t.rt
    lt = t.lt
    fd = t.fd
    bk = t.bk
    sun = t.sun
    
    pu()
    lt(90)
    fd(225)
    rt(90)
    bk(100)
    pd()

    t.color('gold')
    sun(1.5)

    t.moveTo(10, 10)
    t.write("Good Morning!")
