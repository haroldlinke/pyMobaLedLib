from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M14_Select_GotoAct
import ExcelAPI.XLW_Workbook as X02
import pattgen.M09_Language
import pattgen.M06_Goto_Graph
import pattgen.Pattern_Generator as PG

""" Generates additional macros if the Goto mode is used

 The range "Goto_Aktivierung" defines the activation macro which is
 used to select the goto start position.

 Following types are possible:
  - N_Buttons
  - Binary
  - Counter(Flags, Timeout)
  - RandButton(Flags, Timeout)
  - RandomTime(MinTime, MaxTime)
--------------------------------------------------
---------------------------------------------------------
UT---------------------------
# VB2PY (CheckDirective) VB directive took path 1 on True
 08.01.20: New
--------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------
UT----------------------------------------------------
"""

PaCfg_COMMENT = '// Activation: '

def Select_Goto_Activation():
    _fn_return_value = None
    #--------------------------------------------------
    # Return True is a valid Goto Activation has been selected
    _fn_return_value = pattgen.M14_Select_GotoAct.Select_GotoAct()
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: x - ByVal 
def Get_BinSize(x):
    _fn_return_value = None
    #---------------------------------------------------------
    # Number of binary bits necessary for x different values
    _fn_return_value = X02.Application.RoundUp(Log(x) / Log(2), 0)
    return _fn_return_value

def Test_Get_BinSize():
    i = Long()

    y = Integer()
    #UT---------------------------
    for i in vbForRange(1, 20):
        y = Get_BinSize(i)
        Debug.Print('Get_BinSize(' + i + ')=' + y + '  2^' + y + ' = ' + 2 ** y)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Params - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Loc_InCh - ByRef 
