#!/usr/bin/python

"""
__version__ = "$Revision: 1.16 $"
__date__ = "$Date: 2004/08/08 18:31:53 $"
"""

import wx
from PythonCard import model

import os, sys
import re
import webbrowser

class ReDemo(model.Background):
    
    def on_initialize(self, event):
        self.compiled = None
        self.previousSource = self.components.fldSource.text
        
    def recompile(self):
        pattern = self.components.fldPattern.text
        text = self.components.fldSource.text
        flags = self.getflags()
        try:
            self.compiled = re.compile(pattern, flags)
            self.components.stcStatusMessage.text = ''
        except re.error, msg:
            self.compiled = None
            self.components.stcStatusMessage.text = "re.error: %s" % str(msg)
            self.components.stcStatusMessage.backgroundColor = 'red'
        except TypeError, msg:
            self.components.stcStatusMessage.text = "TypeError: %s" % str(msg)
            self.components.stcStatusMessage.backgroundColor = 'red'
        self.reevaluate()

    # the logic of the tkinter version
    # eludes me
    def getflags(self):
        flags = 0
        comp = self.components
        if comp.chkIGNORECASE.checked:
            flags += re.IGNORECASE
        if comp.chkLOCALE.checked:
            flags += re.LOCALE
        if comp.chkMULTILINE.checked:
            flags += re.MULTILINE
        if comp.chkDOTALL.checked:
            flags += re.DOTALL
        if comp.chkVERBOSE.checked:
            flags += re.VERBOSE
        return flags

    def reevaluate(self):
        text = self.components.fldSource.text
        # effectively clear any existing matches
        self.components.fldSource.SetStyle(0, len(text), wx.TextAttr("black", "white"))

        if not self.compiled:
            return

        # first item in the radio is the display once button
        # this will check it regardless of any future language
        # changes made to the resource
        displayJustOne = self.components.radSearchString.stringSelection == \
            self.components.radSearchString.items[0]

        last = 0
        nmatches = 0
        listGroups = self.components.listGroups
        listGroups.items = []
        while last <= len(text):
            m = self.compiled.search(text, last)
            if m is None:
                break
            first, last = m.span()
            if last == first:
                last = first+1
            self.components.fldSource.SetStyle(first, last, wx.TextAttr("black", "yellow"))
            if nmatches == 0:
                groups = list(m.groups())
                groups.insert(0, m.group())
                for i in range(len(groups)):
                    g = "%2d: %s" % (i, `groups[i]`)
                    listGroups.append(g)
            nmatches = nmatches + 1
            if displayJustOne:
                break

            
        if nmatches == 0:
            self.components.stcStatusMessage.text = '(no match)'
            self.components.stcStatusMessage.backgroundColor = 'yellow'
        #print "nmatches", nmatches, "\n"


    def on_fldPattern_textUpdate(self, event):
        self.recompile()

    # textUpdate events occur on SetStyle
    # so a variable is needed to know that we are in 
    # the midst of an update
    def on_fldSource_textUpdate(self, event):
        if self.previousSource != self.components.fldSource.text:
            self.previousSource = self.components.fldSource.text
            self.recompile()

    # checkboxes
    def on_mouseClick(self, event):
        self.recompile()

    # radiobutton
    def on_radSearchString_select(self, event):
        self.reevaluate()

    def on_menuHelpReModule_select(self, event):
        module_url = "http://docs.python.org/lib/module-re.html"
        if sys.platform.startswith('win'):
            fn = os.path.dirname(os.__file__)
            fn = os.path.join(fn, os.pardir, "Doc", "lib", "module-re.html")
            fn = os.path.normpath(fn)
            if os.path.isfile(fn):
                module_url = fn
            del fn
        webbrowser.open(module_url)

    def on_menuHelpReHowTo_select(self, event):
        webbrowser.open('http://py-howto.sourceforge.net/regex/regex.html')
        


if __name__ == '__main__':
    app = model.Application(ReDemo)
    app.MainLoop()
