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

import time
import platform

# fromx proggen.M02_Public import *
# fromx proggen.M06_Write_Header_LED2Var import *
# fromx proggen.M06_Write_Header_Sound import *
# fromx proggen.M06_Write_Header_SW import *
# fromx proggen.M09_Language import *
# fromx proggen.M09_Select_Macro import *
# fromx proggen.M20_PageEvents_a_Functions import *
# fromx proggen.M25_Columns import *
# fromx proggen.M28_divers import *
# fromx proggen.M30_Tools import *

# fromx proggen.M80_Create_Mulitplexer import *


import proggen.M02_Public as M02
import proggen.M02a_Public as M02a
#import proggen.M02_Scripting as Scripting
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
import proggen.M06_Write_Header as M06
import proggen.M07_COM_Port as M07
import proggen.M08_Fast_ARDUINO as M08FA
import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
#import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M38_Extensions as M38
import proggen.M39_Simulator as M39
import proggen.M40_ShellandWait as M40
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Mulitplexer as M80
import proggen.M98_Ondrive as M98

#import proggen.D08_Select_COM_Port_Userform as D08

import  proggen.F00_mainbuttons as F00

import ExcelAPI.XLW_Workbook as P01

import mlpyproggen.Prog_Generator as PG

""" Die MobaLedLib wird nur dann Installiert wenn sie nicht vorhanden ist
 - Das Excel sheet würde sich selber überschreiben
 Comma separeted list of libraries (Case sensitive => check the library.property file
 The MCP_CAN lib can't be installed from the IDE because
  - it's not available in the library manager
  - the debug mode is enabled in the version on GitHub
 => It's included to the program directory

# VB2PY (CheckDirective) VB directive took path 1 on OLD_LIB_CHECK

"""
#Public Enum ActionOnBreak
IgnoreBreak = 0
AbandonWait = 1
PromptUser = 2
#End Enum
Start_Compile_Time = 0


def Use_Excel_Console():
    #---------------------------------------------
    fn_return_value = M28.Get_Bool_Config_Var('Use_Excel_Console')
    return fn_return_value

def LEDNr_Display_Type():
    #---------------------------------------------
    fn_return_value = M28.Get_Num_Config_Var('LEDNr_Display_Type')
    return fn_return_value

def Test_Cmd_Admin():
    #Shell('cmd runas /user:Administrator cmd /c')
    pass

def Find_ArduinoExe(data=False):
    private_startfile=False
    
    system_platform = platform.platform()
    Dirs = ""
    ARDUINO_EXE = ""
    
    if not "Windows" in system_platform:
        private_startfile = True
        
    if private_startfile == True:
        filename = PG.get_global_controller().getConfigData("startcmd_filename")
        Dirs=filename
        #logging.debug("Find ARDUINO exe - Individual Filename: %s",filename)
        if filename == " " or filename == "":
            filename = "No Filename provided"
        logging.debug("Find ARDUINO EXE - Platform: %s",platform.platform())
        
        macos = "macOS" in system_platform
        macos_fileending = "/Contents/MacOS/Arduino" 
        if macos:
            logging.debug("This is a MAC")
            if not filename.endswith(macos_fileending):
                filename = filename + "/Contents/MacOS/Arduino"
        
        if os.path.isfile(filename):
            logging.debug("Find ARDUINO exe - Individual Filename: %s",filename)
            if data and macos:
                filename=filename.replace("/MacOS/Arduino", "/Java/")
            return filename
        else:
            logging.debug("Find ARDUINO exe - No Filename provided")
            return ""
    else:
    
        ARDUINO_EXE = 'arduino_debug.exe'
    
        Dirs = '  C:\\Program Files (x86)\\Arduino\\' + ARDUINO_EXE + vbCr + '  C:\\Program Files\\Arduino\\' + ARDUINO_EXE
    
        FileName = Variant()
        #-------------------------------------------
        for FileName in Split(Dirs, vbCr):
            FileName = Trim(FileName)
            if Dir(FileName) != '':
                fn_return_value = FileName
                logging.debug("Find ARDUINO exe - Individual Filename: %s",FileName)
                return fn_return_value
    
    if P01.MsgBox(M09.Get_Language_Str('Fehler: Die Arduino Entwicklungsumgebung ist nicht oder nicht im Standard Verzeichnis installiert.' + 
                                       vbCr + 'Das Programm muss abhängig vom Betriebssystem hier installiert sein:') + vbCr + Dirs + vbCr + vbCr +
                  M09.Get_Language_Str('Achtung: Die \'App\' Version der Arduino IDE wird nicht unterstützt. ' + vbCr + 'Es muss die \'Windows Installer, for Windows XP and up\' Version installiert werden.' +
                                       vbCr + vbCr +
                                       'Soll die Arduino Webseite geöffnet werden damit die richtige Version herunter geladen werden kann ?'), 
                  vbCritical + vbYesNo, M09.Get_Language_Str('Fehler: \'') + ARDUINO_EXE + M09.Get_Language_Str('\' nicht gefunden')) == vbYes:
        logging.debug("Find ARDUINO exe - ARDUINO.Exe not found")
        #*HL Shell('Explorer "https://www.arduino.cc/en/main/software"')
    
    #M30.EndProg()
    return "" #fn_return_value

def GetWorkbookPath():
    _fn_return_value = None
    # 06.02.23: Jürgen
    _fn_return_value = M98.GetLocalPath(PG.ThisWorkbook.Path)
    return _fn_return_value

def GetShortPath(Path):
    #fso = FileSystemObject()
    #-----------------------------------------------------
    fn_return_value = ""
    if Path == '':
        return fn_return_value
    #Add a reference to Microsoft Scripting Runtime
    # if fso is None:
    #     fso = FileSystemObject()
    #If the path is a file - Output the full path in 8.3 format
    #if fso.FileExists(Path):
    if os.path.isfile(Path):
        #*HLfn_return_value = fso.GetFile(Path).ShortPath
        fn_return_value = Path
        return fn_return_value
    #If the path is a folder - Output the full path in 8.3 format
    #if fso.FolderExists(Path):
    if os.path.isdir(Path):
        #*HLfn_return_value = fso.GetFolder(Path).ShortPath
        fn_return_value = Path
        return fn_return_value
    P01.MsgBox('Internal error: \'GetShortPath()\' was called with the invalid path: \'' + Path + '\'', vbCritical, 'Internal error')
    M30.EndProg()
    return fn_return_value

def Create_Start_Sub(BoardName, ResultName, ComPort, BuildOptions, InoName, SrcDir, CPUType):
    fp = Integer()

    Name = String()

    FindStr = String()

    CMD_Name = String()

    i = int()
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    fn_return_value = ""
    
    if BoardName == 'PICO':
        Board_Version = M37.Get_Lib_Version('rp2040:rp2040')
        if Board_Version == '':
            P01.MsgBox(M09.Get_Language_Str('Fehler: Eine notwendige Arduino Erweiterung ist nicht installiert:') + '  \'' + 'Raspberry Pico Board' + '\'', vbCritical, M09.Get_Language_Str('Fehlende Erweiterung'))
            return fn_return_value
    CMD_Name = 'Start_' + BoardName + '_Sub.cmd'
    fp = FreeFile()
    Name = SrcDir + CMD_Name
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    try:
        VBFiles.openFile(fp, Name, 'w') 
        VBFiles.writeText(fp, '@ECHO OFF', '\n')
        VBFiles.writeText(fp, 'REM This file was generated by \'' + PG.ThisWorkbook.Name + '\'  ' + Time, '\n')
        if M30.Win10_or_newer():
            VBFiles.writeText(fp, 'CHCP 65001 >NUL', '\n')
        VBFiles.writeText(fp, '', '\n')
        
        if M28.Get_Bool_Config_Var("Use_PlatformIO") == False:
            FindStr = ' 2>&1 | find /v "Set log4j store directory" | find /v " StatusLogger " | find /v "serial.SerialDiscovery"'
            #*** 14.07.20: Faster way to compile from Jürgen (10 sec instead of 22 sec) ***
            # Create_PrivateBuild_cmd_if_missing SrcDir                           ' 28.10.20: Jürgen: Disabled
            if False: #True == M28.Get_Bool_Config_Var('Fast_Build_and_Upload'):
                Debug.Print("Fast Build and Upload")
                OptParts = Split(BuildOptions, ' ')
                if UBound(OptParts) >= 1:
                    BuildOptOnly=""
                    if OptParts(0) == '--board':
                        BuildOptOnly = OptParts(1)
                    elif OptParts(1) == '--board':
                        BuildOptOnly = OptParts(2)
                    if BuildOptOnly!="":
                        if InStr(BuildOptions, M02.BOARD_NANO_OLD) or InStr(BuildOptions, M02.BOARD_UNO_NORM) > 0:
                            BaudRate = '57600'
                        else:
                            BaudRate = '115200'
                        CommandStr = '"' + M30.FilePath(Find_ArduinoExe()) + '" "' + InoName + '" ' + ComPort + ' "' + BuildOptOnly + '" ' + BaudRate + '  "' + GetShortPath(M30.DelLast(M02a.Get_Ardu_LibDir())) + '" ' + CPUType
                        CommandStr = CommandStr + " %*"      # 19.12.21: Jürgen: Added noflash option
                        VBFiles.writeText(fp, 'if not exist MyPrivateBuildScript.cmd (', '\n')
                        VBFiles.writeText(fp, '  REM embedded Fast Build and Upload', '\n')
                        VBFiles.writeText(fp, '  call :build ' + CommandStr, '\n')
                        VBFiles.writeText(fp, ') else (', '\n')
                        VBFiles.writeText(fp, '  REM user defined Build and Upload', '\n')
                        VBFiles.writeText(fp, '  call MyPrivateBuildScript.cmd ' + CommandStr, '\n')
                        VBFiles.writeText(fp, ')', '\n')
                        #CommandStr = "call privateBuild.cmd """ & FilePath(Find_ArduinoExe) & """ """ & InoName & """ " & ComPort & " """ & BuildOptOnly & """ " & BaudRate & "  """ & DelLast(Get_Ardu_LibDir()) & """"
                        FindStr = ''
            else:
                ## VB2PY (CheckDirective) VB directive took path 1 on 1
                # Use a separate Build directory. => Speed up 12 sec instead of 18
                BuildDir = Replace(Environ('APPDATA'), 'Roaming', '') + 'Arduino_Build_' + Replace(InoName, '.ino', '')
                BuildDirForScript = '%APPDATA%\\..\\' + 'Arduino_Build_' + Replace(InoName, '.ino', '')
                # to avoid nonprintables
                if P01.Dir(BuildDir + '\\.') == '':
                    # VB2PY (UntranslatedCode) On Error Resume Next
                    # In case the directory is created but empty
                    MkDir(BuildDir)
                    # VB2PY (UntranslatedCode) On Error GoTo 0
                    BuildDirForScript = '%APPDATA%\\..\\' + 'Arduino_Build_' + Replace(InoName, '.ino', '')
                    #Debug.Print "BuildDir='" & BuildDir & "'"
                # Other options:  --verbose-build --verbose-upload"
                #   Boards  see: C:\Program Files (x86)\Arduino\hardware\arduino\avr\boards.txt
                #   New Bootloader: nano.menu.cpu.atmega328=ATmega328P
                CommandStr = '"' + Find_ArduinoExe() + '" "' + InoName + '" --upload --port ' + ComPort + ' ' + BuildOptions
                if BuildDirForScript != '':
                    CommandStr = CommandStr + ' --pref build.path="' + BuildDirForScript + '"' + ' --preserve-temp-files'
                VBFiles.writeText(fp, CommandStr, '\n')
            
            VBFiles.writeText(fp, 'IF ERRORLEVEL 1 ECHO Start_Arduino_Result: %ERRORLEVEL% > "' + ResultName + '"', '\n')
            VBFiles.writeText(fp, 'goto :eof', '\n')
            for i in vbForRange(1, 100):
                VBFiles.writeText(fp, '', '\n') # generate empty lines to hide the following to courious people (Jürgen)
            VBFiles.writeText(fp, ':build', '\n')
            M08FA.Create_Build(BoardName, fp) # M08_Fast_ARDUINO
        else:
            __Environment = 'nano_new'
            OptParts = Split(BuildOptions, ' ')
            if UBound(OptParts) >= 1:
                if OptParts(0) == '--board':
                    BuildOptOnly = OptParts(1)
                    if InStr(BuildOptions, M02.BOARD_NANO_OLD):
                        __Environment = 'nano_old'
                    elif InStr(BuildOptions, M02.BOARD_NANO_FULL):
                        __Environment = 'nano_full'
            __Create_PIO_Build(fp, __Environment, ResultName, ComPort, SrcDir)            
            
        VBFiles.closeFile(fp)
        # VB2PY (UntranslatedCode) On Error GoTo 0
        fn_return_value = 'Call ' + CMD_Name + ' ' + FindStr
        return fn_return_value
    except BaseException as e:
        Debug.Print("Create_Start_Sub-Exception")
        Debug.Print(e)
        VBFiles.closeFile(fp)
        P01.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Start Datei'))
        return fn_return_value

    
