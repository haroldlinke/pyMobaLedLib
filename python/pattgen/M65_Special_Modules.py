# -*- coding: utf-8 -*-

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from tkinter import filedialog
import ExcelAPI.XLA_Application as X02
import pattgen.M09_Language as M09
import pattgen.M30_Tools as M30
import proggen.M40_ShellandWait as M40
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M01a_Public_Constants_a_Var as M01a
import proggen.M07_COM_Port as M07a
import proggen.M07_COM_Port_New as M07b
import proggen.M08_ARDUINO as M08
import mlpyproggen.Pattern_Generator as PG
import mlpyproggen.Prog_Generator as ProgGen
import proggen.M02_Public as M02

import ExcelAPI.XLWA_WinAPI as X03
import ExcelAPI.XLC_Excel_Consts as X01

from tools.CRCalgorithms import CalculateControlValuewithChecksum

def Find_File_in_UserDir_with_Version_Dir(UserDir, VersionDir, SearchName):
    _fn_return_value = None
    SearchDir = String()

    VerDir = String()

    OtherDir = String()
    #------------------------------------------------------------------------------------------------------------------------------
    # Example:
    # Seach for %USERPROFILE%\AppData\Local\Arduino15\packages\arduino\tools\avrdude\6.3.0-arduino17/bin/avrdude.exe
    # Parameters:
    #   UserDir:    "\AppData\Local\Arduino15\packages\arduino\tools\avrdude\"
    #   VersionDir: "*-arduino*"
    #   SearchName: "\bin\avrdude.exe"
    SearchDir = Environ(M02.Env_USERPROFILE) + UserDir
    
    # arduino_packages_dir = Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + 'packages/' # 'C:\Users/Harold/AppData/Local/Arduino15/packages/'
    VerDir = Dir(SearchDir + VersionDir, vbDirectory)
    if VerDir == '':
        X02.MsgBox(Replace(M09.Get_Language_Str('Fehler: Das Verzeichnis \'#1#\' wurde nicht gefunden'), '#1#', SearchDir + VersionDir), vbCritical, M09.Get_Language_Str('Verzeichnis nicht gefunden'))
        # 09.04.20: Added: SeachDir to prevent empty string id searched from "Find_Avrdude_conf()"
        return _fn_return_value
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
    if Dir(SearchDir + VerDir + SearchName) == '':
        X02.MsgBox(M09.Get_Language_Str('Fehler: \'') + SearchName + M09.Get_Language_Str('\' existiert nicht in dem Verzeichnis:') + vbCr + '  \'' + SearchDir + VerDir + '\'', vbCritical, M09.Get_Language_Str('Fehler: Datei wurde nicht gefunden ;-('))
        return _fn_return_value
    _fn_return_value = SearchDir + VerDir + SearchName
    return _fn_return_value

def Find_Avrdude():
    _fn_return_value = None
    
    if X02.checkplatform("Windows"):
        avrdude = "avrdude.exe"
    else:
        avrdude = "avrdude"
    #----------------------------------------
    
    #userdir = '\\AppData\\Local\\Arduino15\\packages\\arduino\\tools\\avrdude\\'
    userdir = M02.AppLoc_Ardu + "packages/arduino/tools/avrdude/"
    _fn_return_value = Find_File_in_UserDir_with_Version_Dir(userdir, '*-arduino*', '/bin/'+avrdude)
    return _fn_return_value

def Find_Avrdude_conf():
    _fn_return_value = None
    #---------------------------------------------
    # %USERPROFILE%\AppData\Local\Arduino15\packages\ATTinyCore\hardware\avr\1.3.2/avrdude.conf
    #userdir = '\\AppData\\Local\\Arduino15\\packages\\ATTinyCore\\hardware\\avr\\'
    userdir = M02.AppLoc_Ardu + "packages/ATTinyCore/hardware/avr/"    
    _fn_return_value = Find_File_in_UserDir_with_Version_Dir(userdir, '*', '/avrdude.conf')
    #Debug.Print "Result" & Find_Avrdude_conf
    return _fn_return_value

