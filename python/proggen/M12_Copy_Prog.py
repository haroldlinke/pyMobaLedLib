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

from ExcelAPI.XLC_Excel_Consts import *
import ExcelAPI.XLA_Application as P01

import proggen.M02_Public as M02
import proggen.M02a_Public as M02a
import proggen.M09_Language as M09
import proggen.M30_Tools as M30
import proggen.M08_ARDUINO as M08
import mlpyproggen.Prog_Generator as PG





""" Copy the program to %USERPROFILE%\\Documents\\Arduino\\MobaLedLib_<Version>\
 To update the icon Cache in windows enter
   ie4uinit -show
 in the command line
-------------------------------------------------------------------------------------------------------------------------------------------------------------
"""


def Remove_File_If_Exists(FileName):

    #---------------------------------------------------------------------------------------------------------------
    fn_return_value = True
    if Dir(FileName) == '':
        return fn_return_value
    # VB2PY (UntranslatedCode) On Error GoTo Remove_Error
    try:
        Kill(( FileName ))
        # VB2PY (UntranslatedCode) On Error GoTo 0
        return fn_return_value
    except:
        P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Die Datei #1# konnte nicht gelöscht werden\''), '#1#', FileName), vbCritical, M09.Get_Language_Str('Fehler beim Löschen')))
        fn_return_value = False
        return fn_return_value


def FileCopy_with_Check(DestDir, Name, SourceName=VBMissingArgument):
    fn_return_value = False
    CopyDir = Boolean()

    SrcPath = String()

    SrcName = String()
    #---------------------------------------------------------------------------------------------------------------
    # Could also copy a whole folder with all sub directories
    # If SourceName is empty the file/directory "Name" is copied from the program dir to DestDir
    # If a SourceName is given the file the source dir is extracted from the name.
    SrcPath = M08.GetWorkbookPath() + '/'
    SrcName = Name
    if SourceName != '':
        if M30.FilePath(SourceName) != '':
            SrcPath = M30.FilePath(SourceName)
        SrcName = M30.FileNameExt(SourceName)
    if Dir(SrcPath + SrcName) == '':
        if Dir(SrcPath + SrcName, vbDirectory) != '':
            CopyDir = True
        else:
            P01.MsgBox(M09.Get_Language_Str('Fehler: Die Datei oder das Verzeichnis \'') + SrcName + M09.Get_Language_Str('\' ist nicht im Verzeichnis') + vbCr + '  \'' + SrcPath + '\'' + vbCr + M09.Get_Language_Str('vorhanden.'), vbCritical, M09.Get_Language_Str('Fehler beim kopieren'))
            return fn_return_value
    # VB2PY (UntranslatedCode) On Error GoTo CopyError
    try:
        if CopyDir:
            #*HL fsoObj = Scripting.FileSystemObject()
            #*HL fsoObj.CopyFolder(SrcPath + SrcName, DestDir + Name, OverWriteFiles=True)
            shutil.copytree(SrcPath + SrcName, DestDir + Name, dirs_exist_ok=True)
        else:
            FileCopy(SrcPath + SrcName, DestDir + Name)
        # VB2PY (UntranslatedCode) On Error GoTo 0
        fn_return_value = True
        return fn_return_value
    except:
        P01.MsgBox(M09.Get_Language_Str('Es ist ein Fehler beim kopieren der Datei oder des Verzeichnisses \'') + SrcName + M09.Get_Language_Str('\' vom Verzeichnis') + vbCr + '  \'' + SrcPath + '\'' + vbCr + M09.Get_Language_Str('nach \'') + DestDir + M09.Get_Language_Str('\' aufgetreten'), vbCritical, M09.Get_Language_Str('Fehler beim kopieren'))
        return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DidCopy - ByRef 
