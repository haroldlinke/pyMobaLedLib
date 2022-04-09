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

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

"""---------------------

---------------------------------------------------
 Berechnung der Zeiten:                                                    ' 15.01.20:
 ~~~~~~~~~~~~~~~~~~~~~~
 Die Zeiten sind als 16 Bit Zahl angelegt. => Es sind maximal 65 Sekunden pro Schritt möglich.
 Wenn längere Zeiten Benötigt werden muss man das Flag "PF_SLOW" setzen. Damit werden die Zeiten
 in 16 ms Schritten gezählt.
 Das Setzen des Flags soll automatisch gemacht werden.
 Eine Funktion berechnet aus den Zeiten einen String. Diese Funktion Prüft ob eine der Zeiten größer
 als 65 sekunden ist. Wenn ja, dann werden alle Zeiten durch 16 geteilt.
 Es gibt zwei möglichkeiten wie das gemacht werden kann:
 1. Es wird einfach ein "\16" angehängt.
    Das hat den Vorteil, das man am Makro erkennt welche Zeit verwendet wird.
    Für die Übertragung zum Servo Modul ist aber eine zusätzliche Berechnung nötig.
 2. Der Wert wird umgerechnet im 16 ms und als Zahl abgelegt.
----------------------------------------------------------------------------------
"""

__MAX_VARARGS = 2000
START_BIT = 128
POS_M_BIT = 64
GOTOENDNR = POS_M_BIT - 1
MAXGOTONR = GOTOENDNR - 1
Last_SelectedCell = None #*HL Range()
__OldMessage = String()
__initDone = Boolean()

def Auto_Open():
    #---------------------
    # For some reasons the Workbook_Open() macro is not allways called ;-(
    # Therefor we use this Auto_Open() macro in addition
    #
    # But this macro is not called if the file is opened from an other excel sheet
    # See: https://www.pcreview.co.uk/threads/auto_open-vs-workbook_open.953960/
    #
    Debug.Print('Auto_Open() called')
    Init()

def Init():
    ShowSaveMsg = Boolean()
    #----------------
    #Stop  ' uncomment to have a breakpoint at startup
    P01.ThisWorkbook.Activate()
    if __initDone:
        return
    __initDone = True
    if P01.Sheets('Multiplexer').Visible == True:
        P01.Sheets('Main').Select()
        # Prevent problem in the following line
    Debug.Print('Init() called (Sheets.count=' + P01.ThisWorkbook.Sheets.Count + ')')
    P01.Sheets('Languages').Visible(False)
    P01.Sheets('Goto_Activation_Entries').Visible(False)
    P01.Sheets('Special_Mode_Dlg').Visible(False)
    P01.Sheets('Par_Description').Visible(False)
    P01.Sheets('Multiplexer').Visible(False)
    #*HL Cleare_Mouse_Hook()
    Check_Version()
    Update_Language_in_All_Sheets()
    if ThisWorkbook.Sheets.Count == 6:
        __Clear_Com_Port()
        ShowSaveMsg = Load_AllExamples_Sheets()
        ThisWorkbook.Activate()
        Sheets('Main').Select()
        Protect_Active_Sheet()
        ActiveWindow.DisplayHeadings = False
        #Update_Grafik
    else:
        __Reset_Com_Port()
    Copy_Prog_If_in_LibDir()
    if ShowSaveMsg:
        MsgBox('Das Excel Programm sollte gespeichert werden damit die Beispiele beim nächsten Start nicht erneut geladen werden müssen.', vbInformation, 'Bitte Excel speichern')

def __Reset_Com_Port():
    Col = Long()
    #---------------------------
    for Col in vbForRange(COMPort_COL, COMPrtT_COL):
        with_0 = Sheets('Main').Cells(SH_VARS_ROW, Col)
        if with_0.Value != '':
            #Debug.Print "Reset_Com_Port in column " & Col & " in the Main sheet (Old:" & .Value & ")"
            if with_0.Value > 0:
                with_0.Value = - with_0.Value

