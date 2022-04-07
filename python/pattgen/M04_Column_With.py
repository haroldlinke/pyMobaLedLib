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

"""-----------------------------------------------------------------------------------------------
------------------------------------------
UT------------------------
------------------------------
"""


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: FirstEmptyCol - ByRef 
def __Get_Duration(c, FirstEmptyCol, Values):
    fn_return_value = None
    #-----------------------------------------------------------------------------------------------
    if c.Value == '':
        if FirstEmptyCol == 0:
            FirstEmptyCol = c.Column
        fn_return_value = Values(( c.Column - FirstEmptyCol )  %  ( FirstEmptyCol - Dauer_Col1 ))
    else:
        s = c.Value
        V = Val(s)
        if InStr(s, 'Sec') > 0 or InStr(s, 'Sek') > 0 or InStr(s, 'sec') > 0 or InStr(s, 'sek') > 0:
            V = V * 1000
        elif InStr(s, 'Min') > 0:
            V = V * 60 * 1000
        fn_return_value = V
    return fn_return_value

def Adjust_Column_With_to_Duration():
    FirstLEDsRow = Long()

    LastLEDsRow = Long()

    LastLEDsCol = Long()

    Col = Long()

    ms = Long()

    Min_t = Long()

    Max_t = Long()

    Values = vbObjectInitialize(objtype=Long)

    i = Long()

    FirstEmptyCol = Long()

    WasProtected = Boolean()

    Min_Width = Double()

    Max_width = Double()

    Max2Min = Double()

    ScaleF = Double()

    MessageShown = Boolean()
    #------------------------------------------
    FirstLEDsRow = Range(FirstLEDTabRANGE).Row
    LastLEDsRow = FirstLEDsRow + Range(LED_Cnt_Rng) - 1
    #LastLEDsCol = LastFilledColumn(Range(LEDsRANGE), LastLEDsRow) ' Find the last used column
    LastLEDsCol = LastFilledColumn2(Range(LEDsRANGE), LastLEDsRow)
    if LastLEDsCol > Dauer_Col1:
        Values = vbObjectInitialize((LastLEDsCol - Dauer_Col1,), Variant)
        Min_t = 999999
        for Col in vbForRange(Dauer_Col1, LastLEDsCol):
            with_0 = Cells(Dauer_Row, Col)
            ms = __Get_Duration(Cells(Dauer_Row, Col), FirstEmptyCol, Values)
            Values[i] = ms
            i = i + 1
            if ms > Max_t:
                Max_t = ms
            if ms < Min_t:
                Min_t = ms
    if Max_t == Min_t:
        Normal_Column_With()
        return
    if Min_t == 0:
        MsgBox(Get_Language_Str('Error in function \'Adjust_Column_With_to_Duration\' ;-('))
        Normal_Column_With()
        return
    WasProtected = ActiveSheet.ProtectContents
    if WasProtected:
        ActiveSheet.Unprotect()
    #Debug.Print "Max_t / Min_t =  " & Max_t / Min_t 'Debug
    Max2Min = Max_t / Min_t
    if Max2Min < NormWidth_MM:
        Min_Width = NormColWidth
    elif Max2Min > Min_Width_MM:
        Min_Width = Min_ColWidth
    else:
        m = ( NormColWidth - Min_ColWidth )  /  ( NormWidth_MM - Min_Width_MM )
        B = NormColWidth - m * NormWidth_MM
        Min_Width = m * Max2Min + B
    Max_width = Min_Width * Max_t / Min_t
    ScaleF = ( Max_width - Min_Width )  /  ( Max_t - Min_t )
    Application.StatusBar = ''
    i = 0
    for Col in vbForRange(Dauer_Col1, LastLEDsCol):
        with_1 = Cells(Dauer_Row, Col)
        ms = Values(i)
        i = i + 1
        w = ( ms - Min_t )  * ScaleF + Min_Width
        if w > 100:
            w = 100
            if not MessageShown:
                Application.StatusBar = Get_Language_Str('Achtung die Darstellung der Spaltenbreite wurde begrenzt')
            MessageShown = True
        with_1.ColumnWidth = w
    if not MessageShown:
        if Application.StatusBar == Get_Language_Str('Achtung die Darstellung der Spaltenbreite wurde begrenzt'):
            Application.StatusBar = ''
    if WasProtected:
        Protect_Active_Sheet()

def __Test_MaxWidth():
    i = Long()
    #UT------------------------
    with_2 = Cells(1, 7)
    for i in vbForRange(250, 260):
        with_2.ColumnWidth = i

def Normal_Column_With():
    WasProtected = Boolean()

    FirstLEDsRow = Long()

    LastLEDsRow = Long()

    LastLEDsCol = Long()

    Col = Long()
    #------------------------------
    WasProtected = ActiveSheet.ProtectContents
    if WasProtected:
        ActiveSheet.Unprotect()
    FirstLEDsRow = Range(FirstLEDTabRANGE).Row
    LastLEDsRow = FirstLEDsRow + Range(LED_Cnt_Rng) - 1
    #LastLEDsCol = LastFilledColumn(Range(LEDsRANGE), LastLEDsRow) ' Find the last used column
    LastLEDsCol = LastFilledColumn2(Range(LEDsRANGE), LastLEDsRow)
    for Col in vbForRange(Dauer_Col1, LastLEDsCol):
        with_3 = Cells(Dauer_Row, Col)
        if with_3.ColumnWidth != NormColWidth:
            with_3.ColumnWidth = NormColWidth
    if WasProtected:
        Protect_Active_Sheet()

# VB2PY (UntranslatedCode) Option Explicit



