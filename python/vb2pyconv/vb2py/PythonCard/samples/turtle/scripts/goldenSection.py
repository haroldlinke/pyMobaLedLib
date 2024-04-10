
# adapted from Just example at:
# http://just.letterror.com/ltrwiki/DrawBot
# the main downside to this version that I see
# is that apparently the Oval primitive or underlying
# Mac OS X draw calls change the thickness
# of the oval outline as well as anti-alias the drawing
# which I'm not sure how to do with wxPython
# I could probably anti-alias by drawing at 4x the size and then
# scaling the image I guess?!
# but in comparison that would be lame

import math

def draw(canvas):
    canvas.foregroundColor = 'black'
    canvas.backgroundColor = 'white'
    canvas.clear()

    # if you want to speed up drawing a bit, uncomment
    # the canvas.autoRefresh and canvas.refresh() lines below
    # I think it is more fun to watch the pattern being drawn
    #canvas.autoRefresh = False
    w, h = canvas.size
    
    cx, cy = w/2, h/2
    phi = (math.sqrt(5) + 1)/2-1
    oradius = 10.0
    blue = int(255 * 0.25)
    for i in range(720):
        #c = (0.0, 0.0, 0.0)
        radius = 1.5*oradius * math.sin(i * math.pi/720)
        r = round(radius)
        temp = phi*i*2*math.pi
        # color args need to be ints where 0 <= c <=s 255
        c = min(255 * i / 360.0, 255)
        canvas.fillColor = (c, c, blue)
        canvas.drawEllipse((round(cx-(radius/2) + 0.25*i*math.cos(temp)),
            round(cy-(radius/2) + 0.25*i*math.sin(temp))),
            (r, r))

    #canvas.autoRefresh = True
    #canvas.refresh()
