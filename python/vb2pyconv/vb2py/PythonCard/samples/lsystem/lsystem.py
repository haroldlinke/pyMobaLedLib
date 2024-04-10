#!/usr/bin/python

"""
A fractal display program using the Lindenmayer rule system to describe the fractal.
"""
__version__ = "$Revision: 1.6 $"
__date__ = "$Date: 2005/12/13 11:13:23 $"

from PythonCard import clipboard, dialog, graphic, model
from PythonCard.turtle import AbstractTurtle, BitmapTurtle
import wx
import os
import time

class LSystem(model.Background):

    def on_initialize(self, event):
        self.filename = None
        self.on_iterations_select(None)
        self.on_angle_select(None)
    
    def on_iterations_select(self, event):
        self.components.iterationDisplay.text = \
            str(self.components.iterations.value)
    
    def on_angle_select(self, event):
        self.components.angleDisplay.text = \
            str(self.components.angle.value)
    
    def on_angleDisplay_textUpdate(self, event):
        self.components.angle.value = \
            int(self.components.angleDisplay.text)
        
    def on_Render_command(self, event):
        self.statusBar.text = "Drawing, please wait..."
        starttime = time.time()

        fractalString = self.expand(
                self.components.scriptField.text,
                self.components.iterations.value)
        borderWidth = 5.0
        angle = self.components.angle.value
        self.components.bufOff.autoRefresh = False
        bounds = drawAbstractFractal(
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
        self.components.bufOff.autoRefresh = True
        self.drawFractal(
            fractalString,
            'blue',
            scale,
            angle,
            startPos)

        stoptime = time.time()
        self.statusBar.text = "Draw time: %.2f seconds" % (stoptime - starttime)

    def drawFractal(self, aFractalString, color, legLength, angle, startPos):
        self.components.bufOff.clear()
        t = BitmapTurtle(self.components.bufOff)
        t.color(color)
        t.lt(90)
        t.moveTo(startPos[0], startPos[1])
        for char in aFractalString:
            if char=='F':
                t.fd(legLength)
            elif char=='B':
                t.bk(legLength)
            elif char=='+':
                t.rt(angle)
            elif char=='-':
                t.lt(angle)
            elif char=='[':
                t.push()
            elif char==']':
                t.pop()
            
    def expand(self, fractalRules, iterations):
        lines = fractalRules.upper().split('\n')
        rules = {}
        for rule in lines:
            name, value = rule.split('=')
            assert(name=='AXIOM' or len(name)==1)
            rules[name] = value
        ret = rules['AXIOM']
        for i in range(iterations):
            l = list(ret)
            for pos, char in enumerate(l):
                repl = rules.get(char, None)
                if repl:
                    l[pos] = repl
            ret = ''.join(l)
        return ret
        
    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        comp = self.components
        flags = wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_BOTTOM
        # Mac wxButton needs 7 pixels on bottom and right
        macPadding = 7
        sizer1.Add(comp.btnColor, 0, flags, macPadding)
        sizer1.Add(comp.bufOff, 1, wx.EXPAND)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def on_btnColor_mouseClick(self, event):
        result = dialog.colorDialog(self)
        if result.accepted:
            self.components.bufOff.foregroundColor = result.color
            event.target.backgroundColor = result.color

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
            bmp = self.components.bufOff.getBitmap()
            try:
                bmp.SaveFile(path, fileType)
                return True
            except IOError:
                return False
        else:
            return False

    def on_menuEditCopy_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canCopy():
            widget.copy()
        else:
            clipboard.setClipboard(self.components.bufOff.getBitmap())

    def on_menuEditPaste_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canPaste():
            widget.paste()
        else:
            bmp = clipboard.getClipboard()
            if isinstance(bmp, wx.Bitmap):
                self.components.bufOff.drawBitmap(bmp)

    def on_editClear_command(self, event):
        self.components.bufOff.clear()

def drawAbstractFractal(aFractalString, legLength, angle, startPos):
    def recalcBounds(bounds, turtle):
        x, y = turtle.getXY()
        bounds[0] = min(bounds[0], x)
        bounds[1] = min(bounds[1], y)
        bounds[2] = max(bounds[2], x)
        bounds[3] = max(bounds[3], y)
        
    t = AbstractTurtle((1,1))
    t.lt(90)
    t.moveTo(startPos[0], startPos[1])
    bounds = list(startPos + startPos)
    for char in aFractalString:
        if char=='F':
            t.fd(legLength)
            recalcBounds(bounds, t)
        elif char=='B':
            t.bk(legLength)
            recalcBounds(bounds, t)
        elif char=='+':
            t.rt(angle)
        elif char=='-':
            t.lt(angle)
        elif char=='[':
            t.push()
        elif char==']':
            t.pop()
    return bounds

from PythonCard.tests import pyunit

class LSystemTests(pyunit.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testBoundsCheckBackwardMoves(self):
        bounds = drawAbstractFractal('BB+B', 1, 90, (10.0,20.0))
        # remember that down is positive in this coordinate system
        self.assertEqual([9.0, 20.0, 10.0, 22.0], bounds)
    def testBoundsCheckForwardMoves(self):
        bounds = drawAbstractFractal('FF-F', 1, 90, (10.0,20.0))
        # remember that down is positive in this coordinate system
        self.assertEqual([9.0, 18.0, 10.0, 20.0], bounds)

if __name__ == '__main__':
    app = model.Application(LSystem)
    app.MainLoop()
