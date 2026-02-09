from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbclasses import *
import ExcelAPI.XLA_Application as X02
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M01_Public_Constants_a_Var as M01
import ExcelAPI.XLWA_WinAPI as X03
import pattgen.M09_Language as M09
import mlpyproggen.Pattern_Generator as PG
import pgcommon.G00_common as G00
import os

""" Used with GetAsyncKeyState

------------------------------------------
"""

VK_CONTROL = 0x11
CP_UTF8 = 65001

def IsFilled(c):
    _fn_return_value = None
    #---------------------------------------
    _fn_return_value = Trim(c.Value) != ''
    if isinstance(c.Value, list):
        _fn_return_value = False
    return _fn_return_value

def LastFilledColumn(Rng, LastRow):
    _fn_return_value = None
    #*HL c = X02.Range()

    MaxColumn = Long()
    #---------------------------------------------------------------
    # Die Funktion läuft durch alle Spalten und alle Reihen im angegebenen Bereich
    # Das ist nicht besonders schnell
    # => Die Funktion sollte nicht mehr genutzt werden.
    #    Ersetzt durch LastFilledColumn2()
    # Find the last used column
    #if type(Rng)==X02.CRange:        #*HL
    #    _fn_return_value=Rng.Column #*HL 
    #else:                           #*HL
    
    
    for c in Rng:
        if c.Row > LastRow:
            break
        if IsFilled(c) and c.Column > MaxColumn:
            MaxColumn = c.Column
    _fn_return_value = MaxColumn
    return _fn_return_value

def LastFilledColumn2(Rng, LastRow):
    return LastFilledColumn(Rng, LastRow) #*HL
    #return Rng.get_last_used_column(LastRow)

    _fn_return_value = None
    Row = Long()

    MaxColumn = Long()

    LastF = Long()

    FirstRow = Long()
    # 20.11.19:
    #--------------------------------------------------------------------
    # Faster than LastFilledColumn() because it doesn't loop through al columns
    FirstRow = Rng.Row
    # Find the last used column
    _with2 = Rng.Worksheet
    for Row in vbForRange(FirstRow, LastRow):
        LastF = _with2.Cells(Row, _with2.Cells(Row, 1).EntireRow.Columns.Count).End(X01.xlToLeft).Column
        if LastF > MaxColumn:
            MaxColumn = LastF
    _fn_return_value = MaxColumn
    return _fn_return_value

def LastUsedRowIn(Sheet):
    _fn_return_value = None
    Sh = Variant()
    #-----------------------------------------------
    # return the last used row in the given sheet.
    # The sheet could be given as sheet name or as worksheets variable.
    if X02.VarType(Sheet) == vbString:
        Sh = X02.Sheets(Sheet)
    else:
        Sh = Sheet
    ## VB2PY (CheckDirective) VB2PY Python directive
    _fn_return_value = Sh.get_LastUsedRow()
    Sh = None
    return _fn_return_value

def LastUsedColumnInRow(Sh, Row):
    return Sh.LastUsedColumn #*HL

    _fn_return_value = None
    #---------------------------------------------------------------
    _fn_return_value = Sh.Cells(Row, Sh.Columns.Count).End(X01.xlToLeft).Column
    return _fn_return_value

def LastFilledRowIn(Sh, FirstCheckCol, LastCheckCol):
    _fn_return_value = None
    Row = Long()
    #---------------------------------------------------------------------------------------------
    Row = LastUsedRowIn(Sh)
    _with3 = Sh
    while _with3.Cells(Row, FirstCheckCol).End(X01.xlToRight).Column > LastCheckCol:
        Row = Row - 1
    _fn_return_value = Row
    return _fn_return_value

def Test_LastFilledRowIn():
    Start = Variant()
    #UT------------------------------------------
    Start = Timer()
    Debug.Print(LastFilledRowIn(X02.ActiveSheet, 4, M01.Last_LEDsCol) + 'Duration: ' + Round(Timer() - Start, 2))

def LastUsedColumn():
    _fn_return_value = None
    #--------------------------------
    _fn_return_value = X02.ActiveSheet.UsedRange.Columns(X02.ActiveSheet.UsedRange.Columns.Count).Column
    return _fn_return_value

def LastUsedColumnIn(Sheet):
    _fn_return_value = None
    Sh = Variant()
    #--------------------------------------------------
    if X02.VarType(Sheet) == vbString:
        Sh = X02.Sheets(Sheet)
    else:
        Sh = Sheet
    _fn_return_value = Sh.UsedRange.Columns(Sh.UsedRange.Columns.Count).Column
    Sh = None
    return _fn_return_value

def Row_Filled_w_Attrib(Rng, LastAttrCheckCol):
    _fn_return_value = False
    c = X02.Range()
    #----------------------------------------------------------------------------------------
    # Check if the row in the given Range is used
    # - The whole range is checked for characters
    # - Only the first columns until LastAttrCheckCol are checked for fill color
    if Rng.End(X01.xlToRight).Column <= Rng.Column + Rng.Columns.Count:
        Debug.Print("Row_Filled_w_Attrib",Rng.End(X01.xlToRight).Column,Rng.Column, Rng.Columns.Count)
        _fn_return_value = True
        return _fn_return_value
    for c in Rng:
        if c.Column > LastAttrCheckCol:
            return _fn_return_value
        if c.Interior.Color != 16777215:
            _fn_return_value = True
            return _fn_return_value
    return _fn_return_value

