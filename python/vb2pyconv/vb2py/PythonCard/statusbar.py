
"""
__version__ = "$Revision: 1.13 $"
__date__ = "$Date: 2004/07/17 17:20:10 $"
"""

import wx

class StatusBar(wx.StatusBar):
    """
    A simple StatusBar with a single text field.
    """
    
    def __init__(self, parent):
        # only display the resizing grip if the window is resizable
        # the logic below is used because it appears different
        # default flags are used on different platforms
        if not (parent.GetWindowStyle() & wx.RESIZE_BORDER):
            wx.StatusBar.__init__(self, parent, wx.NewId(), 0)
        else:
            wx.StatusBar.__init__(self, parent)
        if wx.Platform == '__WXMAC__':
            self.SetSize((self.GetSizeTuple()[0], 15))

    text = property(wx.StatusBar.GetStatusText, wx.StatusBar.SetStatusText, doc="text displayed in the statusBar")
