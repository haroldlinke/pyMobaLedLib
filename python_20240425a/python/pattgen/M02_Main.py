from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as X02
import ExcelAPI.XLWF_Worksheetfunction as P01
import pattgen.M35_Mouse_Scroll
import pattgen.M30_Tools as M30
import pattgen.M08_Load_Sheet_Data
import pattgen.M12_Copy_Prog
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M09_Language as M09
import pattgen.M04_Column_With
import pattgen.M03_Analog_Trend
import pattgen.M06_Goto_Graph
import pattgen.M80_Multiplexer_INI_Handling
import pattgen.M14_Select_GotoAct
import pattgen.M60_Select_LED
import pattgen.M55_PWM_Data_Send
import pattgen.D00_Forms as D00
import mlpyproggen.Pattern_Generator as PG

""" Limmitted by the COUNT_VARARGS macro in MobaLedLib.h
'# VB2PY (CheckDirective) VB2PY directive Ignore Text

 Berechnung der Zeiten:
 15.01.20:
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

"""
Last_SelectedCell = None
MAX_VARARGS = 2000
START_BIT = 128
POS_M_BIT = 64
GOTOENDNR = POS_M_BIT - 1
MAXGOTONR = GOTOENDNR - 1
OldMessage = String()
initDone = Boolean()

def Auto_Open():
    # 14.06.20: Changed to Public to be able to call it from an other program
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
    global initDone
    ShowSaveMsg = Boolean()
    #----------------
    #Stop
    # uncomment to have a breakpoint at startup
    PG.ThisWorkbook.Activate()
    if initDone:
        return
    initDone = True
    #if X02.Sheets('Multiplexer').Visible == True:
    X02.Sheets('Main').Select()
    # Prevent problem in the following line
    #Debug.Print('Init() called (Sheets().count=' + PG.ThisWorkbook.Sheets.Count + ')')
    X02.ThisWorkbook.SheetsDict['Languages'].Visible = False
    X02.ThisWorkbook.SheetsDict['Goto_Activation_Entries'].Visible = False
    X02.ThisWorkbook.SheetsDict['Special_Mode_Dlg'].Visible = False
    X02.ThisWorkbook.SheetsDict['Par_Description'].Visible = False
    #X02.SheetsDict['Multiplexer'].Visible = False
    # 02.06.20: Misha
    pattgen.M35_Mouse_Scroll.Cleare_Mouse_Hook()
    # 28.04.20:
    M30.Check_Version()
    # 21.11.21: Juergen
    M09.Update_Language_in_All_Sheets()
    # 04.06.20: Old: Update_Language_in_All_Pattern_Config_Sheets
    if len(PG.ThisWorkbook.Sheets()) == 7: #6:
        # Main, Language, Goto_Activation_Entries, Special_Mode_Dlg, Par_Description
        Clear_Com_Port()
        #*HL ShowSaveMsg = pattgen.M08_Load_Sheet_Data.Load_AllExamples_Sheets()
        PG.ThisWorkbook.Activate()
        X02.ThisWorkbook.Sheets('Main').Select()
        M30.Protect_Active_Sheet()
        X02.ActiveWindow.DisplayHeadings = False
        #Update_Grafik
    else:
        Reset_Com_Port()
    pattgen.M12_Copy_Prog.Copy_Prog_If_in_LibDir()
    if ShowSaveMsg:
        X02.MsgBox('Das Excel Programm sollte gespeichert werden damit die Beispiele beim nächsten Start nicht erneut geladen werden müssen.', vbInformation, 'Bitte Excel speichern')

def Reset_Com_Port():
    Col = Long()
    #---------------------------
    for Col in vbForRange(M01.COMPort_COL, M01.COMPrtT_COL):
        _with0 = X02.Sheets('Main').Cells(M01.SH_VARS_ROW, Col)
        if _with0.Value != '':
            #Debug.Print "Reset_Com_Port in column " & Col & " in the Main sheet (Old:" & .Value & ")"
            if _with0.Value > 0:
                _with0.Value = - _with0.Value

