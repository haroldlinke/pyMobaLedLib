#!/usr/bin/python

"""
__version__ = "$Revision: 1.27 $"
__date__ = "$Date: 2005/09/18 03:59:22 $"
"""

import wx
from PythonCard import configuration, model
import os, sys
import shutil
from BaseHTTPServer import HTTPServer
import CGIHTTPServer
from CGIHTTPServer  import CGIHTTPRequestHandler
import threading 
import Queue
import ConfigParser
import socket

# imports needed code is moved back into standard libs
import urllib
import select

CONFIG_FILE = 'webserver.ini'

# a backwards compatible date_time_string function
# with the one in BaseHTTPRequestHandler
# it seems like this should be moved and made a function
# as I've done below

import time
import rfc822

weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

monthname = [None,
             'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def date_time_string(t=None):
    global weekdayname, monthname
    """Return the current date and time formatted for a message header."""
    if not t:
        t = time.time()
    # assume user supplied time value will be local, not gmt!
    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(t)
    s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
            weekdayname[wd],
            day, monthname[month], year,
            hh, mm, ss)
    return s


class MyRequestHandler(CGIHTTPRequestHandler):
    # the server variable contains the reference back to the view
    def log_message(self, format, *args):
        msg = "%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args)
        if format.startswith('"%s"'):
            self.server._notify_window.msgQueue.put(msg)
            wx.WakeUpIdle()
            # just log to the GUI now, this could go to a file as well
        else:
            # don't put CGI error and exit status messages in the main log
            print msg

    cgi_extensions = [".py", ".pyw", ".cgi"]

    def is_python(self, path):
        """Test whether argument path is a Python script."""
        head, tail = os.path.splitext(path)
        return tail.lower() in self.cgi_extensions


class WebServer(HTTPServer):
    def __init__(self, notify_window, server_address, RequestHandlerClass, validIPList=None):
        self._notify_window = notify_window 
        # this list will come from a config file
        # and there will be a dialog to edit the valid IP addresses
        if validIPList:
            self.validIPList = validIPList
        else:
            self.validIPList = ['127.0.0.1']
        # add host IP address that this server is running on
        # this will fail for address spaces like 10.0.0.x, 192.168.0.x
        # etc., so what is the appropriate way to add those?
        # I get errors like
        # socket.gaierror: (7, 'No address associated with nodename')
        try:
            self.validIPList.append(socket.gethostbyname(socket.gethostname()))
        except Exception, msg:
            pass
        self.allowAny = 0
        HTTPServer.__init__(self, server_address, RequestHandlerClass)

    def verify_request(self, request, client_address):
        if self.allowAny or client_address[0] in self.validIPList:
            return 1
        else:
            return 0

    # just a guess that this is how we should use threads
    def server(self):
        self.serve_forever()


class WebServerView(model.Background):

    def on_initialize(self, event):
        self.initSizers()

        self.loadConfig()
        
        # if you wanted to limit the on screen log size, then set
        # this to something other than 0
        self.maxSizeLog = 0
        
        # Set up event handler for any worker thread results 
        """
        Robin said:
        The Queue class is thread-safe, using a mutex and semaphore to protect
        access to its contents, so is ideally suited for something like this.
        """
        self.msgQueue = Queue.Queue()
            
        os.chdir(self.htdocs)
        self.srvraddr = ('', self.port)
        # give the server and request handlers 
        # a reference back to the view for logging
        self.webServer = WebServer(self, self.srvraddr, MyRequestHandler, self.validIPList)
        self.thread = threading.Thread(target = self.webServer.server)
        # I think this allows Python to kill the thread when we quit wxPython
        # setDaemon must be called before start
        self.thread.setDaemon(1)
        self.thread.start()

    def loadConfig(self):
        self.configPath = os.path.join(configuration.homedir, 'webserver')
        if not os.path.exists(self.configPath):
            os.mkdir(self.configPath)
        configPath = os.path.join(self.configPath, CONFIG_FILE)
        defaultPath = os.path.join(self.application.applicationDirectory, CONFIG_FILE)
        if not os.path.exists(configPath):
            shutil.copy2(defaultPath, configPath)
        parser = ConfigParser.ConfigParser()
        parser.read(configPath)
        self.htdocs = parser.get('ConfigData', 'htdocs')
        self.port = int(parser.get('ConfigData', 'port'))
        ips = parser.get('ConfigData', 'iplist')
        self.validIPList = ips.split(',')

    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.components.fldLog, 1, wx.EXPAND)

        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def on_idle(self, event):
        if not self.msgQueue.empty():
            msg = self.msgQueue.get()
            self.doLogResult(msg)
            event.RequestMore()

    def doLogResult(self, data):
        if data is not None:
            # code borrowed from the Message Watcher event history display
            log = self.components.fldLog
            log.SetReadOnly(0)
            if self.maxSizeLog and log.GetLength() > self.maxSizeLog:
                # delete many lines at once to reduce overhead
                text = log.GetText()
                endDel = text.index('\n', self.maxSizeLog / 10) + 1
                log.SetTargetStart(0)
                log.SetTargetEnd(endDel)
                log.ReplaceTarget("")
            log.GotoPos(log.GetLength())
            log.AddText(data)
            log.GotoPos(log.GetLength())
            log.SetReadOnly(1)
        else:
            pass

    def on_menuOptionsAllowAny_select(self, event):
        self.webServer.allowAny = self.menuBar.getChecked('menuOptionsAllowAny')


if __name__ == '__main__':
    app = model.Application(WebServerView)
    app.MainLoop()
