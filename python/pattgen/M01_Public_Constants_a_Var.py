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

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

"""# VB2PY (CheckDirective) VB directive took path 1 on USE_SKETCHBOOK_DIR
 Proportional column width display in Adjust_Column_With_to_Duration()
 The quotiont Max_t / Min_t define the minimal column width.
Public Button_Init_Proc_Finished As Boolean                                                     ' 05.01.22: Juergen call init function synchronous
 Sheet names:
 COM Port:
---------------------------------------------------------------------
----------------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on USE_SKETCHBOOK_DIR
"""

Lib_Version_Nr = '3.1.0'
Exp_Prog_Gen_Version = Lib_Version_Nr
DEBUG_CHANGEEVENT = False
__USE_SKETCHBOOK_DIR = True
__SrcDirInLib = '\\libraries\\MobaLedLib\\extras\\'
__DestDir_All = '\\MobaLedLib\\Ver_' + Lib_Version_Nr + '\\'
AppLoc_Ardu = '\\AppData\\Local\\Arduino15\\'
INTPROGNAME = 'Pattern_Configurator'
DSKLINKNAME = 'MobaLedLib Pattern_Configurator'
DefaultIcon = 'Icons\\05_Gerald_Patt.ico'
SECOND_PROG = 'Prog_Generator_MobaLedLib'
SECOND_LINK = 'Prog_Generator MobaLedLib'
SECOND_ICON = 'Icons\\05_Gerald_Prog.ico'
WikiPg_Icon = 'Icons\\WikiMLL_v5.ico'
WikiPg_Link = 'https://wiki.mobaledlib.de/'
Env_USERPROFILE = 'USERPROFILE'
ACT_MLL_pcf_Version = 1
MacEnab_Rng = 'E1'
LED_Cnt_Rng = 'E5'
BitsVal_Rng = 'E6'
WertMin_Rng = 'E7'
WertMax_Rng = 'E8'
AnaFade_Rng = 'E11'
GrafDsp_Rng = 'E14'
ErgebnisRng = 'E20'
Macro_N_Rng = 'E22'
PARAMETER_RANGE = 'D2:D22'
PARAMETER_Col = 4
PARAMETER_Ro11 = 2
PARAMETER_Ro1N = 24
Goto_Txt_col = 5
LED_Text_Col = 5
GotoModeRow = 12
GrafDsp_Row = 14
GrafDsp_Col = 6
TableEmptyMsgRng = 'F44'
FirstLEDTabRANGE = 'E50'
LEDsRANGE = 'E50:EW304'
LEDs__TAB = 'F50:EW304'
LED_NR_ROW = 49
LEDsTAB_R = 50
LEDsTAB_C = 6
Last_LEDsCol = 153
Last_LEDs_ChkAttrCol = 27
Dauer_Rng = 'F28:AI28'
Dauer_Row = 28
Dauer_Col1 = 6
Dauer__Cnt = 30
GoTo_RNG = 'F47:EW47'
GoTo_Row = 47
GoTo_Col1 = 6
NormWidth_MM = 4
Min_Width_MM = 50
NormColWidth = 6.71
Min_ColWidth = 0.8
Transp_Start_Graph = 0.7
ExampleDir = 'Pattern_Config_Examples'
MyExampleDir = 'MyPattern_Config_Examples'
OVERWRITE_EXISTING_PIC = False
pcfSep = 175
FROM_PAT_CONFIG_TXT = ' (pc)'
WertMinMaxValid = String()
WertMin = Integer()
WertMax = Integer()
BitsVal = Integer()
LED_Scale = Double()
LED_Offset = Double()
StartMax = Double()
StartMin = Double()
SaveDirCreated = Boolean()
ExampleName = String()
StdDescStart = 'Mit diesem Blatt kann die Konfiguration'
StdDescEdges = '497;0;767.4421;142.8818'
MAIN_SH = 'Main'
LANGUAGES_SH = 'Languages'
PAR_DESCRIPTION_SH = 'Par_Description'
GOTO_ACTIVATION_SH = 'Goto_Activation_Entries'
SPECIAL_MODEDLG_SH = 'Special_Mode_Dlg'
ComPortfromOnePage = MAIN_SH
Page_ID = 'DCC'
COMPort_COL = 30
COMPrtR_COL = 31
COMPrtT_COL = 32
BuildOT_COL = 33
SH_VARS_ROW = 1
BOARD_NANO_OLD = '--board arduino:avr:nano:cpu=atmega328old'
BOARD_NANO_NEW = '--board arduino:avr:nano:cpu=atmega328'
BOARD_UNO_NORM = '--board arduino:avr:uno'
AUTODETECT_STR = 'AutoDet'
DEFARDPROG_STR = '--pref programmer=arduino:arduinoisp'
MouseHook_Store_Page = 'Main'
Sketchbook_Path = String()

def Read_Sketchbook_Path_from_preferences_txt():
    fn_return_value = None
    Name = String()

    FileStr = String()
    #---------------------------------------------------------------------
    # Attention: The file uses UTF8
    Name = Environ(Env_USERPROFILE) + AppLoc_Ardu + 'preferences.txt'
    Debug.Print("Read_Sketchbook_Path_from_preference_txt - Name:"+Name)
    FileStr = Read_File_to_String(Name)
    if FileStr != '#ERROR#':
        Sketchbook_Path = ConvertUTF8Str(Get_Ini_Entry(FileStr, 'sketchbook.path='))
        #ThisWorkbook.Sheets(LIBRARYS__SH).Range("Sketchbook_Path") = Sketchbook_Path
        if Sketchbook_Path == '#ERROR#':
            MsgBox(Replace(Get_Language_Str('Fehler: beim lesen des \'sketchbook.path\' in \'#1#\''), '#1#', Name), vbCritical, Get_Language_Str('Fehler beim lesen der Datei:') + ' \'preferences.txt\'')
            return fn_return_value
        if Left(Sketchbook_Path, 2) == '\\\\':
            MsgBox(Get_Language_Str('Fehler: Der Arduino \'sketchbook.path\' darf kein Netzlaufwerk sein:') + vbCr + '  \'' + Sketchbook_Path + '\'', vbCritical, Get_Language_Str('Ungültiger Arduino \'sketchbook.path\''))
            return fn_return_value
        CreateFolder(Sketchbook_Path + '\\')
        fn_return_value = True
    return fn_return_value

def Get_Sketchbook_Path():
    fn_return_value = None
    #----------------------------------------------
    Debug.Print('Get_Sketchbook_Path called')
    if Sketchbook_Path == '':
        Read_Sketchbook_Path_from_preferences_txt()()
    fn_return_value = Sketchbook_Path
    return fn_return_value

def Get_SrcDirInLib():
    fn_return_value = None
    fn_return_value = Get_Sketchbook_Path() + __SrcDirInLib
    return fn_return_value

def Get_DestDir_All():
    fn_return_value = None
    fn_return_value = Get_Sketchbook_Path() + __DestDir_All
    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit

