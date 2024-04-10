
"""
A spec file to make a standalone of minimal for
Windows and Linux platforms.  You can get
Gordon McMillans installer from
http://www.mcmillan-inc.com/install1.html

Use this command to build the standalone
and collect the other needed files:

  Build.py minimal.spec

__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2002/07/29 17:44:55 $"

"""

a = Analysis(['minimal.py'],
             pathex=[])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name='buildminimal/minimal.exe',
          debug=0,
          console=1)
coll = COLLECT( exe,
               a.binaries + \
               [('minimal.rsrc.py', 'minimal.rsrc.py', 'DATA')] + \
               [('readme.txt', 'readme.txt', 'DATA')],
               name='distminimal')
