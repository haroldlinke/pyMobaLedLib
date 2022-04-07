# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
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

from ExcelAPI.X01_Excel_Consts import *

import urllib.request 

import os

import proggen.M02_Public as M02
import proggen.M02_global_variables as M02GV
import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M08_Fast_ARDUINO as M08F
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
import proggen.M40_ShellandWait as M40
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80

import proggen.D02_Userform_Select_Typ_DCC as D02
import proggen.D09_StatusMsg_Userform as D09
import  proggen.F00_mainbuttons as F00

import ExcelAPI.P01_Workbook as P01

""" Install all required Libraries
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Make sure that all required libraries are installed
 - It's called every time when the program is started
 - All missing libraries are installed, also if they are needed only
   for a special project. Also the libraries needed for the Pattern_Configurator
   => more likely that the DetectVers are compatible
 - Hidden sheet "Libraries" contains all data
 ToDo:
 ~~~~~
 - Installation In SketchDir
   - Test
 - Aus irgend einem Grund funktioniert das Installieren der MobaLedLib mit einer "Required Version" nicht.
   Bei der "FastLED" und der "NmraDcc" geht es.
   Es geht auch nicht von Excel aus. Es kommt die Fehlermeldung:
      "Library MobaLedLib is already installed in: E:\Test Arduino Lib mit Ã¤\libraries\MobaLedLib"
   => Die Bibliothek muss von Hand gelöscht werden
   Manchmal geht es aber auch ?!?
----------------------------------------------------------------------
 Erkennung des Standard Arduino Boards
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Das Verwendete Nano board hängt von der installierten Arduino IDE ab. Es kann aber auch
 nachträglich eine anderes Board installiert werden. Das macht es kompliziert.

 Die installierte Arduino IDE Version kann man aus der Datei auslesen:
  C:\Program Files (x86)\Arduino\lib\version.txt enthält 1.8.12
 Die Folgende Tabelle enthält die Zusammenhänge.

 IDE      Board   GCC                         o.k. FastLed 3.3.3
 ~~~~     ~~~~~   ~~~                         ~~~~~~~~~~~~~~~~~~
 1.8.13   1.8.3   7.3.0-atmel3.6.1-arduino5
 1.8.12   1.8.2   7.3.0-atmel3.6.1-arduino5   Yes
 1.8.11   1.8.2   7.3.0-atmel3.6.1-arduino5   Yes
 1.8.10   1.8.1   7.3.0-atmel3.6.1-arduino5   Yes
 1.8.8    1.6.23  5.4.0-atmel3.6.1-arduino2   No   #define FL_FALLTHROUGH __attribute__ ((fallthrough));

 Arduino Releases: https://github.com/arduino/Arduino/releases

 In der Datei
   C:\Program Files (x86)\Arduino\hardware\package_index_bundled.json
 findet man die Standard Board Version. Hier für die IDE 1.8.8
   "version": "1.6.23",
 Bei der IDE Version ist
   "version": "1.6.23",
 eingetragen

 Wenn ein anderes Board installiert wurde, dann findet man die Version hier:
  C:\\Users\\Hardi\\AppData\\Local\Arduino15\\packages\\arduino\\hardware\\avr\\1.8.1

 Boards Manager Anzeigen von der Arduino IDE 1.8.12:
 Version 1.8.1:
   Arduino AVR Boards
   by Arduino Version 1.8.1
 Version 1.8.2:
   Built-In by Arduino Version 1.8.2

 => Das 'Built-In' zeigt, dass es die Standard mäßig in der Arduino IDE 1.8.12 enthalten Board Version ist

 Bei der installation des ATTinys kommt folgende Fehlermeldung:
 Warnung: nicht vertrauenswürdiger Beitrag, Skript-Ausführung wird übersprungen (C:\\Users\\Hardi\\AppData\\Local\\Arduino15\\packages\\ATTinyCore\\tools\\micronucleus\\2.5-azd1b\\post_install.bat)


"""

__First_Dat_Row = 9
__SelectRow_Col = 2
__Installed_Col = 3
__Lib_Board_Col = 4
__Libr_Name_Col = 5
__Test_File_Col = 6
__Reque_Ver_Col = 7
__DetectVer_Col = 8
__Other_Src_Col = 9
__UPDATE_LIB_CMD_NAME = 'Update_Libraries.cmd'
__RESTART_PROGGEN_CMD = 'Restart_ProgGen.cmd'
__UnzipList = String()
__Update_Time = Variant()
WIN7_COMPATIBLE_DOWNLOAD = True

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Is_Libraries_Select_Column(Target):
    fn_return_value = None
    #----------------------------------------------------------------------
    if Target.CountLarge == 1:
        fn_return_value = Target.Row >= __First_Dat_Row and Target.Column == __SelectRow_Col
    return fn_return_value

def Get_User_std_Arduino_Lib_Ver():
    fn_return_value = None
    OtherBoardDir = String()
    #-------------------------------------------------------
    OtherBoardDir = Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + 'packages\\arduino\\hardware\\avr\\'
    fn_return_value = M30.Get_First_SubDir(OtherBoardDir)
    return fn_return_value

def Get_Std_Arduino_Lib_Ver():
    fn_return_value = None
    BoardVer = String()

    ArduinoDir = String()
    #---------------------------------------------------
    # Std. Boards (Nano, Uno, ...)
    # The C:\Users\Hardi\AppData\Local\Arduino15\packages\arduino\hardware\avr\
    ArduinoDir = M30.FilePath(M08.Find_ArduinoExe())
    BoardVer = Get_User_std_Arduino_Lib_Ver()
    if BoardVer == '':
        Package_Index_Bundled = M30.Read_File_to_String(ArduinoDir + 'hardware/package_index_bundled.json')
        BoardVer = Replace(Replace(M30.Get_Ini_Entry(Package_Index_Bundled, '"version": "'), '"', ''), ',', '')
    fn_return_value = BoardVer
    return fn_return_value

def __Update_General_Versions():
    #Sh = Worksheet()

    #ArduinoDir = String()

    #ArduinoVer = String()
    #------------------------------------
    # Update the general versions in the Libraries sheet
    # - Arduino IDE
    # - Std. Boards (Nano, Uno, ...)
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    # Arduino IDE
    ArduinoDir = M30.FilePath(M08.Find_ArduinoExe())
    ArduinoVer = M30.Read_File_to_String(ArduinoDir + 'lib/version.txt')
    Sh.Range_set('Arduino_IDE_Ver', ArduinoVer)
    # Std. Boards (Nano, Uno, ...)
    Sh.Range_set('Std_Boards_Ver', Get_Std_Arduino_Lib_Ver())

def __Get_DetectVer_form_library_properties(LibDir):
    fn_return_value = None
    Name = String()

    FileStr = String()
    #-------------------------------------------------------------------------------------------------------------
    Name = LibDir + 'library.properties'
    if Dir(Name) != '':
        FileStr = M30.Read_File_to_String(Name)
        if FileStr != '#ERROR#':
            fn_return_value = M30.Get_Ini_Entry(FileStr, 'version=')
    else:
        fn_return_value = '?'
    return fn_return_value

def __Test_Get_State_of_Board_Row():
    #UT--------------------------------------
    __Get_State_of_Board_Row(21)

def __Get_State_of_Board_Row(Row):
    #Sh = Worksheet()

    #BoardDir = String()

    #TestFile = String()

    #Board_and_Proc = String()

    #Board = String()

    #ProcessorTyp = String()

    VerList = "" #String()

    #Res = String()

    #Ver = Variant()
    #----------------------------------------------
    # Don't know how the boards are treated. In the boards manager of the Arduino IDE the first (in alphabetical order)
    # board is shown. Old "libraries" directories are not (always) deleted if a new version is installed ;-(
    # But (sometimes) the old directories are empty.
    # The first not empty directory is listed.
    #
    # We assume the following structure:
    #                                                  Name                  Processor  Version             TestFile
    #                                                  ~~~~~~~~~~            ~~~~~~~~~  ~~~~~~~             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # "C:\Users\Hardi\AppData\Local\Arduino15\packages\ATTinyCore\ hardware\ avr\       1.3.2\   libraries\ ATTinyCore\src\ATTinyCore.h"
    # "C:\Users\Hardi\AppData\Local\Arduino15\packages\esp8266   \ hardware\ esp8266\   2.3.0\   libraries\ ESP8266AVRISP\src\ESP8266AVRISP.h"
    # "C:\Users\Hardi\AppData\Local\Arduino15\packages\arduino   \ hardware\ megaavr\   1.6.26\  libraries\ Wire\src\Wire.h"
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    Board_and_Proc = Sh.Cells(Row, __Libr_Name_Col)
    Board = Split(Board_and_Proc, ':')(0)
    ProcessorTyp = Split(Board_and_Proc, ':')(1)
    if Board == 'arduino' and ProcessorTyp == 'avr':
        Sh.CellDict[Row, __Installed_Col] = 1
        Sh.CellDict[Row, __DetectVer_Col] = Get_Std_Arduino_Lib_Ver()
        return
    TestFile = Sh.Cells(Row, __Test_File_Col)
    BoardDir = Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + 'packages/' + Board + '/hardware/'
    Res = Dir(BoardDir + ProcessorTyp + '/*.*', vbDirectory)
    while Res != '':
        if Left(Res, 1) != '.':
            VerList = VerList + Res + vbTab
        Res = Dir()
    VerList = M30.DelLast(VerList)
    for Ver in Split(VerList, vbTab):
        DirName = BoardDir + ProcessorTyp + '/' + Ver + '/libraries/'
        if not M30.Dir_is_Empty(DirName):
            with_0 = Sh.Cells(Row, __Installed_Col)
            if Dir(DirName + TestFile) != '':
                Sh.CellDict[Row, __DetectVer_Col] = Ver
                with_0.Value = 1
            else:
                with_0.Value = ''
            return

