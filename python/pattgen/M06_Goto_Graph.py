from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import ExcelAPI.XLC_Excel_Consts as XLC
import pattgen.M30_Tools as M30
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M03_Analog_Trend
import pattgen.M05_Goto_Gr_Calc_Height
import mlpyproggen.Pattern_Generator as PG

""" Number of Goto start points which is updated when Draw_All_Arrows is called
-----------------------------
------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------
UT------------------------------
----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------
---------------------------------------------------------------
UT-------------------------------
-------------------------------------------------------------------
-----------------------------------------------
---------------------------
-------------------------------------
--------------------------------------------------------------------------------------------------
UT-----------------------------------
------------------------------------------
-------------------------------------------------------
UT-------------------------------------------
---------------------------------------------------
--------------------------------------------------
"""
guifactor = 1 #XLC.xlvp2py_guifactor
Goto_Start_Points = Long()

def Delete_Goto_Graph():
    WasProtected = Boolean()

    o = Variant()
    #-----------------------------
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    for o in X02.ActiveSheet.Shapes:
        if Left(o.Name, Len('Goto_Graph')) == 'Goto_Graph':
            o.Delete()
    if WasProtected:
        M30.Protect_Active_Sheet()

def Draw_GotoArrowXY(X1, X2, y, h, Color):
    o = Variant()
    #------------------------------------------------------------------------------------------------------
    # Draw a curved arrow from x1, y to x2, y.
    # h defines the height. Positive numbers draw the arrow below y, negative above y
    # http://www.herber.de/mailing/vb/html/xlobjfreeformbuilder.htm
    _with8 = X02.ActiveSheet
    _with9 = _with8.Shapes.BuildFreeform(XLC.msoEditingCorner, X1, y)
    # Startpunkt
    #                                             Richt1   Richt2    Ende
    _with9.AddNodes(XLC.msoSegmentCurve, XLC.msoEditingCorner, X1, y, ( X1 + X2 )  / 2, y + 2 * h, X2, y)
    o = _with9.ConvertToShape()
    #.Shapes (.Shapes.Count)
    # Debug
    _with10 = o
    _with11 = _with10.Line
    _with11.EndArrowheadStyle = XLC.msoArrowheadTriangle
    _with11.ForeColor.rgb = Color
    _with10.Name = 'Goto_Graph_CurvedArrow' + str(X02.ActiveSheet.Shapes.Count())

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: r1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: r2 - ByVal 
def Draw_GotoArrow(r1, r2, h, Color):
    #-----------------------------------------------------------------------------------------
    if r1 != r2:
        Draw_GotoArrowXY(r1.Left + r1.Width * 0.5, r2.Left + r2.Width * 0.5, r1.Top + r1.Height, h, Color)
    else:
        Draw_GotoArrowXY(r1.Left + r1.Width * 0.3, r2.Left + r2.Width * 0.7, r1.Top + r1.Height, h, rgb(255, 0, 0))

def Test_Draw_GotoArrow():
    #UT------------------------------
    #Delete_Goto_Graph
    #Draw_GotoArrowXY 100, 200, 100, 50, rgb(255, 0, 0)
    Draw_GotoArrow(X02.ActiveCell(), X02.ActiveCell().offset(0, 2), 60, rgb(0, 0, 255))

def Draw_StraitArrow(r, Txt, h, dx, Dir, Color):
    
    tdx = - 10*guifactor

    tdy = - 16*guifactor

    th = 72*guifactor

    x = Double()

    y = Double()

    x0 = Double()

    y0 = Double()

    o = Variant()
    #----------------------------------------------------------------------------------------------------------------------
    if Dir == 1:
        x = r.Left + r.Width * 0.3
    else:
        x = r.Left + r.Width * 0.7
    y = r.Top
    x0 = x - dx
    y0 = y - h
    _with12 = X02.ActiveSheet.Shapes.AddConnector(XLC.msoConnectorStraight, x0, y0, x, y)
    if Dir == 1:
        _with12.Line.EndArrowheadStyle = XLC.msoArrowheadStealth
        # Other type: msoArrowheadTriangle
    else:
        _with12.Line.BeginArrowheadStyle = XLC.msoArrowheadStealth
        # Other type: msoArrowheadOval
    _with12.Line.ForeColor.rgb = Color
    _with12.Name = 'Goto_Graph_Arrow' + str(X02.ActiveSheet.Shapes.Count())
    _with13 = X02.ActiveSheet.Shapes.AddLabel(XLC.msoTextOrientationHorizontal, x0 + tdx, y0 + tdy, 40*guifactor, th)
    _with13.TextFrame2.TextRange.Characters.Text = Txt
    _with13.Name = 'Goto_Graph_Label' + str(X02.ActiveSheet.Shapes.Count())

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: r - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByVal 
def Draw_StartArrow(r, Txt):
    #-----------------------------------------------------------------
    Draw_StraitArrow(r, Txt, 30*guifactor, 10*guifactor, 1, rgb(0, 128, 0))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: r - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByVal 
