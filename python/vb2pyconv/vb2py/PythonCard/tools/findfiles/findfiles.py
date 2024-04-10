#!/usr/bin/python

"""
KEA notes to myself

Created: 2001-07-25
__version__ = "$Revision: 1.86 $"
__date__ = "$Date: 2004/10/05 23:43:54 $"
__author__ = "Kevin Altis <altis@semi-retired.com>"

2002-06-11
converted from regex to re, see these helpful pages for more info
http://py-howto.sourceforge.net/regex-to-re/
http://py-howto.sourceforge.net/regex-to-re/node3.html

"""

import urllib
import webbrowser
import pprint
import os, sys
import re

from PythonCard import configuration, dialog, log, model, util
import wx

# KEA 2004-07-22
# force imports for components used in .rsrc.py file
# so we can do a make standalones with py2exe and bundlebuilder
from PythonCard.components import button, checkbox, combobox, list, statictext, textfield
LASTGREPFILE = 'findfiles.grep'
USERCONFIG = 'user.config.txt'

pythoncard_url = util.documentationURL("documentation.html")
findfiles_url = util.documentationURL("findfiles.html")

class FindFiles(model.Background):

    def on_initialize(self, event):
        self.dir = None
        self.documentPath = None
        self.documentChanged = 0
        
        # there should probably be a menu item to 
        # raise and lower the font size
        if wx.Platform in ('__WXMAC__', '__WXGTK__'):
            font = self.components.listResults.font
            if wx.Platform == '__WXMAC__':
                font.size = 10
            elif wx.Platform == '__WXGTK__':
                font.size = 12
            self.components.listResults.font = font

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

        self.sizerLayout()

        self.configPath = os.path.join(configuration.homedir, 'findfiles')
        self.loadConfig()

        path = os.path.join(self.configPath, LASTGREPFILE)
        self.loadGrepFile(path)


    def sizerLayout(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.FlexGridSizer(3, 4, 3, 10)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        stcSizerAttrs = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL         
        fldSizerAttrs = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL
        vertFlags = wx.LEFT | wx.TOP | wx.ALIGN_LEFT
        chkSizerAttrs = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL

        comp = self.components

        # sadly this doesn't look good on the Mac
        #w, h = comp.lblSearchFor.size
        #sizer3.Add((w + 10, 5), 0)  # spacer
        sizer3.Add((5, 5), 0)  # spacer
        sizer3.Add(comp.chkCaseSensitive, 0, chkSizerAttrs, 20)
        sizer3.Add(comp.chkSearchSubdirectories, 0, chkSizerAttrs, 20)
        #sizer3.Add(comp.chkVerbose, 0, chkSizerAttrs, 20)
        sizer3.Add(comp.chkOpenWithResourceEditor, 0, chkSizerAttrs, 20)
        sizer3.Add(comp.btnViewFile, 0, chkSizerAttrs, 20)

        sizer2.Add(comp.lblSearchFor, flag=stcSizerAttrs)
        sizer2.Add(comp.fldSearchPattern, flag=fldSizerAttrs)
        sizer2.Add(comp.btnSearch, flag=fldSizerAttrs)
        sizer2.Add(comp.btnCancel, flag=fldSizerAttrs)

        sizer2.Add(comp.lblDirectories, flag=stcSizerAttrs)
        sizer2.Add(comp.fldDirectories, flag=fldSizerAttrs)
        sizer2.Add(comp.btnAddDirs, flag=fldSizerAttrs)
        sizer2.Add((5, 5), 0)  # spacer

        sizer2.Add(comp.lblFileTypes, flag=stcSizerAttrs)
        sizer2.Add(comp.fldWildcard, flag=fldSizerAttrs)
        sizer2.Add((5, 5), 0)  # spacer
        sizer2.Add((5, 5), 0)  # spacer

        sizer1.Add(sizer2, 0, vertFlags)
        sizer1.Add((5, 5), 0)  # spacer
        sizer1.Add(sizer3, 0, vertFlags)
        sizer1.Add((5, 5), 0)  # spacer

        sizer1.Add(comp.listResults, 1, wx.EXPAND)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()
        
        self.visible = True

    def OnFileHistory(self, event):
        fileNum = event.GetId() - wx.ID_FILE1
        path = self.fileHistory.GetHistoryFile(fileNum)
        self.loadGrepFile(path)

    def loadConfig(self):
        try:
            if not os.path.exists(self.configPath):
                os.mkdir(self.configPath)
            path = os.path.join(self.configPath, USERCONFIG)
            self.config = util.readAndEvalFile(path)
            if self.config != {}:
                if 'findfiles.position' in self.config:
                    self.position = self.config['findfiles.position']
                if 'findfiles.size' in self.config:
                    self.size = self.config['findfiles.size']
                if 'searches' in self.config:
                    self.components.fldSearchPattern.items = self.config['searches']
                if 'history' in self.config:
                    history = self.config['history']
                    history.reverse()
                    for h in history:
                        self.fileHistory.AddFileToHistory(h)
        except:
            self.config = {}

    def saveConfig(self):
        self.config['findfiles.position'] = self.GetRestoredPosition()
        self.config['findfiles.size'] = self.GetRestoredSize()
        history = []
        for i in range(self.fileHistory.GetCount()):
            history.append(self.fileHistory.GetHistoryFile(i))
        # the limitation on the number of items to save is obviously
        # arbitrary, so I guess this could be made a setting as well
        self.config['searches'] = self.components.fldSearchPattern.items[:100]
        self.config['history'] = history
        try:
            path = os.path.join(self.configPath, USERCONFIG)
            f = open(path, "w")
            pprint.pprint(self.config, f)
            f.close()
        except:
            pass    # argh


    def on_close(self, event):
        # kill search loop if needed
        self.stopSearching = True
        path = os.path.join(self.configPath, LASTGREPFILE)
        self.saveGrepFile(path)
        self.saveConfig()
        event.skip()

    def on_menuFileOpen_select(self, event):        
        # split this method into several pieces to make it more flexible
        wildcard = "Grep files (*.grep)|*.grep|All files (*.*)|*.*"
        result = dialog.openFileDialog(wildcard=wildcard)
        if result.accepted:
            path = result.paths[0]
            self.loadGrepFile(path)

    def on_btnChangeDirs_mouseClick(self, event):
        wildcard = "Grep files (*.grep)|*.grep"
        result = dialog.openFileDialog(wildcard=wildcard)
        if result.accepted:
            s = result.paths[0]
            self.dir = os.path.dirname(s)
            fileList = [] 
            filenames = os.listdir(self.dir)
            for fName in filenames:
                root, ext = os.path.splitext(fName)
                if ext == '.grep':
                    fileList.append(fName)
            fileList.sort() # again, need a case-insensitive sort
            self.components.listFiles.items = fileList

    def setSearchParams(self, searchPattern='', dirs='', wildcard='*', caseSensitive=False,
                        searchSubdirectories=True, verbose=False):
        self.components.fldDirectories.text = dirs
        self.components.fldWildcard.text = wildcard
        self.components.fldSearchPattern.text = searchPattern
        self.components.chkCaseSensitive.checked = caseSensitive
        self.components.chkSearchSubdirectories.checked = searchSubdirectories
        self.components.chkVerbose.checked = verbose

    def loadGrepFile(self, filename):
        try:
            file = open(filename, 'rb')
            txt = file.read()
            file.close()
            dirs, wildcard, searchPattern, caseSensitive, searchSubdirectories, verbose = txt.split('\t')
            self.setSearchParams(searchPattern, dirs, wildcard, caseSensitive in ('1', 'True'),
                                 searchSubdirectories in ('1', 'True'), verbose.rstrip() in ('1', 'True'))
            self.components.fldSearchPattern.setFocus()
            self.documentPath = None
            self.documentChanged = 0
            self.fileHistory.AddFileToHistory(filename)
        except:
            pass
        self.components.fldSearchPattern.SetMark(-1, -1)

    def on_listFiles_select(self, event):
        try:
            filename = os.path.join(self.dir, list.stringSelection)
            self.loadGrepFile(filename)
        except:
            pass

    def toggleSearchCancel(self, state):
        self.components.btnSearch.enabled = state
        self.components.btnCancel.enabled = not state

    def doSearch(self):
        self.toggleSearchCancel(False)
        
        log.info("Grep for %s in %s" % (self.greppattern, self.filpattern))
        log.info('#Search '+self.dirpattern)
        if self.verbose:
            log.info('#   ='+self.dirpattern)
        log.info('# Files '+self.filpattern)
        log.info('#   For '+self.greppattern)
        # KEA 2002-06-11
        # "There's no equivalent of regex_syntax; 
        # re supports only one syntax, and you can't change it."
        # http://py-howto.sourceforge.net/regex-to-re/node3.html
        #regex.set_syntax(regex_syntax.RE_SYNTAX_GREP)
        if self.casesensitive:
            self.pat = re.compile(self.greppattern)
        else:
            self.pat = re.compile(self.greppattern, re.IGNORECASE)
        log.info("Searching.  Please wait...")
        
        patterns = self.filpattern.split(";")
        self.components.listResults.clear()
        self.statusBar.text = "Searching..."
        found = 0
        self.stopSearching = False
        for dir in self.dirpattern.split(';'):
            for filename in util.dirwalk(dir, patterns, self.recurse):
                if self.SearchFile(filename):
                    found += 1
                if self.stopSearching:
                    break
                else:
                    self.statusBar.text = "Files found: %d     Searching: %s" % (found, filename)
                    wx.SafeYield(self, True)
        self.statusBar.text = "Files found: %d" % found
        self.toggleSearchCancel(True)

    def SearchFile(self, filename):
        if self.verbose:
            log.info('# ..'+filename)
        try:
            lines = open(filename, 'r').readlines()
        except:
            lines = []
        found = 0
        for i in range(len(lines)):
            line = lines[i]
            if self.pat.search(line) is not None:
                if not found:
                    self.components.listResults.append(filename)
                    found = 1
                self.components.listResults.append('  '+`i+1` + ': '+line[:-1])
        return found
        
    def addTextToItems(self):
        target = self.components.fldSearchPattern
        text = target.text
        items = target.items
        if not items.count(text):
            items.insert(0, text)
            target.items = items
            target.text = text
            target.SetInsertionPointEnd()
            target.SetMark(-1, -1)

    def on_btnSearch_mouseClick(self, event):
        self.addTextToItems()

        self.dirpattern = self.components.fldDirectories.text
        self.filpattern = self.components.fldWildcard.text
        if self.filpattern == '':
            self.filpattern = '*'
        self.greppattern = self.components.fldSearchPattern.text
        self.casesensitive = self.components.chkCaseSensitive.checked
        self.recurse = self.components.chkSearchSubdirectories.checked
        self.verbose = self.components.chkVerbose.checked
        #print self.greppattern
        #print self.dirpattern
        #print self.filpattern
        #print self.casesensitive
        #print self.recurse
        #print self.verbose
        self.doSearch()

    def on_btnCancel_mouseClick(self, event):
        self.stopSearching = True
        self.toggleSearchCancel(True)

    def on_btnAddDirs_mouseClick(self, event):
        wFldDirectories = self.components.fldDirectories
        dirs = wFldDirectories.text
        result = dialog.directoryDialog(self, '', '')
        if result.accepted:
            s = result.path
            if dirs == "":
                wFldDirectories.text = s
            else:
                found = 0
                # should the search be case-insensitive?
                for dir in dirs.split(";"):
                    if s.upper() == dir.upper():
                        found = 1
                        break
                if not found:
                    wFldDirectories.text = dirs + ";" + s

    def saveGrepFile(self, path):
        txt = self.components.fldDirectories.text + "\t" + \
        self.components.fldWildcard.text + "\t" + \
        self.components.fldSearchPattern.text + "\t" + \
        str(self.components.chkCaseSensitive.checked) + "\t" + \
        str(self.components.chkSearchSubdirectories.checked) + "\t" + \
        str(self.components.chkVerbose.checked) + "\n"
        try:
            f = open(path, 'wb')
            f.write(txt)
            f.close()
            self.documentPath = path
            self.documentChanged = 0
            self.fileHistory.AddFileToHistory(path)
        except:
            pass

    def on_menuFileSaveAs_select(self, event):
        wildcard = "Grep files (*.grep)|*.grep|All files (*.*)|*.*"
        if self.documentPath is None:
            dir = ''
            filename = '*.grep'
        else:
            dir = os.path.dirname(self.documentPath)
            filename = os.path.basename(self.documentPath)
        result = dialog.saveFileDialog(None, "Save As", dir, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            self.saveGrepFile(path)
            return True
        else:
            return False

    def editFile(self, filename, lineno=None):
        if filename == '':
            return

        log.debug("filename: " + filename + "  lineno: " + str(lineno))
        # edit Python scripts with codeEditor
        # everything else with textEditor
        # the list of extensions and associated programs to
        # open with should be user settable
        if self.components.chkOpenWithResourceEditor.checked and filename.endswith('.rsrc.py'):
            program = os.path.join("..", "resourceEditor", "resourceEditor.pyw")
            if not os.path.exists(program):
                program = os.path.join("..", "resourceEditor", "resourceEditor.py")
        else:
            program = os.path.join("..", "codeEditor", "codeEditor.pyw")
            if not os.path.exists(program):
                program = os.path.join("..", "codeEditor", "codeEditor.py")
        # throw an exception if program can't be found?
        log.debug('program: ' + program)

        if wx.Platform in ('__WXMAC__', '__WXGTK__'):
            args = [filename]
        else:
            args = ['"' + filename + '"']
        if lineno is not None:
            args.append(str(lineno))
        log.debug(args)
        if ' ' in program:
            program = '"' + program + '"'
        python = sys.executable
        if ' ' in python:
            pythonQuoted = '"' + python + '"'
        else:
            pythonQuoted = python
        os.spawnv(os.P_NOWAIT, python, [pythonQuoted, program] + args)

    def on_btnViewFile_mouseClick(self, event):
        self.on_listResults_mouseDoubleClick(None)

    def on_listResults_mouseDoubleClick(self, event):
        target = self.components.listResults
        #clickLine = target.positionToXY(target.getInsertionPoint())[1] + 1
        clickLine = target.selection
        log.info("clickLine: " + str(clickLine))
        # getLineText is 0 based
        #current = target.getLineText(clickLine - 1)
        current = target.stringSelection
        if not current.startswith("  "):
            self.editFile(current.rstrip())
        else:
            """
            if current[:1] == '#':  # we have a comment line
                return current
            if current[:2] != '  ': # just fake a result line
                return current[:-1] + "(1) # LLAMA LINE\n"
            """

            delim = current.find(': ')
            greplineno = current[2:delim]
            greptext = current[delim+2:]
            # search backwards in the results until we find
            # a line that doesn't begin with two spaces, which should
            # be the full path for the grep result
            line = ''
            lineno = clickLine
            while lineno != 0:
                lineno = lineno - 1
                line = target.getString(lineno)
                if not line.startswith("  "):
                    break
            # chop any trailing newline
            filename = line.rstrip() 
            #print 'delim:', delim
            #print 'greplineno:', greplineno
            #print 'greptext:', greptext
            #print 'filename:', filename
            #print filename + '(' + greplineno + ') ' + greptext
            self.editFile(filename, greplineno)

    def on_fldSearchPattern_keyPress(self, event):
        keyCode = event.keyCode
        target = event.target
        # once the Search button has gotten
        # focus the return key doesn't appear
        # to go to the ComboBox anymore
        # need to investigate further
        if keyCode == 13:
            # pressing return also starts a search
            # just as if the user clicked on the Search button
            self.on_btnSearch_mouseClick(None)
            #wx.CallAfter(target.setFocus())
        else:
            event.skip()

    def on_showFindFilesDocumentation_command(self, event):
        global findfiles_url
        webbrowser.open(findfiles_url)

    def on_showPythonCardDocumentation_command(self, event):
        global pythoncard_url
        webbrowser.open(pythoncard_url)


if __name__ == '__main__':
    app = model.Application(FindFiles)
    app.MainLoop()
