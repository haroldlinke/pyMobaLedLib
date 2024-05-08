# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
# * Author: Harold Linke
# * Date: January 1st, 2020
# * Copyright: Harold Linke 2020
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 10.03.2020 - Harold Linke - first release
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

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

"""----------------------------------------------------------------
 Module made by Misha 21-4-2020, Bug 'Brightness' fixed 3-5-2020 by Misha.
 Updated 26-5-2020 by Misha. Now compatible with Multiplexer 0.99a.

 This code is used by the Multiplexer macros and needs integration in the MobaLedLib Program Generator.

----------------------------------------------------------------

 ToDo:
 - Support the LED_Channel
 - Control the Multiplexer by DCC/Switch/Variable
   - Change the displayed pattern
   - Enable/Disable the whole multiplexer
# VB2PY (CheckDirective) VB directive took path 1 on VBA7

"""

Version = 'v0.99'
Multiplexer_INI_FILE_NAME = 'Multiplexer.ini'
MltPlxr = int()
__FirstOneInGroup = Boolean()

def Get_Multiplexer_Group(Res, Description, Row):
    _ret = ""
    LStr = String()

    RStr = String()

    p_str = String()

    Parts = vbObjectInitialize(objtype=String)

    LedsInGroup = Integer()

    Groups = Integer()

    Cmd = String()

    i = Integer()

    LEDCnt = Integer()

    Options = Integer()
    #----------------------------------------------------------------
    #   Added by Misha 29-03-2020
    #   Needed for multipling group of Leds with 'Multiplexer' commands
    # Multiplexer_<Value>(#LED, #InCh, #LocInCh, Brightness, Groups, Options, RndMinTime, RndMaxTime, #CtrMode, ControlNr, NumOfLEDs)
    # Param:                0      1      2         3           4       5          6           7          8         9        10
    LStr = Left(Res, InStr(Res, ')'))
    RStr = Mid(Res, InStr(Res, ')') + 1)
    Cmd = Left(Res, InStr(Res, '('))
    Parts = Split(Mid(LStr, Len(Cmd) + 1, Len(Res) - Len(RStr) - 1), ',')
    LEDCnt = val(Parts(0))
    Groups = val(Parts(4))
    Options = val(Parts(5))
    LedsInGroup = val(__ReadIniFileString('Multiplexer_' + Cells(Row, Descrip_Col).Value, 'Number_Of_LEDs'))
    # Added: "val" to prevent crash
    __FirstOneInGroup = True
    for i in vbForRange(1, Groups):
        p_str = p_str + __Create_Multiplexer(Trim(LStr), LEDCnt +  ( i - 1 )  * LedsInGroup, Description, Row)
        __FirstOneInGroup = False
    _ret = p_str
    return _ret

