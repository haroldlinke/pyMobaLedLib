# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
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

import subprocess
import zipfile
import platform
import shutil
import pathlib

from ExcelAPI.XLC_Excel_Consts import *
# fromx proggen.M02_Public import Get_BoardTyp

import ExcelAPI.XLW_Workbook as P01

import proggen.M02_Public as M02
import proggen.M02a_Public as M02a
#import proggen.M02_global_variables as M02GV
#import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
#import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
import proggen.M12_Copy_Prog as M12
#import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
#import proggen.M27_Sheet_Icons as M27
#import proggen.M28_divers as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80

import mlpyproggen.Prog_Generator as PG

PlatformKey_ROW = 3
PlatformKey_COL = 3
PlatformParName_COL = 1
PlatformParams = {} #Scripting.Dictionary()
StartTime_for_ms_Timer = int()
#StartTime_for_ms_Timer = int()


class POINTAPI:
    def __init__(self):
        self.X = int()
        self.Y = int()

CP_UTF8 = 65001
SM_CXSCREEN = 0
SM_CYSCREEN = 1
SM_CMONITORS = 80
SW_NORMAL = 1
class WinPos_T:
    def __init__(self):
        self.Valid = Boolean()
        self.Left = Double()
        self.Top = Double()


def Start_ms_Timer():
    #--------------------------
    global StartTime_for_ms_Timer
    # Timer for debugging
    ## VB2PY (CheckDirective) VB directive took path 1 on Win64
    StartTime_for_ms_Timer = int(time() * 1000)

def Get_ms_Duration():
    #----------------------------------------
    # Timer for debugging
    fn_return_value = int(time() * 1000) - StartTime_for_ms_Timer
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
def AddSpaceToLen(s, MinLength):
    #----------------------------------------------------------------------------
    if type(s) != str:
        s = str(s)
    
    while Len(s) < MinLength:
        s = s + r' '
    fn_return_value = s
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
def AddSpaceToLenLeft(s, MinLength):
    #--------------------------------------------------------------------------------
    s=str(s)
    while Len(s) < MinLength:
        s = r' ' + s
    fn_return_value = s
    return fn_return_value

def IsArrayEmpty(anArray):
    fn_return_value = False
    #---------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo IS_EMPTY
    if ( UBound(anArray) >= 0 ) :
        return fn_return_value
    fn_return_value = True
    return fn_return_value

def LastUsedRow(sheet=None):
    #-----------------------------
    # Return the last used row in the active sheet.
    # Attention: Rows containing only format informations are also 'used' rows.
    #fn_return_value = P01.ActiveSheet.UsedRange.Rows(P01.ActiveSheet.UsedRange.Rows.Count).Row
    if sheet==None:
        fn_return_value = P01.ActiveSheet.LastUsedRow
    else:
        fn_return_value = P01.Sheets(sheet).LastUsedRow
    return fn_return_value

def LastUsedColumn():
    #--------------------------------
    fn_return_value = P01.ActiveSheet.LastUsedColumn #*HL P01.ActiveSheet.UsedRange.Columns(P01.ActiveSheet.UsedRange.Columns.Count).Column
    return fn_return_value

def LastColumnDatSheet():
    #------------------------------------
    # Last column containing data in the data sheets
    fn_return_value = M25.LED_Nr__Col + M02.INTERNAL_COL_CNT - 1
    return fn_return_value

def LastUsedRowIn(Sheet):
    #Sh:P01.CWorksheet = Variant()
    #-----------------------------------------------
    # return the last used row in the given sheet.
    # The sheet could be given as sheet name or as worksheets variable.
    if P01.VarType(Sheet) == vbString:
        Sh = PG.ThisWorkbook.Sheets(Sheet)
    else:
        Sh = Sheet
    #*HL fn_return_value = Sh.UsedRange.Rows(Sh.UsedRange.Rows.Count).Row
    fn_return_value = Sh.get_LastUsedRow() #len(Sh.UsedRange_Rows())-1
    Sh = None
    return fn_return_value

def LastUsedColumnInRow(Sh, Row):
    #---------------------------------------------------------------
    fn_return_value = Sh.Cells(Row, Sh.Columns.Count).Column #*HL .End(xlToLeft).Column
    return fn_return_value

def LastUsedColumnIn(Sheet):
    #Sh:P01.CWorksheet = Variant()
    #--------------------------------------------------
    if P01.VarType(Sheet) == vbString:
        Sh = PG.ThisWorkbook.Sheets(Sheet)
    else:
        Sh = Sheet
    fn_return_value = Sh.LastUsedColumn #*HLSh.UsedRange.Columns(Sh.Columns.Count).Column
    Sh = None
    return fn_return_value

def LastFilledRowIn(Sh, CheckCol):
    #Row = int()
    #------------------------------------------------------------------
    Row = LastUsedRowIn(Sh)
    with_variable0 = Sh
    while with_variable0.Cells(Row, CheckCol) == r'' and Row > 0:
        Row = Row - 1
    fn_return_value = Row
    return fn_return_value

def LastFilledRow(CheckCol):
    #-----------------------------------------------
    fn_return_value = LastFilledRowIn(P01.ActiveSheet, CheckCol)
    return fn_return_value

def LastFilledColumnIn(Sh, CheckRow):
    Column = int()
    #---------------------------------------------------------------------
    Column = LastUsedColumnIn(Sh)
    with_variable1 = Sh
    while with_variable1.Cells(CheckRow, Column) == r'':
        Column = Column - 1
        if Column == 0:
            return fn_return_value
    fn_return_value = Column
    return fn_return_value

def LastFilledColumn(CheckRow):
    #--------------------------------------------------
    fn_return_value = LastFilledColumnIn(P01.ActiveSheet, CheckRow)
    return fn_return_value

def First_Change_in_Line(Target):
    #--------------------------------------------------------------
    # Check if the target cell is the only cell which contains data
    #First_Change_in_Line = Target.End(xlToLeft).Column = 1 And Target.End(xlToRight).Column = Target.Parent.Columns.Count ' 10.09.19: Removed: (Target = "") And  ' 28.10.19: Replaced P01.ActiveSheet with Target.Parent
    
    #*HL 
    #*HL
    #fn_return_value = Target.End(xlToLeft).Column == 1 and Target.End(xlToRight).Column == LED_Nr__Col
    fn_return_value = Target.check_if_empty_row()
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def LastFilledRowIn_ChkAll(Sh):
    Row = int()
    #-------------------------------------------------------------
    Row = LastUsedRowIn(Sh)+1
    with_variable2 = Sh
    while First_Change_in_Line(with_variable2.Cells(Row, 1)):
        Row = Row - 1
        if Row == 0:
            return 0
    fn_return_value = Row
    return fn_return_value

def Test_LastFilledRowIn_ChkAll():
    #UT--------------------------------------
    Debug.Print(LastFilledRowIn_ChkAll(P01.ActiveSheet))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
