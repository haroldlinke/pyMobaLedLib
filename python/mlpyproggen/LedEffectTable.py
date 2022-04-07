# -*- coding: utf-8 -*-
#
#         MobaLedCheckColors: Color checker for WS2812 and WS2811 based MobaLedLib
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
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# *
# ***************************************************************************

import tkinter as tk
from tkinter import ttk,messagebox,filedialog
#from mlpyproggen.configfile import ConfigFile
#from mlpyproggen.dictFile import readDictFromFile, saveDicttoFile
#from mlpyproggen.ConfigurationPage import ConfigurationPage
#from mlpyproggen.SerialMonitorPage import SerialMonitorPage
#from mlpyproggen.ColorCheckPage import ColorCheckPage
#from mlpyproggen.EffectTestPage import EffectTestPage
#from mlpyproggen.EffectMacroPage import EffectMacroPage
#from mlpyproggen.LEDListPage import LEDListPage
#from mlpyproggen.SoundCheckPage import SoundCheckPage
#from mlpyproggen.tooltip import Tooltip
from mlpyproggen.DefaultConstants import SETMACRO_LIST, SWITCHMACROLIST, SingleEffectHandling_Tbl, EFFECT_LED_CHANNELS_LIST, EFFECT_LED_STARTLED_LIST,SIZEFACTOR

import json
from locale import getdefaultlocale
#import os
#import serial
#import sys
#import threading
#import queue
#import time
import logging
import re
#import webbrowser
#from datetime import datetime


# --- Translation - not used
EN = {}
FR = {}
DE = {}

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

MAXLED = 256*3-1


class RightClickMenu(tk.Frame):   
    def __init__(self, parent, ledlabel, mainpage):
        self.master = parent
        self.mainpage = mainpage
        tk.Frame.__init__(self, self.master)  
        self.ledlabel = ledlabel
        self.create_widgets()

    def create_widgets(self):
        self.create_right_click_menu()       

    def create_right_click_menu(self):
        self.right_click_menu = tk.Menu(self.master, tearoff=0, relief='sunken')
        self.right_click_menu.add_command(label="Kopieren", command=self.copy_leds)
        self.right_click_menu.add_command(label="Ausscheiden", command=self.cut_leds)
        self.right_click_menu.add_command(label="Einfügen", command=self.paste_leds)        
        self.right_click_menu.add_separator()
        
        self.right_click_menu.add_command(label="Daten löschen", command=self.delete_entry)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Anschlüße entfernen", command=self.remove_leds)
        self.right_click_menu.add_command(label="Anschlüße einfügen", command=self.insert_leds)
        self.right_click_menu.add_command(label="Als letzte LED markieren", command=self.mark_lastled)

        #self.right_click_menu.add_separator()
        
        #self.right_click_menu.add_command(label="LED Typ: RGB", command=self.setLEDtypeRGB)
        #self.right_click_menu.add_command(label="LED Typ: Single", command=self.setLEDtypeSingle)
        

    def popup_text(self, event):
        self.right_click_menu.post(event.x_root, event.y_root)


    def insert_leds(self):
        label = self.ledlabel #event.widget
        keyint = int(label.key)
        n = self.mainpage.ledcount_int
        self.mainpage.controller.ledeffecttable_insert_leds(keyint,n)
        self.mainpage.update_ledtable_complete()

    def remove_leds(self):
        label = self.ledlabel #event.widget
        keyint = int(label.key)
        n = self.mainpage.ledcount_int
        self.mainpage.controller.ledeffecttable_remove_leds(keyint,n)
        self.mainpage.update_ledtable_complete()
        
    def copy_leds(self):
        label = self.ledlabel #event.widget
        keyint = int(label.key)
        n = self.mainpage.ledcount_int
        start_idx = self.mainpage.lednum_int
        self.mainpage.controller.ledeffecttable.copy_leds_to_clipboard(start_idx,n)
        
    
    def cut_leds(self):
        label = self.ledlabel #event.widget
        keyint = int(label.key)
        n = self.mainpage.ledcount_int
        start_idx = self.mainpage.lednum_int
        self.mainpage.controller.ledeffecttable.copy_leds_to_clipboard(start_idx,n,copytype="cut")
        
        
    def paste_leds(self):
        label = self.ledlabel #event.widget
        keyint = int(label.key)
        n = self.mainpage.ledcount_int
        
        self.mainpage.controller.ledeffecttable.paste_leds_from_clipboard(keyint)
        self.mainpage.update_ledtable_complete()       
    
    def delete_entry(self):
        label = self.ledlabel #event.widget
        keystr = label.key
        keyint = int(keystr)
        selectedareabegin = int(self.mainpage.lednum.get())
        n = self.mainpage.ledcount_int
        selectedareaend = keyint+n-1
        
        if keyint in range(selectedareabegin,selectedareaend):
            curkeyint = selectedareabegin
        else:
            curkeyint = keyint
            n=1
       
        self.mainpage.controller.ledeffecttable_init_entries(curkeyint,n)        
        self.mainpage.update_ledtable_complete()

    def menuUndo(self):
        mainpage = self.mainpage
        mainpage.MenuUndo()
        
    def setLEDtypeRGB(self):
        label = self.ledlabel #event.widget
        keystr = label.key        
        self.mainpage.controller.ledeffecttable.setLEDtype(keystr,"RGB")
    
    def setLEDtypeSingle(self):
        label = self.ledlabel #event.widget
        keystr = label.key        
        self.mainpage.controller.ledeffecttable.setLEDtype(keystr,"Single")
        
    def mark_lastled(self):
        label = self.ledlabel #event.widget
        keystr = label.key
        keyint = int(keystr)
        lednumint=int(keyint/3)+1
        self.mainpage.controller.set_maxLEDcnt(lednumint)
        self.mainpage.update_ledtable_complete()
        

# ------------------------------

# ********************************************************************************
# *
# * Class: ledeffecttable
# *
# * Description: holds all data and params for the led macros and effects
# *
# *
# * Structure: 
# *   "ledeffecttable": {
# *            "000": {
# *                "type": "RGB",
# *                "effect": "ROOM_DARK",
# *                "macro": "House",
# *                "active": "False",
# *                "effect2": "",
# *                "effect3": "",
# *                "groupname": "Group01",
# *                "color": "#FFFFFF",
# *                "params": {}
# *            },
# *            "001": {
# *                "type": "RGB",
# *                "effect": "ROOM_BRIGHT",
# *                "macro": "House",
# *                "active": "False",
# *                "effect2": "",
# *                "effect3": "",
# *                "groupname": "Group01",
# *                "color": "#FFFFFF",
# *                "params": {}
# *            },
# *            "002": {
# *                "type": "RGB",
# *                "effect": "",
# *                "macro": "Const",
# *                "active": "True",
# *                "effect2": "",
# *                "effect3": "",
# *                "groupname": "Group02",
# *                "color": "#FFFF00",
# *                "params": {
# *                    "S_Class": "SI_1",
# *                    "S_Address": "Switch01",
# *                    "S_Type": "S_ONOFF",
# *                    "S_Start": "Off",
# *                    "Cx": "C_ALL",
# *                    "Val0": 0,
# *                    "Val1": 255,
# *                    "Group_Name": "Group02",
# *                    "Group_Distributor": "",
# *                    "Group_Connector": "",
# *                    "Group_Colour": "#FFFF00",
# *                    "Group_Comment": ""
# *                }
# *            },
# *
# *
# ********************************************************************************