def Clear_Com_Port():
    Col = Long()
    #---------------------------
    for Col in vbForRange(M01.COMPort_COL, M01.COMPrtT_COL):
        _with1 = X02.Sheets('Main').Cells(M01.SH_VARS_ROW, Col)
        if _with1.Value != '':
            #Debug.Print "Clear_Com_Port in column " & Col & " in the Main sheet (Old:" & .Value & ")"
            _with1.Value = ''

def Workbook_Open():
    #--------------------------
    Debug.Print('Workbook_Open() in modul M02_Main called (Sheets.count=' + PG.ThisWorkbook.Sheets.Count + ')')
    Stop()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: MaxVal - ByVal 
def Get_LED_Val(c, MaxVal):
    _fn_return_value = None
    V = Integer()
    #----------------------------------------------------------------------------
    c=str(c) #*HL
    if c != '':
        if IsNumeric(c):
            V = Val(c)
            # 03.06.20: Old: c.value
            if V > MaxVal:
                V = MaxVal
        else:
            s = Trim(c)
            if s == '' or s == '.' or s == '-':
                V = 0
            else:
                V = MaxVal
    _fn_return_value = V
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: MaxVal - ByVal 
def Get_LED_Val_8_Bit(c, MaxVal):
    _fn_return_value = None
    V = Integer()
    #----------------------------------------------------------------------------------
    if c != '':
        if IsNumeric(c):
            V = Val(c)
            # 04.06.20: Old: c.Value
            if V > MaxVal:
                V = MaxVal
            _fn_return_value = V
        else:
            s = Trim(c)
            if s == '' or s == '.' or s == '-':
                _fn_return_value = 0
            elif Len(s) > 1:
                _fn_return_value = s
            else:
                _fn_return_value = MaxVal
    else:
        _fn_return_value = 0
        # 03.06.19:
    return _fn_return_value

