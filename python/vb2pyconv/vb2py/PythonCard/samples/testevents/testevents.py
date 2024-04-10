#!/usr/bin/python

"""
__version__ = "$Revision: 1.22 $"
__date__ = "$Date: 2005/12/25 17:11:55 $"
"""

import wx
print "wxPython", wx.__version__

from PythonCard import model, timer

class MinimalChild(model.Background):
    # creates a child window - using same resource file
    #  same appearance - but buttons and fields are not activated
    def on_initialize(self, event):
        print "initialize child window"
        self.title = "Child Window"
        
    def callableFunction(self, stringParameter):
        print "in child function", stringParameter
    
class Minimal(model.Background):

    # background events
    
    def on_initialize(self, event):
        print "initialize", event.target.name
        self.num_idles = 0
        self.fldTimer = timer.Timer(self.components.fld)
        self.fldTimer.start(10 * 1000) # 10 seconds
        self.btnTimer = timer.Timer(self.components.btn)
        self.btnTimer.start(3 * 1000) # 3 seconds
        self.components.btn.setFocus()
        # on the Mac, findFocus() is returning None
        # when the sample is started with a runtime tool
        focus = self.findFocus()
        if focus:
            print "  has focus:", focus.name

    def on_activate(self, event):
        print "activate", event.target.name
        event.skip()

    def on_deactivate(self, event):
        print "deactivate", event.target.name
        event.skip()

    def on_close(self, event):
        print "close", event.target.name
        self.fldTimer.stop()
        self.btnTimer.stop()
        event.skip()

    def on_idle(self, event):
        # prevent idle message flood
        self.num_idles += 1
        if self.num_idles < 5:
            print "idle", event.target.name
        event.skip()

    def on_timer(self, event):
        print "timer", event.target.name, \
            " interval: %.2f seconds" % (event.interval / 1000.0)

    def on_maximize(self, event):
        print "maximize", event.target.name
        event.skip()

    def on_minimize(self, event):
        print "minimize", event.target.name
        event.skip()

    def on_restore(self, event):
        print "restore", event.target.name
        event.skip()

    def on_move(self, event):
        print "move", event.target.name, event.position
        event.skip()

    def on_size(self, event):
        print "size", event.target.name, event.size
        event.skip()

    # component events
    def on_gainFocus(self, event):
        print "gainFocus", event.target.name
        event.skip()

    def on_loseFocus(self, event):
        print "loseFocus", event.target.name
        event.skip()

    def on_closeField(self, event):
        print "closeField", event.target.name
        event.skip()
        
    def on_mouseMove(self, event):
        print "mouseMove", event.target.name, event.position
        event.skip()

    def on_mouseDrag(self, event):
        print "mouseDrag", event.target.name, event.position
        event.skip()

    def on_mouseEnter(self, event):
        print "mouseEnter", event.target.name, event.position
        event.skip()

    def on_mouseLeave(self, event):
        print "mouseLeave", event.target.name, event.position
        event.skip()

    def on_keyDown(self, event):
        print "keyDown", event.target.name, event.keyCode, \
            event.altDown, event.controlDown, event.shiftDown
        event.skip()

    def on_keyUp(self, event):
        print "keyUp", event.target.name, event.keyCode, \
            event.altDown, event.controlDown, event.shiftDown
        event.skip()

    def on_keyPress(self, event):
        print "keyPress", event.target.name, event.keyCode, \
            event.altDown, event.controlDown, event.shiftDown
        event.skip()

    def on_textUpdate(self, event):
        print "textUpdate", event.target.name
        event.skip()

    def on_mouseDown(self, event):
        print "mouseDown", event.target.name
        event.skip()

    def on_mouseUp(self, event):
        print "mouseUp", event.target.name
        event.skip()

    def on_mouseClick(self, event):
        print "mouseClick", event.target.name
        event.skip()

    def on_btn_mouseClick(self, event):
        print "btn mouseClick", event.target.name
        event.skip()

    def on_setText_command(self, event):
        print "setText command", event.target.name
        self.components.fld.text = "After setText"
        event.skip()

    def on_openChildWindow_command(self, event):
        # delayed events - check the order these 'print's appear
        # should be 
        #   openChildWindow command
        #   leaving openCHildWindow
        #   initializing child window
        #   in child function via CallAfter
        #   in child function 10 ms in future
        print "openChildWindow command", event.target.name
        # KEA 2005-12-25
        # the path for sys.modules[MinimalChild.__module__].__file__
        # will be relative to the starting directory
        # so childWindow will fail if a resource file isn't provided
        # I'm not sure if this is a bug due to PythonCard changing the
        # directory to the application directory on startup or
        # the __file__ attribute already being set prior to our sys.path[0]
        # fix in model.py a combination of the two or something else.
        # However, always providing a resource path seems to work for
        # childWindow.
        win = model.childWindow(self, MinimalChild, 'testevents.rsrc.py')
        wx.FutureCall(10, win.callableFunction, "10 ms in the Future")
        wx.CallAfter(win.callableFunction, "via CallAfter")
        print "leaving openChildWindow"

if __name__ == '__main__':
    app = model.Application(Minimal)
    app.MainLoop()
