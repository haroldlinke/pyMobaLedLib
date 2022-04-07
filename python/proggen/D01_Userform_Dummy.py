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

class UserForm_DialogGuide1:
    def __init__(self, value, title, labeltext = '' ):
        self.value = value
        self.parent = PG.get_dialog_parent()
        self.title = title
        self.labeltext = labeltext
        self.controller = PG.get_global_controller()
        self.IsActive = False

 
    def ok(self, event=None):
        print ("Has escrito ...", self.e.get())
        #self.valor.set(self.e.get())
        self.IsActive = False
        self.top.destroy()
 
    def cancel(self, event=None):
        self.IsActive = False
        self.top.destroy()

    def Show(self):
        self.top = tk.Toplevel(self.parent)
        self.top.transient(self.parent)
        self.top.grab_set()
        if len(self.title) > 0: self.top.title(self.title)
        if len(self.labeltext) == 0: self.labeltext = 'Valor'
        tk.Label(self.top, text=self.labeltext).pack()
        self.top.bind("<Return>", self.ok)
        self.e = tk.Entry(self.top, text=self.value.get())
        self.e.bind("<Return>", self.ok)
        self.e.bind("<Escape>", self.cancel)
        self.e.pack(padx=15)
        self.e.focus_set()
        b = tk.Button(self.top, text="OK", command=self.ok)
        b.pack(pady=5)
        self.IsActive = True
        self.controller.wait_window(self.top)
        
    
        