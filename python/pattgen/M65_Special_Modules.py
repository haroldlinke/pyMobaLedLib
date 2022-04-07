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

"""------------------------------------------------------------------------------------------------------------------------------
----------------------------------------
---------------------------------------------
-----------------------------------------------------------------------------------------------------------
UT-----------------------------------------
-------------------------------------------------------------------------------------------
UT-------------------------------------
---------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------
------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------
----------------------------------------------------------------
UT-----------------------------------
-----------------------------
----------------------------
-------------------------------------------------------------------------------------
----------------------
----------------------
"""


def __Find_File_in_UserDir_with_Version_Dir(UserDir, VersionDir, SearchName):
    fn_return_value = None
    SeachDir = String()

    VerDir = String()

    OtherDir = String()
    #------------------------------------------------------------------------------------------------------------------------------
    # Example:
    # Seach for %USERPROFILE%\AppData\Local\Arduino15\packages\arduino\tools\avrdude\6.3.0-arduino17/bin/avrdude.exe
    # Parameters:
    #   UserDir:    "\AppData\Local\Arduino15\packages\arduino\tools\avrdude\"
    #   VersionDir: "*-arduino*"
    #   SearchName: "\bin\avrdude.exe"
    SeachDir = Environ('USERPROFILE') + UserDir
    VerDir = Dir(SeachDir + VersionDir, vbDirectory)
    if VerDir == '':
        MsgBox(Replace(Get_Language_Str('Fehler: Das Verzeichnis \'#1#\' wurde nicht gefunden'), '#1#', SeachDir + VersionDir), vbCritical, Get_Language_Str('Verzeichnis nicht gefunden'))
        return fn_return_value
    #Debug.Print "VerDir:" & VerDir
    while 1:
        OtherDir = Dir()
        #Debug.Print "OterDir" & OtherDir
        if OtherDir != '':
            if OtherDir > VerDir:
                VerDir = OtherDir
        else:
            break
        if not (True):
            break
    if Dir(SeachDir + VerDir + SearchName) == '':
        MsgBox(Get_Language_Str('Fehler: \'') + SearchName + Get_Language_Str('\' existiert nicht in dem Verzeichnis:') + vbCr + '  \'' + SeachDir + VerDir + '\'', vbCritical, Get_Language_Str('Fehler: Datei wurde nicht gefunden ;-('))
        return fn_return_value
    fn_return_value = '%USERPROFILE%' + UserDir + VerDir + SearchName
    return fn_return_value

def __Find_Avrdude():
    fn_return_value = None
    #----------------------------------------
    fn_return_value = __Find_File_in_UserDir_with_Version_Dir('\\AppData\\Local\\Arduino15\\packages\\arduino\\tools\\avrdude\\', '*-arduino*', '\\bin\\avrdude.exe')
    return fn_return_value

def __Find_Avrdude_conf():
    fn_return_value = None
    #---------------------------------------------
    # %USERPROFILE%\AppData\Local\Arduino15\packages\ATTinyCore\hardware\avr\1.3.2/avrdude.conf
    fn_return_value = __Find_File_in_UserDir_with_Version_Dir('\\AppData\\Local\\Arduino15\\packages\\ATTinyCore\\hardware\\avr\\', '', '\\avrdude.conf')
    #Debug.Print "Result" & Find_Avrdude_conf
    return fn_return_value

