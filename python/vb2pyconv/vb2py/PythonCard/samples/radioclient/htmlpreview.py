#!/usr/bin/python

"""
__version__ = "$Revision: 1.9 $"
__date__ = "$Date: 2004/04/17 19:32:43 $"
"""

from PythonCard import model
import wx

class HtmlPreview(model.Background):

    def on_initialize(self, event):
        self.html = self.components.html
        self.html.SetRelatedFrame(self, "HTML Preview: %s")
        self.html.SetRelatedStatusBar(0)

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.html, 1, wx.EXPAND)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def on_close(self, event):
        self.visible = False
