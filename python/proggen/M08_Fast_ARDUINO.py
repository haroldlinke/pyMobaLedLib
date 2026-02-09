# -*- coding: utf-8 -*-
#
#         M08 Fast_ARDUINO
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
# 2022-01-07 v4.02 HL: - Else:, ByRef check done, first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *


# fromx proggen.M02_Public import *
# fromx proggen.M06_Write_Header_LED2Var import *
# fromx proggen.M06_Write_Header_Sound import *
# fromx proggen.M06_Write_Header_SW import *
# fromx proggen.M09_Language import *
# fromx proggen.M09_Select_Macro import *
# fromx proggen.M20_PageEvents_a_Functions import *
# fromx proggen.M25_Columns import *
# fromx proggen.M28_Diverse import *
# fromx proggen.M30_Tools import *

# fromx proggen.M80_Create_Multiplexer import *


import proggen.M02_Public as M02
#import proggen.M02_Scripting as Scripting
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
import proggen.M06_Write_Header as M06
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
#import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M40_ShellandWait as M40
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Multiplexer as M80

import ExcelAPI.XLA_Application as P01

import mlpyproggen.Prog_Generator as PG


from vb2py.vbfunctions import *
from vb2py.vbdebug import *


def Packages_Dir_Available():
    fn_return_value = False
    Res = String()
    #--------------------------------------------------
    Res = Dir(Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu, vbDirectory)
    while Res != '' and LCase(Res) != 'packages':
        Res = Dir()
    if LCase(Res) != '':
        fn_return_value = True
    return fn_return_value

def Create_Packages_Dir_if_not_Available():
    #------------------------------------------------
    if not Packages_Dir_Available():
        M30.CreateFolder(Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + 'packages/')

def Create_Build(BoardName, fp):
    # 28.10.20: Jürgen (Old name: Create_PrivateBuild_cmd_if_missing)
    #-------------------------------------
    if BoardName == M02.HT_AM328:
        Create_Build_Arduino(( fp ))
        return
    if BoardName == M02.HT_PICO:
        # 17.04.21: Jürgen
        Create_Build_Pico(( fp ))
        return
    VBFiles.writeText(fp, 'pause Invalid BoardType' + BoardName, '\n')
    VBFiles.writeText(fp, 'exit /b 1', '\n')

