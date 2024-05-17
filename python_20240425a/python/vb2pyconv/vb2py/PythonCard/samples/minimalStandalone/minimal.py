#!/usr/bin/python

"""
__version__ = "$Revision: 1.5 $"
__date__ = "$Date: 2004/05/05 16:53:26 $"
"""

from PythonCard import model

# KEA 2001-12-11
# if you want to build a standalone executable using py2exe
# then uncomment the import line below
# due to the way the dynamic imports of components work, each
# component that an app uses needs to be imported statically when
# doing a py2exe build
from PythonCard.components import textfield

class Minimal(model.Background):
    pass


if __name__ == '__main__':
    app = model.Application(Minimal)
    app.MainLoop()
