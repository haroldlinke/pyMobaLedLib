from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import pattgen.M14_Select_GotoAct
import pattgen.M30_Tools as M30
import pattgen.Pattern_Generator as PG

""" Select_GotoAct_Form
 ~~~~~~~~~~~~~~~~~
 Module Description:
 ~~~~~~~~~~~~~~~~~~~
 This module contains functions for the Goto Activation dialog.
 The user could select a Goto Activation type with then mouse.
 The result is stored in the public variable GotoAct_Res
 Revision History:
 ~~~~~~~~~~~~~~~~~
 19.11.19: - Copied from Prog_Generator
-----------------------------
-------------------------------
-----------------------------
--------------------------------
--------------------------------------------------------
---------------------------
------------------------------------------------------------------
-------------------------
----------------------------------
---------------------------------------------------------
--------------------------------
-----------------------------------------------
-----------------------------------------------------------------------
"""

Enable_Listbox_Changed = Boolean()
SrcSh = X02.Worksheet()
ListDataSh = String()
ExpOutCnt = Integer()

def Calc_GotoAct_Res():
    Nr = Long()

    Res = String()
    #-----------------------------
    # Return the name and the row number in the Data Sheet
    # If MultiSelect is enabled a space separated list is returned
    for Nr in vbForRange(0, ListBox.ListCount - 1):
        if ListBox.Selected(Nr):
            Res = Res + ListBox.List(Nr, 0) + ',' + Get_Row_with_Mode_Filter(Nr) + ' '
            # Return "Name,Nr"  Nr: row nr in the data sheet
    pattgen.M14_Select_GotoAct.GotoAct_Res = M30.DelLast(Res)
    # Delete the tailing space

def Abort_Button_Click():
    global Enable_Listbox_Changed
    #-------------------------------
    UnhookFormScroll()
    # Deactivate the mouse wheel scroll function
    Me.Hide()
    # no "Unload Me" to Don't keep the entered data.
    pattgen.M14_Select_GotoAct.GotoAct_Res = ''
    Enable_Listbox_Changed = False

def Del_Button_Click():
    global Enable_Listbox_Changed
    #-----------------------------
    UnhookFormScroll()
    # Deactivate the mouse weel scrol function
    Me.Hide()
    # no "Unload Me" to keep the entered data.
    pattgen.M14_Select_GotoAct.GotoAct_Res = 'DELETE'
    Enable_Listbox_Changed = False

def Select_Button_Click():
    global Enable_Listbox_Changed
    #--------------------------------
    UnhookFormScroll()
    # Deactivate the mouse weel scrol function
    Me.Hide()
    # no "Unload Me" to keep the entered data.
    Enable_Listbox_Changed = False
    Calc_GotoAct_Res()

def Get_Row_with_Mode_Filter(ListNr):
    _fn_return_value = None
    Nr = Long()

    r = Long()
    #--------------------------------------------------------
    r = pattgen.M14_Select_GotoAct.SM_DIALOGDATA_ROW1
    Nr = - 1
    _with70 = X02.Sheets(ListDataSh)
    while True:
        if Nr < ListNr:
            r = r + 1
        else:
            _fn_return_value = r
            return _fn_return_value
    return _fn_return_value

def ListBox_Change():
    #---------------------------
    #'  Description = ""
    #'  Detail = ""
    if Enable_Listbox_Changed:
        for Nr in vbForRange(0, ListBox.ListCount - 1):
            if ListBox.Selected(Nr):
                Cnt = Cnt + 1
                Row = Get_Row_with_Mode_Filter(Nr)
                Txt = Replace(SrcSh.Cells(Row, pattgen.M14_Select_GotoAct.SM_DetailCOL), '|', vbLf)
                #'            If Txt <> "" Then
                #'                  Description = Description & Txt & vbCr
                #'            Else
                Description = Description + SrcSh.Cells(Row, pattgen.M14_Select_GotoAct.SM_ShrtD_COL) + vbCr
                #'            End If
                #'            Detail = Detail & Replace_Double_Space(SrcSh.Cells(Row, SM_Macro_COL)) & vbCr
                # Show one or more selected details
        SelectedCnt_Label = 'Selected: ' + Cnt

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cancel - ByVal 
def ListBox_DblClick(Cancel):
    #------------------------------------------------------------------
    Select_Button_Click()

def Add_Filtered():
    r = X02.Range()

    c = X02.Range()
    #-------------------------
    _with71 = X02.Sheets(ListDataSh)
    r = _with71.Range(_with71.Cells(pattgen.M14_Select_GotoAct.SM_DIALOGDATA_ROW1, pattgen.M14_Select_GotoAct.SM_Name__COL), _with71.Cells(M30.LastUsedRowIn(PG.ThisWorkbook.Sheets(ListDataSh)), pattgen.M14_Select_GotoAct.SM_Name__COL))
    for c in r:
        #'If (.Cells(c.Row, SM_Mode__COL) = "" Or Expert_CheckBox) And .Cells(c.Row, SM_OutCntCOL) >= ExpOutCnt Then
        #'   ListBox.AddItem c.Value
        #'   ListBox.List(ListBox.ListCount - 1, 1) = c.offset(0, 1).Value
        #'End If
        pass

def Expert_CheckBox_Click():
    #----------------------------------
    Load_Data_to_Listbox(ListDataSh)

def Load_Data_to_Listbox(ListDataSh_par):
    global ListDataSh, SrcSh
    #---------------------------------------------------------
    # Defines the sheet which contains the data and loads the data into the form.
    ListDataSh = ListDataSh_par
    # VB2PY (UntranslatedCode) On Error Resume Next
    # For some reasons this function is called two times and the second call generates a crash
    SrcSh = PG.ThisWorkbook.Sheets(ListDataSh)
    Me.ListBox.Clear()
    # VB2PY (UntranslatedCode) On Error GoTo 0
    _with72 = Me.ListBox
    _with72.ColumnCount = 2
    _with72.ColumnWidths = '100 Pt'
    Add_Filtered()

def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ": Select_GotoAct_Form Initialize"
    Change_Language_in_Dialog(Me)
    X02.Center_Form(Me)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lngRotation - ByVal 
def MouseWheel(lngRotation):
    #-----------------------------------------------
    # Process the mouse wheel changes
    _with73 = ListBox
    # Adapt to the listbox which should be controlled
    if lngRotation > 0:
        if _with73.TopIndex > 0:
            if _with73.TopIndex > 3:
                _with73.TopIndex = _with73.TopIndex - 3
            else:
                _with73.TopIndex = 0
    else:
        _with73.TopIndex = _with73.TopIndex + 3

def Show_Select_GotoAct_Form(ListDataSh, MinOutCnt):
    global ExpOutCnt, Enable_Listbox_Changed
    #-----------------------------------------------------------------------
    # Use this function to show the dialog.
    ExpOutCnt = MinOutCnt
    Load_Data_to_Listbox(ListDataSh)
    Enable_Listbox_Changed = True
    SelectedCnt_Label = 'Selected: 0'
    Me.Controls('ListBox').setFocus()
    HookFormScroll(Me, 'ListBox')
    # Initialize the mouse wheel scroll function
    Me.Show()

# VB2PY (UntranslatedCode) Option Explicit
