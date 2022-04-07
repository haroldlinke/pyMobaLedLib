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

""" Decode Macro string into a Sheet
----------------------------------
--------------------------------------------------------
UT-------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on 1
----------------------------------------------------
--------------------------------------------------------------------------------------------------------------
-----------------------------------------------------
------------------------------------------------------------------------------------------------------------------
UT-------------------------------------------------------
UT-------------------------------------------------------
--------------------------------
------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------
"""

class Pattern_T:
    def __init__(self):
        self.AnalogFading = String()
        self.FirstRGBLED = Long()
        self.StartChannel = Long()
        self.BitsPerChannel = Long()
        self.SwitchNumber = String()
        self.Goto_Mode = String()
        self.GraphicDisplay = String()
        self.Channels = Long()
        self.Min_Val = Long()
        self.Max_Val = Long()
        self.Val_Off = Long()
        self.Mode = String()
        self.Duration = String()
        self.LED_Table = String()
        self.Goto_List = String()
        self.MaxBitVal = Long()

Add_To_This_Sheet_Default_Answer = Integer()

def __ErrorMsg(Msg):
    #----------------------------------
    MsgBox(Msg, vbCritical, Get_Language_Str('Fehler beim Dekodieren des Makros'))

def __Get_Goto_Chars(Par):
    fn_return_value = None
    Res = String()

    GotoNr = Integer()
    #--------------------------------------------------------
    if Par and START_BIT:
        Res = Res + 'S'
    if Par and POS_M_BIT:
        Res = Res + 'P'
    GotoNr = Par and GOTOENDNR
    if (GotoNr == 0):
        pass
    elif (GotoNr == GOTOENDNR):
        Res = Res + 'E'
    else:
        Res = Res + 'G' + GotoNr
    fn_return_value = Res
    return fn_return_value

def __Test_Decode_Pattern_String():
    #UT-------------------------------------
    #Decode_Pattern_String_and_Compare "PatternT1(0,28,SI_LocalVar,1,0,255,0,0,400 ms,0,19,26,30,36,48,0  ,1,129,129,129,129,129,127)     // _LocalVar_Sound_JQ6500"
    #Decode_Pattern_String_and_Compare "PatternT1(LED,4,InCh,6,5,128,0,PM_PINGPONG,1 Sek,3,192,0,48,0,12,0,3,192)"
    #Decode_Pattern_String_and_Compare "PatternT1(LED,128,SI_1,6,5,128,0,PM_PINGPONG,1 Sek,129,64,32,16,8)"
    #Decode_Pattern_String_and_Compare "PatternT1(LED,196,SI_1,5,5,128,0,PM_PINGPONG,1 Sek,3,48,0,3,48,0,3)"
    #Decode_Pattern_String_and_Compare "PatternT1(0,168,SI_1,5,5,128,0,PM_PINGPONG,1 Sek,7,0,28,0,112,0,192,1,0,7)     // Wechselblinker"
    __Decode_Pattern_String_and_Compare()('PatternT1(0,96,SI_1,1,0,255,0,PM_SEQUENZ_NO_RESTART,240,213,221,85,232,34,142,35,14,168,162,163,139,43,10)     // Morsecode')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: a - ByRef 
