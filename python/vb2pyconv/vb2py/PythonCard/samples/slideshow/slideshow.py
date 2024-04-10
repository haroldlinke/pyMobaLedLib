#!/usr/bin/python

"""
__version__ = "$Revision: 1.43 $"
__date__ = "$Date: 2005/12/13 11:13:25 $"
"""

from PythonCard import dialog, graphic, log, model, timer, util, EXIF
import wx
import os, sys
import zipfile
from cStringIO import StringIO

def imageFile(path):
    if os.path.isfile(path):
        ext = os.path.splitext(path)[-1].lower()
        if ext != '' and ext[0] == '.':
            ext = ext[1:]
        if ext in ['bmp', 'gif', 'jpeg', 'jpg', 'pcx', 
                   'png', 'pnm', 'tif', 'tiff', 'xbm', 'xpm']:
            return 1
    return 0

def htmlFile(path):
    if os.path.isfile(path):
        ext = os.path.splitext(path)[-1].lower()
        if ext != '' and ext[0] == '.':
            ext = ext[1:]
        if ext in ['htm', 'html']:
            return 1
    return 0    
    
class SlideShow(model.Background):

    def on_initialize(self, event):
        self.x = 0
        self.y = 0
        self.filename = None
        self.directory = None
        self.zip = None
        self.bmp = None
        self.fileList = None
        self.fileIndex = 0
        self.clockTimer = timer.Timer(self.components.bufOff, -1)
        self.interval = 1000 * 2 # 5 seconds
        self.loop = 0

        self.components.bufOff.backgroundColor = 'black'
        self.components.bufOff.clear()
        
        if sys.platform.startswith('win'):
            del self.components['htmlView']
            self.components['htmlView'] = {'type':'IEHtmlWindow', 'name':'htmlView', 
                'position':(0, 0), 'size':(150, 150), 'visible':0}
            # can't disable the component if we want it
            # to scroll, so need another way to capture
            # key presses so the IE control doesn't get them
            # however since slideshow is for displaying HTML
            # where you shouldn't need to scroll this is probably fine
            # there is still some kind of focus bug with the IE control
            # on certain HTML pages
            self.components.htmlView.enabled = 0

        # this is the code from pictureViewer
        # instead of a file argument, slideshow
        # should take either a file or directory
        # argument
        # if given a directory, the slide show would
        # be setup to start in that directory
        # if given a file argument, the contents
        # of the file would contain a list of files to
        # display, one file per line
        if len(sys.argv) > 1:
            # accept a file argument on the command-line
            filename = os.path.abspath(sys.argv[1])
            log.info('slideshow filename: ' + filename)
            if not os.path.exists(filename):
                filename = os.path.abspath(os.path.join(self.application.startingDirectory, sys.argv[1]))
            #print filename
            if os.path.isfile(filename):
                #self.openFile(filename)
                self.buildFileListFromFile(filename)
                self.on_menuSlideshowFirstSlide_select(None)
            elif os.path.isdir(filename):
                includeSubDirs = self.menuBar.getChecked('menuOptionsIncludeSubDirectories')
                self.buildFileListFromDirectory(filename, includeSubDirs)
                self.on_menuSlideshowFirstSlide_select(None)

        # PythonCard doesn't currently support
        # binding key presses to just the background, so this
        # is a hack
        wx.EVT_KEY_UP(self.components.bufOff, self.on_keyPress)
        wx.EVT_KEY_UP(self.components.htmlView, self.on_keyPress)

        self.visible = True
        self.on_size(None)

    def on_timer(self, event):
        self.displayNextFile()

    def on_keyPress(self, event):
        # need to enable keyPresses
        # for backgrounds without a component that accepts keyPresses
        keyCode = event.GetKeyCode()
        #print keyCode
        if keyCode == wx.WXK_UP or keyCode == wx.WXK_HOME:
            self.on_menuSlideshowFirstSlide_select(None)
        elif keyCode == wx.WXK_LEFT:
            self.on_menuSlideshowPreviousSlide_select(None)
        elif keyCode == wx.WXK_RIGHT or keyCode == wx.WXK_SPACE:
            self.on_menuSlideshowNextSlide_select(None)
        elif keyCode == wx.WXK_DOWN or keyCode == wx.WXK_END:
            self.on_menuSlideshowLastSlide_select(None)

    def on_size(self, event):
        size = self.GetClientSize()
        self.panel.SetSize(size)
        self.components.bufOff.size = size
        self.components.htmlView.size = size
        self.displayFile()

    def displayFile(self):
        # always display the file limited to the current size of buffer
        if self.filename is not None:
            if htmlFile(self.filename):
                self.components.htmlView.text = self.filename
                self.components.bufOff.visible = 0
                self.components.htmlView.visible = 1
                #self.components.htmlView.setFocus()
            else:
                self.components.htmlView.visible = 0

                bufOff = self.components.bufOff
                bufOff.autoRefresh = 0
    
                imgSize = self.bmp.getSize()
                bufSize = bufOff.size
                
                bufOff.clear()
                bufOff.autoRefresh = 1
    
                # the image will be displayed scaled centered
                # in the current buffer window
                # so we need to know the smallest scale dimension
                # and use that for scaling
                #newSize = self.sizeScaled(imgSize, bufSize[0], heightScale)
                
                # if the size of the image is <= the width and height of the 
                # buffer then don't scale the image, just center it
                if imgSize[0] <= bufSize[0] and imgSize[1] <= bufSize[1]:
                    xOffset = (bufSize[0] - imgSize[0]) / 2
                    yOffset = (bufSize[1] - imgSize[1]) / 2
                    bufOff.drawBitmap(self.bmp, (xOffset, yOffset))
                else:
                    widthScale = (0.0 + bufSize[0]) / imgSize[0]
                    heightScale = (0.0 + bufSize[1]) / imgSize[1]
                    if widthScale > heightScale:
                        scale = heightScale
                        newSize = (int(round(imgSize[0] * scale)), int(round((imgSize[1] * scale))))
                        # center horizontally
                        offset = (bufSize[0] - newSize[0]) / 2
                        #print "offset", offset
                        position = (int(round(offset)), 0)
                    else:
                        scale = widthScale
                        newSize = (int(round(imgSize[0] * scale)), int(round((imgSize[1] * scale))))
                        # center vertically
                        offset = (bufSize[1] - newSize[1]) / 2
                        #print "offset", offset
                        position = (0, int(round(offset)))
                    bufOff.drawBitmapScaled(self.bmp, position, newSize)
                self.components.bufOff.visible = 1
                #self.components.bufOff.setFocus()

    def openFile(self, path, slideNumber=None):
        self.filename = path
        if htmlFile(self.filename):
            title = os.path.split(self.filename)[-1]
        else:
            if self.zip:
                data = self.zip.read(self.filename)
                tags = EXIF.process_file(StringIO(data))
                log.debug("Getting %s from zip file" % self.filename)
                self.bmp = graphic.Bitmap()
                self.bmp.setImageBits(wx.ImageFromStream(StringIO(data)))
            else:
                if not os.path.exists(self.filename):
                    return
                f = open(self.filename, 'rb')
                tags = EXIF.process_file(f)
                f.close()
                log.debug("Getting %s from file" % self.filename)
                self.bmp = graphic.Bitmap(self.filename)
            if tags.has_key('Image Orientation'):
                # the repr() is something like
                # (0x0112) Short=8 @ 54
                # but the str() is just 1, 8, etc.
                orientation = int(str(tags['Image Orientation']))
            else:
                orientation = 1
            log.debug('Image Orientation: %d' % orientation)
            if tags.has_key('Thumbnail Orientation'):
                log.debug('Thumbnail Orientation: %s' % tags['Thumbnail Orientation'])
            if orientation == 8:
                # need to rotate the image
                # defaults to clockwise, 0 means counter-clockwise
                self.bmp.rotate90(0)
            elif orientation == 6:
                self.bmp.rotate90(1)
            size = self.bmp.getSize()
            title = os.path.split(self.filename)[-1] + "  %d x %d" % size
        if slideNumber is not None:
            title = title + "  Slide: %d of %d" % (slideNumber + 1, len(self.fileList))
        self.title = title
        self.displayFile()

    def displayNextFile(self):
        if self.fileList is None:
            return
        index = self.fileIndex + 1
        if self.loop and index == len(self.fileList):
            index = 0
        if index < len(self.fileList):
            self.fileIndex = index
            self.openFile(self.fileList[self.fileIndex], self.fileIndex)
            # one shot timer
            self.clockTimer.start(self.interval, 1)

    def doSlideShow(self):
        if self.fileList is not None and self.fileList != []:
            self.fileIndex = -1
            self.displayNextFile()

    def on_menuSlideshowLoop_select(self, event):
        self.loop = self.menuBar.getChecked('menuSlideshowLoop')

    def on_menuSlideshowContinue_select(self, event):
        # act as a toggle
        if self.clockTimer.isRunning():
            self.clockTimer.stop()
        else:
            self.displayNextFile()

    def on_menuSlideshowShowSlides_select(self, event):
        self.doSlideShow()

    def on_menuSlideshowSetInterval_select(self, event):
        interval = str(self.interval / 1000)
        result = dialog.textEntryDialog(self, "Time interval between slides (seconds):", "Slide interval", interval)
        if result.accepted:
            try:
                interval = int(result.text) * 1000
                self.interval = interval
            except ValueError:
                pass

    def buildFileListFromFile(self, path):
        try:
            f = open(path)
            txt = f.read()
            f.close()
            self.fileList = txt.splitlines()
        except IOError:
            pass

    def buildFileListFromDirectory(self, path, recurse=True):
        self.zip = None
        self.directory = path
        fileList = util.dirwalk(path, ['*'], recurse)
        log.debug('Directory file list: %s' % fileList)
        # self.fileList should be filtered here
        self.fileList = []
        self.fileIndex = -1
        for path in fileList:
            if imageFile(path) or htmlFile(path):
                self.fileList.append(path)
        self.fileList = util.caseinsensitive_sort(self.fileList)
        
    def buildFileListFromZip(self, path):
        self.zip = zipfile.ZipFile(path)
        self.directory = None
        fileList = self.zip.namelist()
        log.debug('Zip file list: %s' % fileList)
        # self.fileList should be filtered here
        self.fileList = []
        self.fileIndex = -1
        for f in fileList:
            ext = os.path.splitext(f)[-1].lower()
            if ext != '' and ext[0] == '.':
                ext = ext[1:]
            if ext in ['bmp', 'gif', 'jpeg', 'jpg', 'pcx', 
                       'png', 'pnm', 'tif', 'tiff', 'xbm', 'xpm']:
                self.fileList.append(f)

    def on_menuSlideshowChooseZip_select(self, event):
        wildcard = "Zip archives (*.zip)|*.ZIP;*.zip"
        if 0:
            if self.documentPath is None:
                dir = ''
                filename = '*.txt'
            else:
                dir = os.path.dirname(self.documentPath)
                filename = os.path.basename(self.documentPath)
        result = dialog.openFileDialog(self, 'Choose a zip', wildcard=wildcard)
        if result.accepted:
            self.buildFileListFromZip(result.paths[0])
            self.on_menuSlideshowFirstSlide_select(None)

    def on_menuSlideshowChooseDirectory_select(self, event):
        if self.directory is not None:
            directory = self.directory
        else:
            directory = ''
        result = dialog.directoryDialog(self, 'Choose a directory', directory)
        if result.accepted:
            includeSubDirs = self.menuBar.getChecked('menuOptionsIncludeSubDirectories')
            self.buildFileListFromDirectory(result.path, includeSubDirs)
            self.on_menuSlideshowFirstSlide_select(None)

    def on_menuSlideshowToggleFullScreen_select(self, event):
        self.ShowFullScreen(self.menuBar.getChecked('menuSlideshowToggleFullScreen'))

    def on_menuSlideshowStopSlides_select(self, event):
        # KEA 2004-07-17
        # if the slideshow is running in fullscreen mode then
        # people can panic not knowing how to stop the slideshow and get
        # control back so I made the ESC key stop the slideshow and
        # go back to a normal window size
        if self.clockTimer.isRunning():
            self.clockTimer.stop()
        if self.menuBar.getChecked('menuSlideshowToggleFullScreen'):
            self.menuBar.setChecked('menuSlideshowToggleFullScreen', False)
            self.ShowFullScreen(False)

    def on_menuSlideshowFirstSlide_select(self, event):
        if self.fileList is not None and self.fileList != []:
            self.fileIndex = 0
            self.openFile(self.fileList[self.fileIndex], self.fileIndex)
            if self.clockTimer.isRunning():
                self.clockTimer.start(self.interval, 1)

    def on_menuSlideshowPreviousSlide_select(self, event):
        if self.fileList is not None and self.fileList != []:
            self.fileIndex -= 1
            if self.fileIndex == -1:
                self.fileIndex = len(self.fileList) - 1
            self.openFile(self.fileList[self.fileIndex], self.fileIndex)
            if self.clockTimer.isRunning():
                self.clockTimer.start(self.interval, 1)

    def on_menuSlideshowNextSlide_select(self, event):
        if self.fileList is not None and self.fileList != []:
            self.fileIndex += 1
            if self.fileIndex == len(self.fileList):
                self.fileIndex = 0
            self.openFile(self.fileList[self.fileIndex], self.fileIndex)
            if self.clockTimer.isRunning():
                self.clockTimer.start(self.interval, 1)

    def on_menuSlideshowGotoSlide_select(self, event):
        if self.fileList is not None and self.fileList != []:
            result = dialog.textEntryDialog(self, "Slide number:", "Goto slide", str(self.fileIndex + 1))
            # this version doesn't alert the user if the line number is out-of-range
            # it just fails quietly
            if result.accepted:
                try:
                    n = int(result.text) - 1
                    if n >= 0 and n < len(self.fileList):
                        self.fileIndex = n
                        self.openFile(self.fileList[self.fileIndex], self.fileIndex)
                except ValueError:
                    pass

    def on_mouseUp(self, event):
        self.on_menuSlideshowNextSlide_select(None)

    def on_menuSlideshowLastSlide_select(self, event):
        if self.fileList is not None and self.fileList != []:
            self.fileIndex = len(self.fileList) - 1
            self.openFile(self.fileList[self.fileIndex], self.fileIndex)
            if self.clockTimer.isRunning():
                self.clockTimer.start(self.interval, 1)

    def on_menuFileOpen_select(self, event):
        result = dialog.openFileDialog()
        if result.accepted:
            self.openFile(result.paths[0])

    def on_menuFileOpenSlide_select(self, event):
        if self.fileList is not None and self.fileList != []:
            path = self.fileList[self.fileIndex]
            if imageFile(path):
                log.debug("image: %s" % path)
                viewer = os.path.abspath(os.path.join('..', 'pictureViewer', 'pictureViewer.py'))
                if " " in path:
                    path = '"' + path + '"'
                try:
                    util.runScript(viewer, path)
                except: # Fail gracefully if displaying fails
                    pass
            elif htmlFile(path):
                log.debug("html: %s" % path)
                import webbrowser
                webbrowser.open(path, 1, 1)

    def on_close(self, event):
        self.clockTimer.stop()
        self.bmp = None
        event.skip()

if __name__ == '__main__':
    app = model.Application(SlideShow)
    app.MainLoop()
