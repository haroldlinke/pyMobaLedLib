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




def __TestCreateDesktopShortcut():
    #UT------------------------------------
    CreateDesktopShortcut()('Aber Hallo', P01.ThisWorkbook.Name, 'mll_platine_ausschnitt3_icon.ico')

def CreateDesktopShortcut(LinkName, BookFullName, IconName):
    return True #*HL
    fn_return_value = None
    location = 'Desktop'

    LinkExt = '.lnk'

    oWsh = Object()

    oShortcut = Object()

    Sep = String()

    Path = String()

    DesktopPath = String()

    Shortcut = String()
    #---------------------------------------------------------------------------------------------------------------
    # Create a custom icon shortcut on the users desktop
    # Constant string values, you can replace "Desktop"
    # with any Special Folders name to create the shortcut there
    # Object variables
    # String variables
    # Initialize variables
    Sep = P01.Application.PathSeparator
    Path = P01.ThisWorkbook.Path
    # VB2PY (UntranslatedCode) On Error GoTo ErrHandle
    # The WScript.Shell object provides functions to read system
    # information and environment variables, work with the registry
    # and manage shortcuts
    oWsh = CreateObject('WScript.Shell')
    DesktopPath = oWsh.SpecialFolders(location)
    # Get the path where the shortcut will be located
    Shortcut = DesktopPath + Sep + LinkName + LinkExt
    oShortcut = oWsh.CreateShortcut(Shortcut)
    # Link it to this file
    with_0 = oShortcut
    with_0.TargetPath = BookFullName
    with_0.IconLocation = Path + Sep + IconName
    with_0.Save()
    # Explicitly clear memory
    oWsh = None
    oShortcut = None
    fn_return_value = True
    return fn_return_value
    #return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit