#!/usr/bin/python

"""
KEA notes to myself

__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2005/09/18 03:59:22 $"
__author__ = "Kevin Altis <altis@semi-retired.com>"

"""

from PythonCard import dialog, model
import os
import inspect
import wx

BORDER = 5
RESIZE_LEFT = 1
RESIZE_RIGHT = 2
DRAG_X = 3
RESIZE_TOP = 4
RESIZE_BOTTOM = 5
DRAG_Y = 6

class WidgetsTest(model.PageBackground):
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
        print "on_chkVisible_mouseClick"
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


    # KEA 2002-05-07
    # some methods to build up component documentation
    # using the built-in component specs

    def getAttributesList(self, attributes):
        names = [a for a in attributes]
        names.sort()
        listX = []
        for n in names:
            if attributes[n].hasDefaultValueList():
                listX.append([n, attributes[n].getDefaultValueList()])
            else:
                value = attributes[n].getDefaultValue()
                if value == '':
                    value = "''"
                listX.append([n, value])
        return listX

    def getEventsList(self, spec):
        events = [e.name for e in spec.getEvents()]
        events.sort()
        return events

    def getMethodsList(self, object):
        listX = []
        methods = inspect.getmembers(object, inspect.ismethod)
        for m in methods:
            if m[0][0] in "abcdefghijklmnopqrstuvwxyz":
                listX.append(m[0])
        return listX

    def on_menuFileDumpWidgets_select(self, event):
        self.dumpDocs()

    def dumpDocs(self):
        #try:
        result = dialog.directoryDialog(None, 'Create widgets_documention in:', '')
        if result.accepted:
            widgetsDir = result.path
        else:
            return
        widgetsDir = os.path.join(widgetsDir, 'components')
        if not os.path.exists(widgetsDir):
            os.mkdir(widgetsDir)
        imagesDir = os.path.join(widgetsDir, 'images')
        if not os.path.exists(imagesDir):
            os.mkdir(imagesDir)

        toc = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'
        toc += '<html>\n<head><title>%s</title></head><body>\n' % 'PythonCard Components'
        toc += '<h1>PythonCard Components</h1>\n'
        componentsList = []

        for w in self.components.itervalues():
            if w.__class__.__name__.startswith(w.name[3:]):
                # document each widget
                name = w.__class__.__name__
                spec = w._spec

                doc = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'
                doc += '<html>\n<head><title>%s</title></head><body>\n' % (name + ': PythonCard component')
                doc += '<h1>Component: %s</h1>' % name

                doc += '\n<img src="%s"><BR>\n' % ('images/' + name + '.png')

                doc += '\n<h2>Required Attributes</h2>\n'
                doc += '<table border="1">\n'
                doc += '<tr><td><b>Name<b></td><td><b>Default value</b></td></tr>\n'
                for a in self.getAttributesList(spec.getRequiredAttributes()):
                    doc += "<tr><td>%s</td><td>%s</td></tr>\n" % (a[0], a[1])
                doc += '</table>'

                doc += '\n\n<h2>Optional Attributes</h2>\n'
                doc += '<table border="1">\n'
                doc += '<tr><td><b>Name<b></td><td><b>Default value</b></td></tr>\n'
                for a in self.getAttributesList(spec.getOptionalAttributes()):
                    doc += "<tr><td>%s</td><td>%s</td></tr>\n" % (a[0], a[1])
                doc += '</table>'

                doc += '\n\n<h2>Events:</h2>\n'
                doc += '<table border="1">\n'
                for e in self.getEventsList(spec):
                    doc += "<tr><td>%s</td></tr>\n" % e
                doc += '</table>'

                doc += '\n\n<h2>Methods:</h2>\n'
                doc += '<table border="1">\n'
                td = '<td><b>%s</b></td>' * 4
                tr = '<tr>' + td + '</tr>\n'
                doc += tr % ('method', 'args', 'doc string', 'comments')
                for e in self.getMethodsList(w):
                    method = getattr(w, e)
                    docstring = inspect.getdoc(method)
                    if docstring is None:
                        docstring = "&nbsp;"
                    comments = inspect.getcomments(method)
                    if comments is None:
                        comments = "&nbsp;"
                    #source = inspect.getcomments(method)
                    argspec = inspect.getargspec(method)
                    formattedargs = inspect.formatargspec(argspec[0], argspec[1], argspec[2], argspec[3])
                    doc += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n" % \
                        (e, formattedargs, docstring, comments)
                doc += '</table>'

                # need to decide what we want to dump from the methods
                # we probably don't want to dump everything including
                # wxPython methods, so this is where we need to decide
                # on the case of the first letter of the method
                # whatever is done here should be the same thing used
                # to display methods in the shell
                # arg lists and tooltips (docstrings) will be used here too

                # write out the documentation for the component
                doc += '\n<hr><img src="http://sourceforge.net/sflogo.php?group_id=19015&type=1" width="88" height="31" border="0" alt="SourceForge Logo">'
                doc += '\n</body>\n</html>'
                filename = name + '.html'
                path = os.path.join(widgetsDir, filename)
                f = open(path, 'w')
                f.write(doc)
                f.close()

                # create an image using the actual component
                # on screen
                # comment this out once you have created the images
                # you want
                bmp = wx.EmptyBitmap(w.size[0], w.size[1])
                memdc = wx.MemoryDC()
                memdc.SelectObject(bmp)
                dc = wx.WindowDC(w)
                memdc.BlitPointSize((0, 0), w.size, dc, (0, 0))
                imgfilename = os.path.join(imagesDir, name + '.png')
                bmp.SaveFile(imgfilename, wx.BITMAP_TYPE_PNG)
                dc = None
                memdc.SelectObject(wx.NullBitmap)
                memdc = None
                bmp = None

                componentsList.append('<a href="%s">%s</a><br>\n' % (filename, name))

        # now create the table of contents, index.html
        componentsList.sort()
        for c in componentsList:
            toc += c
        toc += '\n<hr><img src="http://sourceforge.net/sflogo.php?group_id=19015&type=1" width="88" height="31" border="0" alt="SourceForge Logo">'
        toc += '\n</body>\n</html>'
        filename = os.path.join(widgetsDir, 'index.html')
        f = open(filename, 'w')
        f.write(toc)
        f.close()

if __name__ == '__main__':
    app = model.Application(WidgetsTest)
    app.MainLoop()
