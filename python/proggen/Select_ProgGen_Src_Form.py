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
import mlpyproggen.Prog_Generator as PG
import ExcelAPI.XLF_FormGenerator as XLF

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as X02
import proggen.M09_Language as M09
import proggen.M25_Columns as M25
import proggen.M28_Diverse as M28
import proggen.M50_Exchange as M50
"""-------------------------------
----------------------------
---------------------------------------------
--------------------------------
"""

# VB2PY (UntranslatedCode) Option Explicit

            
#################################################################################################

    
class CSelect_ProgGen_Src_Form:
    
    def __init__(self,controller):
        self.controller    = controller
        self.IsActive      = False
        self.Form          = None
        self.UserForm_Res  = ""
        self.Controls      = []
        self.Controls_Dict = {}
        self.Callback_Proc = None
        #*HL Center_Form(Me)
        
        self.Select_ProgGen_Src_Form_RSC = {"UserForm":{
                                            "Name"          : "Select_ProgGen_Src_Form",
                                            "BackColor"     : "#000008",
                                            "BorderColor"   : "#000012",
                                            "Caption"       : "Quellzeile im Prog_Generator auswählen",
                                            "Height"        : 218.25,
                                            "Left"          : 0,
                                            "Top"           : 0,
                                            "Type"          : "MainWindow",
                                            "Visible"       : True,
                                            "Width"         : 266.25,
                                            "Components"    : [{"Name":"Text_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                "Caption":"Klicken Sie in die Zeile aus der das Muster gelesen werden soll und betätigen dann den 'OK' Knopf.\nWenn bereits die richtige Zeile aktiviert ist, dann kann dieser Dialog direkt mit 'Enter' geschlossen werden.\n\nAchtung: Es können nur Zeilen importiert werden welche den 'Pattern' Befehl enthalten.",
                                                                "ControlTipText":"","ForeColor":"#000012","Height":90,"Left":18,"TextAlign":"fmTextAlignLeft","Top":60,"Type":"Label","Visible":True,"Width":234},
                                                               {"Name":"Head_Label","BackColor":"#FF0000","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                "Caption":"Quellzeile im Prog_Generator auswählen aus der das LED Muster gelesen werden soll.",
                                                                "ControlTipText":"","ForeColor":"#FF0000","Height":48,"Left":18,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":234},
                                                               {"Name":"Abort_Button","Accelerator":"A","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                "Caption":"Abbrechen",
                                                                "Command": self.Abort_Button_Click ,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":96,"Top":156,"Type":"CommandButton","Visible":True,"Width":72},
                                                               {"Name":"OK_Button","Accelerator":"O","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                "Caption":"OK",
                                                                "Command":self.OK_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":174,"Top":156,"Type":"CommandButton","Visible":True,"Width":72},
                                                             ]}
                                       }
    
    def UserForm_Initialize(self):
        #--------------------------------
        # Is called once to initialice the form
        #Debug.Print vbCr & Me.Name & ": UserForm_Initialize"
        #Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        self.Form=XLF.generate_form(self.Select_ProgGen_Src_Form_RSC,self.controller,dlg=self,modal=False,jump_table=X02.ActiveWorkbook.jumptable, defaultfont=X02.DefaultFont)
                
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
            self.Callback_Proc(False, '', '', 0)
    
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
            else:
                M25.Make_sure_that_Col_Variables_match()
                if InStr(X02.Cells(X02.ActiveCell().Row, M25.Config__Col), 'PatternT') == 0:
                    Message = M09.Get_Language_Str('Achtung: Die ausgewählte Zeile enthält kein Makro welches vom Pattern_Generator importiert werden kann.')
        if Message != '':
            select_0 = X02.MsgBox(Message, vbCritical + vbRetryCancel, M09.Get_Language_Str('Fehler bei der Auswahl der Zielzeile'))
            if (select_0 == vbCancel):
                self.Hide()
            elif (select_0 == vbRetry):
                if X02.ActiveWorkbook.Name != PG.ThisWorkbook.Name:
                    PG.ThisWorkbook.Activate()
                return
        else:
            self.Hide()
            if self.Callback_Proc:
                self.Callback_Proc( True, X02.Cells(X02.ActiveCell().Row, M25.Descrip_Col), X02.Cells(X02.ActiveCell().Row, M25.Config__Col), X02.ActiveCell().Row)

# VB2PY (UntranslatedCode) Option Explicit



