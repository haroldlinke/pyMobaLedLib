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
# * MobaLedCheckColors is based on tkColorPicker by Juliette Monsel
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

from mlpyproggen.DefaultConstants import ARDUINO_WAITTIME,LARGE_FONT, SMALL_FONT, VERY_LARGE_FONT, PROG_VERSION,ARDUINO_LONG_WAITTIME
from mlpyproggen.configfile import ConfigFile
from locale import getdefaultlocale

import os
import serial
import sys
import threading
import queue
import time
import logging
from scrolledFrame.ScrolledFrame import VerticalScrolledFrame,HorizontalScrolledFrame,ScrolledFrame

from datetime import datetime


# --- Translation - not used
EN = {}
FR = {"Red": "Rouge", "Green": "Vert", "Blue": "Bleu",
      "Hue": "Teinte", "Saturation": "Saturation", "Value": "Valeur",
      "Cancel": "Annuler", "Color Chooser": "Sélecteur de couleur",
      "Alpha": "Alpha"}
DE = {"Red": "Rot", "Green": "Grün", "Blue": "Blau",
      "Hue": "Farbton", "Saturation": "Sättigung", "Value": "Helligkeit",
      "Cancel": "Beenden", "Color Chooser": "Farbwähler",
      "Alpha": "Alpha", "Configuration": "Einstellungen"}

try:
    TR = EN
    if getdefaultlocale()[0][:2] == 'fr':
        TR = FR
    else:
        if getdefaultlocale()[0][:2] == 'de':
            TR = DE
except ValueError:
    TR = EN


def _(text):
    """Translate text."""
    return TR.get(text, text)

ThreadEvent = None

BUTTONLABELWIDTH = 10
            
class DCCKeyboardPage(tk.Frame):
    def __init__(self, parent, controller):
        self.tabClassName = "DCCKeyboardPage"
        tk.Frame.__init__(self,parent)
        self.controller = controller
        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName)
        
        #button1_text = macrodata.get("Button_1",self.tabClassName)
        #button2_text = macrodata.get("Button_2",self.tabClassName)
        
        self.fontlabel = self.controller.get_font("FontLabel")
        self.fontspinbox = self.controller.get_font("FontSpinbox")
        self.fonttext = self.controller.get_font("FontText")
        self.fontbutton = self.controller.get_font("FontLabel")
        self.fontentry = self.controller.get_font("FontEntry")
        self.fonttext = self.controller.get_font("FontText")
        self.fontscale = self.controller.get_font("FontScale")
        self.fonttitle = self.controller.get_font("FontTitle")        
        
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

        title_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2)

        label = ttk.Label(title_frame, text=self.title, font=self.fonttitle)
        label.pack(padx=5,pady=(5,5))
        
        config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=1,startrow =1,style="CONFIGPage")        
        
        
        # create buttons
        
        base_address = int(self.controller.get_macroparam_val(self.tabClassName, "DCC BaseAddress"))
        row = 0
        in_button_frame =  ttk.Frame(self.main_frame, relief="ridge", borderwidth=1)
        self.buttonlist = []
        
        for j in range (0,4):
    
            for i in range(0,8): # create switch buttons
                address = j*8 + i
                self.create_button(i,j*2,address,0,str(address+base_address),"red",in_button_frame)
                self.create_button(i,j*2+1,address,1," ","green",in_button_frame)
    
        # Tabframe
        self.frame.grid(row=0,column=0)
        self.scroll_main_frame.grid(row=0,column=0,sticky="nesw")
        # scroll_main_frame
        self.main_frame.grid(row=0,column=0)
        # main_frame                
        
        title_frame.grid(row=0, column=0, columnspan=2, pady=(4, 10), padx=10)
        config_frame.grid(row=1, columnspan=2, pady=(20, 30), padx=10)        
        in_button_frame.grid(row=2, column=0, sticky="n", padx=4, pady=4)
        
        # ----------------------------------------------------------------
        # Standardprocedures for every tabpage
        # ----------------------------------------------------------------

    def tabselected(self):
        #self.controller.currentTabClass = self.tabClassName
        logging.debug("Tabselected: %s",self.tabname)
        #self.controller.send_to_ARDUINO("#END")
        #time.sleep(ARDUINO_WAITTIME)        
        pass
    
    def tabunselected(self):
        logging.debug("Tabunselected: %s",self.tabname)
        #self.controller.send_to_ARDUINO("#BEGIN")
        #time.sleep(ARDUINO_WAITTIME)            
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
        pass
    
    def MenuRedo(self,_event=None):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass
    
    # ----------------------------------------------------------------
    # End of Standardprocedures for every tabpage
    # ----------------------------------------------------------------    

    def create_button(self,column, row, number, channel, text, color,in_button_frame):
        inbuttonlabel1 = tk.Label(in_button_frame, text=text, width=BUTTONLABELWIDTH, height=1, relief="raised", background=color,borderwidth=2,font=self.fontbutton) #,command=lambda: self._button_cmd(button=number,channel=channel))
        inbuttonlabel1.grid(row=row, column=column, sticky="n", padx=4, pady=4)
        inbuttonlabel1.button=number
        inbuttonlabel1.channel=channel
        inbuttonlabel1.bind("<Button-1>", self._buttonlabel_cmd)
        inbuttonlabel1.bind("<ButtonRelease-1>", lambda e: e.widget.configure(relief="raised"))        
        
        #self.controller.ToolTip(inbuttonlabel1, text="Button {}".format(number))
        self.buttonlist.append(inbuttonlabel1)
        
        
    def _buttonlabel_cmd(self, _event):
        """Respond to user click on a button item."""
        label = _event.widget
        label.focus_set()
        label.configure(relief="sunken")
        self.update()
        address = self.controller.get_macroparam_val(self.tabClassName, "DCC BaseAddress")   #self.input.get()
        address_int=address+label.button
        logging.debug ("_button_cmd: %s - %s",address_int,label.channel)
        command = "@ {:03} {:02} 01".format(address_int,label.channel)
        self.send_command_to_ARDUINO(command)
        for button in self.buttonlist:
            if button.channel == 0:
                button.config(text=str(button.button+address))

    def send_command_to_ARDUINO(self,command):
        self.controller.connect_if_not_connected()
        for c in command:
            self.controller.send_to_ARDUINO(c)
            #time.sleep(0.01)
        c = chr(10)
        self.controller.send_to_ARDUINO(c)

    def _button_cmd(self, button=0,channel=0):
        """Respond to user click on a Button"""
        address = self.controller.get_macroparam_val(self.tabClassName, "DCC BaseAddress")   #self.input.get()
        address_int=address+button
        logging.debug ("_button_cmd: %s - %s",address_int,channel)
        command = "@ {:03} {:02} 01".format(address_int,channel)
        self.send_command_to_ARDUINO(command)
