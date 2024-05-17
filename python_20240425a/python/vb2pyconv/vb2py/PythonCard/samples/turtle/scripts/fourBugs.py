# example based on article in BYTE magazine
# 4 bugs starting in separate corners of a square
# walk towards each other (this is also the picture on the cover)
# November 1982
# p. 236 - 240

from wrappers import Turtle
import wx

def draw(canvas):
    t = Turtle(canvas)
    t.cls()

    # create four bugs and send them to the four corners of a square
    bug1 = Turtle(canvas)
    bug1.color('magenta')
    bug1.st()
    bug1.pu()
    bug1.rt(45)
    bug1.fd(300)
    bug1.pd()

    bug2 = Turtle(canvas)
    bug2.color('green')
    bug2.st()
    bug2.pu()
    bug2.rt(135)
    bug2.fd(300)
    bug2.pd()

    bug3 = Turtle(canvas)
    bug3.color('blue')
    bug3.st()
    bug3.pu()
    bug3.rt(225)
    bug3.fd(300)
    bug3.pd()

    bug4 = Turtle(canvas)
    bug4.color('orange')
    bug4.st()
    bug4.pu()
    bug4.rt(315)
    bug4.fd(300)
    bug4.pd()

    # bug1 is added at the end of the list as a convenience
    bList = [bug1, bug2, bug3, bug4, bug1]

    # speed up drawing time
    tempAutoRefresh = canvas.autoRefresh
    canvas.autoRefresh = 0

    # the bugs take 400 "steps" toward each other
    for i in range(430):
        # orient each bug towards its neighbor
        # by doing this separately from
        # the step forward, we don't need to maintain
        # state in a separate list
        for b in range(4):
            h = bList[b].towards(bList[b + 1])
            bList[b].setHeading(h)
    
        # each bug takes one step forward
        for b in range(4):
            bList[b].fd(1)
        canvas.refresh()
        if wx.Platform == '__WXMAC__':
            canvas.redraw()

    canvas.autoRefresh = tempAutoRefresh

    for b in range(4):
        bList[b].ht()

