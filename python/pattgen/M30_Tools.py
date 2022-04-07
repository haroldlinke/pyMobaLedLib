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

"""# VB2PY (CheckDirective) VB directive took path 1 on VBA7
# VB2PY (CheckDirective) VB directive took path 1 on Win64
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
'' Maps a character string to a UTF-16 (wide character) string             ' 26.05.20:
# VB2PY (CheckDirective) VB directive took path 1 on VBA7

"""

VK_CONTROL = 0x11
__CP_UTF8 = 65001

def __IsFilled(c):
    fn_return_value = None
    #---------------------------------------
    fn_return_value = Trim(c.Value) != ''
    return fn_return_value

def __LastFilledColumn(Rng, LastRow):
    fn_return_value = None
    c = Range()

    MaxColumn = Long()
    #---------------------------------------------------------------
    # Die Funktion läuft durch alle Spalten und alle Reihen im angegebenen Bereich
    # Das ist nicht besonders schnell
    # => Die Funktion sollte nicht mehr genutzt werden.
    #    Ersetzt durch LastFilledColumn2()
    # Find the last used column
    for c in Rng:
        if c.Row > LastRow:
            break
        if __IsFilled(c) and c.Column > MaxColumn:
            MaxColumn = c.Column
    fn_return_value = MaxColumn
    return fn_return_value

def __LastFilledColumn2(FirstRow, LastRow):
    fn_return_value = None
    Row = Long()

    MaxColumn = Long()

    LastF = Long()
    #--------------------------------------------------------------------
    # Faster than LastFilledColumn() because it doesn't loop through al columns
    # Find the last used column
    for Row in vbForRange(FirstRow, LastRow):
        LastF = Cells(Row, Cells(Row, 1).EntireRow.Columns.Count).End(xlToLeft).Column
        if LastF > MaxColumn:
            MaxColumn = LastF
    fn_return_value = MaxColumn
    return fn_return_value

def __LastFilledColumn2(Rng, LastRow):
    fn_return_value = None
    Row = Long()

    MaxColumn = Long()

    LastF = Long()

    FirstRow = Long()
    #--------------------------------------------------------------------
    # Faster than LastFilledColumn() because it doesn't loop through al columns
    FirstRow = Rng.Row
    # Find the last used column
    with_0 = Rng.Worksheet
    for Row in vbForRange(FirstRow, LastRow):
        LastF = with_0.Cells(Row, with_0.Cells(Row, 1).EntireRow.Columns.Count).End(xlToLeft).Column
        if LastF > MaxColumn:
            MaxColumn = LastF
    fn_return_value = MaxColumn
    return fn_return_value

def __LastUsedRowIn(Sheet):
    fn_return_value = None
    Sh = Variant()
    #-----------------------------------------------
    # return the last used row in the given sheet.
    # The sheet could be given as sheet name or as worksheets variable.
    if VarType(Sheet) == vbString:
        Sh = Sheets(Sheet)
    else:
        Sh = Sheet
    fn_return_value = Sh.UsedRange.Rows(Sh.UsedRange.Rows.Count).Row
    Sh = None
    return fn_return_value

def __LastUsedColumnInRow(Sh, Row):
    fn_return_value = None
    #---------------------------------------------------------------
    fn_return_value = Sh.Cells(Row, Sh.Columns.Count).End(xlToLeft).Column
    return fn_return_value

def __LastFilledRowIn(Sh, FirstCheckCol, LastCheckCol):
    fn_return_value = None
    Row = Long()
    #---------------------------------------------------------------------------------------------
    Row = __LastUsedRowIn(Sh)
    with_1 = Sh
    while with_1.Cells(Row, FirstCheckCol).End(xlToRight).Column > LastCheckCol:
        Row = Row - 1
    fn_return_value = Row
    return fn_return_value

def __Test_LastFilledRowIn():
    Start = Variant()
    #UT------------------------------------------
    Start = Timer()
    Debug.Print(__LastFilledRowIn(ActiveSheet, 4, Last_LEDsCol) + 'Duration: ' + Round(Timer() - Start, 2))

def __LastUsedColumn():
    fn_return_value = None
    #--------------------------------
    fn_return_value = ActiveSheet.UsedRange.Columns(ActiveSheet.UsedRange.Columns.Count).Column
    return fn_return_value

def __LastUsedColumnIn(Sheet):
    fn_return_value = None
    Sh = Variant()
    #--------------------------------------------------
    if VarType(Sheet) == vbString:
        Sh = Sheets(Sheet)
    else:
        Sh = Sheet
    fn_return_value = Sh.UsedRange.Columns(Sh.UsedRange.Columns.Count).Column
    Sh = None
    return fn_return_value

