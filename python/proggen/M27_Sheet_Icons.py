# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
# * Author: Harold Linke
# * Date: January 1st, 2020
# * Copyright: Harold Linke 2020
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 10.03.2020 - Harold Linke - first release
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

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from ExcelAPI.XLC_Excel_Consts import *
import proggen.M02_Public as M02
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
import proggen.M25_Columns as M25
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
import proggen.Prog_Generator as PG

# fromx ExcelAPI.X02_Workbook import *
import ExcelAPI.XLW_Workbook as P01


""" ToDo: Untersuchen wie das bei anderen Skaliereungen aussieht
       - Excel          O.K.
       - Windows
"""

__Icon_Size = 11
__Icon_Ext = '.bmp'
__Icon_Left = 2
__Icon_Top = 1

def __Icon_Path():
    fn_return_value = None
    #-------------------------------------
    fn_return_value = PG.ThisWorkbook.pyProgPath + '/icons/'
    return fn_return_value

def Add_Icon(Name, Row, Sh=None):
    #r = Range()

    #Pic = Variant()
    
    iconfilename = __Icon_Path() + Name + __Icon_Ext
    
    #-------------------------------------------------------------------------
    M25.Make_sure_that_Col_Variables_match(Sh)
    if Sh is None:
        Sh = P01.ActiveSheet
    if M25.MacIcon_Col <= 0:
        return
    #if Sh.Columns(M25.MacIcon_Col).Hidden:
    #    return
    Sh.Cells(Row,M25.MacIcon_Col).set_value({"Icon" : iconfilename})
    
    return #*HL

    # VB2PY (UntranslatedCode) On Error GoTo ErrProc
    Pic = Sh.Pictures.Insert(__Icon_Path() + Name + __Icon_Ext)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    with_0 = Pic
    with_0.Locked = True
    with_0.Placement = xlMoveAndSize
    with_1 = with_0.ShapeRange
    if with_1.Width > with_1.Height:
        with_1.Width = __Icon_Size
    else:
        with_1.Height = __Icon_Size
    with_1.Left = Sh.Cells(Row, M25.MacIcon_Col).Left + __Icon_Left +  ( __Icon_Size - with_1.Width )  / 2
    with_1.Top = Sh.Cells(Row, M25.MacIcon_Col).Top + __Icon_Top
    with_0.OnAction = 'SelectMacros_from_Icon'
    return

def __Test_Add_Icon():
    #UT------------------------
    Add_Icon('Ampel', 10)
    Add_Icon('BlueLight', 11)
    Add_Icon('Andreaskreuz', 12)

def Del_Icons(r):
    return #*HL
    Pic = Variant()

    MinTop = Double()

    MaxTop = Double()

    MinLeft = Double()

    MaxLeft = Double()

    #Sh = P01.Worksheet
    #--------------------------------
    Sh = r.Parent
    with_2 = Sh
    MinTop = r.Top
    MaxTop = MinTop + r.Height
    MinLeft = r.Left
    MaxLeft = MinLeft + r.Width
    for Pic in with_2.Shapes.shapelist:
        if Pic.Top > MinTop and Pic.Top < MaxTop and Pic.Left >= MinLeft and Pic.Left <= MaxLeft:
            Pic.Delete()

def Del_one_Icon_in_IconCol(Row, Sh=None):
    #----------------------------------------------
    if Sh is None:
        Sh = P01.ActiveSheet
    M25.Make_sure_that_Col_Variables_match(Sh)
    with_3 = Sh
    Del_Icons(with_3.Cells(Row, M25.MacIcon_Col))

def __Test_Del_one_Icon_in_IconCol():
    #UT---------------------------------------
    Add_Icon('Ampel', 10)
    Del_one_Icon_in_IconCol(10)

def __Del_Icons_in_Col(Col, Sh):
    #---------------------------------------------------------
    with_4 = Sh
    Del_Icons(with_4.Range(with_4.Cells(M02.FirstDat_Row, Col), with_4.Cells(M02.MAX_ROWS, Col)))

