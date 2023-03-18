from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M02_Main as M02a
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M30_Tools as M30
import pattgen.M06_Goto_Graph
import pattgen.M31_modKeyState

""" Values see above
------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------
--------------------------
-------------------------------------------------------
-----------------------------------------------------------------
 Anzeige im GoTo-Mode:
 ~~~~~~~~~~~~~~~~~~~~~
 Wenn der GoTo Mode aktiviert ist, und "Analoges Überblenden" = X ist,
 dann hängt das Bild von der GotoZeile (GoTo_Row) ab.
 Wenn die entsprechende Spalte angesprungen werden kann, dann hängt
 die Start Helligkeit von der ltzen Spalte ab. Zur darstellung werden
 zwei überlagerte Dreiecke verwendet. Das eine kommt von 0, das andere von 100%
 Folgende Einträge in der GoTo Tabelle markieren eine Spalte welche angesprungen
 werden kann:
  - Erste Spalte
  - 'S' = Startsplate
  - 'P' = Position für Goto

 Besonderheit:
 Wenn die vorangegangene Spalte ein 'E' enthält, und die aktuelle Spalte
 keine Startspalte ist, dann kann sie nicht angesprungen werden.
 => Hier wird nichts angezeigt
-------------------------------------------------------------
---------------------------------------
--------------------------------------------------
--------------------------------------------------------------------------------------------------------
----------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on 1
--------------------------------------
--------------------------------------
UT------------------------------------------
------------------------------------
--------------------------------------------------------------------
--------------------------------------
"""

Is_Reachable = 1
Is_Goto1_Col = 2
Is_Start_Col = 10
Reachable_Col = vbObjectInitialize(objtype=Integer)
Came_From_Col = vbObjectInitialize(objtype=Integer)
PosColArray = vbObjectInitialize(objtype=Long)
PosList = String()
Debug_Reachable = False

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: h1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: h2 - ByVal 
def Draw_Analog_Trend(c, h1, h2, rgb, Transparency=0.5):
    X1 = Double()

    y0 = Double()

    X2 = Double()

    Y1 = Double()

    Y2 = Double()
    #------------------------------------------------------------------------------------------------------------------------------------
    if h1 == 0 and h2 == 0:
        return
    _with14 = c
    if h1 == h2:
        if h1 * _with14.Height < 1:
            h1 = 1 / _with14.Height
        # Make small rects visible
        if h2 * _with14.Height < 1:
            h2 = 1 / _with14.Height
    else:
        if h1 > h2:
            if h1 * _with14.Height < 1:
                h1 = 1 / _with14.Height
            # Make small triangles visible
        else:
            if h2 * _with14.Height < 1:
                h2 = 1 / _with14.Height
    X1 = _with14.Left
    y0 = _with14.Top + _with14.Height
    X2 = _with14.Left + _with14.Width
    Y1 = _with14.Top + _with14.Height *  ( 1 - h2 )
    Y2 = _with14.Top + _with14.Height *  ( 1 - h1 )
    _with15 = X02.ActiveSheet.Shapes.BuildFreeform(X01.msoEditingAuto, X1, y0)
    _with15.AddNodes(X01.msoSegmentLine, X01.msoEditingAuto, X2, y0)
    _with15.AddNodes(X01.msoSegmentLine, X01.msoEditingAuto, X2, Y1)
    _with15.AddNodes(X01.msoSegmentLine, X01.msoEditingAuto, X1, Y2)
    _with15.ConvertToShape().Select()
    _with16 = X02.Selection.ShapeRange
    _with16.Line.Visible = X01.msoFalse
    _with16.Name = 'Analog_Trend'
    _with17 = _with16.Fill
    _with17.ForeColor.rgb = rgb
    _with17.Transparency = Transparency
    X02.Selection.OnAction = '\'Click_TrendGrafik "' + str(c.Row) + ' ' + str(c.Column) + '"\''
    # To be able to move the cursor to the selected cell

