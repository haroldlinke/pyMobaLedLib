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

import proggen.M08_ARDUINO as M08
import proggen.M02_Public as M02
from datetime import datetime
import json

import socket
import sys
import binascii


VERSION ="V01.17 - 25.12.2019"
LARGE_FONT= ("Verdana", 12)
VERY_LARGE_FONT = ("Verdana", 14)
SMALL_FONT= ("Verdana", 8)






HOST = ''	# Symbolic name meaning all available interfaces

# define Z21 constants 
z21HWTypeMSB = 0x02
z21HWTypeLSB = 0x01

z21FWVersionMSB = 0x01
z21FWVersionLSB = 0x30
#Seriennummer:
z21SnMSB = 0x1A
z21SnLSB = 0xF5
z21Port  =21105

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = z21Port 


#Z21LAN Protokoll Spezifikation:
LAN_X_Header                  = 0x40 
LAN_GET_SERIAL_NUMBER         = 0x10
LAN_GET_CODE                  = 0x18 
LAN_LOGOFF                    = 0x30
LAN_X_GET_SETTING             = 0x21  
LAN_X_BC_TRACK_POWER          = 0x61
LAN_X_UNKNOWN_COMMAND         = 0x61
LAN_X_STATUS_CHANGED          = 0x62
LAN_X_GET_VERSION             = 0x63  
LAN_X_SET_STOP                = 0x80  
LAN_X_BC_STOPPED              = 0x81
LAN_X_GET_FIRMWARE_VERSION    = 0xF1
LAN_SET_BROADCASTFLAGS        = 0x50
LAN_GET_BROADCASTFLAGS        = 0x51
LAN_SYSTEMSTATE_DATACHANGED   = 0x84
LAN_SYSTEMSTATE_GETDATA       = 0x85
LAN_GET_HWINFO                = 0x1A
LAN_GET_LOCOMODE              = 0x60
LAN_SET_LOCOMODE              = 0x61
LAN_GET_TURNOUTMODE           = 0x70
LAN_SET_TURNOUTMODE           = 0x71
LAN_X_GET_LOCO_INFO           = 0xE3
LAN_X_SET_LOCO                = 0xE4
LAN_X_SET_LOCO_FUNCTION       = 0xF8
LAN_X_LOCO_INFO               = 0xEF
LAN_X_GET_TURNOUT_INFO        = 0x43 
LAN_X_SET_TURNOUT             = 0x53
LAN_X_TURNOUT_INFO            = 0x43 
LAN_X_CV_READ                 = 0x23
LAN_X_CV_WRITE                = 0x24
LAN_X_CV_NACK_SC              = 0x61
LAN_X_CV_NACK                 = 0x61
LAN_X_CV_RESULT               = 0x64
LAN_RMBUS_DATACHANGED         = 0x80
LAN_RMBUS_GETDATA             = 0x81
LAN_RMBUS_PROGRAMMODULE       = 0x82
LAN_RAILCOM_DATACHANGED       = 0x88
LAN_RAILCOM_GETDATA           = 0x89
LAN_LOCONET_Z21_RX            = 0xA0
LAN_LOCONET_Z21_TX            = 0xA1
LAN_LOCONET_FROM_LAN          = 0xA2
LAN_LOCONET_DISPATCH_ADDR     = 0xA3
LAN_LOCONET_DETECTOR          = 0xA4
LAN_CAN_DETECTOR              = 0xC4
LAN_X_CV_POM                  = 0xE6
LAN_X_MM_WRITE_BYTE           = 0x24
LAN_X_DCC_READ_REGISTER       = 0x22
LAN_X_DCC_WRITE_REGISTER      = 0x23

z21_code_dict = {
"LAN_X_Header":0x40, 
"LAN_GET_SERIAL_NUMBER":0x10,
"LAN_GET_CODE":0x18,
"LAN_LOGOFF":0x30,
"LAN_X_GET_SETTING":0x21,
"LAN_X_BC_TRACK_POWER":0x61,
"LAN_X_UNKNOWN_COMMAND":0x61,
"LAN_X_STATUS_CHANGED":0x62,
"LAN_X_GET_VERSION":0x63,
"LAN_X_SET_STOP":0x80,
"LAN_X_BC_STOPPED":0x81,
"LAN_X_GET_FIRMWARE_VERSION":0xF1,
"LAN_SET_BROADCASTFLAGS":0x50,
"LAN_GET_BROADCASTFLAGS":0x51,
"LAN_SYSTEMSTATE_DATACHANGED":0x84,
"LAN_SYSTEMSTATE_GETDATA":0x85,
"LAN_GET_HWINFO":0x1A,
"LAN_GET_LOCOMODE":0x60,
"LAN_SET_LOCOMODE":0x61,
"LAN_GET_TURNOUTMODE":0x70,
"LAN_SET_TURNOUTMODE":0x71,
"LAN_X_GET_LOCO_INFO":0xE3,
"LAN_X_SET_LOCO":0xE4,
"LAN_X_SET_LOCO_FUNCTION":0xF8,
"LAN_X_LOCO_INFO":0xEF,
"LAN_X_GET_TURNOUT_INFO":0x43, 
"LAN_X_SET_TURNOUT":0x53,
"LAN_X_TURNOUT_INFO":0x43, 
"LAN_X_CV_READ":0x23,
"LAN_X_CV_WRITE":0x24,
"LAN_X_CV_NACK_SC":0x61,
"LAN_X_CV_NACK":0x61,
"LAN_X_CV_RESULT":0x64,
"LAN_RMBUS_DATACHANGED":0x80,
"LAN_RMBUS_GETDATA":0x81,
"LAN_RMBUS_PROGRAMMODULE":0x82,
"LAN_RAILCOM_DATACHANGED":0x88,
"LAN_RAILCOM_GETDATA":0x89,
"LAN_LOCONET_Z21_RX":0xA0,
"LAN_LOCONET_Z21_TX":0xA1,
"LAN_LOCONET_FROM_LAN":0xA2,
"LAN_LOCONET_DISPATCH_ADDR":0xA3,
"LAN_LOCONET_DETECTOR":0xA4,
"LAN_CAN_DETECTOR":0xC4,
"LAN_X_CV_POM":0xE6, 
"LAN_X_MM_WRITE_BYTE":0x24,
"LAN_X_DCC_READ_REGISTER":0x22,
"LAN_X_DCC_WRITE_REGISTER":0x23
}

