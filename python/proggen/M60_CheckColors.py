# -*- coding: utf-8 -*-
#
#         Write header
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

import proggen.M02_Public as M02
import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
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

import ExcelAPI.XLA_Application as P01
import mlpyproggen.Prog_Generator as PG

from ExcelAPI.XLC_Excel_Consts import *


""" Support for the Python modul MobaLedCheckColors.py from Harold
 ToDo:
 - Verwendet die Datei: LEDs_AutoProg\\MobaLedTest_config.json
 - Keine py Dateien unterstützen
 - Download testen
 - Wenn bereits eine ColTab Zeile vorhanden ist, dann sollen die Farben verwendet werden
# VB2PY (CheckDirective) VB directive took path 1 on USE_pyPROGGEN = 2
Private Const DOWNLOAD_EXEPROG = "http://www.hlinke.de/files/pyProg_Generator_MobaLedLib.zip"

 Start des Check Color Programms:
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Es gibt eine py Version und eine Exe Version und seit 27.01.21 eine Zip Version.
 Die Exe muss manuell von Harolds Seite herunter geladen werden. Für die py Version benötigt
 man einen Python Interpreter. Die Zip Version muss zusätzlich entzippt werden.
 Wenn das Programm die EXE Version findet, dann wird diese ausgeführt. Dabei wird davon
 ausgangen, dass der Benutzer sich selber um die neueste Version kümmert.
 Wenn die EXE Version nicht vorhanden ist, dann wird geprüft ob Python installiert ist.
 Ist Pyton nicht installiert, dann wird nachgefragt ob die EXE herunter laden will
 Oder Python installieren will.

UT-------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------
"""

__USE_pyPROGGEN = 2
__CHECKCOL_EXE_DIR = "" #M02.Ino_Dir_LED + 'pyProg_Generator_MobaLedLib\\'
__CHECKCOL_DAT_DIR = "" #M02.Ino_Dir_LED
__CHECKCOL_ZIP_DIR = "" #M02.Ino_Dir_LED
__DOWNLOAD_EXEPROG = 'https://github.com/haroldlinke/MobaLedLib_pyProgGen/blob/master/pyProg_Generator_MobaLedLib.zip?raw=true'
__CHECK_COLORS_EXE = 'pyProg_Generator_MobaLedLib.exe'
__CHECK_COLORS_DST = 'pyProg_Generator_MobaLedLib.zip'
__PYCMDLINE_PARAMS = ' --startpage ColorCheckPage'
__CONFIG_FILE_NAME = 'MobaLedTest_config.json'
__DISCONECTED_NAME = 'MobaLedTest_disconnect.Txt'
__CLOSE_CHECKCOL_N = 'MobaLedTest_Close.Txt'
__COLTEST_ONLYFILE = 'ColorTestOnly.txt'
__START_PALETTETXT = '    "palette": {'
__ENDE_PALETTE_TXT = '    },'
__START_SERPORT_NR = '    "serportnumber":'
__START_SERPO_NAME = '    "serportname": "'
__EXP_PYTHON_V_STR = '3.7.0'
__PYTHON_DOWNLOADP = 'https://www.python.org/downloads/'
__FINISHEDTXT_FILE = __CHECKCOL_EXE_DIR + 'Finished.txt'
__COLTAB_SIZE = 17
__NamesList = 'ROOM_COL0,' + 'ROOM_COL1,' + 'ROOM_COL2,' + 'ROOM_COL3,' + 'ROOM_COL4,' + 'ROOM_COL5,' + 'GAS_LIGHT D,' + 'GAS LIGHT,' + 'NEON_LIGHT D,' + 'NEON_LIGHT M,' + 'NEON_LIGHT,' + 'ROOM_TV0 A,' + 'ROOM_TV0 B,' + 'ROOM_TV1 A,' + 'ROOM_TV1 B,' + 'SINGLE_LED,' + 'SINGLE_LED D'

class RGB_T:
    def __init__(self):
       
        self.r = Integer()
        self.g = Integer()
        self.b = Integer()

__PythonVer = int()
__Smiley_Direction = int()
__Smiley_Cnt = int()
__Proc_CheckColors_Form_Callback = String()
__ColTab_Dest_Sheet = String()
__ColTab_Dest_Row = int()
ColTab = vbObjectInitialize((__COLTAB_SIZE,), RGB_T)


def __VerStr_to_long(p_str):
    fn_return_value = None
    Parts = vbObjectInitialize(objtype=String)
    #-----------------------------------------------------
    Parts = Split(p_str, '.')
    fn_return_value = Parts(0) * 1000000
    if UBound(Parts) >= 1:
        fn_return_value = __VerStr_to_long() + Parts(1) * 1000
    if UBound(Parts) >= 2:
        fn_return_value = __VerStr_to_long() + Parts(2)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ExistingVer - ByRef 
