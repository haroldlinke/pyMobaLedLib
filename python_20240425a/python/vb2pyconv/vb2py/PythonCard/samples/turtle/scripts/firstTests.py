
from wrappers import CurvesTurtle

class SimpleTurtle(CurvesTurtle):
    def square1(self, distance):
        self.polygon(4, distance)

    # just to be different, turn right instead of left
    def square2(self, distance):
        for i in range(4):
            self.forward(distance)
            self.right(90)

    def polygon(self, sides, distance):
        angle = 360.0 / sides
        for i in range(sides):
            self.forward(distance)
            self.left(angle)

def draw(canvas):
    t = SimpleTurtle(canvas)
    t.color('blue')
    t.rDragon(3, 12)
    t.color('orange')
    t.cCurve(5, 10)
    t.color('black')
    t.square2(30)
    t.square1(100)
    t.polygon(6, 30)
    #print t._invradian
    #print t.angle
    
    # I would like to be able to call routines like square2 and polygon1
    # without having refer to the object if something like below
    # is possible?
    #def polygon(sides, distance): tc.polygon1(sides, distance)
    #polygon(3, 60)
    
    # I got this from chapter 4 of Learning Python, it seems to work
    # functions are just objects
    # so we create local objects that point to the methods of the object
    # this only works for the object, not the class in general, so a
    # different solution might be more appropriate
    square = t.square1
    polygon = t.polygon

    t.color('green')
    # test to see if we get a green square
    square(150)
    # this also shows some kind of truncation or rounding error
    # the top corners of the triangle are off by one pixel
    t.color('black')
    
    t.pu()
    t.home()
    t.lt(180)
    t.fd(200)
    t.rt(180)
    t.pd()
    t.color('blue')
    for i in range(5):
        polygon(5, 40)
        #t.polygon(5, 40)
        t.left(360.0 / 5)

    t2 = SimpleTurtle(canvas)
    t2.color('red')
    t2.polygon(16, 10)

    t.color('blue')
    #t.forward(200)
    polygon(8, 80)

    # if this works correctly
    # the arcs will be different colors
    # so _goto has to be changed to set the pen characteristics
    # before drawing
    for i in range(18):
        #t.color('blue')
        t.forward(50)
        t.right(30)
        #t2.color('red')
        t2.fd(50)
        t2.rt(30)
