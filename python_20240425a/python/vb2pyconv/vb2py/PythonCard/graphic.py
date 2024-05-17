"""
__version__ = "$Revision: 1.18 $"
__date__ = "$Date: 2005/08/11 06:26:32 $"
"""

import os
import wx

try:
    import Image
    # necessary to avoid name collision with Image class
    from Image import fromstring
    PIL_FOUND = 1
except ImportError:
    PIL_FOUND = 0


def PILToImage(pilImage):
    if (pilImage.mode != 'RGB'):
        pilImage = pilImage.convert('RGB')
    imageData = pilImage.tostring('raw', 'RGB')
    img = wx.EmptyImage(pilImage.size[0], pilImage.size[1])
    img.SetData(imageData)
    return img

def PILToBitmap(image):
    return wx.BitmapFromImage(PILToImage(image))

def BitmapToPIL(bmp):
    imageData = wx.ImageFromBitmap(bmp).GetData()
    imagePIL = fromstring('RGB', (bmp.GetWidth(), bmp.GetHeight()), imageData)
    imagePIL = imagePIL.convert('RGB')
    return imagePIL

def numericArrayToImage(array):
    height, width = array.shape[:2]
    img = wx.EmptyImage(width, height)
    img.SetData(array.tostring())
    return img


def bitmapType(filename):
    """
    Get the type of an image from the file's extension ( .jpg, etc. )
    """

    if filename == '':
        return None

    name, ext = os.path.splitext(filename)
    ext = ext[1:].upper()
    if ext == 'BMP':
        return wx.BITMAP_TYPE_BMP
    elif ext == 'GIF':
        return wx.BITMAP_TYPE_GIF
    elif ext == 'JPG' or ext == 'JPEG':
        return wx.BITMAP_TYPE_JPEG
    elif ext == 'PCX':
        return wx.BITMAP_TYPE_PCX
    elif ext == 'PICT':
        return wx.BITMAP_TYPE_PICT
    elif ext == 'PNG':
        return wx.BITMAP_TYPE_PNG
    elif ext == 'PNM':
        return wx.BITMAP_TYPE_PNM
    elif ext == 'TIF' or ext == 'TIFF':
        return wx.BITMAP_TYPE_TIF
    elif ext == 'XBM':
        return wx.BITMAP_TYPE_XBM
    elif ext == 'XPM':
        return wx.BITMAP_TYPE_XPM
    else:
        # KEA 2001-10-10
        # rather than throw an exception, we could try and have wxPython figure out the image
        # type by returning wxBITMAP_TYPE_ANY
        raise 'invalid graphics format'    # should throw an exception here


def saveWindowScreenshot(w, path):
    bmp = wx.EmptyBitmap(w.size[0], w.size[1])
    memdc = wx.MemoryDC()
    memdc.SelectObject(bmp)
    dc = wx.WindowDC(w)
    memdc.BlitPointSize((0, 0), w.size, dc, (0, 0))
    bmp.SaveFile(path, bitmapType(path))
    dc = None
    memdc.SelectObject(wx.NullBitmap)
    memdc = None
    bmp = None


class Bitmap :

    def __init__(self, filename=None, size=(-1, -1)):
        if filename is None or filename == '':
            self._filename = None
        else:
            self._filename = filename
        # KEA 2004-07-27
        # Mac checks that the bitmap is Ok() so need
        # to use a valid size
        if (self._filename is None) and (tuple(size) == (-1, -1)):
            self._size = (10, 10)
        else:
            self._size = size
        self._type = None
        self.loadFile(self._filename, self._size)

    def getBits( self ) :
        return self._bits

    def setBits( self, aWxBitmap ) :
        self._bits = aWxBitmap

    def setPILBits(self, image):
        self._bits = PILToBitmap(image)

    def getPILBits(self):
        return BitmapToPIL(self._bits)

    def setImageBits(self, image):
        self._bits = wx.BitmapFromImage(image)

    def getImageBits(self):
        return wx.ImageFromBitmap(self._bits)

    def getHeight( self ) :
        return self._bits.GetHeight()

    def getWidth( self ) :
        return self._bits.GetWidth()

    def getSize( self ) :
        return (self._bits.GetWidth(), self._bits.GetHeight())

    # KEA special handling for -2 size option
    def setSize( self, aSize ):
        raise NotImplementedError

    def getType( self ) :
        return  self._type

    def _getBitmapType( self, filename ) :
        """
        Get the type of an image from the file's extension ( .jpg, etc. )
        """
        # KEA 2001-07-27
        # was
        #name, ext = filename.split( '.' )
        #ext = ext.upper()
        if filename is None or filename == '':
            return None

        name, ext = os.path.splitext(filename)
        ext = ext[1:].upper()
        if ext == 'BMP':
            return wx.BITMAP_TYPE_BMP
        elif ext == 'GIF':
            return wx.BITMAP_TYPE_GIF
        elif ext == 'JPG' or ext == 'JPEG':
            return wx.BITMAP_TYPE_JPEG
        elif ext == 'PCX':
            return wx.BITMAP_TYPE_PCX
        #elif ext == 'PICT':
        #    return wx.BITMAP_TYPE_PICT
        elif ext == 'PNG':
            return wx.BITMAP_TYPE_PNG
        elif ext == 'PNM':
            return wx.BITMAP_TYPE_PNM
        elif ext == 'TIF' or ext == 'TIFF':
            return wx.BITMAP_TYPE_TIF
        elif ext == 'XBM':
            return wx.BITMAP_TYPE_XBM
        elif ext == 'XPM':
            return wx.BITMAP_TYPE_XPM
        else:
            # KEA 2001-10-10
            # rather than throw an exception, we could try and have wxPython figure out the image
            # type by returning wxBITMAP_TYPE_ANY
            raise 'invalid graphics format'    # should throw an exception here

    # xbm format doesn't seem to work on Windows
    def loadFile(self, filename=None, size=(-1, -1)):
        if filename is None or filename == '':
            self._filename = None
        else:
            self._filename = filename
        if (self._filename is None) and (tuple(size) == (-1, -1)):
            self._size = (10, 10)
        else:
            self._size = size
        self._type = self._getBitmapType(self._filename)
        if self._type is None:
            self._bits = wx.EmptyBitmap(self._size[0], self._size[1])
        else:
            self._bits = wx.Bitmap(self._filename, self._type)

    # attempting to save a GIF image will result in a zero length file
    def saveFile(self, filename=None):
        if filename is None:
            filename = self._filename
        try:
            self._bits.SaveFile(filename, self._getBitmapType(filename))
        except:
            pass

    def rotate90(self, clockwise=1):
        image = wx.ImageFromBitmap(self._bits)
        self._bits = wx.BitmapFromImage(image.Rotate90(clockwise))