def Draw_EndArrow(r, Txt):
    #---------------------------------------------------------------
    Draw_StraitArrow(r, Txt, 17*guifactor, - 10*guifactor, - 1, rgb(128, 0, 0))

def Test_Draw_StartArrow():
    #UT-------------------------------
    Delete_Goto_Graph()
    Draw_StartArrow(X02.ActiveCell(), '7')
    Draw_EndArrow(X02.ActiveCell(), 'E')
    X02.ActiveCell().Select()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: GotoArrowTab - ByVal 
def Draw_GotoArrowTab(GotoArrowTab, LastCol):
    MaxH = Double()

    GNr = Long()

    ArrowTabEntry = Variant()

    ArrTabArr = vbObjectInitialize(objtype=String)
    #-------------------------------------------------------------------
    # Draw the Goto arrows
    MaxH = X02.Cells(M01.GoTo_Row + 1, 1).Height * 0.8 * 0.5 #*HL
    ArrTabArr = Split(GotoArrowTab, ' ')
    for ArrowTabEntry in ArrTabArr:
        Cols = Split(ArrowTabEntry, ',')
        GNr = GNr + 1
        if UBound(Cols) == 2:
            # Three parameters given ?
            h = MaxH * int(Cols(2))
        else:
            h = MaxH * GNr /  ( UBound(ArrTabArr) + 1 )
            # Old format without height
        if Val(Cols(1)) <= LastCol:
            # Inside the valid range ?
            Color = rgb(0, 0, 255)
            # Blue
        else:
            Color = rgb(255, 153, 0)
            # Orange
        Draw_GotoArrow(X02.Cells(M01.GoTo_Row, Val(Cols(0))), X02.Cells(M01.GoTo_Row, Val(Cols(1))), h, Color)

def Goto_Mode_is_Active():
    _fn_return_value = None
    #-----------------------------------------------
    _fn_return_value = PG.ThisWorkbook.ActiveSheet.Range('Goto_Mode') == '1'
    return _fn_return_value

def Draw_All_Arrows():
    global Goto_Start_Points
    WasProtected = Boolean()

    OldScrUpd = Boolean()

    LastCol = Long()

    c = Variant()

    V = String()

    SNr = Long()

    GotoArrowTab = String()

    LastLEDsCol = Long()

    LastLEDsRow = Long()

    FirstLEDsRow = Long()
    #---------------------------
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    OldScrUpd = X02.Application.ScreenUpdating
    X02.Application.ScreenUpdating = False
    Delete_Goto_Graph()
    Goto_Start_Points = 0
    if Goto_Mode_is_Active() == False:
        return
    pattgen.M03_Analog_Trend.Calc_Reachable_Columns()
    ## VB2PY (CheckDirective) VB2PY Python directive
    FirstLEDsRow = X02.Range(M01.FirstLEDTabRANGE).Row
    LastLEDsRow = FirstLEDsRow + X02.Range(M01.LED_Cnt_Rng) - 1
    #LastLEDsCol = LastFilledColumn(Range(LEDsRANGE), LastLEDsRow)
    # Find the last used column
    LastLEDsCol = M30.LastFilledColumn2(X02.Range(M01.LEDsRANGE), LastLEDsRow)
    # Find the last used column  20.11.19: Faster function
    LastCol = M30.LastUsedColumnInRow(X02.ActiveSheet, M01.GoTo_Row)
    if LastLEDsCol > LastCol:
        LastCol = LastLEDsCol
    if LastCol >= M01.GoTo_Col1:
        GotoCells = X02.Range(X02.Cells(M01.GoTo_Row, M01.GoTo_Col1), X02.Cells(M01.GoTo_Row, LastCol))
        for c in GotoCells:
            V = UCase(c)
            if SNr == 0 or InStr(V, 'S') > 0:
                Draw_StartArrow(c, SNr)
                SNr = SNr + 1
            Goto_Start_Points = SNr
            if InStr(V, 'E') > 0 and pattgen.M03_Analog_Trend.Reachable_Col(c.Column - M01.GoTo_Col1) > 0:
                Draw_EndArrow(c, 'E')
            # Fill the GotoArrowTab list
            if InStr(V, 'G') > 0 and pattgen.M03_Analog_Trend.Reachable_Col(c.Column - M01.GoTo_Col1) > 0:
                p = pattgen.M03_Analog_Trend.Get_Number_from_Str(V)
                if p > 0:
                    if InStr(pattgen.M03_Analog_Trend.PosList, ' ' + str(p) + ' ') > 0:
                        GotoArrowTab = GotoArrowTab + str(c.Column) + ',' + str(pattgen.M03_Analog_Trend.PosColArray(p - 1)) + ' '
                    else:
                        GotoArrowTab = GotoArrowTab + str(c.Column) + ',' + str(LastCol) + 1 + ' '
        # Draw the Goto arrows
        if GotoArrowTab != '':
            List_w_Height = pattgen.M05_Goto_Gr_Calc_Height.Calc_Height_GotoArrow(Left(GotoArrowTab, Len(GotoArrowTab) - 1))
            Draw_GotoArrowTab(List_w_Height, LastCol)
    if WasProtected:
        M30.Protect_Active_Sheet()
    X02.Application.ScreenUpdating = OldScrUpd