def __isInitialised(a):
    fn_return_value = None
    #----------------------------------------------------
    # Check if an array in initialized
    # This is usefull for functions which return an array
    # in case they fail
    # VB2PY (UntranslatedCode) On Error Resume Next
    fn_return_value = IsNumeric(UBound(a))
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: str - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Pattern_Res - ByRef 
def Decode_Pattern_String_to_Struct(str, Pattern_Res):
    fn_return_value = None
    Name = String()
    #--------------------------------------------------------------------------------------------------------------
    # Examples to Decode:
    #   PatternT1(LED,4,InCh,6,5,128,0,PM_PINGPONG,1 Sek,3,192,0,48,0,12,0,3,192)
    # Decode the name
    Name = Trim(Split(str, '(')(0))
    if Left(Name, Len('Pattern')) != 'Pattern' and Mid(Name, 2, Len('Pattern')) != 'Pattern':
        __ErrorMsg(Get_Language_Str('Fehler: Unbekannter Pattern Name \'') + Name + '\'')
        return fn_return_value
    with_0 = Pattern_Res
    select_1 = Left(Name, 1)
    if (select_1 == 'P'):
        with_0.AnalogFading = ''
    elif (select_1 == 'A'):
        with_0.AnalogFading = '1'
    elif (select_1 == 'X'):
        with_0.AnalogFading = 'X'
    else:
        __ErrorMsg(Get_Language_Str('Fehler: Unbekannter Pattern Typ \'') + Name + '\'')
        return fn_return_value
    TimeCnt = Val(Mid(Name, InStr(1, Name, 'PatternT') + Len('PatternT')))
    Params = Trim(Split(Split(str, '(')(1), ')')(0))
    Par = Split(Params, ',')
    with_0.FirstRGBLED = Val(Par(0))
    # Par(1): StCh_FreeBits_BpC = Startkanal+(Bits_pro_Wert-1)*4+FreeBits*32    ffffbbbss
    with_0.StartChannel = Par(1) % 4
    with_0.BitsPerChannel = 1 + Int(Par(1) / 4) % 8
    with_0.MaxBitVal = ( 2 ** with_0.BitsPerChannel )  - 1
    FreeBits = Int(Par(1) / 32)
    # Par(2): Input channel
    select_2 = Par(2)
    if (select_2 == 'InCh'):
        with_0.SwitchNumber = 'SI_1'
    elif (select_2 == 'SI_LocalVar'):
        with_0.SwitchNumber = Par(2)
        GotoMode = True
    else:
        with_0.SwitchNumber = Par(2)
    # Write the Goto Mode
    if GotoMode:
        with_0.Goto_Mode = 1
        with_0.GraphicDisplay = 1
    else:
        with_0.Goto_Mode = ''
    # Parameters 3..7
    LEDs = Par(3)
    with_0.Channels = LEDs
    with_0.Min_Val = Par(4)
    with_0.Max_Val = Par(5)
    with_0.Val_Off = Par(6)
    with_0.Mode = Par(7)
    # Par(8..): Time
    # VB2PY (UnhandledDefinition) Dim of implicit 'With' object (Duration) is not supported
    Duration = vbObjectInitialize(((1, TimeCnt),), Variant)
    DNr = 1
    for ParNr in vbForRange(8, 8 + TimeCnt - 1):
        with_0.Duration[DNr] = Par(ParNr)
        DNr = DNr + 1
    # Fill then LEDs table
    BitMaskCnt = UBound(Par) + 1 - ParNr
    BitsPerState = LEDs * with_0.BitsPerChannel
    if GotoMode:
        BitsPerState = BitsPerState + 8
        # One additional byte for the "Goto table"
    LastState = Int(( BitMaskCnt * 8 - FreeBits )  / BitsPerState) - 1
    if LastState < 1:
        return fn_return_value
        # Prevent crash if table is empty   ' 15.07.20:
    EndRow = LEDsTAB_R + LEDs
    LastCol = LEDsTAB_C + LastState
    # VB2PY (UnhandledDefinition) Dim of implicit 'With' object (LED_Table) is not supported
    LED_Table = vbObjectInitialize(((1, LEDs), (1, LastState + 1),), Variant)
    TabRow = 1
    TabCol = 1
    Row = LEDsTAB_R
    Col = LEDsTAB_C
    Div = 2 ** with_0.BitsPerChannel
    Mask = ( 2 ** with_0.BitsPerChannel )  - 1
    ActByte = Par(ParNr)
    ParNr = ParNr + 1
    RemBits = 8
    while not Finished:
        V = ActByte and Mask
        if (V == Mask):
            with_0.LED_Table[TabRow, TabCol] = 'x'
            ColFilled = True
        elif (V == 0):
            with_0.LED_Table[TabRow, TabCol] = ''
        else:
            with_0.LED_Table[TabRow, TabCol] = V
            ColFilled = True
        ActByte = Int(ActByte / Div)
        RemBits = RemBits - with_0.BitsPerChannel
        Finished = Row + 1 >= EndRow and Col + 1 > LastCol
        if not Finished:
            if RemBits < with_0.BitsPerChannel:
                ActByte = ActByte + Par(ParNr) *  ( 2 ** RemBits )
                ParNr = ParNr + 1
                RemBits = RemBits + 8
        TabRow = TabRow + 1
        Row = Row + 1
        if Row >= EndRow:
            if not ColFilled:
                with_0.LED_Table[TabRow - 1, TabCol] = '.'
                # Make sure that the last column contains at least one entry
            Row = LEDsTAB_R
            TabRow = 1
            TabCol = TabCol + 1
            Col = Col + 1
            ColFilled = False
    # Process the Goto Mode
    if GotoMode:
        # VB2PY (UnhandledDefinition) Dim of implicit 'With' object (Goto_List) is not supported
        Goto_List = vbObjectInitialize(((1, LastState + 1),), Variant)
        #Finished = False
        #Row = GoTo_Row
        #Col = GoTo_Col1
        GCol = 1
        while ParNr <= UBound(Par):
            with_0.Goto_List[GCol] = __Get_Goto_Chars(Val(Par(ParNr)))
            #Col = Col + 1
            GCol = GCol + 1
            ParNr = ParNr + 1
        # VB2PY (UnhandledDefinition) Dim of implicit 'With' object (Goto_List) is not supported
        Goto_List = vbObjectInitialize(((1, GCol - 1),), Variant, Goto_List)
    fn_return_value = True
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: str - ByVal 
def __Decode_Pattern_String(str):
    Pattern = Pattern_T()
    #-----------------------------------------------------
    # Examples to Decode:
    #   PatternT1(LED,4,InCh,6,5,128,0,PM_PINGPONG,1 Sek,3,192,0,48,0,12,0,3,192)
    if Decode_Pattern_String_to_Struct(str, Pattern):
        with_1 = Pattern
        OldEvents = Application.EnableEvents
        Application.EnableEvents = False
        Oldupdating = Application.ScreenUpdating
        Application.ScreenUpdating = False
        Range['Analoges_Überblenden'] = with_1.AnalogFading
        Range['ErsteRGBLED'] = with_1.FirstRGBLED
        Range['Startkanal'] = with_1.StartChannel
        Range['Bits_pro_Wert'] = with_1.BitsPerChannel
        Range['SchalterNr'] = with_1.SwitchNumber
        Range['Goto_Mode'] = with_1.Goto_Mode
        Range['Grafische_Anzeige'] = with_1.GraphicDisplay
        Range['Kanaele'] = with_1.Channels
        Range['Wert_Min'] = with_1.Min_Val
        Range['WertMax'] = with_1.Max_Val
        Range['Wert_ausgeschaltet'] = with_1.Val_Off
        Range['Mode'] = with_1.Mode
        # Fill the Duration table
        Range(Dauer_Rng).ClearContents()
        Dauer_Col = Dauer_Col1
        for D in with_1.Duration:
            Cells[Dauer_Row, Dauer_Col] = D
            Dauer_Col = Dauer_Col + 1
        # Fill then LEDs table
        Range(LEDsRANGE).ClearContents()
        Row = LEDsTAB_R
        for LRow in vbForRange(1, UBound(with_1.LED_Table, 1)):
            Col = LEDsTAB_C
            for LCol in vbForRange(1, UBound(with_1.LED_Table, 2)):
                Cells[Row, Col].Value = with_1.LED_Table(LRow, LCol)
                Col = Col + 1
            Row = Row + 1
        # Process the Goto Mode
        Range(GoTo_RNG).ClearContents()
        if __isInitialised(with_1.Goto_List):
            Col = GoTo_Col1
            for G in with_1.Goto_List:
                Cells[GoTo_Row, Col] = G
                Col = Col + 1
        Global_Worksheet_Change(Cells(1, 1))
        Application.EnableEvents = OldEvents
        Calculate()
        Application.ScreenUpdating = Oldupdating

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: str - ByVal 
def __Decode_Pattern_String_and_Compare(str, Gen_Message=VBMissingArgument):
    fn_return_value = None
    Org = String()

    Res = String()
    #------------------------------------------------------------------------------------------------------------------
    Org = Split(str, ')')(0) + ')'
    Org = Replace(Org, '(LED,', '(0,')
    Org = Replace(Org, '(#LED,', '(0,')
    Org = Replace(Org, ',InCh,', ',SI_1,')
    __Decode_Pattern_String(str)
    Res = Split(Range(ErgebnisRng), ')')(0) + ')'
    if Org != Res:
        Debug.Print('')
        Debug.Print('Error importing macro:')
        Debug.Print('Org: ' + Org)
        Debug.Print('Res: ' + Res, '')
        if Gen_Message:
            MsgBox(Get_Language_Str('Fehler beim importieren des Makros aufgetreten ;-(' + vbCr + vbCr + 'Das Macro entspricht leider nicht genau dem original Macro.' + vbCr + 'Problem bitte an Hardi melden...'), vbCritical, Get_Language_Str('Interne Fehler beim importieren des Macros'))
    else:
        fn_return_value = True
    return fn_return_value