def __Create_Set_Fuses_Cmd_file(ResultName, Mode, DstDir):
    fn_return_value = None
    Avrdude = String()

    Avrdude_conf = String()

    ClockTxt = String()

    BODTxt = String()

    LTOTxt = String()

    LFuse = String()

    HFuse = String()

    fp = Integer()

    Name = String()
    #-----------------------------------------------------------------------------------------------------------
    if ResultName == '':
        ResultName = 'Set_Fuses_Result.txt'
    if Dir(ResultName) != '':
        Kill(ResultName)
    Avrdude = __Find_Avrdude()
    if Avrdude == '':
        return fn_return_value
    Avrdude_conf = __Find_Avrdude_conf()
    if Avrdude_conf == '':
        return fn_return_value
    if (Mode == '16MHz, BOD 2.7V'):
        LFuse = '0xF1'
        HFuse = '0xD5'
        ClockTxt = '\'16 MHz (PLL)\''
        BODTxt = '\'B.O.D. Enabled (2.7V)\''
    elif (Mode == ' 8MHz, BOD 2.7V'):
        LFuse = '0xE2'
        HFuse = '0xD5'
        ClockTxt = '\'8 MHz\''
        BODTxt = '\'B.O.D. Enabled (2.7V)\''
    elif (Mode == ' 8MHz, BOD 2.7V, RstAsIO'):
        LFuse = '0xE2'
        HFuse = '0x55'
        ClockTxt = '\'8 MHz\''
        BODTxt = '\'B.O.D. Enabled (2.7V)\''
    elif (Mode == '16MHz, BOD 2.7V, RstAsIO'):
        LFuse = '0xF1'
        HFuse = '0x55'
        ClockTxt = '\'16 MHz (PLL)\''
        BODTxt = '\'B.O.D. Enabled (2.7V)\''
    else:
        MsgBox('Undefined Mode ')
        EndProg()
    fp = FreeFile()
    Name = DstDir + 'Set_Fuses.cmd'
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM This file was generated by \'' + ThisWorkbook.Name + '\'  ' + Time, '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM Setting the fuses for the ATTiny', '\n')
    VBFiles.writeText(fp, 'REM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM   Arduino Configuration:                            Comments', '\n')
    VBFiles.writeText(fp, 'REM   ~~~~~~~~~~~~~~~~~~~~~~', '\n')
    VBFiles.writeText(fp, 'REM   Board:              \'ATtiny25/45/85\'', '\n')
    VBFiles.writeText(fp, 'REM   Clock:              ' + ClockTxt, '\n')
    VBFiles.writeText(fp, 'REM   Chip:               \'ATTiny85\'', '\n')
    VBFiles.writeText(fp, 'REM   B.O.D.Level:        ' + BODTxt, '\n')
    VBFiles.writeText(fp, 'REM   Save EEPROM:        \'EEPROM retained\'', '\n')
    VBFiles.writeText(fp, 'REM   Timer 1 Clock:      \'CPU\'', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'REM Schwarz auf Ocker', '\n')
    VBFiles.writeText(fp, 'COLOR 60', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, Replace(Get_Language_Str('ECHO Programmierung der Fuses fuer den ATTiny' + vbCr + 'ECHO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' + vbCr + 'ECHO Mit diesem Programm werden die Fuses des ATTiny85 gesetzt.' + vbCr + 'ECHO Die Fuses bestimmen die Taktfrequenz (') + ClockTxt + Get_Language_Str(') und die' + vbCr + 'ECHO Unterspannungserkennung (B.O.D. Level ') + BODTxt + ')' + vbCr + Get_Language_Str('ECHO Der ATTiny85 muss dazu in die Tiny_UniProg Platine gesteckt sein.' + vbCr + 'ECHO Dieser Vorgang muss nur ein mal gemacht werden. Danach wird nur noch die geaenderte' + vbCr + 'ECHO Konfiguration vom Pattern_Configuartor aus zum ATTiny geschickt.'), vbCr, vbCrLf), '\n')
    VBFiles.writeText(fp, 'ECHO.', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'SET DefaultPort=5', '\n')
    VBFiles.writeText(fp, 'SET ComPort=%1', '\n')
    VBFiles.writeText(fp, 'IF NOT "%ComPort%" == "" Goto PortIsSet', '\n')
    VBFiles.writeText(fp, '   SET /P PortNr=COM port Nummer an den der Tiny_UniProg angeschlossen ist [%DefaultPort%]:', '\n')
    VBFiles.writeText(fp, '   IF "%PortNr%" == "" SET PortNr=%DefaultPort%', '\n')
    VBFiles.writeText(fp, '   SET ComPort=\\\\.\\COM%PortNr%', '\n')
    VBFiles.writeText(fp, ':PortIsSet', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '"' + Avrdude + '" ^', '\n')
    VBFiles.writeText(fp, '    "-C' + Avrdude_conf + '"  ^', '\n')
    # Print #fp, "    -v -pattiny85 -cstk500v1 -P%ComPort% -b19200 -e ^"
    VBFiles.writeText(fp, '    -v -pattiny85 -cstk500v1 -P%ComPort% -b19200 ^', '\n')
    VBFiles.writeText(fp, '    -Uefuse:w:0xFF:m -Uhfuse:w:' + HFuse + ':m -Ulfuse:w:' + LFuse + ':m', '\n')
    VBFiles.writeText(fp, '', '\n')
    #Print #fp, "ECHO avrdude result: %ERRORLEVEL%"
    #Print #fp, "Pause"
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'IF ERRORLEVEL 1 (', '\n')
    VBFiles.writeText(fp, '    ECHO Error settung the fuses ;-(', '\n')
    VBFiles.writeText(fp, '    ECHO Starting second try', '\n')
    VBFiles.writeText(fp, '    timeout /T 3 /nobreak', '\n')
    VBFiles.writeText(fp, '    "' + Avrdude + '" ^', '\n')
    VBFiles.writeText(fp, '        "-C' + Avrdude_conf + '"  ^', '\n')
    VBFiles.writeText(fp, '        -v -pattiny85 -cstk500v1 -P%ComPort% -b19200 ^', '\n')
    VBFiles.writeText(fp, '        -Uefuse:w:0xFF:m -Uhfuse:w:' + HFuse + ':m -Ulfuse:w:' + LFuse + ':m', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '   )', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'IF ERRORLEVEL 1 (', '\n')
    VBFiles.writeText(fp, '    ECHO Error settung the fuses ;-(((', '\n')
    VBFiles.writeText(fp, '    ECHO Starting third try', '\n')
    VBFiles.writeText(fp, '    timeout /T 3 /nobreak', '\n')
    VBFiles.writeText(fp, '    "' + Avrdude + '" ^', '\n')
    VBFiles.writeText(fp, '        "-C' + Avrdude_conf + '"  ^', '\n')
    VBFiles.writeText(fp, '        -v -pattiny85 -cstk500v1 -P%ComPort% -b19200 ^', '\n')
    VBFiles.writeText(fp, '        -Uefuse:w:0xFF:m -Uhfuse:w:' + HFuse + ':m -Ulfuse:w:' + LFuse + ':m', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '   )', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'IF ERRORLEVEL 1 (', '\n')
    VBFiles.writeText(fp, '   REM White on RED', '\n')
    VBFiles.writeText(fp, '   COLOR 4F', '\n')
    VBFiles.writeText(fp, '   ECHO Set_Fuses Result: %ERRORLEVEL% > "' + ResultName + '"', '\n')
    VBFiles.writeText(fp, '   ECHO   *********************************************', '\n')
    VBFiles.writeText(fp, '   ECHO  ' + Get_Language_Str('* Da ist was schief gegangen ;-(            *') + '              ERRORLEVEL %ERRORLEVEL%', '\n')
    VBFiles.writeText(fp, '   ECHO   *********************************************', '\n')
    VBFiles.writeText(fp, '   Pause', '\n')
    VBFiles.writeText(fp, '   )', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = Name
    return fn_return_value
    MsgBox(Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, Get_Language_Str('Fehler beim erzeugen der cmd Datei'))
    VBFiles.closeFile(fp)
    return fn_return_value

def __Test_Create_Set_Fuses_Cmd_file():
    ResultName = String()
    #UT-----------------------------------------
    Debug.Print(__Create_Set_Fuses_Cmd_file(ResultName, '16MHz, BOD 2.7V', Replace(ThisWorkbook.Path, 'extras', 'examples\\80.Modules\\02.CharlieplexTiny\\')))

def __Write_Fuses(ComPort, Mode, DstDir):
    fn_return_value = None
    ResFile = String()

    CommandStr = String()

    Res = ShellAndWaitResult()
    #-------------------------------------------------------------------------------------------
    CommandStr = __Create_Set_Fuses_Cmd_file(ResFile, Mode, DstDir)
    if CommandStr != '':
        ChDrive(CommandStr)
        ChDir(FilePath(CommandStr))
        Res = ShellAndWait(CommandStr + ' ' + ComPort, 0, vbNormalFocus, PromptUser)
        if (Res == Success) or (Res == Timeout):
            pass
        else:
            MsgBox(Get_Language_Str('Fehler ') + Res + Get_Language_Str(' beim starten des Arduino Programms \'') + CommandStr + '\'', vbCritical, Get_Language_Str('Fehler beim starten des Arduino programms'))
        if Dir(ResFile) != '':
            MsgBox(Get_Language_Str('Es ist ein Fehler beim setzen der Fuses aufgetreten ;-(' + vbCr + vbCr + 'Falls die blaue \'Reset as IOPin\' LED am Tiny_UniProg leuchtet, dann muss ' + 'die rechte Taste (\'Cng Reset Pin\') am Tiny_UniProc für eine Sekunde gedückt werden. ' + 'Damit wird der Reset Pin wieder aktiviert.' + vbCr + 'Wenn die Taste länger als 3 Sekunden gehalten wird, dann wird der Pin zum Ein/Ausgang umprogrammiert.' + vbCr + 'Das erkennt man an der blauen LED. Dieser Modus wird z.B. bei der Servo Platine benötigt.' + vbCr + vbCr + 'Wenn der Fehler immer wieder auftritt, dann kann ein Screenshot des ' + 'vorangegangenen Bildschirms zusammen mit einer ausführlichen Beschreibung an ' + vbCr + '  MobaLedLib@gmx.de' + vbCr + 'geschickt werden.'), vbInformation, Get_Language_Str('Fehler schreiben der Fuses'))
            return fn_return_value
        fn_return_value = True
    return fn_return_value

def __Test_Write_Fuses_if_Wanted():
    #UT-------------------------------------
    __Write_Fuses()('\\\\.\\COM7', '16MHz, BOD 2.7V', Replace(ThisWorkbook.Path, 'extras', 'examples\\80.Modules\\02.CharlieplexTiny\\'))
    # Write_Fuses "\\.\COM7", " 8MHz, BOD 2.7V", Replace(ThisWorkbook.Path, "extras", "examples\80.Modules\02.CharlieplexTiny\")

def __Compile_and_Upload(SrcDir, InoName, CommandStr, ResFile):
    fn_return_value = None
    Res = ShellAndWaitResult()

    Start = Variant()

    ComPortColumn = COMPrtT_COL
    #---------------------------------------------------------------------------------------------------------------------------
    Start = Time
    if Dir(SrcDir + InoName) == '':
        MsgBox(Get_Language_Str('Fehler das Program ') + InoName + Get_Language_Str(' ist nicht vorhanden in:') + vbCr + '  \'' + SrcDir + '\'', vbCritical, Get_Language_Str('Fehler Ino-Programm nicht vorhanden'))
        return fn_return_value
    ChDrive(SrcDir)
    ChDir(SrcDir)
    Res = ShellAndWait(CommandStr, 0, vbNormalFocus, PromptUser)
    if (Res == Success) or (Res == Timeout):
        pass
    else:
        MsgBox(Get_Language_Str('Fehler ') + Res + Get_Language_Str(' beim starten des Arduino Programms \'') + CommandStr + '\'', vbCritical, Get_Language_Str('Fehler beim starten des Arduino programms'))
    if Dir(ResFile) != '':
        MsgBox(Get_Language_Str('Es ist ein Fehler aufgetreten ;-(' + vbCr + vbCr + 'Kommunikationsprobleme erkennt man an dieser Meldung: ' + vbCr + '   avrdude: ser_open(): can\'t open device "\\\\.\\COM') + Cells(SH_VARS_ROW, ComPortColumn) + '":' + vbCr + Get_Language_Str('   Das System kann die angegebene Datei nicht finden.' + vbCr + 'In diesem Fall müssen die Verbindungen überprüft und der Arduino durch einen neuen ersetzt werden.' + vbCr + vbCr + 'Wenn der Fehler nicht immer wieder auftritt, dann kann ein Screenshot des ' + 'vorangegangenen Bildschirms zusammen mit einer ausführlichen Beschreibung an ' + vbCr + '  MobaLedLib@gmx.de' + vbCr + 'geschickt werden.'), vbInformation, Get_Language_Str('Fehler beim Hochladen des Programms'))
        EndProg()
    else:
        Debug.Print('Compile and upload duaration: ' + Format(Time - Start, 'hh:mm:ss'))
        Show_Status_for_a_while(Get_Language_Str('Programm erfolgreich hochgeladen. Kompilieren und Hochladen dauerte ') + Format(Time - Start, 'hh:mm:ss'), '00:00:30')
        fn_return_value = True
    return fn_return_value

def __Get_COMPortStr(ComPortColumn):
    fn_return_value = None
    #---------------------------------------------------------------
    Check_USB_Port_with_Dialog(ComPortColumn)
    fn_return_value = '\\\\.\\COM' + ComPortPage().Cells(SH_VARS_ROW, ComPortColumn)
    return fn_return_value

def __Check_If_Arduino_could_be_programmed_PatGen():
    fn_return_value = None
    BuildOptions = String()

    ActSheet = String()

    OldUpdateing = Boolean()
    #------------------------------------------------------------------------
    OldUpdateing = Application.ScreenUpdating
    Application.ScreenUpdating = False
    ThisWorkbook.Activate()
    ActSheet = ActiveSheet.Name
    Sheets(MAIN_SH).Select()
    fn_return_value = Check_If_Arduino_could_be_programmed_and_set_Board_type(COMPrtT_COL, BuildOT_COL, BuildOptions)
    Debug.Print('Check_If_Arduino_could_be_programmed_and_set_Board_type=' + __Check_If_Arduino_could_be_programmed_PatGen() + ' BuildOptions=' + BuildOptions)
    Sheets(ActSheet).Select()
    Application.ScreenUpdating = OldUpdateing
    return fn_return_value

def __Compile_and_Upload_Prog_to_ATTiny(InoName, WorkDir, Mode, Mode2=VBMissingArgument):
    fn_return_value = None
    ComPort = String()

    ResFile = String()

    CommandStr = String()

    ComPortColumn = COMPrtT_COL
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # 07.08.20: Disabled
    #If MsgBox(Get_Language_Str("Achtung: Der Programmieradapter (Tiny_UniProg) benötigt nach den anstecken das USB Steckers " & _
"bis zu 3 Sekunden zum starten und erkennen des eingesteckten ATTinys. Das er bereit ist erkennt man " & _
"an der pulsierenden grünen 'Heart Beat' LED. Außerdem darf die rote 'Error' LED nicht leuchten." & vbCr & _
"Der Programmiervorgang kann erst gestartet werden wenn beide Bedingungen erfüllt sind." & vbCr & _
vbCr & _
"Die Erkennung des ATTinys kann mit einem kurzen Druck Reset Taste am Arduino neu gestartet werden " & _
"falls die 'Error' LED leuchtet." & vbCr & _
vbCr & _
"Falls die blaue 'Reset as IOPin' LED leuchtet, dann muss die rechte Taste ('Cng Reset Pin') am Tiny_UniProc " & _
"für eine Sekunde gedückt werden. Damit wird der Reset Pin wieder aktiviert." & vbCr & _
"Wenn die Taste länger als 3 Sekunden gehalten wird, dann wird der Pin zum Ein/Ausgang umprogrammiert." & vbCr & _
"Das erkennt man an der blauen LED. Dieser Modus wird z.B. bei der Servo Platine benötigt." & vbCr & _
vbCr & _
"Soll die Programmierung jetzt gestartet werden ?"), vbQuestion + vbOKCancel, _
Get_Language_Str("Programmieradapter Bereit ?")) = vbCancel Then Exit Function
    if __Check_If_Arduino_could_be_programmed_PatGen() == False:
        return fn_return_value
        # 05.06.20:
    ComPort = __Get_COMPortStr(ComPortColumn)
    Sleep(1000)
    if __Write_Fuses(ComPort, Mode, WorkDir) == False:
        return fn_return_value
        # The fuses are always written because it's better not to ask the user to avoid confusion
    ResFile = 'Compile_and_Upload_to_ATTiny85_Result.txt'
    CommandStr = 'Compile_and_Upload_to_ATTiny85.cmd ' + ComPort
    if __Compile_and_Upload(WorkDir, InoName, CommandStr, ResFile) == False:
        return fn_return_value
        # 05.06.20: Removed: ComPortColumn because it was always set to COMPrtT_COL
    if Mode2 != '':
        Sleep(2000)
        if __Write_Fuses(ComPort, Mode2, WorkDir) == False:
            return fn_return_value
            # The fuses are always written because it's better not to ask the user to avoid confusion
    fn_return_value = True
    return fn_return_value

