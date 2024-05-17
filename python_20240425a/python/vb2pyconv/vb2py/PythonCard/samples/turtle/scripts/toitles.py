from wrappers import Turtle

def draw(canvas):
    t = Turtle(canvas)
    t.cls()

    namedColors = ['aquamarine', 'black', 'blue', 'blue violet', 'brown', 'cadet blue',
                   'coral', 'cornflower blue', 'cyan', 'dark grey', 'dark green',
                   'dark olive green', 'dark orchid', 'dark slate blue']
    boids = []
    for i in range(len(namedColors)):
        b = Turtle(canvas)
        b.moveTo(50, 50)
        #b.penUp()
        b.color(namedColors[i])
        print namedColors[i]
        b.showTurtle()
        b.rt(5 * i)
        b.fd(10 * i)
        boids.append(b)

    autoRefreshTemp = boids[0].canvas.autoRefresh
    boids[0].canvas.autoRefresh = False

    for i in range(550):
        for b in boids:
            b.fd(1)
        boids[0].canvas.refresh()

    boids[0].canvas.autoRefresh = autoRefreshTemp

