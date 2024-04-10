#!/usr/bin/env python
"""
__version__ = "$Revision: 1.5 $"
__date__ = "$Date: 2005/12/29 02:48:25 $"

PythonCard Editor (codeEditor) wiki page
http://wiki.wxpython.org/index.cgi/PythonCardEditor

wxStyledTextCtrl documentation
http://wiki.wxpython.org/index.cgi/wxStyledTextCtrl
"""

from PythonCard import about, configuration, dialog, log, menu, model, resource, util, registry
from PythonCard.templates.dialogs import runOptionsDialog

from modules import scriptutils
import os, sys
import wx
from wx import stc
from wx.html import HtmlEasyPrinting
import pprint
from PythonCard import STCStyleEditor

from modules import colorizer
import cStringIO
import webbrowser


class CodePage(model.PageBackground):
    
    def on_initialize(self, event):
        self.initSizers()

        self.setDefaultStyles()
        self.lastStatus = None
        self.lastPos = None

    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.components.document, 1, wx.EXPAND)

        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def setDefaultStyles(self):
        config = configuration.getStyleConfigPath()
        # KEA 2002-05-28
        # STCStyleEditor doesn't work yet on OS X
        if config is not None:
            STCStyleEditor.initSTC(self.components.document, config, 'python')
            if self.application.shell is not None:
                STCStyleEditor.initSTC(self.application.shell, config, 'python')

    def setEditorStyle(self):
        try:
            self.components.document.setEditorStyle(os.path.splitext(self.documentPath)[-1])
        except:
            self.components.document.setEditorStyle('python')

    def saveAsFile(self):
        resourceStrings = self.topLevelParent.resource.strings
        #wildcard = "Python scripts (*.py;*.pyw)|*.py;*.pyw|Text files (*.txt)|*.txt|All files (*.*)|*.*"
        wildcard = resourceStrings.saveAsWildcard
        if self.documentPath is None:
            dir = ''
            filename = '*.py'
        else:
            dir = os.path.dirname(self.documentPath)
            filename = os.path.basename(self.documentPath)
        result = dialog.saveFileDialog(None, resourceStrings.saveAs, dir, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            self.saveFile(path)
            self.topLevelParent.fileHistory.AddFileToHistory(path)
            return True
        else:
            return False
        

    def newFile(self):
        self.components.document.text = ''
        self.documentPath = None
        self.setEditorStyle()
        self.components.document.SetSavePoint()
        self.statusBar.text = self.resource.strings.untitled
        self.lastStatus = None
        # KEA 2003-07-26
        # reset EOL to match platform
        # this may not actually be what the user expects
        # so perhaps this should be an option in a dialog?!
        self.autoSetEOL()
        self.topLevelParent.setTitleBar(self.resource.strings.untitled)

    def openFile(self, path):
        try:
            self.components.document.SetUndoCollection(0)
            self.components.document.ClearAll()
            f = open(path, 'rb')
            try:
                self.components.document.text = f.read()
            finally:
                f.close()
            self.documentPath = path
            os.chdir(os.path.dirname(self.documentPath))
            self.components.document.EmptyUndoBuffer()
            self.components.document.SetUndoCollection(1)
            self.components.document.SetSavePoint()
            #self.statusBar.text = path
            self.lastStatus = None
            self.topLevelParent.fileHistory.AddFileToHistory(path)
            # KEA 2002-06-29
            # just as a test, let's see how the XML and/or HTML styles
            # look
            self.setEditorStyle()
            self.autoSetEOL()
            self.topLevelParent.setTitleBar(os.path.split(path)[-1])
            wx.CallAfter(self.components.document.SetFocus)
        except:
            pass

    def saveFile(self, path):
        try:
            f = open(path, 'wb')
            try:
                f.write(self.components.document.text)
            finally:
                f.close()
            self.documentPath = path
            os.chdir(os.path.dirname(self.documentPath))
            self.components.document.SetSavePoint()
            #self.statusBar.text = path
            self.lastStatus = None
            self.setEditorStyle()
            self.topLevelParent.setTitleBar(os.path.split(path)[-1])
        except:
            pass

    # KEA 2003-07-26
    def autoSetEOL(self):
        """
        when opening an existing file
        automatically set the EOL mode to
        match the current line endings for the file
        if the document is empty then set EOL to
        the original EOL state
        """
        doc = self.components.document
        if doc.GetLength():
            line = doc.GetLine(0)
        else:
            line = os.linesep
        if line.endswith('\r\n'):
            doc.SetEOLMode(stc.STC_EOL_CRLF)
        elif line.endswith('\n'):
            doc.SetEOLMode(stc.STC_EOL_LF)
        elif line.endswith('\r'):
            doc.SetEOLMode(stc.STC_EOL_CR)


    # Edit menu
    
    def on_menuEditUndo_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.CanUndo():
            widget.Undo()

    def on_menuEditRedo_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.CanRedo():
            widget.Redo()

    def on_menuEditCut_select(self, event):
        widget = self.findFocus()
        # KEA 2002-05-03
        # no CanCut() method?
        if hasattr(widget, 'editable'):
            widget.Cut()

    def on_menuEditCopy_select(self, event):
        widget = self.findFocus()
        # KEA 2002-05-03
        # no CanCopy() method?
        if hasattr(widget, 'editable'):
            widget.Copy()

    def on_menuEditPaste_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.CanPaste():
            widget.Paste()
        
    def on_menuEditClear_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable'):
            widget.ClearSelection()            

    def on_menuEditSelectAll_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable'):
            widget.SelectAll()

    def on_document_keyDown(self, event):
        #print "keyPress", event.keyCode, event.shiftDown, event.controlDown, event.altDown

        # smart auto-indent on Return
        # this is brute force and currently assumes 4 space
        # Guido indentation style
        keyCode = event.keyCode
        target = event.target

        if keyCode == wx.WXK_RETURN:
            # since we won't be calling skip, insert a newline manually
            self.components.document.CmdKeyExecute(stc.STC_CMD_NEWLINE)
            # why isn't GetCurrentLine 0 based?
            line = target.GetCurrentLine() - 1
            txt = target.GetLine(line)

            stripped = txt.rstrip()
            # auto-indent block
            indent = target.GetLineIndentation(line)
            padding = " " * indent
            pos = target.GetCurrentPos()
            if len(stripped) > 0 and stripped[-1] == ':':
                # KEA 2002-05-06 to do
                # should use GetStyleAt() on the actual pos of
                # the : to make sure the style is not wxSTC_P_COMMENTLINE...
                # actually this is more complex and really when the style
                # we need to walk backwards until we find a colon not in
                # one of the comment styles before doing an auto-indent
                # but I don't feel like getting it all working before 0.6.6
                # so this is left as an exercise for the reader ;-)
##                whitespace = len(txt) - len(stripped)
##                colonPos = target.GetLineEndPosition(line) - whitespace + 1
##                if target.GetStyleAt(colonPos) not in \
##                   [stc.STC_P_COMMENTLINE,
##                    stc.STC_P_COMMENTBLOCK,
##                    stc.STC_P_TRIPLEDOUBLE ]:
                padding += " " * 4
            target.InsertText(pos, padding)
            newpos = pos + len(padding)
            target.SetCurrentPos(newpos)
            target.SetSelection(newpos, newpos)
        else:
            event.skip()

    # AGT 2004/10/03
    # why have this here - just do in top level ???
    # but keep this here as a placeholder to remind me to change it
    def becomeFocus(self):
        if self.documentPath:
            self.topLevelParent.setTitleBar(self.documentPath)
        else:
            self.topLevelParent.setTitleBar("")
            

        
# This is no longer a stand-alone - need to add a simple wrapper to test

#if __name__ == '__main__':
    #app = model.Application(CodePage)
    #app.MainLoop()