def Create_Set_Fuses_Cmd_file(ResultName, Mode, DstDir, ComPort):
    _fn_return_value = None
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
    Avrdude = Find_Avrdude()
    if Avrdude == '':
        return _fn_return_value
    Avrdude_conf = Find_Avrdude_conf()
    if Avrdude_conf == '':
        return _fn_return_value
    _select57 = Mode
    if (_select57 == '16MHz, BOD 2.7V'):
        LFuse = '0xF1'
        HFuse = '0xD5'
        EFuse = '0xFF'
        ClockTxt = '\'16 MHz (PLL)\''
        BODTxt = '\'B.O.D. Enabled (2.7V)\''
    elif (_select57 == ' 8MHz, BOD 2.7V'):
        LFuse = '0xE2'
        HFuse = '0xD5'
        EFuse = '0xFF'
        ClockTxt = '\'8 MHz\''
        BODTxt = '\'B.O.D. Enabled (2.7V)\''
    elif (_select57 == ' 8MHz, BOD 2.7V, RstAsIO'):
        LFuse = '0xE2'
        HFuse = '0x55'
        EFuse = '0xFF'
        ClockTxt = '\'8 MHz\''
        BODTxt = '\'B.O.D. Enabled (2.7V)\''
        # 05.06.20:
    elif (_select57 == '16MHz, BOD 2.7V, RstAsIO'):
        LFuse = '0xF1'
        HFuse = '0x55'
        EFuse = '0xFF'
        ClockTxt = '\'16 MHz (PLL)\''
        BODTxt = '\'B.O.D. Enabled (2.7V)\''
        # 04.08.20:
    elif (_select57 == '16MHz, BOD 2.7V, Eckhart'):
        LFuse = '0xE1'
        HFuse = '0xD5'
        EFuse = '0xFF'
        ClockTxt = '\'16 MHz (PLL)\''
        BODTxt = '\'B.O.D. Enabled (2.7V) Eckhart\''
        # 01.07.24
    elif (_select57 == '16MHz, BOD 2.7V, Eckhart-LED'):
        LFuse = '0xE1'
        HFuse = '0x55'
        EFuse = '0xFF'
        ClockTxt = '\'16 MHz (PLL)\''
        BODTxt = '\'B.O.D. Enabled (2.7V) Eckhart-LED\''
        # 04.08.20:
    elif (_select57 == '16MHz, BOD 2.7V, Eckhart-Boot'):
        LFuse = '0xE1'
        HFuse = '0x55'
        EFuse = '0xFE'
        ClockTxt = '\'16 MHz (PLL)\''
        BODTxt = '\'B.O.D. Enabled (2.7V) Eckhart-Boot\''
        # 04.08.20:             
    else:
        X02.MsgBox('Undefined Mode ')
        # & Mode & "' in 'Create_Set_Fuses_Cmd_file()'", vbCritical, "Internal Error"
        M30.EndProg()
    fp = FreeFile()
    
    if False: #X02.checkplatform("Windows"): 
        Name = DstDir + '/Set_Fuses.cmd'
        # VB2PY (UntranslatedCode) On Error GoTo WriteError
        VBFiles.openFile(fp, Name, 'w') 
        VBFiles.writeText(fp, '@ECHO OFF', '\n')
        VBFiles.writeText(fp, 'REM This file was generated by \'' + PG.ThisWorkbook.Name + '\'  ' + str(X02.Time()), '\n')
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
        VBFiles.writeText(fp, Replace(M09.Get_Language_Str('ECHO Programmierung der Fuses fuer den ATTiny' + vbCr + 'ECHO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' + vbCr + 'ECHO Mit diesem Programm werden die Fuses des ATTiny85 gesetzt.' + vbCr + 'ECHO Die Fuses bestimmen die Taktfrequenz (') + ClockTxt + M09.Get_Language_Str(') und die' + vbCr + 'ECHO Unterspannungserkennung (B.O.D. Level ') + BODTxt + ')' + vbCr + M09.Get_Language_Str('ECHO Der ATTiny85 muss dazu in die Tiny_UniProg Platine gesteckt sein.' + vbCr + 'ECHO Dieser Vorgang muss nur ein mal gemacht werden. Danach wird nur noch die geaenderte' + vbCr + 'ECHO Konfiguration vom Pattern_Configuartor aus zum ATTiny geschickt.'), vbCr, vbCrLf), '\n')
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
        # 24.07.20: Removed chip erase: -e
        VBFiles.writeText(fp, '    -Uefuse:w:'+EFuse + ':m -Uhfuse:w:' + HFuse + ':m -Ulfuse:w:' + LFuse + ':m', '\n')
        VBFiles.writeText(fp, '', '\n')
        #Print #fp, "ECHO avrdude result: %ERRORLEVEL%"
        #Print #fp, "Pause"
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 (', '\n')
        # 07.08.20:
        VBFiles.writeText(fp, '    ECHO *******************************************************************', '\n')
        VBFiles.writeText(fp, '    ECHO Error settung the fuses ;-(', '\n')
        VBFiles.writeText(fp, '    ECHO Starting second try', '\n')
        VBFiles.writeText(fp, '    ECHO *******************************************************************', '\n')
        #VBFiles.writeText(fp, '    timeout /T 3 /nobreak', '\n')
        VBFiles.writeText(fp, '    "' + Avrdude + '" ^', '\n')
        VBFiles.writeText(fp, '        "-C' + Avrdude_conf + '"  ^', '\n')
        VBFiles.writeText(fp, '        -v -pattiny85 -cstk500v1 -P%ComPort% -b19200 ^', '\n')
        VBFiles.writeText(fp, '        -Uefuse:w:0xFF:m -Uhfuse:w:' + HFuse + ':m -Ulfuse:w:' + LFuse + ':m', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '   )', '\n')
        VBFiles.writeText(fp, '', '\n')
        
        #VBFiles.writeText(fp, 'IF ERRORLEVEL 1 (', '\n')
        # 07.08.20:
        #VBFiles.writeText(fp, '   ******************************************************************************************', '\n')
        #VBFiles.writeText(fp, '    ECHO Error settung the fuses ;-(((', '\n')
        #VBFiles.writeText(fp, '    ECHO Starting third try', '\n')
        #VBFiles.writeText(fp, '   ******************************************************************************************', '\n')
        #VBFiles.writeText(fp, '    timeout /T 3 /nobreak', '\n')
        #VBFiles.writeText(fp, '    "' + Avrdude + '" ^', '\n')
        #VBFiles.writeText(fp, '        "-C' + Avrdude_conf + '"  ^', '\n')
        #VBFiles.writeText(fp, '        -v -pattiny85 -cstk500v1 -P%ComPort% -b19200 ^', '\n')
        #VBFiles.writeText(fp, '        -Uefuse:w:0xFF:m -Uhfuse:w:' + HFuse + ':m -Ulfuse:w:' + LFuse + ':m', '\n')
        #VBFiles.writeText(fp, '', '\n')
        #VBFiles.writeText(fp, '   )', '\n')
        #VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'IF ERRORLEVEL 1 (', '\n')
        VBFiles.writeText(fp, '   REM White on RED', '\n')
        VBFiles.writeText(fp, '   COLOR 4F', '\n')
        VBFiles.writeText(fp, '   ECHO Set_Fuses Result: %ERRORLEVEL% > "' + ResultName + '"', '\n')
        VBFiles.writeText(fp, '   ECHO   *********************************************', '\n')
        VBFiles.writeText(fp, '   ECHO  ' + M09.Get_Language_Str('* Da ist was schief gegangen ;-(            *') + '              ERRORLEVEL %ERRORLEVEL%', '\n')
        VBFiles.writeText(fp, '   ECHO   *********************************************', '\n')
        VBFiles.writeText(fp, '   Pause', '\n')
        VBFiles.writeText(fp, '   )', '\n')
        VBFiles.writeText(fp, 'Pause', '\n')
        VBFiles.closeFile(fp)
        # VB2PY (UntranslatedCode) On Error GoTo 0
        _fn_return_value = Name
    else:
        cmd = '    "' + Avrdude + '" -C' + Avrdude_conf + '  -v -pattiny85 -cstk500v1 -P' + ComPort + ' -b19200 -Uefuse:w:'+EFuse + ':m -Uhfuse:w:' + HFuse + ':m -Ulfuse:w:' + LFuse + ':m' + '\n'
        _fn_return_value = cmd
    return _fn_return_value
    X02.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der cmd Datei'))
    VBFiles.closeFile(fp)
    return _fn_return_value

def Test_Create_Set_Fuses_Cmd_file():
    ResultName = String()
    #UT-----------------------------------------
    Debug.Print(Create_Set_Fuses_Cmd_file(ResultName, '16MHz, BOD 2.7V', Replace(PG.ThisWorkbook.Path, 'extras', 'examples\\80.Modules\\02.CharlieplexTiny\\'), "COMX"))

def Write_Fuses(ComPort, Mode, DstDir):
    _fn_return_value = False
    ResFile = "Write_Fuses_Result.txt"

    CommandStr = String()

    #Res = ShellAndWaitResult()
    #-------------------------------------------------------------------------------------------
    CommandStr = Create_Set_Fuses_Cmd_file(ResFile, Mode, DstDir, ComPort)
    if CommandStr != '':
        if False: #X02.checkplatform("Windows"):
            X02.ChDrive(CommandStr)
            ChDir(M30.FilePath(CommandStr))
            #Res = M40.ShellAndWait(CommandStr + ' ' + ComPort, 0, vbNormalFocus, PromptUser)
            ProgGen.global_controller.disconnect()
            res = ProgGen.dialog_parent.start_ARDUINO_program_cmd(CommandStr + ' ' + str(ComPort),arduino_type="Tiny") #*HL
            # No timeout to be able to study the results in case of an error
        else:
            ProgGen.global_controller.disconnect()
            Res = ProgGen.dialog_parent.start_ARDUINO_program_cmd(CommandStr) #*HL
            
        _select58 = Res
        if (_select58 == M40.Success) or (_select58 == M40.Timeout):
            # No additional error message. They have been shown in the DOS box
            pass
        else:
            X02.MsgBox(M09.Get_Language_Str('Fehler ') + str(Res) + M09.Get_Language_Str(' beim starten des Arduino Programms \'') + CommandStr + '\'', vbCritical, M09.Get_Language_Str('Fehler beim starten des Arduino programms'))
        if Dir(ResFile) != '':
            X02.MsgBox(M09.Get_Language_Str('Es ist ein Fehler beim setzen der Fuses aufgetreten ;-(' + vbCr + vbCr + 'Falls die blaue \'Reset as IOPin\' LED am Tiny_UniProg leuchtet, dann muss ' + 'die rechte Taste (\'Cng Reset Pin\') am Tiny_UniProc für eine Sekunde gedückt werden. ' + 'Damit wird der Reset Pin wieder aktiviert.' + vbCr + 'Wenn die Taste länger als 3 Sekunden gehalten wird, dann wird der Pin zum Ein/Ausgang umprogrammiert.' + vbCr + 'Das erkennt man an der blauen LED. Dieser Modus wird z.B. bei der Servo Platine benötigt.' + vbCr + vbCr + 'Wenn der Fehler immer wieder auftritt, dann kann ein Screenshot des ' + 'vorangegangenen Bildschirms zusammen mit einer ausführlichen Beschreibung an ' + vbCr + '  https://forum.mobaledlib.de' + vbCr + 'geschickt werden.'), vbInformation, M09.Get_Language_Str('Fehler schreiben der Fuses'))
            return _fn_return_value
        _fn_return_value = True
    return _fn_return_value

def Test_Write_Fuses_if_Wanted():
    #UT-------------------------------------
    Write_Fuses('\\\\.\\COM7', '16MHz, BOD 2.7V', Replace(PG.ThisWorkbook.Path, 'extras', 'examples\\80.Modules\\02.CharlieplexTiny\\'))
    # Write_Fuses "\\.\COM7", " 8MHz, BOD 2.7V", Replace(ThisWorkbook.Path, "extras", "examples\80.Modules\02.CharlieplexTiny\")

def Compile_and_Upload(SrcDir, InoName, CommandStr, ResFile):
    _fn_return_value = False
    Res = 0

    Start = Variant()

    ComPortColumn = M01.COMPrtT_COL
    # 05.06.20: Removed: ComPortColumn because it was always set to COMPrtT_COL
    #---------------------------------------------------------------------------------------------------------------------------
    Start = X02.Time
    if Dir(SrcDir + InoName) == '':
        X02.MsgBox(M09.Get_Language_Str('Fehler das Program ') + InoName + M09.Get_Language_Str(' ist nicht vorhanden in:') + vbCr + '  \'' + SrcDir + '\'', vbCritical, M09.Get_Language_Str('Fehler Ino-Programm nicht vorhanden'))
        return _fn_return_value
    X02.ChDrive(SrcDir)
    ChDir(SrcDir)
    # Change to the directory because the Arduino compiler doesn't like special characters like "ä" in the path
    #Res = M40.ShellAndWait(CommandStr, 0, vbNormalFocus, M40.PromptUser)
    ProgGen.global_controller.disconnect()
    ProgGen.dialog_parent.start_ARDUINO_program_cmd(CommandStr,arduino_type="Tiny") #*HL
    Res = M40.Success
    # No timeout to be able to study the results in case of an error
    _select59 = Res
    if (_select59 == M40.Success) or (_select59 == M40.Timeout):
        # No additional error message. They have been shown in the DOS box
        pass
    else:
        X02.MsgBox(M09.Get_Language_Str('Fehler ') + str(Res) + M09.Get_Language_Str(' beim starten des Arduino Programms \'') + CommandStr + '\'', vbCritical, M09.Get_Language_Str('Fehler beim starten des Arduino programms'))
    
    if Dir(ResFile) != '':
        X02.MsgBox(M09.Get_Language_Str('Es ist ein Fehler aufgetreten ;-(' + vbCr + vbCr + 'Kommunikationsprobleme erkennt man an dieser Meldung: ' + vbCr + '   avrdude: ser_open(): can\'t open device "\\\\.\\') + X02.Cells(M01.SH_VARS_ROW, ComPortColumn) + '":' + vbCr + M09.Get_Language_Str('   Das System kann die angegebene Datei nicht finden.' + vbCr + 'In diesem Fall müssen die Verbindungen überprüft und der Arduino durch einen neuen ersetzt werden.' + vbCr + vbCr + 'Wenn der Fehler nicht immer wieder auftritt, dann kann ein Screenshot des ' + 'vorangegangenen Bildschirms zusammen mit einer ausführlichen Beschreibung an ' + vbCr + '  https://forum.mobaledlib.de' + vbCr + 'geschickt werden.'), vbInformation, M09.Get_Language_Str('Fehler beim Hochladen des Programms'))
        M30.EndProg()
    else:
        Debug.Print('Compile and upload duration: ' + X02.Format(X02.Time() - Start(), 'hh:mm:ss'))
        M30.Show_Status_for_a_while(M09.Get_Language_Str('Programm erfolgreich hochgeladen. Kompilieren und Hochladen dauerte ') + X02.Format(X02.Time() - Start(), 'hh:mm:ss'), '00:00:30')
        _fn_return_value = True
    return _fn_return_value

def Get_COMPortStr(ComPortColumn):
    _fn_return_value = None
    #---------------------------------------------------------------
    M07a.Check_USB_Port_with_Dialog(ComPortColumn)
    #_fn_return_value = '\\\\.\\' + M07a.ComPortPage().Cells(M01.SH_VARS_ROW, ComPortColumn)
    _fn_return_value = M07a.ComPortPage().Cells(M01.SH_VARS_ROW, ComPortColumn)
    return _fn_return_value

def Check_If_Arduino_could_be_programmed_PatGen():
    _fn_return_value = False
    BuildOptions = String()

    ActSheet = String()

    OldUpdateing = Boolean()
    
    DeviceSignature = ""
    # 05.06.20:
    #------------------------------------------------------------------------
    OldUpdateing = X02.Application.ScreenUpdating
    X02.Application.ScreenUpdating = False
    PG.ThisWorkbook.Activate()
    # 08.08.20: Added to prevent problems if the user has switched to an other workbook while the options dialog is open
    ActSheet = X02.ActiveSheet.Name
    X02.Sheets(M01.MAIN_SH).Select()
    _fn_return_value ,BuildOptions,DeviceSignature = M08.Check_If_Arduino_could_be_programmed_and_set_Board_type(M01.COMPrtT_COL, M01.BuildOT_COL, BuildOptions,DeviceSignature)
    #Debug.Print('Check_If_Arduino_could_be_programmed_and_set_Board_type=' + Check_If_Arduino_could_be_programmed_PatGen() + ' BuildOptions=' + BuildOptions)
    # Debug
    X02.Sheets(ActSheet).Select()
    X02.Application.ScreenUpdating = OldUpdateing
    return _fn_return_value

def Compile_and_Upload_Prog_to_ATTiny(InoName, WorkDir, Mode, Mode2=VBMissingArgument):
    _fn_return_value = None
    ComPort = String()

    ResFile = String()

    CommandStr = String()

    ComPortColumn = M01.COMPrtT_COL
    # , ComPortColumn As Long
    # 05.06.20: Removed: ComPortColumn because it was always set to COMPrtT_COL
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # 07.08.20: Disabled

    if Check_If_Arduino_could_be_programmed_PatGen() == False:
        return _fn_return_value
    # 05.06.20:
    # 07.08.20: Moved down
    ComPort = Get_COMPortStr(ComPortColumn)
    X03.Sleep(1000)
    # 07.08.20:
    if Write_Fuses(ComPort, Mode, WorkDir) == False:
        return _fn_return_value
    # The fuses are always written because it's better not to ask the user to avoid confusion
    ResFile = 'Compile_and_Upload_to_ATTiny85_Result.txt'
    # ToDo: Prüfen ob das auch im Endgültigen speicherplatz der Library geht
    CommandStr = 'Compile_and_Upload_to_ATTiny85.cmd ' + ComPort
    if Compile_and_Upload(WorkDir, InoName, CommandStr, ResFile) == False:
        return _fn_return_value
    # 05.06.20: Removed: ComPortColumn because it was always set to COMPrtT_COL
    if Mode2 != '':
        X03.Sleep(2000)
        # 07.08.20:
        if Write_Fuses(ComPort, Mode2, WorkDir) == False:
            return _fn_return_value
        # The fuses are always written because it's better not to ask the user to avoid confusion
    _fn_return_value = True
    return _fn_return_value

def Write_LED_Polarity_h(SrcDir, LED_Polarity):
    _fn_return_value = None
    fp = Integer()

    Name = String()
    #------------------------------------------------------------------------------------------
    fp = FreeFile()
    Name = SrcDir + 'LED_Polarity.h'
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '// This file was generated by \'' + PG.ThisWorkbook.Name + '\'  ' + str(X02.Time()), '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#define LED_POLARITY_NORMAL ' + str(LED_Polarity), '\n')
    VBFiles.writeText(fp, '// 1 = Normal LED polarity (+ on the left side)', '\n')
    VBFiles.writeText(fp, '// 0 = invers LED polarity (- on the left side)', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    _fn_return_value = True
    return _fn_return_value
    X02.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Datei'))
    VBFiles.closeFile(fp)
    return _fn_return_value

def Define_LED_Polarity(SrcDir):
    _fn_return_value = None
    LED_Polarity = Integer()
    #----------------------------------------------------------------
    _select60 = X02.MsgBox(M09.Get_Language_Str('Der Bestückungsdruck der LEDs bei der ersten "TinyUniProg" Platine ' + 'vom 16.06.19 ist dummerweise falsch ;-(' + vbCr + vbCr + 'Soll das Programm auf einer neueren Platine verwendet werden bzw. ist der Plus Pol ' + 'der LEDs auf der linken Seite der Platine (=Abgeflachte Seite der LED rechts) ?' + vbCr + vbCr + 'Ja:  Plus Pol links, abgeflachte Seite rechts' + vbCr + 'Nein: Plus Pol rechts, abgeflachte Seite links'), vbQuestion + vbYesNoCancel, M09.Get_Language_Str('Einbaurichtung der LEDs?'))
    if (_select60 == vbYes):
        LED_Polarity = 1
    elif (_select60 == vbCancel):
        return _fn_return_value
    _fn_return_value = Write_LED_Polarity_h(SrcDir, LED_Polarity)
    return _fn_return_value

def Test_Define_LED_Polarity():
    #UT-----------------------------------
    Debug.Print(Define_LED_Polarity('C:\\Dat\\Märklin\\Arduino\\LEDs_Eisenbahn\\examples\\90.Tools\\02.Tiny_UniProg\\'))

def Prog_Tiny_UniProg():
    SrcDir = String()

    CommandStr = String()
    #-----------------------------
    if LCase(Left(PG.ThisWorkbook.Path, Len('extras'))) == 'extras':
        SrcDir = PG.ThisWorkbook.Path
    else:
        SrcDir = M01a.Get_SrcDirInLib()
    SrcDir = Replace(SrcDir, 'extras', 'examples\\90.Tools\\02.Tiny_UniProg\\', Compare= X01.vbTextCompare)
    if Define_LED_Polarity(SrcDir) == False:
        return
    # 05.06.20:
    if Check_If_Arduino_could_be_programmed_PatGen() == False:
        return
    # 05.06.20:
    
    #ECHO Programmierung des Arduino Uno als ISP für die Tiny_UniProg Platine
    #ECHO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #ECHO Mit diesem Programm wird das Programm zum Tiny_UniProg Programmiergeraet geschickt.
    #ECHO Dieser Vorgang muss nur einmal durchgefuehrt werden.
    #ECHO. 
    #IF NOT EXIST "%USERPROFILE%\Documents\Arduino\libraries\TimerOne\" (
    #ECHO **********************************
    #ECHO * Installing TimerOne library... *
    #ECHO **********************************
    #ECHO.
    #"%ProgDir%\Arduino\arduino_debug.exe" --install-library "TimerOne"
    #)
    #ECHO.
    #ECHO.
    #ECHO **********************************
    #ECHO * Compile and uplaod the program *
    #ECHO **********************************
    #ECHO.
    #CHCP 65001 >NUL    
    
    #"%ProgDir%\Arduino\arduino_debug.exe" "02.Tiny_UniProg.ino" ^
       #--upload ^
       #--port %ComPort% ^
       #--board arduino:avr:uno --pref programmer=arduino:arduinoisp ^    
    
    ARDUINO_exe = M08.Find_ArduinoExe()
    if ARDUINO_exe =="":
        return
    
    #CommandStr = 'Compile_and_Upload_to_Uno.cmd ' + Get_COMPortStr(M01.COMPrtT_COL)
    CommandStr = '"' + ARDUINO_exe + '" "02.Tiny_UniProg.ino" --upload --port ' + Get_COMPortStr(M01.COMPrtT_COL) + ' --board arduino:avr:uno --pref programmer=arduino:arduinoisp'
    
    
    Compile_and_Upload(SrcDir, '02.Tiny_UniProg.ino', CommandStr, 'Compile_and_Upload_to_Uno_Result.txt')
    # , COMPrtT_COL
    # 05.06.20: Removed: COMPrtT_COL

def Prog_Charlieplex():
    WorkDir = String()
    #----------------------------
    PG.ThisWorkbook.Activate()
    if LCase(Right(PG.ThisWorkbook.Path, Len('extras'))) == 'extras':
        WorkDir = PG.ThisWorkbook.Path
    else:
        WorkDir = M01a.Get_SrcDirInLib()
    WorkDir = Replace(WorkDir, 'extras', 'examples\\80.Modules\\02.CharlieplexTiny\\', Compare= X01.vbTextCompare)
    if Compile_and_Upload_Prog_to_ATTiny('02.CharlieplexTiny.ino', WorkDir, '16MHz, BOD 2.7V'):
        # COMPrtT_COL,
        # 05.06.20: Removed: COMPrtT_COL
        X02.MsgBox(M09.Get_Language_Str('Das "Betriebssystem" des Charlieplexing Moduls wurde erfolgreich programmiert.' + vbCr + 'Dieser Schritt ist nur ein mal pro Platine nötig.' + vbCr + 'Als nächstes muss die Konfiguration zum ATTiny geschickt werden. Das wird über den "Zum Modul schicken" ' + 'Knopf der entsprechenden Seite gemacht.'), vbInformation, M09.Get_Language_Str('Programm erfolgreich zum ATTiny übertragen'))

def Create_Inp_Prtx(DstDir, Correct_Pins):
    _fn_return_value = None
    fp = Integer()

    Name = String()
    #-------------------------------------------------------------------------------------
    fp = FreeFile()
    Name = DstDir + 'Inp_Prtx.h'
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '// This file was generated by \'' + PG.ThisWorkbook.Name + '\'  ' + str(X02.Time()), '\n')
    VBFiles.writeText(fp, '', '\n')
    if Correct_Pins:
        VBFiles.writeText(fp, '// Corrected input Pin list for servo platine ver. 1.0 with SMD WS2811', '\n')
        VBFiles.writeText(fp, 'const uint8_t Inp_Prtx[MAX_CHANNEL] = {4, 3, 5 }; // PBx number n', '\n')
    else:
        VBFiles.writeText(fp, '// Normal input Pin list for servo platine > Ver 1.0 or DIL WS2811', '\n')
        VBFiles.writeText(fp, 'const uint8_t Inp_Prtx[MAX_CHANNEL] = {3, 4, 5 }; // PBx number n', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    _fn_return_value = True
    return _fn_return_value
    X02.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der \'Create_Inp_Prtx\' Datei'))
    VBFiles.closeFile(fp)
    return _fn_return_value

