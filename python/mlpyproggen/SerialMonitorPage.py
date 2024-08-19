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
import traceback
from tkinter import ttk,messagebox
# fromx tkcolorpicker.functions import tk, ttk, round2, create_checkered_image, \
#    overlay, hsv_to_rgb, hexa_to_rgb, rgb_to_hexa, col2hue, rgb_to_hsv, convert_K_to_RGB
# fromx tkcolorpicker.alphabar import AlphaBar
# fromx tkcolorpicker.gradientbar import GradientBar
# fromx tkcolorpicker.lightgradientbar import LightGradientBar
# fromx tkcolorpicker.colorsquare import ColorSquare
# fromx tkcolorpicker.colorwheel import ColorWheel
# fromx tkcolorpicker.spinbox import Spinbox
# fromx tkcolorpicker.limitvar import LimitVar
from mlpyproggen.configfile import ConfigFile
from locale import getdefaultlocale
from scrolledFrame.ScrolledFrame import VerticalScrolledFrame,HorizontalScrolledFrame,ScrolledFrame

#import re
#import math
import os
import serial
import sys
import threading
import queue
import time
import logging
#import concurrent.futures
#import random
#import webbrowser
from datetime import datetime
#import json

VERSION ="V01.17 - 25.12.2019"
LARGE_FONT= ("Verdana", 12)
VERY_LARGE_FONT = ("Verdana", 14)
SMALL_FONT= ("Verdana", 8)


ThreadEvent = None
            
