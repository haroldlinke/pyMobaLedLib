# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 4.02
# * Author: Harold Linke
# * Date: January 7, 2022
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
# 2021-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2022-01-07 v4.02 HL: - Else:, ByRef check done, first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

import proggen.M02_Public as M02
import proggen.M02a_Public as M02a
import proggen.M09_Language as M09
import proggen.M25_Columns as M25
import proggen.M30_Tools as M30
import proggen.F00_mainbuttons as F00

import ExcelAPI.XLA_Application as P01

from ExcelAPI.XLC_Excel_Consts import *


""" Exchange functions for the Pattern_Configuarator                          ' 16.09.19:

"""

__Default_Pattern_Configurator_Name = 'Pattern_Configurator.xlsm'

def Get_Prog_Version_Nr():
    fn_return_value = None
    #----------------------------------------------
    # Return a number like: 1.0.8b
    fn_return_value = M02.Prog_Version_Nr
    return fn_return_value

def Selected_Row_Valid():
    fn_return_value = None
    #----------------------------------------------
    M25.Make_sure_that_Col_Variables_match()
    fn_return_value = ( P01.ActiveCell().Row >= M02.FirstDat_Row )
    return fn_return_value

def Get_Description_Range_from_Act_Row():
    fn_return_value = None
    #------------------------------------------------------------
    M25.Make_sure_that_Col_Variables_match()
    fn_return_value = P01.Cells(P01.ActiveCell().Row, M25.Descrip_Col)
    return fn_return_value

def Write_Macro_to_Act_Row(MacroTxt, LEDs, InCnt, LocInCh, Comment="", WrapText=False):
    #Row = Long()

    #LEDs_Channel = Long()
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ResOk=False
    M25.Make_sure_that_Col_Variables_match()
    Row = P01.ActiveCell().Row
    if P01.Cells(Row, M25.LED_Cha_Col) == '':
        while not ResOk:
            Res = P01.InputBox(M09.Get_Language_Str('Welcher LED Kanal soll verwendet werden?' + vbCr + '  0 = Standard LEDs' + vbCr + '  1 = Taster LEDs' + vbCr + '  2 = Optionale LED Gruppe 2' + vbCr + '  3 = Optionale LED Gruppe 2' + vbCr + vbCr + 'LED Kanal (0..3):'), M09.Get_Language_Str('Eingabe des LED Kanals'), 0)
            Res = Trim(Res)
            if Res == '':
                return
            if IsNumeric(Res) and P01.val(Res) >= 0 and P01.val(Res) < M02.LED_CHANNELS:
                ResOk = True
        P01.CellDict[Row, M25.LED_Cha_Col] = P01.val(Res)
    M25.LEDs_Channel = P01.val(P01.Cells(Row, M25.LED_Cha_Col))
    P01.CellDict[Row, M02.Enable_Col] = ChrW(M02.Hook_CHAR)
    P01.CellDict[Row, M25.Config__Col] = MacroTxt
    P01.CellDict[Row, M25.Config__Col].WrapText = WrapText
    P01.CellDict[Row, M25.LEDs____Col] = LEDs
    P01.CellDict[Row, M25.InCnt___Col] = InCnt
    P01.CellDict[Row, M25.LocInCh_Col] = LocInCh
    if Comment != '':
        P01.CellDict[Row, M25.Descrip_Col] = Comment

def __Get_WinStateName(State):
    fn_return_value = None
    #---------------------------------------------------------
    if (State == xlMinimized):
        fn_return_value = 'xlMinimized'
    elif (State == xlMaximized):
        fn_return_value = 'xlMaximized'
    elif (State == xlNormal):
        fn_return_value = 'xlNormal'
    else:
        fn_return_value = 'Unknown ' + State
    return fn_return_value

def NotMinimizedWindow(NewState, Fource=False):
    #--------------------------------------------------------------------------
    if P01.Application.WindowState == xlMinimized or Fource:
        Debug.Print('Set Application.WindowState to' + __Get_WinStateName(NewState))
        P01.Application.WindowState = NewState
    else:
        Debug.Print('Don\'t change Application.WindowState=' + __Get_WinStateName(P01.Application.WindowState))

def Select_Line_for_Patern_Config_and_Call_Macro(Get_Dest, Macro_Callback):
    #-----------------------------------------------------------------------------------------------------
    # Select the destination / Source row
    if Get_Dest:
        F00.Select_ProgGen_Dest_Form.Check_and_Start(Macro_Callback)
    else:
        F00.Select_ProgGen_Src_Form.Check_and_Start(Macro_Callback)

def __Get_Pattern_Configurator_Name():
    fn_return_value = None
    #---------------------------------------------------------
    if Same_Name_already_open(__Default_Pattern_Configurator_Name):
        fn_return_value = P01.Workbooks(__Default_Pattern_Configurator_Name).FullName
    else:
        Path = M02.Get_DestDir_All()
        # Check if it exists in the user dir
        FullPath = Path + __Default_Pattern_Configurator_Name
        if Dir(FullPath) == '':
            # Check if it exists in the lib dir
            Path = M02a.Get_SrcDirInLib()
            FullPath = Path + __Default_Pattern_Configurator_Name
            if Dir(FullPath) == '':
                P01.MsgBox(M09.Get_Language_Str('Fehler: Das Programm \'') + __Default_Pattern_Configurator_Name + '\'' + vbCr + M09.Get_Language_Str('existiert nicht im Standard Verzeichnis:') + vbCr + '  \'' + Path + '\'', vbCritical, M09.Get_Language_Str('Fehler ') + __Default_Pattern_Configurator_Name + M09.Get_Language_Str(' nicht vorhanden'))
                return fn_return_value
        fn_return_value = FullPath
    return fn_return_value

def Start_Pattern_Configurator():
    Pattern_Configurator_Name = String()
    #--------------------------------------
    # Make sure that the Pattern_Configurator excel sheet is opened
    # and activated.
    # If the program is already opened it's shown normal (Not minimized) and brought to the top
    # If not it's opened from
    #   1.: %USERPROFILE%\Documents\Arduino\MobaLedLib_ <Lib Ver>
    #   2.: %USERPROFILE%\Documents\Arduino\libraries\MobaLedLib\extras\
    Pattern_Configurator_Name = __Get_Pattern_Configurator_Name()
    if Pattern_Configurator_Name == '':
        return
    if Same_Name_already_open(Pattern_Configurator_Name):
        P01.Workbooks(M30.FileNameExt(Pattern_Configurator_Name)).Activate()
        P01.Application.WindowState = xlNormal
    else:
        P01.Workbooks.Open(Pattern_Configurator_Name).RunAutoMacros(( xlAutoOpen ) )

def Copy_Pattern_Config():
    Pattern_Configurator_Name = String()
    #-------------------------------
    #
    Pattern_Configurator_Name = __Get_Pattern_Configurator_Name()
    ChDrive(Pattern_Configurator_Name)
    ChDir(FilePath(Pattern_Configurator_Name))
    Run(FileNameExt(Pattern_Configurator_Name) + '!Copy_Prog_If_in_LibDir')

# VB2PY (UntranslatedCode) Option Explicit
