#!/usr/bin/python

"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/10/03 23:58:02 $"
"""

from PythonCard import model

class MyBackground(model.Background):

    def on_initialize(self, event):
        # if you have any initialization
        # including sizer setup, do it here
        pass


if __name__ == '__main__':
    app = model.Application(MyBackground)
    app.MainLoop()
