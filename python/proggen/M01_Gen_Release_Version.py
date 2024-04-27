# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 4.15
# * Author: Harold Linke
# * Date: March 13, 2022
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
# 2021-01-07 v4.02 HL: - Else: check done, first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

""" Call the following function to generate a release version

"""
import proggen.M02_Public as M02
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header as M06
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
#import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_SelectMacro_Treeview as M09SMT
import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80
import proggen.D06_Userform_House as D06
import proggen.D07_Userform_Other as D07
import mlpyproggen.Prog_Generator as PG

import ExcelAPI.XLA_Application as P01

from ExcelAPI.XLC_Excel_Consts import *




def __Gen_Release_Version():
    #--------------------------------
    __Release_or_Debug_Version(True)
    M09.Set_Language_Def(- 1)
    M09SMT.Set_Lib_Macros_Test_Language(- 1)

def __Gen_Debug_Version():
    #------------------------------
    __Release_or_Debug_Version(False)

def __Update_Version_InActSheet(SetCursorPos):
    
    return #*HL
    #------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo ErrMsg
    P01.ActiveSheet.Shapes.Range(Array('Version_TextBox')).Select()
    P01.Selection.ShapeRange[1].TextFrame2.TextRange.Characters.Text = Prog_Version
    P01.ActiveSheet.Hyperlinks.Add(Anchor=Selection.ShapeRange(1), Address='', ScreenTip=Str(Now))
    # VB2PY (UntranslatedCode) On Error GoTo 0
    P01.Range('A1').Activate()
    # Set Cursor out of the version text box
    if SetCursorPos != '':
        P01.Range(SetCursorPos).Select()
    else:
        Row = M02.FirstDat_Row
        while P01.Cells(Row, 1).EntireRow.Hidden:
            Row = Row + 1
        P01.Cells(Row, M25.Descrip_Col).Select()
    return
    P01.MsgBox('Error: \'Version_TextBox\' not found in sheet \'' + P01.ActiveSheet.Name + '\'', vbCritical, 'Internal Error')

