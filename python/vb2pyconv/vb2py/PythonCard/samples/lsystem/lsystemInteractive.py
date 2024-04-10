#!/usr/bin/python

"""
A fractal display program using the Lindenmayer rule system to describe the fractal.
"""
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2005/12/13 11:13:23 $"

from PythonCard import clipboard, dialog, graphic, model
from PythonCard.turtle import AbstractTurtle, BitmapTurtle
import wx
import os
import time
import lsystem

class LSystem(lsystem.LSystem):

    def on_initialize(self, event):
        self.filename = None
        #self.on_iterations_select(None)
        #self.on_angle_select(None)
        self.components.iterationDisplay.text = \
            str(self.components.iterations.value)
        self.components.angleDisplay.text = \
            str(self.components.angle.value)
        self.on_Render_command(None)
    
    # depending on the complexity of the pattern string
    # my system becomes pretty unresponsive above 6 or 7 iterations
    
    def on_iterations_select(self, event):
        self.components.iterationDisplay.text = \
            str(self.components.iterations.value)
        self.components.iterationDisplay.redraw()
        self.on_Render_command(None)
    
    def on_angle_select(self, event):
        self.components.angleDisplay.text = \
            str(self.components.angle.value)
        self.components.angleDisplay.redraw()
        self.on_Render_command(None)
    
    def on_angleDisplay_textUpdate(self, event):
        # how do we want to validate here
        # just use a try/except block?
        try:
            self.components.angle.value = \
                int(self.components.angleDisplay.text)
            self.on_Render_command(None)
        except ValueError:
            pass

##    # this seemed like a good idea, but you tend to press Render so it isn't needed
##    def on_scriptField_closeField(self, event):
##        self.on_Render_command(None)
                
    def on_Render_command(self, event):
        self.statusBar.text = "Drawing, please wait..."
        starttime = time.time()

        fractalString = self.expand(
                self.components.scriptField.text,
                self.components.iterations.value)
        borderWidth = 5.0 * 4
        angle = self.components.angle.value
        bounds = lsystem.drawAbstractFractal(
            fractalString,
            1,
            angle,
            (0,0))
        width, height = self.components.bufOff.size
        scale = min(
            (width - 2 * borderWidth) / (bounds[2]-bounds[0]),
            (height - 2 * borderWidth) / (bounds[3]-bounds[1]))
        startPos = (bounds[0] * -scale + borderWidth,
                    bounds[1] * -scale + borderWidth) 
##        self.components.bufOff.autoRefresh = True
        self.components.bufOff.autoRefresh = False
        self.drawFractal(
            fractalString,
            'blue',
            scale,
            angle,
            startPos)

        # the bufOff BitmapCanvas should always be 4x the size
        # of the onscreen BitmapCanvas so we have a simple
        # method to anti-alias the drawing
        # also need to add some padding around side, so I
        # multiplied borderWidth * 4 above
        bmp = self.components.bufOff.getBitmap()
        self.components.onscreen.drawBitmapScaled(bmp, (0, 0), self.components.onscreen.size)
        # not sure if this is needed to prevent a memory leak
        bmp = None
        
        stoptime = time.time()
        self.statusBar.text = "Draw time: %.2f seconds" % (stoptime - starttime)

    def drawFractal(self, aFractalString, color, legLength, angle, startPos):
        self.components.bufOff.clear()
        t = BitmapTurtle(self.components.bufOff)
        t.color(color)
        t.width(3)
        #t.setBackColor('black')
        t.cls()
        t.lt(90)
        t.moveTo(startPos[0], startPos[1])
##        bounds = list(startPos + startPos)
        for char in aFractalString:
            if char=='F':
                t.fd(legLength)
                curPos = t.getXY()
##                bounds[0] = min(bounds[0], curPos[0])
##                bounds[1] = min(bounds[1], curPos[1])
##                bounds[2] = max(bounds[2], curPos[0])
##                bounds[3] = max(bounds[3], curPos[1])
            elif char=='+':
                t.rt(angle)
            elif char=='-':
                t.lt(angle)
            elif char=='B':
                t.bk(legLength)
            elif char=='[':
                t.push()
            elif char==']':
                t.pop()
##        return bounds


if __name__ == '__main__':
    app = model.Application(LSystem)
    app.MainLoop()
