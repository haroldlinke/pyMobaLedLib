# -*- coding: utf-8 -*-
#
#         MobaLedCheckColors: Color checker for WS2812 and WS2811 based MobaLedLib
#
#         ServoTestPage
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
# * MobaLedCheckColors is free software: you can servo_0istribute it and/or modify
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
# * tkcolorpicker is free software: you can servo_0istribute it and/or modify
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
from tkcolorpicker.spinbox import Spinbox
from tkcolorpicker.limitvar import LimitVar
from tools.CRCalgorithms import CalculateControlValuewithChecksum

from mlpyproggen.DefaultConstants import COLORCOR_MAX, DEFAULT_PALETTE, LARGE_FONT, NORMAL_FONT, SMALL_FONT, VERY_LARGE_FONT, PROG_VERSION, PERCENT_BRIGHTNESS, BLINKFRQ
# fromx mlpyproggen.dictFile import saveDicttoFile, readDictFromFile
import mlpyproggen.dictFile as dictFile
from scrolledFrame.ScrolledFrame import VerticalScrolledFrame,HorizontalScrolledFrame,ScrolledFrame
from locale import getdefaultlocale
import re
import time
import logging

PERCENT_BRIGHTNESS = 1  # 1 = Show the brightnes as percent, 0 = Show the brightnes as ">>>"# 03.12.19:

COLORCOR_MAX = 255

ARDUINO_WAITTIME = 0.5

Servo_Scale_Min = 0

Servo_Min = 10

Servo_Stop = 0

Servo_Scale_Max = 255
# ----------------------------------------------------------------
# Class ServoTestPage
# ----------------------------------------------------------------

