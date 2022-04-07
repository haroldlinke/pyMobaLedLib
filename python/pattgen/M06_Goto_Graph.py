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


Goto_Start_Points = Long()

def Delete_Goto_Graph():
    WasProtected = Boolean()

    o = Variant()
    #-----------------------------
    WasProtected = ActiveSheet.ProtectContents
    if WasProtected:
        ActiveSheet.Unprotect()
    for o in ActiveSheet.Shapes:
        if Left(o.Name, Len('Goto_Graph')) == 'Goto_Graph':
            o.Delete()
    if WasProtected:
        Protect_Active_Sheet()

def __Draw_GotoArrowXY(X1, X2, y, h, Color):
    o = Variant()
    #------------------------------------------------------------------------------------------------------
    # Draw a curved arrow from x1, y to x2, y.
    # h defines the height. Positive numbers draw the arrow below y, negative above y
    # http://www.herber.de/mailing/vb/html/xlobjfreeformbuilder.htm
    with_0 = ActiveSheet
    with_1 = with_0.Shapes.BuildFreeform(msoEditingCorner, X1, y)
    #                                             Richt1   Richt2    Ende
    with_1.AddNodes(msoSegmentCurve, msoEditingCorner, X1, y, ( X1 + X2 )  / 2, y + 2 * h, X2, y)
    o = with_1.ConvertToShape
    #.Shapes (.Shapes.Count) ' Debug
    with_2 = o
    with_3 = with_2.Line
    with_3.EndArrowheadStyle = msoArrowheadTriangle
    with_3.ForeColor.rgb = Color
    with_2.Name = 'Goto_Graph_CurvedArrow' + ActiveSheet.Shapes.Count

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: r1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: r2 - ByVal 
def __Draw_GotoArrow(r1, r2, h, Color):
    #-----------------------------------------------------------------------------------------
    if r1 != r2:
        __Draw_GotoArrowXY(r1.Left + r1.Width * 0.5, r2.Left + r2.Width * 0.5, r1.Top + r1.Height, h, Color)
    else:
        __Draw_GotoArrowXY(r1.Left + r1.Width * 0.3, r2.Left + r2.Width * 0.7, r1.Top + r1.Height, h, rgb(255, 0, 0))

def __Test_Draw_GotoArrow():
    #UT------------------------------
    #Delete_Goto_Graph
    #Draw_GotoArrowXY 100, 200, 100, 50, rgb(255, 0, 0)
    __Draw_GotoArrow(ActiveCell, ActiveCell.offset(0, 2), 60, rgb(0, 0, 255))

def __Draw_StraitArrow(r, Txt, h, dx, Dir, Color):
    tdx = - 10

    tdy = - 16

    th = 72

    x = Double()

    y = Double()

    x0 = Double()

    y0 = Double()

    o = Variant()
    #----------------------------------------------------------------------------------------------------------------------
    if Dir() == 1:
        x = r.Left + r.Width * 0.3
    else:
        x = r.Left + r.Width * 0.7
    y = r.Top
    x0 = x - dx
    y0 = y - h
    with_4 = ActiveSheet.Shapes.AddConnector(msoConnectorStraight, x0, y0, x, y)
    if Dir() == 1:
        with_4.Line.EndArrowheadStyle = msoArrowheadStealth
    else:
        with_4.Line.BeginArrowheadStyle = msoArrowheadStealth
    with_4.Line.ForeColor.rgb = Color
    with_4.Name = 'Goto_Graph_Arrow' + ActiveSheet.Shapes.Count
    with_5 = ActiveSheet.Shapes.AddLabel(msoTextOrientationHorizontal, x0 + tdx, y0 + tdy, 40, th)
    with_5.TextFrame2.TextRange.Characters.Text = Txt
    with_5.Name = 'Goto_Graph_Label' + ActiveSheet.Shapes.Count

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: r - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByVal 
def __Draw_StartArrow(r, Txt):
    #-----------------------------------------------------------------
    __Draw_StraitArrow(r, Txt, 30, 10, 1, rgb(0, 128, 0))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: r - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByVal 
def __Draw_EndArrow(r, Txt):
    #---------------------------------------------------------------
    __Draw_StraitArrow(r, Txt, 17, - 10, - 1, rgb(128, 0, 0))

