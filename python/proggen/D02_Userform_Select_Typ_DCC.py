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
from tkinter import ttk
import mlpyproggen.Prog_Generator as PG
from vb2py.vbconstants import *
from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import proggen.M09_Language as M09


# VB2PY (UntranslatedCode) Option Explicit


class UserForm_Select_Typ_DCC:
    def __init__(self):
        
        self.title = M09.Get_Language_Str("Einführung und Auswahl der Zielzeile")
        self.label1_txt = M09.Get_Language_Str('Ein Steuereingang von der Zentrale kann entweder als \nEin- / Ausschalter oder als Taster (Rot/Grün) interpretiert werden.\n\n* Ein- / Ausschalter verwendet man z.B. bei Häusern. \n* Taster werden Beispielsweise bei Sounds eingesetzt.\n\nBeim Taster können zwei verschiedene Aktionen über einer Adresse ausgelöst werden.\nAnstelle von "Rot" und "Grün" kann je nach Zentrale auch "Abbiegen" oder "Gerade",0 oder 1 angezeigt werden.')
        self.label2_txt = M09.Get_Language_Str('"Rot" und "Grün" ist symbolisch zu verstehen und hat nichts mit den LED Farben zu tun.')
        #self.label3_txt = "Der Dialog muss dazu nicht beendet werden.Zusätzliche Zeilen können mit der Schaltfläche ""Zeile einfügen"" hinzugefügt werden. Wenn die Zeile bereits Daten enthält, dann werden diese ab der ausgewählten Position vervollständigt. "
        self.controller = PG.get_global_controller()
        self.IsActive = False
        self.button1_txt = M09.Get_Language_Str("Abbrechen")
        self.button2_txt = M09.Get_Language_Str("Ok")
        self.radiobtn1_txt = M09.Get_Language_Str("An / Aus")
        self.radiobtn2_txt = M09.Get_Language_Str("Rot")
        self.radiobtn3_txt = M09.Get_Language_Str("Grün")
        self.res = tk.IntVar()
        self.Userform_res = ""
        
        
    def __Abort_Button_Click(self):
        #-------------------------------
        self.Userform_res = ''
        self.top.destroy()
    
    def __OK_Button_Click(self):
        #----------------------------
        M09.Set_Tast_Txt_Var()
        if Button_OnOff:
            Userform_res = OnOff_T
        elif Button_Red:
            Userform_res = Red_T
        else:
            Userform_res = Green_T
        self.top.destroy()
    
    def setFocus(self,Target):
        #-----------------------------------------
        M09.Set_Tast_Txt_Var()
        self.res.set(1)
        select_0 = Left(Target, 1)
        if (select_0 == UCase(Left(M09.OnOff_T, 1))):
            #Button_OnOff = True
            self.res.set(1)
        elif (select_0 == UCase(Left(M09.Green_T, 1))):
            #Button_Green = True
            self.res.set(3)
        elif (select_0 == UCase(Left(M09.Red_T, 1))):
            #Button_Red = True
            self.res.set(2)
            # In any other cases the last state is used
        value = self.res.get()
        if value == 1: #Button_OnOff:
            #Button_OnOff.setFocus()
            pass
        elif value == 2: # Button_Red:
            #Button_Red.setFocus()
            pass
        else:
            #Button_Green.setFocus()
            pass
 
    def ok(self, event=None):
        self.IsActive = False
        value = self.res.get()
        if value ==1:
            self.Userform_res = M09.OnOff_T
        elif value == 2:
            self.Userform_res = M09.Red_T
        else:
            self.Userform_res = M09.Green_T
        self.top.destroy()
 
    def cancel(self, event=None):
        self.UserForm_res = ""
        self.IsActive = False
        self.top.destroy()

    def Show(self):
        self.top = tk.Toplevel(self.controller)
        self.top.transient(self.controller)
                
        self.top.grab_set()
        
        self.top.resizable(False, False)  # This code helps to disable windows from resizing
        
        window_height = 500
        window_width = 450
        
        winfo_x = PG.global_controller.winfo_x()
        winfo_y = PG.global_controller.winfo_y()
        
        screen_width = PG.global_controller.winfo_width()
        screen_height = PG.global_controller.winfo_height()
        
        x_cordinate = winfo_x+int((screen_width/2) - (window_width/2))
        y_cordinate = winfo_y+int((screen_height/2) - (window_height/2))
        
        self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))                 
        
        if len(self.title) > 0: self.top.title(self.title)
        self.label1 = ttk.Label(self.top, text=self.label1_txt,wraplength=window_width-20,font=("Tahoma", 11))
        self.label2 = ttk.Label(self.top, text=self.label2_txt,wraplength=window_width/2,font=("Tahoma", 11),foreground="#0000FF")
        #self.label3 = ttk.Label(self.top, text=self.label3_txt,wraplength=window_width,font=("Tahoma", 11))
        self.label1.grid(row=0,column=0,columnspan=2,sticky="nesw",padx=10,pady=10)
        self.label2.grid(row=1,column=1,columnspan=2,rowspan=3,sticky="nesw",padx=10,pady=10)
        #self.label3.grid(row=2,column=0,columnspan=3,sticky="nesw",padx=10,pady=10)
        
        
        self.R1 = tk.Radiobutton(self.top, text=self.radiobtn1_txt, variable=self.res, value=1)
        self.R2 = tk.Radiobutton(self.top, text=self.radiobtn2_txt, variable=self.res, value=2)
        self.R3 = tk.Radiobutton(self.top, text=self.radiobtn3_txt, variable=self.res, value=3) 
        
        self.R1.grid(row=1,column=0,sticky="nesw",padx=10,pady=10)
        self.R2.grid(row=2,column=0,sticky="nesw",padx=10,pady=10)
        self.R3.grid(row=3,column=0,sticky="nesw",padx=10,pady=10)
        self.R1.focus_set()
        self.button_frame = ttk.Frame(self.top)
        
        self.b_cancel = tk.Button(self.button_frame, text=self.button1_txt, command=self.cancel,width=10,font=("Tahoma", 11))
        self.b_ok = tk.Button(self.button_frame, text=self.button2_txt, command=self.ok,width=10,font=("Tahoma", 11))

        self.b_cancel.grid(row=0,column=0,sticky="e",padx=10,pady=10)
        self.b_ok.grid(row=0,column=1,sticky="e",padx=10,pady=10)
        
        self.button_frame.grid(row=4,column=1,sticky="e",padx=10,pady=10)
        
        self.top.bind("<Return>", self.ok)
        self.top.bind("<Escape>", self.cancel)        
        
        self.IsActive = True
        self.controller.wait_window(self.top)
        
    
        