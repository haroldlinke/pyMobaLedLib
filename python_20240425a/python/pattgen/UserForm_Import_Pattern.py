from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M80_Multiplexer_INI_Handling
import pattgen.M09_Language
import ExcelAPI.XLA_Application as X02
import pattgen.M17_Import_a_Dec_Macro
import pattgen.M80_Multiplexer_INI_Misc
import mlpyproggen.Pattern_Generator as PG

""" 11.06.20:
--------------------------------
--------------------------------------------------------------------------------------------------------------------
-------------------------------
----------------------------
----------------------------
-----------------------------------------
"""


def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
    #  Change_Language_in_Dialog Me
    # 20.02.20:
    Restore_Pos_or_Center_Form2(Me, pattgen.M80_Multiplexer_INI_Handling.OtherForm_Pos)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: MacroCodeNr - ByVal 
def Show_UserForm_Other(MacroCodeNr, Description, LEDs):
    #--------------------------------------------------------------------------------------------------------------------
    if Description == '':
        Description_TextBox = pattgen.M09_Language.Get_Language_Str('Noch keine Beschreibung zur Funktion \'') + Name + pattgen.M09_Language.Get_Language_Str('\' vorhanden ;-(')
    else:
        Description_TextBox = Description
    Me.Caption = pattgen.M09_Language.Get_Language_Str('Importieren Sie das gewünschte Pattern für das Makro : ') + MacroCodeNr
    #  Me.Caption = "Import the desired Pattern for Macro : " & MacroCodeNr
    Me.Controls['Option_Name'].Caption = pattgen.M09_Language.Get_Language_Str('Optionsname') + '   :'
    Me.Controls['Option_Pattern'].Caption = pattgen.M09_Language.Get_Language_Str('Optionsmuster') + '  :'
    Me.Controls['Number_Macro_LEDs'].Caption = pattgen.M09_Language.Get_Language_Str('Wählen Sie Muster für ') + LEDs + ' LED\'s !'
    Opening_Pattern_Configurator
    #  Center_Form Me
    # 18.01.20:
    Me.Show(vbModeless)

def Abort_Button_Click():
    #-------------------------------
    Me.Option_Name_Field.Value = ''
    Me.Option_Pattern_Field.Value = ''
    #Store_Pos2(Me, pattgen.M80_Multiplexer_INI_Handling.OtherForm_Pos)
    X02.Unload(Me)
    # Don't keep the entered data. Importand because the positions of the controlls and the visibility have been changed
    X02.Worksheets('Multiplexer').Select()