def Get_Counter_Act_Macro(Params, Loc_InCh):
    _fn_return_value = None
    Parts = Variant()

    i = Long()

    Res = String()
    #--------------------------------------------------------------------------------------------------
    # Goto activation: "Counter(Flags, Timeout)"
    # This mode selects the next 'Goto Number' if the input changes from 0 to 1.
    #
    # If generates the following activation macro:
    #   New_Local_Var()
    #   Counter(CF_ONLY_LOCALVAR | Flags, #InCh, SI_1, Timeout, Goto_Start_Points)
    # Counter macro
    Parts = Split(Params, ',')
    if UBound(Parts) != 1:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Falsche Parameter Anzahl in \'RandButton...()\' Funktion ;-(' + vbCr + 'Es müssen folgende zwei Parameter angegeben werden:' + vbCr + '  Flags, Timeout'), vbCritical, pattgen.M09_Language.Get_Language_Str('Falsche Parameter Anzahl in') + ' \'RandButton...()\'')
        _fn_return_value = 'ERROR'
        return _fn_return_value
    Res = 'New_Local_Var()' + vbLf + 'Counter(CF_ONLY_LOCALVAR'
    if Trim(Parts(0)) != '':
        Res = Res + ' | ' + Parts(0)
    Res = Res + ', #InCh, SI_1, ' + Parts(1) + ', ' + pattgen.M06_Goto_Graph.Goto_Start_Points + ')' + vbLf
    Loc_InCh = 0
    _fn_return_value = Res
    # 08.01.20: Added: "New_Local_Var()" & vbcr &
    return _fn_return_value, Loc_InCh #*HL ByRef

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Params - ByVal 
def Get_RandomB_Act_Macro(Params):
    _fn_return_value = None
    Parts = Variant()
    #-----------------------------------------------------------------------
    # Goto activation: "RandButton(Flags, Timeout)"
    # This mode selects a random 'Goto Number' if the input changes from 0 to 1
    #
    # It generates the following activation macro:
    #   New_Local_Var()
    #   Counter(CF_ONLY_LOCALVAR | CF_RANDOM | Flags, #InCh, SI_1, Timeout, Goto_Start_Points)
    Parts = Split(Params, ',')
    if UBound(Parts) != 1:
        # ToDo: Stimmt den die Fehlermeldung 'RandButton()' oder ist das ein Copy Paste Fehler von oben ?
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Falsche Parameter Anzahl in \'RandButton()\' Funktion ;-(' + vbCr + 'Es müssen folgende zwei Parameter angegeben werden:' + vbCr + '  Flags, Timeout'), vbCritical, pattgen.M09_Language.Get_Language_Str('Falsche Parameter Anzahl in') + ' \'RandButton()\'')
        _fn_return_value = 'ERROR'
        return _fn_return_value
    _fn_return_value = 'New_Local_Var()' + vbLf + 'Counter(CF_ONLY_LOCALVAR | CF_RANDOM | ' + Parts(0) + ', #InCh, SI_1, ' + Parts(1) + ', ' + pattgen.M06_Goto_Graph.Goto_Start_Points + ')' + vbLf
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Loc_InCh - ByRef 
def Get_RandTimeAct_Macro(Params, Loc_InCh, Add_Flag):
    _fn_return_value = None
    Parts = Variant()
    #----------------------------------------------------------------------------------------------------------------
    # Goto activation: "RandomTime(MinTime, MaxTime)"
    # This selects an other 'Goto Number' ramdomly by time and number
    # The InCh is used to enable the random change. If InCh is disabled
    # the Goto Start position 0 is activated.
    # It generates the following activation macro:
    #   Random(#LocInCh, #InCh, RM_NORMAL, MinTime, MaxTime, 1 ms, 1 ms)
    #   New_Local_Var()
    #   Counter(CF_ONLY_LOCALVAR | CF_RANDOM | CF_SKIP0, #LocInCh, #InCh, 0 Sec, Goto_Start_Points)
    Parts = Split(Params, ',')
    if UBound(Parts) != 1:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Falsche Parameter Anzahl in \'Counter()\' Funktion ;-(' + vbCr + 'Es müssen folgende zwei Parameter angegeben werden:' + vbCr + '  MinTime, MaxTime'), vbCritical, pattgen.M09_Language.Get_Language_Str('Falsche Parameter Anzahl in') + ' \'RandomTime()\'')
        _fn_return_value = 'ERROR'
        return _fn_return_value
    _fn_return_value = 'Random(#LocInCh, #InCh, RM_NORMAL, ' + Parts(0) + ', ' + Parts(1) + ', 1 ms, 1 ms)' + vbLf + 'New_Local_Var()' + vbLf + '// Attention: State 0 is used if input is disabled' + vbLf + 'Counter(CF_ONLY_LOCALVAR' + Add_Flag + ' | CF_SKIP0, #LocInCh, #InCh, 0 Sec, ' + pattgen.M06_Goto_Graph.Goto_Start_Points + ')' + vbLf
    Loc_InCh = 1
    return _fn_return_value, Loc_InCh

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Act_Macro - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InCnt - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Loc_InCh - ByRef 
def Get_Additional_Goto_Activation_Macro(Act_Macro, InCnt, Loc_InCh):
    _fn_return_value = None
    ActWB = String()

    Bin_Start_Points = Long()
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # Generate an additional macro if the Goto Mode is active.
    # The macro fills a local variable with the goto number.
    # Return False to abort
    if not pattgen.M06_Goto_Graph.Goto_Mode_is_Active():
        _fn_return_value = True
        return _fn_return_value, Act_Macro, InCnt, Loc_InCh #*HL ByRef
    ActWB = X02.ActiveWorkbook.Name
    # Dell_All_Arrows must be run in this workbook
    PG.ThisWorkbook.Activate()
    pattgen.M06_Goto_Graph.Draw_All_Arrows()
    # redraw and calc Goto_Start_Points
    if pattgen.M06_Goto_Graph.Goto_Start_Points <= 1:
        # Do we have more than the start point 0 ?
        _fn_return_value = True
        # No => Noting to do, Exit
        return _fn_return_value,Act_Macro, InCnt, Loc_InCh #*HL ByRef
    Bin_Start_Points = Get_BinSize(pattgen.M06_Goto_Graph.Goto_Start_Points)
    while Act_Macro == '':
        GotoAct = Trim(X02.Range('Goto_Aktivierung'))
        Comment = PaCfg_COMMENT + GotoAct + vbLf
        p = InStr(GotoAct, '(')
        if p > 0:
            Name = Left(GotoAct, p - 1)
            Params = Replace(Mid(GotoAct, p + 1), ')', '')
        else:
            Name = GotoAct
        _select41 = Name
        if (_select41 == 'N_Buttons'):
            InCnt = pattgen.M06_Goto_Graph.Goto_Start_Points
            Act_Macro = 'InCh_to_TmpVar(#InCh, ' + InCnt + ')' + vbLf
        elif (_select41 == 'N_Buttons1'):
            InCnt = pattgen.M06_Goto_Graph.Goto_Start_Points - 1
            Act_Macro = 'InCh_to_TmpVar1(#InCh, ' + InCnt + ')' + vbLf
            # 07.05.20:
        elif (_select41 == 'N_OneTimeBut'):
            InCnt = pattgen.M06_Goto_Graph.Goto_Start_Points
            Act_Macro = 'InCh_to_LocalVar(#InCh, ' + InCnt + ')' + vbLf
            # 08.06.20:
        elif (_select41 == 'N_OneTimeBut1'):
            InCnt = pattgen.M06_Goto_Graph.Goto_Start_Points - 1
            Act_Macro = 'InCh_to_LocalVar1(#InCh, ' + InCnt + ')' + vbLf
            # 08.06.20:
        elif (_select41 == 'Binary'):
            InCnt = Bin_Start_Points
            Act_Macro = 'Bin_InCh_to_TmpVar(#InCh, ' + InCnt + ')' + vbLf
        elif (_select41 == 'Binary1'):
            InCnt = Bin_Start_Points - 1
            Act_Macro = 'Bin_InCh_to_TmpVar1(#InCh, ' + InCnt + ')' + vbLf
            # 07.05.20:
        elif (_select41 == 'Counter'):
            InCnt = 1
            Act_Macro, Loc_InCh = Get_Counter_Act_Macro(Params, Loc_InCh)
        elif (_select41 == 'RandButton'):
            InCnt = 1
            Act_Macro = Get_RandomB_Act_Macro(Params)
        elif (_select41 == 'RandomTime'):
            InCnt = 1
            Act_Macro, Loc_InCh = Get_RandTimeAct_Macro(Params, Loc_InCh, ' | CF_RANDOM')
        elif (_select41 == 'RandomCount'):
            InCnt = 1
            Act_Macro, Loc_InCh = Get_RandTimeAct_Macro(Params, Loc_InCh, ' | CF_ROTATE')
            # 13.01.20:
        elif (_select41 == 'RandomPingPong'):
            InCnt = 1
            Act_Macro, Loc_InCh = Get_RandTimeAct_Macro(Params, Loc_InCh, ' | CF_PINGPONG')
            # 13.01.20:
        elif (_select41 == 'Nothing'):
            # Nothing
            Act_Macro = 'Nothing'
        else:
            # Goto Activation is empty or invalid
            if False == Select_Goto_Activation():
                Act_Macro = 'ABORT'
        if Act_Macro == 'ERROR' or Act_Macro == 'ABORT':
            X02.Workbooks(ActWB).Activate()
            return _fn_return_value, Act_Macro, InCnt, Loc_InCh #*HL ByRef
    if Act_Macro == 'Nothing':
        Act_Macro = ''
    else:
        Act_Macro = Comment + Act_Macro
    _fn_return_value = True
    X02.Workbooks(ActWB).Activate()
    return _fn_return_value, Act_Macro, InCnt, Loc_InCh #*HL ByRef

def Test_Get_Additional_Goto_Activation_Macro():
    Act_Macro = String()

    InCnt = Integer()

    Loc_InCh = Integer()
    #UT----------------------------------------------------
    res, Act_Macro, InCnt, Loc_InCh = Get_Additional_Goto_Activation_Macro(Act_Macro, InCnt, Loc_InCh)
    if res:
        Debug.Print('InCnt=' + InCnt + ' Loc_InCh=' + Loc_InCh)
        Debug.Print(' Act_Macro=' + Act_Macro)

# VB2PY (UntranslatedCode) Option Explicit
