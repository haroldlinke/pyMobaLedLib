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

Servo_Scale_Min = 10

Servo_Min = 10

Servo_Stop = 0

Servo_Scale_Max = 210
# ----------------------------------------------------------------
# Class ServoTestPage
# ----------------------------------------------------------------

class ServoTestPage(tk.Frame):

    # ----------------------------------------------------------------
    # ServoTestPage __init__
    # ----------------------------------------------------------------

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.tabClassName = "ServoTestPage"
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
        
        self.buttonservostop=tk.Label(servo_direct_position_frame, text="Servo STOP",width=15,height=4,fg="black",relief="raised",font=self.fontbutton)

        self.controller.ToolTip(self.buttonservostop, text="Stop the Servo")
        self.buttonservostop.bind("<ButtonRelease-1>",lambda event: self.servo_prog_label_released(event=event,code=0))
        self.buttonservostop.bind("<Button-1>",lambda event: self.servo_prog_label_pressed(event=event,code=0))        
                

        self.servo_pos_var = tk.DoubleVar()
        self.servo_pos_var.set(0)
        #self.servo_scale = ttk.Scale( servo_direct_position_frame, variable = self.servo_pos_var,command=self._update_servo_position,from_=0,to=220,orient=tk.HORIZONTAL,length=440)
        self.servo_scale = tk.Scale( servo_direct_position_frame, variable = self.servo_pos_var,command=self._update_servo_position,from_=Servo_Scale_Min,to=Servo_Scale_Max,orient=tk.HORIZONTAL,length=440,label="Servo position",tickinterval=20,font=self.fontscale)
        
        self.controller.ToolTip(self.servo_scale, text="Position of Servo 10..220\nAnklicken zum Aktivieren der Tasten:\n[Right]/[Left]\n - single step\n[CTRL-Right]/[CTRL-Left]\n - long step\n[Pos1]/[Ende}\n - Anfang/Ende\n"+
                                "\nKlicken auf dem Sliderfeld:\n<Linke Taste>\n - single step vorwärts/rückwärts\n<Rechte Taste>\n - spring zum angeklickten Wert\n<CTRL Linke Taste>\n - springe zum Anfang/Ende")
        self.servo_scale.focus_set()
        self.servo_scale.bind("<Button-1>", self.servo_scale_focus_set)
        
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
        self.buttonservostop.grid(row=0,column=0,sticky="",padx=20, pady=10)  
        servo_set_pos_speed_frame.grid(row=1, column=0, pady=5, padx=5, sticky="")
        
        #servo_set_speed_frame.grid(row=3, column=1, pady=10, padx=10, sticky="e")
        
        # ------------------- buttons
        show_buttons=False
        if show_buttons:
            button_frame = ttk.Frame(self.tab_frame,relief="ridge", borderwidth=2,width=500)
        
            label1 = ttk.Label(button_frame, text='(Only for testing\nStep 1 - Select Servo').grid(row=1, column=0, sticky='e',
                                                     padx=4, pady=4)
            
            button1=ttk.Button(button_frame, text="T225 Sel Servo 1",width=20, command=lambda: self.servo_prog_button(code=225))
            button1.grid(row=1, column=1, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button1, text="Taster1\n[CTRL-o]")
    
            button2=ttk.Button(button_frame, text="T230 Sel Servo 2",width=20, command=lambda: self.servo_prog_button(code=230))
            button2.grid(row=1, column=2, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button2, text="Taster2")
            
            button3=ttk.Button(button_frame, text="T235 Sel Servo 3",width=20, command=lambda: self.servo_prog_button(code=235))
            button3.grid(row=1, column=3, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button3, text="Taster1\n[CTRL-o]")
    
            label2 = ttk.Label(button_frame, text='Step 2 - Select Task').grid(row=2, column=0, sticky='e',
                                                     padx=4, pady=4)
    
            button4=ttk.Button(button_frame, text="T240 Set Min/Max",width=20, command=lambda: self.servo_prog_button(code=240))
            button4.grid(row=2, column=1, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button4, text="Taster2")
            
            button5=ttk.Button(button_frame, text="T245 Set Speed",width=20, command=lambda: self.servo_prog_button(code=245))
            button5.grid(row=2, column=3, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button5, text="Taster1\n[CTRL-o]")
    
            button6=ttk.Button(button_frame, text="T250 Start",width=20, command=lambda: self.servo_prog_button(code=250))
            button6.grid(row=3, column=2, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button6, text="Taster2")
            
    
            label3 = ttk.Label(button_frame, text='Step 3 - Set Min').grid(row=4, column=0, sticky='e',
                                                     padx=4, pady=4)
            
            label4 = ttk.Label(button_frame, text='Step 4 - Set Max').grid(row=5, column=0, sticky='e',
                                                     padx=4, pady=4)
    
            button9=ttk.Button(button_frame, text="T9 (205) Next step",width=20, command=lambda: self.servo_prog_button(code=205))
            button9.grid(row=5, column=1, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button9, text="Taster2")
    
            label5 = ttk.Label(button_frame, text='Step 5 - use <<,<,>,>> to Set Max').grid(row=6, column=0, sticky='e',
                                                     padx=4, pady=4)
    
            label6 = ttk.Label(button_frame, text='Step 6 - Store Max').grid(row=7, column=0, sticky='e',
                                                     padx=4, pady=4)
            button9a=ttk.Button(button_frame, text="T205 Next step",width=20, command=lambda: self.servo_prog_button(code=205))
            button9a.grid(row=7, column=1, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button9a, text="Taster2")
    
            label6 = ttk.Label(button_frame, text='Step 6 - save and end').grid(row=8, column=0, sticky='e',
                                                     padx=4, pady=4)
            button10=ttk.Button(button_frame, text="T254 Save",width=20, command=lambda: self.servo_prog_button(code=254))
            button10.grid(row=8, column=1, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button10, text="Taster2")
            
            button11=ttk.Button(button_frame, text="T0 Back to normal",width=20, command=lambda: self.servo_prog_button(code=0))
            button11.grid(row=9, column=1, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button10, text="Taster2")                    
            
            button12=ttk.Button(button_frame, text="T220 High Pos",width=20, command=lambda: self.servo_prog_button(code=220))
            button12.grid(row=10, column=1, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button12, text="Taster2")
            
            button13=ttk.Button(button_frame, text="T10 Low Pos",width=20, command=lambda: self.servo_prog_button(code=10))
            button13.grid(row=10, column=3, padx=10, pady=(10, 4), sticky='w')
            self.controller.ToolTip(button13, text="Taster2")
            
            
        set_button_frame = ttk.Frame(servo_program_frame, relief="flat", borderwidth=0)

        button7=tk.Label(set_button_frame, text="Dec <<",width=15,fg="black",relief="raised",font=self.fontbutton)
        button7.grid(row=4, column=1, padx=10, pady=(10, 4), sticky='w')
        self.controller.ToolTip(button7, text="T60 Dec <<")
        button7.bind("<ButtonRelease-1>",lambda event: self.servo_prog_label_released(event=event))
        button7.bind("<Button-1>",lambda event: self.servo_prog_label_pressed(event=event,code=60))
        
        button7a=tk.Label(set_button_frame, text="Dec <",width=15,fg="black",relief="raised",font=self.fontbutton)
        button7a.grid(row=4, column=2, padx=10, pady=(10, 4), sticky='w')
        self.controller.ToolTip(button7a, text="T90 Dec <<")
        button7a.bind("<ButtonRelease-1>",lambda event: self.servo_prog_label_released(event=event))
        button7a.bind("<Button-1>",lambda event: self.servo_prog_label_pressed(event=event,code=90))        
        
        #button7b=ttk.Button(set_button_frame, text="Stop",width=15, command=lambda: self.servo_prog_button(code=100))
        #button7b.grid(row=4, column=3, padx=10, pady=(10, 4), sticky='w')
        #self.controller.ToolTip(button7b, text="T100 Stop")
        
        button8=tk.Label(set_button_frame, text="Inc >",width=15,fg="black",relief="raised",font=self.fontbutton)
        button8.grid(row=4, column=3, padx=10, pady=(10, 4), sticky='w')
        self.controller.ToolTip(button8, text="T110 Inc >")
        button8.bind("<ButtonRelease-1>",lambda event: self.servo_prog_label_released(event=event))
        button8.bind("<Button-1>",lambda event: self.servo_prog_label_pressed(event=event,code=110))
        
        button8a=tk.Label(set_button_frame, text="Inc >>",width=15,fg="black",relief="raised",font=self.fontbutton)
        button8a.grid(row=4, column=4, padx=10, pady=(10, 4), sticky='w')
        self.controller.ToolTip(button8a, text="T140 Dec <<")
        button8a.bind("<ButtonRelease-1>",lambda event: self.servo_prog_label_released(event=event))
        button8a.bind("<Button-1>",lambda event: self.servo_prog_label_pressed(event=event,code=140))               


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
        if show_buttons:
            button_frame.grid(row=3, column=0, pady=0, padx=5,sticky="ew")
        set_button_frame.grid(row=4, column=0, pady=0, padx=5,sticky="ew")
        
        self.tab_frame.grid_columnconfigure(0,weight=1)
        #self.tab_frame.grid_columnconfigure(1,weight=0)
        #self.tab_frame.grid_columnconfigure(2,weight=0)
        #self.tab_frame.grid_columnconfigure(3,weight=1)
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

        #self.setConfigData("lastLed"     , self.v_servo_address.get())
        #self.setConfigData("lastservo_channel", self.v_servo_channel.get())
        #self.setParamData("Lednum"   , self.v_servo_address.get())
        #self.setParamData("servo_channel" , self.v_servo_channel.get())
        
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

    def connect(self):
        pass

    def disconnect(self):
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
            
    def servo_scale_focus_set(self,event=None):
        self.servo_scale.focus_set()

    def _update_servo_channel(self, servo_address, servo_channel, position):
        if servo_channel == 0:
            self._update_servos(servo_address, position, 0, 0)
        elif servo_channel == 1:
            self._update_servos(servo_address, 0, position, 0)
        else:
            self._update_servos(servo_address, 0, 0, position)

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
        if position_int in range(1,Servo_Min): # Limit 
            position_int = Servo_Min

        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_channel = self.controller.get_macroparam_val(self.tabClassName, "ServoChannel")
        self._update_servo_channel(servo_address, servo_channel, position_int)
        
    def _update_servo_speed(self, event=None):
        speed=self.v_speed_0.get()
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_channel = self.controller.get_macroparam_val(self.tabClassName, "ServoChannel")        
        self._update_servos(servo_address, speed, speed, speed)

    def _get_servo_channel_code(self, servo_channel):
        # select the right servo
        if servo_channel == 0:
            return 225
        elif servo_channel == 1:
            return 230
        else:
            return 235

            
    def _cancel_set_min_max_pos(self, event=None):
        # select the right servo
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_channel = self.controller.get_macroparam_val(self.tabClassName, "ServoChannel")
                
        #send code to ARDUINO
        self._update_servos(servo_address, 0, 0, 0)
        
        self.status = "Start Min Pos"
        self.ssp_label2.config(background="white",text="")
        self.button_start_save_mm_pos.config(text="Starte Min-Max Pos/Speed programmieren")
        
    def _save_min_max_pos(self, event=None):
        
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_channel = self.controller.get_macroparam_val(self.tabClassName, "ServoChannel")
        servo_channel_code = self._get_servo_channel_code(servo_channel)        
        
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
        servo_channel = self.controller.get_macroparam_val(self.tabClassName, "ServoChannel")
        servo_channel_code = self._get_servo_channel_code(servo_channel)        
        
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
        servo_position = self.servo_0.get()
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_channel = self.controller.get_macroparam_val(self.tabClassName, "ServoChannel")

    def _update_servo_address(self, event=None):
        self.servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        self.servo_channel = self.controller.get_macroparam_val(self.tabClassName, "ServoChannel") 
        
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
        servo_channel = self.controller.get_macroparam_val(self.tabClassName, "ServoChannel")        
        self._update_servos(servo_address,code,0,0)
        
    def servo_prog_label_pressed(self,event=None,code=0):
    # send code to Servo
        event.widget.config(relief="sunken")
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_channel = self.controller.get_macroparam_val(self.tabClassName, "ServoChannel")        
        self._update_servos(servo_address,code,0,0)
        
    def servo_prog_label_released(self,event=None,code=100):
    # send code to Servo
        event.widget.config(relief="raised")
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_channel = self.controller.get_macroparam_val(self.tabClassName, "ServoChannel")        
        self._update_servos(servo_address,code,0,0)        
        
    def _update_servos(self, lednum, servo_0, servo_1, servo_2):
        if self.controller.mobaledlib_version == 1:
            message = "#L" + '{:02x}'.format(lednum) + " " + '{:02x}'.format(servo_0) + " " + '{:02x}'.format(servo_1) + " " + '{:02x}'.format(servo_2) + " " + '{:02x}'.format(1) + "\n"
        else:
            message = "#L " + '{:02x}'.format(lednum) + " " + '{:02x}'.format(servo_0) + " " + '{:02x}'.format(servo_1) + " " + '{:02x}'.format(servo_2) + " " + '{:02x}'.format(1) + "\n"
        self.controller.send_to_ARDUINO(message)
        time.sleep(0.2)


            


