# -*- coding: utf-8 -*-
#
#         M02_Public
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
# 2022-01-07 v4.02 HL: - Else:. ByRef check done  - first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *
#from proggen.M30_Tools import *

#from proggen.M30_Tools import Read_File_to_String

#import proggen.Prog_Generator as PG

#import proggen.M02_Public as M02
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header as M06
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
#import proggen.M07_COM_Port as M07
#import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
#import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
#import proggen.M27_Sheet_Icons as M27
#import proggen.M28_divers as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Mulitplexer as M80

from ExcelAPI.X01_Excel_Consts import *
import ExcelAPI.P01_Workbook as P01


"""# VB2PY (CheckDirective) VB directive took path 1 on USE_SKETCHBOOK_DIR
"""
# ####################################################
#
# Public Const
#
# ##################################################### Public Const

Lib_Version_Nr = '3.1.0'                                    # If changed check also "Exp_Prog_Gen_Version" in Pattern_Configurator
Test_Sufix = 'F4'                                            # The Excel programs use the same version number than the library to avoid confusion
Prog_Version = 'Ver. ' + Lib_Version_Nr + Test_Sufix        # A sufix could be used for beta version
Prog_Version_Nr = Lib_Version_Nr + Test_Sufix               # Call Gen_Release_Version() to update all sheets
DEBUG_CHANGEEVENT = False
DEBUG_DCCSEND = False

InoName_DCC = '23_A.DCC_Interface.ino'
InoName__SX = '23_A.Selectrix_Interface.ino'

Ino_Dir_LED = 'LEDs_Autoprog/'
InoName_LED = 'LEDs_AutoProg.ino'
Cfg_Dir_LED = "Configuration/"
CfgName_LED = "Configuration.cpp"
CfgBuild_Script = "build.cmd"

USE_SKETCHBOOK_DIR = True

SrcDirInLib = '/libraries/MobaLedLib/extras/'
DestDir_All = '/MobaLedLib/Ver_' + Lib_Version_Nr + '/'
MobaUserDir = '/'
Ardu_LibDir = '/libraries/'
SrcDirExamp = '/libraries/MobaLedLib/examples/'

MyExampleDir = 'Prog_Generator_Data'

AppLoc_Ardu = '/AppData/Local/Arduino15/'

DestDir_LED = DestDir_All + 'LEDs_AutoProg'

INTPROGNAME = 'Prog_Generator'
DSKLINKNAME = 'Prog_Generator MobaLedLib'
DefaultIcon = 'Icons/05_Gerald_Prog.ico'

SECOND_PROG = 'Pattern_Configurator'
SECOND_LINK = 'MobaLedLib Pattern_Configurator'
SECOND_ICON = 'Icons/05_Gerald_Patt.ico'

WikiPg_Icon = 'Icons/WikiMLL_v5.ico'
WikiPg_Link = 'https://wiki.mobaledlib.de/'

Env_USERPROFILE = 'USERPROFILE'

Include_FileName = 'LEDs_AutoProg.h'

LED_CHANNELS = 10                                       #*HL 18.02.22: increase to 10 (8 Led, 1 DMX, 1 virtuell)
SERIAL_CHANNELS = 8
SerialChannelPrefix = 'S'
INTERNAL_COL_CNT = 1 + 4                                # 03.04.21: Juergen Internal used columns in case of compact LedNr display, which should not be modified

# Special function prefixes
SF_LED_TO_VAR = 'LED_to_Var('
SF_SERIAL_SOUND_PIN = 'SOUND_CHANNEL_DEFINITON('

# Sheet Lib_Macros: (The Sheet can not be changed by the USER => We keep the constants)
SM_DIALOGDATA_ROW1 = 4

SM_Typ___COL = 1
SM_Mode__COL = 2
SM_LEDS__COL = 3
SM_InCnt_COL = 4
SM_OutCntCOL = 5
SM_LocInCCOL = 6
SM_Tmp8BtCOL = 7
SM_SngLEDCOL = 8
SM_DefCh_COL = 9
SM_Type__COL = 10
SM_ListS_COL = 11
SM_TreeS_COL = 12
SM_TMode_COL = 13
SM_Pic_N_COL = 14
SM_Macro_COL = 15
SM_FindN_COL = 16
SM_Name__COL = 17
SM_Group_COL = 18
SM_LName_COL = 19
SM_ShrtD_COL = 20
SM_DetailCOL = 21