def __Get_State_of_BoardExtras_Row(Row):
    #Sh = Worksheet()

    #BoardDir = String()

    #TestFile = String()

    #Board_and_Proc = String()

    #Board = String()

    #ExtraType = String()

    VerList = "" #String()

    Res = "" #String()

    Ver = Variant()
    #----------------------------------------------
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    Board_and_Proc = Sh.Cells(Row, __Libr_Name_Col)
    Board = Split(Board_and_Proc, ':')(0)
    ExtraType = Split(Board_and_Proc, ':')(1)
    TestFile = Sh.Cells(Row, __Test_File_Col)
    BoardDir = Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + 'packages/' + Board
    Res = Dir(BoardDir + '\\' + ExtraType + '/*.*', vbDirectory)
    while Res != '':
        if Left(Res, 1) != '.':
            VerList = VerList + Res + vbTab
        Res = Dir()
    VerList = M30.DelLast(VerList)
    for Ver in Split(VerList, vbTab):
        DirName = BoardDir + '/' + ExtraType + '/' + Ver
        if not M30.Dir_is_Empty(DirName):
            with_1 = Sh.Cells(Row, __Installed_Col)
            if Dir(DirName + '/' + TestFile) != '':
                Sh.CellDict[Row, __DetectVer_Col] = Ver
                with_1.Value = 1
            else:
                with_1.Value = ''
            return

def __Get_All_Library_States():
    fn_return_value = None
    LibrariesDir = String()

    Row = int()

    #Sh = Worksheet()
    #---------------------------------------------------
    # Get the states of all libraries:
    # - Installed
    # - DetectVer
    if M02.Read_Sketchbook_Path_from_preferences_txt() == False:
        return fn_return_value
    P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH).Range_set('Sketchbook_Path',M02.Sketchbook_Path)
    LibrariesDir = M02.Sketchbook_Path + '/libraries/'
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    Row = __First_Dat_Row
    while Sh.Cells(Row, __Libr_Name_Col) != '':
        TestFile = Sh.Cells(Row, __Test_File_Col)
        Sh.CellDict[Row, __DetectVer_Col] = ''
        Sh.CellDict[Row, __Installed_Col] = ''
        if InStr(Sh.Cells(Row, __Lib_Board_Col), 'L') > 0:
            # *** Library ***
            LibDir = LibrariesDir + Sh.Cells(Row, __Libr_Name_Col) + '/'
            with_2 = Sh.Cells(Row, __Installed_Col)
            with_2.Value = ''
            # VB2PY (UntranslatedCode) On Error GoTo ErrDontExist
            if os.path.isdir(LibDir): # Dir(LibDir, vbDirectory) != '':
                if os.path.exists(LibDir + TestFile) or os.path.exists(LibDir + 'src/' + TestFile): #Dir(LibDir + TestFile) != '' or Dir(LibDir + 'src\\' + TestFile) != '':
                    with_2.Value = '1'
                else:
                    P01.MsgBox(M09.Get_Language_Str('Fehler beim lesen des Verzeichnisses:') + vbCr + '  \'' + LibDir + '\'' + vbCr + 'Error Nr: ' + Err.Number + vbCr + Err.Description, vbCritical, M09.Get_Language_Str('Fehler beim lesen des Verzeichnisses:'))
            # VB2PY (UntranslatedCode) On Error GoTo 0
            installed = Sh.Cells(Row, __Installed_Col)
            if installed == "":
                installed = 0
            if int(installed) > 0:
                Sh.CellDict[Row, __DetectVer_Col] = __Get_DetectVer_form_library_properties(LibDir)
        elif InStr(Sh.Cells(Row, __Lib_Board_Col), 'BE') > 0:
            # *** Board Extras ***
            __Get_State_of_BoardExtras_Row(Row)
        elif InStr(Sh.Cells(Row, __Lib_Board_Col), 'B') > 0:
            # *** Board ***
            __Get_State_of_Board_Row(Row)
        Row = Row + 1
    fn_return_value = True
    P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH).Range_set('Last_Update_Time',P01.Date_str() + P01.Time_str())
    return fn_return_value
    # 07.06.20:
    P01.MsgBox(M09.Get_Language_Str('Fehler beim lesen des Verzeichnisses:') + vbCr + '  \'' + LibDir + '\'' + vbCr + 'Error Nr: ' + Err.Number + vbCr + Err.Description, vbCritical, M09.Get_Language_Str('Fehler beim lesen des Verzeichnisses:'))
    # VB2PY (UntranslatedCode) Resume DontExist
    return fn_return_value

def Check_if_curl_is_Available_and_gen_Message_if_not(Name, InstLink):
    fn_return_value = None
    #---------------------------------------------------------------------------------------------------------------
    if M30.Win10_or_newer():
        fn_return_value = True
        return fn_return_value
    P01.MsgBox(Replace(M09.Get_Language_Str('Die Programme \'curl\' und \'tar\' sind erst ab Win10 verfügbar. ' + 'Darum kann \'#1#\' nicht automatisch installiert werden ;-(' + vbCr + 'Es kann manuell von hier installiert werden:'), "#1#", Name) + vbCr + '  \'' + InstLink + '\'' + vbCr + vbCr, vbInformation, M09.Get_Language_Str('Windows Version ist zu alt. Keine automatische Installation möglich'))
    return fn_return_value

def __Add_Update_from_Other_Source(fp, Row):
    global __UnzipList
    #Sh = Worksheet()

    #LibName = String()

    #InstLink = String()
    #-------------------------------------------------------------------
    # Creates:
    #   powershell Invoke-WebRequest "https://github.com/merose/AnalogScanner/archive/master.zip" -o:AnalogScanner.zip
    # Or if WIN7_COMPATIBLE_DOWNLOAD is not defined:
    #   curl -LJO https://github.com/merose/AnalogScanner/archive/master.zip
    #   tar  -xf AnalogScanner-master.zip
    #   ren  AnalogScanner-master AnalogScanner
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    LibName = Sh.Cells(Row, __Libr_Name_Col)
    InstLink = Trim(Sh.Cells(Row, __Other_Src_Col))
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'ECHO ' + M30.Replicate('*', Len('Updating ' + LibName + '...')), '\n')
    VBFiles.writeText(fp, 'ECHO Updating ' + LibName + '...', '\n')
    VBFiles.writeText(fp, 'ECHO ' + M30.Replicate('*', Len('Updating ' + LibName + '...')), '\n')
    VBFiles.writeText(fp, 'if EXIST ' + LibName + '\\NUL (', '\n')
    VBFiles.writeText(fp, '   ECHO deleting old directory ' + LibName + '\\', '\n')
    VBFiles.writeText(fp, '   rmdir ' + LibName + '\\ /s /q', '\n')
    VBFiles.writeText(fp, '   REM timeout /T 3 /nobreak', '\n')
    VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, 'if EXIST ' + LibName + '\\NUL (', '\n')
    VBFiles.writeText(fp, '   ECHO Error deleting old directory ' + LibName + '\\', '\n')
    VBFiles.writeText(fp, '   ECHO For some reasons the directory could not be deleted ;-(', '\n')
    VBFiles.writeText(fp, '   ECHO Check if an other program is active which prevents the deleting', '\n')
    VBFiles.writeText(fp, '   ECHO of the directory', '\n')
    VBFiles.writeText(fp, '   ECHO.', '\n')
    VBFiles.writeText(fp, '   ECHO Going to try a second time', '\n')
    VBFiles.writeText(fp, '   PAUSE', '\n')
    VBFiles.writeText(fp, '   rmdir ' + LibName + '\\ /s /q', '\n')
    VBFiles.writeText(fp, '   timeout /T 3 /nobreak', '\n')
    VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, 'if EXIST ' + LibName + '\\NUL (', '\n')
    VBFiles.writeText(fp, '   COLOR 4F', '\n')
    VBFiles.writeText(fp, '   ECHO Error: Still not able to delete the old directory ' + LibName + '\\   ;-(((', '\n')
    VBFiles.writeText(fp, '   PAUSE', '\n')
    VBFiles.writeText(fp, ')', '\n')
    if WIN7_COMPATIBLE_DOWNLOAD:
        VBFiles.writeText(fp, 'powershell Invoke-WebRequest "' + InstLink + '" -o:' + LibName + '.zip', '\n')
        VBFiles.writeText(fp, 'ECHO Invoke-WebRequest result: %ERRORLEVEL%', '\n')
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 Goto ErrorMsg', '\n')
        __UnzipList = __UnzipList + LibName + vbTab
    else:
        if Check_if_curl_is_Available_and_gen_Message_if_not(LibName, InstLink) == False:
            return
        VBFiles.writeText(fp, 'curl -LJ "' + InstLink + '" --output ' + LibName + '.zip', '\n')
        VBFiles.writeText(fp, 'ECHO curl result: %ERRORLEVEL%', '\n')
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 Goto ErrorMsg', '\n')
        VBFiles.writeText(fp, 'tar -xmf ' + LibName + '.zip', '\n')
        VBFiles.writeText(fp, 'ECHO tar  result: %ERRORLEVEL%', '\n')
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 Goto ErrorMsg', '\n')
        VBFiles.writeText(fp, 'ren ' + LibName + '-master ' + LibName, '\n')
        VBFiles.writeText(fp, 'ECHO ren  result: %ERRORLEVEL%', '\n')
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 GOTO ErrorMsg', '\n')
        VBFiles.writeText(fp, 'if EXIST ' + LibName + '.zip del ' + LibName + '.zip', '\n')
    VBFiles.writeText(fp, 'ECHO.', '\n')
    #  Print #fp, "PAUSE" ' Debug
    VBFiles.writeText(fp, '', '\n')
    
