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
--------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------
UT----------------------------------------------------
"""

__PaCfg_COMMENT = '// Activation: '

def Select_Goto_Activation():
    fn_return_value = None
    #--------------------------------------------------
    # Return True is a valid Goto Activation has been selected
    fn_return_value = Select_GotoAct()
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: x - ByVal 
def __Get_BinSize(x):
    fn_return_value = None
    #---------------------------------------------------------
    # Number of binary bits necessary for x different values
    fn_return_value = Application.RoundUp(Log(x) / Log(2), 0)
    return fn_return_value

def __Test_Get_BinSize():
    i = Long()

    y = Integer()
    #UT---------------------------
    for i in vbForRange(1, 20):
        y = __Get_BinSize(i)
        Debug.Print('Get_BinSize(' + i + ')=' + y + '  2^' + y + ' = ' + 2 ** y)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Params - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Loc_InCh - ByRef 
def __Get_Counter_Act_Macro(Params, Loc_InCh):
    fn_return_value = None
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
        MsgBox(Get_Language_Str('Falsche Parameter Anzahl in \'RandButton...()\' Funktion ;-(' + vbCr + 'Es müssen folgende zwei Parameter angegeben werden:' + vbCr + '  Flags, Timeout'), vbCritical, Get_Language_Str('Falsche Parameter Anzahl in') + ' \'RandButton...()\'')
        fn_return_value = 'ERROR'
        return fn_return_value
    Res = 'New_Local_Var()' + vbLf + 'Counter(CF_ONLY_LOCALVAR'
    if Trim(Parts(0)) != '':
        Res = Res + ' | ' + Parts(0)
    Res = Res + ', #InCh, SI_1, ' + Parts(1) + ', ' + Goto_Start_Points + ')' + vbLf
    Loc_InCh = 0
    fn_return_value = Res
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Params - ByVal 
def __Get_RandomB_Act_Macro(Params):
    fn_return_value = None
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
        MsgBox(Get_Language_Str('Falsche Parameter Anzahl in \'RandButton()\' Funktion ;-(' + vbCr + 'Es müssen folgende zwei Parameter angegeben werden:' + vbCr + '  Flags, Timeout'), vbCritical, Get_Language_Str('Falsche Parameter Anzahl in') + ' \'RandButton()\'')
        fn_return_value = 'ERROR'
        return fn_return_value
    fn_return_value = 'New_Local_Var()' + vbLf + 'Counter(CF_ONLY_LOCALVAR | CF_RANDOM | ' + Parts(0) + ', #InCh, SI_1, ' + Parts(1) + ', ' + Goto_Start_Points + ')' + vbLf
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Loc_InCh - ByRef 
def __Get_RandTimeAct_Macro(Params, Loc_InCh, Add_Flag):
    fn_return_value = None
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
        MsgBox(Get_Language_Str('Falsche Parameter Anzahl in \'Counter()\' Funktion ;-(' + vbCr + 'Es müssen folgende zwei Parameter angegeben werden:' + vbCr + '  MinTime, MaxTime'), vbCritical, Get_Language_Str('Falsche Parameter Anzahl in') + ' \'RandomTime()\'')
        fn_return_value = 'ERROR'
        return fn_return_value
    fn_return_value = 'Random(#LocInCh, #InCh, RM_NORMAL, ' + Parts(0) + ', ' + Parts(1) + ', 1 ms, 1 ms)' + vbLf + 'New_Local_Var()' + vbLf + '// Attention: State 0 is used if input is disabled' + vbLf + 'Counter(CF_ONLY_LOCALVAR' + Add_Flag + ' | CF_SKIP0, #LocInCh, #InCh, 0 Sec, ' + Goto_Start_Points + ')' + vbLf
    Loc_InCh = 1
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Act_Macro - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InCnt - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Loc_InCh - ByRef 
def Get_Additional_Goto_Activation_Macro(Act_Macro, InCnt, Loc_InCh):
    fn_return_value = None
    ActWB = String()

    Bin_Start_Points = Long()
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # Generate an additional macro if the Goto Mode is active.
    # The macro fills a local variable with the goto number.
    # Return False to abort
    if not Goto_Mode_is_Active():
        fn_return_value = True
        return fn_return_value
    ActWB = ActiveWorkbook.Name
    ThisWorkbook.Activate()
    Draw_All_Arrows()
    if Goto_Start_Points <= 1:
        fn_return_value = True
        return fn_return_value
    Bin_Start_Points = __Get_BinSize(Goto_Start_Points)
    while Act_Macro == '':
        GotoAct = Trim(Range('Goto_Aktivierung'))
        Comment = __PaCfg_COMMENT + GotoAct + vbLf
        p = InStr(GotoAct, '(')
        if p > 0:
            Name = Left(GotoAct, p - 1)
            Params = Replace(Mid(GotoAct, p + 1), ')', '')
        else:
            Name = GotoAct
        if (Name == 'N_Buttons'):
            InCnt = Goto_Start_Points
            Act_Macro = 'InCh_to_TmpVar(#InCh, ' + InCnt + ')' + vbLf
        elif (Name == 'N_Buttons1'):
            InCnt = Goto_Start_Points - 1
            Act_Macro = 'InCh_to_TmpVar1(#InCh, ' + InCnt + ')' + vbLf
        elif (Name == 'N_OneTimeBut'):
            InCnt = Goto_Start_Points
            Act_Macro = 'InCh_to_LocalVar(#InCh, ' + InCnt + ')' + vbLf
        elif (Name == 'N_OneTimeBut1'):
            InCnt = Goto_Start_Points - 1
            Act_Macro = 'InCh_to_LocalVar1(#InCh, ' + InCnt + ')' + vbLf
        elif (Name == 'Binary'):
            InCnt = Bin_Start_Points
            Act_Macro = 'Bin_InCh_to_TmpVar(#InCh, ' + InCnt + ')' + vbLf
        elif (Name == 'Binary1'):
            InCnt = Bin_Start_Points - 1
            Act_Macro = 'Bin_InCh_to_TmpVar1(#InCh, ' + InCnt + ')' + vbLf
        elif (Name == 'Counter'):
            InCnt = 1
            Act_Macro = __Get_Counter_Act_Macro(Params, Loc_InCh)
        elif (Name == 'RandButton'):
            InCnt = 1
            Act_Macro = __Get_RandomB_Act_Macro(Params)
        elif (Name == 'RandomTime'):
            InCnt = 1
            Act_Macro = __Get_RandTimeAct_Macro(Params, Loc_InCh, ' | CF_RANDOM')
        elif (Name == 'RandomCount'):
            InCnt = 1
            Act_Macro = __Get_RandTimeAct_Macro(Params, Loc_InCh, ' | CF_ROTATE')
        elif (Name == 'RandomPingPong'):
            InCnt = 1
            Act_Macro = __Get_RandTimeAct_Macro(Params, Loc_InCh, ' | CF_PINGPONG')
        elif (Name == 'Nothing'):
            Act_Macro = 'Nothing'
        else:
            if False == Select_Goto_Activation():
                Act_Macro = 'ABORT'
        if Act_Macro == 'ERROR' or Act_Macro == 'ABORT':
            Workbooks(ActWB).Activate()
            return fn_return_value
    if Act_Macro == 'Nothing':
        Act_Macro = ''
    else:
        Act_Macro = Comment + Act_Macro
    fn_return_value = True
    Workbooks(ActWB).Activate()
    return fn_return_value

def __Test_Get_Additional_Goto_Activation_Macro():
    Act_Macro = String()

    InCnt = Integer()

    Loc_InCh = Integer()
    #UT----------------------------------------------------
    if Get_Additional_Goto_Activation_Macro(Act_Macro, InCnt, Loc_InCh):
        Debug.Print('InCnt=' + InCnt + ' Loc_InCh=' + Loc_InCh)
        Debug.Print(' Act_Macro=' + Act_Macro)

# VB2PY (UntranslatedCode) Option Explicit