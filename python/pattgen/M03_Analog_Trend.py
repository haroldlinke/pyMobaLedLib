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

"""------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------
--------------------------
-------------------------------------------------------
-----------------------------------------------------------------
 Anzeige im GoTo-Mode:
 ~~~~~~~~~~~~~~~~~~~~~
 Wenn der GoTo Mode aktiviert ist, und "Analoges Überblenden" = X ist,
 dann hängt das Bild von der GotoZeile (GoTo_Row) ab.
 Wenn die entsprechende Spalte angesprungen werden kann, dann hängt
 die Start Helligkeit von der ltzen Spalte ab. Zur darstellung werden
 zwei überlagerte Dreiecke verwendet. Das eine kommt von 0, das andere von 100%
 Folgende Einträge in der GoTo Tabelle markieren eine Spalte welche angesprungen
 werden kann:
  - Erste Spalte
  - 'S' = Startsplate
  - 'P' = Position für Goto

 Besonderheit:
 Wenn die vorangegangene Spalte ein 'E' enthält, und die aktuelle Spalte
 keine Startspalte ist, dann kann sie nicht angesprungen werden.
 => Hier wird nichts angezeigt
-------------------------------------------------------------
---------------------------------------
--------------------------------------------------
--------------------------------------------------------------------------------------------------------
----------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on 1
--------------------------------------
--------------------------------------
UT------------------------------------------
------------------------------------
--------------------------------------------------------------------
--------------------------------------
"""

__Is_Reachable = 1
__Is_Goto1_Col = 2
__Is_Start_Col = 10
Reachable_Col = vbObjectInitialize(objtype=Integer)
Came_From_Col = vbObjectInitialize(objtype=Integer)
PosColArray = vbObjectInitialize(objtype=Long)
PosList = String()
__Debug_Reachable = False

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: h1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: h2 - ByVal 
def __Draw_Analog_Trend(c, h1, h2, rgb, Transparency=0.5):
    X1 = Double()

    y0 = Double()

    X2 = Double()

    Y1 = Double()

    Y2 = Double()
    #------------------------------------------------------------------------------------------------------------------------------------
    if h1 == 0 and h2 == 0:
        return
    with_0 = c
    if h1 == h2:
        if h1 * with_0.Height < 1:
            h1 = 1 / with_0.Height
            # Make small rects visible
        if h2 * with_0.Height < 1:
            h2 = 1 / with_0.Height
    else:
        if h1 > h2:
            if h1 * with_0.Height < 1:
                h1 = 1 / with_0.Height
                # Make small triangles visible
        else:
            if h2 * with_0.Height < 1:
                h2 = 1 / with_0.Height
    X1 = with_0.Left
    y0 = with_0.Top + with_0.Height
    X2 = with_0.Left + with_0.Width
    Y1 = with_0.Top + with_0.Height *  ( 1 - h2 )
    Y2 = with_0.Top + with_0.Height *  ( 1 - h1 )
    with_1 = ActiveSheet.Shapes.BuildFreeform(msoEditingAuto, X1, y0)
    with_1.AddNodes(msoSegmentLine, msoEditingAuto, X2, y0)
    with_1.AddNodes(msoSegmentLine, msoEditingAuto, X2, Y1)
    with_1.AddNodes(msoSegmentLine, msoEditingAuto, X1, Y2)
    with_1.ConvertToShape.Select()
    with_2 = Selection.ShapeRange
    with_2.Line.Visible = msoFalse
    with_2.Name = 'Analog_Trend'
    with_3 = with_2.Fill
    with_3.ForeColor.rgb = rgb
    with_3.Transparency = Transparency
    Selection.OnAction = '\'Click_TrendGrafik "' + c.Row + ' ' + c.Column + '"\''

def __Get_Avg_LED_Raw(r, MaxVal):
    fn_return_value = None
    c = Variant()

    Val = Double()
    #--------------------------------------------------------------------------
    for c in r:
        Val = Val + Get_LED_Val(c, MaxVal)
    fn_return_value = Val / r.Count
    return fn_return_value

def __Check_WertMinMaxValid():
    #--------------------------
    if ActiveSheet.Name != WertMinMaxValid:
        WertMinMaxValid = ActiveSheet.Name
        if Range(BitsVal_Rng) < 8:
            WertMin = Range(WertMin_Rng)
            WertMax = Range(WertMax_Rng)
        else:
            WertMin = 0
            WertMax = 255
        BitsVal = ( 2 ** Range(BitsVal_Rng) )  - 1
        LED_Scale = ( WertMax - WertMin )  / BitsVal
        LED_Offset = WertMin
        StartMax = WertMax / 255
        StartMin = WertMin / 255