def Prog_Servo():
    WorkDir = String()

    Correct_Pins = Boolean()
    #----------------------
    PG.ThisWorkbook.Activate()
    if LCase(Right(PG.ThisWorkbook.Path, Len('extras'))) == 'extras':
        WorkDir = PG.ThisWorkbook.Path
    else:
        WorkDir = M01a.Get_SrcDirInLib()
    WorkDir = Replace(WorkDir, 'extras', 'examples\\80.Modules\\01.ATTiny85_Servo\\', Compare= X01.vbTextCompare)
    _select61 = X02.MsgBox(M09.Get_Language_Str('Bei der Servo Platine der Version 1.0 hat sich ein Fehler bei der Pin Definition des SMD WS2811 eingeschlichen ;-(' + vbCr + 'Das führt dazu, das der rote und grüne Kanal vertauscht sind.' + vbCr + vbCr + 'Korrektur der SMD WS2811 Pins?' + vbCr + vbCr + 'Ja:' + vbCr + 'Wenn die Platine vom 14.6.19 ist UND ein SMD WS2811 bestückt wurde' + vbCr + 'Nein:' + vbCr + 'Bei einer neueren Platine oder wenn ein DIL WS2811 verwendet wird'), vbQuestion + vbYesNoCancel, M09.Get_Language_Str('Korrektur der SMD WS2811 Pins?'))
    if (_select61 == vbCancel):
        return
    elif (_select61 == vbYes):
        Correct_Pins = True
    elif (_select61 == vbNo):
        Correct_Pins = False
    if Create_Inp_Prtx(WorkDir, Correct_Pins) == False:
        return
    if Compile_and_Upload_Prog_to_ATTiny('01.ATTiny85_Servo.ino', WorkDir, '16MHz, BOD 2.7V', '16MHz, BOD 2.7V, RstAsIO'):
        # 05.06.20: Removed: COMPrtT_COL
        # 04.08.20: Old: " 8MHz, BOD 2.7V", " 8MHz, BOD 2.7V, RstAsIO"
        X02.MsgBox(M09.Get_Language_Str('Das "Betriebssystem" des Servo Moduls wurde erfolgreich programmiert.' + vbCr + 'Dieser Schritt ist nur ein mal pro Platine nötig.' + vbCr + 'Als nächstes sollten die Endpositionen und die Geschwindigkeiten eingestellt werden.' + vbCr + 'Das kann mit zwei verschiednen Programmen gemacht werden:' + vbCr + '- das Arduino Programm "01.Servo_Pos"' + vbCr + '- das "Farbtest" Programm von Harold (\'Prog_Generator\' Menü)"'), vbInformation, M09.Get_Language_Str('Programm erfolgreich zum ATTiny übertragen'))