def DelLast(s, Cnt=1):
    #----------------------------------------------------------------------
    fn_return_value=s
    if Len(s) > 0:
        fn_return_value = Left(s, Len(s) - Cnt)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: s - ByVal 
def DelAllLast(s, Chars):
    #----------------------------------------------------------------
    while InStr(Chars, Right(s, 1)) > 0:
        s = Left(s, Len(s) - 1)
    fn_return_value = s
    return fn_return_value

def Center_Form(f):
    #---------------------------
    with_variable3 = f
    with_variable3.StartUpPosition = 0
    with_variable3.Left = P01.Application.Left +  ( P01.Application.Width - with_variable3.Width )  / 2
    with_variable3.Top = P01.Application.Top +  ( P01.Application.Height - with_variable3.Height )  / 2
    if with_variable3.Top < P01.Application.Top:
        with_variable3.Top = P01.Application.Top
        # 02.03.20
    if with_variable3.Left < P01.Application.Left:
        with_variable3.Left = P01.Application.Left

def Restore_Pos_or_Center_Form(f, OldPos):
    #--------------------------------------------------------------
    if OldPos.Valid:
        f.StartUpPosition = 0
        f.Left = OldPos.Left
        f.Top = OldPos.Top
    else:
        Center_Form(f)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PosVar - ByRef 
def Store_Pos(f, PosVar):
    #---------------------------------------------------
    PosVar.Valid = True
    PosVar.Left = f.Left
    PosVar.Top = f.Top

def Test_Center_Form():
    #UT---------------------------
    Center_Form(UserForm_Other)
    UserForm_Other.Show()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByVal 
def Replace_Multi_Space(Txt):
    Res = String()
    #----------------------------------------------------------
    Res = Txt
    while InStr(Res, r'  ') > 0:
        Res = Replace(Res, r'  ', r' ')
    fn_return_value = Res
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: c - ByVal 
def CellLinesSum(c):
    #--------------------------------------------------
    fn_return_value = 0 #*HL
    if InStr(c, vbLf):
        for Line in Split(c, vbLf):
            fn_return_value = fn_return_value + P01.val(Line)
    else:
        fn_return_value = P01.val(c)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByVal 
def Is_Contained_in_Array(Txt, Arr):
    fn_return_value = False
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

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: stringToBeFound - ByVal 
def IsInArray(stringToBeFound, Arr):
    i = int()
    #--------------------------------------------------------------------------
    # default return value if value not found in array
    fn_return_value = - 1
    for i in vbForRange(LBound(Arr), UBound(Arr)):
        if StrComp(stringToBeFound, Arr(i)) == 0:
            fn_return_value = i
            break
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: StartHide_Name - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: StartMove_Name - ByVal 
def Hide_and_Move_up(dlg, StartHide_Name, StartMove_Name):
    MoveDelta = int()

    StartHide_y = Single()

    StartMove_y = Single()

    c = Variant()
    #--------------------------------------------------------------------------------------------------
    # Hide the controls where StartHide_y <= controls.Top < StartMove_y
    # Move the controls up where controls.Top >= StartMove_y
    StartHide_y = dlg.Controls(StartHide_Name).Top
    StartMove_y = dlg.Controls(StartMove_Name).Top
    MoveDelta = StartMove_y - StartHide_y
    #Debug.Print "Hide_and_Move_up from '" & StartHide_Name & "' to '" & StartMove_Name & "' " & MoveDelta ' Debug
    for c in dlg.Controls:
        if c.Top >= StartMove_y -1:         # 15.03.22: Buttons are placed 1 pixel above input field/label
            c.Top = c.Top - MoveDelta
        elif c.Top >= StartHide_y -1:       # 15.03.22: Buttons are placed 1 pixel above input field/label
            c.Visible = False
    dlg.Height = dlg.Height - MoveDelta

def FindHeadCol(Sh, Row, Name):
    r = None #Range()

    p = None #Variant()
    #-------------------------------------------------------------------------
    with_variable4 = Sh
    r = with_variable4.Range(with_variable4.Cells(Row, 1), with_variable4.Cells(Row, LastUsedColumnIn(Sh)))
    ## VB2PY (CheckDirective) VB directive took path 1 on 1
    p = P01.Application.Match(Name, r, 0)
    if IsError(p):
        P01.MsgBox(M09.Get_Language_Str(r'Fehler: Die Spalte '') + Name + M09.Get_Language_Str(r'' wurde nicht im Sheet '') + Sh.Name + M09.Get_Language_Str(r'' gefunden!' + vbCr + vbCr + r'Die Spaltennamen dürfen nicht verändert werden'), vbCritical, M09.Get_Language_Str(r'Fehler Spaltenname nicht gefunden'))
        EndProg()
    else:
        fn_return_value = p
    return fn_return_value

def Test_FindHeadCol():
    #UT---------------------------
    Debug.Print(FindHeadCol(P01.ActiveSheet, 2, r'Beschreibung'))

def InputBoxMov(prompt, Title=VBMissingArgument, Default=VBMissingArgument, Left=VBMissingArgument, Top=VBMissingArgument, helpfile=VBMissingArgument, HelpContextID=VBMissingArgument):
    OldUpdate = Boolean()
    #--------------------------------------------------------------------------------------------------------
    # InputBox which could be moved with correct screen update even if screenupdating is disabled
    OldUpdate = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = True
    fn_return_value = InputBox(prompt, Title, Default, Left, Top, helpfile, HelpContextID)
    Sleep(50)
    P01.Application.ScreenUpdating = OldUpdate
    return fn_return_value

def Test_InputBoxMov():
    #-----------------------------
    P01.Application.ScreenUpdating = False
    Debug.Print(InputBoxMov(r'Hallo', r'Title', r'Dafault'))
    P01.Application.ScreenUpdating = True

def MsgBoxMov(prompt, Buttons=VBMissingArgument, Title=VBMissingArgument, helpfile=VBMissingArgument, context=VBMissingArgument):
    OldUpdate = Boolean()
    #----------------------------------------------------------------------------------------
    # MsgBox which could be moved with correct screen update even if screenupdating is disabled
    OldUpdate = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = True
    fn_return_value = P01.MsgBox(prompt, Buttons, Title)
    #*HL Sleep(50)
    P01.Application.ScreenUpdating = OldUpdate
    return fn_return_value

def Test_MsgBoxMov():
    #UT-------------------------
    P01.Application.ScreenUpdating = False
    Debug.Print(MsgBoxMov(r'Hallo', vbYesNoCancel, r'Titel'))
    P01.Application.ScreenUpdating = True

def ShowHourGlassCursor(bApply):
    return #*HL'

    pt = POINTAPI()
    #-----------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on HostProject = "Access"
    P01.Application.DoCmd.Hourglass(bApply)
    ## VB2PY (CheckDirective) VB directive took path 1 on Mac = False
    if not bApply:
        # in some systems the cursor may fail to reset to default, this forces it
        GetCursorPos(pt)
        SetCursorPos(pt.X, pt.Y)
        

def IsHourGlassCursor():
    #---------------------------------------------
    fn_return_value = ( P01.Application.Cursor == xlWait )
    return fn_return_value