def Move_Add_Del_Col_Buttons():
    o = Variant()

    y = Double()
    # 20.11.19:
    #-------------------------------------
    # The buttons have to be moved if the height of the column is changed
    y = X02.Rows(M01.GoTo_Row + 1).Top + X02.Rows(M01.GoTo_Row + 1).Height
    for o in X02.ActiveSheet.Shapes.getlist(): #*HL
        if o.AlternativeText == 'Add_Del_Button':
            o.Top = y - o.Height - 2

def Hide_Show_GotoLines(Hide, Resize_And_Move_Buttons=True):
    #--------------------------------------------------------------------------------------------------
    if X02.Rows(str(M01.GoTo_Row) + ':' + str(M01.GoTo_Row)).EntireRow.Hidden != Hide: #*HL
        # 25.06.19: Old: "& GoTo_Row + 1"
        WasProtected = X02.ActiveSheet.ProtectContents
        if WasProtected:
            X02.ActiveSheet.Unprotect()
        X02.Rows(str(M01.GoTo_Row) + ':' + str(M01.GoTo_Row)).EntireRow.Hidden = Hide #*HL
        # 25.06.19: Don't hide "Bitte Tabelle ausfüllen..." line Old: "& GoTo_Row + 1"
        if Resize_And_Move_Buttons:
            if Hide:
                X02.RowDict[M01.GoTo_Row - 1].RowHeight = 12
                X02.RowDict[M01.GoTo_Row + 1].RowHeight = 15
            else:
                X02.RowDict[M01.GoTo_Row - 1].RowHeight = 60
                X02.RowDict[M01.GoTo_Row + 1].RowHeight = 60
            Move_Add_Del_Col_Buttons()
        if WasProtected:
            M30.Protect_Active_Sheet()

def Test_Hide_Show_GotoLines():
    #UT-----------------------------------
    Hide_Show_GotoLines(not X02.Rows(M01.GoTo_Row + ':' + M01.GoTo_Row + 1).EntireRow.Hidden)

def Hide_Show_GotoLines_If_Enabled():
    #------------------------------------------
    Hide_Show_GotoLines(not Goto_Mode_is_Active())

def Hide_Show_Special_ModeLines(Hide):
    # 29.12.19:
    #-------------------------------------------------------
    if X02.Range('RGB_Modul_Nr').EntireRow.Hidden != Hide:
        WasProtected = X02.ActiveSheet.ProtectContents
        if WasProtected:
            X02.ActiveSheet.Unprotect()
        X02.Range(X02.Range('RGB_Modul_Nr'), X02.Range('Analog_Inputs')).EntireRow.Hidden = Hide #*HL
        #X02.ActiveSheet.Send2Module_Button.Visible = not Hide
        #X02.ActiveSheet.Send2Module_Button.Enabled = not Hide
        #X02.ActiveSheet.Prog_Generator_Button.Visible = Hide
        #X02.ActiveSheet.Prog_Generator_Button.Enabled = Hide
        if WasProtected:
            M30.Protect_Active_Sheet()

def Test_Hide_Show_Special_ModeLines():
    # 29.12.19:
    #UT-------------------------------------------
    Hide_Show_Special_ModeLines(not X02.Range('RGB_Modul_Nr').EntireRow.Hidden)

def Special_Mode_is_Active():
    _fn_return_value = None
    Special_Mode = String()

    OldEvents = Boolean()
    # 29.12.19:
    #---------------------------------------------------
    Special_Mode = PG.ThisWorkbook.ActiveSheet.Range('Special_Mode')
    OldEvents = X02.Application.EnableEvents
    X02.Application.EnableEvents = False
    _select4 = UCase(Left(Special_Mode, 1))
    if (_select4 == 'C'):
        # Charliplexing
        if Left(Special_Mode, Len('Charlieplexing')) != 'Charlieplexing':
            PG.ThisWorkbook.ActiveSheet.RangeDict['Special_Mode'] = 'Charlieplexing V2'
            # Correct the active cell. It shold be the next line and not the line after the hidden range
            if X02.ActiveCell().Address == X02.Range('Analog_Inputs').offset(1, 0).Address:
                X02.Range('Special_Mode').offset(1, 0).Select()
        _fn_return_value = True
    X02.Application.EnableEvents = OldEvents
    return _fn_return_value

def Hide_Show_Special_ModeLines_If_Enabled():
    # 29.12.19:
    #--------------------------------------------------
    Hide_Show_Special_ModeLines(not Special_Mode_is_Active())
    #  If Not Special_Mode_is_Active() Then
    # Prevent that a hidden cell is selected
    #     If ActiveCell.Address = Range("RGB_Modul_Nr").Address Then Range("Analog_Inputs").offset(1, 0).Select
    #  End If

# VB2PY (UntranslatedCode) Option Explicit