def __Release_or_Debug_Version(Release):
    #Sh = Variant()

    #LastSheet = String()
    #-------------------------------------------------------
    LastSheet = P01.ActiveSheet.Name
    # AddImagesToTreeForm ".\Icons", True                                     ' 28.11.21: For some reasons this call generates an error. The same function could be called by the "Read Pictures" button in the "Lib_Macros" sheet without problems ?!?
    #           => It has to be called manually
    if Release:
        PG.ThisWorkbook.Sheets(M02.LANGUAGES_SH).Visible = False
        PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH).Visible = False
        PG.ThisWorkbook.Sheets(M02.PAR_DESCR_SH).Visible = False
        PG.ThisWorkbook.Sheets(M02.LIBRARYS__SH).Visible = False
        PG.ThisWorkbook.Sheets(M02.PLATFORMS_SH).Visible = False
    
    for Sh in PG.ThisWorkbook.sheets:
        if M28.Is_Data_Sheet(Sh):
            Sh.Select()
            P01.ActiveWindow.Zoom = 100
            P01.ActiveWindow.ScrollColumn = 1
            M25.Make_sure_that_Col_Variables_match(Sh)
            __Update_Version_InActSheet('')
            # Show / Hide the internal variables
            #with_0 = P01.Range(P01.Cells(M02.SH_VARS_ROW, 1), P01.Cells(M02.SH_VARS_ROW, M30.LastUsedColumn())).Font
            #if Release:
            #    with_0.ThemeColor = xlThemeColorDark1
            #else:
            #    with_0.ColorIndex = xlAutomatic
            # This internal data are always shown
            #P01.CellDict[M02.SH_VARS_ROW, M25.BUILDOP_COL].Font.ColorIndex = xlAutomatic
            #P01.CellDict[M02.SH_VARS_ROW, M25.COMPort_COL].Font.ColorIndex = xlAutomatic
            #P01.CellDict[M02.SH_VARS_ROW, M25.COMPrtR_COL].Font.ColorIndex = xlAutomatic
            #P01.CellDict[M02.SH_VARS_ROW, M25.BUILDOpRCOL].Font.ColorIndex = xlAutomatic
            # Show / Hide the internal columns
            #P01.CellDict[1, M25.InCnt___Col].EntireColumn.Hidden = False
            #P01.CellDict[1, M25.LocInCh_Col].EntireColumn.Hidden = False
            #           have been hidden in release mode
            # Build otions
            P01.CellDict[M02.SH_VARS_ROW, M25.BUILDOP_COL] = '\'' + M02.AUTODETECT_STR + ' ' + M02.BOARD_NANO_OLD + ' ' + M02.DEFARDPROG_STR
            if M25.Page_ID != 'CAN':
                P01.CellDict[M02.SH_VARS_ROW, M25.BUILDOpRCOL] = '\'' + M02.AUTODETECT_STR + ' ' + M02.BOARD_NANO_OLD + ' ' + M02.DEFARDPROG_STR
            # Activate the Filter                                              ' 02.03.20: ' 14.06.20: Filters ar no longer used in the release version
            #Range(Cells(Header_Row, Enable_Col), Cells(LastUsedRow(), LastUsedColumn())).AutoFilter Field:=2, Criteria1:="=B01", Operator:=xlOr, Criteria2:="="
    # Show / Hide the internal sheets
    PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH).Visible = not Release
    PG.ThisWorkbook.Sheets(M02.PAR_DESCR_SH).Visible = not Release
    PG.ThisWorkbook.Sheets(M02.PLATFORMS_SH).Visible = not Release
    #Sheets("Farbentest").Visible = Not Release
    # Start sheet
    #PG.ThisWorkbook.Sheets(M02.START_SH).Select()
    #P01.ActiveSheet.Unprotect()
    #__Update_Version_InActSheet('M7')
    #if Release:
    #    PG.ThisWorkbook.Sheets(M02.START_SH).Protect(DrawingObjects=True, Contents=True, Scenarios=True)
    #    PG.ThisWorkbook.ActiveWindow.DisplayHeadings = False
    #else:
    #    PG.ThisWorkbook.Sheets(M02.START_SH).Unprotect()
    if Release:
        __Set_Config_Default_Values_for_Release()
    M28.Clear_COM_Port_Check_and_Set_Cursor_in_all_Sheets(Release) 
    if Release:
        # move cursor to begin of sheet data                               ' 10.03.21  Juergen
        for Sh in PG.ThisWorkbook.sheets:
            if M28.Is_Data_Sheet(Sh):
                Sh.Select()
                factor = 10
                M25.Make_sure_that_Col_Variables_match(Sh)
                P01.Columns(M02.Enable_Col).ColumnWidth = 5.8*factor #*HL
                if Sh.Name == 'Examples':
                    P01.Columns(M25.Filter__Col).ColumnWidt = 11*factor
                    P01.Columns(M25.Inp_Typ_Col).ColumnWidth = 22*factor
                else:
                    P01.Columns(M25.Filter__Col).ColumnWidth = 5.8*factor
                    P01.Columns(M25.Inp_Typ_Col).ColumnWidth = 22*factor
                if M25.Page_ID != 'Selectrix':
                    P01.Columns(M25.DCC_or_CAN_Add_Col).ColumnWidth = 11.57*factor
                else:
                    P01.Columns(M25.SX_Channel_Col).ColumnWidth = 13.29*factor
                    P01.Columns(M25.SX_Bitposi_Col).ColumnWidth = 9.57*factor
                P01.Columns(M25.Start_V_Col).ColumnWidth = 4.57*factor
                P01.Columns(M25.Descrip_Col).ColumnWidth = 43.5*factor
                P01.Columns(M25.Dist_Nr_Col).ColumnWidth = 8*factor
                P01.Columns(M25.Conn_Nr_Col).ColumnWidth = 8.86*factor
                P01.Columns(M25.Config__Col).ColumnWidth = 60*factor
                P01.Columns(M25.LED_Nr__Col).ColumnWidth = 4.71*factor
                P01.Columns(M25.LEDs____Col).ColumnWidth = 7*factor
                P01.Columns(M25.InCnt___Col).ColumnWidth = 4.71*factor
                P01.Columns(M25.LocInCh_Col).ColumnWidth = 4.71*factor
                P01.Columns(M25.LED_Cha_Col).ColumnWidth = 4.71*factor
                P01.Cells(M02.Header_Row + 1, M25.Descrip_Col).Select()
        #PG.ThisWorkbook.Sheets(M02.START_SH).Select()
    else:
        PG.ThisWorkbook.Sheets(LastSheet).Select()
    if Release:
        M60.Write_Default_CheckColors_Parameter_File()
        # 01.12.19:
        
