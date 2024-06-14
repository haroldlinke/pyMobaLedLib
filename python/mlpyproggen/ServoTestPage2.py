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
from tools.CRCalgorithms import CalculateControlValuewithChecksum, CalculateControlValuewithChecksum_old

from mlpyproggen.DefaultConstants import COLORCOR_MAX, DEFAULT_PALETTE, LARGE_FONT, NORMAL_FONT, SMALL_FONT, VERY_LARGE_FONT, PROG_VERSION, PERCENT_BRIGHTNESS, BLINKFRQ
# fromx mlpyproggen.dictFile import saveDicttoFile, readDictFromFile
import mlpyproggen.dictFile as dictFile
from scrolledFrame.ScrolledFrame import VerticalScrolledFrame,HorizontalScrolledFrame,ScrolledFrame
from locale import getdefaultlocale
import re
import time
import logging
import pattgen.D00_Forms as D00

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
        
        self.buttonProgramServo=ttk.Button(servo_direct_position_frame, text="Servo Programmieren", command=self.servo_program_button, style='my.TButton')

        self.controller.ToolTip(self.buttonProgramServo, text="Servo Programm auf den Servo hochladen")
        #self.buttonEnter.bind("<ButtonRelease-1>",lambda event: self.servo_prog_label_released(event=event,code=0))
        #self.buttonEnter.bind("<Button-1>",lambda event: self.servo_prog_label_pressed(event=event,code=0))                

        self.servo_pos_var = tk.DoubleVar()
        self.servo_pos_var.set(0)
        #self.servo_scale = ttk.Scale( servo_direct_position_frame, variable = self.servo_pos_var,command=self._update_servo_position,from_=0,to=220,orient=tk.HORIZONTAL,length=440)
        self.servo_scale = tk.Scale( servo_direct_position_frame, variable = self.servo_pos_var,command=self._update_servo_position,from_=Servo_Scale_Min,to=Servo_Scale_Max,orient=tk.HORIZONTAL,length=440,label="Servo position",tickinterval=20,font=self.fontscale)
        
        self.controller.ToolTip(self.servo_scale, text="Position of Servo 0..255\nAnklicken zum Aktivieren der Tasten:\n[Right]/[Left]\n - single step\n[CTRL-Right]/[CTRL-Left]\n - long step\n[Pos1]/[Ende}\n - Anfang/Ende\n"+
                                "\nKlicken auf dem Sliderfeld:\n<Linke Taste>\n - single step vorwärts/rückwärts\n<Rechte Taste>\n - spring zum angeklickten Wert\n<CTRL Linke Taste>\n - springe zum Anfang/Ende")
        self.servo_scale.focus_set()
        self.servo_scale.bind("<Button-1>", self.servo_scale_focus_set)
        self.servo_position = 0
        
        servo_program_frame =ttk.Frame(self.tab_frame,relief="flat", borderwidth=0,width=500)
        
        # ------------- SERVO Pos
        s = ttk.Style()
        s.configure('my.TButton', font=self.fontbutton)
                
        self.servo_scale.grid(row=0,column=1,sticky="")
        self.buttonEnter.grid(row=0,column=0,sticky="",padx=20, pady=10)
        self.buttonProgramServo.grid(row=0,column=2,sticky="",padx=20, pady=10)  

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

    def _update_servo_position(self, position):
        position_int=int(position)
        self.servo_position = position_int

        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_control = int(self.controller.get_macroparam_val(self.tabClassName, "ServoControl"))
        if servo_control in [1, 2, 3]:

            self._update_servo_channel(servo_address, servo_control, position_int)
        
    def led_off(self,_event=None):
    # switch off all LED
        self.ledhighlight = False
        if self.controller.mobaledlib_version == 1:
            message = "#L00 00 00 00 FF\n"
        else:
            message = "#L 00 00 00 00 7FFF\n"
        self.controller.send_to_ARDUINO(message)
        #self.controller.ledtable.clear()
        
    def servo_program_button(self,event=None,code=0):
    # send code to Servo
        D00.MainMenu_Form.Show(page1=1, page2=3)
        
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

        servo_use_old_crc = int(self.controller.get_macroparam_val(self.tabClassName, "ServoCRCold"))

        if servo_use_old_crc:
            newcontrolValue =  CalculateControlValuewithChecksum_old (controlValue, positionValueHigh, positionValueLow) 
        else:
            newcontrolValue =  CalculateControlValuewithChecksum (controlValue, positionValueHigh, positionValueLow)
        if self.controller.mobaledlib_version == 1:
            message = "#L" + '{:02x}'.format(lednum) + " " + '{:02x}'.format(positionValueHigh) + " " + '{:02x}'.format(newcontrolValue) + " " + '{:02x}'.format(positionValueLow) + " " + '{:02x}'.format(1) + "\n"
        else:
            message = "#L " + '{:02x}'.format(lednum) + " " + '{:02x}'.format(positionValueHigh) + " " + '{:02x}'.format(newcontrolValue) + " " + '{:02x}'.format(positionValueLow) + " " + '{:04x}'.format(1) + "\n"
        self.controller.send_to_ARDUINO(message)
        #time.sleep(0.2)


            


