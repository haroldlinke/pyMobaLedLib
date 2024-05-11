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

import proggen.M02_Public as M02
import proggen.M09_Language as M09

"""
def Abort_Button_Click():
    #-------------------------------
    M02.Userform_Res = ''
    Me.Hide()
    # no "Unload Me" to keep the entered data and dialog position

def CheckBox1_Click():
    OK_Button.Enabled = CheckBox1.Value

def Label3_Click():
    # VB2PY (UntranslatedCode) On Error GoTo CantOpen
    P01.ActiveWorkbook.FollowHyperlink(Address=Label3.Caption, NewWindow=True)
    return
    P01.MsgBox(M09.Get_Language_Str('Der Link kann nicht geöffnet werden: ' + Label3.Caption), vbCritical, 'Link öffnen')

def OK_Button_Click():
    #----------------------------
    M02.Userform_Res = 'ok'
    Me.Hide()

def ShowForm():
    _fn_return_value = False
    #------------------------------------------------------
    CheckBox1.Value = False
    Me.Show()
    _fn_return_value = M02.Userform_Res == 'ok'
    return _fn_return_value

def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
    Change_Language_in_Dialog(Me)
    # 20.02.20:
    P01.Center_Form(Me)
"""


class CUserForm_ConfirmLicense:

    def __init__(self,controller):
        self.controller    = controller
        self.IsActive      = False
        self.Form          = None
        self.UserForm_Res  = ""
        self.Controls      = []
        self.Controls_Dict = {}
        self.Visible = True

        self.ConfirmLicense_Form_RSC = {"UserForm":{
                                "Name"          : "UserForm_ConfirmLicense",
                                "BackColor"     : "#00000F",
                                "BorderColor"   : "#000012",
                                "Caption"       : "LNet Lizenzbestimmungen",
                                "Height"        : 497.4,
                                "Left"          : 0,
                                "Top"           : 0,
                                "Type"          : "MainWindow",
                                "Visible"       : True,
                                "Width"         : 534,
                                "Components"    : [{"Name":"Label1","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Die Verwendung des LNet Protokoll basiert auf der 'LocoNet Personal Edition' und ist vom Lizenzinhaber Digitrax ausschließlich für die private, nicht-kommerzielle Nutzung erlaubt. Die Lizenzbestimmungen sind hier nachzulesen:",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":42,"Left":12,"TextAlign":"fmTextAlignLeft","Top":12,"Type":"Label","Visible":True,"Width":500},
                                                   
                                                   {"Name":"Label3","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"https://www.digitrax.com/support/loconet/home/",
                                                    "ControlTipText":"","ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","Top":60,"Type":"Label","Visible":True,"Width":500},
                                                   
                                                   {"Name":"Image1","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "ControlTipText":"","Height":324,"IconName":"LocoNetLicense.png","Left":12,"Top":78,"Type":"Image","Visible":True,"Width":500},                                                   
                                                   
                                                   {"Name":"Abort_Button","Accelerator":"A","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Abbrechen",
                                                    "Command": self.Abort_Button_Click ,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":186,"Top":438,"Type":"CommandButton","Visible":True,"Width":72},
                                                   
                                                   {"Name":"OK_Button","Accelerator":"O","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"OK",
                                                    "Command": self.OK_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":264,"Top":438,"Type":"CommandButton","Visible":True,"Width":72},
                                                   
                                                   {"Name":"CheckBox1","Accelerator":"B","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Ich bestätige die Einhaltung dieser Lizenzbestimmungen",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":24,"Left":12,"Top":408,"Type":"CheckBox","Visible":True,"Width":500},                                                   
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
    
    def ShowForm(self):
        self.UserForm_Initialize()
        self.CheckBox1.Value = False
        self.Show()
        return self.UserForm_Res == "ok"

    def UserForm_Initialize(self):
        #--------------------------------
        # Is called once to initialice the form
        #Debug.Print vbCr & Me.Name & ": UserForm_Initialize"
        #Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        self.Form=XLF.generate_form(self.ConfirmLicense_Form_RSC,self.controller,dlg=self,modal=False, jump_table=PG.ThisWorkbook.jumptable, defaultfont=X02.DefaultFont)

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
        self.controller.wait_window(self.Form)

    def __UserForm_Initialize():
        #--------------------------------
        # Center the dialog if it's called the first time.
        # On a second call without me.close this function is not called
        # => The last position ist used
        # Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        pass
    
    def CheckBox1_Click(self):
        self.OK_Button.Enabled = self.CheckBox1.Value
        
    def Abort_Button_Click(self):
        #-------------------------------
        self.UserForm_Res = ''
        self.Hide()
        
        
    def OK_Button_Click(self):
        #-------------------------------
        if self.CheckBox1.Value:
            self.UserForm_Res = 'ok'
        else:
            self.UserForm_Res = ""
        self.Hide()

