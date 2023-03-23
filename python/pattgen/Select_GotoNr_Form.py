# VB2PY (UntranslatedCode) Option Explicit

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
import proggen.Prog_Generator as PG
import ExcelAPI.XLF_FormGenerator as XLF
import ExcelAPI.XLW_Workbook as X02

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

import ExcelAPI.XLW_Workbook as X02
import pattgen.M30_Tools as M30
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.Pattern_Generator as PG
import pattgen.M80_Multiplexer_INI_Misc as M80
import pattgen.M80_Multiplexer_INI_Handling

#
"""'# VB2PY (CheckDirective) VB2PY directive Ignore Text
------------------------------------------
-------------------------------------
-----------------------------
--------------------------------
-----------------------------------------------------------------
"""


class CSelect_GotoNr_Form:

    def __init__(self,controller):
        self.controller    = controller
        self.IsActive      = False
        self.Form          = None
        self.UserForm_Res  = ""
        self.Controls      = []
        self.Controls_Dict = {}
        self.Visible = True
        
        self.Button_Callback_Proc = None
                

        self.Select_GotoNr_Form_RSC = {"UserForm":{
                                "Name"          : "Select_GotoNr_Form",
                                "BackColor"     : "#000008",
                                "BorderColor"   : "#000012",
                                "Caption"       : "Simmulation der Konfiguration am PC",
                                "Height"        : 382.5,
                                "Left"          : 0,
                                "Top"           : 0,
                                "Type"          : "MainWindow",
                                "Visible"       : True,
                                "Width"         : 332.5,
                                "Components"    : [{"Name":"Label1","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Auswahl der Start Nummer:",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":180},
                                                   
                                                   {"Name":"Label2","BackColor":"#FF0000","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Diese Konfiguration hat verschiedene Startpunkte.\nSie sind in der 'Goto Tabelle' über ein 'S' markiert und werden, wenn die 'Grafische Anzeige' aktiviert ist mit einem Pfeil und der Startnummer angezeigt.",
                                                    "ControlTipText":"","ForeColor":"#FF0000","Height":84,"Left":12,"TextAlign":"fmTextAlignLeft","Top":24,"Type":"Label","Visible":True,"Width":300},
                                              
                                                   ]}
                                             }
        
    def ControlsFind(self,searchname):
        #return control with searchname
        for control in self.Controls:
            if control.Name==searchname:
                return control
        return None
    
    def destroy(self):
        Debug.Print("Destroy Form")
        self.Form.destroy()
    
    def Button_0_Click():
        Proc_Button(0)
    
    def Button_1_Click():
        Proc_Button(1)
    
    def Highlight_Button(self,Nr):
        i = Integer()

        #------------------------------------------
        # -1 => All buttons normal
        for i in vbForRange(0, self.GotoCnt):
            _with83 = self.ControlsFind('Button_' + str(i))
            if _with83:
                if i == Nr:
                    _with83.BackColor = 0xFF00
                else:
                    _with83.BackColor = 0x8000000F
    
    def Proc_Button(self,Nr):
        #-------------------------------------
        PG.ThisWorkbook.Activate()
        # In case the user has switched to an other excel WB
        self.Highlight_Button(Nr)
        self.Button_Callback_Proc(Nr)
    
    def End_Button_Click(self):
        self.Button_Callback_Proc(- 1)
        #M80.Store_Pos2(self, pattgen.M80_Multiplexer_INI_Handling.Pos_Select_GotoNr_Form)
        X02.Unload(self)
    
    def Show_Dialog(self,GotoCnt, Button_Callback):
        global Button_Callback_Proc

        #-----------------------------------------------------------------
        self.GotoCnt = GotoCnt
        #self.Highlight_Button(- 1)
        self.Button_Callback_Proc = Button_Callback
        #HideRow = WorksheetFunction.RoundUp(GotoCnt / 10, 0) * 10
        #if HideRow <= 60:
        #    M30.Hide_and_Move_up(Me, 'Button_' + HideRow, 'End_Button')
        #for Nr in vbForRange(GotoCnt, HideRow - 1):
        #    Me.Controls['Button_' + Nr].Visible = False
            
        #add buttons 1-64
        
        left_start = 12
        left_delta = 42-left_start
        top_start = 120
        top_delta = 150-top_start
        buttons_per_line = 20
        userform = self.Select_GotoNr_Form_RSC["UserForm"]
        comp_list = userform["Components"]
        left = left_start
        top  = top_start
        
        for i in range(0,GotoCnt):
            button_def = {"Name":"Button_"+str(i),"Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                          "Caption":str(i),
                          "Command": lambda param=i:self.Proc_Button(param),"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":left,"Top":top,"Type":"CommandButton","Visible":True,"Width":24}
            comp_list.append(button_def)
            if (i+1)%buttons_per_line == 0:
                left=left_start
                top += top_delta
            else:
                left+=left_delta
        
        top += top_delta
        button_def = {"Name":"End_Button","Accelerator":"E","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                      "Caption":"Ende",
                      "Command": self.End_Button_Click ,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":246,"Top":top,"Type":"CommandButton","Visible":True,"Width":72}
        comp_list.append(button_def)
        self.UserForm_Initialize()
        self.Show()


    def UserForm_Initialize(self):
        #--------------------------------
        # Is called once to initialice the form
        #Debug.Print vbCr & Me.Name & ": UserForm_Initialize"
        #Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        self.Form=XLF.generate_form(self.Select_GotoNr_Form_RSC,self.controller,dlg=self,modal=False)

    def UserForm_Activate(self):
        #------------------------------
        # Is called every time when the form is shown
        #M25.Make_sure_that_Col_Variables_match()
        pass

    def Hide(self):
        self.IsActive=False
        self.Form.destroy()

    def AddControl(self,control):
        self.Controls.append(control)
        self.Controls_Dict[control.Name]=control

    def Show(self):
        self.IsActive = True
        self.UserForm_Activate()
        self.Form.update()
        self.Form.deiconify()
        #self.controller.wait_window(self.Form)

    def __UserForm_Initialize():
        #--------------------------------
        # Center the dialog if it's called the first time.
        # On a second call without me.close this function is not called
        # => The last position ist used
        # Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        pass

    def Abort_Button_Click(self):
        #-------------------------------
        global Result, Enable_Listbox_Changed
        #-------------------------------
        self.Hide()
        self.Result = ''
        self.Enable_Listbox_Changed = False
 