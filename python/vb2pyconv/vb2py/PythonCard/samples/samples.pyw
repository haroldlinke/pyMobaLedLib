#!/usr/bin/python

"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2005/03/28 05:37:31 $"
"""

from PythonCard import about, dialog, model
import os, sys
import webbrowser
import wx

class Launcher(model.Background):

    def setupSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        comp = self.components
        
        btnFlags = wx.LEFT | wx.ALIGN_BOTTOM
        vertFlags = wx.LEFT | wx.TOP | wx.ALIGN_LEFT

        sizer4.Add(comp.btnLaunch, 1, btnFlags, 5)
        sizer4.Add(comp.btnDescription, 1, btnFlags, 5)
        sizer4.Add(comp.btnSource, 1, btnFlags, 5)
        sizer4.Add(comp.btnResource, 1, btnFlags, 5)

        sizer3.Add(comp.stcCmdLineArgs, 0, wx.LEFT | wx.BOTTOM | wx.ALIGN_TOP, 5)
        sizer3.Add(comp.chkDebugMenu, 0, vertFlags, 5)
        sizer3.Add(comp.chkLogging, 0, vertFlags, 5)
        sizer3.Add(comp.chkMessageWatcher, 0, vertFlags, 5)
        sizer3.Add(comp.chkNamespaceViewer, 0, vertFlags, 5)
        sizer3.Add(comp.chkPropertyEditor, 0, vertFlags, 5)
        sizer3.Add(comp.chkShell, 0, vertFlags, 5)
        sizer3.Add((5, 5), 1)  # spacer
        sizer3.Add(sizer4, 1, wx.ALIGN_BOTTOM | wx.EXPAND)

        sizer2.Add(comp.listSamples, 0, wx.RIGHT | wx.ALIGN_TOP, 5)
        sizer2.Add(sizer3, 1, wx.EXPAND)

        sizer1.Add(sizer2, 0, vertFlags)
        sizer1.Add((5, 5), 0)  # spacer
        sizer1.Add(comp.stcDescription, 0, wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_LEFT | wx.EXPAND, 5)
        sizer1.Add(comp.fldDescription, 1, wx.EXPAND)
        self.sizer1 = sizer1
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()
        self.visible = True

    def on_initialize(self, event):
        self.setupSizers()
        
        self.showDescription()
        try:
            self.readme = open('readme.txt').read()
        except:
            self.readme = ''

    def getCommandLineArgs(self):
        args = []
        if self.components.chkDebugMenu.checked:
            args.append('-d')
        if self.components.chkLogging.checked:
            args.append('-l')
        if self.components.chkMessageWatcher.checked:
            args.append('-m')
        if self.components.chkNamespaceViewer.checked:
            args.append('-n')
        if self.components.chkPropertyEditor.checked:
            args.append('-p')
        if self.components.chkShell.checked:
            args.append('-s')
        return args

    def on_launch_command(self, event):
        name = self.components.listSamples.stringSelection
        if name == "samples":
            path = self.application.applicationDirectory
        else:
            path = os.path.join(self.application.applicationDirectory, name)
        if os.path.exists(os.path.join(path, name + ".pyw")):
            filename =  os.path.join(path, name + ".pyw")
        else:
            filename = os.path.join(path, name + ".py")
        args = self.getCommandLineArgs()
        # KEA 2002-04-28
        # os.spawnv probably works on all platforms
        # and regardless of the quoting needs for paths with
        # and without spaces, but each platform is separate
        # below until that is confirmed
        if ' ' in filename:
            filename = '"' + filename + '"'
        python = sys.executable
        if ' ' in python:
            pythonQuoted = '"' + python + '"'
        else:
            pythonQuoted = python
        os.spawnv(os.P_NOWAIT, python, [pythonQuoted, filename] + args)

    def showDescription(self):
        path = self.components.listSamples.stringSelection
        if path == "samples":
            path = ""
        name = 'readme.txt'
        try:
            path = os.path.join(path, name)
            desc = open(path).read()
            self.components.fldDescription.text = desc
            self.components.stcDescription.text = 'Description: ' + path
        except:
            pass

        if self.components.fldSource.visible:
            self.components.fldSource.visible = 0
            self.sizer1.Remove(self.components.fldSource)
            self.sizer1.Add(self.components.fldDescription, 1, wx.EXPAND)
            self.components.fldDescription.visible = 1
            self.sizer1.Layout()

    def on_showDescription_command(self, event):
        self.showDescription()

    def showSource(self, source):
        name = self.components.listSamples.stringSelection
        if name == "samples":
            path = ""
        else:
            path = name
        try:
            if source == 'source':
                p = os.path.join(path, name + '.py')
                if os.path.exists(p):
                    path = p
                else:
                    path = os.path.join(path, name + '.pyw')
                self.components.stcDescription.text = 'Source code: ' + path
            else:
                path = os.path.join(path, name + '.rsrc.py')
                self.components.stcDescription.text = 'Resource: ' + path
            src = open(path).read()
            # KEA 2002-06-21
            # you can't change the text of a CodeEditor
            # component if it isn't editable
            # should we change that?
            self.components.fldSource.editable = 1
            self.components.fldSource.text = src            
            self.components.fldSource.editable = 0
        except:
            pass

        if self.components.fldDescription.visible:
            self.components.fldDescription.visible = 0
            self.sizer1.Remove(self.components.fldDescription)
            self.sizer1.Add(self.components.fldSource, 1, wx.EXPAND)
            self.components.fldSource.visible = 1
            self.sizer1.Layout()

    def on_showSource_command(self, event):
        self.showSource('source')

    def on_showResource_command(self, event):
        self.showSource('resource')

    def on_listSamples_select(self, event):
        if self.components.stcDescription.text.startswith('Description'):
            self.showDescription()
        elif self.components.stcDescription.text.startswith('Source code'):
            self.showSource('source')
        else:
            self.showSource('resource')

    def on_listSamples_mouseDoubleClick(self, event):
        self.on_launch_command(None)

    def on_menuHelpPythonCardHomePage_select(self, event):
        webbrowser.open('http://pythoncard.sourceforge.net/', 1, 1) 

    def on_menuHelpOnlineDocumentation_select(self, event):
        webbrowser.open('http://pythoncard.sourceforge.net/documentation.html', 1, 1) 

    def on_menuHelpAbout_select(self, event):
        dialog.scrolledMessageDialog(self, self.readme, 'About samples...')

    def on_doHelpAboutPythonCard_command(self, event):
        about.aboutPythonCardDialog(self)

if __name__ == '__main__':
    app = model.Application(Launcher)
    app.MainLoop()
