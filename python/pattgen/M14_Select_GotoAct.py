from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M02_Main as M02
import pattgen.M09_Language
import pattgen.Pattern_Generator as PG
import pattgen.D00_Forms

""" Sheet Goto_Activation_Entries: (The Sheet can not be changed by the USER => We keep the constants)
------------------------------------------------------------------------------------
-------------------------------------------------------
-----------------------------------------------------------------------------
"""

SM_DIALOGDATA_ROW1 = 4
SM_Mode__COL = 1
SM_OutCntCOL = 2
SM_Macro_COL = 3
SM_Name__COL = 4
SM_ShrtD_COL = 5
SM_DetailCOL = 6
GotoAct_Res = String()
Userform_Res = String()
ExpOutCnt_g = Integer()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Macro - ByVal 
def Proc_General(Macro, Description):
    _fn_return_value = None
    Parts = Variant()

    Res = String()

    Param = Variant()
    #------------------------------------------------------------------------------------
    if Macro == '':
        return _fn_return_value
    if InStr(Macro, '(') == 0:
        _fn_return_value = Macro
        return _fn_return_value
    Parts = Split(Replace(Macro, ')', ''), '(')
    Param = Split(Parts(1), ',')
    UserForm_Other.Show_UserForm_Other(Parts(1), Parts(0), Description)
    _fn_return_value = Userform_Res
    return _fn_return_value

def Check_Param_Goto(Row):
    _fn_return_value = None
    #-------------------------------------------------------
    # This function is used in the Goto Dialog
    _with52 = X02.Sheets(M01.GOTO_ACTIVATION_SH)
    _fn_return_value = ( _with52.Cells(Row, SM_OutCntCOL) >= ExpOutCnt_g )
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ExpOutCnt=VBMissingArgument - ByVal 
def Select_GotoAct(ExpOutCnt=VBMissingArgument):
    global ExpOutCnt_g, GotoAct_Res
    _fn_return_value = None
    #-----------------------------------------------------------------------------
    ExpOutCnt_g = ExpOutCnt
    GotoAct_Res = pattgen.D00_Forms.Select_from_Sheet_Form.Show_Form(M01.GOTO_ACTIVATION_SH, pattgen.M09_Language.Get_Language_Str('Auswahl der Goto Aktivierung'), pattgen.M09_Language.Get_Language_Str('Goto Aktivierung auswählen:'), pattgen.M09_Language.Get_Language_Str('Wenn der Goto Mode verwendet wird, dann kann das Muster an verschiedenen Stellen ' + 'gestartet werden. Diese Spalten sind in der Tabelle mit nummerierten Pfeilen markiert.' + vbCr + 'Mit diesem Dialog wird definiert wie die Startspalte im Betrieb ausgewählt wird.'), oCheck_Param_Func= 'Check_Param_Goto', oMiddleWinCOL= 6, oDelete_Button= True)
    if GotoAct_Res != '':
        if GotoAct_Res == 'DELETE':
            X02.RangeDict['Goto_Aktivierung'] = ''
        else:
            MacroName = Split(GotoAct_Res, ',')(0)
            SelRow = Split(GotoAct_Res, ',')(1)
            _with53 = PG.ThisWorkbook.Sheets(M01.GOTO_ACTIVATION_SH)
            Macro = _with53.Cells(SelRow, SM_Macro_COL)
            Description = Replace(_with53.Cells(SelRow, SM_DetailCOL), '|', vbLf)
            if Description == '':
                Description = _with53.Cells(SelRow, SM_ShrtD_COL)
            Res = Proc_General(Macro, Description)
            if Res != '':
                X02.RangeDict['Goto_Aktivierung'] = Res
                _fn_return_value = True
    if not M02.Last_SelectedCell is None:
        if M02.Last_SelectedCell.Worksheet.Name != X02.ActiveSheet.Name:
            M02.Last_SelectedCell = None
    # Move the cursor out of the cell because otherwise the user may change things by mistake
    X02.Application.EnableEvents = False
    # Don't call Worksheet_SelectionChange
    if M02.Last_SelectedCell is None:
        X02.ActiveCell().offset(1, 0).Select()
    else:
        dRow = - 1
        if M02.Last_SelectedCell.Row <= X02.ActiveCell().Row:
            dRow = 1
        X02.ActiveCell().offset(dRow, 0).Select()
    X02.Application.EnableEvents = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
