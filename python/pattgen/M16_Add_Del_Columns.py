from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M09_Language
import pattgen.M30_Tools as M30
import pattgen.M02_Main as M02a

""" Probleme mit den Add / Del columns Buttons:
 22.11.19:
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Die Funktionen Add_Columns_to_Pattern() und Del_Columns_to_Pattern()
 Konnten im Goto Mode nur etwa 10 mal aufgerufen werden. Danach dauerte
 das Kopieren immer länger. Erst eine Sekunde, dann 3, dann 16, 32, ...
 Schuld war die "Src.Copy Dst" Zeile in Copy_Columns()
 Die Ausführung dauerte in der "GoTo_Row" bei jedem Aufruf länger ;-(
 Zusammen mit Armin haben wir herausgefunden, dass Excel die Bedingte
 Formatierung in der "Flash Bedarf:" Zelle versehentlich jedes mal
 kopiert (verdoppelt) hat. Das hat nach 2^n Aufrufen den Rechner ausgebremst.
 Verantwortlich dafür war vermutlich dass:
 - Die "Flash Bedarf:" Zelle aus zwei verbundenen Zellen Bestand (E42 & F43)
 - Die bedingte Formatierung sich versehentlich auf meherer Zellen (=$F$43;$E$42)
   bezugen hat. Die Zelle F43 ist die erste Zelle der Goto Tabelle.
 => Dieser Fehler hat mich vermutlich 6 Stunden gekostet ;-(
----------------------------------------------------------
----------------------------------------------------
---------------------------------------------
--------------------------------------------------------
-------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
----------------------------------
------------------------------------
"""

Add_Column_Message_Shown = Boolean()
Del_Column_Message_Shown = Boolean()

def Selection_in_Range(r):
    _fn_return_value = False
    isect = Variant()
    #----------------------------------------------------------
    # Check if the Selection is inside the range
    # VB2PY (UntranslatedCode) On Error GoTo WrongSelection
    isect = X02.Application.Intersect(r, X02.Selection)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if not isect is None:
        if isect.Column <= X02.Selection.Column:
            _fn_return_value = True
    return _fn_return_value

def Get_LEDs_Tab_Range_w_Head():
    _fn_return_value = None
    #----------------------------------------------------
    _fn_return_value = X02.Range(X02.Cells(M01.LEDsTAB_R - 1, M01.LEDsTAB_C), X02.Cells(M01.LEDsTAB_R + int(X02.Range('Kanaele')) - 1, M01.Last_LEDsCol))
    return _fn_return_value

def In_Pattern_Table():
    _fn_return_value = None
    #---------------------------------------------
    # Check if the Selection is inside the pattern table, the Duration line or goto line
    _fn_return_value = True
    if Selection_in_Range(Get_LEDs_Tab_Range_w_Head()):
        return _fn_return_value
    if Selection_in_Range(X02.Range(X02.Cells(M01.Dauer_Row, M01.Dauer_Col1), X02.Cells(M01.Dauer_Row, M01.Dauer_Col1 + M01.Dauer__Cnt - 1))):
        return _fn_return_value
    if Selection_in_Range(X02.Range(X02.Cells(M01.GoTo_Row, M01.GoTo_Col1), X02.Cells(M01.GoTo_Row, M01.Last_LEDsCol))):
        return _fn_return_value
    _fn_return_value = False
    return _fn_return_value

def Msg_if_not_in_Pattern_Table():
    _fn_return_value = None
    #--------------------------------------------------------
    if not In_Pattern_Table():
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Zum einfügen oder löschen von Spalten muss sich aktuelle Zelle innerhalb der Tabelle befinden.'), vbCritical, pattgen.M09_Language.Get_Language_Str('Cursor außerhalb der Tabelle'))
        _fn_return_value = True
        return _fn_return_value
    return _fn_return_value

def Copy_Columns(FirstRow, LastRow, SrcCol, DstCol, Cnt):
    #-------------------------------------------------------------------------------------------------------
    if Cnt > 0:
        LastCol = SrcCol + Cnt - 1
        Src = X02.Range(X02.Cells(FirstRow, SrcCol), X02.Cells(LastRow, LastCol))
        #Src.Select
        # Debug
        Dst = X02.Cells(FirstRow, DstCol)
        Src.Copy(Dst)

def Del_Columns(FirstRow, LastRow, StartCol, Cnt):
    #----------------------------------------------------------------------------------------
    if Cnt < 1:
        X02.MsgBox('Internal Error in Del_Columns(): Cnt < 1', vbCritical, 'Internal error')
    else:
        #Range(Cells(FirstRow, StartCol), Cells(LastRow, StartCol + Cnt - 1)).Select
        # Debug
        X02.Range(X02.Cells(FirstRow, StartCol), X02.Cells(LastRow, StartCol + Cnt - 1)).ClearContents()
        # Old:  = ""

