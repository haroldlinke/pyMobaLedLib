
"""
__version__ = "$Revision: 1.47 $"
__date__ = "$Date: 2005/12/25 13:53:15 $"
"""

import wx
from PythonCard import event, font, graphic, widget

try:
    import Image
    # necessary to avoid name collision with Image class
    from Image import fromstring
    PIL_FOUND = True
except ImportError:
    PIL_FOUND = False

try:
    from Numeric import ArrayType
    NUMERIC_FOUND = True
except ImportError:
    NUMERIC_FOUND = False


class BitmapCanvasSpec(widget.WidgetSpec):
    def __init__(self):
        attributes = {
            'size' : { 'presence' : 'optional', 'default' : [ 50, 50 ] },
        }
        widget.WidgetSpec.__init__( self, 'BitmapCanvas', 'Widget', [], attributes )


# are NOR and NAND descriptions reversed?!
# double-check wxWidgets docs and/or wxPython source again
LogicalCopyModes = {
        "AND"           : wx.AND,           # src AND dst
        "AND_INVERT"    : wx.AND_INVERT,    # (NOT src) AND dst
        "AND_REVERSE"   : wx.AND_REVERSE,   # src AND (NOT dst)
        "CLEAR"         : wx.CLEAR,         # 0
        "COPY"          : wx.COPY,          # src
        "EQUIV"         : wx.EQUIV,         # (NOT src) XOR dst
        "INVERT"        : wx.INVERT,        # NOT dst
        "NAND"          : wx.NAND,          # (NOT src) OR (NOT dst)
        "NOR"           : wx.NOR,           # (NOT src) AND (NOT dst)
        "NO_OP"         : wx.NO_OP,         # dst
        "OR"            : wx.OR,            # src OR dst
        "OR_INVERT"     : wx.OR_INVERT,     # (NOT src) OR dst
        "OR_REVERSE"    : wx.OR_REVERSE,    # src OR (NOT dst)
        "SET"           : wx.SET,           # 1
        "SRC_INVERT"    : wx.SRC_INVERT,    # NOT src
        "XOR"           : wx.XOR,           # src XOR dst
        }

BrushFillStyleList = {
        "TRANSPARENT"    : wx.TRANSPARENT,
        "SOLID"          : wx.SOLID,
        "BDIAGONAL_HATCH": wx.BDIAGONAL_HATCH,
        "CROSSDIAG_HATCH" : wx.CROSSDIAG_HATCH,
        "FDIAGONAL_HATCH": wx.FDIAGONAL_HATCH,
        "CROSS_HATCH"     : wx.CROSS_HATCH,
        "HORIZONTAL_HATCH": wx.HORIZONTAL_HATCH,
        "VERTICAL_HATCH"  : wx.VERTICAL_HATCH
        }

