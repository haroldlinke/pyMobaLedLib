#!/usr/bin/python

"""
__version__ = "$Revision: 1.4 $"
__date__ = "$Date: 2005/09/18 03:59:22 $"
"""

"""
this is a direct port of the Java applet at
http://www.wordsmith.org/anu/java/spirograph.html
"""

from PythonCard import clipboard, dialog, graphic, model
import wx
import os
import random
import math

class Spirograph(model.Background):

    def on_initialize(self, event):
        self.filename = None
        comp = self.components
        self.sliderLabels = {
        'stcFixedCircleRadius':comp.stcFixedCircleRadius.text,
        'stcMovingCircleRadius':comp.stcMovingCircleRadius.text,
        'stcMovingCircleOffset':comp.stcMovingCircleOffset.text,
        'stcRevolutionsInRadians':comp.stcRevolutionsInRadians.text,
        }
        self.setSliderLabels()
        if self.components.chkDarkCanvas.checked:
            self.components.bufOff.backgroundColor = 'black'
            self.components.bufOff.clear()
        self.doSpirograph()

    def doSpirograph(self):
        comp = self.components
        
        canvas = comp.bufOff
        width, height = canvas.size
        xOffset = width / 2
        yOffset = height / 2

        R = comp.sldFixedCircleRadius.value
        r = comp.sldMovingCircleRadius.value
        O = comp.sldMovingCircleOffset.value
        revolutions = comp.sldRevolutionsInRadians.value
        
        color = comp.btnColor.backgroundColor
        canvas.foregroundColor = color

        canvas.autoRefresh = 0
        canvas.clear()
        
        if comp.radDrawingStyle.stringSelection == 'Lines':
            drawLines = 1
        else:
            drawLines = 0

        t = 0.0

        if R+r+O == 0:
            # avoid divide by zero errors
            s = 5.0/0.0000001
        else:
            s = 5.0/(R+r+O)
        rSum = R + r
        # avoid divide by zero errors
        if r == 0:
            r = 0.0000001
        exprResult = (rSum * t) / r
        lastX = rSum*math.cos(t) - O*math.cos(exprResult) + xOffset
        lastY = rSum*math.sin(t) - O*math.sin(exprResult) + yOffset
        self.keepDrawing = 1
        points = []
        while abs(t) <= revolutions:
            exprResult = (rSum * t) / r
            x = rSum*math.cos(t) - O*math.cos(exprResult) + xOffset
            y = rSum*math.sin(t) - O*math.sin(exprResult) + yOffset
            if drawLines:
                points.append((lastX, lastY, x, y))
                lastX = x
                lastY = y
            else:
                points.append((x, y))
            t += s

        if drawLines:
            canvas.drawLineList(points)
        else:
            canvas.drawPointList(points)
        canvas.autoRefresh = 1
        canvas.refresh()

    def on_btnColor_mouseClick(self, event):
        result = dialog.colorDialog(self)
        if result.accepted:
            self.components.bufOff.foregroundColor = result.color
            event.target.backgroundColor = result.color
            self.doSpirograph()

    def on_select(self, event):
        name = event.target.name
        # only process Sliders
        if name.startswith('sld'):
            labelName = 'stc' + name[3:]
            self.components[labelName].text = self.sliderLabels[labelName] + \
                ' ' + str(event.target.value)
        self.doSpirograph()

    def on_chkDarkCanvas_mouseClick(self, event):
        if event.target.checked:
            self.components.bufOff.backgroundColor = 'black'
        else:
            self.components.bufOff.backgroundColor = 'white'
        self.doSpirograph()

    def setSliderLabels(self):
        comp = self.components
        for key in self.sliderLabels:
            sliderName = 'sld' + key[3:]
            comp[key].text = self.sliderLabels[key] + ' ' + str(comp[sliderName].value)

    def on_btnRandom_mouseClick(self, event):
        comp = self.components
        comp.sldFixedCircleRadius.value = random.randint(1, 100)
        comp.sldMovingCircleRadius.value = random.randint(-50, 50)
        comp.sldMovingCircleOffset.value = random.randint(1, 100)
        self.setSliderLabels()
        self.doSpirograph()

    def openFile(self):
        wildcard = "All files (*.*)|*.*"
        result = dialog.openFileDialog(None, "Import which file?", '', '', wildcard)
        if result.accepted:
            path = result.paths[0]
            os.chdir(os.path.dirname(path))
            try:
                self.filename = path
                
                filename = os.path.splitext(os.path.basename(path))[0]
                if filename.startswith('spiro'):
                    items = filename[5:].split('_')
                    comp = self.components
                    comp.sldFixedCircleRadius.value = int(items[0])
                    comp.sldMovingCircleRadius.value = int(items[1])
                    comp.sldMovingCircleOffset.value = int(items[2])
                    comp.btnColor.backgroundColor = eval(items[3])
                    comp.chkDarkCanvas.checked = int(items[4])
                    if items[5] == 'L':
                        comp.radDrawingStyle.stringSelection = 'Lines'
                    else:
                        comp.radDrawingStyle.stringSelection = 'Points'
                    comp.sldRevolutionsInRadians.value = int(items[6])
                    self.setSliderLabels()
    
                    bmp = graphic.Bitmap(self.filename)
                    self.components.bufOff.drawBitmap(bmp, (0, 0))
            except IOError, msg:
                pass

    def on_menuFileOpen_select(self, event):
        self.openFile()

    def on_menuFileSaveAs_select(self, event):
        if self.filename is None:
            path = ''
            filename = ''
        else:
            path, filename = os.path.split(self.filename)
            
        comp = self.components
        style = comp.radDrawingStyle.stringSelection[0]
        filename = 'spiro' + str(comp.sldFixedCircleRadius.value) + '_' + \
            str(comp.sldMovingCircleRadius.value) + '_' + \
            str(comp.sldMovingCircleOffset.value) + '_' + \
            str(comp.btnColor.backgroundColor) + '_' + \
            str(comp.chkDarkCanvas.checked) + '_' + \
            style + '_' + \
            str(comp.sldRevolutionsInRadians.value) + \
            '.png'

        wildcard = "All files (*.*)|*.*"
        result = dialog.saveFileDialog(None, "Save As", path, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            fileType = graphic.bitmapType(path)
            try:
                bmp = self.components.bufOff.getBitmap()
                bmp.SaveFile(path, fileType)
                return True
            except IOError, msg:
                return False
        else:
            return False

    def on_menuEditCopy_select(self, event):
        clipboard.setClipboard(self.components.bufOff.getBitmap())

    def on_menuEditPaste_select(self, event):
        bmp = clipboard.getClipboard()
        if isinstance(bmp, wx.Bitmap):
            self.components.bufOff.drawBitmap(bmp)

    def on_editClear_command(self, event):
        self.components.bufOff.clear()


if __name__ == '__main__':
    app = model.Application(Spirograph)
    app.MainLoop()
