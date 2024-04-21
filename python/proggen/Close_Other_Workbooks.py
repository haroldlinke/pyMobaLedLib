from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as P01

"""--------------------------------
----------------------------
-----------------------------------
--------------------------------
"""

Callback_Proc = String()

def Abbort_Button_Click():
    #--------------------------------
    Me.Hide()

def OK_Button_Click():
    #----------------------------
    Me.Hide()
    if Callback_Proc != '':
        P01.Run(Callback_Proc)

def Start(Callback):
    global Callback_Proc
    #-----------------------------------
    Callback_Proc = Callback
    Me.Show()

def UserForm_Initialize():
    #--------------------------------
    # Center the dialog if it's called the first time.
    # On a second call without me.close this function is not called
    # => The last position ist used
    Change_Language_in_Dialog(Me)
    P01.Center_Form(Me)

# VB2PY (UntranslatedCode) Option Explicit
