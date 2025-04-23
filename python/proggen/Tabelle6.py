from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import proggen.M28_Diverse as M28
import ExcelAPI.XLA_Application as P01
import proggen.M25_Columns as M25
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M27_Sheet_Icons as M27

""" 03.04.21: Juergen in case the LEDNr_Display_Type is changed we need to modify the headers and contents
--------------------------------------------------
------------------------------------------------------------------------------------------------------
"""


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Worksheet_Change(Target):
    #--------------------------------------------------
    if not M28.Is_Named_Range(Target):
        return
    if Target.Name.Name == 'LEDNr_Display_Type':
        P01.Application.ScreenUpdating = False
        P01.Application.EnableEvents = False
        curSheet = P01.Application.ActiveSheet
        for s in P01.ThisWorkbook.Worksheets:
            # Find the last data sheet
            if M28.Is_Data_Sheet(s):
                s.Select()
                M25.Make_sure_that_Col_Variables_match()
                M20.Update_Start_LedNr()
        curSheet.Select()
        P01.Application.EnableEvents = True
        P01.Application.ScreenUpdating = True
    elif Target.Name.Name == 'Show_Icon_Column':
        #Application.EnableEvents = False
        M27.Show_Hide_Column_in_all_Sheets(M28.Get_Bool_Config_Var(Target.Name.Name), 'MacIcon_Col')
        Make_Sure_That_One_Macro_Column_is_Visible('Show_Simple_Names', 'LanName_Col')
        #Application.EnableEvents = True
    elif Target.Name.Name == 'Show_Simple_Names':
        #Application.EnableEvents = False
        M27.Show_Hide_Column_in_all_Sheets(M28.Get_Bool_Config_Var(Target.Name.Name), 'LanName_Col')
        Make_Sure_That_One_Macro_Column_is_Visible('Show_Icon_Column', 'MacIcon_Col')
        #Application.EnableEvents = True
    elif Target.Name.Name == 'Show_Macros_Column':
        #Application.EnableEvents = False
        M27.Show_Hide_Column_in_all_Sheets(M28.Get_Bool_Config_Var(Target.Name.Name), 'Config__Col')
        Make_Sure_That_One_Macro_Column_is_Visible('Show_Simple_Names', 'LanName_Col')
        #Application.EnableEvents = True


def Make_Sure_That_One_Macro_Column_is_Visible(Config_Var, Prefered_Column):
    #------------------------------------------------------------------------------------------------------
    if M28.Get_Bool_Config_Var('Show_Icon_Column') == False and M28.Get_Bool_Config_Var('Show_Simple_Names') == False and M28.Get_Bool_Config_Var('Show_Macros_Column') == False:
        M28.Set_String_Config_Var(Config_Var, '1')
        M27.Show_Hide_Column_in_all_Sheets(1, Prefered_Column)

# VB2PY (UntranslatedCode) Option Explicit
