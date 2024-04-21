from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as P01

""" F
 F
---------------------------------------------
-----------------------------
-----------------------------
-------------------------------------
----------------------------------------------
------------------------------
--------------------------------
----------------------------------------
----------------------------------------
-----------------------------------
-----------------------------------
--------------------------------
"""

WB1_Name = 'Prog_Generator_MobaLedLib.xlsm'
WB2_Name = 'Prog_Generator_MobaLedLib copie.xlsm'
FirstCol = 6
Last_Col = 6
sh1 = P01.Worksheet()
sh2 = P01.Worksheet()
r1 = P01.Range()
r2 = P01.Range()
MaxCol = Long()
MaxRow = Long()
EndReached = Boolean()
Direction = Integer()

def Make_sure_that_Var_are_defined():
    global r1, MaxCol, MaxRow, r2
    Old_WB = String()
    #---------------------------------------------
    Old_WB = P01.ActiveWorkbook.Name
    if r1 is None:
        P01.Workbooks(WB1_Name).Activate()
        r1 = P01.ActiveCell
        MaxCol = LastUsedColumn()
        MaxRow = LastUsedRow
        P01.Workbooks(WB2_Name).Activate()
        r2 = P01.ActiveCell
        if LastUsedColumn() > MaxCol:
            MaxCol = LastUsedColumn()
        if LastUsedRow > MaxRow:
            MaxRow = LastUsedRow
        if MaxCol > Last_Col:
            MaxCol = Last_Col
        P01.Workbooks(Old_WB).Activate()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: r - ByRef 
def Next_Cell(r):
    global EndReached
    #-----------------------------
    if r.Column < MaxCol:
        r = r.Offset(0, 1)
    else:
        r = r.Offset(1, - r.Column + FirstCol)
    EndReached = r.Row >= MaxRow

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: r - ByRef 
def Prev_Cell(r):
    global EndReached
    #-----------------------------
    if r.Column > FirstCol:
        r = r.Offset(0, - 1)
    else:
        if r.Row > 1:
            RowOffs = - 1
        r = r.Offset(RowOffs, MaxCol - 1)
        #EndReached = r.Row >= MaxRow And r.Column >= MaxCol
    EndReached = r.Row == 1 and r.Column == FirstCol

def Show_Act_Cells_in_Dialog():
    p = Long()

    i = Long()
    #-------------------------------------
    p = InStr(r1, '|')
    if p > 0:
        Debug.Print('Nach |' + Asc(Mid(r1, p + 1, 1)))
    Cell1Box = '{' + r1 + '}'
    # Add {} to see space characters at the end
    Cell2Box = '{' + r2 + '}'
    Diff1Box = ''
    Diff2Box = ''
    for i in vbForRange(1, Len(r1) + 1):
        if Mid(r1, i, 1) != Mid(r2, i, 1):
            if Len(r1) > i:
                Diff1Box = 'ASC(' + Asc(Mid(r1, i, 1)) + '):'
            else:
                Diff1Box = 'Len(' + Len(r1) + '):'
            Diff1Box = Diff1Box + Mid(r1, i)
            if Len(r2) > i:
                Diff2Box = 'ASC(' + Asc(Mid(r2, i, 1)) + '):'
            else:
                Diff2Box = 'Len(' + Len(r2) + '):'
            Diff2Box = Diff2Box + Mid(r2, i)
            break
    if r1 == r2:
        Diff1Box = '>>> Equal <<<'
    Addr1 = Replace(r1.Address, '$', '')
    Addr2 = Replace(r2.Address, '$', '')

def Show_Next_Prev_Diff(Nxt):
    global Direction
    ActWb = String()
    #----------------------------------------------
    Make_sure_that_Var_are_defined()
    ActWb = P01.ActiveWorkbook.Name
    if r1 == r2:
        while 1:
            if Nxt:
                Next_Cell(r1)
                Next_Cell(r2)
                Direction = 1
            else:
                Prev_Cell(r1)
                Prev_Cell(r2)
                Direction = - 1
            if r1 != r2 or EndReached:
                break
    Show_Act_Cells_in_Dialog()
    r1.Parent.Parent.Activate()
    # Switch to the workbook
    r1.Select()
    r2.Parent.Parent.Activate()
    # Switch to the workbook
    r2.Select()
    P01.Workbooks(ActWb).Activate()

def AbortButton_Click():
    #------------------------------
    Me.Hide()

def Reload_Button_Click():
    global r1, r2
    #--------------------------------
    r1 = None
    r2 = None
    Make_sure_that_Var_are_defined()
    Show_Act_Cells_in_Dialog()

def Show_Next_Diff_Button_Click():
    #----------------------------------------
    Show_Next_Prev_Diff(True)

def Show_Prev_Diff_Button_Click():
    #----------------------------------------
    Show_Next_Prev_Diff(False)

def Use_Lower_Button_Click():
    global r1
    #-----------------------------------
    # Copy the lower text to the upper
    if left(r2, 1) == '\'':
        r1 = '\'' + r2
    else:
        r1 = r2
    Show_Next_Prev_Diff(Direction >= 0)

def Use_Upper_Button_Click():
    global r2
    #-----------------------------------
    # Copy the upper text to the lower
    if left(r1, 1) == '\'':
        r2 = '\'' + r1
    else:
        r2 = r1
    Show_Next_Prev_Diff(Direction >= 0)

def UserForm_Initialize():
    #--------------------------------
    # Center the dialog if it's called the first time.
    # On a second call without me.close this function is not called
    # => The last position is used
    P01.Center_Form(Me)
    Make_sure_that_Var_are_defined()
    Show_Act_Cells_in_Dialog()

# VB2PY (UntranslatedCode) Option Explicit
