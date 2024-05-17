#!/usr/bin/env python
"""
__version__ = "$Revision: 1.14 $"
__date__ = "$Date: 2004/09/16 21:11:33 $"

experimental version with Resource File support

PythonCard Editor (codeEditor) wiki page
http://wiki.wxpython.org/index.cgi/PythonCardEditor

wxStyledTextCtrl documentation
http://wiki.wxpython.org/index.cgi/wxStyledTextCtrl
"""

import os
import wx
from PythonCard import model, registry, resource
import codeEditor


def getResourceFilename(path):
    path, filename = os.path.split(path)
    base = os.path.splitext(filename)[0]
    resourceFilename = os.path.join(path, base + '.rsrc.py')
    return resourceFilename

# this really needs to know about the structure
# of the file by parsing the classes and methods
# it won't deal with duplicate handler names...
# with just simple matching
def handlerExists(text, componentName, eventName):
    eventText = 'def on_' + componentName + '_' + eventName + '('
    # commands are a special case since the command name
    # does not have to be tied to the component name
    # so that will require special handling by looking
    # at the command attribute of the component
    return text.find(eventText)


class CodeEditorR(codeEditor.CodeEditor):
    
    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        sizer2.Add(self.components.popComponentNames)
        sizer2.Add(self.components.popComponentEvents)

        sizer1.Add(sizer2, 0)
        sizer1.Add(self.components.document, 1, wx.EXPAND)

        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def on_idle(self, event):
        self.updateTitleBar()
        self.updateStatusBar()
        # KEA 2003-01-06
        # resource file support
        # if there is an associated resource file then
        # it should be checked periodically to see if it has
        # changed and if so, update our internal resource
        # as well as the component names and events menus
        # the events menu should also be updated as the user
        # edits the text to keep the defined events marked
        # with a +
        # the code below is too CPU intensive to run
        # all the time, so I've commented it out until
        # a better way of updating the event list is found
        ##sel = self.components.popComponentNames.stringSelection
        ##if sel != '':
        ##    self.fillEventNames(sel)

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
            # KEA 2003-01-06
            # resource file support
            self.setResourceFile()
        except:
            pass


    # KEA 2003-01-06
    # resource file support
    def setResourceFile(self):
        self.components.popComponentNames.items = []
        self.components.popComponentEvents.items = []
        try:
            self.resourceFilename = getResourceFilename(self.documentPath)
            self.rsrc = resource.ResourceFile(self.resourceFilename).getResource()
            self.rsrcComponents = {}
            if hasattr(self.rsrc, 'application'):
                components = self.rsrc.application.backgrounds[0].components
            else:
                # CustomDialog
                components = self.rsrc.components
            for c in components:
                self.rsrcComponents[c.name] = c.type
            items = self.rsrcComponents.keys()
            items.sort()
            self.components.popComponentNames.items = items
        except:
            pass

    def fillEventNames(self, componentName):
        r = registry.Registry.getInstance()
        componentType = self.rsrcComponents[componentName]
        spec = r.components[componentType]._spec
        tmp = spec.getEventNames() + ['command']
        tmp.sort()

        text = self.components.document.text
        eventNames = []
        for e in tmp:
            if handlerExists(text, componentName, e) != -1:
                eventNames.append('+ ' + e)
            else:
                eventNames.append('   ' + e)
        # should we try and save and restore the current selection?
        if self.components.popComponentEvents.items != eventNames:
            self.components.popComponentEvents.items = eventNames

    def on_popComponentNames_select(self, event):
        self.fillEventNames(event.target.stringSelection)

    def on_popComponentEvents_select(self, event):
        document = self.components.document
        componentName = self.components.popComponentNames.stringSelection
        # this is tied to the '   ' and '+ ' used in fillEventNames
        # we just want the event name
        eventName = event.target.stringSelection.split(' ')[-1]
        eventText = 'def on_' + componentName + '_' + eventName + '('
        offset = handlerExists(document.text, componentName, eventName)
        #print eventText, offset
        if offset != -1:
            document.SetSelection(offset, offset)
        else:
            # event handler doesn't exist?
            # so create one at the current selection?
            sel = document.GetSelection()
            start = document.LineFromPosition(sel[0])
            # this could take into account the current indent
            eventText = eventText + 'self, event):\n    pass\n'
            firstChar = document.PositionFromLine(start)
            
            document.BeginUndoAction()
            document.InsertText(firstChar, eventText)
            document.SetCurrentPos(document.PositionFromLine(start))
            document.EndUndoAction()
            
        document.setFocus()


if __name__ == '__main__':
    app = model.Application(CodeEditorR)
    app.MainLoop()