def LastFilledRowIn_w_Attrib(Sh, FirstCheckCol, LastCheckCol, LastAttrCheckCol):
    _fn_return_value = None
    Row = Long()

    Last_u_Col = Long()
    #--------------------------------------------------------------------------------------------------------------------------------
    Row = LastUsedRowIn(Sh)
    _with4 = Sh
    while Row_Filled_w_Attrib(_with4.Range(_with4.Cells(Row, FirstCheckCol), _with4.Cells(Row, LastCheckCol)), LastAttrCheckCol) == 0 and Row > 0:
        Row = Row - 1
    _fn_return_value = Row
    return _fn_return_value

def Test_LastFilledRowIn_w_Attrib():
    Start = Variant()
    #UT----------------------------------------
    Start = Timer()
    Debug.Print(LastFilledRowIn_w_Attrib(X02.ActiveSheet, 4, M01.Last_LEDsCol, M01.Last_LEDs_ChkAttrCol) + 'Duration: ' + Round(Timer() - Start, 2))

def SheetEx(Name):
    _fn_return_value = None
    s = Variant()
    #-------------------------------
    for s in X02.Worksheets: #*HL
        if s.Name == Name:
            _fn_return_value = True
            return _fn_return_value
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
def Replace_Illegal_Char(s):
    _fn_return_value = ""
    OldChars = 'ä,  ö,  ü,  Ä,  Ö,  Ü,  ß'

    NewChars = 'ae, oe, ue, Ae, Oe, Ue, ss'

    OldList = vbObjectInitialize(objtype=String)

    NewList = vbObjectInitialize(objtype=String)

    i = Long()

    Res = String()
    #---------------------------------------------------------
    # ToDo: Add the characters from other languages (French, Dutch, ...)
    OldList = Split(OldChars, ',')
    NewList = Split(NewChars, ',')
    Res = s
    for i in vbForRange(0, UBound(OldList) - 1):
        Res = Replace(Res, Trim(OldList(i)), Trim(NewList(i)))
    Res = Replace(Res, ' ', '_')
    for i in vbForRange(1, Len(Res)):
        c = Mid(Res, i, 1)
        if c >= '0' and c <= '9' or c >= 'A' and c <= 'Z' or c >= 'a' and c <= 'z' or c == '_':
            _fn_return_value = _fn_return_value + c
    return _fn_return_value

