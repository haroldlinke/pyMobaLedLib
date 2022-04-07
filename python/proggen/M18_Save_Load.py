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

import  proggen.F00_mainbuttons as F00

from ExcelAPI.X01_Excel_Consts import *


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

""" Save and load data from one or several Sheets
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Save the data from DCC, Selectrix and CAN sheets to a text file

 File Format
 ~~~~~~~~~~~
 - Tab separated text file
 - Header: Filetype, Version
 - Sub Header for each sheet: Sheet Typ, Sheet Name
 - Ext. MLL_pgf
 ToDo:
 - Es soll möglich sein, dass ein Sheet in ein Sheet geladen wird welches eine andere Page_ID hat
 - Wann sol gefragt werden welche Seiten gespeichert/importiert werden sollen
   - Beim Import von einer alten Version sollen alle Seiten importiert werden
   - Beim Speichern Menu werden alle oder alle ausgewählten Seiten gespeichert
   - Beim Laden Menü wird anfangs gefragt ob alle oder nur bestimmte Seiten importiert werden sollen
   - Mit einem Copy Befehl können Daten von einem Sheet in ein anderes Sheet kopiert werden.
"""

PGF_Identification = 'Program_Generator configuration file'
PGF_Version_String = 'V1.0'
__Head_ID = 'Head:'
__SheetID = 'Sheet:'
__Line_ID = 'Line:'
__Import_Page_ID = String()
__First_Line = Boolean()
__AddedToFilterColumn = Long()
__HiddenRows = Long()
__Start_Row = Long()
__LastA_Row = Long()
__Save_Data_FileName = String()
__Changed2SaveDir = Boolean()
__Copy_S2S_SrcSheet = String()
__ImportFollowingSheets = Boolean()

def __Create_pgf_File(Name):
    fn_return_value = None
    fp = Integer()
    #----------------------------------------------------------
    fp = FreeFile()
    try:
        # VB2PY (UntranslatedCode) On Error GoTo WriteError
        VBFiles.openFile(fp, Name, 'w') 
        VBFiles.writeText(fp, __Head_ID + vbTab + PGF_Identification + vbTab + PGF_Version_String, '\n')
        fn_return_value = fp
        # VB2PY (UntranslatedCode) On Error GoTo 0
        return fn_return_value
    except:
        P01.MsgBox(M09.Get_Language_Str('Fehler beim erzeugen der Programm Generator Konfigurationsdatei:') + vbCr + '  \'' + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Konfigurationsdatei:'))
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def __Save_Sheet_to_pgf(fp, Sh):
    fn_return_value = None
    #OldSh = String()

    #rng = Range()

    #r = Variant()
    #----------------------------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    try:
        
        OldSh = P01.ActiveSheet.Name
        Sh.Select()
        Page_ID = P01.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL)
        VBFiles.writeText(fp, __SheetID + vbTab, Page_ID + vbTab + Sh.Name, '\n')
        if len(P01.Selection.Cells) > 1:
            rng = P01.Selection
        else:
            rng = P01.Range(P01.Cells(M02.FirstDat_Row, 1), P01.Cells(M30.LastFilledRowIn_ChkAll(Sh), 1))
        Col_from_Sheet = ''
        M25.Make_sure_that_Col_Variables_match(Sh)
        for r in rng.Rows:
            if not r.Hidden and r.Row >= M02.FirstDat_Row:
                if P01.Cells(r.Row, M02.Enable_Col) == ChrW(M02.Hook_CHAR):
                    Enabled = 'Act'
                else:
                    Enabled = '-'
                VBFiles.writeText(fp, __Line_ID + vbTab + Enabled)
                for Col in vbForRange(M02.Enable_Col + 1, M30.LastColumnDatSheet()):
                    if Col == M25.MacIcon_Col:
                        #Col = Col + 1
                        continue
                        # Skip the Icon column (MacIcon_Col is -1 if the column doesn't exist)      ' 20.10.21
                    if Col == M25.LanName_Col:
                        #Col = Col + 1
                        continue
                        # Use two lines to be able to enable both new columns separately                             '
                    VBFiles.writeText(fp, vbTab + Replace(P01.Cells(r.Row, Col), vbLf, '{NewLine}'))
                VBFiles.writeText(fp, '', '\n')
        # VB2PY (UntranslatedCode) On Error GoTo 0
        P01.Sheets(OldSh).Select()
        fn_return_value = True
        return fn_return_value
    except:
        raise
        P01.Sheets(OldSh).Select()
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def __Save_SingleSheet_to_pgf(Name, Sh):
    fn_return_value = None
    fp = Integer()
    #-----------------------------------------------------------------------------------------
    if not M28.Is_Data_Sheet(Sh):
        P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Die Seite \'#1#\' ist keine gültige Datenseite'), '#1#', Sh.Name), vbCritical, M09.Get_Language_Str('Ungültige Daten Seite ausgewählt'))
        return fn_return_value
    fp = __Create_pgf_File(Name)
    if fp > 0:
        fn_return_value = __Save_Sheet_to_pgf(fp, Sh)
        VBFiles.closeFile(fp)
    return fn_return_value

