# examples derived from
# Visual Modeling with Logo: A Structural Approach to Seeing
# by James Clayson
# and
# Turtle Geometry: The Computer as a Medium for Exploring Mathematics
# by Harold Abelson and Andrea diSessa

import wrappers
from random import uniform

class TreesTurtle(wrappers.Turtle):
    # TG p. 85
    def node(self, length, angle, level):
        if level == 0: return
        # point along left branch and draw it
        self.left(angle)
        self.lbranch(length, angle, level - 1)
        # draw right branch
        self.right(2 * angle)
        self.rbranch(length, angle, level - 1)
        # make node state-transparent
        self.left(angle)

    # TG p. 84
    def lbranch(self, length, angle, level):
        # draw a long stem
        self.forward(2 * length)
        # do next level
        self.node(length, angle, level)
        # make lbranch state-transparent
        self.back (2 * length)

    # TG p. 84
    def rbranch(self, length, angle, level):
        # draw a short stem
        self.forward(length)
        # do next level
        self.node(length, angle, level)
        # make lbranch state-transparent
        self.back (length)

    # VM p. 292
    def tree(self, a, b, n, t, bt, f, l):
        if l < 1: return
        pos = self.getXY()
        self.fd(a)
        self.rt(t)
        for i in range(n):
            pos2 = self.getXY()
            self.fd(b)
            self.tree(a * f, b * f, n, t, bt, f, l - 1)
            #self.bk(b)
            self.setXY(pos2)
            self.lt(bt)
        self.rt((n * bt) - t)
        #self.moveTo(pos[0], pos[1])
        self.setXY(pos)
        #self.bk(a)

    # VM p. 306
    def randTree(self, a, n, t, bt, f, l):
        # to draw multiply branched recursive trees
        # with randomized components
        if l < 1: return
        # save the current position and angle
        pos = self.getXY()
        heading = self.getHeading()
        self.fd(uniform(0.5 * a, 1.5 * a))
        self.rt(uniform(0.5 * t, 1.5 * t))
        #self.fd(uniform(0.5 * t, 1.5 * t))
        for i in range(n):
            d = uniform(0.5 * a / 2, 1.5 * a / 2)
            # save the position (not the heading)
            pos2 = self.getXY()
            self.fd(d)
            self.randTree(a * f, n, t, bt, f, l - 1)
            # restore the position
            self.setXY(pos2)
            self.lt(uniform(0.5 * bt, 1.5 * bt))
        # restore the saved position and heading
        self.setXY(pos)
        self.setHeading(heading)

    def testTree(self, size):
        if size < 5: return
        self.fd(size)
        self.lt(30)
        self.testTree(size * .7)
        self.rt(60)
        self.testTree(size * .7)
        self.lt(30)
        self.bk(size)

    def testRTree(self, size):
        if size < 5: return
        self.fd(size)
        self.lt(30)
        self.testRTree(size * ((uniform(1, 5) + 5) / 10))
        self.rt(60)
        self.testRTree(size * ((uniform(1, 5) + 5) / 10))
        self.lt(30)
        self.bk(size)


def draw(canvas):
    t = TreesTurtle(canvas)
    t.cls()
    t.left(90)

    #t.tree(80, 40, 4, 60, 30, .6, 5)
    #t.randTree(50, 3, 60, 30, .6, 4)
    #t.randTree(30, 3, 30, 30, .75, 5)
    #t.randTree(30, 3, 30, 15, .9, 5)

    t.pu()
    t.bk(150)
    t.pd()
    #t.testTree(75)
    t.testRTree(50)

    #t.lbranch(20, 20, 7)