class BitmapCanvas(widget.Widget, wx.Window):
    """
    A double-bufferd bitmap drawing area.
    """

    _spec = BitmapCanvasSpec()
    
    def __init__( self, aParent, aResource ) :
        self._thickness = 1
        self.autoRefresh = True
        self._drawingInProgress = False
        self._bufImage = None
       
        wx.Window.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id),
            aResource.position, 
            aResource.size,
            style = wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name                       
        )
        
        self._size = self.GetClientSize()
        
        # create offscreen buffer where drawing occurs
        bitmap = wx.EmptyBitmap(self._size[0], self._size[1])
        self._bufImage = wx.MemoryDC()
        self._bufImage.SelectObject(bitmap)
        del bitmap

        widget.Widget.__init__(self, aParent, aResource)
        
        wx.EVT_PAINT(self, self._onPaint)
        wx.EVT_SIZE(self, self._onSize)
        wx.EVT_WINDOW_DESTROY(self, self._onDestroy)

        self.backgroundColor = (255, 255, 255)  # 'white'
        self.clear()
        self._setForegroundColor((0,0,0))       # 'black'
        # these are the defaults for a new MemoryDC
        self._fillColor = 'WHITE'
        self._fillMode = 'SOLID'
        self._logicalCopyMode = 'COPY'

        self._bindEvents(event.WIDGET_EVENTS)

    def _onDestroy(self, event):
        # memory leak cleanup
        self._bufImage = None
        self._penColor = None
        self._pen = None
        event.Skip()

    def _getLogicalCopyMode(self):
        return self._logicalCopyMode
        
    def _setLogicalCopyMode(self, logicalCopyMode):
        self._bufImage.SetLogicalFunction(LogicalCopyModes[logicalCopyMode.upper()])

    def _getBackgroundColor(self):
        if self._bufImage is not None:
            brush = self._bufImage.GetBackground()
            return brush.GetColour()

    def _setBackgroundColor(self, aColor):
        aColor = self._getDefaultColor(aColor)
        if self._bufImage is not None:
            brush = self._bufImage.GetBackground()
            brush.SetColour(aColor)
            self._bufImage.SetBackground(brush)

    def _getFillColor(self):
        return self._fillColor

    def _setFillColor(self, aColor):
        aColor = self._getDefaultColor(aColor)
        if self._bufImage is not None:
            # KEA 2004-03-01
            # updated to work with wxPython 2.4.x
            # and wxPython 2.5.x
            # need to double-check other places copies of pen and brush
            # are manipulated in the rest of the framework and samples!!!
            nb = wx.Brush(aColor)
            ob = self._bufImage.GetBrush()
            if ob.Ok():
                nb.SetStyle(ob.GetStyle())
                s = ob.GetStipple()
                if s.Ok():
                    nb.SetStipple(s)
            self._bufImage.SetBrush(nb)

    def _getFillMode(self):
        return self._fillMode

    def _setFillMode(self, fillStyle):
        brush = self._bufImage.GetBrush()
        brush.SetStyle(BrushFillStyleList[fillStyle.upper()])
        self._bufImage.SetBrush(brush)

    def _getForegroundColor(self):
        return self._penColor

    def _setForegroundColor(self, aColor):
        aColor = self._getDefaultColor( aColor )
        self._penColor = aColor
        self._pen = wx.Pen(self._penColor, self._thickness, wx.SOLID)
        #self._pen.SetCap(wx.CAP_PROJECTING)
        if self._bufImage is not None:
            self._bufImage.SetPen(self._pen)
            self._bufImage.SetTextForeground(self._penColor)

    def _getThickness(self):
        return self._thickness

    def _setThickness(self, thickness):
        self._thickness = thickness
        self._pen = wx.Pen(self._penColor, self._thickness, wx.SOLID)
        if self._bufImage is not None:
            self._bufImage.SetPen(self._pen)

    def _getFont(self):
        if self._font is None:
            desc = font.fontDescription(self.GetFont())
            self._font = font.Font(desc)
        return self._font

    def _setFont(self, aFont):
        if isinstance(aFont, dict):
            aFont = font.Font(aFont, aParent=self)
        else: # Bind the font to this widget.
            aFont._parent = self
        self._font = aFont
        aWxFont = aFont._getFont()
        self._bufImage.SetFont(aWxFont)


    # when we Blit to the "window", we're actually blitting to the
    # offscreen bitmap and then that is blitted onscreen in the same
    # operation
    def blit(self, destXY, widthHeight, source, srcXY,
             logicalFunc=wx.COPY, useMask=False): #, xsrcMask=-1, ysrcMask=-1):
        self._bufImage.BlitPointSize(destXY, widthHeight, source, srcXY,
                            logicalFunc, useMask) #, xsrcMask, ysrcMask)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def clear(self):
        self._bufImage.Clear()
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    # this is poorly named, it should be DrawAxis
    def crossHair(self, xy):
        self._bufImage.CrossHairPoint(xy)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawArc(self, x1y1, x2y2, xcyc):
        """
        Draws an arc of a circle, centered on (xc, yc), with starting
        point (x1, y1) and ending at (x2, y2). The current pen is used
        for the outline and the current brush for filling the shape.

        The arc is drawn in an anticlockwise direction from the start
        point to the end point.
        """

        self._bufImage.DrawArcPoint(x1y1, x2y2, xcyc)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    # doesn't exist in wxMemoryDC
    #def DrawCheckMark(self, xy, widthHeight):
    #    self._bufImage.DrawCheckMark(xy, widthHeight)
    #    if self.autoRefresh: self.refresh()

    def drawBitmap(self, aBitmap, xy=(0, 0), transparency=1):
        if isinstance(aBitmap, graphic.Bitmap):
            bmp = aBitmap.getBits()
        elif isinstance(aBitmap, wx.Bitmap):
            bmp = aBitmap            
        elif isinstance(aBitmap, wx.Image):
            bmp = wx.BitmapFromImage(aBitmap)
        elif PIL_FOUND and isinstance(aBitmap, Image.Image):
            bmp = wx.BitmapFromImage(graphic.PILToImage(aBitmap))
        elif NUMERIC_FOUND and isinstance(aBitmap, ArrayType):
            bmp = wx.BitmapFromImage(graphic.numericArrayToImage(aBitmap))
        else:
            return

        self._bufImage.DrawBitmapPoint(bmp, xy, transparency)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawBitmapScaled(self, aBitmap, xy, size, transparency=1):
        if isinstance(aBitmap, graphic.Bitmap):
            img = wx.ImageFromBitmap(aBitmap.getBits())
        elif isinstance(aBitmap, wx.Bitmap):
            img = wx.ImageFromBitmap(aBitmap)
        elif isinstance(aBitmap, wx.Image):
            img = aBitmap
        elif PIL_FOUND and isinstance(aBitmap, Image.Image):
            img = graphic.PILToImage(aBitmap)
        elif NUMERIC_FOUND and isinstance(aBitmap, ArrayType):
            img = graphic.numericArrayToImage(aBitmap)
        else:
            return

        bmp = wx.BitmapFromImage(img.Scale(size[0], size[1]))
        self._bufImage.DrawBitmapPoint(bmp, xy, transparency)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawCircle(self, xy, radius):
        self._bufImage.DrawCirclePoint(xy, radius)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawEllipse(self, xy, widthHeight):
        self._bufImage.DrawEllipsePointSize(xy, widthHeight)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawEllipticArc(self, xy, widthHeight, startEnd):
        self._bufImage.DrawEllipticArcPointSize(xy, widthHeight, startEnd)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawIcon(self, aIcon, xy):
        self._bufImage.DrawIconPoint(aIcon, xy)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawLine(self, startXY, endXY):
        self._bufImage.DrawLinePoint(startXY, endXY)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawLines(self, pointsList):
        self._bufImage.DrawLines(pointsList)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawPoint(self, xy):
        self._bufImage.DrawPointPoint(xy)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawPolygon(self, pointsList):
        self._bufImage.DrawPolygon(pointsList)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawRectangle(self, xy, widthHeight):
        self._bufImage.DrawRectanglePointSize(xy, widthHeight)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawPointList(self, points, pens=None):
        self._bufImage.DrawPointList(points, pens)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    # KEA 2003-03-14
    # need to add other DrawXXXList methods once we are
    # requiring wxPython 2.4.0.6 or higher
    def drawRectangleList(self, rects, pens=None, brushes=None):
        self._bufImage.DrawRectangleList(rects, pens, brushes)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawRotatedText(self, aString, xy, angle):
        self._bufImage.DrawRotatedTextPoint(aString, xy, angle)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawRoundedRectangle(self, xy, widthHeight, radius):
        self._bufImage.DrawRoundedRectanglePointSize(xy, widthHeight, radius)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawSpline(self, pointsList):
        self._bufImage.DrawSpline(pointsList)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawLineList(self, lines, pens=None):
        self._bufImage.DrawLineList(lines, pens)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def drawText(self, aString, xy):
        self._bufImage.DrawTextPoint(aString, xy)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    # KEA 2002-03-31 this doesn't seem to work
    def floodFill(self, xy, colour, style=wx.FLOOD_SURFACE):
        self._bufImage.FloodFillPoint(xy, colour, style)
        if self.autoRefresh:
            dc = wx.ClientDC(self)
            dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))

    def getPixel(self, xy):
        return self._bufImage.GetPixelPoint(xy)

    def getTextExtent(self, aString):
        return self._bufImage.GetTextExtent(aString)

    def getFullTextExtent(self, aString):
        return self._bufImage.GetFullTextExtent(aString)

    def refresh(self, enableAutoRefresh=False):
        if enableAutoRefresh:
            self.autoRefresh = True
        dc = wx.ClientDC(self)
        dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))
        # KEA 2005-03-26
        # this is necessary to force a screen update on the Mac
        if wx.Platform == '__WXMAC__':
            #self.canvas.Refresh()
            self.Update()


    def _onPaint(self, evt):
        #starttime = time.time()
        rect = self.GetUpdateRegion().GetBox()
        #print "OnPaint", rect
        dc = wx.PaintDC(self)
        #dc.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))
        dc.BlitPointSize((rect[0], rect[1]), (rect[2], rect[3]), self._bufImage, (rect[0], rect[1]))
        #stoptime = time.time()
        #elapsed = stoptime - starttime
        #print "OnPaint time: %f seconds" % (elapsed)

    def resizeBuffer(self, size):
        brush = self._bufImage.GetBackground()
        bitmap = wx.EmptyBitmap(size[0], size[1])
        _bufImage = wx.MemoryDC()
        _bufImage.SelectObject(bitmap)
        del bitmap
        _bufImage.SetBackground(brush)
        _bufImage.SetPen(self._pen)
        aWxFont = self._getFont()._getFont()
        _bufImage.SetFont(aWxFont)
        _bufImage.SetTextForeground(self._penColor)
        _bufImage.Clear()
        _bufImage.BlitPointSize((0, 0), (self._size[0], self._size[1]), self._bufImage, (0, 0))
        
        self._size = size

        #self._bufImage.SelectObject(wx.NullBitmap)
        self._bufImage = _bufImage

    # need to copy the old bitmap
    # before resizing
    # plus the various pen attributes
    # there is probably a memory leak in the code below
    def _onSize(self, evt):
        size = self.GetClientSizeTuple()
        #print "OnSize", size, self._size
        if size == (0, 0) or not self._pen.GetColour().Ok():
            evt.Skip()
            return

        try:
            # in case self._bufImage hasn't been initialized
            brush = self._bufImage.GetBackground()
        except:
            evt.Skip()
            return

        # KEA 2002-03-30
        # only resize the offscreen bitmap when the onscreen window gets
        # larger than the offscreen bitmap
        #minX = min(size[0], self._size[0])
        #minY = min(size[1], self._size[1])
        maxX = max(size[0], self._size[0])
        maxY = max(size[1], self._size[1])
        #print minX, minY, maxX, maxY
        if (self._size[0] < maxX) or (self._size[1] < maxY):
            self.resizeBuffer((maxX, maxY))
            evt.Skip()

    def getBitmap(self, xy=(0, 0), widthHeight=(-1, -1)):
        w, h = self.GetClientSizeTuple()
        if widthHeight[0] != -1:
            w = widthHeight[0]
        if widthHeight[1] != -1:
            h = widthHeight[1]
        memory = wx.MemoryDC()
        bitmap = wx.EmptyBitmap(w, h)
        memory.SelectObject(bitmap)
        memory.BlitPointSize((0, 0), (w, h), self._bufImage, xy)
        memory.SelectObject(wx.NullBitmap)
        return bitmap

    backgroundColor = property(_getBackgroundColor, _setBackgroundColor)
    fillColor = property(_getFillColor, _setFillColor)
    fillMode = property(_getFillMode, _setFillMode)
    font = property(_getFont, _setFont)
    foregroundColor = property(_getForegroundColor, _setForegroundColor)
    logicalCopyMode = property(_getLogicalCopyMode, _setLogicalCopyMode)
    thickness = property(_getThickness, _setThickness)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].BitmapCanvas)