def Get_Avg_LED_Raw(r, MaxVal):
    _fn_return_value = None
    c = Variant()

    Val = Double()
    #--------------------------------------------------------------------------
    for c in r:
        Val = Val + M02a.Get_LED_Val(c, MaxVal)
    _fn_return_value = Val / r.Count
    return _fn_return_value

def Check_WertMinMaxValid():
    #--------------------------
    if X02.ActiveSheet.Name != M01.WertMinMaxValid:
        M01.WertMinMaxValid = X02.ActiveSheet.Name
        if X02.Range(M01.BitsVal_Rng) < 8:
            M01.WertMin = int(X02.Range(M01.WertMin_Rng))
            M01.WertMax = int(X02.Range(M01.WertMax_Rng))
        else:
            # If 8 bits are used WertMin and WertMax are not used
            M01.WertMin = 0
            M01.WertMax = 255
        M01.BitsVal = ( 2 ** X02.Range(M01.BitsVal_Rng) )  - 1
        M01.LED_Scale = ( M01.WertMax - M01.WertMin )  / M01.BitsVal
        M01.LED_Offset = M01.WertMin
        M01.StartMax = M01.WertMax / 255
        M01.StartMin = M01.WertMin / 255

def Get_Avg_LED_Val(r):
    _fn_return_value = None
    #-------------------------------------------------------
    _fn_return_value = Get_Avg_LED_Raw(r, M01.BitsVal) * M01.LED_Scale + M01.LED_Offset
    return _fn_return_value

