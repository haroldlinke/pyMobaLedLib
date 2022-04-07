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

from proggen.M25_Columns import Make_sure_that_Col_Variables_match
from ExcelAPI.P01_Workbook import (TimeValue, ActiveCell, create_workbook, IsError, Cells, Range, Sheets, Rows, Columns, IsEmpty, val, VarType, ChDrive, Format, 
                                        MsgBox, InputBox, CWorkbook, CWorksheet, CRange, CRectangles, CSelection, CRow, CEntireRow, CColumn, CEntireColumn, CCell, CCellDict, CWorksheetFunction, CApplication, CFont, CActiveWindow, SoundLines)
from proggen.M09_Language import (Get_Language_Str,Set_Tast_Txt_Var, Get_ExcelLanguage, Set_Language_Def,Find_Language_Str_Row, Check_SIMULATE_LANGUAGE, Run)

from proggen.M02_Public import (Lib_Version_Nr, Test_Sufix, Prog_Version, Prog_Version_Nr, DEBUG_CHANGEEVENT, InoName_DCC, InoName__SX, Ino_Dir_LED, InoName_LED, MyExampleDir, AppLoc_Ardu, DestDir_LED, 
                                   INTPROGNAME, DSKLINKNAME, DefaultIcon, SECOND_PROG, SECOND_LINK, SECOND_ICON, WikiPg_Icon, WikiPg_Link, Env_USERPROFILE, Include_FileName, LED_CHANNELS, SERIAL_CHANNELS, SerialChannelPrefix,
                                   INTERNAL_COL_CNT, SF_LED_TO_VAR, SF_SERIAL_SOUND_PIN, SM_DIALOGDATA_ROW1,
                                   SM_Typ___COL, SM_Mode__COL, SM_LEDS__COL, SM_InCnt_COL, SM_OutCntCOL, SM_LocInCCOL, SM_Tmp8BtCOL, SM_SngLEDCOL, SM_DefCh_COL, SM_Type__COL, SM_ListS_COL, SM_TreeS_COL, SM_TMode_COL, SM_Pic_N_COL, SM_Macro_COL, SM_FindN_COL, SM_Name__COL, SM_Group_COL,
                                   SM_LName_COL, SM_ShrtD_COL,SM_DetailCOL, DeltaCol_Lib_Macro_Lang,
                                   MST_None, MST_CTR_NONE, MST_CTR_ON, MST_CTR_OFF, MST_PREVENT_STORE,
                                   SST_NONE, SST_COUNTER_ON, SST_COUNTER_OFF, SST_S_ONOFF, SST_TRIGGER, SST_DISABLED,  AUTOSTORE_ON, AUTOSTORE_OFF,
                                   Enable_Col, Header_Row, FirstDat_Row, SH_VARS_ROW, PAGE_ID_COL, AllData_PgIDs, Prog_for_Right_Ardu, MAX_ROWS, MAX_COLUMNS, Hook_CHAR, SPARE_ROWS,
                                   LANGUAGES_SH, LIBMACROS_SH, PAR_DESCR_SH, LIBRARYS__SH, PLATFORMS_SH, START_SH, ConfigSheet,
                                   ComPortfromOnePage, MouseHook_Store_Page,
                                   BOARD_NANO_OLD, BOARD_NANO_FULL, BOARD_NANO_NEW, BOARD_NANO_EVERY, BOARD_UNO_NORM, BOARD_ESP32, BOARD_PICO,  AUTODETECT_STR, DEFARDPROG_STR,
                                   L2V_COM_OPERATORS, MB_LED_NR_STR, MB_LED_PIN_NR, USE_SWITCH_AND_LED_ARRAY,
                                   Read_Sketchbook_Path_from_preferences_txt, Get_Sketchbook_Path, Get_BoardTyp,
                                   Get_SrcDirInLib,Get_DestDir_All, Get_MobaUserDir, Get_Ardu_LibDir, Get_SrcDirExamp)

