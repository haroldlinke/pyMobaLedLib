# -*- coding: utf-8 -*-
#
#         MobaLedCheckColors: Color checker for WS2812 and WS2811 based MobaLedLib
#
#         SerialMonitorPage
#
# * Version: 1.00
# * Author: Harold Linke
# * Date: December 25th, 2019
# * Copyright: Harold Linke 2019
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 25.12.2019 - Harold Linke - first release
# *
# *
# * MobaLedCheckColors supports the MobaLedLib by Hardi Stengelin
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
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# * MobaLedCheckColors use tkColorPicker by Juliette Monsel
# * https://sourceforge.net/projects/tkcolorpicker/
# *
# * tkcolorpicker - Alternative to colorchooser for Tkinter.
# * Copyright 2017 Juliette Monsel <j_4321@protonmail.com>
# *
# * tkcolorpicker is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * tkcolorpicker is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# * The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# * License: http://creativecommons.org/licenses/by-sa/3.0/
# ***************************************************************************

import tkinter as tk
from tkinter import ttk,messagebox

from mlpyproggen.configfile import ConfigFile
from mlpyproggen.DefaultConstants import LARGE_FONT,SMALL_FONT,VERY_LARGE_FONT,Very_SMALL_FONT
from locale import getdefaultlocale
from scrolledFrame.ScrolledFrame import VerticalScrolledFrame,HorizontalScrolledFrame,ScrolledFrame

import logging


from datetime import datetime

            
class ARDUINOMonitorPage(tk.Frame):
    
    def __init__(self, parent, controller):
        self.tabClassName = "ARDUINOMonitorPage"
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = self.macrodata.get("MTabName",self.tabClassName)
        self.title = self.macrodata.get("Title",self.tabClassName)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        
        self.frame=ttk.Frame(self,relief="ridge", borderwidth=1)
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)        
        
        self.scroll_main_frame = ScrolledFrame(self.frame)
        self.scroll_main_frame.grid_columnconfigure(0,weight=1)
        self.scroll_main_frame.grid_rowconfigure(0,weight=1)
        
        self.main_frame = ttk.Frame(self.scroll_main_frame.interior, relief="ridge", borderwidth=2)
        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(2,weight=1) 

        self.suppressLinesList= self.macrodata.get("suppressLinesList",[])
        
        title_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2)

        label = ttk.Label(title_frame, text=self.title, font=LARGE_FONT)
        label.pack(padx=5,pady=(5,5))
        
        config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=1,startrow =1,style="CONFIGPage")        

        text_frame = tk.Frame(self.main_frame, padx=10, pady= 10)

        #self.text = tk.Text(frameLabel, wrap='word', bg=self.cget('bg'), height=25, width=70)         # 04.12.19: Old: height=10, width=50
        self.text = tk.Text(text_frame, wrap='word', bg=self.cget('bg'),height=25,width=100)         # 04.12.19: Old: height=10, width=50
        
        # add a vertical scroll bar to the text area
        scroll=tk.Scrollbar(text_frame)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.text.yview)

        #pack everything
        self.text.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
        scroll.pack(side=tk.RIGHT,fill=tk.Y)
        
        # Tabframe
        self.frame.grid(row=0,column=0)
        self.scroll_main_frame.grid(row=0,column=0,sticky="nesw")
        # scroll_main_frame
        self.main_frame.grid(row=0,column=0)        
        # place frames in main_frame
        title_frame.grid(row=0, column=0, columnspan=2, pady=(4, 10), padx=10)
        config_frame.grid(row=1, columnspan=2, pady=(20, 30), padx=10)
        text_frame.grid(row=3, column=0,padx=10, pady=(10, 4),sticky="nesw")
        
        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(3,weight=1)         

        # ----------------------------------------------------------------
        # Standardprocedures for every tabpage
        # ----------------------------------------------------------------

    def tabselected(self):
        #self.controller.currentTabClass = self.tabClassName
        logging.debug("Tabselected: %s",self.tabname)
        pass
    
    def tabunselected(self):
        logging.debug("Tabunselected: %s",self.tabname)
        pass
    
    def TabChanged(self,_event=None):
        logging.debug("Tabchanged: %s",self.tabname)
        pass
 
    def cancel(self,_event=None):
        pass

    def getConfigData(self, key):
        return self.controller.getConfigData(key)
    
    def readConfigData(self):
        self.controller.readConfigData()
        
    def setConfigData(self,key, value):
        self.controller.setConfigData(key, value)

    def setParamData(self,key, value):
        self.controller.setParamData(key, value)

    def MenuUndo(self,_event=None):
        logging.debug("MenuUndo: %s",self.tabname)
        pass
    
    def MenuRedo(self,_event=None):
        logging.debug("ReUndo: %s",self.tabname)
        pass
    
    def connect(self,port):    
        pass
    
    def disconnect(self):
        pass
    
    # ----------------------------------------------------------------
    # End of Standardprocedures for every tabpage
    # ----------------------------------------------------------------    
        
    def block_line(self,string):
        for substring in self.suppressLinesList:
            if substring in string:
                return True
        return False            

    def add_text_to_textwindow(self,text,highlight=""):
        date_time = datetime.now()
        d = date_time.strftime("%H:%M:%S")
        textlines = text.split("\n")
        textmessage = ""
        for textline in textlines:
            if textline !="":
                if not self.block_line(textline):
                    logging.debug("%s: Textwindow: %s",self.tabname,textline)
                    textmessage = d + "  " + textline+"\n"        
                    self.text.insert("end", textmessage)
                    self.text.yview("end")
        
        if highlight=="Error":
            self.text.tag_add("Text", "1.0", tk.END)
            self.text.tag_config("Text", background="red", foreground="white")
        elif highlight=="OK":
            self.text.tag_add("Text", "1.0", tk.END)
            self.text.tag_config("Text", background="green", foreground="white")
        else:
            self.text.tag_add("Text", "1.0", tk.END)
            self.text.tag_config("Text", background="white", foreground="black")      

    def delete_text_from_textwindow(self):
        self.text.delete('1.0', tk.END)

