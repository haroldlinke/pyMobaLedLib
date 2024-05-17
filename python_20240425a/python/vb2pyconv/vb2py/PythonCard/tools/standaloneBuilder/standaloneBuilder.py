#!/usr/bin/python
#
# PythonCard standaloneBuilder tool - Phil Edwards <phil@linux2000.com>
# Copyright (c) 2001-2005 PythonCard developers
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
# EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY 
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF 
# SUCH DAMAGE.
# 
# vim: ai et sw=4 ts=4

# standard imports
import os
import sys
import ConfigParser
import time
import pprint

# pythoncard imports
import wx
from wxPython.html import wxHtmlEasyPrinting
from PythonCard import dialog, model, util
from PythonCard.templates.dialogs import runOptionsDialog

# local imports
from customDialogs import *
import outputWindow

# temporary hack until we get it working properly under MacOS
if wx.Platform == '__WXMAC__':
    from wxPython.wx import wxPySimpleApp, wxFrame, wxMessageDialog, wxICON_EXCLAMATION, wxOK, wxVERSION_STRING
    app = wxPySimpleApp()
    title = 'Sorry!'
    frame = wxFrame(None, -1, title)
    message = 'standaloneBuilder currently does not work properly under MacOS. This shortcoming will '
    message += 'be fixed in a future release.\n\nClick OK to exit.'
    dialog = wxMessageDialog(frame, wrap_string(message, 52), title, wxICON_EXCLAMATION | wxOK)
    dialog.ShowModal()
    dialog.Destroy()
    sys.exit(0)

if sys.platform.startswith('win'):
    try:
        from win32api import GetShortPathName
        import versionInfo
    except ImportError:
        from wxPython.wx import wxPySimpleApp, wxFrame, wxMessageDialog, wxICON_EXCLAMATION, wxOK, wxVERSION_STRING
        app = wxPySimpleApp()
        title = 'Required component missing'
        frame = wxFrame(None, -1, title)
        message = "standaloneBuilder requires that you have a version of the Python win32 extensions " + \
            "installed - this appears to be missing from your system.\n\nClick OK to exit."
        dialog = wxMessageDialog(frame, wrap_string(message, 60), title, wxICON_EXCLAMATION | wxOK)
        dialog.ShowModal()
        dialog.Destroy()
        sys.exit(0)
else:
    import commands

# imports required by mcmillan installer
#from PythonCard.components import statictext, imagebutton, textfield, \
#    textarea, list, staticbox, checkbox, choice
from PythonCard.components import button, checkbox, choice, htmlwindow, image, imagebutton, list, spinner, staticbox, statictext, textarea, textfield

    
class standaloneBuilder(model.Background):

##############################################################################
# generic pythoncard event handlers
#
##############################################################################
    def on_initialize(self, event):
        self.str = self.resource.strings
        self.startTitle = self.GetTitle()
        self.loadConfig()
        
        # start with almost all of the UI disabled
        for comp in self.components.keys():
            self.components[comp].enabled = False
        self.components.newBtn.enabled = True
        self.components.openBtn.enabled = True
        self.components.prefsBtn.enabled = True
        self.components.quitBtn.enabled = True
        
        # likewise, start with almost all of the menu disabled
        self.menuBar.setEnabled('menuFileNew', True)
        self.menuBar.setEnabled('menuFileOpen', True)
        self.menuBar.setEnabled('menuFileSave', False)
        self.menuBar.setEnabled('menuFileSaveAs', False)
        self.menuBar.setEnabled('menuFileExit', True)
        self.menuBar.setEnabled('menuEditMainScript', False)
        self.menuBar.setEnabled('menuEditChglog', False)
        self.menuBar.setEnabled('menuEditReadme', False)
        self.menuBar.setEnabled('menuEditSpecfile', False)
        self.menuBar.setEnabled('menuEditInnoFile', False)
        self.menuBar.setEnabled('menuEditProps', False)
        self.menuBar.setEnabled('menuEditPrefs', True)
        self.menuBar.setEnabled('menuToolsLogAdd', False)
        self.menuBar.setEnabled('menuToolsChkImport', False)
        self.menuBar.setEnabled('menuToolsAddScript', False)
        self.menuBar.setEnabled('menuToolsAddResource', False)
        self.menuBar.setEnabled('menuToolsAddPixmap', False)
        self.menuBar.setEnabled('menuToolsAddOther', False)
        self.menuBar.setEnabled('menuToolsRunMain', False)
        self.menuBar.setEnabled('menuToolsRebuild', False)
        self.menuBar.setEnabled('menuToolsRelease', False)
        self.menuBar.setEnabled('menuHelpManual', True)
        self.menuBar.setEnabled('menuHelpAbout', True)
            
        self.documentChanged = False
        self.cmdLineArgs = {'debugmenu':False, 'logging':False, 'messagewatcher':False,
                            'namespaceviewer':False, 'propertyeditor':False,
                            'shell':False, 'otherargs':''}
        
        if sys.platform.startswith('win32'):
            self.PATHSEP = os.sep + os.sep
        else:
            self.PATHSEP = os.sep
            
        self.setupCode = open('templates/setup.py').read()
        
        self.outputWindow = model.childWindow(self, outputWindow.outputWindow)
        
    def on_close(self, event):
        if self.doExit(): event.Skip()
        
    def on_menuFileExit_command(self, event):
        self.close()

