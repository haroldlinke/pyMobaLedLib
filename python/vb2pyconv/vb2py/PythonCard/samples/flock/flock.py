#!/usr/bin/python

"""
Builds on the "gravity" sample to show a simple animation of "boids"; shows simple emergent behaviour for a 2-D flock of "boids".

This sample uses two images to animate the movement of bird-like objects.
"""
__version__ = "$Revision: 1.4 $"
__date__ = "$Date: 2005/12/14 01:24:24 $"

# KEA 2004-09-25
# based on the excellent work by Keith Peters
# http://www.bit-101.com/tutorials/gravity.html

# AGT 2004-10-05
# Based on Kevin's imagegravity sample - simple 2-D boids

from __future__ import division

try:
    import psyco
    psyco.full()
except ImportError:
    pass

import os
import wx
import random

from PythonCard import clipboard, dialog, graphic, model, util, timer


# helper functions
def pointInRect(xy, rect):
    x, y = xy
    left, top, right, bottom = rect
    if x >= left and x <= right and y >= top and y <= bottom:
        return True
    else:
        return False

visible_radius = 1000
max_neighbours = 40

def randomColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def find_nearest(this, allsprites):
    nearest = []
    for s in allsprites:
        if s == this: continue
        if s.x < this.x-visible_radius: continue
        if s.x > this.x+visible_radius: continue
        dist = abs(s.x-this.x)+abs(s.y-this.y)
        if dist > visible_radius: continue
        nearest.append( (dist, s.x, s.y, s.xspeed, s.yspeed) )
    if len(nearest) == 0: return nearest

    nearest.sort()
    del nearest[max_neighbours:]
    return nearest

def centre_of_mass(this, allsprites, nearest):
    x,y = 0,0
    if len(nearest) == 0: return 0,0
    for nbr in nearest:
        x += nbr[1]
        y += nbr[2]
    num = len(nearest)
    return (x/num - this.x)*0.01, (y/num - this.y)* 0.01

def not_too_close(this, allsprites, nearest):
    x,y = 0, 0
    for nbr in nearest:
        if nbr[0] < 16:
            x += this.x - nbr[1]
            y += this.y - nbr[2]
    return x,y

def align_with(this, allsprites, nearest):
    x,y = 0,0
    for nbr in nearest:
        x += nbr[3]
        y += nbr[4]
    num = len(nearest)
    return 0.125 * x/num, 0.125 * y/num

class Sprite(object):
    def __init__(self, parent):
        self.parent = parent

class BoidSprite(Sprite):
    def __init__(self, parent, name, x, y, radius, color='red'):
        Sprite.__init__(self, parent)
        self.name = name
        self.name2 = name+"-2"
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y
        self.radius = radius
        self.color = color
        self.xspeed = random.random() * 30
        self.yspeed = random.random() * 30
        self.gravity = 2
        self.drag = .85
        self.bounce = .9
        self.dragging = False
        self.canvas = self.parent.components.bufOff
##        self.canvas = self.parent.panel
        x, y = self.canvas.position
