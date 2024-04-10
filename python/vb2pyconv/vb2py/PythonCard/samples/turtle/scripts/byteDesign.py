# example based on article in BYTE magazine
# Problem Solving with Logo: Using Turtle Graphics to Redraw a Design
# November 1982
# p. 118 - 134

from wrappers import Turtle

class ByteTurtle(Turtle):
    def design(self, homePos, scale):
        self.pu()
        for i in range(5):
            self.fd(64.65 * scale)
            self.pd()
            self.wheel(self.getXY(), scale)
            self.pu()
            self.bk(64.65 * scale)
            self.rt(72)
        self.pu(); self.setXY(homePos); self.rt(36); self.fd(24.5 * scale); self.rt(198); self.pd()
        self.centerpiece(46 * scale, 143.4, scale)

    def wheel(self, initpos, scale):
        self.rt(54)
        for i in range(4): self.pentpiece(initpos, scale)
        self.pd(); self.lt(36)
        for i in range(5): self.tripiece(initpos, scale)
        self.lt(36)
        for i in range(5):
            self.pd()
            self.rt(72)
            self.fd(28 * scale)
            self.pu()
            self.bk(28 * scale)
        self.lt(54)

    def tripiece(self, initpos, scale):
        oldh = self.getHeading()
        self.pd(); self.bk(2.5 * scale)
        self.tripolyr(31.5 * scale, scale)
        self.pu(); self.setXY(initpos); self.setHeading(oldh)
        self.pd(); self.bk(2.5 * scale)
        self.tripolyl(31.5 * scale, scale)
        self.pu(); self.setXY(initpos); self.setHeading(oldh)
        self.lt(72)

    def pentpiece(self, initpos, scale):
        oldh = self.getHeading()
        self.pu(); self.fd(29 * scale); self.pd()
        for i in range(5):
            self.fd(18 * scale)
            self.rt(72)
        self.pentr(18 * scale, 75, scale)
        self.pu(); self.setXY(initpos); self.setHeading(oldh)
        self.fd(29 * scale); self.pd()
        for i in range(5):
            self.fd(18 * scale)
            self.rt(72)
        self.pentl(18 * scale, 75, scale)
        self.pu(); self.setXY(initpos); self.setHeading(oldh)
        self.lt(72)

    def pentl(self, side, ang, scale):
        if side < (2 * scale): return
        self.fd(side)
        self.lt(ang)
        self.pentl(side - (.38 * scale), ang, scale)

    def pentr(self, side, ang, scale):
        if side < (2 * scale): return
        self.fd(side)
        self.rt(ang)
        self.pentr(side - (.38 * scale), ang, scale)

    def tripolyr(self, side, scale):
        if side < (4 * scale): return
        self.fd(side)
        self.rt(111)
        self.fd(side / 1.78)
        self.rt(111)
        self.fd(side / 1.3)
        self.rt(146)
        self.tripolyr(side * .75, scale)

    def tripolyl(self, side, scale):
        if side < (4 * scale): return
        self.fd(side)
        self.lt(111)
        self.fd(side / 1.78)
        self.lt(111)
        self.fd(side / 1.3)
        self.lt(146)
        self.tripolyl(side * .75, scale)
        
    def centerpiece(self, s, a, scale):
        self.fd(s); self.lt(a)
        if s < (7.5 * scale): return
        self.centerpiece(s - (1.2 * scale), a, scale)

def draw(canvas):
    t = ByteTurtle(canvas)
    t.cls()
    """
    t.pu()
    t.lt(90)
    t.fd(30)
    t.rt(90)
    t.pd()
    """

    t.design(t.getXY(), 2.3)