def Calc_DecStr_Normal(Rng, LastRow, MaxColumn, BitLen):
    _fn_return_value = None
    ColCnt = Long()

    #c = X02.Range()

    #Col = X02.Range()

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
        Cnt=0
        for c in Col.Cells:
            if c.Row > LastRow:
                break
            #Debug.Print "R:" & c.Row & "  C:" & c.Column
            if c.Value != '':
                Cnt = Cnt + 1
            Val = Get_LED_Val(c, MaxVal)
            # 07.05.19: Extracted calculation to separate function
            Bits = P01.Dec2Bin(Val, BitLen) + Bits
    BitCnt = Len(Bits)
    #Debug.Print Len(Bits) & ": " & Bits & "  "
    # Debug
    while Len(Bits) > 0:
        ByteCnt = ByteCnt + 1
        DecStr = DecStr + ',' + str(P01.Bin2Dec(Right(Bits, 8)))
        if Len(Bits) > 8:
            Bits = Left(Bits, Len(Bits) - 8)
        else:
            Bits = ''
    #Debug.Print "Used bytes: " & ByteCnt
    if ByteCnt > MAX_VARARGS:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Error: Number of used bytes to high !') + MAX_VARARGS + pattgen.M09_Language.Get_Language_Str(' bytes are possible.') + vbCr + 'The current configuration uses ' + ByteCnt + ' bytes ;-(', vbCritical, pattgen.M09_Language.Get_Language_Str('Error to many bytes used'))
    #Debug.Print DecStr
    # Debug
    FreeBits = ByteCnt * 8 - BitCnt
    _fn_return_value = str(FreeBits) + ':' + DecStr
    return _fn_return_value

def Calc_DecStr_8_Bits(Rng, LastRow, MaxColumn, BitLen):
    _fn_return_value = None
    ColCnt = Long()

    #*HL c = X02.Range()

    #Col = X02.Range()

    MaxVal = Integer()

    DecStr = String()

    BitCnt = Long()

    ByteCnt = Long()
    # 20.05.19
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
            #*HLif c.Value != '':
            #*HL    Cnt = Cnt + 1
            DecStr = DecStr + ',' + str(Get_LED_Val_8_Bit(c, MaxVal))
            ByteCnt = ByteCnt + 1
    if ByteCnt > MAX_VARARGS:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Error: Number of used bytes to high !') + MAX_VARARGS + pattgen.M09_Language.Get_Language_Str(' bytes are possible.') + vbCr + pattgen.M09_Language.Get_Language_Str('The current configuration uses ') + ByteCnt + ' bytes ;-(', vbCritical, pattgen.M09_Language.Get_Language_Str('Error to many bytes used'))
    _fn_return_value = '0:' + DecStr
    # 0 Free bits
    return _fn_return_value

def Ist_Formel(c):
    _fn_return_value = None
    # 02.12.19:
    #-----------------------------------------
    # Excel 2010 doesn't have the "IstFormel()" command
    _fn_return_value = Left(c.Formula, 1) == '='
    return _fn_return_value

def CalculatePattern(ChannelsRange, BitLenRange, PatternRange):
    _fn_return_value = None
    #Rng = X02.Range()

    Channels = Long()

    BitLen = Long()

    FirstRow = Long()

    LastRow = Long()

    MaxVal = Integer()

    #c = X02.Range()

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
    #MaxColumn = LastFilledColumn(Rng, LastRow)
    # Find the last used column
    MaxColumn = M30.LastFilledColumn2(Rng, LastRow)
    # Find the last used column    20.11.19: Faster function
    if BitLen < 8:
        _fn_return_value = Calc_DecStr_Normal(Rng, LastRow, MaxColumn, BitLen)
    else:
        _fn_return_value = Calc_DecStr_8_Bits(Rng, LastRow, MaxColumn, BitLen)
    #Debug.Print "CalculatePattern(" & ChannelsRange & ", " & BitLenRange & "," & PatternRange.Address & ")  called from " & ActiveSheet.Name & ":" & CalculatePattern
    return _fn_return_value

def Calculate_Goto(ChannelsRange, GotoModeRange, GotoTabRange, PatternRange):
    global OldMessage
    _fn_return_value = ""
    #Rng = X02.Range()

    Channels = Long()

    FirstRow = Long()

    LastRow = Long()

    MaxColumn = Long()

    #c = X02.Range()

    ColumnNr = Long()

    Unknown = String()

    WrongNumberFound = String()

    message = String()
    #--------------------------------------------------------------------------------------------------------------------------------------
    if GotoModeRange != 1:
        return _fn_return_value
    # ToDo: Übergebene Variablen Typen prüfen...
    Channels = ChannelsRange
    Rng = PatternRange
    FirstRow = Rng.Row
    LastRow = FirstRow + Channels - 1
    #MaxColumn = LastFilledColumn(Rng, LastRow)
    # Find the last used column
    MaxColumn = M30.LastFilledColumn2(Rng, LastRow)
    # Find the last used column    20.11.19: Faster function
    _fn_return_value = '  '
    # Separator for debugging
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
            _select0 = w
            if (_select0 == ''):
                # Nothing
                pass
            elif (_select0 == 'S'):
                # "S" is not possible in the first column because then the first column is adressed with 0 and 1 => All numbers are shifted by 1 ;-(
                if ColumnNr > 1:
                    # 09.01.20:
                    Start = True
            elif (_select0 == 'P'):
                Pos_M = True
            elif (_select0 == 'G'):
                GotoP = True
            elif (_select0 == 'E'):
                GoEnd = True
            else:
                # Check if its a number
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
            else:
                Nr = Nr + Number
        elif GoEnd:
            Nr = Nr + GOTOENDNR
        #Debug.Print Format(ColumnNr, "@@@") & ": Nr=" & Format(Nr, "@@@") & "  Start=" & Format(Start, "@@@@@@@") & " GoEnd=" & Format(GoEnd, "@@@@@@@") & " Goto=" & Format(GotoP, "@@@@@@@") & " " & Number
        # Debug
        _fn_return_value = _fn_return_value + ',' + str(Nr)
    if WrongNumberFound != '':
        WrongNumberFound = Mid(WrongNumberFound, 2)
    # Remove leading ","
    #Debug.Print
    # Debug
    if Unknown != '':
        message = message + pattgen.M09_Language.Get_Language_Str('Ignored expresions: ') + Unknown + vbCr
    if WrongNumberFound != '':
        message = message + pattgen.M09_Language.Get_Language_Str('Falsche oder fehlende Nummer in Spalte gefunden: ') + WrongNumberFound + vbCr + pattgen.M09_Language.Get_Language_Str('(Gültiger Bereich: 1..63)')
    if message != OldMessage:
        OldMessage = message
        if message != '':
            X02.MsgBox(message, vbOKOnly, pattgen.M09_Language.Get_Language_Str('Problems in Goto tabele:'))
    #Debug.Print Message
    return _fn_return_value

def Update_Grafik_from_Str(GrafDsp):
    Oldupdating = Boolean()

    GrafDsp_U = String()

    Show_AnalogTrend = Boolean()

    Show_Goto_Graph = Boolean()

    Show_CorrectWidth = Boolean()
    #---------------------------------------------------
    Oldupdating = X02.Application.ScreenUpdating
    X02.Application.ScreenUpdating = False
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
        pattgen.M04_Column_With.Adjust_Column_With_to_Duration()
    else:
        pattgen.M04_Column_With.Normal_Column_With()
    if Show_AnalogTrend:
        pattgen.M03_Analog_Trend.Draw_Analog_Trend_of_Sheet()
    else:
        pattgen.M03_Analog_Trend.Del_Analog_Trend_Objects()
    if Show_Goto_Graph:
        pattgen.M06_Goto_Graph.Draw_All_Arrows()
    else:
        pattgen.M06_Goto_Graph.Delete_Goto_Graph()
    X02.Application.ScreenUpdating = Oldupdating

def Calc_TimesStr(TimeRange, ModeRange):
    _fn_return_value = None
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
                V = M30.Convert_TimeStr_to_ms(c)
                # Returns -99999 in case of an error
            if V > 65535:
                if V > 65535 * 16:
                    V = - 16
                else:
                    Use_PF_SLOW = True
            if V < 0:
                # Displaying of messages in the statusbar is not possible in a user defined function in Excel ;-(
                # See: https://support.microsoft.com/en-us/help/170787/description-of-limitations-of-custom-functions-in-excel
                Res = Res + '!Error:' + c + ','
            else:
                Res = Res + Replace(c, ',', '.') + ','
        else:
            # Empty
            EmptyCol = True
    if InStr(ModeRange, 'PF_SLOW') > 0:
        Use_PF_SLOW = True
    if Use_PF_SLOW:
        Res = Replace(Res, ',', '/16,')
        while InStr(Res, ' +') > 0:
            Res = Replace(Res, ' +', '+')
        Res = Replace(Res, '+', '/16 +')
    _fn_return_value = ',' + M30.DelLast(Res)
    return _fn_return_value

def Hide_Show_Check_Goto_Activation(Correct_Act_Cell=VBMissingArgument):
    Hide = Boolean()
    #-------------------------------------------------------------------------------
    # Hide the "Goto Aktivation" row
    Hide = not pattgen.M06_Goto_Graph.Goto_Mode_is_Active()
    if X02.Range('Goto_Aktivierung').EntireRow.Hidden != Hide:
        WasProtected = X02.ActiveSheet.ProtectContents
        if WasProtected:
            X02.ActiveSheet.Unprotect()
        X02.Range('Goto_Aktivierung').EntireRow.Hidden = Hide
        if WasProtected:
            M30.Protect_Active_Sheet()
        if Correct_Act_Cell and Hide == False and X02.ActiveCell().Address == X02.Range('Goto_Aktivierung').offset(1, 0).Address:
            # Goto mode was disabled before and is enabled now
            X02.ActiveCell().offset(- 1, 0).Activate()
            # Move the active cell into the prior hidden row

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Global_Worksheet_Change(Target):
    #--------------------------------------------------------------
    # This function is called if the worksheet is changed.
    # It performs several checks after a user input depending form the column of the changed cell:
    # Attention: It's also called from some functions to update the display
    if M01.DEBUG_CHANGEEVENT:
        Debug.Print('Global_Worksheet_Change')
    if Target.CountLarge == 1:
        if Is_Data_Sheet(Target.Parent):
            # Prevent Crash in Hide_Show_GotoLines_If_Enabled if the wron sheet is active
            Oldupdating = X02.Application.ScreenUpdating
            X02.Application.ScreenUpdating = False
            Hide_Show_Check_Goto_Activation(True)
            pattgen.M06_Goto_Graph.Hide_Show_GotoLines_If_Enabled()
            pattgen.M06_Goto_Graph.Hide_Show_Special_ModeLines_If_Enabled()
            # 29.12.19:
            Update_Grafik_from_Str(X02.Range(M01.GrafDsp_Rng))
            # 18.11.19:
            X02.Application.ScreenUpdating = Oldupdating
            if Target.Address == X02.Range('Kanaele').Address:
                pattgen.M80_Multiplexer_INI_Handling.Change_Number_Of_LEDs()
    #X02.ActiveSheet.Redraw_Table()
            # Added by Misha 20-6-2020  06.07.20: Hardi: Moved up

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Global_Worksheet_SelectionChange(Target):
    global Last_SelectedCell
    # 19.11.19:
    #-----------------------------------------------------------------------
    # Is called by event if the worksheet selection has changed

    if pattgen.M80_Multiplexer_INI_Handling.TestPatternButtonOn:
        Debug.Print('Global_Worksheet_SelectionChange called => Stop executing the Displaying of a Pattern')
        pattgen.M80_Multiplexer_INI_Handling.Button_Pressed_Handling('Test_Leds_M99O01', True)
        # Stop executing the Displaying of a Pattern
        # 02.06.20: Misha
    if Target.Column == X02.Range('Goto_Aktivierung').Column:
        if Target.Row == X02.Range('Goto_Aktivierung').Row:
            if pattgen.M06_Goto_Graph.Goto_Mode_is_Active() and X02.Range('Goto_Aktivierung') == '':
                pattgen.M14_Select_GotoAct.Select_GotoAct()
                Target = X02.ActiveCell()
                # The ActiveCell is changed in the function => we have to change Targed to store it correctly
    Last_SelectedCell = Target
    #Debug.Print "Store Last " & Target.Row

def Button_Pressed_Proc():
    #--------------------------------
    X02.Selection.Select()
    # Remove the focus from the button
    M30.Enable_Application_Automatics()
    # In case the program crashed before
    Correct_Buttonsizes()

def Correct_Create_Buttonsize(obj):
    #-----------------------------------------
    obj.Height = 160
    obj.Width = 100
    obj.Height = 83
    # 18.11.19: Size increased for other monitor resolution
    obj.Width = 56

def Correct_Buttonsizes():
    OldScreenupdating = Boolean()
    #--------------------------------
    # There is a bug in excel which changes the size of the buttons
    # if the resolution of the display is changed. This happens
    # fore instance if the computer is connected to a beamer.
    # To prevent this the buttons are resized with this function.
    OldScreenupdating = X02.Application.ScreenUpdating
    X02.Application.ScreenUpdating = False
    #'# VB2PY (CheckDirective) VB2PY directive Ignore Text
    X02.Application.ScreenUpdating = OldScreenupdating

def Main_Menu():
    #---------------------
    if pattgen.M80_Multiplexer_INI_Handling.TestPatternButtonOn:
        pattgen.M80_Multiplexer_INI_Handling.Button_Pressed_Handling('Test_Leds_M99O01', True)()
    # Stop executing the Displaying of a Pattern
    # 02.06.20: Misha
    D00.MainMenu_Form.Show()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def Is_Data_Sheet(Sh):
    _fn_return_value = None
    Is_PatternSheet = Boolean()
    # 01.01.20:
    #--------------------------------------------------------------
    # Check if the sheet is an data sheet
    # VB2PY (UntranslatedCode) On Error Resume Next
    _fn_return_value = ( Sh.Range('RGB_Modul_Nr').Address != '' )
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return _fn_return_value

def worksheet_redraw(sheet):
    if sheet.Datasheet:
        sheet.clear_shapelist()
        sheet.recreate_controls()
        X02.ActiveSheet=sheet
        PG.button_aktualisieren_cmd()
        

def Global_On_Enter_Proc():
    Offs = Long()
    # 01.01.20
    #--------------------------------
    ## VB2PY (CheckDirective) VB directive took path 2 on DEBUG_CHANGEEVENT
    if Is_Data_Sheet(X02.ActiveSheet):
        if not X02.IsError(X02.ActiveCell()):
            # 15.01.20:
            if X02.ActiveCell() == '' or X02.ActiveCell() == '?':
                _select1 = X02.ActiveCell().Address
                if (_select1 == X02.Range('Goto_Aktivierung').Address):
                    pattgen.M14_Select_GotoAct.Select_GotoAct()
                elif (_select1 == X02.Range('Special_Mode').Address):
                    pattgen.M60_Select_LED.Select_Special_Mode()
                elif (_select1 == X02.Range('RGB_Modul_Nr').Address):
                    pattgen.M60_Select_LED.Get_LED_Address_Dialog()
                elif (_select1 == X02.Range('CPX_LED_Assignement').Address):
                    pattgen.M55_PWM_Data_Send.LED_Assignement_Dialog()
    # Select next cell, but not a hidden cell
    Offs = 1
    while 1:
        if X02.ActiveCell().offset(Offs, 0).EntireRow.Hidden:
            Offs = Offs + 1
        else:
            break
        if not (Offs < 1000):
            break
    X02.ActiveCell().offset(Offs, 0).Select()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cancel - ByRef 
def Proc_DoubleCkick(Sh, Target, Cancel):
    # 01.01.20
    #----------------------------------------------------------------------------------------------
    Cancel = False
    if Is_Data_Sheet(X02.ActiveSheet):
        _select2 = X02.ActiveCell().Address
# Cancel = True to disable the standard function => Don't go into cell edit mode
        if (_select2 == X02.Range('Goto_Aktivierung').Address):
            Cancel = True
            pattgen.M14_Select_GotoAct.Select_GotoAct()
        elif (_select2 == X02.Range('Special_Mode').Address):
            Cancel = True
            pattgen.M60_Select_LED.Select_Special_Mode()
        elif (_select2 == X02.Range('RGB_Modul_Nr').Address):
            Cancel = True
            pattgen.M60_Select_LED.Get_LED_Address_Dialog()
        elif (_select2 == X02.Range('CPX_LED_Assignement').Address):
            Cancel = True
            pattgen.M55_PWM_Data_Send.LED_Assignement_Dialog()
    return Cancel

def Global_Worksheet_Deactivate():
    # 02.06.20: Misha
    #---------------------------------------
    X02.Application.OnKey('{Return}', '')
    # 27.10.20:
    if pattgen.M80_Multiplexer_INI_Handling.TestPatternButtonOn:
        Debug.Print('Global_Worksheet_Deactivate called => Stop executing the Displaying of a Pattern')
        pattgen.M80_Multiplexer_INI_Handling.Button_Pressed_Handling('Test_Leds_M99O01', True)
        # Stop executing the Displaying of a Pattern

# VB2PY (UntranslatedCode) Option Explicit
