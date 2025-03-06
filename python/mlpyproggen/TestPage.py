# -*- coding: utf-8 -*-
#
#         MobaLedCheckColors: Color checker for WS2812 and WS2811 based MobaLedLib
#
#         ConfigPage
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

#from tkcolorpicker.spinbox import Spinbox
#from tkcolorpicker.limitvar import LimitVar
#import serial.tools.list_ports as portlist
from scrolledFrame.ScrolledFrame import VerticalScrolledFrame,HorizontalScrolledFrame,ScrolledFrame
#from vb2pyconv.projectconverter import vb2py

#from locale import getdefaultlocale
import logging
#import serial
#import time
#import platform
import os
import proggen.M40_ShellandWait as M40
from vb2py.vbconstants import *
import mlpyproggen.Prog_Generator as PG
import ExcelAPI.XLA_Application as P01
import proggen.Userform_Testgrafik as D15

from mlpyproggen.DefaultConstants import COLORCOR_MAX, DEFAULT_PALETTE, LARGE_FONT, SMALL_FONT, VERY_LARGE_FONT, PROG_VERSION

Resp_STK_OK = b'\x10'
Resp_STK_FAILED = b'\x11'
Resp_STK_INSYNC = b'\x14'
Sync_CRC_EOP = b'\x20'
Cmnd_STK_GET_PARAMETER = b'\x41'
Cmnd_STK_GET_SYNC = b'\x30'
STK_READ_SIGN = b'\x75'
Parm_STK_HW_VER = b'\x80'
Parm_STK_SW_MAJOR = b'\x81'
Parm_STK_SW_MINOR = b'\x82'


# ----------------------------------------------------------------
# Class VB2PYPage
# ----------------------------------------------------------------

class TestPage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        self.arduino_portlist = {}
        tk.Frame.__init__(self,parent)
        self.tabClassName = "TestPage"
        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName)

        self.ProgGen_Excel_filename = ""
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        
        self.frame=ttk.Frame(self,relief="ridge", borderwidth=1)
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)        
        
        #self.scroll_main_frame = ScrolledFrame(self.frame)
        #self.scroll_main_frame.grid_columnconfigure(0,weight=1)
        #self.scroll_main_frame.grid_rowconfigure(0,weight=1)
        
        self.main_frame = ttk.Frame(self.frame, relief="ridge", borderwidth=2)
        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(2,weight=1) 
                
        title_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2)

        label = ttk.Label(title_frame, text=self.title, font=LARGE_FONT)
        label.pack(padx=5,pady=(5,5))
        
        #self.scroll_configframe = VerticalScrolledFrame(self.main_frame)
        
        #config_frame = self.controller.create_macroparam_frame(self.scroll_configframe.interior,self.tabClassName, maxcolumns=1,startrow =10,style="CONFIGPage")        
        config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=1,startrow =10,style="CONFIGPage")  
        # --- Buttons
        button_frame = ttk.Frame(self.main_frame)