def __Add_Update_from_Other_Source_Linux(Row):
    global __UnzipList
    #Sh = Worksheet()

    #LibName = String()

    #InstLink = String()
    #-------------------------------------------------------------------
    # Creates:
    #   powershell Invoke-WebRequest "https://github.com/merose/AnalogScanner/archive/master.zip" -o:AnalogScanner.zip
    # Or if WIN7_COMPATIBLE_DOWNLOAD is not defined:
    #   curl -LJO https://github.com/merose/AnalogScanner/archive/master.zip
    #   tar  -xf AnalogScanner-master.zip
    #   ren  AnalogScanner-master AnalogScanner
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    LibName = Sh.Cells(Row, __Libr_Name_Col)
    InstLink = Trim(Sh.Cells(Row, __Other_Src_Col))
    #VBFiles.writeText(fp, '', '\n')
    Debug.Print('ECHO ' + M30.Replicate('*', Len('Updating ' + LibName + '...')), '\n')
    Debug.Print('ECHO Updating ' + LibName + '...', '\n')
    Debug.Print('ECHO ' + M30.Replicate('*', Len('Updating ' + LibName + '...')), '\n')
    Debug.Print('if EXIST ' + LibName + '\\NUL (', '\n')
    Debug.Print('   ECHO deleting old directory ' + LibName + '\\', '\n')
    Debug.Print('   rmdir ' + LibName + '\\ /s /q', '\n')
    Debug.Print('   REM timeout /T 3 /nobreak', '\n')
    Debug.Print(')', '\n')
    Debug.Print('if EXIST ' + LibName + '\\NUL (', '\n')
    Debug.Print('   ECHO Error deleting old directory ' + LibName + '\\', '\n')
    Debug.Print('   ECHO For some reasons the directory could not be deleted ;-(', '\n')
    Debug.Print('   ECHO Check if an other program is active which prevents the deleting', '\n')
    Debug.Print('   ECHO of the directory', '\n')
    Debug.Print('   ECHO.', '\n')
    Debug.Print('   ECHO Going to try a second time', '\n')
    Debug.Print('   PAUSE', '\n')
    Debug.Print('   rmdir ' + LibName + '\\ /s /q', '\n')
    Debug.Print('   timeout /T 3 /nobreak', '\n')
    Debug.Print(')', '\n')
    Debug.Print('if EXIST ' + LibName + '\\NUL (', '\n')
    Debug.Print( '   COLOR 4F', '\n')
    Debug.Print('   ECHO Error: Still not able to delete the old directory ' + LibName + '\\   ;-(((', '\n')
    Debug.Print('   PAUSE', '\n')
    Debug.Print(')', '\n')
    
    try:
        shutil.rmtree(LibName)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    
    
    if WIN7_COMPATIBLE_DOWNLOAD:
        Debug.Print( 'powershell Invoke-WebRequest "' + InstLink + '" -o:' + LibName + '.zip', '\n')
        Debug.Print( 'ECHO Invoke-WebRequest result: %ERRORLEVEL%', '\n')
        #VBFiles.writeText(fp, 'IF ERRORLEVEL 1 Goto ErrorMsg', '\n')
        urllib.request.urlretrieve(InstLink, LibName + '.zip')
        
        __UnzipList = __UnzipList + LibName + vbTab
    else:
        if Check_if_curl_is_Available_and_gen_Message_if_not(LibName, InstLink) == False:
            return
        VBFiles.writeText(fp, 'curl -LJ "' + InstLink + '" --output ' + LibName + '.zip', '\n')
        VBFiles.writeText(fp, 'ECHO curl result: %ERRORLEVEL%', '\n')
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 Goto ErrorMsg', '\n')
        VBFiles.writeText(fp, 'tar -xmf ' + LibName + '.zip', '\n')
        VBFiles.writeText(fp, 'ECHO tar  result: %ERRORLEVEL%', '\n')
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 Goto ErrorMsg', '\n')
        VBFiles.writeText(fp, 'ren ' + LibName + '-master ' + LibName, '\n')
        VBFiles.writeText(fp, 'ECHO ren  result: %ERRORLEVEL%', '\n')
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 GOTO ErrorMsg', '\n')
        VBFiles.writeText(fp, 'if EXIST ' + LibName + '.zip del ' + LibName + '.zip', '\n')
    #VBFiles.writeText(fp, 'ECHO.', '\n')
    #  Print #fp, "PAUSE" ' Debug
    #VBFiles.writeText(fp, '', '\n')

def __Proc_UnzipList():
    global __UnzipList
    try:
        if __UnzipList == "":
            return
        LibName = Variant()
    
        LibName_with_path = String()
        #---------------------------
        __UnzipList = M30.DelLast(__UnzipList)
        for LibName in Split(__UnzipList, vbTab):
            LibName_with_path = M02.Get_Ardu_LibDir() + LibName
            if not M30.UnzipAFile(LibName_with_path + '.zip', M02.Get_Ardu_LibDir()):
                return
            if os.path.isdir(LibName_with_path + '-master'): # Dir(LibName_with_path + '-master', vbDirectory) != '':
                # VB2PY (UntranslatedCode) On Error GoTo RenameErr
                os.rename(LibName_with_path + '-master', LibName_with_path)
            elif os.path.isdir(LibName_with_path + '-beta'): # Dir(LibName_with_path + '-beta', vbDirectory) != '':
                # VB2PY (UntranslatedCode) On Error GoTo RenameErr
                os.rename(LibName_with_path + '-beta', LibName_with_path)
            else:
                P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Das Verzeichnis \'#1#\' wurde nicht erzeugt beim entzippen von:'), "#1#", LibName + '-master') + vbCr + '  \'' + LibName_with_path + '.zip', vbCritical, M09.Get_Language_Str('Fehler beim entzippen'))
            # VB2PY (UntranslatedCode) On Error Resume Next
            try:
                Kill(LibName_with_path + '.zip')
            except:
                pass
            # VB2PY (UntranslatedCode) On Error GoTo 0
        return
    except:
        P01.MsgBox(M09.Get_Language_Str('Fehler beim Umbenennen des Verzeichnisses:') + vbCr + '  \'' + LibName_with_path + '-master\'' + vbCr + 'nach \'...' + LibName + '\'', vbCritical, M09.Get_Language_Str('Verzeichnis kann nicht umbenannt werden'))
    # VB2PY (UntranslatedCode) Resume Next

def Init_Libraries_Page():
    #-------------------------------
    #*HLP01.ThisWorkbook.Sheets(M02.LIBRARYS__SH).CheckBoxes['Check Box 10'] = xlOff
    pass

