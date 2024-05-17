from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M02_Main as M02a
import pattgen.M17_Import_a_Dec_Macro
import pattgen.M80_Multiplexer_INI_Handling
import pattgen.M11_To_Prog_Gen
import ExcelAPI.XLA_Application as X02
import pattgen.M03_Analog_Trend
import pattgen.M30_Tools as M30
import pattgen.M55_PWM_Data_Send

"""---------------------------------------------
---------------------------------------
----------------------------------------
-----------------------------------
-------------------------------------
--------------------------------------------------------
-----------------------------------------------------------------
-------------------------------
---------------------------------
"""


def Import_from_ProgGen_Button_Click():
    #---------------------------------------------
    M02a.Button_Pressed_Proc()
    pattgen.M17_Import_a_Dec_Macro.Import_From_Prog_Gen()

def InsertPicture_Button_Click():
    #---------------------------------------
    M02a.Button_Pressed_Proc()
    pattgen.M80_Multiplexer_INI_Handling.Button_Pressed_Entry('Insert_Picture_M98O01')

def Prog_Generator_Button_Click():
    #----------------------------------------
    M02a.Button_Pressed_Proc()
    pattgen.M11_To_Prog_Gen.Select_Destination_for_the_Pattern_Macro_and_Call_Copy()

def RGB_LED_CheckBox_Click():
    WasProtected = Boolean()
    # 13.06.20:
    #-----------------------------------
    # Added by Misha 20-06-2020
    WasProtected = X02.ActiveSheet.ProtectContents
    # Added by Misha 20-06-2020
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    # Added by Misha 20-06-2020
    pattgen.M03_Analog_Trend.Update_Grafik(False)
    pattgen.M80_Multiplexer_INI_Handling.Change_Number_Of_LEDs
    # Added by Misha 20-06-2020
    if WasProtected:
        M30.Protect_Active_Sheet()
    # Added by Misha 20-06-2020

def Send2Module_Button_Click():
    #-------------------------------------
    M02a.Button_Pressed_Proc()
    pattgen.M55_PWM_Data_Send.Send_to_ATTiny_Main()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Worksheet_Change(Target):
    #--------------------------------------------------------
    # This function is called if the worksheet is changed.
    # It performs several checks after a user input depending form the column of the changed cell:
    M02a.Global_Worksheet_Change(Target)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Worksheet_SelectionChange(Target):
    #-----------------------------------------------------------------
    # Is called by event if the worksheet selection has changed
    M02a.Global_Worksheet_SelectionChange(Target)

def Worksheet_Activate():
    #-------------------------------
    Debug.Print('Worksheet_Activate ' + X02.ActiveSheet.Name)
    X02.Application.OnKey('{Return}', 'Global_On_Enter_Proc')

def Worksheet_Deactivate():
    # 02.06.20: Misha
    #---------------------------------
    M02a.Global_Worksheet_Deactivate()

# VB2PY (UntranslatedCode) Option Explicit
