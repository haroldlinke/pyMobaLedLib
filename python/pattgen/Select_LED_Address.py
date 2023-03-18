from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M60_Select_LED
import ExcelAPI.XLW_Workbook as X02

"""-------------------------------
----------------------------
-----------------------------------------------
-----------------------------
-----------------------------
-------------------------------
--------------------------------
-----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
------------------------------------------------------------------------
"""

ComPort = Integer()
MaxLed = Long()
IncDec_Act = Boolean()
Res = Integer()

def Abort_Button_Click():
    global Res
    #-------------------------------
    Res = - 1
    Me.Hide()

def OK_Button_Click():
    global Res
    #----------------------------
    if IsNumeric(LED_Address):
        Res = Val(LED_Address)
    else:
        Res = - 2
    Me.Hide()

def IncDec_LED_Address(Delta):
    global IncDec_Act
    Nr = Integer()
    #-----------------------------------------------
    if IncDec_Act:
        return
    IncDec_Act = True
    if IsNumeric(LED_Address):
        Nr = Val(LED_Address)
    else:
        Nr = 0
    Nr = Nr + Delta
    if Nr < 0:
        Nr = 0
    if Nr > MaxLed:
        Nr = MaxLed
    if IsNumeric(LED_Address) or Delta != 0:
        LED_Address = Nr
        pattgen.M60_Select_LED.Start_Flash_LED(ComPort, Nr)
        pattgen.M60_Select_LED.Set_Flash_LED(Nr)
    else:
        pattgen.M60_Select_LED.Stop_Flash_LED()
    IncDec_Act = False

def Dec_Button_Click():
    #-----------------------------
    IncDec_LED_Address(- 1)

def Inc_Button_Click():
    #-----------------------------
    IncDec_LED_Address(1)

def LED_Address_Change():
    #-------------------------------
    #  Debug.Print "LED_Address_Change :" & LED_Address
    pass

def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
    Change_Language_in_Dialog(Me)
    X02.Center_Form(Me)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyCode - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
def All_Buttons_KeyDown(KeyCode, Shift):
    #-----------------------------------------------------------------------------------------------------
    _select55 = KeyCode
    if (_select55 == vbKeyReturn):
        OK_Button.setFocus()
        OK_Button_Click()
    elif (_select55 == 189):
        IncDec_LED_Address(- 1)
        Dec_Button.setFocus()
    elif (_select55 == 187):
        IncDec_LED_Address(1)
        Inc_Button.setFocus()
    elif (_select55 == vbKeyDown):
        IncDec_LED_Address(- 1)
        Dec_Button.setFocus()
    elif (_select55 == vbKeyUp):
        IncDec_LED_Address(1)
        Inc_Button.setFocus()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyCode - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
def LED_Address_KeyDown(KeyCode, Shift):
    #----------------------------------------------------------------------------------------------
    Debug.Print('LED_Address_Keydown ' + KeyCode)
    _select56 = KeyCode
    if (_select56 == vbKeyReturn):
        IncDec_LED_Address(0)
        OK_Button.setFocus()
    else:
        All_Buttons_KeyDown(KeyCode, Shift)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyCode - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
def Dec_Button_KeyDown(KeyCode, Shift):
    #---------------------------------------------------------------------------------------------
    All_Buttons_KeyDown(KeyCode, Shift)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyCode - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
def Inc_Button_KeyDown(KeyCode, Shift):
    #---------------------------------------------------------------------------------------------
    All_Buttons_KeyDown(KeyCode, Shift)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyCode - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
def Ok_Button_KeyDown(KeyCode, Shift):
    #---------------------------------------------------------------------------------------------
    All_Buttons_KeyDown(KeyCode, Shift)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyCode - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
def Abort_Button_KeyDown(KeyCode, Shift):
    #-----------------------------------------------------------------------------------------------
    All_Buttons_KeyDown(KeyCode, Shift)

def ShowForm(PortId, Max_LEDNr):
    global ComPort, MaxLed
    _fn_return_value = None
    #------------------------------------------------------------------------
    ComPort = PortId
    MaxLed = Max_LEDNr
    LED_Address.setFocus()
    MaxNr_Label = 'Max: ' + Max_LEDNr
    Me.Show()
    pattgen.M60_Select_LED.Stop_Flash_LED()
    _fn_return_value = Res
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
