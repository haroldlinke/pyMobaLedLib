#!/usr/bin/python

"""
KEA notes to myself

Created: 2001-07-22
__version__ = "$Revision: 1.28 $"
__date__ = "$Date: 2005/09/18 03:59:22 $"
__author__ = "Kevin Altis <altis@semi-retired.com>"

I'm using an ImageButton rather than an image because I want to catch
mouseMove (hmm, should that be mouseOver ?) events and pop up a relative
time for east coast, midwest, london, sydney, etc.

However, we need the option to set style=0 rather than the default
wxBU_AUTODRAW.

http://www.time.gov/images/xearths/night.jpg
"""

import urllib
import os
import time
import wx
from cStringIO import StringIO

from PythonCard import graphic, log, model, timer

import xearth

class WorldClock(model.Background):

    def on_initialize(self, event):
        self.url = ''
        # KEA 2002-05-27
        # switched to timer events
        self.clockTimer = timer.Timer(self.components.staticTextClock, -1)
        self.clockTimer.start(1000)  # 1 second
        self.imageTimer = timer.Timer(self.components.imageButtonWorld, -1)
        self.imageTimer.start(5 * 60 * 1000)  # 5 minutes
        # force the first update
        self.updateDateAndTime()
        self.updateImage()

    def on_staticTextClock_timer(self, event):
        self.updateDateAndTime()

    def updateDateAndTime(self):        
        t = time.strftime("%I:%M %p")
        if t[0] == "0":
            t = t[1:]
        if self.components.staticTextClock.text != t:
            self.components.staticTextClock.text = t
            d = time.strftime("%A, %B %d, %Y")
            if self.components.staticTextDate.text != d:
                self.components.staticTextDate.text = d

    def on_imageButtonWorld_timer(self, event):
        self.updateImage()

    def updateImage(self):        
        log.info("interval is up...")
        url = "http://www.time.gov/" + xearth.getLatLong()
        if url == self.url:
            return
        self.url = url
        log.info("updating image ", url)

        # download image from www.time.gov
        try:
            fp = urllib.urlopen(url)
            jpg = fp.read()
            fp.close()
        except Exception, msg:
            return

        wImageButtonWorld = self.components.imageButtonWorld

        # with wxPython 2.3.3.1 and above it is no longer
        # necessary to write the file to disk before displaying it
        newBitmap = graphic.Bitmap()
        # I could probably use the fp file object, but using the 
        # jpg variable seems cleaner
        newBitmap.setImageBits(wx.ImageFromStream(StringIO(jpg)))

        wImageButtonWorld.bitmap = newBitmap

    def on_close(self, event):
        self.clockTimer.stop()
        self.imageTimer.stop()
        event.skip()

if __name__ == '__main__':
    app = model.Application(WorldClock)
    app.MainLoop()
