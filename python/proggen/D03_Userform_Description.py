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


class UserForm_Description:
    def __init__(self):
        self.title = M09.Get_Language_Str("Eingabe der Beschreibung")
        self.label1_txt = M09.Get_Language_Str("Zu jeder Zeile sollte eine aussagekräftige Beschreibung eingegeben werden damit man später noch versteht was die Funktion macht und welches Haus oder andere Objekt von der Zeile gesteuert wird. Die Beschreibung kann beliebig lang sein. Es können auch mehrere Zeilen verwendet werden. \n\nMögliche Angaben:\n* Beschreibung des Objekts (z.B.: Hauptbahnhof)\n* Angaben zur Funktion (z.B: Wird automatisch bei Dunkelheit aktiviert)\n* ...")
        self.label2_txt = M09.Get_Language_Str("Mit Shift+Enter wird eine neue Zeile begonnen")
        #self.label3_txt = "Der Dialog muss dazu nicht beendet werden.Zusätzliche Zeilen können mit der Schaltfläche ""Zeile einfügen"" hinzugefügt werden. Wenn die Zeile bereits Daten enthält, dann werden diese ab der ausgewählten Position vervollständigt. "
        self.controller = PG.get_global_controller()
        self.IsActive = False
        self.button1_txt = M09.Get_Language_Str("Abbrechen")
        self.button2_txt = M09.Get_Language_Str("Ok")
        self.Userform_res = ""
 
 
    def ok(self, event=None):
        self.IsActive = False
        value = self.TextBox.get("1.0","end-1c")
        self.Userform_res = value
        self.top.destroy()
 
    def cancel(self, event=None):
        self.Userform_res = '<Abort>'
        self.IsActive = False
        self.top.destroy()

    def ShowForm(self,Txt):
        self.top = tk.Toplevel(self.controller)
        self.top.transient(self.controller)
        
        self.TextBox = tk.Text(self.top,height=20,width=40,wrap="word")
        self.TextBox.insert("end",Txt)
        
        self.top.grab_set()
        
        self.top.resizable(False, False)  # This code helps to disable windows from resizing
        
        window_height = 800
        window_width = 900
        
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
        self.label1.grid(row=0,column=0,columnspan=1,sticky="nesw",padx=10,pady=10)
        #self.label3.grid(row=2,column=0,columnspan=3,sticky="nesw",padx=10,pady=10)
        self.TextBox.grid(row=1,column=0,sticky="nesw",padx=10,pady=10)
        self.TextBox.focus_set()
        self.label2.grid(row=2,column=0,columnspan=1,rowspan=1,sticky="nesw",padx=10,pady=10)

        self.top.bind("<Return>", self.ok)
        self.top.bind("<Escape>", self.cancel)
        self.button_frame = ttk.Frame(self.top)
        
        self.b_cancel = tk.Button(self.button_frame, text=self.button1_txt, command=self.cancel,width=10,font=("Tahoma", 11))
        self.b_ok = tk.Button(self.button_frame, text=self.button2_txt, command=self.ok,width=10,font=("Tahoma", 11))

        self.b_cancel.grid(row=0,column=0,sticky="e",padx=10,pady=10)
        self.b_ok.grid(row=0,column=1,sticky="e",padx=10,pady=10)
        
        self.button_frame.grid(row=3,column=0,sticky="e",padx=10,pady=1)
        
        self.IsActive = True
        self.controller.wait_window(self.top)

        return self.Userform_res
        

        