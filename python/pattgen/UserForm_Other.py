from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M09_Language
import ExcelAPI.XLW_Workbook as X02
import pattgen.M30_Tools as M30
import pattgen.M15_Par_Description
import pattgen.M14_Select_GotoAct

""" Use case sensitive compare. Important for the "Sec" compare below
-------------------------------------------------------------------------------
-----------------------------------------------------------
-------------------------------------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 2 on 0
--------------------------------
-----------------------------------------------------------------------------------------------
-------------------------------------------------------------
-------------------------------
----------------------------
"""

ParList = Variant()
FuncName = String()
NamesA = Variant()
MAX_PAR_CNT = 6
TypA = vbObjectInitialize((MAX_PAR_CNT,), String)
MinA = vbObjectInitialize((MAX_PAR_CNT,), Variant)
MaxA = vbObjectInitialize((MAX_PAR_CNT,), Variant)
ParName = vbObjectInitialize((MAX_PAR_CNT,), String)

def Check_Limit_to_MinMax(ParNr, Value):
    _fn_return_value = None
    Msg = String()

    ValidRangeTxt = String()
    #-------------------------------------------------------------------------------
    # Return true if its within the alowed range
    #With Controls("Par" & ParNr)
    ValidRangeTxt = vbCr + pattgen.M09_Language.Get_Language_Str('Bitte einen Wert zwischen ') + MinA(ParNr - 1) + pattgen.M09_Language.Get_Language_Str(' und ') + MaxA(ParNr - 1) + pattgen.M09_Language.Get_Language_Str(' eingeben.')
    if Value == '':
        Msg = pattgen.M09_Language.Get_Language_Str('leer.') + ValidRangeTxt
    elif not IsNumeric(Value):
        Msg = pattgen.M09_Language.Get_Language_Str('keine gültige Zahl.') + ValidRangeTxt
    elif CStr(Round(Value, 0)) != CStr(Value):
        Msg = pattgen.M09_Language.Get_Language_Str('nicht Ganzzahlig.') + ValidRangeTxt
    elif MinA(ParNr - 1) != '' and Value < Val(MinA(ParNr - 1)):
        Msg = pattgen.M09_Language.Get_Language_Str('zu klein!' + vbCr + 'Der Minimal zulässiger Wert ist: ') + MinA(ParNr - 1)
    elif MaxA(ParNr - 1) != '' and Value > Val(MaxA(ParNr - 1)):
        Msg = pattgen.M09_Language.Get_Language_Str('zu groß!' + vbCr + 'Der Maximal zulässige Wert ist: ') + MaxA(ParNr - 1)
    if Msg != '':
        Controls('Par' + ParNr).setFocus()
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Der Parameter \'') + Controls('LabelPar' + ParNr).Caption + pattgen.M09_Language.Get_Language_Str('\' ist ') + Msg, vbInformation, pattgen.M09_Language.Get_Language_Str('Bereichsüberschreitung'))
    else:
        _fn_return_value = True
    #End With
    return _fn_return_value

