"""
__version__ = "$Revision: 1.6 $"
__date__ = "$Date: 2004/04/16 00:32:34 $"
"""

import wx

def getClipboard():
    data = None
    try:
        if wx.TheClipboard.Open():
            if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)):
                do = wx.TextDataObject()
                wx.TheClipboard.GetData(do)
                data = do.GetText()
            elif wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_BITMAP)):
                do = wx.BitmapDataObject()
                wx.TheClipboard.GetData(do)
                data = do.GetBitmap()
            wx.TheClipboard.Close()
    except:
        data = None
    return data

def setClipboard(data):
    try:
        if wx.TheClipboard.Open():
            if isinstance(data, str):
                do = wx.TextDataObject()
                do.SetText(data)
                wx.TheClipboard.SetData(do)
            elif isinstance(data, wx.Bitmap):
                do = wx.BitmapDataObject()
                do.SetBitmap(data)
                wx.TheClipboard.SetData(do)
            wx.TheClipboard.Close()
    except:
        pass