class ServoTestPage2(tk.Frame):

    # ----------------------------------------------------------------
    # ServoTestPage __init__
    # ----------------------------------------------------------------

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.tabClassName = "ServoTestPage2"
        tk.Frame.__init__(self,parent)
        self.controller = controller
        
        self.fontlabel = self.controller.get_font("FontLabel")
        self.fontspinbox = self.controller.get_font("FontSpinbox")
        self.fonttext = self.controller.get_font("FontText")
        self.fontbutton = self.controller.get_font("FontLabel")
        self.fontentry = self.controller.get_font("FontEntry")
        self.fonttext = self.controller.get_font("FontText")
        self.fontscale = self.controller.get_font("FontScale")
        self.fonttitle = self.controller.get_font("FontTitle")
        
        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName)
        
        #button1_text = macrodata.get("Button_1",self.tabClassName)
        #button2_text = macrodata.get("Button_2",self.tabClassName)
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        
        self.frame=ttk.Frame(self,relief="ridge", borderwidth=1)
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)        
        
        self.scroll_main_frame = ScrolledFrame(self.frame)
        self.scroll_main_frame.grid_columnconfigure(0,weight=1)
        self.scroll_main_frame.grid_rowconfigure(0,weight=1)
        
        self.main_frame = ttk.Frame(self.scroll_main_frame.interior, relief="flat", borderwidth=0)        
        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(2,weight=1) 
        
        title_frame = ttk.Frame(self.main_frame, relief="flat", borderwidth=0)

        label = ttk.Label(title_frame, text=self.title, font=self.fonttitle)
        label.pack(padx=5,pady=(5,5))
        
        config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=4,startrow =1,style="CONFIGPage")        
                
        self.on_lednum = 0

        led = self.getConfigData("lastLed")

        serport = controller.arduino

        self.tab_frame = ttk.Frame(self.main_frame,borderwidth=0,relief="flat")

        #direct control frame for servos
        direct_control_frame = ttk.Frame(self.tab_frame,relief="flat", borderwidth=0)
     
        servo_direct_position_frame = ttk.Frame(direct_control_frame, relief="flat", borderwidth=0)
        servo_direct_position_frame.grid(row=0, column=0, padx=0, pady=0,sticky="")
        
        #dc_label1 = ttk.Label(servo_direct_position_frame, text='Servo Direct Control').grid(row=0, column=0, sticky='w', padx=4, pady=4)
     
        servo_direct_position_frame.columnconfigure(0, weight=1)
        
        self.buttonEnter=tk.Label(servo_direct_position_frame, text="ENTER",width=15,height=4,fg="black",relief="raised",font=self.fontbutton)

        self.controller.ToolTip(self.buttonEnter, text="Enter")
        self.buttonEnter.bind("<ButtonRelease-1>",lambda event: self.servo_prog_label_released(event=event,code=0))
        self.buttonEnter.bind("<Button-1>",lambda event: self.servo_prog_label_pressed(event=event,code=0))        
                

        self.servo_pos_var = tk.DoubleVar()
        self.servo_pos_var.set(0)
        #self.servo_scale = ttk.Scale( servo_direct_position_frame, variable = self.servo_pos_var,command=self._update_servo_position,from_=0,to=220,orient=tk.HORIZONTAL,length=440)
        self.servo_scale = tk.Scale( servo_direct_position_frame, variable = self.servo_pos_var,command=self._update_servo_position,from_=Servo_Scale_Min,to=Servo_Scale_Max,orient=tk.HORIZONTAL,length=440,label="Servo position",tickinterval=20,font=self.fontscale)
        
        self.controller.ToolTip(self.servo_scale, text="Position of Servo 0..255\nAnklicken zum Aktivieren der Tasten:\n[Right]/[Left]\n - single step\n[CTRL-Right]/[CTRL-Left]\n - long step\n[Pos1]/[Ende}\n - Anfang/Ende\n"+
                                "\nKlicken auf dem Sliderfeld:\n<Linke Taste>\n - single step vorwärts/rückwärts\n<Rechte Taste>\n - spring zum angeklickten Wert\n<CTRL Linke Taste>\n - springe zum Anfang/Ende")
        self.servo_scale.focus_set()
        self.servo_scale.bind("<Button-1>", self.servo_scale_focus_set)
        self.servo_position = 0
        
        # constants
        select_servo0 = 225
        select_servo1 = 230
        select_servo2 = 235
        
        select_set_min_max_pos = 240
        
        select_set_speed = 245
        
        set_speed_by_button = 250
        
        save_changes = 254
        
        save_position = 205
        
        back_to_normal = 0
        
        lowPos = 1
        
        high_pos = 220
        
        servo_program_frame =ttk.Frame(self.tab_frame,relief="flat", borderwidth=0,width=500)
        #sp_label1 = ttk.Label(servo_program_frame, text='Servo Programmieren').grid(row=0, column=0, sticky='ew',padx=4, pady=4)

        # ------------- SERVO Pos
        s = ttk.Style()
        s.configure('my.TButton', font=self.fontbutton)
                
        servo_set_pos_speed_frame = ttk.Frame(servo_program_frame,relief="flat", borderwidth=0)
        ssp_label1 = ttk.Label(servo_set_pos_speed_frame, text='Programmierung von Min/Max Position und Geschwindigkeit',font=self.fontlabel)
        ssp_label1.grid(row=0, column=0, sticky='',padx=5, pady=5)
       
        self.button_cancel_mm_pos_speed=ttk.Button(servo_set_pos_speed_frame, text="Beende Programmierung ohne Speichern", command=self._cancel_set_min_max_pos,style='my.TButton')
        self.controller.ToolTip(self.button_cancel_mm_pos_speed, text="Beende die Programmierung ohne zu Speichern")
        
        #self.status = "Save Min Pos"
        self.status = "Start Min Pos"

        self.ssp_label2 = ttk.Label(servo_set_pos_speed_frame, text="",width=60,font=self.fontlabel)
        
        
        #self.button_start_save_mm_pos=ttk.Button(servo_set_pos_frame, text="Beende Min Pos programmieren",width=40, command=self._save_min_max_pos)
        self.button_start_save_mm_pos=ttk.Button(servo_set_pos_speed_frame, text="Starte Min-Max Pos/Speed programmieren", command=self._save_min_max_pos, style='my.TButton')
        self.controller.ToolTip(self.button_start_save_mm_pos, text="Startet die Min/Max und Geschwindigkeitsprogrammierung und geht zum nächsten Schritt")
        
        self.button_start_save_mm_pos.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.ssp_label2.grid(row=2, column=0, sticky='ew',padx=5, pady=5)
        self.button_cancel_mm_pos_speed.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
        
        self.servo_scale.grid(row=0,column=1,sticky="")
        self.buttonEnter.grid(row=0,column=0,sticky="",padx=20, pady=10)  

        # --- placement
        self.frame.grid(row=0,column=0)
        self.scroll_main_frame.grid(row=0,column=0,sticky="nesw")
        # scroll_main_frame
        self.main_frame.grid(row=0,column=0)
        # main_frame
        title_frame.grid(row=0, column=0, pady=5, padx=5)
        config_frame.grid(row=1, column=0, pady=5, padx=5)
        self.tab_frame.grid(row=2, column=0, pady=0, padx=5)
        
        self.main_frame.columnconfigure(0,weight=1)
        
        # tab_frame
        direct_control_frame.grid(row=1, rowspan=1, column=0, pady=0, padx=5, sticky="")
        servo_program_frame.grid(row=2, column=0, pady=0, padx=5,sticky="ew")

        self.tab_frame.grid_columnconfigure(0,weight=1)

        self.tab_frame.grid_rowconfigure(3,weight=1)                

        # --- bindings
        #self.controller.bind("<Control-Right>",self.s_servo_address.invoke_buttonup)
        #self.controller.bind("<Control-Left>",self.s_servo_address.invoke_buttondown)
        #self.controller.bind("<Control-Up>",self.s_servo_channel.invoke_buttonup)
        #self.controller.bind("<Control-Down>",self.s_servo_channel.invoke_buttondown)
        self.controller.bind("<F1>",self.controller.call_helppage)
        self.controller.bind("<Alt-F4>",self.cancel)
        self.controller.bind("<Control-o>",self.led_off)

 
    def cancel(self,_event=None):
        try:
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
        #self.controller.bind("<Control-Down>",self.s_servo_address.invoke_buttonup)
        #self.controller.bind("<Control-Up>",self.s_servo_address.invoke_buttondown)
        #self.controller.bind("<Control-Right>",self.s_servo_channel.invoke_buttonup)
        #self.controller.bind("<Control-Left>",self.s_servo_channel.invoke_buttondown)

        self.controller.bind("<F1>",self.controller.call_helppage)
        self.controller.bind("<Alt-F4>",self.cancel)
        
    def tabunselected(self):
        logging.debug("Tabunselected: %s",self.tabname)
        #self.controller.send_to_ARDUINO("#END")
        #time.sleep(ARDUINO_WAITTIME)
        self.controller.ARDUINO_end_direct_mode()
        pass
        
        logging.info(self.tabname)
        pass        

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

            
    def servo_scale_focus_set(self,event=None):
        self.servo_scale.focus_set()

    def _update_servo_channel(self, servo_address, servo_control, position):
        #if servo_control == 0:
        self._update_servos(servo_address, position, servo_control, 0)
        #elif servo_control == 1:
        #    self._update_servos(servo_address, 1, position, 1)
        #else:
        #    self._update_servos(servo_address, 1, 1, position)

    def servo_pos_inc(self,event):
        #var = self.servo_pos_var.get()
        #self.servo_pos_var.set(var + 1)
        pass
        
    def servo_pos_dec(self,event):
        #var = self.servo_pos_var.get()
        #self.servo_pos_var.set(var - 1)
        pass
            
    def _update_servo_position(self, position):
        position_int=int(position)
        self.servo_position = position_int

        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_control = int(self.controller.get_macroparam_val(self.tabClassName, "ServoControl"))
        if servo_control in [1, 2, 3]:

            self._update_servo_channel(servo_address, servo_control, position_int)
        
    def _get_servo_channel_code(self, servo_control):
        # select the right servo
        if servo_control == 0:
            return 225
        elif servo_control == 1:
            return 230
        else:
            return 235

            
    def _cancel_set_min_max_pos(self, event=None):
        # select the right servo
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_control = self.controller.get_macroparam_val(self.tabClassName, "ServoControl")
                
        #send code to ARDUINO
        self._update_servos(servo_address, 0, 0, 0)
        
        self.status = "Start Min Pos"
        self.ssp_label2.config(background="white",text="")
        self.button_start_save_mm_pos.config(text="Starte Min-Max Pos/Speed programmieren")
        
    def _save_min_max_pos(self, event=None):
        
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_control = self.controller.get_macroparam_val(self.tabClassName, "ServoControl")
        servo_channel_code = self._get_servo_channel_code(servo_control)        
        
        if self.status == "Start Min Pos":
            #send code to ARDUINO
            self._update_servos(servo_address, servo_channel_code, 0, 0)
            # send "start pos setting"
            self._update_servos(servo_address, 240, 0, 0)
             # send "start min pos setting"
            self._update_servos(servo_address, 250, 0, 0)
            self.ssp_label2.config(background="#ffff05",text="Bewege den Servo zur Min Position mit den <<,<,>,>> Tastern")        
            self.button_start_save_mm_pos.config(text="Gehe zu Max Pos programmieren")
            self.status = "Save Min Pos"
        elif self.status == "Save Min Pos":
            self.status = "Save Max Pos"
            self.ssp_label2.config(text="Bewege den Servo zur Max Position mit den <<,<,>,>> Tastern")
            #send "save"-code to ARDUINO
            self._update_servos(servo_address, 205, 0, 0)
            self.button_start_save_mm_pos.config(text="Beende Max Pos programmieren")
        elif self.status == "Save Max Pos":
            self.status = "Save Speed"
            self.ssp_label2.config(text="Stelle die Geschwindigkeit mit mit den <<,<,>,>> Tastern ein")
            self.button_start_save_mm_pos.config(text="Beende Speed programmieren")
        
            #send PWMButton1-code to ARDUINO
            self._update_servos(servo_address, 205, 0, 0)
            
            #send speed-code to ARDUINO
            self._update_servos(servo_address, 245, 0, 0)
            
            # send "set speed"
            self._update_servos(servo_address, 250, 0, 0)            

        else:
            self.status = "Start Min Pos"
            self.ssp_label2.config(background="white",text="")
            self.button_start_save_mm_pos.config(text="Starte Min-Max Pos/Speed programmieren")
        
            #send "end"-code to ARDUINO
            self._update_servos(servo_address, 254, 0, 0)
            
            #send "back to normal"-code to ARDUINO
            self._update_servos(servo_address, 0, 0, 0)        

    def _save_min_max_pos2(self, event=None):
        
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_control = self.controller.get_macroparam_val(self.tabClassName, "ServoControl")
        servo_channel_code = self._get_servo_channel_code(servo_control)        
        
        if self.status == "Save Min Pos":
            self.status = "Save Max Pos"
            self.ssp_label2.config(text="Bewege den Servo zur Max Position mit den <<,<,>,>> Tastern")
            #send "save"-code to ARDUINO
            self._update_servos(servo_address, 205, 0, 0)
            self.button_start_save_mm_pos.config(text="Beende Max Pos programmieren")
        elif self.status == "Save Max Pos":
            self.status = "Save Speed"
            self.ssp_label2.config(text="Stelle die Geschwindigkeit mit mit den <<,<,>,>> Tastern ein")
            self.button_start_save_mm_pos.config(text="Beende Speed programmieren")
        
            #send PWMButton1-code to ARDUINO
            self._update_servos(servo_address, 205, 0, 0)
            
            #send speed-code to ARDUINO
            self._update_servos(servo_address, 245, 0, 0)
            
            # send "set speed"
            self._update_servos(servo_address, 250, 0, 0)            

        else:
            self.status = "Save Min Pos"
            self.ssp_label2.config(background="white",text="")
            self.button_start_save_mm_pos.config(text="Beende Min Pos programmieren")
        
            #send "end"-code to ARDUINO
            self._update_servos(servo_address, 254, 0, 0)
            
            #send "back to normal"-code to ARDUINO
            self._update_servos(servo_address, 0, 0, 0)        
        
    def _update_set_servo_position(self, event=None):
        servo_position = self.servo_position
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_control = self.controller.get_macroparam_val(self.tabClassName, "ServoControl")

    def _update_servo_address(self, event=None):
        self.servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        self.servo_control = self.controller.get_macroparam_val(self.tabClassName, "ServoControl") 
        
    def led_off(self,_event=None):
    # switch off all LED
        self.ledhighlight = False
        if self.controller.mobaledlib_version == 1:
            message = "#L00 00 00 00 FF\n"
        else:
            message = "#L 00 00 00 00 7FFF\n"
        self.controller.send_to_ARDUINO(message)
        #self.controller.ledtable.clear()
        
    def servo_prog_button(self,event=None,code=0):
    # send code to Servo
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_control = self.controller.get_macroparam_val(self.tabClassName, "ServoControl")        
        self._update_servos(servo_address,code,0,0)
        
    def servo_prog_label_pressed(self,event=None,code=0):
    # send code to Servo
        event.widget.config(relief="sunken")
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_control = int(self.controller.get_macroparam_val(self.tabClassName, "ServoControl"))
        servo_position = self.servo_position
        if servo_control in [2, 3]: # add input bit only for pos training
            servo_control += 8 # set input bit
        self._update_servos(servo_address,servo_position,servo_control,0)
        
    def servo_prog_label_released(self,event=None,code=100):
    # send code to Servo
        event.widget.config(relief="raised")
        servo_position = self.servo_position
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_control = int(self.controller.get_macroparam_val(self.tabClassName, "ServoControl"))
        self._update_servos(servo_address,servo_position,servo_control,0)
        
    def _update_servos(self, lednum, positionValueHigh, controlValue, positionValueLow):
        newcontrolValue =  CalculateControlValuewithChecksum (controlValue, positionValueHigh, positionValueLow)
        if self.controller.mobaledlib_version == 1:
            message = "#L" + '{:02x}'.format(lednum) + " " + '{:02x}'.format(positionValueHigh) + " " + '{:02x}'.format(newcontrolValue) + " " + '{:02x}'.format(positionValueLow) + " " + '{:02x}'.format(1) + "\n"
        else:
            message = "#L " + '{:02x}'.format(lednum) + " " + '{:02x}'.format(positionValueHigh) + " " + '{:02x}'.format(newcontrolValue) + " " + '{:02x}'.format(positionValueLow) + " " + '{:02x}'.format(1) + "\n"
        self.controller.send_to_ARDUINO(message)
        time.sleep(0.2)


            