def __Check_Phyton(ExpVerStr, ExistingVer):
    fn_return_value = None
    PythonStr = 'Python '

    Res = String()

    ExpVer = int()

    ActVer = int()
    #--------------------------------------------------------------------------------------
    # Return a positiv number if the detected version is >= the expectet version
    #        a negative number if the detected version is < the expectet version
    #        The number is the actual version
    #        0 if python is not installed
    ExpVer = __VerStr_to_long(ExpVerStr)
    Res = F_shellExec('cmd /c Python -V')
    if Res != '':
        if Left(Res, Len(PythonStr)) == PythonStr:
            ExistingVer = Trim(Replace(Replace(Mid(Res, Len(PythonStr)), vbLf, ''), vbCr, ''))
            ActVer = __VerStr_to_long(ExistingVer)
            if ActVer >= ExpVer:
                fn_return_value = ActVer
                fn_return_value = - ActVer
    return fn_return_value

def __Test_Check_Phyton():
    ExistingVer = String()
    #UT----------------------------
    Debug.Print(__Check_Phyton('3.8.0', ExistingVer) + ' ExistingVer=\'' + ExistingVer + '\'')

def __Start_MobaLedCheckColors_py():
    __CHECKCOL_EXE_DIR = M02.Ino_Dir_LED + 'pyProg_Generator_MobaLedLib\\'
    __CHECKCOL_DAT_DIR = M02.Ino_Dir_LED
    __CHECKCOL_ZIP_DIR = M02.Ino_Dir_LED            
    
    fn_return_value = None
    DstDir = String()

    OldDir = String()
    #--------------------------------------------------------
    OldDir = CurDir
    DstDir = M08.GetWorkbookPath() + '/' + __CHECKCOL_EXE_DIR
    # VB2PY (UntranslatedCode) On Error GoTo DirError
    ChDrive(DstDir)
    ChDir(DstDir)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    Debug.Print(Shell('cmd /c start /min python MobaLedCheckColors.py'))
    #Debug.Print Shell("cmd /c start /min Start_py.cmd") ' Program is started in background because otherwise Excel "hangs"
    ChDrive(OldDir)
    ChDir(OldDir)
    fn_return_value = True
    return fn_return_value
    MsgBox(Get_Language_Str('Fehler beim Wechsel in das Verzeichnis:') + vbCr + '  \'' + DstDir + '\'', vbCritical, Get_Language_Str('Fehler beim Start der Farbauswahl'))
    return fn_return_value

def __Start_MobaLedCheckColors_exe():
    global __CHECKCOL_DAT_DIR,__CHECKCOL_EXE_DIR,__CHECKCOL_ZIP_DIR
    fn_return_value = None
    DstDir = String()

    OldDir = String()
    #---------------------------------------------------------
    OldDir = CurDir
    DstDir = M08.GetWorkbookPath() + '\\' + __CHECKCOL_EXE_DIR
    # VB2PY (UntranslatedCode) On Error GoTo DirError
    ChDrive(DstDir)
    ChDir(DstDir)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    Debug.Print(Shell('cmd /c start ' + __CHECK_COLORS_EXE + __PYCMDLINE_PARAMS))
    ChDrive(OldDir)
    ChDir(OldDir)
    fn_return_value = True
    return fn_return_value
    MsgBox(Get_Language_Str('Fehler beim Wechsel in das Verzeichnis:') + vbCr + '  \'' + DstDir + '\'', vbCritical, Get_Language_Str('Fehler beim Start der Farbauswahl'))
    return fn_return_value

def Disconnect_CheckColors():
    fp = Integer()

    Name = String()
    #----------------------------------
    Name = M08.GetWorkbookPath() + '/' + __CHECKCOL_DAT_DIR + __DISCONECTED_NAME
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return
    MsgBox(Get_Language_Str('Fehler beim erzeugen der Disconnect Datei:') + vbCr + '  \'' + Name + '\'', vbCritical, Get_Language_Str('Fehler beim trennen der Verbindung zum Arduino'))

def Close_CheckColors():
    fp = Integer()

    Name = String()
    #-----------------------------
    Name = ThisWorkbook.Path + '\\' + __CHECKCOL_EXE_DIR + __CLOSE_CHECKCOL_N
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return
    MsgBox(Get_Language_Str('Fehler beim erzeugen der Close Datei:') + vbCr + '  \'' + Name + '\'', vbCritical, Get_Language_Str('Fehler beim beenden des Farbtest Programms'))

def __Delete_CheckColors_CloseFile():
    Name = String()
    #-----------------------------------------
    Name = M08.GetWorkbookPath() + '/' + __CHECKCOL_EXE_DIR + __CLOSE_CHECKCOL_N
    if Dir(Name) != '':
        Kill(Name)

def Write_ColTest_Only_File():
    fp = Integer()

    Name = String()
    #-----------------------------------
    Name = ThisWorkbook.Path + '\\' + __CHECKCOL_EXE_DIR + __COLTEST_ONLYFILE
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return
    MsgBox(Get_Language_Str('Fehler beim erzeugen der Datei:') + vbCr + '  \'' + Name + '\'', vbCritical, Get_Language_Str('Fehler beim anlegen einer Datei'))

