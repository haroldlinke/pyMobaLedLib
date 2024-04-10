#!/usr/bin/python

"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2005/09/18 03:59:22 $"
"""

from PythonCard import clipboard, dialog, graphic, model
import wx
import os
import minimal
import doodle

# minimalist panel that works like PageBackground
# for testing purposes 
class MyPanel(wx.Panel):
    def __init__(self, aParent, size, name):
        wx.Panel.__init__(self, aParent,
                            -1, 
                            size=size,
                            name=name)
                            
        self.panel = wx.Panel(self, -1, 
            style=wx.TAB_TRAVERSAL | wx.NO_FULL_REPAINT_ON_RESIZE)
        
        self.field1 = wx.TextCtrl(self, -1, 'Hello World')

        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self._sizer.Add(self.panel, True, wx.EXPAND)
        self._sizer.Fit(self)
        self._sizer.SetSizeHints(self)
        self.SetSizer(self._sizer)
        self.Layout()

class TestSplitter(model.SplitterBackground):

    def on_initialize(self, event):
        # the splitter code is adapted from the wxPython demo Main.py
        
        # I was having to do RemoveChild with Background
        # but SplitterBackground seems okay
##        self.RemoveChild(self.panel)
##        self.panel = None

        splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)
        splitter2 = wx.SplitterWindow(splitter, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)
        self.splitter = splitter
        self.splitter2 = splitter2

        win1 = MyPanel(splitter, (100, 50), 'win1')
        #win1 = model.childWindow(splitter, doodle.Doodle)
        win1 = model.childWindow(splitter, minimal.Minimal)
        #win2 = model.childWindow(splitter, minimal.Minimal)
        #win2 = MyPanel(splitter, (100, 50), 'win2')
        win2 = model.childWindow(splitter2, doodle.Doodle)
        #win2 = model.childWindow(splitter2, minimal.Minimal)
        win3 = model.childWindow(splitter2, doodle.Doodle)

        self.win1 = win1
        self.win2 = win2
        self.win3 = win3
       
        # add the windows to the splitter and split it.
        splitter2.SplitHorizontally(win2, win3, 160)
        splitter.SplitVertically(win1, splitter2, 200)
        #splitter.SplitVertically(win1, win2, 150)

        splitter.SetMinimumPaneSize(20)
        splitter2.SetMinimumPaneSize(20)
        self.size = (600, 400)

        # Make the splitter on the right expand the top window when resized
        def SplitterOnSize(evt):
            splitter = evt.GetEventObject()
            sz = splitter.GetSize()
            splitter.SetSashPosition(sz.height - 160, False)
            evt.Skip()

        #splitter2.Bind(wx.EVT_SIZE, SplitterOnSize)



    """
    Doodle methods
    
    MAJOR UNRESOLVED ISSUES
    
    just like top-level event handlers and methods
    when dealing with a Notebook
    how do we want these kinds of methods to work with a SplitterBackground?
    if the event handlers and methods such as openFile are defined in the
    top-level parent then they will be found, but rather than references
    such as self.components.bufOff they would have to make specific
    references to the child such as self.win3.components.bufOff

    this makes sense from the standpoint that the associated menus
    also have to be specified in the top-level Background resource
    but it would seem to reduce reusability
    
    so could we and should we bind and dispatch events such that
    a child could add menus and menu items from its resource
    during the initLayout call or something like that?
    depending on the focus context, events would be directed
    at the appropriate child.
    i'm not even sure that is doable.
    
    needless to say the containers introduced with Notebook
    and SplitterBackground are making me worry about PythonCard
    becoming even more of a confusing hack job than it already is.
    """
    
    def openFile(self):
        win = self.findFocus()
        print win
        result = dialog.openFileDialog(None, "Import which file?")
        if result.accepted:
            path = result.paths[0]
            os.chdir(os.path.dirname(path))
            self.filename = path
            bmp = graphic.Bitmap(self.filename)
            #self.components.bufOff.drawBitmap(bmp, (0, 0))
            self.win3.components.bufOff.drawBitmap(bmp, (0, 0))

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
                #bmp = self.components.bufOff.getBitmap()
                bmp = self.win3.components.bufOff.getBitmap()
                bmp.SaveFile(path, fileType)
                return 1
            except Exception, msg: # Should check for a particular exception
                return 0
        else:
            return 0

    def on_menuEditCopy_select(self, event):
        #clipboard.setClipboard(self.components.bufOff.getBitmap())
        clipboard.setClipboard(self.win3.components.bufOff.getBitmap())

    def on_menuEditPaste_select(self, event):
        bmp = clipboard.getClipboard()
        if isinstance(bmp, wx.Bitmap):
            #self.components.bufOff.drawBitmap(bmp)
            self.win3.components.bufOff.drawBitmap(bmp)

    def on_editClear_command(self, event):
        #self.components.bufOff.clear()
        self.win3.components.bufOff.clear()


if __name__ == '__main__':
    app = model.Application(TestSplitter)
    app.MainLoop()
