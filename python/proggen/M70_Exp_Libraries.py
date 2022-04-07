# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 4.02
# * Author: Harold Linke
# * Date: January 7, 2022
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
# 2021-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2022-01-07 v4.02 HL: - Else:,ByRef check done - first PoC release

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

#from proggen.M25_Columns import Make_sure_that_Col_Variables_match
#from ExcelAPI.P01_Workbook import (TimeValue, ActiveCell, create_workbook, IsError, Cells, Range, Sheets, Rows, Columns, IsEmpty, val, VarType, ChDrive, Format, 
#                                        MsgBox, InputBox, CWorkbook, CWorksheet, CRange, CRectangles, CSelection, CRow, CEntireRow, CColumn, CEntireColumn, CCell, CCellDict, CWorksheetFunction, CApplication, CFont, CActiveWindow, SoundLines)



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



# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Path - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ExpectedFilesLst - ByVal 
def __Check_Expected_Files(Path, ExpectedFilesLst):
    fn_return_value = None
    Name = Variant()
    #-------------------------------------------------------------------------------------------------------
    for Name in Split(ExpectedFilesLst, ' '):
        if Dir(Path + Name) == '':
            return fn_return_value
    fn_return_value = True
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Expected_DirName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ExpectedFilesLst - ByVal 
def __Make_Sure_that_GitHub_Library_Exists(Expected_DirName, ExpectedFilesLst):
    fn_return_value = None
    DestName_for_ZIP = String()

    ExtractedDirName = String()

    DestName = Variant()

    Path = String()
    #-----------------------------------------------------------------------------------------------------------------------------------
    DestName_for_ZIP = Expected_DirName + '.zip'
    ExtractedDirName = Expected_DirName + '-master'
    Path = M02.Get_Ardu_LibDir()
    M30.CreateFolder(Path)
    if Dir(Path + Expected_DirName, vbDirectory) != '':
        Debug.Print('Directory already exists: ' + Path + Expected_DirName)
        if __Check_Expected_Files(Path + Expected_DirName + '\\', ExpectedFilesLst):
            fn_return_value = True
            return fn_return_value
        else:
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Das Verzeichnis \'#1#\' existiert, es enthält aber ' + 'nicht alle der erwarteten Dateien:'), "#1#", Path + Expected_DirName) + vbCr + '  \'' + ExpectedFilesLst + '\'' + vbCr + vbCr + M09.Get_Language_Str('Das Verzeichnis muss manuell gelöscht werden!'), vbCritical, M09.Get_Language_Str('Fehler: Einige Dateien Fehlen'))
            return fn_return_value
    DestName = M02.Get_Ardu_LibDir() + DestName_for_ZIP
    if M37.WIN7_COMPATIBLE_DOWNLOAD:
        M30.F_shellExec('powershell Invoke-WebRequest "' + 'https://github.com/merose/AnalogScanner/archive/master.zip" -o:' + DestName + '"')
    else:
        if M37.Check_if_curl_is_Available_and_gen_Message_if_not('AnalogScanner', 'https://github.com/merose/AnalogScanner/archive/master.zip') == False:
            return fn_return_value
            # 05.06.20:
        M30.F_shellExec('powershell curl "' + 'https://github.com/merose/AnalogScanner/archive/master.zip" -o:' + DestName + '"')
    #   ToDo:
    #   - Erkennung von Fehlern
    # Unzip
    if not M30.UnzipAFile(DestName, Path):
        return fn_return_value
        # Wenn die Datei bereits existiert, dann wird eine Windows Meldung angezeigt
    if Dir(Path + ExtractedDirName, vbDirectory) == '':
        P01.MsgBox(M09.Get_Language_Str('Fehler beim entpacken der ZIP-Datei:') + vbCr + '  \'' + DestName + '\'', vbCritical, M09.Get_Language_Str('Fehler: Zip-Datei konnte nicht entpackt werden'))
        return fn_return_value
    else:
        # VB2PY (UntranslatedCode) On Error GoTo Error_Rename
        #Name(Path + ExtractedDirName + Expected_DirName)
        # VB2PY (UntranslatedCode) On Error GoTo 0
        if Dir(Path + Expected_DirName, vbDirectory) == '':
            # VB2PY (UntranslatedCode) GoTo Error_Rename
            pass
    fn_return_value = True
    # VB2PY (UntranslatedCode) On Error Resume Next
    Kill(DestName)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return fn_return_value
    P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler beim umbenennen des Verzeichnisses' + vbCr + '  \'#1#\'' + vbCr + 'nach' + vbCr + '  \'#2#\''), "#1#", ExtractedDirName), '#2#', Expected_DirName))
    return fn_return_value
    return fn_return_value

def __Test_Download_Exe():
    #UT----------------------------
    #Const Link_to_Exe_ZipFile = "https://www.hlinke.de/dokuwiki/lib/exe/fetch.php?media=de:mobaledcheckcolors_exe_v01.00.zip"
    # Download ins "Downloads" Verzeichnis. Die Web Seite bleibt offen
    #Shell "Explorer """ & Link_to_Exe_ZipFile & """"
    # Damit kann die Datei heruntergeladen werden ohne das eine Explorer Fenster offen bleibt             (Getestet mit Win7)
    #Shell "powershell Invoke-WebRequest """ & Link_to_Exe_ZipFile & """ -o:C:\Temp\TestDownload.zip"""
    # mit F_shellExec wird gewartet bis der download beendet ist
    # Das geht auch mit einer Exe auf GitHub: ("curl" ist eine Abkürzung für "Invoke-WebRequest")
    M30.F_shellExec('powershell curl "' + 'https://github.com/Hardi-St/MobaLedLib_Docu/blob/master/Tools/CheckColors/MobaLedCheckColors.exe?raw=true" -o:C:\\Temp\\DownloadTest\\MobaLedCheckColors.exe"')
    #   ToDo:
    #   - Erkennung von Fehlern
    ## VB2PY (CheckDirective) VB directive took path 1 on False
    # Unzip
    # VB2PY (UntranslatedCode) On Error Resume Next
    MkDir('C:\\Temp\\TestUnZip')
    # VB2PY (UntranslatedCode) On Error GoTo 0
    M30.UnzipAFile('C:\\Temp\\TestDownload.zip', 'C:\\Temp\\TestUnZip')

def Make_Sure_that_AnalogScanner_Library_Exists():
    fn_return_value = None
    #------------------------------------------------------------------------
    fn_return_value = __Make_Sure_that_GitHub_Library_Exists('AnalogScanner', 'AnalogScanner.cpp AnalogScanner.h')
    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