def set_columnwidth(Sh):
    if M28.Is_Data_Sheet(Sh):
        Sh.Select()
        factor = 10
        M25.Make_sure_that_Col_Variables_match(Sh)
        P01.Columns(M02.Enable_Col).ColumnWidth = 5.8*factor #*HL
        if Sh.Name == 'Examples':
            P01.Columns(M25.Filter__Col).ColumnWidt = 11*factor
            P01.Columns(M25.Inp_Typ_Col).ColumnWidth = 16*factor
        else:
            P01.Columns(M25.Filter__Col).ColumnWidth = 5.8*factor
            P01.Columns(M25.Inp_Typ_Col).ColumnWidth = 12*factor
        if M25.Page_ID != 'Selectrix':
            P01.Columns(M25.DCC_or_CAN_Add_Col).ColumnWidth = 11.57*factor
        else:
            P01.Columns(M25.SX_Channel_Col).ColumnWidth = 13.29*factor
            P01.Columns(M25.SX_Bitposi_Col).ColumnWidth = 9.57*factor
        P01.Columns(M25.Start_V_Col).ColumnWidth = 4.57*factor
        P01.Columns(M25.Descrip_Col).ColumnWidth = 43.5*factor
        P01.Columns(M25.Dist_Nr_Col).ColumnWidth = 8*factor
        P01.Columns(M25.Conn_Nr_Col).ColumnWidth = 8.86*factor
        P01.Columns(M25.Config__Col).ColumnWidth = 60*factor
        P01.Columns(M25.LED_Nr__Col).ColumnWidth = 4.71*factor
        P01.Columns(M25.LEDs____Col).ColumnWidth = 7*factor
        P01.Columns(M25.InCnt___Col).ColumnWidth = 4.71*factor
        P01.Columns(M25.LocInCh_Col).ColumnWidth = 4.71*factor
        P01.Columns(M25.LED_Cha_Col).ColumnWidth = 4.71*factor
        P01.Cells(M02.Header_Row + 1, M25.Descrip_Col).Select() 

def Set_Config_Default_Values_at_Program_Start():
    #------------------------------------------------------
    M28.Set_Bool_Config_Var('Lib_Installed_other', False)

def __Set_Config_Default_Values_for_Release():
    #--------------------------------------------------
    M28.Set_String_Config_Var('MinTime_House', '')
    M28.Set_String_Config_Var('MaxTime_House', '')
    M28.Set_String_Config_Var('DCC_Offset', '')
    M28.Set_String_Config_Var('Color_Test_Mode', '1')
    M28.Set_String_Config_Var('USE_SPI_Communication', '0')
    M28.Set_String_Config_Var('Use_Excel_Console', '0')
    M28.Set_String_Config_Var('LEDNr_Display_Type', '1')
    M28.Set_String_Config_Var('Expert_Mode_aktivate', '')
    M28.Set_String_Config_Var('Use_TreeView_for_Macros', '')
    M28.Set_String_Config_Var('Show_Icon_Column', '1')
    M28.Set_String_Config_Var('Show_Simple_Names', '1')
    M28.Set_String_Config_Var('Show_Macros_Column', '1')
    M28.Set_String_Config_Var('Use_PlatformIO', '0')
    M28.Set_String_Config_Var('SimPosX', '800')
    M28.Set_String_Config_Var('SimPosY', '200')
    M28.Set_String_Config_Var('SimLedsX', '8')
    M28.Set_String_Config_Var('SimLedsY', '8')
    M28.Set_String_Config_Var('SimLedSize', '24')
    M28.Set_String_Config_Var('SimAutostart', '0')
    M28.Set_String_Config_Var('SimOffset', '0')
    M28.Set_String_Config_Var('SimOnTop', '1')    
    #M28.Set_String_Config_Var('GEN_BUTTON_RELEASE_COM', '0')
# VB2PY (UntranslatedCode) Option Explicit