def Prog_Servo_2(dm_servo_with_LED=False, hexfile_name="DM-TinyServo.hex", fusemode = '16MHz, BOD 2.7V, Eckhart'):
    WorkDir = String()

    #----------------------
    PG.ThisWorkbook.Activate()
    WorkDir = PG.ThisWorkbook.Path + "/hex-files"

    #WorkDir = Replace(WorkDir, 'extras', 'examples\\80.Modules\\04.ATTiny85_Servo2', Compare= X01.vbTextCompare)
    
    #hexfile_name =  "RailMail-TinyServo.hex"
    
    if Dir(WorkDir + "/"+ hexfile_name) == '':
        # ask for filename - makefile or hexfile_name
        
        filenameandpath = filedialog.askopenfilename(filetypes=[("hex-File","*.hex"), ("makefile","makefile")], initialdir=WorkDir)
        if not filenameandpath:
            return
        if not os.path.exists(filenameandpath):
            #print ('file does not exist')
            return        
        filepath,filename = os.path.split(filenameandpath) 
        WorkDir = filepath
        
        if filename.lower() == "makefile":
            # compile first
            X02.ChDrive(WorkDir)
            ChDir(WorkDir)
            ProgGen.dialog_parent.start_ARDUINO_program_cmd("make servo",arduino_type="Tiny")
            Res = M40.Success 
            hexfile_name =  "RailMail-TinyServo.hex"
        else:
            hexfile_name = filename
    if Dir(WorkDir + "/"+ hexfile_name) == '':
        return
    X02.ChDrive(WorkDir)
    ChDir(WorkDir)    
    
    ComPortColumn = M01.COMPrtT_COL
    # , ComPortColumn As Long
    # 05.06.20: Removed: ComPortColumn because it was always set to COMPrtT_COL
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # 07.08.20: Disabled

    if Check_If_Arduino_could_be_programmed_PatGen() == False:
        return
    # 05.06.20:
    # 07.08.20: Moved down
    ComPort = Get_COMPortStr(ComPortColumn)
    
    # fusemode = '16MHz, BOD 2.7V, Eckhart' - new parameter
    if Upload_HEX_to_ATTiny(ComPort, hexfile_name, WorkDir):
        # 05.06.20: Removed: COMPrtT_COL
        # 04.08.20: Old: " 8MHz, BOD 2.7V", " 8MHz, BOD 2.7V, RstAsIO"
        X03.Sleep(1000)
        if dm_servo_with_LED:
            fusemode = '16MHz, BOD 2.7V, Eckhart-LED'
        if Write_Fuses(ComPort, fusemode, WorkDir) == False:
            return
        X02.MsgBox(M09.Get_Language_Str('Das "Betriebssystem" des Servo Moduls wurde erfolgreich programmiert.' + vbCr + 'Dieser Schritt ist nur ein mal pro Platine nötig.' + vbCr + 'Als nächstes sollten die Endpositionen und die Geschwindigkeiten eingestellt werden.' + vbCr + 'Das kann mit zwei verschiednen Programmen gemacht werden:' + vbCr + '- das Arduino Programm "01.Servo_Pos"' + vbCr + '- das "Farbtest" Programm von Harold (\'Prog_Generator\' Menü)"'), vbInformation, M09.Get_Language_Str('Programm erfolgreich zum ATTiny übertragen'))
                     