def __Row_Filled_w_Attrib(Rng, LastAttrCheckCol):
    fn_return_value = None
    c = Range()
    #----------------------------------------------------------------------------------------
    # Check if the row in the given Range is used
    # - The whole range is checked for characters
    # - Only the first columns until LastAttrCheckCol are checked for fill color
    if Rng.End(xlToRight).Column <= Rng.Column + Rng.Columns.Count:
        fn_return_value = True
        return fn_return_value
    for c in Rng:
        if c.Column > LastAttrCheckCol:
            return fn_return_value
        if c.Interior.Color != 16777215:
            fn_return_value = True
            return fn_return_value
    return fn_return_value

def __LastFilledRowIn_w_Attrib(Sh, FirstCheckCol, LastCheckCol, LastAttrCheckCol):
    fn_return_value = None
    Row = Long()

    Last_u_Col = Long()
    #--------------------------------------------------------------------------------------------------------------------------------
    Row = __LastUsedRowIn(Sh)
    with_2 = Sh
    while __Row_Filled_w_Attrib(with_2.Range(with_2.Cells(Row, FirstCheckCol), with_2.Cells(Row, LastCheckCol)), LastAttrCheckCol) == 0 and Row > 0:
        Row = Row - 1
    fn_return_value = Row
    return fn_return_value

def __Test_LastFilledRowIn_w_Attrib():
    Start = Variant()
    #UT----------------------------------------
    Start = Timer()
    Debug.Print(__LastFilledRowIn_w_Attrib(ActiveSheet, 4, Last_LEDsCol, Last_LEDs_ChkAttrCol) + 'Duration: ' + Round(Timer() - Start, 2))

def __SheetEx(Name):
    fn_return_value = None
    s = Variant()
    #-------------------------------
    for s in Sheets:
        if s.Name == Name:
            fn_return_value = True
            return fn_return_value
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
def __Replace_Illegal_Char(s):
    fn_return_value = None
    OldChars = 'ä,  ö,  ü,  Ä,  Ö,  Ü,  ß'

    NewChars = 'ae, oe, ue, Ae, Oe, Ue, ss'

    OldList = vbObjectInitialize(objtype=String)

    NewList = vbObjectInitialize(objtype=String)

    i = Long()

    Res = String()
    #---------------------------------------------------------
    OldList = Split(OldChars, ',')
    NewList = Split(NewChars, ',')
    Res = s
    for i in vbForRange(0, UBound(OldList) - 1):
        Res = Replace(Res, Trim(OldList(i)), Trim(NewList(i)))
    Res = Replace(Res, ' ', '_')
    for i in vbForRange(1, Len(Res)):
        c = Mid(Res, i, 1)
        if c >= '0' and c <= '9' or c >= 'A' and c <= 'Z' or c >= 'a' and c <= 'z' or c == '_':
            fn_return_value = __Replace_Illegal_Char() + c
    return fn_return_value

