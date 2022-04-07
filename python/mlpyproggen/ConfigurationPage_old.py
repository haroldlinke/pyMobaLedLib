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

from tkcolorpicker.spinbox import Spinbox
from tkcolorpicker.limitvar import LimitVar
import serial.tools.list_ports as portlist
from scrolledFrame.ScrolledFrame import VerticalScrolledFrame,HorizontalScrolledFrame,ScrolledFrame


from locale import getdefaultlocale
import logging
import serial
import time
import platform

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
# Class ConfigurationPage
# ----------------------------------------------------------------

class ConfigurationPage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        self.arduino_portlist = {}
        tk.Frame.__init__(self,parent)
        self.tabClassName = "ConfigurationPage"
        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName)

        self.startcmd_filename = ""
        
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
        
        #self.scroll_configframe = VerticalScrolledFrame(self.main_frame)
        
        #config_frame = self.controller.create_macroparam_frame(self.scroll_configframe.interior,self.tabClassName, maxcolumns=1,startrow =10,style="CONFIGPage")        
        config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=1,startrow =10,style="CONFIGPage")  
        # --- Buttons
        button_frame = ttk.Frame(self.main_frame)
#
        button1_text = macrodata.get("Button_1",self.tabClassName)
        button2_text = macrodata.get("Button_2",self.tabClassName)
        button3_text = macrodata.get("Button_3",self.tabClassName)
        
        self.update_button = ttk.Button(button_frame, text=button1_text, command=self.save_config)
        self.update_button.pack(side="right", padx=10)
        
        # --- start cmd checkbox and file selection
        startcmd_frame = ttk.Frame(self.main_frame, relief="ridge", borderwidth=2)
        
        self.s_startcmdcbvar = tk.IntVar()
        self.s_startcmdcb = ttk.Checkbutton(startcmd_frame,text=button2_text,variable=self.s_startcmdcbvar,onvalue = 1, offvalue = 0, command=self.startcmd)
        self.s_startcmdcb.grid(sticky='w', padx=4, pady=4, row=0,column=0)
        self.s_startcmdcbvar.set(self.getConfigData("startcmdcb"))
        
        self.startcmd_filename = self.getConfigData("startcmd_filename")
        self.startcmd_button = ttk.Button(startcmd_frame, text=button3_text,width=30, command=self.askselectfile)
        self.startcmd_button.grid(row=0,column=1, padx=4, pady=4,sticky="w")
        self.startcmd_label = tk.Label(startcmd_frame, text=self.startcmd_filename,width=120,height=1,wraplength=700)
        self.startcmd_label.grid(row=1,column=0,columnspan=2,padx=4, pady=4,sticky="w")

        # --- placement
        # Tabframe
        self.frame.grid(row=0,column=0)
        self.scroll_main_frame.grid(row=0,column=0,sticky="nesw")
        # scroll_main_frame
        self.main_frame.grid(row=0,column=0)
        # main_frame        
        title_frame.grid(row=0, column=0, pady=10, padx=10)
        button_frame.grid(row=1, column=0,pady=10, padx=10)
        config_frame.grid(row=2, column=0, pady=10, padx=10, sticky="nesw")
        startcmd_frame.grid(row=3, column=0, pady=10, padx=10, stick="ew")
        

        macroparams = macrodata.get("Params",[])
        
        for paramkey in macroparams:
            paramconfig_dict = self.controller.MacroParamDef.data.get(paramkey,{})
            param_type = paramconfig_dict.get("Type","")
            if param_type == "Multipleparams":
                mparamlist = paramconfig_dict.get("MultipleParams",[])
                mp_repeat  = paramconfig_dict.get("Repeat","")
                if mp_repeat == "":
                    for mparamkey in mparamlist:
                        configdatakey = self.controller.getConfigDatakey(mparamkey)
                        value = self.getConfigData(configdatakey)
                        self.controller.set_macroparam_val(self.tabClassName, mparamkey, value)
                else:
                    # get the repeated multipleparams rep_mparamkey=macro.mparamkey.index (e.g. ConfigDataPage.Z21Data.0
                    for i in range(int(mp_repeat)):
                        for mparamkey in mparamlist:
                            configdatakey = self.controller.getConfigDatakey(mparamkey)
                            value = self.controller.getConfigData_multiple(configdatakey,paramkey,i)
                            mp_macro = self.tabClassName+"." + paramkey + "." + str(i)
                            self.controller.set_macroparam_val(mp_macro, mparamkey, value)
            else:
                configdatakey = self.controller.getConfigDatakey(paramkey)
                value = self.getConfigData(configdatakey)
                self.controller.set_macroparam_val(self.tabClassName, paramkey, value)

        # ----------------------------------------------------------------
        # Standardprocedures for every tabpage
        # ----------------------------------------------------------------

    def tabselected(self):
        #self.controller.currentTabClass = self.tabClassName
        #self.ledmaxcount.set(self.controller.get_maxLEDcnt())
        logging.debug("Tabselected: %s",self.tabname)
        self.store_old_config()
        self.controller.disconnect()
        if self.arduino_portlist == {}:
            logging.debug("Create Portlist")
            self.comports=portlist.comports(include_links=False)
            self.old_ports=[]
            conarduino_str = ""
            for comport in self.comports:
                logging.debug("Portlist.ComPorts:"+comport[0]+" "+comport[1]+" "+comport[2])
                if self.check_string(comport[1],["ARDUINO","CH340","USB Serial Port","ttyACM","USB"]):
                    portlist_data = self.arduino_portlist.get(comport[0],{})
                    if portlist_data == {}:
                        self.arduino_portlist[comport[0]]={
                                                "Description"    : comport[1],
                                                "Baudrate"       : "???",
                                                "DeviceSignature": "???",
                                                "Status"         : "unchecked"
                                                }
                    else:
                        portlist_data["Description"]     = comport[1]
                        portlist_data["Baudrate"]        = "???"
                        portlist_data["DeviceSignature"] = "???"
                        portlist_data["Status"]          = "unchecked"
        
        self.update_ARDUINO_data(update_comport=True)
        
        # bind update of Comport combobox to event
        combobox_var = self.controller.macroparams_var["ConfigurationPage"]["ARDUINO Port"]
        
        combobox_var.bind("<<ComboboxSelected>>",self.on_comport_value_changed)
        
        self.controller.set_macroparam_val(self.tabClassName, "ARDUINOMessage", "Erkennung der ARDUINOs ...",disable=True)
        logging.debug(repr(self.arduino_portlist))
        self.monitor_arduino_ports = True
        self.after(200,self.on_update_ARDUINO_data)
    
    def tabunselected(self):
        logging.debug("Tabunselected: %s",self.tabname)
        self.monitor_arduino_ports = False
        self.blink_ARDUINO = ""
        if self.check_if_config_data_changed():
            answer = tk.messagebox.askyesnocancel ('Sie verlassen die Einstellungen','Die Daten wurden verändert. Sollen die Daten gesichert werden?',default='no')
            if answer == None:
                return # cancelation return to "ConfigurationOage"
            if answer:
                self.save_config()
       
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
    
    def connect (self):
        pass
    
    def disconnect (self):
        pass    
    

    # ----------------------------------------------------------------
    # ConfigurationPage save_config
    # ----------------------------------------------------------------
    
    DeviceSignature2Chip_dict={
    b'\x1E\x90\x07':"ATtiny13",
    b'\x1E\x91\x0A':"ATtiny2313",
    b'\x1E\x92\x0A':"ATmega48P",
    b'\x1E\x93\x07':"ATmega8",
    b'\x1E\x94\x06':"ATmega168",
    b'\x1E\x95\x02':"ATmega32",
    b'\x1E\x95\x0F':"ATmega328P (Nano/Uno)",
    b'\x1E\x95\x14':"ATmega328-PU",
    b'\x1E\x96\x02':"ATmega64",
    b'\x1E\x96\x09':"ATmega644",
    b'\x1E\x97\x02':"ATmega128",
    b'\x1E\x97\x03':"ATmega1280",
    b'\x1E\x98\x01':"ATmega2560"}
    
    def on_comport_value_changed(self,event):
        combobox_var = event.widget
        port = combobox_var.get()
        logging.debug("Comport_value_changed %s", port)
        
        takeover = self.controller.get_macroparam_val("ConfigurationPage","ARDUINOTakeOver")
        
        if takeover:
            # set boardtype and baudrate
            portdata = self.arduino_portlist.get(port,{})
            if portdata != {}:
                baudrate = portdata.get("Baudrate","115200")
                if baudrate !=0:
                    self.controller.set_macroparam_val("ConfigurationPage","ARDUINO Baudrate",baudrate)
                    if baudrate == "115200":
                        self.controller.set_macroparam_val("ConfigurationPage","ARDUINO Type",1)
                    else:
                        self.controller.set_macroparam_val("ConfigurationPage","ARDUINO Type",0)
        self.blink_ARDUINO = port
        self.after(200,self.on_blink_arduino_led)
                        
    def on_blink_arduino_led(self):
        arduino_blick_cb = self.controller.get_macroparam_val("ConfigurationPage","ARDUINOBlink")
        if self.blink_ARDUINO != "" and arduino_blick_cb==1:
            portdata = self.arduino_portlist.get(self.blink_ARDUINO,{})
            if portdata != {}:
                baudrate = portdata.get("Baudrate","0") 
                if baudrate in ["115200","57600"]: # check if device is an ARDUINO
                    Baudrate = 50
                    Res, DeviceSignatur = self.Get_Arduino_Baudrate(self.blink_ARDUINO, Start_Baudrate=Baudrate,trials=1)
                    self.after(2000,self.on_blink_arduino_led)
        
    def determine_new_and_removed_ports(self,updated_comports_list):
        removed_ports_list = []
        new_ports_list = []
        show_entry = self.controller.get_macroparam_val("ConfigurationPage","ARDUINOShowAll")
        # check for removed ports
        for port in self.old_ports:
            port_found=False
            for comport in updated_comports_list:
                if not show_entry:
                    check_entry = self.check_string(comport[1],["ARDUINO","CH340","USB Serial Port","ttyACM","USB"])                
                if port == comport[0] and (show_entry or check_entry):
                    port_found = True
                    break
            if not port_found:
                removed_ports_list.append(port)
        
        # check for new ports        
        for comport in updated_comports_list:
            port = comport[0]
            if not port in self.old_ports:
                
                if not show_entry:
                    check_entry = self.check_string(comport[1],["ARDUINO","CH340","USB Serial Port","ttyACM","USB"])
                if show_entry or check_entry:
                    new_ports_list.append(port)
                    self.arduino_portlist[port]={
                                            "Description"    : comport[1],
                                            "Baudrate"       : "???",
                                            "DeviceSignature": "???",
                                            "Status"         : "unchecked"
                                           }
        if new_ports_list != []:
            logging.debug("determine_new_and_removed_ports %s",repr(new_ports_list))
        if removed_ports_list != []:
            logging.debug("determine_new_and_removed_ports %s",repr(removed_ports_list))            

        return new_ports_list,removed_ports_list

    def update_ARDUINO_data(self,update_comport=False):
        conarduino_str = ""
        ARDUINO_port = self.controller.get_macroparam_val("ConfigurationPage","ARDUINO Port")
        new_ARDUINO_port = "NO DEVICE"
        port_found=False
        for port in sorted(self.arduino_portlist.keys()):
            port_data = self.arduino_portlist[port]
            conarduino_str += port + " " + port_data["Description"] + " Baudrate:" + port_data["Baudrate"] + " " + self.DeviceSignature2Chip_dict.get(port_data["DeviceSignature"],"unknown device") +"\n"
            if not port_data["Baudrate"] in ["???","0"]:
                new_ARDUINO_port = port
                if port == ARDUINO_port:
                    port_found=True
        if port_found:
            new_ARDUINO_port = ARDUINO_port
        self.controller.set_macroparam_val(self.tabClassName, "ARDUINOConnected", conarduino_str,disable=True)
        
        takeover = self.controller.get_macroparam_val("ConfigurationPage","ARDUINOTakeOver")
        if takeover and update_comport:
            comport_valuelist = sorted(self.arduino_portlist.keys())
            comport_valuelist[:0] = ["NO DEVICE"]
            self.controller.update_combobox_valuelist("ConfigurationPage","ARDUINO Port",comport_valuelist,value=new_ARDUINO_port)
            
            paramconfig_dict = self.controller.MacroParamDef.data.get("Z21Data",{})
            mp_repeat  = paramconfig_dict.get("Repeat","")
            for i in range(int(mp_repeat)):            
                self.controller.update_combobox_valuelist("ConfigurationPage.Z21Data.{:1}".format(i),"ARDUINO Port",comport_valuelist,value="")

            
            portdata = self.arduino_portlist.get(new_ARDUINO_port,{})
            if portdata != {}:
                baudrate = portdata.get("Baudrate","115200")
                if baudrate !=0:
                    self.controller.set_macroparam_val("ConfigurationPage","ARDUINO Baudrate",baudrate)
                    if baudrate == "115200":
                        self.controller.set_macroparam_val("ConfigurationPage","ARDUINO Type",1)
                    else:
                        self.controller.set_macroparam_val("ConfigurationPage","ARDUINO Type",0)            
    
    def on_update_ARDUINO_data(self):
        if self.monitor_arduino_ports:
            temp_comports_list=portlist.comports(include_links=False)
            
            new_ports_list,removed_ports_list = self.determine_new_and_removed_ports(temp_comports_list)
            
            # delete ports not in ports_list anymore
            for port in removed_ports_list:
                logging.debug("Port %s delete from ARDUINO portlist",port)
                del self.arduino_portlist[port]
                self.old_ports.remove(port)
            
            for port in new_ports_list:
                logging.debug("Try to add Port %s to ARDUINO portlist",port)
                self.controller.set_macroparam_val(self.tabClassName, "ARDUINOMessage", "Teste Port: "+port+ "...",disable=True)
                self.controller.update()
                
                baudrate, DeviceSignature = self.Get_Arduino_Baudrate(port)
                
                portlist_data = self.arduino_portlist.get(port,{})
                if portlist_data == {}:
                    self.arduino_portlist[port]={
                                            "Description"    : port,
                                            "Baudrate"       : str(baudrate),
                                            "DeviceSignature": DeviceSignature,
                                            "Status"         : "new"
                                           }
                else:
                    #portlist_data["Description"]     = port
                    portlist_data["Baudrate"]        = str(baudrate)
                    portlist_data["DeviceSignature"] = DeviceSignature
                    portlist_data["Status"]          = "new"

                self.old_ports.append(port)
                break
    
            if removed_ports_list!=[] or new_ports_list!=[]:
                update_comport = len(new_ports_list)==1 or removed_ports_list != []
                self.update_ARDUINO_data(update_comport=update_comport)
            
            if new_ports_list!=[]:
                if self.monitor_arduino_ports:
                    self.after(100,self.on_update_ARDUINO_data)
                self.controller.set_macroparam_val(self.tabClassName, "ARDUINOMessage", "ARDUINO Erkennung ... ",disable=True)   
            else:
                if self.monitor_arduino_ports:
                    self.after(1000,self.on_update_ARDUINO_data)
                self.controller.set_macroparam_val(self.tabClassName, "ARDUINOMessage", "ARDUINO Erkennung beendet",disable=True)
                
    def check_string(self,string, substring_list):
        for substring in substring_list:
            if substring.upper() in string.upper():
                return True
        return False
    
    def Get_Arduino_Baudrate(self,ComPort,Start_Baudrate=1,trials=4):
        # Return  >0: Baudrate 57600/115200
        #          0: if no arduino is detected
        #         -1: can't open com port => used by an other program ?
        #         -2: can't create com port file
        #         -3: can't reset arduino
        # DeviceSignature
        
        if Start_Baudrate == 1:
            Baudrate = 115200
        elif Start_Baudrate == 2:
            Baudrate = 57600
        else:
            Baudrate = Start_Baudrate
        #if not Baudrate in [115200,57600]: Baudrate = 115200
        
        for i in range(trials):
            logging.debug("Trying COM %s with Baudrate %s",ComPort,Baudrate)
            Res, DeviceSignatur = self.detect_arduino(ComPort, Baudrate,No_of_trials=int(trials/2)) 
            if Res == 1: # Arduino detected
                logging.debug("  Serial Port     : %s",ComPort)
                logging.debug("  Serial Baudrate : %s",Baudrate)
                logging.debug("  Device signature: %s",DeviceSignatur)
                if DeviceSignatur == b'\x1E\x95\x0F': logging.debug("ATMega328P")
                logging.debug("Device: %s - %s",DeviceSignatur,self.DeviceSignature2Chip_dict.get(DeviceSignatur,"unknown device"))
                return Baudrate, DeviceSignatur
            elif Res == 0:
                logging.debug("%s:no ARDUINO detected, baudrate: %s",ComPort, Baudrate)
                pass
            elif Res == -1:
                DeviceSignatur = "can't open com port"
                logging.debug("%s:%s, baudrate: %s",ComPort, DeviceSignatur, Baudrate)
                return Res, DeviceSignatur
            elif Res == -2:
                DeviceSignatur = "can't create com port file" # should never happen
                logging.debug("%s:%s, baudrate: %s",ComPort, DeviceSignatur, Baudrate)
                return Res, DeviceSignatur
            elif Res == -3:
                DeviceSignatur = "can't reset ARDUINO" # should never happen
                logging.debug("%s:%s, baudrate: %s",ComPort, DeviceSignatur, Baudrate)
                return Res, DeviceSignatur                
            else: 
                logging.debug("%s:unkonw ERROR, baudrate: %s",ComPort, Baudrate)
                return Res, b"unknown ERROR "
            if Baudrate == 115200: 
                Baudrate=57600
            else: 
                Baudrate=115200 #Check again with the other baudrate
        return 0, b''
        
    
    def transact(self,bytemessage,nNumberOfBytesToRead=10):
        
        #clear outputbuffer
        bytemessage += Sync_CRC_EOP
        #self.controller.arduino.reset_input_buffer()
        #self.controller.arduino.reset_output_buffer()                   
        #self.controller.arduino.cancel_read()
        #self.controller.arduino.cancel_write()
            
        # write message to serport
        nbytes_written = self.controller.arduino.write(bytemessage)
        if nbytes_written != len(bytemessage):
            logging.debug("ERROR write to ARDUINO")
            return b''
        no_of_trials=2
        for i in range (no_of_trials):
            # read from serport nNumberOfBytesToRead
            read_data = self.controller.arduino.read(size=nNumberOfBytesToRead)
            logging.debug("transact: %s",read_data)
            if (read_data[:1] == Resp_STK_INSYNC and read_data[-1:] == Resp_STK_OK) or read_data[-1:] == Resp_STK_FAILED:
            # return response
                logging.debug("transact data_ok: %s",read_data)
                return read_data
        return b''
    
    def getdeviceinformation(self):
        logging.debug("getdeviceinformation")
        DeviceSignatur = b''
        HWVersion = b''
        SWMajorVersion  = b''
        SWMinorVersion  = b''
        Data = self.transact(STK_READ_SIGN, 5)
        if len(Data)==5:
            if Data[4].to_bytes(1,byteorder="little") == Resp_STK_OK:
                DeviceSignatur = Data[1:4]
                logging.debug("getdeviceinformation: %s",str(DeviceSignatur))
                if DeviceSignatur == b'\x1E\x95\x0F':
                    logging.info("ATMEGA328P")
        
        #Data = self.transact(Cmnd_STK_GET_PARAMETER + Parm_STK_HW_VER, 3)
        #if len(Data)==3:
        #    if Data[2].to_bytes(1,byteorder="little") == Resp_STK_OK:
        #        HWVersion = Data[1]
        #Data = self.transact(Cmnd_STK_GET_PARAMETER + Parm_STK_SW_MAJOR, 3)
        #if len(Data)==3:
        #    if Data[2].to_bytes(1,byteorder="little") == Resp_STK_OK:
        #        SWMajorVersion = Data[1]
        #Data = self.transact(Cmnd_STK_GET_PARAMETER + Parm_STK_SW_MINOR, 3)
        #if len(Data)==3:
        #    if Data[2].to_bytes(1,byteorder="little") == Resp_STK_OK:
        #        SWMinorVersion = Data[1]
        #logging.debug("DeviceSignatur: %s, HWVersion: %s, SW_Major_Version: %s SW_Minor_Version: %s",DeviceSignatur,HWVersion,SWMajorVersion,SWMinorVersion)
        return DeviceSignatur

    
    def detect_arduino(self,port,baudrate,No_of_trials=2):
        # protocol see application note 1AVR061 here http://ww1.microchip.com/downloads/en/Appnotes/doc2525.pdf
        # Result:  1: O.K
        #          0: Give up after n trials => if no arduino is detected
        #         -1: can't open com port
        #         -2: can't close and assign port
        #         -3: can't reset arduino
        
        logging.debug ("detect_arduino:",port)
        no_port=None
        try: # close the port if it is open and reopen it with DTR = False
            if self.controller.arduino and self.controller.arduino.is_open:
                self.controller.arduino.close()
            self.controller.arduino = serial.Serial(no_port,baudrate=baudrate,timeout=0.2,write_timeout=1,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
            #logging.info("connected to: " + self.controller.arduino.port)
        except BaseException as e:
            logging.debug(e)
            logging.debug("detect_arduino: Error assigning port")
            return -2, None
        self.controller.arduino.port = port
        self.controller.arduino.dtr = False
        try:
            self.controller.arduino.open()
        except BaseException as e:
            logging.debug(e)            
            logging.debug("detect_arduino: Error opening  port")
            return -1, None           
        try:
            self.controller.arduino.dtr = True
            time.sleep(0.250)
            self.controller.arduino.dtr = False
        except BaseException as e:
            logging.debug(e)                 
            logging.debug("Error, reset ARDUINO")
            return -3, None
    
        # now get in sync
        message = Cmnd_STK_GET_SYNC
        
        sucessful=False
        
        for i in range (No_of_trials):
            message = self.transact(Cmnd_STK_GET_SYNC,2)
            
            if message == Resp_STK_INSYNC + Resp_STK_OK:
                devicesignatur = self.getdeviceinformation()
                self.controller.arduino.close()
                return 1, devicesignatur
        if not sucessful:
            logging.debug("Give up after %s trials",No_of_trials)
        return 0, None


    def save_config(self):
        self.setConfigData("pos_x",self.winfo_x())
        self.setConfigData("pos_y",self.winfo_y())
        #self.setConfigData("serportnumber", self.combo.current())
        #self.setConfigData("serportname", self.combo.get())
        
        #self.setConfigData("maxLEDcount", self.s_ledmaxcount.get())
        #self.controller.set_maxLEDcnt(self.s_ledmaxcount.get())
        
        #self.setConfigData("colorview", self.comboview.current())

        #self.setConfigData("wheeldir", self.combodir.current())
        #self.setConfigData("startpage", "-1") # not used anymore
        #startindex = self.combopage.current()
        #startpagename = self.controller.getStartPageName(startindex)
        #self.setConfigData("startpagename", startpagename)
        
        #self.setConfigData("baudrate", self.comboBd.get())
        
        #self.setConfigData("led_correction_r", self.cs_red.get())
        #self.setConfigData("led_correction_g", self.cs_green.get())
        #self.setConfigData("led_correction_b", self.cs_blue.get())
        
        self.setConfigData("startcmd_filename", self.startcmd_filename)
        
        param_values_dict = self.get_macroparam_var_values(self.tabClassName)
        
        self.setConfigDataDict(param_values_dict)
        
        self.store_old_config()
        self.controller.SaveConfigData()
        
        logging.debug("SaveConfig: %s - %s",self.tabname,repr(self.controller.ConfigData.data))

    def store_old_config(self):
        self.old_startcmd_filename = self.startcmd_filename
        self.old_param_values_dict = self.get_macroparam_var_values(self.tabClassName)
    
    def check_if_config_data_changed(self):
        
        if self.old_startcmd_filename != self.startcmd_filename:
            return True
        param_values_dict = self.get_macroparam_var_values(self.tabClassName)
        if self.old_param_values_dict != param_values_dict:
            return True
        return False
                
                


    # ----------------------------------------------------------------
    # ConfigurationPage _update_led_count
    # ----------------------------------------------------------------

    def _update_led_count(self, event=None):
        if event is None or event.widget.old_value != event.widget.get():
            maxledcount = self.s_ledmaxcount.get()

    def autocn(self,event=None):
        if self.s_autocnvar.get() == 1:
            self.setConfigData("autoconnect", True)
        else:
            self.setConfigData("autoconnect", False)
            
    def startcmd(self,event=None):
        if self.s_startcmdcbvar.get() == 1:
            self.setConfigData("startcmdcb", True)
        else:
            self.setConfigData("startcmdcb", False)    
            
    def _update_cor_rgb(self, event=None):
        """Update display after a change in the RGB spinboxes."""
        if event is None or event.widget.old_value != event.widget.get():
            self.setConfigData("led_correction_r", self.cs_red.get())
            self.setConfigData("led_correction_g", self.cs_green.get())
            self.setConfigData("led_correction_b", self.cs_blue.get())
            
    def askselectfile(self):
        self.startcmd_filename = tk.filedialog.askopenfilename()
        system_platform = platform.platform()
        macos = "macOS" in system_platform
        macos_fileending = "/Contents/MacOS/Arduino" 
        if macos:
            logging.debug("This is a MAC")
            if not self.startcmd_filename.endswith(macos_fileending):
                self.startcmd_filename = self.startcmd_filename + "/Contents/MacOS/Arduino"        
        self.startcmd_label.configure(text=self.startcmd_filename)
    


