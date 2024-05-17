#!/usr/bin/python

"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2005/09/18 03:59:22 $"
"""

from PythonCard import clipboard, dialog, graphic, model
import wx
import os

class Doodle(model.PageBackground):

    def on_initialize(self, event):
        self.x = 0
        self.y = 0
        self.filename = None
        
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

    def on_bufOff_mouseEnter(self, event):
        self.x, self.y = event.position

    def on_bufOff_mouseDown(self, event):
        self.x, self.y = event.position
        event.target.drawLine((self.x, self.y), (self.x + 1, self.y + 1))

    def on_bufOff_mouseDrag(self, event):
        x, y = event.position
        event.target.drawLine((self.x, self.y), (x, y))
        self.x = x
        self.y = y

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
            try:
                bmp = self.components.bufOff.getBitmap()
                bmp.SaveFile(path, fileType)
                return 1
            except IOError, msg:
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
    app = model.Application(Doodle)
    app.MainLoop()
