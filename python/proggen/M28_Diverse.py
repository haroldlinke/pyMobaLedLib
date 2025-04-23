# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
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

import ExcelAPI.XLA_Application as P01
import proggen.M25_Columns as M25
import proggen.M02_Public as M02
import proggen.M09_Language as M09
import proggen.M30_Tools as M30
import mlpyproggen.Prog_Generator as PG
import proggen.F00_mainbuttons as F00


"""--------------------------------------------------------------
UT-----------------------------
----------------------------
-------------------------------------------------------------------
 24.12.19:
 Bei Armin stürtzt das Programm beim starten in den beiden folgenden Zeilen ab:
   sh.Cells(FirstDat_Row, Descrip_Col).Select
   .Cells(LRow + 1, Descrip_Col).Select
 Siehe Mail vom 23.12.19.
 Bei ihm hat die
   sh.Select
 Zeile gefehlt.
 Als Work arround habe ich die "On Error.. " Zeilen eingebaut. Damut läuft es.
-----------------------------------------------------------------------------------
UT-----------------------------------------------------------------
-------------------------------------------------------------
------------------------------------------
------------------------------------------   04.03.22 Juergen
UT----------------------------------
-------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------------
"""


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def Is_Data_Sheet(Sh):
    _fn_return_value = False
    PageId = String()
    #--------------------------------------------------------------
    PageId = Sh.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL)
    if PageId == '':
        return _fn_return_value
    # 07.10.21:
    _fn_return_value = ( InStr(M02.AllData_PgIDs, ' ' + PageId + ' ') > 0 )
    # 17.10.20: removed: And Sh.Name <> "Examples"
    # 07.08.20: Added: And Sh.Name <> "Examples"
    #Debug.Print "Is_Data_Sheet(" & sh.Name & ")=" & Is_Data_Sheet
    # Debug
    return _fn_return_value

def Test_Is_Data_Sheet():
    #UT-----------------------------
    Debug.Print(Is_Data_Sheet(P01.ThisWorkbook.Sheets('Start')))

def EnableAllButtons():
    Sh = Variant()
    #----------------------------
    # Enable all buttons in case they have been disabled by a crash
    for Sh in PG.ThisWorkbook.sheets:
        if Is_Data_Sheet(Sh):
            Sh.EnableDisableAllButtons(True)

def __Clear_COM_Port_Check(r, ReleaseMode):
    #-------------------------------------------------------------------
    # Set to a negativ number.
    _with0 = r
    if not ReleaseMode and IsNumeric(_with0.Value):
        _with0.Value = - Abs(P01.val(_with0.Value))
    else:
        #_with0.Value = 'COM?'
        #_with0.Value = F00.port_set_busy(_with0.Value)
        pass

def Clear_COM_Port_Check_and_Set_Cursor_in_all_Sheets(ReleaseMode):
    
    Skip_Scroll_Down = Boolean()
    # 25.12.19: Old: Clear_COM_Port_Check_ans_Set_Cursor_in_all_Sheets
    #-----------------------------------------------------------------------------------
    OldSh = P01.ActiveSheet
    if P01.ActiveSheet is None:
        # 29.10.19:
        Debug.Print('ActiveSheet Is Nothing in Clear_COM_Port_Check_and_Set_Cursor_in_all_Sheets')
        Debug.Print('Tritt beim ersten Start nach dem Download vom Internet auf (\'Geschützte Ansicht\')')
        Skip_Scroll_Down = True
    for Sh in PG.ThisWorkbook.sheets:
        if Is_Data_Sheet(Sh):
            _with1 = Sh
            M25.Make_sure_that_Col_Variables_match(Sh)
            __Clear_COM_Port_Check(_with1.Cells(M02.SH_VARS_ROW, M25.COMPort_COL), ReleaseMode)
            if Sh.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL) != 'CAN':
                __Clear_COM_Port_Check(_with1.Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL), ReleaseMode)
                if ReleaseMode:
                    _with1.CellDict[M02.SH_VARS_ROW, M25.R_UPLOD_COL] = 'R not Chk'
                # Right arduino software is not checked
            if not Skip_Scroll_Down:
                # 29.10.19:
                # VB2PY (UntranslatedCode) On Error Resume Next
                # 24.12.19: Problems with Office 365 ?
                Sh.Select()
                # 29.10.19:
                Sh.Cells(M02.FirstDat_Row, M25.Descrip_Col).Select()
                # Scroll to the top
                LRow = M30.LastFilledRowIn_ChkAll(Sh)
                _with1.Cells(LRow + 1, M25.Descrip_Col).Select()
                # Select the first empty row
                #While .Rows(LRow).EntireRow.Hidden                            ' 29.10.19: Disabled
                # 29.10.19: Disabled
                #   LRow = LRow + 1
                #Wend
                # VB2PY (UntranslatedCode) On Error GoTo 0
                # 24.12.19:
            # 12.10.21: Jürgen Clear errors
            #*HL for rngCell in Sh.UsedRange:
            #*HL     for i in vbForRange(1, 7):
            #*HL        pass #*HL rngCell.Errors.Item[i].Ignore = True
    if not OldSh is None:
        OldSh.Select()

