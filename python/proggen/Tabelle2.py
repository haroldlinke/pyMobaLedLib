from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import proggen.M06_Write_Header as M06
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M03_Dialog as M03
import ExcelAPI.XLA_Application as P01
import proggen.M22_Hide_UnHide
import proggen.M23_Add_Move_Del_Row
import proggen.M02_Public as M02

"""---------------------------------
------------------------------------
-------------------------------
------------------------------
--------------------------------
-----------------------------------------
------------------------
------------------------------------------------------
-----------------------------
------------------------------
-----------------------------
------------------------------
------------------------------
----------------------------------
----------------------------------
-----------------------------------
--------------------------------------------------------
-----------------------------------------------------------------
-------------------------------
--------------------------------
"""


def Arduino_Button_Click():
    #---------------------------------
    Button_Pressed_Proc()
    M06.Create_HeaderFile()

def ClearSheet_Button_Click():
    #------------------------------------
    Button_Pressed_Proc()
    M20.ClearSheet()

def Dialog_Button_Click():
    #-------------------------------
    Button_Pressed_Proc()
    M03.Dialog_Guided_Input()

def Help_Button_Click():
    #------------------------------
    Button_Pressed_Proc()
    M20.Show_Help()

def Button_Pressed_Proc():
    #--------------------------------
    P01.Selection.Select()
    # Remove the focus from the button
    P01.Application.EnableEvents = True
    # In case the program crashed before
    Correct_Buttonsizes()

def Name_with_LF():
    Hide_Button.Caption = 'Aus- oder' + vbLf + 'Einblenden'

def Correct_Create_Buttonsize(obj):
    #-----------------------------------------
    obj.Height = 160
    obj.Width = 100
    obj.Height = 76
    obj.Width = 60

def Correct_Buttonsizes():
    OldScreenupdating = Boolean()
    #------------------------
    # There is a bug in excel which changes the size of the buttons
    # if the resolution of the display is changed. This happens
    # for instance if the computer is connected to a beamer.
    # To prevent this the buttons are resized with this function.
    # Unfortunately this take some time (600ms)
    #  Start_ms_Timer
    OldScreenupdating = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = False
    Correct_Create_Buttonsize(Arduino_Button)
    Correct_Create_Buttonsize(Dialog_Button)
    Correct_Create_Buttonsize(Insert_Button)
    Correct_Create_Buttonsize(Del_Button)
    Correct_Create_Buttonsize(Move_Button)
    Correct_Create_Buttonsize(Copy_Button)
    Correct_Create_Buttonsize(Hide_Button)
    Correct_Create_Buttonsize(UnHideAll_Button)
    Correct_Create_Buttonsize(ClearSheet_Button)
    Correct_Create_Buttonsize(Options_Button)
    Correct_Create_Buttonsize(Options_Button2)
    Correct_Create_Buttonsize(Help_Button)
    P01.Application.ScreenUpdating = OldScreenupdating
    #  Debug.Print "Correct_Buttonsizes duration " & Get_ms_Duration() & " ms"

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
    Options_Button2.Enabled = Enab
    Help_Button.Enabled = Enab

def EnableAllButtons():
    #-----------------------------
    # Could be called manually after a crash
    EnableDisableAllButtons(True)

def Hide_Button_Click():
    #------------------------------
    Button_Pressed_Proc()
    proggen.M22_Hide_UnHide.Proc_Hide_Unhide()

def Insert_Button_Click():
    Button_Pressed_Proc()
    proggen.M23_Add_Move_Del_Row.Proc_Insert_Line()

def Del_Button_Click():
    #-----------------------------
    Button_Pressed_Proc()
    proggen.M23_Add_Move_Del_Row.Proc_Del_Row()

def Move_Button_Click():
    #------------------------------
    Button_Pressed_Proc()
    proggen.M23_Add_Move_Del_Row.Proc_Move_Row()

def Copy_Button_Click():
    #------------------------------
    Button_Pressed_Proc()
    proggen.M23_Add_Move_Del_Row.Proc_Copy_Row()

def Options_Button_Click():
    #----------------------------------
    Button_Pressed_Proc()
    M20.Option_Dialog()

def Options_Button2_Click():
    # 29.11.23:
    #----------------------------------
    Button_Pressed_Proc()
    M20.Option_Dialog()

def UnHideAll_Button_Click():
    #-----------------------------------
    Button_Pressed_Proc()
    proggen.M22_Hide_UnHide.Proc_UnHide_All()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Worksheet_Change(Target):
    #--------------------------------------------------------
    # This function is called if the worksheet is changed.
    # It performs several checks after a user input depending form the column of the changed cell:
    M20.Global_Worksheet_Change(Target)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Worksheet_SelectionChange(Target):
    #-----------------------------------------------------------------
    # Is called by event if the worksheet selection has changed
    M20.Global_Worksheet_SelectionChange(Target)

def Worksheet_Activate():
    #-------------------------------
    M20.Global_Worksheet_Activate()

def Worksheet_Calculate():
    #--------------------------------
    # This proc is also called if an other workbook (from a mail/internet) is opened    24.02.20:
    if M02.DEBUG_CHANGEEVENT:
        Debug.Print('Worksheet_Calculate() in sheet \'DCC\' called')
    if P01.ActiveSheet is None:
        return
    if P01.Cells(1, 1).Parent.Name == P01.ActiveSheet.Name:
        # At program start the Worksheet_Calculate proc is called without activating the sheet.
        M20.Global_Worksheet_Calculate()
        # This causes a crash in Make_sure_that_Col_Variables_match

# VB2PY (UntranslatedCode) Option Explicit
