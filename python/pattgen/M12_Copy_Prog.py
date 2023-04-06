from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import pattgen.M30_Tools as M30
import pattgen.M09_Language
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.Pattern_Generator as PG

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
    _fn_return_value = None
    CopyDir = Boolean()

    SrcPath = String()

    SrcName = String()
    #---------------------------------------------------------------------------------------------------------------------
    # Could also copy a whole folder with all sub directories
    # If SourceName is empty the file/directory "Name" is copied from the program dir to DestDir
    # If a SourceName is given the file the source dir is extracted from the name.
    SrcPath = PG.ThisWorkbook.Path + '\\'
    SrcName = Name
    if SourceName != '':
        if M30.FilePath(SourceName) != '':
            SrcPath = M30.FilePath(SourceName)
        SrcName = M30.FileNameExt(SourceName)
    if Dir(SrcPath + SrcName) == '':
        if Dir(SrcPath + SrcName, vbDirectory) != '':
            # Check if it's a directory
            CopyDir = True
        else:
            X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Die Datei oder das Verzeichnis \'') + SrcName + pattgen.M09_Language.Get_Language_Str('\' ist nicht im Verzeichnis') + vbCr + '  \'' + SrcPath + '\'' + vbCr + pattgen.M09_Language.Get_Language_Str('vorhanden.'), vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler beim kopieren'))
            return _fn_return_value
    # VB2PY (UntranslatedCode) On Error GoTo CopyError
    if CopyDir:
        ## VB2PY (CheckDirective) VB2PY Python directive
        shutil.copytree(SrcPath + SrcName, DestDir + Name, dirs_exist_ok == True)
    else:
        FileCopy(SrcPath + SrcName, DestDir + Name)
        # Copy single file
    # VB2PY (UntranslatedCode) On Error GoTo 0
    _fn_return_value = True
    return _fn_return_value
    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Es ist ein Fehler beim kopieren der Datei oder des Verzeichnisses \'') + SrcName + pattgen.M09_Language.Get_Language_Str('\' vom Verzeichnis') + vbCr + '  \'' + SrcPath + '\'' + vbCr + pattgen.M09_Language.Get_Language_Str('nach \'') + DestDir + pattgen.M09_Language.Get_Language_Str('\' aufgetreten'), vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler beim kopieren'))
    return _fn_return_value

def Copy_File_With_new_Name_If_Exists(Name):
    _fn_return_value = None
    ProgName = String()

    FullDestDir = String()
    # 14.06.20:
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
            return _fn_return_value
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Achtung: Die Datei \'') + M30.FileNameExt(Name) + pattgen.M09_Language.Get_Language_Str('\' existiert bereits im Verzeichnis') + vbCr + '  \'' + FullDestDir + '\'' + vbCr + vbCr + pattgen.M09_Language.Get_Language_Str('Das existierende Programm wurde unter dem Namen \'') + M30.FileName(CopyName) + pattgen.M09_Language.Get_Language_Str('\' gesichert.') + vbCr + vbCr + pattgen.M09_Language.Get_Language_Str('Dieser Fehler tritt auf wenn das Programm mehrfach aus dem \'extras\' Verzeichnis ' + 'der Bibliothek gestartet wird.') + vbCr + pattgen.M09_Language.Get_Language_Str('Das Programm muss nur beim ersten mal nach der Installation der MobaLedLib aus dem ' + 'Bibliotheksverzeichnis gestartet werden. Dabei wird es in das oben genannte Verzeichnis ' + 'kopiert damit die Bibliothek unverändert bleibt.' + vbCr + 'Im folgenden wird ein Link auf dem Desktop kreiert über den das Programm in Zukunft gestartet wird.'), vbInformation, pattgen.M09_Language.Get_Language_Str('Programm existiert bereits (Mehrfacher Start aus \'extras\' Verzeichnis)'))
    _fn_return_value = True
    return _fn_return_value