def __Copy_File_With_new_Name_If_Exists(Name, DidCopy):
    fn_return_value = False
    ProgName = String()

    FullDestDir = String()
    # 12.11.21: set DidCopy to true in case of copy occured
    #----------------------------------------------------------------------------
    FullDestDir = M30.FilePath(Name)
    ProgName = FullDestDir + M30.FileNameExt(Name)
    # Check if the program already exists
    if Dir(ProgName) != '':
        while 1:
            Nr = Nr + 1
            CopyName = FullDestDir + M30.FileName(Name) + '_Old_' + Nr + '.xlsm'
            if not (Dir(CopyName) != ''):
                break
        if not FileCopy_with_Check(FullDestDir, M30.FileNameExt(CopyName), FullDestDir + M30.FileNameExt(Name)):
            return fn_return_value
        DidCopy = True
        P01.MsgBox(M09.Get_Language_Str('Achtung: Die Datei \'') + M30.FileNameExt(Name) + M09.Get_Language_Str('\' existiert bereits im Verzeichnis') + vbCr + '  \'' + FullDestDir + '\'' + vbCr + vbCr + M09.Get_Language_Str('Das existierende Programm wurde unter dem Namen \'') + M30.FileName(CopyName) + M09.Get_Language_Str('\' gesichert.') + vbCr + vbCr + M09.Get_Language_Str('Dieser Fehler tritt auf wenn das Programm mehrfach aus dem \'extras\' Verzeichnis ' + 'der Bibliothek gestartet wird.') + vbCr + M09.Get_Language_Str('Das Programm muss nur beim ersten mal nach der Installation der MobaLedLib aus dem ' + 'Bibliotheksverzeichnis gestartet werden. Dabei wird es in das oben genannte Verzeichnis ' + 'kopiert damit die Bibliothek unverändert bleibt.' + vbCr + 'Im folgenden wird ein Link auf dem Desktop kreiert über den das Programm in Zukunft gestartet wird.'), vbInformation, M09.Get_Language_Str('Programm existiert bereits (Mehrfacher Start aus \'extras\' Verzeichnis)'))
    fn_return_value = True
    return fn_return_value

def Copy_Prog_If_in_LibDir():
    fn_return_value = False
    Result = Boolean()
    fn_return_value = Copy_Prog_If_in_LibDir_WithResult(Result)
    return fn_return_value

def Activate_Options_Button(Gerald):
    Sh = P01.Worksheet()
    # 29.11.23:
    #-----------------------------------------------------
    for Sh in P01.ActiveWorkbook.Sheets:
        if M28.Is_Data_Sheet(Sh):
            _with97 = P01.Sheets(Sh.Name)
            _with97.Options_Button.Visible = Gerald
            _with97.Options_Button2.Visible = not Gerald

def Test_Activate_Options_Button():
    # 29.11.23:
    #UT---------------------------------------
    Activate_Options_Button(False)

def Test_Select_Icons():
    Result = String()
    # 29.11.23:
    #UT----------------------------
    Result = Select_Icons.ShowForm()
    Activate_Options_Button(Result == 'Gerald')
    Debug.Print('Test_Select_Icons:' + Result)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DidCopy - ByRef 
def Copy_Prog_If_in_LibDir_WithResult(DidCopy):
    fn_return_value = False
    FullDestDir = String()

    Parts = Variant()

    p = Variant()

    ActDir = String()

    ProgName = String()

    CopyMsg = String()
    #--------------------------------------------------
    # Return true if the programm was stored in the LibDir
    if InStr(UCase(M08.GetWorkbookPath() + '/'), UCase(M02a.Get_SrcDirInLib())) == 0:
        return fn_return_value
    fn_return_value = True
    DidCopy = False
    # 30.05.20: Disabled
    #Dim UserProfile As String
    #UserProfile = Environ(Env_USERPROFILE)
    #If UserProfile = "" Then
    #   MsgBox Get_Language_Str("Fehler: Die Variable 'USERPROFILE' ist nicht definiert ;-(" & vbCr & '            vbCr & '            "Das Programm wird nach 'C:") & Get_DestDir_All() & Get_Language_Str("' kopiert."), vbInformation, '          Get_Language_Str("Fehler beim kopieren des LED Programmiertool")
    #   UserProfile = "C:"
    #End If
    # Create the destination directory if it doesn't exist
    FullDestDir = M02.Get_DestDir_All()
    # VB2PY (UntranslatedCode) On Error Resume Next
    Parts = Split(FullDestDir, '/')
    for p in Parts:
        ActDir = ActDir + p + '/'
        if Len(ActDir) > 3:
            MkDir(ActDir)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    # 14.06.20: Copy both programms
    if not FileCopy_with_Check(FullDestDir, 'Pattern_Config_Examples'):
        return fn_return_value
    if not FileCopy_with_Check(FullDestDir, 'LEDs_AutoProg'):
        return fn_return_value
    
    if not FileCopy_with_Check(FullDestDir, 'Configuration'):
        return fn_return_value
        # 04.03.22 Juergen Simulator
    # 24.01.22: remove some files which have been moved to MobaLedLib\src dir
    # in case of BETA update function these files would not be deleted and lead to a build error
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\Helpers.cpp')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\Helpers.h')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\CommInterface.cpp')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\CommInterface.h')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\InMemoryStream.cpp')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\InMemoryStream.h')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\DCCInterface.cpp')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\DCCInterface.h')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\DMXInterface.cpp')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\DMXInterface.h')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\SXInterface.cpp')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\SXInterface.h')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\SX20.cpp')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\SX20.h')
    # 29.12.23: remove some more files caused by LNet changes
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\LocoNetInterface.cpp')
    Remove_File_If_Exists(FullDestDir + 'LEDs_AutoProg\\LocoNetInterface.h')
    # 11.02.25: improve ESP32 userinterface
    Remove_File_If_Exists(FullDestDir + "LEDs_AutoProg\\SSD1306UI.cpp")    
    
    
    if not FileCopy_with_Check(FullDestDir, 'Prog_Generator_Examples'):
        return fn_return_value
        # 05.10.20:
    if not FileCopy_with_Check(FullDestDir, 'Icons'):
        return fn_return_value
        # Is used in both programms
        
    if not FileCopy_with_Check(FullDestDir, 'Boards'):
        return fn_return_value
        # 15.02.22: Juergen - for platformio build
        
    if not __Copy_File_With_new_Name_If_Exists(FullDestDir + M02.SECOND_PROG + '.xlsm', DidCopy):
        return fn_return_value
        # 14.06.20: Copy also the second program
    if not FileCopy_with_Check(FullDestDir, M02.SECOND_PROG + '.xlsm'):
        return _fn_return_value
    # 29.11.23:
    Result = Select_Icons.ShowForm()
    Activate_Options_Button(Result == 'Gerald')
    if Result == 'Gerald':
        DefaultIcon = M02.DEFAULTICON1
        Second_Icon = M02.SECOND_ICON1
        WikiPg_Icon = M02.WIKIPG_ICON1
        Remove_File_If_Exists()(FullDestDir + 'UseNewIcons')
    else:
        DefaultIcon = M02.DEFAULTICON2
        Second_Icon = M02.SECOND_ICON2
        WikiPg_Icon = M02.WIKIPG_ICON2
        fp = FreeFile()
        VBFiles.openFile(fp, FullDestDir + 'UseNewIcons', 'w') 
        VBFiles.writeText(fp, 'Use the new icons from Michael in the Patternconfigurator', '\n')
        VBFiles.closeFile(fp)
    CreateDesktopShortcut()(M02.SECOND_LINK, FullDestDir + M02.SECOND_PROG + '.xlsm', Second_Icon)
    # 14.06.20: Create Link to the second programm
    ProgName = FullDestDir + PG.ThisWorkbook.Name
    if not __Copy_File_With_new_Name_If_Exists(ProgName, DidCopy):
        return fn_return_value
        # 14.06.20: Moved in seperate function
    # VB2PY (UntranslatedCode) On Error GoTo ErrSaveAs
    P01.Application.DisplayAlerts = False
    PG.ThisWorkbook.SaveAs(ProgName)
    P01.Application.DisplayAlerts = True
    # VB2PY (UntranslatedCode) On Error GoTo 0
    CopyMsg = M09.Get_Language_Str('Das Programm wurde in das Verzeichnis') + vbCr + '  \'' + FullDestDir + '\'' + vbCr + M09.Get_Language_Str('kopiert.') + vbCr + vbCr
    #If Create_Desktoplink_w_Powershell(DSKLINKNAME, ProgName) Then
    if CreateDesktopShortcut(M02.DSKLINKNAME, ProgName):
        P01.MsgBox(CopyMsg + M09.Get_Language_Str('In Zukunft kann das Programm über den Link') + vbCr + '   ' + Split(M02.DSKLINKNAME, ' ')(0) + vbCr + '   ' + Split(M02.DSKLINKNAME, ' ')(1) + vbCr + M09.Get_Language_Str('auf dem Desktop gestartet werden'), vbInformation, M09.Get_Language_Str('Programm kopiert und Link auf Desktop erzeugt'))
    else:
        P01.MsgBox(CopyMsg + M09.Get_Language_Str('Beim Anlegen des Links gab es Probleme ;-(' + vbCr + 'Das Programm kann trotzdem von der oben angegebenen Position aus gestartet werden.'), vbInformation, M09.Get_Language_Str('Programm kopiert'))
    CreateDesktopShortcut('Wiki MobaLedLib', M02.WikiPg_Link, M02.WIKIPG_ICON1)
    CreateDesktopShortcut( "Shop MobaLedLib", M02.MLLSHOP_LINK, M02.MLLSHOP_ICON) # Create Link to the MLL Shop' 
    CreateDesktopShortcut( "MobaLedLib Suche", M02.SUCHE_LINK, M02.SUCHE_ICON) #' Create Link to the MLL Suche')
         
    return fn_return_value
    P01.Application.DisplayAlerts = True
    P01.MsgBox(M09.Get_Language_Str('Fehler beim Speichern des Programms im Verzeichnis:') + vbCr + '  \'' + M30.FilePath(ProgName) + '\'', vbCritical, M09.Get_Language_Str('Fehler beim Speichen des Excel Programms'))
    return fn_return_value

def __TestCreateDesktopShortcut():
    #UT------------------------------------
    CreateDesktopShortcut('Aber Hallo3', PG.ThisWorkbook.FullName)

def __TestCreateWikiDesktopShortcut():
    #UT----------------------------------------
    CreateDesktopShortcut('Wiki MobaLedLib', M02.WikiPg_Link, M02.WikiPg_Icon)

def CreateDesktopShortcut(LinkName, BookFullName, IconName=M02.DefaultIcon):
    Debug.Print("CreateDesktopShortcut not implemented: %s", LinkName)
    return False

    import winshell
    from pathlib import Path
    
    #example:
    # Define all the file paths needed for the shortcut
    # Assumes default miniconda install
    desktop = Path(winshell.desktop())
    miniconda_base = Path(
        winshell.folder('CSIDL_LOCAL_APPDATA')) / 'Continuum' / 'miniconda3'
    win32_cmd = str(Path(winshell.folder('CSIDL_SYSTEM')) / 'cmd.exe')
    icon = str(miniconda_base / "Menu" / "Iconleak-Atrous-Console.ico")
    
    # This will point to My Documents/py_work. Adjust to your preferences
    my_working = str(Path(winshell.folder('CSIDL_PERSONAL')) / "py_work")
    link_filepath = str(desktop / "python_working.lnk")
    
    # Build up all the arguments to cmd.exe
    # Use /K so that the command prompt will stay open
    arg_str = "/K " + str(miniconda_base / "Scripts" / "activate.bat") + " " + str(
        miniconda_base / "envs" / "work")
    
    # Create the shortcut on the desktop
    with winshell.shortcut(link_filepath) as link:
        link.path = win32_cmd
        link.description = "Python(work)"
        link.arguments = arg_str
        link.icon_location = (icon, 0)
    link.working_directory = my_working

    fn_return_value = None
    location = 'Desktop'

    LinkExt = '.lnk'

    oWsh = Object()

    oShortcut = Object()

    Sep = String()

    Path = String()

    DesktopPath = String()

    Shortcut = String()
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Create a custom icon shortcut on the users desktop
    # Constant string values, you can replace "Desktop"
    # with any Special Folders name to create the shortcut there
    # Object variables
    # String variables
    # Initialize variables
    Sep = P01.Application.PathSeparator
    Path =M08.GetWorkbookPath()
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
    if IconName != '':
        if Dir(Path + Sep + IconName) == '':
            P01.MsgBox(M09.Get_Language_Str('Fehler: Das Icon \'') + IconName + M09.Get_Language_Str('\' existiert nicht'), vbCritical, M09.Get_Language_Str('Fehler: Icon nicht im Programm Verzeichnis'))
        else:
            with_0.IconLocation = Path + Sep + IconName
    with_0.Save()
    # Explicitly clear memory
    oWsh = None
    oShortcut = None
    fn_return_value = True
    return fn_return_value

    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit