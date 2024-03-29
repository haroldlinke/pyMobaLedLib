from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M30_Tools as M30
import pattgen.M09_Language as M09
#import pattgen.M09_Language
import ExcelAPI.XLW_Workbook as X02


""" Debug Events
 30.05.20:
# VB2PY (CheckDirective) VB directive took path 1 on USE_SKETCHBOOK_DIR
 06.12.19: Old: "\libraries\MobaLedLib\examples\23_B.LEDs_AutoProg"
 20.07.20: All Versions are located in "\MobaLedLib\Ver_..." to be able to set one exclusion in the virus scan program for all versions
 14.06.20:
 Version of the MLL_pcf file    17.11.19:
 ??
                     (29.12.19: Old E16)
                     (29.12.19: Old E18)
                     (29.12.19: Old D2:D18)
 Column D
                     (29.12.19: Old 20)
 Column E
 Column E
 Column F
                     (29.12.19: Old E46)
                     (29.12.19: Old E46:EW300)
                     (29.12.19: Old F46:EF300)
                     (29.12.19: Old 46)
 Column F
 Column EW
 We just check the attributes of the first x LED columns
                     (29.12.19: Old F24:AI24)
                     (29.12.19: Old 24)
 Column F
                     (29.12.19: Old F43:EW43)
                     (29.12.19: Old 43)
 Column F
 Proportional column width display in Adjust_Column_With_to_Duration()
 The quotiont Max_t / Min_t define the minimal column width.
 If the quotient is below the normal column width (NormColWidth) is used for the small columns
 If the quotient id greater the small columns are limmited to Min_ColWidth. In between the with is adapted proportional
 Normal column width. Also used in Normal_Column_With
 Minimal width
 Could be set to true to regenerate all pictures
 OEM char(MultiEdit): >>   Win: upperline (Line on top of the characters)
 This text is added to the Description in the Prog_Generator as a hint for automatic generated entry which could be replaced automatically
 Contains the sheet name which is used to read WertMin and WertMax, ... from
Public Button_Init_Proc_Finished As Boolean
 05.01.22: Juergen call init function synchronous
 Sheet names:
 COM Port:
 Column where the com port for the Left Arduino on the Main Board is stored
 Column where the com port for the Right Arduino on the Main Board is stored (Not used in this project)
 Column where the com port for programming the Tinys is stored
 Column where the build options for programming the Tinys is stored
 This row contains some sheet specific varaibles. The text uses white color => It' not visible
 This page is used to store the MouseHook. There must be a named range called "MouseHook" (X1).
---------------------------------------------------------------------
----------------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on USE_SKETCHBOOK_DIR
"""

def Read_Sketchbook_Path_from_preferences_txt():
    
    _fn_return_value = None
    Name = String()

    FileStr = String()
    #---------------------------------------------------------------------
    # Attention: The file uses UTF8
    Name = Environ(M01.Env_USERPROFILE) + M01.AppLoc_Ardu + 'preferences.txt'
    FileStr = M30.Read_File_to_String(Name)
    if FileStr != '#ERROR#':
        M01.Sketchbook_Path = M30.ConvertUTF8Str(M30.Get_Ini_Entry(FileStr, 'sketchbook.path='))
        #ThisWorkbook.Sheets(LIBRARYS__SH).Range("Sketchbook_Path") = Sketchbook_Path
        if M01.Sketchbook_Path == '#ERROR#':
            X02.MsgBox(Replace(M09.Get_Language_Str('Fehler: beim lesen des \'sketchbook.path\' in \'#1#\''), '#1#', Name), vbCritical, M09.Get_Language_Str('Fehler beim lesen der Datei:') + ' \'preferences.txt\'')
            return _fn_return_value
        if Left(M01.Sketchbook_Path, 2) == '\\\\':
            X02.MsgBox(M09.Get_Language_Str('Fehler: Der Arduino \'sketchbook.path\' darf kein Netzlaufwerk sein:') + vbCr + '  \'' + M01.Sketchbook_Path + '\'', vbCritical, M09.Get_Language_Str('Ungültiger Arduino \'sketchbook.path\''))
            return _fn_return_value
        M30.CreateFolder(M01.Sketchbook_Path + '\\')
        _fn_return_value = True
    return _fn_return_value

def Get_Sketchbook_Path():
    _fn_return_value = None
    #----------------------------------------------
    Debug.Print('Get_Sketchbook_Path called')
    if M01.Sketchbook_Path == '':
        Read_Sketchbook_Path_from_preferences_txt()
    _fn_return_value = M01.Sketchbook_Path
    return _fn_return_value

def Get_SrcDirInLib():
    _fn_return_value = None
    _fn_return_value = Get_Sketchbook_Path() + M01.SrcDirInLib
    return _fn_return_value

def Get_DestDir_All():
    _fn_return_value = None
    _fn_return_value = Get_Sketchbook_Path() + M01.DestDir_All
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
