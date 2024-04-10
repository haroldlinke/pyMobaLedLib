#!/usr/bin/python

"""
_A fairly simple implementation of Conway's Game of Life.
"""
_version__ = "$Revision: 1.18 $"
__date__ = "$Date: 2005/12/13 11:13:23 $"

from PythonCard import model

import wx

import os
import glob

from util import readLifeFile

class Patterns(model.Background):

    def on_initialize(self, event):
        #self.initSizers()
        self.components.fldDescription.lineNumbersVisible = 0
        self.components.fldDescription.setEditorStyle('text')
        self.patternsPath = self.getParent().patternsPath
        self.populatePatternsList()

    def initSizers(self):
        self.html = self.components.html
        self.html.SetRelatedFrame(self, "HTML Preview: %s")
        self.html.SetRelatedStatusBar(0)

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.html, 1, wx.EXPAND)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def populatePatternsList(self):
        files = glob.glob(os.path.join(self.patternsPath, '*.[Ll][Ii][Ff]'))
        items = []
        self.files = {}
        for file in files:
            filename = os.path.basename(file)
            base, ext = os.path.splitext(filename.lower())
            #items.append(base)
            self.files[base] = file
        items = self.files.keys()
        items.sort()
        self.components.lstPatterns.items = items
        self.components.lstPatterns.selection = 0
        # now simulate the user doing a selection
        self.on_lstPatterns_select(None)

    def loadPattern(self, name):
        path = self.files[name]
        #print num, path
        description, patterns, topLeft, size = readLifeFile(path)
        #print "topLeft:", topLeft, "size", size
        self.GetParent().initAndPlacePatterns(patterns, topLeft, size)

    def on_lstPatterns_select(self, event):
        path = self.files[self.components.lstPatterns.stringSelection]
        description, patterns, topLeft, size = readLifeFile(path)
        self.description = description
        self.patterns = patterns
        self.patternSize = size
        self.components.fldDescription.text = description
        self.components.stcSize.text = "Size: (%d, %d)" % size

    def on_btnLoad_mouseClick(self, event):
        self.loadPattern(self.components.lstPatterns.stringSelection)

    def on_lstPatterns_mouseDoubleClick(self, event):
        self.loadPattern(self.components.lstPatterns.stringSelection)

    def on_close(self, event):
        self.visible = False
