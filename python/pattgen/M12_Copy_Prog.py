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

""" Copy the program to %USERPROFILE%\Documents\Arduino\MobaLedLib_<Version>\
---------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------
--------------------------------------------------
UT------------------------------------
UT----------------------------------------
 To update the icon Cache in windows enter
   ie4uinit -show
 in the command line
-------------------------------------------------------------------------------------------------------------------------------------------------------------
"""


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SourceName=VBMissingArgument - ByVal 
def FileCopy_with_Check(DestDir, Name, SourceName=VBMissingArgument):
    fn_return_value = None
    CopyDir = Boolean()

    SrcPath = String()

    SrcName = String()
    #---------------------------------------------------------------------------------------------------------------------
    # Could also copy a whole folder with all sub directories
    # If SourceName is empty the file/directory "Name" is copied from the program dir to DestDir
    # If a SourceName is given the file the source dir is extracted from the name.
    SrcPath = ThisWorkbook.Path + '/'
    SrcName = Name
    if SourceName != '':
        if FilePath(SourceName) != '':
            SrcPath = FilePath(SourceName)
        SrcName = FileNameExt(SourceName)
    if Dir(SrcPath + SrcName) == '':
        if Dir(SrcPath + SrcName, vbDirectory) != '':
            CopyDir = True
        else:
            MsgBox(Get_Language_Str('Fehler: Die Datei oder das Verzeichnis \'') + SrcName + Get_Language_Str('\' ist nicht im Verzeichnis') + vbCr + '  \'' + SrcPath + '\'' + vbCr + Get_Language_Str('vorhanden.'), vbCritical, Get_Language_Str('Fehler beim kopieren'))
            return fn_return_value
    # VB2PY (UntranslatedCode) On Error GoTo CopyError
    if CopyDir:
        fsoObj = Scripting.FileSystemObject()
        fsoObj.CopyFolder(SrcPath + SrcName, DestDir + Name, OverWriteFiles=True)
    else:
        FileCopy(SrcPath + SrcName, DestDir + Name)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = True
    return fn_return_value
    MsgBox(Get_Language_Str('Es ist ein Fehler beim kopieren der Datei oder des Verzeichnisses \'') + SrcName + Get_Language_Str('\' vom Verzeichnis') + vbCr + '  \'' + SrcPath + '\'' + vbCr + Get_Language_Str('nach \'') + DestDir + Get_Language_Str('\' aufgetreten'), vbCritical, Get_Language_Str('Fehler beim kopieren'))
    return fn_return_value

def __Copy_File_With_new_Name_If_Exists(Name):
    fn_return_value = None
    ProgName = String()

    FullDestDir = String()
    #----------------------------------------------------------------------------
    FullDestDir = FilePath(Name)
    ProgName = FullDestDir + FileNameExt(Name)
    # Check if the program already exists
    if Dir(ProgName) != '':
        while 1:
            Nr = Nr + 1
            CopyName = FullDestDir + FileName(Name) + '_Old_' + Nr + '.xlsm'
            if not (Dir(CopyName) != ''):
                break
        if not FileCopy_with_Check(FullDestDir, FileNameExt(CopyName), FullDestDir + FileNameExt(Name)):
            return fn_return_value
        MsgBox(Get_Language_Str('Achtung: Die Datei \'') + FileNameExt(Name) + Get_Language_Str('\' existiert bereits im Verzeichnis') + vbCr + '  \'' + FullDestDir + '\'' + vbCr + vbCr + Get_Language_Str('Das existierende Programm wurde unter dem Namen \'') + FileName(CopyName) + Get_Language_Str('\' gesichert.') + vbCr + vbCr + Get_Language_Str('Dieser Fehler tritt auf wenn das Programm mehrfach aus dem \'extras\' Verzeichnis ' + 'der Bibliothek gestartet wird.') + vbCr + Get_Language_Str('Das Programm muss nur beim ersten mal nach der Installation der MobaLedLib aus dem ' + 'Bibliotheksverzeichnis gestartet werden. Dabei wird es in das oben genannte Verzeichnis ' + 'kopiert damit die Bibliothek unverändert bleibt.' + vbCr + 'Im folgenden wird ein Link auf dem Desktop kreiert über den das Programm in Zukunft gestartet wird.'), vbInformation, Get_Language_Str('Programm existiert bereits (Mehrfacher Start aus \'extras\' Verzeichnis)'))
    fn_return_value = True
    return fn_return_value

