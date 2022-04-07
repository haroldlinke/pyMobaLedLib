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

import proggen.M02_Public as M02
import proggen.M02_global_variables as M02GV
import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
import proggen.M09_SelectMacro_Treeview as M09SMT
import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80


import proggen.Prog_Generator as PG

import ExcelAPI.P01_Workbook as P01

from ExcelAPI.X01_Excel_Consts import *

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

""" Example from
  - http://www.herber.de/forum/archiv/1124to1128/1126102_GetKeyState_Taste_abfragen.html
    http://www.herber.de/bbs/user/66853.xls
  - https://stackoverflow.com/questions/47271141/vba-get-cursor-position-as-cell-address
 https://stackoverflow.com/questions/20269844/api-timers-in-vba-how-to-make-safe
# VB2PY (CheckDirective) VB directive took path 1 on VBA7 And Win64
 Use LongLong and LongPtr
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
 Create custom variable that holds two integers
 https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
--------------------------------
---------------------------------------
----------------------------------------------------
-------------------------------------------------------
--------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------
"""

#*HL __hTimer = LongPtr()
VK_SHIFT = 0x10
VK_CONTROL = 0x11
class POINTAPI:
    def __init__(self):
        self.Xcoord = Long()
        self.Ycoord = Long()

__VK_LBUTTON = 0x1
__VK_RBUTTON = 0x2
__VK_MBUTTON = 0x4
__VK_UP = 0x26
__VK_DOWN = 0x28
__VK_RETURN = 0xD
__VK_ESCAPE = 0x1B
__LeftMousePressed = Boolean()
__ESCButtonPressed = Boolean()
__EnterKey_Pressed = Boolean()
__LastRow = Long()
__Col1 = Long()
__ColN = Long()

def __MouseCheckTimerProc():
    global __LeftMousePressed
    Result = Variant()
    #--------------------------------
    KillTimer(0, __hTimer)
    Result = P01.GetAsyncKeyState(__VK_LBUTTON)
    if Result != 0:
        __LeftMousePressed = True
    __hTimer = SetTimer(0, 0, 50, AddressOf(__MouseCheckTimerProc))

def __Show_Insert_Pos(Row):
    #---------------------------------------
    if Row > 0:
        with_0 = P01.Range(P01.Cells(Row, __Col1), P01.Cells(Row, __ColN)).Borders(xlEdgeTop)
        with_0.ThemeColor = 10
        with_0.TintAndShade = - 0.249977111117893
        with_0.Weight = xlThick

def __Normal_Line(Sh, Row):
    #----------------------------------------------------
    with_1 = Sh
    with_2 = with_1.Range(with_1.Cells(Row, __Col1), with_1.Cells(Row, __ColN)).Borders(xlEdgeTop)
    with_2.ColorIndex = 0
    with_2.TintAndShade = 0
    with_2.Weight = xlThin

def __GetRange(X, Y):
    fn_return_value = None
    #-------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error Resume Next
    fn_return_value = P01.ActiveWindow.RangeFromPoint(X, Y)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return fn_return_value



def __Show_InsertLine_until_Mousepressed(MinRow, SheetName):
    global __ESCButtonPressed,__EnterKey_Pressed
    fn_return_value = None
    llCoord = POINTAPI()

    #rng = Range()

    MoveByKey = Boolean()

    Row = Long()
    #--------------------------------------------------------------------------------------------------
    P01.GetCursorPos(llCoord)
    #Debug.print "X Position: " & llCoord.Xcoord & vbNewLine & "Y Position: " & llCoord.Ycoord ' Display the cursor position coordinates
    P01.DoEvents()
    if P01.GetAsyncKeyState(__VK_ESCAPE) != 0:
        __ESCButtonPressed = True
    if P01.GetAsyncKeyState(__VK_UP) != 0:
        MoveByKey = True
    if P01.GetAsyncKeyState(__VK_DOWN) != 0:
        MoveByKey = True
    if P01.GetAsyncKeyState(__VK_RETURN) != 0:
        __EnterKey_Pressed = True
    if MoveByKey:
        P01.SetCursorPos(P01.ActiveWindow.ActivePane.PointsToScreenPixelsX(ActiveCell.Left +  ( ActiveCell.Width / 2 )), ActiveWindow.ActivePane.PointsToScreenPixelsY(ActiveCell.Top +  ( ActiveCell.Height / 2 )))
        rng = P01.ActiveCell()
    else:
        rng = __GetRange(llCoord.Xcoord, llCoord.Ycoord)
    if not rng is None:
        Row = rng.Row
        if Row < MinRow:
            Row = MinRow
    if ( Row != 0 and Row != __LastRow )  or __LeftMousePressed or __EnterKey_Pressed or __ESCButtonPressed:
        OldUpdating = P01.Application.ScreenUpdating
        P01.Application.ScreenUpdating = False
        if __LastRow > 0:
            __Normal_Line(P01.Sheets(SheetName), __LastRow)
        if Row != 0:
            __LastRow = Row
        if __LeftMousePressed or __EnterKey_Pressed or __ESCButtonPressed or SheetName != P01.ActiveSheet().Name:
            fn_return_value = True
        else:
            __Show_Insert_Pos(Row)
        P01.Application.ScreenUpdating = OldUpdating
    return fn_return_value

def Select_Move_Dest_by_Mouse(FirstCol, LastCol):
    global __Col1,__ColN, __hTimer, __LeftMousePressed, __EnterKey_Pressed, __ESCButtonPressed
    fn_return_value = 0
    ShName = String()
    #-----------------------------------------------------------------------------------
    # End when Left Mouse, Enter or ESC is pressed
    # Return the destination Row
    # Return 0 if aborted with ESC
    #
    __Col1 = FirstCol
    __ColN = LastCol
    #__hTimer = SetTimer(0, 0, 50, AddressOf(__MouseCheckTimerProc))
    __LeftMousePressed = False
    __EnterKey_Pressed = False
    __ESCButtonPressed = False
    ShName = P01.ActiveSheet.Name
    ShName.EnableMousePosition()
    while __Show_InsertLine_until_Mousepressed(M02.FirstDat_Row, ShName) == False:
        pass
    #M30.KillTimer(0, __hTimer)
    if P01.ActiveSheet.Name == ShName and  ( __LeftMousePressed or __EnterKey_Pressed ) :
        fn_return_value = __LastRow
    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function SetTimer Lib "user32" (ByVal hwnd As LongPtr, ByVal nIDEvent As LongPtr, ByVal uElapse As LongLong, ByVal lpTimerFunc As LongPtr) As LongLong
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function KillTimer Lib "user32" (ByVal hwnd As LongPtr, ByVal nIDEvent As LongPtr) As LongLong
# VB2PY (UntranslatedCode) Public Declare PtrSafe Function GetAsyncKeyState Lib "user32" (ByVal vKey As Long) As Integer
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function GetCursorPos Lib "user32" (lpPoint As POINTAPI) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function SetCursorPos Lib "user32" (ByVal X As Long, ByVal Y As Long) As Long