def EndProg():
    #-------------------
    # Is called in case of an fatal error
    # Normaly this function should not be called because the
    # global variables and dialog positions are cleared.
    #ShowHourGlassCursor(False)
    P01.Application.EnableEvents = True
    P01.Application.ScreenUpdating = True
    Debug.Print("Error in Dialog: End_Prog()")
    raise Exception("Error in Dialog")

def ClearStatusbar():
    #--------------------------
    # Is called by onTime to clear the status bar after a while
    P01.set_statusmessage("")

def Show_Status_for_a_while(Txt, Duration=r'00:00:15'):
    #-------------------------------------------------------------------------------------------
    P01.set_statusmessage(Txt)
    if Txt != r'':
        P01.Application.OnTime(15000, ClearStatusbar)
    else:
        P01.Application.OnTime(15000, ClearStatusbar)

def All_Borderlines(r):
    #-------------------------------------
    #r.Select ' Debug
    r.Borders[xlDiagonalDown].LineStyle = xlNone
    r.Borders[xlDiagonalUp].LineStyle = xlNone
    with_variable5 = r.Borders(xlEdgeLeft)
    with_variable5.LineStyle = xlContinuous
    with_variable5.ColorIndex = 0
    with_variable5.TintAndShade = 0
    with_variable5.Weight = xlThin
    with_variable6 = r.Borders(xlEdgeTop)
    with_variable6.LineStyle = xlContinuous
    with_variable6.ColorIndex = 0
    with_variable6.TintAndShade = 0
    with_variable6.Weight = xlThin
    with_variable7 = r.Borders(xlEdgeBottom)
    with_variable7.LineStyle = xlContinuous
    with_variable7.ColorIndex = 0
    with_variable7.TintAndShade = 0
    with_variable7.Weight = xlThin
    with_variable8 = r.Borders(xlEdgeRight)
    with_variable8.LineStyle = xlContinuous
    with_variable8.ColorIndex = 0
    with_variable8.TintAndShade = 0
    with_variable8.Weight = xlThin
    with_variable9 = r.Borders(xlInsideVertical)
    with_variable9.LineStyle = xlContinuous
    with_variable9.ColorIndex = 0
    with_variable9.TintAndShade = 0
    with_variable9.Weight = xlThin
    with_variable10 = r.Borders(xlInsideHorizontal)
    with_variable10.LineStyle = xlContinuous
    with_variable10.ColorIndex = 0
    with_variable10.TintAndShade = 0
    with_variable10.Weight = xlThin

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def FileNameExt(Name):
    basename = os.path.basename(Name)
    return basename

    Pos = int()

    Pos2 = int()

    Temp = String()
    #---------------------------------------------------
    # Return name and extention without path
    Pos = InStrRev(Name, r'\\')
    Pos2 = InStrRev(Name, r'/')
    if Pos2 > Pos:
        Pos = Pos2
    if Pos > 0:
        Temp = Mid(Name, Pos + 1)
    else:
        Pos = InStrRev(Name, r':')
        if Pos > 0:
            Temp = Mid(Name, Pos + 1)
        else:
            Temp = Name
    fn_return_value = Temp
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def FilePath(Name):
    #------------------------------------------------
    fn_return_value = Left(Name, Len(Name) - Len(FileNameExt(Name)))
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def NoExt(Name):
    Pos = int()
    #---------------------------------------------
    # Cut of the extention of a filename
    Pos = InStrRev(Name, r'.')
    if Pos > 0:
        fn_return_value = Left(Name, Pos - 1)
    else:
        fn_return_value = Name
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def FileName(Name):
    #------------------------------------------------
    # Return name without extention and path
    fn_return_value = NoExt(FileNameExt(Name))
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: FullName - ByVal 
def Same_Name_already_open(FullName):
    #w = Variant()

    #Name = String()
    #-------------------------------------------------------------------
    # Check if a workbook with the same name is already opened
    Name = FileNameExt(FullName)
    for w in P01.Workbooks:
        if UCase(w.Name) == UCase(Name):
            fn_return_value = True
            return fn_return_value
    return fn_return_value

def SheetEx(Name):
    #-------------------------------
    fn_return_value=False
    for s in PG.ThisWorkbook.sheets:
        if s.Name == Name:
            fn_return_value = True
            return fn_return_value
    return fn_return_value

def Protect_Active_Sheet():
    #-------------------------
    P01.ActiveSheet.Protect(DrawingObjects=True, Contents=True, Scenarios=True, AllowFormattingCells=True, AllowInsertingHyperlinks=True)

def ColumnLetters(r):
    #-------------------------------------------
    fn_return_value = Replace(Replace(r.Address, r'$', r''), r.Row, r'')
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Colunm - ByVal 
def ColumnLettersFromNr(Colunm):
    #-------------------------------------------------
    fn_return_value = ColumnLetters(P01.Cells(1, Colunm))
    return fn_return_value

def DisableFiltersInSheet(s):
    #obj = Variant()
    #----------------------------------------
    if s.AutoFilterMode:
        if s.FilterMode:
            # VB2PY (UntranslatedCode) On Error Resume Next
            s.ShowAllData()
            # VB2PY (UntranslatedCode) On Error GoTo 0
            return
    # Check if a table is used. In this case the filter can't be disabled if the active cell is not located in the table
    for obj in s.ListObjects:
        if not obj.AutoFilter is None:
            OldActCell = P01.ActiveCell()
            s.Cells(obj.Range.Row, obj.Range.Column).Select()
            # VB2PY (UntranslatedCode) On Error Resume Next
            s.ShowAllData()
            # VB2PY (UntranslatedCode) On Error GoTo 0
            OldActCell.Select()
            return

def isVariantArray(v):
    i = int()
    #-----------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo ErrorDet
    i = UBound(v)
    fn_return_value = True
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return fn_return_value