class ledeffecttable_class:
    def __init__(self,ledgrouptable, controller):
        self.mledeffecttable = {}
        self.mledgrouptable = ledgrouptable
        self.controller = controller
        self.master = controller
        self.copypaste_dict = {"copytype":"copy", #type "copy, "cut"
                               "copykeys":[]
                               }
        
    def get_table(self):
        return self.mledeffecttable
    
    def set_table(self,new_table):
        self.mledeffecttable = new_table
       
    def get(self, key,default):
        return self.mledeffecttable.get(key,default)
    
    def getpath(self, path, default=None):
        keys = path.split(".")
        val = None
    
        for key in keys:
            if val:
                try:
                    val = val.get(key, default)
                except:
                    val = default
                    break
            else:
                val = self.get(key, default)
    
            if not val:
                break
    
        return val
    
    def set_ledlist_cmd(self,ledlist_cmd, ledlist_shift_cmd):
        self.ledlist_cmd = ledlist_cmd
        self.ledlist_shift_cmd = ledlist_shift_cmd
        
    def setLEDtype(self, keystr,LEDtype):
        lednum_dict = self.get(keystr,{})
        if lednum_dict != {}:
            lednum_dict["type"] = LEDtype
        
        for channel in ["R","G","B"]:
            channelkey = self.getpath(keystr + "." + "channel_keys" + "." + channel,"")
            if channelkey != "":
                lednum_dict = self.get(channelkey,{})
                if channel == "R":
                    lednum_dict["ignore"] = "False"
                else:
                    if LEDtype == "RGB":
                        lednum_dict["ignore"] = "True"
                    else:
                        lednum_dict["ignore"] = "False"
        self.update_ledtable_complete()
        
    def determine_startkey_of_rgb_led(self,keystr):
        key_int = int(keystr)
        startkey_int = key_int - (key_int %3)
        startkey_str = '{:03}'.format(startkey_int)
        return startkey_str
    
    def determine_led_channel_no_Macro(self,macro,effect,params):
        if macro != "":
            macrodata = self.controller.MacroDef.data.get(macro,{})
            no_of_LED_ch = macrodata.get("LEDs or LED Channel","")
            
            if no_of_LED_ch == "":
                return 0
            else:
                if str.isdigit(no_of_LED_ch): # number of RGB LEDs needed, all 3 channels
                    return 1
                else:
                    if no_of_LED_ch == "n": # house of gaslights macro, effect defines the number of LED channels needed
                        start_no_of_LED = EFFECT_LED_STARTLED_LIST.get(effect,"0")
                        if str.isdigit(start_no_of_LED): # value is start number of LED
                            return int(start_no_of_LED)
                        else: #value is "Cx"
                            start_no_of_LED2 = EFFECT_LED_STARTLED_LIST.get(start_no_of_LED,"")
                            if str.isdigit(start_no_of_LED2): # value is start number of LED
                                return int(start_no_of_LED2)
                            else:
                                return 0                    
                    else:
                        #check if value is a param and return the vale of the param
                        
                        if params != {}:
                            start_no_of_LED = str(params.get(no_of_LED_ch,no_of_LED_ch))
                            if str.isdigit(start_no_of_LED): # number of RGB LEDs needed, all 3 channels
                                return 1
                            else: # Cx channel definition
                                start_no_of_LED2 = EFFECT_LED_STARTLED_LIST.get(start_no_of_LED,start_no_of_LED)
                                if str.isdigit(start_no_of_LED2): # value is number of channels needed
                                    return int(start_no_of_LED2)
                                else:
                                    return 0
        
        
        return 0            
        
    
    def ledkey_valid_for_macro(self,macro,effect,macro_params,keystr):
        
        led_channel_no_keystr = self.determine_LED_Channel_number(keystr)
        led_channel_no_Macro = self.determine_led_channel_no_Macro(macro,effect,macro_params)
        
        if led_channel_no_Macro != 0:
            return led_channel_no_keystr == led_channel_no_Macro
        else:
            return True
    
    def determine_no_of_LED_channels_macro(self, keystr, macro, effect, params={}):
        
        led_param_dict = self.mledeffecttable.get(keystr,{})
                
        if macro != "":
            macrodata = self.controller.MacroDef.data.get(macro,{})
            no_of_LED_ch = macrodata.get("LEDs or LED Channel","")
            singleLEDCnt = macrodata.get("SingleLEDCnt","")
            if singleLEDCnt =="":
                #RGB-LED
                LED_factor = 3
            else:
                LED_factor = 1
            if no_of_LED_ch == "":
                return 0
            else:
                if str.isdigit(no_of_LED_ch): # number of RGB LEDs needed, all 3 channels
                    return LED_factor * int(no_of_LED_ch)
                else:
                    if no_of_LED_ch == "n": # house of gaslights macro, effect defines the number of LED channels needed
                        no_of_LED_ch2 = EFFECT_LED_CHANNELS_LIST.get(effect,"0")
                        if str.isdigit(no_of_LED_ch2): # value is number of LEDs needed
                            return int(no_of_LED_ch2) * LED_factor
                        else: #value is "Cx"
                            no_of_LED_ch3 = EFFECT_LED_CHANNELS_LIST.get(no_of_LED_ch2,"")
                            if str.isdigit(no_of_LED_ch3): # value is number of channels needed
                                return int(no_of_LED_ch3)
                            else:
                                return 0                    
                    else:
                        #check if value is a param and return the value of the param
                        
                        if params != "":
                            no_of_LED_ch2 = str(params.get(no_of_LED_ch,no_of_LED_ch))
                            if str.isdigit(no_of_LED_ch2): # number of RGB LEDs needed, all 3 channels
                                if no_of_LED_ch.startswith("C"): # paramname startw with "C" => single channel LED
                                    return int(no_of_LED_ch2)
                                else:
                                    return LED_factor * int(no_of_LED_ch2)
                            else: # Cx channel definition
                                no_of_LED_ch3 = EFFECT_LED_CHANNELS_LIST.get(no_of_LED_ch2,no_of_LED_ch2)
                                if str.isdigit(no_of_LED_ch3): # value is number of channels needed
                                    return int(no_of_LED_ch3)
                                else:
                                    return 0
        
        return 0
    
        
    def determine_no_of_LED_channels_key(self, keystr):
        
        led_param_dict = self.mledeffecttable.get(keystr,{})
        macroparams = led_param_dict.get("params",{})
        
        macro = led_param_dict.get("macro","")
        no_of_LED_ch = 0
        
        if macro != "":
            if macro in ["House","GasLights"]:
                effect = led_param_dict.get("effect","")
            else:
                effect = ""
            no_of_LED_ch = self.determine_no_of_LED_channels_macro(keystr, macro, effect, params=macroparams)
        else:
            ledtype = led_param_dict.get("type","")
            if ledtype == "RGB":
                no_of_LED_ch = 3
            else:
                no_of_LED_ch = 1
        return no_of_LED_ch

    
    def setLEDmacro(self, keystr,macro, effect=""):
        
        # determine LEDs or LED Channel of macro / effect
        no_of_LED_ch = self.determine_no_of_LED_channels_macro(keystr,macro,effect)
        
        # determine start channel
        if no_of_LED_ch >2: # block complete RGB LEDs
            startkey_str = self.determine_startkey_of_rgb_led(keystr)
        else:
            startkey_str = keystr
        
        # set macro/effect in start channel
        
        # set all needed channels to "ignore"="True"
        

        self.update_ledtable_complete()
        
    def removeLEDmacro(self, keystr):
        
        # determine LEDs or LED Channel of macro / effect in the key
        
        # determine start channel and number of channels blocked by macro/effect
        # remove macro/effect from start channel
        
        # set all used channels to "ignore"="False"
        
 
        self.update_ledtable_complete()        
       
    
    def keys(self):
        return self.mledeffecttable.keys()
    
    def len(self):
        return len(self.mledeffecttable)
    
    def init_ledeffecttable(self):
        #self.maxLEDcnt = self.get_maxLEDcnt()
        for i in range(int(MAXLED)):
            keystr = '{:03}'.format(i)
            self.init_entry(keystr)
        keystr = '{:03}'.format(MAXLED)
        self.init_entry(keystr,lastentry="True")
        
 
    def init_entry(self,keystr,lastentry="False"):
        
        LED_number, LED_Channel, LED_Channel_keys = self.determine_LED_Channel_data(keystr)
        
        self.set_led_ignore_entry(keystr,"False") # reset all related ignore entries
                    
        self.mledeffecttable[keystr] = {"type"         : "Single", # type can be RGB,Single
                                       "ignore"       : "False",
                                       "effect"       : "",
                                       "macro"        : "",
                                       "LED_number"   : LED_number,
                                       "channel"      : LED_Channel,
                                       "channel_keys" : LED_Channel_keys,
                                       "lastentry"    : lastentry
                                       }
        if lastentry == "True":
            self.lastentry_key = keystr

    def check_last_entry(self, keystr):
        return keystr == self.lastentry_key

    def init_entries(self,start_idx,cnt_int):
        maxlen = self.len()
        if (start_idx + cnt_int) > maxlen:
            cnt_int = maxlen - start_idx        

        for i in range(cnt_int):
            cur_idx = start_idx + i
            cur_keystr = '{:03}'.format(cur_idx)
            self.init_entry(cur_keystr)
            
    def determine_first_channel(self, value):
        res = int(value/3) * 3
        return res
    
    def determine_LED_Channel_data(self, keystr):
        LED_entry_num = int(keystr)
        LED_Channel = (LED_entry_num % 3)+1
        if LED_Channel == 1:
            LED_Channel_str = "R"
            LED_Channel_keys = {"R": '{:03}'.format(LED_entry_num),
                                "G": '{:03}'.format(LED_entry_num+1),
                                "B": '{:03}'.format(LED_entry_num+2)
                                }
        elif LED_Channel == 2:
            LED_Channel_str = "G"
            LED_Channel_keys = {"R": '{:03}'.format(LED_entry_num-1),
                                "G": '{:03}'.format(LED_entry_num),
                                "B": '{:03}'.format(LED_entry_num+1)
                                }           
        elif LED_Channel == 3:
            LED_Channel_str = "B"
            LED_Channel_keys = {"R": '{:03}'.format(LED_entry_num-2),
                                "G": '{:03}'.format(LED_entry_num-1),
                                "B": '{:03}'.format(LED_entry_num)
                                }
        LED_number = int(LED_entry_num/3)
        return LED_number, LED_Channel_str, LED_Channel_keys
    
    def determine_LED_Channel_number(self, keystr):
        LED_entry_num = int(keystr)
        LED_Channel = (LED_entry_num % 3)+1

        return LED_Channel
    
    def adapt_effect_to_channel(self, keystr, effect):
        if keystr != "":
            adapt_effect = SingleEffectHandling_Tbl.get(effect,effect).format(self.determine_LED_Channel_number(keystr))
        else:
            adapt_effect = effect
        return adapt_effect

    def copy_leds(self,start_idx,cnt_int,dest_idx):
        # copies  leds
        # start_idx : index of start LED-channel in mledeffecttable
        # dest_idx  : index of destination LED-channel in mledeffecttable
        # cnt_int   : number of LED-channels to copy
        #start_idx = self.determine_first_channel(start_idx)
        #dest_idx  = self.determine_first_channel(dest_idx)
        maxlen = self.len()
        copycnt_int = cnt_int
        if (dest_idx + cnt_int) >= maxlen:
            copycnt_int = maxlen - dest_idx
        if (start_idx + copycnt_int) > maxlen:
            copycnt_int = maxlen - start_idx
        for i in range(copycnt_int):    
            if start_idx < dest_idx:
                # copy from lower to higer
                dest_keystr = '{:03}'.format(dest_idx + copycnt_int -i -1)
                start_keystr = '{:03}'.format(start_idx + copycnt_int - i -1)
            else:
                # copy from higher to lower
                dest_keystr = '{:03}'.format(dest_idx+i)
                start_keystr = '{:03}'.format(start_idx+i)
               
            self.mledeffecttable[dest_keystr] = self.mledeffecttable[start_keystr].copy()
            LED_number, LED_Channel, LED_Channel_keys = self.determine_LED_Channel_data(dest_keystr)
            self.mledeffecttable[dest_keystr]["LED_number"]   = LED_number
            self.mledeffecttable[dest_keystr]["channel"]      = LED_Channel
            self.mledeffecttable[dest_keystr]["channel_keys"] = LED_Channel_keys              
 
    def move_leds(self,start_int,cnt_int,dest_int,move_type="init"):
        self.copy_leds(start_int,cnt_int,dest_int)
        if dest_int > start_int:
            remove_start_int = start_int
            if (dest_int - start_int)<cnt_int:
                remove_cnt_int = dest_int-start_int
            else:
                remove_cnt_int = cnt_int
        else:
            remove_start_int = start_int
            if (start_int - dest_int)<cnt_int:
                remove_start_int = dest_int+cnt_int
                remove_cnt_int = start_int-dest_int
            else:
                remove_start_int = start_int
                remove_cnt_int = cnt_int
        if move_type =="init":
            self.init_entries(remove_start_int,remove_cnt_int)
        else:
            self.remove_leds(remove_start_int,remove_cnt_int)
        
    def insert_leds(self,start_int,cnt_int):
        maxlen = self.len()
        ledtocopy = maxlen - start_int
        dest_int  = start_int + cnt_int
        self.move_leds(start_int,ledtocopy,dest_int)

    def remove_leds(self,remove_start_int,cnt_int):
        maxlen = self.len()
        start_idx = remove_start_int
        ledtocopy = maxlen-start_idx-cnt_int
        dest_int  = start_idx
        start_int = start_idx+cnt_int
        self.move_leds(start_int,ledtocopy,dest_int)
        
    def copy_leds_to_clipboard(self,start_idx,cnt_int,copytype="copy"):
        copy_dict = {"type":copytype,
                     "start_idx": start_idx,
                     "count":cnt_int,
                     "data": {}}
        copy_dict_data = copy_dict["data"]
        for i in range (cnt_int):
            start_keystr = '{:03}'.format(start_idx+i)
            copy_dict_data[start_keystr] = self.mledeffecttable.get(start_keystr,{})
      
        parsed_json = json.dumps(copy_dict)
        self.controller.addtoclipboard(parsed_json)
        
    def paste_leds_from_clipboard(self,dest_idx):
        clipboardtext = self.controller.readfromclipboard()
        
        copy_dict = json.loads(clipboardtext)
        
        copy_start_idx = copy_dict.get("start_idx",0)
        copy_count = copy_dict.get("count",0)
        copytype = copy_dict.get("type","copy")
        
        self.insert_leds(dest_idx,copy_count)
        
        if copytype == "copy":        
            self.copy_leds(copy_start_idx,copy_count,dest_idx)
        else:
            self.move_leds(copy_start_idx,copy_count,dest_idx,move_type="remove")
        
    def create_tooltip_from_params(self,ledgroup_params_dict,lednum_params_dict,lednum_setmacro_dict):
        param_str = ""
        if lednum_params_dict != {}:
            if "S_Class" in lednum_params_dict and "S_Address" in lednum_params_dict:
                switch_type = lednum_params_dict.get("S_Class","---")
                if switch_type == "SI_1":
                    param_str = "Schalterart: Immer an"
                else:
                    param_str = "Schalterart: "+switch_type +"\nAdresse:" + lednum_params_dict.get("S_Address","---")
        else:
            if ledgroup_params_dict != {}:
                if "S_Class" in ledgroup_params_dict and "S_Address" in ledgroup_params_dict:
                    switch_type = ledgroup_params_dict.get("S_Class","---")
                    if switch_type == "SI_1":
                        param_str = "Schalterart: Immer an"
                    else:
                        param_str = "Schalterart: "+switch_type +"\nAdresse:" + ledgroup_params_dict.get("S_Address","---")                    
                    
            #param_str = "Group:" + repr(ledgroup_params_dict)                
             
        if lednum_setmacro_dict != {}:
            for key in lednum_setmacro_dict:
                param_str += "\n" + "Set:" + key
        return param_str
    
    def determine_fg_color(self,hex_str):
        '''
        Input a string without hash sign of RGB hex digits to compute
        complementary contrasting color such as for fonts
        '''
        
        (r, g, b) = (hex_str[1:3], hex_str[3:5], hex_str[5:])
        return '#000000' if 1 - (int(r, 16) * 0.299 + int(g, 16) * 0.587 + int(b, 16) * 0.114) / 255 < 0.5 else '#ffffff'        
    
    def update_ledtable_view_key(self, key_str, keylabel):
        if keylabel:
            lednum_dict = self.get(key_str,{}) # type: dict
            lednum_int = int(key_str)
            lednum_groupname = lednum_dict.get("groupname","")
            lednum_macro = lednum_dict.get("macro","")
            ledgroup_dict = self.mledgrouptable.get(lednum_groupname,{})
            if ledgroup_dict != {}:
                ledgroup_params_dict = ledgroup_dict.get("params."+lednum_macro,{}) # check if nested macro params are available
                if ledgroup_params_dict == {}:
                    ledgroup_params_dict = ledgroup_dict.get("params",{})
            else:
                ledgroup_params_dict = {}
                
                                
            ignoreled = lednum_dict.get("ignore","False")

            maxledcnt = int(self.controller.get_maxLEDcnt())
            if lednum_int >= maxledcnt*3:
                ignoreled = True
                
            if ignoreled == "False":
                lednum_effect = lednum_dict.get("effect","")
                ledtype       = lednum_dict.get("type","RGB")
                lednum_params_dict = lednum_dict.get("params",{})
                
                lednum_setmacro_dict = lednum_dict.get("setmacro", {})
                
                text = "<"+lednum_groupname + "> " + lednum_macro
                if lednum_effect != "":
                    text = text + " " + lednum_effect
                param_str = self.create_tooltip_from_params(ledgroup_params_dict,lednum_params_dict,lednum_setmacro_dict)
                                
                if lednum_macro!="":
                    tooltip_text = text + "\n" + param_str
                else:
                    LED_number = int(keylabel.lednum/3)
                    tooltip_text = " LED {:03} - {}  Anschluss:{:03}".format(LED_number,keylabel.channel,keylabel.lednum)          
                
                self.controller.ToolTip(keylabel, text=tooltip_text)
                color_disp = ledgroup_params_dict.get("Group_Colour","#FFFFFF")
                color_fg = self.determine_fg_color(color_disp)
                keylabel.configure(text=text,background=color_disp, borderwidth = 1, foreground=color_fg, relief = "raised")
                keylabel.bind("<Button-1>", self.ledlist_cmd)
                keylabel.bind("<Shift-1>", self.ledlist_shift_cmd)
            else:
                tooltip_text = ""
                self.controller.ToolTip(keylabel, text=tooltip_text)
                color_disp = ledgroup_params_dict.get("Group_Colour","#FFFFFF")
                keylabel.configure(text="",background=color_disp, borderwidth = 0, relief = "flat")
                keylabel.unbind("<Button-1>")
                keylabel.unbind("<Shift-1>")

    def update_ledtable_complete(self):
        for key in self.mledeffecttable.keys():
            label = self.controller.ledeffect_label_list.get(key,None)
            if label:
                self.update_ledtable_view_key(key, label)    
            
    def bind_right_click_menu_to_palettelabel(self, palettelabel,mainpage):
        self.popup = RightClickMenu(self.master, palettelabel, mainpage)        
        palettelabel.bind("<Button-3>", self.popup.popup_text)    
            
    def create_ledlist_frame_content(self, listframe, mainpage):
        
        LEDLISTLABELWIDTH = int(30*SIZEFACTOR)
        row = 1
        for key in self.keys():
            text = ""
            fontcolor = "#000000"
            ledlabel = tk.Label(listframe, background="#FFFFFF", width=LEDLISTLABELWIDTH, height=1,text=text,fg=fontcolor,borderwidth=1, relief="raised") 
            self.bind_right_click_menu_to_palettelabel(ledlabel, mainpage)
            ledlabel.key=key
            ledlabel.bind("<Button-1>", self.ledlist_cmd)
            ledlabel.bind("<Shift-1>", self.ledlist_shift_cmd)
            self.controller.ToolTip(ledlabel, text="LED " + key)
            ledlabel.bind("<FocusOut>", lambda e: e.widget.configure(relief="raised"))
            LED_entry_num = int(key)
            
            lednum_str = '{:03}'.format(LED_entry_num)
        
            LED_Channel = (LED_entry_num % 3)+1
            
            ledlabel.lednum = LED_entry_num
            
            LED_number = int(ledlabel.lednum/3)
            
            if LED_Channel == 1:
                distance = 10
                ledlabel.channel = "R"
                tk.Label(listframe,text="({:03})      R".format(LED_entry_num)).grid(row=row,column=0,padx=4, pady=(distance,0), sticky='e')
            elif LED_Channel == 2:
                distance = 0
                ledlabel.channel = "G"
                tk.Label(listframe,text="LED {:03} G".format(LED_number)).grid(row=row,column=0,padx=4, pady=(distance,0), sticky='e')
            elif LED_Channel == 3:
                distance = 0
                ledlabel.channel = "B"
                tk.Label(listframe,text="B").grid(row=row,column=0,padx=4, pady=(distance,0), sticky='e')
            
            
            tooltip_text = " LED {:03} - {}  Anschluss:{:03}".format(LED_number,ledlabel.channel,ledlabel.lednum)          
            
            ledlabel.grid(row=row, column=1, padx=0, pady=(distance,0),sticky="e")
            self.controller.ledeffect_label_list[key] = ledlabel
            self.update_ledtable_view_key(key,ledlabel)
            row +=1
            

    def set_channel_ignore_entry(self,keystr):
        
        lednum_dict = self.mledeffecttable.get(keystr,{})
        if lednum_dict != {}:
            return lednum_dict.get("ignore","False")
        else:
            return "False"

    def set_led_ignore_entry(self,keystr, ignore_value):
        
        # determine LEDs or LED Channel of macro / effect
        no_of_LED_ch = self.determine_no_of_LED_channels_key(keystr)
        startkey_int = int(keystr)
        for i in range(1, no_of_LED_ch):
            loop_keystr = '{:03}'.format(startkey_int+i)
            loop_lednum_dict = self.mledeffecttable.get(loop_keystr,{}) # type: dict
            loop_lednum_dict['ignore'] = ignore_value
            ledlabel = self.controller.ledeffect_label_list.get(loop_keystr,None)
            self.update_ledtable_view_key(loop_keystr,ledlabel)                           
    
    def led_ignore_entry(self,keystr):
        lednum_dict = self.mledeffecttable.get(keystr,{}) # type: dict
        if lednum_dict != {}:
            return lednum_dict.get('ignore',"False")
        else:
            return "False"
    
    def led_entry_is_empty(self,ledkey_int):
        ledkey = "{:03}".format(ledkey_int)
        ledkey_dict = self.mledeffecttable.get(ledkey,{})
        
        if ledkey_dict == {}:
            return True
        else:
            return False
        
    def macro_nested(self,groupname,macro):
        
        for key in self.controller.ledeffecttable.mledeffecttable:
            leddata_dict = self.controller.ledeffecttable.mledeffecttable.get(key,{})
            if leddata_dict!={}:
                if groupname == leddata_dict.get("groupname",""):
                    if leddata_dict.get("macro","") == "House":
                        if macro != "House":
                            return True

        
        return False

    def update_ledeffecttable_entry(self, keystr, rgb_hex,effect,macro, name, params = {}):
        
        self.controller.paramDataChanged=True
        
        if self.led_ignore_entry(keystr) == "False":
        
            #self.set_led_ignore_entry(keystr,"False") # reset all old ignore values
            
            # determine LEDs or LED Channel of macro / effect
            no_of_LED_ch = self.determine_no_of_LED_channels_macro(keystr,macro,effect,params=params)
            
            # determine start channel
            if no_of_LED_ch >2: # complete RGB LED - start channel is first channel of RGB-LED
                startkey_str = self.determine_startkey_of_rgb_led(keystr)
            else:
                startkey_str = keystr       
            
            if self.ledkey_valid_for_macro(macro,effect,params,keystr):
                lednum_dict = self.mledeffecttable.get(startkey_str,{}) # type: dict
                ledgroup_dict = self.mledgrouptable.get(name,{})
                old_macro = lednum_dict.get("macro","")
                single_effect = False
                
                if macro in SETMACRO_LIST or macro in SWITCHMACROLIST: # assign set macros
                    setmacro_dict = lednum_dict.get("setmacro",{}) # type: dict
                    if setmacro_dict == {}:
                        lednum_dict["setmacro"] = {}
                    setmacro_dict = lednum_dict.get("setmacro",{}) # type: dict
                    if macro =="Set_ColTab":
                        params = self.controller.palette
                    setmacro_dict[macro] = params.copy()
                else:
                    if macro in ["House","GasLights"] and params != {}:
                        # only update params
                        if self.macro_nested(name,macro):
                            ledgroup_dict['params.'+macro] = params.copy()
                        else:
                            ledgroup_dict['params'] = params.copy()
                    else:
                        self.set_led_ignore_entry(keystr,"False") # reset all old ignore values
                                            
                        if macro in ["House","GasLights"] and effect != "":
                            lednum_dict['effect'] = effect
                        else:
                            lednum_dict['effect'] = ""
                            
                        lednum_dict['macro'] = macro
                        lednum_dict['groupname'] = name
                        lednum_dict['active'] = "True"
                        lednum_dict['color'] = rgb_hex
                        lednum_dict['params'] = params.copy()
                        lednum_dict['ignore'] = "False"
                        
                ledlabel = self.controller.ledeffect_label_list.get(keystr,None)
                
                self.update_ledtable_view_key(keystr,ledlabel)
                
                # set for all other channels used by the macro/effect "ignore" = "True"
                if no_of_LED_ch > 1:
                    self.set_led_ignore_entry(startkey_str,"True") # reset all old ignore values

    def update_ledeffecttable(self, lednum, ledcount,rgb_hex,effect,macro, name, params = {}):
        for i in range(ledcount):
            loop_keystr = '{:03}'.format(lednum+i)
            self.update_ledeffecttable_entry(loop_keystr, rgb_hex, effect, macro, name, params)


    def update_ledeffecttable_activestatus(self, lednum, ledcount):
        for key in self.keys():
            lednum_dict = self.mledeffecttable.get(key,{})
            if lednum_dict != {}:
                lednum_dict['active'] = "False"
                if lednum_dict.get("ignore","False") == "False":
                    label = self.controller.ledeffect_label_list.get(key,None)
                    if label:
                        label.configure(relief="raised",borderwidth=1)

        for i in range(ledcount):
            lednum_str = '{:03}'.format(lednum+i)
            lednum_dict = self.mledeffecttable.get(lednum_str,{})
            if lednum_dict != {}:
                lednum_dict['active'] = "True"
                if lednum_dict.get("ignore","False") == "False":
                    label = self.controller.ledeffect_label_list.get(lednum_str,None)
                    if label:
                        label.configure(relief="sunken", borderwidth=1)

    def hexa_to_rgb(self, color):
        """Convert hexadecimal color to RGB."""
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        if len(color) == 7:
            return r, g, b
        elif len(color) == 9:
            return r, g, b, int(color[7:9], 16)
        else:
            raise ValueError("Invalid hexadecimal notation.")


    def handle_setmacros_and_switches(self, group_setmacro_dict):
        macro_str = ""
        progmem_str = ""
        define_str = ""
        start_value_str = ""
        variableNameStr = "SI_1"
        variableNumber = -1
        if group_setmacro_dict != {}:
            # handle set_macros
            logging.info(repr(group_setmacro_dict))

            for setmacro_key in group_setmacro_dict:
                if setmacro_key == "Set_ColTab":
                    color_str = ""
                    coltab_palette = group_setmacro_dict.get("Set_ColTab",{})
                    
                    for i, colorkey in enumerate(coltab_palette):
                        if color_str != "":
                            color_str = color_str + ","
                        keycolor = coltab_palette[colorkey]
                        r,g,b = self.hexa_to_rgb(keycolor)
                        color_str = color_str + str(r) + "," + str(g) + "," + str(b)
                    macro_str = macro_str + "Set_ColTab(" + color_str + ")\n"
                else:
                    setmacro_valuelist = group_setmacro_dict.get(setmacro_key,{})
                    if setmacro_valuelist != {}:
                        macrodata = self.controller.MacroDef.data.get(setmacro_key,{})
                        if macrodata != {}:
                            

                            tmp_macro_str, tmp_progmem_str, tmp_define_str, variableNameStr, variableNumber, tmp_start_value_str = self.handle_switches(setmacro_valuelist)
                            progmem_str += tmp_progmem_str
                            define_str  += tmp_define_str
                            start_value_str += tmp_start_value_str
                            macro_str   += tmp_macro_str
                            setmacro_valuelist["VariableName"]=variableNameStr
                            setmacro_valuelist["VariableNumber"]=variableNumber
                                
                            define_template = macrodata.get("DefineStr","")
                            if define_template != "":
                                define_str = define_str + define_template.format(**setmacro_valuelist)+"\n"
                            setmacro_valuelist["InCh"]=variableNameStr

                            macro_template = macrodata.get("MacroStr","")
                            macro_str = macro_str + macro_template.format(**setmacro_valuelist)
                            macro_str = macro_str + "\n"
                            
        return macro_str, progmem_str, define_str, variableNameStr, variableNumber, start_value_str
    
    def handle_switches(self, paramvaluelist,in_cnt=1):
        
        digital_system = self.controller.get_macroparam_val("ARDUINOConfigPage","MLL_DigitalSystem")
        if digital_system =="DCC":
            self.digitalswitchtype="DCC-switch"
        elif digital_system == "Selectrix":
            self.digitalswitchtype="SX-switch"
        else:
            self.digitalswitchtype="CAN-switch"
        macro_str = ""
        progmem_str = ""
        define_str = ""
        start_value_str = ""
        variableNameStr = "SI_1"
        variableNumber = -1
        first_variableNameStr = "SI_1"
        first_variableNumber = -1        
        if paramvaluelist != {}:
            # handle set_macros
            #print(repr(group_setmacro_dict))
            invert_value = paramvaluelist.get("S_Invert","")
            if invert_value == 1:
                paramvaluelist["S_Invert"] = "_Inv"
            else:
                paramvaluelist["S_Invert"] = ""                         
            switch_type = paramvaluelist.get("S_Class","")
            if switch_type != "":
                if switch_type in ("DCC-switch","CAN-switch","SX-switch","Variable"):
                    
                    # handle DCC switch
                    setmacro_valuelist = paramvaluelist.copy()
                    if setmacro_valuelist != {}:                    
                        macrodata = self.controller.MacroDef.data.get(switch_type,{})
                        if macrodata != {}:
                            # handle case that macro needs a variable
                            progmem_template = macrodata.get("ProgmemStr","")
                            variableNumber = -1
                            variableName = "SI_1"
    
                            if progmem_template != "":
                                s_address_old = setmacro_valuelist["S_Address"]
                                for var_index in range(in_cnt):
                                    if switch_type == "Variable":
                                        #variableNameStr = setmacro_valuelist["S_Address"]
                                        variableName_template = macrodata.get("VariableNameStr","")     
                                        variableNameStr = variableName_template.format(**setmacro_valuelist)                                        
                                    else:
                                        if switch_type == "SX-switch":
                                            s_address = setmacro_valuelist["S_Address"]
                                            s_channel,s_bit=s_address.split(".")
                                            s_channel_int = int(s_channel)+var_index
                                            s_bit_int = int(s_bit)
                                            if s_channel_int in range(0,99) and s_bit_int in range(1,8):
                                                sx_address = s_channel_int*8 + s_bit_int-1
                                                setmacro_valuelist["SX_Address"] = str(sx_address)
                                            else:
                                                setmacro_valuelist["SX_Address"] =  ""
                                        else:
                                            s_address_int = int(setmacro_valuelist["S_Address"])
                                        variableName_template = macrodata.get("VariableNameStr","")     
                                        variableNameStr = variableName_template.format(**setmacro_valuelist)
                                    variableNameexists = False
                                    if variableNameStr in self.variableNameList:
                                        variableNumber = self.variableNameList.index(variableNameStr)
                                        variableNameexists = True
                                        setmacro_valuelist["VariableName"]=variableNameStr
                                        setmacro_valuelist["VariableNumber"]=variableNumber
                                        setmacro_valuelist["InCh"]=variableNameStr                                    
                                    else:
                                        self.variableNameList.append(variableNameStr)
                                        variableNumber = self.variableNameList.index(variableNameStr)
                                        setmacro_valuelist["VariableName"]=variableNameStr
                                        setmacro_valuelist["VariableNumber"]=variableNumber
                                        setmacro_valuelist["InCh"]=variableNameStr                                    
                                        progmem_str = progmem_str + progmem_template.format(**setmacro_valuelist)+"\n"
                                        define_template = macrodata.get("DefineStr","")
                                        if define_template != "":
                                            define_str = define_str + define_template.format(**setmacro_valuelist)+"\n"
                                        start_value_template = macrodata.get("SetStartValueStr","")
                                        if start_value_template != "":
                                            if setmacro_valuelist.get("S_Start","0") != "0":
                                                start_value_str = start_value_str + start_value_template.format(**setmacro_valuelist)+"\n"
                                    # increase address by one for next variable
                                    if not switch_type in ["SX-switch","Variable"]:
                                        s_address_int = int(setmacro_valuelist["S_Address"])+1
                                        setmacro_valuelist["S_Address"] = str(s_address_int)
                                    if var_index == 0: # first entry save variable_name and number
                                        first_variableNameStr=variableNameStr
                                        first_variableNumber=variableNumber
                                        
                                #setmacro_valuelist["S_Address"] = s_address_old
                                
     
                            macro_template = macrodata.get("MacroStr","")
                            macro_str = macro_str + macro_template.format(**setmacro_valuelist)
                            macro_str = macro_str + "\n"                    

                elif switch_type == "ARDUINO-port":
                    pass                

                elif switch_type == "SI_1":
                    pass
                            
        return macro_str, progmem_str, define_str, first_variableNameStr, first_variableNumber, start_value_str 


    def get_param_value_list(self, paramvaluelist, macroparams,groupparams,key=""):
  
        if macroparams != {}:
            for paramkey in macroparams:
                paramvalue = macroparams.get(paramkey,0)
                if paramkey == "Cx":
                    paramvalue = self.adapt_effect_to_channel(key,paramvalue)                        
                paramvaluelist[paramkey] = paramvalue
        if groupparams != {}:
            for paramkey in groupparams:
                paramvalue = groupparams.get(paramkey,0)
                paramvaluelist[paramkey] = paramvalue
        return
    
    def replace_in_string(self,orig_str,replace_dict):
        target_str = orig_str
        for replace_str in replace_dict:
            target_str = target_str.replace(replace_str,replace_dict.get(replace_str,""))
        return target_str

    def generate_macros(self,init_arduino=False):
        macro_str = ""
        define_str = ""
        start_value_str = ""
        progmem_str = ""
        effect_str = ""
        macro_variable = "SI_1"
        LED_old = 0
        LED_Startnum = 0
        old_groupname = ""
        old_macro = ""
        new_macro = True
        nested_macro = False
        macro_str_savednested = ""
        group_setmacro_dict = {}
        macroparams ={}
        groupparams = {}
        paramvaluelist = {}
        macrodata = {}
        self.variableNameList = []
        variableName = ""
        variableNameStr= "SI_1"
        self.digitalswitchtype = ""
        singeleffect_added = False
        if not init_arduino:
            for key in self.mledeffecttable.keys():
                # go through all LEDs in the LED list and create the macros
                # get all parameters for the current LED
                led_param_dict   = self.mledeffecttable.get(key,{})
                macro            = led_param_dict.get("macro","")
                groupname        = led_param_dict.get("groupname","")
                group_param_dict = self.mledgrouptable.get(groupname,{})
                effect           = self.adapt_effect_to_channel(key,led_param_dict.get("effect",""))
                channel          = led_param_dict.get("channel","")
                ignore_entry = led_param_dict.get("ignore","")
                if not ignore_entry == "True":            
                    #if (macro == "House" or ((groupname != old_groupname) and (macro!="")) or self.check_last_entry(key)) and nested_macro:
                    if (macro == "House" or ((groupname != old_groupname)) or self.check_last_entry(key)) and nested_macro:
                        # nested macros are finished, continue with house macro
                        # if the previous macro was "GasLights" then GasLights needs to be closed
                        if old_macro == "GasLights":
                            #close the gaslights macro
                            logging.info("Nested GasLights")
                            tmp_macro_str, tmp_progmem_str, tmp_define_str, variableNameStr, variableNumber, tmp_start_value_str = self.handle_setmacros_and_switches(group_setmacro_dict)
                            self.get_param_value_list(paramvaluelist, macroparams, groupparams)
                            tmp_macro_str1, tmp_progmem_str1, tmp_define_str1, variableNameStr1, variableNumber1,tmp_start_value_str1 = self.handle_switches(paramvaluelist)   
                            macro_str += tmp_macro_str + tmp_macro_str1
                            progmem_str += tmp_progmem_str + tmp_progmem_str1
                            define_str += tmp_define_str + tmp_define_str1
                            start_value_str += tmp_start_value_str + tmp_start_value_str1
                            macro_params = {}
                            group_setmacro_dict = {}
                            paramvaluelist={}
                            self.get_param_value_list(paramvaluelist, macroparams, groupparams, key=key) # ***
                            paramvaluelist["LED"]=int(LED_Startnum/3)
                            paramvaluelist["EffectStr"]= effect_str
                            paramvaluelist["InCh"]=variableNameStr1
                            invert_value = paramvaluelist.get("S_Invert","")
                            if invert_value == 1:
                                paramvaluelist["S_Invert"] = "_Inv"
                            else:
                                paramvaluelist["S_Invert"] = ""                                     
                            macrodata = self.controller.MacroDef.data.get(old_macro,{})
                            if macrodata != {}:
                                macro_template = macrodata.get("MacroStr")
                                macro_str = macro_str + macro_template.format(**paramvaluelist)                    
                            macro_str = macro_str + "\n"
                            
                        # add the nested macro to the nested macro string
                        macro_str_savednested = macro_str_savednested + macro_str
                        
                        # restore save data from "house" macro
                        macro_str = nested_macro_str
                        effect_str = nested_effect_str
                        LED_Startnum = nested_LED_Startnum
                        paramvaluelist = nested_paramvaluelist.copy()
                        group_setmacro_dict = nested_group_setmacro_dict.copy()
                        macro_params = nested_macro_params.copy()
                        old_macro = "House"
                        nested_macro = False
                        new_macro = False
                    # check if the groupname has changed. In this case a new macro has started
                    if ((groupname != old_groupname) and (macro!="")) or self.check_last_entry(key):
                        new_macro = True
                    
                    if new_macro:
                        # end last macro and add macro strings to macro_str
                        if macrodata!={}:
                            in_cnt=int(macrodata.get("In_Cnt","1"))
                        else:
                            in_cnt=1
                        tmp_macro_str, tmp_progmem_str, tmp_define_str, variableNameStr, variableNumber, tmp_start_value_str = self.handle_setmacros_and_switches(group_setmacro_dict)
                        self.get_param_value_list(paramvaluelist, macroparams, groupparams)
                        tmp_macro_str1, tmp_progmem_str1, tmp_define_str1, variableNameStr1, variableNumber1, tmp_start_value_str1 = self.handle_switches(paramvaluelist,in_cnt=in_cnt)   
                        macro_str += tmp_macro_str + tmp_macro_str1
                        progmem_str += tmp_progmem_str + tmp_progmem_str1
                        define_str += tmp_define_str + tmp_define_str1
                        start_value_str += tmp_start_value_str + tmp_start_value_str1
                        macroparams = {}
                        groupparams = {}
                        group_setmacro_dict = {}
         
                        if old_macro =="House" or old_macro == "GasLights":
                            self.get_param_value_list(paramvaluelist, macroparams, groupparams, key=key) # *****
                            paramvaluelist["LED"]=int(LED_Startnum/3)
                            paramvaluelist["EffectStr"]=effect_str
                            paramvaluelist["InCh"]=variableNameStr1
                            macrodata = self.controller.MacroDef.data.get(old_macro,{})
                            if macrodata != {}:
                                macro_template = macrodata.get("MacroStr")
                                macro_str = macro_str + macro_template.format(**paramvaluelist)                    
                            macro_str = macro_str + "\n"
                        if macro_str_savednested != "":
                            # add the nested macros
                            macro_str += macro_str_savednested + "\n"
                            macro_str_savednested=""                
                        new_macro = True # the current macro is a new macro
                        paramvaluelist={}
                    if macro != "":
                        if new_macro:
                            # handle the begin of a macro
                            LED_Startnum = int(key)
                            if macro == "House": # add standard values for house
                                paramvaluelist = {"On_Min" : 1,
                                                  "On_Max" : 2,
                                                  "T_Min"  : 50,
                                                  "T_Max"  : 150}
                            else:
                                paramvaluelist = {}
                            effect_str = ""
                            new_macro = False
                        else:
                            if old_macro == "House"and macro !="House":
                                # handle nested macros
                                nested_macro = True
                                nested_effect_str = effect_str
                                effect_str = ""
                                nested_macro_str = macro_str
                                macro_str = ""
                                nested_LED_Startnum=LED_Startnum
                                LED_Startnum = int(key)
                                nested_paramvaluelist = paramvaluelist.copy()
                                nested_group_setmacro_dict = group_setmacro_dict.copy()
                                nested_macro_params = macroparams.copy()
                                paramvaluelist={}
                                group_setmacro_dict = {}
                       
                        self.get_param_value_list(paramvaluelist, macroparams, groupparams)
                        
                        if macro =="House" or macro == "GasLights":
                            # handle house macro
                            # check if single led effect
                            for singeleffectkey in ["effect","effect2","effect3"]:
                                singleeffect = self.adapt_effect_to_channel(key,led_param_dict.get(singeleffectkey,""))
                                if not nested_macro:
                                    singeleffect_added = True
                                if singleeffect != "":
                                    if effect_str == "":
                                        effect_str = self.adapt_effect_to_channel(key,singleeffect)
                                    else:
                                        effect_str = effect_str + ", " + singleeffect
                        else:
                            macrodata = self.controller.MacroDef.data.get(macro,{})
                            if macrodata != {}:
                                setmacro_dict = led_param_dict.get("setmacro", {})
                                macroparams = led_param_dict.get("params",{})
                                groupparams = group_param_dict.get("params",{})
                                in_cnt=int(macrodata.get("InCnt","1"))
                                self.get_param_value_list(paramvaluelist, macroparams, groupparams, key=key)
                          
                                if setmacro_dict != {}:
                                    # handle set macros
                                    for setkey in setmacro_dict:
                                        group_setmacro_dict[setkey] = setmacro_dict.get(setkey,{})
                                if groupparams!={}:
                                    # handle set macros
                                    for grpkey in groupparams:
                                        group_setmacro_dict[grpkey] = groupparams.get(grpkey,{})
                                        
                                tmp_macro_str, tmp_progmem_str, tmp_define_str, variableNameStr, variableNumber, tmp_start_value_str = self.handle_setmacros_and_switches(group_setmacro_dict)
                                tmp_macro_str1, tmp_progmem_str1, tmp_define_str1, variableNameStr1, variableNumber1, tmp_start_value_str1 = self.handle_switches(macroparams,in_cnt=in_cnt)   
                                macro_str += tmp_macro_str + tmp_macro_str1
                                progmem_str += tmp_progmem_str + tmp_progmem_str1
                                define_str += tmp_define_str + tmp_define_str1
                                start_value_str += tmp_start_value_str + tmp_start_value_str1
                                group_setmacro_dict = {}                        
                                paramvaluelist["LED"]=int(LED_Startnum/3)
                                paramvaluelist["effect_str"]=effect_str
                                paramvaluelist["InCh"]=variableNameStr1                        
                                macro_template = macrodata.get("MacroStr")
                                macro_type = macrodata.get("Typ","")
                                if macro_type =="ImportMacro":
                                    param_replace_dict = macrodata.get("Replace_in_MacroStr",{})
                                    if param_replace_dict!={}:
                                        import_str = paramvaluelist.get("ImportString","")
                                        if import_str != "":
                                            import_str = self.replace_in_string(import_str, param_replace_dict)
                                            import_str = import_str.format(**paramvaluelist)
                                            paramvaluelist["ImportString"]=import_str
                                            import_test=True
                                            #**********************test
                                            if import_test:
                                                try:
                                                    template_str = paramvaluelist.get("TemplateString","")
                                                    template_str = template_str.replace("\n","")
                                                    logging.debug("Import_String: %s Template_string:%s",import_str,template_str)
                                                    m=re.match(template_str,import_str)
                                                    if m:
                                                        logging.debug ("Match:",m.groupdict())
                                                except BaseException as e:
                                                    logging.debug(e)
                                            
                                            
                                macro_str = macro_str + macro_template.format(**paramvaluelist)
                                macro_str = macro_str + "\n"
                                paramvaluelist = {}
                            new_macro = True
                        #if nested_macro:
                        #    if channel == "B" and not singeleffect_added:
                        #        nested_effect_str += ",SKIP_ROOM"
                        
        
                        old_groupname = groupname
                        old_macro = macro
                    if nested_macro:
                        if channel == "R": #and not singeleffect_added:
                            nested_effect_str += ",SKIP_ROOM"            
                    
                    if channel == "R":
                        singeleffect_added = False
                    
                    if macro == "House" or macro == "GasLights":
                        setmacro_dict = led_param_dict.get("setmacro", {})
                        macroparams = led_param_dict.get("params",{})
                        groupparams = group_param_dict.get("params."+macro,{})
                        if groupparams == {}:
                            groupparams = group_param_dict.get("params",{})
                        else:
                            logging.info("nested macro"+macro)
                        if setmacro_dict != {}:
                            # handle set macros
                            for key in setmacro_dict:
                                group_setmacro_dict[key] = setmacro_dict.get(key,{})
           
        #set_coltab_str = self.get_coltab_macro()
        
        #macro_str = set_coltab_str + "\n" + macro_str + "\n"
        final_macro_str = ""
        final_progmem_str = ""
        if progmem_str != "":
            digital_system = self.controller.get_macroparam_val("ARDUINOConfigPage","MLL_DigitalSystem")
            macrodata = self.controller.MacroDef.data.get(self.digitalswitchtype,{})
            if macrodata != {}:
                # handle case that digital switch needs to be defined
                switchtypeStr = macrodata.get("SwitchTypeStr","")
                final_progmem_str = switchtypeStr + "\n"
                     
            final_progmem_str = final_progmem_str + "#define USE_EXT_ADDR\n"
            
            final_progmem_str = final_progmem_str + "#define ADDR_OFFSET 0\n"
            
            final_progmem_str = final_progmem_str + """    
            
#define ADDR_MSK  0x3FFF  // 14 Bits are used for the Address
            
#define S_ONOFF   (uint16_t)0
#define B_RED     (uint16_t)(1<<14)
#define B_GREEN   (uint16_t)(2<<14)
#define B_RESERVE (uint16_t)(3<<14)    // Not used at the moment
#define B_TAST    B_RED
#define SEND_INPUTS
             
typedef struct
        {
        uint16_t AddrAndTyp; // Addr range: 0..16383. The upper two bytes are used for the type
        uint8_t  InCnt;
        } Ext_Addr_T;
            
// Definition of external adresses
const PROGMEM Ext_Addr_T Ext_Addr[] =
{ // Addr & Typ    InCnt\n""" + progmem_str + "\n};\n"
                        
            final_macro_str = final_progmem_str + "\n"
        
        if define_str != "": 
            define_str = "// Input channel defines for local inputs and expert users\n" + define_str
            final_macro_str = final_macro_str + define_str + "\n"
            
        setup_fastled_str = "/*********************/"
        setup_fastled_str += "#define SETUP_FASTLED() \ \n"
        setup_fastled_str += "/*********************/                                                       \ \n"
        setup_fastled_str += "CLEDController& controller0 = FastLED.addLeds<NEOPIXEL,  6>(leds+  0, 20);    \ \n"
        setup_fastled_str += "                                                                              \ \n"
        setup_fastled_str += "  controller0.clearLeds(256);                                                 \ \n"
        setup_fastled_str += "/*End*/ \n"

        final_macro_str += setup_fastled_str
        final_macro_str += "MobaLedLib_Configuration()\n  {\n"
            
        final_macro_str = final_macro_str + macro_str
        
        final_macro_str += "\n  EndCfg // End of the configuration\n  };"
        
        final_start_value_str = """
//*******************************************************************

//---------------------------------------------
void Set_Start_Values(MobaLedLib_C &MobaLedLib)
//---------------------------------------------
{
"""     + start_value_str + """
}

// if function returns TRUE the calling loop stops
typedef bool(*HandleValue_t) (uint8_t CallbackType, uint8_t ValueId, uint8_t* Value, uint16_t EEPromAddr, uint8_t TargetValueId, uint8_t Options);


#define InCnt_MSK  0x0007  // 3 Bits are used for the InCnt
#define IS_COUNTER (uint8_t)0x80
#define IS_PULSE   (uint8_t)0x40
#define IS_TOGGLE  (uint8_t)0x00
#define COUNTER_ID

typedef struct
    {
    uint8_t TypAndInCnt; // Type bit 7, InCnt bits 0..3, reserved 0 bits 4..6
    uint8_t Channel;
    } __attribute__ ((packed)) Store_Channel_T;

"""

        final_macro_str += final_start_value_str
        
        return final_macro_str



