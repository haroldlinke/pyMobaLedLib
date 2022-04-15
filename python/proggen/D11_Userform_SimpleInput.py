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
from vb2py.vbfunctions import *
from vb2py.vbdebug import *

import tkinter as tk
from tkinter import ttk
import proggen.Prog_Generator as PG
import proggen.M09_Language as M09

class UserForm_SimpleInput:
    def __init__(self):
        self.title = M09.Get_Language_Str("Simple Input")
        self.label1_txt =""
        self.label2_txt = ""
        self.controller = PG.get_global_controller()
        self.IsActive = False
        self.button1_txt = M09.Get_Language_Str("Abbrechen")
        self.button2_txt = M09.Get_Language_Str("Ok")
        self.UserForm_res = ""
        self.res = False    
 
    def ok(self, event=None):
        self.IsActive = False
        self.UserForm_res = self.entry1_input.get()
        self.top.destroy()
        self.res = True
 
    def cancel(self, event=None):
        self.UserForm_res = ""
        self.IsActive = False
        self.top.destroy()
        self.res = False

    def Show(self,Message:str, Title:str, Default=None):
        self.title = Title
        self.label1_txt = Message
        self.entry1_input = tk.StringVar(self.controller)
        self.top = tk.Toplevel(self.controller)
        self.top.transient(self.controller)
        if Default!=None:
            self.entry1_input.set(Default)
        else:
            self.entry1_input.set("")
        self.entry1 = tk.Entry(self.top,width=40,textvariable=self.entry1_input)
        self.top.grab_set()
        self.top.resizable(False, False)  # This code helps to disable windows from resizing
        self.label1_txt = Message
        window_height = 600
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

        self.label1.grid(row=0,column=0,columnspan=1,sticky="nesw",padx=10,pady=10)

        self.entry1.grid(row=2,column=0,padx=10,pady=10)
        self.entry1.focus_set()

        self.button_frame = ttk.Frame(self.top)
        
        self.b_cancel = tk.Button(self.button_frame, text=self.button1_txt, command=self.cancel,width=10,font=("Tahoma", 11))
        self.b_ok = tk.Button(self.button_frame, text=self.button2_txt, command=self.ok,width=10,font=("Tahoma", 11))

        self.b_cancel.grid(row=0,column=0,sticky="e",padx=10,pady=10)
        self.b_ok.grid(row=0,column=1,sticky="e",padx=10,pady=10)
        
        self.button_frame.grid(row=5,column=0,sticky="e",padx=10,pady=10)
        
        self.top.bind("<Return>", self.ok)
        self.top.bind("<Escape>", self.cancel)            
        
        self.IsActive = True
        self.controller.wait_window(self.top)

        return self.res
        

        