def __Test_Save_SingleSheet_to_pgf():
    #-----------------------------------------
    Debug.Print('Save_SingleSheet_to_pgf: ' + __Save_SingleSheet_to_pgf(P01.ThisWorkbook.Path + '\\Test.MLL_pgf', P01.ActiveSheet))

def Save_Sheets_to_pgf(Name, FromAllSheets):
    fn_return_value = None
    Res = Boolean()
    #--------------------------------------------------------------------------------------
    if FromAllSheets == False and P01.ActiveWindow.SelectedSheets["Count"] == 1:
        Res = __Save_SingleSheet_to_pgf(Name, P01.ActiveSheet)
    else:
        Res = True
        fp = __Create_pgf_File(Name)
        if fp > 0:
            if P01.ActiveWindow.SelectedSheets["Count"] > 1:
                for Sh in P01.ActiveWorkbook.Sheets:
                    if M28.Is_Data_Sheet(Sh):
                        Res = __Save_Sheet_to_pgf(fp, Sh)
                        if Res == False:
                            break
            else:
                for Sh in P01.ActiveWorkbook.sheets:
                    if M28.Is_Data_Sheet(Sh) and Sh.Visible == xlSheetVisible and Sh.Name != 'Examples':
                        Res = __Save_Sheet_to_pgf(fp, Sh)
                        if Res == False:
                            break
            VBFiles.closeFile(fp)
    if Res == False:
        P01.MsgBox(M09.Get_Language_Str('Fehler beim Schreiben der Programm Generator Konfigurationsdatei:') + vbCr + '  \'' + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim Schreiben der Konfigurationsdatei:'))
    fn_return_value = Res
    return fn_return_value

def __Test_Save_Sheets_to_pgf():
    #UT----------------------------------
    Debug.Print('Save_Sheets_to_pgf=' + Save_Sheets_to_pgf(P01.ThisWorkbook.Path + '\\Test_All.MLL_pgf', True))

def __Find_Sheet_with_matching_Page_ID(Page_ID):
    fn_return_value = None
    #Sh = P01.Worksheet()
    #--------------------------------------------------------------------------------
    for Sh in P01.ActiveWorkbook.Sheets:
        if Sh.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL) == Page_ID:
            fn_return_value = Sh
            return fn_return_value
    return fn_return_value

