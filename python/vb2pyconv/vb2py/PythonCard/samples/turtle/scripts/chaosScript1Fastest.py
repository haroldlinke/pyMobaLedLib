# KEA 2001-10-14
# this is the same algorithm as chaosScript1.py
# but rather than using a turtle, the script below uses the
# canvas (BitmapCanvas) and drawPointList directly
# it still draws line by line so the pattern evolves
# on the screen rather than just showing the whole thing at once
# plus the extra blit overhead for each line isn't that bad
# with a decent video card
def draw(canvas):
    canvas.clear()

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
        points = []
        r += inc
        x = 0.3
        y = j + 30
        for i in range(200):
            x = r * x * (1 - x)

        for i in range(300):
            x = r * x * (1 - x)
            x1 = int(500 * x)
            x2 = int(xOffset + scale * x1)
            y2 = int(yOffset + scale * y)
            points.append((x2, y2))

        canvas.drawPointList(points)
