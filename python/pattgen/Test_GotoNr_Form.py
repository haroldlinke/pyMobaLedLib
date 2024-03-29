from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M55_PWM_Data_Send
import ExcelAPI.XLW_Workbook as X02

"""------------------------------------------
----------------------------------------------
-------------------------------------
-----------------------------
--------------------------------
--------------------------------------------------------
"""

ComPort = Integer()
LedNr = Byte()
LEDCnt = 1

def Button_0_Click():
    Proc_Button(0)

def Button_1_Click():
    Proc_Button(1)

def Button_2_Click():
    Proc_Button(2)

def Button_3_Click():
    Proc_Button(3)

def Button_4_Click():
    Proc_Button(4)

def Button_5_Click():
    Proc_Button(5)

def Button_6_Click():
    Proc_Button(6)

def Button_7_Click():
    Proc_Button(7)

def Button_8_Click():
    Proc_Button(8)

def Button_9_Click():
    Proc_Button(9)

def Button_10_Click():
    Proc_Button(10)

def Button_11_Click():
    # CMD 0
    Proc_Button(11)

def Button_12_Click():
    # CMD 255
    Proc_Button(12)

def Highlight_Button(Nr):
    i = Integer()

    BName = String()
    #------------------------------------------
    # -1 => All buttons normal
    for i in vbForRange(0, 12):
        _with34 = Me.Controls('Button_' + i)
        if i == Nr:
            _with34.BackColor = 0xFF00
        else:
            _with34.BackColor = 0x8000000F

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: pwm - ByVal 
def Set_PWM_Label(pwm):
    #----------------------------------------------
    if pwm >= 0:
        PWM_Label = 'CMD: ' + pwm
    else:
        PWM_Label = ''

def Proc_Button(Nr):
    Res = Boolean()

    pwm = Byte()
    #-------------------------------------
    _select24 = Nr
    if (_select24 == 11):
        pwm = 0
    elif (_select24 == 12):
        pwm = 255
    else:
        pwm = pattgen.M55_PWM_Data_Send.Get_Goto_pwm(Nr)
    Res = pattgen.M55_PWM_Data_Send.Send_LED_PWM(ComPort, pwm, LedNr, LEDCnt)
    if Res:
        Highlight_Button(Nr)
        Set_PWM_Label(pwm)
    else:
        Highlight_Button(- 1)
        Set_PWM_Label(- 1)

def End_Button_Click():
    #-----------------------------
    Me.Hide()

def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
    Change_Language_in_Dialog(Me)
    X02.Center_Form(Me)

def Show_Dialog(PortId, LED_Nr):
    global ComPort, LedNr
    #--------------------------------------------------------
    ComPort = PortId
    LedNr = LED_Nr
    Highlight_Button(- 1)
    Set_PWM_Label(- 1)
    Me.Show()

# VB2PY (UntranslatedCode) Option Explicit