def __Del_All_Icons_in_TypCol():
    #Sh = P01.Worksheet
    #------------------------------------
    Sh = P01.ActiveSheet
    M25.Make_sure_that_Col_Variables_match(Sh)
    __Del_Icons_in_Col(M25.Inp_Typ_Col, Sh)

def Del_Icons_in_IconCol():
    #Sh = X02.Worksheet
    #--------------------------------
    Sh = P01.ActiveSheet
    M25.Make_sure_that_Col_Variables_match(Sh)
    __Del_Icons_in_Col(M25.MacIcon_Col, Sh)

def __Test_Add_All_Icons():
    File = String()

    Row = int()
    #UT-----------------------------
    Row = 10
    File = Dir(__Icon_Path() + '*' + __Icon_Ext)
    while File != '':
        Add_Icon(M30.FileName(File), Row)
        P01.CellDict[Row, M25.LanName_Col] = M30.FileName(File)
        Row = Row + 1
        File = Dir()

def __Show_Hide_Column_in_Sheet(Show, Col, Sh):
    fn_return_value = None
    #---------------------------------------------------------------------------------------------------
    # Return true if the state has been chenged
    with_5 = Sh.Columns(M30.ColumnLettersFromNr(Col) + ':' + M30.ColumnLettersFromNr(Col)).EntireColumn
    if with_5.Hidden == Show:
        with_5.Hidden = not Show
        fn_return_value = True
    return fn_return_value

def __Hide_Icons_Column_in_Sheet(Sh):
    #------------------------------------------------------
    M25.Make_sure_that_Col_Variables_match(Sh)
    if __Show_Hide_Column_in_Sheet(False, M25.MacIcon_Col, Sh):
        __Del_Icons_in_Col(M25.MacIcon_Col, Sh)

def __Test_Hide_Icons_Column_in_Sheet():
    #UT------------------------------------------
    __Hide_Icons_Column_in_Sheet(P01.ActiveSheet)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: MacroStr - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Row - ByVal 
def FindMacro_and_Add_Icon_and_Name(MacroStr, Row, Sh, NameOnly=False):
    LibMacRow = int()
    #-------------------------------------------------------------------------------------------------------------------------------------
    LibMacRow = M09SM.Find_Macro_in_Lib_Macros_Sheet(MacroStr)
    if LibMacRow > 0:
        M09SM.Add_Icon_and_Name(LibMacRow, Row, Sh, NameOnly=NameOnly)
    else:
        if InStr(MacroStr, 'Pattern') > 0:
            OldEvents = P01.Application.EnableEvents
            P01.Application.EnableEvents = False
            Sh.CellDict[Row, M25.LanName_Col] = M09.Get_Language_Str('Muster') + ' Pattern_Configurator'
            P01.Application.EnableEvents = OldEvents
            if NameOnly == False:
                Del_one_Icon_in_IconCol(Row, Sh)
                Add_Icon('Pattern', Row, Sh)

def __Show_Icons_Column_in_Sheet(Sh):
    OldUpdating = Boolean()
    #------------------------------------------------------
    OldUpdating = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = False
    M25.Make_sure_that_Col_Variables_match(Sh)
    if __Show_Hide_Column_in_Sheet(True, M25.MacIcon_Col, Sh):
        for Row in vbForRange(M02.FirstDat_Row,M30.LastUsedRowIn(Sh)):
            s = Sh.Cells(Row, M25.Config__Col)
            if s != '':
                FindMacro_and_Add_Icon_and_Name(s, Row, Sh)
    P01.Application.ScreenUpdating = OldUpdating

def __Test_Show_Icons_Column_in_Sheet():
    #UT------------------------------------------
    __Show_Icons_Column_in_Sheet(P01.ActiveSheet)

