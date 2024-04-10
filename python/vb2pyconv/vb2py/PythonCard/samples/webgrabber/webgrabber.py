#!/usr/bin/python

"""
__version__ = "$Revision: 1.13 $"
__date__ = "$Date: 2004/08/30 14:49:51 $"
"""

import wx
from PythonCard import dialog, model, timer
import websucker
import sys
import os
import threading
import Queue
import time

VERBOSE = 2

try:
    class Canceled(Exception):
        "Exception used to cancel run()."
except (NameError, TypeError):
    Canceled = __name__ + ".Canceled"


class SuckerThread(websucker.Sucker):

    stopit = 0
    savedir = None
    rootdir = None

    def __init__(self, msgq):
        self.msgq = msgq
        websucker.Sucker.__init__(self)
        self.setflags(verbose=VERBOSE)
        self.urlopener.addheaders = [
            ('User-agent', 'websucker/%s' % websucker.__version__),
        ]

    def message(self, format, *args):
        if args:
            format = format%args
        ##print format
        self.msgq.put(format)

    def run1(self, url):
        try:
            try:
                self.reset()
                self.addroot(url)
                self.run()
            except Canceled:
                self.message("[canceled]")
            else:
                self.message("[done]")
        finally:
            self.msgq.put(None)

    def savefile(self, text, path):
        if self.stopit:
            raise Canceled
        websucker.Sucker.savefile(self, text, path)

    def getpage(self, url):
        if self.stopit:
            raise Canceled
        return websucker.Sucker.getpage(self, url)

    def savefilename(self, url):
        path = websucker.Sucker.savefilename(self, url)
        print "path", path
        print "self.rootdir", self.rootdir
        if self.savedir:
            n = len(self.rootdir)
            if path[:n] == self.rootdir:
                path = path[n:]
                while path[:1] == os.sep:
                    path = path[1:]
                print "self.savedir", self.savedir
                print "path", path
                path = os.path.join(self.savedir, path)
        return path

    def XXXaddrobot(self, *args):
        pass

    def XXXisallowed(self, *args):
        return 1

class WebSuckerView(model.Background):

    #sucker = None
    #msgq = None

    def on_initialize(self, event):
        self.sucker = None
        self.msgq = None
        self.clockTimer = timer.Timer(self.components.fldURL, -1)
        #self.clockTimer.start(100)  # 100 milliseconds

    def on_close(self, event):
        self.cancel()
        self.clockTimer.stop()
        event.skip()

    def on_timer(self, event):
        if self.msgq is not None:
            self.check_msgq()

    def on_btnDirectory_mouseClick(self, event):
        dir = self.components.fldDirectory.text
        if dir == '':
            dir = self.application.applicationDirectory
        result = dialog.directoryDialog(self, '', dir)
        if result.accepted:
            self.components.fldDirectory.text = result.path

    def on_btnGo_mouseClick(self, event):
        self.go()

    def on_btnCancel_mouseClick(self, event):
        self.cancel()


    # the remaining code is a modification of the App class code
    # in wsgui.py
    
    def message(self, text, *args):
        if args:
            text = text % args
        #self.status_label.config(text=text)
        self.statusBar.text = text

    def check_msgq(self):
        while not self.msgq.empty():
            msg = self.msgq.get()
            if msg is None:
                #self.go_button.configure(state=NORMAL)
                self.components.btnGo.enabled = 1
                #self.auto_button.configure(state=NORMAL)
                #self.cancel_button.configure(state=DISABLED)
                self.components.btnCancel.enabled = 0
                if self.sucker:
                    self.sucker.stopit = 0
                #self.top.bell()
            else:
                self.message(msg)
        #self.top.after(100, self.check_msgq)
        self.clockTimer.start(100, 1)  # 100 milliseconds, one shot

    def go(self, event=None):
        if not self.msgq:
            self.msgq = Queue.Queue(0)
            self.check_msgq()
        if not self.sucker:
            self.sucker = SuckerThread(self.msgq)
        if self.sucker.stopit:
            return
        #self.url_entry.selection_range(0, END)
        #url = self.url_entry.get()
        url = self.components.fldURL.text
        url = url.strip()
        if not url:
            #self.top.bell()
            self.message("[Error: No URL entered]")
            return
        self.rooturl = url
        dir = self.components.fldDirectory.text
        if not dir:
            self.sucker.savedir = None
        else:
            self.sucker.savedir = dir
            self.sucker.rootdir = os.path.dirname(websucker.Sucker.savefilename(self.sucker, url))
        #self.go_button.configure(state=DISABLED)
        self.components.btnGo.enabled = 0
        #self.auto_button.configure(state=DISABLED)
        #self.cancel_button.configure(state=NORMAL)
        self.components.btnCancel.enabled = 1
        self.message( '[running...]')
        self.sucker.stopit = 0
        t = threading.Thread(target=self.sucker.run1, args=(url,))
        t.start()

    def cancel(self):
        if self.sucker:
            self.sucker.stopit = 1
        self.message("[canceling...]")


if __name__ == '__main__':
    app = model.Application(WebSuckerView)
    app.MainLoop()
