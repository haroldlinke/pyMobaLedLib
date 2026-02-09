from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as P01
import proggen.M28_Diverse as M28
import proggen.M02_Public as M02
import proggen.M37_Inst_Libraries as M37
import proggen.M01_Gen_Release_Version as M01
import proggen.M12_Copy_Prog as M12
import proggen.M17_Import_old_Data as M17
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M30_Tools as M30
import proggen.M09_Language as M09
import proggen.M08_ARDUINO as M08
import proggen.M38_Extensions as M38
import proggen.M39_Simulator as M39


""" Deactivate this for tests. Call "Remove_Special_Events" below if disabled
 If this is disabled the LED numbers are not ubdated if lines are hidden or unhidden
 But the numbers are corrected if oter things are changed (Enable hook changed, macros added, ...
 => I have disabled it on 12.10.20.
----------------------------------
--------------------------------------------------
-------------------------
****************************** Mouse Events **************************
# VB2PY (CheckDirective) VB directive took path 2 on 0
 Es gibt zwei Methoden wie man die RECHTE Maustaste abfängt:
 Die eine muss in "Dieser Arbeitsmappe" stehen:
# VB2PY (CheckDirective) VB directive took path 2 on 0
 Die andere muss in der Code Seite es entsprechenden Sheets stehen:
  Private Sub Worksheet_BeforeRightClick(ByVal Target As Range, Cancel As Boolean)

 https://docs.microsoft.com/de-de/office/vba/api/excel.worksheet.beforerightclick

 !! RECHTE Taste nicht die linke [X]<- [ ]
    Debug.Print Activesheet.Name ":Worksheet_BeforeRightClick " & Target.Row
  End Sub
--------------------------------------------------------------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 2 on 0
"""

ENABLE_CRITICAL_EVENTS_WB = False

def Remove_Special_Events():
    # 11.10.20:
    #----------------------------------
    # Events which generate a link to Prog_Generator_MobaLedLib.xlsm
    # They get active if hidden lines are unhiden
    #test P01.Application.CommandBars['row'].FindControl[Id= 883].OnAction = ''
    # "myHideRows_Event"
    #test P01.Application.CommandBars['row'].FindControl[Id= 884].OnAction = ''
    # "myUnhideRows_Event"
    pass

def Workbook_BeforeClose(Cancel):
    #--------------------------------------------------
    if ENABLE_CRITICAL_EVENTS_WB:
        #test P01.Application.CommandBars['row'].FindControl[Id= 883].OnAction = ''
        #test P01.Application.CommandBars['row'].FindControl[Id= 884].OnAction = ''
        pass

def Workbook_Open():
    DidCopy = Boolean()

    OldProgGeneratorFilename = String()
    #-------------------------
    P01.Application.ScreenUpdating = False
    M28.EnableAllButtons()
    P01.Application.EnableEvents = False
    # 28.10.19.
    #Cleare_Mouse_Hook()
    # 28.04.20:
    Debug.Print('Workbook_Open() called')
    # 23.02.20:
    P01.ThisWorkbook.SheetsDict[M02.LANGUAGES_SH].Visible = False
    # 29.04.20: Added: ThisWorkbook to hopefully prevent problems at startup
    P01.ThisWorkbook.SheetsDict[M02.LIBMACROS_SH].Visible = False
    P01.ThisWorkbook.SheetsDict[M02.PAR_DESCR_SH].Visible = False
    P01.ThisWorkbook.SheetsDict[M02.LIBRARYS__SH].Visible = False
    # 28.05.20:
    P01.ThisWorkbook.SheetsDict[M02.PLATFORMS_SH].Visible = False
    # 14.10.21: Juergen
    M30.Check_Version()
    # 21.11.21: Juergen
    if P01.ActiveSheet.Name == M02.ConfigSheet:
        P01.ThisWorkbook.Sheets(M02.START_SH).Select()
    # 30.05.20: In case one of the hidden sheets was active before
    M37.Init_Libraries_Page()
    M09.__Update_Language_in_All_Sheets()
    M28.Clear_COM_Port_Check_and_Set_Cursor_in_all_Sheets(False)
    M01.Set_Config_Default_Values_at_Program_Start()
    
    ARDUINO_exe = M08.Find_ArduinoExe()
    if ARDUINO_exe !="":
        continue_update=True
    else:
        P01.MsgBox(M09.Get_Language_Str('Die ARDUINO IDE wurde nicht gefunden. Entweder wurde ARDUINO noch nicht installiert (Windows) oder das ARDUINO-Verzeichnis wurde noch nicht eingegeben (LINUX/Mac)'), vbInformation, M09.Get_Language_Str('ARDUINO IDE nicht gefunden'))
        continue_update= False
    if continue_update:    
        M37.Install_Missing_Libraries_and_Board()
        # 28.05.20:
        M38.__Load_Extensions()
        # 26.01.22 Juergen add Extension feature
    P01.Application.ScreenUpdating = True
    #if ENABLE_CRITICAL_EVENTS_WB:
        # Generate events for special actions
        # VB2PY (UntranslatedCode) On Error GoTo ErrorDetectEvents
        #test P01.Application.CommandBars['row'].FindControl[Id= 883].OnAction = 'myHideRows_Event'
        #test P01.Application.CommandBars['row'].FindControl[Id= 884].OnAction = 'myUnhideRows_Event'
        # VB2PY (UntranslatedCode) On Error GoTo 0
    #    pass
    #else:
    #    Remove_Special_Events()
    # 13.10.20:
    # 12.11.21: Juergen ImportOld version also in case of Beta Update
    DidCopy = False
    # 19.01.24: Juergen add OldProgGeneratorFilename
    if M12.Copy_Prog_If_in_LibDir_WithResult(DidCopy):
        M17.Import_from_Old_Version_If_exists(not DidCopy)
    if M28.Get_Num_Config_Var_Range('SimAutostart', 0, 3, 0) == 1:
        # 04.04.22: Juergen Simulator
        M39.OpenSimulator()
    P01.Application.EnableEvents = True
    # 28.10.19.
    return
    P01.MsgBox('Interner Fehler: Die Event Routinen wurden nicht gefunden', vbCritical, 'Interner Fehler')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cancel - ByRef 
def Workbook_SheetBeforeDoubleClick(Sh, Target, Cancel):
    #--------------------------------------------------------------------------------------------------------------
    if M02.DEBUG_CHANGEEVENT:
        Debug.Print('DieserArbeitsmappe: Workbook_SheetBeforeDoubleClick:' + Target.Row + ' Cancel=' + Cancel)
    M20.Proc_DoubleClick(Sh, Target, Cancel)
    #Cancel = True

# VB2PY (UntranslatedCode) Option Explicit