def Color_to_RGBColor(colorVal):
    _fn_return_value = None
    #-----------------------------------------------------------------
    # Convert a color given as a long number to a MsoRGBType
    _fn_return_value = rgb(( colorVal % 256 ), ( ( colorVal // 256 )  % 256 ), ( colorVal // 65536 ))
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: c - ByVal 
def Get_Number_from_Str(c):
    _fn_return_value = None
    NrStr = String()

    i = Long()
    #-------------------------------------------------------------
    for i in vbForRange(1, Len(c)):
        if IsNumeric(Mid(c, i, 1)):
            NrStr = NrStr + Mid(c, i, 1)
        else:
            if NrStr != '':
                break
            # First not numeric character after prior numeric characters
    if NrStr == '':
        _fn_return_value = - 1
    else:
        _fn_return_value = Val(NrStr)
    return _fn_return_value

def Update_Following(r):
    global Reachable_Col
    c = Variant()

    Val = String()
    #---------------------------------------
    for c in r:
        Val = UCase(c.offset(0, - 1))
        if Reachable_Col(c.Column - M01.GoTo_Col1) > 0 or InStr(Val, 'G') > 0 or InStr(Val, 'E') > 0:
            break
        Reachable_Col[c.Column - M01.GoTo_Col1] = Is_Reachable
        ## VB2PY (CheckDirective) VB directive took path 2 on Debug_Reachable

def Calc_Reachable_Columns():
    global Reachable_Col, PosList, PosColArray, Came_From_Col
    _fn_return_value = None
    c = Variant()

    LastCol = Long()

    i = Long()

    #*HL GotoCells = X02.Range()

    Val = String()

    PosCnt = Long()

    FirstLEDsRow = Long()

    LastLEDsRow = Long()

    LastLEDsCol = Long()

    ArraySize = Long()

    Updated = Boolean()
    #--------------------------------------------------
    # Generate an array which contains marks for all reachable columns
    # A column is reachable if
    # - it's the first column
    # - it's marked with 'S' = Startcolumn
    # - prior columns are reachable and don't contain an 'G'= Goto or 'E' = End
    # - it contains a 'P' which is reached from a reachable column
    # Returns True if array Reachable_Col id valid
    FirstLEDsRow = X02.Range(M01.FirstLEDTabRANGE).Row
    LastLEDsRow = FirstLEDsRow + int(X02.Range(M01.LED_Cnt_Rng)) - 1 #*HL
    #LastLEDsCol = LastFilledColumn(Range(LEDsRANGE), LastLEDsRow)
    # Find the last used column
    LastLEDsCol = M30.LastFilledColumn2(X02.Range(M01.LEDsRANGE), LastLEDsRow)
    # Find the last used column  20.11.19: Faster function
    LastCol = M30.LastUsedColumnInRow(X02.ActiveSheet, M01.GoTo_Row)
    if LastLEDsCol > LastCol:
        LastCol = LastLEDsCol
    ArraySize = LastCol - M01.GoTo_Col1 + 1
    if ArraySize <= 0:
        return _fn_return_value
    Reachable_Col = vbObjectInitialize((ArraySize,), Variant)
    Came_From_Col = vbObjectInitialize((ArraySize,), Variant)
    if not pattgen.M06_Goto_Graph.Goto_Mode_is_Active():
        for i in vbForRange(0, ArraySize):
            Reachable_Col[i] = Is_Reachable
        _fn_return_value = True
        return _fn_return_value
    ## VB2PY (CheckDirective) VB directive took path 2 on Debug_Reachable
    PosList = ' '
    GotoCells = X02.Range(X02.Cells(M01.GoTo_Row, M01.GoTo_Col1), X02.Cells(M01.GoTo_Row, LastCol))
    for c in GotoCells:
        Val = UCase(c)
        if InStr(Val, 'P') > 0:
            PosColArray = vbObjectInitialize((PosCnt + 1,), Variant, PosColArray)
            PosColArray[PosCnt] = c.Column
            PosCnt = PosCnt + 1
            PosList = PosList + str(PosCnt) + ' '
        if i == 0 or InStr(Val, 'S') > 0:
            Reachable_Col[i] = Is_Start_Col
        else:
            PriorGotoVal = UCase(X02.Cells(M01.GoTo_Row, c.Column - 1))
            if Reachable_Col(i - 1) > 0:
                if InStr(PriorGotoVal, 'G') == 0 and InStr(PriorGotoVal, 'E') == 0:
                    Reachable_Col[i] = Is_Reachable
        ## VB2PY (CheckDirective) VB directive took path 2 on Debug_Reachable
        i = i + 1
    # Check the goto entries
    while 1:
        i = 0
        Updated = False
        for c in GotoCells:
            Val = UCase(c)
            if Reachable_Col(i) > 0:
                if InStr(Val, 'G') > 0:
                    p = Get_Number_from_Str(Val)
                    if p > 0 and InStr(PosList, ' ' + str(p) + ' ') > 0:
                        ArrayPos = PosColArray(p - 1) - M01.GoTo_Col1
                        if Reachable_Col(ArrayPos) == 0:
                            Updated = True
                            if PosColArray(p - 1) + 1 <= LastCol:
                                # Other columns following ?
                                Update_Following(X02.Range(X02.Cells(M01.GoTo_Row, PosColArray(p - 1) + 1), X02.Cells(M01.GoTo_Row, LastCol)))
                            Reachable_Col[ArrayPos] = Is_Goto1_Col
                            Came_From_Col[ArrayPos] = c.Column
                            ## VB2PY (CheckDirective) VB directive took path 2 on Debug_Reachable
                        else:
                            # Was reachable before
                            if Came_From_Col(ArrayPos) != c.Column:
                                Reachable_Col[ArrayPos] = Is_Start_Col
                                ## VB2PY (CheckDirective) VB directive took path 2 on Debug_Reachable
            i = i + 1
        if Updated == False:
            break
    ## VB2PY (CheckDirective) VB directive took path 2 on Debug_Reachable
    _fn_return_value = True
    return _fn_return_value

def Draw_GotoMode_Symbol(cc, LastVAl, ActVal, rgb_col):
    ArrayPos = Long()

    Val = Long()

    CameFrom_R = X02.Range()
    #--------------------------------------------------------------------------------------------------------
    ArrayPos = cc.Column - M01.GoTo_Col1
    _select5 = Reachable_Col(ArrayPos)
    if (_select5 == Is_Start_Col):
        Draw_Analog_Trend(cc, M01.StartMin, ActVal / 255, rgb_col)
        Draw_Analog_Trend(cc, M01.StartMax, ActVal / 255, rgb_col, M01.Transp_Start_Graph)
    elif (_select5 == Is_Goto1_Col):
        CameFrom_R = X02.Range(X02.Cells(cc.Row, Came_From_Col(ArrayPos)), X02.Cells(cc.Row + cc.Rows.Count - 1, Came_From_Col(ArrayPos)))
        #CameFrom_R.Select
        # Debug
        Val = Get_Avg_LED_Val(CameFrom_R)
        Draw_Analog_Trend(cc, Val / 255, ActVal / 255, rgb_col)
    else:
        Draw_Analog_Trend(cc, LastVAl / 255, ActVal / 255, rgb_col)

def Line_Analog_Trend(r):
    c = Variant()

    rgb_col = X01.MsoRGBType()

    ActVal = Double()

    LastVAl = Double()

    LastRow = Long()

    LastCol = Long()

    AnaFade = Integer()

    GotoMod = Boolean()
    #----------------------------------------
    # Generate a analog trend picture for the given range.
    # The picture is a rectangle, a triangle or a one sided trapeze.
    # The range could be one row or several rows.
    # If several rows are given the average value of one column is used.
    # Uses the fill color of the left cell next to the given range
    # or yellow if the cell is not filled.
    _with18 = X02.Cells(r.Row, r.Column - 1)
    # Read the interior color
    if _with18.Interior.Color != 16777215:
        rgb_col = Color_to_RGBColor(_with18.Interior.Color)
    else:
        rgb_col = rgb(220, 220, 0)
        # Yellow
        # 28.11.19: Old: 255, 255, 0
    Check_WertMinMaxValid()
    # Make sure that the constants WertMin, WertMax, BitsVal, LED_Scale, LED_Offset are valid
    LastRow = r.Rows.Count - 1
    LastCol = r.Columns.Count - 1
    LastVAl = Get_Avg_LED_Val(X02.Range(X02.Cells(r.Row, r.Column + LastCol), X02.Cells(r.Row + LastRow, r.Column + LastCol)))
    _select6 = UCase(X02.Range(M01.AnaFade_Rng))
    if (_select6 == '1'):
        AnaFade = 1
    elif (_select6 == 'X'):
        AnaFade = 2
    GotoMod = pattgen.M06_Goto_Graph.Goto_Mode_is_Active()
    for c in r:
        if c.Row == r.Row:
            # All Cells in the column
            cc = X02.Range(c, c.offset(LastRow, 0))
            ActVal = Get_Avg_LED_Val(cc)
            if c.Column - M01.GoTo_Col1 >= 0:
                # 25.6.19:
                if Reachable_Col(c.Column - M01.GoTo_Col1) > 0:
                    if GotoMod and AnaFade == 2:
                        Draw_GotoMode_Symbol(cc, LastVAl, ActVal, rgb_col)
                    else:
                        if AnaFade == 0:
                            LastVAl = ActVal
                        Draw_Analog_Trend(cc, LastVAl / 255.0, ActVal / 255.0, rgb_col)
            LastVAl = ActVal

def IsLEDGroup():
    _fn_return_value = None
    #--------------------------------------
    _fn_return_value = X02.ActiveSheet.RGB_LED_CheckBox.Value
    return _fn_return_value

def Draw_Analog_Trend_of_Sheet():
    WasProtected = Boolean()

    Oldupdating = Boolean()

    LastSel = Variant()

    FirstLEDsRow = Long()

    FirstLEDsCol = Long()

    LastLEDsRow = Long()

    LastLEDsCol = Long()

    Row = Long()
    #--------------------------------------
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    LastSel = X02.Selection
    # 21.11.19: Old: ActiveCell
    Oldupdating = X02.Application.ScreenUpdating
    X02.Application.ScreenUpdating = False
    M01.WertMinMaxValid = ''
    # To read WertMin and WertMax, ... from the sheet again
    FirstLEDsRow = X02.Range(M01.FirstLEDTabRANGE).Row
    FirstLEDsCol = X02.Range(M01.FirstLEDTabRANGE).Column + 1
    LastLEDsRow = FirstLEDsRow + int(X02.Range(M01.LED_Cnt_Rng)) - 1 #*HL
    #LastLEDsCol = LastFilledColumn(Range(LEDsRANGE), LastLEDsRow)
    # Find the last used column
    LastLEDsCol = M30.LastFilledColumn2(X02.Range(M01.LEDsRANGE), LastLEDsRow)
    # Find the last used column  20.11.19: Faster function
    Del_Analog_Trend_Objects()
    if LastLEDsCol > 0:
        # Is anything entered in the LEDs table ?
        if Calc_Reachable_Columns():
            New_Row=0
            for Row in vbForRange(FirstLEDsRow, LastLEDsRow):
                if New_Row<Row:
                    if ( Row - FirstLEDsRow )  % 3 == 0 and IsLEDGroup():
                        # 13.06.20: Old: IsLEDGroup(Row)
                        Line_Analog_Trend(X02.Range(X02.Cells(Row, FirstLEDsCol), X02.Cells(Row + 2, LastLEDsCol)))
                        New_Row = Row + 2
                    else:
                        Line_Analog_Trend(X02.Range(X02.Cells(Row, FirstLEDsCol), X02.Cells(Row, LastLEDsCol)))
    X02.Application.ScreenUpdating = Oldupdating
    # VB2PY (UntranslatedCode) On Error Resume Next
    LastSel.Select()
    # Could cause an error if the last selection is a drawing object and nor a cell
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if WasProtected:
        M30.Protect_Active_Sheet()

def Test_Draw_Analog_Trend_of_Sheet():
    Start = Variant()
    #UT------------------------------------------
    Start = Timer()
    Draw_Analog_Trend_of_Sheet()
    Debug.Print('Duration: ' + Round(Timer() - Start, 2))

def Del_Analog_Trend_Objects():
    WasProtected = Boolean()

    o = Variant()
    #------------------------------------
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    for o in X02.ActiveSheet.Shapes:
        if o.Type == X01.msoFreeform and Left(o.Name, Len('Analog_Trend')) == 'Analog_Trend':
            o.Delete()
    if WasProtected:
        M30.Protect_Active_Sheet()

def Update_Grafik(EnableAutomatics=True):
    #--------------------------------------------------------------------
    # Is called if the "Aktualisieren" Button is pressed or the RGB LED checkbox is changed
    if EnableAutomatics:
        M30.Enable_Application_Automatics()
    # In case it was disabled prior due to a bug  13.06.20: Added "EnableAutomatics" because otherwise the screenoupdating is enabled if an example is loaded where "RGB LED" is activ
    if pattgen.M31_modKeyState.IsAltKeyDown():
        M02a.Update_Grafik_from_Str('')
    else:
        if X02.Range(M01.GrafDsp_Rng) != '':
            M02a.Update_Grafik_from_Str(X02.Range(M01.GrafDsp_Rng))
        else:
            M02a.Update_Grafik_from_Str('1')

def Click_TrendGrafik(Txt):
    Par = vbObjectInitialize(objtype=String)
    #--------------------------------------
    # This function is called if the user clics to the trend grafic if the sheet is protected
    # Since the Grafic overlaps the cell there is no oter way to select the cell with the mouse
    Par = Split(Txt, ' ')
    X02.Cells(Val(Par(0)), Val(Par(1))).Select()

# VB2PY (UntranslatedCode) Option Explicit
