#!/usr/bin/python

"""
__version__ = "$Revision: 1.26 $"
__date__ = "$Date: 2005/03/28 05:47:00 $"

I'll add support for editing the .txt file scripts once we have a multi-window
framework in place and a decent way of doing at least rudimentary editing,
syntax highlighting, syntax checking, etc. In other words, not until scintilla
is running inside the PythonCard framework to give us styled text fields and
more.
"""

import wx
from PythonCard import configuration, dialog, model, turtle
import os
import time

class TurtleBg(model.Background):
    def on_initialize(self, event):
        self.fNameTurtleScript = os.path.join('scripts', 'threeTurtles.py')

        self.singleItemExpandingSizerLayout()

        self.components.bufOff.backgroundColor = 'white'

        if wx.Platform == '__WXMAC__':
            # KEA 2005-03-26
            # if CallAfter isn't used, the Mac doesn't update the menu correctly
            # this might be a bug
            wx.CallAfter(self.menuBar.setChecked, 'menuCommandsAutoRefresh', False)
            self.components.bufOff.autoRefresh = False

    def doDraw(self):
        starttime = time.time()

        cwd = os.getcwd()
        path, filename = os.path.split(self.fNameTurtleScript)
        os.chdir(path)
        module = __import__(os.path.splitext(filename)[0], globals(), globals())
        # make sure that if this module was previously imported
        # that we get the new version
        reload(module)
        module.draw(self.components.bufOff)
        os.chdir(cwd)
        if not self.components.bufOff.autoRefresh:
            self.components.bufOff.refresh()
        # in case a script doesn't cleanup after itself, get the buffer
        # back in sync with the menu
        self.components.bufOff.autoRefresh = self.menuBar.getChecked('menuCommandsAutoRefresh')

        stoptime = time.time()
        elapsed = stoptime - starttime
        self.statusBar.text = "Draw time: %f seconds" % (elapsed)

    def on_menuFileOpen_select(self, event):
        currentDir = os.getcwd()
        wildcard = "Turtle files (*.py)|*.py"
        path = 'scripts'
        filename = ''
        result = dialog.openFileDialog(self, 'Open', path, filename, wildcard)
        if result.accepted:
            self.fNameTurtleScript = result.paths[0]
            os.chdir(currentDir)
            self.doDraw()

    def on_menuFileDrawTurtle_select(self, event):
        self.doDraw()

    def on_menuCommandsClear_select(self, event):
        # this is unclean and will need to be changed
        # I'll change it after I think more about what sorts
        # of commands I want to support in the menu and whether
        # they should be global or specific to individual turtles
        self.components.bufOff.clear()
        if not self.components.bufOff.autoRefresh:
            self.components.bufOff.refresh()

    def on_menuCommandsAutoRefresh_select(self, event):
        self.components.bufOff.autoRefresh = self.menuBar.getChecked('menuCommandsAutoRefresh')

if __name__ == '__main__':
    # now force the shell to be enabled
    configuration.setOption('showShell', True)

    app = model.Application(TurtleBg)
    app.MainLoop()