DeltaCol_Lib_Macro_Lang = 4

# Macro Store Types
MST_None = 0
MST_CTR_NONE = 1
MST_CTR_ON = 2
MST_CTR_OFF = 3
MST_PREVENT_STORE = 4

# Status Storage Types
SST_NONE = 0
SST_COUNTER_ON = 1
SST_COUNTER_OFF = 2
SST_S_ONOFF = 3
SST_TRIGGER = 4
SST_DISABLED = 5

AUTOSTORE_ON = '*'
AUTOSTORE_OFF = '0'

# Valid for all sheets
Enable_Col = 2

Header_Row = 2
FirstDat_Row = Header_Row + 1

SH_VARS_ROW = 1                                 # This row contains some sheet specific varaibles. The text uses white color => It' not visible
PAGE_ID_COL = 2                                 # This cell contains a page ID to idetify the sheet

AllData_PgIDs = ' DCC Selectrix CAN '
Prog_for_Right_Ardu = ' DCC Selectrix Loconet '

MAX_ROWS = 1048576
MAX_COLUMNS = 16384

Hook_CHAR = 252 #61692

SPARE_ROWS = 3                                  # Number of spare rows which are generated if data are entered in a new line

# Sheet names:
LANGUAGES_SH = 'Languages'
LIBMACROS_SH = 'Lib_Macros'
PAR_DESCR_SH = 'Par_Description'
LIBRARYS__SH = 'Libraries'
PLATFORMS_SH = 'Platform_Parameters'
START_SH = 'Start'
ConfigSheet = 'Config'

# Variables
SelectMacro_Res = String()
Userform_Res = String()
Userform_Res_Address = String()

DialogGuideRes = int()
#*HL HouseForm_Pos = WinPos_T()
#*HL OtherForm_Pos = WinPos_T()

Last_SelectedNr_Valid = Boolean()
Last_SelectedNr = int()

ComPortfromOnePage = ''

MouseHook_Store_Page = 'Start'                      # This page is used to store the MouseHook. There must be a named range called "MouseHook".

BOARD_NANO_OLD = '--board arduino:avr:nano:cpu=atmega328old'
BOARD_NANO_FULL = '--board arduino:avr:nano:cpu=atmega328fullmem'
BOARD_NANO_NEW = '--board arduino:avr:nano:cpu=atmega328'
BOARD_NANO_EVERY = '--board arduino:megaavr:nona4809:mode=off'
BOARD_UNO_NORM = '--board arduino:avr:uno'
BOARD_ESP32 = '--board esp32:esp32:esp32:PSRAM=disabled,PartitionScheme=default,CPUFreq=240,FlashMode=qio,FlashFreq=80,FlashSize=4M,UploadSpeed=921600,DebugLevel=none'
BOARD_PICO = '--board rp2040:rp2040:rpipico:flash=2097152_0,freq=125,dbgport=Disabled,dbglvl=None'
AUTODETECT_STR = 'AutoDet'
DEFARDPROG_STR = '--pref programmer=arduino:arduinoisp'

Sketchbook_Path = String()

L2V_COM_OPERATORS = '< > = != & !&'
MB_LED_NR_STR = 'D2 D3 D4 D5 A3 A2 A1 D7 D8 D9 D10 D11 D12 D13 A4 A5 A0'
MB_LED_PIN_NR = '0  1  2  3  4  5  6  7  8  9  10  11  12  13  14 15 16'

# ####################################################
#
# Public Functions
#
# ####################################################


def Read_Sketchbook_Path_from_preferences_txt():
    global Sketchbook_Path
        
    Name = String()

    FileStr = String()
    #---------------------------------------------------------------------
    # Attention: The file uses UTF8
    Name = Environ(Env_USERPROFILE) + AppLoc_Ardu + 'preferences.txt'
    Debug.Print("Read_Sketchbook_Path_from_preference_txt - Name:"+Name)
    FileStr = M30.Read_File_to_String(Name)
    if FileStr != '#ERROR#':
        Sketchbook_Path = M30.Get_Ini_Entry(FileStr, 'sketchbook.path=')
        logging.debug("Sketchbookpath="+Sketchbook_Path)
        #*HL Sketchbook_Path = M30.ConvertUTF8Str(M30.Get_Ini_Entry(FileStr, 'sketchbook.path='))
        #ThisWorkbook.Sheets(LIBRARYS__SH).Range("Sketchbook_Path") = Sketchbook_Path
        if Sketchbook_Path == '#ERROR#':
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: beim lesen des \'sketchbook.path\' in \'#1#\''), "#1#", Name), vbCritical, M09.Get_Language_Str('Fehler beim Lesen der Datei:') + ' \'preferences.txt\'')
            return fn_return_value
        if Left(Sketchbook_Path, 2) == '\\\\':
            P01.MsgBox(M09.Get_Language_Str('Fehler: Der Arduino \'sketchbook.path\' darf kein Netzlaufwerk sein:') + vbCr + '  \'' + Sketchbook_Path + '\'', vbCritical, M09.Get_Language_Str('Ungültiger Arduino \'sketchbook.path\''))
            return fn_return_value
        M30.CreateFolder(Sketchbook_Path + '/')
        fn_return_value = True
    return fn_return_value

