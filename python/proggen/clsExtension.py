from vb2py.vbfunctions import *
from vb2py.vbdebug import *

""" the name of the extension must contain only basic letters (A-Z or a-z) and numbers (0-9), underscores (_)and dashes (-).
 They must start with a letter or number. They must contain at least one letter.

-----------------------------------------------------------
return an error message in case of check fails, otherwise empty string
-----------------------------------------------------------
-----------------------------------------------------------
return an error message in case of check fails, otherwise empty string
-----------------------------------------------------------
"""

Platforms = Collection()
Id = Integer()
Name = String()
path = String()
Includes = String()
MacroIncludes = String()
Constructors = Collection()
Macros = Collection()
Parameters = Collection()
NamePattern = '^[A-Za-z0-9][A-Za-z0-9_\\-]*$'

def class_initialize():
    Constructors = Collection()
    Macros = Collection()
    Parameters = Collection()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: TypeName - ByVal 
def GetConstructor(TypeName):
    _fn_return_value = False
    Constructor = Variant()
    for Constructor in Constructors:
        if Constructor.TypeName == TypeName:
            _fn_return_value = Constructor
            return _fn_return_value
    _fn_return_value = None
    return _fn_return_value

def CheckValid():
    _fn_return_value = False
    if not Matches(Name, NamePattern):
        _fn_return_value = 'Extension Name is invalid'
        return _fn_return_value
    _fn_return_value = ''
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Argument - ByVal 
def IsExtensionParameter(Argument):
    _fn_return_value = False
    Parameter = Variant()
    for Parameter in Parameters:
        if Parameter.Name == Argument:
            _fn_return_value = True
            return _fn_return_value
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
