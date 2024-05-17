#!/usr/bin/python

"""
__version__ = "$Revision: 1.18 $"
__date__ = "$Date: 2005/12/13 11:13:24 $"
"""

from PythonCard import clipboard, dialog, graphic, model
import wx
import os

rsrc = {'application':{'type':'Application',
          'name':'saveClipboardBitmap',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'saveClipboardBitmap PythonCard Application',
          'size':(200, 100),
    'menubar': 
    { 
        'type':'MenuBar',
        'menus': 
        [
            { 'type':'Menu',
              'name':'menuFile',
              'label':'&File',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuFileSaveAs',
                  'label':'&Save As...\tCtrl+S' },
                { 'type':'MenuItem',
                  'name':'menuFileExit',
                  'label':'E&xit\tAlt+X',
                  'command':'exit' },
                ] }
        ]       
    },
         'components': [

] # end components
} # end background
] # end backgrounds
} }

class Minimal(model.Background):

    def on_initialize(self, event):
        self.bmp = None
        self.filename = None
        # since there might already be an image in the clipboard
        # go ahead and prompt to save it
        self.on_menuFileSaveAs_select(None)

    def on_menuFileSaveAs_select(self, event):
        self.bmp = clipboard.getClipboard()
        if not isinstance(self.bmp, wx.Bitmap):
            return
        if self.filename is None:
            path = ''
            filename = ''
        else:
            path, filename = os.path.split(self.filename)
        # wxPython can't save GIF due to the license issues
        # but we can save most other formats, so this list can be expanded
        wildcard = "PNG files (*.png)|*.PNG;*.png" + \
                   "|JPG files (*.jpg;*.jpeg)|*.jpeg;*.JPG;*.JPEG;*.jpg" + \
                   "|BMP files (*.bmp)|*.BMP;*.bmp" + \
                   "|All Files (*.*)|*.*"
        result = dialog.saveFileDialog(None, "Save As", path, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            fileType = graphic.bitmapType(path)
            #print fileType, path
            self.filename = path
            self.bmp.SaveFile(path, fileType)
            return True
        else:
            return False


if __name__ == '__main__':
    app = model.Application(Minimal, None, rsrc)
    app.MainLoop()