##        self.parent.components[name] = {'type':'Image', 'name':name, 'file':'wing1.png', 'position':(self.x + x, self.y + y)}
##        self.image = self.parent.components[name]
##        self.image.visible = True
##        self.parent.components[self.name2] = {'type':'Image', 'name':self.name2, 'file':'wing2.png', 'position':(self.x + x, self.y + y)}
##        self.image2 = self.parent.components[self.name2]
##        self.image.visible = False
        self.image = graphic.Bitmap('wing1.png')
        self.image2 = graphic.Bitmap('wing2.png')
        self.count = 0

    def move(self):
        # this is sort of pointless right now
        # but maybe the dragging code could be moved
        # into the class in which case we might need
        # to know if we're dragging
        if not self.dragging:
            nearest = find_nearest(self, self.parent.sprites)
            x1, y1 = self.xspeed * self.drag, self.yspeed * self.drag
            if len(nearest) > 0:
                x2, y2 = centre_of_mass(self, self.parent.sprites, nearest)
                x3, y3 = not_too_close(self, self.parent.sprites, nearest)
                x4, y4 = align_with(self, self.parent.sprites, nearest)
                x1 += x2+x3+x4
                y1 += y2+y3+y4
            self.xspeed, self.yspeed = x1, y1
            #rint self.name, (x1,y1), (x2, y2), (self.xspeed, self.yspeed)
            
            self.x += self.xspeed
            self.y += self.yspeed
            rightedge, bottomedge = self.canvas.size
            # bounce when we hit the edge
            if (self.x - self.radius) < 0:
                self.x = self.radius
                self.xspeed = -self.xspeed * self.bounce
            elif (self.x + self.radius) > rightedge:
                self.x = rightedge - self.radius
                self.xspeed = -self.xspeed * self.bounce
            if (self.y - self.radius) < 0:
                self.y = self.radius
                self.yspeed = -self.yspeed * self.bounce
            elif (self.y + self.radius) > bottomedge:
                self.y = bottomedge - self.radius
                self.yspeed = -self.yspeed * self.bounce
##            self.xspeed = self.xspeed * self.drag
##            self.yspeed = self.yspeed * self.drag + self.gravity
        else:
            self.xspeed = self.x - self.oldx
            self.yspeed = self.y - self.oldy
            self.oldx = self.x
            self.oldy = self.y
        self.draw()

    def draw(self):
        self.count += 1
        if self.count == 5:
            self.count = 0
            self.canvas.drawBitmap(self.image, (self.x, self.y))
        else:
            self.canvas.drawBitmap(self.image2, (self.x, self.y))


    def draw2(self):
        self.image.position = (self.x, self.y)
        self.image2.position = (self.x, self.y)
        self.count += 1
        if self.count == 5:
            self.count = 0
            self.image.visible = not self.image.visible
            self.image2.visible = not self.image2.visible
        
class Boids(model.Background):

    def on_initialize(self, event):
        self.x = 0
        self.y = 0
        self.animate = False
        self.filename = None
        # leave it black for now
        #self.components.bufOff.foregroundColor = self.color
        self.sprites = []
        self.timer = timer.Timer(self.components.btnAnimate, -1)
        self.initSizers()
        self.components.bufOff.autoRefresh = False

    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        comp = self.components
        flags = wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_BOTTOM
        # Mac wxButton needs 7 pixels on bottom and right
        macPadding = 7
        sizer2.Add(comp.btnNewBoid, 0, flags, macPadding)
        sizer2.Add(comp.btnAnimate, 0, flags, macPadding)
        sizer2.Add(comp.btnStop, 0, flags, macPadding)
        sizer1.Add(sizer2, 0)
        sizer1.Add(comp.bufOff, 1, wx.EXPAND)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()


    def on_btnNewBoid_mouseClick(self, event):
        name = 'boid' + str(len(self.sprites))
        self.sprites.append(BoidSprite(self, name, 20, 20, 15, randomColor()))
        if not self.animate:
            for b in self.sprites:
                b.draw()
            self.components.bufOff.refresh()

    def on_btnAnimate_mouseClick(self, event):
        event.target.enabled = False
        self.animate = True
        self.frame = 0
        self.startTime = util.time()
        self.fps = 10
        timePerFrame = 1000 / self.fps
        self.timer.start(timePerFrame)

    def on_btnAnimate_timer(self, event):
        self.components.bufOff.clear()
        for b in self.sprites:
            b.move()
        # don't need to use redraw() on Mac because
        # we are using a timer and giving the screen
        # a chance to update it itself normally
        self.components.bufOff.refresh()
        self.frame += 1
        self.seconds = util.time()        
        self.statusBar.text = "Average FPS: %.4f     Boids: %d" % (self.frame / (self.seconds - self.startTime), len(self.sprites))

    def on_btnStop_mouseClick(self, event):
        self.animate = False
        self.components.btnAnimate.enabled = True
        self.timer.stop()

    def on_close(self, event):
        self.animate = False
        event.skip()


if __name__ == '__main__':
    app = model.Application(Boids)
    app.MainLoop()

