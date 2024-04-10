shell.autoCompleteIncludeMagic = True
shell.autoCompleteIncludeSingle = False
shell.autoCompleteIncludeDouble = False
shell.autoCompleteWxMethods = False

import os
import sys
# workaround for absolute pathnames
# in sys.path (see model.py)
if sys.path[0] not in ('', '.'):
    sys.path.insert(0, '')

import wx
from PythonCard import dialog, util
bg = pcapp.getCurrentBackground()
self = bg
comp = bg.components
