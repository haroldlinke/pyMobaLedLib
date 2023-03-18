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

import time


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
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
import proggen.M12_Copy_Prog as M12
#import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M40_ShellandWait as M40
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Mulitplexer as M80

import proggen.F00_mainbuttons as F00

import ExcelAPI.XLW_Workbook as P01

import proggen.Prog_Generator as PG


from vb2py.vbfunctions import *
from vb2py.vbdebug import *


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

""" Bootloader Programmieren:
 - Jumper setzen unten die linken Pins verbinden
 - ArduinoISP aud DCC spielen
 - Bootloader schreiben
 - Fragen ob noch weitere Arduinos Programmiert werden sollen
 - Wenn Nein, dann wieder das DCC Prog. Installieren (Wichtig)
 - Jumper öffnen
----------------------------------------------------------------
------------------------------------------------------------------------------------
UT---------------------------------------------------------
---------------------------------------------
----------------------------------
"""


def __Install_ArduinoISP_to_Right_Arduino():
    fn_return_value = False
    InoName = String()

    SrcDir = String()

    DstDir = String()
    #----------------------------------------------------------------
    # Compile and upload the ArduinoISP program to the right Arduino
    M25.Make_sure_that_Col_Variables_match()
    InoName = 'ArduinoISP.ino'
    DstDir = PG.ThisWorkbook.Path + '/' + M30.FileName(InoName) + '/'
    SrcDir = M30.FilePath(M08.Find_ArduinoExe()) + 'examples/11.ArduinoISP/ArduinoISP/'
    M30.CreateFolder(DstDir)
    if not M12.FileCopy_with_Check(DstDir, InoName, SrcDir + InoName):
        return fn_return_value
    if M08.Compile_and_Upload_Prog_to_Arduino(InoName, M25.COMPrtR_COL, M25.BUILDOpRCOL, DstDir):
        P01.CellDict[M02.SH_VARS_ROW, M25.R_UPLOD_COL] = 'R ISP'
        fn_return_value = True
    return fn_return_value

