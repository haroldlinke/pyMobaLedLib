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
import tkinter as tk
import mlpyproggen.Prog_Generator as PG
import ExcelAPI.XLF_FormGenerator as XLF
import ExcelAPI.XLA_Application as X02

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

import ExcelAPI.XLA_Application as X02
import pattgen.M30_Tools as M30
import pattgen.M01_Public_Constants_a_Var as M01
import mlpyproggen.Pattern_Generator as PG
import proggen.M09_Language as M09
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_Diverse as M28
import proggen.M50_Exchange as M50
import proggen.F00_mainbuttons as F00

# VB2PY (UntranslatedCode) Option Explicit

#################################################################################################

class CAttinyDP_UserForm:

    def __init__(self,controller):
        self.controller    = controller
        self.IsActive      = False
        self.Form          = None
        self.UserForm_Res  = ""
        self.Controls      = []
        self.Controls_Dict = {}
        
        self.OK_Pressed = False
                

        self.Attiny_DP_UserForm_RSC = {"UserForm":{
            "Name"          : "AttinyDP_UserForm",
                                "BackColor"     : "#000008",
                                "BorderColor"   : "#000012",
                                "Caption"       : "Program Attiny Direct",
                                "Height"        : 284,
                                "Left"          : 0,
                                "Top"           : 0,
                                "Type"          : "MainWindow",
                                "Visible"       : True,
                                "Width"         : 229,
                                "Components"    : [{"Name":"Label1","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Direktes Hochladen einer neuen Firmware zum Attiny, wobei der Attiny in der MLL-Kette bleibt.\nACHTUNG: Nur zum Testen, wenn man weiß was man tut!!!!",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":60,"Left":18,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":192},

                                                   {"Name":"Abort_Button","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Abbrechen",
                                                    "Command": self.Abort_Button_Click ,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":48,"Top":222,"Type":"CommandButton","Visible":True,"Width":72},
                                                   
                                                   {"Name":"OK_Button","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Auswahl",
                                                    "Command": self.OK_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":132,"Top":222,"Type":"CommandButton","Visible":True,"Width":72},
                                                                                                                                                                                                                                                                                                                               
                                                   ]}
                                             }
        
       # {"Name":"Enter_Bootloader_CheckBox","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
       # "Caption":"Enter Boatloader",
       #  "ControlTipText":"Wenn das normale Servoprogramm läuft, wird der Bootloader im Attiny gestartet","ForeColor":"#000012","Height":18,"Left":24,"Top":70,"Type":"CheckBox","Visible":False,"Width":185},

       # {"Name":"Set_Status_LED_CheckBox","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
       #  "Caption":"Status LED ADresse setzen",
       #  "ControlTipText":"Ändert die Adresse der Status-LED","ForeColor":"#000012","Height":18,"Left":24,"Top":100,"Type":"CheckBox","Visible":False,"Width":185},

       # {"Name":"Upload_Hex_File_CheckBox","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
       #  "Caption":"Hex-Datei Hochladen",
       #  "ControlTipText":"Eine Hex-Datei wird zum Attiny hochgeladen","ForeColor":"#000012","Height":18,"Left":24,"Top":130,"Type":"CheckBox","Visible":False,"Width":185},
                
        
    def ControlsFind(self,searchname):
        #return control with searchname
        for control in self.Controls:
            if control.Name==searchname:
                return control
        return None
    
    def destroy(self):
        Debug.Print("Destroy Form")
        self.Form.destroy()

    def Abort_Button_Click(self):
        #-------------------------------
        self.Hide()
    
    def OK_Button_Click(self):
        
        #----------------------------
        self.OK_Pressed = True
        
        self.Hide()
    
    def UserForm_Initialize(self):
        #--------------------------------
        #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
        self.Form=XLF.generate_form(self.Attiny_DP_UserForm_RSC,self.controller,dlg=self,modal=False, jump_table=PG.ThisWorkbook.jumptable, defaultfont=X02.DefaultFont)
        
        #X02.Center_Form(Me)
        #Change_Language_in_Dialog(Me)
    
    def Hide(self):
        self.IsActive=False
        self.Form.destroy()

    def AddControl(self,control):
        self.Controls.append(control)
        self.Controls_Dict[control.Name]=control

    def Show_Dialog(self, AttinyAdress=None, StatusLEDAdress=None):
        
        #--------------------------------------
        self.UserForm_Initialize()
        self.OK_Pressed = False
        self.Show(AttinyAdress=AttinyAdress)
        return self.OK_Pressed
    
    # VB2PY (UntranslatedCode) Option Explicit
    
    def Show(self, AttinyAdress=None):
        self.IsActive = True
        self.Form.update()
        self.Form.deiconify()
        self.Form.focus_set()
        self.Form.focus_force()
        self.Form.grab_set()
        self.controller.wait_window(self.Form)
    
