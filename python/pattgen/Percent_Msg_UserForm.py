from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02

"""--------------------------------
----------------------------------
-----------------------------------------
"""


def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ":Load_All_Examples Initialize"
    Change_Language_in_Dialog(Percent_Msg_UserForm)
    X02.Center_Form(Me)

def Set_Label(Msg):
    #----------------------------------
    Label = Msg

def Set_Status_Label(Txt):
    #-----------------------------------------
    Status_Label = Txt
    X02.DoEvents()

# VB2PY (UntranslatedCode) Option Explicit
