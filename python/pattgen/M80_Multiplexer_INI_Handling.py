from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import ExcelAPI.XLWA_WinAPI as X03
import pattgen.M09_Language
import pattgen.M81_Create_Multiplexer_Ini
import pattgen.M80_Multiplexer_INI_Misc
import pattgen.M01_Public_Constants_a_Var as M01
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M30_Tools as M30
import pattgen.M02_Main as M02a
import pattgen.M17_Import_a_Dec_Macro
import pattgen.M07_Save_Sheet_Data
import pattgen.M12_Copy_Prog
import pattgen.M08_Load_Sheet_Data
import pattgen.D00_Forms as D00
import pattgen.Pattern_Generator as PG

"""--------------------------------------------------------------------------------------------'
                                                                                            '
   Date        :   22-4-2020                                                                '
                   Finished first version 0.90 on 3-5-2020.                                 '
                   Finished second version 0.99 on 20-5-2020.                               '
                   Final version 1.01 on 10-6-2020.                                         '
                   Updated to version 1.02 on 25-10-2020                                    '
                   Updated to version 1.03 on 06-02-2021                                    '
   Auteur      :   Misha van der Stam                                                       '
   Purpose     :   Managing and Testing Multiplexer Macro's in the "Multiplexer.ini" file.  '
                                                                                            '
--------------------------------------------------------------------------------------------'
-----------------------------------------------------------------------------------'
   Remarks     :   10-6-2020 Working version 1.01                                  '
                   - Implemented Pattern Timing                                    '
                   - Pattern Mode support for PM_NORMAL and PM_PINGPONG            '
                   - Implementation of Brightness                                  '
                   - Implementation of Goto Patterns                               '
                   - No implementation of Fading                                   '
                   - Support for Single LEDs and RGB LEDs                          '
                   - Simply copy Pattern into the Multiplexer                      '
                   - Tested on Windows 32 and Windows 64 bits systems.             '
                                                                                   '
                   25-10-2020 Version 1.02                                         '
                   - LEDs on picture not implemented in Multiplexer.               '
                     But earlier in version 2.0.0 of the Pattern_Configurator.     '
                   - Added the posibility to add Multiplexers to the Multiplexer   '
                     by Button.                                                    '
                   -                                                               '
                                                                                   '
                   06-02-2021 Version 1.03                                         '
                   - Added 'New Multiplexer' Button to add a empty multiplexer.    '
                   - Deleting a multiplexer is also deleting the empty multiplexer.'
                   - Resized the TOP Row buttons to free the version information.  '
                   -                                                               '
                                                                                   '
-----------------------------------------------------------------------------------'
-----------------------------------------------------------------------------------'
   ToDo        :                                                                   '
                   - Testing on more or less at changing number of shapes          '
                     and multiplexers                                              '
                   - Implement other Pattern Modes                                 '
                   - Implement Flags use (PF_...) in Mode                          '
                   - LEDs on Pictures                                              '
                                                                                   '
-----------------------------------------------------------------------------------'
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
For 64 Bit Systems
 04.06.20: Hardi: ToDo: Use ReDim
 11.06.20: Hardi: ToDo: Use ReDim
 1 Led_Name, 2 = Led_Pos_Size (l, t, h, w)
 Stores the last position of the dialog
 Next Goto Number. It's defined in the dialog "Select_GotoNr_Form"
 Trigger to start the LED animation
--------------------------------------------------------------------------------------------
---------------------------------------------------
---------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 2 on False
-----------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------
------------------------------------------
--------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------
TT-----------------------------------------------------------
UT----------------------------------
----------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
------------------------------------
"""

class WinPos_T:
    def __init__(self):
        self.Valid = Boolean()
        self.Left = Double()
        self.Top = Double()

Version = 'v1.03'
MULTIPLEXER_INI_FILE_NAME = 'Multiplexer.ini'
RED = 0
GREEN = 1
BLUE = 2
RGB_Val = 1
Color_Val = 2
LED_Type_Val = 3
Led_Name = 1
Led_Pos_Size = 2
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12
VK_CAPITAL = 0x14
VK_NUMLOCK = 0x90
VK_SCROLL = 0x91
SleepTime = Single()
PrevValue = Variant()
PrevWorkSheet = None #*HL
TargetWorkSheet = None #*HL
Multiplexer_Init = Boolean()
MacroNameInputOK = Boolean()
Test_Buttons = vbObjectInitialize((10000,), Boolean)
TestPatternButtonOn = Boolean()
TestLedButtonClearing = Boolean()
SingleLEDs = vbObjectInitialize(((1, 2000), (1, 100),), String)
LEDs_Config = vbObjectInitialize(((1, 800), (1, 2),), String)
OtherForm_Pos = WinPos_T()
Number_Of_Multiplexers = Integer()
ThreeD = Boolean()
Enable_DCC_Button = Integer()
LED_Nrs_OnOff = Boolean()
DisplayLEDs = Boolean()
DelayTimerOn = Boolean()
EditMode = Boolean()
Pos_Select_GotoNr_Form = WinPos_T()
GotoNr = Long()
RestartDisplay_Leds = Boolean()
# Enumeration 'GetKeyStateKeyboardCodes'
gksKeyboardShift = VK_SHIFT
gksKeyboardCtrl = VK_CONTROL
gksKeyboardAlt = VK_MENU
gksKeyboardCapsLock = VK_CAPITAL
gksKeyboardNumLock = VK_NUMLOCK
gksKeyboardScrollLock = VK_SCROLL

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lKey - ByVal 
def IsKeyPressed(lKey):
    _fn_return_value = None
    iResult = Integer()
    #--------------------------------------------------------------------------------------------
    iResult = X03.GetKeyState(lKey)
    _select70 = lKey
    if (_select70 == gksKeyboardCapsLock) or (_select70 == gksKeyboardNumLock) or (_select70 == gksKeyboardScrollLock):
        #For the three 'toggle' keys, the 1st bit says if it's
        #on or off, so clear any other bits that might be set,
        #using a binary AND
        iResult = iResult and 1
    else:
        #For the other keys, the 16th bit says if it's down or
        #up, so clear any other bits that might be set, using a
        #binary AND
        iResult = iResult and 0x8000
    _fn_return_value = ( iResult != 0 )
    return _fn_return_value

def Unlock_Excel():
    #---------------------------------------------------
    X02.Application.ScreenUpdating = True
    X02.Application.EnableEvents = True

def Conv2Bool(Txt):
    _fn_return_value = False #*HL
    # 03.06.20: Hardi
    #---------------------------------------------------
    _select71 = Txt
    if (_select71 == 'Waar') or (_select71 == 'True') or (_select71 == 'Wahr') or (_select71 == '1'):
        _fn_return_value = True
    return _fn_return_value

def Load_Multiplexer():
    global SleepTime, Number_Of_Multiplexers, ThreeD, Enable_DCC_Button, LED_Nrs_OnOff, DisplayLEDs, Multiplexer_Init
    IniFileName = Variant()

    Map = Variant()

    sectnNames = vbObjectInitialize(objtype=String)

    strBuffer = String()

    tmp = String()

    intx = Variant()

    SectionCount = Integer()

    strfullpath = String()

    MacroRow = Integer()

    MacroNr = Integer()

    LED_Type = Variant()

    Done = Boolean()
    #--------------------------------------------------------------------------------------------
    SleepTime = 0
    # For debugging used with time in seconds (1.5 is one and a half second)!
    X02.ActiveWindow.DisplayHeadings = False
    # Defaults
    Number_Of_Multiplexers = 3
    ThreeD = True
    Enable_DCC_Button = 1
    # 10.02.21: Misha
    LED_Nrs_OnOff = True
    DisplayLEDs = True
    X02.Application.ScreenUpdating = True
    X02.Application.EnableEvents = True
    #Sub to load all of the ini section names into array 'sectnNames().
    Debug.Print('Start loading Multiplexer.')
    Map = Environ('USERPROFILE') + '\\Documents\\' + 'MyPattern_Config_Examples'
    IniFileName = Map + '\\' + MULTIPLEXER_INI_FILE_NAME
    if X02.Dir(IniFileName) == '':
        # 04.06.20: Hardi: Changed Messages
        #                  ToDo: The ini file is saved automatically. The Message that the user has to save it is not necessary
        if X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler die \'Multiplexer.ini\' Datei existiert nicht:') + vbCr + '  \'' + IniFileName + '\'' + vbCr + vbCr + pattgen.M09_Language.Get_Language_Str('Eine neue \'Multiplexer.ini\' wird erstellt.') + vbCr + vbCr + pattgen.M09_Language.Get_Language_Str('Soll die Datei mit Beispiel Daten generiert werden?'), vbQuestion + vbYesNo, pattgen.M09_Language.Get_Language_Str('Multiplexer Datei nicht vorhanden')) == vbYes:
            if pattgen.M81_Create_Multiplexer_Ini.Create_Example_Ini_File(IniFileName) == False:
                Create_Multiplexer_Ini()
            # 04.06.20: Hardi
        else:
            Create_Multiplexer_Ini
    if not X02.Dir(IniFileName) != '':
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler die Datei existiert nicht:') + vbCr + '  \'' + IniFileName + '\'' + vbCrLf + vbCrLf + pattgen.M09_Language.Get_Language_Str('Eine neue \'Multiplexer.ini\' wird erstellt. Vergessen Sie nicht, Ihre Änderungen zu speichern!'), vbCritical, pattgen.M09_Language.Get_Language_Str('Multiplexer Datei nicht gefunden!'))
        Create_Multiplexer_Ini
    X02.Application.EnableEvents = False
    Multiplexer_Init = True
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    StatusMsg_UserForm.Add_Dot_to_ActSheet_Label()
    # Get Defaults
    X02.CellDict[2, X02.Range('Multiplexer.ini_file_date').Column].Value = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString('Multiplexer_Macro', 'INI_File_Production_Date')
    Number_Of_Multiplexers = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString('Multiplexer_Macro', 'Number_Of_Multiplexers')
    ThreeD = Conv2Bool(pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString('Multiplexer_Macro', 'ThreeD'))
    # 03.06.20: Hardi: Added Conv2Bool()
    LED_Nrs_OnOff = Conv2Bool(pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString('Multiplexer_Macro', 'LED_Nrs_OnOff'))
    DisplayLEDs = Conv2Bool(pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString('Multiplexer_Macro', 'DisplayLEDs'))
    Load_Button_Row
    if not DisplayLEDs:
        Delete_All_LEDs()
    MacroRow = 4
    MacroNr = 1
    for MacroNr in vbForRange(1, Number_Of_Multiplexers):
        StatusMsg_UserForm.Add_Dot_to_ActSheet_Label()
        #        Call Load_Buttons(MacroNr, MacroRow - 1)
        # 10.02.21: 20201025 Misha. Waarom aanroep met MacroRow-1 ?
        Load_Buttons(MacroNr, MacroRow)
        # 10.02.21: 20201025 Misha. Voor test zonder -1 ?
        Load_New_Multiplexer_Rows(MacroNr, MacroRow)
        MacroRow = MacroRow + 28
    MacroNr = Number_Of_Multiplexers
    # 10.02.21:
    Erase(sectnNames)
    StatusMsg_UserForm.Add_Dot_to_ActSheet_Label()
    strfullpath = IniFileName
    # Get Path and Name of "Multiplexer.ini" file.
    strBuffer = String(1000, Chr(0))
    # Size of strBuffer$ = 1000, filled with 0 (zero's).
    X03.GetPrivateProfileSectionNames(strBuffer, Len(strBuffer), strfullpath)
    sectnNames = Split(strBuffer, vbNullChar)
    for intx in vbForRange(LBound(sectnNames), UBound(sectnNames)):
        if sectnNames(intx) == vbNullString:
            break
        SectionCount = SectionCount + 1
    if SectionCount > 3:
        MacroRow = 4
        MacroNr = 1
        intx = 0
        #        While sectnNames(intx) <> vbNullString
        while sectnNames(intx) != vbNullString and MacroNr <= Number_Of_Multiplexers:
            # 10.02.21:
            Debug.Print(sectnNames(intx))
            Load_Section(sectnNames(intx), MacroNr, MacroRow, Done)
            X02.Application.ScreenUpdating = False
            X02.Application.EnableEvents = False
            if Done:
                LED_Type = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnNames(intx), 'LED_Type')
                if LED_Type == 'RGB LEDs':
                    X02.Worksheets['Multiplexer'].OptionButtons['RGB_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Value = True
                elif LED_Type == 'Single LEDs':
                    X02.Worksheets['Multiplexer'].OptionButtons['Single_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Value = True
                X02.Worksheets['Multiplexer'].OptionButtons['RGB_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Enabled = False
                X02.Worksheets['Multiplexer'].OptionButtons['Single_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Enabled = False
                if DisplayLEDs:
                    Load_Shapes(MacroNr, MacroRow - 1)()
                if intx > 2:
                    MacroNr = MacroNr + 1
                    MacroRow = MacroRow + 28
            intx = intx + 1
    Erase(sectnNames)
    if SectionCount <= 3:
        Create_Multiplexer_Ini()
    StatusMsg_UserForm.Add_Dot_to_ActSheet_Label()
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_ProtectShapes(True)
    Multiplexer_Init = False
    X02.Application.ScreenUpdating = True
    X02.Application.EnableEvents = True
    StatusMsg_UserForm.Add_Dot_to_ActSheet_Label()
    MacroRow = 4
    X02.Cells(MacroRow, X02.Range('Multiplexer_Name').Column).Select()
    Debug.Print('Loading Multiplexer ready.')

def Reload_Multiplexer():
    #--------------------------------------------------------------------------------------------
    if Delete_All_Multiplexers(False):
        Debug.Print('Multiplexer_Reload_Click')
        # 10.02.21: New Block
        X02.Sheets['Multiplexer'].Visible = True
        X02.Worksheets('Multiplexer').Select()
        StatusMsg_UserForm.Show()
        StatusMsg_UserForm.Set_Label(pattgen.M09_Language.Get_Language_Str('Lade Multiplexer...'))
        StatusMsg_UserForm.Set_ActSheet_Label('          ')
        # Left border for the dot's (Depends on the number of expexted dots)
        Load_Multiplexer
        X02.Unload(StatusMsg_UserForm)
        # 10.02.21:

def Load_Section(sectnName, MacroNr, MacroRow, Done):
    global Number_Of_Multiplexers, ThreeD, LED_Nrs_OnOff, DisplayLEDs, SingleLEDs
    Row = Integer()

    OptionNr = Variant()

    NumberOfLEDs = Integer()

    ChNr = Variant()

    ParamNr = Integer()

    MacroCodeNr = Variant()

    LED_Type = Variant()

    message = String()

    Params = vbObjectInitialize(objtype=String)

    Value = String()
    #--------------------------------------------------------------------------------------------
    Done = False
    if Left(sectnName, Len('Multiplexer_')) == 'Multiplexer_':
        PG.ThisWorkbook.Sheets('Multiplexer').Select()
        X02.Application.EnableEvents = False
        X02.Application.ScreenUpdating = False
        pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
        _select72 = sectnName
        if (_select72 == 'Multiplexer_Macro'):
            X02.CellDict[2, X02.Range('Multiplexer.ini_file_date').Column].Value = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'INI_File_Production_Date')
            Number_Of_Multiplexers = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'Number_Of_Multiplexers')
            ThreeD = Conv2Bool(pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'ThreeD'))
            # 03.06.20: Hardi: Added Conv2Bool()
            LED_Nrs_OnOff = Conv2Bool(pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'LED_Nrs_OnOff'))
            DisplayLEDs = Conv2Bool(pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'DisplayLEDs'))
        else:
            MacroCodeNr = 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'
            NumberOfLEDs = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'Number_Of_LEDs')
            X02.CellDict[MacroRow, X02.Range('Number_Of_LEDs').Column].Value = NumberOfLEDs
            pattgen.M80_Multiplexer_INI_Misc.Format_Multiplexer_Group(MacroRow, X02.Range('Number_Of_LEDs').Column)
            Show_LED_Numbers(MacroRow + 1, X02.Range('Number_Of_LEDs').Column, NumberOfLEDs)
            X02.CellDict[MacroRow, X02.Range('Macro_Description').Column - 1].Value = pattgen.M09_Language.Get_Language_Str('Multiplexer beschreibung') + ' : '
            X02.CellDict[MacroRow, X02.Range('Macro_Description').Column].Value = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'Description')
            pattgen.M80_Multiplexer_INI_Misc.Format_Row(X02.Cells(MacroRow, X02.Range('Macro_Description').Column))
            X02.CellDict[MacroRow, X02.Range('Multiplexer_Name').Column + 1].Value = MacroCodeNr
            X02.CellDict[MacroRow, X02.Range('Multiplexer_Name').Column - 1].Value = pattgen.M09_Language.Get_Language_Str('Multiplexer Name') + ' : '
            X02.CellDict[MacroRow, X02.Range('Multiplexer_Name').Column].Value = sectnName
            pattgen.M80_Multiplexer_INI_Misc.Format_Row(X02.Cells(MacroRow, X02.Range('Multiplexer_Name').Column))
            LED_Type = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'LED_Type')
            Row = 2
            for OptionNr in vbForRange(1, 8):
                MacroCodeNr = Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2)
                X02.Application.EnableEvents = False
                X02.CellDict[MacroRow + Row, X02.Range('Multiplexer_Name').Column - 1].Value = pattgen.M09_Language.Get_Language_Str('Option ') + OptionNr + pattgen.M09_Language.Get_Language_Str(' Name') + '    : '
                X02.CellDict[MacroRow + Row, X02.Range('Multiplexer_Name').Column].Value = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'Option ' + OptionNr + ' Name')
                pattgen.M80_Multiplexer_INI_Misc.Format_Row(X02.Range(X02.Cells(MacroRow + Row, 3).Address(), X02.Cells(MacroRow + Row, 6).Address()))
                X02.Application.EnableEvents = False
                X02.CellDict[MacroRow + Row + 1, X02.Range('Multiplexer_Name').Column - 1].Value = pattgen.M09_Language.Get_Language_Str('Option ') + OptionNr + pattgen.M09_Language.Get_Language_Str(' Muster') + ' : '
                X02.CellDict[MacroRow + Row + 1, X02.Range('Multiplexer_Name').Column].Value = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'Option ' + OptionNr + ' Pattern')
                pattgen.M80_Multiplexer_INI_Misc.Format_Row(X02.Range(X02.Cells(MacroRow + Row + 1, 3).Address(), X02.Cells(MacroRow + Row + 1, 6).Address()))
                X02.Application.EnableEvents = False
                X02.CellDict[MacroRow + Row + 2, 1].RowHeight = 10
                if LED_Type == 'Single LEDs':
                    Value = ''
                    Value = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'Option ' + OptionNr + ' SingleLED_Colors')
                    if Value == '':
                        Value = X02.Cells(MacroRow + Row + 1, X02.Range('Macro_Description').Column + 1).Value
                    else:
                        _with86 = X02.Cells(MacroRow + Row + 1, X02.Range('Macro_Description').Column + 1)
                        _with86.Value = Value
                        _with86.Font.Color = - 2236963
                        _with86.Font.TintAndShade = 0
                    if Value != '' and not Value == 'To be filled!':
                        Params = Split(Value, ',')
                        ParamNr = 0
                        for ChNr in vbForRange(1, NumberOfLEDs):
                            Value = Params(ChNr + ParamNr) + ',' + Params(ChNr + ParamNr + 1) + ',' + Params(ChNr + ParamNr + 2)
                            SingleLEDs[MacroNr * 100 + OptionNr, ChNr] = Value
                            ParamNr = ParamNr + 2
                Row = Row + 3
            Done = True
    else:
        # No Multiplexer Macro section!
        Done = False