def __Create_Do_Update_Script(Pause_at_End):
    global __UPDATE_LIB_CMD_NAME
    fn_return_value = None
    fp = Integer()

    Name = String()

    UpdCnt = int()

    LibList = String()

    BrdList = String()

    URLList = String()

    Row = int()

    #Sh = Worksheet()

    ForceReinstall = Boolean()
    #------------------------------------------------------------------------
    # Updates all selected libraries
    #
    # Arduino parameters see:
    #  https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc
    # Return: -1 in case of an error
    #          0 if nothing has to be updated
    #          n number of necessary updates
    fp = FreeFile()
    Name = P01.ThisWorkbook.Path + '/' + __UPDATE_LIB_CMD_NAME
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'Color 80', '\n')
    VBFiles.writeText(fp, 'REM This file was generated by \'' + P01.ThisWorkbook.Name + '\'  ' + Time, '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM It updates/installs all required libraries for the MobaLedLib projects.', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM Attention:', '\n')
    VBFiles.writeText(fp, 'REM This program must be started from the arduino libraries directory', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, '', '\n')
    if M30.Win10_or_newer():
        VBFiles.writeText(fp, 'CHCP 65001 >NUL', '\n')
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    ForceReinstall = False
    if False: #*HLSh.CheckBoxes('Check Box 10').Value == xlOn:
        Pause_at_End = True
        # Wait at End Checkbox
    Row = __First_Dat_Row
    while Sh.Cells(Row, __Libr_Name_Col) != '':
        if Sh.Cells(Row, __SelectRow_Col) != '':
            UpdCnt = UpdCnt + 1
            if InStr(Sh.Cells(Row, __Lib_Board_Col), 'L') > 0:
                if Sh.Cells(Row, __Other_Src_Col) == '':
                    LibList = LibList + '"' + Sh.Cells(Row, __Libr_Name_Col)
                    if Trim(Sh.Cells(Row, __Reque_Ver_Col)) != '':
                        LibList = LibList + ':' + Sh.Cells(Row, __Reque_Ver_Col)
                    LibList = LibList + '",'
                    # 19.10.21: Juergen Workaround for problem that libraries with 'unknown' versions are not updated
                    if Sh.Cells(Row, __Libr_Name_Col) == 'NmraDcc' and  ( Sh.Cells(Row, __DetectVer_Col) == '2.0.7' or Sh.Cells(Row, __DetectVer_Col) == '2.0.8' ) :
                        M30.Del_Folder(M02.Sketchbook_Path + '/libraries/' + Sh.Cells(Row, __Libr_Name_Col))
                    ForceReinstall = True
                else:
                    __Add_Update_from_Other_Source(fp, Row)
                    ForceReinstall = True
            elif InStr(Sh.Cells(Row, __Lib_Board_Col), 'BE') > 0:
                # skip these extra files
                pass
            elif InStr(Sh.Cells(Row, __Lib_Board_Col), 'B') > 0:
                # Board
                BrdList = BrdList + Sh.Cells(Row, __Libr_Name_Col)
                if Trim(Sh.Cells(Row, __Reque_Ver_Col)) != '':
                    BrdList = BrdList + ':' + Sh.Cells(Row, __Reque_Ver_Col)
                BrdList = BrdList + ','
                ForceReinstall = True
                if Sh.Cells(Row, __Other_Src_Col) != '':
                    if InStr(URLList, Sh.Cells(Row, __Other_Src_Col) + ',') == 0:
                        URLList = URLList + Sh.Cells(Row, __Other_Src_Col) + ','
                M08F.Create_Packages_Dir_if_not_Available()
                Board_and_Proc = Sh.Cells(Row, __Libr_Name_Col)
                Board = Split(Board_and_Proc, ':')(0)
                BoardDir = Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + 'packages/' + Board
                if Dir(BoardDir, vbDirectory) != '':
                    Debug.Print('Deleting: ' + BoardDir)
                    M30.Del_Folder(BoardDir)
        Row = Row + 1
    if ForceReinstall == True:
        if Dir(Environ(M02.Env_USERPROFILE) + '/AppData/Local/Temp/MobaLedLib_build/ESP32/includes.cache') != '':
            Kill(Environ(M02.Env_USERPROFILE) + '/AppData/Local/Temp/MobaLedLib_build/ESP32/includes.cache')
    # *** Libraries ***
    if LibList != '':
        LibList = M30.DelLast(LibList)
        VBFiles.writeText(fp, 'ECHO ************************************', '\n')
        VBFiles.writeText(fp, 'ECHO  Installing the following libraries', '\n')
        VBFiles.writeText(fp, 'ECHO ************************************', '\n')
        for Lib in Split(LibList, ','):
            VBFiles.writeText(fp, 'ECHO   ' + Replace(Lib, '"', ''), '\n')
        VBFiles.writeText(fp, 'ECHO.', '\n')
        # 09.03.21 Juergen: delete cache file to force an ESP32 rebuild, otherwise prebuild library versions would still be used
        VBFiles.writeText(fp, '@if exist "%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache" del "%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache"', '\n')
        VBFiles.writeText(fp, '"' + M08.Find_ArduinoExe() + '"')
        VBFiles.writeText(fp, ' --install-library ' + LibList)
        VBFiles.writeText(fp, ' 2>&1 | find /v " StatusLogger " | find /v " INFO c.a" | find /v " WARN p.a" | find /v " WARN c.a"', '\n')
        VBFiles.writeText(fp, 'ECHO.', '\n')
        VBFiles.writeText(fp, 'ECHO Error %ERRORLEVEL%', '\n')
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 Goto ErrorMsg', '\n')
        VBFiles.writeText(fp, '', '\n')
    # *** Boards ***
    if BrdList != '':
        BrdList = M30.DelLast(BrdList)
        URLList = M30.DelLast(URLList)
        VBFiles.writeText(fp, 'ECHO *********************************', '\n')
        VBFiles.writeText(fp, 'ECHO  Installing the following boards', '\n')
        VBFiles.writeText(fp, 'ECHO *********************************', '\n')
        for Brd in Split(BrdList, ','):
            VBFiles.writeText(fp, 'ECHO   ' + Brd, '\n')
        VBFiles.writeText(fp, 'ECHO.', '\n')
        # 09.03.21 Juergen: delete cache file to force an ESP32 rebuild, otherwise prebuild library versions would still be used
        VBFiles.writeText(fp, '@if exist "%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache" del "%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache"', '\n')
        for Brd in Split(BrdList, ','):
            VBFiles.writeText(fp, '"' + M08.Find_ArduinoExe() + '"')
            VBFiles.writeText(fp, ' --install-boards ' + Brd)
            if URLList != '':
                VBFiles.writeText(fp, ' --pref "boardsmanager.additional.urls=' + URLList + '"')
            VBFiles.writeText(fp, ' 2>&1 | find /v " StatusLogger " | find /v " INFO c.a" | find /v " WARN p.a" | find /v " WARN c.a"', '\n')
            VBFiles.writeText(fp, 'ECHO.', '\n')
            VBFiles.writeText(fp, 'ECHO Error %ERRORLEVEL%', '\n')
            VBFiles.writeText(fp, 'IF ERRORLEVEL 1 Goto ErrorMsg', '\n')
            VBFiles.writeText(fp, '', '\n')
    #Print #fp, "Pause" ' Debug
    if Pause_at_End:
        VBFiles.writeText(fp, 'Pause', '\n')
    VBFiles.writeText(fp, 'Exit', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, ':ErrorMsg', '\n')
    VBFiles.writeText(fp, '   COLOR 4F', '\n')
    VBFiles.writeText(fp, '   ECHO   ****************************************', '\n')
    VBFiles.writeText(fp, '   ECHO    Da ist was schief gegangen ;-(', '\n')
    VBFiles.writeText(fp, '   ECHO   ****************************************', '\n')
    VBFiles.writeText(fp, '   Pause', '\n')
    VBFiles.closeFile(fp)
    fn_return_value = UpdCnt
    return fn_return_value
    VBFiles.closeFile(fp)
    P01.MsgBox(M09.Get_Language_Str('Fehler beim Schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Start Datei'))
    fn_return_value = - 1
    return fn_return_value

def __Create_Do_Update_Script_Linux_part1(Pause_at_End):

    fn_return_value = None
    fp = Integer()

    Name = String()

    UpdCnt = 0 #int()

    LibList = "" #String()

    BrdList = "" #String()
    
    OthersourceList = ""

    URLList = String()

    Row = int()

    #Sh = Worksheet()

    ForceReinstall = Boolean()
    #------------------------------------------------------------------------
    # Updates all selected libraries
    #
    # Arduino parameters see:
    #  https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc
    # Return: -1 in case of an error
    #          0 if nothing has to be updated
    #          n number of necessary updates
    
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    ForceReinstall = False
    if False: #*HLSh.CheckBoxes('Check Box 10').Value == xlOn:
        Pause_at_End = True
        # Wait at End Checkbox
    Row = __First_Dat_Row
    while Sh.Cells(Row, __Libr_Name_Col) != '':
        if Sh.Cells(Row, __SelectRow_Col) != '':
            UpdCnt = UpdCnt + 1
            if InStr(Sh.Cells(Row, __Lib_Board_Col), 'L') > 0:
                if Sh.Cells(Row, __Other_Src_Col) == '':
                    LibList = LibList + '"' + Sh.Cells(Row, __Libr_Name_Col)
                    if Trim(Sh.Cells(Row, __Reque_Ver_Col)) != '':
                        LibList = LibList + ':' + Sh.Cells(Row, __Reque_Ver_Col)
                    LibList = LibList + '",'
                    # 19.10.21: Juergen Workaround for problem that libraries with 'unknown' versions are not updated
                    if Sh.Cells(Row, __Libr_Name_Col) == 'NmraDcc' and  ( Sh.Cells(Row, __DetectVer_Col) == '2.0.7' or Sh.Cells(Row, __DetectVer_Col) == '2.0.8' ) :
                        M30.Del_Folder(M02.Sketchbook_Path + '/libraries/' + Sh.Cells(Row, __Libr_Name_Col))
                    ForceReinstall = True
                else:
                    #*HL __Add_Update_from_Other_Source(fp, Row)
                    OthersourceList = OthersourceList + str(Row)+","
                    ForceReinstall = True
            elif InStr(Sh.Cells(Row, __Lib_Board_Col), 'BE') > 0:
                # skip these extra files
                pass
            elif InStr(Sh.Cells(Row, __Lib_Board_Col), 'B') > 0:
                # Board
                BrdList = BrdList + Sh.Cells(Row, __Libr_Name_Col)
                if Trim(Sh.Cells(Row, __Reque_Ver_Col)) != '':
                    BrdList = BrdList + ':' + Sh.Cells(Row, __Reque_Ver_Col)
                BrdList = BrdList + ','
                ForceReinstall = True
                if Sh.Cells(Row, __Other_Src_Col) != '':
                    if InStr(URLList, Sh.Cells(Row, __Other_Src_Col) + ',') == 0:
                        URLList = URLList + Sh.Cells(Row, __Other_Src_Col) + ','
                M08F.Create_Packages_Dir_if_not_Available()
                Board_and_Proc = Sh.Cells(Row, __Libr_Name_Col)
                Board = Split(Board_and_Proc, ':')(0)
                BoardDir = Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + 'packages/' + Board
                if Dir(BoardDir, vbDirectory) != '':
                    Debug.Print('Deleting: ' + BoardDir)
                    M30.Del_Folder(BoardDir)
        Row = Row + 1
    if ForceReinstall == True:
        if Dir(Environ(M02.Env_USERPROFILE) + '/AppData/Local/Temp/MobaLedLib_build/ESP32/includes.cache') != '':
            Kill(Environ(M02.Env_USERPROFILE) + '/AppData/Local/Temp/MobaLedLib_build/ESP32/includes.cache')
    return UpdCnt,LibList,BrdList,OthersourceList

def __Create_Do_Update_Script_Linux_part2(LibList, BrdList,OthersourceList):

    # *** Libraries ***
    if LibList != '':
        LibList = M30.DelLast(LibList)
        Debug.Print('ECHO ************************************', '\n')
        Debug.Print('ECHO  Installing the following libraries', '\n')
        Debug.Print('ECHO ************************************', '\n')
        for Lib in Split(LibList, ','):
            Debug.Print('ECHO   ' + Replace(Lib, '"', ''), '\n')
        Debug.Print('ECHO.', '\n')
        # 09.03.21 Juergen: delete cache file to force an ESP32 rebuild, otherwise prebuild library versions would still be used
        Debug.Print('@if exist "%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache" del "%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache"', '\n')
        
        CommandStr = '"' + M08.Find_ArduinoExe() + '"' + ' --install-library ' + LibList
        Res = M40.ShellAndWait(CommandStr, 0, vbNormalFocus, M40.PromptUser)        
        #VBFiles.writeText(fp, ' 2>&1 | find /v " StatusLogger " | find /v " INFO c.a" | find /v " WARN p.a" | find /v " WARN c.a"', '\n')
        #VBFiles.writeText(fp, 'ECHO.', '\n')
        #VBFiles.writeText(fp, 'ECHO Error %ERRORLEVEL%', '\n')
        #VBFiles.writeText(fp, 'IF ERRORLEVEL 1 Goto ErrorMsg', '\n')
        #VBFiles.writeText(fp, '', '\n')
        if Res!=M40.Success:
            return Res
    # *** Boards ***
    if BrdList != '':
        BrdList = M30.DelLast(BrdList)
        URLList = M30.DelLast(URLList)
        Debug.Print('ECHO *********************************', '\n')
        Debug.Print('ECHO  Installing the following boards', '\n')
        Debug.Print('ECHO *********************************', '\n')
        for Brd in Split(BrdList, ','):
            Debug.Print('ECHO   ' + Brd, '\n')
        Debug.Print('ECHO.', '\n')
        # 09.03.21 Juergen: delete cache file to force an ESP32 rebuild, otherwise prebuild library versions would still be used
        #VBFiles.writeText(fp, '@if exist "%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache" del "%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache"', '\n')
        for Brd in Split(BrdList, ','):
            
            #VBFiles.writeText(fp, '"' + M08.Find_ArduinoExe() + '"')
            #VBFiles.writeText(fp, ' --install-boards ' + Brd)
            if URLList != '':
                VBFiles.writeText(fp, ' --pref "boardsmanager.additional.urls=' + URLList + '"')
                
            CommandStr = '"' + M08.Find_ArduinoExe() + '"' + ' --install-boards ' + Brd
            if URLList != '':
                CommandStr= CommandStr +' --pref "boardsmanager.additional.urls=' + URLList + '"'
            Res = M40.ShellAndWait(CommandStr, 0, vbNormalFocus, M40.PromptUser)                        
            #VBFiles.writeText(fp, ' 2>&1 | find /v " StatusLogger " | find /v " INFO c.a" | find /v " WARN p.a" | find /v " WARN c.a"', '\n')
            #VBFiles.writeText(fp, 'ECHO.', '\n')
            #VBFiles.writeText(fp, 'ECHO Error %ERRORLEVEL%', '\n')
            #VBFiles.writeText(fp, 'IF ERRORLEVEL 1 Goto ErrorMsg', '\n')
            #VBFiles.writeText(fp, '', '\n')
    #Print #fp, "Pause" ' Debug
    #if Pause_at_End:
    #    VBFiles.writeText(fp, 'Pause', '\n')
    #VBFiles.writeText(fp, 'Exit', '\n')
    #VBFiles.writeText(fp, '', '\n')
    #VBFiles.writeText(fp, ':ErrorMsg', '\n')
    #VBFiles.writeText(fp, '   COLOR 4F', '\n')
    #VBFiles.writeText(fp, '   ECHO   ****************************************', '\n')
    #VBFiles.writeText(fp, '   ECHO    Da ist was schief gegangen ;-(', '\n')
    #VBFiles.writeText(fp, '   ECHO   ****************************************', '\n')
    #VBFiles.writeText(fp, '   Pause', '\n')
    #VBFiles.closeFile(fp)
    #fn_return_value = UpdCnt
    
    if OthersourceList != "":
        rowlist = OthersourceList.split(",")
        
        for Row in rowlist:
            if IsNumeric(Row):
                __Add_Update_from_Other_Source_Linux(int(Row))
        Res=M40.Success
    return Res
    VBFiles.closeFile(fp)
    P01.MsgBox(M09.Get_Language_Str('Fehler beim Schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Start Datei'))
    fn_return_value = - 1
    return fn_return_value

def __Test_Create_Do_Update_Script():
    #UT---------------------------------------
    __Create_Do_Update_Script()(True)

def __Get_Original_Name_from_TestFile(LibDir):
    fn_return_value = ""
    Row = int()

    #Sh = Worksheet()
    #---------------------------------------------------------------------------
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    Row = __First_Dat_Row
    while Sh.Cells(Row, __Libr_Name_Col) != '':
        if InStr(Sh.Cells(Row, __Lib_Board_Col), 'L') > 0:
            TestFile = Sh.Cells(Row, __Test_File_Col)
            if Dir(LibDir + TestFile) != '' or Dir(LibDir + 'src\\' + TestFile) != '':
                fn_return_value = Sh.Cells(Row, __Libr_Name_Col)
                return fn_return_value
        Row = Row + 1
    return fn_return_value

def __Correct_one_Temp_Arduino_nr_Dir(LibDir):
    Org_LibName = String()
    #-----------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on 1
    Org_LibName = __Get_Original_Name_from_TestFile(M02.Sketchbook_Path + '\\libraries\\' + LibDir + '\\')
    if Org_LibName != '':
        Org_LibPath = M02.Sketchbook_Path + '\\libraries\\' + Org_LibName
        if Dir(Org_LibPath, vbDirectory) != '':
            Debug.Print('Deleting old library: ' + Org_LibPath)
            M30.Del_Folder(Org_LibPath)
        Debug.Print('Rename directory \'' + LibDir + '\' to \'' + Org_LibName + '\'')
        M30.ChDir(M02.Sketchbook_Path + '\\libraries\\')
        Debug.Print(Dir(LibDir, vbDirectory))
        # VB2PY (UntranslatedCode) On Error GoTo ErrMsg
        #M30.Name(LibDir)
        # VB2PY (UntranslatedCode) On Error GoTo 0
    return
    P01.MsgBox(M09.Get_Language_Str('Fehler beim umbenennen des temporären Verzeichnisses:') + vbCr + '  \'' + M02.Sketchbook_Path + '\\libraries\\' + LibDir + '\'' + vbCr + M09.Get_Language_Str('Vermutlich ist irgend eine Datei in dem Verzeichniss ' + 'durch ein Programm gesperrt ;-(') + vbCr + M09.Get_Language_Str('Das Verzeichnis muss von Hand gelöscht werden'), vbCritical, M09.Get_Language_Str('Temporäres Verzeichnis konnte nicht umbenannt werden'))

def __Test_name():
    #UT--------------------
    P01.ChDrive('E:')
    ChDir('E:\\Test Arduino Lib mit ä\\libraries')
    os.rename('FastLED\\', 'Arduino_12345')

def __Correct_Temp_Adrduino_nr_Dirs():
    Res = String()

    DirList = String()

    d = Variant()
    #------------------------------------------
    # Sometimes the instalation fails an a "Arduino_<nr>" directory is created.
    # Unfortunately an update with a new version is not possible
    if CheckArduinoHomeDir() == False: # also sets Sketchbook_Path variable  02.12.21: Juergen
        return
    #P01.ChDrive(M02.Sketchbook_Path)
    ChDir(M02.Sketchbook_Path)
    print(os.getcwd())
    #dirpath = M02.Sketchbook_Path+'\\libraries\\Arduino_*.'
    Res = Dir('libraries\\Arduino_*.', vbDirectory)
    #Res = Dir(dirpath, vbDirectory)
    while Res != '':
        DirList = DirList + Res + vbTab
        Res = Dir()
    for d in Split(DirList, vbTab):
        __Correct_one_Temp_Arduino_nr_Dir(( d ))
    return

def CheckArduinoHomeDir():
    fn_return_value = None
    message = Variant()
    #------------------------------------------
    fn_return_value = False
    if M02.Read_Sketchbook_Path_from_preferences_txt() == False:
        Debug.Print("CheckArduinoHomeDir: ERROR")
        return fn_return_value
    # VB2PY (UntranslatedCode) On Error GoTo DirError
    #P01.ChDrive(M02.Sketchbook_Path)
    try:
        ChDir(M02.Sketchbook_Path)
        fn_return_value = True
        Debug.Print("CheckArduinoHomeDir: "+ M02.Sketchbook_Path)
        return fn_return_value
    # VB2PY (UntranslatedCode) On Error GoTo 0
    except:
        message = Replace(M09.Get_Language_Str('Das Arduino Sketchbook Verzeichnis #1# existiert nicht.' + 'Bitte prüfen und korrigieren sie die Einstellungen in der Arduino IDE.'), '#1#', M02.Sketchbook_Path + vbCrLf)
        P01.MsgBox(message, vbCritical, M09.Get_Language_Str('Es sind Fehler aufgetreten'))
        return fn_return_value



def __Check_All_Selected_Libraries_Result(Ask_User):
    fn_return_value = False
    Row = 0 # int()

    #Sh = Worksheet()

    NotInstCnt = 0 #int()

    List = "" #String()
    #-----------------------------------------------------------------------------------
    # Return true if the update should be repeated
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    Row = __First_Dat_Row
    while Sh.Cells(Row, __Libr_Name_Col) != '':
        if Sh.Cells(Row, __SelectRow_Col) != '':
            if Sh.Cells(Row, __Installed_Col) != 1:
                NotInstCnt = NotInstCnt + 1
                List = List + '   ' + Sh.Cells(Row, __Libr_Name_Col) + vbCr
        Row = Row + 1
    if NotInstCnt > 0:
        if Ask_User:
            if P01.MsgBox(M09.Get_Language_Str('Fehler beim Aktualisieren der Bibliotheken und Boards aufgetreten. ' + vbCr + 'Leider treten beim herunter laden vom Arduino Server manchmal Übertragungsfehler auf. ' + vbCr + 'Oft hilft es wenn man den Prozess noch mal startet.' + vbCr + vbCr + 'Nicht installiert:') + vbCr + List + vbCr + M09.Get_Language_Str('Soll die Aktualisierung noch mal aufgerufen werden?'), vbQuestion + vbYesNo, M09.Get_Language_Str('Es sind Fehler beim Aktualisieren aufgetreten')) == vbYes:
                fn_return_value = True
        else:
            fn_return_value = True
    return fn_return_value

def __Test_Check_All_Selected_Libraries_Result():
    #UT---------------------------------------------------
    __Check_All_Selected_Libraries_Result()(True)

def __Update_Status_old(Start=False):
    global __Update_Time
    #---------------------------------------------------
    # Is called by OnTime
    if __Update_Time != 0 or Start:
        if Start:
            __Update_Time = Time
        else:
            F00.StatusMsg_UserForm.Set_ActSheet_Label(P01.Format(Time - __Update_Time, 'hh:mm:ss'))
        
        P01.Application.OnTime(1000, __Update_Status)
        
def __Update_Status(Start=False):
    #---------------------------------------------------------
    global __Update_Time
    # Is called by OnTime
    if __Update_Time != 0 or Start:
        if Start:
            __Update_Time = int(time.time())
        else:
            F00.StatusMsg_UserForm.Set_ActSheet_Label(P01.Format(int(time.time()) - __Update_Time, 'hh:mm:ss'))
        P01.Application.OnTime(1000, __Update_Status)


def __Stop_Status_Display():
    global __Update_Time
    #--------------------------------
    __Update_Time = 0
    P01.Unload(F00.StatusMsg_UserForm)

def __Update_All_Selected_Libraries():
    global __UnzipList, __UPDATE_LIB_CMD_NAME
    fn_return_value = False
    Pause_at_End = Boolean()

    Trials = int()

    Ask_User = Boolean()

    Start_Update = Boolean()

    #hwnd = LongPtr()
    #----------------------------------------------------------
    if M02.Read_Sketchbook_Path_from_preferences_txt() == False:
        # VB2PY (UntranslatedCode) GoTo EndFunc
        pass
    Start_Update = True
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    #hwnd = Application.hwnd
    while 1:
        __UnzipList = ''
        select_0 = __Create_Do_Update_Script(Pause_at_End)
        if (select_0 == 0):
            P01.MsgBox(M09.Get_Language_Str('Es wurden keine Zeilen zur Installation ausgewählt. Die Zeilen müssen mit einem Häkchen in der Spalte \'Select\' markiert werden.' + vbCr + 'Für die ausgewählten Zeilen wird die neueste Software installiert, es sei den in der Spalte "Required Version" ist eine ' + 'bestimmte Version angegeben.'), vbInformation, M09.Get_Language_Str('Keine Zeilen zur Installation ausgewählt.'))
            break #*HL GoTo(EndFunc)
        elif (select_0 == - 1):
            break #*HL GoTo(EndFunc)
        F00.StatusMsg_UserForm.ShowDialog(M09.Get_Language_Str('Aktualisiere Bibliotheken und Boards'), '')
        __Update_Status(Start_Update)
        Start_Update = False
        __Correct_Temp_Adrduino_nr_Dirs()
        P01.ChDrive(M02.Sketchbook_Path)
        ChDir(M02.Sketchbook_Path)
        if Dir('libraries/*', vbDirectory) == '':
            MkDir('libraries/')
        ChDir(M02.Sketchbook_Path + '/libraries/')
        CommandStr = P01.ThisWorkbook.Path + '/' + __UPDATE_LIB_CMD_NAME
        Res = M40.ShellAndWait(CommandStr, 0, vbNormalFocus, M40.PromptUser)
        if (Res == M40.Success) or (Res == M40.Timeout):
            pass
        else:
            P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler #1# beim Starten der Update Programms \'#2#\''), "#1#", str(Res)), '#2#', CommandStr), vbCritical, M09.Get_Language_Str('Fehler beim Aktualisieren der Bibliotheken'))
            break #*HL GoTo(EndFunc)
        if WIN7_COMPATIBLE_DOWNLOAD:
            __Proc_UnzipList()
        P01.Unload(F00.StatusMsg_UserForm)
        # Bring Excel to the top
        # Is not working if an other application has be moved above Excel with Alt+Tab
        # But this is a feature of Windows.
        #   See: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow
        # But it brings up excel again after the upload to the Arduino
        # Without this funchion an other program was activated after the upload for some reasons
        #*HL Bring_to_front(hwnd)
        P01.DoEvents()
        if __Get_All_Library_States() == False:
            fn_return_value = False
            break
            # VB2PY (UntranslatedCode) GoTo EndFunc
            pass
        Trials = Trials + 1
        if Trials >= 2:
            Ask_User = True
            Pause_at_End = True
        __Update_General_Versions()
        if not (__Check_All_Selected_Libraries_Result(Ask_User)):
            fn_return_value = True
            break
        
    __Stop_Status_Display()
    P01.Unload(F00.StatusMsg_UserForm)
    P01.ChDrive(P01.ThisWorkbook.Path)
    ChDir(P01.ThisWorkbook.Path)
    return fn_return_value

def __Update_All_Selected_Libraries_Linux():
    global __UnzipList, __UPDATE_LIB_CMD_NAME
    fn_return_value = False
    Pause_at_End = Boolean()

    Trials = int()

    Ask_User = Boolean()

    Start_Update = Boolean()

    #hwnd = LongPtr()
    #----------------------------------------------------------
    if M02.Read_Sketchbook_Path_from_preferences_txt() == False:
        # VB2PY (UntranslatedCode) GoTo EndFunc
        pass
    Start_Update = True
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    #hwnd = Application.hwnd
    while 1:
        __UnzipList = ''
        updcnt,LibList,BrdList,OthersourceList = __Create_Do_Update_Script_Linux_part1(Pause_at_End)
        if (updcnt == 0):
            P01.MsgBox(M09.Get_Language_Str('Es wurden keine Zeilen zur Installation ausgewählt. Die Zeilen müssen mit einem Häkchen in der Spalte \'Select\' markiert werden.' + vbCr + 'Für die ausgewählten Zeilen wird die neueste Software installiert, es sei den in der Spalte "Required Version" ist eine ' + 'bestimmte Version angegeben.'), vbInformation, M09.Get_Language_Str('Keine Zeilen zur Installation ausgewählt.'))
            break #*HL GoTo(EndFunc)
        elif (updcnt == - 1):
            break #*HL GoTo(EndFunc)
        F00.StatusMsg_UserForm.ShowDialog(M09.Get_Language_Str('Aktualisiere Bibliotheken und Boards'), '')
        __Update_Status(Start_Update)
        Start_Update = False
        __Correct_Temp_Adrduino_nr_Dirs()
        P01.ChDrive(M02.Sketchbook_Path)
        ChDir(M02.Sketchbook_Path)
        if Dir('libraries/*', vbDirectory) == '':
            MkDir('libraries/')
        ChDir(M02.Sketchbook_Path + '/libraries/')
        Res = __Create_Do_Update_Script_Linux_part2(LibList,BrdList,OthersourceList)
        #CommandStr = P01.ThisWorkbook.Path + '/' + __UPDATE_LIB_CMD_NAME
        #Res = M40.ShellAndWait(CommandStr, 0, vbNormalFocus, M40.PromptUser)
        if (Res == M40.Success) or (Res == M40.Timeout):
            pass
        else:
            P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler #1# beim Starten der Update Programms \'#2#\''), "#1#", str(Res)), '#2#', CommandStr), vbCritical, M09.Get_Language_Str('Fehler beim Aktualisieren der Bibliotheken'))
            break #*HL GoTo(EndFunc)
        if WIN7_COMPATIBLE_DOWNLOAD:
            __Proc_UnzipList()
        P01.Unload(F00.StatusMsg_UserForm)
        # Bring Excel to the top
        # Is not working if an other application has be moved above Excel with Alt+Tab
        # But this is a feature of Windows.
        #   See: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow
        # But it brings up excel again after the upload to the Arduino
        # Without this funchion an other program was activated after the upload for some reasons
        #*HL Bring_to_front(hwnd)
        P01.DoEvents()
        if __Get_All_Library_States() == False:
            fn_return_value = False
            break
            # VB2PY (UntranslatedCode) GoTo EndFunc
            pass
        Trials = Trials + 1
        if Trials >= 2:
            Ask_User = True
            Pause_at_End = True
        __Update_General_Versions()
        if not (__Check_All_Selected_Libraries_Result(Ask_User)):
            fn_return_value = True
            break
        
    __Stop_Status_Display()
    P01.Unload(F00.StatusMsg_UserForm)
    P01.ChDrive(P01.ThisWorkbook.Path)
    ChDir(P01.ThisWorkbook.Path)
    return fn_return_value

def __Select_Missing():
    fn_return_value = None
    Row = int()

    #Sh = Worksheet()

    NotInstCnt = int()

    FastLED_Ver = String()

    Arduino_Ver = String()

    Arduino_row = int()
    #----------------------------------------
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    Row = __First_Dat_Row
    while Sh.Cells(Row, __Libr_Name_Col) != '':
        with_3 = Sh.Cells(Row, __SelectRow_Col)
        with_3.Value = ''
        if InStr(Sh.Cells(Row, __Lib_Board_Col), '*') == 0:
            if Sh.Cells(Row, __Installed_Col) != "1":
                with_3.Value = ChrW(M02.Hook_CHAR)
                NotInstCnt = NotInstCnt + 1
            elif Sh.Cells(Row, __Reque_Ver_Col) != '':
                if M30.VersionStr_is_Greater(Sh.Cells(Row, __Reque_Ver_Col), Sh.Cells(Row, __DetectVer_Col)):
                    with_3.Value = ChrW(M02.Hook_CHAR)
                    NotInstCnt = NotInstCnt + 1
        select_2 = Sh.Cells(Row, __Libr_Name_Col)
        if (select_2 == 'FastLED'):
            FastLED_Ver = Sh.Cells(Row, __DetectVer_Col)
        elif (select_2 == 'arduino:avr'):
            Arduino_Ver = Sh.Cells(Row, __DetectVer_Col)
            Arduino_row = Row
        Row = Row + 1
    # Special Check: FastLED >= 3.3.3 require GCC > 7.3.0  => arduino lib >= 1.6.23
    if Sh.Cells(Arduino_row, __SelectRow_Col) != ChrW(M02.Hook_CHAR):
        if M30.VersionStr_is_Greater(FastLED_Ver, '3.3.2') and not M30.VersionStr_is_Greater(Arduino_Ver, '1.6.23'):
            Sh.CellDict[Arduino_row, __SelectRow_Col] = ChrW(M02.Hook_CHAR)
            if not M30.VersionStr_is_Greater(Sh.Cells(Arduino_row, __Reque_Ver_Col), '1.6.23'):
                Sh.CellDict[Arduino_row, __Reque_Ver_Col] = ''
            NotInstCnt = NotInstCnt + 1
    fn_return_value = NotInstCnt
    return fn_return_value

def __Create_Restart_Cmd():
    global __RESTART_PROGGEN_CMD
    fn_return_value = None
    fp = Integer()

    Name = String()

    #UpdCnt = int()
    #----------------------------------------------
    # Create a CMD file which restarts the new version of the Prog_Generator
    # - Wait until the existing prog generator is closes
    # - Restart excel
    if M02.Read_Sketchbook_Path_from_preferences_txt() == False:
        return fn_return_value
    fp = FreeFile()
    Name = P01.ThisWorkbook.Path + '\\' + __RESTART_PROGGEN_CMD
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'Color 79', '\n')
    VBFiles.writeText(fp, 'REM This file was generated by \'' + P01.ThisWorkbook.Name + '\'  ' + Time, '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'Rem Wait until the Prog_Generator_MobaLedLib is closed', '\n')
    VBFiles.writeText(fp, 'REM and restart the new version of the Prog_Generator_MobaLedLib', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'ECHO  ~~~~~~~~~~~~~~~~~~', '\n')
    VBFiles.writeText(fp, 'ECHO  Update is finished', '\n')
    VBFiles.writeText(fp, 'ECHO  ~~~~~~~~~~~~~~~~~~', '\n')
    VBFiles.writeText(fp, 'ECHO.', '\n')
    VBFiles.writeText(fp, 'ECHO  Going to restarting the new Prog_Generator_MobaLedLib.xlsm', '\n')
    VBFiles.writeText(fp, 'ECHO.', '\n')
    VBFiles.writeText(fp, 'ECHO  If the program hangs here the hidden file "~$Prog_Generator_MobaLedLib.xlsm"', '\n')
    VBFiles.writeText(fp, 'ECHO  is not deleted for some reasons. It has to be deleted manualy.', '\n')
    VBFiles.writeText(fp, 'ECHO.', '\n')
    VBFiles.writeText(fp, 'ECHO  Make sure that all excel instances are closed if it hangs.', '\n')
    VBFiles.writeText(fp, 'ECHO  In case of problems the installation is continued in one minute.', '\n')
    VBFiles.writeText(fp, 'ECHO.', '\n')
    VBFiles.writeText(fp, 'set /A counter=1', '\n')
    VBFiles.writeText(fp, '::define a variable containing a single backspace character', '\n')
    VBFiles.writeText(fp, 'for /f %%A in (\'"prompt $H &echo on &for %%B in (1) do rem"\') do set BS=%%A', '\n')
    VBFiles.writeText(fp, 'echo | set /p=%BS% Waiting until excel is closed', '\n')
    VBFiles.writeText(fp, ': Wait', '\n')
    VBFiles.writeText(fp, '@ping localhost -n 3 > NUL', '\n')
    VBFiles.writeText(fp, 'echo | set /p=.', '\n')
    VBFiles.writeText(fp, 'set /A counter=%counter%+1', '\n')
    VBFiles.writeText(fp, 'if %counter% gtr 20 ( goto :Continue )', '\n')
    VBFiles.writeText(fp, 'if exist "~$Prog_Generator_MobaLedLib.xlsm" Goto Wait', '\n')
    VBFiles.writeText(fp, ':Continue', '\n')
    VBFiles.writeText(fp, 'ECHO.', '\n')
    VBFiles.writeText(fp, 'ECHO  Going to start the Prog_Generator_MobaLedLib again', '\n')
    VBFiles.writeText(fp, 'CHCP 65001 > NUL', '\n')
    VBFiles.writeText(fp, Left(M02.Sketchbook_Path, 2), '\n')
    VBFiles.writeText(fp, 'CD "' + M30.ConvertToUTF8Str(M02.Sketchbook_Path) + '\\libraries\\MobaLedLib\\extras\\"', '\n')
    #  Print #fp, "CD"    ' Debug
    #  Print #fp, "PAUSE" ' Debug
    VBFiles.writeText(fp, '@ping localhost -n 1 > NUL', '\n')
    # 09.03.21 Juergen: delete cache file to force an ESP32 rebuild, otherwise prebuild library versions would still be used
    VBFiles.writeText(fp, '@if exist "%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache" del "%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache"', '\n')
    VBFiles.writeText(fp, 'Start Prog_Generator_MobaLedLib.xlsm', '\n')
    VBFiles.writeText(fp, 'EXIT', '\n')
    VBFiles.closeFile(fp)
    fn_return_value = M08.GetShortPath(P01.ThisWorkbook.Path) + '\\' + __RESTART_PROGGEN_CMD
    return fn_return_value
    VBFiles.closeFile(fp)
    P01.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Start Datei'))
    return fn_return_value

def __Select_from_Range(RangeStr):
    fn_return_value = None
    #Row = int()

    #Sh = Worksheet()
    #----------------------------------------------------------------
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    Row = __First_Dat_Row
    while Sh.Cells(Row, __Libr_Name_Col) != '':
        with_4 = Sh.Cells(Row, __SelectRow_Col)
        with_4.Value = ''
        Row = Row + 1
    # VB2PY (UntranslatedCode) On Error GoTo Range_Not_Found
    P01.Application.EnableEvents=False
    Sh.Range_set(RangeStr,ChrW(M02.Hook_CHAR))
    P01.Application.EnableEvents=True
    fn_return_value = 9 #*HL
    
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = Sh.Range(RangeStr,None).Row
    return fn_return_value
    
    P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Der Bereich \'#1#\' wurde nicht im Blatt \'#2#\' gefunden'), "#1#", RangeStr), '#2#', Sh.Name), vbCritical, M09.Get_Language_Str('Fehler beim aktivieren der Update Zeile'))
    fn_return_value = - 1
    return fn_return_value

