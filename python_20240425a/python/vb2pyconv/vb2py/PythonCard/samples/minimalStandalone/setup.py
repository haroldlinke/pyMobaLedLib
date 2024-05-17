# A distutils script to make a standalone .exe of minimal for
# Windows platforms.  You can get py2exe from
# http://py2exe.sourceforge.net/.  Use this command to build the .exe
# and collect the other needed files:
#
#       python setup.py py2exe --excludes=Image
#

"""
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2005/04/05 18:44:54 $"
"""

from distutils.core import setup
import sys

if sys.platform == 'darwin':
    import py2app
    buildstyle = 'app'
else:
    import py2exe
    buildstyle = 'console'

setup( name = "minimal",
       data_files = [ (".", ["readme.txt", "minimal.rsrc.py"]) ],
       **{buildstyle: ["minimal.py"]}
       )