def Load_MacroOption_SingleLEDs_Colors(sectnName, MacroNr, OptionNr, NumberOfLEDs):
    global SingleLEDs
    ChNr = Variant()

    ParamNr = Integer()

    Value = String()

    Params = vbObjectInitialize(objtype=String)
    #--------------------------------------------------------------------------------------------
    Value = pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString(sectnName, 'Option ' + OptionNr + ' SingleLED_Colors')
    if Value != '':
        Params = Split(Value, ',')
        ParamNr = 0
        for ChNr in vbForRange(1, NumberOfLEDs):
            Value = Params(ChNr + ParamNr) + ',' + Params(ChNr + ParamNr + 1) + ',' + Params(ChNr + ParamNr + 2)
            SingleLEDs[MacroNr * 100 + OptionNr, ChNr] = Value
            ParamNr = ParamNr + 2

def Load_Shapes(MacroNr, MacroRow, New_Multiplexer_Ini_File=VBMissingArgument):
    Target = X02.Range()

    Row = Integer()

    OptionNr = Integer()

    MacroCodeNr = String()

    NumberOfLEDs = Long()
    #--------------------------------------------------------------------------------------------
    X02.Application.ScreenUpdating = False
    PG.ThisWorkbook.Sheets('Multiplexer').Select()
    Row = 3
    NumberOfLEDs = X02.Cells(MacroRow + 1, X02.Range('Number_Of_LEDs').Column).Value
    for OptionNr in vbForRange(1, 8):
        MacroCodeNr = 'M' + Right('00' + CStr(MacroNr), 2) + 'O' + Right('00' + CStr(OptionNr), 2)
        Target = X02.Range('Multiplexer_Name')
        X02.Application.EnableEvents = False
        Add_LEDs_in_ActiveCell(Target.offset(MacroRow + Row, 6), MacroCodeNr, NumberOfLEDs)
        Row = Row + 3

def Load_Buttons(MacroNr, MacroRow, New_Multiplexer_Ini_File=VBMissingArgument):
    Target = X02.Range()

    Row = Integer()

    OptionNr = Integer()

    MacroCodeNr = String()
    #--------------------------------------------------------------------------------------------
    PG.ThisWorkbook.Sheets('Multiplexer').Select()
    MacroCodeNr = 'M' + Right('00' + CStr(MacroNr), 2) + 'O' + Right('00' + CStr(OptionNr), 2)
    Add_ControlForm_Button_in_ActiveCell(MacroCodeNr, 'GroupBox', VBGetMissingArgument(Add_ControlForm_Button_in_ActiveCell, 2), MacroRow)
    Add_ControlForm_Button_in_ActiveCell(MacroCodeNr, 'Delete_Multiplexer', VBGetMissingArgument(Add_ControlForm_Button_in_ActiveCell, 2), MacroRow)
    Row = 2
    for OptionNr in vbForRange(1, 8):
        MacroCodeNr = Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2)
        Add_ControlForm_Button_in_ActiveCell(MacroCodeNr, 'Test_Leds', OptionNr, MacroRow + Row + 1)
        Add_ControlForm_Button_in_ActiveCell(MacroCodeNr, 'Add Option', OptionNr, MacroRow - 1 + Row)
        Row = Row + 3

def Load_Button_Row():
    Target = X02.Range()

    Row = Variant()

    t = Variant()

    l = Integer()

    OptionNr = Integer()

    MacroCodeNr = String()

    Sh = Icon()

    WorkingPath = String()
    #--------------------------------------------------------------------------------------------
    PG.ThisWorkbook.Sheets('Multiplexer').Select()
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    Delete_Button_Row_Shapes
    X02.Columns[1].ColumnWidth = 8
    X02.Columns[2].ColumnWidth = 23
    X02.Columns[3].ColumnWidth = 37
    X02.Columns[4].ColumnWidth = 14
    X02.Columns[5].ColumnWidth = 30
    X02.Columns[6].ColumnWidth = 50
    X02.Columns[7].ColumnWidth = 16
    X02.Columns[8].ColumnWidth = 8
    X02.Range[X02.Columns(9), X02.Columns(42)].ColumnWidth = 5
    X02.Range[X02.Rows(1).Address(), X02.Rows(2).Address()].RowHeight = 27
    Add_ControlForm_Button_in_ActiveCell('', 'New Multiplexer', VBGetMissingArgument(Add_ControlForm_Button_in_ActiveCell, 2), X02.Range('Multiplexer_Name').Row)
    # 10.02.21: Enabled abain
    Add_ControlForm_Button_in_ActiveCell('', 'Save Multiplexer', VBGetMissingArgument(Add_ControlForm_Button_in_ActiveCell, 2), X02.Range('Multiplexer_Name').Row)
    Add_ControlForm_Button_in_ActiveCell('', 'Reload Multiplexer', VBGetMissingArgument(Add_ControlForm_Button_in_ActiveCell, 2), X02.Range('Macro_Description').Row)
    Add_ControlForm_Button_in_ActiveCell('', 'Close Multiplexer', VBGetMissingArgument(Add_ControlForm_Button_in_ActiveCell, 2), X02.Range('Macro_Description').Row)
    X02.CellDict[X02.Range('Multiplexer.ini_file_date').Row - 1, X02.Range('Multiplexer.ini_file_date').Column].Value = 'Multiplexer.ini file date : '
    X02.CellDict[X02.Range('Number_Of_LEDs').Row, X02.Range('Number_Of_LEDs').Column + 5].Value = 'Help --->'
    #Cells(Range("Number_Of_LEDs").Row + 1, Range("Number_Of_LEDs").Column - 3).Value = "Version : "
    # Is already contained in the string
    # 11.06.20: Hardi
    X02.CellDict[X02.Range('Number_Of_LEDs').Row + 1, X02.Range('Number_Of_LEDs').Column - 2].Value = X02.Sheets(M01.MAIN_SH).Range('MainVersion')
    # 11.06.20: Hardi: Using the same version number than the main sheet to prevent confusing the user
    X02.CellDict[X02.Range('Number_Of_LEDs').Row + 1, X02.Range('Number_Of_LEDs').Column + 5].Value = 'By Misha'
    WorkingPath = PG.ThisWorkbook.Path
    X02.ActiveSheet.Pictures.Insert(WorkingPath + '\\Icons\\WikiMLL_v5.ico').Select()
    t = X02.Cells(X02.Range('Number_Of_LEDs').Row, X02.Range('Number_Of_LEDs').Column + 7).Top
    l = X02.Cells(X02.Range('Number_Of_LEDs').Row, X02.Range('Number_Of_LEDs').Column + 7).Left
    _with87 = X02.Selection.ShapeRange
    _with87.Top = t + 5
    _with87.Left = l + 10
    _with87.Height = 45
    _with87.Width = 45
    _with87.Name = 'WikiMLL'
    _with87.AlternativeText = 'URL to MLL WiKi.'
    #        ActiveSheet.Hyperlinks.Add Anchor:=.Item(1), Address:="https://wiki.mobaledlib.de/anleitungen/spezial/multiplexing"
    X02.ActiveSheet.Hyperlinks.Add(Anchor=_with87.Item(1), Address=pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString('Multiplexer_Macro', 'WiKi_URL'))
    Debug.Print('65 Loading ButtonRow Ready! : ' + MacroCodeNr)

def Show_LED_Numbers(MacroRow, Col, NumberOfLEDs):
    LedNr = Integer()
    #--------------------------------------------------------------------------------------------
    if not DisplayLEDs and NumberOfLEDs != 0:
        for LedNr in vbForRange(1, NumberOfLEDs):
            X02.CellDict[MacroRow, Col - 1 + LedNr].Value = LedNr
            _with88 = X02.Cells(MacroRow, Col - 1 + LedNr)
            _with88.HorizontalAlignment = X01.xlCenter
            _with88.VerticalAlignment = X01.xlBottom
            _with88.WrapText = False
            _with88.Orientation = 0
            _with88.AddIndent = False
            _with88.IndentLevel = 0
            _with88.ShrinkToFit = False
            _with88.ReadingOrder = X01.xlContext
            _with88.MergeCells = False
    else:
        if NumberOfLEDs == 0:
            NumberOfLEDs = 32
        for LedNr in vbForRange(1, NumberOfLEDs):
            X02.CellDict[MacroRow, Col - 1 + LedNr].Value = ''

def Test_Delete_Multiplexer():
    MacroCodeNr = String()
    #--------------------------------------------------------------------------------------------
    MacroCodeNr = 'M01O00'
    Delete_Multiplexer(MacroCodeNr, False)

def Delete_Multiplexer(MacroCodeNr, Delete_All_Multiplexer):
    global Number_Of_Multiplexers
    Found = Boolean()

    Answer = String()

    MacroName = String()

    Target = X02.Range()

    TargetMacroNr = Integer()

    TargetMacroCodeNr = Variant()

    DeletedMacroCodeNr = String()

    MacroRow = Integer()

    DeletedMacroNr = Integer()
    #--------------------------------------------------------------------------------------------
    X02.Worksheets('Multiplexer').Select()
    X02.Application.ScreenUpdating = False
    X02.Application.EnableEvents = False
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    Found = False
    for MacroRow in vbForRange(4, 400, 28):
        if X02.Cells(MacroRow, X02.Range('MultiplexerNumber').Column).Value == MacroCodeNr:
            Found = True
            break
    if not Found:
        Beep()
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Multiplexer ') + MacroCodeNr + pattgen.M09_Language.Get_Language_Str(' NICHT gefunden!'))
        return
    MacroName = X02.Cells(MacroRow, 3).Value
    if not Delete_All_Multiplexer:
        Beep()
        Answer = pattgen.M09_Language.Get_Language_Str('Möchten Sie das Multiplexer-Makro wirklich entfernen? ') + vbCrLf + vbCrLf + '" ' + MacroName + ' "'
        Answer = X02.MsgBox(Answer, vbQuestion + vbYesNo + vbDefaultButton2, pattgen.M09_Language.Get_Language_Str('Deleting Multiplexer ...'))
        if Answer == vbNo:
            MacroName = vbNo
            return
    Target = X02.Range('Multiplexer_Name')
    DeletedMacroNr = Val(Right(Left(Target.offset(MacroRow - 1, 1).Value, 3), 2))
    # 10.02.21: 20210206 Misha, caused by adding a 'New Multiplexer' button there is no need to keep empty multiplexers.
    # So deleting meens also delete the empty multiplexer. 'If' function not needed anymore!
    #    If Not Cells(MacroRow + 28, 4).Value = "" Then
    while not X02.Cells(MacroRow + 28, 4).Value == '':
        Target = X02.Range('Multiplexer_Name')
        TargetMacroNr = Val(Right(Left(Target.offset(MacroRow - 1 + 28, 1), 3), 2))
        Delete_Multiplexer_Rows(MacroRow)
        X02.Application.ScreenUpdating = False
        X02.Application.EnableEvents = False
        Show_LED_Numbers(MacroRow + 1, X02.Range('Number_Of_LEDs').Column, 0)
        Copy_Multiplexer_Rows(MacroRow)
        if DisplayLEDs:
            Load_Shapes(DeletedMacroNr, MacroRow)()
        if X02.Cells(MacroRow + 29, 4).Value != '':
            Delete_Multiplexer_Rows(MacroRow + 29)
            Show_LED_Numbers(MacroRow + 29 + 1, X02.Range('Number_Of_LEDs').Column, 0)
        MacroRow = MacroRow + 1 + 28
        DeletedMacroNr = TargetMacroNr
    #    Else
    # 10.02.21: 20210206 Misha
    Number_Of_Multiplexers = Number_Of_Multiplexers - 1
    DeletedMacroCodeNr = 'M' + Right('00' + CStr(DeletedMacroNr), 2) + 'O00'
    Show_LED_Numbers(MacroRow + 1, X02.Range('Number_Of_LEDs').Column, 0)
    Clear_Multiplexer(DeletedMacroNr, MacroRow)
    # 10.02.21:
    Delete_Shapes(DeletedMacroCodeNr)
    Delete_Multiplexer_Rows(MacroRow)
    #    End If
    # 20210206 Misha
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    X02.ActiveSheet.Shapes['Save_Multiplexer'].Fill.ForeColor.rgb = rgb(0, 230, 255)
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_ProtectShapes(True)
    MacroRow = 3
    Target = X02.Range('Multiplexer_Name')
    X02.Application.EnableEvents = False
    Target.offset(3, 0).Select()

def Copy_Multiplexer_Rows(MacroRow):
    Target = X02.Range()

    DeletedMacroCodeNr = String()

    TargetMacroCodeNr = String()

    TargetMacroNr = Integer()

    DeletedMacroNr = Integer()

    OptionNr = Variant()

    Row = Variant()

    MacroNr = Integer()

    NumberOfLEDs = Integer()

    LED_Type = Boolean()
    #--------------------------------------------------------------------------------------------
    X02.Worksheets('Multiplexer').Select()
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    X02.Application.ScreenUpdating = False
    X02.Application.EnableEvents = False
    Target = X02.Range('Multiplexer_Name')
    DeletedMacroNr = Val(Right(Left(Target.offset(MacroRow - 1, 1).Value, 3), 2))
    Row = 0
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    MacroRow = MacroRow - 1
    Target = X02.Range('Multiplexer_Name')
    TargetMacroNr = Val(Right(Left(Target.offset(MacroRow + 28, 1).Value, 3), 2))
    if TargetMacroNr != 0:
        OptionNr = 0
        TargetMacroCodeNr = 'M' + Right('00' + CStr(TargetMacroNr), 2) + 'O' + Right('00' + CStr(OptionNr), 2)
        X02.Worksheets['Multiplexer'].OptionButtons['RGB_LEDs_' + 'M' + Right('00' + CStr(DeletedMacroNr), 2) + 'O00'].Value = X02.Worksheets('Multiplexer').OptionButtons('RGB_LEDs_' + 'M' + Right('00' + CStr(TargetMacroNr), 2) + 'O00').Value
        X02.Worksheets['Multiplexer'].OptionButtons['RGB_LEDs_' + 'M' + Right('00' + CStr(DeletedMacroNr), 2) + 'O00'].Enabled = False
        X02.Worksheets['Multiplexer'].OptionButtons['Single_LEDs_' + 'M' + Right('00' + CStr(DeletedMacroNr), 2) + 'O00'].Value = X02.Worksheets('Multiplexer').OptionButtons('Single_LEDs_' + 'M' + Right('00' + CStr(TargetMacroNr), 2) + 'O00').Value
        X02.Worksheets['Multiplexer'].OptionButtons['Single_LEDs_' + 'M' + Right('00' + CStr(DeletedMacroNr), 2) + 'O00'].Enabled = False
        Target = X02.Range('Number_Of_LEDs')
        X02.Application.EnableEvents = False
        Target.offset[MacroRow, 0].Value = X02.Cells(MacroRow + 1 + 28, X02.Range('Number_Of_LEDs').Column).Value
        NumberOfLEDs = X02.Cells(MacroRow + 1 + 28, X02.Range('Number_Of_LEDs').Column).Value
        X02.CellDict[MacroRow + 1, X02.Range('Number_Of_LEDs').Column].Locked = True
        Target = X02.Range('Macro_Description')
        X02.Application.EnableEvents = False
        Target.offset[MacroRow, 0].Value = X02.Cells(MacroRow + 1 + 28, X02.Range('Macro_Description').Column).Value
        Target = X02.Range('Multiplexer_Name')
        X02.Application.EnableEvents = False
        Target.offset[MacroRow + Row, 0].Value = X02.Cells(MacroRow + 1 + 28, X02.Range('Multiplexer_Name').Column).Value
        # Add LEDs
        Row = 3
        for OptionNr in vbForRange(1, 8):
            Target = X02.Range('Multiplexer_Name')
            X02.Application.EnableEvents = False
            Target.offset[MacroRow - 1 + Row, 0].Value = X02.Cells(MacroRow + Row + 28, X02.Range('Multiplexer_Name').Column).Value
            X02.Application.EnableEvents = False
            Target.offset[MacroRow - 1 + Row + 1, 0].Value = X02.Cells(MacroRow + Row + 1 + 28, X02.Range('Multiplexer_Name').Column).Value
            X02.Application.EnableEvents = False
            _with89 = Target.offset(MacroRow - 1 + Row + 1, 4)
            _with89.Value = X02.Cells(MacroRow + Row + 1 + 28, X02.Range('Multiplexer_Name').Column + 4).Value
            _with89.Font.Color = - 2236963
            _with89.Font.TintAndShade = 0
            Row = Row + 3
        Show_LED_Numbers(MacroRow + 2, X02.Range('Number_Of_LEDs').Column, NumberOfLEDs)

