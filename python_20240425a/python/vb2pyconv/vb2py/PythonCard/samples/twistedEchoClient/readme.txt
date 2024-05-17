Twisted Echo client which uses the TwistedApplication class.

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


You need to start pbecho.py first so you have a server to connect to. pbecho.py is included in the Twisted distribution within your Python site-packages directory:

    site-packages/TwistedDocs/examples/pbecho.py

Contributed by Stephen Waterbury. Additional code by Kevin Altis

Adapted from Uwe C. Schroeder's cookbook entry "Using wxPython with Twisted Python"

    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/181780
