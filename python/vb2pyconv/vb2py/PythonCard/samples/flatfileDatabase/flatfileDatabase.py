#!/usr/bin/python

"""
__version__ = "$Revision: 1.21 $"
__date__ = "$Date: 2004/08/03 15:57:05 $"

flatfileDatabase was derived from the addresses sample.

"""

from PythonCard import flatfileDatabase, model
import os, sys
import ConfigParser

CONFIG_FILE = 'flatfileDatabase.ini'

class FlatfileDatabase(flatfileDatabase.FlatfileDatabase):
    def on_initialize(self, event):
        # override the config filename
        self.configFilename = CONFIG_FILE
        flatfileDatabase.FlatfileDatabase.on_initialize(self, event)

if __name__ == '__main__':
    # assume the ini file is in the same directory as the script
    path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), CONFIG_FILE)
    parser = ConfigParser.ConfigParser()
    parser.read(path)
    # the resourceFile is settable via the ini file
    resourceFile = parser.get('ConfigData', 'resourceFile')

    # KEA 2002-07-16
    # since all of the needed functionality is in the framework
    # classes, we don't have to subclass in this module, we can
    # just use the base class directly
    app = model.Application(FlatfileDatabase, resourceFile)
    app.MainLoop()
