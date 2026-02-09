# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
# * Author: Harold Linke
# * Date: January 1st, 2020
# * Copyright: Harold Linke 2020
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 10.03.2020 - Harold Linke - first release
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

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import tkinter as tk
import sys

import proggen.M06_Write_Header as M06
import proggen.M03_Dialog as M03
import proggen.M01_Gen_Release_Version as M01
import proggen.M02_Public as M02
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M12_Copy_Prog as M12
import proggen.M17_Import_old_Data as M17
import ExcelAPI.XLA_Application as P01
import mlpyproggen.Prog_Generator as PG
import proggen.M22_Hide_UnHide as M22
import proggen.M23_Add_Move_Del_Row as M23
import proggen.M25_Columns as M25
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M27_Sheet_Icons as M27
import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
import proggen.M32_DCC as M32
import proggen.M37_Inst_Libraries as M37
import proggen.M38_Extensions as M38
import proggen.M39_Simulator as M39

import proggen.Userform_DialogGuide1 as D01
import proggen.Userform_Select_Typ_DCC as D02
import proggen.Userform_Select_Typ_SX as D02SX
import proggen.Userform_Description as D03
import proggen.UserForm_Connector as D04
import proggen.StatusMsg_Userform as D09
import proggen.Select_COM_Port_Userform as D08
import proggen.UserForm_Options as D10
import proggen.Userform_SimpleInput as D11
import proggen.Select_ProgGen_Src_Form as D12
import proggen.Select_ProgGen_Dest_Form as D13
import proggen.Userform_LEDAnim as D14
import proggen.Userform_ServoAnim as D15
import proggen.Userform_LEDColorAnim as D16
import proggen.UserForm_ConfirmLicense as UF_Conf
import pgcommon.G00_common as G00

def Arduino_Button_Click(event=None):
    #---------------------------------
    __Button_Pressed_Proc()
    M06.Create_HeaderFile()
    
def Arduino_Button_Shift_Click(event=None):
    #---------------------------------
    __Button_Pressed_Proc()
    P01.shift_key = True
    M06.Create_HeaderFile()


def ClearSheet_Button_Click():
    #------------------------------------
    __Button_Pressed_Proc()
    M20.ClearSheet()

def NewSheet_Button_Click():
    #------------------------------------
    __Button_Pressed_Proc()
    G00.New_Sheet()    
    
def Dialog_Button_Click():
    #-------------------------------
    __Button_Pressed_Proc()
    M03.Dialog_Guided_Input()

def Help_Button_Click():
    #------------------------------
    __Button_Pressed_Proc()
    M20.Show_Help()

def __Button_Pressed_Proc():
    #--------------------------------
    #Selection.Select()
    #Application.EnableEvents = True
    #__Correct_Buttonsizes()
    pass

def __Name_with_LF():
    Hide_Button.Caption = 'Aus- oder' + vbLf + 'Einblenden'

def __Correct_Create_Buttonsize(obj):
    #-----------------------------------------
    obj.Height = 160
    obj.Width = 100
    obj.Height = 76
    obj.Width = 60

def __Correct_Buttonsizes():
    OldScreenupdating = Boolean()
    #------------------------
    # There is a bug in excel which changes the size of the buttons
    # if the resolution of the display is changed. This happens
    # fore instance if the computer is connected to a beamer.
    # To prevent this the buttons are resized with this function.
    OldScreenupdating = Application.ScreenUpdating
    Application.ScreenUpdating = False
    __Correct_Create_Buttonsize(Arduino_Button)
    __Correct_Create_Buttonsize(Dialog_Button)
    __Correct_Create_Buttonsize(Insert_Button)
    __Correct_Create_Buttonsize(Del_Button)
    __Correct_Create_Buttonsize(Move_Button)
    __Correct_Create_Buttonsize(Copy_Button)
    __Correct_Create_Buttonsize(Hide_Button)
    __Correct_Create_Buttonsize(UnHideAll_Button)
    __Correct_Create_Buttonsize(ClearSheet_Button)
    __Correct_Create_Buttonsize(Options_Button)
    __Correct_Create_Buttonsize(Help_Button)
    Application.ScreenUpdating = OldScreenupdating

def EnableDisableAllButtons(Enab):
    #------------------------------------------------------
    Arduino_Button.Enabled = Enab
    Dialog_Button.Enabled = Enab
    Insert_Button.Enabled = Enab
    Del_Button.Enabled = Enab
    Move_Button.Enabled = Enab
    Copy_Button.Enabled = Enab
    Hide_Button.Enabled = Enab
    UnHideAll_Button.Enabled = Enab
    ClearSheet_Button.Enabled = Enab
    Options_Button.Enabled = Enab

def __EnableAllButtons():
    #-----------------------------
    # Could be called manually after a crash
    EnableDisableAllButtons(True)

