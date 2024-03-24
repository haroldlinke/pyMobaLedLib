from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02

"""--------------------------------
----------------------------------
-------------------------------------------
-------------------------------------
"""


def Label1_Click():

def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ":Load_All_Examples Initialize"
    Change_Language_in_Dialog(Me)
    X02.Center_Form(Me)

def Set_Label(Msg):
    #----------------------------------
    Label = Msg

def Set_ActSheet_Label(Txt):
    #-------------------------------------------
    ActSheet_Label = Txt
    ActSheet_Label.TextAlign = fmTextAlignCenter
    X02.DoEvents()

def Add_Dot_to_ActSheet_Label():
    #-------------------------------------
    ActSheet_Label.TextAlign = fmTextAlignLeft
    ActSheet_Label = ActSheet_Label + ChrW(9679)
    # Filled dot
    if Len(ActSheet_Label) > 10:
        ActSheet_Label = ''
    X02.DoEvents()