def Delete_Multiplexer_Rows(MacroRow):
    Target = X02.Range()

    DeletedMacroCodeNr = String()

    TargetMacroCodeNr = String()

    TargetMacroNr = Integer()

    DeletedMacroNr = Integer()

    OptionNr = Variant()

    Row = Integer()

    NumberOfLEDs = Long()

    LED_Type = Boolean()
    #--------------------------------------------------------------------------------------------
    X02.Worksheets('Multiplexer').Select()
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    X02.Application.ScreenUpdating = False
    X02.Application.EnableEvents = False
    Target = X02.Range('Multiplexer_Name')
    DeletedMacroCodeNr = Target.offset(MacroRow - 1, 1).Value
    DeletedMacroNr = Val(Right(Left(DeletedMacroCodeNr, 3), 2))
    NumberOfLEDs = X02.Cells(MacroRow, X02.Range('Number_Of_LEDs').Column).Value
    Delete_Shapes(DeletedMacroCodeNr, NumberOfLEDs)
    if DeletedMacroNr > Number_Of_Multiplexers:
        X02.Range(X02.Rows(MacroRow).Address(), X02.Rows(MacroRow + 27).Address()).Delete()
        # Rename Buttons and Shapes to new position
        Row = 0
        while not X02.Cells(MacroRow, 4).Value == '':
            pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
            Target = X02.Range('Multiplexer_Name')
            TargetMacroNr = Val(Right(Left(Target.offset(MacroRow - 1, 1).Value, 3), 2))
            if X02.Worksheets('Multiplexer').OptionButtons('RGB_LEDs_' + 'M' + Right('00' + CStr(TargetMacroNr), 2) + 'O00').Value == 1:
                LED_Type = True
            elif X02.Worksheets('Multiplexer').OptionButtons('Single_LEDs_' + 'M' + Right('00' + CStr(TargetMacroNr), 2) + 'O00').Value == 1:
                LED_Type = False
            OptionNr = 0
            DeletedMacroCodeNr = 'M' + Right('00' + CStr(DeletedMacroNr), 2) + 'O' + Right('00' + CStr(OptionNr), 2)
            Target = X02.Range('Multiplexer_Name')
            Target.offset[MacroRow + Row - 1, 1].Value = DeletedMacroCodeNr
            TargetMacroCodeNr = 'M' + Right('00' + CStr(TargetMacroNr), 2) + 'O' + Right('00' + CStr(OptionNr), 2)
            pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
            Delete_Shapes(TargetMacroCodeNr, NumberOfLEDs)
            Load_Buttons(DeletedMacroNr, MacroRow - 1)
            if LED_Type:
                X02.Worksheets['Multiplexer'].OptionButtons['RGB_LEDs_' + 'M' + Right('00' + CStr(DeletedMacroNr), 2) + 'O00'].Value = True
            else:
                X02.Worksheets['Multiplexer'].OptionButtons['Single_LEDs_' + 'M' + Right('00' + CStr(DeletedMacroNr), 2) + 'O00'].Value = True
            X02.Worksheets['Multiplexer'].OptionButtons['RGB_LEDs_' + 'M' + Right('00' + CStr(DeletedMacroNr), 2) + 'O00'].Enabled = False
            X02.Worksheets['Multiplexer'].OptionButtons['Single_LEDs_' + 'M' + Right('00' + CStr(DeletedMacroNr), 2) + 'O00'].Enabled = False
            # Add LEDs
            Row = 3
            NumberOfLEDs = X02.Cells(MacroRow, X02.Range('Number_Of_LEDs').Column).Value
            for OptionNr in vbForRange(1, 8):
                # LED_M01O01L1
                DeletedMacroCodeNr = 'M' + Right('00' + CStr(DeletedMacroNr), 2) + 'O' + Right('00' + CStr(OptionNr), 2)
                Target = X02.Range('Multiplexer_Name')
                Add_LEDs_in_ActiveCell(Target.offset(MacroRow + Row - 1, 5), DeletedMacroCodeNr, NumberOfLEDs)
                Row = Row + 3
            Row = 0
            MacroRow = MacroRow + 28
            DeletedMacroNr = TargetMacroNr
    else:
        Clear_Multiplexer(DeletedMacroNr, MacroRow)
    if X02.Cells(4, 4).Value == '':
        # No more Multiplexer's in "Multiplexer" !
        PG.ThisWorkbook.Sheets['Multiplexer'].Range['Multiplexer.ini_file_date'].Value = ''
        return

def Delete_All_Multiplexers(FirstLoad):
    _fn_return_value = None
    MacroRow = Variant()

    Answer = Integer()

    MacroCodeNr = String()
    #--------------------------------------------------------------------------------------------
    if not FirstLoad:
        Beep()
        Answer = X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Möchten Sie wirklich alle Multiplexer Makros löschen?') + vbCrLf + pattgen.M09_Language.Get_Language_Str('und die Multiplexer Datei neu laden?') + vbCrLf + vbCrLf + pattgen.M09_Language.Get_Language_Str('Alle Änderungen werden ignoriert!'), vbQuestion + vbYesNo + vbDefaultButton2, pattgen.M09_Language.Get_Language_Str('Alle Multiplexer löschen ...'))
        if Answer == vbNo:
            _fn_return_value = False
            return _fn_return_value
    StatusMsg_UserForm.Show()
    # 10.02.21:
    StatusMsg_UserForm.Set_Label(pattgen.M09_Language.Get_Language_Str('Deleting Multiplexers...'))
    StatusMsg_UserForm.Set_ActSheet_Label('          ')
    # Left border for the dot's (Depends on the number of expexted dots)
    StatusMsg_UserForm.Add_Dot_to_ActSheet_Label()
    MacroRow = 4
    while X02.Cells(MacroRow, 4).Value != '':
        MacroCodeNr = X02.Cells(MacroRow, 4).Value
        Delete_Multiplexer(MacroCodeNr, True)
        StatusMsg_UserForm.Add_Dot_to_ActSheet_Label()
        # 10.02.21:
    X02.Unload(StatusMsg_UserForm)
    # 10.02.21:
    _fn_return_value = True
    return _fn_return_value

def Test_Delete_Shapes():
    MacroCodeNr = String()
    #--------------------------------------------------------------------------------------------
    MacroCodeNr = 'M01O00'
    Delete_Shapes(( MacroCodeNr ))

def Delete_Shapes(MacroCodeNr, LEDs=0):
    global TargetWorkSheet
    OptionNr = Variant()

    LedNr = Integer()

    ButtonName = String()

    MacroNr = Variant()

    MacroRow = Variant()

    NumberOfLEDs = Variant()

    Max_LEDs = Integer()

    DeleteShapes = Boolean()

    WasProtected = Boolean()

    RGB_Type = Boolean()
    #--------------------------------------------------------------------------------------------
    # Delete_Multiplexer_M01O00_Click     = Shape
    # Test_Leds_M01O01                    = Shape
    # LED_M01O01L8                        = Shape Circle (Oval)
    # Find the buttons.
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    MacroNr = Val(Mid(MacroCodeNr, 2, 2))
    NumberOfLEDs = LEDs
    if MacroNr < 90:
        #        Number_Of_Multiplexers = ReadIniFileString("Multiplexer_Macro", "Number_Of_Multiplexers")
        # 10.02.21: Disabled
        pass
    else:
        if X02.ActiveSheet.RGB_LED_CheckBox.Value == True:
            RGB_Type = True
            # LED type is RGB
            NumberOfLEDs = NumberOfLEDs / 3
    if PrevWorkSheet is None:
        TargetWorkSheet = X02.ActiveSheet
    else:
        TargetWorkSheet = PrevWorkSheet
    if MacroNr > Number_Of_Multiplexers:
        DeleteShapes = True
    ButtonName = 'GroupBox_' + MacroCodeNr
    if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName) and not Multiplexer_Init and DeleteShapes:
        TargetWorkSheet.Shapes.Range(Array(ButtonName)).Delete()
    OptionNr = 0
    ButtonName = 'Delete_Multiplexer_' + Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2)
    if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName) and not Multiplexer_Init and DeleteShapes:
        TargetWorkSheet.Shapes.Range(Array(ButtonName)).Delete()
    ButtonName = 'Single_LEDs_' + MacroCodeNr
    if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName) and not Multiplexer_Init and DeleteShapes:
        TargetWorkSheet.Shapes.Range(Array(ButtonName)).Delete()
    ButtonName = 'RGB_LEDs_' + MacroCodeNr
    if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName) and not Multiplexer_Init and DeleteShapes:
        TargetWorkSheet.Shapes.Range(Array(ButtonName)).Delete()
    MacroRow = pattgen.M80_Multiplexer_INI_Misc.Get_MacroRow(Left(MacroCodeNr, 4) + '00')
    if X02.ActiveSheet.Name == 'Multiplexer':
        NumberOfLEDs = X02.Cells(MacroRow, X02.Range('Number_Of_LEDs').Column).Value
    for OptionNr in vbForRange(1, 8):
        if MacroNr < 90:
            ButtonName = 'Test_Leds_' + Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2)
            if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName) and DeleteShapes:
                TargetWorkSheet.Shapes.Range(Array(ButtonName)).Delete()
                Debug.Print('25 Deleted Button  : ' + ButtonName)
            ButtonName = 'Add_Option_' + Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2)
            if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName) and DeleteShapes:
                TargetWorkSheet.Shapes.Range(Array(ButtonName)).Delete()
        for Max_LEDs in vbForRange(32, 0, - 1):
            # Get highest used LED number
            ButtonName = 'LED_' + Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2) + 'L' + str(Max_LEDs) #*HL
            if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName):
                break
        for LedNr in vbForRange(1, Max_LEDs):
            ButtonName = 'LED_' + Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2) + 'L' + str(LedNr)
            if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName) and  ( LedNr > NumberOfLEDs or  ( MacroNr < 90 and not DisplayLEDs ) ) :
                #TargetWorkSheet.Shapes.Range(Array(ButtonName)).Select
                # Debug
                TargetWorkSheet.Shapes.Range(Array(ButtonName)).Delete()
            ButtonName = 'LED_' + Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2) + 'L' + "100" + str(LedNr) #*HL
            if not RGB_Type and pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName):
                TargetWorkSheet.Shapes.Range(Array(ButtonName)).Delete()
        if MacroNr >= 90:
            break
        # Only the Multiplexer have 8 options. Therefore exit by Option 1.
    if WasProtected:
        M30.Protect_Active_Sheet()
    Debug.Print('29 Deleting shapes Ready! : ' + MacroCodeNr)

def Delete_All_LEDs():
    OptionNr = Variant()

    LedNr = Variant()

    MacroNr = Integer()

    ButtonName = String()
    #--------------------------------------------------------------------------------------------
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    for MacroNr in vbForRange(1, 20):
        if MacroNr % 5 == 1:
            StatusMsg_UserForm.Add_Dot_to_ActSheet_Label()
        for OptionNr in vbForRange(1, 8):
            for LedNr in vbForRange(1, 32):
                # LED_M01O01L1
                ButtonName = 'LED_M' + Right('00' + CStr(MacroNr), 2) + 'O' + Right('00' + CStr(OptionNr), 2) + 'L' + LedNr
                if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName):
                    X02.ActiveSheet.Shapes.Range(Array(ButtonName)).Delete()
                ButtonName = 'LED_M' + Right('00' + CStr(MacroNr), 2) + 'O' + Right('00' + CStr(OptionNr), 2) + 'L' + 100 + LedNr
                if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName):
                    X02.ActiveSheet.Shapes.Range(Array(ButtonName)).Delete()
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_ProtectShapes(True)
    Debug.Print('Deleting All Shapes Ready!')

def Delete_Button_Row_Shapes():
    ButtonName = String()
    #--------------------------------------------------------------------------------------------
    PG.ThisWorkbook.Sheets('Multiplexer').Select()
    ButtonName = 'Reload_Multiplexer'
    if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName):
        X02.ActiveSheet.Shapes.Range(Array(ButtonName)).Delete()
    ButtonName = 'Close_Multiplexer'
    if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName):
        X02.ActiveSheet.Shapes.Range(Array(ButtonName)).Delete()
    ButtonName = 'Save_Multiplexer'
    if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName):
        X02.ActiveSheet.Shapes.Range(Array(ButtonName)).Delete()
    ButtonName = 'New_Multiplexer'
    if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName):
        X02.ActiveSheet.Shapes.Range(Array(ButtonName)).Delete()
    ButtonName = 'WikiMLL'
    if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName):
        X02.ActiveSheet.Shapes.Range(Array(ButtonName)).Delete()
    X02.Range(X02.Cells(1, 2).Address(), X02.Cells(2, 2).Address()).ClearContents()
    X02.Range(X02.Cells(1, 12).Address(), X02.Cells(1, 15).Address()).ClearContents()
    X02.Range(X02.Cells(2, 9).Address(), X02.Cells(2, 15).Address()).ClearContents()

def Add_LEDs_in_ActiveCell(r, MacroCodeNr, NumberOfLEDs, LED_Array=VBMissingArgument, MacroRow=VBMissingArgument):
    t = Double()

    l = Double()

    h = Variant()

    w = Variant()

    min_dim = Variant()

    v_center = Variant()

    h_center = Double()

    LedNr = Integer()

    Nr = Integer()

    LED = String()

    #*HL Sh = Shape()

    MacroNr = Integer()
    # 03.06.20: Hardi: Added: R
    #-----------------------------------------------------------------------------------------------------------------
    #    Dim t2, l2, h2, w2, min_dim2, v_center2, h_center2 As Double
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    # ActiveCell Position and Size
    t = r.Top
    l = r.Left - 27
    h = r.Height - 10
    w = r.Width - 10
    min_dim = IIf(h > w, w, h)
    v_center = t + h / 2 - min_dim / 2
    h_center = l + w / 2 - min_dim / 2
    MacroNr = Val(Mid(MacroCodeNr, 2, 2))
    LED = 'LED_' + MacroCodeNr + 'L'
    LedNr = 1
    for Nr in vbForRange(1, NumberOfLEDs):
        Add_LED_Shape(LED, LedNr, l, t + 3, 19, 19)
        LedNr = LedNr + 1
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_ProtectShapes(( True ))
    X02.ActiveCell().Select() #*HL
    # deselect the last added shape
    # 03.06.20: Hardi

def Load_msoShapeOval(Pos, LedName=VBMissingArgument):
    global EditMode
    guifactor =1.55
    Params = vbObjectInitialize(objtype=String)

    LED = String()

    l = Double()

    t = Double()

    h = Double()

    w = Double()

    r = Double()

    LedNr = Integer()
    #---------------------------------------------------------------------------------------------------------------
    # Print #FileNr, TypeName & Chr(pcfSep) & o.Left & ";" & o.Top & ";" & o.Width & ";" & o.Height;
    # ActiveSheet.Shapes.AddShape(msoShapeOval, l, t, h, w)
    LED = Left(LedName, Len('LED_M99O01L'))
    LedNr = Val(Mid(LedName, Len('LED_M99O01L') + 1))
    Params = Split(Pos, ';')
    l = M30.NrStr2d(Params(0)) * guifactor
    # 27.07.20: Added "NrStr2d()" to prevent problems with german decimal separator
    t = M30.NrStr2d(Params(1)) * guifactor
    w = M30.NrStr2d(Params(2)) * guifactor
    # 12.07.20: Swapped w and h
    h = M30.NrStr2d(Params(3)) * guifactor
    if UBound(Params) == 4:
        r = M30.NrStr2d(Params(4))
    else:
        r = 0
    EditMode = True
    if not pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(LED + str(LedNr)):
        # If not exists then Add the (Led)shape
        Add_LED_Shape(LED, LedNr, l, t, h, w)
        _with90 = X02.ActiveSheet.get_Shape(LED + str(LedNr))
        _with90.ZOrder(X01.msoBringToFront)
        _with90.Rotation = r
    else:
        # If exists then move to loaded position.
        _with91 = X02.ActiveSheet.get_Shape(LED + str(LedNr))
        _with91.Left = l
        _with91.Top = t
        _with91.Height = h
        _with91.Width = w
        _with91.ZOrder(X01.msoBringToFront)
        _with91.Rotation = r
    EditMode = False

