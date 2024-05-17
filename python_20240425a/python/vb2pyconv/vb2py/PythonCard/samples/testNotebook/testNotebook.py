#!/usr/bin/python

"""
__version__ = "$Revision: 1.6 $"
__date__ = "$Date: 2004/09/16 16:11:34 $"
"""

import os, sys
import wx
from PythonCard import model
import minimal
import widgets
import doodle


class TestNotebook(model.Background):
    def on_initialize(self, event):
        # KEA 2004-09-16
        # if we don't set a min size then the window is
        # very small. this may not be the correct way to
        # solve the problem...
        self.components.notebook.SetMinSize(self.components.notebook.size)
        self.singleItemExpandingSizerLayout()

        panel = wx.Panel(self.components.notebook, -1)
        panel.text1 = wx.TextCtrl(panel, -1, 'Hello Notebook', (5, 5))
        self.components.notebook.AddPage(panel, 'wx panel', True)

        # you can't add a wx.Frame to a notebook
##        frame = wx.Frame(self.components.notebook, -1)
##        frame.text1 = wx.TextCtrl(frame, -1, 'Notebook 2', (5, 5))
##        self.components.notebook.AddPage(frame, 'frame', True)

        # let's pretend we were just given a string with the class to
        # load to see how this would be handled in the Notebook component
        # automatically
        #win = model.childWindow(self.components.notebook, minimal.Minimal)
        pageName = 'minimal'
        classString = 'minimal.Minimal'
        # assume for now that there will be one and only one
        # dot rather than something like modules.minimal.Minimal or just Minimal
        # indicating that the class is actually in the main source file
        # which would cause all sorts of problems with finding the resource file
        print "adding minimal page..."
        import imp
        moduleName, className = classString.split('.')
        fp, pathname, description = imp.find_module(moduleName)
        try:
            m = imp.load_module(moduleName, fp, pathname, description)
            win = model.childWindow(self.components.notebook, getattr(m, className))
            self.components.notebook.AddPage(win, pageName, True)
            # now test setting the attribute for reference below
            setattr(self.components.notebook, pageName, win)
            #print self.components.notebook.GetPage(1).components.field1.text
            page = self.components.notebook.minimal
            print page.components.field1.text
            print "menuFileExit enabled:", page.menuBar.getEnabled('menuFileExit')
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()

        win2 = model.childWindow(self.components.notebook, widgets.WidgetsTest)
        self.components.notebook.AddPage(win2, 'widgets', True)

        win3 = model.childWindow(self.components.notebook, doodle.Doodle)
        self.components.notebook.AddPage(win3, 'doodle', True)
        page = self.components.notebook.getPage(3)
        # it appears that since on_initialize hasn't run yet
        # after adding the page, the sizer code in doodle
        # in on_initialize hasn't been run so the page size
        # below is what we want but after the sizer code runs it
        # will be (300, 260)
        # if the user resizes the window, the sizer works as expected
        # but if the window hasn't been resized, then when you click
        # on the doodle tab the page doesn't fill the whole window
        # I don't know what the correct solution is yet, but this seems
        # to work. i have to use a method with CallAfter
        # so that's why we aren't just using the attribute
        size = page.size
        wx.CallAfter(page.SetSize, size)

        print "number of pages:", self.components.notebook.getPageCount()
        print "last page text: %s\n" % \
            self.components.notebook.getPageText(self.components.notebook.getPageCount() - 1)
        
        print "stringSelection:", self.components.notebook.stringSelection
        self.components.notebook.stringSelection = 'minimal'

    def on_notebook_pageChanging(self, event):
        print "pageChanging - oldSelection: %d, selection: %d" % (event.oldSelection, event.selection)
        event.skip()

    def on_notebook_pageChanged(self, event):
        print "pageChanged  - oldSelection: %d, selection: %d" % (event.oldSelection, event.selection)
        event.skip()


if __name__ == '__main__':
    app = model.Application(TestNotebook)
    app.MainLoop()