def Test_Replace_Illegal_Char():
    #UT------------------------------------
    Debug.Print(Replace_Illegal_Char('Hallo Was Geht äö(2346$ Test'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def FileNameExt(Name):
    _fn_return_value = None
    Pos = Long()

    Pos2 = Long()

    Temp = String()
    #---------------------------------------------------
    # Return name and extention without path
    Pos = InStrRev(Name, '\\')
    Pos2 = InStrRev(Name, '/')
    # 22.11.13: Added to support also links like https://share.gm.com/sites/gmesc/WHO/Shared%20Documents/Documents/Other/Testresults.xlsm
    if Pos2 > Pos:
        Pos = Pos2
    if Pos > 0:
        Temp = Mid(Name, Pos + 1)
    else:
        Pos = InStrRev(Name, ':')
        if Pos > 0:
            Temp = Mid(Name, Pos + 1)
        else:
            Temp = Name
    _fn_return_value = Temp
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def FilePath(Name):
    _fn_return_value = None
    #------------------------------------------------
    _fn_return_value = Left(Name, Len(Name) - Len(FileNameExt(Name)))
    return _fn_return_value

def NoExt(Name):
    _fn_return_value = None
    Pos = Long()
    #----------------------------------------
    # Cut of the extention of a filename
    Pos = InStrRev(Name, '.')
    if Pos > 0:
        _fn_return_value = Left(Name, Pos - 1)
    else:
        _fn_return_value = Name
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def FileExt(Name):
    _fn_return_value = None
    Pos = Long()
    #-----------------------------------------------
    # Return the file extention including the point
    Pos = InStrRev(Name, '.')
    if Pos > 0:
        _fn_return_value = Mid(Name, Pos)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def FileName(Name):
    _fn_return_value = None
    #------------------------------------------------
    # Return name without extention and path
    _fn_return_value = NoExt(FileNameExt(Name))
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: FullName - ByVal 
def Same_Name_already_open(FullName):
    _fn_return_value = None
    w = Variant()

    Name = String()
    #-------------------------------------------------------------------
    # Check if a workbook with the same name is already opened
    Name = FileNameExt(FullName)
    for w in X02.Workbooks:
        if UCase(w.Name) == UCase(Name):
            _fn_return_value = True
            return _fn_return_value
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SheetName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Add_to_Duplicate_Name='_Copy_' - ByVal 
def Unic_SheetName(SheetName, Add_to_Duplicate_Name='_Copy_'):
    _fn_return_value = None
    OrgName = String()

    Cnt = Long()
    #----------------------------------------------------------------------------------------------------------------------
    OrgName = SheetName
    while SheetEx(SheetName):
        Cnt = Cnt + 1
        while 1:
            SheetName = OrgName + Add_to_Duplicate_Name + str(Cnt)
            if Len(SheetName) > 31:
                CutOff = Len(SheetName) - 31
                if CutOff <= Len(Add_to_Duplicate_Name):
                    Add_to_Duplicate_Name = DelLast(Add_to_Duplicate_Name, CutOff)
                else:
                    Add_to_Duplicate_Name = ''
                    OrgName = DelLast(OrgName)
                    # 07.07.20: Prevent endless Loop   Old: SheetName = DelLast(SheetName)
            if not (Len(SheetName) > 31):
                break
        # Repeat until it's <= 31
    _fn_return_value = SheetName
    return _fn_return_value

def Test_Unic_SheetName():
    #UT------------------------------
    Debug.Print('Unic_SheetName:' + Unic_SheetName('KS_Hauptsignal_Zs3_Zs 6_Zs1_RGB'))

def Protect_Active_Sheet():
    #-------------------------
    X02.ActiveSheet.Protect(DrawingObjects=True, Contents=True, Scenarios=True, AllowFormattingCells=True, AllowInsertingHyperlinks=True)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def Protect_Sheet(Sh):
    # 07.03.20:
    #---------------------------------------
    Sh.Protect(DrawingObjects=True, Contents=True, Scenarios=True, AllowFormattingCells=True, AllowInsertingHyperlinks=True)

def GetPathOnly(sPath):
    _fn_return_value = None
    #------------------------------------------------------
    #*HL _fn_return_value = Left(sPath, InStrRev(sPath, '/', Len(sPath)) - 1) #HL // durch / ersetzt
    
    _fn_return_value = os.path.dirname(sPath) #*HL
    return _fn_return_value

def CreateFolder(sFolder):
    _fn_return_value = None
    s = String()
    #--------------------------------------------------------
    # http://www.freevbcode.com/ShowCode.asp?ID=257
    # VB2PY (UntranslatedCode) On Error GoTo ErrorHandler
    s = GetPathOnly(sFolder)
    if Dir(s, vbDirectory) == '':
        s = CreateFolder(s)
        MkDir(s)
    _fn_return_value = sFolder
    return _fn_return_value


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
def NrStr2d(s):
    _fn_return_value = None
    #--------------------------------------------
    if X02.Application.International(X01.xlDecimalSeparator) == ',':
        _fn_return_value = Val(Replace(s, '.', ','))
    else:
        _fn_return_value = Val(Replace(s, ',', '.'))
    return _fn_return_value

def CorrectKomma(s):
    _fn_return_value = None
    #-------------------------------------------
    if X02.Application.International(X01.xlDecimalSeparator) == ',':
        _fn_return_value = Replace(s, '.', ',')
    else:
        _fn_return_value = Replace(s, ',', '.')
    return _fn_return_value

def t():
    Res = Variant()
    Res = X02.Application.International(X01.xlDecimalSeparator)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cnt=1 - ByVal 
def DelLast(s, Cnt=1):
    _fn_return_value = None
    #----------------------------------------------------------------------------
    if Len(s) > 0:
        _fn_return_value = Left(s, Len(s) - Cnt)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
def DelAllLast(s, Chars):
    _fn_return_value = None
    #----------------------------------------------------------------
    while InStr(Chars, Right(s, 1)) > 0:
        s = Left(s, Len(s) - 1)
    _fn_return_value = s
    return _fn_return_value

def Center_Form(f):
    #---------------------------
    # Manchmal funktioniert das nicht beim starten des Programms weil das Excel Programm                  13.06.20:
    # Noch nicht richtig geöffnet ist und darum noch kein eigenes Fenster hat. Dann werden
    # die Positionen eines zufor geöffenetn Exce Programms benutzt und der Dialog wird zentriert
    # zu diesem Dialog gezeigt. Als Abhilfe habe ich mal "ThisWorkbook." eingefügt...
    # Aufgefallen ist es beim "Examples_UserForm".
    X02.DoEvents()
    _with5 = f
    _with5.StartupPosition = 0
    _with5.Left = PG.ThisWorkbook.Application.Left +  ( PG.ThisWorkbook.Application.Width - _with5.Width )  / 2
    _with5.Top = PG.ThisWorkbook.Application.Top +  ( PG.ThisWorkbook.Application.Height - _with5.Height )  / 2

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByVal 
def Replace_Double_Space(Txt):
    _fn_return_value = None
    Res = String()
    #-----------------------------------------------------------
    Res = Txt
    while InStr(Res, '  ') > 0:
        Res = Replace(Res, '  ', ' ')
    _fn_return_value = Res
    return _fn_return_value

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

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByVal 
def Get_Position_In_Array(Txt, Arr):
    e = Variant()

    Nr = int()
    #----------------------------------------------------------------------------------
    fn_return_value = - 1
    if not isInitialised(Arr):
        return fn_return_value
    Nr = 0 #LBound(Arr)
    Txt = Trim(Txt)
    for e in Arr:
        if Trim(e) == Txt:
            fn_return_value = Nr
            return fn_return_value
        Nr = Nr + 1
    return fn_return_value



# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByVal 
def Is_Contained_in_Array(Txt, Arr):
    _fn_return_value = None
    e = Variant()
    #-------------------------------------------------------------------------------------
    #If StrPtr(Arr) = 0 Then Exit Function
    # 06.05.20: Jürgen
    if not isInitialised(Arr):
        return _fn_return_value
    # 06.05.20:
    Txt = Trim(Txt)
    for e in Arr:
        if Trim(e) == Txt:
            _fn_return_value = True
            return _fn_return_value
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: stringToBeFound - ByVal 
def IsInArray(stringToBeFound, Arr):
    _fn_return_value = None
    i = Long()
    #--------------------------------------------------------------------------
    # default return value if value not found in array
    _fn_return_value = - 1
    for i in vbForRange(LBound(Arr), UBound(Arr)):
        if StrComp(stringToBeFound, Arr(i), X01.vbTextCompare) == 0:
            _fn_return_value = i
            break
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: StartHide_Name - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: StartMove_Name - ByVal 
def Hide_and_Move_up(dlg, StartHide_Name, StartMove_Name):
    MoveDelta = Double()

    StartHide_y = Double()

    StartMove_y = Double()

    c = Variant()
    #---------------------------------------------------------------------------------------------------------
    # Hide the controls where StartHide_y <= controls.Top < StartMove_y
    # Move the controls up where controls.Top >= StartMove_y
    # 04.06.20: Changed from long to double
    StartHide_y = dlg.ControlsFind(StartHide_Name).Top
    StartMove_y = dlg.ControlsFind(StartMove_Name).Top
    MoveDelta = StartMove_y - StartHide_y
    #Debug.Print "Hide_and_Move_up from '" & StartHide_Name & "' to '" & StartMove_Name & "' " & MoveDelta
    # Debug
    for c in dlg.Controls:
        if c.Top >= StartMove_y:
            c.Top = c.Top - MoveDelta
        elif c.Top >= StartHide_y:
            c.Visible = False
    dlg.Height = dlg.Height - MoveDelta

def EndProg():
    #-------------------
    # Is called in case of an fatal error
    # Normaly this function should not be called because the
    # global variables and dialog positions are cleared.
    Enable_Application_Automatics()
    X02.Application.EnableEvents = True
    X02.Application.ScreenUpdating = True
    Debug.Print("Error in Dialog: End_Prog()")
    raise Exception("Error in Dialog")    
    #sys.exit(0)

def Enable_Application_Automatics():
    #-----------------------------------------
    X02.Application.EnableEvents = True
    X02.Application.ScreenUpdating = True
    X02.ActiveSheet.EnableCalculation = True
    X02.Application.Calculation = X01.xlCalculationAutomatic

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def ValidNameCharacters(Name):
    _fn_return_value = None
    Pos = Integer()

    Res = String()

    c = String()
    #------------------------------------------------------------------
    for Pos in vbForRange(1, Len(Name)):
        c = Mid(Name, Pos, 1)
        if ( c >= 'A' and c <= 'Z' )  or  ( c >= 'a' and c <= 'z' )  or  ( c >= '0' and c <= '9' ) :
            Res = Res + c
        else:
            _select3 = c
            if (_select3 == 'ä'):
                Res = Res + 'ae'
                # Todo: Check alo characters fron other languages (French, ...)
            elif (_select3 == 'Ä'):
                Res = Res + 'Ae'
            elif (_select3 == 'ö'):
                Res = Res + 'oe'
            elif (_select3 == 'Ö'):
                Res = Res + 'Oe'
            elif (_select3 == 'ü'):
                Res = Res + 'ue'
            elif (_select3 == 'Ü'):
                Res = Res + 'Ue'
            elif (_select3 == 'ß'):
                Res = Res + 'ss'
            else:
                if Right(Res, 1) != '_':
                    Res = Res + '_'
    _fn_return_value = Res
    return _fn_return_value

def F_shellExec(sCmd):
    _fn_return_value = None
    oShell = WshShell()
    #----------------------------------------------------
    # Excecute command and get the output as string
    # Example call:
    #   MsgBox F_shellExec("cmd /c dir c:\")
    #
    # Requires ref to Windows Script Host Object Model
    # To do this go to Extras -> References in the VBA IDE's menu bar.
    # See:
    #   https://stackoverflow.com/questions/2784367/capture-output-value-from-a-shell-command-in-vba
    _fn_return_value = oShell.Exec(sCmd).StdOut.ReadAll
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: WindowMode - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Wait - ByVal 
def F_shellRun(sCmd, WindowMode, Wait):
    oShell = WshShell()
    #----------------------------------------------------------------------------------------
    # Excecute command
    # Example call:
    #   MsgBox F_shellRun("cmd /c dir c:\", 0, true)
    #
    #0: versteckt das Fenster und aktiviert ein anderes
    #1: aktiviert und zeigt ein Fenster
    #2: aktiviert und minimiert das Fenster
    #3: aktiviert und maximiert das Fenster
    #4: zeigt das Fenster in seiner letzen Position, das aktive Fenster bleibt aktiv
    #5: zeigt das Fenster in seiner letzen grösse und Position
    #6: minimiert das Fenster und aktiviert ein anderes
    #7: minimiert das Fenster, das aktive Fenster bleibt aktiv
    #8: zeigt das Fenster in seiner letzen Position, das aktive Fenster bleibt aktiv
    #9: stellt ein minimiertes Fenster wieder in seinen ursprünglichen Zustand
    #10: setzt das Fenster gleich dem Programm
    oShell.Run(sCmd, WindowMode, Wait)

def Test_Shell():
    #UT---------------------
    X02.MsgBox(F_shellExec('cmd /c Dir C:\\'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Nr - ByVal 
def Hex02(Nr):
    _fn_return_value = None
    #--------------------------------------------
    _fn_return_value = Right('0' + Hex(Nr), 2)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Value - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
def SHR(Value, Shift):
    _fn_return_value = None
    i = Byte()
    #--------------------------------------------------------------------
    _fn_return_value = Value
    if Shift > 0:
        _fn_return_value = Int(SHR() /  ( 2 ** Shift ))
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Value - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
def SHL(Value, Shift):
    _fn_return_value = None
    #--------------------------------------------------------------------
    _fn_return_value = Value
    if Shift > 0:
        for i in vbForRange(1, Shift):
            m = SHL() and 0x40000000
            _fn_return_value = ( SHL() and 0x3FFFFFFF )  * 2
            if m != 0:
                _fn_return_value = SHL() or 0x80000000
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParamStr - ByRef 
def Replace_Const(ParamStr, ReplaceList, MainDelimmiter, SubDelimmiter):
    ReplacePair = Variant()
    #---------------------------------------------------------------------------------------------------------------------------
    for ReplacePair in Split(ReplaceList, MainDelimmiter):
        if Trim(ReplacePair) != '':
            Parts = Split(ReplacePair, SubDelimmiter)
            ParamStr = Replace(ParamStr, Trim(Parts(0)), Trim(Parts(1)))
    return ParamStr #*HL ByRef

def Test_Dec_Sep():
    p_str = String()
    #-------------------------
    # Die Val() Funktion liefert auch wenn als Dezimaltrennzeichen ein "," eingestellt ist
    # den richtigen Wert
    # => Es ist O.K. wenn man bei den Zeiten immer den "." als trennzeichen verwendt.
    p_str = '1.3'
    Debug.Print(Val(p_str) * 2)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Parm - ByVal 
def Convert_TimeStr_to_ms(Parm):
    _fn_return_value = None
    ReplaceList = 'Ms > ms; sec > Sec; sek > Sec; Sek > Sec; , > .; - > + -'

    DivideBy16 = Boolean()

    Part = Variant()

    NrStr = String()

    Res = Long()
    #------------------------------------------------------------------
    # Converte a string like "3.5 Min + 2.4 Sec + 200 ms"
    # to a two byte string
    # Return -99999 in case of an error
    Parm = Replace_Const(Parm, ReplaceList, ';', '>')
    if InStr(Parm, '/16') > 0:
        # It's o.k. if there is only one "/16" in a sum. We divide the whole result even
        DivideBy16 = True
        # if this is not mathematicaly correct because we assume that prior checks make
        Parm = Replace(Parm, '/16', '')
        # shure that all sumands have a "/16"
    for Part in Split(Parm, '+'):
        Part = Trim(Part)
        if Part != '':
            if Right(Part, Len(' Sec')) == ' Sec':
                NrStr = Trim(Replace(Part, 'Sec', ''))
                if IsNumeric(NrStr):
                    Res = Res + Int(Val(NrStr) * 1000 + 0.00001)
                    # Add + 0.00001 to prevent round error 2.4 Sec => 2399
                else:
                    _fn_return_value = - 99999
                    return _fn_return_value
            elif Right(Part, Len(' Min')) == ' Min':
                NrStr = Trim(Replace(Part, 'Min', ''))
                if IsNumeric(NrStr):
                    Res = Res + Int(Val(NrStr) * 60 * 1000 + 0.00001)
                else:
                    _fn_return_value = - 99999
                    return _fn_return_value
            elif Right(Part, Len(' ms')) == ' ms':
                NrStr = Trim(Replace(Part, 'ms', ''))
                if IsNumeric(NrStr):
                    Res = Res + Int(Val(NrStr))
                else:
                    _fn_return_value = - 99999
                    return _fn_return_value
            else:
                NrStr = Trim(Part)
                if IsNumeric(NrStr):
                    Res = Res + Int(Val(NrStr))
                else:
                    _fn_return_value = - 99999
                    return _fn_return_value
    if DivideBy16:
        Res = Res / 16
    _fn_return_value = Res
    return _fn_return_value

def Test_Convert_TimeStr_to_ms():
    #UT-------------------------------------
    Debug.Print(Convert_TimeStr_to_ms('3.5 Min + 2.4 Sek + 200 ms') + ' should be 212600')
    #Debug.Print Convert_TimeStr_to_ms("3.5 Min - 2.4 Sek + 200 ms") & " should be 207800"
    #Debug.Print Convert_TimeStr_to_ms("- 2.4 Sek + 3.5 Min  + 200 ms") & " should be 207800"
    #Debug.Print Convert_TimeStr_to_ms("2,5 Sekunden") & " should be -99999"
    #Debug.Print Convert_TimeStr_to_ms("2673 Sek") & " should be 2673000"

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Val - ByVal 
def Long_to_2ByteStr(Val):
    _fn_return_value = None
    LowByte = Byte()

    HighByte = Byte()
    #------------------------------------------------------------
    # Generates: "13, 16"
    LowByte = Val and 0xFF
    HighByte = Int(Val / 256)
    _fn_return_value = LowByte + ', ' + HighByte
    return _fn_return_value

def ClearStatusbar():
    #--------------------------
    # Is called by onTime to clear the status bar after a while
    X02.Application.StatusBar = ''

def Show_Status_for_a_while(Txt, Duration='00:00:15'):
    #-------------------------------------------------------------------------------------------
    X02.Application.StatusBar = Txt
    if Txt != r'':
        X02.Application.OnTime(15000, ClearStatusbar)
    else:
        X02.Application.OnTime(15000, ClearStatusbar)
 
def InputBoxMov(prompt, Title=VBMissingArgument, Default=VBMissingArgument, Left=VBMissingArgument, Top=VBMissingArgument, helpfile=VBMissingArgument, HelpContextID=VBMissingArgument):
    _fn_return_value = None
    OldUpdate = Boolean()
    #--------------------------------------------------------------------------------------------------------
    # InputBox which could be moved with correct screen update even if screenupdating is disabled
    OldUpdate = X02.Application.ScreenUpdating
    X02.Application.ScreenUpdating = True
    _fn_return_value = G00.InputBox(prompt, Title, Default, Left, Top, helpfile, HelpContextID)
    X03.Sleep(50)
    # Time to update the display
    X02.Application.ScreenUpdating = OldUpdate
    return _fn_return_value

def Test_InputBoxMov():
    #UT---------------------------
    X02.Application.ScreenUpdating = False
    Debug.Print(InputBoxMov('Hallo', 'Title', 'Dafault'))
    X02.Application.ScreenUpdating = True

def MsgBoxMov(prompt, Buttons=VBMissingArgument, Title=VBMissingArgument, helpfile=VBMissingArgument, context=VBMissingArgument):
    _fn_return_value = None
    OldUpdate = Boolean()
    #----------------------------------------------------------------------------------------
    # MsgBox which could be moved with correct screen update even if screenupdating is disabled
    OldUpdate = X02.Application.ScreenUpdating
    X02.Application.ScreenUpdating = True
    _fn_return_value = X02.MsgBox(prompt, Buttons, Title, helpfile, context)
    X03.Sleep(50)
    # Time to update the display
    X02.Application.ScreenUpdating = OldUpdate
    return _fn_return_value

def Test_MsgBoxMov():
    #UT-------------------------
    X02.Application.ScreenUpdating = False
    Debug.Print(MsgBoxMov('Hallo', vbYesNoCancel, 'Titel'))
    X02.Application.ScreenUpdating = True

def myInStr(s, search):
    _fn_return_value = None
    #--------------------------------
    _fn_return_value = InStr(s, search)
    return _fn_return_value

def Read_File_to_String(FileName):
    try:
        #open text file in read mode
        text_file = open(FileName, "r")
         
        #read whole file to a string
        fn_return_value = text_file.read()
         
        #close file
        text_file.close()        

        return fn_return_value
    except:
        Debug.Print("Read_File_to_String: Fehler beim Lesen der Datei "+FileName)
        X02.MsgBox(M09.Get_Language_Str(r'Fehler beim lesen der Datei:') + vbCr + r'  ' + FileName + r'', vbCritical, M09.Get_Language_Str(r'Fehler beim Datei lesen'))
        fn_return_value = r'#ERROR#'
        return fn_return_value    
    
    
    #_fn_return_value = None
    #strFileContent = String()

    #fp = Integer()
    #----------------------------------------------------------------
    #fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo ReadError
    #VBFiles.openFile(fp, FileName, 'r') 
    #_fn_return_value = Input(LOF(fp), fp)
    #VBFiles.closeFile(fp)
    #return _fn_return_value
    #X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler beim lesen der Datei:') + vbCr + '  \'' + FileName() + '\'', vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler beim Datei lesen'))
    #_fn_return_value = '#ERROR#'
    #return _fn_return_value

def Get_Ini_Entry(FileStr, EntryName):
    _fn_return_value = None
    p = Long()

    e = String()
    #------------------------------------------------------------------------------
    _fn_return_value = '#ERROR#'
    p = InStr(FileStr, EntryName)
    if p == 0:
        return _fn_return_value
    p = p + Len(EntryName)
    e = InStr(p, FileStr, vbCr)
    if e == 0:
        e = InStr(p, FileStr, vbLf)
    if e == 0:
        return _fn_return_value
    _fn_return_value = Mid(FileStr, p, e - p)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Source - ByRef 
def ConvertToUTF8(Source):
    _fn_return_value = None
    Length = Long()

    Pointer = LongPtr()

    Size = Long()

    Buffer = vbObjectInitialize(objtype=Byte)
    #---------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    # 28.05.20:
    Length = Len(Source)
    Pointer = StrPtr(Source)
    Size = X03.WideCharToMultiByte(CP_UTF8, 0, Pointer, Length, 0, 0, 0, 0)
    Buffer = vbObjectInitialize(((0, Size - 1),), Variant)
    X03.WideCharToMultiByte(CP_UTF8, 0, Pointer, Length, VarPtr(Buffer(0)), Size, 0, 0)
    _fn_return_value = Buffer
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Source - ByRef 
def ConvertToUTF8Str(Source):
    _fn_return_value = None
    Bytes = vbObjectInitialize(objtype=Byte)

    Res = String()

    i = Variant()
    #-----------------------------------------------------------------
    Bytes = ConvertToUTF8(Source)
    for i in vbForRange(0, UBound(Bytes)):
        Res = Res + Chr(Bytes(i))
    _fn_return_value = Res
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Source - ByRef 
def ConvertFromUTF8(Source):
    Source_str = str(Source)
    _fn_return_value =  Source_str.decode('utf-8')
    
    #_fn_return_value = None
    #Size = Long()

    #Pointer = LongPtr()

    #Length = Long()

    #Buffer = String()
    # 26.05.20:
    #----------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    # 28.05.20:
    #Size = UBound(Source) - LBound(Source) + 1
    #Pointer = VarPtr(Source(LBound(Source)))
    #Length = X03.MultiByteToWideChar(CP_UTF8, 0, Pointer, Size, 0, 0)
    #Buffer = Space(Length)
    #X03.MultiByteToWideChar(CP_UTF8, 0, Pointer, Size, StrPtr(Buffer), Length)
    #_fn_return_value = Buffer
    return _fn_return_value

def ConvertUTF8Str(UTF8Str):
    return UTF8Str

    _fn_return_value = None
    bStr = vbObjectInitialize(objtype=Byte)

    i = Long()
    # 26.05.20:
    #----------------------------------------------------------
    bStr = vbObjectInitialize((Len(UTF8Str) - 1,), Variant)
    for i in vbForRange(1, Len(UTF8Str)):
        bStr[i - 1] = Asc(Mid(UTF8Str, i, 1))
    _fn_return_value = ConvertFromUTF8(bStr)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: vArrayName - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lUpper=- 1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lLower=- 1 - ByVal 
def Array_BubbleSort(vArrayName, lUpper=- 1, lLower=- 1):
    vtemp = Variant()

    i = Long()

    j = Long()
    #---------------------------------------------------------
    # https://bettersolutions.com/vba/arrays/sorting-bubble-sort.htm
    if X02.IsEmpty(vArrayName) == True:
        return
    if lLower == - 1:
        lLower = LBound(vArrayName, 1)
    if lUpper == - 1:
        lUpper = UBound(vArrayName, 1)
    for i in vbForRange(lLower, ( lUpper - 1 )):
        for j in vbForRange(i, lUpper):
            if ( vArrayName(j) < vArrayName(i) ) :
                vtemp = vArrayName(i)
                vArrayName[i] = vArrayName(j)
                vArrayName[j] = vtemp

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Text - ByVal 
def Button_Setup(Button, Text):
    Err = Boolean()
    #---------------------------------------------------------------------
    # If text is empty the button is not shown
    Text = Trim(Text)
    Button.Visible = ( Text != '' )
    if Text != '':
        Err = ( Len(Text) < 3 )
        if not Err:
            Err = ( Mid(Text, 2, 1) != ' ' )
        if Err:
            X02.MsgBox('Internal Error: Button text is wrong \'' + Text + '\'.' + vbCr + 'It must contain an Accelerator followed by the text.' + vbCr + 'Example: \'H Hallo\'', vbCritical, 'Internal Error (Wrong translation?)')
            EndProg()
        Button.Caption = Mid(Text, 3, 255)
        Button.Accelerator = Left(Text, 1)

def Bring_to_front():
    # 20.05.20:
    #--------------------------
    # Is not working if an other application has be moved above Excel wit Alt+Tab
    # But this is a feature od Windows.
    # See: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow
    # But it brings up excel again after the upload to the Arduino
    # Without this funchion an other program was activated after the upload for some reasons
    PG.ThisWorkbook.Activate()
    X03.SetForegroundWindow(X02.Application.hWnd)

def Is_Minimized(Name):
    _fn_return_value = None
    guid = vbObjectInitialize(((0, 3),), Variant)

    acc = Object()

    hWnd = Variant()

    hwnd2 = Variant()

    hwnd3 = Variant()
    # 31.05.20:
    #---------------------------------------------------
    # Adapted from
    # https://stackoverflow.com/questions/5292626/couldnt-find-child-window-using-findwindowexa
    _fn_return_value = - 1
    # Not found
    ## VB2PY (CheckDirective) VB directive took path 1 on VB2PY
    guid[0] = 0x20400
    guid[1] = 0x0
    guid[2] = 0xC0
    guid[3] = 0x46000000
    while 1:
        hWnd = X03.FindWindowExA(0, hWnd, vbNullString, vbNullString)
        if hWnd == 0:
            break
        hwnd2 = X03.FindWindowExA(hWnd, 0, 'XLDESK', vbNullString)
        hwnd3 = X03.FindWindowExA(hwnd2, 0, 'EXCEL7', vbNullString)
        if X03.AccessibleObjectFromWindow(hwnd3, 0xFFFFFFF0, guid(0), acc) == 0:
            Debug.Print(hWnd + '  ' + acc.Caption + '  ' + X03.IsIconic(hWnd))
            if acc.Caption == Name:
                _fn_return_value = X03.IsIconic(hWnd)
                return _fn_return_value
    return _fn_return_value

def Test_Is_Minimized():
    #UT----------------------------
    #Debug.Print "Is_Minimized:" & Is_Minimized("Prog_Generator_MobaLedLib.xlsm")
    Debug.Print(PG.ThisWorkbook.Name + ' Is_Minimized:' + Is_Minimized(PG.ThisWorkbook.Name))

def VersionStr_is_Greater(Ver1, Ver2, Delimmiter='.'):
    _fn_return_value = None
    Ver1A = vbObjectInitialize(objtype=String)

    Ver2A = vbObjectInitialize(objtype=String)

    EndNr = Long()

    Nr = Long()
    #--------------------------------------------------------------------------------------------------------------------
    # Compares two version strings like
    #  "1.0.7"
    # If one string is shorter than the other the missing digits are replaced by 0
    # "1.0" => "1.0.0"
    Ver1A = Split(Ver1, Delimmiter)
    Ver2A = Split(Ver2, Delimmiter)
    EndNr = X02.Application.WorksheetFunction.Max(UBound(Ver1A), UBound(Ver2A))
    for Nr in vbForRange(0, EndNr):
        if UBound(Ver1A) >= Nr:
            v1 = Val(Ver1A(Nr))
        else:
            v1 = 0
        if UBound(Ver2A) >= Nr:
            v2 = Val(Ver2A(Nr))
        else:
            v2 = 0
        if v1 != v2:
            _fn_return_value = v1 > v2
            return _fn_return_value
    return _fn_return_value

def Test_VersionStr_is_Greater():
    #UT-------------------------------------
    #Debug.Print VersionStr_is_Greater("1.0.7", "1.03.1")
    #Debug.Print VersionStr_is_Greater("1.0.7", "1.0.1")
    #Debug.Print VersionStr_is_Greater("1.0.7", "1.0.8")
    #Debug.Print VersionStr_is_Greater("2.0.7", "")
    Debug.Print(VersionStr_is_Greater('1.0.8', '1.0.7b'))

def CenterOnCell(OnCell):
    VisRows = Integer()

    VisCols = Integer()
    # 12.07.20:
    #---------------------------------------
    # http://www.cpearson.com/excel/zoom.htm
    # Switch over to the OnCell's workbook and worksheet.
    OnCell.Parent.Parent.Activate()
    OnCell.Parent.Activate()
    # Get the number of visible rows and columns for the active window.
    _with6 = X02.ActiveWindow.VisibleRange
    VisRows = _with6.Rows.Count
    VisCols = _with6.Columns.Count
    # Now, determine what cell we need to GOTO. The GOTO method will
    # place that cell reference in the upper left corner of the screen,
    # so that reference needs to be VisRows/2 above and VisCols/2 columns
    # to the left of the cell we want to center on. Use the MAX function
    # to ensure we're not trying to GOTO a cell in row <=0 or column <=0.
    _with7 = X02.Application
    _with7.GoTo(Reference=OnCell.Parent.Cells(_with7.WorksheetFunction.Max(1, OnCell.Row +  _
( OnCell.Rows.Count / 2 )  -  ( VisRows / 2 )), _with7.WorksheetFunction.Max(1, OnCell.Column +  _
( OnCell.Columns.Count / 2 )  - _with7.WorksheetFunction.RoundDown(( VisCols / 2 ), 0))), Scroll=True)

def Check_Version():
    _fn_return_value = None
    if not Valid_Excel():
        message = Replace(pattgen.M09_Language.Get_Language_Str('Diese Excel Version wird nicht unterstützt.' + 'Bitte besuchen sie die Webseite #1# für weitergehende Informationen.' + 'Das Programm wird weiter ausgeführt, es kann jedoch zu unerwarteten Fehlfunktionen' + ', Fehlermeldung und Abstürzen kommen.'), '#1#', vbCrLf + vbCrLf + 'https://wiki.mobaledlib.de/anleitungen/programmgenerator' + vbCrLf + vbCrLf)
        X02.MsgBox(message, vbCritical, pattgen.M09_Language.Get_Language_Str('Versionsprüfung'))
    return _fn_return_value

def Valid_Excel():
    _fn_return_value = None
    exVer = Variant()
    #------------------------------------------
    # see details on https://wiki.mobaledlib.de/anleitungen/programmgenerator
    # Excel Version on https://de.wikipedia.org/wiki/Microsoft_Excel
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    exVer = Val(X02.Application.Version)
    _fn_return_value = exVer >= 15
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Public Declare PtrSafe Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
# VB2PY (UntranslatedCode) Public Declare PtrSafe Function GetAsyncKeyState Lib "user32" (ByVal vKey As Long) As Integer
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function SetForegroundWindow Lib "user32" (ByVal hWnd As LongPtr) As LongPtr
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function IsIconic Lib "user32" (ByVal hWnd As LongPtr) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function AccessibleObjectFromWindow Lib "oleacc" (ByVal hWnd As LongPtr, ByVal dwId As Long, riid As Any, ppvObject As Object) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function FindWindowExA Lib "user32" (ByVal hwndParent As LongPtr, ByVal hwndChildAfter As LongPtr, ByVal lpszClass As String, ByVal lpszWindow As String) As LongPtr
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function WideCharToMultiByte Lib "kernel32.dll" ( _\nByVal CodePage As Long, _\nByVal dwFlags As Long, _\nByVal lpWideCharStr As Long, _\nByVal cchWideChar As Long, _\nByVal lpMultiByteStr As Long, _\nByVal cbMultiByte As Long, _\nByVal lpDefaultChar As Long, _\nByVal lpUsedDefaultChar As Long) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function MultiByteToWideChar Lib "kernel32" ( _\nByVal CodePage As Long, _\nByVal dwFlags As Long, _\nByVal lpMultiByteStr As LongPtr, _\nByVal cchMultiByte As Long, _\nByVal lpWideCharStr As LongPtr, _\nByVal cchWideChar As Long _\n) As Long