def Add_LED_Shape(LED, LedNr, l, t, h, w):
    
    global LED_Nrs_OnOff
    guifactor =1
    
    #*HL Sh = Shape()
    #---------------------------------------------------------------------------------------------------------------
    if not pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(LED + str(LedNr)):
        # Add the shape
        # ActiveSheet.Shapes.AddShape(msoShapeOval, h_center, v_center, min_dim, min_dim).Select
        # ActiveSheet.Shapes.AddShape(msoShapeOval, l, t, h, w).Select
        Sh = X02.ActiveSheet.Shapes.AddShape(X01.msoShapeOval, l*guifactor, t*guifactor, h*guifactor, w*guifactor)
        Sh.Name = LED + str(LedNr)  #*HL
        #Sh.Title = "LedNr = " & LED & LedNr
        # 11.07.20: Disabled because it doubles the "AlternativeText"
        Sh.AlternativeText = 'LedNr = ' + LED + str(LedNr)
        #        Sh.Placement = xlMove
        Sh.Placement = X01.xlFreeFloating
        #        Sh.LockAspectRatio = msoTrue
        if not EditMode:
            Sh.Left = l + 3 + LedNr * 30
        #        Debug.Print LED & LedNr & " / Left = " & ActiveSheet.get_Shape(LED & LedNr).Left
        _with92 = Sh.Line
        _with92.Visible = X01.msoTrue
        _with92.ForeColor.rgb = rgb(0, 0, 0)
        # Black ring
        _with92.Transparency = 0
        _with92.Weight = 0.1
        _with93 = Sh.Fill
        _with93.Visible = X01.msoTrue
        _with93.ForeColor.rgb = rgb(0, 0, 0)
        # Filled with Black
        _with93.Transparency = 0
        _with93.Solid()
        if LED_Nrs_OnOff:
            _with94 = Sh.TextFrame2
            _with94.VerticalAnchor = X01.msoAnchorMiddle
            _with94.HorizontalAnchor = X01.msoAnchorCenter
            if LedNr > 0:
                _with94.TextRange.Characters.Text = LedNr
            else:
                _with94.TextRange.Characters.Text = ' '
            _with94.TextRange.Characters[1, 1].ParagraphFormat.FirstLineIndent = 0
            _with94.TextRange.Characters[1, 1].ParagraphFormat.Alignment = X01.msoAlignLeft
            _with94.WordWrap = X01.msoFalse
            _with95 = Sh.TextFrame2.TextRange.Characters(1, 1).ParagraphFormat
            _with95.FirstLineIndent = 0
            _with95.Alignment = X01.msoAlignLeft
            _with96 = Sh.TextFrame2.TextRange.Characters(1, 1).Font
            _with96.NameComplexScript = '+mn-cs'
            _with96.NameFarEast = '+mn-ea'
            _with96.Fill.Visible = X01.msoTrue
            _with96.Fill.ForeColor.ObjectThemeColor = X01.msoThemeColorLight1
            _with96.Fill.ForeColor.TintAndShade = 0
            ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
            _with96.Fill.ForeColor.Brightness = 0
            _with96.Fill.Transparency = 0
            _with96.Fill.Solid()
            _with96.Size = 11
            _with96.Name = '+mn-lt'
        if ThreeD:
            _with97 = Sh.ThreeD
            _with97.BevelTopType = X01.msoBevelArtDeco
            _with97.BevelTopInset = 6
            _with97.BevelTopDepth = 4

def Add_ControlForm_Button_in_ActiveCell(MacroCodeNr, Purpose, OptionNr=VBMissingArgument, MacroRow=VBMissingArgument):
    t = Integer()

    l = Integer()

    h = Integer()

    w = Integer()

    min_dim = Variant()

    v_center = Variant()

    h_center = Variant()

    FontSize = Variant()

    MacroNr = Integer()

    obj = Object()

    sMacroNr = Variant()

    sOptionNr = Variant()

    Code = Variant()

    ButtonCaption = Variant()

    MacroName = String()

    Parts = vbObjectInitialize(objtype=String)

    ButtonName = String()

    Sh = Shape()
    #---------------------------------------------------------------------------------------------------------------
    # Create ControlForm Button
    t = X02.ActiveCell().Top
    l = X02.ActiveCell().Left
    h = X02.ActiveCell().Height
    w = X02.ActiveCell().Width
    min_dim = IIf(h > w, w, h)
    v_center = t + h / 2 - min_dim / 2
    h_center = l + w / 2 - min_dim / 2
    MacroNr = Val(Mid(MacroCodeNr, 2, 2))
    MacroName = 'Button_Pressed'
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    #    Debug.Print 51 & " Adding Button : " & Purpose & "_" & MacroCodeNr
    #create buttons
    _select73 = Purpose
    if (_select73 == 'New Multiplexer'):
        # 10.02.21: 20210206 Misha, Added 'New Multiplexer' button
        l = X02.Cells(MacroRow, X02.Range('Multiplexer_Name').Column).Left + 40
        w = 160
        h = 30
        t = 15
        FontSize = 12
        ButtonName = 'New_Multiplexer'
        ButtonCaption = pattgen.M09_Language.Get_Language_Str('Neuer ') + ' "' + ' Multiplexer ' + '"'
    elif (_select73 == 'Save Multiplexer'):
        l = X02.Cells(MacroRow, X02.Range('Multiplexer_Name').Column).Left + 215
        w = 170
        h = 30
        t = 15
        FontSize = 12
        ButtonName = 'Save_Multiplexer'
        ButtonCaption = pattgen.M09_Language.Get_Language_Str('Speichern') + ' "' + ' Multiplexer ' + '"'
    elif (_select73 == 'Reload Multiplexer'):
        l = X02.Cells(MacroRow, X02.Range('Multiplexer_Name').Column).Left + 400
        w = 175
        h = 30
        t = 15
        FontSize = 12
        ButtonName = 'Reload_Multiplexer'
        ButtonCaption = pattgen.M09_Language.Get_Language_Str('Neu laden') + ' "' + ' Multiplexer ' + '"'
    elif (_select73 == 'Close Multiplexer'):
        l = X02.Cells(MacroRow, X02.Range('Multiplexer_Name').Column).Left + 590
        w = 170
        h = 30
        t = 15
        FontSize = 12
        ButtonName = 'Close_Multiplexer'
        ButtonCaption = pattgen.M09_Language.Get_Language_Str('Schließen') + ' "' + ' Multiplexer ' + '"'
    elif (_select73 == 'Add Option'):
        #        t = Cells(MacroRow + 2, Range("Add_Option").Column).Top + 15
        #        l = Cells(MacroRow + 2, Range("Add_Option").Column).Left + 15
        t = X02.Cells(MacroRow + 1, X02.Range('Add_Option').Column).Top + 15
        l = X02.Cells(MacroRow + 1, X02.Range('Add_Option').Column).Left + 15
        w = 20
        h = 20
        ButtonName = 'Add_Option' + '_' + Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2)
        ButtonCaption = 'Add Option'
        FontSize = 10
    elif (_select73 == 'Test_Leds'):
        #        t = Cells(MacroRow + 1, Range("Macro_Description").Column).Top + 1
        #        l = Cells(MacroRow + 1, Range("Macro_Description").Column).Left + 283
        t = X02.Cells(MacroRow, X02.Range('Macro_Description').Column).Top + 1
        l = X02.Cells(MacroRow, X02.Range('Macro_Description').Column).Left + 283
        w = 80
        h = 24
        ButtonName = 'Test_Leds_' + Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2)
        ButtonCaption = pattgen.M09_Language.Get_Language_Str(Left(Purpose, InStr(Purpose, '_') - 1))
        FontSize = 10
    elif (_select73 == 'Delete_Multiplexer'):
        #        t = Cells(MacroRow + 1, Range("Macro_Description").Column).Top + 1
        #        l = Cells(MacroRow + 1, Range("Macro_Description").Column).Left + 283
        t = X02.Cells(MacroRow, X02.Range('Macro_Description').Column).Top + 1
        l = X02.Cells(MacroRow, X02.Range('Macro_Description').Column).Left + 283
        w = 80
        h = 24
        ButtonName = Purpose + '_' + Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2)
        ButtonCaption = pattgen.M09_Language.Get_Language_Str(Left(Purpose, InStr(Purpose, '_') - 1))
        FontSize = 10
    elif (_select73 == 'GroupBox'):
        #        t = Cells(MacroRow + 1, Range("Number_Of_LEDs").Column).Top - 12
        #        l = Cells(MacroRow + 1, Range("Number_Of_LEDs").Column).Left
        t = X02.Cells(MacroRow, X02.Range('Number_Of_LEDs').Column).Top - 12
        l = X02.Cells(MacroRow, X02.Range('Number_Of_LEDs').Column).Left
        w = 20
        h = 20
        ButtonName = 'GroupBox_' + MacroCodeNr
        ButtonCaption = pattgen.M09_Language.Get_Language_Str('Multiplexer-Gruppe')
    if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName):
        #        Debug.Print "Shape exists : " & ButtonName
        if not Left(ButtonName, Len('GroupBox')) == 'GroupBox':
            X02.ActiveSheet.Shapes.Range[Array(ButtonName)].TextFrame2.TextRange.Characters.Text = ButtonCaption
            # Text on the Button
        return
        #    Else
        #        Debug.Print "Shape NOT exists : " & ButtonName
    if ButtonCaption == 'Add Option' and MacroNr <= Number_Of_Multiplexers:
        Sh = X02.ActiveSheet.Shapes.AddShape(msoShapeMathPlus, l, t, w, h)
        Sh.Fill.Visible = X01.msoFalse
        Sh.Name = ButtonName
        # Name of the Button
        Sh.Title = 'ButtonName = ' + ButtonName
        Sh.AlternativeText = 'ButtonName = ' + ButtonName
        #        sh.TextFrame2.TextRange.Characters.Text = ButtonCaption
        # Text on the Button. NOT neccessary on this type of Button!
        Sh.OnAction = MacroName
        _with98 = Sh.Fill
        _with98.Visible = msoTrue
        # .ForeColor.RGB = RGB(55, 230, 255)
        _with98.ForeColor.rgb = 0xFFFFC0
        _with98.Transparency = 0
        _with98.Solid()
        #        Debug.Print 54 & " Adding Multiplexer  : " & MacroName
    elif Purpose == 'GroupBox' and MacroNr <= Number_Of_Multiplexers:
        if not pattgen.M80_Multiplexer_INI_Misc.Shape_Exists('GroupBox_' + MacroCodeNr):
            Create_GroupBox(MacroCodeNr, l, t, w, h, MacroName)
        else:
            # Only change Name to be shure that Name is Translated.
            X02.ActiveSheet.Shapes.Range[Array(ButtonName)].Characters.Text = ButtonCaption
            # Text on the Button
    else:
        if MacroNr <= Number_Of_Multiplexers:
            if not pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName):
                # Excel type constants;
                # msoShapeRectangle = 1
                # msoShapeRoundedRectangle = 5
                # msoShapeMathPlus = 163
                Sh = X02.ActiveSheet.Shapes.AddShape(msoShapeRoundedRectangle, l, t, w, h)
                Sh.Fill.Visible = X01.msoFalse
                Sh.Name = ButtonName
                # Name of the Button
                Sh.Title = 'ButtonName = ' + ButtonName
                Sh.AlternativeText = 'ButtonName = ' + ButtonName
                Sh.TextFrame2.TextRange.Characters.Text = ButtonCaption
                # Text on the Button
                Sh.OnAction = MacroName
                #        Debug.Print 55 & " Adding Multiplexer  : " & MacroName
                _with99 = Sh.Fill
                _with99.Visible = msoTrue
                # .ForeColor.RGB = RGB(55, 230, 255)
                _with99.ForeColor.rgb = 0xFFFFC0
                _with99.Transparency = 0
                _with99.Solid()
                _with100 = Sh.ThreeD
                _with100.BevelTopType = msoBevelCircle
                _with100.BevelTopInset = 6
                _with100.BevelTopDepth = 6
                _with101 = Sh.TextFrame2
                _with101.VerticalAnchor = msoAnchorMiddle
                _with101.HorizontalAnchor = msoAnchorNone
                _with102 = Sh.TextFrame2.TextRange.Characters().ParagraphFormat
                _with102.FirstLineIndent = 0
                _with102.Alignment = msoAlignCenter
                _with103 = Sh.TextFrame2.TextRange.Characters().Font
                _with103.Bold = msoTrue
                _with103.Name = '@Microsoft JhengHei'
                _with103.NameComplexScript = '+mn-cs'
                _with103.NameFarEast = '+mn-ea'
                _with103.Fill.Visible = msoTrue
                _with103.Fill.ForeColor.rgb = rgb(0, 0, 0)
                _with103.Fill.Transparency = 0
                _with103.Fill.Solid()
                _with103.Size = FontSize
            else:
                # Only change Name to be shure that Name is Translated.
                X02.ActiveSheet.Shapes.Range[Array(ButtonName)].TextFrame2.TextRange.Characters.Text = ButtonCaption
                # Text on the Button
    #    Debug.Print 56 & " Button adding Ready! : " & Purpose & "_" & MacroCodeNr

def Create_GroupBox(MacroCodeNr, l, t, w, h, MacroName):
    ButtonCaption = String()
    #--------------------------------------------------------------------------------------------
    ButtonCaption = pattgen.M09_Language.Get_Language_Str('Multiplexer-Gruppe')
    X02.ActiveSheet.GroupBoxes.Add(l - 6, t + 2, 300, 40).Select()
    X02.Selection.ShapeRange.Name = 'GroupBox_' + MacroCodeNr
    # Name of the GroupBox
    X02.ActiveSheet.Shapes.Range(Array('GroupBox_' + MacroCodeNr)).Select()
    X02.Selection.ShapeRange.AlternativeText = 'GroupName = ' + 'GroupBox_' + MacroCodeNr
    X02.Selection.Characters.Text = ButtonCaption
    # Text on the Button
    X02.ActiveSheet.Shapes.Range(Array('GroupBox_' + MacroCodeNr)).Select()
    ButtonCaption = pattgen.M09_Language.Get_Language_Str('RGB LEDs')
    l = l + 160
    w = 65
    h = 20
    t = t + 14
    X02.ActiveSheet.OptionButtons.Add(l, t, w, h).Select()
    X02.Selection.Characters.Text = ButtonCaption
    # Text on the Button
    _with104 = X02.Selection.ShapeRange
    _with104.Fill.Visible = X01.msoFalse
    _with104.Name = 'RGB_LEDs_' + MacroCodeNr
    # Name of the Button
    _with104.AlternativeText = 'ButtonName = ' + 'RGB_LEDs_' + MacroCodeNr
    ButtonCaption = pattgen.M09_Language.Get_Language_Str('Single LEDs')
    l = l + 65
    w = 65
    h = 20
    t = t
    X02.ActiveSheet.OptionButtons.Add(l, t, w, h).Select()
    X02.Selection.Characters.Text = ButtonCaption
    # Text on the Button
    _with105 = X02.Selection.ShapeRange
    _with105.Fill.Visible = X01.msoFalse
    _with105.Name = 'Single_LEDs_' + MacroCodeNr
    # Name of the Button
    _with105.AlternativeText = 'ButtonName = ' + 'Single_LEDs_' + MacroCodeNr
    _with106 = X02.ActiveSheet.OptionButtons('Single_LEDs_' + MacroCodeNr)
    #            .Font.Size = 12
    # Not working?????
    #            .Enabled = True
    _with106.Value = False
    _with106.OnAction = MacroName
    _with107 = X02.ActiveSheet.OptionButtons('RGB_LEDs_' + MacroCodeNr)
    #            .Font.Size = 12
    # Not working?????
    #            .Enabled = True
    _with107.Value = False
    _with107.OnAction = MacroName

def Print_All_OptionButtons():
    optBtn = OptionButton()
    #--------------------------------------------------------------------------------------------
    for optBtn in X02.ActiveSheet.OptionButtons:
        #        If optBtn.Value = 1 Then
        Debug.Print(optBtn.GroupBox.Name)
        Debug.Print(optBtn.Name)
        #        End If

def Key_CTRL_And_T_Pressed():
    ButtonName = String()
    #Attribute Key_CTRL_And_T_Pressed.VB_ProcData.VB_Invoke_Func = "t\n14"
    #--------------------------------------------------------------------------------------------
    if X02.Cells(1, 1) == 'Normal Data Sheet' and not X02.ActiveSheet.Name == 'Multiplexer':
        ButtonName = 'Test_Leds_M99O01'
        Button_Pressed_Entry(( ButtonName ))

def Button_Pressed():
    ButtonName = String()
    ButtonName = X02.Application.Caller
    Button_Pressed_Entry(( ButtonName ))

def Button_Pressed_Entry(ButtonName):
    global TargetWorkSheet, TestLedButtonClearing
    MacroNr = Variant()

    OptionNr = Integer()
    #--------------------------------------------------------------------------------------------
    # Delete_Multiplexer_M01O00()
    # Test_Leds_M01O01()
    MacroNr = Val(Mid(Right(ButtonName, 6), 2, 2))
    OptionNr = Val(Mid(Right(ButtonName, 6), 5, 2))
    if ( Left(ButtonName, 4) == 'Test' and not Test_Buttons(MacroNr * 100 + OptionNr) )  or DelayTimerOn:
        Clear_Test_Led_Buttons()
    if not DelayTimerOn or MacroNr >= 90:
        TargetWorkSheet = X02.ActiveSheet
        TestLedButtonClearing = False
        Button_Pressed_Handling(ButtonName)

def Set_Button_Text_and_Color(MacroCodeNr, Txt, rgbNr):
    # 03.06.20: Hardi
    #-----------------------------------------------------------------------------------------
    _with108 = X02.ActiveSheet.get_Shape('Test_Leds_' + MacroCodeNr)
    if _with108:
        _with108.Locked = False
        _with108.Fill.ForeColor.rgb = rgbNr
        _with108.TextFrame2.TextRange.Characters.Text = Txt
        _with108.Locked = True

