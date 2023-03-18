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


# fromx proggen.M02_Public import SH_VARS_ROW,PAGE_ID_COL,Header_Row

from ExcelAPI.XLC_Excel_Consts import *

import proggen.M02_Public as M02
#import proggen.M02_global_variables as M02GV
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header as M06
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
#import proggen.M07_COM_Port as M07
#import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
#import proggen.M20_PageEvents_a_Functions as M20
#import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Mulitplexer as M80
import proggen.Prog_Generator as PG

import ExcelAPI.XLW_Workbook as P01


Col_from_Sheet = ""  #*HL
Filter__Col = int()
Inp_Typ_Col = int()
Start_V_Col = int()
Descrip_Col = int()
Dist_Nr_Col = int()
Conn_Nr_Col = int()
MacIcon_Col = int()
LanName_Col = int()
Config__Col = int()
LED_Nr__Col = int()
LEDs____Col = int()
InCnt___Col = int()
LocInCh_Col = int()
LED_Cha_Col = int()
LED_TastCol = int()
COMPort_COL = int()
BUILDOP_COL = int()
R_UPLOD_COL = int()
COMPrtR_COL = int()
BUILDOpRCOL = int()
COMPrtT_COL = 0
DCC_or_CAN_Add_Col = int()
SX_Channel_Col = int()
SX_Bitposi_Col = int()
Page_ID = String()

def Add_Icons_and_Lines():
    #Sh = P01.CWorksheet
    #--------------------------------
    P01.Application.EnableEvents = False
    for Sh in PG.ThisWorkbook.Sheets:
        if M28.Is_Data_Sheet(Sh):
            Make_sure_that_Col_Variables_match(Sh)
            with_variable0 = Sh
            if with_variable0.Cells(M02.Header_Row, MacIcon_Col) == r'Beleuchtung, Sound, oder andere Effekte':
                with_variable1 = with_variable0.Columns(M30.ColumnLettersFromNr(MacIcon_Col) + r':' + M30.ColumnLettersFromNr(MacIcon_Col))
                #.Select ' Debug
                with_variable1.Insert(Shift=xlToRight, CopyOrigin=xlFormatFromLeftOrAbove)
                with_variable1.Insert(Shift=xlToRight, CopyOrigin=xlFormatFromLeftOrAbove)
                with_variable0.Columns[M30.ColumnLettersFromNr(MacIcon_Col) + r':' + M30.ColumnLettersFromNr(MacIcon_Col)].ColumnWidth = 1.78
                with_variable2 = with_variable0.Cells(M02.Header_Row, MacIcon_Col)
                with_variable2.FormulaR1C1 = r'Icon'
                with_variable2.Orientation = 90
                with_variable2.Offset[0, 1].FormulaR1C1 = r'Name'
                with_variable0.Range[with_variable0.Cells(M02.Header_Row, LanName_Col), with_variable0.Cells(M30.LastUsedRowIn(Sh), LanName_Col)].HorizontalAlignment = xlLeft
                with_variable0.CellDict[M02.SH_VARS_ROW, Conn_Nr_Col] = r''
                with_variable0.CellDict[M02.SH_VARS_ROW, COMPrtR_COL] = r'Com?'
    P01.Application.EnableEvents = True

def Del_Icons_and_Lines():
    #Sh = Variant()
    #--------------------------------
    P01.Application.EnableEvents = False
    for Sh in PG.ThisWorkbook.Sheets:
        if M28.Is_Data_Sheet(Sh):
            Make_sure_that_Col_Variables_match(Sh)
            First_Col = MacIcon_Col
            with_variable3 = Sh
            if with_variable3.Cells(M02.Header_Row, First_Col) == r'Icon':
                with_variable3.Columns(M30.ColumnLettersFromNr(First_Col) + r':' + M30.ColumnLettersFromNr(First_Col + 1)).Delete(Shift=xlToLeft)
    P01.Application.EnableEvents = True

