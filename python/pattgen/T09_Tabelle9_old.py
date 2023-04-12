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
import tkinter as tk
from tkinter import ttk,messagebox

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *


import mlpyproggen.Prog_Generator as PG

import ExcelAPI.XLW_Workbook as P01
import pattgen.M02_Main as PAM02
import pattgen.M17_Import_a_decode_Macro as PAM17
import pattgen.M11_To_Prog_Gen as PAM11

from ExcelAPI.XLC_Excel_Consts import *


from vb2py.vbfunctions import *
from vb2py.vbdebug import *


def Import_from_ProgGen_Button_Click():
    #---------------------------------------------
    notimplemented("Import")
    return
    M02.Button_Pressed_Proc()
    M17.Import_From_Prog_Gen()

def InsertPicture_Button_Click():
    #---------------------------------------
    notimplemented("Insert")
    return    
    M02.Button_Pressed_Proc()
    Button_Pressed_Entry('Insert_Picture_M98O01')

def Prog_Generator_Button_Click():
    #----------------------------------------
    notimplemented("Prog Generator")
    return     
    M02.Button_Pressed_Proc()
    PAM11.Select_Destination_for_the_Pattern_Macro_and_Call_Copy()

def RGB_LED_CheckBox_Click():
    WasProtected = Boolean()
    #-----------------------------------
    WasProtected = ActiveSheet.ProtectContents
    if WasProtected:
        ActiveSheet.Unprotect()
        # Added by Misha 20-06-2020
    Update_Grafik(False)
    Change_Number_Of_LEDs
    if WasProtected:
        Protect_Active_Sheet()
        # Added by Misha 20-06-2020

def Send2Module_Button_Click():
    #-------------------------------------
    M02.Button_Pressed_Proc()
    Send_to_ATTiny_Main()

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
    Debug.Print('Worksheet_Activate ' + ActiveSheet.Name)
    Application.OnKey('{Return}', 'Global_On_Enter_Proc')

def __Worksheet_Deactivate():
    #---------------------------------
    Global_Worksheet_Deactivate()

# VB2PY (UntranslatedCode) Option Explicit

def Option_Button_Click():
    #---------------------------------------------
    notimplemented("Options")
    return
    M02.Button_Pressed_Proc()
    
def notimplemented(command):
    n = tk.messagebox.showinfo(command,
                           "Not implemented yet",
                            parent=PG.dialog_parent)    