def Select_Button_Click():
    tmp = Variant()

    PattConfFile = Variant()

    MacroName = String()

    OptionNr = Integer()

    MacroRow = Integer()

    Pattern = Pattern_T()

    LED_Type = Boolean()

    MacroCodeNr = String()

    ChNr = Integer()

    CountRGB = Variant()

    CountSingle = Variant()

    Error = Integer()

    LED_Color = String()

    MacroNr = Variant()

    OptieNr = Integer()

    NumberOfLEDs = Integer()
    #----------------------------
    #Public Type Pattern_T
    #  StartChannel As Long
    # "Startkanal" 0, 1, 2
    #  Channels As Long
    # "Kanaele"
    #End Type
    PattConfFile = 'Pattern_Configurator.xlsm'
    Me.Option_Name_Field.Value = X02.Workbooks(PattConfFile).ActiveSheet.Range('Makro_Name').Value
    tmp = X02.Workbooks(PattConfFile).ActiveSheet.Range('Macro_Range').Value
    tmp = Trim(Mid(tmp, InStr(tmp, ')') + 1))
    Me.Option_Pattern_Field.Value = tmp
    if X02.Cells(1, 1) != 'Normal Data Sheet' or X02.ActiveSheet.Name == 'Multiplexer':
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Kein Tab mit einem ausgewählten Muster !!!'), vbExclamation, pattgen.M09_Language.Get_Language_Str('Importfehler!'))
        Me.Option_Name_Field.Value = ''
        Me.Option_Pattern_Field.Value = ''
        return
    if pattgen.M17_Import_a_Dec_Macro.Decode_Pattern_String_to_Struct(tmp, Pattern):
        _with128 = Pattern
        CountRGB = 0
        CountSingle = 0
        New_ChNr=0 #*HL Adaption of loopvariable to VBA behavior
        for ChNr in vbForRange(1, _with128.Channels):
            if ChNr>New_ChNr: #*HL Adaption of loopvariable to VBA behavior
                # If next Three Channels have the same name then Channel is first Channel in RGB Group!
                if pattgen.M80_Multiplexer_INI_Misc.IS_RGB_Group(ChNr):
                    CountRGB = CountRGB + 1
                    New_ChNr = ChNr + 2 #*HL Adaption of loopvariable to VBA behavior
                else:
                    CountSingle = CountSingle + 1
        if CountRGB > 0 and CountSingle > 0:
            X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Kombinationen von Einzel- und RGB-LEDs werden vom Multiplexer nicht unterstützt !!!'), vbExclamation, pattgen.M09_Language.Get_Language_Str('Importfehler!'))
            Me.Option_Name_Field.Value = ''
            Me.Option_Pattern_Field.Value = ''
            return
        MacroCodeNr = Right(Me.Caption, 6)
        MacroNr = Val(Mid(MacroCodeNr, 2, 2))
        OptieNr = Val(Right(MacroCodeNr, 2))
        MacroName = Left(MacroCodeNr, 3)
        # Only one LED_Type is supported in the Multiplexer. Might be Single or RGB.
        # LED_Type => False = Single LED, True= RGB LED
        # For RGB LEDs no Array needed!
        if CountRGB * 3 == _with128.Channels:
            LED_Type = True
        if not LED_Type:
            # Single LEDs
            X02.Range(X02.Cells(49 + 1, 5).Address(), X02.Cells(49 + _with128.Channels, 5).Address()).Select()
            for Rng in X02.Selection.Cells:
                LED_Color = pattgen.M80_Multiplexer_INI_Misc.iColor(Rng, 'RGB')
                # SingleLEDs(MacroCodeNr,ChNr) = LED_Color
                pattgen.M80_Multiplexer_INI_Handling.SingleLEDs[MacroNr * 100 + OptieNr, Rng.Row - 49] = Trim(LED_Color)
        else:
            pattgen.M80_Multiplexer_INI_Handling.SingleLEDs[MacroNr * 100 + OptieNr, 1] = ''
            # If Emtpy then Pattern is RGB LEDs!
        for MacroRow in vbForRange(4, 400, 28):
            if X02.Worksheets('Multiplexer').Cells(MacroRow, 4).Value == MacroName + 'O00':
                break
        NumberOfLEDs = X02.Worksheets('Multiplexer').Cells(MacroRow, X02.Worksheets('Multiplexer').Range('Number_Of_LEDs').Column).Value
        # Check_Pattern(PatternRow As Integer, Optional PattStr As String, Optional Channels As Integer)
        if not pattgen.M80_Multiplexer_INI_Handling.Check_Pattern(MacroRow, Me.Option_Pattern_Field.Value, NumberOfLEDs):
            Error = 0