def __Show_Close_Message_if_Other_WB_are_Open():
    return False #*HL

    fn_return_value = False
    #wb = Variant()
    #--------------------------------------------------------------------
    for wb in P01.Workbooks:
        if wb.Name != P01.ThisWorkbook.Name:
            #*HL Close_Other_Workbooks.Start('Start_Update_MobaLedLib_and_Restarte_Excel')
            fn_return_value = True
            return fn_return_value
    return fn_return_value

def __Start_Update_MobaLedLib_and_Restarte_Excel():
    #wb = Variant()

    CommandStr = String()
    #-------------------------------------------------------
    # Close all other workbooks without saving (The user has been warned before)
    #*HLfor wb in P01.Workbooks:
    #*HL    if wb.Name != P01.ThisWorkbook.Name:
    #*HL        wb.Close(Savechanges=False)
    if __Update_All_Selected_Libraries_Linux() == False:
        return
    CommandStr = __Create_Restart_Cmd()
    if CommandStr == '':
        return
    #*HL no retsrt needed P01.ThisWorkbook.Save()
    #*HL P01.Shell('cmd /c start ' + CommandStr)
    #  MsgBox "Warte"
    #*HL P01.Application.Quit()

def __Update_MobaLedLib_from_Range_and_Restart_Excel(RangeStr):
    
    Row = Integer()

    Ctrl_Pressed = Boolean()
    #-----------------------------------------------------------------------------
    Row = __Select_from_Range(RangeStr)
    if Row < 0:
        return
    #*HL Ctrl_Pressed = P01.GetAsyncKeyState(M24.VK_CONTROL) != 0
    if False: #*HLCtrl_Pressed:
        currentUrl = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH).Cells(Row, __Other_Src_Col)
        frm = UserForm_SingleInput()
        newUrl = frm.ShowForm(M09.Get_Language_Str('Beta-Test Installation'), M09.Get_Language_Str('Bitte geben sie die URL ein, von der sie die neue Beta Version herunterladen wollen'), currentUrl)
        if newUrl == '<Abort>':
            return
        P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH).CellDict[Row, __Other_Src_Col] = newUrl
    if __Show_Close_Message_if_Other_WB_are_Open():
        return
        # Other Workbooks are opened => "Start_Update_MobaLedLib_and_Restarte_Excel" is called after they ara closed
    __Start_Update_MobaLedLib_and_Restarte_Excel()

