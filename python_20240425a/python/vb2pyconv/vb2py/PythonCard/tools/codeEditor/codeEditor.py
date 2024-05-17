#!/usr/bin/env python
"""
__version__ = "$Revision: 1.126 $"
__date__ = "$Date: 2005/12/19 23:18:04 $"

PythonCard Editor (codeEditor) wiki page
http://wiki.wxpython.org/index.cgi/PythonCardEditor

wxStyledTextCtrl documentation
http://wiki.wxpython.org/index.cgi/wxStyledTextCtrl
"""

from PythonCard import about, configuration, dialog, log, menu, model, resource, util
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

# KEA 2004-07-22
# force imports for components used in .rsrc.py file
# so we can do a make standalones with py2exe and bundlebuilder
from PythonCard.components import codeeditor

USERCONFIG = 'user.config.txt'

# KEA 2002-05-03
# this could be more sophisticated
# by using an external source code colorizer
# or Scintillas over lexical analyzer?!
def textToHtml(source):
    """Return text converted to HTML."""
    # KEA 2003-08-07
    # how should we deal with Unicode?
    source = source.encode('iso-8859-1')
    output = cStringIO.StringIO()
    colorizer.Parser(source, output).format(None, None)
    html = output.getvalue()
    return html


# KEA doc handling adapted from python_docs 
# method in IDLE EditorWindow.py

pythoncard_url = util.documentationURL("documentation.html")
shell_url = util.documentationURL("shell.html")

help_url = "http://docs.python.org/"
if sys.platform.startswith("win"):
    fn = os.path.dirname(os.__file__)
    fn = os.path.join(fn, os.pardir, "Doc", "index.html")
    fn = os.path.normpath(fn)
    if os.path.isfile(fn):
        help_url = fn
    del fn
elif sys.platform == 'darwin':
    fn = '/Library/Frameworks/Python.framework/Versions/' + \
        'Current/Resources/Python.app/Contents/Resources/English.lproj/' + \
        'PythonDocumentation/index.html'
    if os.path.exists(fn):
        help_url = "file://" + fn