def Create_Build_Arduino(fp):
    PackageDestDir = String()
    # 28.10.20: Jürgen (Old name: Create_PrivateBuild_cmd_if_missing)
    #-------------------------------------
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM Fast Build command from Juergen', '\n')
    VBFiles.writeText(fp, 'REM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM Compile and flash time 10 sec instead of 23 sec ! on Hardis laptop', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM Speed up by', '\n')
    VBFiles.writeText(fp, 'REM - not using the Arduino Core', '\n')
    VBFiles.writeText(fp, 'REM - not checking the flash at the end (saves 3 sec)', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM This file could be modified by the user to support special compiler switches', '\n')
    VBFiles.writeText(fp, 'REM It is called if the switch the "Schnells Build und Upload verwenden:" in the \'Config\' sheet is enabled', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM Parameter:               Example', '\n')
    VBFiles.writeText(fp, 'REM  1: Arduino EXE Path:    "C:\\Program Files (x86)\\Arduino\\"', '\n')
    VBFiles.writeText(fp, 'REM  2: Ino Name:            "LEDs_AutoProg.ino"', '\n')
    VBFiles.writeText(fp, 'REM  3: Com port:            "\\\\.\\COM3"', '\n')
    VBFiles.writeText(fp, 'REM  4: Build options:       "arduino:avr:nano:cpu=atmega328"', '\n')
    VBFiles.writeText(fp, 'REM  5: Baudrate:            "57600" or "115200"', '\n')
    VBFiles.writeText(fp, 'REM  6: Arduino Library path "%USERPROFILE%\\Documents\\Arduino\\libraries"', '\n')
    VBFiles.writeText(fp, 'REM  7: CPU type:            "atmega328p, atmega4809', '\n')
    # 28.10.20: Jürgen
    VBFiles.writeText(fp, 'REM  8: options:             "noflash|norebuild"', '\n')
    # 19.12.21: Jürgen: Added noflash option
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM The program uses the captured and adapted command line from the Arduino IDE', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'SET aHome=%~1', '\n')
    VBFiles.writeText(fp, 'SET fqbn=%~4', '\n')
    VBFiles.writeText(fp, 'SET lib=%~6', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'SET aTemp=%USERPROFILE%\\AppData\\Local\\Temp\\pyMobaLedLib_build\\ATMega', '\n')
    # 01.12.20: Added: "\ATMega" otherwise the esp32 fastbuild fails if the prog. is conpuled for the Nano
    VBFiles.writeText(fp, 'SET aCache=%USERPROFILE%\\AppData\\Local\\Temp\\MobaLedLib_cache\\ATMega', '\n')
    #    "            "
    VBFiles.writeText(fp, 'if not exist "%aTemp%"  md "%aTemp%"', '\n')
    VBFiles.writeText(fp, 'if not exist "%aCache%" md "%aCache%"', '\n')
    VBFiles.writeText(fp, '', '\n')
    # 28.01.24 Juergen delete compiler cache if last build failed
    VBFiles.writeText(fp, 'if exist "%aTemp%\\buildFailed.txt" (', '\n')
    VBFiles.writeText(fp, '   echo Last build failed ;-( - rebuild everything', '\n')
    VBFiles.writeText(fp, '   rd "%aTemp%" /s/q', '\n')
    VBFiles.writeText(fp, '   rd "%aCache%" /s/q', '\n')
    VBFiles.writeText(fp, '   md "%aTemp%"', '\n')
    VBFiles.writeText(fp, '   md "%aCache%"', '\n')
    VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, '', '\n')
    # Example: "C:\Users\Hardi\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.3"
    # 01.11.20:
    PackageDestDir = M08.GetShortPath(Environ(M02.Env_USERPROFILE)) + M02.AppLoc_Ardu + 'packages\\arduino\\hardware\\avr\\' + M37.Get_Std_Arduino_Lib_Ver()
    if M37.Get_User_std_Arduino_Lib_Ver() == '':
        # No own board package installed => Copy the standard board
        VBFiles.writeText(fp, 'robocopy "%aHome%\\hardware\\arduino\\avr" "' + PackageDestDir + '" /mir /s >nul', '\n')
    VBFiles.writeText(fp, 'xcopy ' + M08.GetShortPath(M08.GetWorkbookPath()) + '\\LEDs_AutoProg\\boards.local.txt "' + PackageDestDir + '\\" /d /y >nul', '\n')
    # 06.03.21 Juergen: overwrite file if needed, don't promt user, has blocked the build
    Create_Packages_Dir_if_not_Available()
    # Create the 'packages' folder otherwise we get an error in the following 'GetShortPath()' call   07.10.21:
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'REM *** Call the arduino builder ***', '\n')
    VBFiles.writeText(fp, '"%aHome%\\arduino-builder" -compile -logger=human ^', '\n')
    VBFiles.writeText(fp, '     -hardware "%aHome%\\hardware" ^', '\n')
    VBFiles.writeText(fp, '     -hardware "' + M08.GetShortPath(Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + 'packages') + '" ^', '\n')
    # 28.10.20: Jürgen
    VBFiles.writeText(fp, '     -tools "%aHome%\\tools-builder" ^', '\n')
    VBFiles.writeText(fp, '     -tools "%aHome%\\hardware\\tools\\avr" ^', '\n')
    VBFiles.writeText(fp, '     -built-in-libraries "%aHome%\\libraries" -libraries "%LIB%" ^', '\n')
    VBFiles.writeText(fp, '     -fqbn=%fqbn% -build-path "%aTemp%" ^', '\n')
    VBFiles.writeText(fp, '     -warnings=default ^', '\n')
    VBFiles.writeText(fp, '     -build-cache "%aCache%" ^', '\n')
    VBFiles.writeText(fp, '     -prefs=build.warn_data_percentage=75 ^', '\n')
    VBFiles.writeText(fp, '     -prefs=runtime.tools.avrdude.path="%aHome%\\hardware\\tools\\avr" ^', '\n')
    VBFiles.writeText(fp, '     -prefs=runtime.tools.avr-gcc.path="%aHome%\\hardware\\tools\\avr"  ^', '\n')
    VBFiles.writeText(fp, '     %2', '\n')
    # 28.01.24 Juergen: mark last build as failed
    VBFiles.writeText(fp, 'if errorlevel 1 (', '\n')
    VBFiles.writeText(fp, '    echo %date% > "%aTemp%\\buildFailed.txt"', '\n')
    VBFiles.writeText(fp, '    exit /b 1', '\n')
    VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'set subType=%7', '\n')
    # 08.12.23: Juergen 328PB support
    VBFiles.writeText(fp, 'set mainType=%subType:~0,9%', '\n')
    #           ---- " ---
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'if "%8"=="noflash" goto :EOF', '\n')  # 19.12.21: Jürgen: add noflash option
    #VBFiles.writeText(fp, 'if errorlevel 0 (', '\n')
    VBFiles.writeText(fp, '   REM *** Flash program ***', '\n')
    VBFiles.writeText(fp, '   REM -v = Verbose output. -v -v for more.', '\n')
    VBFiles.writeText(fp, '   REM -V = Do not verify.                      => Saves 3 sec', '\n')
    VBFiles.writeText(fp, '   REM -D = Disable auto erase for flash memory', '\n')
    VBFiles.writeText(fp, '   set extraArgs=', '\n')
    # 28.10.20: Jürgen: New Block
    VBFiles.writeText(fp, '   if "%7"=="atmega4809" (', '\n')
    VBFiles.writeText(fp, '      echo Forcing reset using 1200bps open/close on port %3', '\n')
    VBFiles.writeText(fp, '      mode %3 1200,n,8,1', '\n')
    VBFiles.writeText(fp, '      set extraArgs=-cjtag2updi -e -Ufuse2:w:0x01:m -Ufuse5:w:0xC9:m -Ufuse8:w:0x00:m', '\n')
    VBFiles.writeText(fp, '      goto flash', '\n')
    VBFiles.writeText(fp, '   )', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'if "%mainType%"=="atmega328" (', '\n')
    # 08.12.23: Juergen 328PB support
    VBFiles.writeText(fp, '   set extraArgs=-carduino', '\n')
    VBFiles.writeText(fp, '   goto flash', '\n')
    VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, ':flash', '\n')
    VBFiles.writeText(fp, '"%aHome%\\hardware\\tools\\avr/bin/avrdude" -C"%aHome%\\hardware\\tools\\avr/etc/avrdude.conf" ^', '\n')
    VBFiles.writeText(fp, '   -V -p%7 -P\\\\.\\%3 -b%~5 -D -Uflash:w:"%aTemp%/%~2.hex":i %extraArgs%', '\n')
    return