def Delete_Selected():
    Row = int()

    #Sh = Worksheet()

    DidDelete = Boolean()

    i = int()
    #---------------------------
    if M02.Read_Sketchbook_Path_from_preferences_txt() == False:
        return
    DidDelete = False
    Sh = P01.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
    Row = __First_Dat_Row
    while Sh.Cells(Row, __Libr_Name_Col) != '':
        if Sh.Cells(Row, __SelectRow_Col) != '':
            if InStr(Sh.Cells(Row, __Lib_Board_Col), 'L') > 0:
                # *** Library ***
                LibrariesDir = M02.Sketchbook_Path + '\\libraries\\'
                LibDir = LibrariesDir + Sh.Cells(Row, __Libr_Name_Col)
                if Dir(LibDir, vbDirectory) != '':
                    Debug.Print('Deleting: ' + LibDir)
                    M30.Del_Folder(LibDir)
                    DidDelete = True
            elif InStr(Sh.Cells(Row, __Lib_Board_Col), 'B') > 0:
                # Board
                Board_and_Proc = Sh.Cells(Row, __Libr_Name_Col)
                Board = Split(Board_and_Proc, ':')(0)
                BoardDir = Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + 'packages\\' + Board
                if Dir(BoardDir, vbDirectory) != '':
                    Debug.Print('Deleting: ' + BoardDir)
                    M30.Del_Folder(BoardDir)
                    DidDelete = True
        Row = Row + 1
    if DidDelete == True:
        if Dir(Environ(M02.Env_USERPROFILE) + '\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache') != '':
            Kill(Environ(M02.Env_USERPROFILE) + '\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32\\includes.cache')
    Debug.Print('Waiting')
    for i in vbForRange(1, 30):
        DoEvents()
        Debug.Print('.')
        Sleep(100)
    Debug.Print('')
    __Get_All_Library_States()()