def __Create_Multiplexer(Res, LEDCnt, Description, Row):
    _ret = ""
    ProgDir = Variant()

    Map = String()

    FileName = Variant()

    IniFileName = String()

    Nr = Integer()

    LStr = String()

    RStr = String()

    Cmd = String()

    RdCmd = String()

    Parts = vbObjectInitialize(objtype=String)

    MltplxrOptions = Integer()

    binOptions = String()

    ParOpt = Integer()

    DstVar = String()

    InCh = String()

    LocInCh = String()

    Brightness = Integer()

    RndMinTime = int()

    RndMaxTime = int()

    Tmp = String()

    ReadStr = String()

    RandomDescription = String()

    OptionName = Variant()

    OptionPattern = Variant()

    RestPartsFrom6 = String()

    PartsCount = Variant()

    PartNr = Integer()

    OptionNr = Integer()
    #---------------------------------------------------------------------------------------------------------------
    #  Dim INCH_RND As String, ReadLines() As String, Line As Variant, LastLine As Long, FoundCmd As Boolean
    #    IniFileName = Get_MyExampleDir() & "\" & Multiplexer_INI_FILE_NAME
    Map = Environ(M02.Env_USERPROFILE) + '\\Documents\\' + 'MyPattern_Config_Examples'
    IniFileName = Map + '\\' + Multiplexer_INI_FILE_NAME
    ProgDir = IniFileName
    if Dir(ProgDir, vbDirectory) == '':
        MsgBox(Get_Language_Str('Fehler das Verzeichnis existiert nicht:') + vbCr + '  \'' + ProgDir + '\'', vbCritical, Get_Language_Str('Multiplexer Verzeichnis nicht vorhanden'))
        return _ret
    if not Dir(IniFileName) != '':
        MsgBox(Get_Language_Str('Fehler die Datei existiert nicht:') + vbCr + '  \'' + IniFileName + '\'', vbCritical, Get_Language_Str('Multiplexer Datei nicht gefunden!'))
        return _ret
    LStr = Left(Res, InStr(Res, ')'))
    RStr = Mid(Res, InStr(Res, ')') + 1)
    Cmd = Left(Res, InStr(Res, '(') - 1)
    Parts = Split(Mid(Left(LStr, InStr(Res, ')') - 1), Len(Cmd) + 1, Len(Res) - Len(RStr) - 1), ',')
    # Multiplexer_<Value>(#LED, #InCh, #LocInCh, Brightness, Groups, Options, RndMinTime, RndMaxTime, CtrMode, ControlNr, NumOfLEDs)
    #                Param: 0      1      2         3           4       5          6           7         8         9        10
    InCh = Parts(1)
    # Input Channel
    if InCh == ' [Multiplexer]':
        InCh = ' SI_1'
        # 10.02.21: Misha
    LocInCh = Parts(2)
    # local Input Channel
    Brightness = val(Trim(Parts(3)))
    MltplxrOptions = val(Trim(Parts(5)))
    # Which patterns should be seen on the LED display of the Multiplexer command. Decimal number represents a binary value.
    ParOpt = __Count_Ones(val(Parts(5)))
    # Number off 1's (binary number off patterns to display) needed to add the correct number of INCH parameters to counter.
    RndMinTime = val(Trim(Parts(6)))
    # Minimum Time for the Random Function to switch to next pattern
    RndMaxTime = val(Trim(Parts(7)))
    # Maximum Time for the Random Function to switch to next pattern
    if MltplxrOptions <= 0:
        # If there are zero Options then no patterns can be displayed.
        _ret = '  // No Patterns for command : ' + Res + vbCrLf
        return _ret
    # Syntax for reading INI file
    # Section = "Test_Multiplexer_RGB_Ext4"              ' Cmd
    # KeyName = "Option 1 Name"                     ' Variable Name
    # Value   = ReadIniFileString(Section, KeyName) ' Variable Value
    #---------------------------------------------------------------------------------------------------------------
    # Create Multiplexer Line with Random() and Counter()
    #---------------------------------------------------------------------------------------------------------------
    Description = __ReadIniFileString('Multiplexer_' + Cells(Row, Descrip_Col).Value, 'Description')
    ReadStr = ReadStr + vbCrLf + __Add_Description('  // ' + Res, '- Excel row ' + Row + ' - ' + Description, True)
    # Comment about Multiplexer
    if __FirstOneInGroup:
        # Random( DstVar, InCh, RandMode, MinTime, MaxTime, MinOn, MaxOn)
        # Parts(x)  0       1      2         3        4       5      6
        #        DstVar = "MltPlxr" & Int((999 - 300 + 1) * Rnd + 300)                                        ' Random Number for DstVar between 300-999
        # Random Number for DstVar between 300-999
        DstVar = 'MltPlxr' + MltPlxr
        MltPlxr = MltPlxr + 1
        Tmp = Add_Variable_to_DstVar_List(DstVar)
        RandomDescription = 'Trigger for Counter in ' + Cmd + ' with Destination Variable : ' + DstVar
        #        ReadStr = ReadStr & Add_Description("  Random(" & DstVar & ", SI_1, RF_SEQ," & Parts(6) & "," & Parts(7) & ", 5 Sec, 5 Sec)", RandomDescription, True)
        ReadStr = ReadStr + __Add_Description('  Random(' + DstVar + ',' + InCh + ', RF_SEQ,' + Parts(6) + ',' + Parts(7) + ', 5 Sec, 5 Sec)', RandomDescription, True)
        # 10.02.21: Misha
        # Counter(CtrMode, InCh, Enable, TimeOut, ...)
        # Parts(x)  0        1      2       3      4
        # Counter(CF_ROTATE|CF_SKIP0, #INCH_RND, SI_1, 0 Sek, #LOC_INCH)     Opties: CF_ROTATE|CF_SKIP0 and CF_RANDOM|CF_SKIP0
        ReadStr = ReadStr + __Add_Description('  Counter(' + Trim(Parts(8)) + ',' + DstVar + ',' + InCh + ', 0 Sek' + __Options_INCH(LocInCh, ParOpt) + ')', RandomDescription, False)
        # 10.02.21: Misha: Using InCh instead og SI_1
        # How to implement the DCC InCh ?????       !!!!! 31-3-2020 Hardi HELP !!!!!
        #        ReadStr = ReadStr & Add_Description("  Counter(" & Trim(Parts(8)) & "," & "INCH_DCC_22_GREEN" & ", SI_1, 0 Sek" & Options_INCH(LocInCh, ParOpt) & ")", RandomDescription, False)
    #---------------------------------------------------------------------------------------------------------------
    # Create Pattern Lines
    #---------------------------------------------------------------------------------------------------------------
    # PatternT(x)(Start LED, Brightness Level (bits), InCh, Number Output Channels, Min Brightness, Max Brightness, SwitchMode, CtrMode, < Patternconfig >)
    # Parts(y)        0               1                 2             3                   4               5             6          7          8 ...>
    # XPatternT1(9,4,LOC_INCH0+0,12,0,128,0,PM_NORMAL,1 sec,0,0,0)   /* 0_Pattern_to_stop_Multiplexer (pc)      ' 10.02.21: Misha: New block                                                                                                                                                    */
    OptionName = '0_Pattern_to_stop_Multiplexer (pc)'
    OptionPattern = 'XPatternT1(#LED,4,LOC_INCH0+0,12,0,128,0,PM_NORMAL,1 sec,0,0,0)'
    RdCmd = Left(OptionPattern, InStr(OptionPattern, '('))
    Parts = Split(Mid(OptionPattern, InStr(OptionPattern, '(') + 1, Len(OptionPattern)), ',')
    PartsCount = UBound(Parts())
    RestPartsFrom6 = ''
    for PartNr in vbForRange(6, PartsCount):
        RestPartsFrom6 = RestPartsFrom6 + Parts(PartNr)
        if PartNr < PartsCount:
            RestPartsFrom6 = RestPartsFrom6 + ','
    ReadStr = ReadStr + __Add_Description('  /* ' + OptionName + ' */ ', Description, False)
    ReadStr = ReadStr + __Add_Description(( '  ' + RdCmd + LEDCnt + ',' + Parts(1) + ',' + LocInCh + '+' + OptionNr + ',' + Parts(3) + ',' + Parts(4) + ',' + Brightness + ',' + RestPartsFrom6 ), Description, False)
    OptionNr = OptionNr + 1
    for Nr in vbForRange(1, 8):
        OptionName = __ReadIniFileString('Multiplexer_' + Cells(Row, Descrip_Col).Value, 'Option ' + Nr + ' Name')
        OptionPattern = __ReadIniFileString('Multiplexer_' + Cells(Row, Descrip_Col).Value, 'Option ' + Nr + ' Pattern')
        RdCmd = Left(OptionPattern, InStr(OptionPattern, '('))
        Parts = Split(Mid(OptionPattern, InStr(OptionPattern, '(') + 1, Len(OptionPattern)), ',')
        PartsCount = UBound(Parts())
        RestPartsFrom6 = ''
        for PartNr in vbForRange(6, PartsCount):
            RestPartsFrom6 = RestPartsFrom6 + Parts(PartNr)
            if PartNr < PartsCount:
                RestPartsFrom6 = RestPartsFrom6 + ','
        binOptions = __DecToBin(MltplxrOptions)
        if Right(binOptions, 1) == 1:
            # LSB = 1
            ReadStr = ReadStr + __Add_Description('  /* Option ' + Nr + ' - ' + OptionName + ' */ ', Description, False)
            ReadStr = ReadStr + __Add_Description(( '  ' + RdCmd + LEDCnt + ',' + Parts(1) + ',' + LocInCh + '+' + OptionNr + ',' + Parts(3) + ',' + Parts(4) + ',' + Brightness + ',' + RestPartsFrom6 ), Description, False)
            OptionNr = OptionNr + 1
        else:
            ReadStr = ReadStr + __Add_Description('  /* Option ' + Nr + ' - ' + OptionName + ' */ ', Description, False)
            ReadStr = ReadStr + __Add_Description('  /* Option ' + Nr + ' - NOT selected! */ ', Description, False)
        MltplxrOptions = Application.WorksheetFunction.Bitrshift(MltplxrOptions, 1)
        # Shift to right for next bit (next Multiplexer option)
    _ret = ReadStr
    return _ret