def __Get_Avg_LED_Val(r):
    fn_return_value = None
    #-------------------------------------------------------
    fn_return_value = __Get_Avg_LED_Raw(r, BitsVal) * LED_Scale + LED_Offset
    return fn_return_value

def __Color_to_RGBColor(colorVal):
    fn_return_value = None
    #-----------------------------------------------------------------
    # Convert a color given as a long number to a MsoRGBType
    fn_return_value = rgb(( colorVal % 256 ), ( ( colorVal // 256 )  % 256 ), ( colorVal // 65536 ))
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: c - ByVal 
def Get_Number_from_Str(c):
    fn_return_value = None
    NrStr = String()

    i = Long()
    #-------------------------------------------------------------
    for i in vbForRange(1, Len(c)):
        if IsNumeric(Mid(c, i, 1)):
            NrStr = NrStr + Mid(c, i, 1)
        else:
            if NrStr != '':
                break
                # First not numeric character after prior numeric characters
    if NrStr == '':
        fn_return_value = - 1
    else:
        fn_return_value = Val(NrStr)
    return fn_return_value

def __Update_Following(r):
    c = Variant()

    Val = String()
    #---------------------------------------
    for c in r:
        Val = UCase(c.offset(0, - 1))
        if Reachable_Col(c.Column - GoTo_Col1) > 0 or InStr(Val, 'G') > 0 or InStr(Val, 'E') > 0:
            break
        Reachable_Col[c.Column - GoTo_Col1] = __Is_Reachable
        ## VB2PY (CheckDirective) VB directive took path 1 on Debug_Reachable
        c.offset[1, 0].Value = c.offset(1, 0).Value + '+'

def Calc_Reachable_Columns():
    fn_return_value = None
    c = Variant()

    LastCol = Long()

    i = Long()

    GotoCells = Range()

    Val = String()

    PosCnt = Long()

    FirstLEDsRow = Long()

    LastLEDsRow = Long()

    LastLEDsCol = Long()

    ArraySize = Long()

    OldEvents = Boolean()

    Updated = Boolean()
    #--------------------------------------------------
    # Generate an array which contains marks for all reachable columns
    # A column is reachable if
    # - it's the first column
    # - it's marked with 'S' = Startcolumn
    # - prior columns are reachable and don't contain an 'G'= Goto or 'E' = End
    # - it contains a 'P' which is reached from a reachable column
    # Returns True if array Reachable_Col id valid
    FirstLEDsRow = Range(FirstLEDTabRANGE).Row
    LastLEDsRow = FirstLEDsRow + Range(LED_Cnt_Rng) - 1
    #LastLEDsCol = LastFilledColumn(Range(LEDsRANGE), LastLEDsRow) ' Find the last used column
    LastLEDsCol = LastFilledColumn2(Range(LEDsRANGE), LastLEDsRow)
    LastCol = LastUsedColumnInRow(ActiveSheet, GoTo_Row)
    if LastLEDsCol > LastCol:
        LastCol = LastLEDsCol
    ArraySize = LastCol - GoTo_Col1 + 1
    if ArraySize <= 0:
        return fn_return_value
    Reachable_Col = vbObjectInitialize((ArraySize,), Variant)
    Came_From_Col = vbObjectInitialize((ArraySize,), Variant)
    if not Goto_Mode_is_Active():
        for i in vbForRange(0, ArraySize):
            Reachable_Col[i] = __Is_Reachable
        fn_return_value = True
        return fn_return_value
    ## VB2PY (CheckDirective) VB directive took path 1 on Debug_Reachable
    OldEvents = Application.EnableEvents
    Application.EnableEvents = False
    PosList = ' '
    GotoCells = Range(Cells(GoTo_Row, GoTo_Col1), Cells(GoTo_Row, LastCol))
    for c in GotoCells:
        Val = UCase(c)
        if InStr(Val, 'P') > 0:
            PosColArray = vbObjectInitialize((PosCnt + 1,), Variant, PosColArray)
            PosColArray[PosCnt] = c.Column
            PosCnt = PosCnt + 1
            PosList = PosList + PosCnt + ' '
        if i == 0 or InStr(Val, 'S') > 0:
            Reachable_Col[i] = __Is_Start_Col
        else:
            PriorGotoVal = UCase(Cells(GoTo_Row, c.Column - 1))
            if Reachable_Col(i - 1) > 0:
                if InStr(PriorGotoVal, 'G') == 0 and InStr(PriorGotoVal, 'E') == 0:
                    Reachable_Col[i] = __Is_Reachable
        ## VB2PY (CheckDirective) VB directive took path 1 on Debug_Reachable
        with_4 = Cells(GoTo_Row + 1, c.Column)
        if Reachable_Col(i) > 0:
            with_4.Value = 'r'
        else:
            with_4.Value = ''
        i = i + 1
    # Check the goto entries
    while 1:
        i = 0
        Updated = False
        for c in GotoCells:
            Val = UCase(c)
            if Reachable_Col(i) > 0:
                if InStr(Val, 'G') > 0:
                    p = Get_Number_from_Str(Val)
                    if p > 0 and InStr(PosList, ' ' + p + ' ') > 0:
                        ArrayPos = PosColArray(p - 1) - GoTo_Col1
                        if Reachable_Col(ArrayPos) == 0:
                            Updated = True
                            if PosColArray(p - 1) + 1 <= LastCol:
                                __Update_Following(Range(Cells(GoTo_Row, PosColArray(p - 1) + 1), Cells(GoTo_Row, LastCol)))
                            Reachable_Col[ArrayPos] = __Is_Goto1_Col
                            Came_From_Col[ArrayPos] = c.Column
                            ## VB2PY (CheckDirective) VB directive took path 1 on Debug_Reachable
                            Cells[GoTo_Row + 1, PosColArray(p - 1)] = 'G1'
                        else:
                            if Came_From_Col(ArrayPos) != c.Column:
                                Reachable_Col[ArrayPos] = __Is_Start_Col
                                ## VB2PY (CheckDirective) VB directive took path 1 on Debug_Reachable
                                Cells[GoTo_Row + 1, PosColArray(p - 1)] = 'R'
            i = i + 1
        if Updated == False:
            break
    ## VB2PY (CheckDirective) VB directive took path 1 on Debug_Reachable
    # Debug Check Reachable_Col()
    i = 0
    for c in GotoCells:
        if ( Reachable_Col(i) > 0 )  !=  ( c.offset(1, 0) != '' ) :
            c.offset(1, 0).Select()
            MsgBox('Error Reachable_Col(' + i + ') <> Debug Line (See selected cell)')
        if Reachable_Col(i) == __Is_Start_Col:
            c.offset[1, 0].Value = 'S' + c.offset(1, 0).Value
        i = i + 1
    Application.EnableEvents = OldEvents
    fn_return_value = True
    return fn_return_value

def __Draw_GotoMode_Symbol(cc, LastVAl, ActVal, rgb_col):
    ArrayPos = Long()

    Val = Long()

    CameFrom_R = Range()
    #--------------------------------------------------------------------------------------------------------
    ArrayPos = cc.Column - GoTo_Col1
    select_0 = Reachable_Col(ArrayPos)
    if (select_0 == __Is_Start_Col):
        __Draw_Analog_Trend(cc, StartMin, ActVal / 255, rgb_col)
        __Draw_Analog_Trend(cc, StartMax, ActVal / 255, rgb_col, Transp_Start_Graph)
    elif (select_0 == __Is_Goto1_Col):
        CameFrom_R = Range(Cells(cc.Row, Came_From_Col(ArrayPos)), Cells(cc.Row + cc.Rows.Count - 1, Came_From_Col(ArrayPos)))
        #CameFrom_R.Select ' Debug
        Val = __Get_Avg_LED_Val(CameFrom_R)
        __Draw_Analog_Trend(cc, Val / 255, ActVal / 255, rgb_col)
    else:
        __Draw_Analog_Trend(cc, LastVAl / 255, ActVal / 255, rgb_col)

def __Line_Analog_Trend(r):
    c = Variant()

    rgb_col = MsoRGBType()

    ActVal = Double()

    LastVAl = Double()

    LastRow = Long()

    LastCol = Long()

    AnaFade = Integer()

    GotoMod = Boolean()
    #----------------------------------------
    # Generate a analog trend picture for the given range.
    # The picture is a rectangle, a triangle or a one sided trapeze.
    # The range could be one row or several rows.
    # If several rows are given the average value of one column is used.
    # Uses the fill color of the left cell next to the given range
    # or yellow if the cell is not filled.
    with_5 = Cells(r.Row, r.Column - 1)
    if with_5.Interior.Color != 16777215:
        rgb_col = __Color_to_RGBColor(with_5.Interior.Color)
    else:
        rgb_col = rgb(220, 220, 0)
    __Check_WertMinMaxValid()
    LastRow = r.Rows.Count - 1
    LastCol = r.Columns.Count - 1
    LastVAl = __Get_Avg_LED_Val(Range(Cells(r.Row, r.Column + LastCol), Cells(r.Row + LastRow, r.Column + LastCol)))
    select_1 = UCase(Range(AnaFade_Rng))
    if (select_1 == '1'):
        AnaFade = 1
    elif (select_1 == 'X'):
        AnaFade = 2
    GotoMod = Goto_Mode_is_Active()
    for c in r:
        if c.Row == r.Row:
            cc = Range(c, c.offset(LastRow, 0))
            ActVal = __Get_Avg_LED_Val(cc)
            if c.Column - GoTo_Col1 >= 0:
                if Reachable_Col(c.Column - GoTo_Col1) > 0:
                    if GotoMod and AnaFade == 2:
                        __Draw_GotoMode_Symbol(cc, LastVAl, ActVal, rgb_col)
                    else:
                        if AnaFade == 0:
                            LastVAl = ActVal
                        __Draw_Analog_Trend(cc, LastVAl / 255, ActVal / 255, rgb_col)
            LastVAl = ActVal

def IsLEDGroup():
    fn_return_value = None
    #--------------------------------------
    fn_return_value = ActiveSheet.RGB_LED_CheckBox
    return fn_return_value

def Draw_Analog_Trend_of_Sheet():
    WasProtected = Boolean()

    Oldupdating = Boolean()

    LastSel = Variant()

    FirstLEDsRow = Long()

    FirstLEDsCol = Long()

    LastLEDsRow = Long()

    LastLEDsCol = Long()

    Row = Long()
    #--------------------------------------
    WasProtected = ActiveSheet.ProtectContents
    if WasProtected:
        ActiveSheet.Unprotect()
    LastSel = Selection
    Oldupdating = Application.ScreenUpdating
    Application.ScreenUpdating = False
    WertMinMaxValid = ''
    FirstLEDsRow = Range(FirstLEDTabRANGE).Row
    FirstLEDsCol = Range(FirstLEDTabRANGE).Column + 1
    LastLEDsRow = FirstLEDsRow + Range(LED_Cnt_Rng) - 1
    #LastLEDsCol = LastFilledColumn(Range(LEDsRANGE), LastLEDsRow) ' Find the last used column
    LastLEDsCol = LastFilledColumn2(Range(LEDsRANGE), LastLEDsRow)
    Del_Analog_Trend_Objects()
    if LastLEDsCol > 0:
        if Calc_Reachable_Columns():
            for Row in vbForRange(FirstLEDsRow, LastLEDsRow):
                if ( Row - FirstLEDsRow )  % 3 == 0 and IsLEDGroup():
                    __Line_Analog_Trend(Range(Cells(Row, FirstLEDsCol), Cells(Row + 2, LastLEDsCol)))
                    Row = Row + 2
                else:
                    __Line_Analog_Trend(Range(Cells(Row, FirstLEDsCol), Cells(Row, LastLEDsCol)))
    Application.ScreenUpdating = Oldupdating
    # VB2PY (UntranslatedCode) On Error Resume Next
    LastSel.Select()
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if WasProtected:
        Protect_Active_Sheet()

def __Test_Draw_Analog_Trend_of_Sheet():
    Start = Variant()
    #UT------------------------------------------
    Start = Timer()
    Draw_Analog_Trend_of_Sheet()
    Debug.Print('Duration: ' + Round(Timer() - Start, 2))

def Del_Analog_Trend_Objects():
    WasProtected = Boolean()

    o = Variant()
    #------------------------------------
    WasProtected = ActiveSheet.ProtectContents
    if WasProtected:
        ActiveSheet.Unprotect()
    for o in ActiveSheet.Shapes:
        if o.Type == msoFreeform and Left(o.Name, Len('Analog_Trend')) == 'Analog_Trend':
            o.Delete()
    if WasProtected:
        Protect_Active_Sheet()

def Update_Grafik(EnableAutomatics=True):
    #--------------------------------------------------------------------
    # Is called if the "Aktualisieren" Button is pressed or the RGB LED checkbox is changed
    if EnableAutomatics:
        Enable_Application_Automatics()
        # In case it was disabled prior due to a bug  13.06.20: Added "EnableAutomatics" because otherwise the screenoupdating is enabled if an example is loaded where "RGB LED" is activ
    if IsAltKeyDown():
        Update_Grafik_from_Str('')
    else:
        if Range(GrafDsp_Rng) != '':
            Update_Grafik_from_Str(Range(GrafDsp_Rng))
        else:
            Update_Grafik_from_Str('1')

def Click_TrendGrafik(Txt):
    Par = vbObjectInitialize(objtype=String)
    #--------------------------------------
    # This function is called if the user clics to the trend grafic if the sheet is protected
    # Since the Grafic overlaps the cell there is no oter way to select the cell with the mouse
    Par = Split(Txt, ' ')
    Cells(Val(Par(0)), Val(Par(1))).Select()

# VB2PY (UntranslatedCode) Option Explicit




