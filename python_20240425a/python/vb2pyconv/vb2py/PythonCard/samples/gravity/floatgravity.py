#!/usr/bin/python

"""
Conversion of Flash animation to PythonCard.
"""
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2005/12/13 11:13:23 $"

# KEA 2004-09-25
# based on the excellent work by Keith Peters
# http://www.bit-101.com/tutorials/gravity.html
# I started with the doodle sample, so this sample still
# contains some cruft
# the big missing item is that I'm not currently doing hit
# detection on the individual balls so they go right through each
# other. I guess that needs to be part of the move method
# with a reference back to the sprites list, but I have
# a feeling it will be more complicated because if ball 1
# runs into ball 2, then they both need to react...

from PythonCard import clipboard, dialog, graphic, model, util
import wx
import os
import random


# helper functions
def pointInRect(xy, rect):
    x, y = xy
    left, top, right, bottom = rect
    if x >= left and x <= right and y >= top and y <= bottom:
        return True
    else:
        return False

def randomColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Sprite(object):
    def __init__(self, canvas):
        self.canvas = canvas

class BallSprite(Sprite):
    def __init__(self, canvas, x, y, radius, color='red'):
        Sprite.__init__(self, canvas)
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y
        self.radius = radius
        self.color = color
        self.xspeed = random.random() * 30
        self.yspeed = random.random() * 30
        self.gravity = 2
        self.drag = .98
        self.bounce = .9
        self.dragging = False
        
        self.circle = canvas.AddCircle(x, y, radius * 2, LineWidth=1, LineColor='black',FillColor=color)
        print self.circle
        print dir(self.circle)

    def move(self):
        # this is sort of pointless right now
        # but maybe the dragging code could be moved
        # into the class in which case we might need
        # to know if we're dragging
        if not self.dragging:
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
            self.xspeed = self.xspeed * self.drag
            self.yspeed = self.yspeed * self.drag + self.gravity
        else:
            self.xspeed = self.x - self.oldx
            self.yspeed = self.y - self.oldy
            self.oldx = self.x
            self.oldy = self.y
            #print "speed", self.xspeed, self.yspeed
        self.draw()

    def draw(self):
##        self.canvas.setFillColor(self.color)
        #self.canvas.foregroundColor = self.color
##        self.canvas.drawCircle((self.x, self.y), self.radius)
        # this should probably be part of move, draw with a FloatCanvas
        # wouldn't need to do anything?!
        self.circle.SetXY(self.x, self.y)
        
class Gravity(model.Background):

    def on_initialize(self, event):
        self.x = 0
        self.y = 0
        self.dragging = False
        self.animate = False
        self.filename = None
        # leave it black for now
        #self.components.bufOff.foregroundColor = self.color
        self.sprites = []
        self.initSizers()

        canvas = self.components.bufOff
        canvas.ClearAll()
        canvas.SetProjectionFun(None)

        # go ahead and create one ball to get started
        # if you want to stress the animation loop
        # uncomment the loop below
        # my Win2K box can do approximately 130 balls and still
        # maintain 30 (29.9...) FPS, but above that and it starts
        # to slow down
##        for i in range(130):
##            self.sprites.append(BallSprite(self.components.bufOff, 20, 20, 15, randomColor()))
        self.on_btnNewBall_mouseClick(None)

    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        comp = self.components
        flags = wx.ALL | wx.ALIGN_CENTER_VERTICAL
        padding = 7
        sizer2.Add(comp.btnNewBall, 0, flags, padding)
        sizer2.Add(comp.btnAnimate, 0, flags, padding)
        sizer2.Add(comp.btnStop, 0, flags, padding)
        sizer1.Add(sizer2, 0)
        sizer1.Add(comp.bufOff, 1, wx.EXPAND)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()


    def on_btnNewBall_mouseClick(self, event):
        canvas = self.components.bufOff
        self.sprites.append(BallSprite(canvas, 20, 20, 15, randomColor()))
        if not self.animate:
##            canvas.clear()
            for ball in self.sprites:
                ball.draw()
            canvas.redraw()
            self.statusBar.text = "Balls: %d" % len(self.sprites)
            

    def on_btnAnimate_mouseClick(self, event):
        event.target.enabled = False
        canvas = self.components.bufOff
##        canvas.autoRefresh = False
        self.animate = True
        avgfps = 0
        frame = 0
        
        seconds = util.time()
        # number of frames to display a second
        # on faster boxes this will throttle the number
        # of frames calculated and displayed, but on slower
        # boxes it won't prevent slowdown
        fps = 30
        # amount of time that should pass before drawing another frame
        timePerFrame = 1.0 / fps
        #print timePerFrame
        
        # hack to force a difference
        # between time and startTime
        # to avoid a division by zero exception on fast machines
        # aka my Windows box ;-)
        startTime = util.time() - 0.001
        while self.animate:
            newSeconds = util.time()
            if newSeconds - seconds >= timePerFrame:
                seconds = newSeconds
