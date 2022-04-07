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

""" Probleme mit den Add / Del columns Buttons:                               ' 22.11.19:
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Die Funktionen Add_Columns_to_Pattern() und Del_Columns_to_Pattern()
 Konnten im Goto Mode nur etwa 10 mal aufgerufen werden. Danach dauerte
 das Kopieren immer länger. Erst eine Sekunde, dann 3, dann 16, 32, ...
 Schuld war die "Src.Copy Dst" Zeile in Copy_Columns()
 Die Ausführung dauerte in der "GoTo_Row" bei jedem Aufruf länger ;-(
 Zusammen mit Armin haben wir herausgefunden, dass Excel die Bedingte
 Formatierung in der "Flash Bedarf:" Zelle versehentlich jedes mal
 kopiert (verdoppelt) hat. Das hat nach 2^n Aufrufen den Rechner ausgebremst.
 Verantwortlich dafür war vermutlich dass:
 - Die "Flash Bedarf:" Zelle aus zwei verbundenen Zellen Bestand (E42 & F43)
 - Die bedingte Formatierung sich versehentlich auf meherer Zellen (=$F$43;$E$42)
   bezugen hat. Die Zelle F43 ist die erste Zelle der Goto Tabelle.
 => Dieser Fehler hat mich vermutlich 6 Stunden gekostet ;-(

"""

__Add_Column_Message_Shown = Boolean()
__Del_Column_Message_Shown = Boolean()

def __Selection_in_Range(r):
    fn_return_value = None
    isect = Variant()
    #----------------------------------------------------------
    # Check if the Selection is inside the range
    # VB2PY (UntranslatedCode) On Error GoTo WrongSelection
    isect = Application.Intersect(r, Selection)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if not isect is None:
        if isect.Column <= Selection.Column:
            fn_return_value = True
    return fn_return_value

def __Get_LEDs_Tab_Range_w_Head():
    fn_return_value = None
    #----------------------------------------------------
    fn_return_value = Range(Cells(LEDsTAB_R - 1, LEDsTAB_C), Cells(LEDsTAB_R + Range('Kanaele') - 1, Last_LEDsCol))
    return fn_return_value

def __In_Pattern_Table():
    fn_return_value = None
    #---------------------------------------------
    # Check if the Selection is inside the pattern table, the Duration line or goto line
    fn_return_value = True
    if __Selection_in_Range(__Get_LEDs_Tab_Range_w_Head()):
        return fn_return_value
    if __Selection_in_Range(Range(Cells(Dauer_Row, Dauer_Col1), Cells(Dauer_Row, Dauer_Col1 + Dauer__Cnt - 1))):
        return fn_return_value
    if __Selection_in_Range(Range(Cells(GoTo_Row, GoTo_Col1), Cells(GoTo_Row, Last_LEDsCol))):
        return fn_return_value
    fn_return_value = False
    return fn_return_value

def __Msg_if_not_in_Pattern_Table():
    fn_return_value = None
    #--------------------------------------------------------
    if not __In_Pattern_Table():
        MsgBox(Get_Language_Str('Zum einfügen oder löschen von Spalten muss sich aktuelle Zelle innerhalb der Tabelle befinden.'), vbCritical, Get_Language_Str('Cursor außerhalb der Tabelle'))
        fn_return_value = True
        return fn_return_value
    return fn_return_value

def __Copy_Columns(FirstRow, LastRow, SrcCol, DstCol, Cnt):
    #-------------------------------------------------------------------------------------------------------
    if Cnt > 0:
        LastCol = SrcCol + Cnt - 1
        Src = Range(Cells(FirstRow, SrcCol), Cells(LastRow, LastCol))
        #Src.Select ' Debug
        Dst = Cells(FirstRow, DstCol)
        Src.Copy(Dst)

def __Del_Columns(FirstRow, LastRow, StartCol, Cnt):
    #----------------------------------------------------------------------------------------
    if Cnt < 1:
        MsgBox('Internal Error in Del_Columns(): Cnt < 1', vbCritical, 'Internal error')
    else:
        #Range(Cells(FirstRow, StartCol), Cells(LastRow, StartCol + Cnt - 1)).Select ' Debug
        Range(Cells(FirstRow, StartCol), Cells(LastRow, StartCol + Cnt - 1)).ClearContents()