def __Test_Decode_Pattern_String_with_All_Examples():
    Sh = Variant()

    ErrCnt = Long()
    #UT-------------------------------------------------------
    # Attention the content in the actual sheet is changed
    for Sh in ThisWorkbook.Sheets:
        if Is_Normal_Data_Sheet(Sh.Name, Get_Language_Str('verglichen')) and Sh.Name != ActiveSheet.Name:
            Debug.Print('Checking ' + Sh.Name)
            if __Decode_Pattern_String_and_Compare(Sh.Range(ErgebnisRng)):
                Debug.Print('O.k.')
            else:
                ErrCnt = ErrCnt + 1
    Debug.Print('*** All Sheets checked! ' + ErrCnt + ' Errors ***')

def __Test_Decode_Pattern_String_by_Sheetname():
    Sh = Variant()
    #UT-------------------------------------------------------
    # Attention the content in the actual sheet is changed
    Sh = Sheets('LocalVar Sound')
    Debug.Print('Checking ' + Sh.Name)
    if __Decode_Pattern_String_and_Compare(Sh.Range(ErgebnisRng)):
        Debug.Print(Sh.Name + ' O.k.')

def Import_From_Prog_Gen():
    #--------------------------------
    Select_Line_in_Prog_Gen_and_Call_Macro(False, 'Import_From_Prog_Gen_Callback')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Line - ByVal 