##########################################################################
# top level routines - menu code
#
##########################################################################
    def on_menuFileSaveAs_select(self, event):
        wildcard = "Project files (*.pmr)|*.pmr;*.PMR|All files (*.*)|*.*"
        if self.documentPath is None:
            dir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
            if sys.platform.startswith('win'):
                filename = '%s.pmr' % self.components.projectName.text
            else:
                filename = 'Untitled.pmr'
        else:
            dir = os.path.dirname(self.documentPath)
            filename = os.path.basename(self.documentPath)
        result = dialog.saveFileDialog(None, "Save As", dir, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            self.saveFile(path)
            return 1
        else:
            return 0
            
    def on_menuToolsLogAdd_command(self, event):
        vstring = string.split(self.components.versionString.text, '.')
        template = {}
        template['name'] = self.components.projectName.text
        template['major'] = vstring[0]
        template['minor'] = vstring[1]
        template['fix'] = vstring[2]
        
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        chglog = os.path.join(basedir, 'changelog.txt')
        
        if not os.path.exists(chglog):
            fd = open(chglog, 'w')
            tmplfile = os.path.join('templates', 'changelog.txt')
            chglogData = open(tmplfile, 'r').read()
            chglogData = chglogData % template
            dashes = '-' * len(chglogData)
            fd.write(chglogData + '\n')
            fd.write(dashes + '\n')
            fd.close()
            
        # add a new changelog entry
        result = dialog.multilineTextEntryDialog(self, 'Add Changelog Entry', 'Enter the new text below, and click OK:')
            
        if result.accepted:
            fmtstring = string.split(wrap_string(result.text, 65), '\n')
            infd = open(chglog, 'r')
            outfd = open(chglog + '-new', 'w')
            
            # keep the top 2 lines of the existing file
            outfd.write(infd.readline())
            outfd.write(infd.readline())
            
            # write out the new entry
            for cnt in range(len(fmtstring)):
                if fmtstring[cnt] != '':
                    if cnt == 0:
                        outfd.write('    - ' + fmtstring[cnt] + '\n')
                    else:
                        outfd.write('      ' + fmtstring[cnt] + '\n')
                
            # then write out all the remaining entries
            ln = infd.readline()
            while ln:
                outfd.write(ln)
                ln = infd.readline()

            infd.close()
            outfd.close()
            
            os.unlink(chglog)
            os.rename(chglog + '-new', chglog)
            
    def on_menuToolsChkImport_command(self, event):
        if self.components.mainScript.text != '':
            impFound, impLine = self.checkImports()
            if not impFound:
                self.outputWindow.components.clipBoardBtn.userdata = impLine
                self.outputWindow.components.txt5.enabled = False
                self.outputWindow.components.txt5.visible = False
                self.outputWindow.components.returnedText.enabled = False
                self.outputWindow.components.returnedText.visible = False
                self.outputWindow.components.importError.enabled = True
                self.outputWindow.components.importError.visible = True
                self.outputWindow.SetTitle('PythonCard Component Import Check')
                self.outputWindow.Show()
                self.outputWindow.clearLines()
                self.outputWindow.components.txt1a.visible = False # rebuilding spec file
                self.outputWindow.components.txt1b.visible = False # done
                self.outputWindow.components.txt2a.visible = False # rebuilding versioninfo file
                self.outputWindow.components.txt2b.visible = False # done
                self.outputWindow.components.txt3a.visible = False # rebuilding application
                self.outputWindow.components.txt3b.visible = False # done
                self.outputWindow.components.txt3c.visible = False # please wait...
                self.outputWindow.components.txt4a.visible = False # rebuilding distributable
                self.outputWindow.components.txt4b.visible = False # done
                self.outputWindow.components.txt4c.visible = False # please wait
                #self.outputWindow.components.clipBoardBtn.visible = True
                txt = 'The main script should include the following import statement on a '
                self.outputWindow.addLine(txt)
                txt = 'single line:\n\n'
                self.outputWindow.addLine(txt)
                txt = impLine + '\n\n'
                self.outputWindow.addLine(txt)
                if sys.platform.startswith('win'):
                    self.outputWindow.components.clipBoardBtn.visible = True
                    txt = 'Click the \'Clipboard\' button below to place this line on '
                    self.outputWindow.addLine(txt)
                    txt = 'the clipboard ready to be pasted into your code.'
                    self.outputWindow.addLine(txt)
                else:
                    self.outputWindow.components.clipBoardBtn.visible = False
                    txt = 'Copy and paste this line into your code before rebuilding.'
                    self.outputWindow.addLine(txt)
            else:
                title = 'Component import check'
                txt = 'PythonCard components import line present and correct!'
                bull = dialog.messageDialog(self, wrap_string(txt, 60), title, wx.ICON_INFORMATION)
                
    def on_menuHelpManual_command(self, event):
        title = 'Sorry!'
        txt = 'Online manual functionality will be implemented in a future '
        txt += 'version of standaloneBuilder.'
        bull = dialog.alertDialog(self, txt, title)
                
        
    def on_menuHelpAbout_command(self, event):
        dlg = HTMLHelp(self)
        dlg.showModal()
        dlg.destroy()
        
##########################################################################
# toplevel routines - toolbar button events
#
##########################################################################
    def on_newBtn_command(self, event):
        if not self.saveIfRequired(): return
        dlg = newProjectWizard(self)
        dlg.ShowModal()
        result = dlg.getResult()
        if result.accepted: self.newFile(result)
        dlg.Destroy()
        
    def on_openBtn_command(self, event):
        if not self.saveIfRequired(): return
        wildcard = "Project files (*.pmr)|*.pmr;*.PMR|All files (*.*)|*.*"
        result = dialog.openFileDialog(wildcard=wildcard)
        if result.accepted:
            path = result.paths[0]
            self.openFile(path)
            
    def on_saveBtn_command(self, event):
        if self.documentPath is None:
            # this a "new" document and needs to go through Save As...
            self.on_menuFileSaveAs_select(None)
        else:
            self.saveFile(self.documentPath)
            
    def on_editPrefs_command(self, event):
        dlg = prefsDialog(self, self.CONFIG_FILE)
        dlg.ShowModal()
        dlg.Destroy()
        if self.components.projectName.text != '':
            if self.cfg.get('ConfigData', 'buildtool') != 'pyInstaller':
                self.components.specBtn.enabled = False
                self.menuBar.setEnabled('menuEditSpecfile', False)
            else:
                self.components.specBtn.enabled = True
                self.menuBar.setEnabled('menuEditSpecfile', True)
            
    def on_quitBtn_command(self, event):
        self.Close()

##########################################################################
# top level routines - user interface events
#
##########################################################################
    def on_iconBtn_mouseClick(self, event):
        title = 'Select icon'
        basepath = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        #basepath = os.path.join(basepath, self.components.projectIcon.text)
        wildcard = "Icon files (*.ico)|*.ico;*.ICO|All files (*.*)|*.*"
        old = self.components.projectIcon.text
        result = dialog.openFileDialog(self, title, basepath, '', wildcard=wildcard)
        if result.accepted:
            rpath = self.getRelativePath(basepath, result.paths[0])
            if rpath != old:
                self.components.projectIcon.text = rpath
                self.documentChanged = True
                self.updateStatusBar()            
                
    def on_baseDirBtn_mouseClick(self, event):
        title = 'Select directory'
        basepath = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        old = self.components.baseDir.text
        result = dialog.directoryDialog(self, title, basepath)
        if result.accepted:
            projdir = self.cfg.get('ConfigData', 'projects')
            rpath = string.replace(result.path, projdir, '')
            if rpath[0] == os.sep: rpath = rpath[1:]
            if rpath != old:
                self.components.baseDir.text = rpath
                self.documentChanged = True
                self.updateStatusBar()
            
    def on_mainScriptBtn_mouseClick(self, event):
        title = 'Select main script file'
        basepath = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        old = self.components.mainScript.text
        wildcard = "Script files (*.py)|*.py;*.PY"
        result = dialog.fileDialog(self, title, basepath, '', wildcard)
        if result.accepted:
            rpath = self.getRelativePath(basepath, result.paths[0])
            if rpath != old:
                if rpath in self.components.scriptList.items:
                    title = 'Script select error'
                    msg = '"%s" must be removed from the list of additional scripts if you wish to set it as the main script for your project' % rpath
                    bull = dialog.alertDialog(self, wrap_string(msg, 60), title)
                else:
                    self.checkResourceFile(result.paths[0])
                    self.components.mainScript.text = rpath
                    self.documentChanged = True
                    self.updateStatusBar()
                    
    def on_EditMainScript_command(self, event):
        editor = self.cfg.get('ConfigData', 'codeeditor')
        item = self.pathJoin(self.components.mainScript.text)
        item = os.path.join(self.components.baseDir.text, item)
        item = os.path.join(self.cfg.get('ConfigData', 'projects'), item)
        if sys.platform.startswith('win'):
            os.system('python "' + editor + '" "' + item + '"')
        else:
            os.system('"' + editor + '" "' + item + '"')
        
    def on_addScript_command(self, event):
        # add a script file to the project
        title = 'Select script(s)'
        wildcard = "Script files (*.py)|*.py;*.PY|All files (*.*)|*.*"
        basepath = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        current = self.components.scriptList.items
        result = dialog.openFileDialog(self, title, basepath, '', wildcard, wx.MULTIPLE)
        if result.accepted:
            for p in result.paths:
                path = os.path.basename(p)
                if not (path in current):
                    if path == self.components.mainScript.text:
                        title = 'Script select error'
                        msg = 'You have already selected "%s" as your main script - it does not need to be included in this list' % path
                        bull = dialog.alertDialog(self, wrap_string(msg, 60), title)
                    else:
                        self.checkResourceFile(p)
                        current.append(path)
                        current.sort()
                        self.documentChanged = True
                        self.updateStatusBar()
            if self.documentChanged: self.components.scriptList.items = current
        
    def on_scriptDelBtn_mouseClick(self, event):
        if self.components.scriptList.stringSelection != '':
            self.components.scriptList.items = self.delItem(self.components.scriptList.items, self.components.scriptList.stringSelection)
            
    def on_scriptEditBtn_mouseClick(self, event):
        if self.components.scriptList.stringSelection != '':
            editor = self.cfg.get('ConfigData', 'codeeditor')
            item = self.pathJoin(self.components.scriptList.stringSelection)
            item = os.path.join(self.components.baseDir.text, item)
            item = os.path.join(self.cfg.get('ConfigData', 'projects'), item)
            if sys.platform.startswith('win'):
                os.system('python "' + editor + '" "' + item + '"')
            else:
                os.system(editor + ' ' + item)
            
    def on_scriptDelAllBtn_mouseClick(self, event):
        title = 'Are you absolutely sure?'
        msg = 'This will remomve all the listed script files from your project. Is this really what you want to do?'
        result = dialog.messageDialog(self, wrap_string(msg, 60), title, wx.ICON_EXCLAMATION | wx.YES_NO | wx.NO_DEFAULT)
        if result.accepted:
            self.components.scriptList.items = []
            self.documentChanged = True
            self.updateStatusBar()
        
    def on_addResource_command(self, event):
        # add a resource file to the project
        title = 'Select resource file'
        basepath = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        wildcard = "Resource files (*.rsrc.py)|*.rsrc.py;*.RSRC.PY|All files (*.*)|*.*"
        current = self.components.resList.items
        self.components.resList.items = self.addItem(title, basepath, wildcard, current)
        
    def on_resDelBtn_mouseClick(self, event):
        if self.components.resList.stringSelection != '':
            self.components.resList.items = self.delItem(self.components.resList.items, self.components.resList.stringSelection)

    def on_resEditBtn_mouseClick(self, event):
        if self.components.resList.stringSelection != '':
            editor = self.cfg.get('ConfigData', 'reseditor')
            item = self.pathJoin(self.components.resList.stringSelection)
            item = os.path.join(self.components.baseDir.text, item)
            item = os.path.join(self.cfg.get('ConfigData', 'projects'), item)
            if sys.platform.startswith('win'):
                os.system('python "' + editor + '" "' + item + '"')
            else:
                os.system(editor + ' ' + item)
            
    def on_resDelAllBtn_mouseClick(self, event):
        title = 'Are you absolutely sure?'
        msg = 'This will remomve all the listed resource files from your project. Is this really what you want to do?'
        result = dialog.messageDialog(self, wrap_string(msg, 60), title, wx.ICON_EXCLAMATION | wx.YES_NO | wx.NO_DEFAULT)
        if result.accepted:
            self.components.resList.items = []
            self.documentChanged = True
            self.updateStatusBar()
                    
    def on_addPixmap_command(self, event):
        # add a pixmap file to the project
        title = 'Select pixmap file'
        basepath = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        basepath = os.path.join(basepath, self.project.get('Project', 'pixmapspath'))
        refpath = basepath
        #basepath = os.path.join(self.components.baseDir.text, self.project.get('Project', 'pixmapspath'))
        wildcard = "GIF Image (*.gif)|*.gif;*.GIF"
        wildcard += "|JPEG Image (*.jpg, *.jpeg)|*.jpg;*.jpeg;*.JPG;*.JPEG"
        wildcard += "|PNG Image (*.png)|*.png;*.PNG"
        wildcard += "|All files (*.*)|*.*"
        current = self.components.pixmapList.items
        self.components.pixmapList.items = self.addItem(title, basepath, wildcard, current, refpath)
        
    def on_pixmapDelBtn_mouseClick(self, event):
        if self.components.pixmapList.stringSelection != '':
            self.components.pixmapList.items = self.delItem(self.components.pixmapList.items, self.components.pixmapList.stringSelection)
            
    def on_pixmapDelAllBtn_mouseClick(self, event):
        title = 'Are you absolutely sure?'
        msg = 'This will remomve all the listed pixmaps from your project. Is this really what you want to do?'
        result = dialog.messageDialog(self, wrap_string(msg, 60), title, wx.ICON_EXCLAMATION | wx.YES_NO | wx.NO_DEFAULT)
        if result.accepted:
            self.components.pixmapList.items = []
            self.documentChanged = True
            self.updateStatusBar()
            
    def on_addOther_command(self, event):
        # add a resource file to the project
        title = 'Select documentation/other file'
        #basepath = os.path.join(self.components.baseDir.text, self.project.get('Project', 'docfilepath'))
        basepath = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        refpath = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        wildcard = "Text files (*.txt)|*.txt;*.TXT"
        wildcard += "|All files (*.*)|*.*"
        current = self.components.otherList.items
        self.components.otherList.items = self.addItem(title, basepath, wildcard, current, refpath)
        
    def on_docDelBtn_mouseClick(self, event):
        if self.components.otherList.stringSelection != '':
            self.components.otherList.items = self.delItem(self.components.otherList.items, self.components.otherList.stringSelection)

    def on_docEditBtn_mouseClick(self, event):
        if self.components.otherList.stringSelection != '':
            editor = self.cfg.get('ConfigData', 'texteditor')
            itempath = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
            itempath = os.path.join(itempath, self.components.otherList.stringSelection)
            if sys.platform.startswith('win'):
                if editor.endswith('.py'):
                    os.system('python "' + editor + '" "' + itempath + '"')
                else:
                    os.system('"' + editor + '" "' + itempath + '"')
            else:
                os.system(editor + ' ' + itempath)
            
    def on_docDelAllBtn_mouseClick(self, event):
        title = 'Are you absolutely sure?'
        msg = 'This will remomve all the listed files from your project. Is this really what you want to do?'
        result = dialog.messageDialog(self, wrap_string(msg, 60), title, wx.ICON_EXCLAMATION | wx.YES_NO | wx.NO_DEFAULT)
        if result.accepted:
            self.components.otherList.items = []
            self.documentChanged = True
            self.updateStatusBar()

    def on_editProps_command(self, event):
        dlg = propertiesDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
        self.updateStatusBar()
            
    def on_editChgLog_command(self, event):
        # edit changelog, create it if it doesn't exist
        vstring = string.split(self.components.versionString.text, '.')
        template = {}
        template['name'] = self.components.projectName.text
        template['major'] = vstring[0]
        template['minor'] = vstring[1]
        template['fix'] = vstring[2]
        
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        chglog = str(os.path.join(basedir, 'changelog.txt'))
        
        if not os.path.exists(chglog):
            fd = open(chglog, 'w')
            tmplfile = os.path.join('templates', 'changelog.txt')
            chglogData = open(tmplfile, 'r').read()
            chglogData = chglogData % template
            fd.write(chglogData)
            fd.close()
            
        editor = self.cfg.get('ConfigData', 'texteditor')
        if sys.platform.startswith('win'):
            if editor.endswith('.py'):
                os.system('python "' + editor + '" "' + chglog + '"')
            else:
                os.system('"' + editor + '" "' + chglog + '"')
        else:
            os.system(editor + ' ' + chglog)
        
    def on_editReadme_command(self, event):
        editor = self.cfg.get('ConfigData', 'texteditor')
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        readme = os.path.join(basedir, 'readme.txt')
        if sys.platform.startswith('win'):
            if editor.endswith('.py'):
                os.system('python "' + editor + '" "' + readme + '"')
            else:
                os.system('"' + editor + '" "' + readme + '"')
        else:
            os.system(editor + ' ' + readme)
        
    def on_editSpecFile_command(self, event):
        editor = self.cfg.get('ConfigData', 'texteditor')
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        spec = self.components.projectName.text + '.spec'
        spec = os.path.join(basedir, spec)
        cmd = '"' + editor + '" "' + spec + '"'
        if sys.platform.startswith('win'):
            if editor.endswith('.py'):
                os.system('python "' + editor + '" "' + spec + '"')
            else:
                os.system('"' + editor + '" "' + spec + '"')
        else:
            os.system(editor + ' ' + spec)
        
    def on_editInnoFile_command(self, event):
        editor = self.cfg.get('ConfigData', 'texteditor')
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        spec = self.components.projectName.text + '.iss'
        spec = os.path.join(basedir, spec)
        if sys.platform.startswith('win'):
            if editor.endswith('.py'):
                os.system('python "' + editor + '" "' + spec + '"')
            else:
                os.system('"' + editor + '" "' + spec + '"')
        else:
            os.system(editor + ' ' + spec)
        
    def on_runMainScript_command(self, event):
        # save the project if required
        ret = self.saveIfRequired()
        if not ret: return
        
        result = runOptionsDialog.runOptionsDialog(self, self.cmdLineArgs)
        if result.accepted:
            self.cmdLineArgs['debugmenu'] = result.debugmenu
            self.cmdLineArgs['logging'] = result.logging
            self.cmdLineArgs['messagewatcher'] = result.messagewatcher
            self.cmdLineArgs['namespaceviewer'] = result.namespaceviewer
            self.cmdLineArgs['propertyeditor'] = result.propertyeditor
            self.cmdLineArgs['shell'] = result.shell
            self.cmdLineArgs['otherargs'] = result.otherargs
            self.runScript(False)
        
    def on_rebuildCmd_command(self, event):
        # we have to make sure that there is something defined as a 'main
        # script' before we can do a rebuild
        if self.components.mainScript.text == '':
            title = 'Project error!'
            txt = 'You have not specified the main script for this project!'
            bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
            return
            
        # save the project if required
        if not self.saveIfRequired(): return
        
        # rebuild under Linux just involves making a tarball of the source
        # code plus associated files
        if sys.platform.startswith('linux') or sys.platform.startswith('freebsd'):
            self.rebuildLinux()
            return 0
            
        impFound, impLine = self.checkImports()
        
        if not impFound:
            self.outputWindow.components.clipBoardBtn.userdata = impLine
            self.outputWindow.components.txt5.enabled = False
            self.outputWindow.components.txt5.visible = False
            self.outputWindow.components.returnedText.enabled = False
            self.outputWindow.components.returnedText.visible = False
            self.outputWindow.components.importError.enabled = True
            self.outputWindow.components.importError.visible = True
            self.outputWindow.Show()
            self.outputWindow.clearLines()
            self.outputWindow.components.txt1a.visible = False # rebuilding spec file
            self.outputWindow.components.txt1b.visible = False # done
            self.outputWindow.components.txt2a.visible = False # rebuilding versioninfo file
            self.outputWindow.components.txt2b.visible = False # done
            self.outputWindow.components.txt3a.visible = False # rebuilding application
            self.outputWindow.components.txt3b.visible = False # done
            self.outputWindow.components.txt3c.visible = False # please wait...
            self.outputWindow.components.txt4a.visible = False # rebuilding distributable
            self.outputWindow.components.txt4b.visible = False # done
            self.outputWindow.components.txt4c.visible = False # please wait
            txt = 'The main script should include the following import statement on a '
            self.outputWindow.addLine(txt)
            txt = 'single line:\n\n'
            self.outputWindow.addLine(txt)
            txt = impLine + '\n\n'
            self.outputWindow.addLine(txt)
            if sys.platform.startswith('win'):
                self.outputWindow.components.clipBoardBtn.visible = True
                txt = 'Click the \'Clipboard\' button below to place this line on '
                self.outputWindow.addLine(txt)
                txt = 'the clipboard ready to be pasted into your code.'
                self.outputWindow.addLine(txt)
            else:
                txt = 'Copy and paste this line into your code before rebuilding.'
                self.outputWindow.addLine(txt)
            return
                    
        # give a warning message if the debug and/or console options
        # are switched on in project properties.
        if self.project.getboolean('Project', 'console') or self.project.getboolean('Project', 'debug'):
            txt = 'Please note that you currently have either the debug and/or the console option(s)'
            txt += ' switched on in the properties for this project.\n\nYou should probably switch these off'
            txt += ' prior to building the final version of your application'
            title = 'Project options warning!'
            bull = dialog.alertDialog(self, wrap_string(txt, 60), title)

        self.outputWindow.components.txt5.enabled = True
        self.outputWindow.components.txt5.visible = True
        self.outputWindow.components.returnedText.enabled = True
        self.outputWindow.components.returnedText.visible = True
        self.outputWindow.components.importError.enabled = False
        self.outputWindow.components.importError.visible = False
        self.outputWindow.components.txt1a.visible = False # rebuilding spec file
        self.outputWindow.components.txt1b.visible = False # done
        self.outputWindow.components.txt2a.visible = False # rebuilding versioninfo file
        self.outputWindow.components.txt2b.visible = False # done
        self.outputWindow.components.txt3a.visible = False # rebuilding application
        self.outputWindow.components.txt3b.visible = False # done
        self.outputWindow.components.txt3c.visible = False # please wait...
        self.outputWindow.components.txt4a.visible = False # rebuilding distributable
        self.outputWindow.components.txt4b.visible = False # done
        self.outputWindow.components.txt4c.visible = False # please wait
            
        # delete all transient files from previous rebuilds
        basedir = str(os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text))
        versionfile = os.path.join(basedir, 'versioninfo.txt')
        innofile = self.components.projectName.text + '.iss'
        innofile = os.path.join(basedir, innofile)
        
        try:
            os.unlink(str(versionfile))
        except:
            pass
            
        try:
            os.unlink('datafiles.dat')
        except:
            pass
            
        try:
            os.unlink('buildoptions.dat')
        except:
            pass
            
        try:
            os.unlink('standalone.dat')
        except:
            pass
            
        try:
            os.unlink(str(innofile))
        except:
            pass
            
        self.recursiveDirDelete(os.path.join(basedir, 'build'))
        self.recursiveDirDelete(os.path.join(basedir, 'dist'))
            
        # window for progress marks and output messages
        self.outputWindow.Show()
        self.outputWindow.clearLines()
        
        # make all the text fields invisible
        self.outputWindow.components.txt1a.visible = False # rebuilding spec file
        self.outputWindow.components.txt1b.visible = False # done
        self.outputWindow.components.txt2a.visible = False # rebuilding versioninfo file
        self.outputWindow.components.txt2b.visible = False # done
        self.outputWindow.components.txt3a.visible = False # rebuilding application
        self.outputWindow.components.txt3b.visible = False # done
        self.outputWindow.components.txt3c.visible = False # please wait...
        self.outputWindow.components.txt4a.visible = False # rebuilding distributable
        self.outputWindow.components.txt4b.visible = False # done
        self.outputWindow.components.txt4c.visible = False # please wait
                    
        # rebuild the spec file - not required when using py2exe
        self.outputWindow.components.txt1a.visible = True # rebuilding spec file
        self.outputWindow.Update()
        self.outputWindow.Refresh()
        if self.cfg.get('ConfigData', 'buildtool') == 'pyInstaller': self.buildSpecFile() # not required with py2exe
        self.outputWindow.components.txt1b.visible = True # done
        
        # rebuild the versioninfo file
        self.outputWindow.components.txt2a.visible = True # rebuilding versioninfo file
        self.outputWindow.Update()
        self.outputWindow.Refresh()
        self.buildVersionFile()
        self.outputWindow.components.txt2b.visible = True # done
        
        # rebuild the application
        self.outputWindow.components.txt3a.visible = True # rebuilding application
        self.outputWindow.components.txt3c.visible = True # please wait...
        self.outputWindow.Update()
        self.outputWindow.Refresh()
        if self.cfg.get('ConfigData', 'buildtool') == 'pyInstaller':
            allokay = self.buildApplication()
        else:
            allokay = self.buildWithpy2exe()
        self.outputWindow.components.txt3c.visible = False
        self.outputWindow.components.txt3b.visible = True # done
        if not allokay: self.outputWindow.components.txt3b.text = '*** ERROR ***'
        self.outputWindow.Update()
        
        # rebuild the Inno script file
        self.outputWindow.components.txt4a.visible = True # rebuilding distributable
        self.outputWindow.components.txt4c.visible = True # please wait
        self.outputWindow.Update()
        self.outputWindow.Refresh()
        if allokay: self.buildInnoFile()
        
        # rebuild the distributable
        #self.buildDistFile()
        self.outputWindow.components.txt4c.visible = False
        self.outputWindow.components.txt4b.visible = True # done
        if allokay:
            self.buildInstaller()
            #self.outputWindow.Update()
            #self.outputWindow.Refresh()
            #self.outputWindow.Raise()
        else:
            self.outputWindow.components.txt4b.text = '*** ERROR ***' # rebuilding distributable            
        
        # if the project is not frozen, increment the build number to finish
        if self.project.get('Project', 'status') == 'open' and allokay:
            build = self.project.getint('Project', 'build')
            build += 1
            self.project.set('Project', 'build', str(build))
            self.documentChanged = True
            self.updateStatusBar()
            
        self.outputWindow.Update()
        self.outputWindow.Refresh()
        self.outputWindow.Raise()
        
    def on_releaseCmd_command(self, event):
        # do stuff for releasing a project
        pstatus = self.project.get('Project', 'status')
        if pstatus == 'open':
            # give a warning message if the debug and/or console options
            # are switched on in project properties.
            if self.project.getboolean('Project', 'console') or self.project.getboolean('Project', 'debug'):
                txt = 'Please note that you currently have either the debug and/or the console option(s)'
                txt += ' switched on in the properties for this project.\n\nYou might want to switch these off'
                txt += ' prior to releasing the final version of your application'
                title = 'Project options warning!'
                bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
            # freeze the project ready for release
            txt = 'This will freeze the current release so that no more changes can '
            txt += 'be made. You should only do this if you are absolutely sure that '
            txt += 'your project is ready to be released. Once frozen, the project '
            txt += 'should be rebuilt on all the platforms you are interested in.\n\nYou '
            txt += 'should then click the release button again to un-freeze the '
            txt += 'project and initialize the next version.\n\nIf you clicked this '
            txt += 'button by mistake, select Cancel below, otherwise select OK to '
            txt += 'continue with the release process.'
            result = dialog.messageDialog(self, wrap_string(txt, 60), 'Please confirm',
                wx.ICON_EXCLAMATION|wx.OK|wx.CANCEL)
            if not result.accepted: return 0
            if not self.freezeProject(): return 0
            
        if pstatus == 'frozen':
            # mark the release as finished and start the next one
            vstring = self.project.get('Project', 'projectdesc') + ' Ver '
            vstring += self.project.get('Project', 'majorversion') + '.'
            vstring += self.project.get('Project', 'minorversion') + '.'
            vstring += self.project.get('Project', 'fixnumber')
            txt = 'You are about to release %s ' % vstring
            txt += '- this will close off the current release and start a new '
            txt += 'release. Please ensure that you have run the build process on all '
            txt += 'applicable platforms before continuing.\n\nIf you clicked this '
            txt += 'button by mistake, select Cancel below, otherwise select OK to '
            txt += 'continue with the release process.'
            result = dialog.messageDialog(self, wrap_string(txt, 60), 'Please confirm',
                wx.ICON_EXCLAMATION|wx.OK|wx.CANCEL)
            if not result.accepted: return 0
            if not self.releaseProject(): return 0
        