def __Test_Replace_Illegal_Char():
    #UT------------------------------------
    Debug.Print(__Replace_Illegal_Char('Hallo Was Geht äö(2346$ Test'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def __FileNameExt(Name):
    fn_return_value = None
    Pos = Long()

    Pos2 = Long()

    Temp = String()
    #---------------------------------------------------
    # Return name and extention without path
    Pos = InStrRev(Name, '\\')
    Pos2 = InStrRev(Name, '/')
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
    fn_return_value = Temp
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def __FilePath(Name):
    fn_return_value = None
    #------------------------------------------------
    fn_return_value = Left(Name, Len(Name) - Len(__FileNameExt(Name)))
    return fn_return_value

def __NoExt(Name):
    fn_return_value = None
    Pos = Long()
    #----------------------------------------
    # Cut of the extention of a filename
    Pos = InStrRev(Name, '.')
    if Pos > 0:
        fn_return_value = Left(Name, Pos - 1)
    else:
        fn_return_value = Name
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def __FileExt(Name):
    fn_return_value = None
    Pos = Long()
    #-----------------------------------------------
    # Return the file extention including the point
    Pos = InStrRev(Name, '.')
    if Pos > 0:
        fn_return_value = Mid(Name, Pos)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def __FileName(Name):
    fn_return_value = None
    #------------------------------------------------
    # Return name without extention and path
    fn_return_value = __NoExt(__FileNameExt(Name))
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: FullName - ByVal 
def __Same_Name_already_open(FullName):
    fn_return_value = None
    w = Variant()

    Name = String()
    #-------------------------------------------------------------------
    # Check if a workbook with the same name is already opened
    Name = __FileNameExt(FullName)
    for w in Workbooks:
        if UCase(w.Name) == UCase(Name):
            fn_return_value = True
            return fn_return_value
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SheetName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Add_to_Duplicate_Name='_Copy_' - ByVal 
def __Unic_SheetName(SheetName, Add_to_Duplicate_Name='_Copy_'):
    fn_return_value = None
    OrgName = String()

    Cnt = Long()
    #----------------------------------------------------------------------------------------------------------------------
    OrgName = SheetName
    while __SheetEx(SheetName):
        Cnt = Cnt + 1
        while 1:
            SheetName = OrgName + Add_to_Duplicate_Name + Cnt
            if Len(SheetName) > 31:
                CutOff = Len(SheetName) - 31
                if CutOff <= Len(Add_to_Duplicate_Name):
                    Add_to_Duplicate_Name = __DelLast(Add_to_Duplicate_Name, CutOff)
                else:
                    Add_to_Duplicate_Name = ''
                    OrgName = __DelLast(OrgName)
            if not (Len(SheetName) > 31):
                break
    fn_return_value = SheetName
    return fn_return_value

def __Test_Unic_SheetName():
    #UT------------------------------
    Debug.Print('Unic_SheetName:' + __Unic_SheetName('KS_Hauptsignal_Zs3_Zs 6_Zs1_RGB'))

def __Protect_Active_Sheet():
    #-------------------------
    ActiveSheet.Protect(DrawingObjects=True, Contents=True, Scenarios=True, AllowFormattingCells=True, AllowInsertingHyperlinks=True)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def __Protect_Sheet(Sh):
    #---------------------------------------
    Sh.Protect(DrawingObjects=True, Contents=True, Scenarios=True, AllowFormattingCells=True, AllowInsertingHyperlinks=True)

def __GetPathOnly(sPath):
    fn_return_value = None
    #------------------------------------------------------
    fn_return_value = Left(sPath, InStrRev(sPath, '/', Len(sPath)) - 1)
    return fn_return_value

def CreateFolder(sFolder):
    fn_return_value = None
    s = String()
    #--------------------------------------------------------
    # http://www.freevbcode.com/ShowCode.asp?ID=257
    # VB2PY (UntranslatedCode) On Error GoTo ErrorHandler
    s = __GetPathOnly(sFolder)
    if Dir(s, vbDirectory) == '':
        s = CreateFolder(s)
        MkDir(s)
    fn_return_value = sFolder
    return fn_return_value
    return fn_return_value
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
def __NrStr2d(s):
    fn_return_value = None
    #--------------------------------------------
    if Application.International(xlDecimalSeparator) == ',':
        fn_return_value = Val(Replace(s, '.', ','))
    else:
        fn_return_value = Val(Replace(s, ',', '.'))
    return fn_return_value

def __CorrectKomma(s):
    fn_return_value = None
    #-------------------------------------------
    if Application.International(xlDecimalSeparator) == ',':
        fn_return_value = Replace(s, '.', ',')
    else:
        fn_return_value = Replace(s, ',', '.')
    return fn_return_value

def __t():
    Res = Variant()
    Res = Application.International(xlDecimalSeparator)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cnt=1 - ByVal 
def __DelLast(s, Cnt=1):
    fn_return_value = None
    #----------------------------------------------------------------------------
    if Len(s) > 0:
        fn_return_value = Left(s, Len(s) - Cnt)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
def __DelAllLast(s, Chars):
    fn_return_value = None
    #----------------------------------------------------------------
    while InStr(Chars, Right(s, 1)) > 0:
        s = Left(s, Len(s) - 1)
    fn_return_value = s
    return fn_return_value

def __Center_Form(f):
    #---------------------------
    # Manchmal funktioniert das nicht beim starten des Programms weil das Excel Programm                  13.06.20:
    # Noch nicht richtig geöffnet ist und darum noch kein eigenes Fenster hat. Dann werden
    # die Positionen eines zufor geöffenetn Exce Programms benutzt und der Dialog wird zentriert
    # zu diesem Dialog gezeigt. Als Abhilfe habe ich mal "ThisWorkbook." eingefügt...
    # Aufgefallen ist es beim "Examples_UserForm".
    DoEvents()
    with_3 = f
    with_3.StartupPosition = 0
    with_3.Left = ThisWorkbook.Application.Left +  ( ThisWorkbook.Application.Width - with_3.Width )  / 2
    with_3.Top = ThisWorkbook.Application.Top +  ( ThisWorkbook.Application.Height - with_3.Height )  / 2

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByVal 
def __Replace_Double_Space(Txt):
    fn_return_value = None
    Res = String()
    #-----------------------------------------------------------
    Res = Txt
    while InStr(Res, '  ') > 0:
        Res = Replace(Res, '  ', ' ')
    fn_return_value = Res
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByVal 
def Is_Contained_in_Array(Txt, Arr):
    fn_return_value = None
    e = Variant()
    #-------------------------------------------------------------------------------------
    #If StrPtr(Arr) = 0 Then Exit Function                                     ' 06.05.20: Jürgen
    if not isInitialised(Arr):
        return fn_return_value
        # 06.05.20:
    Txt = Trim(Txt)
    for e in Arr:
        if Trim(e) == Txt:
            fn_return_value = True
            return fn_return_value
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: stringToBeFound - ByVal 
def __IsInArray(stringToBeFound, Arr):
    fn_return_value = None
    i = Long()
    #--------------------------------------------------------------------------
    # default return value if value not found in array
    fn_return_value = - 1
    for i in vbForRange(LBound(Arr), UBound(Arr)):
        if StrComp(stringToBeFound, Arr(i), vbTextCompare) == 0:
            fn_return_value = i
            break
    return fn_return_value

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
    StartHide_y = dlg.Controls(StartHide_Name).Top
    StartMove_y = dlg.Controls(StartMove_Name).Top
    MoveDelta = StartMove_y - StartHide_y
    #Debug.Print "Hide_and_Move_up from '" & StartHide_Name & "' to '" & StartMove_Name & "' " & MoveDelta ' Debug
    for c in dlg.Controls:
        if c.Top >= StartMove_y-1:   # 15.03.22: Buttons are placed 1 pixel above input field/label
            c.Top = c.Top - MoveDelta
        elif c.Top >= StartHide_y-1: # 15.03.22: Buttons are placed 1 pixel above input field/label
            c.Visible = False
    dlg.Height = dlg.Height - MoveDelta

def EndProg():
    #-------------------
    # Is called in case of an fatal error
    # Normaly this function should not be called because the
    # global variables and dialog positions are cleared.
    Enable_Application_Automatics()
    sys.exit(0)

def Enable_Application_Automatics():
    #-----------------------------------------
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    ActiveSheet.EnableCalculation = True
    Application.Calculation = xlCalculationAutomatic

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def ValidNameCharacters(Name):
    fn_return_value = None
    Pos = Integer()

    Res = String()

    c = String()
    #------------------------------------------------------------------
    for Pos in vbForRange(1, Len(Name)):
        c = Mid(Name, Pos, 1)
        if ( c >= 'A' and c <= 'Z' )  or  ( c >= 'a' and c <= 'z' )  or  _
( c >= '0' and c <= '9' ) :
            Res = Res + c
        else:
            if (c == 'ä'):
                Res = Res + 'ae'
            elif (c == 'Ä'):
                Res = Res + 'Ae'
            elif (c == 'ö'):
                Res = Res + 'oe'
            elif (c == 'Ö'):
                Res = Res + 'Oe'
            elif (c == 'ü'):
                Res = Res + 'ue'
            elif (c == 'Ü'):
                Res = Res + 'Ue'
            elif (c == 'ß'):
                Res = Res + 'ss'
            else:
                if Right(Res, 1) != '_':
                    Res = Res + '_'
    fn_return_value = Res
    return fn_return_value

def F_shellExec(sCmd):
    fn_return_value = None
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
    fn_return_value = oShell.Exec(sCmd).StdOut.ReadAll
    return fn_return_value

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

def __Test_Shell():
    #UT---------------------
    MsgBox(F_shellExec('cmd /c Dir C:\\'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Nr - ByVal 
def __Hex02(Nr):
    fn_return_value = None
    #--------------------------------------------
    fn_return_value = Right('0' + Hex(Nr), 2)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Value - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
def SHR(Value, Shift):
    fn_return_value = None
    i = Byte()
    #--------------------------------------------------------------------
    fn_return_value = Value
    if Shift > 0:
        fn_return_value = Int(SHR() /  ( 2 ** Shift ))
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Value - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
def SHL(Value, Shift):
    fn_return_value = None
    #--------------------------------------------------------------------
    fn_return_value = Value
    if Shift > 0:
        for i in vbForRange(1, Shift):
            m = SHL() and 0x40000000
            fn_return_value = ( SHL() and 0x3FFFFFFF )  * 2
            if m != 0:
                fn_return_value = SHL() or 0x80000000
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParamStr - ByRef 
def Replace_Const(ParamStr, ReplaceList, MainDelimmiter, SubDelimmiter):
    ReplacePair = Variant()
    #---------------------------------------------------------------------------------------------------------------------------
    for ReplacePair in Split(ReplaceList, MainDelimmiter):
        if Trim(ReplacePair) != '':
            Parts = Split(ReplacePair, SubDelimmiter)
            ParamStr = Replace(ParamStr, Trim(Parts(0)), Trim(Parts(1)))

def __Test_Dec_Sep():
    str = String()
    #-------------------------
    # Die Val() Funktion liefert auch wenn als Dezimaltrennzeichen ein "," eingestellt ist
    # den richtigen Wert
    # => Es ist O.K. wenn man bei den Zeiten immer den "." als trennzeichen verwendt.
    str = '1.3'
    Debug.Print(Val(str) * 2)

def __One_Time_Str_to_Seconds(vSeconds):
    fn_return_value = None
    Parts = vbObjectInitialize(objtype=String)
    #----------------------------------------------------------------------
    # Possible imputs:
    #   1.3 Sec, 1.3 sec, 1.3 Sek, 1.3 sek
    #   1.4 Min
    #   1500, 1500 ms 1500 Ms
    Parts = Split(Trim(vSeconds), ' ')
    if Application.International(xlDecimalSeparator) == ',':
        Parts[0] = Replace(Parts(0), '.', ',')
    if UBound(Parts) > 0:
        if UCase(Left(Parts(1), 1)) == 'S':
            fn_return_value = Val(Parts(0))
        elif Parts(1) == 'Min':
            fn_return_value = Val(Parts(0)) * 60
        else:
            fn_return_value = Val(vSeconds) / 1000
    else:
        fn_return_value = Val(vSeconds) / 1000
    return fn_return_value

def __Time_Str_to_Seconds(vSeconds):
    fn_return_value = None
    Parts = vbObjectInitialize(objtype=String)

    Part = Variant()
    #------------------------------------------------------------------
    # 1.5 Sec + 2 Min
    Parts = Split(vSeconds, '+')
    for Part in Parts:
        fn_return_value = __Time_Str_to_Seconds() + __One_Time_Str_to_Seconds(Part)
    return fn_return_value

def __Test_Time_Str_to_Seconds():
    #UT-----------------------------------
    Debug.Print(__Time_Str_to_Seconds('1512 Ms') + 's')
    #Debug.Print Time_Str_to_Seconds("1.5 Min") & "s"
    #Debug.Print Time_Str_to_Seconds("15 ") & "s"
    #Debug.Print Time_Str_to_Seconds("1.5 Sec + 2 Min") & "s"

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Parm - ByVal 
def Convert_TimeStr_to_ms(Parm):
    fn_return_value = None
    ReplaceList = 'Ms > ms; sec > Sec; sek > Sec; Sek > Sec; , > .; - > + -'

    DivideBy16 = Boolean()

    Part = Variant()

    NrStr = String()

    Res = Long()
    #------------------------------------------------------------------
    # Converte a string like "3.5 Min + 2.4 Sec + 200 ms"
    # to a two byte string
    # Return -99999 in case of an error
    Replace_Const(Parm, ReplaceList, ';', '>')
    if InStr(Parm, '/16') > 0:
        DivideBy16 = True
        Parm = Replace(Parm, '/16', '')
    for Part in Split(Parm, '+'):
        Part = Trim(Part)
        if Part != '':
            if Right(Part, Len(' Sec')) == ' Sec':
                NrStr = Trim(Replace(Part, 'Sec', ''))
                if IsNumeric(NrStr):
                    Res = Res + Int(Val(NrStr) * 1000 + 0.00001)
                else:
                    fn_return_value = - 99999
                    return fn_return_value
            elif Right(Part, Len(' Min')) == ' Min':
                NrStr = Trim(Replace(Part, 'Min', ''))
                if IsNumeric(NrStr):
                    Res = Res + Int(Val(NrStr) * 60 * 1000 + 0.00001)
                else:
                    fn_return_value = - 99999
                    return fn_return_value
            elif Right(Part, Len(' ms')) == ' ms':
                NrStr = Trim(Replace(Part, 'ms', ''))
                if IsNumeric(NrStr):
                    Res = Res + Int(Val(NrStr))
                else:
                    fn_return_value = - 99999
                    return fn_return_value
            else:
                NrStr = Trim(Part)
                if IsNumeric(NrStr):
                    Res = Res + Int(Val(NrStr))
                else:
                    fn_return_value = - 99999
                    return fn_return_value
    if DivideBy16:
        Res = Res / 16
    fn_return_value = Res
    return fn_return_value

def __Test_Convert_TimeStr_to_ms():
    #UT-------------------------------------
    Debug.Print(Convert_TimeStr_to_ms('3.5 Min + 2.4 Sek + 200 ms') + ' should be 212600')
    #Debug.Print Convert_TimeStr_to_ms("3.5 Min - 2.4 Sek + 200 ms") & " should be 207800"
    #Debug.Print Convert_TimeStr_to_ms("- 2.4 Sek + 3.5 Min  + 200 ms") & " should be 207800"
    #Debug.Print Convert_TimeStr_to_ms("2,5 Sekunden") & " should be -99999"
    #Debug.Print Convert_TimeStr_to_ms("2673 Sek") & " should be 2673000"

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Val - ByVal 
def Long_to_2ByteStr(Val):
    fn_return_value = None
    LowByte = Byte()

    HighByte = Byte()
    #------------------------------------------------------------
    # Generates: "13, 16"
    LowByte = Val and 0xFF
    HighByte = Int(Val / 256)
    fn_return_value = LowByte + ', ' + HighByte
    return fn_return_value

def ClearStatusbar():
    #--------------------------
    # Is called by onTime to clear the status bar after a while
    Application.StatusBar = ''

def Show_Status_for_a_while(Txt, Duration='00:00:15'):
    #-------------------------------------------------------------------------------------------
    P01.Application.StatusBar = Txt
    if Txt != '':
        P01.Application.OnTime(Duration, 'ClearStatusbar')
    else:
        pass # Application.OnTime(0, 'ClearStatusbar')

def __InputBoxMov(prompt, Title=VBMissingArgument, Default=VBMissingArgument, Left=VBMissingArgument, Top=VBMissingArgument, helpfile=VBMissingArgument, HelpContextID=VBMissingArgument):
    fn_return_value = None
    OldUpdate = Boolean()
    #--------------------------------------------------------------------------------------------------------
    # InputBox which could be moved with correct screen update even if screenupdating is disabled
    OldUpdate = Application.ScreenUpdating
    Application.ScreenUpdating = True
    fn_return_value = InputBox(prompt, Title, Default, Left, Top, helpfile, HelpContextID)
    Sleep(50)
    Application.ScreenUpdating = OldUpdate
    return fn_return_value

def __Test_InputBoxMov():
    #UT---------------------------
    Application.ScreenUpdating = False
    Debug.Print(__InputBoxMov('Hallo', 'Title', 'Dafault'))
    Application.ScreenUpdating = True

def __MsgBoxMov(prompt, Buttons=VBMissingArgument, Title=VBMissingArgument, helpfile=VBMissingArgument, context=VBMissingArgument):
    fn_return_value = None
    OldUpdate = Boolean()
    #----------------------------------------------------------------------------------------
    # MsgBox which could be moved with correct screen update even if screenupdating is disabled
    OldUpdate = Application.ScreenUpdating
    Application.ScreenUpdating = True
    fn_return_value = MsgBox(prompt, Buttons, Title, helpfile, context)
    Sleep(50)
    Application.ScreenUpdating = OldUpdate
    return fn_return_value

def __Test_MsgBoxMov():
    #UT-------------------------
    Application.ScreenUpdating = False
    Debug.Print(__MsgBoxMov('Hallo', vbYesNoCancel, 'Titel'))
    Application.ScreenUpdating = True

def myInStr(s, search):
    fn_return_value = None
    #--------------------------------
    fn_return_value = InStr(s, search)
    return fn_return_value

def Read_File_to_String(FileName):
    fn_return_value = None
    strFileContent = String()

    fp = Integer()
    #----------------------------------------------------------------
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo ReadError
    VBFiles.openFile(fp, FileName(), 'r') 
    fn_return_value = Input(LOF(fp), fp)
    VBFiles.closeFile(fp)
    return fn_return_value
    MsgBox(Get_Language_Str('Fehler beim lesen der Datei:') + vbCr + '  \'' + FileName() + '\'', vbCritical, Get_Language_Str('Fehler beim Datei lesen'))
    fn_return_value = '#ERROR#'
    return fn_return_value

def Get_Ini_Entry(FileStr, EntryName):
    fn_return_value = None
    p = Long()

    e = String()
    #------------------------------------------------------------------------------
    fn_return_value = '#ERROR#'
    p = InStr(FileStr, EntryName)
    if p == 0:
        return fn_return_value
    p = p + Len(EntryName)
    e = InStr(p, FileStr, vbCr)
    if e == 0:
        e = InStr(p, FileStr, vbLf)
    if e == 0:
        return fn_return_value
    fn_return_value = Mid(FileStr, p, e - p)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Source - ByRef 
def ConvertToUTF8(Source):
    fn_return_value = None
    Length = Long()

    Pointer = LongPtr()

    Size = Long()

    Buffer = vbObjectInitialize(objtype=Byte)
    #---------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    Length = Len(Source)
    Pointer = StrPtr(Source)
    Size = WideCharToMultiByte(__CP_UTF8, 0, Pointer, Length, 0, 0, 0, 0)
    Buffer = vbObjectInitialize(((0, Size - 1),), Variant)
    WideCharToMultiByte(__CP_UTF8, 0, Pointer, Length, VarPtr(Buffer(0)), Size, 0, 0)
    fn_return_value = Buffer
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Source - ByRef 
def ConvertToUTF8Str(Source):
    fn_return_value = None
    Bytes = vbObjectInitialize(objtype=Byte)

    Res = String()

    i = Variant()
    #-----------------------------------------------------------------
    Bytes = ConvertToUTF8(Source)
    for i in vbForRange(0, UBound(Bytes)):
        Res = Res + Chr(Bytes(i))
    fn_return_value = Res
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Source - ByRef 
def ConvertFromUTF8(Source):
    fn_return_value = None
    Size = Long()

    Pointer = LongPtr()

    Length = Long()

    Buffer = String()
    #----------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    Size = UBound(Source) - LBound(Source) + 1
    Pointer = VarPtr(Source(LBound(Source)))
    Length = MultiByteToWideChar(__CP_UTF8, 0, Pointer, Size, 0, 0)
    Buffer = Space(Length)
    MultiByteToWideChar(__CP_UTF8, 0, Pointer, Size, StrPtr(Buffer), Length)
    fn_return_value = Buffer
    return fn_return_value

def ConvertUTF8Str(UTF8Str):
    fn_return_value = None
    bStr = vbObjectInitialize(objtype=Byte)

    i = Long()
    #----------------------------------------------------------
    bStr = vbObjectInitialize((Len(UTF8Str) - 1,), Variant)
    for i in vbForRange(1, Len(UTF8Str)):
        bStr[i - 1] = Asc(Mid(UTF8Str, i, 1))
    fn_return_value = ConvertFromUTF8(bStr)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: vArrayName - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lUpper=- 1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lLower=- 1 - ByVal 
def Array_BubbleSort(vArrayName, lUpper=- 1, lLower=- 1):
    vtemp = Variant()

    i = Long()

    j = Long()
    #---------------------------------------------------------
    # https://bettersolutions.com/vba/arrays/sorting-bubble-sort.htm
    if IsEmpty(vArrayName) == True:
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
            MsgBox('Internal Error: Button text is wrong \'' + Text + '\'.' + vbCr + 'It must contain an Accelerator followed by the text.' + vbCr + 'Example: \'H Hallo\'', vbCritical, 'Internal Error (Wrong translation?)')
            EndProg()
        Button.Caption = Mid(Text, 3, 255)
        Button.Accelerator = Left(Text, 1)

def Bring_to_front():
    #--------------------------
    # Is not working if an other application has be moved above Excel wit Alt+Tab
    # But this is a feature od Windows.
    # See: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow
    # But it brings up excel again after the upload to the Arduino
    # Without this funchion an other program was activated after the upload for some reasons
    ThisWorkbook.Activate()
    SetForegroundWindow(Application.hWnd)

def Is_Minimized(Name):
    fn_return_value = None
    guid = vbObjectInitialize(((0, 3),), Variant)

    acc = Object()

    hWnd = Variant()

    hwnd2 = Variant()

    hwnd3 = Variant()
    #---------------------------------------------------
    # Adapted from
    # https://stackoverflow.com/questions/5292626/couldnt-find-child-window-using-findwindowexa
    fn_return_value = - 1
    guid[0] = 0x20400
    guid[1] = 0x0
    guid[2] = 0xC0
    guid[3] = 0x46000000
    while 1:
        hWnd = FindWindowExA(0, hWnd, vbNullString, vbNullString)
        if hWnd == 0:
            break
        hwnd2 = FindWindowExA(hWnd, 0, 'XLDESK', vbNullString)
        hwnd3 = FindWindowExA(hwnd2, 0, 'EXCEL7', vbNullString)
        if AccessibleObjectFromWindow(hwnd3, 0xFFFFFFF0, guid(0), acc) == 0:
            Debug.Print(hWnd + '  ' + acc.Caption + '  ' + IsIconic(hWnd))
            if acc.Caption == Name:
                fn_return_value = IsIconic(hWnd)
                return fn_return_value
    return fn_return_value

def __Test_Is_Minimized():
    #UT----------------------------
    #Debug.Print "Is_Minimized:" & Is_Minimized("Prog_Generator_MobaLedLib.xlsm")
    Debug.Print(ThisWorkbook.Name + ' Is_Minimized:' + Is_Minimized(ThisWorkbook.Name))

def VersionStr_is_Greater(Ver1, Ver2, Delimmiter='.'):
    fn_return_value = None
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
    EndNr = WorksheetFunction.Max(UBound(Ver1A), UBound(Ver2A))
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
            fn_return_value = v1 > v2
            return fn_return_value
    return fn_return_value

def __Test_VersionStr_is_Greater():
    #UT-------------------------------------
    #Debug.Print VersionStr_is_Greater("1.0.7", "1.03.1")
    #Debug.Print VersionStr_is_Greater("1.0.7", "1.0.1")
    #Debug.Print VersionStr_is_Greater("1.0.7", "1.0.8")
    #Debug.Print VersionStr_is_Greater("2.0.7", "")
    Debug.Print(VersionStr_is_Greater('1.0.8', '1.0.7b'))

def CenterOnCell(OnCell):
    VisRows = Integer()

    VisCols = Integer()
    #---------------------------------------
    # http://www.cpearson.com/excel/zoom.htm
    # Switch over to the OnCell's workbook and worksheet.
    OnCell.Parent.Parent.Activate()
    OnCell.Parent.Activate()
    # Get the number of visible rows and columns for the active window.
    with_4 = ActiveWindow.VisibleRange
    VisRows = with_4.Rows.Count
    VisCols = with_4.Columns.Count
    # Now, determine what cell we need to GOTO. The GOTO method will
    # place that cell reference in the upper left corner of the screen,
    # so that reference needs to be VisRows/2 above and VisCols/2 columns
    # to the left of the cell we want to center on. Use the MAX function
    # to ensure we're not trying to GOTO a cell in row <=0 or column <=0.
    with_5 = Application
    with_5.GoTo(Reference=OnCell.Parent.Cells(with_5.WorksheetFunction.Max(1, OnCell.Row +  _
( OnCell.Rows.Count / 2 )  -  ( VisRows / 2 )), with_5.WorksheetFunction.Max(1, OnCell.Column +  _
( OnCell.Columns.Count / 2 )  - with_5.WorksheetFunction.RoundDown(( VisCols / 2 ), 0))), Scroll=True)

def Check_Version():
    fn_return_value = None
    if not Valid_Excel():
        message = Replace(Get_Language_Str('Diese Excel Version wird nicht unterstützt.' + 'Bitte besuchen sie die Webseite #1# für weitergehende Informationen.' + 'Das Programm wird weiter ausgeführt, es kann jedoch zu unerwarteten Fehlfunktionen' + ', Fehlermeldung und Abstürzen kommen.'), '#1#', vbCrLf + vbCrLf + 'https://wiki.mobaledlib.de/anleitungen/programmgenerator' + vbCrLf + vbCrLf)
        MsgBox(message, vbCritical, Get_Language_Str('Versionsprüfung'))
    return fn_return_value

def Valid_Excel():
    fn_return_value = None
    exVer = Variant()
    #------------------------------------------
    # see details on https://wiki.mobaledlib.de/anleitungen/programmgenerator
    # Excel Version on https://de.wikipedia.org/wiki/Microsoft_Excel
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    exVer = Val(Application.Version)
    fn_return_value = exVer >= 15
    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Public Declare PtrSafe Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
# VB2PY (UntranslatedCode) Public Declare PtrSafe Function GetAsyncKeyState Lib "user32" (ByVal vKey As Long) As Integer
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function SetForegroundWindow Lib "user32" (ByVal hWnd As LongPtr) As LongPtr
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function IsIconic Lib "user32" (ByVal hWnd As LongPtr) As Long   
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function AccessibleObjectFromWindow Lib "oleacc" (ByVal hWnd As LongPtr, ByVal dwId As Long, riid As Any, ppvObject As Object) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function FindWindowExA Lib "user32" (ByVal hwndParent As LongPtr, ByVal hwndChildAfter As LongPtr, ByVal lpszClass As String, ByVal lpszWindow As String) As LongPtr
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function WideCharToMultiByte Lib "kernel32.dll" ( _\nByVal CodePage As Long, _\nByVal dwFlags As Long, _\nByVal lpWideCharStr As Long, _\nByVal cchWideChar As Long, _\nByVal lpMultiByteStr As Long, _\nByVal cbMultiByte As Long, _\nByVal lpDefaultChar As Long, _\nByVal lpUsedDefaultChar As Long) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function MultiByteToWideChar Lib "kernel32" ( _\nByVal CodePage As Long, _\nByVal dwFlags As Long, _\nByVal lpMultiByteStr As LongPtr, _\nByVal cchMultiByte As Long, _\nByVal lpWideCharStr As LongPtr, _\nByVal cchWideChar As Long _\n) As Long