def __Import_GotoActivation(Line):
    ActStr = '// Activation: '
    #------------------------------------------------------
    if Left(Line, Len(ActStr)) == ActStr:
        ActTxt = Mid(Line, Len(ActStr) + 1)
        Range['Goto_Aktivierung'] = ActTxt

def __Import_From_Prog_Gen_Callback(OK_Pressed, Description, Macro, Row):
    MacroName = String()

    Line = Variant()
    #--------------------------------------------------------------------------------------------------------------------
    ThisWorkbook.Activate()
    if not OK_Pressed:
        return
    if (Add_To_This_Sheet_Default_Answer == 1):
        Add_To_This_Sheet_Default_Answer = vbDefaultButton1
    elif (Add_To_This_Sheet_Default_Answer == 2):
        Add_To_This_Sheet_Default_Answer = vbDefaultButton2
    else:
        Add_To_This_Sheet_Default_Answer = vbDefaultButton2
    MacroName = 'Imported_Pattern'
    if Right(Description, Len(FROM_PAT_CONFIG_TXT)) == FROM_PAT_CONFIG_TXT:
        MacroName = Replace(Left(Description, Len(Description) - Len(FROM_PAT_CONFIG_TXT)), ' ', '_')
        MacroName = ValidNameCharacters(MacroName)
    select_5 = MsgBox(Get_Language_Str('Soll die Zeile in das aktuelle Blatt eingefügt werden?' + vbCr + vbCr + 'Ja: Die Daten in diesem Blatt werden überschrieben' + vbCr + 'Nein: Es wird ein neues Blatt angelegt'), vbYesNoCancel + Add_To_This_Sheet_Default_Answer, Get_Language_Str('Daten in aktuelles oder neues Blatt einfügen'))
    if (select_5 == vbYes):
        Add_To_This_Sheet_Default_Answer = 1
    elif (select_5 == vbCancel):
        return
    elif (select_5 == vbNo):
        Add_To_This_Sheet_Default_Answer = 2
        Name = InputBox(Get_Language_Str('Name des neuen Blattes?'), Get_Language_Str('Neues Blatt anlegen'), Unic_SheetName(MacroName, '_'))
        if Name == '':
            return
        Create_New_Sheet(Name, Add_to_Duplicate_Name='_', AfterSheetName=MAIN_SH)
        Load_Textbox(StdDescEdges + Chr(pcfSep) + Get_Language_Str(StdDescStart))
        Range[Macro_N_Rng] = Replace_Illegal_Char(ActiveSheet.Name)
        Add_by_Hardi()
        Range(FirstLEDTabRANGE).Select()
        Protect_Active_Sheet()
    Range['Makro_Name'] = MacroName
    Range('Goto_Aktivierung').ClearContents()
    # Decode the imported macro line
    for Line in Split(Macro, vbLf):
        if InStr(Line, 'PatternT') > 0:
            __Decode_Pattern_String_and_Compare()(Line, True)
        else:
            __Import_GotoActivation(Line)

# VB2PY (UntranslatedCode) Option Explicit