def Get_NumberOfLEDs():
    _fn_return_value = None
    Kanaele = Long()

    Startkanal = Long()
    # 14.07.20:
    #------------------------------------------
    Kanaele = PG.ThisWorkbook.ActiveSheet.Range('Kanaele')
    if PG.ThisWorkbook.ActiveSheet.RGB_LED_CheckBox.Value:
        Kanaele = WorksheetFunction.RoundUp(Kanaele / 3, 0)
    _fn_return_value = Kanaele
    return _fn_return_value

def Button_Pressed_Handling(ButtonName, StopDisplay=False):
    global EditMode, TestLedButtonClearing, Multiplexer_Init, LED_Nrs_OnOff, Test_Buttons, TargetWorkSheet, TestPatternButtonOn, PrevWorkSheet
    MacroName = String()

    Pattern = String()

    Parts = vbObjectInitialize(objtype=String)

    MacroCodeNr = String()

    MultiplexerName = String()

    Answer = Variant()

    Output_Channels = Integer()

    NumberOfLEDs = Integer()

    Max_LEDs = Integer()

    LedNr = Integer()

    MacroNr = Integer()

    OptionNr = Integer()

    MacroRow = Integer()

    LEDs = Long()

    Display = Boolean()

    NewWorksheet = X02.Worksheet()

    WasProtected = Boolean()
    #--------------------------------------------------------------------------------------------
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    # Delete_Multiplexer_M01O00()
    # Test_Leds_M01O01()
    Parts = Split(ButtonName, '_')
    MacroName = Parts(0)
    if MacroName == '':
        MacroName = ButtonName
    if Left(Right(ButtonName, 6), 1) == 'M':
        MacroCodeNr = Right(ButtonName, 6)
        MacroNr = Val(Mid(Right(ButtonName, 6), 2, 2))
        OptionNr = Val(Mid(Right(ButtonName, 6), 5, 2))
    if MacroNr >= 90:
        if IsKeyPressed(gksKeyboardShift):
            # MsgBox ("Shift key was held!")
            if MacroNr >= 90 and MacroName == 'Test' and not EditMode:
                EditMode = True
                Set_Button_Text_and_Color(MacroCodeNr, 'Edit Mode', rgb(230, 60, 60))
                #ActiveSheet.Shapes.Range(Array("Insert_Picture_M98O01")).Visible = True
                # 12.06.20: Disabled
                Debug.Print('* Edit Mode Started')
                #'# VB2PY (CheckDirective) VB2PY directive Ignore Text
                X03.Sleep(( 500 ))
                # To give the program time to de-Select 'Test' Button.
                # 14.07.20: Disabled: UserForm_Move_Shapes.Show vbModeless
                ## VB2PY (CheckDirective) VB directive took path 2 on USE_SHAPE_MOVE_EVENT
                Display_Leds_Ending(MacroCodeNr, Get_NumberOfLEDs(), True)
                # 14.07.20: Disabled: UserForm_Move_Shapes.Add_Dot_to_ActSheet_Label
                return
        else:
            # MsgBox ("Standard, no shift key")
            if EditMode and MacroName == 'Test':
                EditMode = False
                # 14.07.20: Disabled: Unload UserForm_Move_Shapes
                # ActiveSheet.Shapes.Range(Array("Insert_Picture_M98O01")).Visible = False
                # 12.06.20: Disabled to show the button always
                Set_Button_Text_and_Color(MacroCodeNr, 'Test Pattern', rgb(232, 232, 232))
                if LED_Nrs_OnOff == False:
                    Display_Leds_Ending(MacroCodeNr, Get_NumberOfLEDs(), False)
                Debug.Print('* Edit Mode Ended')
                M30.Protect_Active_Sheet()
                return
        if MacroNr >= 90 and MacroName == 'Insert':
            Load_New_Picture()
        # 12.06.20: Removed: 'And EditMode'
    Display = True
    _select74 = MacroName
    if (_select74 == 'Reload'):
        # Reload Multiplexer
        Clear_Test_Led_Buttons
        Reload_Multiplexer
    elif (_select74 == 'Save'):
        # Save Multiplexer
        Clear_Test_Led_Buttons
        Save_Multiplexer
    elif (_select74 == 'New'):
        # New Multiplexer
        Clear_Test_Led_Buttons
        New_Multiplexer
    elif (_select74 == 'Delete'):
        # Delete Multiplexer
        Clear_Test_Led_Buttons
        Delete_Multiplexer(MacroCodeNr, False)
    elif (_select74 == 'Add'):
        # Add Multiplexer Option
        Clear_Test_Led_Buttons
        MacroRow = pattgen.M80_Multiplexer_INI_Misc.Get_MacroRow(Left(MacroCodeNr, 4) + '00')
        if Check_Multiplexergroup_Filled(MacroCodeNr, MacroNr, MacroRow):
            TestLedButtonClearing = True
            NumberOfLEDs = X02.Cells(MacroRow, X02.Range('Number_Of_LEDs').Column).Value
            Add_Multiplexer_Option(MacroCodeNr, NumberOfLEDs)
    elif (_select74 == 'Close'):
        # Close Multiplexer worksheet
        Clear_Test_Led_Buttons
        if not X02.ActiveSheet.get_Shape('Save_Multiplexer').Fill.ForeColor.rgb == 0xFFFFC0:
            Answer = X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Die \'Multiplexer\' wurde noch nicht gespeichert. Willst du das noch machen?'), vbQuestion + vbYesNo + vbDefaultButton2, pattgen.M09_Language.Get_Language_Str('Schließen \'Multiplexer\'…'))
            if Answer == vbNo:
                X02.Sheets['Multiplexer'].Visible = False
        else:
            X02.Sheets['Multiplexer'].Visible = False
        TestLedButtonClearing = True
    elif (_select74 == 'RGB') or (_select74 == 'Single'):
        if X02.Worksheets('Multiplexer').OptionButtons('RGB_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00').Enabled == True or X02.Worksheets('Multiplexer').OptionButtons('Single_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00').Enabled == True:
            MacroRow = pattgen.M80_Multiplexer_INI_Misc.Get_MacroRow(Left(MacroCodeNr, 4) + '00')
            pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
            Multiplexer_Init = True
            Delete_Shapes(X02.Cells(MacroRow, X02.Range('MultiplexerNumber').Column).Value, X02.Cells(MacroRow, X02.Range('Number_Of_LEDs').Column).Value)
            Load_Buttons(Val(Right(Left(X02.Cells(MacroRow, 4).Value, 3), 2)), MacroRow - 1)
            if DisplayLEDs:
                Load_Shapes(Val(Right(Left(X02.Cells(MacroRow, 4).Value, 3), 2)), MacroRow - 1)()
            Multiplexer_Init = False
        else:
            X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Wenn dieser Multiplexer-Gruppe bereits ein Muster zugewiesen wurde, dürfen die Multiplexer-Gruppenparameter nicht mehr geändert werden!') + ', ' + MacroCodeNr, vbExclamation, pattgen.M09_Language.Get_Language_Str('Multiplexer-Gruppe') + ' ...')
    elif (_select74 == 'Test'):
        # Test Leds Pattern
        if TestPatternButtonOn:
            StopDisplay = True
        if MacroNr >= 90:
            # Get Pattern Parameters
            Pattern = X02.ActiveSheet.Range('Macro_Range').Value
            Pattern = Trim(Mid(Pattern, InStr(Pattern, ')') + 1))
            LED_Nrs_OnOff = Conv2Bool(pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString('Multiplexer_Macro', 'LED_Nrs_OnOff'))
        else:
            if X02.ActiveSheet.Name == 'Multiplexer':
                MacroRow = pattgen.M80_Multiplexer_INI_Misc.Get_MacroRow(Left(MacroCodeNr, 4) + '00')
                if MacroRow == 0:
                    MacroRow = 4
                if OptionNr != 0:
                    MacroRow = MacroRow + OptionNr * 3 - 1
            MacroRow = pattgen.M80_Multiplexer_INI_Misc.Get_MacroRow(Left(MacroCodeNr, 4) + '00')
            MultiplexerName = X02.Cells(MacroRow, X02.Range('Multiplexer_Name').Column).Value
            NumberOfLEDs = X02.Cells(MacroRow, X02.Range('Number_Of_LEDs').Column).Value
            Load_MacroOption_SingleLEDs_Colors(MultiplexerName, MacroNr, OptionNr, NumberOfLEDs)
        if Test_Buttons(MacroNr * 100 + OptionNr) or TestLedButtonClearing or StopDisplay:
            # Stop Displaying Pattern
            Test_Buttons[MacroNr * 100 + OptionNr] = False
            if MacroNr >= 90:
                if PrevWorkSheet is None:
                    TargetWorkSheet = X02.ActiveSheet
                else:
                    NewWorksheet = X02.ActiveSheet
                    TargetWorkSheet = PrevWorkSheet
                TestPatternButtonOn = False
                TargetWorkSheet.Activate()
                Pattern = X02.ActiveSheet.Range('Macro_Range').Value
                Pattern = Trim(Mid(Pattern, InStr(Pattern, ')') + 1))
                Parts = Split(Pattern, ',')
                Output_Channels = Parts(3)
                LEDs = Output_Channels
                # 3 RGB Channels / LEDs is number of RGB Led's
                Oldupdating = X02.Application.ScreenUpdating
                # 03.06.20: Hardi
                X02.Application.ScreenUpdating = False
                Set_Button_Text_and_Color(MacroCodeNr, 'Test Pattern', rgb(232, 232, 232))
                # 03.06.20: Hardi
                X02.Application.ScreenUpdating = Oldupdating
                # 03.06.20: Hardi
                Display = False
                if NewWorksheet is None:
                    TargetWorkSheet = X02.ActiveSheet
                else:
                    TargetWorkSheet = NewWorksheet
                TargetWorkSheet.Activate()
                TestLedButtonClearing = False
                if D00.Select_GotoNr_Form.Visible:
                    D00.Select_GotoNr_Form.End_Button_Click()
                # 04.06.20: Hardi
            else:
                LEDs = NumberOfLEDs
                if not DisplayLEDs:
                    Delete_Shapes(MacroCodeNr, LEDs)()
                Set_Button_Text_and_Color(MacroCodeNr, 'Test', 0xFFFFC0)
                # 03.06.20: Hardi
                Display = False
            PrevWorkSheet = None
        else:
            Test_Buttons[MacroNr * 100 + OptionNr] = True
            # Start Displaying Pattern
            Set_Button_Text_and_Color(MacroCodeNr, 'Stop', rgb(0, 230, 255))
            # 03.06.20: Hardi
            if MacroNr >= 90:
                PrevWorkSheet = X02.ActiveSheet
        X02.DoEvents()
        if Display:
            if not Display_Pattern_LED(MacroCodeNr, Pattern):
                if not TestLedButtonClearing:
                    Debug.Print('No Pattern Found for : ', MacroCodeNr)
                    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Kein Muster gefunden !!!') + ', ' + MacroCodeNr, vbExclamation, pattgen.M09_Language.Get_Language_Str('Test Muster ...'))
                if MacroNr < 90:
                    Test_Buttons[MacroNr * 100 + OptionNr] = False
                    Set_Button_Text_and_Color(MacroCodeNr, 'Test', 0xFFFFC0)
                    # 03.06.20: Hardi
        else:
            TestPatternButtonOn = False
            # Stop Displaying LEDs by stopping the DelayTimer() with this parameter
    if not EditMode:
        M30.Protect_Active_Sheet()

def Check_Multiplexergroup_Filled(MacroCodeNr, MacroNr, MacroRow):
    _fn_return_value = None
    Filled = Boolean()
    #----------------------------------------------------------------------------------------------------------------
    Filled = True
    if X02.Cells(MacroRow, X02.Range('Number_Of_LEDs').Column).Value == '':
        Filled = False
    if X02.Worksheets('Multiplexer').OptionButtons('RGB_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00').Value != 1 and X02.Worksheets('Multiplexer').OptionButtons('Single_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00').Value != 1:
        Filled = False
    if not Filled:
        _fn_return_value = False
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Geben Sie zuerst die Anzahl der LEDs und den LED-Typ ein, bevor Sie ein Muster hinzufügen!') + vbCrLf + vbCrLf + MacroCodeNr, vbExclamation, pattgen.M09_Language.Get_Language_Str('Testen, ob die Multiplexer-Gruppe eingestellt ist …'))
        return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

def Clear_Test_Led_Buttons():
    MacroNr = Variant()

    OptionNr = Integer()

    MacroCodeNr = Variant()

    ButtonName = String()
    #--------------------------------------------------------------------------------------------
    if Multiplexer_Init:
        return
    for MacroNr in vbForRange(1, 8):
        for OptionNr in vbForRange(1, 8):
            MacroCodeNr = 'M' + Right('00' + CStr(MacroNr), 2) + 'O' + Right('00' + CStr(OptionNr), 2)
            # Test_Leds_M01O01
            ButtonName = 'Test_Leds_' + MacroCodeNr
            if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(ButtonName) and Test_Buttons(MacroNr * 100 + OptionNr):
                Button_Pressed_Handling(ButtonName)
                X02.DoEvents()

def Test_Display_Pattern_LED():
    #--------------------------------------------------------------------------------------------
    # PatternT2(LED,4,InCh,12,0,128,0,PM_NORMAL,0.5 sec,0.5 sec,0,0,0,195,48,12)
    Display_Pattern_LED('M99O01', 'PatternT2(LED,4,InCh,12,0,128,0,PM_NORMAL,0.3 sec,0.5 sec,0,0,0,195,48,12)')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Pattern - ByRef 
def Get_RGB_Value(LED_Value, Pattern):
    _fn_return_value = None
    MinBright = 150
    # 03.06.20: Hardi
    #--------------------------------------------------------------------------------------
    # If less then 8 bits are used the value is influenced in addition by "Value Min" and "Value Max"
    _with109 = Pattern
    if _with109.BitsPerChannel < 8:
        ValNr = M02a.Get_LED_Val(LED_Value, _with109.MaxBitVal)
        _fn_return_value = Round(( ( _with109.Max_Val - _with109.Min_Val )  /  ( X02.Application.WorksheetFunction.Power(2, _with109.BitsPerChannel) - 1 ) )  * ValNr) + _with109.Min_Val
    else:
        _fn_return_value = M02a.Get_LED_Val_8_Bit(LED_Value, _with109.Max_Val)
    # Try to simulate the real LED brightness
    # Problem: The LED value of 1 is visible with a LED, but not visible at all on the monitor
    # LED Brightness
    if _fn_return_value > 0: #*HL
        m = ( 255 - MinBright )  / 255
        _fn_return_value = m * _fn_return_value + MinBright #*HL
    return int(_fn_return_value)