def __Delete_ColTest_Only_File():
    Name = String()
    #-------------------------------------
    Name = M08.GetWorkbookPath() + '/' + __CHECKCOL_EXE_DIR + __COLTEST_ONLYFILE
    if Dir(Name) != '':
        Kill(Name)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ColTab - ByRef 
def __Set_Default_ColTab():
    #------------------------------------------------------
    ColTab[0].r = 15
    ColTab[0].g = 13
    ColTab[0].b = 3
    ColTab[1].r = 22
    ColTab[1].g = 44
    ColTab[1].b = 27
    ColTab[2].r = 155
    ColTab[2].g = 73
    ColTab[2].b = 5
    ColTab[3].r = 39
    ColTab[3].g = 18
    ColTab[3].b = 1
    ColTab[4].r = 30
    ColTab[4].g = 0
    ColTab[4].b = 0
    ColTab[5].r = 79
    ColTab[5].g = 39
    ColTab[5].b = 7
    ColTab[6].r = 50
    ColTab[6].g = 50
    ColTab[6].b = 50
    ColTab[7].r = 255
    ColTab[7].g = 255
    ColTab[7].b = 255
    ColTab[8].r = 20
    ColTab[8].g = 20
    ColTab[8].b = 27
    ColTab[9].r = 70
    ColTab[9].g = 70
    ColTab[9].b = 80
    ColTab[10].r = 245
    ColTab[10].g = 245
    ColTab[10].b = 255
    ColTab[11].r = 50
    ColTab[11].g = 50
    ColTab[11].b = 20
    ColTab[12].r = 70
    ColTab[12].g = 70
    ColTab[12].b = 30
    ColTab[13].r = 50
    ColTab[13].g = 50
    ColTab[13].b = 8
    ColTab[14].r = 50
    ColTab[14].g = 50
    ColTab[14].b = 8
    ColTab[15].r = 255
    ColTab[15].g = 255
    ColTab[15].b = 255
    ColTab[16].r = 50
    ColTab[16].g = 50
    ColTab[16].b = 50
    
    return ColTab

def __Dec_2_Hex2(d):
    fn_return_value = None
    #--------------------------------------------------
    fn_return_value = Right('00' + Hex(d), 2)
    return fn_return_value

def __RGB_to_Hex(rgb):
    fn_return_value = None
    #--------------------------------------------------
    fn_return_value = __Dec_2_Hex2(rgb.r) + __Dec_2_Hex2(rgb.g) + __Dec_2_Hex2(rgb.b)
    return fn_return_value

def __Write_ColTab(fp, ColTab):
    Name = Variant()

    NamesArray = vbObjectInitialize(objtype=String)

    Nr = Integer()
    #---------------------------------------------------------
    VBFiles.writeText(fp, __START_PALETTETXT, '\n')
    NamesArray = Split(__NamesList, ',')
    for Name in NamesArray:
        VBFiles.writeText(fp, '        "' + Name + '": "#' + __RGB_to_Hex(ColTab(Nr)) + '"')
        if Nr < UBound(NamesArray):
            VBFiles.writeText(fp, ',', '\n')
            VBFiles.writeText(fp, '', '\n')
        Nr = Nr + 1
    VBFiles.writeText(fp, __ENDE_PALETTE_TXT, '\n')