def __Test_Draw_StartArrow():
    #UT-------------------------------
    Delete_Goto_Graph()
    __Draw_StartArrow(ActiveCell, '7')
    __Draw_EndArrow(ActiveCell, 'E')
    ActiveCell.Select()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: GotoArrowTab - ByVal 
def __Draw_GotoArrowTab(GotoArrowTab, LastCol):
    MaxH = Double()

    GNr = Long()

    ArrowTabEntry = Variant()

    ArrTabArr = vbObjectInitialize(objtype=String)
    #-------------------------------------------------------------------
    # Draw the Goto arrows
    MaxH = Cells(GoTo_Row + 1, 1).Height * 0.8
    ArrTabArr = Split(GotoArrowTab, ' ')
    for ArrowTabEntry in ArrTabArr:
        Cols = Split(ArrowTabEntry, ',')
        GNr = GNr + 1
        if UBound(Cols) == 2:
            h = MaxH * Cols(2)
        else:
            h = MaxH * GNr /  ( UBound(ArrTabArr) + 1 ) 
        if Val(Cols(1)) <= LastCol:
            Color = rgb(0, 0, 255)
        else:
            Color = rgb(255, 153, 0)
        __Draw_GotoArrow(Cells(GoTo_Row, Val(Cols(0))), Cells(GoTo_Row, Val(Cols(1))), h, Color)

def Goto_Mode_is_Active():
    fn_return_value = None
    #-----------------------------------------------
    fn_return_value = ThisWorkbook.ActiveSheet.Range('Goto_Mode') == '1'
    return fn_return_value

def Draw_All_Arrows():
    WasProtected = Boolean()

    OldScrUpd = Boolean()

    LastCol = Long()

    GotoCells = Range()

    c = Variant()

    V = String()

    SNr = Long()

    GotoArrowTab = String()

    LastLEDsCol = Long()

    LastLEDsRow = Long()

    FirstLEDsRow = Long()
    #---------------------------
    WasProtected = ActiveSheet.ProtectContents
    if WasProtected:
        ActiveSheet.Unprotect()
    OldScrUpd = Application.ScreenUpdating
    Application.ScreenUpdating = False
    Delete_Goto_Graph()
    Goto_Start_Points = 0
    if Goto_Mode_is_Active() == False:
        return
    Calc_Reachable_Columns()
    FirstLEDsRow = Range(FirstLEDTabRANGE).Row
    LastLEDsRow = FirstLEDsRow + Range(LED_Cnt_Rng) - 1
    #LastLEDsCol = LastFilledColumn(Range(LEDsRANGE), LastLEDsRow) ' Find the last used column
    LastLEDsCol = LastFilledColumn2(Range(LEDsRANGE), LastLEDsRow)
    LastCol = LastUsedColumnInRow(ActiveSheet, GoTo_Row)
    if LastLEDsCol > LastCol:
        LastCol = LastLEDsCol
    if LastCol >= GoTo_Col1:
        GotoCells = Range(Cells(GoTo_Row, GoTo_Col1), Cells(GoTo_Row, LastCol))
        for c in GotoCells:
            V = UCase(c)
            if SNr == 0 or InStr(V, 'S') > 0:
                __Draw_StartArrow(c, SNr)
                SNr = SNr + 1
            Goto_Start_Points = SNr
            if InStr(V, 'E') > 0 and Reachable_Col(c.Column - GoTo_Col1) > 0:
                __Draw_EndArrow(c, 'E')
            # Fill the GotoArrowTab list
            if InStr(V, 'G') > 0 and Reachable_Col(c.Column - GoTo_Col1) > 0:
                p = Get_Number_from_Str(V)
                if p > 0:
                    if InStr(PosList, ' ' + p + ' ') > 0:
                        GotoArrowTab = GotoArrowTab + c.Column + ',' + PosColArray(p - 1) + ' '
                    else:
                        GotoArrowTab = GotoArrowTab + c.Column + ',' + LastCol + 1 + ' '
        # Draw the Goto arrows
        if GotoArrowTab != '':
            List_w_Height = Calc_Height_GotoArrow(Left(GotoArrowTab, Len(GotoArrowTab) - 1))
            __Draw_GotoArrowTab(List_w_Height, LastCol)
    if WasProtected:
        Protect_Active_Sheet()
    Application.ScreenUpdating = OldScrUpd

def __Move_Add_Del_Col_Buttons():
    o = Variant()

    y = Double()
    #-------------------------------------
    # The buttons have to be moved if the height of the column is changed
    y = Rows(GoTo_Row + 1).Top + Rows(GoTo_Row + 1).Height
    for o in ActiveSheet.Shapes:
        if o.AlternativeText == 'Add_Del_Button':
            o.Top = y - o.Height - 2

def Hide_Show_GotoLines(Hide, Resize_And_Move_Buttons=True):
    #--------------------------------------------------------------------------------------------------
    if Rows(GoTo_Row + ':' + GoTo_Row).EntireRow.Hidden != Hide:
        WasProtected = ActiveSheet.ProtectContents
        if WasProtected:
            ActiveSheet.Unprotect()
        Rows[GoTo_Row + ':' + GoTo_Row].EntireRow.Hidden = Hide
        if Resize_And_Move_Buttons:
            if Hide:
                Rows[GoTo_Row - 1].RowHeight = 12
                Rows[GoTo_Row + 1].RowHeight = 15
            else:
                Rows[GoTo_Row - 1].RowHeight = 60
                Rows[GoTo_Row + 1].RowHeight = 60
            __Move_Add_Del_Col_Buttons()
        if WasProtected:
            Protect_Active_Sheet()

def __Test_Hide_Show_GotoLines():
    #UT-----------------------------------
    Hide_Show_GotoLines(not Rows(GoTo_Row + ':' + GoTo_Row + 1).EntireRow.Hidden)

def Hide_Show_GotoLines_If_Enabled():
    #------------------------------------------
    Hide_Show_GotoLines(not Goto_Mode_is_Active())

def __Hide_Show_Special_ModeLines(Hide):
    #-------------------------------------------------------
    if Range('RGB_Modul_Nr').EntireRow.Hidden != Hide:
        WasProtected = ActiveSheet.ProtectContents
        if WasProtected:
            ActiveSheet.Unprotect()
        Range[Range('RGB_Modul_Nr'), Range('Analog_Inputs')].EntireRow.Hidden = Hide
        ActiveSheet.Send2Module_Button.Visible = not Hide
        ActiveSheet.Send2Module_Button.Enabled = not Hide
        ActiveSheet.Prog_Generator_Button.Visible = Hide
        ActiveSheet.Prog_Generator_Button.Enabled = Hide
        if WasProtected:
            Protect_Active_Sheet()

def __Test_Hide_Show_Special_ModeLines():
    #UT-------------------------------------------
    __Hide_Show_Special_ModeLines(not Range('RGB_Modul_Nr').EntireRow.Hidden)

def __Special_Mode_is_Active():
    fn_return_value = None
    Special_Mode = String()

    OldEvents = Boolean()
    #---------------------------------------------------
    Special_Mode = ThisWorkbook.ActiveSheet.Range('Special_Mode')
    OldEvents = Application.EnableEvents
    Application.EnableEvents = False
    select_0 = UCase(Left(Special_Mode, 1))
    if (select_0 == 'C'):
        if Left(Special_Mode, Len('Charlieplexing')) != 'Charlieplexing':
            ThisWorkbook.ActiveSheet.Range['Special_Mode'] = 'Charlieplexing V2'
            # Correct the active cell. It shold be the next line and not the line after the hidden range
            if ActiveCell.Address == Range('Analog_Inputs').offset(1, 0).Address:
                Range('Special_Mode').offset(1, 0).Select()
        fn_return_value = True
    Application.EnableEvents = OldEvents
    return fn_return_value

def Hide_Show_Special_ModeLines_If_Enabled():
    #--------------------------------------------------
    __Hide_Show_Special_ModeLines(not __Special_Mode_is_Active())
    #  If Not Special_Mode_is_Active() Then ' Prevent that a hidden cell is selected
    #     If ActiveCell.Address = Range("RGB_Modul_Nr").Address Then Range("Analog_Inputs").offset(1, 0).Select
    #  End If

# VB2PY (UntranslatedCode) Option Explicit