def __Copy_and_Clear_Sheet(SheetName, Page_ID):
    fn_return_value = None
    #Sh = P01.Worksheet()
    #---------------------------------------------------------------------------------------
    Sh = __Find_Sheet_with_matching_Page_ID(Page_ID)
    if Sh is None:
        P01.MsgBox(M09.Get_Language_Str('Fehler: Es existiert keine passende Seite als Vorlage zum importieren der Daten'), vbCritical, M09.Get_Language_Str('Fehler: Seite kann nicht angelegt werden'))
        return fn_return_value
    else:
        for s in P01.ActiveWorkbook.Sheets:
            if M28.Is_Data_Sheet(s):
                DstSh = s
        Sh.Copy(after=DstSh)
        P01.ActiveSheet.Name = SheetName
        First_Row = M02.FirstDat_Row
        while P01.Cells(First_Row, 1).EntireRow.Hidden:
            First_Row = First_Row + 1
        P01.Rows(M02.FirstDat_Row + ':' + P01.ActiveSheet.get_LastUsedRow()).ClearContents()
        fn_return_value = True
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def __Open_or_Create_Sheet(SheetName, Inp_Page_ID, Name, ToActiveSheet):
    global Page_ID,__Import_Page_ID,__First_Line
    fn_return_value = None
    CreatedNewSheet = Boolean()

    Row = Long()

    Col = Long()

    i = Long()
    #---------------------------------------------------------------------------------------------------------------------------------------
    Debug.Print('Open_or_Create_Sheet(')
    if ToActiveSheet:
        Page_ID = P01.ActiveSheet.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL)
        if not M28.Is_Data_Sheet(P01.ActiveSheet):
            P01.MsgBox(M09.Get_Language_Str('Fehler: Die Ausgewählte Seite ist keine gültige Daten Seite'), vbCritical, M09.Get_Language_Str('Falsche Seite ausgewählt'))
            return fn_return_value
        Name = __Copy_S2S_SrcSheet
        if Page_ID != Inp_Page_ID and  ( Page_ID == 'Selectrix' or Inp_Page_ID == 'Selectrix' ) :
            P01.MsgBox(M09.Get_Language_Str('Achtung: Die Adressen werden automatisch konvertiert. Sie müssen im Anschluss manuell überprüft werden.'), vbInformation, M09.Get_Language_Str('Achtung: Anpassung der Adressen überprüfen'))
    else:
        if not M30.SheetEx(SheetName):
            if not __Copy_and_Clear_Sheet(SheetName, Inp_Page_ID):
                return fn_return_value
            CreatedNewSheet = True
        else:
            P01.Sheets(SheetName).Activate()
        Page_ID = P01.ActiveSheet.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL)
    __Import_Page_ID = Inp_Page_ID
    __First_Line = True
    M25.Make_sure_that_Col_Variables_match()
    Row = M30.LastFilledRowIn_ChkAll(P01.ActiveSheet) + 2
    if CreatedNewSheet == False:
        P01.CellDict[Row, M25.Descrip_Col] = M09.Get_Language_Str('Importiert von:') + Name
        P01.Cells(Row, M02.Enable_Col).ClearContents()
    fn_return_value = True
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: prLst - ByRef 
def __Adapt_Adress_and_Typ_from_Selectrix(prLst):
    Addr = Long()
    #----------------------------------------------------------------------
    # Adapt a DCC or CAN Address from Selectrix to DCC or CAN
    if IsNumeric(prLst(M25.DCC_or_CAN_Add_Col - 1)):
        Addr = 1 + prLst(M25.DCC_or_CAN_Add_Col - 1) * 8
        if IsNumeric(prLst(M25.DCC_or_CAN_Add_Col - 1 + 1)):
            Addr = Addr + prLst(M25.DCC_or_CAN_Add_Col - 1 + 1)
        prLst[M25.DCC_or_CAN_Add_Col - 1] = Addr
    if prLst(M25.Inp_Typ_Col - 1 + 1) != '':
        M09.Set_Tast_Txt_Var()
        if prLst(M25.Inp_Typ_Col - 1 + 1) == M09.Tast_T:
            prLst[M25.Inp_Typ_Col - 1 + 1] = ''
    return prLst

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: prLst - ByRef 
def __Adapt_Adress_and_Typ_to_Selectrix(prLst):
    Addr = Long()
    #--------------------------------------------------------------------
    # Adapt a DCC or CAN Address to Selectrix
    if IsNumeric(prLst(M25.SX_Channel_Col - 1)):
        Addr = prLst(M25.SX_Channel_Col - 1)
        if Addr > 0:
            Addr = Addr - 1
        prLst[M25.SX_Channel_Col - 1] = Int(Addr / 8)
        prLst[M25.SX_Bitposi_Col - 1] = Addr % 8
    if prLst(M25.Inp_Typ_Col - 1) != '':
        M09.Set_Tast_Txt_Var()
        if prLst(M25.Inp_Typ_Col - 1) != M09.OnOff_T:
            prLst[M25.Inp_Typ_Col - 1] = M09.Tast_T
    return prLst