def __Clear_Com_Port():
    Col = Long()
    #---------------------------
    for Col in vbForRange(COMPort_COL, COMPrtT_COL):
        with_1 = Sheets('Main').Cells(SH_VARS_ROW, Col)
        if with_1.Value != '':
            #Debug.Print "Clear_Com_Port in column " & Col & " in the Main sheet (Old:" & .Value & ")"
            with_1.Value = ''

def __Workbook_Open():
    #--------------------------
    Debug.Print('Workbook_Open() in modul M02_Main called (Sheets.count=' + ThisWorkbook.Sheets.Count + ')')
    Stop()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: MaxVal - ByVal 
def Get_LED_Val(c, MaxVal):
    fn_return_value = None
    V = Integer()
    #----------------------------------------------------------------------------
    if c != '':
        if IsNumeric(c):
            V = Val(c)
            if V > MaxVal:
                V = MaxVal
        else:
            s = Trim(c)
            if s == '' or s == '.' or s == '-':
                V = 0
                V = MaxVal
    fn_return_value = V
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: MaxVal - ByVal 
def Get_LED_Val_8_Bit(c, MaxVal):
    fn_return_value = None
    V = Integer()
    #----------------------------------------------------------------------------------
    if c != '':
        if IsNumeric(c):
            V = Val(c)
            if V > MaxVal:
                V = MaxVal
            fn_return_value = V
        else:
            s = Trim(c)
            if s == '' or s == '.' or s == '-':
                fn_return_value = 0
            elif Len(s) > 1:
                fn_return_value = s
            else:
                fn_return_value = MaxVal
        fn_return_value = 0
    return fn_return_value

def __Calc_DecStr_Normal(Rng, LastRow, MaxColumn, BitLen):
    fn_return_value = None
    ColCnt = Long()

    c = Range()

    Col = Range()

    Bits = String()

    MaxVal = Integer()

    BitCnt = Long()

    ByteCnt = Long()

    DecStr = String()

    FreeBits = Long()
    #--------------------------------------------------------------------------------------------------------------
    MaxVal = ( 2 ** BitLen )  - 1
    for Col in Rng.Columns:
        if Col.Column > MaxColumn:
            break
        ColCnt = ColCnt + 1
        for c in Col.Cells:
            if c.Row > LastRow:
                break
            #Debug.Print "R:" & c.Row & "  C:" & c.Column
            if c.Value != '':
                Cnt = Cnt + 1
            Val = Get_LED_Val(c, MaxVal)
            Bits = WorksheetFunction.Dec2Bin(Val, BitLen) + Bits
    BitCnt = Len(Bits)
    #Debug.Print Len(Bits) & ": " & Bits & "  "   ' Debug
    while Len(Bits) > 0:
        ByteCnt = ByteCnt + 1
        DecStr = DecStr + ',' + WorksheetFunction.Bin2Dec(Right(Bits, 8))
        if Len(Bits) > 8:
            Bits = Left(Bits, Len(Bits) - 8)
            Bits = ''
    #Debug.Print "Used bytes: " & ByteCnt
    if ByteCnt > __MAX_VARARGS:
        MsgBox(Get_Language_Str('Error: Number of used bytes to high !') + __MAX_VARARGS + Get_Language_Str(' bytes are possible.') + vbCr + 'The current configuration uses ' + ByteCnt + ' bytes ;-(', vbCritical, Get_Language_Str('Error to many bytes used'))
    #Debug.Print DecStr      ' Debug
    FreeBits = ByteCnt * 8 - BitCnt
    fn_return_value = FreeBits + ':' + DecStr
    return fn_return_value

