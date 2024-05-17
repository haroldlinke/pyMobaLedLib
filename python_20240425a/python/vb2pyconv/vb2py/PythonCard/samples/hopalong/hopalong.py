#!/usr/bin/python

"""
__version__ = "$Revision: 1.28 $"
__date__ = "$Date: 2004/09/28 04:12:11 $"
"""

from PythonCard import model, util
import math
import wx


# from PIDDLE/SPING color spectrum test
def bluefunc(x):  return 1.0 / (1.0 + math.exp(-10*(x-0.6)))
def redfunc(x): return 1.0 / (1.0 + math.exp(10*(x-0.5)))
def greenfunc(x): return 1 - pow(redfunc(x+0.2),2) - bluefunc(x-0.3)
def genColors(n=100):
    out = [None]*n;
    for i in range(n):
        x = float(i)/n
        out[i] = (int(redfunc(x) * 255), int(greenfunc(x) * 255), int(bluefunc(x) * 255))
    return out


class Hopalong(model.Background):

    def on_initialize(self, event):
        self.drawing = False
        self.components.bufOff.backgroundColor = 'black'
        self.components.bufOff.clear()

        self.initSizers()

    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        comp = self.components
        stcFlags = wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTER
        fldFlags = wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER
        padding = 5
        # Mac wxButton needs 7 pixels on bottom and right
        macPadding = 7
        sizer2.Add(comp.stcA, 0, stcFlags, padding)
        sizer2.Add(comp.fldA, 0, fldFlags, padding)
        sizer2.Add(comp.stcB, 0, stcFlags, padding)
        sizer2.Add(comp.fldB, 0, fldFlags, padding)
        sizer2.Add(comp.stcC, 0, stcFlags, padding)
        sizer2.Add(comp.fldC, 0, fldFlags, padding)
        sizer2.Add(comp.stcIterations, 0, stcFlags, padding)
        sizer2.Add(comp.fldIterations, 0, fldFlags, padding)
        sizer2.Add(comp.stcXOffset, 0, stcFlags, padding)
        sizer2.Add(comp.fldXOffset, 0, fldFlags, padding)
        sizer2.Add(comp.stcYOffset, 0, stcFlags, padding)
        sizer2.Add(comp.fldYOffset, 0, fldFlags, padding)
        sizer2.Add(comp.stcScale, 0, stcFlags, padding)
        sizer2.Add(comp.fldScale, 0, fldFlags, padding)
        sizer2.Add(comp.stcColors, 0, stcFlags, padding)
        sizer2.Add(comp.fldColors, 0, fldFlags, padding)
        sizer2.Add((5, 5), 1)  # spacer
        sizer2.Add(comp.btnDraw, 0, fldFlags, macPadding)
        sizer2.Add(comp.btnCancel, 0, fldFlags, macPadding)
        sizer1.Add(sizer2, 0, wx.EXPAND)

        sizer1.Add(comp.bufOff, 1, wx.EXPAND)
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()


    def hopalong(self, a=30.0, b=1.0, c=0.9, iterations=100000,
                    xOffset=300.0, yOffset=300.0, scale=10.0, numColors=1000):

        x = 0.0
        y = 0.0

        colors = genColors(numColors)
        
        colorIter = iterations / len(colors)
        #print iterations, len(colors), colorIter
        
        sqrt = math.sqrt
        for i in range(len(colors)):
            points = []
            for j in range(colorIter):
                if x < 0:
                    temp = y + sqrt(abs(b * x - c))
                else:
                    temp = y - sqrt(abs(b * x - c))
                y = a - x
                x = temp
                points.append((xOffset + (x * scale), yOffset + (y * scale)))
            # to speed up drawing, we only update when the color changes
            yield (colors[i], points)

    def doHopalong(self):
        self.statusBar.text = "Drawing, please wait..."
        canvas = self.components.bufOff
        
        a = float(self.components.fldA.text)
        b = float(self.components.fldB.text)
        c = float(self.components.fldC.text)
        iterations = int(self.components.fldIterations.text)
        xOffset = float(self.components.fldXOffset.text)
        yOffset = float(self.components.fldYOffset.text)
        scale = float(self.components.fldScale.text)
        numColors = int(self.components.fldColors.text)
        
        totalPointsDrawn = 0
        starttime = util.time()

        canvas.clear()
        for color, points in self.hopalong(a, b, c, iterations, xOffset, yOffset, scale, numColors):
            canvas.foregroundColor = color
            canvas.drawPointList(points)
            totalPointsDrawn += len(points)
            wx.SafeYield(self)
            if not self.drawing:
                break
            
        elapsed = util.time() - starttime
        self.statusBar.text = "hopalong time: %f seconds (%d points drawn)" % (elapsed, totalPointsDrawn)
        self.drawing = False
        self.components.btnDraw.enabled = True
        self.components.btnCancel.enabled = False
        
    def on_btnDraw_mouseClick(self, event):
        self.drawing = True
        event.target.enabled = False
        self.components.btnCancel.enabled = True
        self.doHopalong()

    def on_btnCancel_mouseClick(self, event):
        self.drawing = False

    def on_editClear_command(self, event):
        self.components.bufOff.clear()

    def on_close(self, event):
        self.drawing = False
        event.skip()


if __name__ == '__main__':
    app = model.Application(Hopalong)
    app.MainLoop()
