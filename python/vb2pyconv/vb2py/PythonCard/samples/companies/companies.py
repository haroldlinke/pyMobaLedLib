#!/usr/bin/python

"""
__version__ = "$Revision: 1.13 $"
__date__ = "$Date: 2004/07/28 07:11:06 $"

"""

from PythonCard import configuration, flatfileDatabase, model
import os, sys
import webbrowser
import wx

# don't use a .ini
DATA_FILE = 'companies.pickle'
#DATA_FILE = 'companies-recs.xml'

class FlatfileDatabase(flatfileDatabase.FlatfileDatabase):
    def on_initialize(self, event):
        # override the data filename
        # so a .ini isn't needed
        self.configPath = os.path.join(configuration.homedir, 'companies')
        if not os.path.exists(self.configPath):
            os.mkdir(self.configPath)
        self.dataFile = os.path.join(self.configPath, DATA_FILE)
        flatfileDatabase.FlatfileDatabase.on_initialize(self, event)

    # KEA 2004-07-27
    # we won't receive a mouseUp event on Mac OS X
    # so we fake it
    def on_mouseDown(self, event):
        if wx.Platform == '__WXMAC__':
            self.on_mouseUp(event)
        else:
            event.skip()

    def on_mouseUp(self, event):
        #print event.target.name
        name = event.target.name
        if name in ['Profile', 'Symbol', 'Web']:
            url = event.target.text
            if name == 'Symbol':
                if url != '':
                    url = 'http://finance.yahoo.com/q?s=' + url + '&d=t'
            if url.startswith('http://'):
                webbrowser.open(url)
        else:
            event.skip()


if __name__ == '__main__':
    # dumb check and exit for the pickle file
    # there is almost certainly a better way to deal
    # with a missing data file
    configPath = os.path.join(configuration.homedir, 'companies')
    if not os.path.exists(configPath):
        os.mkdir(configPath)
    path = os.path.join(configPath, DATA_FILE)
    if not os.path.exists(path):
        print "Please run parse_companies.py first"
        sys.exit()
    
    app = model.Application(FlatfileDatabase)
    app.MainLoop()
