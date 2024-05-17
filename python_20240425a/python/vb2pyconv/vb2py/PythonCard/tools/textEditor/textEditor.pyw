#!/usr/bin/python

"""
__version__ = "$Revision: 1.76 $"
__date__ = "$Date: 2004/09/30 23:59:06 $"

I had noticed before that selecting a menu item wipes out the contents of the
status bar, but I had forgotten about it. I need to investigate this. I'm
assuming some sort of help tip is supposed to be displayed?!

Other ideas without turning this into a full blown editor
  insert time/date stamp like notepad.exe in Windows

"""

from PythonCard import configuration, dialog, log, model, resource, util
from PythonCard.templates.dialogs import findDialog
import os, sys
import wx
from wx.html import HtmlEasyPrinting
import pprint

USERCONFIG = 'user.config.txt'

def textToHtml(txt):
    # the wxHTML classes don't require valid HTML
    # so this is enough
    html = txt.replace('\n\n', '<P>')
    html = html.replace('\n', '<BR>')
    return html


class TextEditor(model.Background):
    
    def on_initialize(self, event):
        self.singleItemExpandingSizerLayout()

        # KEA 2002-06-27
        # copied from codeEditor.py
        # wxFileHistory isn't wrapped, so use raw wxPython
        # also the file list gets appended to the File menu
        # rather than going in front of the Exit menu
        # I suspect I have to add the Exit menu after the file history
        # which means changing how the menus in resources are loaded
        # so I'll do that later
        self.fileHistory = wx.FileHistory()
        fileMenu = self.GetMenuBar().GetMenu(0)
        self.fileHistory.UseMenu(fileMenu)
        wx.EVT_MENU_RANGE(self, wx.ID_FILE1, wx.ID_FILE9, self.OnFileHistory)

        self.configPath = os.path.join(configuration.homedir, 'texteditor')
        self.loadConfig()
        self.lastFind = {'searchText':'', 'wholeWordsOnly':0, 'caseSensitive':0}
        self.startTitle = self.title
        if len(sys.argv) > 1:
            # accept a file argument on the command-line
            filename = os.path.abspath(sys.argv[1])
            log.info('textEditor filename: ' + filename)
            if not os.path.exists(filename):
                filename = os.path.abspath(os.path.join(self.application.startingDirectory, sys.argv[1]))
            #print filename
            if os.path.isfile(filename):
                self.openFile(filename)
                # the second argument can be a line number to jump to
                # this is experimental, but a nice feature
                if (len(sys.argv) > 2):
                    try:
                        line = int(sys.argv[2])
                        self.gotoLine(line)
                    except:
                        pass
            else:
                self.newFile()
        else:
            self.newFile()

        self.printer = HtmlEasyPrinting()

        self.visible = True


    def on_idle(self, event):
        self.updateTitleBar()

    def updateTitleBar(self):
        title = self.title
        modified = self.documentChanged
        if modified and title[0] != '*':
            self.title = '* ' + title + ' *'
        elif not modified and title[0] == '*':
            self.title = title[2:-2]

    def OnFileHistory(self, event):
        fileNum = event.GetId() - wx.ID_FILE1
        path = self.fileHistory.GetHistoryFile(fileNum)
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
        self.openFile(path)

    def loadConfig(self):
        try:
            if not os.path.exists(self.configPath):
                os.mkdir(self.configPath)
            path = os.path.join(self.configPath, USERCONFIG)
            self.config = util.readAndEvalFile(path)
            if self.config != {}:
                self.setDocumentFont()
                if 'position' in self.config:
                    self.position = self.config['position']
                if 'size' in self.config:
                    self.size = self.config['size']
                if 'history' in self.config:
                    history = self.config['history']
                    history.reverse()
                    for h in history:
                        self.fileHistory.AddFileToHistory(h)
        except:
            self.config = {}

    def saveConfig(self):
        self.config['defaultFont'] = self.components.fldDocument.font
        self.config['position'] = self.GetRestoredPosition()
        self.config['size'] = self.GetRestoredSize()
        history = []
        for i in range(self.fileHistory.GetCount()):
            history.append(self.fileHistory.GetHistoryFile(i))
        self.config['history'] = history
        try:
            path = os.path.join(self.configPath, USERCONFIG)
            f = open(path, "w")
            pprint.pprint(self.config, f)
            f.close()
        except:
            pass    # argh

    def saveChanges(self):
        # save configuration info in the app directory
        #filename = os.path.basename(self.documentPath)
        if self.documentPath is None:
            filename = "Untitled"
        else:
            filename = self.documentPath
        msg = "The text in the %s file has changed.\n\nDo you want to save the changes?" % filename
        result = dialog.messageDialog(self, msg, 'textEditor',
                                   wx.ICON_EXCLAMATION | wx.YES_NO | wx.CANCEL)
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
            return True

    def on_close(self, event):
        if self.doExit():
            self.saveConfig()
            self.fileHistory = None
            self.printer = None
            event.skip()

    def setDocumentFont(self):
        self.components.fldDocument.font = self.config['defaultFont']

    def on_doSetFont_command(self, event):
        result = dialog.fontDialog(self, self.components.fldDocument.font)
        if result.accepted:
            self.config['defaultFont'] = result.font
            self.setDocumentFont()

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
            self.fileHistory.AddFileToHistory(path)
            return True
        else:
            return False

    def on_fldDocument_textUpdate(self, event):
        self.documentChanged = True

    def newFile(self):
        self.components.fldDocument.text = ''
        self.documentPath = None
        self.documentChanged = 0
        self.title = 'Untitled - ' + self.startTitle
        self.statusBar.text = 'Untitled'

    def openFile(self, path):
        try:
            f = open(path)
            self.components.fldDocument.text = f.read().replace('\r\n','\n')
            f.close()
            self.documentPath = path
            self.documentChanged = 0
            self.title = os.path.split(path)[-1] + ' - ' + self.startTitle
            self.statusBar.text = path
            self.fileHistory.AddFileToHistory(path)
        except:
            pass

    def saveFile(self, path):
        try:
            f = open(path, 'w')
            f.write(self.components.fldDocument.text)
            f.close()
            self.documentPath = path
            self.documentChanged = 0
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
        source = textToHtml(self.components.fldDocument.text)
        self.printer.PrintText(source)

    def on_menuFilePrintPreview_select(self, event):
        source = textToHtml(self.components.fldDocument.text)
        self.printer.PreviewText(source)

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

    # end of searchexplorer edit menu items

    def findNext(self, searchText, wholeWordsOnly, caseSensitive):
        fldDocument = self.components.fldDocument
        selOffset = fldDocument.getSelection()[1]
        offset = util.findString(searchText, fldDocument.text[selOffset:],
            caseSensitive, wholeWordsOnly)
        
        if offset != -1:
            offset += selOffset
            fldDocument.setSelection(offset, offset + len(searchText))
            fldDocument.setFocus()

    def on_doEditFind_command(self, event):
        # keep track of the last find and preload
        # the search text and radio buttons
        lastFind = self.lastFind
        
        # two versions of Find, the first one is using the FindDialog
        # defined in dialog.py, the second one is using a FindDialog class
        # defined in templates.dialogs.findDialog
        # the second one is what you should base your own dialogs on
        """
        result = dialog.findDialog(self, lastFind['searchText'],
                                lastFind['wholeWordsOnly'],
                                lastFind['caseSensitive'])
        """

        result = findDialog.findDialog(self, lastFind['searchText'],
                        lastFind['wholeWordsOnly'],
                        lastFind['caseSensitive'])

        if result.accepted:
            lastFind['searchText'] = result.searchText
            lastFind['wholeWordsOnly'] = result.wholeWordsOnly
            lastFind['caseSensitive'] = result.caseSensitive

            self.findNext(lastFind['searchText'],
                          lastFind['wholeWordsOnly'],
                          lastFind['caseSensitive'])

    def on_doEditFindNext_command(self, event):
        self.findNext(self.lastFind['searchText'],
                      self.lastFind['wholeWordsOnly'],
                      self.lastFind['caseSensitive'])

    def findNth(self, pattern, n, txt):
        """find the nth occurance of pattern in txt and return the offset"""
        #print "findNth", pattern, n
        start = 0
        offset = -1
        i = 1
        while i <= n:
            offset = txt.find(pattern, start)
            #print 'offset', offset
            # if the pattern isn't found before the end of the text is reached
            # return -1
            if offset == -1:
                break
            start = offset + 1
            i = i + 1
        return offset
        
    def gotoLine(self, lineNumber):
        try:
            if lineNumber <= self.components.fldDocument.getNumberOfLines():
                if wx.Platform == '__WXGTK__':
                    sel = self.components.fldDocument.xyToPosition(0, lineNumber - 1)
                    self.components.fldDocument.setSelection(sel, sel)
                    self.components.fldDocument.setInsertionPoint(sel)
                else:
                    # windows wxTE_RICH style wraps lines, so we need to count
                    # newlines to get an offset
                    if lineNumber == 1:
                        self.components.fldDocument.setInsertionPoint(0)
                    else:
                        #offset = self.findNth('\n', lineNumber - 1, self.components.fldDocument.text)
                        offset = util.findnth(self.components.fldDocument.text, '\n', lineNumber - 1)
                        self.components.fldDocument.setInsertionPoint(offset + 1)
                    
        except:
            pass
        
    def on_doEditGoTo_command(self, event):
        result = dialog.textEntryDialog(self, 'Goto line number:', 'Goto line', '')
        # this version doesn't alert the user if the line number is out-of-range
        # it just fails quietly
        if result.accepted:
            try:
                self.gotoLine(int(result.text))
            except:
                pass

    def wordCount(self, text):
        chars = len(text)
        words = len(text.split())
        # this doesn't always match the getNumberOfLines() method
        # so this should probably be changed
        lines = len(text.split('\n'))
        return chars, words, lines

    def on_doHelpAbout_command(self, event):
        # once we have generic dialogs going, put a more interesting
        # About box here
        if self.documentPath is None:
            filename = 'Untitled'
        else:
            filename = os.path.basename(self.documentPath)
        dialog.messageDialog(self,
                                   'textEditor sample' + "\n\n" + \
                                   "Document: %s\n" % filename + \
                                   "%d chars, %d words, %d lines" \
                                   % self.wordCount(self.components.fldDocument.text),
                                   'About textEditor...',
                                   wx.ICON_INFORMATION | wx.OK)


    def on_menuScriptletShell_select(self, event):
        self.loadShell()

        if self.application.shell is not None:
            self.application.shellFrame.visible = not self.application.shellFrame.visible

    def on_menuScriptletSaveShellSelection_select(self, event):
        if self.application.shell is not None:
            txt = self.application.shell.GetSelectedText()
            lines = []
            for line in txt.splitlines():
                lines.append(self.application.shell.lstripPrompt(line))
            # this is the quick way to convert a list back into a string
            # appending to strings can be slow because it creates a new string
            # each time, so a list is used instead while building up the script
            script = "\n".join(lines)
            try:
                wildcard = "Python files (*.py)|*.py|All Files (*.*)|*.*"
                scriptletsDir = os.path.join(self.application.applicationDirectory, 'scriptlets')
                result = dialog.saveFileDialog(None, "Save As", scriptletsDir, 'scriptlet.py', wildcard)
                if result.accepted:
                    path = result.paths[0]
                    f = open(path, 'w')
                    f.write(script)
                    f.close()
            except:
                pass

    def on_menuScriptletRunScriptlet_select(self, event):
        self.loadShell()

        #curDir = os.getcwd()
        if self.application.shell is not None:
            wildcard = "Python files (*.py)|*.py|All Files (*.*)|*.*"
            # wildcard = '*.py'
            scriptletsDir = os.path.join(self.application.applicationDirectory, 'scriptlets')
            result = dialog.openFileDialog(self, 'Open', scriptletsDir, '', wildcard)
            if result.accepted:
                filename = result.paths[0]
                try:
                    command = 'execfile(%r)' % filename
                    self.application.shell.run(command=command, prompt=0, verbose=0)
                except:
                    pass
        #os.chdir(curDir)


if __name__ == '__main__':
    app = model.Application(TextEditor)
    app.MainLoop()
