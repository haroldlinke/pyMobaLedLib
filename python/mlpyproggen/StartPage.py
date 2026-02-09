# -*- coding: utf-8 -*-
#
#         MobaLedCheckColors: Color checker for WS2812 and WS2811 based MobaLedLib
#
#         StartPage
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
# * V1.00 11.04.2020 - Harold Linke - first release
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
from mlpyproggen.configfile import ConfigFile
from locale import getdefaultlocale
#import re
#import math
import os
#import serial
#import sys
#import threading
#import queue
import time
import logging
logger=logging.getLogger(__name__)

import urllib
#import concurrent.futures
#import random
#import webbrowser
from datetime import datetime
from scrolledFrame.ScrolledFrame import VerticalScrolledFrame,HorizontalScrolledFrame,ScrolledFrame

#import json

VERSION ="V02.00 - 11.04.2020"
LARGE_FONT= ("Verdana", 12)
VERY_LARGE_FONT = ("Verdana", 14)
SMALL_FONT= ("Verdana", 8)

BUTTONLABELWIDTH = 10

def check_for_existing_messages(mode=""):
    try:
        currURL = "http://www.hlinke.de/files/pyMobaLedLibMessage.html"
        # Assign the open file to a variable
        webFile = urllib.request.urlopen(currURL)
        html_message = str(webFile.read())
    except:
        html_message = ""
    
    if mode !="":
        # check if there is a mode specific message available
        try:
            currURL = "http://www.hlinke.de/files/pyMobaLedLibMessage"+ mode+".html"
            # Assign the open file to a variable
            webFile = urllib.request.urlopen(currURL)
            # Read the file contents to a variable
            html_message = str(webFile.read())
        except:
            pass
        
    html_message = html_message[2:len(html_message)-1]
    return html_message
            
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        self.tabClassName = "StartPage"
        self.controller = controller
        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName)
        
        tk.Frame.__init__(self, parent)
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        
        self.frame=ttk.Frame(self,relief="ridge", borderwidth=1)
        
        self.scroll_main_frame = ScrolledFrame(self.frame)

        self.main_frame = ttk.Frame(self.scroll_main_frame.interior, relief="ridge", borderwidth=2)

        title_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=1)
        label = ttk.Label(title_frame, text=self.title, font=LARGE_FONT)
        label.pack(padx=5,pady=(5,5))

        config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=4,startrow =1,style="CONFIGPage")
        
        text_frame = ttk.Frame(self.main_frame,relief="ridge", borderwidth=2)

        #text = macrodata.get("Ausführliche Beschreibung","")
        
        photo_filename = macrodata.get("Photo","")
        try:
            if photo_filename != "":
                filedir = os.path.dirname(os.path.realpath(__file__))
                self.photofilepath = os.path.join(filedir, photo_filename)
                text1 = tk.Text(text_frame, width=30,bg=self.cget('bg'),relief="flat")
                self.photo=tk.PhotoImage(file=self.photofilepath)
                text1.insert(tk.END,'\n')
                text1.image_create(tk.END, image=self.photo)
        except BaseException as e:
            logger.debug("Startpage: Image "+self.photofilepath+" not found")
            self.photo = None
        
        content = macrodata.get("Content",{})
        
        if content != {}:
            text_widget = tk.Text(text_frame,wrap=tk.WORD,bg=self.cget('bg'),relief="flat")
            text_scroll = tk.Scrollbar(text_frame, command=text_widget.yview)
            text_widget.configure(yscrollcommand=text_scroll.set)                    
            for titel,text in content.items():
                text_widget.tag_configure('bold_italics', font=('Verdana', 10, 'bold', 'italic'))
                text_widget.tag_configure('big', font=('Verdana', 14, 'bold'))
                text_widget.tag_configure('normal', font=('Verdana', 10, ))
                text_widget.insert(tk.END,"\n"+titel+"\n", 'big')
                text_widget.insert(tk.END, text, 'normal')
            text_widget.config(state=tk.DISABLED)        

        # --- placement
        # Tabframe => frame
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)                
        # Frame placement => scroll_main_frame
        self.frame.grid(row=0,column=0,sticky="n")
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)              
        # scroll_main_frame => scroll_main_frame.interior => main_frame
        self.scroll_main_frame.grid(row=0,column=0,sticky="nesw")
        self.scroll_main_frame.grid_columnconfigure(0,weight=1)
        self.scroll_main_frame.grid_rowconfigure(0,weight=1)
        
        self.scroll_main_frame.interior.grid_rowconfigure(0,weight=1)
        self.scroll_main_frame.interior.grid_columnconfigure(0,weight=1)
        
        # main_frame => title_frame, config_frame, text_frame
        self.main_frame.grid(row=0,column=0,sticky="nesw")
        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(2,weight=1)         
        # place frames in main_frame
        title_frame.grid(row=0, column=0, pady=10, padx=10)
        config_frame.grid(row=1, column=0, pady=10, padx=10)
        text_frame.grid(row=2,column=0,padx=10, pady=0,sticky="nesw")
        text_frame.grid_columnconfigure(1,weight=1)
        text_frame.grid_rowconfigure(0,weight=1)
        
        html_message=check_for_existing_messages(mode="")
        if html_message != "":
            html_label = tk.Label(self.main_frame,text=html_message,height=1,width=200,borderwidth=2,relief="ridge",)                
            html_label.grid(row=3, column=0, pady=0, padx=10,sticky=("nesw"))
        # place widgets in text_frame => text1,text:widget, text_scroll
        #text1.pack(side=tk.LEFT,expand=0)
        #text_widget.pack(side=tk.LEFT,fill=tk.BOTH,padx=10,pady=(10,0))
        #text_scroll.pack(side=tk.LEFT,fill=tk.Y)
        text1.grid(row=0,column=0,sticky="ns")
        text_widget.grid(row=0,column=1,sticky=("nesw"),padx=10,pady=10)
        text_scroll.grid(row=0,column=2,sticky=("ns"))                


       
    def cancel(self,_event=None):
        pass
        
    def tabselected(self):
        logger.debug("Tabselected: %s",self.tabname)
        #self.controller.currentTabClass = self.tabClassName
        logger.info(self.tabname)
        pass
    
    def tabunselected(self):
        logger.debug("Tabunselected: %s",self.tabname)
        pass
    
    def TabChanged(self,_event=None):
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
    
    def dummy(self,event):
        logger.info("dummy")

    def send_command_to_ARDUINO(self,command):
        pass

    def connect(self,port):
        pass

    def disconnect(self):
        pass