class SerialMonitorPage(tk.Frame):
    def __init__(self, parent, controller):
        self.tabClassName = "SerialMonitorPage"
        tk.Frame.__init__(self,parent)
        self.controller = controller
        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName)
        
        button1_text = macrodata.get("Button_1",self.tabClassName)
        button2_text = macrodata.get("Button_2",self.tabClassName)        

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

        label = ttk.Label(title_frame, text=self.title, font=LARGE_FONT)
        label.pack(padx=5,pady=(5,5))
        
        config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=1,startrow =1,style="CONFIGPage")        
        
        button_frame = ttk.Frame(self.main_frame)

        self.send_button = ttk.Button(button_frame, text=button1_text,width=30, command=self.send)
        self.send_button.pack(side="left", padx=4, pady=(4, 1))
        text_frame = tk.Frame(self.main_frame, padx=10, pady= 10)
        self.text = tk.Text(text_frame, wrap='word', bg=self.cget('bg'),height=25,width=100)         # 04.12.19: Old: height=10, width=50
        scroll=tk.Scrollbar(text_frame)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.text.yview)
        #pack everything
        self.text.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
        scroll.pack(side=tk.RIGHT,fill=tk.Y)
        # locate frames in main_frame
        # Tabframe
        self.frame.grid(row=0,column=0)
        self.scroll_main_frame.grid(row=0,column=0,sticky="nesw")
        # scroll_main_frame
        self.main_frame.grid(row=0,column=0)
        # main_frame                
        title_frame.grid(row=0, column=0, columnspan=2, pady=(4, 10), padx=10)
        config_frame.grid(row=1, columnspan=2, pady=(20, 30), padx=10)
        button_frame.grid(row=2, column=0,padx=10, pady=(10, 4))
        text_frame.grid(row=3, column=0,padx=10, pady=(10, 4),sticky="nesw")
        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(3,weight=1)                
        self.queue = queue.Queue()
        self.monitor_serial = False
        self.Z21page = self.controller.tabdict.get("Z21MonitorPage",None)
        self.check_RMBUS = False
        if self.Z21page:
            self.RMBUS_request_timer_confvalue_str = self.controller.getConfigData("RMbusTimer")
            if self.RMBUS_request_timer_confvalue_str == "":
                self.RMBUS_request_timer_confvalue = 0
            else:
                self.RMBUS_request_timer_confvalue = int(self.RMBUS_request_timer_confvalue_str)
            self.RMBUS_request_timer = self.RMBUS_request_timer_confvalue

    def tabselected(self):
        logging.debug("Tabselected: %s",self.tabname)
        logging.info(self.tabname)
    
    def tabunselected(self):
        logging.debug("Tabunselected: %s",self.tabname)
    
    def _update_value(self,paramkey):
        logging.info("SerialMonitorPage - update_value: %s",paramkey)
        message = self.controller.get_macroparam_val(self.tabClassName, "SerialMonitorInput")+"\r\n" #self.input.get() +"\r\n"
        self.controller.send_to_ARDUINO(message)        

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
        logging.info("dummy")

    def send(self,event=None):
        message = self.controller.get_macroparam_val(self.tabClassName, "SerialMonitorInput")+"\r\n" #self.input.get() +"\r\n"
        self.controller.send_to_ARDUINO(message)

    def process_serial(self):
        #print("Serial MonitorPage - process_serial: Start")
        textmessage = self.controller.checkconnection()
        if textmessage:
            self.text.insert("end", textmessage)
            self.text.yview("end")
            self.controller.set_ARDUINOmessage(textmessage)
        else:
            if self.controller.queue:
                while self.controller.queue.qsize():
                    #print("process_serial: While loop")
                    try:
                        readtext = self.controller.queue.get()
                        date_time = datetime.now()
                        d = date_time.strftime("%H:%M:%S")
                        textmessage = d + "  " + readtext
                        if not textmessage.endswith("\n"):
                            textmessage = textmessage +"\n"
                        #write message into text window
                        self.text.insert("end", textmessage)
                        self.text.yview("end")
                        if readtext.startswith("JSON:"):
                            json_str = readtext[5:]
                            if self.Z21page:
                                self.Z21page.notifyZ21_RMBUS_DATA(json_str)
                        elif readtext.startswith("#?"):
                            temp_list = readtext.split(",")
                            self.controller.max_ledcnt_list = temp_list[1:]
                            self.controller.max_LEDchannel = len(self.controller.max_ledcnt_list)
                            ledchannel_str = self.getConfigData("LEDchannel")
                            if ledchannel_str != "":
                                self.controller.LEDchannel = int(ledchannel_str)
                            else:
                                self.controller.LEDchannel = 0
                            if len(self.controller.max_ledcnt_list)<=self.controller.LEDchannel:
                                self.controller.LEDchannel = 0
                            self.controller.set_maxLEDcnt(int(self.controller.max_ledcnt_list[self.controller.LEDchannel]))
                            self.controller.LED_baseadress = 0
                            maxLEDcnt = 0
                            # maxLEDcnt = sum of all maxLEDcnt per channel
                            for i in range (0,self.controller.max_LEDchannel):
                                maxLEDcnt+=int(self.controller.max_ledcnt_list[i])
                            self.controller.set_maxLEDcnt(maxLEDcnt)
                        else:
                            self.controller.set_ARDUINOmessage(textmessage)
                    except IOError:
                        pass
        if self.check_RMBUS:
            self.RMBUS_request_timer -= 1
            if self.RMBUS_request_timer == 0:
                self.controller.send_to_ARDUINO("?*\n")
                self.RMBUS_request_timer = self.RMBUS_request_timer_confvalue
        if self.monitor_serial:
            self.after(100, self.process_serial)

    def set_check_RMBUS(self,value=False):
                
        if self.RMBUS_request_timer_confvalue>0:
            self.check_RMBUS = False #value
        else:
            self.check_RMBUS = False
        if self.check_RMBUS:
            self.RMBUS_request_timer = self.RMBUS_request_timer_confvalue
        
        if value:
            #self.controller.send_to_ARDUINO("?+\r\n")
            pass
        else:
            #self.controller.send_to_ARDUINO("?-\r\n")
            pass
    
    def start_process_serial(self):
        global ThreadEvent
        logging.debug("SerialMonitorPage: start_process_serial")
        ThreadEvent = threading.Event()
        ThreadEvent.set()
        time.sleep(2)
        ThreadEvent.clear()
        self.monitor_serial = True
        self.thread = SerialThread(self.controller.queue,self.controller.arduino)
        self.thread.start()
        self.process_serial()
        self.RMBUS_request_timer_confvalue_str = self.controller.getConfigData("RMbusTimer")
        if self.RMBUS_request_timer_confvalue_str == "":
            self.RMBUS_request_timer_confvalue = 1
        else:
            self.RMBUS_request_timer_confvalue = int(self.RMBUS_request_timer_confvalue_str)
        self.RMBUS_request_timer = self.RMBUS_request_timer_confvalue        
        self.RMBUS_request_timer = self.RMBUS_request_timer_confvalue

    def stop_process_serial(self):
        logging.debug("stop_process_serial")
        #print("SerialMonitorPage: stop_process_serial")
        global ThreadEvent
        self.monitor_serial = False
        if ThreadEvent:
            logging.debug("Set ThreadEvent")
            ThreadEvent.set()
        #time.sleep(1)
        
    def cancel(self):
        self.stop_process_serial()
        
    def connect (self,port):
        self.start_process_serial()
    
    def disconnect (self):
        self.stop_process_serial()
        
