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
from tkinter import ttk, messagebox, filedialog
from tkcolorpicker.functions import tk, ttk, round2, create_checkered_image, \
    overlay, hsv_to_rgb, hexa_to_rgb, rgb_to_hexa, col2hue, rgb_to_hsv, convert_K_to_RGB
from tkcolorpicker.gradientbar import GradientBar
from tkcolorpicker.colorsquare import ColorSquare
from tkcolorpicker.spinbox import Spinbox
from tkcolorpicker.limitvar import LimitVar

from mlpyproggen.lightgradientbar import LightGradientBar
from mlpyproggen.colorwheel import ColorWheel
from mlpyproggen.DefaultConstants import COLORCOR_MAX, DEFAULT_PALETTE, LARGE_FONT, SMALL_FONT, VERY_LARGE_FONT, PROG_VERSION, PERCENT_BRIGHTNESS, BLINKFRQ, ARDUINO_WAITTIME
# fromx mlpyproggen.dictFile import saveDicttoFile, readDictFromFile
import mlpyproggen.dictFile as dictFile
from locale import getdefaultlocale
import re
import time
import logging

VERSION ="V01.17 - 25.12.2019"
LARGE_FONT= ("Verdana", 12)
VERY_LARGE_FONT = ("Verdana", 14)
SMALL_FONT= ("Verdana", 8)

PERCENT_BRIGHTNESS = 1  # 1 = Show the brightnes as percent, 0 = Show the brightnes as ">>>"# 03.12.19:

COLORCOR_MAX = 255

        
# ----------------------------------------------------------------
# Class SoundCheckPage
# ----------------------------------------------------------------

