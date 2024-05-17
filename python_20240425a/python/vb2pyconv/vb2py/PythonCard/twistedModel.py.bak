
"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2004/04/28 19:09:34 $"
"""

"""
Adapted from Uwe C. Schroeder's cookbook entry "Using wxPython with Twisted Python"

    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/181780
"""

import wx
import model
from twisted.internet import reactor

class TwistedApplication(model.Application):
    def OnInit(self):
        model.Application.OnInit(self)
        reactor.startRunning()
        wx.EVT_TIMER(self, 999999, self.OnTimer)
        self.twistedTimer = wx.Timer(self, 999999)
        self.twistedTimer.Start(250, False)
        return True

    def OnTimer(self, event):
        reactor.iterate()

    def OnExit(self):
        # need to stop the timer for cleanup purposes
        self.twistedTimer.Stop()
        self.twistedTimer = None
        reactor.stop()
