#!/usr/bin/python

"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/09/14 17:28:46 $"
"""

from PythonCard import model

class Minimal(model.PageBackground):
    pass

if __name__ == '__main__':
    app = model.Application(Minimal)
    app.MainLoop()