def F_shellExec(sCmd):
    #oShell = WshShell()
    #----------------------------------------------------
    # Excecute command and get the output as string
    # Example call:
    #   MsgBox F_shellExec("cmd /c dir c:\")
    #
    # Requires ref to Windows Script Host Object Model
    # To do this go to Extras -> References in the VBA IDE's menu bar.
    # See:
    #   https://stackoverflow.com/questions/2784367/capture-output-value-from-a-shell-command-in-vba
    #fn_return_value = oShell.Exec(sCmd).StdOut.ReadAll
    
    proc = subprocess.Popen(sCmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    fn_return_value = proc.stdout.read()    
    
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: WindowMode - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Wait - ByVal 
def F_shellRun(sCmd, WindowMode, Wait):
    #oShell = WshShell()
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
    
    subprocess.call(sCmd)
    #oShell.Run(sCmd, WindowMode, Wait)

def Test_Shell():
    #UT---------------------
    P01.MsgBox(F_shellExec(r'cmd /c Dir C:\\'))

def Read_File_to_String(FileName):
    #strFileContent = String()

    #fp = Integer()
    #----------------------------------------------------------------
    #fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo ReadError
    try:
        #open text file in read mode
        text_file = open(FileName, "r")
         
        #read whole file to a string
        fn_return_value = text_file.read()
         
        #close file
        text_file.close()        

        # VBFiles.openFile(fp, FileName(), 'r') 
        # fn_return_value = Input(LOF(fp), fp)
        # VBFiles.closeFile(fp)
        return fn_return_value
    except BaseException as e:
        Debug.Print("Read_File_to_String: Fehler beim Lesen der Datei "+FileName)
        logging.debug(e)
        P01.MsgBox(M09.Get_Language_Str(r'Fehler beim lesen der Datei:') + vbCr + r'  ' + FileName + r'', vbCritical, M09.Get_Language_Str(r'Fehler beim Datei lesen'))
        fn_return_value = r'#ERROR#'
        return fn_return_value

def Get_Ini_Entry(FileStr, EntryName):
    p = int()

    e = String()
    #------------------------------------------------------------------------------
    fn_return_value = r'#ERROR#'
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

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Arr - ByRef 
def Debug_Print_Arr(Arr, ArrName=r'arr'):
    i = int()
    #-----------------------------------------------------------------------------------
    for i in vbForRange(0, UBound(Arr)):
        Debug.Print(ArrName + r'(' + i + r')=' + Arr(i))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Index - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: prLst - ByRef 
def DeleteElementAt(Index, prLst):
    i = int()
    #-------------------------------------------------------------------------
    # Move all element back one position
    for i in vbForRange(Index + 1, UBound(prLst)):
        prLst[i - 1] = prLst(i)
    # Shrink the array by one, removing the last one
    #prLst = vbObjectInitialize((UBound(prLst) - 1,), Variant, prLst)
    prLst.delete()

def Test_DeleteElementAt():
    Arr = vbObjectInitialize(objtype=String)
    #UT-------------------------------
    Arr = Split(r'A B C D E', r' ')
    DeleteElementAt(1, Arr)
    Debug.Print(r'')
    Debug_Print_Arr(Arr, r'arr')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Index - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: prLst - ByRef 
def InsertElementAt(Index, prLst, InsertVal):
    i = int()
    #-----------------------------------------------------------------------------------------------
    # index could be 0 .. UBound(prLst)+1
    # If index is > UBound(prLst)+1 the function will crash
    # Tested with prList() string and prList() interger
    prLst = vbObjectInitialize((UBound(prLst) + 1,), Variant, prLst)
    for i in vbForRange(UBound(prLst), Index + 1, - 1):
        prLst[i] = prLst(i - 1)
    prLst[Index] = InsertVal

def Test_InsertElementAt():
    Arr = vbObjectInitialize(objtype=String)

    iarr = vbObjectInitialize(objtype=Integer)

    i = int()
    #UT-------------------------------
    Arr = Split(r'1 2 3 4 5', r' ')
    InsertElementAt(0, Arr, 0)
    Debug.Print(r'')
    Debug_Print_Arr(Arr, r'arr')
    iarr = vbObjectInitialize((UBound(Arr),), Variant)
    for i in vbForRange(0, UBound(Arr)):
        iarr[i] = Arr(i)
    InsertElementAt(3, iarr, - 1)
    Debug_Print_Arr(iarr, r'iarr')

def GetPathOnly(sPath):
    #------------------------------------------------------
    fn_return_value = Left(sPath, InStrRev(sPath, '/', Len(sPath)) - 1)
    return fn_return_value

def CreateFolder(sFolder):
    s = String()
    #--------------------------------------------------------
    # http://www.freevbcode.com/ShowCode.asp?ID=257
    # sFolder must have an "\" at the end
    # VB2PY (UntranslatedCode) On Error GoTo ErrorHandler
    logging.debug("Create_Folder:"+sFolder)
    s = GetPathOnly(sFolder)
    if Dir(s) == r'':
        s = CreateFolder(s)
        MkDir(s)
    fn_return_value = sFolder
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: zippedFileFullName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: unzipToPath - ByVal 
def UnzipAFile(zippedFileFullName, unzipToPath):
    #ShellApp = Object()
    #-------------------------------------------------------------------------------------------------------
    # The Destination directory must exist
    # The Arguments must be "byVal" and "Variant" otherwise the program fails
    #Copy the files & folders from the zip into a folder
    #ShellApp = CreateObject(r'Shell.Application')
    # VB2PY (UntranslatedCode) On Error GoTo ErrMsg
    #ShellApp.Namespace(unzipToPath).CopyHere(ShellApp.Namespace(zippedFileFullName).Items)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    
    zip = zipfile.ZipFile(zippedFileFullName)
    #os.mkdir(unzipToPath)
    zip.extractall(path=unzipToPath)    
    
    fn_return_value = True
    return fn_return_value
    #MsgBox(Replace(Replace(M09.Get_Language_Str(r'Fehler beim entpacken der ZIP-Datei:' + vbCr + r'  "#1#"' + vbCr + r'nach' + vbCr + r'  '#2#''), r'#1#', zippedFileFullName), r'#2#', unzipToPath), vbCritical, M09.Get_Language_Str(r'Fehler: Zip-Datei konnte nicht entpackt werden'))
    #return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: a - ByRef 
def isInitialised(a):
    #----------------------------------------------------
    # Check if an array in initialized
    # This is usefull for functions which return an array
    # in case they fail
    # VB2PY (UntranslatedCode) On Error Resume Next
    fn_return_value = IsNumeric(UBound(a))
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Text - ByVal 
def SplitMultiDelims(Text, DelimChars):
    Pos1 = int()

    N = int()

    M = int()

    Arr = vbObjectInitialize(objtype=String)

    i = int()

    TextLen = int()
    #--------------------------------------------------------------------------------
    # SplitMutliChar
    # This function splits Text into an array of substrings, each substring
    # delimited by any character in DelimChars. Only a single character
    # may be a delimiter between two substrings, but DelimChars may
    # contain any number of delimiter characters. It returns
    # an unallocated array it Text is empty, a single element array
    # containing all of text if DelimChars is empty, or a 1 or greater
    # element array if the Text is successfully split into substrings.
    #
    # http://www.cpearson.com/excel/splitondelimiters.aspx
    #
    # Adapted by Hardi to
    # - skip multiple delimiters between two parts
    # - generate an array starting wit 0 like the split function
    #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    TextLen = Len(Text)
    #'''''''''''''''''''''''''''''''
    # if Text is empty, get out
    #'''''''''''''''''''''''''''''''
    if TextLen == 0:
        return fn_return_value
    #'''''''''''''''''''''''''''''''''''''''''''''
    # if DelimChars is empty, return original text
    #''''''''''''''''''''''''''''''''''''''''''''
    if DelimChars == vbNullString:
        fn_return_value = Array(Text)
        return fn_return_value
    #''''''''''''''''''''''''''''''''''''''''''''''
    # oversize the array, we'll shrink it later so
    # we don't need to use Redim Preserve
    #''''''''''''''''''''''''''''''''''''''''''''''
    Arr = vbObjectInitialize(((0, Len(Text) - 1),), Variant)
    i = 0
    N = 1
    while N <= TextLen and InStr(DelimChars, Mid(Text, N, 1)) > 0:
        N = N + 1
    Pos1 = N
    N = N + 1
    while N <= TextLen:
        if InStr(DelimChars, Mid(Text, N, 1)) > 0:
            Arr[i] = Mid(Text, Pos1, N - Pos1)
            i = i + 1
            while N <= TextLen and InStr(DelimChars, Mid(Text, N, 1)) > 0:
                N = N + 1
            Pos1 = N
        N = N + 1
    if Pos1 <= Len(Text):
        Arr[i] = Mid(Text, Pos1)
        i = i + 1
    #'''''''''''''''''''''''''''''''''''''
    # chop off unused array elements
    #'''''''''''''''''''''''''''''''''''''
    if i >= 1:
        Arr = vbObjectInitialize(((0, i - 1),), Variant, Arr)
        fn_return_value = Arr
    return fn_return_value

def Test_SplitMultiDelims():
    Res = vbObjectInitialize(objtype=String)

    i = int()
    #UT--------------------------------
    Debug.Print(r'Test_SplitMultiDelims')
    Res = SplitMultiDelims(r'  Text  with+several|delimmiters +|', r' +|')
    #Res = SplitMultiDelims("a", " +|")
    if isInitialised(Res):
        for i in vbForRange(0, UBound(Res)):
            Debug.Print(r''' + Res(i) + r''')
    Debug.Print(r'---')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InString - ByVal 
def SplitEx(InString, IgnoreDoubleDelmiters, *Delims):
    Delims = VBArray.createFromData(Delims)
    Arr = vbObjectInitialize(objtype=String)

    Ndx = int()

    N = int()
    #-----------------------------------------------------------------------------------------------------------------------
    # http://www.cpearson.com/excel/splitondelimiters.aspx
    if Len(InString) == 0:
        fn_return_value = Arr
        return fn_return_value
    if IgnoreDoubleDelmiters == True:
        for Ndx in vbForRange(LBound(Delims), UBound(Delims)):
            N = InStr(1, InString, Delims(Ndx) + Delims(Ndx), vbTextCompare)
            while not (N == 0):
                InString = Replace(InString, Delims(Ndx) + Delims(Ndx), Delims(Ndx))
                N = InStr(1, InString, Delims(Ndx) + Delims(Ndx), vbTextCompare)
    Arr = vbObjectInitialize(((1, Len(InString)),), Variant)
    for Ndx in vbForRange(LBound(Delims), UBound(Delims)):
        InString = Replace(InString, Delims(Ndx), Chr(1))
    Arr = Split(InString, Chr(1))
    fn_return_value = Arr
    return fn_return_value

def Test_SplitEx():
    s = String()

    t = vbObjectInitialize(objtype=String)

    N = int()
    #UT-----------------------
    # Attention: The result contains space characters
    #S = "A AND #InCh OR A AND NOT #InCh + 1 OR D"
    #S = "#InCh"
    t = SplitEx(s, True, r'OR', r'AND', r'NOT')
    if isInitialised(t):
        for N in vbForRange(LBound(t), UBound(t)):
            Debug.Print(N, t(N))
    else:
        Debug.Print(r'Empty')

def Get_Primary_Monitor_Pixel_Cnt_X():
    #--------------------------------------------------------
    fn_return_value = PG.global_controller.winfo_screenwidth() # GetSystemMetrics(SM_CXSCREEN)
    return fn_return_value

def Get_Primary_Monitor_Pixel_Cnt_Y():
    #--------------------------------------------------------
    fn_return_value = PG.global_controller.winfo_screenheight() # GetSystemMetrics(SM_CYSCREEN)
    return fn_return_value

def ResetComments():
    #objComment = Comment()
    #------------------
    # https://www.heise.de/ct/hotline/Excel-Kommentare-automatisch-positionieren-2055961.html
    # Alle Kommentare des aktuellen Arbeitsblatts
    # durchlaufen
    
    return #*HL

    for objComment in P01.ActiveSheet.Comments:
        with_variable11 = objComment
        # Top-Wert des Kommentars auf Top-Wert
        # der verknüpften Zelle setzen
        with_variable11.Shape.Top = with_variable11.Parent.Top + with_variable11.Parent.Height - with_variable11.Shape.Height
        # Left-Wert des Kommentars auf Left-Wert
        # der verknüpften Zelle plus Zellbreite
        # mal zwei setzen
        with_variable11.Shape.Left = with_variable11.Parent.Left +  ( with_variable11.Parent.Width * 2 )

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: vArrayName - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lUpper=- 1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lLower=- 1 - ByVal 

def Array_BubbleSort(vArrayName, lUpper=- 1, lLower=- 1):
    vtemp = Variant()

    i = int()

    j = int()
    #---------------------------------------------------------
    # https://bettersolutions.com/vba/arrays/sorting-bubble-sort.htm
    if P01.IsEmpty(vArrayName) == True:
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
    Button.Visible = ( Text != r'' )
    if Text != r'':
        Err = ( Len(Text) < 3 )
        if not Err:
            Err = ( Mid(Text, 2, 1) != r' ' )
        if Err:
            P01.MsgBox(r'Internal Error: Button text is wrong '' + Text + r''.' + vbCr + r'It must contain an Accelerator followed by the text.' + vbCr + r'Example: "H Hallo"', vbCritical, r'Internal Error (Wrong translation?)')
            M30.EndProg()
        Button.Caption = Mid(Text, 3, 255)
        Button.Accelerator = Left(Text, 1)

#----------------------------------------
def Bring_Application_to_front():
    Bring_to_front (P01.Application.hWnd)                                          # 06.03.22: Juergen add helper function

#----------------------------------------
        

def Bring_to_front(hwnd):
    #----------------------------------------
    # Is not working if an other application has be moved above Excel with Alt+Tab
    # But this is a feature od Windows.
    # See: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow
    # But it brings up excel again after the upload to the Arduino
    # Without this funchion an other program was activated after the upload for some reasons
    PG.ThisWorkbook.Activate()
    #*HL SetForegroundWindow(hwnd)

def Replicate(RepeatString, NumOfTimes):
    s = String()

    c = int()

    l = int()

    i = int()
    #--------------------------------------------------------------------
    l = Len(RepeatString)
    c = l * NumOfTimes
    s = "" #Space(c)
    fn_return_value=""
    for i in vbForRange(1, c, l):
        s = s + RepeatString
        #Mid[s, i, l] = RepeatString
    fn_return_value = s
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Source - ByRef 
def ConvertToUTF8(Source):
    #Length = int()

    #Pointer = LongPtr()

    #Size = int()

    #Buffer = vbObjectInitialize(objtype=Byte)
    #---------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    #Length = Len(Source)
    #Pointer = StrPtr(Source)
    #Size = WideCharToMultiByte(CP_UTF8, 0, Pointer, Length, 0, 0, 0, 0)
    #Buffer = vbObjectInitialize(((0, Size - 1),), Variant)
    #WideCharToMultiByte(CP_UTF8, 0, Pointer, Length, VarPtr(Buffer(0)), Size, 0, 0)
    #fn_return_value = Buffer
    
    fn_return_value =  Source.encode('utf-8')
    
    return fn_return_value    
    
    

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Source - ByRef 
def ConvertToUTF8Str(Source):
    fn_return_value =  Source #*HL.encode('utf-8')
    
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Source - ByRef 
def ConvertFromUTF8(Source):
    Size = int()

    #Pointer = LongPtr()

    Length = int()

    Buffer = String()
    #----------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    #Size = UBound(Source) - LBound(Source) + 1
    #Pointer = VarPtr(Source(LBound(Source)))
    #Length = MultiByteToWideChar(CP_UTF8, 0, Pointer, Size, 0, 0)
    #Buffer = Space(Length)
    #MultiByteToWideChar(CP_UTF8, 0, Pointer, Size, StrPtr(Buffer), Length)
    #fn_return_value = Buffer
    Source_str = str(Source)
    fn_return_value =  Source_str.decode('utf-8')
    
    return fn_return_value

def ConvertUTF8Str(UTF8Str):
    bStr = vbObjectInitialize(objtype=Byte)

    i = int()
    #----------------------------------------------------------
    bStr = vbObjectInitialize((Len(UTF8Str) - 1,), Variant)
    for i in vbForRange(1, Len(UTF8Str)):
        bStr[i - 1] = Asc(Mid(UTF8Str, i, 1))
    fn_return_value = ConvertFromUTF8(bStr)
    
   # fn_return_value =  UTF8Str.decode('utf-8')
    return fn_return_value

def Dir_is_Empty(DirName):
    
    #---------------------------------------------------------
    # Return false it the directory contains at least one subdirectory or one file
    searchpath = pathlib.Path(DirName)
    if searchpath.exists():
        pathlist=pathlib.Path(DirName).iterdir()
        for path in pathlist:
            if path !="":
                return False
        return True
    return True


def Get_First_SubDir(DirName):
    Res = String()
    fn_return_value=""
    #------------------------------------------------------------
    if DirName[-1:]=="/":
        DirName = DirName[:-1]
        
    Res = Dir(DirName + r'/*.*', vbDirectory)
    while Res != r'':
        if Res != r'' and Left(Res, 1) != r'.':
            fn_return_value = Res
            return fn_return_value
        Res = Dir()
    return fn_return_value

def VersionStr_is_Greater(Ver1, Ver2, Delimmiter=r'.'):
    Ver1A = vbObjectInitialize(objtype=String)

    Ver2A = vbObjectInitialize(objtype=String)

    EndNr = int()

    Nr = int()
    #--------------------------------------------------------------------------------------------------------------------
    # Compares two version strings like
    #  "1.0.7"
    # If one string is shorter than the other the missing digits are replaced by 0
    # "1.0" => "1.0.0"
    Ver1A = Split(Ver1, Delimmiter)
    Ver2A = Split(Ver2, Delimmiter)
    EndNr = max(UBound(Ver1A), UBound(Ver2A))
    for Nr in vbForRange(0, EndNr):
        if UBound(Ver1A) >= Nr:
            v1 = P01.val(Ver1A(Nr))
        else:
            v1 = 0
        if UBound(Ver2A) >= Nr:
            v2 = P01.val(Ver2A(Nr))
        else:
            v2 = 0
        if v1 != v2:
            fn_return_value = v1 > v2
            return fn_return_value
    return False

def Test_VersionStr_is_Greater():
    #UT-------------------------------------
    #Debug.Print VersionStr_is_Greater("1.0.7", "1.03.1")
    #Debug.Print VersionStr_is_Greater("1.0.7", "1.0.1")
    #Debug.Print VersionStr_is_Greater("1.0.7", "1.0.8")
    #Debug.Print VersionStr_is_Greater("2.0.7", "")
    Debug.Print(VersionStr_is_Greater(r'1.0.8', r'1.0.7b'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DirName - ByVal 
def Del_Folder(DirName, ShowError=True):
    #---------------------------------------------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo ErrMsg
    #*HLCreateObject(r'Scripting.FileSystemObject').DeleteFolder(DirName)
    shutil.rmtree(DirName) #*HL
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = True
    return fn_return_value
    if ShowError:
        P01.MsgBox(Replace(M09.Get_Language_Str(r'Fehler beim Löschen des Verzeichnisses:' + vbCr + r'  "#1#"' + vbCr + r'Evtl. enthält es Dateien welche in einem anderen Programm geöffnet sind oder es ist ' + r'das Arbeitsverzeichnis eines Programms und darf darum nicht gelöscht werden.'), r'#1#', DirName), vbCritical, M09.Get_Language_Str(r'Verzeichnis konnte nicht (vollständig) gelöscht werden'))
    return fn_return_value

def Get_OperatingSystem():
    teststr = platform.platform()
    logging.debug("Get_OperatingSystem: "+teststr)
    return teststr

    # return "Microsoft Windows 10 Home         10.0.18362" #*HL
    localHost = String()

    objWMIService = Variant()

    colOperatingSystems = Variant()

    objOperatingSystem = Variant()
    #----------------------------------------------
    # Returns something like:
    #   objOperatingSystem.Caption        objOperatingSystem.Version
    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~        ~~~~~~~~~~~~~~~~~~~~~~~~~~
    #  "Microsoft Windows 10 Home         10.0.18362"
    #  "Microsoft Windows 8.1 Pro         6.3.9600"
    #  "Microsoft Windows 7 Home Premium  6.1.7601"
    # VB2PY (UntranslatedCode) On Error GoTo Error_Handler
    fn_return_value = ""
    localHost = r'.'
    objWMIService = GetObject(r'winmgmts:{impersonationLevel=impersonate}!\\' + localHost + r'\root\cimv2')
    colOperatingSystems = objWMIService.ExecQuery(r'Select * from Win32_OperatingSystem')
    for objOperatingSystem in colOperatingSystems:
        fn_return_value = objOperatingSystem.Caption + vbTab + objOperatingSystem.Version
        return fn_return_value
    # VB2PY (UntranslatedCode) On Error Resume Next
    return fn_return_value
    P01.MsgBox(r'The following error has occured.' + vbCrLf + vbCrLf + r'Error Number: ' + Err.Number + vbCrLf + r'Error Source: getOperatingSystem' + vbCrLf + r'Error Description: ' + Err.Description, vbCritical, r'An Error has Occured!')
    # VB2PY (UntranslatedCode) Resume Error_Handler_Exit
    return fn_return_value

def Win10_or_newer():
    OpSys = String()

    Nr = Double()
    #------------------------------------------
    OpSys = Get_OperatingSystem()
    Nr = P01.val(Mid(OpSys, Len(r'Microsoft Windows '),num=3)) #*HL
    fn_return_value = ( Nr >= 10 )
    return fn_return_value

def Check_Version():
    if not Valid_Excel():
        message = Replace(M09.Get_Language_Str(r'Diese Excel Version wird nicht unterstützt.' + r'Bitte besuchen sie die Webseite #1# für weitergehende Informationen.' + r'Das Programm wird weiter ausgeführt, es kann jedoch zu unerwarteten Fehlfunktionen' + r', Fehlermeldung und Abstürzen kommen.'), r'#1#', vbCrLf + vbCrLf + r'https://wiki.mobaledlib.de/anleitungen/programmgenerator' + vbCrLf + vbCrLf)
        P01.MsgBox(message, vbCritical, M09.Get_Language_Str(r'Versionsprüfung'))
    return

def Valid_Excel():
    
    exVer = Variant()
    #------------------------------------------
    # see details on https://wiki.mobaledlib.de/anleitungen/programmgenerator
    # Excel Version on https://de.wikipedia.org/wiki/Microsoft_Excel
    ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
    exVer = P01.val(P01.Application.Version)
    fn_return_value = exVer >= 15
    return fn_return_value

def Test_Get_OperatingSystem():
    #UT-----------------------------------
    Debug.Print(r'Get_OperatingSystem:' + Get_OperatingSystem())

def Test_Select_LastusedCol():
    #------------------------------------
    P01.Cells(1, LastUsedColumn()).Select()

def Clear_Platform_Parameter_Cache():
    global PlatformParams
    PlatformParams = None

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: EmptyCheck=False - ByVal 
def Get_Current_Platform_String(ParName, EmptyCheck=False, Silent=False):
    fn_return_value = Get_Platform_String(M02a.Get_BoardTyp(), ParName, EmptyCheck, Silent)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParName - ByVal 
def Get_Current_Platform_Bool(ParName, Silent=False):
    fn_return_value = Get_Platform_Bool(M02a.Get_BoardTyp(), ParName, Silent)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParName - ByVal 
def Get_Current_Platform_Int(ParName, Silent=False):
    fn_return_value = Get_Platform_Int(M02a.Get_BoardTyp(), ParName, Silent)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PlatformKey - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: EmptyCheck=False - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Silent=False - ByVal 
def Get_Platform_String(PlatformKey, ParName, EmptyCheck=False, Silent=False):
    #Offs = int()

    #r = Range()

    #f = Variant()

    #Platform_COL = Integer()
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    fn_return_value = r''
    global PlatformParams
    if PlatformParams is None:
        PlatformParams = {} #*HL  Scripting.Dictionary()
    #if PlatformParams.Exists(PlatformKey + r'|' + ParName):
    if (PlatformKey + r'|' + ParName in PlatformParams.keys()): #*HL
        fn_return_value = PlatformParams.get(PlatformKey + r'|' + ParName) #*HL
        return fn_return_value
    Sh = PG.ThisWorkbook.Sheets(M02.PLATFORMS_SH)
    r = Sh.Range(Sh.Cells(PlatformKey_ROW, PlatformKey_COL), Sh.Cells(PlatformKey_ROW, PlatformKey_COL + 99))
    f = r.Find(What= PlatformKey, LookIn= xlFormulas, LookAt= xlWhole, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False)
    if f is None:
        Debug.Print(r'Fehlende Plattform ' + PlatformKey)
        if not Silent:
            P01.MsgBox(Replace(M09.Get_Language_Str(r'Fehler: Die Plattform "#1#" ist nicht definiert.'), r'#1#', PlatformKey), vbCritical, M09.Get_Language_Str(r'Internal Error'))
        return fn_return_value
    Platform_COL = f.Column
    r = Sh.Range(Sh.Cells(PlatformKey_ROW + 1, PlatformParName_COL), Sh.Cells(LastUsedRowIn(Sh), PlatformParName_COL))
    f = r.Find(What= ParName, LookIn= xlFormulas, LookAt= xlWhole, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False)
    if f is None:
        if not Silent:
            Show_Missing_Platform_Parameter_Error(PlatformKey, ParName)
        return fn_return_value
    if EmptyCheck and Sh.Cells(f.Row, Platform_COL) == r'':
        Debug.Print(r'Der Parameter' + ParName + r' für Plattform ' + PlatformKey + r' darf nicht leer sein')
        if not Silent:
            Show_Invalid_Platform_Parameter_Error(PlatformKey, ParName)
        return fn_return_value
    fn_return_value = Sh.Cells(f.Row, Platform_COL)
    # values starting with "=" indicate an indirection, get the referenced value
    if Left(fn_return_value, 1) == r'=': #*HL
        fn_return_value = Get_Platform_String(PlatformKey, Mid(fn_return_value, 2), EmptyCheck, Silent) #*HL
    #PlatformParams.Add(PlatformKey + r'|' + ParName, fn_return_value) #*HL
    PlatformParams[PlatformKey + r'|' + ParName] =  fn_return_value #*HL
        
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PlatformKey - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParName - ByVal 
def Get_Platform_Bool(PlatformKey, ParName, Silent=False):
    Value = String()
    fn_return_value = False
    Value = Get_Platform_String(PlatformKey, ParName, True, Silent)
    if UCase(Value) == r'TRUE' or Value == r'1':
        fn_return_value = True
    elif not UCase(Value) == r'FALSE' and Value != r'0':
        Debug.Print(r'Der Parameter' + ParName + r' für Plattform ' + PlatformKey + r' ist weder true noch false')
        Show_Invalid_Platform_Parameter_Error(PlatformKey, ParName)
        return fn_return_value
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PlatformKey - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParName - ByVal 
def Get_Platform_Int(PlatformKey, ParName, Silent=False):
    Value = String()
    fn_return_value = 0
    Value = Get_Platform_String(PlatformKey, ParName, True, Silent)
    if not IsNumeric(Value):
        Debug.Print(r'Der Parameter' + ParName + r' für Plattform ' + PlatformKey + r' ist nicht numerisch')
        Show_Invalid_Platform_Parameter_Error(PlatformKey, ParName)
        return fn_return_value
    fn_return_value = P01.val(Value)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Pin - ByVal 
def AliasToPin(Pin):
    fn_return_value = Get_Current_Platform_String(r'PIN_ALIAS_' + UCase(Pin), False, True)
    if AliasToPin() == r'':
        # not a valid alias definition
        fn_return_value = Pin
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PlatformKey - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParName - ByVal 
def Show_Invalid_Platform_Parameter_Error(PlatformKey, ParName):
    P01.MsgBox(Replace(Replace(M09.Get_Language_Str(r'Fehler: Der Parameter "#2#" für die Plattform "#1#" hat keinen gültigen Wert.'), r'#1#', PlatformKey), r'#2#', ParName), vbCritical, M09.Get_Language_Str(r'Parameter Fehler'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PlatformKey - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParName - ByVal 
def Show_Missing_Platform_Parameter_Error(PlatformKey, ParName):
    Debug.Print(r'Fehlender Parameter: ' + ParName + r' für Plattform ' + PlatformKey)
    P01.MsgBox(Replace(Replace(M09.Get_Language_Str(r'Fehler: Der Parameter "#2#" ist für die Plattform "#1#" nicht definiert.'), r'#1#', PlatformKey), r'#2#', ParName), vbCritical, M09.Get_Language_Str(r'Parameter Fehler'))

def Test_Get_Platform_String():
    # Test values for parameter sheet
    #   SPI_Pins    Pin list must have leading & trailing blanks    10 11 12    5 19 23
    #   a       Test
    #   TRUE        TRUE
    #   TRue        TRue
    #   0       0
    #   1       1
    #   false       false
    #   intGood         -22
    #   intBad          a44
    Get_Platform_String(r'ESP32', r'SPI_Pins')
    Get_Platform_Bool(r'AM328', r'TRUE')
    Get_Platform_Bool(r'AM328', r'TRue')
    Get_Platform_Bool(r'AM328', r'false')
    Get_Platform_Bool(r'AM328', r'0')
    Get_Platform_Bool(r'AM328', r'1')
    Get_Platform_Int(r'PICO', r'intGood')
    Get_Platform_Int(r'PICO', r'intBad')

def Get_Act_ms():
    
    fn_return_value = int(time() * 1000)
    
    return fn_return_value

def HourGlassCursor(bApply):
    return #* no hourglass supported
    pt = POINTAPI()
    #--------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on HostProject = "Access"
    Application.DoCmd.Hourglass(bApply)
    ## VB2PY (CheckDirective) VB directive took path 1 on Mac = False
    if not bApply:
        # in some systems the cursor may fail to reset to default, this forces it
        GetCursorPos(pt)
        SetCursorPos(pt.X, pt.Y)
    return

def CreateHeaderFile(Platform, SheetName):
    OriginalPlatform = String()
    #MsgBox "CreateHeaderFile for " & Platform & "/" & SheetName
    #ThisWorkbook.Close SaveChanges:=False
    for Sh in P01.ActiveWorkbook.Sheets:
        if Sh.Name == SheetName:
            break
    if Sh is None:
        P01.MsgBox('The sheet ' + SheetName + ' does not exist')
        return
    PG.ThisWorkbook.Sheets(SheetName).Select()
    M25.Make_sure_that_Col_Variables_match()
    OriginalPlatform = P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL)
    if (Platform == 'ESP32'):
        P01.CellDict[M02.SH_VARS_ROW, M25.BUILDOP_COL] = M02.BOARD_ESP32
    elif (Platform == 'AM328'):
        P01.CellDict[M02.SH_VARS_ROW, M25.BUILDOP_COL] = M02.BOARD_NANO_NEW
    elif (Platform == 'PICO'):
        P01.CellDict[M02.SH_VARS_ROW, M25.BUILDOP_COL] = M02.BOARD_PICO
    else:
        P01.MsgBox('The platform ' + Platform + ' is not supported')
        return
    if M06.Create_HeaderFile(True):
        M12.FileCopy_with_Check(M08.GetWorkbookPath() + '/' + M02.Ino_Dir_LED, Platform + '_Header_' + SheetName + '.h', M08.GetWorkbookPath() + '/' + M02.Ino_Dir_LED + M02.Include_FileName)
    else:
        TargetName = M08.GetWorkbookPath() + '/' + M02.Ino_Dir_LED + Platform + '_Header_' + SheetName + '.h'
        if Dir(TargetName) != '':
            Kill(TargetName)
    P01.CellDict[M02.SH_VARS_ROW, M25.BUILDOP_COL] = OriginalPlatform
    
def __IsValidPageId(ID):
    fn_return_value = True
    if ID == 'DCC':
        return fn_return_value
    if ID == 'Selectrix':
        return fn_return_value
    if ID == 'CAN':
        return fn_return_value
    fn_return_value = False
    return fn_return_value

def CreateAllHeaderFiles():
   
    for Sh in P01.ActiveWorkbook.Sheets:
        if __IsValidPageId(Sh.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL)):
            CreateHeaderFile('ESP32', Sh.Name)
    for Sh in P01.ActiveWorkbook.Sheets:
        if __IsValidPageId(Sh.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL)):
            CreateHeaderFile('AM328', Sh.Name)
    for Sh in P01.ActiveWorkbook.Sheets:
        if __IsValidPageId(Sh.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL)):
            CreateHeaderFile('PICO', Sh.Name)

""" 31.01.22: Juergen
---------------------------------------------------------------------------------------------------------------------------------
"""
def Matches(p_str, reg, matchIndex=VBMissingArgument, subMatchIndex=VBMissingArgument):
    #---------------------------------------------------------------------------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo ErrHandl
    fn_return_value = False
    regex = CreateObject('VBScript.RegExp')
    regex.Pattern = reg
    regex.Global = not ( matchIndex == 0 and subMatchIndex == 0 ) 
    if regex.Test(p_str):
        Match = regex.Execute(p_str)
        fn_return_value = Match.Count == 1
        return fn_return_value
    fn_return_value = False
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SeachStr - ByVal 
def FastFind(SeachStr, r):
    _fn_return_value = None
    # 14.02.23: Hardi
    #--------------------------------------------------------------
    # .Match is much faster then .find
    # See: http://fastexcel.wordpress.com/2011/10/26/match-vs-find-vs-variant-array-vba-performance-shootout/
    # The search is case insensitive ! Also if its located in a "Option Compare Binary" modul
    # Filtered lines are also found.
    # VB2PY (UntranslatedCode) On Error GoTo NotFound
    _fn_return_value = P01.Application.WorksheetFunction.Match(SeachStr, r, 0)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SeachStr - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: r - ByVal 
def CSFastFind(SeachStr, r):
    _fn_return_value = None
    Offset = Long()
    # 14.02.23: Hardi
    #----------------------------------------------------------------------
    # Case sensitive FastFind function
    # Filtered lines are also found.
    #
    # The seach string must match exactly with the whole cell. Parts of the string are not found.
    # VB2PY (UntranslatedCode) On Error GoTo Is_Sil_Sheet
    _fn_return_value = P01.Application.WorksheetFunction.Match(SeachStr, r, 0)
    if _fn_return_value > 0:
        if r(_fn_return_value, 1) != SeachStr:
            # Same case ?
            if _fn_return_value < r.Count:
                Offset = Offset + _fn_return_value
                r = P01.Application.Intersect(r.Offset(_fn_return_value), r)
                _fn_return_value = 0
            else:
                _fn_return_value = 0
    if _fn_return_value > 0:
        _fn_return_value = _fn_return_value + Offset
    return _fn_return_value

def WorksheetExists(SheetName):
    _fn_return_value = None
    TempSheetName = String()

    # 15.02.23: Juergen
    #----------------------------------------------------------------------
    TempSheetName = UCase(SheetName)
    for Sheet in PG.ThisWorkbook.sheets:
        if TempSheetName == UCase(Sheet.Name):
            _fn_return_value = True
            return _fn_return_value
    _fn_return_value = False
    return _fn_return_value

