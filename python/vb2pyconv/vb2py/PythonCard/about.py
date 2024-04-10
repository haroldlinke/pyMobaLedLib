
"""
__version__ = "$Revision: 1.6 $"
__date__ = "$Date: 2004/10/03 18:53:22 $"
"""

import os, sys
import wx
from . import __version__
from . import dialog

def aboutPythonCardDialog(parent=None):
    """Displays a ScrolledMessageDialog containing info about PythonCard and version numbers"""

    aboutTitle = "About PythonCard"
    txt = """PythonCard
        
PythonCard is a GUI construction kit for building cross-platform desktop applications on Windows, Mac OS X, and Linux, using the Python language.

"""
    txt += "PythonCard version: %s\n" % __version__.VERSION_STRING
    txt += "wxPython version: %s\n" % wx.VERSION_STRING
    txt += "Python version: %s\n" % sys.version
    txt += "Platform: %s\n" % os.sys.platform
    txt += """
        
For more information see the docs directory included with this distribution.

Latest release files:
http://sourceforge.net/project/showfiles.php?group_id=19015

PythonCard home page
http://pythoncard.sourceforge.net/

SourceForge summary page
http://sourceforge.net/projects/pythoncard/

Mailing list
http://lists.sourceforge.net/lists/listinfo/pythoncard-users

PythonCard requires Python 2.3 or later and wxPython 2.5.2.8 or later.
"""
    dialog.scrolledMessageDialog(parent, txt, aboutTitle)
