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
import proggen.M24_Mouse_Insert_Pos as M24
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

import ExcelAPI.XLW_Workbook as P01

from ExcelAPI.XLC_Excel_Consts import *

from vb2py.vbfunctions import *
from vb2py.vbdebug import *


__Move_Info_Shown = Boolean()
__Del_Row_Msg_Shown = Boolean()

def Used_Rows_All_Borderlines():
    #-------------------------------------
    M30.All_Borderlines(P01.Range(P01.Cells(M02.FirstDat_Row, M02.Enable_Col), P01.Cells(M30.LastUsedRow, M30.LastColumnDatSheet())))

def Proc_Insert_Line_Above(c):
    OldUpdating = Boolean()

    OldMode = Variant()
    #--------------------------------------------
    OldUpdating = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = False
    OldMode = P01.Application.CutCopyMode
    P01.Application.CutCopyMode = xlCut
    if c.Row == M02.FirstDat_Row:
        c.EntireRow.Insert(Shift=xlDown, CopyOrigin=xlFormatFromRightOrBelow)
    elif c.Row > M02.FirstDat_Row:
        c.EntireRow.Insert(Shift=xlDown, CopyOrigin=xlFormatFromLeftOrAbove)
    P01.Application.CutCopyMode = OldMode
    P01.Application.ScreenUpdating = OldUpdating

def Proc_Insert_Line():
    #----------------------------
    Proc_Insert_Line_Above(P01.ActiveCell())

def Proc_Del_Row():
    OldUpdating = Boolean()

    OldEvents = Boolean()
    #------------------------
    if not __Del_Row_Msg_Shown:
        if P01.MsgBox(M09.Get_Language_Str('Mit dem \'Lösche Zeilen\' Knopf können eine oder mehrere Zeilen gelöscht werden.' + vbCr + vbCr + 'Die zu löschenden Zeilen markiert man mit der Maus oder Tastatur und der Großschreibetaste und betätigt den \'Löschen\' Knopf. ' + vbCr + vbCr + 'Tipp:' + vbCr + 'Mit einem Klick auf den Haken an Anfang der Zeile können diese deaktiviert werden ohne sie gleich zu löschen.' + vbCr + 'Alternativ können Zeilen über den \'Aus- und Einblenden\' Knopf versteckt werden. Unsichtbare Zeilen werden nicht in die Arduino Konfiguration übernommen.' + vbCr + vbCr + 'Soll die Zeile tatsächlich gelöscht werden?'), vbYesNo + vbQuestion, M09.Get_Language_Str('Zeile löschen?')) == vbNo:
            return
    __Del_Row_Msg_Shown = True
    OldUpdating = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = False
    OldEvents = P01.Application.EnableEvents
    P01.Application.EnableEvents = False
    if P01.ActiveCell().Row >= M02.FirstDat_Row:
        P01.Selection.EntireRow.Delete(Shift=xlUp)
        M20.Update_Start_LedNr()
        M30.All_Borderlines(P01.Range(P01.Cells(M02.FirstDat_Row, M02.Enable_Col), P01.Cells(M30.LastUsedRow + M02.SPARE_ROWS, M30.LastColumnDatSheet())))
        M20.Format_Cells_to_Row(M30.LastUsedRow)
    P01.Application.ScreenUpdating = OldUpdating
    P01.Application.EnableEvents = OldEvents

