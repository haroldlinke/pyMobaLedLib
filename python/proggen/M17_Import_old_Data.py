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
import proggen.M18_Save_Load as M18
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

""" Import data from an old version

 ToDo:
 - Sollen mehrere Sheets gespeichert / geladen werden oder nur eins
   => Beim speichern werden alle Sheets gespeichert
 - Was ist wenn mehrere DCC Sheets vorhanden sind
   => Die Sheets werden angelegt
 - Save und Load
"""

__ImportWB = None

def __Close_and_Delete_Temp_Prog_Gen(TempName):
    fn_return_value = None
    #-----------------------------------------------------------------
    #*HL if Same_Name_already_open(FileNameExt(TempName)):
    #*HL     Workbooks(FileNameExt(TempName)).Close(Savechanges=False)
    # VB2PY (UntranslatedCode) On Error GoTo Error_Kill
    try:
        if Dir(TempName) != '':
            Kill(TempName)()
        # VB2PY (UntranslatedCode) On Error GoTo 0
        fn_return_value = True
        return fn_return_value
    except:
        P01.MsgBox(M09.Get_Language_Str('Fehler beim löschen der Datei') + vbCr + '  \'' + TempName + '\' ', vbCritical, M09.Get_Language_Str('Fehler beim löschen des temporären version alten Programm Generators'))
        return fn_return_value

def __Select_and_Open_Old_Version():
    fn_return_value = None
    Name = Variant()

    Path = String()
    #---------------------------------------------------------
    # Select the old version of the Prog_Generator and open it
    Path = M02.Get_MobaUserDir()
    P01.ChDrive(Path)
    ChDir(Path)
    while 1:
        Name = P01.Application.GetOpenFilename(fileFilter='Program generator  (*.xlsm), *.xlsm', Title= M09.Get_Language_Str('Altes Prog_Generator Programm auswählen von der importiert werden soll'))
        if Name != False:
            if InStr(M30.FileName(Name), 'Prog_Generator') == 0:
                if P01.MsgBox(M09.Get_Language_Str('Fehler: Der Dateiname muss \'Prog_Generator\' enthalten.' + vbCr + vbCr + 'Auswahl wiederholen?'), vbQuestion + vbOKCancel, M09.Get_Language_Str('Fehler: Falsche Datei ausgewählt')) == vbCancel:
                    Name = ''
                else:
                    Name = False
            if Name == PG.ThisWorkbook.FullName:
                Name = False
                if P01.MsgBox(M09.Get_Language_Str('Fehler: Die Daten können nicht aus der aktuellen Datei importiert werden.' + vbCr + vbCr + 'Auswahl wiederholen?'), vbQuestion + vbOKCancel, M09.Get_Language_Str('Fehler: Aktuelle Datei ausgewählt')) == vbCancel:
                    Name = ''
        else:
            Name = ''
        if Name != False:
            break
    if Name != '':
        TempName = M30.FilePath(Name) + '~' + M30.FileName(Name) + '~Temp.xlsm'
        if __Close_and_Delete_Temp_Prog_Gen(TempName):
            # VB2PY (UntranslatedCode) On Error GoTo Error_Copy
            FileCopy(Name, TempName)
            # VB2PY (UntranslatedCode) On Error GoTo 0
            fn_return_value = P01.Workbooks.Open(TempName, ReadOnly= True)
    ChDir(PG.ThisWorkbook.Path)
    P01.ChDrive(PG.ThisWorkbook.Path)
    return fn_return_value
    P01.MsgBox(M09.Get_Language_Str('Fehler beim kopieren der Datei') + vbCr + '  \'' + Name + '\' ' + M09.Get_Language_Str('nach') + vbCr + '  \'' + TempName + '\'', vbCritical, M09.Get_Language_Str('Fehler beim kopieren der alten Programm Generators'))
    ChDir(PG.ThisWorkbook.Path)
    P01.ChDrive(PG.ThisWorkbook.Path)
    return fn_return_value