#**************************************************************
#Z21 BC Flags
Z21bcNone                    = 0B00000000
Z21bcAll                     = 0x00000001
Z21bcAll_s                   = 0B00000001
Z21bcRBus                    = 0x00000002
Z21bcRBus_s                  = 0B00000010
Z21bcRailcom                 = 0x00000004
Z21bcRailcom_s               = 0x100

Z21bcSystemInfo              = 0x00000100
Z21bcSystemInfo_s            = 0B00000100

#ab FW Version 1.20:
Z21bcNetAll                  = 0x00010000
Z21bcNetAll_s                = 0B00001000

Z21bcLocoNet                 = 0x01000000
Z21bcLocoNet_s               = 0B00010000
Z21bcLocoNetLocos            = 0x02000000
Z21bcLocoNetLocos_s          = 0B00100000
Z21bcLocoNetSwitches         = 0x04000000
Z21bcLocoNetSwitches_s       = 0B01000000

#ab FW Version 1.22:
Z21bcLocoNetGBM              = 0x08000000
Z21bcLocoNetGBM_s            = 0B10000000

#ab FW Version 1.29:
Z21bcRailComAll              = 0x00040000
Z21bcRailComAll_s            = 0x200

#ab FW Version 1.30:
Z21bcCANDetector             = 0x00080000
Z21bcCANDetector_s           = 0x400


ThreadEvent_Z21 = None
            