def Update_MobaLedLib_from_Arduino_and_Restart_Excel():
    #------------------------------------------------------------
    if P01.MsgBox(M09.Get_Language_Str('Soll die MobaLedLib aktualisiert werden?' + vbCr + 'Wenn die vorhandene Bibliothek die gleiche oder eine neuere Version besitzt, dann ' + 'wird die existierend Bibliothek beibehalten.'), vbQuestion + vbYesNo, M09.Get_Language_Str('Aktualisieren der MobaLedLib')) != vbYes:
        return
    __Update_MobaLedLib_from_Range_and_Restart_Excel('Select_MobaLedLib_Arduino')

def Update_MobaLedLib_from_Beta_and_Restart_Excel():
    #---------------------------------------------------------
    if P01.MsgBox(M09.Get_Language_Str('Soll die Beta Test Version der MobaLedLib installiert werden?'), vbQuestion + vbYesNo, M09.Get_Language_Str('Beta Test der MobaLedLib installieren?')) != vbYes:
        return
    __Update_MobaLedLib_from_Range_and_Restart_Excel('Select_MobaLedLib_Beta')

def Check_Actual_Versions():
    #---------------------------------
    # Is called by the button in the "Libraries" sheet
    # It checks all versions and selects the rows which have to be updated
    __Update_General_Versions()
    __Get_All_Library_States()()
    __Select_Missing()()