##############################################################################
# second level stuff - routines called by the first level code
#
##############################################################################
    def recursiveDirDelete(self, path=None):
        # recursively delete a sub directory
        if path is None: return
        if not os.path.isdir(path): return
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files: os.unlink (os.path.join(root, name))
            for name in dirs: os.rmdir(os.path.join(root, name))
        os.rmdir(path)
        
    def checkResourceFile(self, path):
        # when adding a script, see if there is a matching resource file
        root, ext = os.path.splitext(path)
        script = os.path.basename(path)
        resfile = root + '.rsrc.py'
        if os.path.isfile(resfile):
            # is it already in the list of resource files?
            if not os.path.basename(resfile) in self.components.resList.items:
                txt = '%s has a matching PythonCard resource file. Would you like to also' % (script)
                txt += ' add the resource file to your project?'
                result = dialog.messageDialog(self, wrap_string(txt, 60), 'Please confirm',
                    wx.ICON_EXCLAMATION|wx.YES_NO|wx.YES_DEFAULT)
                if result.accepted:
                    x = self.components.resList.items
                    x.append(os.path.basename(resfile))
                    x.sort()
                    self.components.resList.items = x

    def runScript(self, useInterpreter):
        item = self.pathJoin(self.components.mainScript.text)
        item = os.path.join(self.components.baseDir.text, item)
        item = os.path.join(self.cfg.get('ConfigData', 'projects'), item)
        # pinched this code from the resource editor - thanks, Kevin!
        #path = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        #path, filename = os.path.split(self.filename)
        path, filename = os.path.split(item)
        name = filename.split('.')[0]
        if os.path.exists(os.path.join(path, name + ".pyw")):
            filename = '"' + os.path.join(path, name + ".pyw") + '"'
        else:
            filename = '"' + os.path.join(path, name + ".py") + '"'
        # the args should come from a dialog or menu items that are checked/unchecked
        args = self.getCommandLineArgs()

        if useInterpreter:
            interp = ' -i '
        else:
            interp = ' '
            
        if sys.platform.startswith('win'):
            # KEA 2002-03-06
            # always launch with console in the resourceEditor for debugging purposes
            python = os.path.join(os.path.dirname(sys.executable), 'python.exe')
            if ' ' in python:
                pythonQuoted = '"' + python + '"'
            else:
                pythonQuoted = python
            if useInterpreter and os.name != 'nt':
                os.spawnv(os.P_NOWAIT, python, [pythonQuoted, interp, filename, args])
            else:
                os.spawnv(os.P_NOWAIT, python, [pythonQuoted, interp, filename, args])
        else:
            if ' ' in sys.executable:
                python = '"' + sys.executable + '"'
            else:
                python = sys.executable
            os.system(python + interp + filename + args + ' &')
    
    def saveIfRequired(self):
        # save the project if required
        retflag = True
        if self.documentChanged:
            save = self.saveChanges()
            if save == wx.ID_CANCEL:
                retflag = False # don't do anything, just go back to editing
            elif save == wx.ID_NO:
                pass # any changes will be lost
            else:
                if self.documentPath is None:
                    # if the user cancels out of the Save As then go back to editing
                    if not self.on_menuFileSaveAs_select(None): retflag = False
                else:
                    self.saveFile(self.documentPath)
        return retflag
        
    def getCommandLineArgs(self):
        args = ' '
        if self.cmdLineArgs['debugmenu']:
            args += '-d '
        if self.cmdLineArgs['logging']:
            args += '-l '
        if self.cmdLineArgs['messagewatcher']:
            args += '-m '
        if self.cmdLineArgs['namespaceviewer']:
            args += '-n '
        if self.cmdLineArgs['propertyeditor']:
            args += '-p '
        if self.cmdLineArgs['shell']:
            args += '-s '
        if self.cmdLineArgs['otherargs'] != '':
            args += self.cmdLineArgs['otherargs']
        return args
    
    def getRelativePath(self, root, path):
        # remove the root part of an absolute path
        retPath = string.replace(path, root, '')
        if retPath[0] == os.sep: retPath = retPath[1:]
        #bull = raw_input()
        return retPath
        
    def loadConfig(self):
        # first job is to work out where the config file should be stored
        if sys.platform.startswith('linux') or sys.platform.startswith('freebsd'):
            # on Linux & FreeBSD, it goes in ~/.pmrc
            self.HOMEDIR = os.path.expanduser('~')
            self.CONFIG = '.standaloneBuilderrc'
        else:
            # Windows needs to put the config file in C:\Program Files\PM\pm.ini
            self.HOMEDIR = os.path.dirname(sys.argv[0])
            self.CONFIG = 'standaloneBuilder.ini'

        self.CONFIG_FILE = os.path.join(self.HOMEDIR, self.CONFIG)
        
        # allow a different config file to be specified on the command line
        # for testing purposes etc
        for optnum in range(len(sys.argv)):
            if sys.argv[optnum] == '-f':
                self.CONFIG_FILE = sys.argv[optnum + 1]
                break
        
        # create a default config the very first time we run standaloneBuilder
        if not os.path.exists(self.CONFIG_FILE):
            self.createConfig()
        else:
            self.cfg = ConfigParser.ConfigParser()
            self.cfg.read(self.CONFIG_FILE)

        # check that pyInstaller and py2exe haven't gone missing
        instpath = self.cfg.get('ConfigData', 'installerpath')
        btool = self.cfg.get('ConfigData', 'buildtool')
        if btool == 'pyInstaller' and not os.path.exists(instpath):
            title = '*** WARNING ***'
            txt = 'Your copy of pyInstaller was previously located at '
            txt += instpath + '. It appears to have vanished. You should open '
            txt += 'the preferences dialog and check that your settings are '
            txt += 'still valid.'
            bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
            
        if btool == 'py2exe':
            try:
                from distutils.core import setup as wibble
            except ImportError:
                title = '*** WARNING ***'
                txt = 'You have configured standaloneBuilder to use py2exe as '
                txt += 'the build mechanism but you do not appear to have a '
                txt += 'copy of the distutils package installed. You should open '
                txt += 'the preferences dialog and check that your settings are '
                txt += 'still valid.'
                bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
            try:
                import py2exe as wibble
            except ImportError:
                title = '*** WARNING ***'
                txt = 'You have configured standaloneBuilder to use py2exe as '
                txt += 'the build mechanism but you do not appear to have a '
                txt += 'copy of the py2exe package installed. You should open '
                txt += 'the preferences dialog and check that your settings are '
                txt += 'still valid.'
                bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
                
        # check that Inno Setup is still installed
        isccpath = self.cfg.get('ConfigData', 'compilerpath')
        if not os.path.exists(isccpath) and sys.platform.startswith('win'):
            title = '*** WARNING ***'
            txt = 'Your copy of Inno Setup was previously located at '
            txt += isccpath + '. It appears to have vanished. You should open '
            txt += 'the preferences dialog and check that your settings are '
            txt += 'still valid.'
            bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
                

    def doExit(self):
        if self.documentChanged:
            save = self.saveChanges()
            if save == wx.ID_CANCEL:
                return 0
            elif save == wx.ID_NO:
                return 1
            else:
                if self.documentPath is None:
                    return self.on_menuFileSaveAs_select(None)
                else:
                    self.saveFile(self.documentPath)
                    return 1
        else:
            return 1

    def saveFile(self, path):
        self.UI2Project()
        try:
            f = open(path, 'w')
            self.project.write(f)
            f.close()
            self.documentPath = path
            self.documentChanged = False
            self.SetTitle(os.path.split(path)[-1] + ' - ' + self.startTitle)
            self.updateStatusBar()
        except:
            pass
        
    def saveChanges(self):
        if self.documentPath is None:
            filename = "Untitled"
        else:
            filename = self.documentPath
        msg = "The text in the %s file has changed.\n\nDo you want to save the changes?" % filename
        result = dialog.messageDialog(self, msg, 'textEditor', wx.ICON_EXCLAMATION | wx.YES_NO | wx.CANCEL)
        return result.returned

    def newFile(self, wizResult):
        self.documentPath = None
        self.documentChanged = True
        self.SetTitle(wizResult.projectName + ' - ' + self.startTitle)
        self.statusBar.text = wizResult.projectName
        self.components.projectName.text = wizResult.projectName
        self.components.projectIcon.text = ''
        self.components.baseDir.text = wizResult.baseDir
        self.components.projectDesc.text = wizResult.projectDesc
        self.components.mainScript.text = ''
        self.components.versionString.text = '0.1.1'
        self.components.scriptList.items = []
        self.components.resList.items = []
        self.components.pixmapList.items = []
        self.components.otherList.items = []
        
        # here's where we create a basic project definition
        self.project = ConfigParser.ConfigParser()
        self.UI2Project()
        
        # add in the remainder of the project default properties
        self.project.set('Project', 'build', '1')
        self.project.set('Project', 'docfilespath', 'doc')
        self.project.set('Project', 'buildfilespath', 'build')
        self.project.set('Project', 'distfilespath', 'dist')
        self.project.set('Project', 'pixmapspath', 'pixmaps')
        self.project.set('Project', 'tarballspath', 'tarballs')
        self.project.set('Project', 'onedir', '1')
        self.project.set('Project', 'ascii', '0')
        self.project.set('Project', 'striplib', '0')
        self.project.set('Project', 'console', '1') # best to have a console for new projects!
        self.project.set('Project', 'optimize', '1')
        self.project.set('Project', 'compress', '0')
        self.project.set('Project', 'debug', '0')
        self.project.set('Project', 'publisher', self.cfg.get('ConfigData', 'publisher'))
        self.project.set('Project', 'appurl', '')
        self.project.set('Project', 'status', 'open')
        
        self.project.set('Project', 'applicence', 'doc,gpl.txt')
        
        x = os.path.join('build', '%s.iss' % self.components.projectName.text)
        self.project.set('Project', 'innoscript', x)
        
        x = os.path.join('build', '%s.spec' % self.components.projectName.text)
        self.project.set('Project', 'specfile', x)
        
        self.project.set('Otherfiles', '0', os.path.join('doc', 'about.html'))
        self.project.set('Otherfiles', '1', os.path.join('doc', 'author.html'))
        self.project.set('Otherfiles', '2', os.path.join('doc', 'gpl.txt'))
        self.project.set('Otherfiles', '3', os.path.join('doc', 'gpl.html'))
        self.project.set('Otherfiles', '4', 'changelog.txt')
        self.project.set('Otherfiles', '5', 'readme.txt')
        
        self.createProject()
        self.Project2UI()
        self.on_menuFileSaveAs_select(None) # save the project
        self.updateStatusBar()
        
        for comp in self.components.keys():
            self.components[comp].enabled = 1
        
    def delItem(self, items, selected):
        newlist = []
        for item in items:
            if selected != item:
                newlist.append(item)
        if newlist != items:
            self.documentChanged = True
            self.updateStatusBar()
        return newlist
            
    def addItem(self, title, basepath, wildcard, current, refpath=None):
        x = current[:]
        result = dialog.openFileDialog(self, title, basepath, '', wildcard, wx.MULTIPLE)
        if result.accepted:
            for p in result.paths:
                if not os.path.exists(p):
                    title = 'Invalid filename!'
                    txt = '%s is not a valid filename!' % p
                    bull = dialog.alertDialog(self, wrap_string(txt, 70), title)
                else:
                    if refpath is None:
                        # we want the whole path to the item
                        path = os.path.basename(p)
                    else:
                        # we just want the part thats relative to 'refpath'
                        path = string.replace(p, refpath + os.sep, '')
                    if not (path in x):
                        x.append(path)
                        x.sort()
                        self.documentChanged = True
                        self.updateStatusBar()
                        self.Refresh()
        return x
        
    def rebuildLinux(self):
        # build a tarball for a Linux system
        # create a top level directory for the stuff to go in
        vstring = self.components.versionString.text
        tdir = self.project.get('Project', 'name')
        tdir += '-' + vstring
        tdir += '-' + self.project.get('Project', 'build')
        topdir = tdir
        tarball = tdir + '.tar.gz'
        tdir = os.path.join(self.components.baseDir.text, tdir)
        tdir = os.path.join(self.cfg.get('ConfigData', 'projects'), tdir)
        
        try:
            cmd = 'rm -rf %s' % tdir
            os.system(cmd)
            #os.removedirs(tdir)
        except:
            pass
        os.mkdir(tdir)
        
        # write everything out to a 'manifest.in' file
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        manifestfile = os.path.join(basedir, 'manifest.in')
        fd = open(manifestfile, 'w')
        
        fd.write(self.pathJoin(self.project.get('Project', 'mainscript')) + '\n') # main script file

        section = 'Scripts'
        self.sectionOutput(section, fd)

        section = 'ResourceFiles'
        self.sectionOutput(section, fd)

        section = 'Pixmaps'
        prefix = self.pathJoin(self.project.get('Project', 'pixmapspath'))
        self.sectionOutput(section, fd, prefix)

        section = 'Otherfiles'
        self.sectionOutput(section, fd)
        
        fd.close()
        
        # use cpio to copy everything listed in manifest.in into the temp
        # directory just created
        cmd = "cd %s; cat manifest.in|cpio -vdump %s" % (basedir, topdir)
        os.system(cmd)
        
        # now we can create the tarball, ensuring that the tarballs path
        # actually exists beforehand
        tb = os.path.join(basedir, self.pathJoin(self.project.get('Project', 'tarballspath')))
        try:
            os.mkdir(tb)
        except:
            pass
        tb = os.path.join(tb, tarball)
        cmd = "cd %s; tar -zcvf %s %s > /dev/null 2>&1" % (basedir, tb, topdir)
        os.system(cmd)
        
        # remove the temporary directory when done
        cmd = "cd %s; rm -rf %s" % (basedir, topdir)
        os.system(cmd)
        
    def checkImports(self):
        # if we're building from a PythonCard application, check that the
        # main script includes imports of the required PythonCard components
        imps = {}
        impline = 'from PythonCard.components import '
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        
        for res in self.components.resList.items:
            fullpath = str(os.path.join(basedir, res))
            res = util.readAndEvalFile(fullpath)
            try:
                comps = res['components']
            except:
                comps = res['application']['backgrounds'][0]['components']
            for comp in comps:
                type = comp['type']
                if not imps.has_key(type): imps[type] = 1
                
        ikeys = imps.keys()
        ikeys.sort()
        
        for i in ikeys:
            impline += i.lower() + ', '
            
        impline = impline[:-2]
        #print impline
        
        # read through the main script looking for a matching import line
        mainScript = os.path.join(basedir, str(self.components.mainScript.text))
        fd = open(mainScript)
        impFound = False
        
        line = fd.readline()
        while line:
            if line == impline + '\n':
                impFound = True
                break
            line = fd.readline()
        
        fd.close()
            
        return impFound, impline
        
    def buildWithpy2exe(self):
        # rebuild the application using py2exe
        basedir = str(os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text))
        mainScript = self.components.mainScript.text
        mainResource = str(mainScript.split('.py')[0] + '.rsrc.py')
        finalResource = str(self.components.projectName.text + '.rsrc.py')
        if mainResource != finalResource:
            fd = open(os.path.join(basedir, mainResource))
            res = fd.read()
            fd.close()
            fd = open(os.path.join(basedir, finalResource), 'w')
            fd.write(res)
            fd.close()
        origin = os.getcwd()
        os.chdir(basedir)
        
        # make sure we have a setup.py script in the current directory
        setupScript = os.path.join(basedir, 'setup.py')
        if not os.path.exists(setupScript):
            fd = open(setupScript, 'w')
            fd.write(self.setupCode)
            fd.close()
        
        specfile = os.path.join(basedir, self.components.projectName.text + '.spec')
        versionfile = os.path.join(basedir, 'versioninfo.txt')
        
        exefile = os.path.join(self.pathJoin(self.project.get('Project', 'buildfilespath')), self.project.get('Project', 'name') + '.exe')
        
        # write out all the files that make up the application into a list of
        # tuples that py2exe can deal with
        data_files = []
        tmp = ('.', [])

        # commented this out, as we don't need to explicitly distribute the extra python
        # modules that the main script imports - anything that does actually need
        # to be distributed should be added to the 'other files' list by the user
        #for script in self.components.scriptList.items: tmp[1].append(str(script))
            
        # then add in all resource files, which will also be in the top level
        # directory
        for res in self.components.resList.items:
            if res == mainResource:
                tmp[1].append(str(finalResource))
            else:
                tmp[1].append(str(res))
            
        # and anything in the 'other files' list which doesn't appear to be in
        # its own sub-directory
        for other in self.components.otherList.items:
            if not os.sep in other: tmp[1].append(str(other))
            
        data_files.append(tmp)
        
        # add in all the pixmap files
        pixmap = self.project.get('Project', 'pixmapspath')
        tmp = (str(pixmap), [])
        for pix in self.components.pixmapList.items: tmp[1].append(str(os.path.join(pixmap, pix)))
        data_files.append(tmp)
        
        # now process everything in the 'other files' list that lives in its
        # own subdirectory, generating a tuple for each sub-directoy found
        subdirs = {}
        for item in self.components.otherList.items:
            item = str(item)
            if os.sep in item:
                d = string.split(item, os.sep)
                if subdirs.has_key(d[0]):
                    ilist = subdirs[d[0]]
                    ilist.append(item)
                else:
                    ilist = []
                    ilist.append(item)
                subdirs[d[0]] = ilist
        for subdir in subdirs.keys():
            data_files.append((subdir, subdirs[subdir]))
            
        # write the data_files information out to a file where the setup script
        # can read it from
        fd = open('datafiles.dat', 'w')
        pprint.pprint(data_files, fd)
        fd.close()
        
        # build a second dictionary which is used to define the application
        # itself to py2exe
        standalone = {}
        standalone['script'] = str(self.components.mainScript.text)
        standalone['dest_base'] = self.project.get('Project', 'name')
        if self.components.projectIcon.text != '':
            standalone['icon_resources'] = [(1, str(self.components.projectIcon.text))]
        fd = open('standalone.dat', 'w')
        pprint.pprint(standalone, fd)
        fd.close()
        
        # create a data file which tells the setup script whether we want a console
        # build or not
        fd = open('buildoptions.dat', 'w')
        buildOpts = {}
        if self.project.getboolean('Project', 'console'):
            buildOpts['buildType'] = 'console'
        else:
            buildOpts['buildType'] = 'windows'
        pprint.pprint(buildOpts, fd)
        fd.close()
            
        # run the setup script and capture the output
        cmd = 'python setup.py py2exe'
        stin, stout, sterr = os.popen3(cmd)
        stin.close()
        result = stout.readline()
        while result:
            self.outputWindow.addLine(result)
            self.outputWindow.Update()
            self.outputWindow.Refresh()
            result = stout.readline()
        stout.close()
        
        # see if there were any errors
        allokay = True
        result = sterr.readline()
        while result:
            allokay = False
            self.outputWindow.addLine(result)
            self.outputWindow.Update()
            self.outputWindow.Refresh()
            result = sterr.readline()
        sterr.close()

        # update the version information in the executable
        if allokay:
            basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
            exefile = os.path.join(basedir, self.project.get('Project', 'distfilespath'))
            exefile = os.path.join(exefile, self.project.get('Project', 'name'))
            exefile += '.exe'
            versionfile = os.path.join(basedir, 'versioninfo.txt')
            versionInfo.SetVersion(exefile, versionfile)
            
        # flip back to the original working directory
        os.chdir(origin)
            
        return allokay
        
    def buildSpecFile(self):
        # build a spec file and write it to disk
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        specfile = os.path.join(basedir, self.components.projectName.text + '.spec')
        versionfile = os.path.join(basedir, 'versioninfo.txt')
        exefile = os.path.join(self.pathJoin(self.project.get('Project', 'buildfilespath')), self.project.get('Project', 'name') + '.exe')
        mainScript = self.components.mainScript.text
        mainResource = mainScript.split('.py')[0] + '.rsrc.py'
        finalResource = self.components.projectName.text + '.rsrc.py'
        
        spec = []
        spec.append("p = '%s%s' # defines project root directory" % (basedir, os.sep))
        spec.append("a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'),")
        spec.append("    os.path.join(HOMEPATH,'support\\useUnicode.py'),")
        spec.append("    p + '%s']," % self.components.mainScript.text)
        spec.append("    pathex=['%s'])" % self.cfg.get('ConfigData', 'installerpath'))
        spec.append("pyz = PYZ(a.pure)")
        spec.append("exe = EXE(pyz,")
        spec.append("          a.scripts,")
        spec.append("          exclude_binaries=1,")
        spec.append("          name='%s'," % exefile)
        
        if int(self.project.getboolean('Project', 'debug')) == 1:
            spec.append("          debug=True,")
        else:
            spec.append("          debug=False,")
            
        if int(self.project.getboolean('Project', 'striplib')) == 1:
            spec.append("          strip=True,")
        else:
            spec.append("          strip=False,")
            
        if int(self.project.getboolean('Project', 'compress')) == 1:
            spec.append("          upx=True,")
        else:
            spec.append("          upx=False,")
            
        if int(self.project.getboolean('Project', 'console')) == 1:
            spec.append("          console=True,")
        else:
            spec.append("          console=False,")
        
        if self.components.projectIcon.text != '':
            iconfile = os.path.join(basedir, self.components.projectIcon.text)
            spec.append("          icon = '%s'," % iconfile)
            
        spec.append("          version = '%s')" % versionfile)
        spec.append("coll = COLLECT(exe,")
        spec.append("               a.binaries,")
        
        # add in all the resource files
        for res in self.components.resList.items:
            if res == mainResource:
                spec.append("               [('%s', p + '%s', 'DATA')]," % (finalResource, res))
            else:
                spec.append("               [('%s', p + '%s', 'DATA')]," % (res, res))
            
        # add in all the pixmap files
        for p in self.components.pixmapList.items:
            pixmap = os.path.join(self.project.get('Project', 'pixmapspath'), p)
            spec.append("               [('%s', p + '%s', 'DATA')]," % (pixmap, pixmap))
            
        # add in all the other files
        for other in self.components.otherList.items:
            spec.append("               [('%s', p + '%s', 'DATA')]," % (other, other))
            
        # last few bits and bobs
        #spec.append("               strip=%s," % int(self.project.getboolean('Project', 'striplib')))
        #spec.append("               upx=%s," % int(self.project.getboolean('Project', 'compress')))
        
        if int(self.project.getboolean('Project', 'striplib')) == 1:
            spec.append("           strip=True,")
        else:
            spec.append("           strip=False,")
            
        if int(self.project.getboolean('Project', 'compress')) == 1:
            spec.append("           upx=True,")
        else:
            spec.append("           upx=False,")
            
        spec.append("               name='%s')" % self.project.get('Project', 'distfilespath'))
        
        fd = open(specfile, 'w')
        for s in spec:
            s = string.replace(s, os.sep, self.PATHSEP)
            fd.write(s + '\n')
        fd.close()

    def buildVersionFile(self):
        # build a versioninfo file and write it to disk
        VINFO = open(os.path.join('templates', 'versioninfo.txt')).read()
        vinfo = {}
        vinfo['major'] = self.project.get('Project', 'majorversion')
        vinfo['minor'] = self.project.get('Project', 'minorversion')
        vinfo['fix'] = self.project.get('Project', 'fixnumber')
        vinfo['build'] = self.project.getint('Project', 'build')
        vinfo['name'] = self.project.get('Project', 'name')
        vinfo['date'] = time.strftime('%Y%m%d').upper()
        vinfo['publisher'] = self.project.get('Project', 'publisher')
        vinfo['desc'] = self.project.get('Project', 'projectdesc')
        vinfo['companyname'] = self.cfg.get('ConfigData', 'companyname')
        
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        versionfile = os.path.join(str(basedir), 'versioninfo.txt')
        #bull = raw_input('should now have [%s]' % versionfile)
        
        fd = open(versionfile, 'w')
        fd.write(VINFO % vinfo)
        fd.close()
        
    def buildApplication(self):
        # run the pyInstaller build script and capture the output
        if sys.platform.startswith('win'):
            cmd = 'python ' + GetShortPathName(self.cfg.get('ConfigData', 'installerpath'))
        else:
            cmd = self.cfg.get('ConfigData', 'installerpath')

        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        specfile = os.path.join(basedir, self.components.projectName.text + '.spec') # possible bug???
        cmd += ' "' + specfile + '" -o "' + os.path.join(basedir, self.pathJoin(self.project.get('Project','buildfilespath'))) + '"'
        stin, stout, sterr = os.popen3(cmd)
        stin.close()
        result = stout.readline()
        while result:
            self.outputWindow.addLine(result)
            self.outputWindow.Update()
            self.outputWindow.Refresh()
            result = stout.readline()
        stout.close()
        
        # see if there were any errors
        allokay = True
        result = sterr.readline()
        while result:
            allokay = False
            self.outputWindow.addLine(result)
            self.outputWindow.Update()
            self.outputWindow.Refresh()
            result = sterr.readline()
        sterr.close()
            
        return allokay
        
    def buildInnoFile(self):
        # rebuild the Inno Setup spec file
        inno = []
        
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        
        innofile = self.components.projectName.text + '.iss'
        innofile = os.path.join(basedir, innofile)
        
        inno.append('; script auto-generated by standaloneBuilder - do not edit!')
        inno.append('')
        
        inno.append('[Setup]')
        inno.append('AppName=%s' % self.project.get('Project', 'name'))
        appverstring = self.project.get('Project', 'name') + ' '
        appverstring += self.project.get('Project', 'majorversion') + '.'
        appverstring += self.project.get('Project', 'minorversion') + '.'
        appverstring += self.project.get('Project', 'fixnumber')
        inno.append('AppVerName=%s' % appverstring)
        
        if self.project.get('Project', 'publisher') != '':
            inno.append('AppPublisher=%s' % self.project.get('Project', 'publisher'))
        
        if self.project.get('Project', 'appurl') != '':
            inno.append('AppPublisherURL=%s' % self.project.get('Project', 'appurl'))
        
        if self.project.get('Project', 'appurl') != '':
            inno.append('AppSupportURL=%s' % self.project.get('Project', 'appurl'))
            
        if self.project.get('Project', 'appurl') != '':
            inno.append('AppUpdatesURL=%s' % self.project.get('Project', 'appurl'))
            
        inno.append('DefaultDirName={pf}%s' % (chr(92) + self.project.get('Project', 'name')))
        inno.append('DefaultGroupName=%s' % self.project.get('Project', 'name'))
        inno.append('AllowNoIcons=yes')
        
        if self.project.get('Project', 'applicence') != '':
            licencefile = os.path.join(basedir,self.pathJoin(self.project.get('Project', 'applicence')))
            inno.append('LicenseFile=%s' % licencefile)
            
        infofile = os.path.join(basedir, 'changelog.txt')
        inno.append('InfoBeforeFile=%s' % infofile)
        
        outputfile = self.project.get('Project', 'name') + '-'
        outputfile += self.project.get('Project', 'majorversion') + '.'
        outputfile += self.project.get('Project', 'minorversion') + '.'
        outputfile += self.project.get('Project', 'fixnumber') + '-'
        outputfile += self.project.get('Project', 'build')
        
        inno.append('OutputBaseFilename=%s' % outputfile)
        inno.append('')
        inno.append('[Tasks]')
        inno.append('Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked')
        inno.append('Name: "quicklaunchicon"; Description: "Create a &Quick Launch icon"; GroupDescription: "Additional icons:"; Flags: unchecked')
        inno.append('')
        inno.append('[Files]')
        
        outputDir = os.path.join(basedir, self.pathJoin(self.project.get('Project', 'distfilespath')))
        
        for f in os.listdir(outputDir):
            fullname = os.path.join(outputDir, f)
            if not os.path.isdir(fullname): 
                inno.append('Source: "%s"; DestDir: "{app}"; Flags: ignoreversion' % fullname)
            else:
                x = len(os.listdir(fullname))
                if x > 0: inno.append('Source: "%s\\*"; DestDir: "{app}\\%s"; Flags: ignoreversion recursesubdirs' % (fullname, f))
                
        inno.append('')
        inno.append('[Icons]')
        inno.append('Name: "{group}\\%s"; Filename: "{app}\\%s.exe"' % (self.project.get('Project', 'name'), self.project.get('Project', 'name').lower()))
        inno.append('Name: "{userdesktop}\\%s"; Filename: "{app}\\%s.exe"; Tasks: desktopicon' % (self.project.get('Project', 'name'), self.project.get('Project', 'name').lower()))
        inno.append('Name: "{userappdata}\\Microsoft\\Internet Explorer\\Quick Launch\\%s"; Filename: "{app}\\%s.exe"; Tasks: quicklaunchicon' % (self.project.get('Project', 'name'), self.project.get('Project', 'name').lower()))
        fd = open(innofile, 'w')
        for s in inno:
            s = string.replace(s, os.sep, self.PATHSEP)
            fd.write(s + '\n')
        fd.close()

    def buildInstaller(self):
        # rebuild the distributable
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        innofile = self.components.projectName.text + '.iss'
        innofile = os.path.join(basedir, innofile)

        try:
            import ctypes
        except ImportError:
            try:
                import win32api
            except ImportError:
                #import os
                os.startfile(innofile)
            else:
                win32api.ShellExecute(0, "compile", innofile, None, None, 0)
        else:
            res = ctypes.windll.shell32.ShellExecuteA(0, "compile", innofile, None, None, 0)
            if res < 32:
                raise RuntimeError, "ShellExecute failed, error %d" % res
        
    def freezeProject(self):
        # freeze the project for a release
        frozen = False
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        chglog = os.path.join(basedir, 'changelog.txt')
        newchglog = os.path.join(basedir, 'changelog-new.txt')
        
        fd = open(chglog, 'r')
        log = fd.readlines()
        fd.close()
        
        # There should be a 'TBA' tag in the first line
        if 'TBA' in log[0]:
            rdate = time.strftime('%B %d %Y')
            log[0] = string.replace(log[0], 'TBA', rdate)
            dashes = '-' * (len(log[0]) - 1)
            log[1] = dashes + '\n'
            fd = open(newchglog, 'w')
            for line in log:
                fd.write(line)
            fd.close()
            os.unlink(chglog)
            os.rename(newchglog, chglog)
            self.project.set('Project', 'status', 'frozen')
            self.documentChanged = True
            for comp in self.components.keys():
                if self.components[comp].userdata != 'frozen':
                    self.components[comp].enabled = False
            self.updateStatusBar()
            frozen = True
        else:
            title = 'Release error!'
            txt = 'Release date tag seems to be missing from the changelog file!'
            bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
            
        return frozen
            
    def releaseProject(self):
        # confirm a release
        released = False
        basedir = os.path.join(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        
        # first confirm what the new version number will be
        vstring = self.components.versionString.text
        dlg = versionDialog(self, vstring)
        if dlg.ShowModal() != wx.ID_OK: return 0
        vstring = dlg.getVersion() # returns a list-type
        template = {}
        template['name'] = self.components.projectName.text
        template['major'] = vstring[0]
        template['minor'] = vstring[1]
        template['fix'] = vstring[2]
        
        # now prepend this to the top of the changelog
        tmplfile = os.path.join('templates', 'changelog.txt')
        chglogData = open(tmplfile, 'r').read()
        chglogData = chglogData % template
        dashes = '-' * len(chglogData)

        chglog = os.path.join(basedir, 'changelog.txt')
        fd = open(chglog, 'r')
        log = fd.readlines()
        fd.close()
        
        newchglog = os.path.join(basedir, 'changelog-new.txt')
        fd = open(newchglog, 'w')
        fd.write(chglogData) # new stuff
        fd.write(dashes + '\n')
        fd.write('\n\n') # couple of blank lines
        for line in log:
            fd.write(line)
        fd.close()
        
        os.unlink(chglog)
        os.rename(newchglog, chglog)
        
        # update the project and UI with the new version number and un-freeze
        self.project.set('Project', 'majorversion', vstring[0])
        self.project.set('Project', 'minorversion', vstring[1])
        self.project.set('Project', 'fixnumber', vstring[2])
        self.project.set('Project', 'build', '1')
        self.project.set('Project', 'status', 'open')
        self.components.versionString.text = vstring[0] + '.' + vstring[1] + '.' + vstring[2]
        self.documentChanged = True
        self.updateStatusBar()
        released = True
        for comp in self.components.keys():
            self.components[comp].enabled = True
                
        return released
        
##############################################################################
# third level stuff - routines called by the second level code
#
##############################################################################
    def createConfig(self):
        # create a config file the first time pimp is run
        title = 'Initial setup'
        txt = 'Since this is the first time you have run standaloneBuilder, you need to configure '
        txt += 'the program according to your preferences. Most users should find that the '
        txt += 'default settings are satisfactory.\n\nOn this system, settings will be stored '
        txt += 'in "%s". In the preferences dialog, you can click the "?" buttons to get ' % self.CONFIG_FILE
        txt += 'help with any of the options.\n\nClick OK to begin configuring standaloneBuilder.'
        bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
        
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.add_section('ConfigData')
        
        # see if we have the PythonCard code editor
        want = os.path.join('PythonCard', 'tools')
        want = os.path.join(want, 'codeEditor')
        want = os.path.join(want, 'codeEditor.py')
        editor = self.lookFor(want)
        self.cfg.set('ConfigData', 'codeeditor', editor)
            
        # see if we have the PythonCard resource editor
        # C:\Python23\Lib\site-packages\PythonCard\tools\resourceEditor
        want = os.path.join('PythonCard', 'tools')
        want = os.path.join(want, 'resourceEditor')
        want = os.path.join(want, 'resourceEditor.py')
        resedit = self.lookFor(want)
        self.cfg.set('ConfigData', 'reseditor', resedit)
        
        self.cfg.set('ConfigData', 'pixmapeditor', '')
        self.cfg.set('ConfigData', 'texteditor', editor)
        
        # see if we can find pyInstaller
        # C:\Python23\pyInstaller\Build.py
        want = os.path.join('pyInstaller', 'Build.py')
        installer = self.lookFor(want)
        self.cfg.set('ConfigData', 'installerpath', installer)
        
        if installer == '':
            self.cfg.set('ConfigData', 'buildtool', 'py2exe')
        else:
            self.cfg.set('ConfigData', 'buildtool', 'pyInstaller')
        
        # see if we can find the Inno Setup command line compiler
        # C:\Program Files\Inno Setup 5\ISCC.exe
        want = os.path.join('Inno Setup 5', 'ISCC.exe')
        compiler = self.lookFor(want)
        self.cfg.set('ConfigData', 'compilerpath', compiler)
        
        self.cfg.set('ConfigData', 'publisher', '')
        self.cfg.set('ConfigData', 'companyname', '')
        
        if sys.platform.startswith('linux') or sys.platform.startswith('freebsd'):
            projdir = os.path.expanduser('~')
            projdir = os.path.join(projdir, 'proj')
        else:
            projdir = ''
        self.cfg.set('ConfigData', 'projects', projdir)
        
        dlg = prefsDialog(self, self.CONFIG_FILE)
        
        if dlg.ShowModal() != wx.ID_OK:
            title = 'Preferences not saved!'
            txt = 'You must configure your preferences before using standaloneBuilder!'
            bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
            dlg.destroy()
            sys.exit(1)
            
        dlg.Destroy()
            
    def UI2Project(self):
        # update the project object
        try:
            self.project.add_section('Project')
        except:
            pass
            
        vstring = string.split(self.components.versionString.text, '.')
        self.project.set('Project', 'majorversion', str(vstring[0]))
        self.project.set('Project', 'minorversion', str(vstring[1]))
        self.project.set('Project', 'fixnumber', str(vstring[2]))
        self.project.set('Project', 'name', self.components.projectName.text)
        
        # set the project basepath, we need to split off the top level projects
        # folder as defined in prefs
        base = self.getRelativePath(self.cfg.get('ConfigData', 'projects'), self.components.baseDir.text)
        base = self.pathSplit(base)
        self.project.set('Project', 'basepath', base)
        
        self.project.set('Project', 'projectdesc', self.components.projectDesc.text)
        self.project.set('Project', 'mainscript', self.pathSplit(self.components.mainScript.text))
        self.project.set('Project', 'iconfile', self.pathSplit(self.components.projectIcon.text))
        self.project.set('Project', 'innoscript', '%s.iss' % self.components.projectName.text)
        self.project.set('Project', 'specfile', '%s.spec' % self.components.projectName.text)
        
        try:
            self.project.remove_section('Scripts')
            self.project.add_section('Scripts')
        except:
            pass
            
        cnt = 0
        for item in self.components.scriptList.items:
            self.project.set('Scripts', str(cnt), self.pathSplit(item))
            cnt += 1
            
        try:
            self.project.remove_section('ResourceFiles')
            self.project.add_section('ResourceFiles')
        except:
            pass
            
        cnt = 0
        for item in self.components.resList.items:
            self.project.set('ResourceFiles', str(cnt), self.pathSplit(item))
            cnt += 1

        try:
            self.project.remove_section('Otherfiles')
            self.project.add_section('Otherfiles')
        except:
            pass
            
        cnt = 0
        for item in self.components.otherList.items:
            self.project.set('Otherfiles', str(cnt), self.pathSplit(item))
            cnt += 1

        try:
            self.project.add_section('Pixmaps')
        except:
            pass
            
        cnt = 0
        for item in self.components.pixmapList.items:
            self.project.set('Pixmaps', str(cnt), self.pathSplit(item))
            cnt += 1
            
    def pathSplit(self, item):
        # splits a path up into comma separated sections
        out = string.replace(item, os.sep, ',')
        return out
    
    def updateStatusBar(self):
        string = self.components.projectName.text
        string += '-'
        string += self.components.versionString.text
        string += ' (Build ' + self.project.get('Project', 'build') + ')'
        string += ' - Release status: %s' % self.project.get('Project', 'status')
        mod = ''
        if self.documentChanged: mod = ' *'
        if self.documentPath is not None:
            self.SetTitle(self.startTitle + ' - [' + os.path.split(self.documentPath)[-1] + mod + ']')
        else:
            self.SetTitle(self.startTitle + ' - [Untitled' + mod + ']')
            
        self.statusBar.text = string
        try:
            wx.Yield()
        except:
            pass
            
    def createProject(self):
        # create all the folders and other gubbins
        basepath = os.path.join(self.cfg.get('ConfigData', 'projects'), self.pathJoin(self.project.get('Project', 'basepath')))
      
        try:
            os.mkdir(os.path.join(basepath, self.project.get('Project', 'buildfilespath')))
        except:
            pass
            
        try:
            os.mkdir(os.path.join(basepath, self.project.get('Project', 'distfilespath')))
        except:
            pass
            
        try:
            os.mkdir(os.path.join(basepath, self.project.get('Project', 'pixmapspath')))
        except:
            pass
            
        try:
            os.mkdir(os.path.join(basepath, self.project.get('Project', 'tarballspath')))
        except:
            pass
            
        try:
            os.mkdir(os.path.join(basepath, self.project.get('Project', 'docfilespath')))
        except:
            pass
        
        # copy in various things from templates
        templatedir = os.path.dirname(os.path.abspath(__file__))
        templatedir = os.path.join(templatedir, 'templates')
        
        vinfo = {}
        vinfo['major'] = self.project.get('Project', 'majorversion')
        vinfo['minor'] = self.project.get('Project', 'minorversion')
        vinfo['fix'] = self.project.get('Project', 'fixnumber')
        vinfo['build'] = str('%04d' % self.project.getint('Project', 'build'))
        vinfo['name'] = self.project.get('Project', 'name')
        vinfo['date'] = time.strftime('%Y%b%d').upper()
        vinfo['publisher'] = self.project.get('Project', 'publisher')
        vinfo['desc'] = self.project.get('Project', 'projectdesc')
        vinfo['appurl'] = self.project.get('Project', 'appurl')
        
        # HTML about page
        VINFO = open(os.path.join(templatedir, 'about.html')).read()
        afile = os.path.join(basepath, self.project.get('Project', 'docfilespath'))
        afile = os.path.join(afile, 'about.html')
        if os.path.exists(afile):
            txt = '%s already exists. Would you like to overwrite this' % (afile)
            txt += ' file with a new version?'
            result = dialog.messageDialog(self, wrap_string(txt, 60), 'Please confirm',
                wx.ICON_EXCLAMATION|wx.YES_NO|wx.NO_DEFAULT)
            if result.accepted:
                fd = open(afile, 'w')
                fd.write(VINFO % vinfo)
                fd.close()
        else:
            fd = open(afile, 'w')
            fd.write(VINFO % vinfo)
            fd.close()
        
        # HTML author page
        VINFO = open(os.path.join(templatedir, 'author.html')).read()
        afile = os.path.join(basepath, self.project.get('Project', 'docfilespath'))
        afile = os.path.join(afile, 'author.html')
        if os.path.exists(afile):
            txt = '%s already exists. Would you like to overwrite this' % (afile)
            txt += ' file with a new version?'
            result = dialog.messageDialog(self, wrap_string(txt, 60), 'Please confirm',
                wx.ICON_EXCLAMATION|wx.YES_NO|wx.NO_DEFAULT)
            if result.accepted:
                fd = open(afile, 'w')
                fd.write(VINFO % vinfo)
                fd.close()
        else:
            fd = open(afile, 'w')
            fd.write(VINFO % vinfo)
            fd.close()
        
        # HTML GPL license text page
        VINFO = open(os.path.join(templatedir, 'gpl.html')).read()
        afile = os.path.join(basepath, self.project.get('Project', 'docfilespath'))
        afile = os.path.join(afile, 'gpl.html')
        if os.path.exists(afile):
            txt = '%s already exists. Would you like to overwrite this' % (afile)
            txt += ' file with a new version?'
            result = dialog.messageDialog(self, wrap_string(txt, 60), 'Please confirm',
                wx.ICON_EXCLAMATION|wx.YES_NO|wx.NO_DEFAULT)
            if result.accepted:
                fd = open(afile, 'w')
                fd.write(VINFO % vinfo)
                fd.close()
        else:
            fd = open(afile, 'w')
            fd.write(VINFO % vinfo)
            fd.close()
        
        # plaintext GPL license text page
        VINFO = open(os.path.join(templatedir, 'gpl.txt')).read()
        afile = os.path.join(basepath, self.project.get('Project', 'docfilespath'))
        afile = os.path.join(afile, 'gpl.txt')
        if os.path.exists(afile):
            txt = '%s already exists. Would you like to overwrite this' % (afile)
            txt += ' file with a new version?'
            result = dialog.messageDialog(self, wrap_string(txt, 60), 'Please confirm',
                wx.ICON_EXCLAMATION|wx.YES_NO|wx.NO_DEFAULT)
            if result.accepted:
                fd = open(afile, 'w')
                fd.write(VINFO % vinfo)
                fd.close()
        else:
            fd = open(afile, 'w')
            fd.write(VINFO % vinfo)
            fd.close()
        
        # changelog template
        VINFO = open(os.path.join(templatedir, 'changelog.txt')).read()
        afile = os.path.join(basepath, 'changelog.txt')
        if os.path.exists(afile):
            txt = '%s already exists. Would you like to overwrite this' % (afile)
            txt += ' file with a new version?'
            result = dialog.messageDialog(self, wrap_string(txt, 60), 'Please confirm',
                wx.ICON_EXCLAMATION|wx.YES_NO|wx.NO_DEFAULT)
            if result.accepted:
                fd = open(afile, 'w')
                txtline = VINFO % vinfo
                dashes = '-' * len(txtline)
                fd.write(txtline)
                fd.write(dashes + '\n')
                fd.close()
        else:
            fd = open(afile, 'w')
            txtline = VINFO % vinfo
            dashes = '-' * len(txtline)
            fd.write(txtline)
            fd.write(dashes + '\n')
            fd.close()
        
        # readme template
        VINFO = open(os.path.join(templatedir, 'readme.txt')).read()
        afile = os.path.join(basepath, 'readme.txt')
        if os.path.exists(afile):
            txt = '%s already exists. Would you like to overwrite this' % (afile)
            txt += ' file with a new version?'
            result = dialog.messageDialog(self, wrap_string(txt, 60), 'Please confirm',
                wx.ICON_EXCLAMATION|wx.YES_NO|wx.NO_DEFAULT)
            if result.accepted:
                fd = open(afile, 'w')
                fd.write(VINFO % vinfo)
                fd.close()
        else:
            fd = open(afile, 'w')
            fd.write(VINFO % vinfo)
            fd.close()
                        
    def Project2UI(self):
        vstring = (self.project.get('Project', 'majorversion')) +'.'
        vstring += (self.project.get('Project', 'minorversion')) + '.'
        vstring += (self.project.get('Project', 'fixnumber'))
        self.components.versionString.text = vstring
        self.components.projectName.text = self.project.get('Project', 'name')
        self.components.baseDir.text = self.pathJoin(self.project.get('Project', 'basepath'))
        self.components.projectDesc.text = self.project.get('Project', 'projectdesc')
        self.components.mainScript.text = self.pathJoin(self.project.get('Project', 'mainscript'))
        self.components.projectIcon.text = self.pathJoin(self.project.get('Project', 'iconfile'))
        self.components.scriptList.items = self.sectionOutput('Scripts')
        self.components.resList.items = self.sectionOutput('ResourceFiles')
        self.components.otherList.items = self.sectionOutput('Otherfiles')
        self.components.pixmapList.items = self.sectionOutput('Pixmaps')
        
    def sectionOutput(self, section, fd=None, prefix=None):
        # take a section of a project file and either output
        # it to a given filehandle or add it to a list. In both
        # cases, os-specific path separators are added as
        # required
        
        cnt = 0
        list = []
        
        while 1:
            try:
                item = self.project.get(section, str(cnt))
            except:
                break
            else:
                if prefix is not None: item = os.path.join(prefix, item)
                if fd is None:
                    list.append(self.pathJoin(item))
                else:
                    fd.write(self.pathJoin(item) + '\n')
                cnt += 1
                
        return list
        
    def pathJoin(self, item):
        # replace commas with os-specific path separators
        if ',' in item:
            ilist = string.split(item, ',')
            result = ''
            for part in ilist:
                result = os.path.join(result, part)
            item = result
        return item
    
    def lookFor(self, want):
        found = ''
        searchpaths = sys.path
        
        if sys.platform.startswith('linux') or sys.platform.startswith('freebsd'):
            searchpaths.append('/usr/share')
        
        if sys.platform.startswith('win'):
            searchpaths.append('C:\\Program Files')
            
        for search in searchpaths:
            if os.path.exists(os.path.join(search, want)):
                found = os.path.join(search, want)
                break
                    
        return found
            
    def openFile(self, path):
        self.project = ConfigParser.ConfigParser()
        self.project.read(path)
        self.documentPath = path
        self.documentChanged = False
        self.SetTitle(os.path.split(path)[-1] + ' - ' + self.startTitle)
        self.Project2UI()
        self.updateStatusBar()
        
        pstatus = self.project.get('Project', 'status')
        
        if pstatus == 'frozen':
            title = 'Frozen project'
            txt = 'This release of the %s project has been frozen ready ' % self.project.get('Project', 'name')
            txt += 'for release. The project '
            txt += 'should be rebuilt on all the platforms you are interested in.\n\nYou '
            txt += 'should then click the release button to un-freeze the '
            txt += 'project and initialize the next version.'
            bull = dialog.alertDialog(self, wrap_string(txt, 60), title)            
            for comp in self.components.keys():
                if self.components[comp].userdata != pstatus:
                    self.components[comp].enabled = False
                else:
                    self.components[comp].enabled = True
            self.menuBar.setEnabled('menuFileNew', True)
            self.menuBar.setEnabled('menuFileOpen', True)
            self.menuBar.setEnabled('menuFileSave', False)
            self.menuBar.setEnabled('menuFileSaveAs', False)
            self.menuBar.setEnabled('menuFileExit', True)
            self.menuBar.setEnabled('menuEditMainScript', False)
            self.menuBar.setEnabled('menuEditChglog', False)
            self.menuBar.setEnabled('menuEditReadme', False)
            self.menuBar.setEnabled('menuEditSpecfile', False)
            self.menuBar.setEnabled('menuEditInnoFile', False)
            self.menuBar.setEnabled('menuEditProps', False)
            self.menuBar.setEnabled('menuEditPrefs', True)
            self.menuBar.setEnabled('menuToolsLogAdd', False)
            self.menuBar.setEnabled('menuToolsChkImport', False)
            self.menuBar.setEnabled('menuToolsAddScript', False)
            self.menuBar.setEnabled('menuToolsAddResource', False)
            self.menuBar.setEnabled('menuToolsAddPixmap', False)
            self.menuBar.setEnabled('menuToolsAddOther', False)
            self.menuBar.setEnabled('menuToolsRunMain', False)
            self.menuBar.setEnabled('menuToolsRebuild', True)
            self.menuBar.setEnabled('menuToolsRelease', True)
            self.menuBar.setEnabled('menuHelpManual', True)
            self.menuBar.setEnabled('menuHelpAbout', True)
                    
        if pstatus == 'open':
            for comp in self.components.keys(): self.components[comp].enabled = True
            self.menuBar.setEnabled('menuFileNew', True)
            self.menuBar.setEnabled('menuFileOpen', True)
            self.menuBar.setEnabled('menuFileSave', True)
            self.menuBar.setEnabled('menuFileSaveAs', True)
            self.menuBar.setEnabled('menuFileExit', True)
            self.menuBar.setEnabled('menuEditMainScript', True)
            self.menuBar.setEnabled('menuEditChglog', True)
            self.menuBar.setEnabled('menuEditReadme', True)
            self.menuBar.setEnabled('menuEditSpecfile', True)
            self.menuBar.setEnabled('menuEditInnoFile', True)
            self.menuBar.setEnabled('menuEditProps', True)
            self.menuBar.setEnabled('menuEditPrefs', True)
            self.menuBar.setEnabled('menuToolsLogAdd', True)
            self.menuBar.setEnabled('menuToolsChkImport', True)
            self.menuBar.setEnabled('menuToolsAddScript', True)
            self.menuBar.setEnabled('menuToolsAddResource', True)
            self.menuBar.setEnabled('menuToolsAddPixmap', True)
            self.menuBar.setEnabled('menuToolsAddOther', True)
            self.menuBar.setEnabled('menuToolsRunMain', True)
            self.menuBar.setEnabled('menuToolsRebuild', True)
            self.menuBar.setEnabled('menuToolsRelease', True)
            self.menuBar.setEnabled('menuHelpManual', True)
            self.menuBar.setEnabled('menuHelpAbout', True)
            if self.cfg.get('ConfigData', 'buildtool') != 'pyInstaller':
                self.components.specBtn.enabled = False
                self.menuBar.setEnabled('menuEditSpecfile', False)
            else:
                self.components.specBtn.enabled = True
                self.menuBar.setEnabled('menuEditSpecfile', True)

if __name__ == '__main__':
    app = model.Application(standaloneBuilder)
    app.MainLoop()