class Z21MonitorPage(tk.Frame):
    
    def __init__(self, parent, controller):
        if controller.executetests:
            self.test_convert_7bit_to_8bit()
        self.tabClassName = "Z21MonitorPage"
        tk.Frame.__init__(self,parent)
        self.controller = controller
        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName)
        
        button1_text = macrodata.get("Button_1",self.tabClassName)
        button2_text = macrodata.get("Button_2",self.tabClassName)
        button3_text = macrodata.get("Button_3",self.tabClassName)        

        self.main_frame = ttk.Frame(self, relief="ridge", borderwidth=2)
        self.main_frame.pack(expand=1,fill="both")
        
        title_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2)

        label = ttk.Label(title_frame, text=self.title, font=LARGE_FONT)
        label.pack(padx=5,pady=(5,5))
        
        config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=1,startrow =1,style="CONFIGPage")        
        
        button_frame = ttk.Frame(self.main_frame)

        self.send_button = ttk.Button(button_frame, text=button1_text,width=30, command=self.start)
        self.send_button.pack(side="left", padx=4, pady=(4, 1))
        self.stop_button = ttk.Button(button_frame, text=button2_text,width=30, command=self.stop)
        self.stop_button.pack(side="left", padx=4, pady=(4, 1))
        
        self.show_button = ttk.Button(button_frame, text=button3_text,width=30, command=self.show_key_adresses)
        self.show_button.pack(side="left", padx=4, pady=(4, 1))        
        
        #self.input.bind("<Return>",self.send)

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
        
        # locate frames in main_frame
        title_frame.grid(row=0, column=0, columnspan=2, pady=(4, 10), padx=10)
        config_frame.grid(row=1, columnspan=2, pady=(20, 30), padx=10)
        button_frame.grid(row=2, column=0,padx=10, pady=(10, 4))
        text_frame.grid(row=3, column=0,padx=10, pady=(10, 4),sticky="nesw")
        
        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(3,weight=1)         

        self.queue = queue.Queue()
        self.queue_z21 = queue.Queue()
        self.monitor_serial = False
        
        self.client_turnout_info_dict = {}
        self.client_broadcast_flag_dict = {}
        self.client_RMBUS_GETDATA_dict = {}
        self.RMBUS_DATA_bytearray = {0: bytearray(10)}
                
        #create command dictionary
        self.z21_code2text_dict={}
        for key,value in z21_code_dict.items():
            self.z21_code2text_dict[value]=key
            
        #self.start_process_serial()

    def tabselected(self):
        logging.debug("Tabselected: %s",self.tabname)
        #self.controller.currentTabClass = self.tabClassName
        logging.debug(self.tabname)
        pass
    
    def tabunselected(self):
        logging.debug("Tabunselected: %s",self.tabname)
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
        logging.debug("dummy")
        
    def addTexttoQueue(self,text):
        self.controller.queue.put(text)    
    
    def _update_value(self,paramkey):
        logging.info("Z21MonitorPage - update_value: %s",paramkey)
        message = self.controller.get_macroparam_val(self.tabClassName, "Z21KeyTestInput")+"\r\n" #self.input.get() +"\r\n"
        #self.controller.send_to_ARDUINO(message)
        if message.startswith("JSON:"):
            self.addTexttoQueue(message)
        else:
            if len(message)%2 !=0:
                message = message[:-2]+"0"
            else:
                message = message[:-2]
            message = "JSON:{\"RMBUS\": \"" + message + "\"}"
        self.addTexttoQueue(message)
        
    def reset_z21_data(self):
        self.client_turnout_info_dict = {}
        self.client_broadcast_flag_dict = {}
        self.client_RMBUS_GETDATA_dict = {}
        self.RMBUS_DATA_bytearray = {0: bytearray(10)}
        logging.debug("reset_z21_data-end")
        
    def send_command_to_ARDUINO(self,dccaddress,channel,activate):
        logging.debug("send_command_to_ARDUINO entry: %s - %s",dccaddress,channel)
        #self.controller.connect_if_not_connected()
        #select the ARDUINO to send the commands to
        for port in self.controller.serial_port_dict:
            dcc_address_range=self.controller.serial_port_dict[port]["dcc_address_range"]
            if dccaddress in range(dcc_address_range[0],dcc_address_range[1]):
                #address_int=int(dccaddress)
                command = "@ {:03} {:02} {:02}".format(dccaddress,channel,activate)
                logging.debug ("send_com_to_ARDUINO(%s): %s - %s - %s",port,dccaddress,channel,command)
                
                arduino = self.controller.serial_port_dict[port]["ARDUINO"]
                #arduino=self.controller.arduino
                for c in command:
                    self.controller.send_to_ARDUINO(c,arduino=arduino)
                    time.sleep(0.01)
                c = chr(10)
                self.controller.send_to_ARDUINO(c,arduino=arduino)
                time.sleep(0.01)
        
    def start(self,event=None):
        self.start_process_Z21()
        
    def stop(self,event=None):
        logging.debug ("Z21_Stop")
        self.stop_process_Z21()
        
    def show_key_adress_for_variables(self,text):
        self.add_text_to_textwindow(text)
        
    def show_key_adresses(self,event=None):

        filepath = M08.GetWorkbookPath() + '/' + M02.Ino_Dir_LED + M02.Include_FileName
        try:
            with open (filepath, "r") as myfile:
                self.file_data=myfile.readlines()
        except:
            self.file_data = []
            self.add_text_to_textwindow("Datei: "+filepath + " nicht gefunden")
            return
            
        searchstring1 = "//*** Output Channels ***\n"
        searchstring2 = "#define START_SEND_INPUTS"
        
        varlist_found=False
        
        for line in self.file_data:
            if line==searchstring1:
                varlist_found=True
            if varlist_found:
                if line.startswith(searchstring2):
                    break
                else:
                    self.add_text_to_textwindow(line)
            
            


        
    def add_text_to_textwindow(self,text):
        self.text.insert("end", text)
        self.text.yview("end")        

    def process_Z21(self):

        if self.queue_z21:

            while self.queue_z21.qsize():
                #logging.debug("process_serial: While loop")
                try:
                    #readtext = self.queue.get()
                    d = self.queue_z21.get()
                    readtext = d[0]
                    #self.mainpage.addr = d[1]
                    client = d[1]
                    date_time = datetime.now()
                    d = date_time.strftime("%H:%M:%S")
                    readtext_str = binascii.hexlify(readtext)
                    textmessage = d + "  " + str(readtext_str)
                    #self.add_text_to_textwindow(textmessage)
                    self.slicePacket(client,readtext)
                    #self.add_text_to_textwindow("\n")
                except IOError:
                    pass
            
        if self.monitor_serial:
            self.after(100, self.process_Z21)
        else:
            textmessage = "Z21 Simulator stopped\n"
            self.add_text_to_textwindow(textmessage)

    def connect_all_serial_interfaces(self):
        usez21data = self.getConfigData("UseZ21Data")
        
        if usez21data:
        
            paramconfig_dict = self.controller.MacroParamDef.data.get("Z21Data",{})
            mp_repeat  = paramconfig_dict.get("Repeat","")
            
            for i in range(int(mp_repeat)):
                port = self.controller.getConfigData_multiple("serportname","Z21Data",i)
                dcc_Start =  self.controller.getConfigData_multiple("dcc_start","Z21Data",i)
                dcc_End = self.controller.getConfigData_multiple("dcc_end","Z21Data",i)
                if dcc_Start != "" and dcc_End !="":
                    dcc_adress_range = (int(dcc_Start),int(dcc_End))
                else:
                    dcc_adress_range = (1,9999)
                self.controller.connect_Z21(port,dcc_adress_range)
        else:
            logging.debug("Z21MonitorPage: Connect ARDUINO")
            self.controller.connect()
        self.controller.start_process_serial_all()
            
    def disconnect_all_serial_interfaces(self):
        paramconfig_dict = self.controller.MacroParamDef.data.get("Z21Data",{})
        mp_repeat  = paramconfig_dict.get("Repeat","")
        
        for i in range(int(mp_repeat)):
            port = self.controller.getConfigData_multiple("serportname","Z21Data",i)
            self.controller.disconnect_Z21(port)

    def add_client(self,client,broadcastflags):
        self.client_broadcast_flag_dict.update({client:broadcastflags})
        if broadcastflags & 0b0001:
            self.client_turnout_info_dict.update({client:broadcastflags})
        if broadcastflags & 0b0010:
            self.client_RMBUS_GETDATA_dict.update({client:broadcastflags})
            SerialMonitorPage = self.controller.getFramebyName("SerialMonitorPage")
            SerialMonitorPage.set_check_RMBUS(value=True)

    def remove_client(self,client):
        self.client_broadcast_flag_dict.pop(client,None)
        self.client_turnout_info_dict.pop(client,None)
        self.client_RMBUS_GETDATA_dict.pop(client,None)
        if self.client_RMBUS_GETDATA_dict == {}:
            SerialMonitorPage = self.controller.getFramebyName("SerialMonitorPage")
            SerialMonitorPage.set_check_RMBUS(value=FALSE)
            
    def send_RMBUS_DATA(self,send_data,groupidx=0):
        empty_bytearray = bytearray(12)
        data = bytearray(1)
        #logging.debug("send_RMBUS_DATA")
        data[0] = groupidx
        data.extend(send_data)
        if len(data)<10:
            data.extend(empty_bytearray[len(data):11])
        for info_client in self.client_RMBUS_GETDATA_dict.keys():
            self.EthSend (0x0F, LAN_RMBUS_DATACHANGED, data[0:12], False, client=info_client)
            self.add_text_to_textwindow(" - LAN_RMBUS_DATACHANGED: " + data.hex())
            logging.debug("Z21-Simu: LAN_RMBUS_DATACHANGED: " + data.hex());             
        
    def set_RMBUS_DATA(self,data,groupidx=0):
        data_changed = False
        RMBUS_data_ba = self.RMBUS_DATA_bytearray.get(groupidx,{})
        if RMBUS_data_ba != data:
            data_changed = True
            self.RMBUS_DATA_bytearray[groupidx] = data
            self.send_RMBUS_DATA(data, groupidx=groupidx)
            
    def get_RMBUS_DATA(self,groupidx=0):
        RMBUS_data_ba = self.RMBUS_DATA_bytearray.get(groupidx,{})
        self.send_RMBUS_DATA(RMBUS_data_ba,groupidx=groupidx)
        self.controller.send_to_ARDUINO("?*\n")
        
    def convert_7bit_to_8bit_old(self,data_7bit_str):
        
        # php code from https://prlbr.de/2011/05/7-bit-8-bit-konvertierung/
        if True:
            up = (1, 3, 7, 15, 31, 63, 127)    
            down = (255, 254, 252, 248, 240, 224, 192, 128)        
            output = bytearray()
            carry = 0

            for i in range(0,len(data_7bit_str)):
                # calculate the round number modulo 8
                r = i % 8
                # represent an input byte as a 7-bit integer
                integer =(data_7bit_str[i])
                # add an 8-bit output byte created from the 8 - r bits carry
                # and r bits from the 7-bit integer
                if (r != 0):
                    output.extend((carry | (integer & up[r - 1])).to_bytes(length=1,byteorder="big"))
                    # save the other 7 - r bits of the 7-bit integer as new carry
                carry = (integer << 1) & down[r]
            if carry != 0:
                output.extend(carry.to_bytes(length=1,byteorder="big"))
        else:
            output = data_7bit_str
        return output
    
    def test_convert_7bit_to_8bit(self):
        bytestring = b'\x40\x00'
        print(self.convert_7bit_to_8bit(bytestring))
        bytestring = b'\x00\x40'
        print(self.convert_7bit_to_8bit(bytestring))        
        data_7bit_str=b"\x7F\x7F"
        v8bit_str=self.convert_7bit_to_8bit(data_7bit_str)
        print("test_convert_7bit_to_8bit:",data_7bit_str,v8bit_str)
        
    def convert_7bit_to_8bit(self,bytestring):
        
        result = bytearray()
        countbits = 7
        byte = 0
        for i in range(0, len(bytestring)):
            testbyte = bytestring[i]
            for j in range(7,0,-1):
                    bit = (testbyte >> (j-1)) & 1
                    if countbits==0:
                        byte |= bit << (7)
                        result.append(byte)
                        countbits=7
                        byte=0
                    else:
                        byte |= bit << (7-countbits)
                        countbits-=1
        if countbits != 0:
            result.append(byte)
        #print("convert_7bit_to_8bit: Input:")
        for my_byte in bytestring:
            print(f'{my_byte:0>8b}', end=' ')
        #print(" Output:")    
        for my_byte in result:
            print(f'{my_byte:0>8b}', end=' ')
        #print("\n")
        return bytes(result)

    
    def notifyZ21_RMBUS_DATA(self, json_data_str):
        logging.debug("notifyZ21_RMBUS_DATA: %s",json_data_str)
        RMBUS_DATA_dict = json.loads(json_data_str)
        rmbus_7bit_data_str = RMBUS_DATA_dict.get("RMBUS","")
        logging.debug("notifyZ21_RMBUS_DATA 7bit: %s",rmbus_7bit_data_str)
        if len(rmbus_7bit_data_str)==2 and rmbus_7bit_data_str[0]=="?":
            return
        rmbus_data_bytearray = self.convert_7bit_to_8bit(bytearray.fromhex(rmbus_7bit_data_str))
        rmbus_data_str = rmbus_data_bytearray.hex()
        logging.debug("notifyZ21_RMBUS_DATA data_str: %s",rmbus_data_str)
        
        if rmbus_data_str != "":
            group_idx = 0
            data_cnt = len(rmbus_data_str)
            while data_cnt > 0:
                if data_cnt >20:
                    rmbus_data_z21_str = rmbus_data_str[group_idx*20:group_idx*20+20]
                    data_cnt -= 20
                else:
                    rmbus_data_z21_str = rmbus_data_str[group_idx*20:group_idx*20+data_cnt]
                    data_cnt = 0
                    
                rmbus_data_bytearray = bytearray.fromhex(rmbus_data_z21_str)
                self.set_RMBUS_DATA(rmbus_data_bytearray,groupidx=group_idx)
                group_idx += 1
        

    def start_process_Z21(self):
        global ThreadEvent_Z21
        # Datagram (udp) socket
        msg = ""
        try :
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            hostname = socket.gethostname()
            
            ip_address = socket.gethostbyname(hostname)
                      
            self.add_text_to_textwindow("Socket opened: Host " + hostname + " IP-adress " + ip_address + "\n")
            logging.debug ('Socket created: Host' + hostname + " IP-adress " + ip_address)
        except (socket.error, msg) :
            logging.debug ('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            return
        
        # Bind socket to local host and port
        try:
            self.socket.bind((HOST, z21Port))
        except:
            logging.debug ('Bind failed. Error Code : ') #  + str(msg[0]) + ' Message ' + msg[1])
            return

        self.connect_all_serial_interfaces()

        ThreadEvent_Z21 = threading.Event()
        ThreadEvent_Z21.set()
        time.sleep(2)
        ThreadEvent_Z21.clear()
        self.monitor_serial = True
        self.thread = Z21Thread(self.queue_z21,self.socket,self)
        self.thread.start()
        self.process_Z21()

        logging.debug ('Socket bind complete')        
        
        textmessage = "Z21 Simulator started\n"
        self.add_text_to_textwindow(textmessage)            

    def stop_process_Z21(self):
        logging.debug ("Stop_process_Z21")
        global ThreadEvent_Z21
        self.monitor_serial = False
        if ThreadEvent_Z21:
            ThreadEvent_Z21.set()
        logging.debug ("Stop_process_Z21 - disconnect_all_serial_interfaces")
        self.disconnect_all_serial_interfaces()
        logging.debug ("Stop_process_Z21 - reset_z21_data")
        self.reset_z21_data()
        time.sleep(1)
        try:
            logging.debug ("Stop_process_Z21 - socket.close")
            self.socket.close()
        except:
            pass
        
        
    def cancel(self):
        pass
        self.stop_process_Z21()
        
    def connect (self,port):
        pass
        #self.start_process_Z21()
    
    def disconnect (self):
        pass
        #self.stop_process_Z21()

    def EthSend (self,DataLen, Header, dataString,  withXOR, client = None):
        data = bytearray(b"                        ")
            
        data[0] = DataLen & 0xFF
        data[1] = DataLen >> 8
        data[2] = Header & 0xFF
        data[3] = Header >> 8
        data[DataLen - 1] = 0 #	//XOR
    
        if withXOR:
            xorlen=0
        else:
            xorlen=1
    
        for i in range (DataLen-5+xorlen): #Ohne Length und Header und XOR
            if (withXOR):
                data[DataLen-1] = data[DataLen-1] ^ dataString[i]
            data[i+4] = dataString[i]
    
        data_new=data[0:DataLen] 
        self.send_data_to_ETH(data_new,client=client)
    
    def receive_message(self, client, packet): 
        if len(packet) <4:
            logging.debug("ERROR: Packet length")
            return
        
        p3=packet[3]
        p2=packet[2]
        p3s= p3<<8
    
        header = p3s+p2
        header_int=int(header)
    
        #logging.debug("Header: %s %s",header_int,self.z21_code2text_dict.get(header_int,"xx"))     
        data = bytearray(b"                ")
    
        if header == LAN_GET_SERIAL_NUMBER:
            self.add_text_to_textwindow(" - LAN_GET_SERIAL_NUMBER")
            logging.debug("GET_SERIAL_NUMBER");  
            data[0] = z21SnLSB;
            data[1] = z21SnMSB;
            data[2] = 0x00; 
            data[3] = 0x00;
            self.EthSend(0x08, LAN_GET_SERIAL_NUMBER, data, False, client=client) #Seriennummer 32 Bit (little endian)
        elif header == LAN_GET_HWINFO:
            self.add_text_to_textwindow(" - LAN_GET_HWINFO")
            logging.debug("GET_HWINFO"); 
            data[0] = z21HWTypeLSB #HwType 32 Bit
            data[1] = z21HWTypeMSB
            data[2] = 0x00 
            data[3] = 0x00
            data[4] = z21FWVersionLSB #FW Version 32 Bit
            data[5] = z21FWVersionMSB
            data[6] = 0x00 
            data[7] = 0x00
            self.EthSend (0x0C, LAN_GET_HWINFO, data, False, client=client)
        elif header == LAN_LOGOFF:
            self.add_text_to_textwindow(" - LAN_LOGOFF")
            logging.debug("LOGOFF");
        elif header == LAN_GET_CODE: #SW Feature-Umfang der Z21   
            self.add_text_to_textwindow(" - LAN_GET_CODE")
            data[0] = 0x00; #keine Features gesperrt
            self.EthSend (0x05, LAN_GET_CODE, data, False, client=client)
        elif header == LAN_X_Header:
            x_header = packet[4]
            if x_header == LAN_X_GET_SETTING:
                x_get_setting_type = packet[5]
                if x_get_setting_type == 0x21:
                    self.add_text_to_textwindow(" - LAN_X_Header - LAN_X_GET_SETTING - X_GET_VERSION")
                    logging.debug("X_GET_VERSION"); 
                    data[0] = LAN_X_GET_VERSION #;	#X-Header: 0x63
                    data[1] = 0x21 #;	#DB0
                    data[2] = 0x30 #;   #X-Bus Version
                    data[3] = 0x12 #;  #ID der Zentrale
                    self.EthSend (0x09, LAN_X_Header, data, True, client=client)
                elif x_get_setting_type == 0x24:
                    #self.add_text_to_textwindow(" - LAN_X_Header - LAN_X_GET_SETTING - LAN_X_GET_STATUS")
                    #logging.debug("LAN_X_GET_STATUS"); 
                    data[0] = LAN_X_STATUS_CHANGED #	#X-Header: 0x62
                    data[1] = 0x22 #;			#DB0
                    data[2] = 0 #Railpower #;		#DB1: Status
                    self.EthSend (0x08, LAN_X_Header, data, True, client=client)
                elif x_get_setting_type == 0x80:
                    self.add_text_to_textwindow(" - LAN_X_Header - LAN_X_GET_SETTING - X_SET_TRACK_POWER_OFF")
                    logging.debug("X_SET_TRACK_POWER_OFF")
                    self.EthSend (0x07, LAN_X_Header, data, True, client=client)     
                elif x_get_setting_type == 0x81:
                    self.add_text_to_textwindow(" - LAN_X_Header - LAN_X_GET_SETTING - X_SET_TRACK_POWER_ON")
                    logging.debug("X_SET_TRACK_POWER_ON")
                    data[0] = 0x61 #;	#X-Header: 0x63
                    data[1] = 0x01 #;	#DB0
                    self.EthSend (0x07, LAN_X_Header, data, True, client=client)                  
    
            elif x_header == LAN_X_CV_READ:
                if (packet[5] == 0x11):
                    self.add_text_to_textwindow(" - LAN_X_Header - X_CV_READ")
                    logging.debug("X_CV_READ")           
            elif x_header == LAN_X_CV_WRITE: 
                if (packet[5] == 0x12):
                    self.add_text_to_textwindow(" - LAN_X_Header - X_CV_WRITE")
                    logging.debug("X_CV_WRITE") 
            elif x_header == LAN_X_CV_POM: 
                self.add_text_to_textwindow(" - LAN_X_Header - LAN_X_CV_POM")
                logging.debug("LAN_X_CV_POM")
            elif x_header == LAN_X_GET_TURNOUT_INFO:
                self.add_text_to_textwindow(" - LAN_X_Header - X_GET_TURNOUT_INFO")
                logging.debug("X_GET_TURNOUT_INFO ")
                data[0] = 0x43  #X-HEADER
                data[1] = packet[5] #High
                data[2] = packet[6] #Low
                data[3] = 1  #inactive
                #     if (notifyz21AccessoryInfo((packet[5] << 8) + packet[6]) == true):
                #          data[3] = 0x02  #active
                #     else:
                #          data[3] = 0x01  #inactive
                self.EthSend (0x09, LAN_X_Header, data, True, client=client)
            elif x_header == LAN_X_SET_TURNOUT:
                if (packet[7] & 1) == 0:
                    status_str = "Contact 2"
                    ret_value = 1
                    Arduinostate = 0
                else:
                    status_str = "Contact 1"
                    ret_value = 2
                    Arduinostate = 1
                    
                if (packet[7] & 8) == 0:
                    active_str = "deactivate"
                    activate = 0
                else:
                    active_str = "activate"
                    activate = 1
                    
                p5=packet[5]
                p6=packet[6]
                p5s= p5<<8
                
                dccaddress = p5s+p6+1 #Z21 adress start with 0, MobaLEDLib with 1
                
                logging.debug("X_SET_TURNOUT Adr.%s : %s %s-%s",dccaddress, packet[7], status_str,active_str)
                self.add_text_to_textwindow(" - LAN_X_Header - X_SET_TURNOUT Addr:"+ str(dccaddress)+ "-"+ status_str+"-"+active_str)

                data[0] = 0x43  #X-HEADER
                data[1] = packet[5] #High
                data[2] = packet[6] #Low
                data[3] = ret_value
    
                #     if (notifyz21AccessoryInfo((packet[5] << 8) + packet[6]) == true):
                #          data[3] = 0x02  #active
                #     else:
                #          data[3] = 0x01  #inactive
                
                for info_client in self.client_turnout_info_dict.keys():
                    self.EthSend (0x09, LAN_X_Header, data, True, client=info_client)

                
                self.send_command_to_ARDUINO(dccaddress,Arduinostate,activate)
    
                        #endif
                        #bool TurnOnOff = bitRead(packet[7],3);  #Spule EIN/AUS
                #if (notifyz21Accessory) {
                    #notifyz21Accessory((packet[5] << 8) + packet[6], bitRead(packet[7], 0), bitRead(packet[7], 3));
                    #Addresse  	Links/Rechts		Spule EIN/AUS
            elif x_header == LAN_X_SET_STOP:
                self.add_text_to_textwindow(" - LAN_X_Header - X_SET_STOP")
                logging.debug("X_SET_STOP")
            elif x_header == LAN_X_GET_LOCO_INFO:
                if (packet[5] == 0xF0):
                    self.add_text_to_textwindow(" - LAN_X_Header - LAN_X_GET_LOCO_INFO")
                    logging.debug("LAN_X_GET_LOCO_INFO: ")
                    Adr_MSB = packet[6] & 0x3F
                    Adr_LSB = packet[7]
                    data[0] = LAN_X_LOCO_INFO
                    data[1] = Adr_MSB
                    data[2] = Adr_LSB
                    data[3] = 0
                    data[4] = 0
                    data[5] = 0
                    data[6] = 0
                    data[7] = 0
                    data[8] = 0
                    self.EthSend (0x0E, LAN_X_Header, data, True, client=client);                    
    
            elif x_header == LAN_X_SET_LOCO:
                if (packet[5] == LAN_X_SET_LOCO_FUNCTION):
                    self.add_text_to_textwindow(" - LAN_X_Header - LAN_X_SET_LOCO_FUNCTION")
                    logging.debug("LAN_X_SET_LOCO_FUNCTION")
                    Adr_MSB = packet[6] & 0x3F
                    Adr_LSB = packet[7]
                    data[0] = Adr_MSB
                    data[1] = Adr_LSB
                    data[2] = 0
                    data[3] = 0
                    data[4] = 0
                    data[5] = 0
                    data[6] = 0
                    data[7] = 0                    
                    self.EthSend (0x0D, LAN_X_Header, data, True, client=client);                        
                else:
                    self.add_text_to_textwindow(" - LAN_X_Header - X_SET_LOCO_DRIVE")
                    logging.debug("X_SET_LOCO_DRIVE ")
                    Adr_MSB = packet[6] & 0x3F
                    Adr_LSB = packet[7]
                    data[0] = Adr_MSB
                    data[1] = Adr_LSB
                    data[2] = 0
                    data[3] = 0
                    data[4] = 0
                    data[5] = 0
                    data[6] = 0
                    data[7] = 0                            
                    self.EthSend (0x0D, LAN_X_Header, data, True, client=client);                        
            elif x_header ==  LAN_X_GET_FIRMWARE_VERSION:
                self.add_text_to_textwindow(" - LAN_X_Header - X_GET_FIRMWARE_VERSION")
                logging.debug("X_GET_FIRMWARE_VERSION")
                data[0] = 0xF3 #		#identify Firmware (not change)
                data[1] = 0x0A #;		#identify Firmware (not change)
                data[2] = z21FWVersionMSB #;   #V_MSB
                data[3] = z21FWVersionLSB # ;  #V_LSB
                self.EthSend (0x09, LAN_X_Header, data, True, client=client)
    
        elif header == LAN_SET_BROADCASTFLAGS:
            self.add_text_to_textwindow(" - LAN_SET_BROADCASTFLAGS")
            logging.debug("LAN_SET_BROADCASTFLAGS")
            p5=packet[5]
            p4=packet[4]
            p5s= p5<<8
        
            flag = p5s+p4
            flag_int=int(flag)
            
            self.add_client(client,flag)
             
    
        elif header == LAN_GET_BROADCASTFLAGS:
            self.add_text_to_textwindow(" - LAN_GET_BROADCASTFLAGS")
            flag = 0 # getz21BcFlag(addIPToSlot(client, 0x00));
            flag = self.client_broadcast_flag_dict.get(client,0)
            data[0] = flag
            data[1] = flag >> 8
            data[2] = flag >> 16
            data[3] = flag >> 24
            self.EthSend (0x08, LAN_GET_BROADCASTFLAGS, data, false, client=client);
            logging.debug("GET_BROADCASTFLAGS: ")
        elif header == (LAN_GET_LOCOMODE):
            pass
        elif header == (LAN_SET_LOCOMODE):
            pass
        elif header == (LAN_GET_TURNOUTMODE):
            pass
        elif header == (LAN_SET_TURNOUTMODE):
            pass;
        elif header == (LAN_RMBUS_GETDATA):
            logging.debug("RMBUS_GETDATA")
            data[0] = packet[4]
            #data[1] = 0
            #data[2] = 0
            #data[3] = 0
            #data[4] = 0
            #data[5] = 0
            #data[6] = 0
            #data[7] = 0
            #data[8] = 0
            #data[9] = 0
            #data[10] = 0
            #data[11] = 0                    
            #self.EthSend (0x0F, LAN_RMBUS_DATACHANGED, data, False, client=client)
            self.add_text_to_textwindow(" - LAN_RMBUS_GETDATA " + str(data[0]))
            self.get_RMBUS_DATA(data[0])
            
    
        elif header == (LAN_RMBUS_PROGRAMMODULE):
            pass
        elif header == (LAN_SYSTEMSTATE_GETDATA): #System state
            self.add_text_to_textwindow(" - LAN_SYSTEMSTATE_GETDATA")
            logging.debug("LAN_SYSTEMSTATE_GETDATA")
            logging.debug("X_GET_FIRMWARE_VERSION")
            data[0] = 0  # MainCurrent MSB
            data[1] = 0  # MainCurrent LSB
            data[2] = 0  # ProgCurrent MSB
            data[3] = 0  # ProgCurrent LSB
            data[4] = 0  # FilteredMainCurrent MSB
            data[5] = 0  # FilteredMainCurrent LSB
            data[6] = 0  # Temperatur MSB
            data[7] = 0  # Temperatur LSB
            data[8] = 0  # SupplyVoltage MSB
            data[9] = 0  # SupplyVoltage LSB
            data[10] = 0 # VCC Voltage MSB 
            data[11] = 0 # VCCVoltage MSB
            data[12] = 0 # CentralState
            data[13] = 0 # CentralStateEx
            data[14] = 0 # Reserve
            data[15] = 0 # Reserve
  
            self.EthSend (0x14, LAN_SYSTEMSTATE_DATACHANGED, data, False, client=client)            
            
        elif header ==  (LAN_RAILCOM_GETDATA):
            logging.debug ("LAN_RAILCOM_GETDATA")
        elif header ==  (LAN_LOCONET_FROM_LAN): 
            logging.debug("LOCONET_FROM_LAN") 
        elif header ==  (LAN_LOCONET_DISPATCH_ADDR):
            logging.debug("LOCONET_DISPATCH_ADDR ")
        elif header == (LAN_LOCONET_DETECTOR):
            logging.debug("LOCONET_DETECTOR Abfrage")
        elif header == (LAN_CAN_DETECTOR):
            logging.debug("CAN_DETECTOR Abfrage")
        elif header == (0x12): #	#configuration read
            logging.debug("Configuration read")
        elif header == (0x13): # configuration write
            logging.debug("Configuration write")
        elif header == (0x16):  #configuration read
            logging.debug("Configuration read")
        elif header == (0x17): #	#configuration write
            logging.debug("Configuration write")
        else:
            logging.debug("UNKNOWN_COMMAND"); 
    
    def handleMessage_lan_x_loco_info(self,message):
        if message[2] !=  0x40 or message[4] != 0xEF:
            logging.debug(str(message))
            header = message[2]
            header_int=int(header)
            logging.debug("Header: %s %s",header_int,z21_code2text_dict.get(header_int,"xx"))
            return
        logging.debug('LAN_X_LOCO_INFO message received')
        db = message[5:]
        # address
        address = int.from_bytes(db[0:2], byteorder = 'big')
        logging.debug('Address: %s', address)
        # direction
        direction = db[3] & 0b10000000
        if direction != 0:
            logging.debug('Direction: forward')
        else:
            logging.debug('Direction: backward')
        # speed
        speed = db[3] & 0b01111111
        logging.debug('Speed: %s', speed)
        # speed steps
        speedSteps = db[2] & 0b00000111
        if speedSteps == 4:
            logging.debug('Speed steps: 128')
        elif speedSteps == 2:
            logging.debug('Speed steps: 28')
        else:
            logging.debug('Speed steps: 14')
        # F0
        f0 = db[4] & 0b00010000
        if f0 != 0:
            logging.debug('F0 (main lights): ON')
        else:
            logging.debug('F0 (main lights): OFF')
    
    def slicePacket(self,client,data):
        while len(data) > 0:
            dataLen = int.from_bytes(data[0:2], byteorder='little')
            if dataLen == 0:
                data = data[2:]
            else:
                self.receive_message(client,data[0:dataLen])
                #handleMessage(data[0:dataLen])
                data = data[dataLen:]
    
    def send_data_to_ETH(self, data,client=None):
        if client == None:
            client = self.addr
        bytessend = self.socket.sendto(data , client)
        data_str = binascii.hexlify(data)
        #logging.debug("Senddata %s %s %s",bytessend,data_str,client)  


class Z21Thread(threading.Thread):
    def __init__(self, p_queue, p_socket,mainpage):
        #global serialport
        threading.Thread.__init__(self)
        self.queue_z21 = p_queue
        self.socket = p_socket
        self.mainpage = mainpage

    def run(self):
        #global serialport
        logging.debug("Z21Thread started")
        if self.socket:

            #now keep talking with the client
            while not ThreadEvent_Z21.is_set() and self.socket:
                self.socket.settimeout(1)
                try:
                    d = self.socket.recvfrom(1024)
                except (socket.timeout,ConnectionResetError):
                    #print("Timeout")
                    continue
                data = d[0]
                self.mainpage.addr = d[1]
                data_str = binascii.hexlify(data)
                #logging.debug('Z21 Received Message[' + self.mainpage.addr[0] + ':' + str(self.mainpage.addr[1]) + '] - ' + str(data_str)+"]")
                #print ('Z21 Received Message[' + self.mainpage.addr[0] + ':' + str(self.mainpage.addr[1]) + '] - ' + str(data_str))
                
                try:
                    self.queue_z21.put(d)
                except:
                    pass
                
                #logging.debug("Z21 Thread got message: %s", data_str)                     

            #self.socket.close()            
 
        logging.debug("Z21 Thread received event. Exiting")

