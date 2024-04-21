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

from ExcelAPI.XLC_Excel_Consts import *
import ExcelAPI.XLA_Application as P01

import proggen.M02_Public as M02
import proggen.M09_Language as M09
import proggen.M25_Columns as M25
import proggen.M30_Tools as M30

"""# VB2PY (CheckDirective) VB directive took path 1 on USE_SKETCHBOOK_DIR
"""


# ####################################################
#
# Public Functions
#
# ####################################################


def Read_Sketchbook_Path_from_preferences_txt():
    
    M02.Sketchbook_Path = ""
    
    Name = String()

    FileStr = String()
    #-------------------
    fn_return_value = False
    #-------------------------------------------------
    # Attention: The file uses UTF8
    Name = Environ(M02.Env_USERPROFILE) + M02.AppLoc_Ardu + 'preferences.txt'
    Debug.Print("Read_Sketchbook_Path_from_preference_txt - Name:"+Name)
    FileStr = M30.Read_File_to_String(Name)
    if FileStr != '#ERROR#':
        M02.Sketchbook_Path = M30.Get_Ini_Entry(FileStr, 'sketchbook.path=')
        logging.debug("Sketchbookpath="+M02.Sketchbook_Path)
        #*HL Sketchbook_Path = M30.ConvertUTF8Str(M30.Get_Ini_Entry(FileStr, 'sketchbook.path='))
        #ThisWorkbook.Sheets(LIBRARYS__SH).Range("Sketchbook_Path") = Sketchbook_Path
        if M02.Sketchbook_Path == '#ERROR#':
            Debug.Print("Fehler beim Lesen der Datei: preferences.txt")
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: beim lesen des \'sketchbook.path\' in \'#1#\''), "#1#", Name), vbCritical, M09.Get_Language_Str('Fehler beim Lesen der Datei:') + ' \'preferences.txt\'')
            return fn_return_value
        if Left(M02.Sketchbook_Path, 2) == '\\\\':
            P01.MsgBox(M09.Get_Language_Str('Fehler: Der Arduino \'sketchbook.path\' darf kein Netzlaufwerk sein:') + vbCr + '  \'' + M02.Sketchbook_Path + '\'', vbCritical, M09.Get_Language_Str('Ungültiger Arduino \'sketchbook.path\''))
            return fn_return_value
        M30.CreateFolder(M02.Sketchbook_Path + '/')
        fn_return_value = True
    return fn_return_value

def Get_Sketchbook_Path():
    
    #----------------------------------------------
    Debug.Print('Get_Sketchbook_Path called')
    if M02.Sketchbook_Path == '':
        Read_Sketchbook_Path_from_preferences_txt()
    fn_return_value = M02.Sketchbook_Path
    logging.debug("Get_Sketchbook_Path="+ fn_return_value)
    return fn_return_value

def Get_SrcDirInLib():
    fn_return_value = Get_Sketchbook_Path() + M02.SrcDirInLib
    logging.debug("Get_SrcDirInLib="+ fn_return_value)
    return fn_return_value

def Get_DestDir_All():
    fn_return_value = Get_Sketchbook_Path() + M02.DestDir_All
    logging.debug("Get_DestDir_All="+ fn_return_value)
    return fn_return_value

def Get_MobaUserDir():
    fn_return_value = Get_Sketchbook_Path() + M02.MobaUserDir
    logging.debug("Get_MobaUserDir="+ fn_return_value)
    return fn_return_value

def Get_Ardu_LibDir():
    fn_return_value = Get_Sketchbook_Path() + M02.Ardu_LibDir
    if P01.checkplatform("Darwin"): # Mac
        ARDU_ResPath_cb = P01.get_global_controller().getConfigData("resourcePathcb")
        if ARDU_ResPath_cb:
            ARDU_ResPath = P01.get_global_controller().getConfigData("resourcePath_filename")
        else:
            ARDU_ResPath = Get_Sketchbook_Path()
        #Arduino_Exe_dir = M08.Find_ArduinoExe()
        #test_str = "Contents/"
        #Arduino_Exe_dir_part1 = Arduino_Exe_dir[:Arduino_Exe_dir.index(test_str) + len(test_str)] # remove /MacOS/Arduino from path
        #fn_return_value = Arduino_Exe_dir_part1 + "Java/" + "libraries/"
        fn_return_value = ARDU_ResPath + "/libraries/"
    logging.debug("Get_Ardu_LibDir="+ fn_return_value)
    return fn_return_value

def Get_SrcDirExamp():
    fn_return_value = Get_Sketchbook_Path() + M02.SrcDirExamp
    #if P01.checkplatform("Darwin"): # Mac
    #    ARDU_ResPath_cb = PG.get_global_controller().getConfigData("resourcePathcb")
    #    if ARDU_ResPath_cb:
    #        ARDU_ResPath = PG.get_global_controller().getConfigData("resourcePath_filename")
    #    else:
    #        ARDU_ResPath = ""        
        #Arduino_Exe_dir = M08.Find_ArduinoExe()
        #test_str = "Contents/"
        #Arduino_Exe_dir_part1 = Arduino_Exe_dir[:Arduino_Exe_dir.index(test_str) + len(test_str)] # remove /MacOS/Arduino from path
        #fn_return_value = Arduino_Exe_dir_part1 + "Java/" + "examples/"
    #    fn_return_value = ARDU_ResPath + "/examples/"
    logging.debug("Get_SrcDirExamp="+ fn_return_value)
    return fn_return_value

def Get_BoardTyp():
    #---------------------------------------
    # The build options for the ESP32 are something like "esp32:esp32:esp32..."
    fn_return_value = 'AM328'
    if InStr(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL), 'esp32') > 0:
        fn_return_value = 'ESP32'
    elif InStr(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL), 'rp2040') > 0:
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