def __Add_Description(Cmd, Description, AddDescription):
    _ret = ""
    #--------------------------------------------------------------------------------------------
    if AddDescription:
        # The description is only added to the first line
        Cmd = AddSpaceToLen(Cmd, 109) + ' /* ' + Description
    elif Description != '':
        Cmd = AddSpaceToLen(Cmd, 109) + ' /*     "'
    Cmd = AddSpaceToLen(Cmd, 300) + ' */'
    _ret = Cmd + vbCr
    return _ret

def __Count_Ones(Waarde):
    _ret = 0
    t = Integer()

    binOptions = String()

    Count = Integer()
    #--------------------------------------------------------------------------------------------
    for t in vbForRange(1, 8):
        binOptions = __DecToBin(Waarde)
        #        Debug.Print Waarde, " / ", binOptions
        if Right(binOptions, 1) == 1:
            # LSB = 1
            Count = Count + 1
        Waarde = Application.WorksheetFunction.Bitrshift(Waarde, 1)
    _ret = Count
    #    Debug.Print "Count_Ones    = ", Count
    return _ret

def __Test_Count_Ones():
    Options = Integer()

    binOptions = String()

    Count = Integer()
    #--------------------------------------------------------------------------------------------
    Options = 225
    binOptions = __DecToBin(Options)
    Debug.Print('Options       = ', Options)
    Debug.Print('binOptions    = ', binOptions)
    Count = __Count_Ones(Options)
    #    Debug.Print "Count         = ", Count

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DecimalIn - ByVal 
def __DecToBin(DecimalIn):
    _ret = 0
    #--------------------------------------------------------------------------------------------
    # The DecimalIn argument is limited to 79228162514264337593543950245
    # (approximately 96-bits) - large numerical values must be entered
    # as a String value to prevent conversion to scientific notation.
    _ret = ''
    DecimalIn = CDec(DecimalIn)
    while DecimalIn != 0:
        _ret = Trim(Str(DecimalIn - 2 * Int(DecimalIn / 2))) + __DecToBin()
        DecimalIn = Int(DecimalIn / 2)
    return _ret