#        -------------------------------------------------------------------------------------------
#        |     | CRC-4 nach ITU | ENTER-Bit | Command 0..7 | 2. Byte = Position | 3. Byte Pos fine |
#        -------------------------------------------------------------------------------------------
#        | Bit |        7 6 5 4 |         3 |        2 1 0 |    7 6 5 4 3 2 1 0 | 7 6 5 4 3 2 1 0  |
#        -------------------------------------------------------------------------------------------
#        |     |        0 0 0 0 |         0 |        0 0 0 |             unused |           unused | idle, nothing to do
#        -------------------------------------------------------------------------------------------
#        |     |        invalid |         X |        X X X |     not applicable |          not app | failure on WS2811 Bus
#        -------------------------------------------------------------------------------------------
#        |     |     valid (*1) |         X |        0 0 1 |           position | 7 6     pos fine | move between progt positions
#        -------------------------------------------------------------------------------------------
#        |     |     valid (*1) |         X |        0 0 1 |           position |     5   reserved | must be 0
#        -------------------------------------------------------------------------------------------
#        |     |     valid (*1) |         X |        0 0 1 |           position |  seq 4 3 2 1 tag | sequence tag number (*2)
#        -------------------------------------------------------------------------------------------
#        |     |     valid (*1) |         X |        0 0 1 |           position |        seq end 0 | end of sequence (*2)
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         0 |        0 1 0 | training positions | 7 6   train fine | trainig in standard PWM range 1-2ms (0..255/1023)
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         1 |        0 1 0 |  std prog position | 7 6    prog fine | memorize 1st and 2nd position (cycles with ENTER-Bit)
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         0 |        0 1 1 | training positions | 7 6   train fine | trainig in wide PWM range 0,5-2,5ms (0..255/1023)
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         1 |        0 1 1 | wide prog position | 7 6 wide pr fine | memorize 1st and 2nd position (cycles with ENTER-Bit)
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         0 |        1 0 0 |     prog max speed |       MAGIC 0x9A | prerequisite: memorize max speed
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         1 |        1 0 0 |     prog max speed |       MAGIC 0x9A | memorize max speed in max value-step per 20ms ( 0 = off, no limit)
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         0 |        1 0 0 |                  1 |       MAGIC 0x15 | prerequisite: toggle inverse
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         1 |        1 0 0 |                  1 |       MAGIC 0x15 | toggle inverse usage of 0.255 for position and memorize it
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         0 |        1 0 0 |                  1 |       MAGIC 0x87 | prerequisite: toggle LED ON/OFF
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         1 |        1 0 0 |                  1 |       MAGIC 0x87 | toggle LED ON/OFF blinking in regular WS2811 receive process
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         0 |        1 0 0 |  trim OSCCAL 0..18 |       MAGIC 0x9C | prerequisite: trim OSCCAL +0..+35
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         1 |        1 0 0 |  trim OSCCAL 0..18 |       MAGIC 0x9C | memorize custom OSCCAL (*3)
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         0 |        1 0 1 |         MAGIC 0xE9 |       MAGIC 0x8A | RESET prerequisite: servo factory defaults
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         1 |        1 0 1 |         MAGIC 0xE9 |       MAGIC 0x8A | RESET: load factory defaults for servo belonged to this channel
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         0 |        1 0 1 |         MAGIC 0x16 |       MAGIC 0x75 | RESET prerequisite: all factory defaults
#        ------------------------------------------------------------------------------------------
#        |     |          valid |         1 |        1 0 1 |         MAGIC 0x16 |       MAGIC 0x75 | RESET: load factory defaults for ALL servos
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         0 |        1 0 1 |         MAGIC 0x5A |       MAGIC 0x9E | RESET prerequisite: last position
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         1 |        1 0 1 |         MAGIC 0x5A |       MAGIC 0x9E | RESET: last position memory to none
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         X |        1 1 0 |           reserved |         reserved | reserved
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         0 |        1 1 1 |               0x01 |       MAGIC 0xC9 | ESCAPE prerequisite: enter bootloader
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         1 |        1 1 1 |               0x01 |       MAGIC 0xC9 | ESCAPE execute: enter bootloader
#        -------------------------------------------------------------------------------------------
#        |     |          valid |         X |        1 1 1 |           reserved |         reserved | other escapes (ffs)
#        -------------------------------------------------------------------------------------------


