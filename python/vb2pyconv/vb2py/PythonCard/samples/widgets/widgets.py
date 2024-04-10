#!/usr/bin/python

"""
KEA notes to myself

__version__ = "$Revision: 1.45 $"
__date__ = "$Date: 2005/12/29 20:36:25 $"
__author__ = "Kevin Altis <altis@semi-retired.com>"

"""

from PythonCard import dialog, model

BORDER = 5
RESIZE_LEFT = 1
RESIZE_RIGHT = 2
DRAG_X = 3
RESIZE_TOP = 4
RESIZE_BOTTOM = 5
DRAG_Y = 6

class WidgetsTest(model.Background):
    """
    All the widgets that can be changed have a three-letter prefix followed
    by the actual classname to distinguish them from other widgets in the
    background.
    Compare the method of changing the attribute state in on_chkEnabled_mouseClick
    versus on_chkVisible_mouseClick. I'm using self.components.itervalues() 
    to iterate over a list of all the widgets at once.
    """

    def on_initialize(self, event):
        self.bitmapCanvasTest()

    def on_sldSlider_select(self, event):
        self.components.fldTextField.text = str(event.target.value)

    """
    def on_spnSpinner_spinUp(self, event):
        event.target.value = event.target.value + 1
        
    def on_spnSpinner_spinDown(self, event):
        event.target.value = event.target.value - 1
    """

    def bitmapCanvasTest(self):
        canvas = self.components.bmpBitmapCanvas
        canvas.drawPoint((5, 5))
        canvas.foregroundColor = 'red'
        canvas.drawLine((5, 10), (20, 30))
        canvas.foregroundColor = 'blue'
        canvas.drawRectangle((25, 5), (30, 20))
        canvas.drawText('Text', (5, 30))
        canvas.drawRotatedText('Rotated', (60, 40), 90)
        canvas.foregroundColor = 'gray'
        canvas.fillColor = 'gray'
        canvas.drawEllipse((80, 5), (30, 30))
        
    def on_chkEnabled_mouseClick(self, event):
        checked = event.target.checked
        for w in self.components.itervalues():
            # for btnButton, wType would be widget.Button
            # __class__ would be widget.Button
            # we can't use isinstance unless we put it in a try/except
            # block because isinstance requires a valid class as the
            # 2nd argument, so passing in "elTextField" or something like
            # that triggers an exception
            # KEA 2001-08-09
            # need a better way of getting the widget prefix dynamically
            # I've just gone soft in the head and can't see the right way here
            if w.__class__.__name__.startswith(w.name[3:]):
                w.enabled = checked
        self.components.fldTextFieldNoBorder.enabled = checked

    def on_chkVisible_mouseClick(self, event):
        checked = event.target.checked
        for w in self.components.itervalues():
            if w.__class__.__name__.startswith(w.name[3:]):
                w.visible = checked
        self.components.fldTextFieldNoBorder.visible = checked

    # editable only applies to TextField, PasswordField, and TextArea
    def on_chkEditable_mouseClick(self, event):
        checked = event.target.checked
        self.components.fldTextField.editable = checked
        self.components.fldPasswordField.editable = checked
        self.components.fldTextArea.editable = checked
        self.components.fldTextFieldNoBorder.editable = checked
        
    def on_btnBackgroundColor_mouseClick(self, event):
        result = dialog.colorDialog(self)
        if result.accepted:
            color = result.color
            for w in self.components.itervalues():
                if w.__class__.__name__.startswith(w.name[3:]):
                    w.backgroundColor = color
            self.components.fldTextFieldNoBorder.backgroundColor = color

    # compare this method of expliciting setting each component
    # one at a time compared to the for loop above
    def on_btnForegroundColor_mouseClick(self, event):
        result = dialog.colorDialog(self)
        if result.accepted:
            color = result.color
            # print color
            self.components.btnButton.foregroundColor = color
            self.components.fldTextField.foregroundColor = color
            self.components.fldPasswordField.foregroundColor = color
            self.components.fldTextArea.foregroundColor = color
            self.components.txtStaticText.foregroundColor = color
            self.components.chkCheckBox.foregroundColor = color
            self.components.chkToggleButton.foregroundColor = color
            self.components.radRadioGroup.foregroundColor = color
            self.components.popChoice.foregroundColor = color
            self.components.lstList.foregroundColor = color
            self.components.sldSlider.foregroundColor = color
            self.components.imgImage.foregroundColor = color
            self.components.imgImageButton.foregroundColor = color
            self.components.fldTextFieldNoBorder.foregroundColor = color
            self.components.calCalendar.foregroundColor = color
            self.components.cmbComboBox.foregroundColor = color
            self.components.gagGauge.foregroundColor = color
            self.components.spnSpinner.foregroundColor = color
            self.components.linStaticLine.foregroundColor = color
            self.components.stbStaticBox.foregroundColor = color

    def on_btnFont_mouseClick(self, event):
        result = dialog.fontDialog(self, self.components.btnButton.font)
        if result.accepted:
            #color = result.color
            font = result.font
            for w in self.components.itervalues():
                if w.__class__.__name__.startswith(w.name[3:]):
                    w.font = font
            self.components.fldTextFieldNoBorder.font = font

    def on_btnToolTip_mouseClick(self, event):
        result = dialog.textEntryDialog(self, 'Enter a toolTip:', 'ToolTip', 'Hello toolTip')
        if result.accepted:
            txt = result.text
            for w in self.components.itervalues():
                if w.__class__.__name__.startswith(w.name[3:]):
                    w.toolTip = txt

    def on_btnBgBackgroundColor_mouseClick(self, event):
        result = dialog.colorDialog(self)
        if result.accepted:
            color = result.color
            self.backgroundColor = color

    """
    experimental drag and resize code
    hold down the control key and mouseDown to drag a widget
    hold down the control key and mouseDown within 5 pixels of the edge
    of the widget to resize

    This seems to work okay on Windows, but not so well on Linux.
    My algorithm is probably not very good.
    """
    def on_mouseDown(self, event):
        global BORDER

        if event.controlDown:
            # record the starting location so, that the drags are
            # always relative and the widget won't jump around
            self.dragOffset = event.position
            xClick, yClick = self.dragOffset
            size = event.target.size
            rect = (0, 0, size[0] - BORDER, size[1] - BORDER)
            print rect
            print xClick, yClick
            if xClick < BORDER:
                print "resize left"
                self.xOp = RESIZE_LEFT
            elif xClick > rect[2]:
                print "resize right"
                self.xOp = RESIZE_RIGHT
            else:
                print "drag x"
                self.xOp = DRAG_X
            if yClick < BORDER:
                print "resize top"
                self.yOp = RESIZE_TOP
            elif yClick > rect[3]:
                print "resize bottom"
                self.yOp = RESIZE_BOTTOM
            else:
                print "drag y"
                self.yOp = DRAG_Y
        event.skip()

    def on_mouseDrag(self, event):
        target = event.target
        if event.controlDown:
            xPos, yPos = target.position
            width, height = target.size
            newWidth = width
            newHeight = height
            print "xPos %d, yPos %d" % (xPos, yPos)
            if self.xOp == DRAG_X and self.yOp == DRAG_Y:
                xOff = xPos + event.x - self.dragOffset[0]
                yOff = yPos + event.y - self.dragOffset[1]
                print "xOff %d, yOff %d" % (xOff, yOff)
                target.position = (xOff, yOff)
            else:
                xOff = xPos
                if self.xOp == RESIZE_LEFT:
                    # both width and the x position have to change
                    xOff = xPos + event.x - self.dragOffset[0]
                    newWidth = width + xPos - xOff #event.x + self.dragOffset[0]
                elif self.xOp == RESIZE_RIGHT:
                    # RESIZE_RIGHT
                    #newWidth += event.x - self.dragOffset[0]
                    #newWidth += 1
                    newWidth = event.x
                print "width %d, newWidth %d" % (width, newWidth)
                    
                yOff = yPos
                if self.yOp == RESIZE_TOP:
                    # both height and the y position have to change
                    yOff = yPos + event.y - self.dragOffset[1]
                    newHeight = height + yPos - yOff #event.y + self.dragOffset[1]
                elif self.yOp == RESIZE_BOTTOM:
                    # RESIZE_BOTTOM
                    #newHeight += event.y - self.dragOffset[1]
                    #newHeight += 1
                    newHeight = event.y
                print "height %d, newHeight %d" % (height, newHeight)
                    
                print "xOff %d, yOff %d" % (xOff, yOff)

                if xPos != xOff or yPos != yOff:
                    target.position = (xOff, yOff)
                if width != newWidth or height != newHeight:
                    #target._delegate.SetSize((width, height))
                    target.SetSize((newWidth, newHeight))
                #target._delegate.SetDimensions(xOff, yOff, newWidth, newHeight)                    
        event.skip()


    def on_menuFileDumpWidgets_select(self, event):
        self.dumpDocs()

    def dumpDocs(self):
        from PythonCard import documentation
        
        result = dialog.directoryDialog(None, 'Create documention in:', '')
        if result.accepted:
            widgetsDir = result.path
            documentation.dumpComponentDocs(self, widgetsDir)


if __name__ == '__main__':
    app = model.Application(WidgetsTest)
    app.MainLoop()