def __Write_LED_Polarity_h(SrcDir, LED_Polarity):
    fn_return_value = None
    fp = Integer()

    Name = String()
    #------------------------------------------------------------------------------------------
    fp = FreeFile()
    Name = SrcDir + 'LED_Polarity.h'
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '// This file was generated by \'' + ThisWorkbook.Name + '\'  ' + Time, '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#define LED_POLARITY_NORMAL ' + LED_Polarity, '\n')
    VBFiles.writeText(fp, '// 1 = Normal LED polarity (+ on the left side)', '\n')
    VBFiles.writeText(fp, '// 0 = invers LED polarity (- on the left side)', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = True
    return fn_return_value
    MsgBox(Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, Get_Language_Str('Fehler beim erzeugen der Datei'))
    VBFiles.closeFile(fp)
    return fn_return_value

def __Define_LED_Polarity(SrcDir):
    fn_return_value = None
    LED_Polarity = Integer()
    #----------------------------------------------------------------
    select_3 = MsgBox(Get_Language_Str('Der Bestückungsdruck der LEDs bei der ersten "TinyUniProg" Platine ' + 'vom 16.06.19 ist dummerweise falsch ;-(' + vbCr + vbCr + 'Soll das Programm auf einer neueren Platine verwendet werden bzw. ist der Plus Pol ' + 'der LEDs auf der linken Seite der Platine (=Abgeflachte Seite der LED rechts) ?' + vbCr + vbCr + 'Ja:  Plus Pol links, abgeflachte Seite rechts' + vbCr + 'Nein: Plus Pol rechts, abgeflachte Seite links'), vbQuestion + vbYesNoCancel, Get_Language_Str('Einbaurichtung der LEDs?'))
    if (select_3 == vbYes):
        LED_Polarity = 1
    elif (select_3 == vbCancel):
        return fn_return_value
    fn_return_value = __Write_LED_Polarity_h(SrcDir, LED_Polarity)
    return fn_return_value

def __Test_Define_LED_Polarity():
    #UT-----------------------------------
    Debug.Print(__Define_LED_Polarity('C:\\Dat\\Märklin\\Arduino\\LEDs_Eisenbahn\\examples\\90.Tools\\02.Tiny_UniProg\\'))

def Prog_Tiny_UniProg():
    SrcDir = String()

    CommandStr = String()
    #-----------------------------
    if LCase(Left(ThisWorkbook.Path, Len('extras'))) == 'extras':
        SrcDir = ThisWorkbook.Path
    else:
        SrcDir = Get_SrcDirInLib()
    SrcDir = Replace(SrcDir, 'Extras', 'examples\\90.Tools\\02.Tiny_UniProg\\', Compare= vbTextCompare)
    if __Define_LED_Polarity(SrcDir) == False:
        return
        # 05.06.20:
    if __Check_If_Arduino_could_be_programmed_PatGen() == False:
        return
        # 05.06.20:
    CommandStr = 'Compile_and_Upload_to_Uno.cmd ' + __Get_COMPortStr(COMPrtT_COL)
    __Compile_and_Upload()(SrcDir, '02.Tiny_UniProg.ino', CommandStr, 'Compile_and_Upload_to_Uno_Result.txt')

def Prog_Charlieplex():
    WorkDir = String()
    #----------------------------
    ThisWorkbook.Activate()
    if LCase(Right(ThisWorkbook.Path, Len('extras'))) == 'extras':
        WorkDir = ThisWorkbook.Path
    else:
        WorkDir = Get_SrcDirInLib()
    WorkDir = Replace(WorkDir, 'Extras', 'examples\\80.Modules\\02.CharlieplexTiny\\', Compare= vbTextCompare)
    if __Compile_and_Upload_Prog_to_ATTiny('02.CharlieplexTiny.ino', WorkDir, '16MHz, BOD 2.7V'):
        MsgBox(Get_Language_Str('Das "Betriebssystem" des Charlieplexing Moduls wurde erfolgreich programmiert.' + vbCr + 'Dieser Schritt ist nur ein mal pro Platine nötig.' + vbCr + 'Als nächstes muss die Konfiguration zum ATTiny geschickt werden. Das wird über den "Zum Modul schicken" ' + 'Knopf der entsprechenden Seite gemacht.'), vbInformation, Get_Language_Str('Programm erfolgreich zum ATTiny übertragen'))

def __Create_Inp_Prtx(DstDir, Correct_Pins):
    fn_return_value = None
    fp = Integer()

    Name = String()
    #-------------------------------------------------------------------------------------
    fp = FreeFile()
    Name = DstDir + 'Inp_Prtx.h'
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '// This file was generated by \'' + ThisWorkbook.Name + '\'  ' + Time, '\n')
    VBFiles.writeText(fp, '', '\n')
    if Correct_Pins:
        VBFiles.writeText(fp, '// Corrected input Pin list for servo platine ver. 1.0 with SMD WS2811', '\n')
        VBFiles.writeText(fp, 'const uint8_t Inp_Prtx[MAX_CHANNEL] = {4, 3, 5 }; // PBx number n', '\n')
    else:
        VBFiles.writeText(fp, '// Normal input Pin list for servo platine > Ver 1.0 or DIL WS2811', '\n')
        VBFiles.writeText(fp, 'const uint8_t Inp_Prtx[MAX_CHANNEL] = {3, 4, 5 }; // PBx number n', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = True
    return fn_return_value
    MsgBox(Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, Get_Language_Str('Fehler beim erzeugen der \'Create_Inp_Prtx\' Datei'))
    VBFiles.closeFile(fp)
    return fn_return_value

def Prog_Servo():
    WorkDir = String()

    Correct_Pins = Boolean()
    #----------------------
    ThisWorkbook.Activate()
    if LCase(Right(ThisWorkbook.Path, Len('extras'))) == 'extras':
        WorkDir = ThisWorkbook.Path
    else:
        WorkDir = Get_SrcDirInLib()
    WorkDir = Replace(WorkDir, 'Extras', 'examples\\80.Modules\\01.ATTiny85_Servo\\', Compare= vbTextCompare)
    select_4 = MsgBox(Get_Language_Str('Bei der Servo Platine der Version 1.0 hat sich ein Fehler bei der Pin Definition des SMD WS2811 eingeschlichen ;-(' + vbCr + 'Das führt dazu, das der rote und grüne Kanal vertauscht sind.' + vbCr + vbCr + 'Korrektur der SMD WS2811 Pins?' + vbCr + vbCr + 'Ja:' + vbCr + 'Wenn die Platine vom 14.6.19 ist UND ein SMD WS2811 bestückt wurde' + vbCr + 'Nein:' + vbCr + 'Bei einer neueren Platine oder wenn ein DIL WS2811 verwendet wird'), vbQuestion + vbYesNoCancel, Get_Language_Str('Korrektur der SMD WS2811 Pins?'))
    if (select_4 == vbCancel):
        return
    elif (select_4 == vbYes):
        Correct_Pins = True
    elif (select_4 == vbNo):
        Correct_Pins = False
    if __Create_Inp_Prtx(WorkDir, Correct_Pins) == False:
        return
    if __Compile_and_Upload_Prog_to_ATTiny('01.ATTiny85_Servo.ino', WorkDir, '16MHz, BOD 2.7V', '16MHz, BOD 2.7V, RstAsIO'):
        MsgBox(Get_Language_Str('Das "Betriebssystem" des Servo Moduls wurde erfolgreich programmiert.' + vbCr + 'Dieser Schritt ist nur ein mal pro Platine nötig.' + vbCr + 'Als nächstes sollten die Endpositionen und die Geschwindigkeiten eingestellt werden.' + vbCr + 'Das kann mit zwei verschiednen Programmen gemacht werden:' + vbCr + '- das Arduino Programm "01.Servo_Pos"' + vbCr + '- das "Farbtest" Programm von Harold (\'Prog_Generator\' Menü)"'), vbInformation, Get_Language_Str('Programm erfolgreich zum ATTiny übertragen'))

def Prog_ServoMP3():
    WorkDir = String()

    Correct_Pins = Boolean()
    #----------------------
    ThisWorkbook.Activate()
    if LCase(Right(ThisWorkbook.Path, Len('extras'))) == 'extras':
        WorkDir = ThisWorkbook.Path
    else:
        WorkDir = Get_SrcDirInLib()
    WorkDir = Replace(WorkDir, 'Extras', 'examples\\80.Modules\\03.ATTiny85_Sound\\', Compare= vbTextCompare)
    select_5 = MsgBox(Get_Language_Str('Bei der Servo Platine der Version 1.0 hat sich ein Fehler bei der Pin Definition des SMD WS2811 eingeschlichen ;-(' + vbCr + 'Das führt dazu, das der rote und grüne Kanal vertauscht sind.' + vbCr + vbCr + 'Korrektur der SMD WS2811 Pins?' + vbCr + vbCr + 'Ja:' + vbCr + 'Wenn die Platine vom 14.6.19 ist UND ein SMD WS2811 bestückt wurde' + vbCr + 'Nein:' + vbCr + 'Bei einer neueren Platine oder wenn ein DIL WS2811 verwendet wird'), vbQuestion + vbYesNoCancel, Get_Language_Str('Korrektur der SMD WS2811 Pins?'))
    if (select_5 == vbCancel):
        return
    elif (select_5 == vbYes):
        Correct_Pins = True
    elif (select_5 == vbNo):
        Correct_Pins = False
    if __Create_Inp_Prtx(WorkDir, Correct_Pins) == False:
        return
    if __Compile_and_Upload_Prog_to_ATTiny('03.ATTiny85_Sound.ino', WorkDir, '16MHz, BOD 2.7V', '16MHz, BOD 2.7V, RstAsIO'):
        MsgBox(Get_Language_Str('Das "Betriebssystem" des Servo Moduls wurde erfolgreich zur Anbindung von MP3-Modulen programmiert.' + vbCr + 'Dieser Schritt ist nur ein mal pro Platine nötig.' + vbCr + 'Als nächstes sollten angeschlossenen Soundmodule konfiguriert werden (siehe Anleitung' + vbCr + 'im Verzeichnis \'' + WorkDir + '\''), vbInformation, Get_Language_Str('Programm erfolgreich zum ATTiny übertragen'))

# VB2PY (UntranslatedCode) Option Explicit