def OK_Button_Click():
    tmp = Variant()

    PattConfFile = Variant()

    MacroName = Variant()

    Row = Variant()

    Value = String()

    OptionNr = Variant()

    MacroNr = Variant()

    NumberOfLEDs = Integer()

    MacroRow = Integer()

    MacroCodeNr = Variant()
    #----------------------------
    #Public Type Pattern_T
    #  StartChannel As Long
    # "Startkanal" 0, 1, 2
    #  Channels As Long
    # "Kanaele"
    #End Type
    if X02.Cells(1, 1) != 'Normal Data Sheet' or X02.ActiveSheet.Name == 'Multiplexer':
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Kein Tab mit einem ausgewählten Muster !!!'), vbExclamation, pattgen.M09_Language.Get_Language_Str('Importfehler!'))
        Me.Option_Name_Field.Value = ''
        Me.Option_Pattern_Field.Value = ''
        Abort_Button_Click()
        return
    PG.ThisWorkbook.Sheets('Multiplexer').Select()
    X02.Application.EnableEvents = False
    # 11.06.20:
    MacroCodeNr = Trim(Mid(Me.Caption, InStr(Me.Caption, ':') + 2))
    MacroName = Left(MacroCodeNr, 3)
    OptionNr = Val(Right(MacroCodeNr, 2))
    X02.Range('MultiplexerNumber').Select()
    for Row in vbForRange(4, 400, 28):
        RowRes=Row+1 #*HL adaption of loopvariable to VBA behavior 
        if X02.Cells(Row, 4).Value == MacroName + 'O00':
            RowRes=Row #*HL adaption of loopvariable to VBA behavior 
            break
    Row=RowRes #*HL adaption of loopvariable to VBA behavior 
    MacroCodeNr = MacroName + 'O' + Right('00' + CStr(OptionNr), 2)
    MacroRow = Row + OptionNr * 3 - 1
    MacroNr = Val(Mid(MacroCodeNr, 2, 2))
    if pattgen.M80_Multiplexer_INI_Handling.Check_Pattern(MacroRow, Me.Option_Pattern_Field.Value):
        X02.Range(X02.Cells(MacroRow, 3).Address(), X02.Cells(MacroRow, 6).Address()).Select()
        X02.ActiveCell().Value = Me.Option_Name_Field.Value
        X02.Range(X02.Cells(MacroRow + 1, 3).Address(), X02.Cells(MacroRow + 1, 6).Address()).Select()
        X02.ActiveCell().Value = Me.Option_Pattern_Field.Value
    NumberOfLEDs = X02.Cells(Row, X02.Range('Number_Of_LEDs').Column).Value
    if pattgen.M80_Multiplexer_INI_Handling.SingleLEDs(MacroNr * 100 + OptionNr, 1) != '':
        Value = '0' + ','
        # 11.06.20:
        for ChNr in vbForRange(1, NumberOfLEDs):
            # SingleLEDs(MacroCodeNr,ChNr) = LED_Color
            Value = Value + pattgen.M80_Multiplexer_INI_Handling.SingleLEDs(MacroNr * 100 + OptionNr, ChNr)
            if ChNr < NumberOfLEDs:
                Value = Value + ','
    else:
        Value = ''
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    X02.CellDict[MacroRow + 1, X02.Range('Macro_Description').Column + 1].Value = Value
    X02.Cells(MacroRow + 1, X02.Range('Macro_Description').Column + 1).Select()
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_UnProtectShapes
    _with129 = X02.Selection.Font
    _with129.Color = - 2236963
    _with129.TintAndShade = 0
    X02.ActiveSheet.Shapes['Save_Multiplexer'].Fill.ForeColor.rgb = rgb(0, 230, 255)
    # Color the Button
    pattgen.M80_Multiplexer_INI_Misc.ActiveSheet_ProtectShapes(True)
    #Store_Pos2(Me, pattgen.M80_Multiplexer_INI_Handling.OtherForm_Pos)
    X02.Application.EnableEvents = True
    X02.Application.ScreenUpdating = True
    X02.Unload(Me)
    # Don't keep the entered data. Importand because the positions of the controlls and the visibility have been changed

def Opening_Pattern_Configurator():
    wkb = Workbook()

    WorkingPath = Variant()

    PattConfFile = Variant()

    tmp = String()
    #-----------------------------------------
    PattConfFile = 'Pattern_configurator.xlsm'
    WorkingPath = PG.ThisWorkbook.Path
    if Right(WorkingPath, 1) != '\\':
        WorkingPath = WorkingPath + '\\'
    if not IsWorkBookOpen(PattConfFile):
        if Dir(WorkingPath + PattConfFile, vbDirectory) != vbNullString:
            # MsgBox "Folder and Excelsheet exist"
            X02.Workbooks.Open(( WorkingPath + PattConfFile ))
        else:
            X02.MsgBox('Excelsheet \'' + PattConfFile + '\' doesn\'t exist!')
    else:
        # MsgBox "Excelsheet '" & PattConfFile & "' already opend!"
        pass

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: OWB - ByVal 
def IsWorkBookOpen(OWB):
    _fn_return_value = None
    WB = Excel.Workbook()

    WBName = String()

    WBPath = String()

    OWBArray = vbObjectInitialize(objtype=String)
    #********************************************************************************************************************************************************************************
    #Function Name                     : IsWorkBookOpen(ByVal OWB As String)
    #Function Description             : Function to check whether specified workbook is open
    #Data Parameters                  : OWB:- Specify name or path to the workbook. eg: "Book1.xlsx" or "C:\Users\Kannan.S\Desktop\Book1.xlsm"
    # This will capture if the workbook is open in the current instance on the local machine -
    # it wont capture whether the workbook is open in another local instance, or by another user elsewhere.
    # I think WB.Path & "\" & WBName is WB.FullName
    # i 'd also add Set WB = Nothing before exiting the function
    #********************************************************************************************************************************************************************************
    _fn_return_value = False
    Err.Clear()
    # VB2PY (UntranslatedCode) On Error Resume Next
    # 11.06.20:
    OWBArray = Split(OWB, X02.Application.PathSeparator)
    WB = X02.Application.Workbooks(OWBArray(UBound(OWBArray)))
    WBName = OWBArray(UBound(OWBArray))
    WBPath = WB.Path + X02.Application.PathSeparator + WBName
    if not WB is None:
        if UBound(OWBArray) > 0:
            if LCase(WBPath) == LCase(OWB):
                _fn_return_value = True
        else:
            _fn_return_value = True
    Err.Clear()
    WB = None
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