def __Read_Line(line):
    global __LastA_Row,__First_Line,__Import_Page_ID, __Start_Row, __HiddenRows, __LastA_Row, __AddedToFilterColumn
    
    fn_return_value = False
    Parts = vbObjectInitialize(objtype=String)

    SkipLine = Boolean()

    Row = Long()

    Col = Long()

    i = Long()
    #----------------------------------------------------
    Parts = Split(line, vbTab)
    if Page_ID != __Import_Page_ID:
        # Problem "Selectrix" has an additional column "Bitposition"
        if __Import_Page_ID == 'Selectrix':
            Parts = __Adapt_Adress_and_Typ_from_Selectrix(Parts)
            M30.DeleteElementAt(M25.Inp_Typ_Col - 1, Parts)
        if Page_ID == 'Selectrix':
            M30.InsertElementAt(M25.Inp_Typ_Col - 2, Parts, '')
            Parts = __Adapt_Adress_and_Typ_to_Selectrix(Parts)
    Row = M30.LastFilledRowIn_ChkAll(P01.ActiveSheet)
    if __First_Line:
        __First_Line = False
        First_Row = M02.FirstDat_Row
        while P01.Cells(First_Row, 1).EntireRow.Hidden:
            First_Row = First_Row + 1
        # Check if the first line in the sheet an in the file is "RGB_Heartbeat(#LED)"
        # The line is skipped
        if P01.Cells(First_Row, M25.Config__Col) == 'RGB_Heartbeat(#LED)' and P01.Cells(First_Row, M25.Config__Col) == Parts(M25.Config__Col - 1):
            fn_return_value = True
            return fn_return_value
    if not SkipLine:
        OldEvents = P01.Application.EnableEvents
        P01.Application.EnableEvents = False
        Row = Row + 1
        Col = M02.Enable_Col
        P01.CellDict[Row, M25.Descrip_Col].Formula = '=""'
        for i in vbForRange(2, UBound(Parts)):
            Col = Col + 1
            if Col == M25.MacIcon_Col:
                Col = Col + 1
                # Skip the Icon column (MacIcon_Col is -1 if the column doesn't exist)      ' 20.10.21
            if Col == M25.LanName_Col:
                Col = Col + 1
                # Use two lines to be able to enable both new columns separately                             '
            s = Replace(Parts(i), '{NewLine}', vbLf)
            if Left(s, 2) == '==':
                s = '\'' + s
            if Parts(i) != '':
                P01.CellDict[Row, Col] = s
            if Col == M25.Config__Col and s != '':
                M27.FindMacro_and_Add_Icon_and_Name(s, Row, P01.ActiveSheet)
            if Col == M25.LED_Nr__Col:
                P01.CellDict[Row, Col].NumberFormat = 'General'
        if P01.Cells(Row, Col).EntireRow.Hidden:
            __HiddenRows = __HiddenRows + 1
        if P01.Cells(Row, M25.Filter__Col) != '':
            __AddedToFilterColumn = __AddedToFilterColumn + 1
        if __Start_Row == 0:
            __Start_Row = Row
        __LastA_Row = Row
        if Parts(1) == 'Act':
            P01.CellDict[Row, M02.Enable_Col] = ChrW(M02.Hook_CHAR)
            # Enable the Line   ' 01.05.20:
        M20.Update_TestButtons(Row)
        M20.Update_StartValue(Row)
        P01.Application.EnableEvents = OldEvents
    fn_return_value = True
    return fn_return_value

def __PGF_has_Multiple_Sheets(lines):
    fn_return_value = None
    line = Variant()

    SheetCnt = Long()
    #---------------------------------------------------------------------
    for line in lines:
        line = Replace(line, vbLf, '')
        if Left(line, Len(__SheetID)) == __SheetID:
            SheetCnt = SheetCnt + 1
            if SheetCnt > 1:
                fn_return_value = True
                return fn_return_value
    return fn_return_value

def __Check_Hidden_Lines():
    global __HiddenRows, __AddedToFilterColumn
    return #*HL

    #-------------------------------
    if __AddedToFilterColumn:
        M25.Make_sure_that_Col_Variables_match()
        if __HiddenRows > 0:
            P01.Range(P01.Cells(__Start_Row, M25.Filter__Col), P01.Cells(__LastA_Row, M25.Filter__Col)).Select()
            #Application.ScreenUpdating = True
            Proc_Hide_Unhide()
        ## VB2PY (CheckDirective) VB directive took path 1 on 0
        if P01.MsgBox(M09.Get_Language_Str('Achtung es wurden Zeilen hinzugefügt welche durch die Filtereinstellungen ' + 'im aktuellen Blatt ausgeblendet werden können!' + vbCr + 'Der Filter muss angepasst werden sonst werden diese Zeilen evtl. bei der nächsten ' + 'Änderung wieder ausgeblendet.' + vbCr + vbCr + 'Bei dem normalerweise verwendeten Filter löscht man dazu die Einträge in der ' + '\'Filter\' Spalte.' + vbCr + 'Alternativ können die Filtereinstellungen im Anschluss angepasst werden.' + vbCr + vbCr + 'Sollen die Einträge in der Filterspalte gelöscht werden damit die Einträge immer sichtbar sind ?'), vbQuestion + vbYesNo, M09.Get_Language_Str('Zeilen hinzugefügt welche durch den Filter ausgeblendet werden können')) == vbYes:
            P01.Selection.ClearContents()
        if __HiddenRows > 0:
            #Application.ScreenUpdating = False
            P01.Cells(__Start_Row, M25.Descrip_Col).Select()