def Copy_Prog_If_in_LibDir():
    _fn_return_value = None
    FullDestDir = String()

    Parts = Variant()

    p = Variant()

    ActDir = String()

    ProgName = String()

    CopyMsg = String()
    #--------------------------------------------------
    # Return true if the programm was stored in the LibDir
    if InStr(UCase(PG.ThisWorkbook.Path + '\\'), UCase(M01.Get_SrcDirInLib())) == 0:
        # The program is not stored in the library directory
        return _fn_return_value
        # => We don't have to copy it
    _fn_return_value = True
    # 30.05.20: Disabled
    #Dim UserProfile As String
    #UserProfile = Environ(Env_USERPROFILE)
    #If UserProfile = "" Then
    #   MsgBox Get_Language_Str("Fehler: Die Variable 'USERPROFILE' ist nicht definiert ;-(" & vbCr & _

    #            vbCr & _

    #            "Das Programm wird nach 'C:") & Get_DestDir_All() & Get_Language_Str("' kopiert."), vbInformation, _

    #          Get_Language_Str("Fehler beim kopieren des LED Programmiertool")
    #   UserProfile = "C:"
    #End If
    # Create the destination directory if it doesn't exist
    FullDestDir = M01.Get_DestDir_All()
    # VB2PY (UntranslatedCode) On Error Resume Next
    # In case the directory exists
    Parts = Split(FullDestDir, '\\')
    for p in Parts:
        ActDir = ActDir + p + '\\'
        if Len(ActDir) > 3:
            MkDir(ActDir)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    # 14.06.20: Copy both programms
    #If INTPROGNAME = "Pattern_Configurator" Then
    if not FileCopy_with_Check(FullDestDir, 'Pattern_Config_Examples'):
        return _fn_return_value
    #ElseIf INTPROGNAME = "Prog_Generator" Then
    if not FileCopy_with_Check(FullDestDir, 'LEDs_AutoProg'):
        return _fn_return_value
    # If Not FileCopy_with_Check(FullDestDir, "Prog_Generator_MobaLedLib.pdf") Then Exit Function
    #Else
    X02.MsgBox('Internal error: Unknown \'INTPROGNAME\'', vbCritical, 'Internal Error')
    #End If
    if not FileCopy_with_Check(FullDestDir, 'Icons'):
        return _fn_return_value
    # Is used in both programms
    if not Copy_File_With_new_Name_If_Exists(FullDestDir + M01.SECOND_PROG + '.xlsm'):
        return _fn_return_value
    # 14.06.20: Copy also the second program
    if not FileCopy_with_Check(FullDestDir, M01.SECOND_PROG + '.xlsm'):
        return _fn_return_value
    CreateDesktopShortcut(M01.SECOND_LINK, FullDestDir + M01.SECOND_PROG + '.xlsm', M01.SECOND_ICON)
    # 14.06.20: Create Link to the second programm
    ProgName = FullDestDir + PG.ThisWorkbook.Name
    if not Copy_File_With_new_Name_If_Exists(ProgName):
        return _fn_return_value
    # 14.06.20: Moved in seperate function
    # VB2PY (UntranslatedCode) On Error GoTo ErrSaveAs
    X02.Application.DisplayAlerts = False
    PG.ThisWorkbook.SaveAs(ProgName)
    X02.Application.DisplayAlerts = True
    # VB2PY (UntranslatedCode) On Error GoTo 0
    CopyMsg = pattgen.M09_Language.Get_Language_Str('Das Programm wurde in das Verzeichnis') + vbCr + '  \'' + FullDestDir + '\'' + vbCr + pattgen.M09_Language.Get_Language_Str('kopiert.') + vbCr + vbCr
    #If Create_Desktoplink_w_Powershell(DSKLINKNAME, ProgName) Then
    if CreateDesktopShortcut(M01.DSKLINKNAME, ProgName):
        X02.MsgBox(CopyMsg + pattgen.M09_Language.Get_Language_Str('In Zukunft kann das Programm über den Link') + vbCr + '   ' + Split(M01.DSKLINKNAME, ' ')(0) + vbCr + '   ' + Split(M01.DSKLINKNAME, ' ')(1) + vbCr + pattgen.M09_Language.Get_Language_Str('auf dem Desktop gestartet werden'), vbInformation, pattgen.M09_Language.Get_Language_Str('Programm kopiert und Link auf Desktop erzeugt'))
    else:
        X02.MsgBox(CopyMsg + pattgen.M09_Language.Get_Language_Str('Beim Anlegen des Links gab es Probleme ;-(' + vbCr + 'Das Programm kann trotzdem von der oben angegebenen Position aus gestartet werden.'), vbInformation, pattgen.M09_Language.Get_Language_Str('Programm kopiert'))
    CreateDesktopShortcut('Wiki MobaLedLib', M01.WikiPg_Link, M01.WikiPg_Icon)
    # Create Link to the Wiki
    return _fn_return_value
    X02.Application.DisplayAlerts = True
    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler beim Speichern des Programms im Verzeichnis:') + vbCr + '  \'' + M30.FilePath(ProgName) + '\'', vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler beim Speichen des Excel Programms'))
    return _fn_return_value

def TestCreateDesktopShortcut():
    #UT------------------------------------
    CreateDesktopShortcut('Aber Hallo3', PG.ThisWorkbook.FullName)

def TestCreateWikiDesktopShortcut():
    #UT----------------------------------------
    CreateDesktopShortcut('Wiki MobaLedLib', M01.WikiPg_Link, M01.WikiPg_Icon)

def CreateDesktopShortcut(LinkName, BookFullName, IconName=M01.DefaultIcon):
    _fn_return_value = None
    location = 'Desktop'

    LinkExt = '.lnk'

    oWsh = Object()

    oShortcut = Object()

    Sep = String()

    Path = String()

    DesktopPath = String()

    Shortcut = String()
    # 14.02.20:
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Create a custom icon shortcut on the users desktop
    # Constant string values, you can replace "Desktop"
    # with any Special Folders name to create the shortcut there
    # Object variables
    # String variables
    # Initialize variables
    Sep = X02.Application.PathSeparator
    Path = PG.ThisWorkbook.Path
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
    _with80 = oShortcut
    _with80.TargetPath = BookFullName
    if IconName != '':
        if Dir(Path + Sep + IconName) == '':
            X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Das Icon \'') + IconName + pattgen.M09_Language.Get_Language_Str('\' existiert nicht'), vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler: Icon nicht im Programm Verzeichnis'))
        else:
            _with80.IconLocation = Path + Sep + IconName
    _with80.Save()
    # Explicitly clear memory
    oWsh = None
    oShortcut = None
    _fn_return_value = True
    return _fn_return_value
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
