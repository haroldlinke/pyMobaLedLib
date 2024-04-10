
"""
__version__ = "$Revision: 1.19 $"
__date__ = "$Date: 2004/08/11 01:58:03 $"
"""

import wx
from PythonCard import event, graphic, widget
import button, image


class ImageButtonSpec( widget.WidgetSpec ):
    def __init__(self):
        # KEA 2004-04-26
        # test to use new event classes
        events = [button.ButtonMouseClickEvent]
        #events = [ event.MouseClickEvent ]
        attributes = {
            'file' : { 'presence' : 'optional', 'default':'' },
            # KEA shouldn't there be a 'file' attribute here
            # could call it 'image' to match background above
            # but it is mandatory
            #'bitmap' : { 'presence' : 'optional', 'default' : None },
            # KEA kill border for now, until variations of what is possible are worked out
            # use ImageButton if you want images with transparent border
            # KEA since 3d is Windows specific, make transparent the default
            'border' : { 'presence' : 'optional', 'default' : 'transparent', 'values' : [ '3d', 'transparent', 'none' ] },
            'size' : { 'presence' : 'optional', 'default' : [ -1, -1 ] },
        }
        widget.WidgetSpec.__init__( self, 'ImageButton', 'Image', events, attributes )
        

class ImageButton(image.Image, wx.BitmapButton):
    """
    An image that plays the role of a button.
    """

    _spec = ImageButtonSpec()

    def __init__( self, aParent, aResource ) :
        self._border = aResource.border
        self._bitmap = graphic.Bitmap(aResource.file, aResource.size)
        self._file = aResource.file

        # KEA
        # should we modify aResource instead?
        # is aResource used again later?
        #print aResource.size
        self._size = tuple(aResource.size)
        w = aResource.size[0]
        if w == -2:
            w = self._bitmap.getWidth()
        h = aResource.size[1]
        if h == -2:
            h = self._bitmap.getHeight()
        size = (w, h)

        # KEA need to check all possible variations on Win32 and Linux
        if aResource.border == '3d':
            style = wx.BU_AUTODRAW   # Windows specific ?!
        else:
            style = 0

        wx.BitmapButton.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            self._bitmap.getBits(), 
            aResource.position, 
            size,
            style | wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name 
        )

        widget.Widget.__init__( self, aParent, aResource )

        wx.EVT_WINDOW_DESTROY(self, self._OnDestroy)

        # KEA 2001-07-27
        # we should only be binding this if the button
        # is supposed to be transparent
        # so maybe a setTransparent method with true/false parameter?
        # keep track of _transparent attribute and if _transparent
        # then unbind EVT_ERASE_BACKGROUND
        # before changing _transparent to false
        # same kind of thing for setTransparent
        # don't rebind events if not needed
        # getTransparent as well
        # setBorder/getBorder
        #print aResource.border
        if aResource.border == 'transparent':
            #print aResource.border
            wx.EVT_ERASE_BACKGROUND( self, lambda evt: None)

        #adapter = button.ButtonEventBinding(self)
        #adapter.bindEvents()
        self._bindEvents(event.WIDGET_EVENTS + (button.ButtonMouseClickEvent,))

    def _OnDestroy(self, event):
        # memory leak cleanup
        self._bitmap = None
        event.Skip()

    #def _setHelpText( self, aString ) :
    #    pass

    # KEA added getBitmap, setBitmap
    # KEA wxWindows uses a different set for wxStaticBitmap
    # so we have to override
    def _getBitmap( self ) :
        return self._bitmap

    # KEA
    # should something other than Refresh be used to force
    # a screen update?
    def _setBitmap( self, aValue ) :
        self._bitmap = aValue
        bmp = aValue.getBits()
        self.SetBitmapLabel(bmp)
        if wx.Platform != "__WXMSW__":
            self.SetBitmapDisabled(bmp)
            self.SetBitmapFocus(bmp)
            self.SetBitmapSelected(bmp)
        self.Refresh()

    def _getBorder( self ) :
        return self._border

    def _setBorder( self, aString ) :
        raise AttributeError, "border attribute is read-only"

    """
    # KEA do we query the Bitmap to find the actual dimensions
    # _size can contain -1, and -2
    # or provide a special getBitmapSize method?
    # this getSize is actually the same as its parent
    def _getSize( self ) :
        return self.GetSizeTuple()   # get the actual size, not (-1, -1)

    # KEA special handling for -2 size option
    def _setSize( self, aSize ):
        x = aSize[0]
        if x == -2:
            x = self._bitmap.getWidth()
        y = aSize[1]
        if y == -2:
            y = self._bitmap.getHeight()
        self.SetSize( ( x, y ) )
    """


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
    border = property(_getBorder, _setBorder)
    file = property(_getFile, _setFile)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].ImageButton)

