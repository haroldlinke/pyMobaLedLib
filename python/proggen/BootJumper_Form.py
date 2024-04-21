from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as P01

"""--------------------------------
-------------------------------
--------------------------------------
--------------------------------
"""

Res = Boolean()
FlashAs328P = Boolean()

def Abbort_Button_Click():
    global Res
    #--------------------------------
    Res = False
    Me.Hide()
    # no "Unload Me" to keep position

def Start_Button_Click():
    global Res, FlashAs328P
    #-------------------------------
    Res = True
    FlashAs328P = CheckBoxChangeSignature.Value
    Me.Hide()
    # no "Unload Me" to keep position

def ShowDialog():
    global Res
    _fn_return_value = False
    #--------------------------------------
    Res = False
    CheckBoxChangeSignature.Value = True
    Me.Show()
    _fn_return_value = Res
    return _fn_return_value

def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
    Change_Language_in_Dialog(Me)
    P01.Center_Form(Me)

# VB2PY (UntranslatedCode) Option Explicit