##                canvas.clear()
                for ball in self.sprites:
                    ball.move()
                if wx.Platform == '__WXMAC__':
                    canvas.redraw()
                else:
##                    canvas.refresh()
                    pass
                frame += 1
                self.statusBar.text = "Average FPS: %.4f     Balls: %d" % (frame / (seconds - startTime), len(self.sprites))
            # give the user a chance to click Stop
            wx.SafeYield(self, True)

    def on_btnStop_mouseClick(self, event):
        self.animate = False
        self.components.btnAnimate.enabled = True

    def on_close(self, event):
        self.animate = False
        event.skip()


    def on_bufOff_mouseDown(self, event):
        #event.target.drawLine((self.x, self.y), (self.x + 1, self.y + 1))
        # figure out which ball the user clicked on, if any
        # i want to search the list from back to front
        # but I don't change the list in place, so I make a copy
        # is there a way to iterate over a list in reverse without
        # using something awkward like
        # for i in range(len(self.sprites) - 1, -1, -1):
        sprites = self.sprites[:]
        sprites.reverse()
        for ball in sprites:
            radius = ball.radius
            x = ball.x
            y = ball.y
            #print "point", event.position
            #print "rect", x - radius, y - radius, x + radius, y + radius
            if pointInRect(event.position, (x - radius, y - radius, x + radius, y + radius)):
                self.dragging = ball
                ball.dragging = True
                x, y = event.position
                self.dx = ball.x - x
                self.dy = ball.y - y
                #print self.dx, self.dy
                break

    # on a mouseLeave we will no longer
    # get drag messages, so we could end dragging
    # at that point, just keep the current behavior
    
    def on_bufOff_mouseDrag(self, event):
        if self.dragging:
            x, y = event.position
            ball = self.dragging
            ball.x = x + self.dx
            ball.y = y + self.dy
            
            # reraw all the objects
            self.components.bufOff.clear()
            for ball in self.sprites:
                ball.move()
            if wx.Platform == '__WXMAC__':
                self.components.bufOff.redraw()
            else:
                self.components.bufOff.refresh()
            

    def on_bufOff_mouseUp(self, event):
        if self.dragging:
            self.dragging.dragging = False
        self.dragging = None



    # older Doodle code
    # I'm keeping it around in case I need it later
    def on_bufOff_mouseEnter(self, event):
        self.x, self.y = event.position

##    def on_bufOff_mouseDown(self, event):
##        self.x, self.y = event.position
##        event.target.drawLine((self.x, self.y), (self.x + 1, self.y + 1))
##
##    def on_bufOff_mouseDrag(self, event):
##        x, y = event.position
##        event.target.drawLine((self.x, self.y), (x, y))
##        self.x = x
##        self.y = y

    def on_btnColor_mouseClick(self, event):
        result = dialog.colorDialog(self, color=self.color)
        if result.accepted:
            #self.components.bufOff.foregroundColor = result.color
            event.target.backgroundColor = result.color
            self.color = result.color

    def openFile(self):
        result = dialog.openFileDialog(None, "Import which file?")
        if result.accepted:
            path = result.paths[0]
            os.chdir(os.path.dirname(path))
            self.filename = path
            bmp = graphic.Bitmap(self.filename)
            self.components.bufOff.drawBitmap(bmp, (0, 0))

    def on_menuFileOpen_select(self, event):
        self.openFile()

    def on_menuFileSaveAs_select(self, event):
        if self.filename is None:
            path = ''
            filename = ''
        else:
            path, filename = os.path.split(self.filename)
        result = dialog.saveFileDialog(None, "Save As", path, filename)
        if result.accepted:
            path = result.paths[0]
            fileType = graphic.bitmapType(path)
            print fileType, path
            try:
                bmp = self.components.bufOff.getBitmap()
                bmp.SaveFile(path, fileType)
                return 1
            except IOError:
                return 0
        else:
            return 0

    def on_menuEditCopy_select(self, event):
        clipboard.setClipboard(self.components.bufOff.getBitmap())

    def on_menuEditPaste_select(self, event):
        bmp = clipboard.getClipboard()
        if isinstance(bmp, wx.Bitmap):
            self.components.bufOff.drawBitmap(bmp)

    def on_editClear_command(self, event):
        self.components.bufOff.clear()


if __name__ == '__main__':
    app = model.Application(Gravity)
    app.MainLoop()