def Write_Default_CheckColors_Parameter_File():
    return #*HL
    fp = Integer()

    FileName = String()

    ColTab = vbObjectInitialize((__COLTAB_SIZE,), RGB_T)
    #----------------------------------------------------
    FileName = ThisWorkbook.Path + '\\' + __CHECKCOL_DAT_DIR + __CONFIG_FILE_NAME
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, FileName, 'w') 
    VBFiles.writeText(fp, '{', '\n')
    VBFiles.writeText(fp, '    "serportnumber": 0,', '\n')
    VBFiles.writeText(fp, '    "serportname": "",', '\n')
    VBFiles.writeText(fp, '    "maxLEDcount": "256",', '\n')
    VBFiles.writeText(fp, '    "lastLedCount": 1,', '\n')
    VBFiles.writeText(fp, '    "lastLed": 0,', '\n')
    VBFiles.writeText(fp, '    "pos_x": 100,', '\n')
    VBFiles.writeText(fp, '    "pos_y": 100,', '\n')
    VBFiles.writeText(fp, '    "colorview": 1,', '\n')
    VBFiles.writeText(fp, '    "startpage": 1,', '\n')
    VBFiles.writeText(fp, '    "led_correction_r": "100",', '\n')
    VBFiles.writeText(fp, '    "led_correction_g": "69",', '\n')
    VBFiles.writeText(fp, '    "led_correction_b": "94",', '\n')
    VBFiles.writeText(fp, '    "use_led_correction": 1,', '\n')
    VBFiles.writeText(fp, '    "old_color": "#FFA8C7",', '\n')
    ColTab = __Set_Default_ColTab()
    __Write_ColTab(fp, ColTab)
    VBFiles.writeText(fp, '    "autoconnect": true', '\n')
    VBFiles.writeText(fp, '}', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return
    MsgBox(Get_Language_Str('Fehler beim Schreiben der Parameter Datei:') + vbCr + '  \'' + FileName + '\'', vbCritical, Get_Language_Str('Fehler beim Schreiben der Parameter Datei'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sp - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Ep - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: FileName - ByRef 
def __Open_Cfg_File_and_Get_Sp_and_Ep(Txt, Sp, Ep, FileName):
    fn_return_value = None
    #---------------------------------------------------------------------------------------------------------------------------------------------
    FileName = M08.GetWorkbookPath() + '/' + __CHECKCOL_DAT_DIR + __CONFIG_FILE_NAME
    Txt = Read_File_to_String(FileName)
    if Txt == '#ERROR#':
        return fn_return_value
    Sp = InStr(Txt, __START_PALETTETXT)
    if Sp == 0:
        MsgBox(Get_Language_Str('Fehler: Der Text \'') + __START_PALETTETXT + Get_Language_Str('\' existiert nicht in der Datei:') + vbCr + '  \'' + FileName + '\'', vbCritical, Get_Language_Str('Fehler: Anfang der Farbpalette nicht gefunden'))
        return fn_return_value
    Ep = InStr(Txt, __ENDE_PALETTE_TXT)
    if Ep == 0:
        MsgBox(Get_Language_Str('Fehler: Das Ende der Farbpalette wurde nicht gefunden in') + vbCr + '  \'' + FileName + '\'', vbCritical, Get_Language_Str('Ende der Farbpalette nicht gefunden'))
        return fn_return_value
    fn_return_value = True
    return fn_return_value

def __Insert_ColTab_to_ConfigFile(ColTab):
    fn_return_value = None
    FileName = String()

    Txt = String()

    Sp = int()

    Ep = int()

    fp = Integer()
    #-------------------------------------------------------------------------
    if not __Open_Cfg_File_and_Get_Sp_and_Ep(Txt, Sp, Ep, FileName):
        return fn_return_value
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, FileName, 'w') 
    VBFiles.writeText(fp, Left(Txt, Sp - 1))
    __Write_ColTab(fp, ColTab)
    VBFiles.writeText(fp, Mid(Txt, Ep + Len(__ENDE_PALETTE_TXT) + 2))
    VBFiles.closeFile(fp)
    fn_return_value = True
    return fn_return_value
    MsgBox(Get_Language_Str('Fehler beim aktualisieren der Parameter Datei:') + vbCr + '  \'' + FileName + '\'', vbCritical, Get_Language_Str('Fehler beim aktualisieren der Parameter Datei'))
    return fn_return_value

def __Insert_Default_ColTab_to_ConfigFile():
    fn_return_value = None
    

    FileName = String()

    Txt = String()

    Sp = int()

    Ep = int()

    fp = Integer()

    ColTab = vbObjectInitialize((__COLTAB_SIZE,), RGB_T)
    #----------------------------------------------------------------
    ColTab = __Set_Default_ColTab()
    fn_return_value = __Insert_ColTab_to_ConfigFile(ColTab)
    ## VB2PY (CheckDirective) VB directive took path 1 on False
    if not __Open_Cfg_File_and_Get_Sp_and_Ep(Txt, Sp, Ep, FileName):
        return fn_return_value
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, FileName, 'w') 
    VBFiles.writeText(fp, Left(Txt, Sp - 1))
    ColTab = __Set_Default_ColTab()
    __Write_ColTab(fp, ColTab)
    VBFiles.writeText(fp, Mid(Txt, Ep + Len(__ENDE_PALETTE_TXT) + 2))
    VBFiles.closeFile(fp)
    fn_return_value = True
    return fn_return_value
    MsgBox(Get_Language_Str('Fehler beim aktualisieren der Parameter Datei:') + vbCr + '  \'' + FileName + '\'', vbCritical, Get_Language_Str('Fehler beim aktualisieren der Parameter Datei'))
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: FromTxt - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ToTxt - ByVal 
def __Replace_in_String_from_To(Txt, FromTxt, ToTxt, ReplaceTxt, FileName):
    fn_return_value = None
    Sp = Variant()

    Ep = int()
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Sp = InStr(Txt, FromTxt)
    if Sp == 0:
        MsgBox(Get_Language_Str('Fehler: Der Text \'') + FromTxt + Get_Language_Str('\' existiert nicht in der Datei:') + vbCr + '  \'' + FileName + '\'', vbCritical, Get_Language_Str('Fehler beim aktualisieren der Datei'))
        return fn_return_value
    Ep = InStr(Sp, Txt, ToTxt)
    if Ep == 0:
        MsgBox(Get_Language_Str('Fehler: Der Text \'') + ToTxt + Get_Language_Str('\' existiert nicht in der Datei:') + vbCr + '  \'' + FileName + '\'', vbCritical, Get_Language_Str('Fehler beim aktualisieren der Datei'))
        return fn_return_value
    Txt = Left(Txt, Sp + Len(FromTxt) - 1) + ReplaceTxt + Mid(Txt, Ep)
    fn_return_value = True
    return fn_return_value

def __Change_Comport_in_ConfigFile(ComNr):
    return True
    fn_return_value = None
    FileName = String()

    Txt = String()

    fp = Integer()
    #-------------------------------------------------------------------------
    FileName = M08.GetWorkbookPath() + '\\' + __CHECKCOL_DAT_DIR + __CONFIG_FILE_NAME
    Txt = M30.Read_File_to_String(FileName)
    if Txt == '#ERROR#':
        return fn_return_value
    if not __Replace_in_String_from_To(Txt, __START_SERPORT_NR, ',', ' ' + ComNr, FileName):
        return fn_return_value
    if not __Replace_in_String_from_To(Txt, __START_SERPO_NAME, '",', 'COM' + ComNr, FileName):
        return fn_return_value
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, FileName, 'w') 
    VBFiles.writeText(fp, Txt)
    VBFiles.closeFile(fp)
    fn_return_value = True
    return fn_return_value
    MsgBox(Get_Language_Str('Fehler beim aktualisieren des COM Ports in der Parameter Datei:') + vbCr + '  \'' + FileName + '\'', vbCritical, Get_Language_Str('Fehler beim aktualisieren der Parameter Datei'))
    return fn_return_value