def Copy_Prog_If_in_LibDir():
    fn_return_value = None
    FullDestDir = String()

    Parts = Variant()

    p = Variant()

    ActDir = String()

    ProgName = String()

    CopyMsg = String()
    #--------------------------------------------------
    # Return true if the programm was stored in the LibDir
    if InStr(UCase(ThisWorkbook.Path + '/'), UCase(Get_SrcDirInLib())) == 0:
        return fn_return_value
    fn_return_value = True
    # 30.05.20: Disabled
    #Dim UserProfile As String
    #UserProfile = Environ(Env_USERPROFILE)
    #If UserProfile = "" Then
    #   MsgBox Get_Language_Str("Fehler: Die Variable 'USERPROFILE' ist nicht definiert ;-(" & vbCr & _
    #         vbCr & _
    #         "Das Programm wird nach 'C:") & Get_DestDir_All() & Get_Language_Str("' kopiert."), vbInformation, _
    #       Get_Language_Str("Fehler beim kopieren des LED Programmiertool")
    #   UserProfile = "C:"
    #End If
    # Create the destination directory if it doesn't exist
    FullDestDir = Get_DestDir_All()
    # VB2PY (UntranslatedCode) On Error Resume Next
    Parts = Split(FullDestDir, '/')
    for p in Parts:
        ActDir = ActDir + p + '/'
        if Len(ActDir) > 3:
            MkDir(ActDir)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    # 14.06.20: Copy both programms
    #If INTPROGNAME = "Pattern_Configurator" Then
    if not FileCopy_with_Check(FullDestDir, 'Pattern_Config_Examples'):
        return fn_return_value
    #ElseIf INTPROGNAME = "Prog_Generator" Then
    if not FileCopy_with_Check(FullDestDir, 'LEDs_AutoProg'):
        return fn_return_value
    # If Not FileCopy_with_Check(FullDestDir, "Prog_Generator_MobaLedLib.pdf") Then Exit Function
    #Else: MsgBox "Internal error: Unknown 'INTPROGNAME'", vbCritical, "Internal Error"
    #End If
    if not FileCopy_with_Check(FullDestDir, 'Icons'):
        return fn_return_value
        # Is used in both programms
    if not __Copy_File_With_new_Name_If_Exists(FullDestDir + SECOND_PROG + '.xlsm'):
        return fn_return_value
        # 14.06.20: Copy also the second program
    if not FileCopy_with_Check(FullDestDir, SECOND_PROG + '.xlsm'):
        return fn_return_value
    CreateDesktopShortcut()(SECOND_LINK, FullDestDir + SECOND_PROG + '.xlsm', SECOND_ICON)
    ProgName = FullDestDir + ThisWorkbook.Name
    if not __Copy_File_With_new_Name_If_Exists(ProgName):
        return fn_return_value
        # 14.06.20: Moved in seperate function
    # VB2PY (UntranslatedCode) On Error GoTo ErrSaveAs
    Application.DisplayAlerts = False
    ThisWorkbook.SaveAs(ProgName)
    Application.DisplayAlerts = True
    # VB2PY (UntranslatedCode) On Error GoTo 0
    CopyMsg = Get_Language_Str('Das Programm wurde in das Verzeichnis') + vbCr + '  \'' + FullDestDir + '\'' + vbCr + Get_Language_Str('kopiert.') + vbCr + vbCr
    #If Create_Desktoplink_w_Powershell(DSKLINKNAME, ProgName) Then
    if CreateDesktopShortcut(DSKLINKNAME, ProgName):
        MsgBox(CopyMsg + Get_Language_Str('In Zukunft kann das Programm über den Link') + vbCr + '   ' + Split(DSKLINKNAME, ' ')(0) + vbCr + '   ' + Split(DSKLINKNAME, ' ')(1) + vbCr + Get_Language_Str('auf dem Desktop gestartet werden'), vbInformation, Get_Language_Str('Programm kopiert und Link auf Desktop erzeugt'))
    else:
        MsgBox(CopyMsg + Get_Language_Str('Beim Anlegen des Links gab es Probleme ;-(' + vbCr + 'Das Programm kann trotzdem von der oben angegebenen Position aus gestartet werden.'), vbInformation, Get_Language_Str('Programm kopiert'))
    CreateDesktopShortcut()('Wiki MobaLedLib', WikiPg_Link, WikiPg_Icon)
    return fn_return_value
    Application.DisplayAlerts = True
    MsgBox(Get_Language_Str('Fehler beim Speichern des Programms im Verzeichnis:') + vbCr + '  \'' + FilePath(ProgName) + '\'', vbCritical, Get_Language_Str('Fehler beim Speichen des Excel Programms'))
    return fn_return_value

def __TestCreateDesktopShortcut():
    #UT------------------------------------
    CreateDesktopShortcut()('Aber Hallo3', ThisWorkbook.FullName)

def __TestCreateWikiDesktopShortcut():
    #UT----------------------------------------
    CreateDesktopShortcut()('Wiki MobaLedLib', WikiPg_Link, WikiPg_Icon)

def CreateDesktopShortcut(LinkName, BookFullName, IconName=DefaultIcon):
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
    Sep = Application.PathSeparator
    Path = ThisWorkbook.Path
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
            MsgBox(Get_Language_Str('Fehler: Das Icon \'') + IconName + Get_Language_Str('\' existiert nicht'), vbCritical, Get_Language_Str('Fehler: Icon nicht im Programm Verzeichnis'))
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

