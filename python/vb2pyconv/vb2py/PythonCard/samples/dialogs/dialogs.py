#!/usr/bin/python

"""
__version__ = "$Revision: 1.27 $"
__date__ = "$Date: 2004/10/03 18:16:55 $"
"""

from PythonCard import dialog, model
import os, sys
import wx
import minimalDialog

class Dialogs(model.Background):
    def on_initialize(self, event):
        self.fitToComponents(None, 5)

    def on_listDialogs_select(self, event):
        name = event.stringSelection
        handlers = {
            'alert':self.on_buttonAlert_mouseClick,
            'color':self.on_buttonColor_mouseClick,
            'directory':self.on_buttonDir_mouseClick,
            'file':self.on_buttonFile_mouseClick,
            'find':self.on_buttonFind_mouseClick,
            'font':self.on_buttonFont_mouseClick,
            'message':self.on_buttonMessage_mouseClick,
            'multiple choice':self.on_buttonMultipleChoice_mouseClick,
            'scrolled message':self.on_buttonScrolledMessage_mouseClick,
            'single choice':self.on_buttonSingleChoice_mouseClick,
            'open file':self.on_buttonOpenFile_mouseClick,
            'save file':self.on_buttonSaveFile_mouseClick,
            'text entry':self.on_buttonTextEntry_mouseClick,
            'minimal':self.on_buttonMinimalDialog_mouseClick,
        }
        # call the appropriate handler
        handlers[name](None)
        
    def on_buttonMultipleChoice_mouseClick(self, event):
        result = dialog.multipleChoiceDialog(self, "message", "title", ['one', 'two', 'three'])
        self.components.fldResults.text = "multipleChoiceDialog result:\naccepted: %s\nSelection: %s" % (result.accepted, result.selection)

    def on_buttonSingleChoice_mouseClick(self, event):
        result = dialog.singleChoiceDialog(self, "message", "title", ['one', 'two', 'three'])
        self.components.fldResults.text = "singleChoiceDialog result:\naccepted: %s\nSelection: %s" % (result.accepted, result.selection)

    def on_buttonFind_mouseClick(self, event):
        result = dialog.findDialog(self)
        self.components.fldResults.text = "findDialog result:\naccepted: %s\nText: %s\nWhole word only: %s\nCase sensitive: %s" % (result.accepted,
                                                                                                          result.searchText,
                                                                                                          result.wholeWordsOnly,
                                                                                                          result.caseSensitive)

    def on_buttonColor_mouseClick(self, event):
        result = dialog.colorDialog(self)
        self.components.fldResults.text = "colorDialog result:\naccepted: %s\nColor: %s" % (result.accepted, result.color)

    def on_buttonFont_mouseClick(self, event):
        result = dialog.fontDialog(self)
        self.components.fldResults.text = "fontDialog result:\naccepted: %s\nColor: %s\nFont: %s" % (result.accepted, result.color, result.font)

    def on_buttonFile_mouseClick(self, event):
        wildcard = "JPG files (*.jpg;*.jpeg)|*.jpeg;*.JPG;*.JPEG;*.jpg|GIF files (*.gif)|*.GIF;*.gif|All Files (*.*)|*.*"
        # wildcard = '*.py'
        result = dialog.fileDialog(self, 'Open', '', '', wildcard )
        self.components.fldResults.text = "fileDialog result:\naccepted: %s\npaths: %s" % (result.accepted, result.paths)

    def on_buttonOpenFile_mouseClick(self, event):
        wildcard = "JPG files (*.jpg;*.jpeg)|*.jpeg;*.JPG;*.JPEG;*.jpg|GIF files (*.gif)|*.GIF;*.gif|All Files (*.*)|*.*"
        # wildcard = '*.py'
        result = dialog.openFileDialog(wildcard=wildcard)
        self.components.fldResults.text = "openFileDialog result:\naccepted: %s\npaths: %s" % (result.accepted, result.paths)

    def on_buttonSaveFile_mouseClick(self, event):
        wildcard = "JPG files (*.jpg;*.jpeg)|*.jpeg;*.JPG;*.JPEG;*.jpg|GIF files (*.gif)|*.GIF;*.gif|All Files (*.*)|*.*"
        # wildcard = '*.py'
        result = dialog.saveFileDialog(wildcard=wildcard)
        self.components.fldResults.text = "saveFileDialog result:\naccepted: %s\npaths: %s" % (result.accepted, result.paths)

    def on_buttonDir_mouseClick(self, event):
        result = dialog.directoryDialog(self, 'Choose a directory', 'a')
        self.components.fldResults.text = "directoryDialog result:\naccepted: %s\npath: %s" % (result.accepted, result.path)

    """
    You can pass in a specific icon (default is wx.ICON_INFORMATION)
    as well as the buttons (default is wx.OK | wx.CANCEL)
    
    wx.ICON_EXCLAMATION    # Shows an exclamation mark icon.  
    wx.ICON_HAND           # Shows an error icon.  
    wx.ICON_ERROR          # Shows an error icon - the same as wxICON_HAND.  
    wx.ICON_QUESTION       # Shows a question mark icon.  
    wx.ICON_INFORMATION    # Shows an information (i) icon.

    wx.OK           # Show an OK button.  
    wx.CANCEL       # Show a Cancel button.  
    wx.YES_NO       # Show Yes and No buttons.  
    wx.YES_DEFAULT  # Used with wx.YES_NO, makes Yes button the default - which is the default behaviour.  
    wx.NO_DEFAULT   # Used with wx.YES_NO, makes No button the default.  
    """
    def on_buttonMessage_mouseClick(self, event):
        """
        result = dialog.messageDialog(self, 'a message', 'a title',
                               wx.ICON_ERROR | wx.YES_NO)
        """
        result = dialog.messageDialog(self, 'a message', 'a title',
                               wx.ICON_INFORMATION | wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL)
        #result = dialog.messageDialog(self, 'a message', 'a title')
        self.components.fldResults.text = "messageDialog result:\naccepted: %s\nreturnedString: %s" % (result.accepted, result.returnedString)

    # you can pass in an additional aStyle parameter
    # of wx.TE_PASSWORD or wx.TE_MULTILINE
    def on_buttonTextEntry_mouseClick(self, event):
        result = dialog.textEntryDialog(self, 
                                    'What is your favorite language?',
                                    'A window title', 
                                    'Python')
        """
        result = dialog.textEntryDialog(self, 
                                    'What is your favorite language?',
                                    'A window title', 
                                    'Python', wx.TE_MULTILINE)
        """
        self.components.fldResults.text = "textEntryDialog result:\naccepted: %s\nreturnedString: %s\ntext: %s" % (result.accepted, result.returnedString, result.text)

    def on_buttonScrolledMessage_mouseClick(self, event):
        base, ext = os.path.splitext(os.path.split(sys.argv[0])[-1])
        filename = base + ".py"
        if os.path.exists(filename):
            f = open(filename, "r")
            msg = f.read()
        else:
            msg = "Can't find the file dialogs.py"
        result = dialog.scrolledMessageDialog(self, msg, filename)
        self.components.fldResults.text = "scrolledMessageDialog result:\naccepted: %s" % (result.accepted)

    def on_buttonAlert_mouseClick(self, event):
        result = dialog.alertDialog(self, 'a message', 'a title')
        self.components.fldResults.text = "alertDialog result:\naccepted: %s\nreturnedString: %s" % (result.accepted, result.returnedString)

    def on_buttonMinimalDialog_mouseClick(self, event):
        result = minimalDialog.minimalDialog(self, 'hello minimal')
        self.components.fldResults.text = "minimalDialog result:\naccepted: %s\ntext: %s" % (result.accepted, result.text)


if __name__ == '__main__':
    app = model.Application(Dialogs)
    app.MainLoop()