class SoundCheckPage(tk.Frame):

    # ----------------------------------------------------------------
    # ColorCheckPage __init__
    # ----------------------------------------------------------------

    def __init__(self, parent, controller):
        
        self.tabClassName = "SoundCheckPage"
        tk.Frame.__init__(self,parent)
        self.controller = controller
        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName)

        button1_text = macrodata.get("Button_1",self.tabClassName)
        button2_text = macrodata.get("Button_2",self.tabClassName)        

        self.main_frame = ttk.Frame(self, relief="ridge", borderwidth=2)
        self.main_frame.pack(expand=1,fill="both")
        
        title_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2)

        label = ttk.Label(title_frame, text=self.title, font=LARGE_FONT)
        label.pack(padx=5,pady=(5,5))
        
        config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=4,startrow =1,style="CONFIGPage")  
        
        button_frame = ttk.Frame(self.main_frame)

        self.send_button = ttk.Button(button_frame, text=button1_text,width=30, command=self.execute_button_1)
        self.send_button.pack(side="left", padx=4, pady=(4, 1))
                
        # locate frames in main_frame
        title_frame.grid(row=0, column=0, columnspan=2, pady=(4, 10), padx=10)
        config_frame.grid(row=1, columnspan=2, pady=(20, 30), padx=10)
        button_frame.grid(row=2, column=0,padx=10, pady=(10, 4))
        
        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(3,weight=1)         

        # --- bindings
        
        self.controller.bind("<F1>",self.controller.call_helppage)
        self.controller.bind("<Alt-F4>",self.cancel)
        self.controller.bind("<Control-z>",self.controller.MenuUndo)
        self.controller.bind("<Control-y>",self.controller.MenuRedo)

         
    def cancel(self,_event=None):
        try:
            #self.led_off()
            pass
        except:
            pass

    def tabselected(self):
        logging.debug("Tabselected: %s",self.tabname)
        #self.controller.currentTabClass = self.tabClassName
        #self.controller.send_to_ARDUINO("#BEGIN")
        #time.sleep(ARDUINO_WAITTIME)
        #self.controller.connect()
        self.controller.ARDUINO_begin_direct_mode()
        paramdict = self.controller.bind_keys_dict.get(self.tabClassName,{})
        if paramdict != {}:
            for paramkey in paramdict:
                paramvar = paramdict[paramkey]
                if paramvar.key_up != "":
                    self.controller.bind(paramvar.key_up,paramvar.invoke_buttonup)
                if paramvar.key_down != "":    
                    self.controller.bind(paramvar.key_down,paramvar.invoke_buttondown)
        
    def tabunselected(self):
        logging.debug("Tabunselected: %s",self.tabname)
        #self.controller.send_to_ARDUINO("#END")
        #time.sleep(ARDUINO_WAITTIME)
        self.controller.ARDUINO_end_direct_mode()
        paramdict = self.controller.bind_keys_dict.get(self.tabClassName,{})
        if paramdict != {}:
            for paramkey in paramdict:
                paramvar = paramdict[paramkey]
                if paramvar.key_up != "":
                    self.controller.unbind(paramvar.key_up)
                if paramvar.key_down != "":    
                    self.controller.unbind(paramvar.key_down) 
        

    def getConfigData(self, key):
        return self.controller.getConfigData(key)
    
    def readConfigData(self):
        self.controller.readConfigData()
        
    def setConfigData(self,key, value):
        self.controller.setConfigData(key, value)

    def setParamData(self,key, value):
        self.controller.setParamData(key, value)

    def connect(self,port):
        pass

    def disconnect(self):
        pass
    
    def _update_value(self,paramkey):
        logging.info("SoundCheckPage - update_value: %s",paramkey)
        red=self.controller.get_macroparam_val(self.tabClassName, "Sound_RED")
        green=self.controller.get_macroparam_val(self.tabClassName, "Sound_GREEN")
        blue=self.controller.get_macroparam_val(self.tabClassName, "Sound_BLUE")
        address = self.controller.get_macroparam_val(self.tabClassName, "SoundAddress")
        implength = self.controller.get_macroparam_val(self.tabClassName, "SoundImpulsLength")
        self._send_sound_to_ARDUINO(red,green,blue,address,implength)        
            
    def MenuUndo(self,_event=None):
        pass
    
    def MenuRedo(self,_event=None):
        pass

    @staticmethod
    def _select_all_spinbox(event):
        """Select all entry content."""
        event.widget.selection('range', 0, 'end')
        return "break"

    @staticmethod
    def _select_all_entry(event):
        """Select all entry content."""
        event.widget.selection_range(0, 'end')
        return "break"

    def _unfocus(self, event):
        """Unfocus palette items when click on bar or square."""
        w = self.focus_get()
        if w != self and 'spinbox' not in str(w) and 'entry' not in str(w):
            self.focus_set()
          
    def execute_button_1(self,event=None):
        red=self.controller.get_macroparam_val(self.tabClassName, "Sound_RED")
        green=self.controller.get_macroparam_val(self.tabClassName, "Sound_GREEN")
        blue=self.controller.get_macroparam_val(self.tabClassName, "Sound_BLUE")
        address = self.controller.get_macroparam_val(self.tabClassName, "SoundAddress")
        implength = self.controller.get_macroparam_val(self.tabClassName, "SoundImpulsLength")
        self._send_sound_to_ARDUINO(red,green,blue,address,implength)
    
    def _send_sound_to_ARDUINO(self, red, green, blue,address,soundImpulsLength):
        soundmodul = '{:02x}'.format(address)
        sound1 = '{:02x}'.format(red)
        sound2 = '{:02x}'.format(green)
        sound3 = '{:02x}'.format(blue)
        if self.controller.mobaledlib_version == 1:
            message = "#L" + soundmodul + " " + sound1 + " " + sound2 + " " + sound3 + " " + '{:02x}'.format(1) + "\n"
        else:
            message = "#L " + soundmodul + " " + sound1 + " " + sound2 + " " + sound3 + " " + '{:02x}'.format(1) + "\n"
        self.controller.send_to_ARDUINO(message)
        self.after(soundImpulsLength,self.onstopImpuls)
        
            
    def onstopImpuls(self):
        soundmodul = '{:02x}'.format(self.controller.get_macroparam_val(self.tabClassName, "SoundAddress"))
        if self.controller.mobaledlib_version == 1:
            message = "#L" + soundmodul + " 00 00 00 01" + "\n"
        else:
            message = "#L " + soundmodul + " 00 00 00 01" + "\n"
        self.controller.send_to_ARDUINO(message)        



