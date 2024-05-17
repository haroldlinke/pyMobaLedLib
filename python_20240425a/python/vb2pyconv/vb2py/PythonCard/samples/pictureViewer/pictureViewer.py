#!/usr/bin/python

"""
__version__ = "$Revision: 1.25 $"
__date__ = "$Date: 2005/12/13 11:13:24 $"
"""

from PythonCard import clipboard, dialog, graphic, log, model
import wx
import os, sys
from PythonCard import EXIF

class PictureViewer(model.Background):

    def on_initialize(self, event):
        # only respond to size events the user generates
        # I'm not sure of a better way to do this than an IDLE
        # hack
        self.ignoreSizeEvent = 1

        self.x = 0
        self.y = 0
        self.filename = None
        self.bmp = None

        # figure out the maximum usable window size
        # size we can use without overlapping
        # the taskbar
        bgSize = self.size
        bufSize = self.GetClientSize()
        widthDiff = bgSize[0] - bufSize[0]
        heightDiff = bgSize[1] - bufSize[1]
        displayRect = wx.GetClientDisplayRect()
        self.maximizePosition = (displayRect[0], displayRect[1])
        self.maximumSize = (displayRect[2] - widthDiff, displayRect[3] - heightDiff)

        #self.initSizers()
        if len(sys.argv) > 1:
            # accept a file argument on the command-line
            filename = os.path.abspath(sys.argv[1])
            log.info('pictureViewer filename: ' + filename)
            if not os.path.exists(filename):
                filename = os.path.abspath(os.path.join(self.application.startingDirectory, sys.argv[1]))
            #print filename
            if os.path.isfile(filename):
                self.openFile(filename)

        if self.filename is None:
            self.fitWindow()

        self.visible = True

    def on_idle(self, event):
        self.ignoreSizeEvent = 0

    # this breaks when restoring from a minimized (iconized) state
    # the self.normalSize flag fixed the minimize problem
    def on_size(self, event):
        if self.bmp is not None and not self.ignoreSizeEvent:
            #print "on_size", self.components.bufOff.size, self.panel.GetSizeTuple(), \
            #    self.GetClientSize(), self.getSize(), event.GetSize()
            oldSize = self.bmp.getSize()
            newSize = self.GetClientSize()
            widthScale = newSize[0] / (0.0 + oldSize[0])
            heightScale = newSize[1] /(0.0 + oldSize[1])
            #print "old new", oldSize, newSize, widthScale, heightScale
            self.displayFileScaled(widthScale, heightScale, 1)

    def sizeScaled(self, size, widthScale, heightScale):
        return ((int(size[0] * widthScale), int(size[1] * heightScale)))

    def displayFileScaled(self, widthScale, heightScale, inUserResize=0):
        if self.filename is not None:
            bufOff = self.components.bufOff
            bufOff.autoRefresh = 0

            # figure out new size for window
            size = self.bmp.getSize()
            newSize = self.sizeScaled(size, widthScale, heightScale)
            bufOff.size = newSize

            if inUserResize:
                self.panel.SetSize(newSize)
            else:
                self.fitWindow()
            bufOff.clear()
    
            bufOff.autoRefresh = 1
            bufOff.drawBitmapScaled(self.bmp, (0, 0), newSize)

    # attempt to display the file full size if possible
    # otherwise the bitmap needs to be scaled
    def displayFile(self):
        if self.filename is not None:
            bufOff = self.components.bufOff
            bufOff.autoRefresh = 0
            # figure out new size for window
            bufOff.size = self.bmp.getSize()
            # is there a better way to resize the window?
            ##self.panel.Fit()
            ##self.Fit()
            self.fitWindow()
            bufOff.clear()
    
            bufOff.autoRefresh = 1
            bufOff.drawBitmap(self.bmp, (0, 0))

    def on_menuImageHalfSize_select(self, event):
        self.displayFileScaled(0.5, 0.5)

    def on_menuImageNormalSize_select(self, event):
        self.displayFile()

    def on_menuImageDoubleSize_select(self, event):
        self.displayFileScaled(2.0, 2.0)

    # could support true full screen as well
    # using ShowFullScreen
    def fitToScreen(self):
        oldSize = self.bmp.getSize()
        newSize = self.maximumSize
        widthScale = newSize[0] / (0.0 + oldSize[0])
        heightScale = newSize[1] /(0.0 + oldSize[1])
        scale = min(widthScale, heightScale)
        #print "fit", widthScale, heightScale, scale
        self.displayFileScaled(scale, scale)
        #self.position = self.maximizePosition
        self.Center()
        # we could do self.Center(), but I think I like
        # it better on the top-left corner of the screen
        # which also prevents the bottom of the image from
        # having a few pixels chopped off
        # an alternative would be to reduce the maximum size
        # by 4 pixels or so

    def on_menuImageFillScreenSize_select(self, event):
        # figure out which dimension is the limiting factor
        # then scale to that limit
        if self.bmp is not None:
            self.fitToScreen()

    def on_menuImageScaleSize_select(self, event):
        result = dialog.textEntryDialog(self, "Scale by percent:", "Scale image", "")
        if result.accepted:
            try:
                scale = float(result.text) / 100.0
                self.displayFileScaled(scale, scale)
            except ValueError:
                pass

    def fitWindow(self):
        self.ignoreSizeEvent = 1
        size = self.components.bufOff.size
        self.panel.SetSize(size)
        #if self.ignoreSizeEvent == 1:
        self.SetClientSize(size)
        
    def openFile(self, path):
        #os.chdir(os.path.dirname(path))
        self.filename = path

        f = open(path, 'rb')
        tags=EXIF.process_file(f)
        f.close()
        if tags.has_key('Image Orientation'):
            # the repr() is something like
            # (0x0112) Short=8 @ 54
            # but the str() is just 1, 8, etc.
            orientation = int(str(tags['Image Orientation']))
            #print path
            #print 'Image Orientation: %d' % orientation
            #print 'Thumbnail Orientation: %s' % tags['Thumbnail Orientation']
        else:
            orientation = 1

        self.bmp = graphic.Bitmap(self.filename)
        if orientation == 8:
            # need to rotate the image
            # defaults to clockwise, 0 means counter-clockwise
            #print "rotating"
            self.bmp.rotate90(0)
        elif orientation == 6:
            self.bmp.rotate90(1)

        size = self.bmp.getSize()
        title = os.path.split(self.filename)[-1] + "  %d x %d" % size
        self.title = title
        # if either dimension of the image is beyond our maximum
        # then display the image fit to the screen
        if size[0] > self.maximumSize[0] or size[1] > self.maximumSize[1]:
            self.fitToScreen()
        else:
            self.displayFile()

    def on_menuFileOpen_select(self, event):
        result = dialog.openFileDialog()
        if result.accepted:
            self.openFile(result.paths[0])

    def on_menuFileSaveAs_select(self, event):
        if self.filename is None:
            path = ''
            filename = ''
        else:
            path, filename = os.path.split(self.filename)
        wildcard = "All files (*.*)|*.*"
        result = dialog.saveFileDialog(None, "Save As", path, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            fileType = graphic.bitmapType(path)
            #print fileType, path
            # should throw an error here if the user
            # tries to save as GIF since wxWindows doesn't
            # support that format due to licensing restrictions
            try:
                bmp = self.components.bufOff.getBitmap()
                bmp.SaveFile(path, fileType)
                return True
            except IOError:
                return False
        else:
            return False

    def on_menuEditCopy_select(self, event):
        clipboard.setClipboard(self.components.bufOff.getBitmap())

    def on_menuEditPaste_select(self, event):
        bmp = clipboard.getClipboard()
        if isinstance(bmp, wx.Bitmap):
            self.components.bufOff.drawBitmap(bmp)

    def on_editClear_command(self, event):
        self.components.bufOff.clear()

    # decided not to use sizers
    # but leaving this in on the chance
    # I might switch back
    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        comp = self.components
        flags = wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_BOTTOM
        sizer1.Add(comp.bufOff, 1, wx.EXPAND)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()


if __name__ == '__main__':
    app = model.Application(PictureViewer)
    app.MainLoop()