#
        button1_text = macrodata.get("Button_1",self.tabClassName)
        button2_text = macrodata.get("Button_2",self.tabClassName)
        button3_text = macrodata.get("Button_3",self.tabClassName)
        button4_text = macrodata.get("Button_4",self.tabClassName)
        button5_text = macrodata.get("Button_5",self.tabClassName)
        
        self.update_button = ttk.Button(button_frame, text=button1_text, command=self.save_config)
        self.update_button.pack(side="right", padx=10)
        
        # --- start cmd checkbox and file selection
        startcmd_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2)
        
        #self.s_startcmdcbvar = tk.IntVar()
        #self.s_startcmdcb = ttk.Checkbutton(startcmd_frame,text=button2_text,variable=self.s_startcmdcbvar,onvalue = 1, offvalue = 0, command=self.startcmd)
        #self.s_startcmdcb.grid(sticky='w', padx=4, pady=4, row=0,column=0)
        #self.s_startcmdcbvar.set(self.getConfigData("startcmdcb"))
        
        self.ProgGen_Excel_filename = self.getConfigData("ProgGenExcel_filename")
        self.startcmd_button = ttk.Button(startcmd_frame, text=button3_text,width=30, command=self.askselectfile)
        self.startcmd_button.grid(row=0,column=1, padx=4, pady=4,sticky="w")
        self.startcmd_label = tk.Label(startcmd_frame, text=self.ProgGen_Excel_filename,width=120,height=1,wraplength=700)
        self.startcmd_label.grid(row=1,column=0,columnspan=2,padx=4, pady=4,sticky="w")

        #create frame and entry for arduino resources  path (libraries, examples, hardware etc)
        # --- start cmd checkbox and file selection
        resourcePath_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2)
        
        #self.s_resourcePathcbvar = tk.IntVar()
        #self.s_resourcePathcb = ttk.Checkbutton(resourcePath_frame,text=button4_text,variable=self.s_resourcePathcbvar,onvalue = 1, offvalue = 0, command=self.resourcePath)
        #self.s_resourcePathcb.grid(sticky='w', padx=4, pady=4, row=0,column=0)
        #self.s_resourcePathcbvar.set(self.getConfigData("resourcePathcb"))
        
        self.output_dir = self.getConfigData("VB2PY_output_Dir")
        self.resourcePath_button = ttk.Button(resourcePath_frame, text=button4_text,width=30, command=self.askresource_path)
        self.resourcePath_button.grid(row=0,column=1, padx=4, pady=4,sticky="w")
        self.resourcePath_label = tk.Label(resourcePath_frame, text=self.output_dir,width=120,height=1,wraplength=700)
        self.resourcePath_label.grid(row=1,column=0,columnspan=2,padx=4, pady=4,sticky="w")
        
        startConvPath_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2)
        self.startConvbutton = ttk.Button(startConvPath_frame, text=button5_text,width=30, command=self.startGrafik)
        self.startConvbutton.grid(row=0,column=0, padx=4, pady=4,sticky="w")

        # --- placement
        # Tabframe
        self.frame.grid(row=0,column=0)
        #self.scroll_main_frame.grid(row=0,column=0,sticky="nesw")
        # scroll_main_frame
        self.main_frame.grid(row=0,column=0)
        # main_frame        
        title_frame.grid(row=0, column=0, pady=10, padx=10)
        button_frame.grid(row=1, column=0,pady=10, padx=10)
        config_frame.grid(row=2, column=0, pady=10, padx=10, sticky="nesw")
        startcmd_frame.grid(row=3, column=0, pady=10, padx=10, stick="ew")
        #resourcePath_frame.grid(row=4, column=0, pady=10, padx=10, stick="ew")
        startConvPath_frame.grid(row=5, column=0, pady=10, padx=10, stick="ew")

        macroparams = macrodata.get("Params",[])
        
        #for paramkey in macroparams:
        #    #paramconfig_dict = self.controller.MacroParamDef.data.get(paramkey,{})
        #    configdatakey = self.controller.getConfigDatakey(paramkey)
        #    value = self.getConfigData(configdatakey)
        #    self.controller.set_macroparam_val(self.tabClassName, paramkey, value)

        # ----------------------------------------------------------------
        # Standardprocedures for every tabpage
        # ----------------------------------------------------------------

    def tabselected(self):
        #self.controller.currentTabClass = self.tabClassName
        #self.ledmaxcount.set(self.controller.get_maxLEDcnt())
        logging.debug("Tabselected: %s",self.tabname)
        self.store_old_config()
    
    def tabunselected(self):
        logging.debug("Tabunselected: %s",self.tabname)
       
    def cancel(self):
        self.save_config()

    def getConfigPageParams(self):
        pass
    
    def getConfigData(self, key):
        return self.controller.getConfigData(key)
    
    def readConfigData(self):
        self.controller.readConfigData()
        
    def setConfigData(self,key, value):
        self.controller.setConfigData(key, value)
        
    def setConfigDataDict(self,paramdict):
        self.controller.setConfigDataDict(paramdict)
        
    def get_macroparam_var_values(self,macro):
        return self.controller.get_macroparam_var_values(macro)        

    def setParamData(self,key, value):
        self.controller.setParamData(key, value)

    def MenuUndo(self,_event=None):
        logging.debug("MenuUndo: %s",self.tabname)
        pass
    
    def MenuRedo(self,_event=None):
        logging.debug("MenuRedo: %s",self.tabname)
        pass
    
    def connect (self,port):
        pass
    
    def disconnect (self):
        pass
    
    def save_config(self):
        self.setConfigData("pos_x",self.winfo_x())
        self.setConfigData("pos_y",self.winfo_y())
        self.setConfigData("startcmd_filename", self.ProgGen_Excel_filename)
        self.setConfigData("resourcePath_filename", self.output_dir)
        param_values_dict = self.get_macroparam_var_values(self.tabClassName)
        #self.setConfigDataDict(param_values_dict)
        
        self.store_old_config()
        self.controller.SaveConfigData()
        
        logging.debug("SaveConfig: %s - %s",self.tabname,repr(self.controller.ConfigData.data))

    def store_old_config(self):
        self.old_startcmd_filename = self.ProgGen_Excel_filename
        self.old_resourcePath_filename = self.output_dir
        self.old_param_values_dict = self.get_macroparam_var_values(self.tabClassName)
    
    def check_if_config_data_changed(self):
        if self.old_startcmd_filename != self.ProgGen_Excel_filename:
            return True
        if self.old_resourcePath_filename != self.output_dir:
            return True        
        param_values_dict = self.get_macroparam_var_values(self.tabClassName)
        if self.old_param_values_dict != param_values_dict:
            return True
        return False

    def askselectfile(self):
        self.ProgGen_Excel_filename = tk.filedialog.askopenfilename()
        self.startcmd_label.configure(text=self.ProgGen_Excel_filename)
        
    def askresource_path(self):
        self.output_dir = tk.filedialog.askdirectory()
        self.resourcePath_label.configure(text=self.output_dir)
        
    def startGrafik (self):
        background_image = self.ProgGen_Excel_filename
        UserForm_TestGrafik = D15.UserForm_TestGrafik(PG.global_controller, background_image=background_image)
        UserForm_TestGrafik.Show_With_Existing_Data("")
        
        


    