def __Options_INCH(InCh, Options):
    _ret = ""
    i = Integer()

    p_str = String()
    #--------------------------------------------------------------------------------------------
    #    For i = 0 To Options - 1
    for i in vbForRange(0, Options):
        # 10.02.21: 20201028 Misha. Change for adding extra Pattern (Zero position) to hold the Multiplexer.
        p_str = p_str + ',' +  ( InCh + '+' + CStr(i) )
    _ret = p_str
    #    Debug.Print "Options_INCH = ", p_str
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Res - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: LEDs - ByRef 
def Special_Multiplexer_Ext(Res, LEDs):
    _ret = ""
    Parts = Variant()

    Param = Variant()

    Ret = String()

    Cmd = String()

    LedsInGroup = Integer()

    LedType = String()

    Temp = Integer()
    #--------------------------------------------------------------------------------------------
    #   Added by Misha 2020-3-29
    #   Calculate number of used LEDs for the Multiplexer command
    # Multiplexer_<Value>(#LED, #InCh, #LocInCh, Brightness, Groups, Options, RndMinTime, RndMaxTime, CtrMode, ControlNr, NumOfLEDs)
    #                Param: 0      1      2         3           4       5          6           7         8         9        10
    Parts = Split(Replace(Res, ')', ''), '(')
    Param = Split(Parts(1), ',')
    #    Param = Split(Parts(1), " ")                                           ' 10.02.21: Misha
    # 10.02.21: Misha
    Cmd = Left(Res, InStr(Res, '('))
    Ret = Cmd + Trim(Param(0)) + ', ' + Trim(Param(1)) + ', ' + Trim(Param(2)) + ', ' + Trim(Param(3)) + ', ' + Trim(Param(4)) + ', ' + Trim(Param(5)) + ', ' + Trim(Param(6)) + ', ' + Trim(Param(7)) + ', ' + Trim(Param(8)) + ', ' + Trim(Param(9)) + ', ' + Trim(Param(10)) + ')'
    _ret = Ret
    if Cells(ActiveCell.Row, DCC_or_CAN_Add_Col).Value == '':
        P01.CellDict[ActiveCell.Row, DCC_or_CAN_Add_Col].Value = '[Multiplexer]'
    LedsInGroup = val(__ReadIniFileString('Multiplexer_' + Cells(ActiveCell.Row, Descrip_Col).Value, 'Number_Of_LEDs'))
    # 14.06.20: Added "val" to prevent crash
    # 10.02.21: 20201025 Misha. Assingning the right number of LEDs for Single and RGB LEDs.
    LedType = __ReadIniFileString('Multiplexer_' + Cells(ActiveCell.Row, Descrip_Col).Value, 'LED_Type')
    if LedType == 'Single LEDs':
        # LedType = "Single LEDs"
        LEDs = 'C1-' + Trim(Param(4)) * LedsInGroup
        #   Calculate number of used Single LEDs for this command
    else:
        # LedType = "RGB LEDs"
        LEDs = Trim(Param(4)) * LedsInGroup
        #   Calculate number of used RGB LEDs for this command
    return _ret, LEDs #*HL ByRef