def __Import_from_Old_Version_CallBack(Do_Import, Import_FromAllSheets):
    global __ImportWB
    #--------------------------------------------------------------------------------------------------
    Debug.Print('Import_from_Old_Version_CallBack(' + Do_Import + ', ' + Import_FromAllSheets + ')')
    if Do_Import:
        PGF_Name = P01.ActiveWorkbook.Path + '\\Import_From_old_Prog.MLL_pgf'
        Res = M18.Save_Sheets_to_pgf(PGF_Name, Import_FromAllSheets)
        __ImportWB.Close(Savechanges=False)
        PG.ThisWorkbook.Activate()
        if Res:
            Res = M18.Read_PGF(PGF_Name)
    else:
        __ImportWB.Close(Savechanges=False)
    __ImportWB = None

def Remove_Selection_in_Sheet(Sh):
    #----------------------------------------------------
    if M28.Is_Data_Sheet(Sh) and Sh.Visible == xlSheetVisible:
        Sh.Select()
        # VB2PY (UntranslatedCode) On Error Resume Next
        if P01.Selection.Cells.Count > 1:
            P01.Cells(P01.Selection.Row(), P01.Selection.Column()).Select()
        # VB2PY (UntranslatedCode) On Error GoTo 0

def Remove_Selections_in_all_Data_Sheets():
    OldSheet = String()

    Sh = P01.Worksheet

    ScrUpd = Boolean()
    #------------------------------------------------
    ScrUpd = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = False
    OldSheet = P01.ActiveSheet.Name
    for Sh in P01.sheets:
        Remove_Selection_in_Sheet(Sh)
    P01.Sheets(OldSheet).Select()
    P01.Application.ScreenUpdating = ScrUpd

def Import_from_Old_Version():
    global __ImportWB
    #-----------------------------------
    if P01.MsgBox(M09.Get_Language_Str('Mit dem folgenden Dialog wird die alte Version des Prog_Generatos ausgewählt ' + 'von der die Daten importiert werden sollen.'), vbOKCancel, M09.Get_Language_Str('Import der Daten von alter Programm Version')) == vbOK:
        __ImportWB = __Select_and_Open_Old_Version()
        if not __ImportWB is None:
            P01.Application.Visible = True
            Remove_Selections_in_all_Data_Sheets()
            Import_Hide_Unhide.Start('Import_from_Old_Version_CallBack')

def __Old_Version_exists():
    fn_return_value = None
    Name = Variant()

    Path = String()

    ActDir = String()
    #-----------------------------------------------
    ActDir = M30.FileName(PG.ThisWorkbook.Path)
    Path = M02.Get_MobaUserDir() + 'MobaLedLib_*'
    Name = Dir(Path, vbDirectory)
    while Name != '':
        if M30.FileName(Name) != ActDir:
            fn_return_value = True
            return fn_return_value
        Name = Dir()
    # Since Version 1.9.6 the data are stored in the directory "MobaLedlib" and use the prefix "Ver_"  ' 26.10.20:
    Path = M02.Get_MobaUserDir() + 'MobaLedLib\\Ver_*'
    Name = Dir(Path, vbDirectory)
    while Name != '':
        if M30.FileName(Name) != ActDir:
            fn_return_value = True
            return fn_return_value
        Name = Dir()
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: CheckExisting - ByVal 
def Import_from_Old_Version_If_exists(CheckExisting):
    #---------------------------------------------
    if CheckExisting == False or __Old_Version_exists():
        if P01.MsgBox(M09.Get_Language_Str('Sollen die Daten aus der alten Programm Version importiert werden?' + vbCr + 'Dieser Schritt kann auch Später über die \'Optionen/Dateien\' durchgeführt werden.' + vbCr + vbCr + 'Daten jetzt importieren?'), vbQuestion + vbYesNo, M09.Get_Language_Str('Importiren von Daten aus alter Version')) == vbYes:
            Import_from_Old_Version()

# VB2PY (UntranslatedCode) Option Explicit