def __Create_PIO_Build(fp, Environment, ResultName, ComPort, SrcDir):
    fn_return_value = False
    fp2 = Integer()
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'set path=%path%;' + GetShortPath(Environ(M02.Env_USERPROFILE)) + '\\.platformio\\penv\\Scripts', '\n')
    VBFiles.writeText(fp, 'set ' + M02.Env_USERPROFILE + '=' + GetShortPath(Environ(M02.Env_USERPROFILE)), '\n')
    VBFiles.writeText(fp, 'cd ..', '\n')
    VBFiles.writeText(fp, 'if "%1"=="rebuild" pio run -t clean -e ' + Environment, '\n')
    VBFiles.writeText(fp, 'set flash=-t upload', '\n')
    VBFiles.writeText(fp, 'if "%1"=="noflash" set flash=', '\n')
    VBFiles.writeText(fp, 'pio run %flash% -e ' + Environment + ' --upload-port ' + ComPort, '\n')
    VBFiles.writeText(fp, 'IF ERRORLEVEL 1 ECHO Start_Arduino_Result: %ERRORLEVEL% > "%~p0' + ResultName + '"', '\n')
    VBFiles.writeText(fp, 'cd "%~p0"', '\n')
    VBFiles.writeText(fp, '', '\n')
    fp2 = FreeFile()
    VBFiles.openFile(fp2, SrcDir + '..\\platformio.ini', 'w') 
    #Open Replace(SrcDir, "\LEDs_AutoProg\", "\platformio.inx") For Output As #fp2
    VBFiles.writeText(fp2, '[platformio]', '\n')
    VBFiles.writeText(fp2, 'src_dir = LEDs_AutoProg', '\n')
    VBFiles.writeText(fp2, '    ', '\n')
    VBFiles.writeText(fp2, '[env]', '\n')
    VBFiles.writeText(fp2, 'framework = arduino', '\n')
    VBFiles.writeText(fp2, 'src_build_flags =', '\n')
    VBFiles.writeText(fp2, 'lib_deps =', '\n')
    VBFiles.writeText(fp2, '    FastLED', '\n')
    VBFiles.writeText(fp2, '    NmraDcc', '\n')
    VBFiles.writeText(fp2, '    MobaLedLib=file://../../libraries/MobaLedLib', '\n')
    VBFiles.writeText(fp2, '', '\n')
    VBFiles.writeText(fp2, '[env:esp32]', '\n')
    VBFiles.writeText(fp2, 'Platform = espressif32', '\n')
    VBFiles.writeText(fp2, 'Board = esp32dev', '\n')
    VBFiles.writeText(fp2, 'src_filter = ${env.src_filter} -<pyProg_Generator_MobaLedLib/>', '\n')
    VBFiles.writeText(fp2, 'lib_deps = ${env.lib_deps}', '\n')
    VBFiles.writeText(fp2, '    WiFiManager=https://github.com/tzapu/WiFiManager.git', '\n')
    VBFiles.writeText(fp2, '    EspSoftwareSerial', '\n')
    if not M38.Write_PIO_Extension(fp2):
        VBFiles.closeFile(fp2)
        return fn_return_value
    VBFiles.writeText(fp2, 'build_unflags = -Wall', '\n')
    VBFiles.writeText(fp2, '', '\n')
    VBFiles.writeText(fp2, '[env:nano_new]', '\n')
    VBFiles.writeText(fp2, 'Platform = atmelavr', '\n')
    VBFiles.writeText(fp2, 'Board = nanoatmega328new', '\n')
    VBFiles.writeText(fp2, 'src_filter = ${env.src_filter} -<pyProg_Generator_MobaLedLib/>', '\n')
    VBFiles.writeText(fp2, 'lib_deps = ${env.lib_deps}', '\n')
    VBFiles.writeText(fp2, '    EEProm', '\n')
    VBFiles.writeText(fp2, '    SPI', '\n')
    VBFiles.writeText(fp2, '    AnalogScanner=https://github.com/merose/AnalogScanner/archive/master.zip', '\n')
    if not M38.Write_PIO_Extension(fp2):
        VBFiles.closeFile(fp2)
        return fn_return_value
    VBFiles.writeText(fp2, '', '\n')
    VBFiles.writeText(fp2, 'build_unflags = -Wall', '\n')
    VBFiles.writeText(fp2, '', '\n')
    VBFiles.writeText(fp2, 'upload_flags =', '\n')
    VBFiles.writeText(fp2, '    -u', '\n')
    VBFiles.writeText(fp2, '    -V', '\n')
    VBFiles.writeText(fp2, '[env:nano_old]', '\n')
    VBFiles.writeText(fp2, 'Platform = atmelavr', '\n')
    VBFiles.writeText(fp2, 'Board = nanoatmega328', '\n')
    VBFiles.writeText(fp2, 'src_filter = ${env.src_filter} -<pyProg_Generator_MobaLedLib/>', '\n')
    VBFiles.writeText(fp2, 'lib_deps = ${env.lib_deps}', '\n')
    VBFiles.writeText(fp2, '    EEProm', '\n')
    VBFiles.writeText(fp2, '    SPI', '\n')
    VBFiles.writeText(fp2, '    AnalogScanner=https://github.com/merose/AnalogScanner/archive/master.zip', '\n')
    if not M38.Write_PIO_Extension(fp2):
        VBFiles.closeFile(fp2)
        return fn_return_value
    VBFiles.writeText(fp2, '', '\n')
    VBFiles.writeText(fp2, 'build_unflags = -Wall', '\n')
    VBFiles.writeText(fp2, '', '\n')
    VBFiles.writeText(fp2, 'upload_flags =', '\n')
    VBFiles.writeText(fp2, '    -u', '\n')
    VBFiles.writeText(fp2, '    -V', '\n')
    # 15.02.22: Hardi
    VBFiles.writeText(fp2, '[env:nano_full]', '\n')
    VBFiles.writeText(fp2, 'Platform = atmelavr', '\n')
    VBFiles.writeText(fp2, 'Board = nanoatmega328full', '\n')
    VBFiles.writeText(fp2, 'src_filter = ${env.src_filter} -<pyProg_Generator_MobaLedLib/>', '\n')
    VBFiles.writeText(fp2, 'lib_deps = ${env.lib_deps}', '\n')
    VBFiles.writeText(fp2, '    EEProm', '\n')
    VBFiles.writeText(fp2, '    SPI', '\n')
    VBFiles.writeText(fp2, '    AnalogScanner=https://github.com/merose/AnalogScanner/archive/master.zip', '\n')
    if not M38.Write_PIO_Extension(fp2):
        VBFiles.closeFile(fp2)
        return fn_return_value
    VBFiles.writeText(fp2, '', '\n')
    VBFiles.writeText(fp2, 'build_unflags = -Wall', '\n')
    VBFiles.writeText(fp2, '', '\n')
    VBFiles.writeText(fp2, 'upload_flags =', '\n')
    VBFiles.writeText(fp2, '    -u', '\n')
    VBFiles.writeText(fp2, '    -V', '\n')
    VBFiles.closeFile(fp2)
    fn_return_value = True
    return fn_return_value



