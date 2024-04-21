from vb2py.vbfunctions import *
from vb2py.vbdebug import *


# Enumeration 'Language'
DE = 0
EN = 1
Texts = Scripting.Dictionary()

def class_initialize():
    Texts = Scripting.Dictionary()

def SetText(Lang, Key, Value):
    global Texts
    Texts[Lang + '.' + Key] = Value

def GetText(Lang, Key):
    _fn_return_value = False
    if Texts.Exists(Lang + '.' + Key):
        _fn_return_value = Texts(Lang + '.' + Key)
    else:
        _fn_return_value = Key
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