def __Calc_DecStr_8_Bits(Rng, LastRow, MaxColumn, BitLen):
    fn_return_value = None
    ColCnt = Long()

    c = Range()

    Col = Range()

    MaxVal = Integer()

    DecStr = String()

    BitCnt = Long()

    ByteCnt = Long()
    #--------------------------------------------------------------------------------------------------------------
    MaxVal = ( 2 ** BitLen )  - 1
    for Col in Rng.Columns:
        if Col.Column > MaxColumn:
            break
        ColCnt = ColCnt + 1
        for c in Col.Cells:
            if c.Row > LastRow:
                break
            #Debug.Print "R:" & c.Row & "  C:" & c.Column
            if c.Value != '':
                Cnt = Cnt + 1
            DecStr = DecStr + ',' + Get_LED_Val_8_Bit(c, MaxVal)
            ByteCnt = ByteCnt + 1
    if ByteCnt > __MAX_VARARGS:
        MsgBox(Get_Language_Str('Error: Number of used bytes to high !') + __MAX_VARARGS + Get_Language_Str(' bytes are possible.') + vbCr + Get_Language_Str('The current configuration uses ') + ByteCnt + ' bytes ;-(', vbCritical, Get_Language_Str('Error to many bytes used'))
    fn_return_value = '0:' + DecStr
    return fn_return_value

def __Ist_Formel(c):
    fn_return_value = None
    #-----------------------------------------
    # Excel 2010 doesn't have the "IstFormel()" command
    fn_return_value = Left(c.Formula, 1) == '='
    return fn_return_value

def __CalculatePattern(ChannelsRange, BitLenRange, PatternRange):
    fn_return_value = None
    Rng = Range()

    Channels = Long()

    BitLen = Long()

    FirstRow = Long()

    LastRow = Long()

    MaxVal = Integer()

    c = Range()

    MaxColumn = Long()
    #-------------------------------------------------------------------------------------------------------------
    # The first character contains the number of free bits which is needed for the calculation
    # of the number of states in the Arduino program
    # ToDo: Übergebene Variablen Typen prüfen...
    Channels = ChannelsRange
    BitLen = BitLenRange
    Rng = PatternRange
    FirstRow = Rng.Row
    LastRow = FirstRow + Channels - 1
    MaxVal = ( 2 ** BitLen )  - 1
    #MaxColumn = LastFilledColumn(Rng, LastRow) ' Find the last used column
    MaxColumn = LastFilledColumn2(Rng, LastRow)
    if BitLen < 8:
        fn_return_value = __Calc_DecStr_Normal(Rng, LastRow, MaxColumn, BitLen)
        fn_return_value = __Calc_DecStr_8_Bits(Rng, LastRow, MaxColumn, BitLen)
    #Debug.Print "CalculatePattern(" & ChannelsRange & ", " & BitLenRange & "," & PatternRange.Address & ")  called from " & ActiveSheet.Name & ":" & CalculatePattern
    return fn_return_value