def Insert_Columns(FirstRow, LastRow, Col, Cnt, LastCol):
    #-------------------------------------------------------------------------------------------------------
    # Insert columns by moveing the colunms to the left
    Copy_Columns(FirstRow, LastRow, Col, Col + Cnt, LastCol - Col + 1)
    Del_Columns(FirstRow, LastRow, Col, Cnt)

def Delete_Columns(FirstRow, LastRow, Col, Cnt, LastCol):
    CopyCnt = Long()
    #-------------------------------------------------------------------------------------------------------
    # Delete columns with move if there are other columns to the left
    CopyCnt = LastCol -  ( Col + Cnt )  + 1
    Copy_Columns(FirstRow, LastRow, Col + Cnt, Col, CopyCnt)
    if Col <= LastCol:
        if CopyCnt > 0:
            # Not at the end of the used area
            Del_Columns(FirstRow, LastRow, LastCol - Cnt + 1, Cnt)
        else:
            Del_Columns(FirstRow, LastRow, Col, LastCol - Col + 1)

def Insert_or_Delete_Columns(Add, FirstRow, LastRow, Col, Cnt, LastCol):
    #---------------------------------------------------------------------------------------------------------------------------------
    if Add:
        Insert_Columns(FirstRow, LastRow, Col, Cnt, LastCol)
    else:
        Delete_Columns(FirstRow, LastRow, Col, Cnt, LastCol)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Column_Message_Shown - ByRef 
def Add_or_Del_Columns_to_Pattern(Add, Column_Message_Shown):
    FirstLEDsRow = Long()

    LastLEDsRow = Long()

    LastLEDsCol = Long()

    Col = Long()

    DstCol = Long()

    Cnt = Long()
    #-----------------------------------------------------------------------------------------------
    if Msg_if_not_in_Pattern_Table():
        return
    # Message if the button is pressed the first time
    if not Column_Message_Shown:
        if Add:
            Msg = pattgen.M09_Language.Get_Language_Str('Mit diesem Knopf wird eine Spalte in die Tabelle eingefügt.' + vbCr + 'Die Spalte wird vor links neben der aktuellen Position eingefügt.')
            Title = pattgen.M09_Language.Get_Language_Str('Spalte in Tabelle einfügen')
        else:
            Msg = pattgen.M09_Language.Get_Language_Str('Mit diesem Knopf wird die Spalte in der Tabelle gelöscht' + vbCr + 'in der sich der Cursor befindet.')
            Title = pattgen.M09_Language.Get_Language_Str('Spalte in Tabelle löschen')
        if vbCancel == X02.MsgBox(Msg + vbCr + vbCr + pattgen.M09_Language.Get_Language_Str('Achtung: Diese Meldung wird nur ein mal angezeigt'), vbOKCancel + vbInformation, Title):
            return
    Column_Message_Shown = True
    X02.Application.ScreenUpdating = False
    X02.Application.EnableEvents = False
    X02.ActiveSheet.EnableCalculation = False
    FirstLEDsRow = X02.Range(M01.FirstLEDTabRANGE).Row
    LastLEDsRow = FirstLEDsRow + int(X02.Range(M01.LED_Cnt_Rng)) - 1
    # Find the last used column
    LastLEDsCol = X02.Application.WorksheetFunction.Max(M30.LastFilledColumn2(X02.Range(M01.LEDsRANGE), LastLEDsRow), M30.LastFilledColumn2(X02.Cells(M01.Dauer_Row, M01.Dauer_Col1), M01.Dauer_Row), M30.LastFilledColumn2(X02.Cells(M01.GoTo_Row, M01.GoTo_Col1), M01.GoTo_Row))
    Cnt = X02.Selection.Columns.Count
    Col = X02.Selection.Column
    Insert_or_Delete_Columns(Add, FirstLEDsRow, LastLEDsRow, Col, Cnt, LastLEDsCol)
    Insert_or_Delete_Columns(Add, M01.Dauer_Row, M01.Dauer_Row, Col, Cnt, LastLEDsCol)
    Insert_or_Delete_Columns(Add, M01.GoTo_Row, M01.GoTo_Row, Col, Cnt, LastLEDsCol)
    M02a.Global_Worksheet_Change(X02.Cells(1, 1))
    # Redraw everything
    M30.Enable_Application_Automatics()

def Add_Columns_to_Pattern():
    #----------------------------------
    Add_or_Del_Columns_to_Pattern(True, Add_Column_Message_Shown)

def Del_Columns_from_Pattern():
    #------------------------------------
    Add_or_Del_Columns_to_Pattern(False, Del_Column_Message_Shown)

# VB2PY (UntranslatedCode) Option Explicit