class CodeEditor(model.Background):
    
    def on_initialize(self, event):
        self.initSizers()

        self.setDefaultStyles()

        # KEA 2002-05-08
        # wxFileHistory isn't wrapped, so use raw wxPython
        # the file history is not actually saved when you quit
        # or shared between windows right now
        # also the file list gets appended to the File menu
        # rather than going in front of the Exit menu
        # I suspect I have to add the Exit menu after the file history
        # which means changing how the menus in resources are loaded
        # so I'll do that later
        self.fileHistory = wx.FileHistory()
        fileMenu = self.GetMenuBar().GetMenu(0)
        self.fileHistory.UseMenu(fileMenu)
        wx.EVT_MENU_RANGE(self, wx.ID_FILE1, wx.ID_FILE9, self.OnFileHistory)

        self.lastStatus = None
        self.lastPos = None
        #self.configPath = os.path.abspath(os.curdir)
        self.configPath = os.path.join(configuration.homedir, 'codeeditor')
        self.loadConfig()
        self.cmdLineArgs = {'debugmenu':False, 'logging':False, 'messagewatcher':False,
                            'namespaceviewer':False, 'propertyeditor':False,
                            'shell':False, 'otherargs':''}
        self.lastFind = {'searchText':'', 'replaceText':'', 'wholeWordsOnly':False, 'caseSensitive':False}
        self.startTitle = self.title
        if len(sys.argv) > 1:
            # accept a file argument on the command-line
            filename = os.path.abspath(sys.argv[1])
            log.info('codeEditor filename: ' + filename)
            if not os.path.exists(filename):
                filename = os.path.abspath(os.path.join(self.application.startingDirectory, sys.argv[1]))
            #print filename
            if os.path.isfile(filename):
                self.openFile(filename)
                # the second argument can be a line number to jump to
                # this is experimental, but a nice feature
                # KEA 2002-05-01
                # gotoLine causes the Mac to segfault
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

        # KEA 2002-05-08
        # wxSTC defaults will eventually be settable via a dialog
        # and saved in a user config, perhaps compatible with IDLE
        # or Pythonwin
        self.components.document.SetEdgeColumn(75)

        # KEA 2002-05-08
        # the wxFindReplaceDialog is not wrapped
        # so this is an experiment to see how it works
        wx.EVT_COMMAND_FIND(self, -1, self.OnFind)
        wx.EVT_COMMAND_FIND_NEXT(self, -1, self.OnFind)
        wx.EVT_COMMAND_FIND_REPLACE(self, -1, self.OnFind)
        wx.EVT_COMMAND_FIND_REPLACE_ALL(self, -1, self.OnFind)
        wx.EVT_COMMAND_FIND_CLOSE(self, -1, self.OnFindClose)

        self.visible = True
        self.loadShell()


    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.components.document, 1, wx.EXPAND)

        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def on_idle(self, event):
        self.updateTitleBar()
        self.updateStatusBar()

    def updateStatusBar(self):
        if self.documentPath:
            path = self.documentPath
        else:
            path = self.resource.strings.untitled
        pos = self.components.document.GetCurrentPos()
        newText = "File: %s  |  Line: %d  |  Column: %d" % \
            (path,
            self.components.document.LineFromPosition(pos) + 1,
            self.components.document.GetColumn(pos) + 1)
        if self.lastPos != pos and self.lastStatus != newText:
            self.statusBar.text = newText
            self.lastStatus = newText
            self.lastPos = pos

    def updateTitleBar(self):
        title = self.title
        modified = self.components.document.GetModify()
        if modified and title[0] != '*':
            self.title = '* ' + title + ' *'
        elif not modified and title[0] == '*':
            self.title = title[2:-2]
        

    # these are event handlers bound above
    # since they aren't automatically bound by PythonCard
    # I used the wxPython naming conventions
    # these methods will eventually be converted

    # KEA 2002-05-08
    # this is adapted from the wxPython demo
    def OnFind(self, event):
        map = {
            wx.wxEVT_COMMAND_FIND : "FIND",
            wx.wxEVT_COMMAND_FIND_NEXT : "FIND_NEXT",
            wx.wxEVT_COMMAND_FIND_REPLACE : "REPLACE",
            wx.wxEVT_COMMAND_FIND_REPLACE_ALL : "REPLACE_ALL",
            }
        et = event.GetEventType()

        try:
            evtType = map[et]
        except KeyError:
            evtType = "**Unknown Event Type**"

        self.lastFind['searchText'] = event.GetFindString()
        flags = event.GetFlags()
        self.lastFind['wholeWordsOnly'] = flags & wx.FR_WHOLEWORD != 0
        self.lastFind['caseSensitive'] = flags & wx.FR_MATCHCASE != 0
        
        if et == wx.wxEVT_COMMAND_FIND_REPLACE or et == wx.wxEVT_COMMAND_FIND_REPLACE_ALL:
            replaceTxt = "Replace text: " + event.GetReplaceString()
            self.lastFind['replaceText'] = event.GetReplaceString()
        else:
            replaceTxt = ""

        #print "%s -- Find text: %s  %s  Flags: %d  \n" % (evtType, event.GetFindString(), replaceTxt, event.GetFlags())

        if et == wx.wxEVT_COMMAND_FIND or et == wx.wxEVT_COMMAND_FIND_NEXT:
            self.findNext(self.lastFind['searchText'],
                          self.lastFind['wholeWordsOnly'],
                          self.lastFind['caseSensitive'])
        elif et == wx.wxEVT_COMMAND_FIND_REPLACE:
            # the way Notepad works
            # pressing Replace causes a Find Next
            # if there is no selection
            # if the text that is selected matches
            # the search criteria, then it is replaced
            # and a Find Next occurs
            doc = self.components.document
            txt = doc.GetSelectedText()
            sel = doc.GetSelection()
            if self.lastFind['searchText'].lower() == txt.lower():
                # since we don't know criteria for word boundaries
                # let wxSTC do the searching
                doc.SetCurrentPos(doc.GetSelectionStart())
            result = self.findNext(self.lastFind['searchText'],
                                   self.lastFind['wholeWordsOnly'],
                                   self.lastFind['caseSensitive'])
            if result != -1 and sel == doc.GetSelection():
                replaceText = self.lastFind['replaceText']
                doc.ReplaceSelection(replaceText)
                pos = doc.GetCurrentPos()
                doc.SetSelection(pos - len(replaceText), pos)
                result = self.findNext(self.lastFind['searchText'],
                                       self.lastFind['wholeWordsOnly'],
                                       self.lastFind['caseSensitive'])
        elif et == wx.wxEVT_COMMAND_FIND_REPLACE_ALL:
            self.replaceAll(self.lastFind['searchText'],
                            self.lastFind['replaceText'],
                            self.lastFind['wholeWordsOnly'],
                            self.lastFind['caseSensitive'])

    # search/replace from current position
    def replaceAll(self, searchText, replaceText, wholeWordsOnly, caseSensitive):
        # unless there is a built-in method for Replace All
        # we need to brute force this search
        doc = self.components.document
        pos = doc.GetCurrentPos()
        sel = doc.GetSelection()
        doc.SetCurrentPos(0)
        # should we handle this replace all operation as a single
        # undoable operation?
        replaced = 0
        while -1 != self.findNext(searchText,
                                  wholeWordsOnly,
                                  caseSensitive):
            doc.ReplaceSelection(replaceText)
            replaced += 1
        self.statusBar.text = self.resource.strings.replaced % replaced
        self.lastPos = self.components.document.GetCurrentPos()
        if not replaced:
            # restore previous position and selection
            doc.SetSelection(sel[0], sel[1])
            doc.SetCurrentPos(pos)

    def replaceTabs(self):
        """Replace tabs with four spaces."""
        self.replaceAll('\t', '    ', 0, 0)

    def OnFindClose(self, event):
        event.GetDialog().Destroy()

    def OnFileHistory(self, event):
        fileNum = event.GetId() - wx.ID_FILE1
        path = self.fileHistory.GetHistoryFile(fileNum)
        if self.components.document.GetModify():
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


    # back to PythonCard methods

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
        
    def loadConfig(self):
        try:
            if not os.path.exists(self.configPath):
                os.mkdir(self.configPath)
            path = os.path.join(self.configPath, USERCONFIG)
            self.config = util.readAndEvalFile(path)
            if self.config != {}:
                if 'position' in self.config:
                    self.position = self.config['position']
                if 'size' in self.config:
                    self.size = self.config['size']
                if 'history' in self.config:
                    history = self.config['history']
                    history.reverse()
                    for h in history:
                        self.fileHistory.AddFileToHistory(h)
                if 'view_white_space' in self.config:
                    self.components.document.SetViewWhiteSpace(self.config['view_white_space'])
                    self.menuBar.setChecked('menuViewWhitespace', self.config['view_white_space'])
                if 'indentation_guides' in self.config:
                    self.components.document.SetIndentationGuides(self.config['indentation_guides'])
                    self.menuBar.setChecked('menuViewIndentationGuides', self.config['indentation_guides'])
                if 'right_edge_guide' in self.config:
                    self.components.document.SetEdgeMode(self.config['right_edge_guide'])
                    self.menuBar.setChecked('menuViewRightEdgeIndicator', self.config['right_edge_guide'])
                if 'view_EOL' in self.config:
                    self.components.document.SetViewEOL(self.config['view_EOL'])
                    self.menuBar.setChecked('menuViewEndOfLineMarkers', self.config['view_EOL'])
                if 'line_numbers' in self.config:
                    self.components.document.lineNumbersVisible = self.config['line_numbers']
                    self.menuBar.setChecked('menuViewLineNumbers', self.config['line_numbers'])
                if 'folding' in self.config:
                    self.components.document.codeFoldingVisible = self.config['folding']
                    self.menuBar.setChecked('menuViewCodeFolding', self.config['folding'])

                if 'macros' in self.config:
                    self.macros = self.config['macros']
                    # should match based on name instead
                    m = self.menuBar.menus[4]
                    rsrc = resource.Resource({'type':'MenuItem', 'name': 'scriptletSep2', 'label':'-'})
                    mi = menu.MenuItem(self, m, rsrc)
                    m.appendMenuItem(mi)
                    for macro in self.macros:
                        #print 'm', macro
                        if macro['key'] == '':
                            key = ''
                        else:
                            key = '\t' + macro['key']
                        rsrc = resource.Resource({'type':'MenuItem',
                            'name': 'menuScriptlet' + macro['label'], 
                            'label': macro['label'] + key,
                            'command':'runMacro'})
                        mi = menu.MenuItem(self, m, rsrc)
                        m.appendMenuItem(mi)

        except:
            self.config = {}

    def saveConfig(self):
        self.config['position'] = self.GetRestoredPosition()
        self.config['size'] = self.GetRestoredSize()
        self.config['view_white_space'] = self.components.document.GetViewWhiteSpace()
        self.config['indentation_guides'] = self.components.document.GetIndentationGuides()
        self.config['right_edge_guide'] = self.components.document.GetEdgeMode()
        self.config['view_EOL'] = self.components.document.GetViewEOL()
        self.config['line_numbers'] = self.components.document.lineNumbersVisible
        self.config['folding'] = self.components.document.codeFoldingVisible
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
            filename = self.resource.strings.untitled
        else:
            filename = self.documentPath
        msg = self.resource.strings.documentChangedPrompt % filename
        result = dialog.messageDialog(self, msg, self.resource.strings.codeEditor,
                                   wx.ICON_EXCLAMATION | wx.YES_NO | wx.CANCEL)
        return result.returnedString

    def doExit(self):
        if self.components.document.GetModify():
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
            try:
                # KEA 2004-04-08
                # if an exception occurs during on_initialize
                # then saveConfig could fail because some windows
                # might not exist, so in that situation just exit gracefully
                self.saveConfig()
            except:
                pass
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
        #wildcard = "Python scripts (*.py;*.pyw)|*.py;*.pyw|Text files (*.txt)|*.txt|All files (*.*)|*.*"
        wildcard = self.resource.strings.saveAsWildcard
        if self.documentPath is None:
            dir = ''
            filename = '*.py'
        else:
            dir = os.path.dirname(self.documentPath)
            filename = os.path.basename(self.documentPath)
        result = dialog.saveFileDialog(None, self.resource.strings.saveAs, dir, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            self.saveFile(path)
            self.fileHistory.AddFileToHistory(path)
            return True
        else:
            return False

    def newFile(self):
        self.components.document.text = ''
        self.documentPath = None
        self.setEditorStyle()
        self.components.document.SetSavePoint()
        self.title = self.resource.strings.untitled + ' - ' + self.startTitle
        #self.statusBar.text = self.resource.strings.untitled
        self.lastStatus = None
        # KEA 2003-07-26
        # reset EOL to match platform
        # this may not actually be what the user expects
        # so perhaps this should be an option in a dialog?!
        self.autoSetEOL()

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
            self.title = os.path.split(path)[-1] + ' - ' + self.startTitle
            #self.statusBar.text = path
            self.lastStatus = None
            self.fileHistory.AddFileToHistory(path)
            # KEA 2002-06-29
            # just as a test, let's see how the XML and/or HTML styles
            # look
            self.setEditorStyle()
            self.autoSetEOL()
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
            self.title = os.path.split(path)[-1] + ' - ' + self.startTitle
            #self.statusBar.text = path
            self.lastStatus = None
            self.setEditorStyle()
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

    # File menu
    
    # KEA 2002-05-04
    # need to decide on UI for multiple windows
    # New Window, Open in New Window, New, Open, etc.
    # since we aren't doing MDI
    # we could have child windows, but what would the organization be?!
    def on_menuFileNewWindow_select(self, event):
        app = os.path.split(sys.argv[0])[-1]
        filename = os.path.join(self.application.applicationDirectory, app)
        python = sys.executable
        if ' ' in python:
            pythonQuoted = '"' + python + '"'
        else:
            pythonQuoted = python
        os.spawnv(os.P_NOWAIT, python, [pythonQuoted, filename])
        # for this to work, all the windows need to share a common list of windows
        # a File->Exit would iterate through each?
        """
        path = os.path.join(self.application.applicationDirectory, 'codeEditor')
        rsrc = resource.ResourceFile(model.internationalResourceName(path)).getResource()
        self.childWindow = CodeEditor(self, rsrc.application.backgrounds[0])
        """

    def on_menuFileNew_select(self, event):
        if self.components.document.GetModify():
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
        if self.components.document.GetModify():
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
        #wildcard = "Python scripts (*.py;*.pyw)|*.py;*.pyw|Text files (*.txt)|*.txt|All files (*.*)|*.*"
        wildcard = self.resource.strings.saveAsWildcard
        result = dialog.openFileDialog(None, self.resource.strings.openFile, '', '', wildcard)
        if result.accepted:
            path = result.paths[0]
            # an error will probably occur here if the text is too large
            # to fit in the wxTextCtrl (TextArea) or the file is actually
            # binary. Not sure what happens with CR/LF versus CR versus LF
            # line endings either
            self.openFile(path)


        
    def on_menuFilePrint_select(self, event):
        source = textToHtml(self.components.document.text)
        self.printer.PrintText(source)

    def on_menuFilePrintPreview_select(self, event):
        source = textToHtml(self.components.document.text)
        self.printer.PreviewText(source)

    def on_menuFilePageSetup_select(self, event):
        self.printer.PageSetup()


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


    def findNext(self, searchText, wholeWordsOnly, caseSensitive):
        if searchText == '':
            return -1

        doc = self.components.document
        current = doc.GetCurrentPos()
        last = doc.GetLength()
        if wx.VERSION >= (2, 3, 3):
            flags = 0
            if caseSensitive:
                flags = flags + stc.STC_FIND_MATCHCASE
            if wholeWordsOnly:
                flags = flags + stc.STC_FIND_WHOLEWORD
            result = doc.FindText(current, last, searchText, flags)
        else:
            result = doc.FindText(current, last, searchText,
                         caseSensitive,
                         wholeWordsOnly)
        if result != -1:
            # update the selection, which also changes the cursor position
            n = len(searchText)
            doc.SetSelection(result, result + n)
        else:
            # should we beep or flash the screen or present an error dialog?
            pass
        return result


    def on_doEditFindReplace_command(self, event):
        data = wx.FindReplaceData()
        flags = data.GetFlags()
        data.SetFindString(self.lastFind['searchText'])
        data.SetReplaceString(self.lastFind['replaceText'])
        if self.lastFind['wholeWordsOnly']:
            flags = flags | wx.FR_WHOLEWORD
        if self.lastFind['caseSensitive']:
            flags = flags | wx.FR_MATCHCASE
        data.SetFlags(flags)
        dlg = wx.FindReplaceDialog(self, data, "Find & Replace", wx.FR_REPLACEDIALOG)
        dlg.data = data  # save a reference to it...
        # KEA 2004-04-18
        # can't use visible attribute
        # probably need to create a wrapper for FindReplaceDialog
        # to make it more like PythonCard
        #dlg.visible = True
        dlg.Show()

    def on_doEditReplaceTabs_command(self, event):
        self.replaceTabs()
        
    def on_doEditFind_command(self, event):
        # keep track of the last find and preload
        # the search text and radio buttons
        lastFind = self.lastFind

        result = dialog.findDialog(self, lastFind['searchText'],
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
        
    def gotoLine(self, lineNumber):
        try:
            # GotoLine is zero based, but we ask the user
            # for a line number starting at 1
            self.components.document.GotoLine(lineNumber - 1)
        except:
            pass
        
    def on_doEditGoTo_command(self, event):
        result = dialog.textEntryDialog(self, self.resource.strings.gotoLineNumber, self.resource.strings.gotoLine, '')
        # this version doesn't alert the user if the line number is out-of-range
        # it just fails quietly
        if result.accepted:
            try:
                self.gotoLine(int(result.text))
            except:
                pass

    def on_indentRegion_command(self, event):
        self.components.document.CmdKeyExecute(stc.STC_CMD_TAB)

    def on_dedentRegion_command(self, event):
        self.components.document.CmdKeyExecute(stc.STC_CMD_BACKTAB)

    def on_commentRegion_command(self, event):
        # need to do the equivelant of the IDLE
        # comment_region_event in AutoIndent.py
        doc = self.components.document
        sel = doc.GetSelection()
        start = doc.LineFromPosition(sel[0])
        end = doc.LineFromPosition(sel[1])
        if end > start and doc.GetColumn(sel[1]) == 0:
            end = end - 1

        doc.BeginUndoAction()
        for lineNumber in range(start, end + 1):
            firstChar = doc.PositionFromLine(lineNumber)
            doc.InsertText(firstChar, '##')
        doc.SetCurrentPos(doc.PositionFromLine(start))
        doc.SetAnchor(doc.GetLineEndPosition(end))
        doc.EndUndoAction()

    def on_uncommentRegion_command(self, event):
        # need to do the equivelant of the IDLE
        # uncomment_region_event in AutoIndent.py
        doc = self.components.document
        sel = doc.GetSelection()
        start = doc.LineFromPosition(sel[0])
        end = doc.LineFromPosition(sel[1])
        if end > start and doc.GetColumn(sel[1]) == 0:
            end = end - 1

        doc.BeginUndoAction()
        for lineNumber in range(start, end + 1):
            firstChar = doc.PositionFromLine(lineNumber)
            if chr(doc.GetCharAt(firstChar)) == '#':
                if chr(doc.GetCharAt(firstChar + 1)) == '#':
                    # line starts with ##
                    doc.SetCurrentPos(firstChar + 2)
                else:
                    # line starts with #
                    doc.SetCurrentPos(firstChar + 1)
                doc.DelLineLeft()

        doc.SetCurrentPos(doc.PositionFromLine(start))
        doc.SetAnchor(doc.GetLineEndPosition(end))
        doc.EndUndoAction()


    # View menu
    
    def on_menuViewWhitespace_select(self, event):
        self.components.document.SetViewWhiteSpace(event.IsChecked())

    def on_menuViewIndentationGuides_select(self, event):
        self.components.document.SetIndentationGuides(event.IsChecked())

    def on_menuViewRightEdgeIndicator_select(self, event):
        if event.IsChecked():
            self.components.document.SetEdgeMode(stc.STC_EDGE_LINE)
            #self.components.document.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        else:
            self.components.document.SetEdgeMode(stc.STC_EDGE_NONE)

    def on_menuViewEndOfLineMarkers_select(self, event):
        self.components.document.SetViewEOL(event.IsChecked())

    def on_menuViewFixedFont_select(self, event):
        pass

    def on_menuViewLineNumbers_select(self, event):
        self.components.document.lineNumbersVisible = event.IsChecked()

    def on_menuViewCodeFolding_select(self, event):
        self.components.document.codeFoldingVisible = event.IsChecked()


    # Format menu

    def on_doSetStyles_command(self, event):
        config = configuration.getStyleConfigPath()
        if config is None:
            return

        cwd = os.curdir
        os.chdir(os.path.dirname(config))
        dlg = STCStyleEditor.STCStyleEditDlg(self, 
            'Python', 'python',
            #'HTML', 'html',
            #'XML', 'xml',
            #'C++', 'cpp',  
            #'Text', 'text',  
            #'Properties', 'prop',  
            config)
        try: dlg.ShowModal()
        finally: dlg.Destroy()
        os.chdir(cwd)
        self.setDefaultStyles()

    def on_menuFormatWrap_select(self, event):
        self.components.document.SetWrapMode(event.IsChecked())



    def wordCount(self, text):
        chars = len(text)
        words = len(text.split())
        # this doesn't always match the getNumberOfLines() method
        # so this should probably be changed
        lines = len(util.normalizeEOL(text).split('\n'))
        return chars, words, lines

    # Help menu
    
    def on_doHelpAbout_command(self, event):
        # once we have generic dialogs going, put a more interesting
        # About box here
        if self.documentPath is None:
            filename = self.resource.strings.untitled
        else:
            filename = os.path.basename(self.documentPath)
        countString = "%d " + self.resource.strings.chars + \
            ", %d " + self.resource.strings.words + \
            ", %d " + self.resource.strings.lines
        dialog.messageDialog(self,
                             self.resource.strings.sample + "\n\n" + \
                             self.resource.strings.document + ": %s\n" % filename + \
                             countString \
                             % self.wordCount(self.components.document.text),
                             self.resource.strings.about,
                             wx.ICON_INFORMATION | wx.OK)

    def on_doHelpAboutPythonCard_command(self, event):
        about.aboutPythonCardDialog(self)

    def on_menuScriptletShell_select(self, event):
        self.loadShell()

        if self.application.shell is not None:
            self.application.shellFrame.visible = not self.application.shellFrame.visible

    def on_menuScriptletNamespace_select(self, event):
        self.loadNamespace()

        if self.application.namespace is not None:
            self.application.namespaceFrame.visible = not self.application.namespaceFrame.visible

    def on_menuScriptletSaveUserConfiguration_select(self, event):
        configuration.saveUserConfiguration(self.application)
        
    def on_menuShellChangeDirectory_select(self, event):
        try:
            if self.documentPath:
                path = os.path.dirname(self.documentPath)
            else:
                path = ''
            result = dialog.directoryDialog(self, 'Choose a directory', path)
            if result.accepted:
                path = result.path
                os.chdir(path)
                self.application.shell.run('os.getcwd()')
        except:
            pass

    def on_menuScriptletSaveShellSelection_select(self, event):
        if self.application.shell is not None:
            txt = self.application.shell.GetSelectedText()
            lines = []
            for line in txt.splitlines():
                lines.append(self.application.shell.lstripPrompt(line))
            # this is the quick way to convert a list back into a string
            # appending to strings can be slow because it creates a new string
            # each time, so a list is used instead while building up the script
            script = '\n'.join(lines)
            try:
                #wildcard = "Python files (*.py)|*.py|All Files (*.*)|*.*"
                wildcard = self.resource.strings.scriptletWildcard
                scriptletsDir = os.path.join(self.application.applicationDirectory, 'scriptlets')
                result = dialog.saveFileDialog(None, self.resource.strings.saveAs, scriptletsDir, 'scriptlet.py', wildcard)
                if result.accepted:
                    path = result.paths[0]
                    f = open(path, 'w')
                    f.write(script)
                    f.close()
            except:
                pass

    def execScriptlet(self, filename):
        try:
            command = 'execfile(%r)' % filename
            self.application.shell.run(command=command, prompt=0, verbose=0)
        except:
            pass

    def on_menuScriptletRunScriptlet_select(self, event):
        self.loadShell()

        #curDir = os.getcwd()
        if self.application.shell is not None:
            #wildcard = "Python files (*.py)|*.py|All Files (*.*)|*.*"
            wildcard = self.resource.strings.scriptletWildcard
            # wildcard = '*.py'
            scriptletsDir = os.path.join(self.application.applicationDirectory, 'scriptlets')
            result = dialog.openFileDialog(self, self.resource.strings.openFile, scriptletsDir, '', wildcard)
            if result.accepted:
                filename = result.paths[0]
                self.execScriptlet(filename)
        #os.chdir(curDir)

    """
>>> mb = bg.menuBar
>>> m = mb.menus[4]
>>> from PythonCard import menu, resource
>>> rsrc = resource.Resource({'type':'MenuItem', 'name': 'scriptletSep2', 'label':'-'})
>>> mi = menu.MenuItem(bg, m, rsrc)
>>> m.appendMenuItem(mi)
>>> rsrc = resource.Resource({'type':'MenuItem', 'name': 'menuScriptletinsertDateAndTime', 'label':'insertDateAndTime\tCtrl+1', 'command':'runMacro'})
>>> mi = menu.MenuItem(bg, m, rsrc)
>>> m.appendMenuItem(mi)

    """
    """
    Need to have a "Macros" dialog that let's the user select a script to
    run, a label for the script which will default to the script name,
    and a hot key. The dialog will prepend menuScriptlet on the front,
    add the item to the menu and store it in the config so it is remembered
    between loads.
    """
    def on_runMacro_command(self, event):
        name = event.target.name[len('menuScriptlet'):]
        #scriptletsDir = os.path.join(self.application.applicationDirectory, 'scriptlets')
        #filename = os.path.join(scriptletsDir, name + '.py')
        for macro in self.macros:
            if macro['label'] == name:
                filename = macro['filename']
                self.execScriptlet(filename)
                break
    
    # KEA 2002-05-04
    # need to experiment to determine when skip()
    # must be called and when to avoid it when we
    # want to eat and process key presses ourselves
    # also are the wxEVT_STC_ different than the plain
    # EVT_CHAR, EVT_KEY_DOWN ???
    #
    # from binding.py
    # aWxEvent.altDown = aWxEvent.AltDown()
    # aWxEvent.controlDown = aWxEvent.ControlDown()
    # aWxEvent.shiftDown = aWxEvent.ShiftDown()
    # aWxEvent.keyCode = aWxEvent.GetKeyCode()


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

    def on_checkSyntax_command(self, event):
        if self.documentPath is None:
            save = self.saveChanges()
            if save == "Cancel" or save == "No":
                # don't do anything, just go back to editing
                # we have to have a file on disk to check
                # if we used StringIO we could simulate a file
                # but I don't know if it is worth it
                pass
            else:
                if self.on_menuFileSaveAs_select(None):
                    scriptutils.CheckFile(self, self.documentPath)
                    self.lastPos = self.components.document.GetCurrentPos()
        else:
            if self.components.document.GetModify():
                # auto-save
                self.saveFile(self.documentPath)
            scriptutils.CheckFile(self, self.documentPath)
            self.lastPos = self.components.document.GetCurrentPos()
    
    def on_fileRunOptions_command(self, event):
        result = runOptionsDialog.runOptionsDialog(self, self.cmdLineArgs)
        if result.accepted:
            self.cmdLineArgs['debugmenu'] = result.debugmenu
            self.cmdLineArgs['logging'] = result.logging
            self.cmdLineArgs['messagewatcher'] = result.messagewatcher
            self.cmdLineArgs['namespaceviewer'] = result.namespaceviewer
            self.cmdLineArgs['propertyeditor'] = result.propertyeditor
            self.cmdLineArgs['shell'] = result.shell
            self.cmdLineArgs['otherargs'] = result.otherargs


    # script running code
    
    def runScript(self, useInterpreter):
        if self.documentPath is None:
            save = self.saveChanges()
            if save == "Cancel" or save == "No":
                # don't do anything, just go back to editing
                return
            else:
                if not self.on_menuFileSaveAs_select(None):
                    # they didn't actually save, just go back
                    # to editing
                    return
        elif self.components.document.GetModify():
            # auto-save
            self.saveFile(self.documentPath)

        # this algorithm, taken from samples.py assumes the rsrc.py file and the main
        # program file have the same basename
        # if that isn't the case then this doesn't work and we need a different solution
        path, filename = os.path.split(self.documentPath)
        if wx.Platform == '__WXMAC__':
            filename = self.documentPath
        else:
            if ' ' in self.documentPath:
                filename = '"' + self.documentPath + '"'
            else:
                filename = self.documentPath

        # the args should come from a dialog or menu items that are checked/unchecked
        args = util.getCommandLineArgs(self.cmdLineArgs)

        # change to the script directory before attempting to run
        curdir = os.path.dirname(os.path.abspath(os.curdir))
        os.chdir(os.path.dirname(self.documentPath))

        if wx.Platform == '__WXMAC__':
            # this is a bad hack to deal with the user starting
            # codeEditor.py from the Finder
            if sys.executable == '/':
                python = '/Applications/Python.app/Contents/MacOS/python'
            else:
                python = sys.executable
        elif wx.Platform == '__WXMSW__':
            # always launch with a console
            python = os.path.join(os.path.dirname(sys.executable), 'python.exe')
        else:
            python = sys.executable
        if ' ' in python:
            pythonQuoted = '"' + python + '"'
        else:
            pythonQuoted = python

        if useInterpreter:
            os.spawnv(os.P_NOWAIT, python, [pythonQuoted, '-i', filename] + args)
        else:
            os.spawnv(os.P_NOWAIT, python, [pythonQuoted, filename] + args)

        os.chdir(curdir)

    def on_fileRun_command(self, event):
        # KEA 2001-12-14
        # we should prompt to save the file if needed
        # or in the case of a new file, do a save as before attempting
        # to do a run
        self.runScript(0)

    def on_fileRunWithInterpreter_command(self, event):
        # KEA 2001-12-14
        # we should prompt to save the file if needed
        # or in the case of a new file, do a save as before attempting
        # to do a run
        self.runScript(1)

    def on_findFiles_command(self, event):
        fn = self.application.applicationDirectory
        fn = os.path.join(fn, os.pardir, "findfiles", "findfiles.py")
        fn = os.path.normpath(fn)
        if not os.path.isfile(fn):
            return

        if wx.Platform == '__WXMAC__':
            filename = fn
        else:
            filename = '"' + fn + '"'

        if wx.Platform == '__WXMAC__':
            # this is a bad hack to deal with the user starting
            # codeEditor.py from the Finder
            if sys.executable == '/':
                python = '/Applications/Python.app/Contents/MacOS/python'
            else:
                python = sys.executable
        elif wx.Platform == '__WXMSW__':
            python = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        else:
            python = sys.executable
        if ' ' in python:
            pythonQuoted = '"' + python + '"'
        else:
            pythonQuoted = python

        os.spawnv(os.P_NOWAIT, python, [pythonQuoted, filename])

    def on_showShellDocumentation_command(self, event):
        global shell_url
        webbrowser.open(shell_url)

    def on_showPythonCardDocumentation_command(self, event):
        global pythoncard_url
        webbrowser.open(pythoncard_url)

    def on_showPythonDocumentation_command(self, event):
        global help_url

        if sys.platform.startswith("win"):
        # KEA 2003-10-15   AGT 2005-12-20
        # BIG hack for Python 2.3 Windows help file (or Python 2.4)
        # need to decide on a clean way of handling various doc options
            fn = os.path.dirname(os.__file__)
            chmfile = "Python" + sys.version[0] + sys.version[2] + ".chm"
            fn = os.path.join(fn, os.pardir, "Doc", chmfile)
            fn = os.path.normpath(fn)
            if os.path.isfile(fn):
                os.startfile(fn)
        else:
            webbrowser.open(help_url)


# KEA 2004-08-18
# I'll probably move this functionality into model.Application
# and just call a macOpenFile method in the current background
class MyApplication(model.Application):
    # support drag and drop on the application icon on the Mac
    def MacOpenFile(self, filename):
        # code to load filename goes here
        self.backgrounds[0].openFile(filename)


if __name__ == '__main__':
    app = MyApplication(CodeEditor)
    app.MainLoop()