def Upload_firmware_direkt(hexfile_name="RailMail-TinyServo.blthex", AttinyAdress=None):
    print("Upload Firmware direkt:", hexfile_name, AttinyAdress)
    
    #Start Bootloader

    PG.ThisWorkbook.Activate()
    WorkDir = PG.ThisWorkbook.Path + "/hex-files"
    
    if Dir(WorkDir + "/"+ hexfile_name) == '':
        # ask for filename - makefile or hexfile_name
        
        filenameandpath = filedialog.askopenfilename(filetypes=[("hex-File","*.hex"), ("makefile","makefile")], initialdir=WorkDir)
        if not filenameandpath:
            return
        if not os.path.exists(filenameandpath):
            #print ('file does not exist')
            return        
        filepath,filename = os.path.split(filenameandpath) 
        WorkDir = filepath
        hexfile_name = filename

        if Dir(WorkDir + "/"+ hexfile_name) == '':
            return
        
    X02.ChDrive(WorkDir)
    ChDir(WorkDir)
    
    #Open the binary file in read mode
    with open(hexfile_name, 'rb') as binary_file:
        # Read one byte at a time
        
        data = binary_file.read()
            
        # Print each byte in hexadecimal format
        modulo = 0
        block_nr = 0
        block_delta = 0
        len_data = len(data)
        data_ptr = 0
        while true:
            # print('{:02x}'.format(data[i]), " ")
            if block_delta == 0:
                ledadress = AttinyAdress + 1
                print("Block-Nr:", block_nr)
            data_ptr = block_nr * 21 + block_delta
            byte1 = data[data_ptr]
            byte2 = data[data_ptr+1]
            byte3 = data[data_ptr+2]
            data_ptr += 3
            send_databytes_to_Arduino(self, ledadress, byte1, byte2, byte3)
            ledadress += 1
            block_delta += 3
            
            
               
                
        
        
        
    

def send_databytes_to_Arduino(self, ledadress, byte1, byte2, byte3):
    
    if self.controller.mobaledlib_version == 1:
        message = "#L" + '{:02x}'.format(ledadress) + " " + '{:02x}'.format(byte2) + " " + '{:02x}'.format(byte1) + " " + '{:02x}'.format(byte3) + " " + '{:02x}'.format(1) + "\n"
    else:
        message = "#L " + '{:02x}'.format(ledadress) + " " + '{:02x}'.format(byte2) + " " + '{:02x}'.format(byte1) + " " + '{:02x}'.format(byte3) + " " + '{:04x}'.format(1) + "\n"
    self.controller.send_to_ARDUINO(message)
    #time.sleep(0.2)