def Create_WriteFastBootloader_cmd(SrcDir):
    fn_return_value = False
    Name = String()

    fp = Integer()
    #------------------------------------------------------------------------------------
    # "C:\Users\Hardi\AppData\Local\Arduino15\packages\arduino\tools\avrdude\6.3.0-arduino17/bin/avrdude" ^
    #    "-CC:\Users\Hardi\AppData\Local\Arduino15\packages\arduino\tools\avrdude\6.3.0-arduino17/etc/avrdude.conf"
    #    -v -patmega328p -cstk500v1 -PCOM3 -b19200 ^
    #    "-Uflash:w:C:\Program Files (x86)\Arduino\hardware\arduino\avr/bootloaders/optiboot/optiboot_atmega328.hex:i" ^
    #    -Ulock:w:0x0F:m
    Name = SrcDir + 'WriteFastBootloader.cmd'
    #If Dir(Name) <> "" Then                                                  ' 04.11.20: Always write the file
    #   Create_WriteFastBootloader_cmd = Name
    #   Exit Function
    #End If
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM Write the fast Bootloader to the left Arduino', '\n')
    VBFiles.writeText(fp, 'REM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', '\n')
    VBFiles.writeText(fp, 'REM Parameter:               Example', '\n')
    VBFiles.writeText(fp, 'REM  1: Arduino EXE Path:    "C:\\Program Files (x86)\\Arduino\\"', '\n')
    VBFiles.writeText(fp, 'REM  2: Port:                -PCOM3', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM The program uses the captured and adapted command line from the Arduino IDE', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'Rem Using the private OptiBoot version 108.1 to indicate that the HFUSE is set to DE', '\n')
    VBFiles.writeText(fp, 'Rem This bootloader is equal to version 8.1', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM This file was automatically generated by the program ' + PG.ThisWorkbook.Name + ' ' + M02.Prog_Version + '      by Hardi', '\n')
    VBFiles.writeText(fp, 'REM File creation: ' + P01.Date() + ' ' + P01.Time_str(), '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'SET ArduinoExePath=%~1', '\n')
    VBFiles.writeText(fp, 'SET Port=%2', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '"%ArduinoExePath%\\hardware\\tools\\avr/bin/avrdude" ^', '\n')
    VBFiles.writeText(fp, '   "-C%ArduinoExePath%hardware\\tools\\avr\\etc\\avrdude.conf" ^', '\n')
    VBFiles.writeText(fp, '   -v -patmega328p -cstk500v1 %Port%  -b19200 ^', '\n')
    #Print #fp, "   ""-Uflash:w:%ArduinoExePath%hardware\arduino\avr/bootloaders/optiboot/optiboot_atmega328.hex:i"" ^" ' Standard Optiboot bootloader
    #Print #fp, "   ""-Uflash:w:" & GetShortPath(SrcDir & "optiboot_atmega328_Ver108.1.hex") & ":i"" ^"                       ' 02.11.20:
    VBFiles.writeText(fp, '   "-Uflash:w:' + M08.GetShortPath(M02a.Get_SrcDirInLib() + 'ArduinoISP\\optiboot_atmega328_Ver108.1.hex') + ':i" ^', '\n')
    VBFiles.writeText(fp, '   -Ulock:w:0x0F:m ^', '\n')
    VBFiles.writeText(fp, '   -Uhfuse:w:0xDE:m', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'if %errorlevel%==1 (', '\n')
    VBFiles.writeText(fp, '   COLOR 4F', '\n')
    VBFiles.writeText(fp, '   ECHO *********************************', '\n')
    VBFiles.writeText(fp, '   ECHO Error writing the boot loader ;-(', '\n')
    VBFiles.writeText(fp, '   ECHO *********************************', '\n')
    VBFiles.writeText(fp, '   PAUSE', '\n')
    VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = Name
    return fn_return_value
    P01.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Compile und Flash Datei'))
    return fn_return_value

def __Test_Create_WriteFastBootloader_cmd():
    #UT---------------------------------------------------------
    Debug.Print(Create_WriteFastBootloader_cmd(PG.ThisWorkbook.Path + '\\ArduinoISP\\'))

def __Write_Bootloader():
    fn_return_value = None
    #hwnd = LongPtr()

    #CmdName = String()

    #CommandStr = String()

    #Res = ShellAndWaitResult()
    #---------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    #*HL hwnd = Application.hwnd
    CmdName = Create_WriteFastBootloader_cmd(PG.ThisWorkbook.Path + '\\ArduinoISP\\')
    if CmdName == '':
        return fn_return_value
    CommandStr = '"' + CmdName + '" "' + M30.FilePath(M08.Find_ArduinoExe()) + '"' + ' -PCOM' + P01.Cells(M02.SH_VARS_ROW, M25.COMPrtR_COL)
    Res = M40.ShellAndWait(CommandStr, 0, vbNormalFocus, M40.PromptUser)
    if (Res == M40.Success) or (Res == M40.Timeout):
        pass
    else:
        P01.Unload(F00.StatusMsg_UserForm)
        P01.MsgBox(M09.Get_Language_Str('Fehler ') + Res + M09.Get_Language_Str(' beim Starten des Arduino Programms \'') + CommandStr + '\'', vbCritical,M09.Get_Language_Str('Fehler beim Starten des Arduino programms'))
    #*HL Bring_to_front(hwnd)
    fn_return_value = True
    return fn_return_value

def __Old_Prog():
    M08.Compile_and_Upload_Prog_to_Right_Arduino()

def Install_FastBootloader():
    Res = Boolean()
    #----------------------------------
    M25.Make_sure_that_Col_Variables_match()
    if M25.Page_ID != 'DCC' and M25.Page_ID != 'Selectrix':
        P01.MsgBox(M09.Get_Language_Str('Die schnelle Bootloader kann nur von einer DCC oder Selectrix Seite aus installiert werden.'), vbInformation, M09.Get_Language_Str('Falsche Seite zum aktualisieren des Bootloaders ausgewählt'))
        return
    P01.MsgBox(M09.Get_Language_Str('FastBootloader not implemented yet.'), vbInformation, M09.Get_Language_Str('Not implemented'))
    return

    Res = BootJumper_Form.ShowDialog
    time.sleep(1000)
    if Res:
        if not __Install_ArduinoISP_to_Right_Arduino():
            return
        while 1:
            __Write_Bootloader()()
            if not (P01.MsgBox(M09.Get_Language_Str('Installation des Bootloaders abgeschlossen' + vbCr + vbCr + 'Soll der Bootloader auf einen weiteren Arduino geladen werden?' + vbCr + vbCr + 'Wenn ja, dann muss dieser jetzt in den linken Steckplatz gesteckt werden.' + vbCr + 'Mit \'Nein\' wird wieder das DCC/Selectrix Programm auf den rechten Nano installiert.' + vbCr + vbCr + 'Achtung der rechte Arduino darf nicht entfernt werden!'), vbYesNo + vbDefaultButton2, M09.Get_Language_Str('Noch einen Arduino aktualisieren?')) == vbYes):
                break
        M08.Compile_and_Upload_Prog_to_Right_Arduino()
        P01.MsgBox(M09.Get_Language_Str('Achtung: Die Jumper müssen unbedingt wieder entfernt werden sonst geht nichts mehr ;-(' + vbCr + 'Damit sie nicht verloren gehen können sie so eingesteckt werden, dass sie nur auf einem Pin stecken.' + vbCr + vbCr + 'Das USB Kabel sollte wieder auf den linken Arduino gesteckt werden.'), vbInformation, M09.Get_Language_Str('Bootloader Programmierung abgeschlossen'))

# VB2PY (UntranslatedCode) Option Explicit