def Check_Time_String(ParNr):
    _fn_return_value = None
    ValidRangeTxt = String()

    Parts = Variant()
    #-----------------------------------------------------------
    ValidRangeTxt = vbCr + pattgen.M09_Language.Get_Language_Str('Bitte einen Zeit zwischen ') + MinA(ParNr - 1) + pattgen.M09_Language.Get_Language_Str(' ms und ') + MaxA(ParNr - 1) + pattgen.M09_Language.Get_Language_Str(' ms eingeben.' + vbCr + 'Die Zeitangabe kann auch eine der folgenden Einheit enthalten:' + vbCr + ' Min, Sec, ms ' + vbCr + 'Achtung: Zwischen zahl und Einheit muss ein Leerzeichen stehen.' + vbCr + 'Beispiel: 3 Sec')
    # ToDo: Erlaubte Zeiten zusätzlich in Minuten Angeben
    _with50 = Controls('Par' + ParNr)
    Parts = Split(_with50.Value, ' ')
    if UBound(Parts) != 1 or not IsNumeric(Parts(0)) or InStr(ValidUnits, ' ' + Parts(1) + ' ') == 0:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Der Parameter \'') + ParName(ParNr - 1) + pattgen.M09_Language.Get_Language_Str('\' ist ungültig'), vbInformation, pattgen.M09_Language.Get_Language_Str('Ungültiger Parameter') + ValidRangeTxt)
        return _fn_return_value
    else:
        # Two parameter detected. First is numeric, the second is a valid Unit
        _select39 = LCase(Parts(1))
        if (_select39 == 'min'):
            Val = Parts(0) * 60 * 1000
        elif (_select39 == 'sec') or (_select39 == 'sek'):
            Val = Parts(0) * 1000
        elif (_select39 == 'ms'):
            Val = Parts(0)
        else:
            X02.MsgBox('Internal error: Unknown unit \'' + Parts(1) + '\' in Check_Time_String()', vbCritical, 'Internal error')
            M30.EndProg()
        if Check_Limit_to_MinMax(ParNr, Val) == False:
            return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Val - ByRef 
def Check_Par_with_ErrMsg(ParNr, Val):
    _fn_return_value = None
    #-------------------------------------------------------------------------------------
    if ParNr > MAX_PAR_CNT:
        X02.MsgBox('Internal error in Chek_Range()')
        M30.EndProg()
    _with51 = Controls('Par' + ParNr)
    _with51.Value = Trim(_with51.Value)
    #Debug.Print "Check_Range " & ParName(ParNr - 1) & ": " & .Value
    _select40 = TypA(ParNr - 1)
    if (_select40 == ''):
        # Normal Numeric parameter
        if Check_Limit_to_MinMax(ParNr, _with51.Value) == False:
            return _fn_return_value, Val
    elif (_select40 == 'Time'):
        # time could have a tailing "Min", "Sek", "sek", "Sec", "sec", "Ms", "ms"
        if IsNumeric(_with51.Value):
            _with51.Value = Int(_with51.Value)
            if Check_Limit_to_MinMax(ParNr, _with51.Value) == False:
                return _fn_return_value
        else:
            # The parameter is NOT numeric
            if Check_Time_String(ParNr) == False:
                return _fn_return_value
        _with51.Value = Replace(_with51.Value, ',', '.')
        # Replace the german comma
    else:
        X02.MsgBox('Internal error: Unknown parameter Typ: \'' + TypA(ParNr - 1) + '\'', vbCritical, 'Internal Error')
        M30.EndProg()
    Val = _with51.Value
    _fn_return_value = True
    return _fn_return_value, Val

def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
    Change_Language_in_Dialog(Me)
    X02.Center_Form(Me)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Par - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def Show_UserForm_Other(Par, Name, Description):
    global FuncName, ParList, TypA, MinA, MaxA, ParName
    CNames = 'Val0 Val1 Period Duration Timeout DstVar MinTime MaxTime Par1'

    p = Variant()
    
    Typ = String()

    Min = String()

    Max = String()

    Def = String()

    InpTxt = String()

    Hint = String()    

    UsedParNr = Long()

    Show_CounterFlags = Variant()
    #-----------------------------------------------------------------------------------------------
    FuncName = Name
    if Description == '':
        Description_TextBox = pattgen.M09_Language.Get_Language_Str('Noch keine Beschreibung zur Funktion \'') + Name + pattgen.M09_Language.Get_Language_Str('\' vorhanden ;-(')
    else:
        Description_TextBox = Description
    ScrollBar1.Max = Len(Description_TextBox)
    HookFormScroll(Me, 'Description_TextBox')
    # Initialize the mouse wheel scroll function
    Me.Caption = pattgen.M09_Language.Get_Language_Str('Parametereingabe der \'') + Name + pattgen.M09_Language.Get_Language_Str('\' Funktion')
    #Debug.Print
    # Debug
    #Debug.Print Name & " (" & Par & ")"
    # Debug
    #*** Hide all entrys in the dialog which are not needed ***
    ParList = Split(Par, ',')
    # Add parameters
    for p in ParList:
        p = Trim(p)
        if UsedParNr >= MAX_PAR_CNT:
            X02.MsgBox('Internal error: The number of parameters is to large in Show_UserForm_Other()')
            M30.EndProg()
        if p == 'Flags':
            Show_CounterFlags = True
        else:
            Typ, Min, Max, Def, InpTxt, Hint = pattgen.M15_Par_Description.Get_Par_Data(p, Typ, Min, Max, Def, InpTxt, Hint)
            TypA[UsedParNr] = Typ
            MinA[UsedParNr] = Min
            MaxA[UsedParNr] = Max
            ParName[UsedParNr] = p
            UsedParNr = UsedParNr + 1
            Me.Controls['Par' + UsedParNr] = Def
            Me.Controls['LabelPar' + UsedParNr] = InpTxt
            Me.Controls['LabelPar' + UsedParNr].ControlTipText = Hint
    #Debug.Print "UsedParNr=" & UsedParNr
    # Debug
    if not Show_CounterFlags:
        M30.Hide_and_Move_up(Me, 'CounterFlags_Frame', 'Par1')
    M30.Hide_and_Move_up(Me, 'Par' + UsedParNr + 1, 'Abort_Button')
    # Hide the not needed controlls
    Me.Show()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Res - ByRef 