def Display_Pattern_LED(MacroCodeNr, OptionPattern=VBMissingArgument, CreateOnly=False):
    global TestPatternButtonOn, LED_Nrs_OnOff
    _fn_return_value = None
    Oldupdating = Boolean()

    Pattern = pattgen.M17_Import_a_Dec_Macro.Pattern_T()
    #-----------------------------------------------------------------------------------------------
    #Private Type Pattern_T
    #  AnalogFading As String
    # "Analoges_Überblenden": "", "1", "X"
    #  FirstRGBLED As Long
    # "ErsteRGBLED"
    #  StartChannel As Long
    # "Startkanal" 0, 1, 2
    #  BitsPerChannel As Long
    # "Bits_pro_Wert"  1..8  (Eventually this is expanded later for the stepper and servo
    #  SwitchNumber As String
    # "SchalterNr" if "SI_LocalVar" is used the GotoMode is active
    #  Goto_Mode As String
    # "Goto_Mode"
    #  GraphicDisplay As String
    # "Grafische_Anzeige": "", "0", "1", "L", "G"
    #  Channels As Long
    # "Kanaele"
    #  Min_Val As Long
    # "Wert_Min":           0..255 Is not used if BitsPerChannel is 8
    #  Max_Val As Long
    # "WertMax":            0..255 Is not used if BitsPerChannel is 8
    #  Val_Off As Long
    # "Wert_ausgeschaltet"  0..255   Used for all LEDs if input is disabled ?
    #  Mode As String
    # "Mode": Flags and modes like PM_PINGPONG
    #  Duration() As String      '
    #  LED_Table() As String
    # two dimensional array (Row, Col)
    #  Goto_List() As String
    #End Type
    # PatternT(x)(Start LED, Brightness Level (bits), InCh, Number Output Channels, Min Brightness, Max Brightness, SwitchMode, CtrMode, < Patternconfig >)
    # Parts(y)        0               1                 2             3                   4               5             6          7          8 ...>
    # Example => PatternT2(LED,4,InCh,12,0,128,0,PM_NORMAL,0.3 sec,0.5 sec,0,0,0,195,48,12)
    LED_Type_RGB = False
    if OptionPattern == '':
        OptionPattern = pattgen.M80_Multiplexer_INI_Misc.Get_Pattern(MacroCodeNr)
    Debug.Print('OptionPattern : ' + OptionPattern)
    if OptionPattern == '':
        _fn_return_value = False
        return _fn_return_value
    Oldupdating = X02.Application.ScreenUpdating
    if pattgen.M17_Import_a_Dec_Macro.Decode_Pattern_String_to_Struct(OptionPattern, Pattern):
        _with110 = Pattern
        OldEvents = X02.Application.EnableEvents
        X02.Application.EnableEvents = False
        X02.Application.ScreenUpdating = False
        NumberOfPatterns = UBound(_with110.LED_Table, 2)
        if NumberOfPatterns == 0:
            NumberOfPatterns = 1
        MacroNr = Val(Mid(MacroCodeNr, 2, 2))
        OptionNr = Val(Right(MacroCodeNr, 2))
        BrLevelBits = _with110.BitsPerChannel
        for ChNr in vbForRange(1, _with110.Channels):
            # 04.06.20: Hardi: Moved up to call it only once
            if X02.ActiveSheet.Name == 'Multiplexer':
                if X02.Worksheets('Multiplexer').OptionButtons('RGB_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00').Value == 1:
                    LED_Type_RGB = True
                else:
                    LED_Type_RGB = False
            else:
                if pattgen.M80_Multiplexer_INI_Misc.IS_RGB_Group(ChNr):
                    LED_Type_RGB = True
                    # It's enough if only one LED Group has the same name to be able to process
                    break
                    # also memory saving patterns which don't use all colors (Example: AndreaskrLT_RGB)
        # Make sure that the array size can hold all 3 RGB colors even if the macro dosn't define all channels
        if LED_Type_RGB and _with110.Channels % 3 != 0:
            ArraySize = _with110.Channels + 3 - _with110.Channels % 3
        else:
            ArraySize = _with110.Channels
        LED_Array = vbObjectInitialize(((1, NumberOfPatterns), (1, ArraySize), (1, 3),), Variant)
        # LED_Array(Number Of Patterns, Number of Leds, ValueFunction)
        for Pattern_Nr in vbForRange(1, NumberOfPatterns):
            LED_Nr = 1
            RGB_Channel = Split('0,0,0', ',')
            New_ChNr=0
            for ChNr in vbForRange(1, _with110.Channels):
                if New_ChNr<ChNr:
                    LED_Color = '0,0,0'
                    ## VB2PY (CheckDirective) VB directive took path 2 on False
                    if LED_Type_RGB:
                        RGB_Channel[RED] = str(Get_RGB_Value(_with110.LED_Table(ChNr, Pattern_Nr), Pattern))
                        # 03.06.20: Hardi: Moved into function
                        if ChNr + 1 <= _with110.Channels:
                            RGB_Channel[GREEN] = str(Get_RGB_Value(_with110.LED_Table(ChNr + 1, Pattern_Nr), Pattern))
                            if ChNr + 2 <= _with110.Channels:
                                RGB_Channel[BLUE] = str(Get_RGB_Value(_with110.LED_Table(ChNr + 2, Pattern_Nr), Pattern))
                        LED_Array[Pattern_Nr, LED_Nr, RGB_Val] = RGB_Channel(RED) + ',' + RGB_Channel(GREEN) + ',' + RGB_Channel(BLUE)
                        #Debug.Print "RGB - Pattern_Nr : " & Pattern_Nr & " / LED_Nr : " & LED_Nr & " / Value : " & LED_Value, LED_Array(Pattern_Nr, LED_Nr, RGB_Val)
                        New_ChNr = ChNr + 2
                    else:
                        # Single LED
                        ## VB2PY (CheckDirective) VB directive took path 1 on True
                        LED_Array[Pattern_Nr, LED_Nr, RGB_Val] = Get_RGB_Value(_with110.LED_Table(LED_Nr, Pattern_Nr), Pattern)
                        # Disabled. This is not working for Single LEDs. Misha 7-6-2020 11.06.20: Hardi: Enabled again
                        if X02.ActiveSheet.Name == 'Multiplexer':
                            if SingleLEDs(MacroNr * 100 + OptionNr, 1) != '':
                                Brightness = LED_Array(Pattern_Nr, LED_Nr, RGB_Val)
                                colorVal = Split(SingleLEDs(MacroNr * 100 + OptionNr, LED_Nr), ',')
                                LED_Color = X02.Format(( Brightness * colorVal(0) / 256 ), '00') + ', ' + X02.Format(( Brightness * colorVal(1) / 256 ), '00') + ', ' + X02.Format(( Brightness * colorVal(2) / 256 ), '00')
                        else:
                            if LED_Array(Pattern_Nr, LED_Nr, RGB_Val) != 0:
                                # Color of the Cell is the Color of the Single LED
                                ## VB2PY (CheckDirective) VB directive took path 1 on True
                                # 03.06.20: Hardi
                                #LED_Color = iColor(ActiveSheet.Cells(LEDsTAB_R - 1 + LED_Nr, 5), "RGB")
                                LED_Color = pattgen.M80_Multiplexer_INI_Misc.iColor_with_Brightness(X02.ActiveSheet.Cells(M01.LEDsTAB_R - 1 + LED_Nr, 5), LED_Array(Pattern_Nr, LED_Nr, RGB_Val))
                                # 04.06.20: Hardi
                        if Pattern_Nr < 5:
                            LED_Value = 0
                            Debug.Print('SGL-Pattern_Nr: ' + str(Pattern_Nr) + ' / LED_Nr: ' + str(LED_Nr) + ' / Value: ' + str(LED_Value) + '/' + str(LED_Array(Pattern_Nr, LED_Nr, RGB_Val)), ' / Color: ' + str(LED_Color))
                    LED_Array[Pattern_Nr, LED_Nr, Color_Val] = LED_Color
                    LED_Array[Pattern_Nr, LED_Nr, LED_Type_Val] = LED_Type_RGB
                    # 0 = Single LED, 1= RGB LED
                    LED_Nr = LED_Nr + 1
        # Old position of the "End If"   15.07.20:
        if MacroNr >= 90:
            _with111 = Pattern
            TestPatternButtonOn = False
            Add_LEDs_in_ActiveCell(X02.ActiveSheet.Cells(X02.Range('Grafische_Anzeige').Row, 12), MacroCodeNr, LED_Nr - 1, LED_Array)
        else:
            if X02.ActiveSheet.Name == 'Multiplexer':
                TestPatternButtonOn = False
                MacroRow = pattgen.M80_Multiplexer_INI_Misc.Get_MacroRow(Left(MacroCodeNr, 4) + '00')
                Add_LEDs_in_ActiveCell(X02.Cells(MacroRow + OptionNr * 3, X02.Range('Number_Of_LEDs').Column), MacroCodeNr, LED_Nr - 1, LED_Array)
        X02.Application.ScreenUpdating = Oldupdating
        # 03.06.20: Hardi: New Pos
        X02.Application.EnableEvents = OldEvents
        if CreateOnly:
            Display_Leds_Ending(MacroCodeNr, Pattern.Channels, LED_Nrs_OnOff)
        else:
            Display_Leds(MacroCodeNr, NumberOfPatterns, LED_Array, Pattern, LED_Type_RGB)
        _fn_return_value = True
    # 15.07.20: Moved down
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PatternNumber - ByRef 
def Calc_PatternNumber(PatternNumber, Pattern, NumberOfPatterns):
    GotoEntry = String()
    # 03.06.20: Hardi
    #----------------------------------------------------------------------------------------------------------------
    # The Goto line contains the
    #  - Starting columns (S)
    #  - Positions for the Goto instruction (P)
    #  - Goto instructions (G nr)
    #  - GoEnd instructions (E)
    PNr=0
    _with112 = Pattern
    GotoEntry = UCase(_with112.Goto_List[PatternNumber])
    if InStr(GotoEntry, 'E'):
        PatternNumber = NumberOfPatterns + 1
        return PatternNumber
    p = InStr(GotoEntry, 'G')
    if p > 0:
        GotoP = Val(Mid(GotoEntry, p + 1))
        for PatternNumber in vbForRange(1, NumberOfPatterns):
            GotoEntry = UCase(_with112.Goto_List[PatternNumber])
            if InStr(GotoEntry, 'P') > 0:
                PNr = PNr + 1
                if PNr == GotoP:
                    return PatternNumber
        PatternNumber +=1 #*HL Loopvariable adapation to VBA behavior
        return PatternNumber
    PatternNumber = PatternNumber + 1 #*HL loop variable adaption to VBA behavior
    return PatternNumber #*HL ByRef

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PatternNumber - ByRef 
def Calc_StartPatternNumber(GotoNr, PatternNumber, Pattern, NumberOfPatterns):
    GotoEntry = String()
    SNr=0
    # 03.06.20: Hardi
    #-------------------------------------------------------------------------------------------------------------------------------------
    # The Goto line contains the
    #  - Starting columns (S)
    #  - Positions for the Goto instruction (P)
    #  - Goto instructions (G nr)
    #  - GoEnd instructions (E)
    _with113 = Pattern
    for PatternNumber in vbForRange(1, NumberOfPatterns):
        GotoEntry = UCase(_with113.Goto_List[PatternNumber])
        if InStr(GotoEntry, 'S') > 0:
            SNr = SNr + 1
        if SNr >= GotoNr:
            return PatternNumber
    PatternNumber+=1 #*HL Loopvariable adapation to VBA behavior
    return PatternNumber #*HL ByRef

def Test_Callback(Nr, Buff=VBMissingArgument):
    #TT-----------------------------------------------------------
    Debug.Print('Test_Callback:' + Nr + ' ' + Buff)

def Test_Select_GotoNr_Form():
    GotoCnt = 9
    #UT----------------------------------
    D00.Select_GotoNr_Form.Show_Dialog(GotoCnt, Test_Callback)

def Select_GotoNr_Callback(Nr, Buff=VBMissingArgument):
    global GotoNr, RestartDisplay_Leds
    #----------------------------------------------------------------------
    #Debug.Print "Select_GotoNr_Callback:" & Nr & " " & Buff
    # Debug
    GotoNr = Nr
    RestartDisplay_Leds = True

def Get_Start_Cnt(NumberOfPatterns, Pattern):
    _fn_return_value = None
    GotoEntry = String()

    PatternNumber = Long()
    SNr = 0
    # 04.06.20: Hardi
    #-------------------------------------------------------------------------------------------------------------------------------------
    _with114 = Pattern
    for PatternNumber in vbForRange(1, NumberOfPatterns):
        GotoEntry = UCase(_with114.Goto_List[PatternNumber])
        if InStr(GotoEntry, 'S') > 0:
            SNr = SNr + 1
    _fn_return_value = SNr + 1
    return _fn_return_value

def Display_Leds(MacroCodeNr, NumberOfPatterns, LED_Array, Pattern, LED_Type_RGB):
    global GotoNr, RestartDisplay_Leds,  LED_Nrs_OnOff
    #--------------------------------------------------------------------------------------------------------------------------------------------------
    if Pattern.Goto_Mode == "1": #* HL
        D00.Select_GotoNr_Form.Show_Dialog(Get_Start_Cnt(NumberOfPatterns, Pattern), Select_GotoNr_Callback)
        GotoNr = 0
    else:
        GotoNr = - 1
    RestartDisplay_Leds = True
    while 1:
        if RestartDisplay_Leds:
            Debug.Print('Display_Leds_with_StartNr:' + str(GotoNr))
            RestartDisplay_Leds = False
            Display_Leds_with_StartNr(GotoNr, MacroCodeNr, NumberOfPatterns, LED_Array, Pattern, LED_Type_RGB)
        X02.DoEvents()
        if not (GotoNr >= 0):
            break
    Display_Leds_Ending(MacroCodeNr, Pattern.Channels, LED_Nrs_OnOff)
    if Pattern.Goto_Mode == "1":
        Button_Pressed_Handling('Test_Leds_M99O01', True)
        # Stop executing the Displaying of a Pattern
    # Clear the actual position
    X02.Range(X02.Cells(M01.LED_NR_ROW, M01.LEDsTAB_C), X02.Cells(M01.LED_NR_ROW, M01.LEDsTAB_C - 1 + NumberOfPatterns)).Interior.Color = 15652797
    #X02.ActiveSheet.Redraw_table()
    # 13.06.20:

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: StartNr - ByVal 
def Display_Leds_with_StartNr(StartNr, MacroCodeNr, NumberOfPatterns, LED_Array, Pattern, LED_Type_RGB):
    global TestPatternButtonOn
    LED_Nr = Variant()

    ChNr = Long()

    MacroNr = Variant()

    OptionNr = Variant()

    PatternTime = Variant()

    PatternNumber = Integer()

    LED = String()

    RGB_Channel = vbObjectInitialize(objtype=String)

    ReversePattern = Boolean()
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    LED = 'LED_' + MacroCodeNr + 'L'
    MacroNr = Val(Mid(MacroCodeNr, 2, 2))
    OptionNr = Val(Mid(MacroCodeNr, 5, 2))
    _with115 = Pattern
    # 03.06.20: Hardi:
    ExistingShapes = vbObjectInitialize(((1, _with115.Channels),), Variant)
    for ChNr in vbForRange(1, _with115.Channels):
        ExistingShapes[ChNr] = pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(LED + str(ChNr))
    TestPatternButtonOn = True
    PatternNumber = 1
    PingPong = InStr(_with115.Mode, 'PM_PINGPONG') > 0
    # 03.06.20: Hardi
    GotoMode = ( _with115.Goto_Mode == "1" )
    if GotoMode:
        PatternNumber = Calc_StartPatternNumber(StartNr, PatternNumber, Pattern, NumberOfPatterns)
    # 04.06.20: Hardi
    X02.ActiveSheet.Redraw_table()
    while Test_Buttons(MacroNr * 100 + OptionNr) and TestPatternButtonOn and RestartDisplay_Leds == False:
        if MacroNr >= 90:
            # Show the actual displayed column
            X02.Range(X02.Cells(M01.LED_NR_ROW, M01.LEDsTAB_C), X02.Cells(M01.LED_NR_ROW, M01.LEDsTAB_C - 1 + NumberOfPatterns)).Interior.Color = 15652797 #*HL
            X02.CellDict[M01.LED_NR_ROW, M01.LEDsTAB_C - 1 + PatternNumber].Interior.Color = 65535
        for ChNr in vbForRange(1, _with115.Channels):
            if ExistingShapes(ChNr):
                # 03.06.20: Hardi: Old: If Shape_Exists(LED & ChNr)
                LED_Nr = ChNr
                if X02.ActiveSheet.get_Shape(LED + str(LED_Nr)).Visible:
                    # 03.06.20: Hardi: Why is this check implemented ? Only used shapes are visible! Misha 7-6-2020.
                    if LED_Type_RGB:
                        RGB_Channel = Split(LED_Array(PatternNumber, LED_Nr, RGB_Val), ',')
                        _with116 = X02.ActiveSheet.get_Shape(LED + str(LED_Nr))
                        _with116.Fill.ForeColor.rgb = rgb(RGB_Channel(RED), RGB_Channel(GREEN), RGB_Channel(BLUE))
                        _with116.Visible = True
                    else:
                        # Single LEDs
                        RGB_Channel = Split(LED_Array(PatternNumber, LED_Nr, Color_Val), ',')
                        Debug.Print("RGB_Channel: %s, %s, %s, %s",RGB_Channel,PatternNumber, LED_Nr, Color_Val)
                        # 03.06.20: ToDo: Calculate the colors once and fill into an array
                        _with117 = X02.ActiveSheet.get_Shape(LED + str(LED_Nr))
                        if LED_Array(PatternNumber, LED_Nr, RGB_Val) != '' and LED_Array(PatternNumber, LED_Nr, RGB_Val) != '.' and LED_Array(PatternNumber, LED_Nr, RGB_Val) > 0:
                            _with117.Fill.ForeColor.rgb = rgb(Abs(int(RGB_Channel(RED))), Abs(int(RGB_Channel(GREEN))), Abs(int(RGB_Channel(BLUE))))
                            _with117.Visible = True
                        else:
                            _with117.Fill.ForeColor.rgb = rgb(0, 0, 0)
                            # Black
                    X02.ActiveSheet.Unprotect(Password='')
                    X02.ActiveSheet.Shapes.Range(Array(LED + str(LED_Nr))).TextFrame2.TextRange.Characters.Text = ""
                else:
                    Debug.Print ("Not Visible '" + LED + str(LED_Nr) + "'")
                Debug.Print( "LED_Nr : " + str(LED_Nr) + str(RGB_Channel(0)) + "/" + str(RGB_Channel(1)) + "/" + str(RGB_Channel(2)))
        X02.ActiveSheet.Redraw_table()
        DelayTimer(( _with115.Duration(1 +  ( ( PatternNumber - 1 )  % UBound(_with115.Duration) )) ))
        # 03.06.20: Hardi
        if GotoMode:
            PatternNumber=Calc_PatternNumber(PatternNumber, Pattern, NumberOfPatterns) #*HL
            if PatternNumber > NumberOfPatterns:
                #MsgBox "End"
                return
        else:
            if PingPong and ReversePattern:
                # ' 03.06.20: Hardi: Old: InStr(.Mode, "PM_PINGPONG") > 0
                # Counting downwards ( in Reverse / PM_PINGPONG )
                if PatternNumber >= 1:
                    PatternNumber = PatternNumber - 1
                if PatternNumber == 1:
                    ReversePattern = False
                if PatternNumber == 0 and ChNr == 25:
                    PatternNumber = NumberOfPatterns
            else:
                # Counting upwards(PM_NORMAL)
                if PatternNumber <= NumberOfPatterns:
                    PatternNumber = PatternNumber + 1
                if PatternNumber == NumberOfPatterns:
                    ReversePattern = True
                if PatternNumber > NumberOfPatterns:
                    PatternNumber = 1

