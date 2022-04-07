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
# 2021-01-07 v4.02 HL: - Else:, ByRef check done - first PoC release

#from vb2py.vbfunctions import *
#from vb2py.vbdebug import *
#from vb2py.vbconstants import *

import tkinter as tk
from tkinter import ttk
#from mlpyproggen.tooltip import Tooltip
#from tkcolorpicker.spinbox import Spinbox
#from tkcolorpicker.limitvar import LimitVar

import proggen.Prog_Generator as PG

#import proggen.M02_Public as M02
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header as M06
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
#import proggen.M07_COM_Port as M07
#import proggen.M08_ARDUINO as M08
#import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
#import proggen.M20_PageEvents_a_Functions as M20
#import proggen.M25_Columns as M25
#import proggen.M27_Sheet_Icons as M27
#import proggen.M28_divers as M28
#import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Mulitplexer as M80

#from ExcelAPI.X01_Excel_Consts import *
import ExcelAPI.P01_Workbook as P01

import logging


class CStatusMsg_UserForm():
    def __init__(self):

        self.controller = PG.get_global_controller()
        self.IsActive = False
        self.title = "Bitte etwas Geduld..."
        self.label1_txt = "Lade alle Beispiele\nBitte etwas Geduld"
        self.label2_txt = "..."
        self.button1_txt = "Abbrechen"
        self.button2_txt = "Ok"
        self.res = False
        self.UserForm_Res = ""
        self.label1 = None
        self.label2 = None
        self.text = ""
        self.label_txt=""
        
        
    def destroy(self):
        if self.IsActive:
            self.IsActive=False
            self.top.withdraw()
            #self.top.destroy()
        
    #def ok(self, event=None):
    #    self.IsActive = False
    #    self.OK_Button_Click()
        
        #self.Userform_res = value
    #    self.top.destroy()
    #    P01.ActiveSheet.Redraw_table()
    #    self.res = True
 
    #def cancel(self, event=None):
    #    self.UserForm_Res = '<Abort>'
    #    self.IsActive = False
    #    self.top.destroy()
    #    P01.ActiveSheet.Redraw_table()
    #    self.res = False
    
    def create_form(self):
        self.top = tk.Toplevel(self.controller)
        self.top.transient(self.controller)
    
        #self.top.grab_set()
        self.top.focus_set()
    
        self.top.resizable(False, False)  # This code helps to disable windows from resizing
    
        window_height = 100
        window_width = 200
    
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
    
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
    
        self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))                
    
        if len(self.title) > 0: self.top.title(self.title)
        self.label1 = ttk.Label(self.top, text=self.label1_txt,wraplength=window_width-20,font=("Tahoma", 11))
        self.label2 = ttk.Label(self.top, text=self.label2_txt,wraplength=window_width/2,font=("Tahoma", 11),foreground="#0000FF")
        #self.label3 = ttk.Label(self.top, text=self.label3_txt,wraplength=window_width,font=("Tahoma", 11))
        self.label1.grid(row=0,column=0,columnspan=2,sticky="nesw",padx=10,pady=10)
        self.label2.grid(row=1,column=1,columnspan=2,rowspan=3,sticky="nesw",padx=10,pady=10)
        
        P01.updateWindow()
        #self.label3.grid(row=2,column=0,columnspan=3,sticky="nesw",padx=10,pady=10)
    
        #self.top.bind("<Return>", self.ok)
    
        #self.button_frame = ttk.Frame(self.top)
    
        #self.b_cancel = tk.Button(self.button_frame, text=self.button1_txt, command=self.cancel,width=10,font=("Tahoma", 11))
        #self.b_ok = tk.Button(self.button_frame, text=self.button2_txt, command=self.ok,width=10,font=("Tahoma", 11))
    
        #self.b_cancel.grid(row=0,column=0,sticky="e",padx=10,pady=10)
        #self.b_ok.grid(row=0,column=1,sticky="e",padx=10,pady=10)
    
        #self.button_frame.grid(row=4,column=1,sticky="e",padx=10,pady=10)
    
        #self.top.bind("<Return>", self.ok)
        #self.top.bind("<Escape>", self.cancel)                

    def Show(self):
        
        self.IsActive = True
        self.top.update()
        self.top.deiconify()
        #self.controller.wait_window(self.top)        

        return self.res
    
    def __UserForm_Initialize(self):
        #--------------------------------
        #ebug.Print vbCr & me.Name & ":Load_All_Examples Initialize"
        #Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        self.create_form()
        pass
    
    def Set_Label(self, Msg):
        #----------------------------------
        self.label1.configure(text=Msg)
        self.top.update()
        self.top.focus()
        self.label_txt = Msg
        #P01.set_statusmessage(self.label_txt +" "+ self.text)
    
    def Set_ActSheet_Label(self,Txt):
        #-------------------------------------------
        #ActSheet_Label = Txt
        self.text=Txt
        self.label2.configure(text=Txt)
        self.top.update()
        self.top.focus()
        #P01.DoEvents()
        #P01.set_statusmessage(self.label_txt +" "+ self.text)
    
    def ShowDialog(self, Label, Txt):
        #----------------------------------------------------
        self.create_form()
        self.Set_Label(Label)
        self.Set_ActSheet_Label(Txt)
        self.Show()
        self.text=Txt
        self.label_txt = Label
        #P01.set_statusmessage(Label+" "+Txt)
    
    # VB2PY (UntranslatedCode) Option Explicit


