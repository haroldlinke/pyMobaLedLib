from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M01_Public_Constants_a_Var as M01
import ExcelAPI.XLA_Application as X02
import pattgen.M30_Tools as M30
import pattgen.M09_Language

"""-----------------------------------------------------------------------------------------------
------------------------------------------
UT------------------------
------------------------------
"""


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: FirstEmptyCol - ByRef 
def Get_Duration(c, FirstEmptyCol, Values):
    _fn_return_value = None
    #-----------------------------------------------------------------------------------------------
    if c.Value == '':
        if FirstEmptyCol == 0:
            FirstEmptyCol = c.Column
        _fn_return_value = Values(( c.Column - FirstEmptyCol )  %  ( FirstEmptyCol - M01.Dauer_Col1 ))
    else:
        s = c.Value
        V = Val(s)
        if InStr(s, 'Sec') > 0 or InStr(s, 'Sek') > 0 or InStr(s, 'sec') > 0 or InStr(s, 'sek') > 0:
            V = V * 1000
        elif InStr(s, 'Min') > 0:
            V = V * 60 * 1000
        _fn_return_value = V
    return _fn_return_value, FirstEmptyCol #*HL ByRef

def Adjust_Column_With_to_Duration():
    FirstLEDsRow = Long()

    LastLEDsRow = Long()

    LastLEDsCol = Long()

    Col = Long()

    ms = Long()

    Min_t = Long()

    Max_t = Long()

    Values = vbObjectInitialize(objtype=Long)

    i = Long()

    FirstEmptyCol = Long()

    WasProtected = Boolean()

    Min_Width = Double()

    Max_width = Double()

    Max2Min = Double()

    ScaleF = Double()

    MessageShown = Boolean()
    #------------------------------------------
    FirstLEDsRow = X02.Range(M01.FirstLEDTabRANGE).Row
    LastLEDsRow = FirstLEDsRow + int(X02.Range(M01.LED_Cnt_Rng)) - 1
    #LastLEDsCol = LastFilledColumn(Range(LEDsRANGE), LastLEDsRow)
    # Find the last used column
    LastLEDsCol = M30.LastFilledColumn2(X02.Range(M01.LEDsRANGE), LastLEDsRow)
    # Find the last used column  20.11.19: Faster function
    if LastLEDsCol > M01.Dauer_Col1:
        # Prevent problem if noting is marked in the LEDs area
        # 25.12.19:
        Values = vbObjectInitialize((LastLEDsCol - M01.Dauer_Col1,), Variant)
        Min_t = 999999
        for Col in vbForRange(M01.Dauer_Col1, LastLEDsCol):
            _with35 = X02.Cells(M01.Dauer_Row, Col)
            ms, FirstEmptyCol = Get_Duration(X02.Cells(M01.Dauer_Row, Col), FirstEmptyCol, Values)
            Values[i] = ms
            i = i + 1
            if ms > Max_t:
                Max_t = ms
            if ms < Min_t:
                Min_t = ms
    if Max_t == Min_t:
        Normal_Column_With()
        return
    if Min_t == 0:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Error in function \'Adjust_Column_With_to_Duration\' ;-('))
        Normal_Column_With()
        return
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    #Debug.Print "Max_t / Min_t =  " & Max_t / Min_t 'Debug
    Max2Min = Max_t / Min_t
    if Max2Min < M01.NormWidth_MM:
        Min_Width = M01.NormColWidth
    elif Max2Min > M01.Min_Width_MM:
        Min_Width = M01.Min_ColWidth
    else:
        m = ( M01.NormColWidth - M01.Min_ColWidth )  /  ( M01.NormWidth_MM - M01.Min_Width_MM )
        B = M01.NormColWidth - m * M01.NormWidth_MM
        Min_Width = m * Max2Min + B
    Max_width = Min_Width * Max_t / Min_t
    ScaleF = ( Max_width - Min_Width )  /  ( Max_t - Min_t )
    X02.Application.StatusBar = ''
    i = 0
    for Col in vbForRange(M01.Dauer_Col1, LastLEDsCol):
        _with36 = X02.Cells(M01.Dauer_Row, Col)
        ms = Values(i)
        i = i + 1
        w = ( ms - Min_t )  * ScaleF + Min_Width
        if w > 100:
            w = 100
            # Maximal width in excel is limmited to 255
            if not MessageShown:
                X02.Application.StatusBar = pattgen.M09_Language.Get_Language_Str('Achtung die Darstellung der Spaltenbreite wurde begrenzt')
            MessageShown = True
        _with36.ColumnWidth = w
    if not MessageShown:
        if X02.Application.StatusBar == pattgen.M09_Language.Get_Language_Str('Achtung die Darstellung der Spaltenbreite wurde begrenzt'):
            X02.Application.StatusBar = ''
    if WasProtected:
        M30.Protect_Active_Sheet()

def Test_MaxWidth():
    i = Long()
    #UT------------------------
    _with37 = X02.Cells(1, 7)
    for i in vbForRange(250, 260):
        _with37.ColumnWidth = i

def Normal_Column_With():
    WasProtected = Boolean()

    FirstLEDsRow = Long()

    LastLEDsRow = Long()

    LastLEDsCol = Long()

    Col = Long()
    #------------------------------
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    FirstLEDsRow = X02.Range(M01.FirstLEDTabRANGE).Row
    LastLEDsRow = FirstLEDsRow + X02.Range(M01.LED_Cnt_Rng).Row - 1 #*HL
    #LastLEDsCol = LastFilledColumn(Range(LEDsRANGE), LastLEDsRow)
    # Find the last used column
    LastLEDsCol = M30.LastFilledColumn2(X02.Range(M01.LEDsRANGE), LastLEDsRow)
    # Find the last used column    20.11.19: Faster function
    for Col in vbForRange(M01.Dauer_Col1, LastLEDsCol):
        _with38 = X02.Cells(M01.Dauer_Row, Col)
        if _with38.ColumnWidth != M01.NormColWidth:
            _with38.ColumnWidth = M01.NormColWidth
    if WasProtected:
        M30.Protect_Active_Sheet()

# VB2PY (UntranslatedCode) Option Explicit
