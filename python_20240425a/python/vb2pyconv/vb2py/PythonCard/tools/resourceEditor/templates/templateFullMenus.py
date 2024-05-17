#!/usr/bin/python

"""
__version__ = "$Revision: 1.10 $"
__date__ = "$Date: 2004/08/12 19:14:23 $"

"""

import os, sys
import wx
from wx.html import HtmlEasyPrinting
from PythonCard import configuration, dialog, model


def textToHtml(txt):
    # the wxHTML classes don't require valid HTML
    # so this is enough
    html = txt.replace('\n\n', '<P>')
    html = html.replace('\n', '<BR>')
    return html


class MyBackground(model.Background):
    
    def on_initialize(self, event):
        # if you have any initialization
        # including sizer setup, do it here

        self.printer = HtmlEasyPrinting()
        # self.loadConfig()
        self.startTitle = self.title
        self.newFile()

    def loadConfig(self):
        pass

    def saveConfig(self):
        pass

    def saveChanges(self):
        # save configuration info in the app directory
        #filename = os.path.basename(self.documentPath)
        if self.documentPath is None:
            filename = "Untitled"
        else:
            filename = self.documentPath
        msg = "The text in the %s file has changed.\n\nDo you want to save the changes?" % filename
        result = dialog.messageDialog(self, msg, 'textEditor', wx.ICON_EXCLAMATION | wx.YES_NO | wx.CANCEL)
        return result.returnedString

    def doExit(self):
        if self.documentChanged:
            save = self.saveChanges()
            if save == "Cancel":
                return False
            elif save == "No":
                return True
            else:
                if self.documentPath is None:
                    return self.on_menuFileSaveAs_select(None)
                else:
                    self.saveFile(self.documentPath)
                    return True
        else:
            return 1

    def on_close(self, event):
        if self.doExit():
            # self.saveConfig()
            self.fileHistory = None
            self.printer = None
            event.skip()

    def on_menuFileSave_select(self, event):
        if self.documentPath is None:
            # this a "new" document and needs to go through Save As...
            self.on_menuFileSaveAs_select(None)
        else:
            self.saveFile(self.documentPath)

    def on_menuFileSaveAs_select(self, event):
        wildcard = "Text files (*.txt)|*.TXT;*.txt|All files (*.*)|*.*"
        if self.documentPath is None:
            dir = ''
            filename = '*.txt'
        else:
            dir = os.path.dirname(self.documentPath)
            filename = os.path.basename(self.documentPath)
        result = dialog.saveFileDialog(None, "Save As", dir, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            self.saveFile(path)
            return True
        else:
            return False

    def newFile(self):
        # change the code below for
        # creating a new document
        # the commented line is from the textEditor tool

        # self.components.fldDocument.text = ''
        self.documentPath = None
        self.documentChanged = 0
        self.title = 'Untitled - ' + self.startTitle
        self.statusBar.text = 'Untitled'

    def openFile(self, path):
        # change the code below for
        # opening an existing document
        # the commented lines are from the textEditor tool
        try:
            # f = open(path)
            # self.components.fldDocument.text = f.read().replace('\r\n','\n')
            # f.close()
            self.documentPath = path
            self.documentChanged = 0
            self.title = os.path.split(path)[-1] + ' - ' + self.startTitle
            self.statusBar.text = path
        except:
            pass

    def saveFile(self, path):
        # change the code below for
        # saving an existing document
        # the commented lines are from the textEditor tool
        try:
            # f = open(path, 'w')
            # f.write(self.components.fldDocument.text)
            # f.close()
            self.documentPath = path
            self.documentChanged = False
            self.title = os.path.split(path)[-1] + ' - ' + self.startTitle
            self.statusBar.text = path
        except:
            pass

    def on_menuFileNew_select(self, event):
        if self.documentChanged:
            save = self.saveChanges()
            if save == "Cancel":
                # don't do anything, just go back to editing
                pass
            elif save == "No":
                # any changes will be lost
                self.newFile()
            else:
                if self.documentPath is None:
                    if self.on_menuFileSaveAs_select(None):
                        self.newFile()
                else:
                    self.saveFile(self.documentPath)
                    self.newFile()
        else:
            # don't need to save
            self.newFile()

    def on_menuFileOpen_select(self, event):
        # should probably have an alert dialog here
        # warning about saving the current file before opening another one
        if self.documentChanged:
            save = self.saveChanges()
            if save == "Cancel":
                # don't do anything, just go back to editing
                return
            elif save == "No":
                # any changes will be lost
                pass
            else:
                if self.documentPath is None:
                    # if the user cancels out of the Save As then go back to editing
                    if not self.on_menuFileSaveAs_select(None):
                        return
                else:
                    self.saveFile(self.documentPath)
        
        # split this method into several pieces to make it more flexible
        wildcard = "Text files (*.txt)|*.txt;*.TXT|All files (*.*)|*.*"
        result = dialog.openFileDialog(wildcard=wildcard)
        if result.accepted:
            path = result.paths[0]
            # an error will probably occur here if the text is too large
            # to fit in the wxTextCtrl (TextArea) or the file is actually
            # binary. Not sure what happens with CR/LF versus CR versus LF
            # line endings either
            self.openFile(path)

        
    def on_menuFilePrint_select(self, event):
        # put your code here for print
        # the commented code below is from the textEditor tool
        # and is simply an example
        
        #source = textToHtml(self.components.fldDocument.text)
        #self.printer.PrintText(source)
        pass

    def on_menuFilePrintPreview_select(self, event):
        # put your code here for print preview
        # the commented code below is from the textEditor tool
        # and is simply an example
        
        #source = textToHtml(self.components.fldDocument.text)
        #self.printer.PreviewText(source)
        pass

    def on_menuFilePageSetup_select(self, event):
        self.printer.PageSetup()


    # the following was copied and pasted from the searchexplorer sample
    def on_menuEditUndo_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canUndo():
            widget.undo()

    def on_menuEditRedo_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canRedo():
            widget.redo()

    def on_menuEditCut_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canCut():
            widget.cut()

    def on_menuEditCopy_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canCopy():
            widget.copy()

    def on_menuEditPaste_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canPaste():
            widget.paste()
        
    def on_menuEditClear_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable'):
            if widget.canCut():
                # delete the current selection,
                # if we can't do a Cut we shouldn't be able to delete either
                # which is why i used the test above
                sel = widget.replaceSelection('')
            else:
                ins = widget.getInsertionPoint()
                try:
                    widget.replace(ins, ins + 1, '')
                except:
                    pass

    def on_menuEditSelectAll_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable'):
            widget.setSelection(0, widget.getLastPosition())
        

    def on_doHelpAbout_command(self, event):
        # put your About box here
        pass

if __name__ == '__main__':
    app = model.Application(MyBackground)
    app.MainLoop()