def Display_Leds_Ending(MacroCodeNr, NumberOfLEDs, LED_Nrs_OnOff):
    
    LED_Nr = Long()

    LED = String()

    WasProtected = Boolean()
    #---------------------------------------------------------------------------------------------
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    LED = 'LED_' + MacroCodeNr + 'L'
    for LED_Nr in vbForRange(1, NumberOfLEDs):
        # Set LEDs Off
        if pattgen.M80_Multiplexer_INI_Misc.Shape_Exists(LED + str(LED_Nr)): #*HL
            _with118 = X02.ActiveSheet.get_Shape(LED + str(LED_Nr))   #*HL replace Shapoes( with get_Shape(
            _with118.Fill.ForeColor.rgb = rgb(0, 0, 0)
            # Black
            if LED_Nrs_OnOff and X02.ActiveSheet.get_Shape(LED + str(LED_Nr)).Visible:
                _with119 = X02.ActiveSheet.Shapes.Range(Array(LED + str(LED_Nr)))
                # With LED Numbers.
                _with119.TextFrame2.VerticalAnchor = X01.msoAnchorMiddle
                _with119.TextFrame2.HorizontalAnchor = X01.msoAnchorCenter
                _with119.TextFrame2.TextRange.Characters.Text = str(LED_Nr)
                _with119.TextFrame2.TextRange.Characters[1, 1].ParagraphFormat.FirstLineIndent = 0
                _with119.TextFrame2.TextRange.Characters[1, 1].ParagraphFormat.Alignment = X01.msoAlignLeft
                _with119.TextFrame2.WordWrap = X01.msoFalse
                _with120 = X02.ActiveSheet.Shapes.Range(Array(LED + str(LED_Nr))).TextFrame2.TextRange.Characters(1, 1).Font
                _with120.NameComplexScript = '+mn-cs'
                _with120.NameFarEast = '+mn-ea'
                _with120.Fill.Visible = X01.msoTrue
                _with120.Fill.ForeColor.ObjectThemeColor = X01.msoThemeColorLight1
                _with120.Fill.ForeColor.TintAndShade = 0
                ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
                _with120.Fill.ForeColor.Brightness = 0
                _with120.Fill.Transparency = 0
                _with120.Fill.Solid()
                _with120.Size = 11
                _with120.Name = '+mn-lt'
            else:
                if X02.ActiveSheet.get_Shape(LED + str(LED_Nr)).Visible:
                    #*HL _with121 = X02.ActiveSheet.Shapes.Range(Array(LED + str(LED_Nr)))
                    #*HL _with121.TextFrame2.TextRange.Characters.Text = ''
                    pass #*HL
    if WasProtected:
        M30.Protect_Active_Sheet()

def New_Multiplexer():
    global Multiplexer_Init, Number_Of_Multiplexers
    MacroCodeNr = String()

    intx = Integer()

    MacroRow = Integer()

    MacroNr = Integer()

    Target = X02.Range()

    WasProtected = Boolean()
    #--------------------------------------------------------------------------------------------
    Debug.Print('Start New_Multiplexer().')
    X02.Application.EnableEvents = False
    X02.Application.ScreenUpdating = False
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    Multiplexer_Init = True
    Last_Used_MultiplexerNr(MacroCodeNr, MacroRow)
    MacroNr = Val(Right(Left(MacroCodeNr, 3), 2))
    MacroNr = MacroNr + 1
    Number_Of_Multiplexers = MacroNr
    # 10.02.21:
    Load_Buttons(MacroNr, MacroRow)
    X02.DoEvents()
    Load_New_Multiplexer_Rows(MacroNr, MacroRow)
    X02.DoEvents()
    if DisplayLEDs:
        Load_Shapes(MacroNr, MacroRow)()
    X02.DoEvents()
    X02.CellDict[MacroRow + 1, X02.Range('Number_Of_LEDs').Column].Locked = False
    MacroNr = MacroNr + 1
    MacroRow = MacroRow + 28
    Multiplexer_Init = False
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_ProtectShapes(True)
    Target = X02.Range('Multiplexer_Name')
    X02.Application.EnableEvents = False
    Target.offset(MacroRow - 29, 0).Select()
    WasProtected = X02.ActiveSheet.ProtectContents
    # 10.02.21: New Block
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    X02.CellDict[MacroRow - 28, ( X02.Range('Number_Of_LEDs').Column )].Locked = False
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Protect()
    X02.Cells(MacroRow - 28, 3).Select()
    X02.ActiveWindow.ScrollRow = MacroRow - 28
    Debug.Print('Adding New_Multiplexer Ready!' + MacroCodeNr)