def __Calculate_Goto(ChannelsRange, GotoModeRange, GotoTabRange, PatternRange):
    fn_return_value = None
    Rng = Range()

    Channels = Long()

    FirstRow = Long()

    LastRow = Long()

    MaxColumn = Long()

    c = Range()

    ColumnNr = Long()

    Unknown = String()

    WrongNumberFound = String()

    message = String()
    #--------------------------------------------------------------------------------------------------------------------------------------
    if GotoModeRange != 1:
        return fn_return_value
    # ToDo: Übergebene Variablen Typen prüfen...
    Channels = ChannelsRange
    Rng = PatternRange
    FirstRow = Rng.Row
    LastRow = FirstRow + Channels - 1
    #MaxColumn = LastFilledColumn(Rng, LastRow) ' Find the last used column
    MaxColumn = LastFilledColumn2(Rng, LastRow)
    fn_return_value = '  '
    for c in GotoTabRange:
        ColumnNr = ColumnNr + 1
        if c.Column > MaxColumn:
            break
        Start = False
        GotoP = False
        GoEnd = False
        Pos_M = False
        Number = 0
        Words = Split(Replace(Replace(Replace(Replace(Replace(UCase(c), '-', ' - '), 'S', ' S '), 'P', ' P '), 'E', ' E '), 'G', ' G '), ' ')
        for w in Words:
            if (w == ''):
                pass
            elif (w == 'S'):
                if ColumnNr > 1:
                    Start = True
            elif (w == 'P'):
                Pos_M = True
            elif (w == 'G'):
                GotoP = True
            elif (w == 'E'):
                GoEnd = True
            else:
                if IsNumeric(w):
                    Number = Val(w)
                else:
                    Unknown = Unknown + ' \'' + w + '\''
        Nr = 0
        if Start:
            Nr = Nr + START_BIT
        if Pos_M:
            Nr = Nr + POS_M_BIT
        if GotoP:
            if Number <= 0 or Number > MAXGOTONR:
                WrongNumberFound = WrongNumberFound + ', ' + ColumnNr
                Nr = Nr + Number
        elif GoEnd:
            Nr = Nr + GOTOENDNR
        #Debug.Print Format(ColumnNr, "@@@") & ": Nr=" & Format(Nr, "@@@") & "  Start=" & Format(Start, "@@@@@@@") & " GoEnd=" & Format(GoEnd, "@@@@@@@") & " Goto=" & Format(GotoP, "@@@@@@@") & " " & Number ' Debug
        fn_return_value = __Calculate_Goto() + ',' + Nr
    if WrongNumberFound != '':
        WrongNumberFound = Mid(WrongNumberFound, 2)
        # Remove leading ","
    #Debug.Print ' Debug
    if Unknown != '':
        message = message + Get_Language_Str('Ignored expresions: ') + Unknown + vbCr
    if WrongNumberFound != '':
        message = message + Get_Language_Str('Falsche oder fehlende Nummer in Spalte gefunden: ') + WrongNumberFound + vbCr + Get_Language_Str('(Gültiger Bereich: 1..63)')
    if message != __OldMessage:
        __OldMessage = message
        if message != '':
            MsgBox(message, vbOKOnly, Get_Language_Str('Problems in Goto tabele:'))
    #Debug.Print Message
    return fn_return_value

def Update_Grafik_from_Str(GrafDsp):
    Oldupdating = Boolean()

    GrafDsp_U = String()

    Show_AnalogTrend = Boolean()

    Show_Goto_Graph = Boolean()

    Show_CorrectWidth = Boolean()
    #---------------------------------------------------
    Oldupdating = Application.ScreenUpdating
    Application.ScreenUpdating = False
    # Check the "Grafische Anzeige:" field
    GrafDsp_U = UCase(GrafDsp)
    if InStr(GrafDsp_U, '1') > 0:
        Show_AnalogTrend = True
        Show_Goto_Graph = True
    if InStr(GrafDsp_U, 'L') > 0:
        Show_AnalogTrend = True
    if InStr(GrafDsp_U, 'G') > 0:
        Show_Goto_Graph = True
    if InStr(GrafDsp_U, 'D') > 0:
        Show_CorrectWidth = True
    if Show_CorrectWidth:
        Adjust_Column_With_to_Duration()
        Normal_Column_With()
    if Show_AnalogTrend:
        Draw_Analog_Trend_of_Sheet()
        Del_Analog_Trend_Objects()
    if Show_Goto_Graph:
        Draw_All_Arrows()
        Delete_Goto_Graph()
    Application.ScreenUpdating = Oldupdating