def LedCount(Cmd):
    _ret = ""
    OldSheet = X02.Worksheet

    SelRow = int()

    Row = int()
    #--------------------------------------------------------------------------------------------
    #   Added by Misha 2020-3-29
    #   Get number of LEDs used in this Multiplexer command
    OldSheet = P01.ActiveSheet
    ThisWorkbook.Worksheets(LIBMACROS_SH).Activate()
    Row = 3
    r = ThisWorkbook.Sheets(LIBMACROS_SH).Range(ThisWorkbook.Sheets(LIBMACROS_SH).Cells(Row, 1), ThisWorkbook.Sheets(LIBMACROS_SH).Cells(ActiveCell.SpecialCells(xlLastCell).Row, 13))
    f = r.Find(What= Cmd, after= r.Cells(1, 1), LookIn= xlValues, LookAt= xlPart, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= False, SearchFormat= False)
    if f is None:
        MsgBox(Get_Language_Str('Fehler: Die Spalte \'') + Cmd + Get_Language_Str('\' wurde nicht im Sheet \'') + P01.ActiveSheet.Name + Get_Language_Str('\' gefunden!' + vbCr + vbCr + 'Die Spaltennamen dürfen nicht verändert werden'), vbCritical, Get_Language_Str('Fehler Spaltenname nicht gefunden'))
        EndProg()
    else:
        SelRow = f.Row
    _ret = val(ThisWorkbook.Sheets(LIBMACROS_SH).Cells(SelRow, SM_SngLEDCOL))
    OldSheet.Activate()
    return _ret

def IniFileName():
    _ret = ""
    Dir = String()
    #--------------------------------------------------------------------------------------------
    #    IniFileName = ThisWorkbook.Path & "\" & Multiplexer_DIR & "\Multiplexer.ini"
    Dir = Environ(M02.Env_USERPROFILE) + '/Documents/' + 'MyPattern_Config_Examples'
    _ret = Dir + '/' + Multiplexer_INI_FILE_NAME
    return _ret