def Test_Clear_COM_Port_Check_and_Set_Cursor_in_all_Sheets():
    #UT-----------------------------------------------------------------
    Clear_COM_Port_Check_and_Set_Cursor_in_all_Sheets(True)

def Get_Bool_Config_Var(Name):
    _fn_return_value = False
    #-------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo NotFound
    
    _with2 = PG.ThisWorkbook.Sheets(M02.ConfigSheet).Range(Name)
    conf_value = UCase(Left(Trim(_with2.Value), 1))
    # Languages (DE,  EN, NL,  FR,   IT, ES)
    #confsheet = PG.ThisWorkbook.Sheets(M02.ConfigSheet)
    #conf_value = confsheet.find_in_col_ret_col_val(Name,4,3,cache=True)
    if conf_value !=None:
        if (conf_value == '') or (conf_value == 'N') or (conf_value == 'G') or (conf_value == 'A') or (conf_value == '0'):
            _fn_return_value = False
            #            Nein No  geen aucun no  no
            # 14.05.20: Added "0"
            return _fn_return_value
        else:
            _fn_return_value = True
        #            Ja   Yes ja   oui   sì sì
    return _fn_return_value
    P01.MsgBox('Interner Fehler: Die Konfigurationsvariable \'' + Name + '\' wurde nicht im Sheet \'' + M02.ConfigSheet + '\' gefunden', vbCritical, 'Interner Fehler in Get_Bool_Config_Var')
    M30.EndProg()
    return _fn_return_value

def Get_Num_Config_Var(Name):
    _ret = -1
    p_str = String()
    #------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo NotFound
    p_str = PG.ThisWorkbook.Sheets(M02.ConfigSheet).Range(Name)
    
    #confsheet = PG.ThisWorkbook.Sheets(M02.ConfigSheet)
    #Str = confsheet.find_in_col_ret_col_val(Name,4,3,cache=True)    
    if p_str:
        if IsNumeric(p_str):
            _ret = P01.val(p_str)
        else:
            _ret = - 1
        return _ret
    else:
        P01.MsgBox('Interner Fehler: Die Konfigurationsvariable \'' + Name + '\' wurde nicht im Sheet \'' + M02.ConfigSheet + '\' gefunden', vbCritical, 'Interner Fehler in Get_Num_Config_Var')
        M30.EndProg()
        return _ret
    
"""------------------------------------------   04.03.22 Juergen"""


def Get_Num_Config_Var_Range(Name, Min, Max, Default=0):
    fn_return_value = None
    p_str = String()
    #------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo NotFound
    try:
        
        value = PG.ThisWorkbook.Sheets(M02.ConfigSheet).Range(Name)
        if value != None:
            fn_return_value = P01.val(value)
        else:
            fn_return_value = Default
        if fn_return_value < Min:
            fn_return_value = Min
        if fn_return_value> Max:
            fn_return_value = Max
        return fn_return_value
    except:
        
        P01.MsgBox('Interner Fehler: Die Konfigurationsvariable \'' + Name + '\' wurde nicht im Sheet \'' + M02.ConfigSheet + '\' gefunden', vbCritical, 'Interner Fehler in Get_Num_Config_Var')
        M30.EndProg()
        return fn_return_value



def __TestGet_Bool_Config_Var():
    #UT----------------------------------
    Debug.Print('Get_Bool_Config_Var=' + Get_Bool_Config_Var('Lib_Installed_other'))

