"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2003/04/22 02:32:48 $"
"""

from vb2py.PythonCardPrototype import model

#
# VB constants
True = 1
False = 0

class MAINFORM(model.Background):
    """The main form for the application"""

# CODE_GOES_HERE
        
if __name__ == '__main__':
    app = model.vb2py.PythonCardApp(MAINFORM)
    app.MainLoop()
