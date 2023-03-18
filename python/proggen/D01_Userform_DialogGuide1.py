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
import proggen.Prog_Generator as PG
from vb2py.vbconstants import *
import ExcelAPI.XLW_Workbook as P01
import proggen.M09_Language as M09

class UserForm_DialogGuide1:
    def __init__(self):
        
        self.title = M09.Get_Language_Str("Einführung und Auswahl der Zielzeile")
        self.label1_txt = M09.Get_Language_Str("Mit dem Dialog Knopf ist die Eingabe einer Konfigurationszeile ganz einfach. Das Programm zeigt zu jedem Schritt die wichtigsten Informationen. \nDie Eingaben können aber auch jederzeit direkt in der Tabelle gemacht werden.\n\nZunächst muss die Zeile in der Tabelle ausgewählt werden. Die Reihenfolge der Zeilen muss der LEDs Anordnung entsprechen. Die erste Zeile in der Tabelle steuert die erste LED Gruppe auf der Anlage. Mit der zweiten Zeile wird die zweite Gruppe konfiguriert... \nEine Gruppe kann wie bei einem Haus aus mehreren LEDs oder nur aus einer einzigen LED bestehen. Anstelle von LEDs können auch andere Effekte wie Sound, Servos, ... angesteuert werden. Hier wird immer der Begriff LED verwendet. \nFalls die Reihenfolge nicht stimmt können die Zeilen nachträglich verschoben werde.\n")
        self.label2_txt = M09.Get_Language_Str("Mit einem Klick in die Tabelle kann die Zeile jetzt ausgewählt werden.")
        self.label3_txt = M09.Get_Language_Str('Der Dialog muss dazu nicht beendet werden.\nZusätzliche Zeilen können mit der Schaltfläche "Zeile einfügen" hinzugefügt werden. \nWenn die Zeile bereits Daten enthält, dann werden diese ab der ausgewählten Position vervollständigt.')
        self.controller = PG.get_global_controller()
        self.IsActive = False
        self.button1_txt = M09.Get_Language_Str("Abbrechen")
        self.button2_txt = M09.Get_Language_Str("Ok")
        self.res = None
 
    def ok(self, event=None):
        
        self.IsActive = False
        self.res = vbOK
        self.top.destroy()
 
    def cancel(self, event=None):
        self.res = vbAbort
        self.IsActive = False
        self.top.destroy()

    def Show(self):
        geometry=PG.global_controller.geometry()
        winfo_x = PG.global_controller.winfo_x()
        winfo_y = PG.global_controller.winfo_y()
      
        self.top = tk.Toplevel(self.controller)
        self.top.transient(self.controller)
                
        #self.top.grab_set()
        
        self.top.resizable(False, False)  # This code helps to disable windows from resizing
        
        window_height = 500
        window_width  = 700
        
        screen_width = PG.global_controller.winfo_width()
        screen_height = PG.global_controller.winfo_height()
        
        x_cordinate = winfo_x+int((screen_width/2) - (window_width/2))
        y_cordinate = winfo_y+int((screen_height/2) - (window_height/2))
        
        #self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))                
        self.top.geometry("+{}+{}".format(x_cordinate, y_cordinate))                
                
        
        if len(self.title) > 0: self.top.title(self.title)
        self.label1 = ttk.Label(self.top, text=self.label1_txt,wraplength=window_width-20,font=("Tahoma", 11))
        self.label2 = ttk.Label(self.top, text=self.label2_txt,wraplength=window_width-20,font=("Tahoma", 11),foreground="#0000FF")
        self.label3 = ttk.Label(self.top, text=self.label3_txt,wraplength=window_width-20,font=("Tahoma", 11))
        self.label1.grid(row=0,column=0,columnspan=3,sticky="nesw",padx=10,pady=10)
        self.label2.grid(row=1,column=0,columnspan=3,sticky="nesw",padx=10,pady=10)
        self.label3.grid(row=2,column=0,columnspan=3,sticky="nesw",padx=10,pady=10)
        
        PG.global_controller.bind("<Return>", self.ok)
        PG.global_controller.bind("<Escape>",self.cancel)
        
        self.button_frame = ttk.Frame(self.top)
        
        self.b_cancel = tk.Button(self.button_frame, text=self.button1_txt, command=self.cancel,width=10,font=("Tahoma", 11))
        self.b_ok = tk.Button(self.button_frame, text=self.button2_txt, command=self.ok,width=10,font=("Tahoma", 11))

        self.b_cancel.grid(row=0,column=0,sticky="e",padx=10,pady=10)
        self.b_ok.grid(row=0,column=1,sticky="e",padx=10,pady=10)
        
        self.button_frame.grid(row=3,column=2,sticky="e",padx=10,pady=10)
        
        self.IsActive = True
        self.controller.wait_window(self.top)
        P01.ActiveSheet.Redraw_table()
        
        
    
        