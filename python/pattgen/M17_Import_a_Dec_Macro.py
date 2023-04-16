from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M09_Language
import ExcelAPI.XLW_Workbook as X02
import pattgen.M02_Main as M02a
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M08_Load_Sheet_Data
import pattgen.M11_To_Prog_Gen
import pattgen.M30_Tools as M30
import mlpyproggen.Pattern_Generator as PG

""" Decode Macro string into a Sheet
----------------------------------
--------------------------------------------------------
UT-------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on 1
 15.05.20:
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

def ErrorMsg(Msg):
    #----------------------------------
    X02.MsgBox(Msg, vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler beim Dekodieren des Makros'))

def Get_Goto_Chars(Par):
    _fn_return_value = None
    Res = String()

    GotoNr = Integer()
    #--------------------------------------------------------
    if Par & M02a.START_BIT:
        Res = Res + 'S'
    if Par & M02a.POS_M_BIT:
        Res = Res + 'P'
    GotoNr = Par & M02a.GOTOENDNR
    _select33 = GotoNr
    if (_select33 == 0):
        # Nothing
        pass
    elif (_select33 == M02a.GOTOENDNR):
        Res = Res + 'E'
    else:
        Res = Res + 'G' + str(GotoNr)
    _fn_return_value = Res
    return _fn_return_value

def Test_Decode_Pattern_String():
    #UT-------------------------------------
    #Decode_Pattern_String_and_Compare "PatternT1(0,28,SI_LocalVar,1,0,255,0,0,400 ms,0,19,26,30,36,48,0  ,1,129,129,129,129,129,127)     // _LocalVar_Sound_JQ6500"
    #Decode_Pattern_String_and_Compare "PatternT1(LED,4,InCh,6,5,128,0,PM_PINGPONG,1 Sek,3,192,0,48,0,12,0,3,192)"
    #Decode_Pattern_String_and_Compare "PatternT1(LED,128,SI_1,6,5,128,0,PM_PINGPONG,1 Sek,129,64,32,16,8)"
    #Decode_Pattern_String_and_Compare "PatternT1(LED,196,SI_1,5,5,128,0,PM_PINGPONG,1 Sek,3,48,0,3,48,0,3)"
    #Decode_Pattern_String_and_Compare "PatternT1(0,168,SI_1,5,5,128,0,PM_PINGPONG,1 Sek,7,0,28,0,112,0,192,1,0,7)     // Wechselblinker"
    Decode_Pattern_String_and_Compare('PatternT1(0,96,SI_1,1,0,255,0,PM_SEQUENZ_NO_RESTART,240,213,221,85,232,34,142,35,14,168,162,163,139,43,10)     // Morsecode')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: a - ByRef 
def isInitialised(a):
    _fn_return_value = None
    # ToDo: Move to M30_Tools
    #----------------------------------------------------
    # Check if an array in initialized
    # This is usefull for functions which return an array
    # in case they fail
    # VB2PY (UntranslatedCode) On Error Resume Next
    _fn_return_value = IsNumeric(UBound(a))
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: str - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Pattern_Res - ByRef 
def Decode_Pattern_String_to_Struct(p_str, Pattern_Res):
    _fn_return_value = None
    GotoMode = False  #*HL
    ColFilled = False #*HL
    
    Name = String()
    #--------------------------------------------------------------------------------------------------------------
    # Examples to Decode:
    #   PatternT1(LED,4,InCh,6,5,128,0,PM_PINGPONG,1 Sek,3,192,0,48,0,12,0,3,192)
    # Decode the name
    Name = Trim(Split(p_str, '(')(0))
    if Left(Name, Len('Pattern')) != 'Pattern' and Mid(Name, 2, Len('Pattern')) != 'Pattern':
        ErrorMsg(pattgen.M09_Language.Get_Language_Str('Fehler: Unbekannter Pattern Name \'') + Name + '\'')
        return _fn_return_value
    _with46 = Pattern_Res
    _select34 = Left(Name, 1)
    if (_select34 == 'P'):
        _with46.AnalogFading = ''
    elif (_select34 == 'A'):
        _with46.AnalogFading = '1'
    elif (_select34 == 'X'):
        _with46.AnalogFading = 'X'
    else:
        ErrorMsg(pattgen.M09_Language.Get_Language_Str('Fehler: Unbekannter Pattern Typ \'') + Name + '\'')
        return _fn_return_value
    TimeCnt = int(Val(Mid(Name, InStr(1, Name, 'PatternT') + Len('PatternT'))))
    Params = Trim(Split(Split(p_str, '(')(1), ')')(0))
    Par = Split(Params, ',')
    _with46.FirstRGBLED = Val(Par(0))
    # Par(1): StCh_FreeBits_BpC = Startkanal+(Bits_pro_Wert-1)*4+FreeBits*32    ffffbbbss
    _with46.StartChannel = int(Par(1)) % 4 #*HL
    _with46.BitsPerChannel = 1 + int(int(Par(1)) / 4) % 8 #*HL
    _with46.MaxBitVal = ( 2 ** _with46.BitsPerChannel )  - 1
    # 03.06.20:
    FreeBits = int(int(Par(1)) / 32) #*HL
    # Par(2): Input channel
    _select35 = Par(2)
    if (_select35 == 'InCh'):
        _with46.SwitchNumber = 'SI_1'
        # Str is read from "Macro" line => We don't know the "SchalterNr" value
    elif (_select35 == 'SI_LocalVar'):
        _with46.SwitchNumber = Par(2)
        GotoMode = True
    else:
        _with46.SwitchNumber = Par(2)
    # Write the Goto Mode
    if GotoMode:
        _with46.Goto_Mode = "1"
        _with46.GraphicDisplay = "1"
    else:
        _with46.Goto_Mode = ''
    # Parameters 3..7
    LEDs = int(Par(3)) #*HL
    _with46.Channels = LEDs
    # Par(3): Number of output channels
    _with46.Min_Val = int(Par(4))
    # Par(4): Min value
    _with46.Max_Val = int(Par(5))
    # Par(5): Max value
    _with46.Val_Off = int(Par(6))
    # Par(6): Off value
    _with46.Mode = Par(7)
    # Par(7): Mode
    # Par(8..): Time
    # VB2PY (UnhandledDefinition) Dim of implicit 'With' object (Duration) is not supported
    _with46.Duration = vbObjectInitialize(((1, int(TimeCnt)),), Variant)
    DNr = 1
    ParNr = 0
    for ParNr in vbForRange(8, 8 + TimeCnt - 1):
        _with46.Duration[DNr] = Par(ParNr)
        DNr = DNr + 1
    # Fill then LEDs table
    ParNr+=1 #*HL loop variable is one too low at the end of the loop
    BitMaskCnt = UBound(Par) + 1 - ParNr
    # number of remaining parameters
    BitsPerState = LEDs * _with46.BitsPerChannel
    if GotoMode:
        BitsPerState = BitsPerState + 8
    # One additional byte for the "Goto table"
    LastState = Int(( BitMaskCnt * 8 - FreeBits )  / BitsPerState) - 1
    if LastState < 1:
        return _fn_return_value
    # Prevent crash if table is empty
    # 15.07.20:
    EndRow = M01.LEDsTAB_R + LEDs
    LastCol = M01.LEDsTAB_C + LastState
    # VB2PY (UnhandledDefinition) Dim of implicit 'With' object (LED_Table) is not supported
    _with46.LED_Table = vbObjectInitialize(((1, LEDs), (1, LastState + 1),), Variant) #*HL
    TabRow = 1
    TabCol = 1
    Row = M01.LEDsTAB_R
    Col = M01.LEDsTAB_C
    Div = 2 ** _with46.BitsPerChannel
    Mask = ( 2 ** _with46.BitsPerChannel )  - 1

    ActByte = int(Par(ParNr)) #*HL
    ParNr = ParNr + 1
    RemBits = 8
    Finished = False #*HL
    while not Finished:
        V = ActByte & Mask  #*HL
        _select36 = V
        if (_select36 == Mask):
            _with46.LED_Table[TabRow, TabCol] = 'x'
            ColFilled = True
        elif (_select36 == 0):
            _with46.LED_Table[TabRow, TabCol] = ''
        else:
            _with46.LED_Table[TabRow, TabCol] = V
            ColFilled = True
        ActByte = Int(ActByte / Div)
        RemBits = RemBits - _with46.BitsPerChannel
        Finished = Row + 1 >= EndRow and Col + 1 > LastCol
        if not Finished:
            if RemBits < _with46.BitsPerChannel:
                ActByte = ActByte + int(Par(ParNr)) *  ( 2 ** RemBits )
                ParNr = ParNr + 1
                RemBits = RemBits + 8
        TabRow = TabRow + 1
        Row = Row + 1
        if Row >= EndRow:
            if not ColFilled:
                _with46.LED_Table[TabRow - 1, TabCol] = '.'
            # Make sure that the last column contains at least one entry
            Row = M01.LEDsTAB_R
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
            Goto_List[GCol] = Get_Goto_Chars(Val(Par(ParNr)))
            #Col = Col + 1
            GCol = GCol + 1
            ParNr = ParNr + 1
        # VB2PY (UnhandledDefinition) Dim of implicit 'With' object (Goto_List) is not supported
        #Goto_List = vbObjectInitialize(((1, GCol - 1),), Variant, Goto_List)
        _with46.Goto_List = Goto_List
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: str - ByVal 
def Decode_Pattern_String(p_str):
    Pattern = Pattern_T()
    #-----------------------------------------------------
    # Examples to Decode:
    #   PatternT1(LED,4,InCh,6,5,128,0,PM_PINGPONG,1 Sek,3,192,0,48,0,12,0,3,192)
    if Decode_Pattern_String_to_Struct(p_str, Pattern):
        _with47 = Pattern
        OldEvents = X02.Application.EnableEvents
        X02.Application.EnableEvents = False
        Oldupdating = X02.Application.ScreenUpdating
        X02.Application.ScreenUpdating = False
        X02.RangeDict['Analoges_Überblenden'] = _with47.AnalogFading
        X02.RangeDict['ErsteRGBLED'] = _with47.FirstRGBLED
        X02.RangeDict['Startkanal'] = _with47.StartChannel
        X02.RangeDict['Bits_pro_Wert'] = _with47.BitsPerChannel
        X02.RangeDict['SchalterNr'] = _with47.SwitchNumber
        X02.RangeDict['Goto_Mode'] = _with47.Goto_Mode
        X02.RangeDict['Grafische_Anzeige'] = _with47.GraphicDisplay
        X02.RangeDict['Kanaele'] = _with47.Channels
        X02.RangeDict['Wert_Min'] = _with47.Min_Val
        X02.RangeDict['WertMax'] = _with47.Max_Val
        X02.RangeDict['Wert_ausgeschaltet'] = _with47.Val_Off
        X02.RangeDict['Mode'] = _with47.Mode
        # Fill the Duration table
        X02.Range(M01.Dauer_Rng).ClearContents()
        Dauer_Col = M01.Dauer_Col1
        for D in _with47.Duration:
            X02.CellDict[M01.Dauer_Row, Dauer_Col] = D
            Dauer_Col = Dauer_Col + 1
        # Fill then LEDs table
        X02.Range(M01.LEDsRANGE).ClearContents()
        Row = M01.LEDsTAB_R
        for LRow in vbForRange(1, UBound(_with47.LED_Table, 1)):
            Col = M01.LEDsTAB_C
            for LCol in vbForRange(1, UBound(_with47.LED_Table, 2)):
                X02.CellDict[Row, Col].Value = _with47.LED_Table(LRow, LCol)
                Col = Col + 1
            Row = Row + 1
        # Process the Goto Mode
        X02.Range(M01.GoTo_RNG).ClearContents()
        if isInitialised(_with47.Goto_List):
            Col = M01.GoTo_Col1
            for G in _with47.Goto_List:
                X02.CellDict[M01.GoTo_Row, Col] = G
                Col = Col + 1
        M02a.Global_Worksheet_Change(X02.Cells(1, 1))
        # Redraw everything
        X02.Application.EnableEvents = OldEvents
        X02.ActiveSheet.Calculate()
        X02.Application.ScreenUpdating = Oldupdating

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: str - ByVal 
def Decode_Pattern_String_and_Compare(p_str, Gen_Message=VBMissingArgument):
    _fn_return_value = None
    Org = String()

    Res = String()
    #------------------------------------------------------------------------------------------------------------------
    Org = Split(p_str, ')')(0) + ')'
    # Without comment
    Org = Replace(Org, '(LED,', '(0,')
    Org = Replace(Org, '(#LED,', '(0,')
    Org = Replace(Org, ',InCh,', ',SI_1,')
    Decode_Pattern_String(p_str)
    Res = Split(str(X02.Range(M01.ErgebnisRng)), ')')(0) + ')'
    if Org != Res:
        Debug.Print('')
        Debug.Print('Error importing macro:')
        Debug.Print('Org: ' + Org)
        Debug.Print('Res: ' + Res, '')
        if Gen_Message:
            X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler beim importieren des Makros aufgetreten ;-(' + vbCr + vbCr + 'Das Macro entspricht leider nicht genau dem original Macro.' + vbCr + 'Problem bitte an Hardi melden...'), vbCritical, pattgen.M09_Language.Get_Language_Str('Interne Fehler beim importieren des Macros'))
    else:
        _fn_return_value = True
    return _fn_return_value

def Test_Decode_Pattern_String_with_All_Examples():
    Sh = Variant()

    ErrCnt = Long()
    #UT-------------------------------------------------------
    # Attention the content in the actual sheet is changed
    for Sh in PG.ThisWorkbook.sheets:
        if pattgen.M08_Load_Sheet_Data.Is_Normal_Data_Sheet(Sh.Name, pattgen.M09_Language.Get_Language_Str('verglichen')) and Sh.Name != X02.ActiveSheet.Name:
            Debug.Print('Checking ' + Sh.Name)
            if Decode_Pattern_String_and_Compare(Sh.Range(M01.ErgebnisRng)):
                Debug.Print('O.k.')
            else:
                ErrCnt = ErrCnt + 1
    Debug.Print('*** All Sheets checked! ' + ErrCnt + ' Errors ***')

def Test_Decode_Pattern_String_by_Sheetname():
    Sh = Variant()
    #UT-------------------------------------------------------
    # Attention the content in the actual sheet is changed
    Sh = X02.Sheets('LocalVar Sound')
    Debug.Print('Checking ' + Sh.Name)
    if Decode_Pattern_String_and_Compare(Sh.Range(M01.ErgebnisRng)):
        Debug.Print(Sh.Name + ' O.k.')

def Import_From_Prog_Gen():
    #--------------------------------
    pattgen.M11_To_Prog_Gen.Select_Line_in_Prog_Gen_and_Call_Macro(False, Import_From_Prog_Gen_Callback)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Line - ByVal 
def Import_GotoActivation(Line):
    ActStr = '// Activation: '
    #------------------------------------------------------
    if Left(Line, Len(ActStr)) == ActStr:
        ActTxt = Mid(Line, Len(ActStr) + 1)
        X02.RangeDict['Goto_Aktivierung'] = ActTxt

def Import_From_Prog_Gen_Callback(OK_Pressed, Description, Macro, Row):
    global Add_To_This_Sheet_Default_Answer
    MacroName = String()

    Line = Variant()
    #--------------------------------------------------------------------------------------------------------------------
    PG.ThisWorkbook.Activate()
    if not OK_Pressed:
        return
    _select37 = Add_To_This_Sheet_Default_Answer
    if (_select37 == 1):
        Add_To_This_Sheet_Default_Answer = vbDefaultButton1
    elif (_select37 == 2):
        Add_To_This_Sheet_Default_Answer = vbDefaultButton2
    else:
        Add_To_This_Sheet_Default_Answer = vbDefaultButton2
    MacroName = 'Imported_Pattern'
    if Right(Description, Len(M01.FROM_PAT_CONFIG_TXT)) == M01.FROM_PAT_CONFIG_TXT:
        MacroName = Replace(Left(Description, Len(Description) - Len(M01.FROM_PAT_CONFIG_TXT)), ' ', '_')
        MacroName = M30.ValidNameCharacters(MacroName)
    _select38 = X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Soll die Zeile in das aktuelle Blatt eingefügt werden?' + vbCr + vbCr + 'Ja: Die Daten in diesem Blatt werden überschrieben' + vbCr + 'Nein: Es wird ein neues Blatt angelegt'), vbYesNoCancel + Add_To_This_Sheet_Default_Answer, pattgen.M09_Language.Get_Language_Str('Daten in aktuelles oder neues Blatt einfügen'))
    if (_select38 == vbYes):
        # Nothing
        Add_To_This_Sheet_Default_Answer = 1
    elif (_select38 == vbCancel):
        return
    elif (_select38 == vbNo):
        # Create new sheet
        Add_To_This_Sheet_Default_Answer = 2
        Name = X02.InputBox(pattgen.M09_Language.Get_Language_Str('Name des neuen Blattes?'), pattgen.M09_Language.Get_Language_Str('Neues Blatt anlegen'), M30.Unic_SheetName(MacroName, '_'))
        if Name == '':
            return
        pattgen.M08_Load_Sheet_Data.Create_New_Sheet(Name, Add_to_Duplicate_Name='_', AfterSheetName=M01.MAIN_SH)
        pattgen.M08_Load_Sheet_Data.Load_Textbox(M01.StdDescEdges + Chr(M01.pcfSep) + pattgen.M09_Language.Get_Language_Str(M01.StdDescStart))
        X02.RangeDict[M01.Macro_N_Rng] = M30.Replace_Illegal_Char(X02.ActiveSheet.Name)
        pattgen.M08_Load_Sheet_Data.Add_by_Hardi()
        X02.Range(M01.FirstLEDTabRANGE).Select()
        M30.Protect_Active_Sheet()
    X02.RangeDict['Makro_Name'] = MacroName
    X02.Range('Goto_Aktivierung').ClearContents()
    # Decode the imported macro line
    for Line in Split(Macro, vbLf):
        if InStr(Line, 'PatternT') > 0:
            Decode_Pattern_String_and_Compare(Line, True)
        else:
            Import_GotoActivation(Line)

# VB2PY (UntranslatedCode) Option Explicit