def __Test_ReadIniFileString():
    Value = Variant()

    Section = Variant()

    KeyName = String()
    #--------------------------------------------------------------------------------------------
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Description'
    Value = __ReadIniFileString(Section, KeyName)
    Debug.Print(Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 1 Name'
    Value = __ReadIniFileString(Section, KeyName)
    Debug.Print(Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 7 Pattern'
    Value = __ReadIniFileString(Section, KeyName)
    Debug.Print(Value)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Section - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyName - ByVal 
def ReadIniFileString(Section, KeyName):
    _ret = ""
    iNoOfCharInIni = int()

    sIniString = Variant()

    sProfileString = String()

    Worked = int()

    RetStr = FixedString(1500)

    StrSize = int()
    #--------------------------------------------------------------------------------------------
    iNoOfCharInIni = 0
    sIniString = ''
    if Section == '' or KeyName == '':
        MsgBox('Section Or Key To Read Not Specified !!!', vbExclamation, 'INI')
    else:
        sProfileString = ''
        RetStr = Space(1500)
        StrSize = Len(RetStr)
        Worked = GetPrivateProfileString(Section, KeyName, '', RetStr, StrSize, IniFileName())
        if Worked:
            iNoOfCharInIni = Worked
            sIniString = Left(RetStr, Worked)
    _ret = sIniString
    return _ret

def __Test_WriteIniFileString():
    Test = Variant()

    Section = Variant()

    KeyName = Variant()

    Value = String()
    #--------------------------------------------------------------------------------------------
    Section = 'Multiplexer_Macro'
    KeyName = 'INI File Production Date'
    Value = Now()
    Test = __WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Macro Syntax'
    Value = 'Multiplexer_RGB_Ext4(#LED, #InCh, #LocInCh, Brightness, Groups4, #Options, RndMinTime, RndMaxTime, #CtrMode)'
    Test = __WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 1 Name'
    Value = 'RGB_Multiplexer_3_4_Running_Blue (pc)'
    Test = __WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 2 Pattern'
    Value = 'PatternT2(LED,4,#LOC_INCH+1,12,0,Brightness,0,PM_NORMAL,0.1 sec,0.1 sec,0,0,0,195,48,12)'
    Test = __WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 3 Pattern'
    Value = 'PatternT1(LED,4,#LOC_INCH+2,12,0,Brightness,0,PM_NORMAL,100 ms,0,0,48,0,192,0,0,3,0,12,0,0)'
    Test = __WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 4 Pattern'
    Value = 'PatternT1(LED,4,#LOC_INCH+3,12,0,Brightness,0,PM_NORMAL,100 ms,0,240,255,255,15,0)'
    Test = __WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 5 Pattern'
    Value = 'To be filled!'
    Test = __WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 6 Pattern'
    Value = 'To be filled!'
    Test = __WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 7 Pattern'
    Value = 'PatternT1(LED,8,#LOC_INCH+6,24,0,Brightness,0,PM_PINGPONG,108 ms,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,0,0,0,0,0,0,0,112,224,0,0,0,0,0,0,56,112,224,0,0,0,0,0,28,56,112,224,0,0,0,0,14,28,56,112,224,0,0,0,7,14,28,56,112,224,0,128,3,7,14,28,56,112,224,192,129,3,7,14,28,56,112,224,192,129,3,7,14,28,56,112,0,192,129,3,7,14,28,56,0,0,192,129,3,7,14,28,0,0,0,192,129,3,7,14,0,0,0,0,192,129,3,7,0,0,0,0,0,192,129,3,0,0,0,0,0,0,192,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)'
    Test = __WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 8 Pattern'
    Value = 'To be filled!'
    Test = __WriteIniFileString(Section, KeyName, Value)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Section - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Wstr - ByVal 
def __WriteIniFileString(Section, KeyName, Wstr):
    _ret = ""
    iNoOfCharInIni = Variant()

    Worked = int()

    sIniString = String()
    #--------------------------------------------------------------------------------------------
    iNoOfCharInIni = 0
    sIniString = ''
    if Section == '' or KeyName == '':
        MsgBox('Section Or Key To Write Not Specified !!!', vbExclamation, 'INI')
    else:
        Worked = WritePrivateProfileString(Section, KeyName, Wstr, IniFileName())
        if Worked:
            iNoOfCharInIni = Worked
            sIniString = Wstr
        _ret = sIniString
    return _ret

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetPrivateProfileString Lib "kernel32" Alias "GetPrivateProfileStringA" (ByVal lpApplicationName As String, ByVal lpKeyName As Any, ByVal lpDefault As String, ByVal lpReturnedString As String, ByVal nSize As Long, ByVal lpFileName As String) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function WritePrivateProfileString Lib "kernel32" Alias "WritePrivateProfileStringA" (ByVal lpApplicationName As String, ByVal lpKeyName As Any, ByVal lpString As Any, ByVal lpFileName As String) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetPrivateProfileInt Lib "kernel32" Alias "GetPrivateProfileIntA" (ByVal lpApplicationName As String, ByVal lpKeyName As String, ByVal nDefault As Long, ByVal lpFileName As String) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetPrivateProfileSection Lib "kernel32" Alias "GetPrivateProfileSectionA" (ByVal lpAppName As String, ByVal lpReturnedString As String, ByVal nSize As Long, ByVal lpFileName As String) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetPrivateProfileSectionNames Lib "kernel32" Alias "GetPrivateProfileSectionNamesA" (ByVal lpSectionNames As String, ByVal nSize As Long, ByVal lpFileName As String) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function WritePrivateProfileSection Lib "kernel32" Alias "WritePrivateProfileSectionA" (ByVal lpAppName As String, ByVal lpString As String, ByVal lpFileName As String) As Long
