
from wrappers import Turtle

def draw(canvas):
    t = Turtle(canvas)
    t.cls()

    autoRefreshTemp = t.canvas.autoRefresh
    t.canvas.autoRefresh = 0

    xOffset = 50
    yOffset = 0
    scale = 1.0
    r = 2.9
    # when r was 4.0 I got an exception when doing the int
    # conversion below, so I need to consider the appropriate
    # behaviour when x or y is out of bounds for an int
    # and also out of bounds of the current cliprect or frame
    steps = 400

    inc = (4.0 - 2.9) / steps
    for j in range(steps):
        r += inc
        x = 0.3
        y = j + 30
        for i in range(200):
            x = r * x * (1 - x)

        for i in range(300):
            x = r * x * (1 - x)
            x1 = int(500 * x)
            # originally self.plot(dc, x1, y1, xOffset, yOffset, scale)

            # the scale and offset stuff should probably
            # be part of the turtle or coordinate space
            x2 = int(xOffset + scale * x1)
            y2 = int(yOffset + scale * y)
            t.plot(x2, y2)
        t.canvas.refresh()

    t.canvas.autoRefresh = autoRefreshTemp
