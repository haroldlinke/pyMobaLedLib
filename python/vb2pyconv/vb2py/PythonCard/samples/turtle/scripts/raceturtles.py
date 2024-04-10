# simple example to show putting multiple
# turtles in a list and then applying the
# same function to each one, in this case
# "racing" them down the screen

from wrappers import Turtle

def draw(canvas):
    t = Turtle(canvas)
    t.cls()

    #print "On your mark, get set,",
    # don't make this larger than 255
    # since we're using a different shade of red for each turtle
    # and there are only 256 shades :)
    maxTurtles = 200
    tList = []
    for i in range(maxTurtles):
        t = Turtle(canvas)
        t.moveTo((i + 1) * 3, 10)
        t.rt(90)
        t.color(i + (255 - maxTurtles), 0 , 0)  # r, g, b color
        tList.append(t)

    autoRefreshTemp = tList[0].canvas.autoRefresh
    tList[0].canvas.autoRefresh = False

    #print "go!"
    for i in range(50):
        for t in tList:
            t.fd(10)
        tList[0].canvas.refresh()

    tList[0].canvas.autoRefresh = autoRefreshTemp
