#!/usr/bin/python
#
# projectmanager message output window
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright (C)2003 Phil Edwards, phil@linux2000.com
# vim: ts=4 sw=4 ai et

import string
import time
import sys

from PythonCard import model, dialog
import wx

class outputWindow(model.Background):

    def on_initialize(self, event):
        self.parent = self.GetParent()
        
    def clearLines(self):
        self.components.returnedText.text = ''
        self.components.importError.text = ''
        self.Refresh()
        wx.Yield()
        
    def addLine(self, text):
        if self.components.returnedText.enabled:
            self.components.returnedText.text += str(text)
        else:
            self.components.importError.text += str(text)
        #self.Refresh()
        #self.Update()
        #wx.Yield()
        
    def on_closeBtn_mouseClick(self, event):
        self.Hide()
        
    def on_close(self, event):
        self.Hide()
        
    def on_clipBoardBtn_mouseClick(self, event):
        if sys.platform.startswith('win'):
            stuff = wx.TextDataObject()
            stuff.SetText(self.components.clipBoardBtn.userdata)
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(stuff)
                wx.TheClipboard.Close()



if __name__ == '__main__':
    app = model.PythonCardApp(outputWindow)
    app.MainLoop()