class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        msg_length = 0
        result = ""
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        try:
            while not ThreadEvent.is_set() and self.s != None and self.s.is_open:
                i = max(1, min(2048, self.s.in_waiting)) # any bytes in buffer
                data = self.s.read(1)                    # read one byte  
                logging.debug("serialread from ARDUINO:"+ str(data)+ "("+str(data.hex())+")")
                if data >= b"xD0": # binary communication detected, read one binary message
                    chkSum = int.from_bytes(data,byteorder = "big")
                    toReadbyte = self.s.read(1) # read length byte
                    logging.debug("serialread from ARDUINO length:"+ str(toReadbyte)+ "("+str(toReadbyte.hex())+")")
                    msg_length = int.from_bytes(toReadbyte,byteorder = "big")
                    chkSum ^= msg_length
                    result = "JSON:{\"RMBUS\": \""
                    for i in range(msg_length):
                        Readbyte = self.s.read(1)
                        logging.debug("serialread from ARDUINO length:"+ str(Readbyte)+ "("+str(Readbyte.hex())+")")
                        ReadbyteInt = int.from_bytes(Readbyte,byteorder = "big")
                        chkSum ^= ReadbyteInt
                        if i < msg_length-1: # handle data bytes, last byte is for checksum only
                            result_str = Readbyte.hex()
                            result += result_str
                    result += "\"}"
                    if chkSum != 255:
                        logging.debug("Checksum error in Feedback-String:"+ result)
                    return result
                else:
                    i = data.find(b"\n")
                    if i >= 0:
                        r = self.buf + data[:i+1]
                        self.buf[0:] = data[i+1:]
                        return r
                self.buf.extend(data)
        except BaseException as e:
            logging.debug("SerialMonitorPage: Readline exception")
            logging.debug(e, exc_info=True) 
            traceback.print_exc()
            logging.debug("------------------")
            result = ""
            logging.debug("Set ThreadEvent, Readline error")
            ThreadEvent.set() 
            return result

class SerialThread(threading.Thread):
    def __init__(self, p_queue, p_serialport,p_serialportname=""):
        #global serialport
        threading.Thread.__init__(self)
        self.queue = p_queue
        self.serialport = p_serialport
        self.serialport_name = p_serialportname
        self.rl = ReadLine(p_serialport)

    def run(self):
        #global serialport
        logging.info("SerialThread started:"+self.serialport_name)
        if self.serialport:
            while not ThreadEvent.is_set() and self.serialport.is_open:
                if self.serialport and self.serialport.is_open:
                    text = self.rl.readline()
                    if text != None:
                        if len(text)>0:
                            try:
                                self.queue.put(text.decode('utf-8'))
                                logging.info("SerialThread (%s) got message: %s", self.serialport_name,str(text.decode('utf-8')))
                            except:
                                self.queue.put(text)
                                logging.info("SerialThread (%s) got message: %s", self.serialport_name,str(text))
        logging.info("SerialThread (%s) received event. Exiting", self.serialport_name)