def Create_Build_Pico(fp):
    Board_Version = String()
    # 17.04.21: Jürgen
    #-------------------------------------
    Board_Version = M37.Get_Lib_Version('rp2040:rp2040')
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM Fast Build command from Juergen', '\n')
    VBFiles.writeText(fp, 'REM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM Speed up by', '\n')
    VBFiles.writeText(fp, 'REM - not using the Arduino Core', '\n')
    VBFiles.writeText(fp, 'REM - not checking the flash at the end (saves 3 sec)', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM This file could be modified by the user to support special compiler switches', '\n')
    VBFiles.writeText(fp, 'REM It is called if the switch the "Schnells Build und Upload verwenden:" in the \'Config\' sheet is enabled', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM Parameter:               Example', '\n')
    VBFiles.writeText(fp, 'REM  1: Arduino EXE Path:    "C:\\Program Files (x86)\\Arduino\\"', '\n')
    VBFiles.writeText(fp, 'REM  2: Ino Name:            "LEDs_AutoProg.ino"', '\n')
    VBFiles.writeText(fp, 'REM  3: Com port:            "\\\\.\\COM3"', '\n')
    VBFiles.writeText(fp, 'REM  4: Build options:       "rp2040:rp2040:rpipico:flash=2097152_0,freq=125,dbgport=Disabled,dbglvl=None"', '\n')
    VBFiles.writeText(fp, 'REM  5: Baudrate:            "115200"', '\n')
    VBFiles.writeText(fp, 'REM  6: Arduino Library path "%USERPROFILE%\\Documents\\Arduino\\libraries"', '\n')
    VBFiles.writeText(fp, 'REM  7: CPU type:            "rp2040', '\n')
    VBFiles.writeText(fp, 'REM  8: options:             "noflash"', '\n')   # 19.12.21: Jürgen: Added noflash option
    # 19.12.21: Jürgen: Added noflash option
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM The program uses the captured and adapted command line from the Arduino IDE', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'SET aHome=%~1', '\n')
    VBFiles.writeText(fp, 'SET fqbn=%~4', '\n')
    VBFiles.writeText(fp, 'SET lib=%~6', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'call :short aTemp "%USERPROFILE%\\AppData\\Local\\Temp\\pyMobaLedLib_build\\Pico"', '\n')
    VBFiles.writeText(fp, 'SET aCache=%aTemp%\\cache', '\n')
    VBFiles.writeText(fp, 'call :short packages "%USERPROFILE%' + M02.AppLoc_Ardu + 'packages"', '\n')
    VBFiles.writeText(fp, 'if not exist "%aTemp%"  md "%aTemp%"', '\n')
    VBFiles.writeText(fp, 'if not exist "%aCache%" md "%aCache%"', '\n')
    VBFiles.writeText(fp, '', '\n')
    Create_Packages_Dir_if_not_Available()
    # Create the 'packages' folder otherwise we get an error in the following 'GetShortPath()' call   20.10.21:
    VBFiles.writeText(fp, 'REM *** Call the arduino builder ***', '\n')
    VBFiles.writeText(fp, '"%aHome%\\arduino-builder" -compile -logger=human ^', '\n')
    VBFiles.writeText(fp, '     -hardware "%aHome%\\hardware" ^', '\n')
    VBFiles.writeText(fp, '     -hardware "' + M08.GetShortPath(Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + 'packages') + '" ^', '\n')
    # 28.10.20: Jürgen
    VBFiles.writeText(fp, '     -tools "%aHome%\\tools-builder" ^', '\n')
    VBFiles.writeText(fp, '     -tools "%aHome%\\hardware\\tools\\avr" ^', '\n')
    VBFiles.writeText(fp, '     -built-in-libraries "%aHome%\\libraries" -libraries "%LIB%" ^', '\n')
    VBFiles.writeText(fp, '     -fqbn=%fqbn% -build-path "%aTemp%" ^', '\n')
    VBFiles.writeText(fp, '     -warnings=default ^', '\n')
    VBFiles.writeText(fp, '     -build-cache "%aCache%" ^', '\n')
    VBFiles.writeText(fp, '     -prefs=build.warn_data_percentage=75 ^', '\n')
    VBFiles.writeText(fp, '     -prefs=runtime.platform.path="' + M08.GetShortPath(Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + "packages\\rp2040\\hardware\\rp2040\\" + Board_Version) + '" ^','\n') # 16.12.24: Juergen
    VBFiles.writeText(fp, '     %2', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'if "%8"=="noflash" goto :EOF', '\n')   # 19.12.21: Jürgen: add noflash option   
    # 19.12.21: Jürgen: add noflash option
    #VBFiles.writeText(fp, 'if errorlevel 0 (', '\n')
    VBFiles.writeText(fp, '   REM *** Flash program ***', '\n')
    VBFiles.writeText(fp, '   :flash', '\n')
    VBFiles.writeText(fp, '   "%packages%\\rp2040\\tools\\pqt-python3\\1.0.1-base-3a57aed-1\\python3" "%packages%\\rp2040\\hardware\\rp2040\\' + Board_Version + '\\tools\\uf2conv.py" ^', '\n')
    VBFiles.writeText(fp, '   --serial %3 --family RP2040 --deploy "%aTemp%\\LEDs_AutoProg.ino.uf2"', '\n')
    #VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, 'goto :eof', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, ':short', '\n')
    VBFiles.writeText(fp, 'set %1=%~s2', '\n')
    VBFiles.writeText(fp, 'goto :eof', '\n')
    VBFiles.writeText(fp, '', '\n')

def __Test_Create_PrivateBuild_cmd_if_missing():
    Name = String()

    fp = Integer()
    #UT--------------------------------------------------
    Name = M08.GetWorkbookPath() + '\\LEDs_AutoProg\\privateBuild.cmd'
    VBFiles.openFile(fp, Name, 'w') 
    Create_Build('arduino', fp)
    VBFiles.closeFile(fp)

# VB2PY (UntranslatedCode) Option Explicit