def send_commandbytes_to_Arduino(self, attinyadress, controlbyte, cmd_byte2, cmd_byte3):
    #servo_use_old_crc = int(self.controller.get_macroparam_val(self.tabClassName, "ServoCRCold"))
    if True: #controlValue != 1:
        #if servo_use_old_crc:
        #    newcontrolValue =  CalculateControlValuewithChecksum_old (controlValue, positionValueHigh, positionValueLow) 
        #else:
        newcontrolValue =  CalculateControlValuewithChecksum (controlbyte, cmd_byte2, cmd_byte3)
    else:
        newcontrolValue = 1
    if self.controller.mobaledlib_version == 1:
        message = "#L" + '{:02x}'.format(attinyadress) + " " + '{:02x}'.format(cmd_byte2) + " " + '{:02x}'.format(newcontrolValue) + " " + '{:02x}'.format(cmd_byte3) + " " + '{:02x}'.format(1) + "\n"
    else:
        message = "#L " + '{:02x}'.format(attinyadress) + " " + '{:02x}'.format(cmd_byte2) + " " + '{:02x}'.format(newcontrolValue) + " " + '{:02x}'.format(cmd_byte3) + " " + '{:04x}'.format(1) + "\n"
    self.controller.send_to_ARDUINO(message)
    #time.sleep(0.2)

    

def Upload_HEX_to_ATTiny(ComPort, Hexfilename, DstDir):
    
    if True: #not X02.checkplatform("Windows"):
        return Upload_HEX_to_ATTiny_Linux(ComPort, Hexfilename, DstDir)
        
    _fn_return_value = None
    ResFile = "Upload_Hex_result.txt"

    CommandStr = String()

    #Res = ShellAndWaitResult()
    
    #-------------------------------------------------------------------------------------------
    CommandStr = Create_upload_hex_Cmd_file(ResFile, Hexfilename, DstDir)
    if CommandStr != '':
        X02.ChDrive(CommandStr)
        ChDir(M30.FilePath(CommandStr))
        #Res = M40.ShellAndWait(CommandStr + ' ' + ComPort, 0, vbNormalFocus, PromptUser)
        ProgGen.global_controller.disconnect()
        ProgGen.dialog_parent.start_ARDUINO_program_cmd(CommandStr + ' ' + str(ComPort),arduino_type="Tiny") #*HL
        Res = M40.Success
        # No timeout to be able to study the results in case of an error
        _select58 = Res
        if (_select58 == M40.Success) or (_select58 == M40.Timeout):
            # No additional error message. They have been shown in the DOS box
            pass
        else:
            X02.MsgBox(M09.Get_Language_Str('Fehler ') + str(Res) + M09.Get_Language_Str(' beim starten des Arduino Programms \'') + CommandStr + '\'', vbCritical, M09.Get_Language_Str('Fehler beim starten des Arduino programms'))
        if Dir(ResFile) != '':
            X02.MsgBox(M09.Get_Language_Str('Es ist ein Fehler beim setzen der Fuses aufgetreten ;-(' + vbCr + vbCr + 'Falls die blaue \'Reset as IOPin\' LED am Tiny_UniProg leuchtet, dann muss ' + 'die rechte Taste (\'Cng Reset Pin\') am Tiny_UniProc für eine Sekunde gedückt werden. ' + 'Damit wird der Reset Pin wieder aktiviert.' + vbCr + 'Wenn die Taste länger als 3 Sekunden gehalten wird, dann wird der Pin zum Ein/Ausgang umprogrammiert.' + vbCr + 'Das erkennt man an der blauen LED. Dieser Modus wird z.B. bei der Servo Platine benötigt.' + vbCr + vbCr + 'Wenn der Fehler immer wieder auftritt, dann kann ein Screenshot des ' + 'vorangegangenen Bildschirms zusammen mit einer ausführlichen Beschreibung an ' + vbCr + '  https://forum.mobaledlib.de' + vbCr + 'geschickt werden.'), vbInformation, M09.Get_Language_Str('Fehler schreiben der Fuses'))
            return _fn_return_value
        _fn_return_value = True
    return _fn_return_value