def Get_Sketchbook_Path():
    global Sketchbook_Path
    #----------------------------------------------
    Debug.Print('Get_Sketchbook_Path called')
    if Sketchbook_Path == '':
        Read_Sketchbook_Path_from_preferences_txt()
    fn_return_value = Sketchbook_Path
    return fn_return_value

def Get_SrcDirInLib():
    fn_return_value = Get_Sketchbook_Path() + SrcDirInLib
    return fn_return_value

def Get_DestDir_All():
    fn_return_value = Get_Sketchbook_Path() + DestDir_All
    return fn_return_value

def Get_MobaUserDir():
    fn_return_value = Get_Sketchbook_Path() + MobaUserDir
    return fn_return_value

def Get_Ardu_LibDir():
    fn_return_value = Get_Sketchbook_Path() + Ardu_LibDir
    return fn_return_value

def Get_SrcDirExamp():
    fn_return_value = Get_Sketchbook_Path() + SrcDirExamp
    return fn_return_value

def Get_BoardTyp():
    #---------------------------------------
    # The build options for the ESP32 are something like "esp32:esp32:esp32..."
    fn_return_value = 'AM328'
    if InStr(P01.Cells(SH_VARS_ROW, M25.BUILDOP_COL), 'esp32') > 0:
        fn_return_value = 'ESP32'
    elif InStr(P01.Cells(SH_VARS_ROW, M25.BUILDOP_COL), 'rp2040') > 0:
        fn_return_value = 'PICO'
    else:
        fn_return_value = 'AM328'
    # Other types:
    # "Every"           ' Nano Every
    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit

""" Used Cmd colors:                 (See: https://ss64.com/nt/color.html)
 ~~~~~~~~~~~~~~~~
 1F" ' White on Blue                     Arduino Comile DCC
 2F" ' White on Green                    Arduino Comile SX
 3F" ' White on Aqua                     Arduino Comile CAN
 4F" ' Yellow on Red                     Error
 5F" ' White on Purple                   Create_InstalLib_Cmd_file              Wird das noch gebraucht ? => Nein ==> Ist deaktiviert
 80  ' Black on bright Gray              Do_Update_Script
 79" ' Blue  on bright Gray              Restart_Cmd
 Links for 32 and 64 Bit Windows:
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - General description: https://codekabinett.com/rdumps.php?Lang=2&targetDoc=windows-api-declaration-vba-64-bit
   "Also new with VBA7 are the two new compiler constants Win64 and VBA7.
    VBA7 is true if your code runs in the VBA7-Environment (Access/Office 2010 and above).
    Win64 is true if your code actually runs in the 64-bit VBA environment.
    Win64 is not true if you run a 32-Bit VBA Application on a 64-bit system."
 - Overview 32 / 64 Bit functions: https://jkp-ads.com/Articles/apideclarations.asp
 Following parts use declared external functions                 (List is not updated)
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - M06_Write_Header:
    - Detect if CTRL is pressed when the "Arduino" button is pressed
      Public Sub Write_Header_File_and_Upload_to_Arduino()
 - M40_Mouse_Scroll
    - Uses a lot of functions to be able to use the scroll wheel
 - M31_Sound
    - Play a windows sound if the hook is enabled/disabled
      BeepThis2()
 - M24_Mouse_Insert_Pos
    - Mouse cursor if lines are moved (Mouse or Keyboard)
 - M40_ShellAndWait
    - Start the Arduino Compiler
 - M30_Tools
    - Sleep         => Some locatons
    - ShellExecute  => EditFile_Click
    - GetKeyState   => Not used
"""