def Has_Macro_and_LanguageName_Column(Sh, Col):
    #------------------------------------------------------------------------------------------
    with_variable4 = Sh.Cells(M02.Header_Row, Col)
    fn_return_value = True #*HL
    if with_variable4.Orientation == xlUpward:
        fn_return_value = True
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh=None - ByVal 
def Make_sure_that_Col_Variables_match(Sh=None, Switch_back_Target=None):
    global Col_from_Sheet,SH_VARS_ROW,PAGE_ID_COL,Inp_Typ_Col,Filter__Col,Start_V_Col,Descrip_Col,Dist_Nr_Col,Conn_Nr_Col,MacIcon_Col,LanName_Col,Config__Col,LED_Nr__Col,LEDs____Col,InCnt___Col,LocInCh_Col,LED_Cha_Col
    global LED_TastCol,COMPort_COL,BUILDOP_COL,R_UPLOD_COL,COMPrtR_COL,BUILDOpRCOL,COMPrtT_COL,DCC_or_CAN_Add_Col,SX_Channel_Col,SX_Bitposi_Col,Ref_Col,Page_ID
    #----------------------------------------------------------------------------------------------------------------------------------
    # Fills the global variables which contain the column numbers
    if Sh is None:
        Sh = P01.ActiveSheet
    if Sh.Name == Col_from_Sheet:
        return
        # Already read in => exit
    #Debug.Print "Updating the Col_Variables"
    if not Switch_back_Target is None: #*HL
        if Switch_back_Target.Parent.Name != Sh.Name:
            Debug.Print(r'Switching back to ' + Switch_back_Target.Parent.Name + r' in Make_sure_that_Col_Variables_match()')
            # VB2PY (UntranslatedCode) On Error GoTo ErrSwitchBack
            Switch_back_Target.Parent.Select()
            # VB2PY (UntranslatedCode) On Error GoTo 0
        return
    Page_ID = Sh.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL)
    if Page_ID == r'':
        return
        # 07.10.21:
    # Sheet specific columns
    SX_Channel_Col = 0
    SX_Bitposi_Col = 0
    DCC_or_CAN_Add_Col = 0
    select_variable_0 = Page_ID
    if (select_variable_0 == r'Selectrix'):
        SX_Channel_Col = 4
        SX_Bitposi_Col = 5
    elif (select_variable_0 == r'DCC'):
        DCC_or_CAN_Add_Col = 4
    elif (select_variable_0 == r'CAN'):
        DCC_or_CAN_Add_Col = 4
    else:
        Debug.Print(r'Seitenname: ' + Sh.Name + r' Page_ID: ' + Page_ID + r'')
        P01.MsgBox(M09.Get_Language_Str(r'Fehler: Die Excel Seite wurde gewechselt während einer Änderung in einer Zelle. ' + vbCr + r'Die Änderungen können nicht überprüft werden ;-(' + vbCr + vbCr + r'Die Eingaben in einer Zelle müssen mit Enter abgeschlossen werden bevor die Seite gewechselt wird.'), vbCritical, M09.Get_Language_Str(r'Fehler: Seite gewechselt während der Eingabe in einer Zelle'))
        # Normalerweise sollte diese Fehlermeldung nicht mehr kommen wenn Switch_back_to_Last_Sheet aktiv ist.
        # Wenn Col_from_Sheet = "" ist, dann kann es immer noch passiern
        M30.EndProg()
    Filter__Col = 3
    if Page_ID == r'Selectrix':
        Inp_Typ_Col = 6
    else:
        Inp_Typ_Col = 5
    Ref_Col = Inp_Typ_Col
    Start_V_Col = Ref_Col + 1
    Descrip_Col = Ref_Col + 2
    Dist_Nr_Col = Ref_Col + 3
    Conn_Nr_Col = Ref_Col + 4
    if Has_Macro_and_LanguageName_Column(Sh, Conn_Nr_Col + 1):
        MacIcon_Col = Ref_Col + 5
        LanName_Col = Ref_Col + 6
        Ref_Col = Ref_Col + 2
    else:
        MacIcon_Col = 0
        LanName_Col = 0
    Config__Col = Ref_Col + 5
    LED_Nr__Col = Ref_Col + 6
    LEDs____Col = Ref_Col + 7
    InCnt___Col = Ref_Col + 8
    LocInCh_Col = Ref_Col + 9
    LED_Cha_Col = Ref_Col + 10
    LED_TastCol = Ref_Col + 11
    COMPort_COL = Inp_Typ_Col
    BUILDOP_COL = Descrip_Col
    R_UPLOD_COL = Dist_Nr_Col
    COMPrtR_COL = LanName_Col
    BUILDOpRCOL = Config__Col
    Col_from_Sheet = Sh.Name
    return
    P01.MsgBox(r'Interner Fehler: Die letzte Seite '' + Col_from_Sheet + r'' konnte nicht aktiviert werden', vbCritical, r'Interner Fehler')
    M30.EndProg()

def Get_First_Number_of_Range(Row, Col):
    Addr = Variant()
    #-----------------------------------------------------------------------------
    # Accepts also a address which contains two adressed separated by '-'
    # Example: '1 - 3'
    Addr = Replace(Replace(str(P01.Cells(Row, Col)), vbLf, r''), r' ', r'')
    if Addr == r'':
        fn_return_value = r''
        return fn_return_value
    if InStr(Addr, r'-') > 0:
        Parts = Split(Addr, r'-')
        if UBound(Parts) > 1 or IsNumeric(Parts(0)) == False or IsNumeric(Parts(1)) == False:
            fn_return_value = - 9
        else:
            fn_return_value = Int(P01.val(Parts(0)))
    else:
        if IsNumeric(Addr):
            fn_return_value = Int(P01.val(Addr))
        else:
            fn_return_value = r''
    return fn_return_value

def Get_Address_Col():
    #----------------------------------------
    if Page_ID == r'Selectrix':
        fn_return_value = SX_Channel_Col
    else:
        fn_return_value = DCC_or_CAN_Add_Col
    return fn_return_value

def Get_Address_String(Row):
    s = String()

    AddrCol = int()
    #--------------------------------------------------------
    # Return true if the string in the address/selectrix channel column
    AddrCol = Get_Address_Col()
    fn_return_value = Trim(P01.Cells(Row, AddrCol))
    return fn_return_value

def Address_starts_with_a_Number(Row):
    s = String()
    #-------------------------------------------------------------------
    # Return true if the first character of the address/channel column is a number
    s = Get_Address_String(Row)
    fn_return_value = False
    if s != r'':
        fn_return_value = IsNumeric(Left(s, 1))
    return fn_return_value

# Contains Variables which contain the column numbers for
# the date sheets (DCC/Selectrix)
# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Option Compare Binary ' Use case sensitive compare.
#Only valid if the DCC or CAN Page is active
#Only valid if the Selectrix Page is active
## VB2PY (CheckDirective) VB directive took path 1 on False
