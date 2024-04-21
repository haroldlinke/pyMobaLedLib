from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as P01

"""--------------------------------
----------------------------
----------------------------------------------------------------------------
--------------------------------
"""

Callback_Proc = String()

def Abbort_Button_Click():
    #--------------------------------
    Me.Hide()
    if Callback_Proc != '':
        P01.Run(Callback_Proc, False, Import_FromAllSheets_CheckBox)

def OK_Button_Click():
    #----------------------------
    Me.Hide()
    if Callback_Proc != '':
        P01.Run(Callback_Proc, True, Import_FromAllSheets_CheckBox)

def Start(Callback, Import_FromAll=- 1):
    global Callback_Proc
    #----------------------------------------------------------------------------
    Callback_Proc = Callback
    if Import_FromAll == - 2:
        Import_FromAllSheets_CheckBox = False
        Import_FromAllSheets_CheckBox.Enabled = False
        MultiSelectSheets_Label.Visible = False
    else:
        Import_FromAllSheets_CheckBox.Enabled = True
        MultiSelectSheets_Label.Visible = True
        if Import_FromAll > 0:
            Import_FromAllSheets_CheckBox = True
        if Import_FromAll == 0:
            Import_FromAllSheets_CheckBox = False
    Me.Show()

def UserForm_Initialize():
    #--------------------------------
    # Center the dialog if it's called the first time.
    # On a second call without me.close this function is not called
    # => The last position ist used
    Change_Language_in_Dialog(Me)
    P01.Center_Form(Me)

# VB2PY (UntranslatedCode) Option Explicit
