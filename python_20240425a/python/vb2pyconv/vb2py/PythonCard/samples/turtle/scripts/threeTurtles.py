
from wrappers import CurvesTurtle

def draw(canvas):
    # top left corner is 0,0 and bottom right is some positive x and positive y
    # so the coordinate space is not like a Logo turtle where 0,0 is the center
    # of the screen
    t1 = CurvesTurtle(canvas)
    t1.color('red')
    # show turtle
    #t1.st()
    # get rid of any previous drawing
    t1.cls()
    
    t2 = CurvesTurtle(canvas)
    t2.color('green')
    #t2.st()
    t2.left(120)
    
    t3 = CurvesTurtle(canvas)
    t3.color('blue')
    #t3.st()
    t3.left(240)

    tList = [t1, t2, t3]
    for t in tList:
        t.pu()
        t.forward(50)
        t.pd()

##    for i in range(6):
##        [t.fd(80) for t in tList]
##        [t.rt(60) for t in tList]

    #[t.cCurve(4, 10) for t in tList]
    [t.rDragon(4, 11) for t in tList]
    #[t.lDragon(4, 11) for t in tList]
    