def __Show_Hide_Icons_Column(Show):
    Sh = None
    #--------------------------------------------------
    for Sh in PG.ThisWorkbook.Sheets:
        if M28.Is_Data_Sheet(Sh):
            M25.Make_sure_that_Col_Variables_match(Sh)
            if Show:
                __Show_Icons_Column_in_Sheet(Sh)
            else:
                __Hide_Icons_Column_in_Sheet(Sh)

def __Update_Language_Name_Column_in_Sheet(Sh):
    OldUpdating = Boolean()

    Row = int()
    #----------------------------------------------------------------
    OldUpdating = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = False
    M25.Make_sure_that_Col_Variables_match(Sh)
    #If Show_Hide_Column_in_Sheet(True, LanName_Col, Sh) Then
    for Row in vbForRange(M02.FirstDat_Row, M30.LastUsedRowIn(Sh)):
        s = Sh.Cells(Row, M25.Config__Col)
        if s != '':
            FindMacro_and_Add_Icon_and_Name(s, Row, Sh, NameOnly=True)
    #End If
    P01.Application.ScreenUpdating = OldUpdating

def __Test_Update_Language_Name_Column_in_Sheet():
    #UT----------------------------------------------------
    __Update_Language_Name_Column_in_Sheet(P01.ActiveSheet)

def Update_Language_Name_Column_in_all_Sheets():
    Sh = None # P01.Worksheet

    Col = int()

    OldUpdating = Boolean()
    #-----------------------------------------------------
    OldUpdating = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = False
    for Sh in PG.ThisWorkbook.Sheets:
        if M28.Is_Data_Sheet(Sh):
            __Update_Language_Name_Column_in_Sheet(Sh)
    P01.Application.ScreenUpdating = OldUpdating

def SelectMacros_from_Icon():
    Button = Object()

    Row = int()

    Top = Double()
    #----------------------------------
    M25.Make_sure_that_Col_Variables_match()
    # VB2PY (UntranslatedCode) On Error GoTo NotFound
    Button = P01.ActiveSheet.get_Shape(P01.Application.caller)
    Top = Button.Top
    for Row in vbForRange(M30.LastUsedRow(), M02.FirstDat_Row, - 1):
        if P01.Cells(Row, 1).Top < Top:
            P01.Cells(Row, M25.MacIcon_Col).Select()
            M09SM.SelectMacros()
            return

def __Test_Hide_MacIcon_Column():
    Show_Hide_Column_in_all_Sheets(0, 'MacIcon_Col')

def __Test_Show_MacIcon_Column():
    Show_Hide_Column_in_all_Sheets(1, 'MacIcon_Col')

def __Test_Hide_LanName_Column():
    Show_Hide_Column_in_all_Sheets(0, 'LanName_Col')

def __Test_Show_LanName_Column():
    Show_Hide_Column_in_all_Sheets(1, 'LanName_Col')

def __Test_Hide_Config__Column():
    Show_Hide_Column_in_all_Sheets(0, 'Config__Col')

def __Test_Show_Config__Column():
    Show_Hide_Column_in_all_Sheets(1, 'Config__Col')

def Show_Hide_Column_in_all_Sheets(Show, ColName):
    #----------------------------------------------------------------------------
    if ColName == 'MacIcon_Col':
        M30.ShowHourGlassCursor(True)
        __Show_Hide_Icons_Column(Show)
        M30.ShowHourGlassCursor(False)
    else:
        for Sh in PG.ThisWorkbook.Sheets:
            if M28.Is_Data_Sheet(Sh):
                M25.Make_sure_that_Col_Variables_match(Sh)
                if (ColName == 'LanName_Col'):
                    Col = M25.LanName_Col
                elif (ColName == 'Config__Col'):
                    Col = M25.Config__Col
                else:
                    P01.MsgBox('Unknown ColName: \'' + ColName + '\'', vbCritical, 'Internal Error')
                    Stop()
                __Show_Hide_Column_in_Sheet()(Show, Col, Sh)

# VB2PY (UntranslatedCode) Option Explicit