def __Read_PGF_from_String_V1_0(lines, Name, ToActiveSheet):
    global __AddedToFilterColumn, __HiddenRows, __Start_Row, __ImportFollowingSheets
    fn_return_value = False
    LNr = 0 #Long()

    SkipSheet = Boolean()

    Inp_Page_ID = String()

    SheetName = String()

    Multiple_Sheets = Boolean()

    SheetCnt = Long()

    LineNrInSheet = 0 # Long()
    #-----------------------------------------------------------------------------------------------------------------
    Multiple_Sheets = __PGF_has_Multiple_Sheets(lines)
    __AddedToFilterColumn = 0
    __HiddenRows = 0
    __Start_Row = 0
    __ImportFollowingSheets = False
    #Unload(UserForm_Options)
    for LNr in vbForRange(1, UBound(lines) - 1):
        if Trim(Replace(lines(LNr), vbLf, '')) != '':
            Parts = Split(Replace(lines(LNr), vbLf, ''), vbTab)
            select_0 = Parts(0)
            if (select_0 == __SheetID):
                __Check_Hidden_Lines()
                if M28.Is_Data_Sheet(P01.ActiveSheet):
                    M20.Format_Cells_to_Row(P01.ActiveSheet.get_LastUsedRow() + M02.SPARE_ROWS)
                    M20.Update_Start_LedNr()
                Inp_Page_ID = Parts(1)
                SheetName = Parts(2)
                __AddedToFilterColumn = 0
                __HiddenRows = 0
                __Start_Row = 0
                if Multiple_Sheets:
                    if SheetName == 'Examples':
                        SkipSheet = True
                    else:
                        if __ImportFollowingSheets:
                            SkipSheet = False
                        else:
                            select_1 = P01.MsgBox(M09.Get_Language_Str('Soll die Seite') + ' \'' + SheetName + '\' ' + M09.Get_Language_Str('importiert werden?'), vbQuestion + vbYesNoCancel, M09.Get_Language_Str('Seite importieren?'))
                            if (select_1 == vbYes):
                                if P01.GetAsyncKeyState(P01.__VK_CONTROL) != 0:
                                    __ImportFollowingSheets = True
                                SkipSheet = False
                            elif (select_1 == vbNo):
                                SkipSheet = True
                            else:
                                if SheetCnt > 0:
                                    M20.Format_Cells_to_Row(P01.ActiveSheet.get_LastUsedRow() + M02.SPARE_ROWS)
                                    # Add some reserve lines    ' 07.08.20:
                                return fn_return_value
                else:
                    SkipSheet = False
                if not SkipSheet:
                    if SheetCnt > 0:
                        M20.Format_Cells_to_Row(P01.ActiveSheet.get_LastUsedRow() + M02.SPARE_ROWS)
                        # Add some reserve lines    ' 06.08.20:
                    SheetCnt = SheetCnt + 1
                    LineNrInSheet = 1
                    F00.StatusMsg_UserForm.ShowDialog(M09.Get_Language_Str('Lade Seite \'') + SheetName + '\'', '...')
                    if not __Open_or_Create_Sheet(SheetName, Inp_Page_ID, Name, ToActiveSheet):
                        return fn_return_value
            elif (select_0 == __Line_ID):
                if not SkipSheet:
                    if not __Read_Line(lines(LNr)):
                        return fn_return_value
                    F00.StatusMsg_UserForm.Set_ActSheet_Label('Line: ' + str(LineNrInSheet))
                    LineNrInSheet = LineNrInSheet + 1
            else:
                P01.MsgBox(M09.Get_Language_Str('Fehler: Unbekannter Zeilentyp in Zeile:') + ' ' + LNr + vbCr + M09.Get_Language_Str('in der PGF Datei:') + vbCr + '  \'' + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler in PGF Datei'))
                return fn_return_value
    __Check_Hidden_Lines()
    M20.Format_Cells_to_Row(P01.ActiveSheet.get_LastUsedRow() + M02.SPARE_ROWS)
    M20.Update_Start_LedNr()
    fn_return_value = True
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def Read_PGF(Name, ToActiveSheet=False):
    global __ImportFollowingSheets
    
    fn_return_value = False
    #FileStr = String()

    lines = vbObjectInitialize(objtype=String)

    Parts = vbObjectInitialize(objtype=String)

    Err = Boolean()
    #-------------------------------------------------------------------------------------------
    __ImportFollowingSheets = False
    FileStr = M30.Read_File_to_String(Name)
    if FileStr == '#ERROR#':
        return fn_return_value
    lines = Split(FileStr, vbCr)
    if UBound(lines) <= 1:
        lines = Split(FileStr,"\n")
        if UBound(lines) <= 1:
            P01.MsgBox(M09.Get_Language_Str('Fehler: Die PGF Datei enthält keine Daten:') + vbCr + '  \'' + Name + '\'', vbCritical, M09.Get_Language_Str('Ungültige PGF Datei'))
            return fn_return_value
    Parts = Split(lines(0), vbTab)
    Err = ( UBound(Parts) < 2 )
    if not Err:
        Err = ( Parts(0) != __Head_ID )
    if not Err:
        Err = ( Parts(1) != PGF_Identification )
    if not Err:
        ScrUpd = P01.Application.ScreenUpdating
        P01.Application.ScreenUpdating = False
        VerStr = Parts(2)
        if (VerStr == PGF_Version_String):
            fn_return_value = __Read_PGF_from_String_V1_0(lines, Name, ToActiveSheet)
            #*HL StatusMsg_UserForm.Hide()
        else:
            Err = True
        P01.Application.ScreenUpdating = ScrUpd
    if Err:
        P01.MsgBox(M09.Get_Language_Str('Fehler: Die PGF Datei enthält keinen gültigen Header:') + vbCr + '  \'' + Name + '\'', vbCritical,M09.Get_Language_Str('Ungültige PGF Datei'))
    return fn_return_value

def __Test_Read_PGF():
    #UT------------------------
    #Debug.Print "Read_PGF=" & Read_PGF(ThisWorkbook.Path & "\Test.MLL_pgf")
    P01.Application.EnableEvents = False
    Debug.Print('Read_PGF=' + Read_PGF('C:\\Dat\\Märklin\\Arduino\\LEDs_Eisenbahn\\Doc\\von anderen\\Dominik\\Prog_Gen_Data_06_08_2020.MLL_pgf'))
    Debug.Print('Application.EnableEvents:' + P01.Application.EnableEvents)
    P01.Application.EnableEvents = True

def Get_MyExampleDir():
    fn_return_value = None
    Dir = [] 
    #-------------------------------------------
    Dir = Environ('USERPROFILE') + '/Documents/' + M02.MyExampleDir
    M30.CreateFolder(Dir + '/')
    fn_return_value = Dir
    return fn_return_value

def __Save_Data_to_File_CallBack(Do_Import, Import_FromAllSheets):
    global __Changed2SaveDir
    #--------------------------------------------------------------------------------------------
    Debug.Print('Save_Data_to_File_CallBack(' + str(Do_Import) + ', ' + str(Import_FromAllSheets) + ')')
    if Do_Import:
        if Save_Sheets_to_pgf(__Save_Data_FileName, Import_FromAllSheets):
            P01.MsgBox(M09.Get_Language_Str('Die Datei wurde erfolgreich geschrieben:') + vbCr + '  \'' + __Save_Data_FileName + '\'', vbInformation, 'Datei wurde geschrieben')

def __Achtivate_MyExampleDir_if_called_the_first_time():
    global __Changed2SaveDir
    #------------------------------------------------------------
    if __Changed2SaveDir == False:
        ChDir(( Get_MyExampleDir() ))
        __Changed2SaveDir = True

def Save_Data_to_File():
    global __Save_Data_FileName
    
    ExampleName = String()

    Res = Variant()
    #-----------------------------
    # Is called from the options dialog
    __Achtivate_MyExampleDir_if_called_the_first_time()
    ExampleName = 'Prog_Gen_Data_' + Replace(P01.Date_str(), '.', '_')
    Res = P01.Application.GetSaveAsFilename(InitialFileName= ExampleName, fileFilter= M09.Get_Language_Str('Program Generator File (*.MLL_pgf), *.MLL_pgf'), Title= M09.Get_Language_Str('Dateiname zum abspeichern der Daten angeben'))
    if Res:
        #*HL if Dir(Res) != '':
        #*HL    if P01.MsgBox(M09.Get_Language_Str('Achtung die Datei existiert bereits!' + vbCr + vbCr + 'Soll die Datei überschrieben werden?'), vbQuestion + vbOKCancel, M09.Get_Language_Str('Existierende Datei überschreiben?')) != vbOK:
        #*HL         return
        __Save_Data_FileName = Res
        #*HL M17.Remove_Selections_in_all_Data_Sheets()
        #M30.Import_Hide_Unhide.Start('Save_Data_to_File_CallBack', Import_FromAll=ActiveWindow.SelectedSheets.Count - 1)
        __Save_Data_to_File_CallBack(True,False) #*HL

def Load_Data_from_File():
    Res = Variant()
    #-------------------------------
    # Is called from the options dialog
    __Achtivate_MyExampleDir_if_called_the_first_time()
    Res = P01.Application.GetOpenFilename(fileFilter= M09.Get_Language_Str('Program Generator File (*.MLL_pgf), *.MLL_pgf'), Title= M09.Get_Language_Str('Dateiname zum Importieren der Daten angeben'))
    if Res != "":
        Read_PGF(Res)

def __Copy_to_Selected_Sheet_Callback(Do_Copy):
    #--------------------------------------------------------------
    if Do_Copy:
        if P01.ActiveSheet.Name == __Copy_S2S_SrcSheet:
            P01.MsgBox(M09.Get_Language_Str('Achtung: Zum Kopieren der Daten von einer Seite auf eine andere Seite müssen zwei ' + 'verschiedene Seiten ausgewählt werden.' + vbCr + 'Dazu wählt man im folgenden Dialog die gewünschte Zielseite über die Reiter am ' + 'unteren Rand der Seite aus BEVOR man \'OK\' betätigt.'), vbInformation, M09.Get_Language_Str('Zielseite wurde nicht ausgewählt'))
            __Copy_to_Selected_Sheet_Callback() #*HL Select_Dest_Sheet.Start('Copy_to_Selected_Sheet_Callback')
        else:
            Read_PGF(__Save_Data_FileName, ToActiveSheet=True)

def __Save_Data_from_active_Sheet_to_File_CallBack(Do_Import, Import_FromAllSheets):
    global __Copy_S2S_SrcSheet
    
    #--------------------------------------------------------------------------------------------------------------
    Debug.Print('Save_Data_from_active_Sheet_to_File_CallBack(' + Do_Import + ', ' + Import_FromAllSheets + ')')
    if Do_Import:
        P01.ActiveSheet.Select()
        __Copy_S2S_SrcSheet = P01.ActiveSheet.Name
        if Save_Sheets_to_pgf(__Save_Data_FileName, False):
            __Copy_to_Selected_Sheet_Callback() #*HLSelect_Dest_Sheet.Start('Copy_to_Selected_Sheet_Callback')

def Copy_from_Sheet_to_Sheet():
    global __Save_Data_FileName
    #------------------------------------
    # Is called from the options dialog
    if P01.MsgBox(M09.Get_Language_Str('Mit dieser Funktion können ausgewählte Daten aus der ' + 'aktuellen Seite in eine andere Seite kopiert werden.'), vbOKCancel, M09.Get_Language_Str('Kopieren von Daten von dieser Seite in eine andere Seite')) != vbOK:
        return
    __Save_Data_FileName = Get_MyExampleDir() + '\\Copy_Sheet2Sheet.MLL_pgf'
    #*HL M17.Remove_Selection_in_Sheet(P01.ActiveSheet)
    __Save_Data_from_active_Sheet_to_File_CallBack(True,True) #*HLImport_Hide_Unhide.Start('Save_Data_from_active_Sheet_to_File_CallBack', Import_FromAll=- 2)

# VB2PY (UntranslatedCode) Option Explicit
