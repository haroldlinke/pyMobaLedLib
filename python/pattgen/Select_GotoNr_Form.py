from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import pattgen.M80_Multiplexer_INI_Handling
import pattgen.M30_Tools as M30
import pattgen.Pattern_Generator as PG

"""'# VB2PY (CheckDirective) VB2PY directive Ignore Text
------------------------------------------
-------------------------------------
-----------------------------
--------------------------------
-----------------------------------------------------------------
"""

Button_Callback_Proc = String()

def Button_0_Click():
    Proc_Button(0)

def Button_1_Click():
    Proc_Button(1)

def Highlight_Button(Nr):
    i = Integer()

    BName = String()
    #------------------------------------------
    # -1 => All buttons normal
    for i in vbForRange(0, 63):
        _with83 = Me.Controls('Button_' + i)
        if i == Nr:
            _with83.BackColor = 0xFF00
        else:
            _with83.BackColor = 0x8000000F

def Proc_Button(Nr):
    #-------------------------------------
    PG.ThisWorkbook.Activate()
    # In case the user has switched to an other excel WB
    Highlight_Button(Nr)
    X02.Run(Button_Callback_Proc, Nr)

def End_Button_Click():
    Buf = String()
    #-----------------------------
    PG.ThisWorkbook.Activate()
    # In case the user has switched to an other excel WB
    Buf = Me.Top + ' ' + Me.Left
    X02.Run(Button_Callback_Proc, - 1)
    Store_Pos2(Me, pattgen.M80_Multiplexer_INI_Handling.Pos_Select_GotoNr_Form)
    X02.Unload(Me)

def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
    Change_Language_in_Dialog(Me)
    Restore_Pos_or_Leftaligne_Form2(Me, pattgen.M80_Multiplexer_INI_Handling.Pos_Select_GotoNr_Form)

def Show_Dialog(GotoCnt, Button_Callback):
    global Button_Callback_Proc
    HideRow = Long()

    Nr = Long()
    #-----------------------------------------------------------------
    Highlight_Button(- 1)
    Button_Callback_Proc = Button_Callback
    HideRow = WorksheetFunction.RoundUp(GotoCnt / 10, 0) * 10
    if HideRow <= 60:
        M30.Hide_and_Move_up(Me, 'Button_' + HideRow, 'End_Button')
    for Nr in vbForRange(GotoCnt, HideRow - 1):
        Me.Controls['Button_' + Nr].Visible = False
    Me.Show()

# VB2PY (UntranslatedCode) Option Explicit