def Create_Start_ESP32_Sub(ResultName, ComPort, BuildOptions, InoName, SrcDir, CPUType):
    CMD_Name = 'Start_ESP32_Sub.cmd'

    BuildOptOnly = String()

    OptParts = vbObjectInitialize(objtype=String)

    Board_Version = String()

    Tool_Version = String()

    fp = Integer()

    Name = String()

    kk = Integer()
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    OptParts = Split(BuildOptions, ' ')
    if UBound(OptParts) >= 1:
        if OptParts(0) == '--board':
            BuildOptOnly = OptParts(1)
    if BuildOptOnly == '':
        P01.MsgBox(M09.Get_Language_Str('Fehler: die Build Optionen für den ESP32 sind ungültig:') + vbCr + '  \'' + BuildOptions + '\'', vbCritical, M09.Get_Language_Str('Ungültige Build Optionen'))
        return fn_return_value
    Board_Version = M37.Get_Lib_Version('esp32:esp32')
    if Board_Version == '':
        P01.MsgBox(M09.Get_Language_Str('Fehler: Eine notwendige Arduino Erweiterung ist nicht installiert:') + '  \'' + 'ESP32 Board' + '\'', vbCritical, M09.Get_Language_Str('Fehlende Erweiterung'))
        return fn_return_value
    # don't check for this optional library only                          ' 12.11.21 Juergen
    #If Get_Lib_Version("U8g2") = "" Then
    #   MsgBox Get_Language_Str("Fehler: Eine notwendige Arduino Erweiterung ist nicht installiert:") & "  '" & "U8g2: Library for monochrome display" & "'", vbCritical, Get_Language_Str("Fehlende Erweiterung")
    #   Exit Function
    #End If
    #if M37.Get_Lib_Version('CAN') == '':    ' 01.08.22 Juergen - CAN is now embedded in src/MLL_CAN
    #    P01.MsgBox(M09.Get_Language_Str('Fehler: Eine notwendige Arduino Erweiterung ist nicht installiert:') + '  \'' + 'CAN: Library for ESP32 CAN communication' + '\'', vbCritical, M09.Get_Language_Str('Fehlende Erweiterung'))
    #    return fn_return_value
    # don't check for this optional library only                          ' 12.11.21 Juergen
    #If Get_Lib_Version("WifiManager") = "" Then
    #   MsgBox Get_Language_Str("Fehler: Eine notwendige Arduino Erweiterung ist nicht installiert:") & "  '" & "WifiManager: Library for ESP32 Wifi access" & "'", vbCritical, Get_Language_Str("Fehlende Erweiterung")
    #   Exit Function
    #End If
    if Board_Version != M37.Get_Required_Version('esp32:esp32'):
        P01.MsgBox(M09.Get_Language_Str('Fehler: Die notwendige Version der Arduino Erweiterung ist nicht installiert: ') + '  \'' + 'ESP32 Board ' + M37.Get_Required_Version('esp32:esp32') + '\'', vbCritical, M09.Get_Language_Str('Fehlende Erweiterung'))
        return fn_return_value
    if M30.VersionStr_is_Greater(M37.Get_Required_Version('NmraDcc'), M37.Get_Lib_Version('NmraDcc')):
        P01.MsgBox(M09.Get_Language_Str('Fehler: Die notwendige Version der Arduino Erweiterung ist nicht installiert: ') + '  \'' + 'NmraDcc ' + M37.Get_Required_Version('NmraDcc') + '\'', vbCritical, M09.Get_Language_Str('Fehlende Erweiterung'))
        return fn_return_value
    Tool_Version = M37.Get_Lib_Version('esp32:tools\\esptool_py')
    if Tool_Version == '':
        P01.MsgBox(M09.Get_Language_Str('Fehler: Eine notwendige Arduino Erweiterung ist nicht installiert:') + vbCr + '  \'' + 'esptool_py' + '\'', vbCritical, M09.Get_Language_Str('Fehlende Erweiterung'))
        return fn_return_value
    fp = FreeFile()
    Name = SrcDir + CMD_Name
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM This file was generated by \'' + PG.ThisWorkbook.Name + '\'  ' + Time, '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'REM Build script to compile an ESP32 for the MobaLedLib by Juergen', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM When the script is called the first time all libraries have to be compiled', '\n')
    VBFiles.writeText(fp, 'REM This will tace up to 3 minutes. When the ESP is updated the next time only', '\n')
    VBFiles.writeText(fp, 'REM the changed files have to be processed which will speed up the build process', '\n')
    VBFiles.writeText(fp, 'REM dramatically', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'REM Optional parameters:', '\n')
    VBFiles.writeText(fp, 'REM   rebuild     Rebuilds all (will take up to 3 minutes)', '\n')
    VBFiles.writeText(fp, 'REM   download    Send the hex file to the ESP', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    if M30.Win10_or_newer():
        VBFiles.writeText(fp, 'CHCP 65001 >NUL', '\n')
        
    if M28.Get_Bool_Config_Var("Use_PlatformIO") == False:
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, "set ArduinoLib=" & GetShortPath(M30.DelLast(M02a.Get_Ardu_LibDir())), '\n')
        VBFiles.writeText(fp, 'if not exist MyPrivateBuildScript.cmd (', '\n')
        VBFiles.writeText(fp, '       REM embedded Fast Build and Upload', '\n')
        VBFiles.writeText(fp, '       call :build "' + M30.FilePath(Find_ArduinoExe()) + '" "LEDs_AutoProg.ino" ' + ComPort + ' "' + BuildOptOnly + '" 115200  "%ArduinoLib%" esp32 %*', '\n')
        VBFiles.writeText(fp, ') else (', '\n')
        VBFiles.writeText(fp, '       REM user defined Build and Upload', '\n')
        VBFiles.writeText(fp, '       call MyPrivateBuildScript.cmd "' + M30.FilePath(Find_ArduinoExe()) + '" "LEDs_AutoProg.ino" ' + ComPort + ' "' + BuildOptions + '" 115200  "%ArduinoLib%" esp32 %*', '\n')
        VBFiles.writeText(fp, '       )', '\n')
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 ECHO Start_Arduino_Result: %ERRORLEVEL% > "Start_Arduino_Result.txt"', '\n')
        VBFiles.writeText(fp, 'goto :eof', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, ':build', '\n')
        VBFiles.writeText(fp, 'REM                                                                           **** ToDo: Aktualisieren ***', '\n')
        VBFiles.writeText(fp, 'REM Compile and flash time for ESP 14 sec on Hardis laptop', '\n')
        VBFiles.writeText(fp, 'REM', '\n')
        VBFiles.writeText(fp, 'REM', '\n')
        VBFiles.writeText(fp, 'REM This file could be modified by the user to support special compiler switches', '\n')
        VBFiles.writeText(fp, 'REM It is called if the switch the "Schnelles Build und Upload verwenden:" in the \'Config\' sheet is enabled', '\n')
        VBFiles.writeText(fp, 'REM', '\n')
        VBFiles.writeText(fp, 'REM Parameter:               Example', '\n')
        VBFiles.writeText(fp, 'REM  1: Arduino EXE Path:    "' + M30.FilePath(Find_ArduinoExe()) + '"', '\n')
        VBFiles.writeText(fp, 'REM  2: Ino Name:            "LEDs_AutoProg.ino"', '\n')
        VBFiles.writeText(fp, 'REM  3: Com port:            "COM3"', '\n')
        VBFiles.writeText(fp, 'REM  4: Build options:       "arduino:avr:nano:cpu=atmega328"', '\n')
        VBFiles.writeText(fp, 'REM  5: Baudrate:            "57600" or "115200"', '\n')
        VBFiles.writeText(fp, 'REM  6: Arduino Library path "%USERPROFILE%\\Documents\\Arduino\\libraries"', '\n')
        VBFiles.writeText(fp, 'REM  7: CPU type:            "atmega328p, atmega4809, esp32"', '\n')
        VBFiles.writeText(fp, 'REM  8: options:             ""noflash|norebuild""', '\n')
        VBFiles.writeText(fp, 'REM  additional argument from caller', '\n')
        VBFiles.writeText(fp, 'REM', '\n')
        VBFiles.writeText(fp, 'REM The program uses the captured and adapted command line from the Arduino IDE', '\n')
        VBFiles.writeText(fp, 'REM', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'SET aHome=%~1', '\n')
        VBFiles.writeText(fp, 'SET fqbn=%~4', '\n')
        VBFiles.writeText(fp, 'SET lib=%~6', '\n')
        VBFiles.writeText(fp, 'SET ESP32_BOARD_VERSION=' + Board_Version, '\n')
        VBFiles.writeText(fp, 'SET ESP32_TOOL_VERSION=' + Tool_Version, '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'call :short aTemp "%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_build\\ESP32"', '\n')
        VBFiles.writeText(fp, 'SET aCache=%aTemp%\\cache', '\n')
        VBFiles.writeText(fp, 'call :short packages "%USERPROFILE%' + M02.AppLoc_Ardu + 'packages"', '\n')
        VBFiles.writeText(fp, 'if not exist "%aTemp%\\Sketch"  md "%aTemp%\\Sketch"', '\n')
        VBFiles.writeText(fp, 'if not exist "%aCache%" md "%aCache%"', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'SetLocal EnableDelayedExpansion', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'copy "..\\LEDs_AutoProg\\LEDs_AutoProg.h" "%aTemp%\\Sketch" >nul:', '\n')
        VBFiles.writeText(fp, 'if errorlevel 1 (', '\n')
        VBFiles.writeText(fp, '   echo can\'t copy ..\\LEDs_AutoProg\\LEDs_AutoProg.h to build folder', '\n')
        VBFiles.writeText(fp, '   exit /b 1', '\n')
        VBFiles.writeText(fp, '   )', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'call ::getDirectory headerDir ..\\LEDs_AutoProg\\LEDs_AutoProg.h', '\n')
        VBFiles.writeText(fp, 'call ::getDirectory sketchDir %2', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'if not "%headerDir%"=="%sketchDir%" (', '\n')
        VBFiles.writeText(fp, '   REM Necessary for rebuild         11.11.20:', '\n')
        VBFiles.writeText(fp, '   copy "..\\LEDs_AutoProg\\LEDs_AutoProg.h" . >nul:', '\n')
        VBFiles.writeText(fp, '   if errorlevel 1 (', '\n')
        VBFiles.writeText(fp, '      echo can\'t copy ..\\LEDs_AutoProg\\LEDs_AutoProg.h to actual dir', '\n')
        VBFiles.writeText(fp, '      exit /b 1', '\n')
        VBFiles.writeText(fp, '      )', '\n')
        VBFiles.writeText(fp, ')', '\n')
        VBFiles.writeText(fp, 'REM !! developer option copy additional files !!', '\n')
        VBFiles.writeText(fp, 'if exist AdditionalBuildFiles.txt (', '\n')
        VBFiles.writeText(fp, '   echo updating extra files', '\n')
        VBFiles.writeText(fp, '   for /F %%f in (AdditionalBuildFiles.txt) do (', '\n')
        VBFiles.writeText(fp, '      if exist "%%f" (', '\n')
        VBFiles.writeText(fp, '             echo update file %%f', '\n')
        VBFiles.writeText(fp, '             copy "%%f" "%aTemp%\\Sketch" >nul:', '\n')
        VBFiles.writeText(fp, '             if errorlevel 1 (', '\n')
        VBFiles.writeText(fp, '                echo can\'t copy %%file to build folder', '\n')
        VBFiles.writeText(fp, '                exit /b 1', '\n')
        VBFiles.writeText(fp, '             )', '\n')
        VBFiles.writeText(fp, '      ) else (', '\n')
        VBFiles.writeText(fp, '             echo Additional build file \'%%f\' not found', '\n')
        VBFiles.writeText(fp, '             pause', '\n')
        VBFiles.writeText(fp, '             )', '\n')
        VBFiles.writeText(fp, '      )', '\n')
        VBFiles.writeText(fp, ')', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'rem check if prebuild targets exist and the current ino isn\'t newer', '\n')
        VBFiles.writeText(fp, 'set srcFile=%~2', '\n')
        VBFiles.writeText(fp, 'set cppFile=%aTemp%\\sketch\\%srcFile%.cpp', '\n')
        VBFiles.writeText(fp, '', '\n')
        ## VB2PY (CheckDirective) VB directive took path 1 on 1
        VBFiles.writeText(fp, 'copy "%srcFile%" "%cppFile%" /Y >nul:', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'if exist "%aTemp%\\rebuildFailed.txt" (', '\n')
        VBFiles.writeText(fp, '   echo Last rebuild failed ;-(', '\n')
        VBFiles.writeText(fp, '   echo Press ENTER to rebuild everything', '\n')
        VBFiles.writeText(fp, '   if ""%8""=="""" pause', '\n')
        VBFiles.writeText(fp, '   goto :rebuild', '\n')
        VBFiles.writeText(fp, '   )', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'rem if the pre-build files are not there we need to do a complete new build', '\n')
        VBFiles.writeText(fp, 'if not exist "%cppFile%" (', '\n')
        VBFiles.writeText(fp, '   echo CPP File "%cppFile%" does\'n exist, rebuild ...', '\n')
        VBFiles.writeText(fp, '   goto :rebuild', '\n')
        VBFiles.writeText(fp, '   )', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'if "%8"=="rebuild" (', '\n')
        VBFiles.writeText(fp, '   echo Rebuild called from the command line', '\n')
        VBFiles.writeText(fp, '   goto :rebuild', '\n')
        VBFiles.writeText(fp, '   )', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'if "%8"=="flash" (', '\n')
        VBFiles.writeText(fp, '   goto :download', '\n')
        VBFiles.writeText(fp, '   )', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'rem now get date/time of both files to see if time is equal', '\n')
        VBFiles.writeText(fp, 'FOR /F "tokens=* USEBACKQ" %%F IN (`forfiles /p "%atemp%\\sketch" /m "%srcFile%.cpp" /C "cmd /c echo @fdate @ftime"`) DO SET DATE1=%%F', '\n')
        VBFiles.writeText(fp, 'FOR /F "tokens=* USEBACKQ" %%F IN (`forfiles /m "%srcFile%" /C "cmd /c echo @fdate @ftime"`) DO SET DATE2=%%F', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'echo %srcFile%.cpp has date %date1%', '\n')
        VBFiles.writeText(fp, 'echo %srcFile% has date %date2%', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'rem if equal then srcfile isn\'t newer', '\n')
        VBFiles.writeText(fp, 'IF "%DATE1%"=="%DATE2%" goto fastbuild', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'rem now get the newest file', '\n')
        VBFiles.writeText(fp, 'rem to compare, both file must be in same directory', '\n')
        VBFiles.writeText(fp, 'copy "%srcFile%" "%aTemp%\\sketch\\" >nul:', '\n')
        VBFiles.writeText(fp, 'FOR /F %%i IN (\'DIR /B /O:D "%cppFile%" "%aTemp%\\sketch\\%srcFile%"\') DO SET NEWEST=%%i', '\n')
        VBFiles.writeText(fp, 'del "%aTemp%\\sketch\\%srcFile%" >nul:', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'rem check which file is newer, if source is new we need to run a arduino build to recreate the .ino.cpp file', '\n')
        VBFiles.writeText(fp, 'if "%NEWEST%"=="%srcFile%" (', '\n')
        VBFiles.writeText(fp, '   echo New file detected "%NEWEST%", rebuild...', '\n')
        VBFiles.writeText(fp, '   goto :rebuild', '\n')
        VBFiles.writeText(fp, '   ) ', '\n')
        VBFiles.writeText(fp, 'ECHO Newer file is %NEWEST%', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'goto :fastbuild', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, ':getDirectory <resultVar> <pathVar>', '\n')
        VBFiles.writeText(fp, '(', '\n')
        VBFiles.writeText(fp, '    set "%~1=%~d2%~p2"', '\n')
        VBFiles.writeText(fp, '    goto :eof', '\n')
        VBFiles.writeText(fp, ')', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, ':getShortName <resultVar> <filename>', '\n')
        VBFiles.writeText(fp, '(', '\n')
        VBFiles.writeText(fp, '    set %~1=%~s2', '\n')
        VBFiles.writeText(fp, '    goto :eof', '\n')
        VBFiles.writeText(fp, ')', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, ':fastbuild', '\n')
        VBFiles.writeText(fp, 'echo Running fastbuild', '\n')
        VBFiles.writeText(fp, 'call Fastbuild.cmd %8', '\n')
        VBFiles.writeText(fp, 'if errorlevel 1 (', '\n')
        VBFiles.writeText(fp, '    rem use argument norebuild to avoid rebuild in this case', '\n')
        VBFiles.writeText(fp, '    set rebuild=1') 
        VBFiles.writeText(fp, '    if ""%8""==""norebuild"" set rebuild=0') 
        VBFiles.writeText(fp, '    if ""%8""==""additional"" set rebuild=0') 
        VBFiles.writeText(fp, '') 
        VBFiles.writeText(fp, '    if "%rebuild%"=="1" (', '\n')                            #in case the librarys have been changed
        VBFiles.writeText(fp, '        rem in case that FastBuild.cmd returned errolevel 9 also a rebuild won\'t help', '\n')
        VBFiles.writeText(fp, '        if not errorlevel 9 (', '\n')
        VBFiles.writeText(fp, '            echo Fastbuild failed, trying a rebuild...', '\n')
        VBFiles.writeText(fp, '            goto rebuild', '\n')
        VBFiles.writeText(fp, '        )', '\n')
        VBFiles.writeText(fp, '    )', '\n')
        VBFiles.writeText(fp, ')', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'goto download', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, ':rebuild', '\n')
        VBFiles.writeText(fp, 'echo.', '\n')
        VBFiles.writeText(fp, 'echo Running rebuild... Be patient, this will take up to 3 minutes ;-(((', '\n')
        VBFiles.writeText(fp, 'echo.', '\n')
        VBFiles.writeText(fp, 'if exist "%aTemp%" del "%aTemp%" /s/q >nul:', '\n')
        VBFiles.writeText(fp, 'if exist "%aTemp%\\link.cmd" del "%aTemp%\\link.cmd"', '\n')
        VBFiles.writeText(fp, 'echo %date% > "%aTemp%\\rebuildFailed.txt"', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'REM *** Call the arduino builder ***', '\n')
        VBFiles.writeText(fp, 'call :write "%aHome%\\arduino-builder" -compile -logger=human ^', '\n')
        VBFiles.writeText(fp, '     -hardware "%packages%" ^', '\n')
        VBFiles.writeText(fp, '     -tools "%aHome%\\tools-builder" ^', '\n')
        VBFiles.writeText(fp, '     -tools "%aHome%\\hardware\\tools\\avr" ^', '\n')
        VBFiles.writeText(fp, '     -built-in-libraries "%aHome%\\libraries" -libraries "%LIB%" ^', '\n')
        VBFiles.writeText(fp, '     -fqbn=%fqbn% -build-path "%aTemp%" ^', '\n')
        VBFiles.writeText(fp, '     -warnings=default ^', '\n')
        VBFiles.writeText(fp, '     -build-cache "%aCache%" ^', '\n')
        VBFiles.writeText(fp, '     -prefs=build.warn_data_percentage=75 ^', '\n')
        VBFiles.writeText(fp, '     -prefs=runtime.tools.avrdude.path="%aHome%\\hardware\\tools\\avr" ^', '\n')
        VBFiles.writeText(fp, '     -prefs=runtime.tools.avr-gcc.path="%aHome%\\hardware\\tools\\avr" >"%aTemp%\\compile.cmd"', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'if exist AdditionalBuildOptions.txt (', '\n')
        VBFiles.writeText(fp, '  for /F "delims=" %%i in (AdditionalBuildOptions.txt) do call :write %%i >>"%aTemp%\\compile.cmd"', '\n')
        VBFiles.writeText(fp, ')', '\n')
        VBFiles.writeText(fp, 'call :write %srcFile% >>"%aTemp%\\compile.cmd"', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'call "%aTemp%\\compile.cmd"', '\n')
        VBFiles.writeText(fp, 'if not errorlevel 1 (', '\n')
        VBFiles.writeText(fp, '  if exist "%aTemp%\\rebuildFailed.txt" del "%aTemp%\\rebuildFailed.txt" >nul:', '\n')
        VBFiles.writeText(fp, ')', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, ':download', '\n')
        VBFiles.writeText(fp, 'if "%8"=="noflash" goto :EOF', '\n')                         #12.02.22: Juergen
        VBFiles.writeText(fp, 'if not errorlevel 1 (', '\n')
        VBFiles.writeText(fp, '   set uploadTo=%3', '\n')
        VBFiles.writeText(fp, '   if not "%target%"=="" set uploadTo=%target%', '\n')
        VBFiles.writeText(fp, '   echo Uploading to !uploadTo!', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '   REM *** Flash program ***', '\n')
        VBFiles.writeText(fp, '   if "!uploadTo:~0,3!"=="COM" (', '\n')
        # 17.11.20: Added: 0x8000 ...
        # 11.03.21: Added: 0xE000 and 0x1000
        VBFiles.writeText(fp, '          "%packages%\\esp32\\tools\\esptool_py\\%ESP32_TOOL_VERSION%/esptool.exe" --chip esp32 --port \\\\.\\!uploadTo! --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect ' + ' 0xE000  "%packages%\\esp32\\hardware\\esp32\\%ESP32_BOARD_VERSION%/tools/partitions/boot_app0.bin"' + ' 0x1000  "%packages%\\esp32\\hardware\\esp32\\%ESP32_BOARD_VERSION%/tools/sdk/bin/bootloader_qio_80m.bin"' + ' 0x10000 "%aTemp%\\%srcFile%.bin"' + ' 0x8000  "%aTemp%\\%srcFile%.partitions.bin"', '\n')
        VBFiles.writeText(fp, '   ) else (', '\n')
        VBFiles.writeText(fp, '          "%packages%\\esp32\\hardware\\esp32\\%ESP32_BOARD_VERSION%/tools/espota.exe" -i !uploadTo! -p 3232 --auth= -f "%aTemp%\\%srcFile%.bin"', '\n')
        VBFiles.writeText(fp, '          )', '\n')
        VBFiles.writeText(fp, '    REM *** caller expects a positive errorlevel in error case, but ESPTOOL returns errorlevel -1', '\n')
        VBFiles.writeText(fp, '    if not errorlevel 0 exit /b 1', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, ')', '\n')
        VBFiles.writeText(fp, 'Goto :EOF', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, ':: write a text without newline', '\n')
        VBFiles.writeText(fp, ':write', '\n')
        VBFiles.writeText(fp, 'echo | set /p x="%* "', '\n')
        VBFiles.writeText(fp, 'goto :eof', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, ':short', '\n')
        VBFiles.writeText(fp, 'set %1=%~s2', '\n')
        VBFiles.writeText(fp, 'goto :eof', '\n')
        VBFiles.writeText(fp, '', '\n')
    else:
        __Create_PIO_Build(fp, "esp32", ResultName, ComPort, SrcDir)     # 13.02.22: Juergen
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = 'Call ' + CMD_Name
    #*HL if GetAsyncKeyState(VK_SHIFT) != 0:
    #*HL     fn_return_value = Create_Start_ESP32_Sub() + ' rebuild'
    return fn_return_value

    VBFiles.closeFile(fp)
    P01.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Start Datei'))
    return fn_return_value

def Create_Cmd_file(ResultName, ComPort, BuildOptions, InoName, Mode, SrcDir, CPUType):
    USE_SUBCOMMAND = True

    CommandStr = String()

    BuildDir = String()

    BuildDirForScript = Variant()

    fp = Integer()

    Name = String()

    i = Integer()
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Arduino start Parameters see:
    #   https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc
    #   https://forum.arduino.cc/index.php?topic=550577.0
    #   http://inotool.org/
    # 26.09.19:
    # Manchmal Spinnt der Compiler. Er erzeugt seltsame Fehlermeldungen:
    #    " internal compiler error: Segmentation fault "
    # Wenn der Fehler ein mal komm, dann muss irgend was am Programm verädert werden,
    # dann geht es meißtens wieder. Dann kann man die Änderung auch wieder rückgängig
    # machen ohne das der Fehler wieder auftritt ;-(
    #
    # Wenn man das Verzeichnis "C:\Users\Hardi\AppData\Arduino_Build_23_B.LEDs_AutoProg"
    # löscht, dann geht es auch ohne Änderung am Programm.
    #
    # Das Weglassen des Kommandozeilenschalters "--preserve-temp-files" bringt nichts.
    # Das Problem ist hier beschrieben:
    #  https://github.com/arduino/Arduino/issues/8821
    #  https://github.com/arduino/Arduino/issues/7949
    # Im zweiten Post wird behauptet, dass der Fehler mit der Version 1.8.10 nicht mehr auftritt.
    # Dummerweise produziert diese sehr viele Debug Meldungen.
    #
    # Ich habe jetzt mal das Neueste Board Paket für den Nano (1.8.1) Installiert. Mal schauen ob es
    # jetzt besser ist. Dummerweise habe ich mir nicht gemerkt welches Board Paket ich vorher hatte.
    # Es war irgend was mit 1.6?
    # remove "'" in front of the --board options
    BuildOptions = BuildOptions.replace("'", "")    
    
    Debug.Print("Create_Cmd_file")
    if Dir(SrcDir + ResultName) != '':
        Kill(SrcDir + ResultName)
        # 16.03.20: Added Thisworkbook...
    ## VB2PY (CheckDirective) VB directive took path 1 on 1
    BuildDir = Replace(Environ('APPDATA'), 'Roaming', '') + 'Arduino_Build_' + Replace(InoName, '.ino', '')
    BuildDirForScript = '%APPDATA%/../' + 'Arduino_Build_' + Replace(InoName, '.ino', '')
    if Dir(BuildDir + '/.') == '':
        # VB2PY (UntranslatedCode) On Error Resume Next
        MkDir(BuildDir)
        # VB2PY (UntranslatedCode) On Error GoTo 0
        BuildDirForScript = '%APPDATA%/../' + 'Arduino_Build_' + Replace(InoName, '.ino', '')
        #Debug.Print "BuildDir='" & BuildDir & "'"
    # Other options:  --verbose-build --verbose-upload"
    #   Boards  see: C:\P<rogram Files (x86)\Arduino\hardware\arduino\avr\boards.txt
    #   New Bootloader: nano.menu.cpu.atmega328=ATmega328P
    CommandStr = '"' + Find_ArduinoExe() + '" "' + InoName + '" --upload --port \\\\.\\' + ComPort + ' ' + BuildOptions

    if BuildDirForScript != '':
        CommandStr = CommandStr + ' --pref build.path="' + BuildDirForScript + '"' + ' --preserve-temp-files'
    if USE_SUBCOMMAND:
        if M02a.Get_BoardTyp() == 'ESP32':
            CommandStr = Create_Start_ESP32_Sub(ResultName, ComPort, BuildOptions, InoName, SrcDir, CPUType)
        else:
            CommandStr = Create_Start_Sub(M02a.Get_BoardTyp(), ResultName, ComPort, BuildOptions, InoName, SrcDir, CPUType)
        if CommandStr == '':
            return fn_return_value
    # filter the SerialDiscovery messages                                     ' 16.03.20:
    #CommandStr = CommandStr & " 2>&1 | find /v "" StatusLogger "" | find /v ""serial.SerialDiscovery"" | find /v ""fungsvorgang..."""
    fp = FreeFile()
    Name = SrcDir + 'Start_Arduino.cmd'
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM This file was generated by \'' + PG.ThisWorkbook.Name + '\'  ' + Time, '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'if exist "' + ResultName + '" del "' + ResultName + '"', '\n')
    if (Mode == 'Left'):
        VBFiles.writeText(fp, 'COLOR 1F', '\n')
        VBFiles.writeText(fp, 'ECHO    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "', '\n')
        VBFiles.writeText(fp, 'ECHO    "    Zum                                                                  "', '\n')
        VBFiles.writeText(fp, 'ECHO    "     PC                    Prog_Generator ' + M30.AddSpaceToLen(M02.Prog_Version, 20) + ' by Hardi  "', '\n')
        VBFiles.writeText(fp, 'ECHO    "      \\\\                                                                 "', '\n')
        VBFiles.writeText(fp, 'ECHO    "       \\\\                                                                "', '\n')
        VBFiles.writeText(fp, 'ECHO    "    ____\\\\___________________                                            "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  | [_] | | [_] |[oo]    |  ' + M09.Get_Language_Str('Achtung: Es muss der linke               "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | |     |        |  ' + M09.Get_Language_Str('Arduino mit dem PC verbunden             "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | |     |        |  ' + M09.Get_Language_Str('sein.                                    "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  | LED | |     |        |                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  | Nano| |     |        |  ' + M09.Get_Language_Str('Wenn alles gut geht, dann wird das       "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | |     |        |  ' + M09.Get_Language_Str('Fenster ohne eine weitere Meldung        "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | |     |        |  ' + M09.Get_Language_Str('geschlossen (Liest ja eh keiner).        "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |_____| |_____| [O]    |                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    [@] [@] [@]          |  ' + M09.Get_Language_Str('Falls Probleme auftreten, dann wird      "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |__________________[:::]__|  ' + M09.Get_Language_Str('das angezeigt.                           "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "                                                                         "', '\n')
        VBFiles.writeText(fp, 'ECHO    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "', '\n')
    elif (Mode == 'Right'):
        VBFiles.writeText(fp, 'COLOR 2F', '\n')
        if (M25.Page_ID == 'DCC'):
            RightName = ' DCC '
        elif (M25.Page_ID == 'Selectrix'):
            RightName = ' S X '
        elif (M25.Page_ID == 'Loconet'):
            RightName = 'LocoN'
        else:
            P01.MsgBox('Interner Fehler: Unbekante M25.Page_ID: \'' + M25.Page_ID + '\'', vbCritical, 'Interner Fehler')
            M30.EndProg()
        VBFiles.writeText(fp, 'ECHO    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "', '\n')
        VBFiles.writeText(fp, 'ECHO    "            Zum                                                          "', '\n')
        VBFiles.writeText(fp, 'ECHO    "             PC            Prog_Generator ' + M30.AddSpaceToLen(M02.Prog_Version, 20) + ' by Hardi  "', '\n')
        VBFiles.writeText(fp, 'ECHO    "              \\\\                                                         "', '\n')
        VBFiles.writeText(fp, 'ECHO    "               \\\\                                                        "', '\n')
        VBFiles.writeText(fp, 'ECHO    "    ____________\\\\___________                                            "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  | [_] | | [_] |[oo]    |  ' + M09.Get_Language_Str('Achtung: Es muss der rechte              "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | |     |        |  ' + M09.Get_Language_Str('Arduino mit dem PC verbunden             "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | |     |        |  ' + M09.Get_Language_Str('sein.                                    "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | |' + RightName + '|        |                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | | Nano|        |  ' + M09.Get_Language_Str('Wenn alles gut geht, dann wird das       "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | |     |        |  ' + M09.Get_Language_Str('Fenster ohne eine weitere Meldung        "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | |     |        |  ' + M09.Get_Language_Str('geschlossen (Liest ja eh keiner).        "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |_____| |_____| [O]    |                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    [@] [@] [@]          |  ' + M09.Get_Language_Str('Falls Probleme auftreten, dann wird      "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |__________________[:::]__|  ' + M09.Get_Language_Str('das angezeigt.                           "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "                                                                         "', '\n')
        VBFiles.writeText(fp, 'ECHO    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "', '\n')
    elif (Mode == 'CAN'):
        VBFiles.writeText(fp, 'COLOR 3F', '\n')
        VBFiles.writeText(fp, 'ECHO    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "', '\n')
        VBFiles.writeText(fp, 'ECHO    "    Zum                                                                  "', '\n')
        VBFiles.writeText(fp, 'ECHO    "     PC                    Prog_Generator ' + M30.AddSpaceToLen(M02.Prog_Version, 20) + ' by Hardi  "', '\n')
        VBFiles.writeText(fp, 'ECHO    "      \\\\                                                                 "', '\n')
        VBFiles.writeText(fp, 'ECHO    "       \\\\                                                                "', '\n')
        VBFiles.writeText(fp, 'ECHO    "    ____\\\\___________________                                            "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  | [_] |O _________    _|  ' + M09.Get_Language_Str('Achtung: Es wird nur der linke           "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | |         |  |C|  ' + M09.Get_Language_Str('Arduino und ein MCP2515 CAN Modul        "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | | MCP2515 |  |A|  ' + M09.Get_Language_Str('verwendet.                               "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  | LED | |   CAN   |  |N|                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  | Nano| |  Modul  |   ~|  ' + M09.Get_Language_Str('Wenn alles gut geht, dann wird das       "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     | |_________|    |  ' + M09.Get_Language_Str('Fenster ohne eine weitere Meldung        "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |     |                |  ' + M09.Get_Language_Str('geschlossen (Liest ja eh keiner).        "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |  |_____|         [O]    |                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    [@] [@] [@]          |  ' + M09.Get_Language_Str('Falls Probleme auftreten, dann wird      "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |__________________[:::]__|  ' + M09.Get_Language_Str('das angezeigt.                           "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "                                                                         "', '\n')
        VBFiles.writeText(fp, 'ECHO    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "', '\n')
    elif (Mode == 'ESP32'):
        VBFiles.writeText(fp, 'COLOR 1E', '\n')
        VBFiles.writeText(fp, 'ECHO    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "', '\n')
        VBFiles.writeText(fp, 'ECHO    "        Zum                                                              "', '\n')
        VBFiles.writeText(fp, 'ECHO    "         PC                Prog_Generator ' + M30.AddSpaceToLen(M02.Prog_Version, 19) + ' by Juergen "', '\n')
        VBFiles.writeText(fp, 'ECHO    "          \\\\                                                   and Hardi "', '\n')
        VBFiles.writeText(fp, 'ECHO    "           \\\\                                                            "', '\n')
        VBFiles.writeText(fp, 'ECHO    "    ________\\\\_______________                                            "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    | # [_] # |  [oo]   _|  ' + M09.Get_Language_Str('Achtung: Es wird nur ein ESP32           "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    |         |  DCC   |C|  ' + M09.Get_Language_Str('         Modul verwendet.                "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    | ::::::: |        |A|                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    |  _____  |        |N|                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    | |     | |         ~|  ' + M09.Get_Language_Str('Wenn alles gut geht, dann wird das       "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    | |ESP32| |          |  ' + M09.Get_Language_Str('Fenster ohne eine weitere Meldung        "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    | |_____| |          |  ' + M09.Get_Language_Str('geschlossen (Liest ja eh keiner).        "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    |_________|   [O]    |                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    [@] [@] [@]          |  ' + M09.Get_Language_Str('Falls Probleme auftreten, dann wird      "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |__________________[:::]__|  ' + M09.Get_Language_Str('das angezeigt.                           "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "                                                                         "', '\n')
        VBFiles.writeText(fp, 'ECHO    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "', '\n')
    elif (Mode == 'PICO'):
        VBFiles.writeText(fp, 'COLOR 0E', '\n')
        VBFiles.writeText(fp, 'ECHO    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "', '\n')
        VBFiles.writeText(fp, 'ECHO    "        Zum                                                              "', '\n')
        VBFiles.writeText(fp, 'ECHO    "         PC                Prog_Generator ' + M30.AddSpaceToLen(M02.Prog_Version, 19) + ' by Juergen "', '\n')
        VBFiles.writeText(fp, 'ECHO    "          \\\\                                                   and Hardi "', '\n')
        VBFiles.writeText(fp, 'ECHO    "           \\\\                                                            "', '\n')
        VBFiles.writeText(fp, 'ECHO    "    ________\\\\_______________                                            "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    | # [_] # |  [oo]   _|  ' + M09.Get_Language_Str('Achtung: Es wird nur ein Raspberry PICO  "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    |         |  DCC   |C|  ' + M09.Get_Language_Str('         Modul verwendet.                "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    | ::::::: |        |A|                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    |  _____  |        |N|                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    | |     | |         ~|  ' + M09.Get_Language_Str('Wenn alles gut geht, dann wird das       "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    | |PICO | |          |  ' + M09.Get_Language_Str('Fenster ohne eine weitere Meldung        "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    | |_____| |          |  ' + M09.Get_Language_Str('geschlossen (Liest ja eh keiner).        "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    |_________|   [O]    |                                           "', '\n')
        VBFiles.writeText(fp, 'ECHO    "   |    [@] [@] [@]          |  ' + M09.Get_Language_Str('Falls Probleme auftreten, dann wird      "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "   |__________________[:::]__|  ' + M09.Get_Language_Str('das angezeigt.                           "'), '\n')
        VBFiles.writeText(fp, 'ECHO    "                                                                         "', '\n')
        VBFiles.writeText(fp, 'ECHO    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "', '\n')
    VBFiles.writeText(fp, '', '\n')
    if M30.Win10_or_newer():
        VBFiles.writeText(fp, 'CHCP 65001 >NUL', '\n')
    VBFiles.writeText(fp, 'ECHO|SET /p="Verzeichnis: "', '\n')
    VBFiles.writeText(fp, 'CD', '\n')
    VBFiles.writeText(fp, 'ECHO.', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, CommandStr, '\n')
    #Print #fp, "Pause"   ' Debug
    VBFiles.writeText(fp, 'ECHO.', '\n')
    VBFiles.writeText(fp, '', '\n')
    if USE_SUBCOMMAND:
        VBFiles.writeText(fp, 'IF EXIST "' + ResultName + '" (', '\n')
    else:
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 (', '\n')
        VBFiles.writeText(fp, '   ECHO Start_Arduino_Result: %ERRORLEVEL% > "' + ResultName + '"', '\n')
    VBFiles.writeText(fp, '   COLOR 4F', '\n')
    VBFiles.writeText(fp, '   ECHO   ****************************************', '\n')
    VBFiles.writeText(fp, '   ECHO    ' + M09.Get_Language_Str('Da ist was schief gegangen ;-('), '\n')
    VBFiles.writeText(fp, '   ECHO   ****************************************', '\n')
    VBFiles.writeText(fp, '   Pause', '\n')
    VBFiles.writeText(fp, '   )', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = Name
    return fn_return_value
    VBFiles.closeFile(fp)
    P01.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Start Datei'))
    return fn_return_value

def Create_ARDUINO_IDE_Cmd(ResultName, ComPort, BuildOptions, InoName, Mode, SrcDir, CPUType):
   
    CommandStr = String()

    BuildDir = String()

    BuildDirForScript = Variant()

    fp = Integer()

    Name = String()

    i = Integer()
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Arduino start Parameters see:
    #   https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc
    #   https://forum.arduino.cc/index.php?topic=550577.0
    #   http://inotool.org/
    # 26.09.19:
    # Manchmal Spinnt der Compiler. Er erzeugt seltsame Fehlermeldungen:
    #    " internal compiler error: Segmentation fault "
    # Wenn der Fehler ein mal komm, dann muss irgend was am Programm verädert werden,
    # dann geht es meißtens wieder. Dann kann man die Änderung auch wieder rückgängig
    # machen ohne das der Fehler wieder auftritt ;-(
    #
    # Wenn man das Verzeichnis "C:\Users\Hardi\AppData\Arduino_Build_23_B.LEDs_AutoProg"
    # löscht, dann geht es auch ohne Änderung am Programm.
    #
    # Das Weglassen des Kommandozeilenschalters "--preserve-temp-files" bringt nichts.
    # Das Problem ist hier beschrieben:
    #  https://github.com/arduino/Arduino/issues/8821
    #  https://github.com/arduino/Arduino/issues/7949
    # Im zweiten Post wird behauptet, dass der Fehler mit der Version 1.8.10 nicht mehr auftritt.
    # Dummerweise produziert diese sehr viele Debug Meldungen.
    #
    # Ich habe jetzt mal das Neueste Board Paket für den Nano (1.8.1) Installiert. Mal schauen ob es
    # jetzt besser ist. Dummerweise habe ich mir nicht gemerkt welches Board Paket ich vorher hatte.
    # Es war irgend was mit 1.6?
    Debug.Print("Create_ARDUINO_IDE_Cmd")
    if Dir(SrcDir + ResultName) != '':
        Kill(SrcDir + ResultName)
        # 16.03.20: Added Thisworkbook...
    ## VB2PY (CheckDirective) VB directive took path 1 on 1
    BuildDir = Replace(Environ('APPDATA'), 'Roaming', '') + 'Arduino_Build_' + Replace(InoName, '.ino', '')
    BuildDirForScript = '%APPDATA%/../' + 'Arduino_Build_' + Replace(InoName, '.ino', '')
    if Dir(BuildDir + '/.') == '':
        # VB2PY (UntranslatedCode) On Error Resume Next
        MkDir(BuildDir)
        # VB2PY (UntranslatedCode) On Error GoTo 0
        BuildDirForScript = '%APPDATA%/../' + 'Arduino_Build_' + Replace(InoName, '.ino', '')
        #Debug.Print "BuildDir='" & BuildDir & "'"
    # Other options:  --verbose-build --verbose-upload"
    #   Boards  see: C:\P<rogram Files (x86)\Arduino\hardware\arduino\avr\boards.txt
    #   New Bootloader: nano.menu.cpu.atmega328=ATmega328P
    CommandStr = '"' + Find_ArduinoExe() + '" "' + InoName + '" --upload --port ' + ComPort + ' ' + BuildOptions
    if BuildDirForScript != '':
        CommandStr = CommandStr + ' --pref build.path="' + BuildDirForScript + '"' + ' --preserve-temp-files'
        
    # remove "'" in front of the --board options

    #print(CommandStr)
    CommandStr = CommandStr.replace("'", "")
    #print(CommandStr)

    # filter the SerialDiscovery messages                                     ' 16.03.20:
    #CommandStr = CommandStr & " 2>&1 | find /v "" StatusLogger "" | find /v ""serial.SerialDiscovery"" | find /v ""fungsvorgang..."""
    
    #if ArduinoType == " ":
    #    self.startfile = [filedirname,ino_filename,"--upload","--port",serport,"--pref","programmer=arduino:arduinoisp","--pref","build.path=../Arduino_Build_LEDs_AutoProg","--preserve-temp-files"]
    #else:
    #    self.startfile = [filedirname,ino_filename,"--upload","--port",serport,"--board",ArduinoType,"--pref","programmer=arduino:arduinoisp","--pref","build.path=../Arduino_Build_LEDs_AutoProg","--preserve-temp-files"]
    
    #logging.debug(repr(self.startfile)) 
    logging.debug("Commandstr:"+CommandStr)
    
    fn_return_value = CommandStr
    return fn_return_value

    P01.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Start Datei'))
    return fn_return_value

def Get_New_Board_Type(FirmwareVer):
    #------------------------------------------------------------------
    # Problem:
    # There is no way to detect if the HFUSE is set to support a small (512 byte) boot loader
    # because the fueses can't be read over the serial port.
    # By default the Arduino dosn't change the HFUSE. Therefore a boot loader size of 2 KB is
    # reserved even thow the bootloader uses only 512 byte.
    # HFUSE: DA = 2K
    #        DE = 512 Byte
    #
    # We use a special optiboot firmeware version 108.1 to detect if the HFUSE is set to
    # support the full memory
    if FirmwareVer == '108.1':
        fn_return_value = M02.BOARD_NANO_FULL
    else:
        fn_return_value = M02.BOARD_NANO_NEW
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: BuildOptions - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DeviceSignature - ByRef 
def Check_If_Arduino_could_be_programmed_and_set_Board_type(ComPortColumn, BuildOptColumn, BuildOptions, DeviceSignature,CreateFilesOnly=False): # 20.12.21: Jürgen add CreateFilesOnly for programatically generation of header files
    
    Start_Baudrate = int()

    BaudRate = int()

    ComPort = int()

    Msg = String()

    Retry = Boolean()

    AutoDetect = Boolean()
    fn_return_value=False
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The "Buzy" check and the automatic board detection is only active if Autodetect is enabled
    # Otherwise the values in the BuildOptColumn are used
    # 17.06.20: ToDo: Das stimmt nicht. Die Routine wird immer aufgerufen ;-(
    # Result: BuildOptions
    while 1:
        if CreateFilesOnly:
            BuildOptions = P01.Cells(M02.SH_VARS_ROW, BuildOptColumn)
            fn_return_value=True
            return fn_return_value, BuildOptions, DeviceSignature
        
        
        """ 21.01.2021 Optionally get IP Address from cell left to com port"""
        if M02a.Get_BoardTyp() == 'ESP32' and P01.Cells(M02.SH_VARS_ROW, ComPortColumn + 1) != '':
            BuildOptions = P01.Cells(M02.SH_VARS_ROW, BuildOptColumn)
            fn_return_value = True
            return fn_return_value, BuildOptions, DeviceSignature        
        
        Retry = False
        fn_return_value = False
        if M07.Check_USB_Port_with_Dialog(ComPortColumn) == False:
            return fn_return_value, BuildOptions, DeviceSignature
        
            # Display Dialog if the COM Port is negativ and ask the user to correct it
        # Now we are sure that the com port is positiv. Check if it could be accesed and get the Baud rate
        BuildOptions = P01.Cells(M02.SH_VARS_ROW, BuildOptColumn)
        # remove leading "'"
        if len(BuildOptions)>0 and BuildOptions[0]=="'":
            BuildOptions = BuildOptions[1:]
        AutoDetect = InStr(BuildOptions, M02.AUTODETECT_STR) > 0
        if AutoDetect:
            BuildOptions = Trim(Replace(BuildOptions, M02.AUTODETECT_STR, ''))
            if InStr(BuildOptions, M02.BOARD_NANO_OLD) or InStr(BuildOptions, M02.BOARD_UNO_NORM) > 0:
                Start_Baudrate = 57600
            else:
                Start_Baudrate = 115200
        ComPortStr = P01.Cells(M02.SH_VARS_ROW, ComPortColumn)
        if IsNumeric(ComPortStr):
            ComPort = "COM"+ComPortStr
        else:
            ComPort = ComPortStr
        #ComPort = P01.val(P01.Cells(M02.SH_VARS_ROW, ComPortColumn))
        #if ComPort > 255:                                                       # 03.03.22: Juergen avoid overrun error
        #    ComPort = 0
        CheckCOMPort_Txt = M07.Check_If_Port_is_Available_And_Get_Name(ComPort)
        
        FirmwareVer = ""
        BaudRate = 0
        if CheckCOMPort_Txt != '':
            if M02a.Get_BoardTyp() == 'ESP32':
                BaudRate = 921600
            elif M02a.Get_BoardTyp() == 'PICO':
                BaudRate = 921600
            else:
                BaudRate = M07.Get_Arduino_Baudrate(ComPort, Start_Baudrate, DeviceSignature, FirmwareVer)
        if BaudRate <= 0:
            if M07.Check_If_Port_is_Available(ComPort) == False:
                Msg = M09.Get_Language_Str('Fehler: Es ist kein Arduino an COM Port #1# angeschlossen.')
            elif BaudRate == 0:
                Msg = M09.Get_Language_Str('Fehler: Das Gerät am COM Port #1# wurde nicht als Arduino erkannt.' + vbCr + 'Evtl. ist es ein defekter Arduino oder der Bootloader ist falsch.')
            else:
                Msg = M09.Get_Language_Str('Fehler: Der COM Port #1# wird bereits von einem anderen Programm benutzt.' + vbCr + 'Das kann z.B. der serielle Monitor der Arduino IDE oder das Farbtestprogramm sein.' + vbCr + vbCr + 'Das entsprechende Programm muss geschlossen werden.')
            Msg = Replace(Msg, "#1#", str(ComPort)) + vbCr + vbCr + M09.Get_Language_Str('Wollen sie es noch mal mit einem anderen Arduino oder einem anderen COM Port versuchen?') + vbCr + vbCr + M09.Get_Language_Str('Mit \'Nein\' wird die Meldung ignoriert und versucht den Arduino trotzdem zu programmieren.')
            select_variable_ = P01.MsgBox(Msg, vbYesNoCancel + vbQuestion, M09.Get_Language_Str('Fehler bei der Überprüfung des angeschlossenen Arduinos'))
            if (select_variable_ == vbYes):
                Retry = True
                #P01.Cells(M02.SH_VARS_ROW, ComPortColumn).Value = - P01.val(P01.Cells(M02.SH_VARS_ROW, ComPortColumn).Value)
                P01.Cells(M02.SH_VARS_ROW, ComPortColumn).Value = F00.port_set_busy(str(P01.Cells(M02.SH_VARS_ROW, ComPortColumn).Value))
            elif (select_variable_ == vbCancel):
                return fn_return_value, BuildOptions, DeviceSignature
            elif (select_variable_ == vbNo):
                BaudRate = Start_Baudrate
        else:
            if AutoDetect:
                LeftArduino = ( ComPortColumn == M25.COMPort_COL )
                if InStr(CheckCOMPort_Txt, 'Silicon Labs CP210x') > 0:
                    NewBrd = M02.BOARD_ESP32
                else:
                    #If 1 Or BaudRate <> Start_Baudrate Or DeviceSignature = 2004561 Then ' Change the board type to speed up the check the next time ' 28.10.20: Jürgen: Added "Or DeviceSignature..."
                    if DeviceSignature == 2004561:
                        NewBrd = M02.BOARD_NANO_EVERY
                    else:
                        if BaudRate == 57600:
                            NewBrd = M02.BOARD_NANO_OLD
                        else:
                            NewBrd = Get_New_Board_Type(FirmwareVer)
                M28.Change_Board_Typ(LeftArduino, NewBrd)
                BuildOptions = P01.Cells(M02.SH_VARS_ROW, BuildOptColumn)
                # remove leading "'"
                if len(BuildOptions)>0 and BuildOptions[0]=="'":
                    BuildOptions = BuildOptions[1:]                
                BuildOptions = Trim(Replace(BuildOptions, M02.AUTODETECT_STR, ''))
        if not (Retry):
            break
    fn_return_value = True
    return fn_return_value, BuildOptions, DeviceSignature

def Update_Compile_Time(Start=False):
    #---------------------------------------------------------
    global Start_Compile_Time
    # Is called by OnTime
    if Start_Compile_Time != 0 or Start:
        if Start:
            Start_Compile_Time = int(time.time())
        else:
            F00.StatusMsg_UserForm.Set_ActSheet_Label(P01.Format(int(time.time()) - Start_Compile_Time, 'hh:mm:ss'))
        P01.Application.OnTime(1000, Update_Compile_Time)


def Stop_Compile_Time_Display():
    #--------------------------------------
    global Start_Compile_Time
    Start_Compile_Time = 0
    P01.Unload(F00.StatusMsg_UserForm)

def Compile_and_Upload_Prog_to_Arduino(InoName, ComPortColumn, BuildOptColumn, SrcDir,CreateFilesOnly=False): # 20.12.21: Jürgen add CreateFilesOnly for programatically generation of header files
    ComPort = String()

    BuildOptions = String()

    CommandStr = String()

    ResFile = String()

    Mode = String()

    DeviceSignature = int()

    CPUType = String()

    #*HL hwnd = LongPtr()

    #*HL ArduName = String()

    #*HL TextColor = int()

    #*HL Res = ShellAndWaitResult()

    Start = Variant()
    fn_return_value=False
    #------------------------------------------------------------------------------------------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    #*HL hwnd = Application.hwnd
    ## VB2PY (CheckDirective) VB directive took path 1 on OLD_LIB_CHECK
    Check_Required_Libs_and_Install_missing()
    if ComPortColumn == M25.COMPort_COL:
        ArduName = 'LED'
    else:
        ArduName =  M25.Page_ID
        
    #P01.Unload(UserForm_Options) # already done
    F00.StatusMsg_UserForm.ShowDialog(Replace(M09.Get_Language_Str('Programmiere #1# Arduino'), "#1#", ArduName) + vbCr + M30.FileNameExt(InoName), '...')
    
    
    Fn_result, BuildOptions, DeviceSignature = Check_If_Arduino_could_be_programmed_and_set_Board_type(ComPortColumn, BuildOptColumn, BuildOptions, DeviceSignature,CreateFilesOnly=CreateFilesOnly)
    if Fn_result == False:
        Stop_Compile_Time_Display()
        return fn_return_value
    #ComPort = 'COM' + P01.Cells(M02.SH_VARS_ROW, ComPortColumn)
    ComPort = P01.Cells(M02.SH_VARS_ROW, ComPortColumn)
    ComPort = F00.port_check_format(ComPort)
    Update_Compile_Time(True)
    
    # 21.01.2021 Optionally get IP Address from cell left to com port
    if M02a.Get_BoardTyp() == "ESP32" and P01.Cells(M02.SH_VARS_ROW, ComPortColumn + 1) != "":
        ComPort = P01.Cells(M02.SH_VARS_ROW, ComPortColumn + 1)
        ComPort = F00.port_check_format(ComPort)
    
    ResFile = 'Start_Arduino_Result.txt'
    if ComPortColumn == M25.COMPort_COL:
        if M25.Page_ID == 'CAN':
            Mode = 'CAN'
        else:
            Mode = 'Left'
    else:
        Mode = 'Right'
    TextColor = vbWhite
    if M02a.Get_BoardTyp() == 'ESP32' or M02a.Get_BoardTyp() == 'PICO':
        if Mode == 'Right':
            P01.MsgBox(M09.Get_Language_Str('Wenn der ESP32 verwendet wird, dann wird kein rechter Arduino benötigt'), vbInformation, M09.Get_Language_Str('Rechter Arduino nicht benötigt'))
            return fn_return_value
        else:
            Mode = M02a.Get_BoardTyp()
            if Mode=="Pico" and M25.Page_ID == 'Selectrix':
                P01.MsgBox(Replace('Error: The #1# support for \'' + M25.Page_ID + '\' is not finished yet',"#1#",Mode), vbInformation, Replace("#1# support not finished","#1#",Mode))
                return fn_return_value
        TextColor = vbYellow
    if DeviceSignature == 2004561:
        CPUType = 'atmega4809'
    else:
        CPUType = 'atmega328p'
        
    useARDUINO_IDE = True
    system_platform = platform.platform()
    if not "Windows" in system_platform:
        useARDUINO_IDE=True
    else:
        useARDUINO_IDE=False
    if not useARDUINO_IDE: 
        CommandStr = '"' + Create_Cmd_file(ResFile, ComPort, BuildOptions, InoName, Mode, SrcDir, CPUType) + '"'
    else:
        CommandStr = Create_ARDUINO_IDE_Cmd(ResFile, ComPort, BuildOptions, InoName, Mode, SrcDir, CPUType)
        
    # Disable "serial.SerialDiscovery" trial 2                                ' 16.03.20:
    # Problem: Change the background color to Red is not working
    #CommandStr = CommandStr & " 2>&1 | find /v "" StatusLogger "" | find /v ""serial.SerialDiscovery"" | find /v ""fungsvorgang...
    
    
    #if CommandStr == '' or CommandStr == '""':
    #    #U01.Unload(StatusMsg_UserForm)
    #    M30.EndProg()
    
    if CreateFilesOnly:
        Stop_Compile_Time_Display()
        fn_return_value = True
        return fn_return_value
    
    Start = P01.Time()
    if Dir(SrcDir + InoName) == '':
        P01.Unload(F00.StatusMsg_UserForm)
        P01.MsgBox(M09.Get_Language_Str('Fehler das Programm ') + InoName + M09.Get_Language_Str(' ist nicht vorhanden in: ') + vbCr + '  \'' + SrcDir + '\'', vbCritical, M09.Get_Language_Str('Fehler Ino-Programm nicht vorhanden'))
        M30.EndProg()
    #*HL Failed = Not UpdateSimulatorIfNeeded(False, Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0) = 2 Or Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0) = 3)
    
    Failed = not M39.UpdateSimulatorIfNeeded(False, (M28.Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0) in (2,3)))
     
    if not Failed:
    
        P01.ChDrive(SrcDir)
        ChDir(SrcDir)
        if Use_Excel_Console():
            # 27.11.20 Juergen: use modal ShellExecute user form
            #*HL needs to be reworked
            pass
            Stop_Compile_Time_Display()
            F00.notimplemented("Excel Console")
            #Res = UserForm_RunProgram.ShellExecute(CommandStr, 0, Replace(Get_Language_Str('Programmiere #1# Arduino'), "#1#", ArduName) + ' - ' + FileNameExt(InoName), PromptUser, 0x800000, TextColor, Get_Language_Str('Senden zum Arduino abbrechen?'))
        else:
            PG.global_controller.disconnect()
            #Res = M40.ShellAndWait(CommandStr, 0, vbNormalFocus, PromptUser)
            PG.dialog_parent.start_ARDUINO_program_cmd(CommandStr)
            Res = M40.Success
            #Stop_Compile_Time_Display()
        # Bring Excel to the top                                                ' 19.05.20:
        # Is not working if an other application has be moved above Excel with Alt+Tab
        # But this is a feature of Windows.
        #   See: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow
        # But it brings up excel again after the upload to the Arduino
        # Without this funchion an other program was activated after the upload for some reasons
        #Bring_to_front(hwnd)
        #if (Res == M40.Success) or (Res == M40.Timeout) or (Res == M40.UserBreak):
        #    pass
        #else:
        #    P01.Unload(F00.StatusMsg_UserForm)
        #    P01.MsgBox(M09.Get_Language_Str('Fehler ') + Res + M09.Get_Language_Str(' beim Starten des Arduino Programms \'') + CommandStr + '\'', vbCritical, M09.Get_Language_Str('Fehler beim Starten des Arduino programms'))
        
        if Dir(ResFile) != '':
            arduinoMonitorPage=PG.global_controller.getFramebyName ("ARDUINOMonitorPage")
            arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")
            Failed = True
    
    if Failed:
        P01.MsgBox(M09.Get_Language_Str('Es ist ein Fehler aufgetreten ;-(' + vbCr + vbCr + 'Zur Fehlersuche kann man die letzten Änderungen wieder rückgängig machen und es noch mal versuchen. ' + vbCr + vbCr + 'Kommunikationsprobleme erkennt man an dieser Meldung: ' + vbCr + '   avrdude: ser_open(): can\'t open device "\\\\.\\COM') + P01.Cells(M02.SH_VARS_ROW, ComPortColumn) + '":' + vbCr + M09.Get_Language_Str('   Das System kann die angegebene Datei nicht finden.' + vbCr + 'In diesem Fall müssen die Verbindungen überprüft und der Arduino durch einen neuen ersetzt werden.' + vbCr + vbCr + 'Der Fehler kann auch auftreten wenn der DCC/Selextrix Arduino noch nicht programmiert wurde.' + vbCr + 'Am besten man steckt den rechten Arduino erst dann ein wenn er benötigt wird.' + vbCr + vbCr + 'Wenn der Fehler nicht zu finden ist und immer wieder auftritt, dann kann ein Screenshot des ' + 'vorangegangenen Bildschirms (Nach oben scrollen so dass die erste Meldung nach dem Arduino Bild zu sehen ist) ' + 'zusammen mit dem Excel Programm und einer ausführlichen Beschreibung an ' + vbCr + '  MobaLedLib@gmx.de' + vbCr + 'geschickt werden.'), vbInformation, M09.Get_Language_Str('Fehler beim Hochladen des Programms'))
        M30.EndProg()
    #else:
    #    Stop_Compile_Time_Display()
    #    Debug.Print('Compile and upload duration: ' + P01.Format(P01.Time() - Start, 'hh:mm:ss'))
    #    M30.Show_Status_for_a_while(M09.Get_Language_Str('Programm erfolgreich hochgeladen. Kompilieren und Hochladen dauerte ') + P01.Format(P01.Time() - Start, 'hh:mm:ss'), '00:02:00')
       
    fn_return_value = True
    return fn_return_value

def Compile_and_Upload_LED_Prog_to_Arduino(CreateFilesOnly=False):
    #------------------------------------------------------------------
    fn_return_value = False
    Doit = Boolean()
    #------------------------------------------------------------------
    Doit = CreateFilesOnly
    if CreateFilesOnly == False:
        Doit = Upload_the_Right_Arduino_Prog_if_needed()
    if Doit:
        fn_return_value = Compile_and_Upload_Prog_to_Arduino(M02.InoName_LED, M25.COMPort_COL, M25.BUILDOP_COL, GetWorkbookPath() + '/' + M02.Ino_Dir_LED, CreateFilesOnly=CreateFilesOnly)
    return fn_return_value


def Create_Config_Header_File(Name):
    fp = Integer()
    #--------------------------------------------------------------------
    fp = FreeFile()
    fn_return_value=False
    try:
        
        # VB2PY (UntranslatedCode) On Error GoTo WriteError
        VBFiles.openFile(fp, Name, 'w') 
        VBFiles.writeText(fp, '// This file was generated by \'' + PG.ThisWorkbook.Name + '\'  ' + Time, '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '// Eanble / disable the SPI mode according to the config sheet in Excel', '\n')
        if M28.Get_Bool_Config_Var('USE_SPI_Communication'):
            VBFiles.writeText(fp, '#define USE_SPI_SLAVE 1', '\n')
        else:
            VBFiles.writeText(fp, '#define USE_SPI_SLAVE 0', '\n')
        WriteGenButtonReleaseDefine(( fp ))
        # 09.04.23: GEN BUTTON RELEASE HANDLING
    
        VBFiles.closeFile(fp)
        # VB2PY (UntranslatedCode) On Error GoTo 0
        fn_return_value = True
        return fn_return_value
    except BaseException as e:
        logging.debug("Create_Config_Header_File - exception")
        logging.debug(e)
        P01.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Header Datei'))
        fn_return_value = False
        return fn_return_value
    
def WriteGenButtonReleaseDefine(fp):
    GenOption = Integer()
    # 09.04.23: GEN BUTTON RELEASE HANDLING
    #--------------------------------------------------------------------
    GenOption = M28.Get_Num_Config_Var('GEN_BUTTON_RELEASE_COM')
    if GenOption < 2 or GenOption > 3:
        # legacy behavior, off or invalid value
        VBFiles.writeText(fp, '#define GEN_BUTTON_RELEASE_COM GEN_OFF', '\n')
    else:
        VBFiles.writeText(fp, '#define GEN_BUTTON_RELEASE_COM ' + GenOption - 1, '\n')

def Compile_and_Upload_Prog_to_Right_Arduino():
    InoName = String()

    SrcDir = String()
    fn_return_value=False
    #--------------------------------------------------------------------
    M25.Make_sure_that_Col_Variables_match()
    if (M25.Page_ID == 'DCC'):
        InoName = M02.InoName_DCC
    elif (M25.Page_ID == 'Selectrix'):
        InoName = M02.InoName__SX
    elif (M25.Page_ID == 'CAN'):
        P01.MsgBox(M09.Get_Language_Str('Für die Steuerung per CAN Bus wird kein zweiter Arduino benötigt.' + vbCr + vbCr + 'Anstelle des rechen Arduinos muss ein CAN Modul (MCP2515) eingesteckt werden'), vbInformation, M09.Get_Language_Str('Kein Programm für rechten Arduino benötigt'))
        return fn_return_value
    else:
        P01.MsgBox('Interner Fehler: Undefined M25.Page_ID \'' + M25.Page_ID + '\' in Compile_and_Upload_Prog_to_Right_Arduino', vbCritical, 'Interner Fehler')
        Debug.Print('Compile_and_Upload_Prog_to_Right_Arduino: Interner Fehler: Undefined M25.Page_ID: ' + M25.Page_ID)
        M30.EndProg()
    SrcDir = GetWorkbookPath() + '/../examples/' + M30.FileName(InoName) + '/'
    if Dir(SrcDir + InoName) != '':
        Debug.Print('Programm aus lokalem Verzeichnis wird zum Upload verwendet: ' + SrcDir)
        P01.Application.StatusBar = 'Programm aus lokalem Verzeichnis wird zum Upload verwendet: ' + SrcDir
    else:
        SrcDir = M02a.Get_SrcDirExamp() + M30.FileName(InoName) + '/'
    #*HL if M07.ComPortPage().Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value > 0:
    if F00.port_is_available(M07.ComPortPage().Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value):
        #M07.ComPortPage().Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value = - P01.val(M07.ComPortPage().Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value)
        M07.ComPortPage().Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value = F00.port_set_busy(M07.ComPortPage().Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value)
        # Force to show the new COM Port dialog
    if Create_Config_Header_File(SrcDir + Replace(InoName, '.ino', '.h')) == False:
        return fn_return_value
        # 14.05.20:
    if Compile_and_Upload_Prog_to_Arduino(InoName, M25.COMPrtR_COL, M25.BUILDOpRCOL, SrcDir):
        P01.CellDict[M02.SH_VARS_ROW, M25.R_UPLOD_COL] = 'R OK'
        fn_return_value = True
    return fn_return_value

def Ask_To_Upload_the_Right_Arduino_Prog(Focus_Button):
    Other_Prog = String()

    ComPortUnused = int()
    
    #--------------------------------------------------------------------------------------
    # If the cell COMPrtR_COL is "COM?" the user is asked if the program for the
    # right arduino is already uploaded.
    fn_return_value = False
    if not M30.Get_Current_Platform_Bool('NeedLedArduino'):
        fn_return_value = False
        return fn_return_value
    Other_Prog = Replace(Trim(Replace(M02.Prog_for_Right_Ardu, M25.Page_ID + ' ', '')), ' ', ', ')
    select_variable_ = F00.Select_COM_Port_UserForm.ShowDialog(M09.Get_Language_Str('Ist das Programm für den rechten Arduino installiert?'), M09.Get_Language_Str('Programm für ') + M25.Page_ID + ' Arduino', Replace(Replace(M09.Get_Language_Str('Wurde das Programm des rechten #DCC# Arduinos bereits ' + 'installiert?' + vbCr + vbCr + 'Das Programm muss nur beim ersten mal auf den Arduino hochgeladen werden. ' + 'Danach muss es nicht mehr verändert werden solange es keine neue Version der ' + 'MobaLedLib gibt (oder auf #SELECTRIX# umgestellt wird).' + vbCr + vbCr + 'Ja: Diese Frage wird nicht mehr gestellt.' + vbCr + 'Installieren: Das Programm wird installiert.'), '#DCC#', M25.Page_ID), '#SELECTRIX#', Other_Prog), 'DCC_Image', 'I Installieren; A Abbrechen; J Ja', Focus_Button, False, Replace(M09.Get_Language_Str('#DCC# Programm für aktuelle MobaLedLib Version installiert?'), '#DCC#', M25.Page_ID), ComPortUnused)
    if (select_variable_[0] == 1):
        fn_return_value = True
    elif (select_variable_[0] == 2):
        M30.EndProg()
    elif (select_variable_[0] == 3):
        fn_return_value = False
    return fn_return_value

def Display_Connect_to_Left_Arduino():
    #------------------------------------------------------------
    M25.Make_sure_that_Col_Variables_match()
    fn_return_value=False
    if 3 == F00.Select_COM_Port_UserForm.ShowDialog(M09.Get_Language_Str('Linken Arduino anschließen'), M09.Get_Language_Str('Linken (LED) Arduino anstecken'), M09.Get_Language_Str('Das Programm wurde erfolgreich auf den rechten Arduino geladen.' + vbCr + vbCr + 'Dieser Vorgang muss nur ein mal durchgeführt werden. In Zukunft ' + 'wird nur noch das Programm des linken (LED) Arduinos verändert.' + vbCr + vbCr + 'Das USB Kabel muss jetzt an den linken Arduino angeschlossen werden.' + vbCr + vbCr + 'Wenn das geschehen ist die "OK" Taste betätigen'), 'LED_Image', M09.Get_Language_Str('; A Abbrechen; O OK'), 'Default_Button', False, M09.Get_Language_Str('Umstecken zum Linken Arduino'), 0):
        fn_return_value = True
    return fn_return_value

def Upload_the_Right_Arduino_Prog_if_needed():
    #--------------------------------------------------------------------
    # Uploade the program to the right arduino if
    # it's not the CAN page
    # and not uploadeded before (R_OK)
    # and the the sheet uses the right arduino (DCC Adresses/ SX Channels entered)
    M25.Make_sure_that_Col_Variables_match()
    fn_return_value=False
    if M25.Page_ID != 'CAN' and P01.Cells(M02.SH_VARS_ROW, M25.R_UPLOD_COL) != 'R OK' and M06.Ext_AddrTxt_Used():
        if Ask_To_Upload_the_Right_Arduino_Prog('Default_Button'):
            if F00.port_is_available(P01.Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value): # > 0:
                P01.CellDict[M02.SH_VARS_ROW, M25.COMPrtR_COL] = F00.port_set_busy(P01.Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value)
                #*HL P01.Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value = - P01.val(P01.Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL).Value)
                # Force to show the COM port dialog for the right Arduino
            if Compile_and_Upload_Prog_to_Right_Arduino() == False:
                return fn_return_value
            if Display_Connect_to_Left_Arduino() == False:
                return fn_return_value
            #if P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL).Value > 0:
            #    P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL).Value = - P01.val(P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL).Value)
            #    # Force to show the COM port dialog for the left Arduino
            if F00.port_is_available(P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL).Value):
                P01.CellDict[M02.SH_VARS_ROW, M25.COMPort_COL] = F00.port_set_busy(P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL).Value)
                # Force to show the COM port dialog for the left Arduino            
        else:
            P01.CellDict[M02.SH_VARS_ROW, M25.R_UPLOD_COL] = 'R OK'
    fn_return_value = True
    return fn_return_value

def Ask_to_Upload_and_Compile_and_Upload_Prog_to_Right_Arduino():
    #----------------------------------------------------------------------
    M25.Make_sure_that_Col_Variables_match()
    if Ask_To_Upload_the_Right_Arduino_Prog('Check_Button'):
        Compile_and_Upload_Prog_to_Right_Arduino()

def Create_InstalLib_Cmd_file(LibNames=""):
    ResultName = String()

    CommandStr = String()

    fp = Integer()

    Name = String()
    #--------------------------------------------------------------------------------
    # Arduino start Parameters see:
    #   https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc
    # Extract:
    #  --install-library library name[:version]
    #       Fetches available libraries list and install the specified one. If version is omitted, the latest is installed.
    #       If a library with the same version is already installed, nothing is installed and program exits with exit code 1.
    #       If a library with a different version is already installed, it’s replaced. Multiple libraries can be specified, separated by a comma.
    # Ein mal habe ich beobachtet, dass die MobaLedLin in ein anderes Verzeichnis installiert wurde
    # Evtl. lag das daran, das der Library manager offen war
    # Das problem tritt nicht auf wenn nur die Arduino IDE offen
    ResultName = 'Start_Arduino_Result.txt'
    if Dir(ResultName) != '':
        Kill(ResultName)
    if LibNames == '':
        LibNames = M28.Get_String_Config_Var('AddLibNames')
    CommandStr = '"' + Find_ArduinoExe() + '" --install-library "' + LibNames + '"'
    fp = FreeFile()
    Name = PG.ThisWorkbook.Path + '\\Start_Arduino.cmd'
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'COLOR 5F', '\n')
    VBFiles.writeText(fp, 'REM This file was generated by \'' + PG.ThisWorkbook.Name + '\'  ' + Time, '\n')
    VBFiles.writeText(fp, 'ECHO --------------------------------------------------------------------------', '\n')
    VBFiles.writeText(fp, 'ECHO ' + M09.Get_Language_Str('Aktualisiere die Bibliotheken ') + LibNames + ' ...', '\n')
    VBFiles.writeText(fp, 'ECHO --------------------------------------------------------------------------', '\n')
    VBFiles.writeText(fp, 'ECHO.', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, CommandStr, '\n')
    VBFiles.writeText(fp, 'ECHO.', '\n')
    VBFiles.writeText(fp, '', '\n')
    #Print #fp, "Pause"
    VBFiles.writeText(fp, 'IF ERRORLEVEL 1 (', '\n')
    VBFiles.writeText(fp, '   COLOR 4F', '\n')
    VBFiles.writeText(fp, '   ECHO Start_Arduino_Result: %ERRORLEVEL% > "' + ResultName + '"', '\n')
    VBFiles.writeText(fp, '   ECHO   ********************************************', '\n')
    VBFiles.writeText(fp, '   ECHO     ' + M09.Get_Language_Str('Da ist was schief gegangen ;-(') + '             ERRORLEVEL %ERRORLEVEL%', '\n')
    VBFiles.writeText(fp, '   ECHO   ********************************************', '\n')
    VBFiles.writeText(fp, '   Pause', '\n')
    VBFiles.writeText(fp, '   )', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = Name
    return fn_return_value
    P01.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Start Datei'))
    return fn_return_value

def Install_Libraries(LibNames=[]):
    CommandStr = String()

    Res = False # ShellAndWaitResult()

    Start = Variant()

    SrcDir = String()

    ResFile = 'Start_Arduino_Result.txt'
    #---------------------------------------------------------
    CommandStr = Create_InstalLib_Cmd_file(LibNames)
    Start = Time
    Res = M40.ShellAndWait(CommandStr, 0, vbNormalFocus, M40.PromptUser)
    if (Res == M40.Success) or (Res == M40.Timeout):
        pass
    else:
        P01.MsgBox(M09.Get_Language_Str('Fehler ') + Res + M09.Get_Language_Str(' beim starten des Arduino Programms \'') + CommandStr + '\'', vbCritical, M09.Get_Language_Str('Fehler beim Starten des Arduino programms'))
    SrcDir = PG.ThisWorkbook.Path + '/'
    P01.ChDrive(SrcDir)
    ChDir(SrcDir)
    if Dir(ResFile) != '':
        P01.MsgBox(M09.Get_Language_Str('Es ist ein Fehler aufgetreten ;-(' + vbCr + vbCr + 'Wenn der Fehler immer wieder auftritt, dann kann ein Screenshot des ' + 'vorangegangenen Bildschirms und einer ausführlichen Beschreibung an ' + vbCr + '  MobaLedLib@gmx.de' + vbCr + 'geschickt werden.'), vbInformation, M09.Get_Language_Str('Fehler beim Installieren der Bibliotheken'))
        M30.EndProg()
    else:
        Debug.Print('Compile and upload duration: ' + P01.Format(Time - Start, 'hh:mm:ss'))
        M30.Show_Status_for_a_while(M09.Get_Language_Str('Bibliotheken erfolgreich installiert. (Dauer: ') + P01.Format(Time - Start, 'hh:mm:ss') + ')', '00:00:30')

def Check_Required_Libs():
    Debug.Print(Check_Required_Libs)
    return "" #*HL
    LibPath = '\\Arduino\\libraries\\MobaLedLib\\examples\\00.Overview'

    LibDir = String()

    Name = Variant()

    LibNames = String()
    #-----------------------------------------------
    # Return a list of missing libraries
    #
    # ToDo: Check the required version of existing libraries
    LibDir = Replace(Environ('APPDATA'), 'AppData\\Roaming', '') + 'Documents\\Arduino\\libraries\\'
    # VB2PY (UntranslatedCode) On Error GoTo LibDirMissing
    if Dir(LibDir, vbDirectory) == '':
        # VB2PY (UntranslatedCode) GoTo LibDirMissing
        # 06.10.19: Added: vbDirectory to detect also directories without files
        pass
    # VB2PY (UntranslatedCode) On Error GoTo 0
    LibNames = M28.Get_String_Config_Var('AddLibNames')
    for Name in Split(LibNames, ','):
        if Dir(LibDir + Name + '\\', vbDirectory) == '':
            fn_return_value = Check_Required_Libs() + Name + ','
    fn_return_value = M30.DelLast(Check_Required_Libs())
    return fn_return_value
    P01.MsgBox(M09.Get_Language_Str('Fehler: Das Arduino Bibliotheksverzeichnis wurde nicht gefunden:') + vbCr + '  \'' + LibDir + '\'', vbCritical, M09.Get_Language_Str('Fehler Bibliotheksverzeichnis nicht vorhanden'))
    M30.EndProg()
    return fn_return_value

def Test_Check_Required_Libs():
    #UT-----------------------------------
    Debug.Print('Check_Required_Libs: ' + Check_Required_Libs())

def Check_Required_Libs_and_Install_missing():
    Debug.Print("Check_Required_Libs_and_Install_missing")
    MissingLibs = String()
    #---------------------------------------------------
    if M28.Get_Bool_Config_Var('Lib_Installed_other'):
        return
    MissingLibs = Check_Required_Libs()
    if MissingLibs == '':
        return
    select_variable_ = P01.MsgBox(M09.Get_Language_Str('Achtung: Die folgenden Bibliotheken wurden nicht im ' + 'Standardverzeichnis von Arduino gefunden:') + vbCr + '  ' + MissingLibs + vbCr + vbCr + M09.Get_Language_Str('Sollen die Bibliotheken jetzt installiert werden?' + vbCr + vbCr + 'Ja: Die Bibliotheken werden aus dem Internet installiert' + vbCr + vbCr + 'Nein: Es wird davon ausgegangen, dass die Bibliotheken in ' + vbCr + 'einem anderen Verzeichnis verfügbar sind (Für Experten):' + vbCr + 'Wenn beim kompilieren eine fehlende Datei gemeldet wird, dann liegt ' + 'das vermutlich an einer fehlenden oder veralteten Bibliothek. ' + 'In dem Fall muss das Programm neu gestartet werden und die Bibliotheken ' + 'installiert werden.'), vbYesNoCancel + vbQuestion, M09.Get_Language_Str('Fehlende Bibliotheken erkannt'))
    if (select_variable_ == vbYes):
        # one library exists in the same version. => Looks like an error.
        # This very is importand tor the MobaLedLib because otherwise the running Excel
        # sheed may be overwritten
        Install_Libraries(MissingLibs)
    elif (select_variable_ == vbNo):
        M28.Set_Bool_Config_Var('Lib_Installed_other', True)
    elif (select_variable_ == vbCancel):
        M30.EndProg()

# VB2PY (UntranslatedCode) Option Explicit