def Hide_Button_Click():
    #------------------------------
    __Button_Pressed_Proc()
    #notimplemented("Hide/Unhide")
    M22.Proc_Hide_Unhide()

def Insert_Button_Click():
    __Button_Pressed_Proc()
    P01.ActiveSheet.addrow_before_current_row()

def Del_Button_Click():
    #-----------------------------
    __Button_Pressed_Proc()
    P01.ActiveSheet.deleterows()

def Move_Button_Click():
    #------------------------------
    __Button_Pressed_Proc()
    #notimplemented("Move Row")
    M23.Proc_Move_Row()

def Copy_Button_Click():
    #------------------------------
    __Button_Pressed_Proc()
    M23.Proc_Copy_Row()

def Options_Button_Click():
    #----------------------------------
    __Button_Pressed_Proc()
    #notimplemented("Options")
    M20.Option_Dialog()

def UnHideAll_Button_Click():
    #-----------------------------------
    __Button_Pressed_Proc()
    #notimplemented("UnHide All")
    M22.Proc_UnHide_All()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def __Worksheet_Change(Target):
    #--------------------------------------------------------
    # This function is called if the worksheet is changed.
    # It performs several checks after a user input depending form the column of the changed cell:
    Global_Worksheet_Change(Target)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def __Worksheet_SelectionChange(Target):
    #-----------------------------------------------------------------
    # Is called by event if the worksheet selection has changed
    Global_Worksheet_SelectionChange(Target)

def __Worksheet_Activate():
    #-------------------------------
    Global_Worksheet_Activate()

def __Worksheet_Calculate():
    #--------------------------------
    # This proc is also called if an other workbook (from a mail/internet) is opened    24.02.20:
    if DEBUG_CHANGEEVENT:
        Debug.Print('Worksheet_Calculate() in sheet \'DCC\' called')
    if ActiveSheet is None:
        return
    if Cells.Parent.Name == ActiveSheet.Name:
        Global_Worksheet_Calculate()

def Workbook_Open():
    DidCopy = Boolean()
    #-------------------------
    P01.Application.ScreenUpdating = False
    #P01.EnableAllButtons()
    P01.Application.EnableEvents = False
    #Cleare_Mouse_Hook()
    Debug.Print('Workbook_Open() called')
    PG.ThisWorkbook.Sheets(M02.LANGUAGES_SH).Visible = False
    PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH).Visible = False
    PG.ThisWorkbook.Sheets(M02.PAR_DESCR_SH).Visible = False
    PG.ThisWorkbook.Sheets(M02.LIBRARYS__SH).Visible = False
    PG.ThisWorkbook.Sheets(M02.PLATFORMS_SH).Visible = False
    M30.Check_Version()
    if P01.ActiveSheet.Name == M02.ConfigSheet:
        PG.ThisWorkbook.Sheets(M02.START_SH).Select()
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
        M38.__Load_Extensions()
        pass
    P01.Application.ScreenUpdating = True
    #if ENABLE_CRITICAL_EVENTS_WB:
    #    # Generate events for special actions
    #    # VB2PY (UntranslatedCode) On Error GoTo ErrorDetectEvents
    #    Application.CommandBars['row'].FindControl[Id= 883].OnAction = 'myHideRows_Event'
    #    Application.CommandBars['row'].FindControl[Id= 884].OnAction = 'myUnhideRows_Event'
    #    # VB2PY (UntranslatedCode) On Error GoTo 0
    #else:
    #    Remove_Special_Events()
    DidCopy = False
    if M12.Copy_Prog_If_in_LibDir_WithResult(DidCopy):
        M17.Import_from_Old_Version_If_exists(( not DidCopy ))
    if M28.Get_Num_Config_Var_Range('SimAutostart', 0, 3, 0) == 1:
        M39.OpenSimulator()
    P01.Application.EnableEvents = True
    return
    MsgBox('Interner Fehler: Die Event Routinen wurden nicht gefunden', vbCritical, 'Interner Fehler')
        
def workbook_init(workbook):
    #M01.__Release_or_Debug_Version(True)
    
    if P01.checkplatform("Windows"):
        M02.AppLoc_Ardu = '\\AppData\\Local\\Arduino15\\'
        logging.debug("Workbook_init - AppLoc_Ardu:"+M02.AppLoc_Ardu)
        M02.Env_USERPROFILE = 'USERPROFILE'
        logging.debug("Workbook_init - Env_USERPROFILE:"+M02.Env_USERPROFILE)
    elif P01.checkplatform("Darwin"):
        M02.AppLoc_Ardu = "/Library/Arduino15/"
        logging.debug("Workbook_init - AppLoc_Ardu:"+M02.AppLoc_Ardu)
        M02.Env_USERPROFILE = 'HOME'
        logging.debug("Workbook_init - Env_USERPROFILE:"+M02.Env_USERPROFILE)        
    else:
        M02.AppLoc_Ardu = "/.arduino15/"
        logging.debug("Workbook_init - AppLoc_Ardu:"+M02.AppLoc_Ardu)
        M02.Env_USERPROFILE = 'HOME'
        logging.debug("Workbook_init - Env_USERPROFILE:"+M02.Env_USERPROFILE)
    init_UserForms()
    for sheet in workbook.sheets:
        worksheet_init(sheet)
    #Workbook_Open()    
    P01.Application.set_canvas_leftclickcmd(M32.DCCSend)    
    
def worksheet_init(act_worksheet):
    return

    first_call=True

    if act_worksheet.Datasheet:
        P01.ActiveSheet=act_worksheet
        for row in range(3,M30.LastUsedRow()):
            M20.Update_TestButtons(row,First_Call=first_call)
            M20.Update_StartValue(row)
            first_call=False
            
def worksheet_redraw(sheet):
    if sheet.Datasheet:
        sheet.clear_shapelist()
        P01.ActiveSheet=sheet
        M25.Make_sure_that_Col_Variables_match(Sh=sheet)
        for row in range(3,M30.LastUsedRow()):
            MacroStr = P01.Cells(row, M25.Config__Col, ws=sheet)
            if MacroStr != "":
                M27.FindMacro_and_Add_Icon_and_Name(MacroStr, row, sheet)
                M20.Update_TestButtons(row, redraw=True)
            #M20.Update_StartValue(row)
            
    
    
def init_UserForms():
    global StatusMsg_UserForm, UserForm_Select_Typ_DCC, UserForm_Select_Typ_SX, Select_COM_Port_UserForm,UserForm_Options,UserForm_DialogGuide1,UserForm_Description,UserForm_Connector
    global Userform_SimpleInput,Select_ProgGen_Src_Form, Select_ProgGen_Dest_Form, UserForm_PCAnim,  UserForm_LEDColorAnim,  UserForm_LEDAnim,  UserForm_ConfirmLicense
    
    UserForm_DialogGuide1 = D01.UserForm_DialogGuide1()
    UserForm_Select_Typ_DCC = D02.UserForm_Select_Typ_DCC()
    UserForm_Select_Typ_SX = D02SX.UserForm_Select_Typ_SX()
    UserForm_Description = D03.UserForm_Description()
    UserForm_Connector = D04.UserForm_Connector(PG.global_controller)
    Select_COM_Port_UserForm = D08.CSelect_COM_Port_UserForm()
    StatusMsg_UserForm = D09.CStatusMsg_UserForm()
    UserForm_Options = D10.CUserForm_Options()
    Userform_SimpleInput = D11.UserForm_SimpleInput()
    Select_ProgGen_Src_Form = D12.CSelect_ProgGen_Src_Form(PG.global_controller)
    Select_ProgGen_Dest_Form = D13.CSelect_ProgGen_Dest_Form(PG.global_controller)
    UserForm_PCAnim = D15.UserForm_ServoAnim(PG.global_controller)
    UserForm_LEDAnim = D14.UserForm_LEDAnim(PG.global_controller)
    UserForm_LEDColorAnim = D16.UserForm_LEDColorAnim(PG.global_controller)
    UserForm_ConfirmLicense = UF_Conf.CUserForm_ConfirmLicense(PG.global_controller)

    
def notimplemented(command):
    n = tk.messagebox.showinfo(command,
                           "Not implemented yet",
                            parent=PG.dialog_parent)    

# VB2PY (UntranslatedCode) Option Explicit

#***************************
#* UserForms
#***************************

StatusMsg_UserForm = None
UserForm_Select_Typ_DCC = None
UserForm_Select_Typ_SX = None
Select_COM_Port_UserForm = None
Select_ProgGen_Src_Form = None
Select_ProgGen_Dest_Form = None

#**************************
#'  Port handling functions
#**************************

def port_is_busy(port):
    if type(port)==int:
        return port <0
    elif type(port)==str:
        return port.startswith("*")
    elif type(port)==P01.CRange:
        strport=str(port)
        return strport.startswith("*")
    
def port_is_available(port):
    if type(port)==int:
        return port > 0
    elif type(port)==str or type(port)==P01.CRange:
        strport=str(port)
        port_available = not (strport.startswith("*") or strport=="COM?" or strport==" " or strport=="NO DEVICE" or strport=="")
        if port_available:
            if strport.startswith("IP:"):
                pass
        return port_available
    return False
    
def port_reset(port):
    strport=str(port)
    if strport.startswith("*"):
        return(strport[1:])
    else:
        return port
    
def port_check_format(port):
    strport=str(port)
    if IsNumeric(strport):
        return "COM"+strport
    else:
        return strport
    
def port_set_busy(port):
    strport=str(port)
    if strport.startswith("*") or strport.startswith("IP:"):
        return(strport)
    else:
        return "*"+port
    
   
def is_64bit() -> bool:
    return sys.maxsize > 2**32