def Calc_TimesStr(TimeRange, ModeRange):
    fn_return_value = None
    c = Variant()

    V = Long()

    Res = String()

    Use_PF_SLOW = Boolean()

    IsError = Boolean()

    EmptyCol = Boolean()

    FirstCell = Boolean()
    #----------------------------------------------------------------------------------
    # Is called in the Excel sheed with:
    #  =Calc_TimesStr(F28:AI28;Mode)
    # In case of an error following strings are inserted:
    #  "!Error:"
    #  "!Empty"
    # It's also possible to use a decimal komma "," in the time strings like "1,3 Min"
    FirstCell = True
    for c in TimeRange:
        if FirstCell:
            if Trim(c) == '':
                Res = Res + '!Empty,'
            FirstCell = False
        if Trim(c) != '' and Left(c.Formula, 1) != '=':
            if EmptyCol:
                Res = Res + '!Empty,'
                EmptyCol = False
            if IsNumeric(c):
                V = Val(c)
            else:
                V = Convert_TimeStr_to_ms(c)
            if V > 65535:
                if V > 65535 * 16:
                    V = - 16
                    Use_PF_SLOW = True
            if V < 0:
                # Displaying of messages in the statusbar is not possible in a user defined function in Excel ;-(
                # See: https://support.microsoft.com/en-us/help/170787/description-of-limitations-of-custom-functions-in-excel
                Res = Res + '!Error:' + c + ','
            else:
                Res = Res + Replace(c, ',', '.') + ','
        else:
            EmptyCol = True
    if InStr(ModeRange, 'PF_SLOW') > 0:
        Use_PF_SLOW = True
    if Use_PF_SLOW:
        Res = Replace(Res, ',', '/16,')
        while InStr(Res, ' +') > 0:
            Res = Replace(Res, ' +', '+')
        Res = Replace(Res, '+', '/16 +')
    fn_return_value = ',' + DelLast(Res)
    return fn_return_value

def Hide_Show_Check_Goto_Activation(Correct_Act_Cell=VBMissingArgument):
    Hide = Boolean()
    #-------------------------------------------------------------------------------
    # Hide the "Goto Aktivation" row
    Hide = not Goto_Mode_is_Active()
    if Range('Goto_Aktivierung').EntireRow.Hidden != Hide:
        WasProtected = ActiveSheet.ProtectContents
        if WasProtected:
            ActiveSheet.Unprotect()
        Range['Goto_Aktivierung'].EntireRow.Hidden = Hide
        if WasProtected:
            Protect_Active_Sheet()
        if Correct_Act_Cell and Hide == False and ActiveCell.Address == Range('Goto_Aktivierung').offset(1, 0).Address:
            ActiveCell.offset(- 1, 0).Activate()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Global_Worksheet_Change(Target):
    #--------------------------------------------------------------
    # This function is called if the worksheet is changed.
    # It performs several checks after a user input depending form the column of the changed cell:
    # Attention: It's also called from some functions to update the display
    if DEBUG_CHANGEEVENT:
        Debug.Print('Global_Worksheet_Change')
    if Target.CountLarge == 1:
        if Is_Data_Sheet(Target.Parent):
            Oldupdating = Application.ScreenUpdating
            Application.ScreenUpdating = False
            Hide_Show_GotoLines_If_Enabled()
            Hide_Show_Special_ModeLines_If_Enabled()
            Update_Grafik_from_Str(Range(GrafDsp_Rng))
            Hide_Show_Check_Goto_Activation(True)
            Application.ScreenUpdating = Oldupdating
            if Target.Address == Range('Kanaele').Address:
                Change_Number_Of_LEDs()
                # Added by Misha 20-6-2020  06.07.20: Hardi: Moved up

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Global_Worksheet_SelectionChange(Target):
    #-----------------------------------------------------------------------
    # Is called by event if the worksheet selection has changed
    if TestPatternButtonOn:
        Debug.Print('Global_Worksheet_SelectionChange called => Stop executing the Displaying of a Pattern')
        Button_Pressed_Handling('Test_Leds_M99O01', True)
    if Target.Column == Range('Goto_Aktivierung').Column:
        if Target.Row == Range('Goto_Aktivierung').Row:
            if Goto_Mode_is_Active() and Range('Goto_Aktivierung') == '':
                Select_GotoAct()
                Target = ActiveCell
    Last_SelectedCell = Target
    #Debug.Print "Store Last " & Target.Row

def Button_Pressed_Proc():
    #--------------------------------
    Selection.Select()
    Enable_Application_Automatics()
    __Correct_Buttonsizes()

