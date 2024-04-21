from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import proggen.M37_Inst_Libraries as M37
import proggen.M02_Public as M02
import ExcelAPI.XLA_Application as P01
import proggen.M31_Sound as M31

"""-----------------------------------------------------------------"""


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Worksheet_SelectionChange(Target):
    #-----------------------------------------------------------------
    # Is called by event if the worksheet selection has changed
    if M37.Is_Libraries_Select_Column(Target):
        if Target.Value == '':
            Target.Value = ChrW(M02.Hook_CHAR)
        else:
            Target.Value = ''
        P01.Range(P01.ActiveCell.Address).Offset(0, 1).Activate()
        M31.BeepThis2('Windows Balloon.wav')

# VB2PY (UntranslatedCode) Option Explicit
