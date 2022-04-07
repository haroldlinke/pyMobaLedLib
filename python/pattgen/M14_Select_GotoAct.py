# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 4.02
# * Author: Harold Linke
# * Date: January 7, 2021
# * Copyright: Harold Linke 2021
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *  
# * https://github.com/Hardi-St/MobaLedLib
# *
# * MobaLedCheckColors is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * MobaLedCheckColors is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  if not, see <http://www.gnu.org/licenses/>.
# *
# *
# ***************************************************************************

#------------------------------------------------------------------------------
# CHANGELOG:
# 2020-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2021-01-07 v4.02 HL: - Else:, ByRef check done, first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *


import proggen.Prog_Generator as PG

import ExcelAPI.P01_Workbook as P01

from ExcelAPI.X01_Excel_Consts import *


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

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
__ExpOutCnt_g = Integer()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Macro - ByVal 
def __Proc_General(Macro, Description):
    fn_return_value = None
    Parts = Variant()

    Res = String()

    Param = Variant()
    #------------------------------------------------------------------------------------
    if Macro == '':
        return fn_return_value
    if InStr(Macro, '(') == 0:
        fn_return_value = Macro
        return fn_return_value
    Parts = Split(Replace(Macro, ')', ''), '(')
    Param = Split(Parts(1), ',')
    UserForm_Other.Show_UserForm_Other(Parts(1), Parts(0), Description)
    fn_return_value = Userform_Res
    return fn_return_value

def Check_Param_Goto(Row):
    fn_return_value = None
    #-------------------------------------------------------
    # This function is used in the Goto Dialog
    with_0 = Sheets(GOTO_ACTIVATION_SH)
    fn_return_value = ( with_0.Cells(Row, SM_OutCntCOL) >= __ExpOutCnt_g )
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ExpOutCnt=VBMissingArgument - ByVal 
def Select_GotoAct(ExpOutCnt=VBMissingArgument):
    fn_return_value = None
    #-----------------------------------------------------------------------------
    __ExpOutCnt_g = ExpOutCnt
    GotoAct_Res = Select_from_Sheet_Form.Show_Form(GOTO_ACTIVATION_SH, Get_Language_Str('Auswahl der Goto Aktivierung'), Get_Language_Str('Goto Aktivierung auswählen:'), Get_Language_Str('Wenn der Goto Mode verwendet wird, dann kann das Muster an verschiedenen Stellen ' + 'gestartet werden. Diese Spalten sind in der Tabelle mit nummerierten Pfeilen markiert.' + vbCr + 'Mit diesem Dialog wird definiert wie die Startspalte im Betrieb ausgewählt wird.'), oCheck_Param_Func= 'Check_Param_Goto', oMiddleWinCOL= 6, oDelete_Button= True)
    if GotoAct_Res != '':
        if GotoAct_Res == 'DELETE':
            Range['Goto_Aktivierung'] = ''
        else:
            MacroName = Split(GotoAct_Res, ',')(0)
            SelRow = Split(GotoAct_Res, ',')(1)
            with_1 = ThisWorkbook.Sheets(GOTO_ACTIVATION_SH)
            Macro = with_1.Cells(SelRow, SM_Macro_COL)
            Description = Replace(with_1.Cells(SelRow, SM_DetailCOL), '|', vbLf)
            if Description == '':
                Description = with_1.Cells(SelRow, SM_ShrtD_COL)
            Res = __Proc_General(Macro, Description)
            if Res != '':
                Range['Goto_Aktivierung'] = Res
                fn_return_value = True
    if not Last_SelectedCell is None:
        if Last_SelectedCell.Worksheet.Name != ActiveSheet.Name:
            Last_SelectedCell = None
    # Move the cursor out of the cell because otherwise the user may change things by mistake
    Application.EnableEvents = False
    if Last_SelectedCell is None:
        ActiveCell.offset(1, 0).Select()
    else:
        dRow = - 1
        if Last_SelectedCell.Row <= ActiveCell.Row:
            dRow = 1
        ActiveCell.offset(dRow, 0).Select()
    Application.EnableEvents = True
    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