def __Insert_Columns(FirstRow, LastRow, Col, Cnt, LastCol):
    #-------------------------------------------------------------------------------------------------------
    # Insert columns by moveing the colunms to the left
    __Copy_Columns(FirstRow, LastRow, Col, Col + Cnt, LastCol - Col + 1)
    __Del_Columns(FirstRow, LastRow, Col, Cnt)

def __Delete_Columns(FirstRow, LastRow, Col, Cnt, LastCol):
    CopyCnt = Long()
    #-------------------------------------------------------------------------------------------------------
    # Delete columns with move if there are other columns to the left
    CopyCnt = LastCol -  ( Col + Cnt )  + 1
    __Copy_Columns(FirstRow, LastRow, Col + Cnt, Col, CopyCnt)
    if Col <= LastCol:
        if CopyCnt > 0:
            __Del_Columns(FirstRow, LastRow, LastCol - Cnt + 1, Cnt)
        else:
            __Del_Columns(FirstRow, LastRow, Col, LastCol - Col + 1)

def __Insert_or_Delete_Columns(Add, FirstRow, LastRow, Col, Cnt, LastCol):
    #---------------------------------------------------------------------------------------------------------------------------------
    if Add:
        __Insert_Columns(FirstRow, LastRow, Col, Cnt, LastCol)
    else:
        __Delete_Columns(FirstRow, LastRow, Col, Cnt, LastCol)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Column_Message_Shown - ByRef 
def __Add_or_Del_Columns_to_Pattern(Add, Column_Message_Shown):
    FirstLEDsRow = Long()

    LastLEDsRow = Long()

    LastLEDsCol = Long()

    Col = Long()

    DstCol = Long()

    Cnt = Long()
    #-----------------------------------------------------------------------------------------------
    if __Msg_if_not_in_Pattern_Table():
        return
    # Message if the button is pressed the first time
    if not Column_Message_Shown:
        if Add:
            Msg = Get_Language_Str('Mit diesem Knopf wird eine Spalte in die Tabelle eingefügt.' + vbCr + 'Die Spalte wird vor links neben der aktuellen Position eingefügt.')
            Title = Get_Language_Str('Spalte in Tabelle einfügen')
        else:
            Msg = Get_Language_Str('Mit diesem Knopf wird die Spalte in der Tabelle gelöscht' + vbCr + 'in der sich der Cursor befindet.')
            Title = Get_Language_Str('Spalte in Tabelle löschen')
        if vbCancel == MsgBox(Msg + vbCr + vbCr + Get_Language_Str('Achtung: Diese Meldung wird nur ein mal angezeigt'), vbOKCancel + vbInformation, Title):
            return
    Column_Message_Shown = True
    Application.ScreenUpdating = False
    Application.EnableEvents = False
    ActiveSheet.EnableCalculation = False
    FirstLEDsRow = Range(FirstLEDTabRANGE).Row
    LastLEDsRow = FirstLEDsRow + Range(LED_Cnt_Rng) - 1
    # Find the last used column
    LastLEDsCol = Application.WorksheetFunction.Max(LastFilledColumn2(Range(LEDsRANGE), LastLEDsRow), LastFilledColumn2(Cells(Dauer_Row, Dauer_Col1), Dauer_Row), LastFilledColumn2(Cells(GoTo_Row, GoTo_Col1), GoTo_Row))
    Cnt = Selection.Columns.Count
    Col = Selection.Column
    __Insert_or_Delete_Columns(Add, FirstLEDsRow, LastLEDsRow, Col, Cnt, LastLEDsCol)
    __Insert_or_Delete_Columns(Add, Dauer_Row, Dauer_Row, Col, Cnt, LastLEDsCol)
    __Insert_or_Delete_Columns(Add, GoTo_Row, GoTo_Row, Col, Cnt, LastLEDsCol)
    Global_Worksheet_Change(Cells(1, 1))
    Enable_Application_Automatics()

def Add_Columns_to_Pattern():
    #----------------------------------
    __Add_or_Del_Columns_to_Pattern(True, __Add_Column_Message_Shown)

def Del_Columns_from_Pattern():
    #------------------------------------
    __Add_or_Del_Columns_to_Pattern(False, __Del_Column_Message_Shown)

# VB2PY (UntranslatedCode) Option Explicit

