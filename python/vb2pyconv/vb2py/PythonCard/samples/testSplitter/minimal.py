#!/usr/bin/python

"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/09/28 21:23:55 $"
"""

from PythonCard import model

class Minimal(model.PageBackground):
    pass

if __name__ == '__main__':
    app = model.Application(Minimal)
    app.MainLoop()
