
"""
__version__ = "$Revision: 1.24 $"
__date__ = "$Date: 2004/08/11 01:58:03 $"
"""

import wx
from PythonCard import event, graphic, widget

USE_GENERIC = wx.Platform == '__WXGTK__'

if USE_GENERIC:
    from wx.lib.statbmp import GenStaticBitmap as StaticBitmap
else:
    StaticBitmap = wx.StaticBitmap

class ImageSpec(widget.WidgetSpec):
    def __init__(self):
        events = []
        attributes = {
            'file' : { 'presence' : 'optional', 'default':'' },
            # KEA shouldn't there be a 'file' attribute here
            # could call it 'image' to match background above
            # but it is mandatory
            #'bitmap' : { 'presence' : 'optional', 'default' : None },
            # KEA kill border for now, until variations of what is possible are worked out
            # use ImageButton if you want images with transparent border
            #'border' : { 'presence' : 'optional', 'default' : '3d', 'values' : [ '3d', 'transparent', 'none' ] },
            'size' : { 'presence' : 'optional', 'default' : [ -1, -1 ] },
        }
        widget.WidgetSpec.__init__( self, 'Image', 'Widget', events, attributes )
        

class Image(widget.Widget, StaticBitmap):
    """
    A static image.
    """

    _spec = ImageSpec()

    def __init__(self, aParent, aResource):
        self._bitmap = graphic.Bitmap(aResource.file, aResource.size)
        self._file = aResource.file

        self._size = tuple(aResource.size)
        w = aResource.size[0]
        if w == -2:
            w = self._bitmap.getWidth()
        h = aResource.size[1]
        if h == -2:
            h = self._bitmap.getHeight()
        size = (w, h)
        #size = wx.Size( self._bitmap.GetWidth(), self._bitmap.GetHeight() )

        ##if aResource.border == 'transparent':
        ##    mask = wx.MaskColour(self._bitmap, wxBLACK)
        ##    self._bitmap.SetMask(mask)

        StaticBitmap.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id),
            self._bitmap.getBits(), 
            aResource.position, 
            size,
            style = wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name
            )

        widget.Widget.__init__( self, aParent, aResource )

        wx.EVT_WINDOW_DESTROY(self, self._OnDestroy)
        
        self._bindEvents(event.WIDGET_EVENTS)

    def _OnDestroy(self, event):
        # memory leak cleanup
        self._bitmap = None
        event.Skip()

    # KEA added getBitmap, setBitmap
    def _getBitmap( self ) :
        return self._bitmap

    def _setBitmap( self, aValue ) :
        self._bitmap = aValue
        self.SetBitmap( aValue.getBits() )
        # may actually need to refresh the panel as well
        # depending on the size of the new bitmap compared
        # to the old one
        # in addition, the size of the image or imagebutton needs
        # to be set appropriately after changing the bitmap so
        # there are still a few issues to work out
        self.Refresh()

    """
    # KEA do we query the Bitmap to find the actual dimensions
    # _size can contain -1, and -2
    # or provide a special getBitmapSize method?
    # this getSize is actually the same as its parent
    def _getSize( self ) :
        return self.GetSizeTuple()   # get the actual size, not (-1, -1)
    """

    # KEA special handling for -2 size option
    def _setSize(self, aSize):
        self._size = tuple(aSize)
        w = aSize[0]
        if w == -2:
            w = self._bitmap.getWidth()
        h = aSize[1]
        if h == -2:
            h = self._bitmap.getHeight()
        self.SetSize((w, h))

    # KEA 2001-08-02
    # right now the image is loaded from a filename
    # during initialization
    # but later these might not make any sense
    # if setBitmap is used directly in user code
    def _getFile( self ) :
        return self._file

    # KEA 2001-08-14
    # if we're going to support setting the file
    # after initialization, then this will need to handle the bitmap loading
    # overhead
    def _setFile( self, aFile ) :
        self._file = aFile
        self._setBitmap(graphic.Bitmap(aFile))

    def _setBackgroundColor( self, aColor ) :
        aColor = self._getDefaultColor( aColor )
        if self._file == '':
            bmp = self._bitmap.getBits()
            dc = wx.MemoryDC()
            dc.SelectObject(bmp)
            dc.SetBackground(wx.Brush(aColor))
            dc.Clear()
            dc.SelectObject(wx.NullBitmap)
        self.SetBackgroundColour( aColor )
        self.Refresh()   # KEA wxPython bug?

    backgroundColor = property(widget.Widget._getBackgroundColor, _setBackgroundColor)
    bitmap = property(_getBitmap, _setBitmap)
    file = property(_getFile, _setFile)
    size = property(widget.Widget._getSize, _setSize)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].Image)