def Create_upload_hex_Cmd_file(ResultName, hexfile_name, DstDir):
    _fn_return_value = None
    Avrdude = String()
    Avrdude_conf = String()
    fp = Integer()

    Name = String()
    #-----------------------------------------------------------------------------------------------------------
    if ResultName == '':
        ResultName = 'Upload_Hex_Result.txt'
    if Dir(ResultName) != '':
        Kill(ResultName)
    Avrdude = Find_Avrdude()
    if Avrdude == '':
        return _fn_return_value
    Avrdude_conf = Find_Avrdude_conf()
    if Avrdude_conf == '':
        return _fn_return_value

    fp = FreeFile()
    Name = DstDir + "/" + 'upload_hex.cmd'
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM This file was generated by \'' + PG.ThisWorkbook.Name + '\'  ' + str(X02.Time()), '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM Upload hex-file to  ATTiny', '\n')
    VBFiles.writeText(fp, 'REM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, 'REM   Hex-File:              ' + hexfile_name, '\n')
    VBFiles.writeText(fp, 'REM', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'REM Schwarz auf Ocker', '\n')
    VBFiles.writeText(fp, 'COLOR 60', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, Replace(M09.Get_Language_Str('ECHO Hochladen Hexfile fuer den ATTiny') + vbCr + 'ECHO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' + vbCr + M09.Get_Language_Str('ECHO Der ATTiny85 muss dazu in die Tiny_UniProg Platine gesteckt sein.' + vbCr + 'ECHO Dieser Vorgang muss nur ein mal gemacht werden. Danach wird nur noch die geaenderte' + vbCr + 'ECHO Konfiguration vom Pattern_Configuartor aus zum ATTiny geschickt.'), vbCr, vbCrLf), '\n')
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
    # 24.07.20: Removed chip erase: -e
    VBFiles.writeText(fp, '    -U flash:w:' + hexfile_name + ':i', '\n')
    VBFiles.writeText(fp, '', '\n')
    #Print #fp, "ECHO avrdude result: %ERRORLEVEL%"
    #Print #fp, "Pause"
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'IF ERRORLEVEL 1 (', '\n')
    # 07.08.20:
    VBFiles.writeText(fp, '    ECHO Error hochladen ;-(', '\n')
    VBFiles.writeText(fp, '    ECHO Starting second try', '\n')
    #VBFiles.writeText(fp, '    timeout /T 3 /nobreak', '\n')
    VBFiles.writeText(fp, '    "' + Avrdude + '" ^', '\n')
    VBFiles.writeText(fp, '        "-C' + Avrdude_conf + '"  ^', '\n')
    VBFiles.writeText(fp, '        -v -pattiny85 -cstk500v1  -P%ComPort% -b19200 ^', '\n')
    VBFiles.writeText(fp, '        -U flash:w:' + hexfile_name + ':i', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '   )', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'IF ERRORLEVEL 1 (', '\n')
    # 07.08.20:
    VBFiles.writeText(fp, '    ECHO Error setting the fuses ;-(((', '\n')
    VBFiles.writeText(fp, '    ECHO Starting third try', '\n')
    #VBFiles.writeText(fp, '    timeout /T 3 /nobreak', '\n')
    VBFiles.writeText(fp, '    "' + Avrdude + '" ^', '\n')
    VBFiles.writeText(fp, '        "-C' + Avrdude_conf + '"  ^', '\n')
    VBFiles.writeText(fp, '        -v -pattiny85 -cstk500v1 -P%ComPort% -b19200 ^', '\n')
    VBFiles.writeText(fp, '        -Uflash:w:' + hexfile_name + ':i', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '   )', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'IF ERRORLEVEL 1 (', '\n')
    VBFiles.writeText(fp, '   REM White on RED', '\n')
    VBFiles.writeText(fp, '   COLOR 4F', '\n')
    VBFiles.writeText(fp, '   ECHO Set_Fuses Result: %ERRORLEVEL% > "' + ResultName + '"', '\n')
    VBFiles.writeText(fp, '   ECHO   *********************************************', '\n')
    VBFiles.writeText(fp, '   ECHO  ' + M09.Get_Language_Str('* Da ist was schief gegangen ;-(            *') + '              ERRORLEVEL %ERRORLEVEL%', '\n')
    VBFiles.writeText(fp, '   ECHO   *********************************************', '\n')
    VBFiles.writeText(fp, '   Pause', '\n')
    VBFiles.writeText(fp, '   )', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    _fn_return_value = Name
    return _fn_return_value


def Create_upload_hex_Cmd_Linux(ResultName, hexfile_name, DstDir, ComPort):
    _fn_return_value = None
    Avrdude = String()
    Avrdude_conf = String()
        
    #-----------------------------------------------------------------------------------------------------------
    if ResultName == '':
        ResultName = 'Upload_Hex_Result.txt'
    if Dir(ResultName) != '':
        Kill(ResultName)
    Avrdude = Find_Avrdude()
    if Avrdude == '':
        return _fn_return_value
    Avrdude_conf = Find_Avrdude_conf()
    if Avrdude_conf == '':
        return _fn_return_value    
    
    CommandStr1 = '"' + Avrdude + '" -C"' + Avrdude_conf + '" -v -pattiny85 -cstk500v1 -P'+ComPort+' -b19200  -U flash:w:' + hexfile_name + ':i\n'
        
    return CommandStr1
    
def Upload_HEX_to_ATTiny_Linux(ComPort, Hexfilename, DstDir):
    Failed = None
    ResFile = "Upload_Hex_result.txt"
    
    #-------------------------------------------------------------------------------------------
    command = Create_upload_hex_Cmd_Linux(ResFile, Hexfilename, DstDir, ComPort)
    
    ProgGen.global_controller.disconnect()
    arduinoMonitorPage=PG.global_controller.getFramebyName ("ARDUINOMonitorPage")
    arduinoMonitorPage.add_text_to_textwindow("\n*********** Upload hex-file to  ATTiny ***************************\n",highlight="Error")
    arduinoMonitorPage.add_text_to_textwindow("\n  Hex-File:              " + Hexfilename, "\n")
    Res = ProgGen.dialog_parent.start_ARDUINO_program_cmd(command,arduino_type="Tiny") #*HL        
    #Res = M40.Success
        
    if (Res == M40.Success) or (Res == M40.Timeout) or (Res == M40.UserBreak):
        pass
    else:
        Failed = True
    
    if Dir(ResFile) != '' or Failed:
        arduinoMonitorPage=PG.global_controller.getFramebyName ("ARDUINOMonitorPage")
        arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")
        Failed = True
    
    if Failed:
        P01.MsgBox(M09.Get_Language_Str('Es ist ein Fehler aufgetreten ;-(' + vbCr + vbCr + 'Zur Fehlersuche kann man die letzten Änderungen wieder rückgängig machen und es noch mal versuchen. ' + vbCr + vbCr + 'Kommunikationsprobleme erkennt man an dieser Meldung: ' + vbCr + '   avrdude: ser_open(): can\'t open device "\\\\.\\') + P01.Cells(M02.SH_VARS_ROW, ComPortColumn) + '":' + vbCr + M09.Get_Language_Str('   Das System kann die angegebene Datei nicht finden.' + vbCr + 'In diesem Fall müssen die Verbindungen überprüft und der Arduino durch einen neuen ersetzt werden.' + vbCr + vbCr + 'Der Fehler kann auch auftreten wenn der DCC/LNet/Selextrix Arduino noch nicht programmiert wurde.' + vbCr + 'Am besten man steckt den rechten Arduino erst dann ein wenn er benötigt wird.' + vbCr + vbCr + 'Wenn der Fehler nicht zu finden ist und immer wieder auftritt, dann kann ein Screenshot des ' + 'vorangegangenen Bildschirms (Nach oben scrollen so dass die erste Meldung nach dem Arduino Bild zu sehen ist) ' + 'zusammen mit dem Excel Programm und einer ausführlichen Beschreibung an ' + vbCr + '  https://forum.mobaledlib.de' + vbCr + 'geschickt werden.'), vbInformation, M09.Get_Language_Str('Fehler beim Hochladen des Programms'))
        M30.EndProg()
        return False
    
    return Failed



def Prog_ServoMP3():
    WorkDir = String()

    Correct_Pins = Boolean()
    #----------------------
    PG.ThisWorkbook.Activate()
    if LCase(Right(PG.ThisWorkbook.Path, Len('extras'))) == 'extras':
        WorkDir = PG.ThisWorkbook.Path
    else:
        WorkDir = M01a.Get_SrcDirInLib()
    WorkDir = Replace(WorkDir, 'extras', 'examples\\80.Modules\\03.ATTiny85_Sound\\', Compare= X01.vbTextCompare)
    _select62 = X02.MsgBox(M09.Get_Language_Str('Bei der Servo Platine der Version 1.0 hat sich ein Fehler bei der Pin Definition des SMD WS2811 eingeschlichen ;-(' + vbCr + 'Das führt dazu, das der rote und grüne Kanal vertauscht sind.' + vbCr + vbCr + 'Korrektur der SMD WS2811 Pins?' + vbCr + vbCr + 'Ja:' + vbCr + 'Wenn die Platine vom 14.6.19 ist UND ein SMD WS2811 bestückt wurde' + vbCr + 'Nein:' + vbCr + 'Bei einer neueren Platine oder wenn ein DIL WS2811 verwendet wird'), vbQuestion + vbYesNoCancel, M09.Get_Language_Str('Korrektur der SMD WS2811 Pins?'))
    if (_select62 == vbCancel):
        return
    elif (_select62 == vbYes):
        Correct_Pins = True
    elif (_select62 == vbNo):
        Correct_Pins = False
    if Create_Inp_Prtx(WorkDir, Correct_Pins) == False:
        return
    if Compile_and_Upload_Prog_to_ATTiny('03.ATTiny85_Sound.ino', WorkDir, '16MHz, BOD 2.7V', '16MHz, BOD 2.7V, RstAsIO'):
        # 05.06.20: Removed: COMPrtT_COL
        # 04.08.20: Old: " 8MHz, BOD 2.7V", " 8MHz, BOD 2.7V, RstAsIO"
        X02.MsgBox(M09.Get_Language_Str('Das "Betriebssystem" des Servo Moduls wurde erfolgreich zur Anbindung von MP3-Modulen programmiert.' + vbCr + 'Dieser Schritt ist nur ein mal pro Platine nötig.' + vbCr + 'Als nächstes sollten angeschlossenen Soundmodule konfiguriert werden (siehe Anleitung' + vbCr + 'im Verzeichnis \'' + WorkDir + '\''), vbInformation, M09.Get_Language_Str('Programm erfolgreich zum ATTiny übertragen'))

# VB2PY (UntranslatedCode) Option Explicit