def Proc_Move_Row():
    global __Move_Info_Shown
    ActSh = String()
    #-------------------------
    ActSh = P01.ActiveSheet
    if not __Move_Info_Shown:
        if P01.MsgBox(M09.Get_Language_Str('Mit dem \'Verschiebe Zeilen\' Knopf können eine oder mehrere Zeilen verschoben werden.' + vbCr + 'Damit kann die Reihenfolge der Beleuchtungen oder der anderen Effekte an die physikalisch vorgegebene ' + 'Anschlussreihenfolge angepasst werden.' + vbCr + vbCr + 'Die zu verschiebenden Zeilen markiert man mit der Maus oder Tastatur und der Großschreibetaste und betätigt den \'Verschieben\' Knopf. ' + 'Dann wählt man mit der Maus die neue Position der Zeilen. Eine Grüne Linie markiert dabei die Zielposition.' + vbCr + 'Mit der \'ESC\' Taste kann die Aktion abgebrochen werden.' + vbCr + vbCr + 'Achtung: Diese Meldung wird nur einmal pro Programmstart angezeigt.'), vbOKCancel, M09.Get_Language_Str('Funktionsweise des \'Verschiebe Zeilen\' Knopfes')) == vbCancel:
            return
        __Move_Info_Shown = True
    if P01.ActiveCell().Row < M02.FirstDat_Row:
        P01.MsgBox(M09.Get_Language_Str('Achtung: Zum verschieben von Zeilen müssen eine oder mehrere Zellen im Datenbereich der Tabelle markiert ' + 'sein. Die entsprechenden Zeilen können dann per Maus verschoben werden.' + vbCr + vbCr + 'Der gewählte Bereich liegt (teilweise) außerhalb des Datenbereichs'), vbInformation, M09.Get_Language_Str('Zu verschiebende Zeile muss im Datenbereich der Tabelle liegen'))
        return
    
    ActSh.moveRows()
    M20.Update_Start_LedNr()
    
    """
    selectedrows = P01.Selection.EntireRow()
    
    if selectedrows[0] >= M02.FirstDat_Row:
        # VB2PY (UntranslatedCode) On Error GoTo EnabButtons
        P01.ActiveSheet.EnableDisableAllButtons(False)
        src = P01.Selection.EntireRow() #*HL
        #*HLsrc.Select()
        P01.Application.StatusBar = M09.Get_Language_Str('Zeilen verschieben: Bitte Zielposition mit der Maus oder der Tastatur wählen')
        P01.updateWindow()
        
        DestRow = M24.Select_Move_Dest_by_Mouse(M02.Enable_Col, M30.LastColumnDatSheet())
        #DestRow = P01.ActiveSheet.getSelectedRow()
        if DestRow > 0:
            OldUpdating = P01.Application.ScreenUpdating
            P01.Application.ScreenUpdating = False
            OldEvents = P01.Application.EnableEvents
            P01.Application.EnableEvents = False
            if DestRow != src[0]: #*HL .Row:
                #*HL src.EntireRow.Cut()
                #*HL P01.Rows(DestRow + ':' + DestRow + src.Rows.Count).Insert(Shift=xlDown)
                #*HL P01.Rows(DestRow + ':' + DestRow + src.Rows.Count - 1).Select()
                P01.ActiveSheet.moveRows(src,DestRow)
                M20.Update_Start_LedNr()
            #Used_Rows_All_Borderlines()
            #Format_Cells_to_Row LastUsedRow
            M20.Format_All_Rows()
            M20.Update_Sum_Func()
            P01.Application.ScreenUpdating = OldUpdating
            P01.Application.EnableEvents = OldEvents
        P01.Application.StatusBar = ''
    #P01.Sheets(ActSh).EnableDisableAllButtons(True)
    """
    
    return

def Proc_Copy_Row():
    OldUpdating = Boolean()

    OldEvents = Boolean()
    #-------------------------
    Make_sure_that_Col_Variables_match()
    OldUpdating = Application.ScreenUpdating
    Application.ScreenUpdating = False
    OldEvents = Application.EnableEvents
    Application.EnableEvents = False
    if Selection.Row >= FirstDat_Row:
        DestRow = Selection.Row + Selection.Rows.Count
        RowCnt = Selection.Rows.Count
        for i in vbForRange(1, RowCnt):
            Rows(DestRow).EntireRow.Insert(Shift=xlDown, CopyOrigin=xlFormatFromLeftOrAbove)
        EndDestRow = DestRow + Selection.Rows.Count - 1
        RowDict[DestRow + ':' + EndDestRow] = Selection.EntireRow.Value
        Range(Cells(DestRow, Selection.Column), Cells(EndDestRow, Selection.Column + Selection.Columns.Count - 1)).Select()
        Used_Rows_All_Borderlines()
        Format_Cells_to_Row(DestRow + Selection.Rows.Count)
        Update_Sum_Func()
        for Row in vbForRange(DestRow, DestRow + RowCnt):
            s = Cells(Row, Config__Col)
            if s != '':
                FindMacro_and_Add_Icon_and_Name(s, Row, ActiveSheet)
    Update_Start_LedNr()
    Application.ScreenUpdating = OldUpdating
    Application.EnableEvents = OldEvents

# VB2PY (UntranslatedCode) Option Explicit