from proggen.M30_Tools import (SM_CXSCREEN, SM_CYSCREEN, SM_CMONITORS, SW_NORMAL, KS_SHIFT_KEY, KS_CTRL_KEY, KS_ALT_KEY, WinPos_T, Start_ms_Timer, Get_ms_Duratio, AddSpaceToLen, AddSpaceToLenLeft, IsArrayEmpty, LastUsedRow, LastUsedColumn, LastColumnDatSheet, LastUsedRowIn,
                                   LastUsedColumnInRow, LastUsedColumnIn, LastFilledRowIn, LastFilledColumnIn,  LastFilledColumn, First_Change_in_Line, LastFilledRowIn_ChkAll, DelLast, DelAllLast, Center_Form, Restore_Pos_or_Center_Form, Store_Pos,
                                   Replace_Multi_Space, CellLinesSum, Is_Contained_in_Array, Is_Contained_in_Array, Get_Position_In_Array, IsInArray, Hide_and_Move_up, FindHeadCol,
                                   InputBoxMov, MsgBoxMov, ShowHourGlassCursor, IsHourGlassCursor, EndProg, ClearStatusbar, Show_Status_for_a_while, All_Borderlines, FileNameExt, FilePath, FileName, Same_Name_already_open, SheetEx, Protect_Active_Sheet,
                                   ColumnLetters, ColumnLettersFromNr, DisableFiltersInSheet, isVariantArray, F_shellExec, F_shellRun, Read_File_to_String, Get_Ini_Entry, Debug_Print_Arr, DeleteElementAt, InsertElementAt,
                                   GetPathOnly, CreateFolder, UnzipAFile, isInitialised, SplitMultiDelims, SplitEx, Get_Primary_Monitor_Pixel_Cnt_X, Array_BubbleSort, Button_Setup, Bring_to_front, Replicate, ConvertToUTF8, ConvertToUTF8Str, ConvertFromUTF8,
                                   ConvertUTF8Str, Dir_is_Empty, Get_First_SubDir, VersionStr_is_Greater, Del_Folder, Get_OperatingSystem, Win10_or_newer, Check_Version, Valid_Excel, Clear_Platform_Parameter_Cache, Get_Current_Platform_String,
                                   Get_Current_Platform_Bool, Get_Current_Platform_Int, Function, Get_Platform_String, Get_Platform_Bool, Get_Platform_Int, AliasToPin, Get_Act_ms)

import proggen.M02_Public as M02
import proggen.M02_global_variables as M02GV
import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
import proggen.M09_SelectMacro_Treeview as M09SMT
import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80

import proggen.Prog_Generator as PG

import ExcelAPI.P01_Workbook as P01

from ExcelAPI.X01_Excel_Consts import *


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
    Make_sure_that_Col_Variables_match()
    fn_return_value = ( ActiveCell().Row >= M02.FirstDat_Row )
    return fn_return_value

def Get_Description_Range_from_Act_Row():
    fn_return_value = None
    #------------------------------------------------------------
    Make_sure_that_Col_Variables_match()
    fn_return_value = Cells(ActiveCell().Row, M25.Descrip_Col)
    return fn_return_value

def Write_Macro_to_Act_Row(MacroTxt, LEDs, InCnt, LocInCh, Comment="", WrapText=False):
    #Row = Long()

    #LEDs_Channel = Long()
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Make_sure_that_Col_Variables_match()
    Row = ActiveCell.Row
    if Cells(Row, M25.LED_Cha_Col) == '':
        while not ResOk:
            Res = InputBox(Get_Language_Str('Welcher LED Kanal soll verwendet werden?' + vbCr + '  0 = Standard LEDs' + vbCr + '  1 = Taster LEDs' + vbCr + '  2 = Optionale LED Gruppe 2' + vbCr + '  3 = Optionale LED Gruppe 2' + vbCr + vbCr + 'LED Kanal (0..3):'), Get_Language_Str('Eingabe des LED Kanals'), 0)
            Res = Trim(Res)
            if Res == '':
                return
            if IsNumeric(Res) and val(Res) >= 0 and val(Res) < M02.LED_CHANNELS:
                ResOk = True
        Cells[Row, M25.LED_Cha_Col] = val(Res)
    M25.LEDs_Channel = val(Cells(Row, M25.LED_Cha_Col))
    Cells[Row, Enable_Col] = ChrW(M02.Hook_CHAR)
    Cells[Row, M25.Config__Col] = MacroTxt
    Cells[Row, M25.Config__Col].WrapText = WrapText
    Cells[Row, M25.LEDs____Col] = LEDs
    Cells[Row, M25.InCnt___Col] = InCnt
    Cells[Row, M25.LocInCh_Col] = LocInCh
    if Comment != '':
        Cells[Row, M25.Descrip_Col] = Comment

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
        Select_ProgGen_Dest_Form.Check_and_Start(Macro_Callback)
    else:
        Select_ProgGen_Src_Form.Check_and_Start(Macro_Callback)

def __Get_Pattern_Configurator_Name():
    fn_return_value = None
    #---------------------------------------------------------
    if Same_Name_already_open(__Default_Pattern_Configurator_Name):
        fn_return_value = P01.Workbooks(__Default_Pattern_Configurator_Name).FullName
    else:
        Path = Get_DestDir_All()
        # Check if it exists in the user dir
        FullPath = Path + __Default_Pattern_Configurator_Name
        if Dir(FullPath) == '':
            # Check if it exists in the lib dir
            Path = Get_SrcDirInLib()
            FullPath = Path + __Default_Pattern_Configurator_Name
            if Dir(FullPath) == '':
                MsgBox(Get_Language_Str('Fehler: Das Programm \'') + __Default_Pattern_Configurator_Name + '\'' + vbCr + Get_Language_Str('existiert nicht im Standard Verzeichnis:') + vbCr + '  \'' + Path + '\'', vbCritical, Get_Language_Str('Fehler ') + __Default_Pattern_Configurator_Name + Get_Language_Str(' nicht vorhanden'))
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
        P01.Workbooks(FileNameExt(Pattern_Configurator_Name)).Activate()
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