def __Test_Change_Comport_in_ConfigFile():
    #UT--------------------------------------------
    __Change_Comport_in_ConfigFile(4)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ColTab - ByRef 
def __Read_ColTab_from_Config_File():
    fn_return_value = None
    FileName = String()

    Txt = String()

    Sp = int()

    Ep = int()

    Nr = Integer()

    ColTabList = vbObjectInitialize(objtype=String)

    Line = Variant()
    #--------------------------------------------------------------------------------
    #if not __Open_Cfg_File_and_Get_Sp_and_Ep(Txt, Sp, Ep, FileName):
    #    return fn_return_value
    Sp = Sp + Len(__START_PALETTETXT) + 1
    ColTabList = Split(Mid(Txt, Sp, Ep - Sp), vbCr)
    for Line in ColTabList:
        if Nr < __COLTAB_SIZE:
            ColStr = Replace(Replace(Trim(Split(Line, ':')(1)), '"', ''), ',', '')
            ColTab[Nr].r = '&H' + Mid(ColStr, 2, 2)
            ColTab[Nr].g = '&H' + Mid(ColStr, 4, 2)
            ColTab[Nr].b = '&H' + Mid(ColStr, 6, 2)
            Nr = Nr + 1
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ColTab - ByRef 
def __Read_ColTab_from_palette(palette):
    global ColTab
    
    Nr = 0
    for key in palette:
        Line = palette.get(key,"")
        ColStr = Line
        ColTab[Nr].r = '&H' + Mid(ColStr, 2, 2)
        ColTab[Nr].g = '&H' + Mid(ColStr, 4, 2)
        ColTab[Nr].b = '&H' + Mid(ColStr, 6, 2)
        Nr = Nr + 1
    return ColTab


def __Test_Read_ColTab_from_Config_File():
    ColTab = vbObjectInitialize((__COLTAB_SIZE,), RGB_T)
    #UT--------------------------------------------
    __Read_ColTab_from_Config_File(ColTab)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ColTab - ByRef 
def __ColTab_to_C_String(ColTab):
    fn_return_value = None
    DefColTab = vbObjectInitialize((__COLTAB_SIZE,), RGB_T)

    Names = vbObjectInitialize(objtype=String)

    Res = String()

    Nr = Integer()

    Comment = String()
    #---------------------------------------------------------------------
    # Generates this string:
    #   // Set_ColTab(Red Green Blue)
    #   Set_ColTab( 15,  13,   3, // *ROOM_COL0
    #               22,  44,  27, //  ROOM_COL1
    #              155,  73,   5, //  ROOM_COL2
    #               39,  18,   1, // *ROOM_COL3
    #               30,   0,   0, //  ROOM_COL4
    #               79,  39,   7, //  ROOM_COL5
    #               50,  50,  50, //  GAS_LIGHT D
    #              255, 255, 255, //  GAS LIGHT
    #               20,  20,  27, //  NEON_LIGHT D
    #               70,  70,  80, //  NEON_LIGHT M
    #              245, 245, 255, //  NEON_LIGHT
    #               50,  50,  20, //  ROOM_TV0 A
    #               70,  70,  30, //  ROOM_TV0 B
    #               50,  50,   8, //  ROOM_TV1 A
    #               50,  50,   8, //  ROOM_TV1 B
    #              255, 255, 255, //  SINGLE_LED
    #               50,  50,  50) //  SINGLE_LED D
    DefColTab = __Set_Default_ColTab()
    Names = Split(__NamesList, ',')
    Res = '// Set_ColTab(Red Green Blue)      ' + vbLf + 'Set_ColTab('
    for Nr in vbForRange(0, __COLTAB_SIZE - 1):
        Res = Res + Right('   ' + str(ColTab(Nr).r), 3) + ', '
        Res = Res + Right('   ' + str(ColTab(Nr).g), 3) + ', '
        Res = Res + Right('   ' + str(ColTab(Nr).b), 3)
        if DefColTab(Nr).r != ColTab(Nr).r or DefColTab(Nr).g != ColTab(Nr).g or DefColTab(Nr).b != ColTab(Nr).b:
            Comment = ' // *'
        else:
            Comment = ' //  '
        Comment = Comment + Names(Nr)
        if Nr < __COLTAB_SIZE - 1:
            Res = Res + ',' + Comment + vbLf + '           '
        else:
            Res = Res + ')' + Comment
    fn_return_value = Res
    return fn_return_value

def __TestColTab_to_C_String():
    ColTab = vbObjectInitialize((__COLTAB_SIZE,), RGB_T)
    #UT---------------------------------
    __Read_ColTab_from_Config_File(ColTab)
    Debug.Print(__ColTab_to_C_String(ColTab))
    #ActiveCell = ColTab_to_C_String(ColTab)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ColTab - ByRef 
def __C_String_to_ColTab(C_Str):
    fn_return_value = None
    Line = Variant()
    ColTab = vbObjectInitialize((__COLTAB_SIZE,), RGB_T)

    Nr = int()
    #----------------------------------------------------------------------------
    for Line in Split(C_Str, vbLf):
        if Left(Trim(Line), 2) != '//':
            Parts = Split(Trim(Replace(Line, 'Set_ColTab(', '')), ',')
            if Nr < __COLTAB_SIZE:
                with_0 = ColTab(Nr)
                with_0.r = P01.val(Trim(Parts(0)))
                with_0.g = P01.val(Trim(Parts(1)))
                with_0.b = P01.val(Trim(Parts(2)))
            Nr = Nr + 1
    return ColTab

def __Test_C_String_to_ColTab():
    ColTab = vbObjectInitialize((__COLTAB_SIZE,), RGB_T)

    C_Str = String()
    #UT----------------------------------
    __Read_ColTab_from_Config_File(ColTab)
    C_Str = __ColTab_to_C_String(ColTab)
    __C_String_to_ColTab(C_Str, ColTab)
    #ColTab(1).g = 212 ' Simulate an error
    Debug.Print('Vergleich: ' +  ( C_Str == __ColTab_to_C_String(ColTab) ))
    

def __Show_Wait_CheckColors_Form(callback =None):
    #---------------------------------------
    P01.Application.EnableEvents = True
    #Wait_CheckColors_Form.Activity_Label = 'J'
    #__Smiley_Direction = 0
    #__Smiley_Cnt = 0
    #Wait_CheckColors_Form.Show()
    #Application.OnTime(Now + TimeValue('00:00:03'), 'Update_Wait_CheckColors_Form')
    #Debug.Print "*Show_Wait_CheckColors_Form()"
    PG.dialog_parent.checkcolor(ColTab,callback=callback)
    

def __Update_Wait_CheckColors_Form():
    Step = 3
    #-----------------------------------------
    # Update the wait dialog and check if the finish file is generated
    # If the Proc_CheckColors_Form_Callback function is defined it's
    # called when the finish file is detected.
    with_1 = Wait_CheckColors_Form.Activity_Label
    if (__Smiley_Direction == 0):
        with_1.Caption = ' ' + with_1.Caption
        if Len(with_1.Caption) >= 10:
            __Smiley_Direction = __Smiley_Direction + 1
    elif (__Smiley_Direction == 1):
        with_1.Caption = Mid(with_1.Caption, 2)
        if Len(Wait_CheckColors_Form.Activity_Label) <= 1:
            __Smiley_Direction = 0
            __Smiley_Cnt = __Smiley_Cnt + 1
            if (__Smiley_Cnt == Step * 1):
                with_1.Caption = 'K'
            elif (__Smiley_Cnt == Step * 2):
                with_1.Caption = 'L'
            elif (__Smiley_Cnt == Step * 3):
                with_1.Caption = 'M'
            elif (__Smiley_Cnt == Step * 4):
                with_1.Caption = '>'
            elif (__Smiley_Cnt == Step * 5):
                with_1.Caption = 'T'
            elif (__Smiley_Cnt == Step * 6):
                with_1.Caption = 'N'
            elif (__Smiley_Cnt == Step * 7):
                with_1.Caption = '('
            elif (__Smiley_Cnt == Step * 8):
                with_1.Caption = 'J'
                __Smiley_Cnt = 0
    Calculate()
    #Debug.Print "*Update_Wait_CheckColors_Form"
    if Dir(ThisWorkbook.Path + '/' + __FINISHEDTXT_FILE) != '':
        Wait_CheckColors_Form.Hide()
        if __Proc_CheckColors_Form_Callback != '':
            Run(__Proc_CheckColors_Form_Callback)
    else:
        if Wait_CheckColors_Form.Visible:
            Application.OnTime(1000, 'Update_Wait_CheckColors_Form')

def __Set_ColTab_Callback(palette):
    global ColTab
    #--------------------------------
    # Is called if the Python ColorCheck program is closed to set the color table
    Debug.Print('Set_ColTab_Callback')
    ColTab = __Read_ColTab_from_palette(palette)
    #PG.ThisWorkbook.Activate()
    P01.Sheets(__ColTab_Dest_Sheet).Select()
    M25.Make_sure_that_Col_Variables_match()
    P01.CellDict[__ColTab_Dest_Row, M25.Config__Col] = __ColTab_to_C_String(ColTab)
    P01.Cells(__ColTab_Dest_Row, M25.LEDs____Col).Value = "" #.ClearContents()
    P01.Cells(__ColTab_Dest_Row, M25.InCnt___Col).Value = "" #.ClearContents()
    P01.Cells(__ColTab_Dest_Row, M25.LocInCh_Col).Value = "" #.ClearContents()

def Open_MobaLedCheckColors_and_Insert_Set_ColTab_Macro():
    #UT-------------------------------------------------------------
    Open_MobaLedCheckColors(__Set_ColTab_Callback, P01.ActiveSheet.Name, P01.ActiveCell().Row)

def Open_MobaLedCheckColors(Callback, Dest_Sheet="", Dest_Row=-1):
    global __Proc_CheckColors_Form_Callback, __ColTab_Dest_Sheet, __ColTab_Dest_Row, ColTab
    #ProgDir = String()

    #Exe_Exists = Boolean()

    #ExistingVer = String()

    Res = True # Boolean()
    #---------------------------------------------------------------------------------------------------------------
    __Proc_CheckColors_Form_Callback = Callback
    __ColTab_Dest_Sheet = Dest_Sheet
    __ColTab_Dest_Row = Dest_Row
    """
    ProgDir = M08.GetWorkbookPath() + '\\' + __CHECKCOL_EXE_DIR
    if Dir(ProgDir, vbDirectory) == '':
        #MsgBox Get_Language_Str("Fehler das Verzeichnis existiert nicht:") & vbCr & "  '" & ProgDir & "'", vbCritical, Get_Language_Str("CheckColors Verzeichnis nicht vorhanden")
        CreateFolder(ProgDir)
        #Exit Sub                                                              '     "      Disabled
    Close_CheckColors()
    Exe_Exists = ( Dir(ProgDir + __CHECK_COLORS_EXE) != '' )
    if Exe_Exists:
        if GetAsyncKeyState(VK_CONTROL) != 0:
            if MsgBox(Get_Language_Str('Soll das Farbtest Programm neu heruntergeladen werden?'), vbYesNo + vbQuestion, Get_Language_Str('Neue Version des Farbtests herunterladen?')) == vbYes:
                Exe_Exists = False
    if not Exe_Exists:
        ## VB2PY (CheckDirective) VB directive took path 1 on USE_pyPROGGEN = 0
        if __PythonVer <= 0:
            __PythonVer = __Check_Phyton(__EXP_PYTHON_V_STR, ExistingVer)
        if __PythonVer <= 0:
            if __PythonVer < 0:
                Msg = vbCr + Get_Language_Str('Momentan ist die ältere Python Version ') + ExistingVer + Get_Language_Str(' installiert. Es kann evtl. Probleme mit existierenden Python Programmen geben wenn ein neuerer Python Interpreter installiert wird.')
            select_2 = MsgBox(Get_Language_Str('Für das Farbauswahl Programm benötigt man entweder die Python ' + 'Version ') + __EXP_PYTHON_V_STR + Get_Language_Str(' oder das davon unabhängige EXE Programm. ' + 'Leider kann letzteres nicht mit der MobaLedLib verteilt ' + 'werden, weil EXE Programme nicht in einer Arduino Bibliothek erlaubt sind.') + vbCr + Msg + vbCr + vbCr + Get_Language_Str('Soll das eigenständige Exe Programm verwendet werden ?' + vbCr + vbCr + 'Ja:    Das Programm wird automatisch herunter geladen' + vbCr + 'Nein: Python muss manuell installiert werden'), vbQuestion + vbYesNoCancel, Get_Language_Str('Variante des Farbauswahl Programms bestimmen'))
            if (select_2 == vbYes):
                MsgBox(Get_Language_Str('Das Farbauswahl Programm wird von Github herunter geladen. Dazu wird eine Internetverbindung benötigt.' + vbCr + 'Nach dem dieses Meldung bestätigt ist wird ein Kommando Fenster geöffnet in dem der Download ausgeführt wird.' + vbCr + vbCr + 'Achtung: Es kann einige Zeit dauern bis die Verbindung aufgebaut ist. In dieser Zeit ist keine Meldung zu sehen'), vbInformation, Get_Language_Str('Download der EXE Datei'))
                DestName = ThisWorkbook.Path + '\\' + __CHECKCOL_EXE_DIR + __CHECK_COLORS_DST
                if WIN7_COMPATIBLE_DOWNLOAD:
                    F_shellExec('powershell Invoke-WebRequest "' + __DOWNLOAD_EXEPROG + '" "-o:' + DestName + '"')
                else:
                    if Check_if_curl_is_Available_and_gen_Message_if_not(__CHECK_COLORS_EXE, __DOWNLOAD_EXEPROG) == False:
                        return
                        # 05.06.20:
                    F_shellExec('powershell curl "' + __DOWNLOAD_EXEPROG + '" ' + '"-o:' + DestName + '"')
                if Dir(DestName) == '':
                    MsgBox(Get_Language_Str('Beim herunter laden des Farbtest Programms ist etwas schief gegangen ;-('), vbCritical, Get_Language_Str('Fehler beim herunter laden des Farbtest Programms'))
                    return
                else:
                    ## VB2PY (CheckDirective) VB directive took path 1 on USE_pyPROGGEN = 2
                    UnzipAFile(DestName, ThisWorkbook.Path + '\\' + __CHECKCOL_ZIP_DIR)
                    Kill(DestName)
                    Exe_Exists = True
                ## VB2PY (CheckDirective) VB directive took path 1 on USE_pyPROGGEN = 0
            elif (select_2 == vbNo):
                MsgBox(Get_Language_Str('Die Download Seite von Python wird gleich geöffnet. Dort lädt man die neueste ' + 'Python Version für Windows herunter und installiert sie.' + vbCr + 'Bei der Installation muss das Häkchen bei \'Add Python ... to Path\' gesetzt werden.' + vbCr + 'Diese Häkchen befindet sich auf der ersten Seite unten, gleich beim start der Installation.' + vbCr + vbCr + 'Anschließend muss Excel geschlossen werden sonst wird Python nicht gefunden. ' + 'Evtl. muss der Rechner auch neu gestartet werden (Windows ist toll)' + vbCr + 'Dann kann die Farbauswahl Funktion benutzt werden.'), vbInformation, Get_Language_Str('Download und Installation von Python'))
                # Es reicht nicht wenn Excel neu gestartet wird. Es muss auch von einem neuen Explorer aus gestartet werden ;-(
                # Ein Neustart über einen Desktop Link scheint zu funktionieren
                Shell('Explorer "' + __PYTHON_DOWNLOADP + '"')
                return
            else:
                return
    """
    # Com Port detection
    M25.Make_sure_that_Col_Variables_match()
    ColTab = __Set_Default_ColTab()
    if M07.Check_USB_Port_with_Dialog(M25.COMPort_COL) == False:
        return
        # 04.05.20: Added exit (Prior Check_USB_Port_with_Dialog ends the program in case of an error)
    __Change_Comport_in_ConfigFile(P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL))
    # Color table
    if Callback != None:
        __Delete_ColTest_Only_File()
        if InStr(P01.Cells(Dest_Row, M25.Config__Col), 'Set_ColTab') > 0:
            ColTab = __C_String_to_ColTab(P01.Cells(Dest_Row, M25.Config__Col))
            #*HL __Insert_ColTab_to_ConfigFile(ColTab)
            # Moved up
            # ATTENTION: This Message box is necessary to generate the delay which prevents the CheckColor
            #            program to be closed by the "Close" File which has been written above
            #            But it doesn't help if the user closes the message to fast because the current version
            #            of the CheckColor program in not writing the "Close" imidiately
            select_3 = P01.MsgBox(M09.Get_Language_Str('Soll die Standard Farbtabelle geladen werden oder die zuletzt ' + 'benutzte Tabelle benutzt werden?' + vbCr + vbCr + 'Ja: Standard Farbtabelle laden' + vbCr + 'Nein: Letzte Farbtabelle verwenden'), vbQuestion + vbYesNoCancel + vbDefaultButton2, M09.Get_Language_Str('Standard oder letzte Benutzer Farbtabelle verwenden?'))
            if (select_3 == vbYes):
                ColTab = __Set_Default_ColTab()
                #*HL if not __Insert_Default_ColTab_to_ConfigFile():
                #*HL     return
            elif (select_3 == vbNo):
                pass
            elif (select_3 == vbCancel):
                return
    else:
        pass
        #Write_ColTest_Only_File()
        #StatusMsg_UserForm.Set_ActSheet_Label('Please wait')
        #StatusMsg_UserForm.Show()
        #Sleep(( 500 ))
        #U01.Unload(StatusMsg_UserForm)
    #__Delete_CheckColors_CloseFile()
    #if Dir(ThisWorkbook.Path + '\\' + __FINISHEDTXT_FILE) != '':
    #    Kill(ThisWorkbook.Path + '\\' + __FINISHEDTXT_FILE)
    # Start the CheckColors program
    #if Exe_Exists:
    #    Res = __Start_MobaLedCheckColors_exe()
    #    Res = __Start_MobaLedCheckColors_py()
    if Res:
        __Show_Wait_CheckColors_Form(callback=Callback)

# VB2PY (UntranslatedCode) Option Explicit