def Install_Selected():
    #----------------------------
    # Is called by the button in the "Libraries" sheet
    __Update_All_Selected_Libraries_Linux()

def Install_Missing_Libraries_and_Board():
    #-----------------------------------------------
    F00.StatusMsg_UserForm.ShowDialog(M09.Get_Language_Str('Überprüfe Bibliotheken und Boards'), '')
    __Update_General_Versions()
    __Get_All_Library_States()
    if __Select_Missing() > 0:
        Install_Selected()
    P01.Unload(F00.StatusMsg_UserForm)

def OpenSketchbookPath():
    Name = String()
    #------------------------------
    M02.Read_Sketchbook_Path_from_preferences_txt()
    Name = M02.Sketchbook_Path
    Shell('Explorer /root,"' + Name + '"', vbNormalFocus)

def Is_Lib_Installed(LibName):
    fn_return_value = None
    Row = int()
    #-------------------------------------------------------------
    LastRow = M30.LastUsedRow(M02.LIBRARYS__SH)
    Row = __First_Dat_Row
    with_5 = P01.Sheets(M02.LIBRARYS__SH)
    while Row <= LastRow:                                         # 06.12.2021 Juergen Fix issue with empty lines in sheet
        if with_5.Cells(Row, __Libr_Name_Col) == LibName:
            fn_return_value = ( with_5.Cells(Row, __Installed_Col) == 1 )
            return fn_return_value
        Row = Row + 1
    return fn_return_value

def Get_Lib_Version(LibName):
    fn_return_value = None
    Row = int()
    #-------------------------------------------------------------
    LastRow = M30.LastUsedRowIn(M02.LIBRARYS__SH)
    Row = __First_Dat_Row
    with_6 = P01.Sheets(M02.LIBRARYS__SH)
    while Row <= LastRow:                                       # 06.12.2021 Juergen Fix issue with empty lines in sheet
        if with_6.Cells(Row, __Libr_Name_Col) == LibName:
            fn_return_value = with_6.Cells(Row, __DetectVer_Col)
            return fn_return_value
        Row = Row + 1
    fn_return_value = ''
    return fn_return_value

def Get_Required_Version(LibName):
    fn_return_value = None
    Row = int()
    #-------------------------------------------------------------
    LastRow = M30.LastUsedRowIn(M02.LIBRARYS__SH)
    Row = __First_Dat_Row
    with_7 = P01.Sheets(M02.LIBRARYS__SH)
    while Row <= LastRow:                                       # 06.12.2021 Juergen Fix issue with empty lines in sheet
        if with_7.Cells(Row, __Libr_Name_Col) == LibName:
            fn_return_value = with_7.Cells(Row, __Reque_Ver_Col)
            return fn_return_value
        Row = Row + 1
    fn_return_value = ''
    return fn_return_value

def __Test_Is_Lib_Installed():
    #UT--------------------------------
    Debug.Print('Is_Lib_Installed(esp32:esp32): ' + Is_Lib_Installed('esp32:esp32'))
    Debug.Print('Is_Lib_Installed(NichtInstal): ' + Is_Lib_Installed('NichtInstal'))
    Debug.Print('Get_Lib_Version(esp32:tools\\esptool_py)' + Get_Lib_Version('esp32:tools\\esptool_py'))
    Debug.Print('Get_Lib_Version(NichtInstal)' + Get_Lib_Version('NichtInstal'))

def ESP32_Lib_Installed():
    fn_return_value = None
    #-----------------------------------------------
    fn_return_value = Is_Lib_Installed('esp32:esp32')
    return fn_return_value

def PICO_Lib_Installed():
    fn_return_value = None
    #-----------------------------------------------
    fn_return_value = Is_Lib_Installed('rp2040:rp2040')
    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Option Compare Text ' Case insensitive compare