def Set_Bool_Config_Var(Name, val):
    #-------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo NotFound
    _with3 = PG.ThisWorkbook.Sheets(M02.ConfigSheet).Range(Name)
    #if val:
    #    val_str = M09.Get_Language_Str('Ja')
    #else:
    #    val_str = M09.Get_Language_Str('Nein')    
    #confsheet = PG.ThisWorkbook.Sheets(M02.ConfigSheet)
    #if confsheet.find_in_col_set_col_val(Name,4,3,val_str,cache=True):
    #    return True
    #else:
    if _with3!=None:    
        if val:
            _with3.Value = M09.Get_Language_Str('Ja')
        else:
            _with3.Value = M09.Get_Language_Str('Nein')
        return
    else:
        P01.MsgBox('Interner Fehler: Die Konfigurationsvariable \'' + Name + '\' wurde nicht im Sheet \'' + M02.ConfigSheet + '\' gefunden', vbCritical, 'Interner Fehler in Set_Bool_Config_Var')
        M30.EndProg()
    return

def Get_String_Config_Var(Name):
    _ret = ""
    Debug.Print("Get_String_Config_Var: %s",Name)
    #--------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo NotFound
    _ret = PG.ThisWorkbook.Sheets(M02.ConfigSheet).Range(Name)
    if _ret!=None:
        return str(_ret)
    #confsheet = PG.ThisWorkbook.Sheets(M02.ConfigSheet)
    #conf_value = confsheet.find_in_col_ret_col_val(Name,4,3,cache=True)    
    #if conf_value!=None:
    #    return conf_value
    else:
        P01.MsgBox('Interner Fehler: Die Konfigurationsvariable \'' + Name + '\' wurde nicht im Sheet \'' + M02.ConfigSheet + '\' gefunden', vbCritical, 'Interner Fehler in Get_String_Config_Var')
        M30.EndProg()
    return _ret

def Set_String_Config_Var(Name, val):
    #--------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo NotFound
    try:
        PG.ThisWorkbook.Sheets(M02.ConfigSheet).Range(Name).Value=val
    #confsheet = PG.ThisWorkbook.Sheets(M02.ConfigSheet)
    #if confsheet.find_in_col_set_col_val(Name,4,3,val,cache=True):
    #    return True
    except:  
        P01.MsgBox('Interner Fehler: Die Konfigurationsvariable \'' + Name + '\' wurde nicht im Sheet \'' + M02.ConfigSheet + '\' gefunden', vbCritical, 'Interner Fehler in Set_String_Config_Var')
        #test M30.EndProg()

def Get_Old_Board(LeftArduino):
    _ret = ""
    Col = Integer()

    BuildOpt = String()
    # 04.05.20: Extracted from Get_Arduino_Typ()
    #--------------------------------------------------------------
    if LeftArduino:
        Col = M25.BUILDOP_COL
    else:
        Col = M25.BUILDOpRCOL
    BuildOpt = P01.Cells(M02.SH_VARS_ROW, Col)
    if InStr(BuildOpt, M02.BOARD_NANO_OLD) > 0:
        _ret = M02.BOARD_NANO_OLD
    elif InStr(BuildOpt, M02.BOARD_UNO_NORM) > 0:
        _ret = M02.BOARD_UNO_NORM
    elif InStr(BuildOpt, M02.BOARD_NANO_EVERY) > 0:
        _ret = M02.BOARD_NANO_EVERY
        # 28.10.20: Jürgen
    elif InStr(BuildOpt, M02.BOARD_NANO_FULL) > 0:
        _ret = M02.BOARD_NANO_FULL
        # 28.10.20: Jürgen
    elif InStr(BuildOpt, M02.BOARD_NANO_NEW) > 0:
        _ret = M02.BOARD_NANO_NEW
    return _ret

def Change_Board_Typ(LeftArduino, NewBrd):
    Col = int()

    Brd = Integer()

    BuildOpt = String()

    Old_Board = String()
    #--------------------------------------------------------------------
    #  If Disable_Set_Arduino_Typ Then Exit Sub
    if LeftArduino:
        Col = M25.BUILDOP_COL
        Brd = 0
    else:
        Col = M25.BUILDOpRCOL
        Brd = 1
    Old_Board = Get_Old_Board(LeftArduino)
    BuildOpt = P01.Cells(M02.SH_VARS_ROW, Col)
    if Old_Board == '':
        BuildOpt = NewBrd
        # & " " & BuildOpt               28.10.20: Jürgen: Disabled "& " " & BuildOpt"
    else:
        BuildOpt = Replace(BuildOpt, Old_Board, NewBrd)
    P01.CellDict[M02.SH_VARS_ROW, Col] = Trim(BuildOpt)

def Is_Named_Range(rng):
    _ret = False
    # VB2PY (UntranslatedCode) On Error Resume Next
    _ret = rng.Name.Name != ''
    return _ret

# VB2PY (UntranslatedCode) Option Explicit