def Create_Result(Res):
    _fn_return_value = None
    p = Variant()
    #-------------------------------------------------------------
    # Return True if sucessfully checked alt inputs
    Res = ''
    for p in ParList:
        p = Trim(p)
        if p == 'Flags':
            # Enabled could be used later in special counter functions if the parameter is locked or always active
            if Inv_Input_CheckBox.Enabled and Inv_Input_CheckBox:
                Flags = Flags + ' | CF_INV_INPUT'
            if ResetLong_CheckBox.Enabled and ResetLong_CheckBox:
                Flags = Flags + ' | CF_RESET_LONG'
            if RotateCnt_CheckBox.Enabled and RotateCnt_CheckBox:
                Flags = Flags + ' | CF_ROTATE'
            if Ping_Pong_CheckBox.Enabled and Ping_Pong_CheckBox:
                Flags = Flags + ' | CF_PINGPONG'
            if Skip0_Pos_CheckBox.Enabled and Skip0_Pos_CheckBox:
                Flags = Flags + ' | CF_SKIP0'
            if Flags == '':
                Flags = ' | CM_NORMAL'
            Res = Res + Mid(Flags, Len(' | ') + 1)
        else:
            Val = 'Not Found'
            for Nr in vbForRange(1, MAX_PAR_CNT):
                if ParName(Nr - 1) == p:
                    res, Val = Check_Par_with_ErrMsg(Nr, Val)
                    if res == False:
                        return _fn_return_value
                    break
            if Val == 'Not Found':
                X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler der Parameter \'') + p + pattgen.M09_Language.Get_Language_Str('\' wurde nicht gefunden'), vbCritical, pattgen.M09_Language.Get_Language_Str('Programm Fehler'))
        Res = Res + Val + ', '
    Res = FuncName + '(' + M30.DelLast(Res, 2) + ')'
    _fn_return_value = True
    return _fn_return_value, Res #*HL ByRef

def Abort_Button_Click():
    #-------------------------------
    UnhookFormScroll()
    # Deactivate the mouse wheel scroll function
    #Me.Hide
    pattgen.M14_Select_GotoAct.Userform_Res = ''
    X02.Unload(Me)
    # Don't keep the entered data. Importand because the positions of the controlls and the visibility have been changed

def OK_Button_Click():
    #----------------------------
    res, pattgen.M14_Select_GotoAct.Userform_Res = Create_Result(pattgen.M14_Select_GotoAct.Userform_Res)
    if res:
        #UnhookFormScroll()
        # Deactivate the mouse wheel scroll function
        #Me.Hide
        X02.Unload(Me)
        # Don't keep the entered data. Importand because the positions of the controlls and the visibility have been changed

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Option Compare Binary
