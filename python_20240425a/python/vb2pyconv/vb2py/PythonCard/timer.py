"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/04/14 01:35:26 $"
"""

import wx

class Timer(wx.Timer):
    """
    Simple wrapper of wxTimer so that all apps using timers
    can use mixedCase style methods and avoid importing wx.
    """

    getInterval = wx.Timer.GetInterval
    isOneShot = wx.Timer.IsOneShot
    isRunning = wx.Timer.IsRunning
    start = wx.Timer.Start
    stop = wx.Timer.Stop
