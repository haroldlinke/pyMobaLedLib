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


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import proggen.M09_Language as M09
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M50_Exchange as M50
import proggen.F00_mainbuttons as F00
"""-------------------------------
----------------------------
---------------------------------------------
--------------------------------
"""

# VB2PY (UntranslatedCode) Option Explicit

            
#################################################################################################
    


    
class CSelect_ProgGen_Dest_Form:
    
    def __init__(self,controller):
        self.controller    = controller
        self.IsActive      = False
        self.Form          = None
        self.UserForm_Res  = ""
        self.Controls      = []
        self.Controls_Dict = {}
        self.Callback_Proc = None
        #*HL Center_Form(Me)
        
        self.Select_ProgGen_Dest_Form_RSC = {"UserForm":{
                                "Name"          : "Select_ProgGen_Dest_Form",
                                "BackColor"     : "#000008",
                                "BorderColor"   : "#000012",
                                "Caption"       : "Zielzeile im Prog_Generator auswählen",
                                "Height"        : 269.25,
                                "Left"          : 0,
                                "Top"           : 0,
                                "Type"          : "MainWindow",
                                "Visible"       : True,
                                "Width"         : 266.25,
        
                                "Components"    : [{"Name":"Label1","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Klicken Sie in die Zeile in der das Muster eingetragen werden soll und betätigen dann den 'OK' Knopf.\nWenn bereits die richtige Zeile aktiviert ist, dann kann dieser Dialog direkt mit 'Enter' geschlossen werden.\n\nAchtung: Bereits existierende Einträge in der Spalte 'Beleuchtung, Sound, oder andere Effekte' werden überschrieben.",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":102,"Left":18,"TextAlign":"fmTextAlignLeft","Top":42,"Type":"Label","Visible":True,"Width":234},
                                                   {"Name":"Label2","BackColor":"#FF0000","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Zielzeile für das neu erzeugte LED Muster im Prog_Generator auswählen.",
                                                    "ControlTipText":"","ForeColor":"#FF0000","Height":36,"Left":18,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":234},
                                                   {"Name":"Abort_Button","Accelerator":"A","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Abbrechen",
                                                    "Command": self.Abort_Button_Click ,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":96,"Top":204,"Type":"CommandButton","Visible":True,"Width":72},
                                                   {"Name":"OK_Button","Accelerator":"O","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"OK",
                                                    "Command": self.OK_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":174,"Top":204,"Type":"CommandButton","Visible":True,"Width":72},
                                                   {"Name":"GoBack_CheckBox","Accelerator":"P","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Anschließend zurück zum Pattern_Configurator",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":18,"Left":24,"Top":174,"Type":"CheckBox","Visible":True,"Width":228},
                                                   {"Name":"SendToArduino_CheckBox","Accelerator":"A","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"gleich zum Arduino schicken",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":18,"Left":24,"Top":150,"Type":"CheckBox","Visible":True,"Width":228},                                                   
                                                 ]}
                           }        
    
    def UserForm_Initialize(self):
        #--------------------------------
        # Is called once to initialice the form
        #Debug.Print vbCr & Me.Name & ": UserForm_Initialize"
        #Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        self.Form=XLF.generate_form(self.Select_ProgGen_Dest_Form_RSC,self.controller,dlg=self,modal=False)
                
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
        
    def Show_Dialog(self):
        self.Show()
        
    def Show(self):
        self.IsActive = True
        self.UserForm_Initialize()
        self.UserForm_Activate()
        self.Form.update()
        self.Form.deiconify()
        #self.controller.wait_window(self.Form)
        
    
    def Check_and_Start(self,Callback):
        #---------------------------------------------
        self.Callback_Proc = Callback
        self.Show()
    
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
        self.Hide()
        if self.Callback_Proc:
            self.Callback_Proc(False, False, False)
    
    def OK_Button_Click(self):
        Message = String()
        #----------------------------
        if X02.ActiveWorkbook.Name != PG.ThisWorkbook.Name:
            Message = M09.Get_Language_Str('Fehler: Die Zeile muss im Prog_Generator Excel Programm ausgewählt werden')
        else:
            if M28.Is_Data_Sheet(X02.ActiveSheet) == False:
                Message = M09.Get_Language_Str('Fehler: Das Ausgewählte Excel Blatt ist keine gültige Prog_Generator Konfigurationsseite')
        if Message == '':
            if not M50.Selected_Row_Valid():
                Message = M09.Get_Language_Str('Fehler: Die Ausgewählte Zeile ist nicht innerhalb des gültigen Bereichs')
        if Message != '':
            select_0 = X02.MsgBox(Message, vbCritical + vbRetryCancel, M09.Get_Language_Str('Fehler bei der Auswahl der Zielzeile'))
            if (select_0 == vbCancel):
                F00.Select_ProgGen_Src_Form.Hide()
            elif (select_0 == vbRetry):
                if X02.ActiveWorkbook.Name != PG.ThisWorkbook.Name:
                    PG.ThisWorkbook.Activate()
                return
        else:
            self.Hide()
            if self.Callback_Proc:
                self.Callback_Proc( True, self.SendToArduino_CheckBox.Value, self.GoBack_CheckBox.Value)
                PG.ThisWorkbook.Activate()
                with_0 = X02.ActiveSheet.Cells(X02.ActiveCell().Row, M25.Config__Col)
                if with_0.Value != '':
                    M27.FindMacro_and_Add_Icon_and_Name(with_0.Value, X02.ActiveCell().Row, PG.ThisWorkbook.ActiveSheet, False)
                if self.GoBack_CheckBox.Value:
                    self.Callback_Proc(False, False, self.GoBack_CheckBox.Value)


    

# VB2PY (UntranslatedCode) Option Explicit