def __Correct_Create_Buttonsize(obj):
    #-----------------------------------------
    obj.Height = 160
    obj.Width = 100
    obj.Height = 83
    obj.Width = 56

def __Correct_Buttonsizes():
    OldScreenupdating = Boolean()
    #--------------------------------
    # There is a bug in excel which changes the size of the buttons
    # if the resolution of the display is changed. This happens
    # fore instance if the computer is connected to a beamer.
    # To prevent this the buttons are resized with this function.
    OldScreenupdating = Application.ScreenUpdating
    Application.ScreenUpdating = False
    __Correct_Create_Buttonsize(ActiveSheet.Prog_Generator_Button)
    __Correct_Create_Buttonsize(ActiveSheet.Send2Module_Button)
    __Correct_Create_Buttonsize(ActiveSheet.Import_from_ProgGen_Button)
    __Correct_Create_Buttonsize(ActiveSheet.Send2Module_Button)
    __Correct_Create_Buttonsize(ActiveSheet.InsertPicture_Button)
    Application.ScreenUpdating = OldScreenupdating

def Main_Menu():
    #---------------------
    if TestPatternButtonOn:
        Button_Pressed_Handling('Test_Leds_M99O01', True)()
        # Stop executing the Displaying of a Pattern   ' 02.06.20: Misha
    MainMenu_Form.Show()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def Is_Data_Sheet(Sh):
    fn_return_value = None
    Is_PatternSheet = Boolean()
    #--------------------------------------------------------------
    # Check if the sheet is an data sheet
    # VB2PY (UntranslatedCode) On Error Resume Next
    fn_return_value = ( Sh.Range('RGB_Modul_Nr').Address != '' )
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return fn_return_value

def Global_On_Enter_Proc():
    Offs = Long()
    #--------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on DEBUG_CHANGEEVENT
    Debug.Print('Global_On_Enter_Proc ' + ActiveCell.Address + ' ')
    # VB2PY (UntranslatedCode) On Error Resume Next
    Debug.Print(Selection.Address)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    Debug.Print('')
    if Is_Data_Sheet(ActiveSheet):
        if not IsError(ActiveCell):
            if ActiveCell == '' or ActiveCell == '?':
                if (ActiveCell.Address == Range('Goto_Aktivierung').Address):
                    Select_GotoAct()
                elif (ActiveCell.Address == Range('Special_Mode').Address):
                    Select_Special_Mode()
                elif (ActiveCell.Address == Range('RGB_Modul_Nr').Address):
                    Get_LED_Address_Dialog()
                elif (ActiveCell.Address == Range('CPX_LED_Assignement').Address):
                    LED_Assignement_Dialog()
    # Select next cell, but not a hidden cell
    Offs = 1
    while 1:
        if ActiveCell.offset(Offs, 0).EntireRow.Hidden:
            Offs = Offs + 1
            break
        if not (Offs < 1000):
            break
    ActiveCell.offset(Offs, 0).Select()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cancel - ByRef 
def Proc_DoubleCkick(Sh, Target, Cancel):
    #----------------------------------------------------------------------------------------------
    if Is_Data_Sheet(ActiveSheet):
        if (ActiveCell.Address == Range('Goto_Aktivierung').Address):
            Cancel = True
            Select_GotoAct()
        elif (ActiveCell.Address == Range('Special_Mode').Address):
            Cancel = True
            Select_Special_Mode()
        elif (ActiveCell.Address == Range('RGB_Modul_Nr').Address):
            Cancel = True
            Get_LED_Address_Dialog()
        elif (ActiveCell.Address == Range('CPX_LED_Assignement').Address):
            Cancel = True
            LED_Assignement_Dialog()

def Global_Worksheet_Deactivate():
    #---------------------------------------
    Application.OnKey('{Return}', '')
    if TestPatternButtonOn:
        Debug.Print('Global_Worksheet_Deactivate called => Stop executing the Displaying of a Pattern')
        Button_Pressed_Handling('Test_Leds_M99O01', True)

# VB2PY (UntranslatedCode) Option Explicit