def Clear_Multiplexer(MacroNr, MacroRow):
    Target = X02.Range()

    Row = Integer()

    OptionNr = Integer()

    MacroCodeNr = String()
    #--------------------------------------------------------------------------------------------
    X02.Application.EnableEvents = False
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    MacroCodeNr = 'M' + Right('00' + CStr(MacroNr), 2) + 'O' + Right('00' + CStr(OptionNr), 2)
    Target = X02.Range('Number_Of_LEDs')
    X02.Application.EnableEvents = False
    _with122 = Target.offset(MacroRow - 1, 0)
    _with122.Value = ''
    _with122.Locked = False
    _with122.FormulaHidden = False
    X02.Worksheets['Multiplexer'].OptionButtons['RGB_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Value = False
    X02.Worksheets['Multiplexer'].OptionButtons['RGB_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Enabled = True
    X02.Worksheets['Multiplexer'].OptionButtons['Single_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Value = False
    X02.Worksheets['Multiplexer'].OptionButtons['Single_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Enabled = True
    Target = X02.Range('Macro_Description')
    Target.offset[MacroRow - 1, 0].Value = ''
    Target = X02.Range('Multiplexer_Name')
    Target.offset[MacroRow - 1, 0].Value = 'Multiplexer_'
    Row = 2
    for OptionNr in vbForRange(1, 8):
        Target = X02.Range('Multiplexer_Name')
        Target.offset[MacroRow - 1 + Row, 0].Value = ''
        Target.offset[MacroRow - 1 + Row + 1, 0].Value = ''
        Target.offset[MacroRow - 1 + Row + 1, 4].Value = ''
        Row = Row + 3

def Add_Multiplexer_Option(MacroCodeNr, NumberOfLEDs):
    Description = String()
    #--------------------------------------------------------------------------------------------
    Description = pattgen.M09_Language.Get_Language_Str('Wählen Sie im Pattern_Configurator die Arbeitsblatt mit dem gewünschten Muster.') + vbCrLf + vbCrLf + pattgen.M09_Language.Get_Language_Str('Drücken Sie dann die Taste \'SELECT\'.') + vbCrLf + vbCrLf + pattgen.M09_Language.Get_Language_Str('IN ACHT NEHMEN! Wählen Sie nur Patronen aus, die für die richtige Anzahl von LEDs geeignet sind!')
    UserForm_Import_Pattern.Show_UserForm_Other(MacroCodeNr, Description, NumberOfLEDs)

def Last_Used_MultiplexerNr(MacroCodeNr, MacroRow):
    #--------------------------------------------------------------------------------------------
    X02.Worksheets('Multiplexer').Select()
    for MacroRow in vbForRange(4, 400, 28):
        if X02.Cells(MacroRow, 4).Value == '':
            break
        MacroCodeNr = X02.Cells(MacroRow, 4).Value
    MacroRow = MacroRow

def Load_New_Multiplexer_Rows(MacroNr, MacroRow):
    MacroCodeNr = String()

    OptionNr = Variant()

    Row = Integer()

    Target = X02.Range()
    #--------------------------------------------------------------------------------------------
    X02.Worksheets('Multiplexer').Select()
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    X02.Application.EnableEvents = False
    X02.Application.ScreenUpdating = False
    OptionNr = 0
    MacroCodeNr = 'M' + Right('00' + CStr(MacroNr), 2) + 'O' + Right('00' + CStr(OptionNr), 2)
    Target = X02.Range('Number_Of_LEDs')
    Target.offset[MacroRow - 1, 1].Value = pattgen.M09_Language.Get_Language_Str('LEDs in Gruppe')
    Target.offset[MacroRow - 1, 1].Font.Size = 14
    pattgen.M80_Multiplexer_INI_Misc.Format_Multiplexer_Group(Target.offset(MacroRow - 1, 0).Row, Target.offset(MacroRow - 1, 0).Column)
    Target = X02.Range('Macro_Description')
    Target.offset[MacroRow - 1, - 1].Value = pattgen.M09_Language.Get_Language_Str('Multiplexer beschreibung') + ' : '
    Target.offset[MacroRow - 1, - 1].Font.Size = 14
    Target.offset[MacroRow - 1, 0].Value = ''
    pattgen.M80_Multiplexer_INI_Misc.Format_Row(Target.offset(MacroRow - 1, 0))
    Target = X02.Range('Multiplexer_Name')
    Target.offset[MacroRow - 1, 1].Value = MacroCodeNr
    Target.offset[MacroRow - 1, 1].Font.Size = 14
    Target.offset[MacroRow - 1, - 1].Value = pattgen.M09_Language.Get_Language_Str('Multiplexer Name') + ' : '
    Target.offset[MacroRow - 1, - 1].Font.Size = 14
    Target.offset[MacroRow - 1, 0].Value = 'Multiplexer_'
    Target.offset[MacroRow - 1, 0].Font.Size = 14
    pattgen.M80_Multiplexer_INI_Misc.Format_Row(Target.offset(MacroRow - 1, 0))
    Row = 2
    for OptionNr in vbForRange(1, 8):
        MacroCodeNr = Left(MacroCodeNr, 4) + Right('00' + CStr(OptionNr), 2)
        Target = X02.Range('Multiplexer_Name')
        Target.offset[MacroRow - 1 + Row, - 1].Value = pattgen.M09_Language.Get_Language_Str('Option ') + OptionNr + pattgen.M09_Language.Get_Language_Str(' Name') + '    : '
        Target.offset[MacroRow - 1 + Row, - 1].Font.Size = 14
        pattgen.M80_Multiplexer_INI_Misc.Format_Row(X02.Range(X02.Cells(MacroRow + Row, 3).Address(), X02.Cells(MacroRow + Row, 6).Address()))
        Target.offset[MacroRow - 1 + Row + 1, - 1].Value = pattgen.M09_Language.Get_Language_Str('Option ') + OptionNr + pattgen.M09_Language.Get_Language_Str(' Pattern') + ' : '
        Target.offset[MacroRow - 1 + Row + 1, - 1].Font.Size = 14
        pattgen.M80_Multiplexer_INI_Misc.Format_Row(X02.Range(X02.Cells(MacroRow + Row + 1, 3).Address(), X02.Cells(MacroRow + Row + 1, 6).Address()))
        Target.offset[MacroRow - 1 + Row + 2, 0].RowHeight = 10
        Row = Row + 3
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_ProtectShapes(True)

def DelayTimer(vSeconds):
    global DelayTimerOn
    t0 = Single()

    t1 = Single()

    dSeconds = Double()
    
    average_processingtime = 0.5
    #--------------------------------------------------------------------------------------------
    # https://stackoverflow.com/questions/20652409/using-vba-to-detect-which-decimal-sign-the-computer-is-using
    # It is important to know that Application.DecimalSeparator and Application International(xlDecimalSeparator)
    # do not behave the same way:
    #
    # Application.DecimalSeparator will ALWAYS output the decimal separator chosen in Excel options even
    # when Excel is told to use System Separators (from Windows regional settings)
    #
    # Application.International(xlDecimalSeparator) will output whatever is the actual decimal separator
    # used by Excel whether it comes from Windows settings (when Application.UseSystemSeparators = True)
    # or from Excel options (when Application.UseSystemSeparators = False)
    #
    # I therefore strongly recommend to always use Application.International(xlDecimalSeparator).
    #You can use integer (1 for 1 second) or single (1.5 for 1 and a half second)
    dSeconds = M30.Convert_TimeStr_to_ms(vSeconds) / 1000
    dSeconds -= average_processingtime # time already passed by processing
    if dSeconds <= 0:
        X02.DoEvents()
        return
    #    Beep
    # Just for testing purpose!
    #    Debug.Print "DelayTimer : " & dSeconds & " Sec."
    DelayTimerOn = True
    t0 = Timer()
    while 1:
        t1 = Timer()
        if t1 < t0:
            t1 = t1 + 86400
            #Timer overflows at midnight
        if t1 - t0 >= dSeconds:
            break
        # 03.06.20: Hardi: exit befor the DoEvents because this call my be quite long
        time.sleep(0.1)
        #X02.Delay(dSeconds)
        X02.DoEvents()
        if not TestPatternButtonOn:
            break
        if RestartDisplay_Leds:
            break
    # Loop is also exited above
    # 04.06.20: Hardi: Abort if new start is required
    DelayTimerOn = False

def Save_Multiplexer(New_Multiplexer_Ini_File=VBMissingArgument):
    Done = Variant()

    Section = Variant()

    KeyName = Variant()

    Value = Variant()

    MacroDecription = Variant()

    MacroCodeNr = Variant()

    OptionName = Variant()

    OptionPattern = Variant()

    ErrorStr = String()

    MacroRow = Variant()

    NumberOfLEDs = Variant()

    Row = Variant()

    OptionNr = Variant()

    Answer = Variant()

    ChNr = Variant()

    MacroNr = Variant()

    OptieNr = Variant()

    Error = Integer()

    MacroName = String()

    Patterns = vbObjectInitialize((8,), String)

    FirstTime = Boolean()
    #--------------------------------------------------------------------------------------------
    Debug.Print('Start Save Multiplexer.')
    if not New_Multiplexer_Ini_File:
        Beep()
        Answer = X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Möchten Sie die Datei Multiplexer wirklich überschreiben?'), vbQuestion + vbYesNo + vbDefaultButton2, pattgen.M09_Language.Get_Language_Str('Speichern Sie die Datei Multiplexer ...'))
        if Answer == vbNo:
            return
    FirstTime = True
    for MacroRow in vbForRange(4, 400, 28):
        MacroName = X02.Cells(MacroRow, X02.Range('Multiplexer_Name').Column).Value
        MacroDecription = X02.Cells(MacroRow, X02.Range('Macro_Description').Column).Value
        MacroCodeNr = X02.Cells(MacroRow, X02.Range('MultiplexerNumber').Column).Value
        MacroNr = Val(Mid(MacroCodeNr, 2, 2))
        OptieNr = Val(Right(MacroCodeNr, 2))
        NumberOfLEDs = X02.Cells(MacroRow, X02.Range('Number_Of_LEDs').Column).Value
        Error = 0
        if MacroCodeNr != '':
            if Len(MacroName) <= Len('Multiplexer_'):
                Error = Error + 2
            # No MultiplexerName added
            if Left(MacroName, Len('Multiplexer_')) != 'Multiplexer_':
                Error = Error + 4
            # Name must start with "Multiplexer_"
            if MacroDecription == '':
                Error = Error + 8
            # MacroDescription is empty
            if NumberOfLEDs <= 0 or NumberOfLEDs == '':
                Error = Error + 16
            # LEDs in Group is empty
            Row = MacroRow + 2
            for OptionNr in vbForRange(1, 8):
                #                If OptionNr = 1 And Cells(Row, 3).Value = "" Then Error = Error + 32
                #                If OptionNr = 1 And Cells(Row + 1, 3).Value = "" Then Error = Error + 32
                #                If Cells(Row, 3).Value = "" And Cells(Row + 1, 3).Value = "" Then Cells(Row + 1, 7).Value = ""
                # 10.02.21: 20210206 Misha, This row is changed and can be deleted. See next row.
                if X02.Cells(Row, 3).Value == '' and X02.Cells(Row + 1, 3).Value == '':
                    X02.CellDict[Row + 1, 3].Value = ''
                # 10.02.21: 20210206 Misha, Changed Cells(Row + 1, 7).Value into Cells(Row + 1, 3).Value
                if X02.Cells(Row, 3).Value == '':
                    X02.CellDict[Row, 3].Value = 'To be filled!'
                if X02.Cells(Row + 1, 3).Value == '':
                    X02.CellDict[Row + 1, 3].Value = 'To be filled!'
                Row = Row + 3
        if Error == 0 and FirstTime:
            Clear_Multiplexer_Ini
            pattgen.M81_Create_Multiplexer_Ini.Create_Default_Ini_File(IniFileName())
            FirstTime = False
        if MacroCodeNr != '' and Error == 0:
            Section = 'Multiplexer_Macro'
            # 10.02.21: New Block
            KeyName = 'Number_Of_Multiplexers'
            Value = Number_Of_Multiplexers
            Done = pattgen.M80_Multiplexer_INI_Misc.WriteIniFileString(Section, KeyName, Value)
            Section = MacroName
            KeyName = 'Description'
            Value = MacroDecription
            Done = pattgen.M80_Multiplexer_INI_Misc.WriteIniFileString(Section, KeyName, Value)
            Section = MacroName
            KeyName = 'Number_Of_LEDs'
            Value = NumberOfLEDs
            Done = pattgen.M80_Multiplexer_INI_Misc.WriteIniFileString(Section, KeyName, Value)
            Section = MacroName
            KeyName = 'LED_Type'
            if X02.Worksheets('Multiplexer').OptionButtons('RGB_LEDs_' + MacroCodeNr).Value == 1:
                Value = 'RGB LEDs'
            elif X02.Worksheets('Multiplexer').OptionButtons('Single_LEDs_' + MacroCodeNr).Value == 1:
                Value = 'Single LEDs'
            else:
                Value = ''
            Done = pattgen.M80_Multiplexer_INI_Misc.WriteIniFileString(Section, KeyName, Value)
            Section = MacroName
            KeyName = 'Enable_DCC_Button'
            Value = Enable_DCC_Button
            Done = pattgen.M80_Multiplexer_INI_Misc.WriteIniFileString(Section, KeyName, Value)
            Row = MacroRow + 2
            for OptionNr in vbForRange(1, 8):
                if X02.Cells(Row, 3).Value != '':
                    OptionName = X02.Cells(Row, 3).Value
                else:
                    OptionName = 'To be filled!'
                Section = MacroName
                #KeyName = "Option 1 Name"
                KeyName = 'Option ' + OptionNr + ' Name'
                Value = OptionName
                Done = pattgen.M80_Multiplexer_INI_Misc.WriteIniFileString(Section, KeyName, Value)
                if X02.Cells(Row + 1, 3).Value != '':
                    OptionPattern = X02.Cells(Row + 1, 3).Value
                else:
                    OptionPattern = 'To be filled!'
                Section = MacroName
                #KeyName = "Option 1 Pattern"
                KeyName = 'Option ' + OptionNr + ' Pattern'
                Patterns[OptionNr] = OptionPattern
                Value = OptionPattern
                Done = pattgen.M80_Multiplexer_INI_Misc.WriteIniFileString(Section, KeyName, Value)
                Value = ''
                Section = MacroName
                KeyName = 'Option ' + OptionNr + ' SingleLED_Colors'
                #                If Cells(Row + 1, 7).Value <> "" Then
                if SingleLEDs(MacroNr * 100 + OptionNr, 1) != '':
                    Value = '0' + ','
                    for ChNr in vbForRange(1, NumberOfLEDs):
                        # SingleLEDs(MacroCodeNr,ChNr) = LED_Color
                        Value = Value + SingleLEDs(MacroNr * 100 + OptionNr, ChNr)
                        if ChNr < NumberOfLEDs:
                            Value = Value + ','
                else:
                    Value = ''
                #                End If
                Done = pattgen.M80_Multiplexer_INI_Misc.WriteIniFileString(Section, KeyName, Value)
                Row = Row + 3
            Section = MacroName
            KeyName = 'ControlNr'
            Value = pattgen.M80_Multiplexer_INI_Misc.ControlNr(MacroName, Patterns)
            Done = pattgen.M80_Multiplexer_INI_Misc.WriteIniFileString(Section, KeyName, Value)
            X02.Worksheets['Multiplexer'].OptionButtons['RGB_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Enabled = False
            X02.Worksheets['Multiplexer'].OptionButtons['Single_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Enabled = False
        elif Error > 0:
            ErrorStr = ''
            if Error >= 32:
                ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('Leerer Optionsname oder leeres Optionsmuster gefunden!') + vbCrLf + vbCrLf
                Error = Error - 32
            if Error >= 16:
                ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('Keine Nummer in \'LEDs in Gruppe\'!') + vbCrLf + vbCrLf
                Error = Error - 16
            if Error >= 8:
                ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('Makrobeschreibung ist leer!') + vbCrLf + vbCrLf
                Error = Error - 8
            if Error >= 4:
                ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('Name muss mit \'multiplexer_\' beginnen\' !') + vbCrLf + vbCrLf
                Error = Error - 4
            if Error >= 2:
                ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('Kein Multiplexername hinzugefügt!') + vbCrLf + vbCrLf
                Error = Error - 2
            if Error == 1:
                ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('') + vbCrLf + vbCrLf
                # Not Yet Used!
            X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Der Multiplexer kann nicht gespeichert werden, da Fehler erkannt wurden!') + vbCrLf + vbCrLf + MacroCodeNr + ' : ' + vbCrLf + vbCrLf + ErrorStr, vbExclamation, pattgen.M09_Language.Get_Language_Str('Testen, ob die Bedingungen erfüllt sind …'))
    X02.Cells(4, 3).Select()
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    X02.ActiveSheet.Shapes['Save_Multiplexer'].Fill.ForeColor.rgb = 0xFFFFC0
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_ProtectShapes(True)
    Debug.Print('Saving Multiplexer ready.')

def Create_Multiplexer_Ini():
    New_Multiplexer_Ini_File = Boolean()

    LastUsedMacroNr = Integer()

    MacroNr = Integer()

    MacroRow = Integer()

    MacroCodeNr = String()
    #--------------------------------------------------------------------------------------------
    X02.Worksheets('Multiplexer').Select()
    New_Multiplexer_Ini_File = True
    pattgen.M81_Create_Multiplexer_Ini.Create_Default_Ini_File(IniFileName())
    # Create Default Multiplexer.ini file!
    Last_Used_MultiplexerNr(MacroCodeNr, MacroRow)
    LastUsedMacroNr = Val(Mid(MacroCodeNr, 2, 2))
    if LastUsedMacroNr > Number_Of_Multiplexers:
        for MacroNr in vbForRange(Number_Of_Multiplexers + 1, LastUsedMacroNr):
            MacroCodeNr = 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'
            Delete_Multiplexer(MacroCodeNr, True)
    for MacroNr in vbForRange(1, LastUsedMacroNr):
        MacroCodeNr = 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'
        Delete_Shapes(MacroCodeNr)
    MacroRow = 4
    for MacroNr in vbForRange(1, LastUsedMacroNr):
        Clear_Multiplexer(MacroNr, MacroRow)
        MacroRow = MacroRow + 28
    for MacroNr in vbForRange(LastUsedMacroNr, Number_Of_Multiplexers):
        New_Multiplexer
    X02.Application.ScreenUpdating = True
    MacroRow = 4
    X02.Cells(MacroRow, X02.Range('Multiplexer_Name').Column).Select()
    X02.Application.ScreenUpdating = False

def Check_Pattern(PatternRow, PattStr=VBMissingArgument, Channels=VBMissingArgument):
    _fn_return_value = None
    Parts = vbObjectInitialize(objtype=String)

    MacroCodeNr = String()

    PatternStr = Variant()

    RStr = Variant()

    ErrorStr = String()

    Row = Integer()

    LEDs = Variant()

    Error = Variant()

    MacroNr = Variant()

    OptieNr = Variant()

    Divider = Integer()

    LED_Type = Boolean()

    ChNr = Integer()
    #--------------------------------------------------------------------------------------------
    Error = 0
    if PattStr == '':
        PatternStr = X02.Cells(PatternRow, 3).Value
    else:
        PatternStr = PattStr
    RStr = Mid(PatternStr, InStr(PatternStr, '(') + 1)
    Parts = Split(RStr, ',')
    if Channels == 0:
        for Row in vbForRange(PatternRow, 1, - 1):
            RowRes=Row+1 #* HL Loopvariable adaption to VBA behavior
            if Left(X02.Cells(Row, 4).Value, 1) == 'M':
                RowRes=Row
                break
        Row=RowRes #* HL Loopvariable adaption to VBA behavior
        LEDs = X02.Cells(Row, X02.Range('Number_Of_LEDs').Column).Value
    else:
        LEDs = Channels
    MacroCodeNr = Right(UserForm_Import_Pattern.Caption, 6)
    MacroNr = Val(Mid(MacroCodeNr, 2, 2))
    if X02.Worksheets('Multiplexer').OptionButtons('RGB_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00').Value == 1:
        LED_Type = True
    if X02.Worksheets('Multiplexer').OptionButtons('Single_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00').Value == 1:
        LED_Type = False
    # PatternT(x)(Start LED, Brightness Level (bits), InCh, Number Output Channels, Min Brightness, Max Brightness, SwitchMode, CtrMode, < Patternconfig >)
    # Parts(y)        0               1                 2             3                   4               5             6          7          8 ...>
    Error = 1
    Divider = 1
    if LED_Type:
        Divider = 3
    if InStr(PatternStr, 'Pattern') != 0:
        Error = 0
        if Parts(3) / Divider != LEDs:
            Error = Error + 2
        # LEDs = Output_Channels / 3
        # 3 RGB Channels / LEDs is number of RGB Led's in group
        if InStr(Parts(2), 'LocalVar') != 0:
            Error = Error + 4
        # Als hier InCh of SI_0 of SI_1 staat is het geen goto. Als hier SI_LocalVar staat dan is het een goto opdracht.
    if Error == 0 and Channels == 0:
        X02.Worksheets['Multiplexer'].OptionButtons['RGB_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Enabled = False
        X02.Worksheets['Multiplexer'].OptionButtons['Single_LEDs_' + 'M' + Right('00' + CStr(MacroNr), 2) + 'O00'].Enabled = False
        pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
        pattgen.M80_Multiplexer_INI_Misc.Format_Multiplexer_Group(Row, X02.Range('Number_Of_LEDs').Column)
        pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_ProtectShapes(True)
        _fn_return_value = True
    if Error > 0:
        ErrorStr = ''
        if Error >= 32:
            ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('') + vbCrLf + vbCrLf
            Error = Error - 32
        if Error >= 16:
            ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('') + vbCrLf + vbCrLf
            Error = Error - 16
        if Error >= 8:
            ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('') + vbCrLf + vbCrLf
            Error = Error - 8
        if Error >= 4:
            ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('Ein Goto-Muster wurde ausgewählt. Es wird vom Multiplexer nicht unterstützt!') + vbCrLf + vbCrLf
            Error = Error - 4
        if Error >= 2:
            ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('Muster mit falscher Anzahl von LEDs gewählt!') + vbCrLf + vbCrLf
            Error = Error - 2
        if Error == 1:
            ErrorStr = ErrorStr + pattgen.M09_Language.Get_Language_Str('Es wurde kein Pattern Makro gefunden!') + vbCrLf + vbCrLf
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Das Pattern ist kein korrektes Muster für den Multiplexer!') + vbCrLf + vbCrLf + ErrorStr, vbExclamation, pattgen.M09_Language.Get_Language_Str('Überprüfen, ob die Muster gültig ist ...'))
        if PattStr == '':
            X02.CellDict[PatternRow, 3].Value = PrevValue
        _fn_return_value = False
    return _fn_return_value

def Check_MultiplexerName(MacroRow):
    global MacroNameInputOK
    _fn_return_value = None
    MacroName = String()

    Row = Variant()

    Error = Integer()
    #--------------------------------------------------------------------------------------------
    _fn_return_value = False
    MacroNameInputOK = False
    Error = 0
    for Row in vbForRange(MacroRow, 1, - 1):
        RowRes=Row+1
        if Left(X02.Cells(Row, 4).Value, 1) == 'M':
            RowRes=Row
            break
    Row=RowRes
    MacroName = X02.Cells(Row, 3).Value
    if Left(MacroName, Len('Multiplexer_')) != 'Multiplexer_':
        X02.CellDict[Row, 3].Value = 'Multiplexer_' + MacroName
        Error = Error + 1
    if Error == 0:
        MacroNameInputOK = True
        _fn_return_value = True
    else:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Der Multiplexername ist ungültig! Dies sollte mit \'Multiplexer_\' beginnen.') + vbCrLf + vbCrLf + 'Error: ' + Error, vbExclamation, pattgen.M09_Language.Get_Language_Str('Überprüfen, ob der Multiplexername gültig ist ...'))
    return _fn_return_value

def Clear_Multiplexer_Ini():
    sectnNames = vbObjectInitialize(objtype=String)

    strBuffer = String()

    tmp = String()

    intx = Integer()

    strfullpath = String()

    MacroRow = Integer()

    MacroNr = Integer()

    Target = X02.Range()
    #--------------------------------------------------------------------------------------------
    #Sub to load all of the ini section names into array 'sectnNames() and clear the Multiplexer sections.
    Debug.Print('Start Clearing Multiplexer.')
    Erase(sectnNames)
    strfullpath = IniFileName()
    strBuffer = String(1000, Chr(0))
    # Size of strBuffer$ = 1000, filled with 0 (zero's).
    X03.GetPrivateProfileSectionNames(strBuffer, Len(strBuffer), strfullpath)
    sectnNames = Split(strBuffer, vbNullChar)
    for intx in vbForRange(LBound(sectnNames), UBound(sectnNames)):
        if sectnNames(intx) == vbNullString:
            break
        _select75 = sectnNames(intx)
        if (_select75 == 'Multiplexer_Macro') or (_select75 == 'Section'):
            # Do not delete this sections!
            pass
        else:
            pattgen.M80_Multiplexer_INI_Misc.DeleteIniSection(sectnNames(intx), strfullpath)
            Debug.Print(sectnNames(intx))
    Erase(sectnNames)
    Debug.Print('Clearing Multiplexer ready.')

def IniFileName():
    _fn_return_value = None
    #--------------------------------------------------------------------------------------------
    #    Dim WorkingPath As String
    #
    #    WorkingPath = ThisWorkbook.Path
    #
    #    If Right(WorkingPath, 13) = "LEDs_Autoprog" Then
    #        IniFileName = ThisWorkbook.Path & "\" & MULTIPLEXER_INI_FILE_NAME
    #    Else
    #        IniFileName = ThisWorkbook.Path & "\" & "LEDs_Autoprog" & "\" & MULTIPLEXER_INI_FILE_NAME
    #    End If
    _fn_return_value = pattgen.M07_Save_Sheet_Data.Get_MyExampleDir() + '\\' + MULTIPLEXER_INI_FILE_NAME
    return _fn_return_value

def Change_Number_Of_LEDs():
    global LED_Nrs_OnOff
    CreateOnly = Boolean()

    MacroCodeNr = String()

    Pattern = String()

    Parts = vbObjectInitialize(objtype=String)

    OldCalc = Integer()

    NumberOfLEDs = Long()

    WasProtected = Boolean()
    #--------------------------------------------------------------------------------------------
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    CreateOnly = True
    MacroCodeNr = 'M99O01'
    OldCalc = X02.Application.Calculation
    X02.Application.Calculation = X01.xlCalculationAutomatic
    LED_Nrs_OnOff = Conv2Bool(pattgen.M80_Multiplexer_INI_Misc.ReadIniFileString('Multiplexer_Macro', 'LED_Nrs_OnOff'))
    Pattern = X02.ActiveSheet.Range('Macro_Range').Value
    Pattern = Trim(Mid(Pattern, InStr(Pattern, ')') + 1))
    X02.Application.Calculation = OldCalc
    Parts = Split(Pattern, ',')
    NumberOfLEDs = int(Parts(3)) #*HL
    Delete_Shapes(MacroCodeNr, NumberOfLEDs)
    Display_Pattern_LED(MacroCodeNr, Pattern, CreateOnly)
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_ProtectShapes(( WasProtected ))
    if WasProtected:
        M30.Protect_Active_Sheet()

def Load_New_Picture():
    global EditMode
    Res = Variant()
    #------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo 0
    Res = X02.Application.GetOpenFilename(fileFilter= pattgen.M09_Language.Get_Language_Str('Bilder  (*.png; *.jpg; *.jpeg), *.png;*.jpg;*.jpeg'), Title= pattgen.M09_Language.Get_Language_Str('Auswahl eines Bildes'))
    if Res != False:
        Ext = LCase(M30.FileExt(Res))
        if Ext == '.jpg' or Ext == '.jpeg' or Ext == '.png':
            DestDir = pattgen.M07_Save_Sheet_Data.Get_MyExampleDir() + '\\'
            if UCase(M30.FilePath(Res)) != UCase(DestDir):
                # Copy the file ?
                CopyIt = True
                if X02.Dir(DestDir + M30.FileNameExt(Res)) != '':
                    # Already existing
                    if X02.MsgBox(Replace(Replace(pattgen.M09_Language.Get_Language_Str('Das Bild \'#1#\' ist bereits im Verzeichnis' + vbCr + '  \'#2#\' vorhanden.' + vbCr + vbCr + 'Soll die Datei überschrieben werden?' + vbCr + vbCr + 'Das beeinflusst unter Umständen andere Beispiele'), '#1#', M30.FileNameExt(Res)), '#2#', DestDir), vbQuestion + vbYesNo, pattgen.M09_Language.Get_Language_Str('Bild ist bereits im Beispiel Verzeichnis vorhanden')) == vbNo:
                        CopyIt = False
                if CopyIt:
                    pattgen.M12_Copy_Prog.FileCopy_with_Check(DestDir, M30.FileNameExt(Res), Res)
                # Copy the pictute to the MyPattern_Config_Examples directory
            _with123 = X02.Cells(63, 2)
            # Insert the picture below the button
            Line = str(_with123.Left) + ';' + str(_with123.Top) + ';' + '-1' + ';' + '-1' + Chr(M01.pcfSep) + M30.FileNameExt(Res) #*HL
            pattgen.M08_Load_Sheet_Data.Load_Picture(Line, M30.FilePath(Res))
            #If Right(FileName, 3) = "png" Then
            #    Selection.ShapeRange.PictureFormat.TransparentBackground = msoTrue
            # 12.07.20: Disabled
            #    Selection.ShapeRange.PictureFormat.TransparencyColor = rgb(255, 0, 0)
            #    Selection.ShapeRange.Fill.Visible = msoFalse
            #End If
            #Global_Worksheet_Change Cells(1, 1)
            # Redraw everything to make sure that the picture is placed correctly
            if not EditMode:
                Set_Button_Text_and_Color('M99O01', 'Edit Mode', rgb(230, 60, 60))
            EditMode = True

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetKeyState Lib "user32" (ByVal vKey As Long) As Integer
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetPrivateProfileString Lib "kernel32" Alias "GetPrivateProfileStringA" (ByVal lpApplicationName As String, ByVal lpKeyName As Any, ByVal lpDefault As String, ByVal lpReturnedString As String, ByVal nSize As Long, ByVal lpFileName As String) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function WritePrivateProfileString Lib "kernel32" Alias "WritePrivateProfileStringA" (ByVal lpApplicationName As String, ByVal lpKeyName As Any, ByVal lpString As Any, ByVal lpFileName As String) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetPrivateProfileInt Lib "kernel32" Alias "GetPrivateProfileIntA" (ByVal lpApplicationName As String, ByVal lpKeyName As String, ByVal nDefault As Long, ByVal lpFileName As String) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetPrivateProfileSection Lib "kernel32" Alias "GetPrivateProfileSectionA" (ByVal lpAppName As String, ByVal lpReturnedString As String, ByVal nSize As Long, ByVal lpFileName As String) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetPrivateProfileSectionNames Lib "kernel32" Alias "GetPrivateProfileSectionNamesA" (ByVal lpSectionNames As String, ByVal nSize As Long, ByVal lpFileName As String) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function WritePrivateProfileSection Lib "kernel32" Alias "WritePrivateProfileSectionA" (ByVal lpAppName As String, ByVal lpString As String, ByVal lpFileName As String) As Long
