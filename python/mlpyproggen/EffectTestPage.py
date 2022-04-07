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
from tkinter import ttk, messagebox, filedialog,colorchooser,scrolledtext
from tkcolorpicker.functions import tk, ttk, round2, create_checkered_image, \
    overlay, hsv_to_rgb, hexa_to_rgb, rgb_to_hexa, col2hue, rgb_to_hsv, convert_K_to_RGB
from tkcolorpicker.spinbox import Spinbox
from tkcolorpicker.limitvar import LimitVar
from mlpyproggen.DefaultConstants import COLORCOR_MAX, DEFAULT_PALETTE, LARGE_FONT, SMALL_FONT, VERY_LARGE_FONT, Very_SMALL_FONT, PROG_VERSION, PERCENT_BRIGHTNESS, BLINKFRQ, ARDUINO_WAITTIME, ARDUINO_LONG_WAITTIME, HOUSE_PALETTE2COLOR_PALETTE, SWITCHMACROLIST,SIZEFACTOR,MAC_Version
#from mlpyproggen.dictFile import saveDicttoFile, readDictFromFile
import mlpyproggen.dictFile as dictFile
from scrolledFrame.ScrolledFrame import VerticalScrolledFrame,HorizontalScrolledFrame,ScrolledFrame
from locale import getdefaultlocale
import os
import re
import time
import subprocess
import logging
import platform

SCROLLHEIGHT = 600 # pixel

PERCENT_BRIGHTNESS = 1  # 1 = Show the brightnes as percent, 0 = Show the brightnes as ">>>"# 03.12.19:

COLORCOR_MAX = 255

EFFECT_PALLETTE_COLUMNS = 7

# --- Translation - not used
EN = {}
FR = {"Red": "Rouge", "Green": "Vert", "Blue": "Bleu",
      "Hue": "Teinte", "Saturation": "Saturation", "Value": "Valeur",
      "Cancel": "Annuler", "Color Chooser": "Sélecteur de couleur",
      "Alpha": "Alpha"}
DE = {"Red": "Rot", "Green": "Grün", "Blue": "Blau",
      "Hue": "Farbton", "Saturation": "Sättigung", "Value": "Helligkeit",
      "Cancel": "Beenden", "Color Chooser": "Farbwähler",
      "Alpha": "Alpha", "Configuration": "Einstellungen",
      "SI_1":"Immer An", "Digital Address":"Digital Adresse","Variable":"Variable"
      }

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
        self.right_click_menu.add_command(label="Eintrag löschen", command=self.delete_entry)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="n LEDs herausnehmen", command=self.remove_leds)
        
        self.right_click_menu.add_command(label="n LEDs einfügen", command=self.insert_leds)

    def insert_leds(self):
        label = self.ledlabel #event.widget
        keyint = int(label.key)
        n = self.mainpage.ledcount_int
        self.mainpage.controller.ledeffecttable_insert_leds(keyint,n)
        self.mainpage.update_ledtable_complete()
    
    def popup_text(self, event):
        self.right_click_menu.post(event.x_root, event.y_root)

    def remove_leds(self):
        label = self.ledlabel #event.widget
        keyint = int(label.key)
        n = self.mainpage.ledcount_int
        self.mainpage.controller.ledeffecttable_remove_leds(keyint,n)
        self.mainpage.update_ledtable_complete()

    
    def delete_entry(self):
        label = self.ledlabel #event.widget
        keystr = label.key
        n = self.mainpage.ledcount_int
        self.mainpage.controller.init_ledeffecttable_entries(keyint,n)
        self.mainpage.update_ledtable_complete()

    def menuUndo(self):
        mainpage = self.mainpage
        mainpage.MenuUndo()

        
# ----------------------------------------------------------------
# Class ColorCheckPage
# ----------------------------------------------------------------

class EffectTestPage(tk.Frame):

    # ----------------------------------------------------------------
    # EffectTestPage __init__
    # ----------------------------------------------------------------

    def __init__(self, parent, controller):
        
        BUTTONWIDTH = int(15*SIZEFACTOR)
        
        tk.Frame.__init__(self,parent)
        self.tabClassName = "EffectTestPage"
        self.controller = controller
        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName)        
        self.parent = parent
        self.ledhighlight = False
        self.on_lednum = 0
        self.on_ledcount = 1
        self.on_ledon = False 
        self.continue_loop = False
        self.process=None
        self.current_macro = "House"
        self.effect = self.getConfigData("old_effect")
        self.hexa = "#000000"
        self.palette = self.controller.palette
        self.paletteUndoList = []
        self.paletteRedoList = []
        self.palette_frame = None
        self.old_lednum_int = 0
        self.old_ledcount_int = 1
        self.lednum_int = 0
        self.ledcount_int = 1
        self.macroparam_frame_dict = {}
        self.variableNameList = []
        self.digitalswitchtype = ""
        self.ledhighlight_switch = True
           
        led = self.getConfigData("lastLed")

        ledcount = self.getConfigData("lastLedCount")

        serport = controller.arduino

        self.cor_red = self.getConfigData("led_correction_r")
        self.cor_green = self.getConfigData("led_correction_g")
        self.cor_blue = self.getConfigData("led_correction_b")
        
        self.main_frame = ttk.Frame(self, relief="ridge", borderwidth=2)

        # --- ARDUINO Steuerung

        self.arduino_frame = ttk.Frame(self.main_frame,relief="ridge", borderwidth=2)

        # --- ARDUINO LED

        self.arduino_title = ttk.Label(self.arduino_frame, text="ARDUINO",font=LARGE_FONT,anchor="w")
        self.arduino_title.grid(row=0,column=0,padx=2, pady=(2, 2), sticky='w')
        
        arduino_config_text1 = self.getConfigData("serportname")
        arduino_config_text2 = self.getConfigData("ArduinoTypeName")
        arduino_config_text  = arduino_config_text1 + "\n" + arduino_config_text2
        self.arduino_config = ttk.Label(self.arduino_frame, text=arduino_config_text,font=SMALL_FONT,anchor="w")
        self.arduino_config.grid(row=0,column=1,padx=2, pady=(2, 2), sticky='w')
        

        self.led_frame = ttk.Frame(self.arduino_frame) #, relief="ridge", borderwidth=2)
        self.led_frame.columnconfigure(0, weight=1)        
        self.lednum = LimitVar(0, 255, self)
        self.ledcount = LimitVar(1, 256, self)

        self.lednum.set(self.getConfigData("lastLed"))
        self.ledcount.set(self.getConfigData("lastLedCount"))

        self.s_led = Spinbox(self.led_frame, from_=0, to=255, width=5, name='spinbox',
                        textvariable=self.lednum, command=self._update_led_num)
        self.s_ledcount = Spinbox(self.led_frame, from_=1, to=256, width=5, name='spinbox',
                          textvariable=self.ledcount, command=self._update_led_count)
        self.s_led.delete(0, 'end')
        self.s_led.insert(0, led)
        self.s_led.grid(row=0, column=1, sticky='e', padx=2, pady=2)
        self.s_ledcount.delete(0, 'end')
        self.s_ledcount.insert(1, ledcount)
        self.s_ledcount.grid(row=0, column=3, sticky='e', padx=2, pady=2)
        
        self.lednum_int = int(self.s_led.get())
        self.ledcount_int = int(self.s_ledcount.get())
        self.old_ledcount_int = self.ledcount_int
        self.old_lednum_int = self.lednum_int

        ttk.Label(self.led_frame, text=_('Anschluss')).grid(row=0, column=0, sticky='e', padx=2, pady=2)
        ttk.Label(self.led_frame, text=_('Anzahl')).grid(row=0, column=2, sticky='e', padx=2, pady=2)

        self.led_frame.grid(row=1,column=0,columnspan=2,padx=2,pady=(2, 2),sticky="w")
        self.controller.ToolTip(self.led_frame, text="Anschluss/Anschlüsse, die gerade aktiv sind\n[Ctrl-Right/Left] \nAnzahl der Anschlüsse, die gerade aktiv sind\n[Ctrl-Up/Down] ")
        
        ledoff_button=ttk.Button(self.arduino_frame, text="Alle LED aus",width=BUTTONWIDTH, command=self.led_off)
        ledoff_button.grid(row=2, column=0, padx=2, pady=(2, 2), sticky='w')
        self.controller.ToolTip(ledoff_button, text="Alle LED ausschalten\n[CTRL-o]")

        self.blinkoff_button=ttk.Button(self.arduino_frame, text="Blinken Aus",width=BUTTONWIDTH, command=self.blinking_on_off)
        self.blinkoff_button.grid(row=2, column=1, padx=2, pady=(2, 2), sticky='e')
        self.controller.ToolTip(self.blinkoff_button, text="Schaltet das Blinken der LED an oder aus")
        filename = r"/images/ML_icon_send_to_arduino.gif"
        filedir = os.path.dirname(os.path.realpath(__file__))
        filedir2 = os.path.dirname(filedir)
        filepath = filedir2 + filename       
        self.send_icon = tk.PhotoImage(file=filepath)
        self.send_effect_button=ttk.Button(self.arduino_frame, text="Send to ARDUINO", image=self.send_icon, command=self.upload_to_ARDUINO)
        self.send_effect_button.grid(row=0, column=2, rowspan=3)
        self.controller.ToolTip(self.send_effect_button, text="Sendet komplette LED-liste mit den Effekten an den ARDUINO")        

        # --- Group Frame
        self.group_name = self.getConfigData("group_name")
        scroll_groupframe = True
        if scroll_groupframe:
            self.scrolledgroupframe = HorizontalScrolledFrame(self.main_frame)
            self.group_frame=self.create_group_frame(self.group_name,self.scrolledgroupframe.interior)
            self.scrolledgroupframe.grid(row=0,column=1,sticky="nesw")
        else:
            self.group_frame=self.create_group_frame(self.group_name,self.main_frame)
        
        self.effectpalette = self.getConfigData("effectpalette")
        self.update_effectpalette()        
        self.palette = self.effectpalette.get(self.current_macro,{})
        
        # --- define container for tabs
        scroll_macroframe = False
        if scroll_macroframe:
            self.scrolledmacroframe = HorizontalScrolledFrame(self.main_frame)
            self.macro_effect_frame = ttk.Frame(self.scrolledmacroframe.interior,relief="ridge", borderwidth=2)
            self.scrolledmacroframe.grid(row=0,column=1,sticky="nesw")
            self.scrolledmacroframe.grid_columnconfigure(1,weight=1)
        else:     
            self.macro_effect_frame = ttk.Frame(self.main_frame,relief="ridge", borderwidth=2)
        self.main_frame.grid_columnconfigure(1,weight=1)
        self.main_frame.grid_rowconfigure(1,weight=1)
        
        self.macro_effect_frame.grid_rowconfigure(1,weight=1)
        self.macro_effect_frame.grid_columnconfigure(0,weight=1)
        self.macro_effect_title = ttk.Label(self.macro_effect_frame, text="Macros und Effekte",font=LARGE_FONT)
        
        self.container = ttk.Notebook(self.macro_effect_frame)
        self.tabdict = dict()
        self.macro_tab_dict = self.generate_macro_tab_dict()
        for tabName in [" Start","House","GasLights","Light Macros","Sound Macros","Set Macros","Import"]:
            macro_frame = ttk.Frame(self.container, relief="ridge", borderwidth=2)
            self.tabdict[tabName] = {}
            self.tabdict[tabName]["macro_frame"] = macro_frame
            self.container.add(macro_frame, text=tabName)
            if tabName in ["House","GasLights"]:
                scroll_macroparamframe = True
                if scroll_macroparamframe:
                    self.scrolledmacroparamframe = HorizontalScrolledFrame(macro_frame)
                    macroparam_frame = self.create_macroparam_hidden_frames(self.scrolledmacroparamframe.interior, tabName)
                    self.scrolledmacroparamframe.grid(row=0,column=0, pady=(2, 2), padx=2, sticky="nesw")
                    #self.scrolledmacroparamframe.grid_columnconfigure(0,weight=1)
                    #self.scrolledmacroparamframe.grid_rowconfigure(0,weight=1)
                else:   
                    macroparam_frame = self.create_macroparam_hidden_frames(macro_frame, tabName)
                macroparam_frame.grid_rowconfigure(0,weight=1)
                macroparam_frame.grid_columnconfigure(1,weight=1)                
                self.tabdict[tabName]["macroparam_frame"] = macroparam_frame
                
                macroeffect_scrollframe = ScrolledFrame(macro_frame)
                #macroeffect_scrollframe = VerticalScrolledFrame(macro_frame)
                #macroeffect_scrollframe = ScrolledWindow(macro_frame)
                macroeffect_scrollframe.grid(row=1,column=0,sticky="nesw")
                #macroeffect_scrollframe.grid_rowconfigure(0,weight=1)
                #macroeffect_scrollframe.grid_rowconfigure(1,weight=1)
                #macroeffect_scrollframe.grid_columnconfigure(0,weight=1)
                macroeffect_frame = ttk.Frame(macroeffect_scrollframe.interior, borderwidth=0)
                #macroeffect_frame = ttk.Frame(macroeffect_scrollframe.scrollwindow, borderwidth=0)
                macroeffect_frame.grid(row=0,column=0, columnspan=1, pady=(2, 2), padx=2, sticky="nesw")
                
                self.tabdict[tabName]["macroeffect_frame"] = macroeffect_frame
                self.create_effect_palette(tabName, macroeffect_frame)
                macroparam_frame.grid(row=0,column=0, pady=(2, 2), padx=2, sticky="nesw")
            elif tabName == " Start":
                macrolist = self.macro_tab_dict.get(tabName,{})
                macrodata = self.controller.MacroDef.data.get(macrolist[0],{})
                content = macrodata.get("Content",{})
                
                if content != {}:
                    text_widget = tk.Text(macro_frame, wrap=tk.WORD, relief=tk.RIDGE,bg=self.cget('bg'))
                    text_scroll = tk.Scrollbar(macro_frame, command=text_widget.yview)
                    text_widget.configure(yscrollcommand=text_scroll.set)                    
                    for titel,text in content.items():
                        text_widget.tag_configure('bold_italics', font=('Verdana', 10, 'bold', 'italic'))
                        text_widget.tag_configure('big', font=('Verdana', 14, 'bold'))
                        text_widget.tag_configure('normal', font=('Verdana', 10, ))
                        text_widget.insert(tk.END,"\n"+titel+"\n", 'big')
                        text_widget.insert(tk.END, text, 'normal')
                    text_widget.grid(row=0,column=0,rowspan=2,padx=10,pady=10,sticky="nesw")
                    text_scroll.grid(row=0,column=1,rowspan=2,padx=10,pady=10,sticky="ns")
                    #text_widget.pack(side=tk.LEFT,fill=tk.BOTH,padx=10,pady=10)
                    
                    #text_scroll.pack(side=tk.RIGHT,fill=tk.Y)
                    text_widget.config(state=tk.DISABLED)
            else:
                if True:
                    scroll_macroparamframe = True
                    if scroll_macroparamframe:
                        self.scrolledmacroparamframe = HorizontalScrolledFrame(macro_frame)
                        macroparam_frame = self.create_macroparam_hidden_frames(self.scrolledmacroparamframe.interior, tabName)
                        self.scrolledmacroparamframe.grid(row=0,column=0, pady=(2, 2), padx=2, sticky="nesw")
                        #self.scrolledmacroparamframe.grid_columnconfigure(0,weight=1)
                    else:   
                        macroparam_frame = self.create_macroparam_hidden_frames(macro_frame, tabName)
                    #macroparam_frame.grid_rowconfigure(0,weight=1)
                    #macroparam_frame.grid_columnconfigure(0,weight=1)                                
                    #macroparam_frame = self.create_macroparam_hidden_frames(macro_frame, tabName)
                    self.tabdict[tabName]["macroparam_frame"] = macroparam_frame
                    #macrolist_scrollframe = VerticalScrolledFrame(macro_frame)
                    macrolist_scrollframe = ScrolledFrame(macro_frame)                    
                    macrolist_frame = self.create_macrolist_frame(macrolist_scrollframe.interior, tabName)
                    self.tabdict[tabName]["macrolist_frame"] = macrolist_frame
                    self.tabdict[tabName]["macrolist_scrollframe"] = macrolist_scrollframe
                    macrolist_scrollframe.grid(row=1,column=0,sticky="nesw", pady=(2, 2), padx=2)
                    macrolist_frame.grid(row=0,column=0, columnspan=1, pady=(2, 2), padx=2, sticky="nesw")
                    #macrolist_scrollframe.grid_rowconfigure(0,weight=1)
                    macroparam_frame.grid(row=0,column=0, columnspan=1, pady=(2, 2), padx=2, sticky="nesw")
            macro_frame.grid_rowconfigure(0, weight=0)
            macro_frame.grid_rowconfigure(1, weight=1)
            macro_frame.grid_columnconfigure(0, weight=1)
            self.container.grid_columnconfigure(0,weight=1)
     
        self.container.bind("<<NotebookTabChanged>>",self.TabChanged)
        
        self.macro_effect_title.grid(row=0,column=0, pady=(2, 2), padx=2, sticky="w")
        self.container.grid(row=1,column=0,pady=(2, 2), padx=2, sticky="nesw")

        #   LEDList
        self.ledlist_mainframe = ttk.Frame(self.main_frame, relief="ridge", borderwidth=1)
        
        self.ledlist_title = ttk.Label(self.ledlist_mainframe, text="LED Liste",font=LARGE_FONT,anchor="w")
        self.ledlist_scrollframe = VerticalScrolledFrame(self.ledlist_mainframe)
        self.ledlist_title.pack(side="top",padx=2,pady=(2,2),fill="x")
        self.ledlist_scrollframe.pack(side="top", fill="both", expand = True,padx=2,pady=(2,2))
        
        self.controller.ledeffecttable.set_ledlist_cmd(self.ledlist_cmd, self.ledlist_shift_cmd)

        self.controller.ledeffecttable.create_ledlist_frame_content(self.ledlist_scrollframe.interior, self)

        # --- placement
        self.main_frame.grid(row=0, column=0, columnspan=1, pady=(2, 2), padx=2, sticky="nsew")

        self.arduino_frame.grid(row=0, column=0, columnspan=1,pady=(2, 2), padx=2, sticky="nsew")
        self.group_frame.grid(row=0,column=1, pady=(2, 2), padx=2, sticky="nesw")
        self.ledlist_mainframe.grid(row=1,column=0,rowspan=1,pady=(2, 2), padx=2, sticky="nesw")
        self.macro_effect_frame.grid(row=1,column=1, columnspan=1, rowspan=4,pady=(2, 2), padx=2, sticky="nesw")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)        
        
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        self.group_frame.columnconfigure(1, weight=1)
        self.group_frame.rowconfigure(1, weight=1)

        self.ledlist_mainframe.grid_rowconfigure(0,weight=1)
        self.ledlist_mainframe.grid_columnconfigure(0,weight=1)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # --- bindings
        #self.s_led.bind("<FocusOut>", self._update_led_num)
        self.s_led.bind("<Return>", self._update_led_num)
        self.s_led.bind("<Control-a>", self._select_all_entry)
        #self.s_ledcount.bind("<FocusOut>", self._update_led_count)
        self.s_ledcount.bind("<Return>", self._update_led_count)
        self.s_ledcount.bind("<Control-a>", self._select_all_entry)        

        self.controller.bind("<Control-Down>",self.s_led.invoke_buttonup)
        self.controller.bind("<Control-Up>",self.s_led.invoke_buttondown)
        self.controller.bind("<Control-Right>",self.s_ledcount.invoke_buttonup)
        self.controller.bind("<Control-Left>",self.s_ledcount.invoke_buttondown)
        self.controller.bind("<F1>",self.controller.call_helppage)
        self.controller.bind("<Alt-F4>",self.cancel)
        self.controller.bind("<Control-o>",self.led_off)
        self.controller.bind("<Control-z>",self.controller.MenuUndo)
        self.controller.bind("<Control-y>",self.controller.MenuRedo)
 
    def cancel(self,_event=None):
        try:
            #self.led_off()
            pass
        except:
            pass
        self.setConfigData("old_effect"  , self.effect)

    def lednum_up(self,event=None):
        led = int(self.lednum.get())
        led +=1
        ledcount = int(self.ledcount.get())
        ledcnt_max = int(self.controller.get_maxLEDcnt())*3 # number of LED connectors RGB
        if led+ledcount > ledcnt_max:
            ledcount = ledcnt_max-led
            self.ledcount.set(ledcount)
        self.lednum.set(led)
        self._update_ledtable_activestatus(led,1)
        self._show_macroparams(led)
        
    def lednum_down(self,event=None):
        led = int(self.lednum.get())
        led -=1
        if led< 0:
            led = 0
        self.lednum.set(led)
        self._update_ledtable_activestatus(led,1)
        self._show_macroparams(led)            

        
    def tabselected(self):
        logging.debug("Tabselected: %s",self.tabname)
        arduino_config_text1 = self.getConfigData("serportname")
        arduino_config_text2 = self.getConfigData("ArduinoTypeName")
        arduino_config_text  = arduino_config_text1 + "\n" + arduino_config_text2
        self.arduino_config.config(text=arduino_config_text)        
        
        self.controller.unbind("<Control-Down>")
        self.controller.unbind("<Control-Up>")
        self.controller.unbind("<Control-Right>")
        self.controller.unbind("<Control-Left>")        
        
        self.controller.bind("<Control-Down>",self.s_led.invoke_buttonup)
        #self.controller.bind("<Control-Down>",self.lednum_down)
        self.controller.bind("<Control-Up>",self.s_led.invoke_buttondown)
        #self.controller.bind("<Control-Up>",self.lednum_up)
        self.controller.bind("<Control-Right>",self.s_ledcount.invoke_buttonup)
        self.controller.bind("<Control-Left>",self.s_ledcount.invoke_buttondown)
        self.controller.bind("<F1>",self.controller.call_helppage)
        self.controller.bind("<Alt-F4>",self.cancel)
        self.controller.bind("<Control-o>",self.led_off)
        self.controller.bind("<Control-z>",self.controller.MenuUndo)
        self.controller.bind("<Control-y>",self.controller.MenuRedo)
        self.update_ledtable_complete()
        
        #self.controller.connect()
        self.controller.ARDUINO_begin_direct_mode()
        
        #self.controller.send_to_ARDUINO("#BEGIN")
        #time.sleep(ARDUINO_WAITTIME)            

        logging.info(self.tabname)
        pass
    
    def tabunselected(self):
        logging.debug("Tabunselected: %s",self.tabname)
        
        self.switchoff_blink_led()
        #time.sleep(ARDUINO_LONG_WAITTIME) 
        self.controller.ARDUINO_end_direct_mode()
        #self.controller.send_to_ARDUINO("#END")
        #time.sleep(ARDUINO_LONG_WAITTIME)
        
        self.controller.lednum_int = self.lednum_int
        self.controller.ledcout_int = self.ledcount_int
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
            
    def MenuUndo(self,_event=None):
        if self.paletteUndoList:
            undoEntry = self.paletteUndoList.pop()
            self.palette.update(undoEntry)
            self._palette_redraw_colors(self.macroeffect_frame)
        pass
    
    def MenuRedo(self,_event=None):
        pass
    
    # ----------------------------------------------------------------
    # Event TabChanged
    # ----------------------------------------------------------------        
    def TabChanged(self,_event=None):
        pass

    def bind_right_click_menu_to_palettelabel(self, palettelabel):
        self.popup = RightClickMenu(self.master, palettelabel,self)        
        palettelabel.bind("<Button-3>", self.popup.popup_text)
        
    # ----------------------------------------------------------------
    # show_frame byName
    # ----------------------------------------------------------------
    def showFramebyName(self, pageName):
        frame = self.tabdict.get(pageName,None)
        if frame == None:
            pageName = "Start"
            frame = self.tabdict.get(pageName,None)
        self.container.select(self.tabdict[pageName]["macro_frame"])    
    
    def update_GroupComboValues(self):
        
        combo_value_list = list(self.controller.ledeffecttable.mledgrouptable.keys())
        combo_text_list = []
        
        paramvar = self.controller.macroparams_var["Group"]["Group_Name"]
        paramvar["value"] = combo_value_list

        paramvar.keyvalues = combo_value_list
        paramvar.textvalues = combo_text_list
        
    def GroupComboSelected(self,event):
        
        #paramvar = self.controller.macroparams_var["Group"]["Group_Name"]
        paramvar = event.widget
        
        groupname = paramvar.get()
        
        group_dict = self.controller.ledeffecttable.mledgrouptable.get(groupname,{})
        group_param_dict = group_dict.get("params",{})
        if group_param_dict != {}:
            self.set_all_macroparam_val("Group",group_param_dict)
        
    
    def setgroupcolor(self,color):
        if not color:
            color ="#FFFFFF"
        color_fg = self.controller.determine_fg_color(color)
        self.colorlabel.config(bg=color,fg=color_fg)        

        paramvar = self.controller.macroparams_var["Group"]["Group_Colour"]
        paramvar.delete(0, 'end')
        paramvar.insert(0, color)
    
    
    def choosecolor(self):
        paramvar = self.controller.macroparams_var["Group"]["Group_Colour"]
        old_color=paramvar.get()        
        color = colorchooser.askcolor(color=old_color)
        
        if color:
            colorhex = color[1]
            self.setgroupcolor(colorhex)
            
    def checkcolor(self,_event=None):
        self.controller.showFramebyName("ColorCheckPage")
        
        
    def generate_macro_tab_dict(self):
        
        macro_tab_dict = {}
        for key in self.controller.MacroDef.data.keys():
            #logging.info (key)
            macro_data = self.controller.MacroDef.data.get(key,{})
            new_tabname = macro_data.get("TabName","")
            if new_tabname != "":
                macro_tab_list = macro_tab_dict.get(new_tabname,[])
                if macro_tab_list == []:
                    macro_tab_dict[new_tabname] = [key]
                else:
                    macro_tab_dict[new_tabname].append(key)
        
        return macro_tab_dict
    
    def _update_value(self,macro,paramkey):
        logging.debug("update_value: %s - %s",macro,paramkey)
        tabframe=self.controller.getFramebyName(macro)
        if tabframe!=None:
            tabframe._update_value(paramkey)

        
    def xcreate_macroparam_content(self,parent_frame, macro, macroparams,extratitleline=False,maxcolumns=5, startrow=0, minrow=4):
        
        MACROLABELWIDTH = int(15*SIZEFACTOR)
        MACRODESCWIDTH = int(20*SIZEFACTOR)
        MACRODESCWRAPL = int(120*SIZEFACTOR)
        
        PARAMFRAMEWIDTH = int(105*SIZEFACTOR)
        
        PARAMLABELWIDTH = int(15*SIZEFACTOR)
        PARAMLABELWRAPL = int(100*SIZEFACTOR)      
        
        PARAMSPINBOXWIDTH = 6
        PARAMENTRWIDTH = int(16*SIZEFACTOR)
        PARAMCOMBOWIDTH = int(16*SIZEFACTOR)
        
        STICKY = "nw"
        ANCHOR = "center"
        
        if extratitleline:
            titlerow=0
            valuerow=1
            titlecolumn=0
            valuecolumn=0
            deltarow = 2
            deltacolumn = 1
        else:
            titlerow = 0
            valuerow = 0
            titlecolumn = 0
            valuecolumn = 1
            deltarow = 1
            deltacolumn = 2
        
        column = 0
        row = startrow

        for paramkey in macroparams:
            paramconfig_dict = self.controller.MacroParamDef.data.get(paramkey,{})
            param_min = paramconfig_dict.get("Min",0)
            param_max = paramconfig_dict.get("Max",255)
            param_title = paramconfig_dict.get("Input Text","")
            param_tooltip = paramconfig_dict.get("Hint","")
            param_persistent = (paramconfig_dict.get("Persistent","False") == "True")
            param_configname = paramconfig_dict.get("ConfigName",paramkey)
            param_default = paramconfig_dict.get("Default","")
            param_allow_value_entry = (paramconfig_dict.get("AllowValueEntry","False") == "True")
            param_value_change_event = (paramconfig_dict.get("ValueChangeEvent","False") == "True")
            param_hide = (paramconfig_dict.get("Hide","False") == "True")
            param_value_scrollable = (paramconfig_dict.get("Scrollable","False") == "True")            
            
            if param_persistent:
                configData = self.getConfigData(paramkey)
                if configData != "":
                    param_default = configData
            param_readonly = (paramconfig_dict.get("ReadOnly","False") == "True")
            param_type = paramconfig_dict.get("Type","")

            if param_title == "":
                param_title = paramkey
            if param_type == "": # number value param
                
                label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,wraplength = PARAMLABELWRAPL)
                label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.controller.ToolTip(label, text=param_tooltip)
                if param_max == "":
                    param_max = 255
                paramvar = LimitVar(param_min, param_max, parent_frame)
                paramvar.set(param_default)
                paramvar.key = paramkey
                
                if param_value_change_event:
                    s_paramvar = Spinbox(parent_frame, from_=param_min, to=param_max, width=PARAMSPINBOXWIDTH, name='spinbox', textvariable=paramvar,command=lambda:self._update_value(macro,paramkey))
                else:
                    s_paramvar = Spinbox(parent_frame, from_=param_min, to=param_max, width=PARAMSPINBOXWIDTH, name='spinbox', textvariable=paramvar)

                s_paramvar.delete(0, 'end')
                s_paramvar.insert(0, param_default)
                s_paramvar.grid(row=row+valuerow, column=column+valuecolumn, padx=2, pady=2)
                s_paramvar.key = paramkey
                
                param_bind_up   = paramconfig_dict.get("Key_Up","")
                param_bind_down = paramconfig_dict.get("Key_Down","")
                
                if param_bind_up != "":
                    self.bind(param_bind_up,s_paramvar.invoke_buttonup)
                    s_paramvar.key_up=param_bind_up
                    if self.bind_keys_dict.get(macro,{})=={}:
                        self.bind_keys_dict[macro] = {}
                    self.bind_keys_dict[macro][paramkey] = s_paramvar
                if param_bind_down != "":    
                    self.bind(param_bind_down,s_paramvar.invoke_buttondown)
                    s_paramvar.key_down=param_bind_down
                    self.bind_keys_dict[macro][paramkey] = s_paramvar                
            
                self.set_macroparam_var(macro, paramkey, paramvar)
                
                column = column + deltacolumn
                if column > maxcolumns:
                    column = 0
                    row=row+deltarow                    
                
            if param_type == "Time": # Time value param
                
                label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
                label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.controller.ToolTip(label, text=param_tooltip)
                
                
                paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH)
                paramvar.delete(0, 'end')
                paramvar.insert(0, param_default)
                paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                paramvar.key = paramkey
            
                self.set_macroparam_var(macro, paramkey, paramvar)                

                column = column + deltacolumn
                if column > maxcolumns:
                    column = 0
                    row=row+deltarow      
                    
            if param_type == "String": # String value param
                
                label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
                label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.controller.ToolTip(label, text=param_tooltip)
                
                
                paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH)
                
                if param_value_change_event:
                    paramvar.bind("<Return>",self._key_return)     
                
                paramvar.delete(0, 'end')
                paramvar.insert(0, param_default)
                paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                paramvar.key = paramkey
                paramvar.macro = macro
            
                self.set_macroparam_var(macro, paramkey, paramvar)                

                column = column + deltacolumn
                if column > maxcolumns:
                    column = 0
                    row=row+deltarow
            
            if param_type == "BigEntry": # Text value param
                
                label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
                label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.controller.ToolTip(label, text=param_tooltip)
                
                paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH*3)
                

                if param_value_change_event:
                    paramvar.bind("<Return>",self._key_return)
                                
                paramvar.delete(0, 'end')
                paramvar.insert(0, param_default)
                paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                paramvar.key = paramkey
                paramvar.macro = macro
            
                self.set_macroparam_var(macro, paramkey, paramvar)                

                column = column + deltacolumn
                if column > maxcolumns:
                    column = 0
                    row=row+deltarow
                    
            if param_type == "Text": # Text value param
                if not param_hide:
                    label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,wraplength = PARAMLABELWRAPL,anchor=ANCHOR)
                    label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                    self.controller.ToolTip(label, text=param_tooltip)
                
                number_of_lines = param_tooltip = paramconfig_dict.get("Lines","")
                if number_of_lines == "":
                    number_of_lines = "2"
                    
                paramvar = tk.Text(parent_frame,width=PARAMENTRWIDTH*3,height=int(number_of_lines))                
                
                paramvar.delete("1.0", "end")
                paramvar.insert("end",param_default)
                if not param_hide:
                    paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                paramvar.key = paramkey
                
                if param_readonly:
                    paramvar.state = "disabled"
            
                self.set_macroparam_var(macro, paramkey, paramvar)                
    
                column = column + deltacolumn
                if column > maxcolumns:
                    column = 0
                    row=row+deltarow            
        
            
                    
            if param_type == "Checkbutton": # Checkbutton param
                paramvar = tk.IntVar()
                paramvar.key = paramkey
                
                label=ttk.Checkbutton(parent_frame, text=param_title,width=PARAMLABELWIDTH,variable=paramvar)
                label.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                self.controller.ToolTip(label, text=param_tooltip)                
            
                self.set_macroparam_var(macro, paramkey, paramvar)                

                column = column + deltacolumn
                if column > maxcolumns:
                    column = 0
                    row=row+deltarow

                
            if param_type == "Combo": # Combolist param
                
                label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
                label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.controller.ToolTip(label, text=param_tooltip)
                
                if param_allow_value_entry:
                    paramvar = ttk.Combobox(parent_frame, width=PARAMCOMBOWIDTH)
                else:                
                    paramvar = ttk.Combobox(parent_frame, state="readonly", width=PARAMCOMBOWIDTH)                
                
                combo_value_list = paramconfig_dict.get("KeyValues",paramconfig_dict.get("Values",[]))
                combo_text_list = paramconfig_dict.get("ValuesText",[])
                
                if combo_text_list == []:
                    paramvar["value"] = combo_value_list
                else:
                    paramvar["value"] = combo_text_list
                    
                paramvar.current(0) #set the selected view                    
                
                paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                paramvar.key = paramkey
                paramvar.keyvalues = combo_value_list
                paramvar.textvalues = combo_text_list
            
                self.set_macroparam_var(macro, paramkey, paramvar)
                            

                column = column + deltacolumn
                if column > maxcolumns:
                    column = 0
                    row=row+deltarow      
                    
            if param_type == "GroupCombo": # Combolist param
                
                label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
                label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.controller.ToolTip(label, text=param_tooltip)
                
                paramvar = ttk.Combobox(parent_frame, width=PARAMCOMBOWIDTH,postcommand=self.update_GroupComboValues)
                combo_value_list = list(self.controller.ledeffecttable.mledgrouptable.keys())
                combo_text_list = []
                
                if combo_text_list == []:
                    paramvar["value"] = combo_value_list
                else:
                    paramvar["value"] = combo_text_list
                    
                paramvar.current(0) #set the selected view                    
                
                paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                paramvar.key = paramkey
                paramvar.keyvalues = combo_value_list
                paramvar.textvalues = combo_text_list
                paramvar.bind("<<ComboboxSelected>>", self.GroupComboSelected)
            
                self.set_macroparam_var(macro, paramkey, paramvar)               

                column = column + deltacolumn
                if column > maxcolumns:
                    column = 0
                    row=row+deltarow                          
                    
            if param_type == "CX": # Channel value param
                
                label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
                label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.controller.ToolTip(label, text=param_tooltip)
                
                
                paramvar = ttk.Combobox(parent_frame, width=PARAMCOMBOWIDTH)
                
                combo_value_list = paramconfig_dict.get("KeyValues",paramconfig_dict.get("Values",("C_All", "C12", "C23", "C1", "C2", "C3", "C_RED", "C_GREEN", "C_BLUE", "C_WHITE", "C_YELLOW", "C_CYAN")))
                combo_text_list = paramconfig_dict.get("ValuesText",[])
                
                if combo_text_list == []:
                    paramvar["value"] = combo_value_list
                else:
                    paramvar["value"] = combo_text_list                    
                
                paramvar.current(0) #set the selected colorview                    
                
                paramvar.grid(row=row+valuerow, column=column+valuecolumn, columnspan=1, sticky=STICKY, padx=2, pady=2)
                paramvar.key = paramkey
                paramvar.keyvalues = combo_value_list
                paramvar.textvalues = combo_text_list
            
                self.set_macroparam_var(macro, paramkey, paramvar)                

                column = column + deltacolumn
                if column > maxcolumns:
                    column = 0
                    row=row+deltarow      
            

            if param_type == "Multipleparams": # Multiple params
                #logging.debug ("%s-%s",macro,param_type)
                if row >1 or column>0: 
                    row += deltarow
                    column = 0
                
                label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
                label.grid(row=row+titlerow, column=column+titlecolumn, rowspan=2, sticky=STICKY, padx=10, pady=10)
                self.controller.ToolTip(label, text=param_tooltip)
                
                repeat_number = paramconfig_dict.get("Repeat","")
                
                if repeat_number == "":                
                    
                    multipleparam_frame = ttk.Frame(parent_frame)
                    multipleparam_frame.grid(row=row,rowspan=2,column=column+1 ,columnspan=6,sticky='nesw', padx=10, pady=10)
                    
                    multipleparams = paramconfig_dict.get("MultipleParams",[])
                    
                    if multipleparams != []:
                        self.create_macroparam_content(multipleparam_frame,macro, multipleparams,extratitleline=True,maxcolumns=maxcolumns-1,minrow=0)
                        
                    separator = ttk.Separator (parent_frame, orient = tk.HORIZONTAL)
                    separator.grid (row = row+2, column = 0, columnspan= 10, padx=10, pady=10, sticky = "ew")
           
                    column = column + deltacolumn
                    column = 0
                    row=row+3
                else:
                    repeat_number_int = int(repeat_number)
                    
                    repeat_max_columns = 6
                    
                    for i in range(repeat_number_int):
                        repeat_macro=macro+"."+paramkey+"."+str(i)

                        multipleparam_frame = ttk.Frame(parent_frame)
                        multipleparam_frame.grid(row=row,column=column+1 ,columnspan=10,sticky='nesw', padx=0, pady=0)
                        
                        multipleparams = paramconfig_dict.get("MultipleParams",[])
                        
                        if multipleparams != []:
                            self.create_macroparam_content(multipleparam_frame,repeat_macro, multipleparams,extratitleline=extratitleline,maxcolumns=repeat_max_columns,minrow=0,style=style)
               
                        column = 0
                        row=row+1                    
                
            if param_type == "Color": # Color value param
                
                self.colorlabel = tk.Button(parent_frame, text=param_title, width=PARAMLABELWIDTH, height=2, wraplength=PARAMLABELWRAPL,relief="raised", background=param_default,borderwidth=1,command=self.choosecolor)
                #label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,bg=param_default,borderwidth=1)
                self.colorlabel.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.controller.ToolTip(self.colorlabel, text=param_tooltip)
                
                paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH)
                paramvar.delete(0, 'end')
                paramvar.insert(0, param_default)
                paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                paramvar.key = paramkey
            
                self.set_macroparam_var(macro, paramkey, paramvar)                

                column = column + deltacolumn
                if column > maxcolumns:
                    column = 0
                    row=row+deltarow
                    
            if param_type == "ColTab": # Color value param
                
                self.coltablabel = tk.Button(parent_frame, text=param_title, width=PARAMLABELWIDTH, height=2, wraplength=PARAMLABELWRAPL,relief="raised", borderwidth=1,command=self.checkcolor)
                #label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,bg=param_default,borderwidth=1)
                self.coltablabel.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.controller.ToolTip(self.coltablabel, text=param_tooltip)
                
                #paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH)
                #paramvar.delete(0, 'end')
                #paramvar.insert(0, param_default)
                #paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                #paramvar.key = paramkey
            
                #self.set_macroparam_var(macro, paramkey, paramvar)
                
                self.create_color_palette(parent_frame)

                column = 0
                row=row + 4
                    
            if param_type == "Var": # Combolist param
                
                label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
                label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.controller.ToolTip(label, text=param_tooltip)
                
                if param_allow_value_entry:
                    paramvar = ttk.Combobox(parent_frame, width=PARAMCOMBOWIDTH)
                else:                
                    paramvar = ttk.Combobox(parent_frame, state="readonly", width=PARAMCOMBOWIDTH)                
                
                combo_value_list = paramconfig_dict.get("KeyValues",paramconfig_dict.get("Values",[]))
                combo_text_list = paramconfig_dict.get("ValuesText",[])
                
                if combo_text_list != []:
                    paramvar["value"] = combo_text_list
                elif combo_value_list != []:
                    paramvar["value"] = combo_value_list
                else:
                    paramvar["value"] = ["Variable"]
                    
                paramvar.current(0) #set the selected view                    
                
                paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                paramvar.key = paramkey
                paramvar.keyvalues = combo_value_list
                paramvar.textvalues = combo_text_list
            
                self.set_macroparam_var(macro, paramkey, paramvar)
                            

                column = column + deltacolumn
                if column > maxcolumns:
                    column = 0
                    row=row+deltarow                  
        
        if (column<maxcolumns+1) and (column>0):
            for i in range(column,maxcolumns+1):
                label=tk.Label(parent_frame, text=" ",width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
                label.grid(row=row,column=i,sticky=STICKY, padx=2, pady=2)
        
        if maxcolumns > 5:        
            seplabel=tk.Label(parent_frame, text="",width=int(90*SIZEFACTOR),height=1)
            seplabel.grid(row=row+2, column=0, columnspan=10,sticky='ew', padx=2, pady=2)

    def create_macroparam_frame(self,parent_frame, macro):
        
        MACROLABELWIDTH = int(15*SIZEFACTOR)
        MACRODESCWIDTH = int(20*SIZEFACTOR)
        MACRODESCWRAPL = int(120*SIZEFACTOR)
        BUTTONLABELWIDTH = int(10*SIZEFACTOR)
        PARAMFRAMEWIDTH = int(105*SIZEFACTOR)
        
        PARAMLABELWIDTH = int(15*SIZEFACTOR)
        PARAMLABELWRAPL = int(100*SIZEFACTOR)      
        
        PARAMSPINBOXWIDTH = 4
        PARAMENTRWIDTH = int(8*SIZEFACTOR)
        PARAMCOMBOWIDTH = int(16*SIZEFACTOR)        
        
                
        macroparam_frame = ttk.Frame(parent_frame, relief="ridge", borderwidth=0)
        self.macroparam_frame_dict[macro] = macroparam_frame
        macroparam_frame.rowconfigure(0,weight=1)
        #macroparam_frame.columnconfigure(0,weight=1)

        macrodata = self.controller.MacroDef.data.get(macro,{})
        Macrotitle = macro + " - Daten übernehmen"
        
        Macrolongdescription = macrodata.get("Ausführliche Beschreibung","")
        Macrodescription = macrodata.get("Kurzbeschreibung","")
        macrotype = macrodata.get("Typ","")
        setmacro_allowed =  macrodata.get("Allow_SetMacro","") == "True"
        
        if Macrolongdescription =="":
            Macrolongdescription = Macrodescription
        if Macrolongdescription != "":
            #only show description and Butoon, when description is not empty
            macroldlabel = tk.Text(macroparam_frame, wrap='word', bg=self.cget('bg'), borderwidth=2,relief="ridge",height=5,font=SMALL_FONT)
            macroldlabel.grid(row=4, column=0, columnspan=2,padx=10, pady=10,sticky="ew")
            macroldlabel.delete("1.0", "end")
            macroldlabel.insert("end", Macrolongdescription)
            macroldlabel.yview("1.0")
            macroldlabel.config(state="disabled")
                           
            macrolabel = tk.Button(macroparam_frame, text=Macrotitle, width=MACROLABELWIDTH, height=3, wraplength=110,relief="raised", background="white",borderwidth=1,command=lambda: self._macro_cmd(macrokey=macro))
            macrolabel.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
            macrolabel.key=macro
            self.controller.ToolTip(macrolabel, text=Macrodescription)
             
            if setmacro_allowed: # house and gaslights macro can contain setmacros
                paramvar = tk.Text(macroparam_frame, wrap='word', bg=self.cget('bg'), relief="flat",width=MACROLABELWIDTH, height=5,font=SMALL_FONT)   # textfeld for setmacro info
                paramvar.grid(row=1, column=0, sticky="nw", padx=10, pady=10)
                paramvar.delete("1.0", "end")
                self.set_macroparam_var(macro, "SETMACRO_LIST", paramvar)
                paramvar.config(state="disabled")
                
        if macrotype =="ColTab":
            macroparams = ["ColTab"]
        else:       
            macroparams = macrodata.get("Params",[])
        
        if macroparams:
            scrollparam_frame = False
            if scrollparam_frame:
                scrolledparamframe = HorizontalScrolledFrame(macroparam_frame)
                param_frame = ttk.Frame(scrolledparamframe.interior)
                scrolledparamframe.grid(row=0,column=1,rowspan=2,padx=10, pady=10,sticky="new")
                #scrolledparamframe.grid_columnconfigure(0,weight=1)
                param_frame.grid(row=0,column=0,rowspan=2,padx=10, pady=10,sticky="new")
                #param_frame.grid_columnconfigure(0,weight=0)
            else:
                param_frame = ttk.Frame(macroparam_frame) #, borderwidth=2, relief="ridge")
                param_frame.grid(row=0,column=1,rowspan=2,padx=10, pady=10,sticky="new")            
            
            #param_frame = ttk.Frame(macroparam_frame) #, borderwidth=2, relief="ridge")
                                  
            #self.create_macroparam_content(param_frame,macro, macroparams,extratitleline=True) change 29.5.2020
            self.controller.create_macroparam_content(param_frame,macro, macroparams,extratitleline=True) #change 29.5.2020

            #param_frame.grid(row=0,column=1,rowspan=2,padx=10, pady=10,sticky="new")

        return macroparam_frame

    def get_param_config_dict(self, paramkey):
        paramconfig_dict = self.controller.MacroParamDef.data.get(paramkey,{})
        return paramconfig_dict

    def create_macroparam_hidden_frames(self,parent_frame, macrogroup):
        self.macroparam_hiddenframe = ttk.Frame(parent_frame, relief="ridge", borderwidth=0)
        supportmacrolist = self.macro_tab_dict.get(macrogroup,{})
        row = 0
        if True:
            for supportmacro in supportmacrolist:
                macro_paramframe = self.create_macroparam_frame(self.macroparam_hiddenframe, supportmacro)
                macro_paramframe.grid(row=0,column=0, columnspan=2, pady=4, padx=4, sticky="nsew")
                self.macroparam_frame_dict[supportmacro] = macro_paramframe
        return self.macroparam_hiddenframe
        
    def get_macroparam_frame(self,macrokey):
        macro_paramframe = self.macroparam_frame_dict.get(macrokey,None)
        if macro_paramframe == None:
            macro_paramframe = self.create_macroparam_frame(self.macroparam_hiddenframe, macrokey)
            macro_paramframe.grid(row=0,column=0, columnspan=2, pady=4, padx=4, sticky="nsew")
            self.macroparam_frame_dict[macrokey] = macro_paramframe
            self.update()
        return macro_paramframe
    
    def create_macrolist_frame(self,parent_frame, macrogroup):
        
        MACROLABELWIDTH = int(15*SIZEFACTOR)
        MACROLABELWRAPL = int(150*SIZEFACTOR)
        
        MACRODESCWIDTH = int(20*SIZEFACTOR)
        MACRODESCWRAPL = int(120*SIZEFACTOR)
        
        PARAMLABELWIDTH = int(15*SIZEFACTOR)
        PARAMLABELWRAPL = int(100*SIZEFACTOR)       
        
        PARAMSPINBOXWIDTH = 4
        PARAMENTRWIDTH = int(8*SIZEFACTOR)
        
        supportmacro_mainframe = ttk.Frame(parent_frame)
        supportmacrolist = self.macro_tab_dict.get(macrogroup,{})
        row = 0
        column_max = 6
        column=0
        if len(supportmacrolist) >1:
            for supportmacro in supportmacrolist:
                macrodata = self.controller.MacroDef.data.get(supportmacro,{})
                Macrotitle = supportmacro
                Macrodescription = macrodata.get("Kurzbeschreibung","")
                if len(Macrotitle)>10:
                    Macrotitle = Macrotitle.replace("_","\n",1)                
                macrolabel = tk.Label(supportmacro_mainframe, text=Macrotitle, width=MACROLABELWIDTH, height=2, wraplength=MACROLABELWRAPL,relief="raised", background="white",borderwidth=1)
                macrolabel.grid(row=row, column=column, padx=4, pady=4)
                macrolabel.key=supportmacro
                macrolabel.bind("<Button-1>", self._macrolabel_cmd)
                macrolabel.bind("<Shift-1>", self._macrolabel_shift_cmd)
                macrolabel.bind("<FocusOut>", lambda e: e.widget.configure(relief="raised"))            
                self.controller.ToolTip(macrolabel, text=Macrodescription)
                column = column+1
                if column > column_max:
                    row = row+1
                    column = 0
                
        return supportmacro_mainframe
    
    def set_macroparam_var(self, macro, paramkey,variable):
        
        self.controller.set_macroparam_var(macro, paramkey,variable)
        
        #paramdict = self.controller.macroparams_var.get(macro,{})
        #if paramdict == {}:
        #    self.controller.macroparams_var[macro] = {}
        #    self.controller.macroparams_var[macro][paramkey] = variable
        #else:
        #    paramdict[paramkey] = variable
 
    def set_macroparam_val(self, macro, paramkey, value,disable=False):
        
        self.controller.set_macroparam_val(macro, paramkey, value,disable=disable)
        
        if False:
            try:
                macroparams_dict = self.controller.macroparams_var.get(macro,{})
         
                variable = macroparams_dict.get(paramkey,None)
                if variable:
                    var_class = variable.winfo_class()
                    if var_class == "TCombobox":
                        # value of combobox needs to be translated into a generic value
                        current_index = variable.keyvalues.index(value)
                        value = variable.textvalues[current_index]
                        variable.set(value)
                    elif var_class == "Entry":
                        variable.delete(0,tk.END)
                        variable.insert(0,value)
                    elif var_class == "Text":
                        if disable:
                            variable.config(state="normal")
                        variable.delete(1.0,tk.END)
                        variable.insert(1.0,value)
                        if disable:
                            variable.config(state="disabled")
                    else:          
                        variable.set(value)
                else:
                    pass
            except BaseException as e: #limit_var has no winfo_class() function
                logging.debug(e)
                if variable:
                    variable.set(value)
        return
 
    def get_macroparam_val(self, macro, paramkey):
        
        return self.controller.get_macroparam_val(macro,paramkey)
        
        value = ""
        variable = self.controller.macroparams_var[macro][paramkey]
        try:
            var_class = variable.winfo_class()
            if var_class == "TCombobox":
                # value of combobox needs to be translated into a generic value
                current_index = variable.current()
                if current_index == -1: # entry not in list
                    value = variable.get()
                else:
                    value_list = variable.keyvalues
                    value = value_list[current_index]
            elif var_class == "Text":
                value = variable.get("1.0",tk.END)
            else:
                value = variable.get()
        except:
            value = variable.get()
        return value
    
    def set_all_macroparam_val(self, macro, paramvalues):
        self.controller.set_all_macroparam_val(macro, paramvalues)

    def xset_all_macroparam_val(self, macro, paramvalues):
        try:
            if macro != "Set_ColTab":
                for paramkey in paramvalues:
                    value = paramvalues.get(paramkey)
                    if value!=None:
                        self.set_macroparam_val(macro,paramkey,value)
                        if paramkey=="Group_Colour":
                            self.setgroupcolor(value)
            else: # handle set_coltab
                self.update_color_palette(paramvalues)
                 
        except:
            pass
        return
    
    def get_all_macroparam_val(self, macro):
        return self.controller.get_all_macroparam_val(macro)


    def xget_all_macroparam_val(self, macro):
        paramvalues={}
        try:
            for paramkey in self.controller.macroparams_var[macro]:
                value = self.get_macroparam_val(macro,paramkey)
                paramvalues[paramkey] = value
            for paramkey in self.controller.macroparams_var["Group"]:
                value = self.get_macroparam_val("Group",paramkey)
                paramvalues[paramkey] = value            
        except:
            paramvalues = {}
        return paramvalues
        
    def create_effect_palette(self, macrogroup, parent_frame):
        
        LABELWIDTH = int(16*SIZEFACTOR)
        
        # --- palette
        self.effectpalette = self.getConfigData("effectpalette")
        self.update_effectpalette()
        palette = self.effectpalette.get(macrogroup,{})
        palette_frame = ttk.Frame(parent_frame)
        palette_frame.grid(row=0, column=1, rowspan=3, sticky="ne")
        for i, key in enumerate(palette):
            keycolor = "#FFFFFF" #palette[key]
            color_disp,brightness_text = self.keycolor_to_dispcolor(keycolor)
            fontcolor = "#000000"
            text = key #+ "\n" + brightness_text
            if len(text)>10:
                text = text.replace("_","\n",1)
            #f = ttk.Frame(palette_frame, borderwidth=1, relief="raised",
            #              style="palette.TFrame")
            l = tk.Label(palette_frame, background=color_disp, width=LABELWIDTH, height=2,text=text,fg=fontcolor)
            #self.bind_right_click_menu_to_palettelabel(l)
            l.bind("<Button-1>", self._palette_cmd)
            l.bind("<Shift-1>", self._palette_shift_cmd)
            #l.bind("<Control-3>", self._palette_save_cmd)            
            self.controller.ToolTip(l, key=key)
             
            l.bind("<FocusOut>", lambda e: e.widget.configure(relief="raised"))
            #l.pack()
            l.key = key
            l.macrogroup = macrogroup
            l.grid(row=i // EFFECT_PALLETTE_COLUMNS, column=i % EFFECT_PALLETTE_COLUMNS, padx=2, pady=2)
            
    def create_color_palette(self, parent_frame):
        
        LABELWIDTH = int(16*SIZEFACTOR)
        
        COLOR_PALLETTE_COLUMNS = 4
        
        # --- palette
        self.controller.colorpalette = self.getConfigData("palette")
        self.colorpalette_labels_dict={}
        palette = self.controller.colorpalette
        palette_frame = ttk.Frame(parent_frame)
        palette_frame.grid(row=0, column=1, rowspan=3, sticky="ne")
        for i, key in enumerate(palette):
            keycolor = palette[key]
            color_disp,brightness_text = self.keycolor_to_dispcolor(keycolor)
            fontcolor = "#000000"
            text = key #+ "\n" + brightness_text
            if len(text)>10:
                text = text.replace("_","\n",1)
            l = tk.Label(palette_frame, background=color_disp, width=LABELWIDTH, height=2,text=text,fg=fontcolor)
            l.bind("<Button-1>", self._color_palette_cmd)
            self.controller.ToolTip(l, key=key)
            l.bind("<FocusOut>", lambda e: e.widget.configure(relief="raised"))
            #l.pack()
            l.key = key
            l.grid(row=i % COLOR_PALLETTE_COLUMNS, column=i // COLOR_PALLETTE_COLUMNS, padx=2, pady=2)
            
            self.colorpalette_labels_dict[key]=l
            
    def update_color_palette(self,palette):
        self.controller.update_color_palette(palette)

            
    def xupdate_color_palette(self,palette):
        self.colorpalette = palette
        for key in self.colorpalette_labels_dict:
            keycolor = self.colorpalette[key]
            color_disp,brightness_text = self.keycolor_to_dispcolor(keycolor)
            fontcolor = "#000000"
            text = key #+ "\n" + brightness_text
            if len(text)>10:
                text = text.replace("_","\n",1)
            label = self.colorpalette_labels_dict[key]
            label.configure(background=color_disp, fg=fontcolor)

    def group_save(self,_event=None):
    # save group data
        logging.debug("Group Save")
        
        self.get_all_group_params()
        self.update_ledtable_complete()
        self.controller.paramDataChanged=True
        
        #combo_value_list = list(self.controller.mledgrouptable.keys())
        #combo_text_list = []
        
        #paramvar = self.controller.macroparams_var["Group"]["Group_Name"]
        #paramvar["value"] = combo_value_list

        #paramvar.current(0) #set the selected view                    
                
        #paramvar.keyvalues = combo_value_list
        #paramvar.textvalues = combo_text_list        
        
    def groupname_delete_ok(self,groupname):
        for key in self.controller.ledeffecttable.mledeffecttable:
            leddata_dict = self.controller.ledeffecttable.mledeffecttable.get(key,{})
            if leddata_dict!={}:
                if groupname == leddata_dict.get("groupname",""):
                    self.controller.set_statusmessage("Error: "+groupname+ " kann nicht gelöscht werden, da noch in Verwendung",fg="red")
                    return False
        return True
        
    
    def group_delete(self,_event=None):
    # delete group data
        logging.debug("Group Delete")
        groupparams_dict = self.get_all_macroparam_val("Group")
        groupname = groupparams_dict.get("Group_Name","Dummy")
        
        if groupname in self.controller.ledeffecttable.mledgrouptable:
            if self.groupname_delete_ok(groupname):
                del self.controller.ledeffecttable.mledgrouptable[groupname]

    def create_group_frame(self, group_name, parent_frame):
        
        BUTTONWIDTH = int(15*SIZEFACTOR)
        
        group_frame = ttk.Frame(parent_frame, relief="ridge", borderwidth=2)
        
        group_frame.columnconfigure(1, weight=1)
        group_frame.rowconfigure(1, weight=1)

        group_macro = "Group"
        group_data = self.controller.MacroDef.data.get(group_macro,{})
        group_params = group_data.get("Params",[])
        
        group_param_content_frame = ttk.Frame(group_frame)
        self.controller.create_macroparam_content(group_param_content_frame,group_macro, group_params, maxcolumns=4, startrow=0,extratitleline=True)

        group_main_label = ttk.Label(group_frame, text=group_data.get("Kurzbeschreibung",""),font=LARGE_FONT)
        group_save_button=ttk.Button(group_frame, text="Übernehmen",width=BUTTONWIDTH, command=self.group_save)
        self.controller.ToolTip(group_save_button, text="Aktuelle Gruppendaten übernehmen")
        
        group_delete_button=ttk.Button(group_frame, text="Gruppe löschen",width=BUTTONWIDTH, command=self.group_delete)
        self.controller.ToolTip(group_delete_button, text="Gruppendaten der aktuellen Gruppe löschen")
        
        group_main_label.grid(row=0,column=0,columnspan=2,padx=2, pady=(2,2), sticky="w")
        group_param_content_frame.grid(row=1,column=1,columnspan=1,rowspan=2,padx=2, pady=(2,2), sticky='w')
        group_save_button.grid(row=1, column=0, padx=2, pady=(2, 2), sticky='w')
        group_delete_button.grid(row=2, column=0, padx=2, pady=(2, 2), sticky='w')

        return group_frame
        

    def cb(self):
        self._update_cor_rgb()

    def get_color(self):
        """Return selected color, return an empty string if no color is selected."""
        return self.color

    def update_effectpalette(self):
        macrolist = list(self.effectpalette.keys())
        for macro in macrolist:
            for effect in self.effectpalette[macro].keys():
                palette_tab = HOUSE_PALETTE2COLOR_PALETTE.get(effect)
                new_color = self.controller.palette.get(palette_tab, palette_tab)
                self.effectpalette[macro][effect] = new_color

    def _palette_redraw_colors(self,parent_frame):
        
        LABELWIDTH = int(18*SIZEFACTOR)
        
        #if self.palette_frame:
        #    self.palette_frame.destroy()
        tabName = self.current_tabName
        
        palette_frame = ttk.Frame(parent_frame)
        palette_frame.grid(row=0, column=1, rowspan=2, sticky="ne")
        for i, key in enumerate(palette):
            keycolor = self.palette[key]
            color_disp,brightness_text = self.keycolor_to_dispcolor(keycolor)
            fontcolor = "#000000"
            text = key + "\n" + brightness_text
            f = ttk.Frame(self.palette_frame, borderwidth=1, relief="raised",
                          style="palette.TFrame")
            l = tk.Label(f, background=color_disp, width=LABELWIDTH, height=2,text=text,fg=fontcolor, relief="raised")
            l.bind("<Button-1>", self._palette_cmd)
            #l.bind("<Control-3>", self._palette_save_cmd)         
            
            self.bind_right_click_menu_to_palettelabel(l)
            f.bind("<FocusOut>", lambda e: e.widget.configure(relief="raised"))
            l.pack()
            l.key = key
            f.grid(row=i // EFFECT_PALLETTE_COLUMNS, column=i % EFFECT_PALLETTE_COLUMNS, padx=2, pady=2)
        
        
    def palette_reset_colors(self):
        
        self.palette = DEFAULT_PALETTE.copy()
        self._palette_redraw_colors()
        
    #def savePalettetoFile(self, filepath):
    #    
    #    dictFile.saveDicttoFile(filepath, self.palette)

    #def readPalettefromFile(self, filepath):
    #    
    #    palette = dictFile.readDictFromFile(filepath)
    #    if palette:
    #        self.palette = palette.copy()
    #    self._palette_redraw_colors()


    def _correct_rgb_disp(self, r, g, b):
        crf = COLORCOR_MAX/int(self.cor_red)
        cgf = COLORCOR_MAX/int(self.cor_green)
        cbf = COLORCOR_MAX/int(self.cor_blue)
        rcor = int(r*crf)
        gcor = int(g*cgf)
        bcor = int(b*cbf)
        if rcor > 255: rcor = 255
        if gcor > 255: gcor = 255
        if bcor > 255: bcor = 255
        return rcor, gcor, bcor

    def _correct_hsv_disp(self, h,s,v):
        if self.getConfigData("colorview") == 0: # only correct when colorsquare is shown
            r, g, b = hsv_to_rgb(h,s,v)
            rcor,gcor,bcor = self._correct_rgb_disp(r,g,b)
            args = (rcor,gcor, bcor)
            h,s,v = rgb_to_hsv(*args)
        return h,s,v

    def keycolor_to_dispcolor(self, keycolor):
        r,g,b = hexa_to_rgb(keycolor)
        args = (r,g,b)
        h,s,v = rgb_to_hsv(*args)
        r2,g2,b2 = self._correct_rgb_disp(*args)
        #---  palette colors will be displayed with brightness = 100
        args2 = (r2,g2,b2)
        h2,s2,v2 = rgb_to_hsv(*args2)
        r3,g3,b3 = hsv_to_rgb(h2,s2,100)
        args3 = (r3,g3,b3)
        disp_color = rgb_to_hexa(*args3)
        if PERCENT_BRIGHTNESS:                                           # 03.12.19:
            brightness = str(v) + " %"
        else:
            brightness = ""
            v3 = v/10
            for j in range(10):
                if j<v3:
                    brightness = brightness + ">"
        return disp_color, brightness

    def move_ledtable_canvas(self,value):
        self.ledlist_scrollframe.move_canvas(value)

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

    def _update_preview(self, _event=None,_LEDupdate=True,macrogroup=""):
        """Update color preview."""
        color = self.hexa
        red,green,blue = hexa_to_rgb(color)
        if macrogroup != "":
            self.current_macro = macrogroup
        if _LEDupdate:
            ledcount = self.ledcount.get()
            if ledcount >0:
                lednum = self.lednum.get()
                self._update_led(lednum, ledcount, red, green, blue, color,self.effect,self.current_macro, self.group_name_str)

    def get_all_group_params(self):
        # gets all group params and copies them into the ledgrouptable under the groupname
        
        groupparams_dict = self.get_all_macroparam_val("Group")
        groupname = groupparams_dict.get("Group_Name","Dummy")
        
        ledgroup_dict = self.controller.ledeffecttable.mledgrouptable.get(groupname,{})
        if ledgroup_dict == {}:
            self.controller.ledeffecttable.mledgrouptable[groupname] = {"Name":groupname,"params":{"Group_Name":groupname}}
            ledgroup_dict = self.controller.ledeffecttable.mledgrouptable.get(groupname,{})
        ledgroupparams_dict=ledgroup_dict.get("params",{})
        ledgroupparams_dict.update(groupparams_dict)
        return groupname

    def _macro_cmd(self, macrokey=""):
        """Respond to user click on a macro label item in macrolist."""
        
        self.macro = macrokey
        macroparams = self.get_all_macroparam_val(macrokey)
        self.hexa = macroparams.get("Group_Colour","")
        self.group_name_str = self.get_all_group_params()
        
        
        self._update_ledtable(self.lednum_int, int(self.ledcount_int),self.hexa,"",macrokey, self.group_name_str, params=macroparams)
        self.update_ledtable_complete()

    def _button_cmd(self, macrokey="",button=0):
        """Respond to user click on a dcc button item in macrolist."""
        
        self.macro = macrokey
        self.button_nr = button
        logging.debug ("_button_cmd: %s - %s",macrokey,button)

    def _macrolabel_cmd(self, _event=None):
        """Respond to user click on a palette item."""
        label = _event.widget
        label.focus_set()
        label.configure(relief="sunken")
        text = _event.widget["text"]
        macrokey = label.key
        self.macro = macrokey
        macroparams = self.get_all_macroparam_val(macrokey)
        #macroparam_frame = self.macroparam_frame_dict.get(macrokey,None)
        macroparam_frame = self.get_macroparam_frame(macrokey)
        if macroparam_frame:
            macroparam_frame.lift()
        self.group_name_str = macroparams.get("Group_Name","")
        self.hexa = macroparams.get("Group_Colour","")        
        self.group_name_str = self.get_all_group_params()
        self._update_ledtable(self.lednum_int, int(self.ledcount_int),self.hexa,"",macrokey, self.group_name_str, params=macroparams)
        self.update_ledtable_complete()

    def _macrolabel_shift_cmd(self, _event=None):
        """Respond to user click on a macro label item in macrolist."""
        self._macrolabel_cmd(_event=_event)
        keystr = "{:03}".format(self.lednum_int)
        no_of_LED_ch = self.controller.ledeffecttable.determine_no_of_LED_channels_key(keystr)
        new_lednum = self.lednum_int + no_of_LED_ch
        self.set_lednum_count(new_lednum,self.ledcount_int)        

    def _color_palette_cmd(self,_event):
        self.checkcolor()
        
    def _palette_cmd(self, _event):
        """Respond to user click on a palette item."""
        label = _event.widget
        label.master.focus_set()
        label.master.configure(relief="sunken")
        text = _event.widget["text"]
        palettekey = label.key
        macrogroup = label.macrogroup
        macrokey = macrogroup
        #palette = self.effectpalette.get(macrogroup,{})
        keycolor = "#FFFFFF"
        r,g,b = hexa_to_rgb(keycolor)
        args = (r, g, b)
        color = rgb_to_hexa(*args)
        self.hexa = color.upper()
        self.effect = palettekey
        self.group_name_str = self.get_all_group_params()
        #macroparams = self.get_all_macroparam_val("Group")
        macroparams = self.get_all_macroparam_val(macrogroup)
        self.hexa = macroparams.get("Group_Colour","")
        self.current_macro = macrogroup
        self._update_preview(macrogroup=macrogroup)
        self._update_ledtable(self.lednum_int, int(self.ledcount_int),self.hexa,"",macrokey, self.group_name_str, params=macroparams)
        self.update_ledtable_complete()
        
    def _palette_shift_cmd(self, _event):
        """Respond to user click on a palette item."""
        self._palette_cmd(_event)
        keystr = "{:03}".format(self.lednum_int)
        no_of_LED_ch = self.controller.ledeffecttable.determine_no_of_LED_channels_key(keystr)
        
        new_lednum = self.lednum_int + no_of_LED_ch
        self.set_lednum_count(new_lednum,self.ledcount_int)

    def _show_tab_for_macro(self, macro):
        for groupmacro in GROUPMACRO2SUPPORTMACRO:
            macrolist = GROUPMACRO2SUPPORTMACRO.get(groupmacro)
            if macrolist:
                if macro in macrolist:
                    break
        # show tab for group macro
        self.container.select(self.tabdict[groupmacro]["macro_frame"])
        
    def show_macroparam_frame(self,macro):
        #macroparam_frame = self.macroparam_frame_dict.get(macro,None)
        macroparam_frame = self.get_macroparam_frame(macro)
        if macroparam_frame:
            macroparam_frame.lift()
        macrodata = self.controller.MacroDef.data.get(macro,{})
        if macrodata != {}:
            tabname = macrodata.get("TabName","")
            if tabname!="":
                self.showFramebyName(tabname)
    
    def _show_macroparams(self, key):
        # show the parameters of the macro and select the correct tab
        led_param_dict = self.controller.ledeffecttable.get(key,{})
        macro = led_param_dict.get("macro","")
        if macro != "":
            macroparams = led_param_dict.get("params",{})
            self.set_all_macroparam_val(macro,macroparams)            
            groupname = led_param_dict.get("groupname","")
            group_dict = self.controller.ledeffecttable.mledgrouptable.get(groupname,{})
            group_param_dict = group_dict.get("params."+macro,{}) # check for nested macro
            if group_param_dict == {}:
                group_param_dict = group_dict.get("params",{})
            
            if group_param_dict != {}:
                self.set_all_macroparam_val("Group",group_param_dict)
                if macro in ["House","GasLights"]:
                    self.set_all_macroparam_val(macro,group_param_dict)
                else:
                    self.set_all_macroparam_val(macro,macroparams)
            
            setmacro_dict = led_param_dict.get("setmacro",{})
            
            if setmacro_dict !={}:
                setmacro_list_str = "Set Macros:"
                for setmacro in setmacro_dict:
                    setmacro_params = setmacro_dict[setmacro]
                    self.set_all_macroparam_val(setmacro,setmacro_params)
                    setmacro_list_str += "\n"+setmacro
                
                self.set_macroparam_val(macro,"SETMACRO_LIST",setmacro_list_str,disable=True)
            else:
                self.set_macroparam_val(macro,"SETMACRO_LIST","",disable=True)
            
            self.show_macroparam_frame(macro)
                
         
    def setPaletteColor(self, key, color):
        oldcolor= self.palette.get(key,"#000000")
        self.controller.setParamDataChanged()
        self.addtoUndoList(key,oldcolor)
        self.palette[key] = color

    def addtoUndoList(self, key, color):
        undoEntry = {}
        undoEntry[key] = color
        self.paletteUndoList.append(undoEntry)

    def _update_led_num(self, event=None, scroll=True):
        """Update display after a change in the LED spinboxes."""
        if event is None or event.widget.old_value != event.widget.get():
            led = int(self.lednum.get())
            ledcount = int(self.ledcount.get())
            ledcnt_max = int(self.controller.get_maxLEDcnt())*3 # led connectors
            if led+ledcount > ledcnt_max:
                led = ledcnt_max-ledcount
                self.lednum.set(led)
                
            self.old_lednum_int = self.lednum_int
            self.old_ledcount_int = self.ledcount_int
            self.lednum_int = led
            self.ledcount_int = ledcount
            self._update_ledtable_activestatus(led, ledcount)
            self._highlight_led(led, ledcount)
            if scroll:
                if led >15:
                    scrollvalue = (led-15)/(255.0*3)
                else:
                    scrollvalue = 0
                self.move_ledtable_canvas(scrollvalue)

    def _update_led_count(self, event=None):
        """Update display after a change in the LED count spinboxes."""
        if event is None or event.widget.old_value != event.widget.get():
            led = int(self.lednum.get())
            ledcount = int(self.ledcount.get())
            ledcnt_max = int(self.controller.get_maxLEDcnt())*3 # led connectors
            if led+ledcount > ledcnt_max:
                ledcount = ledcnt_max-led
                self.ledcount.set(ledcount)            
            self.old_lednum_int = self.lednum_int
            self.old_ledcount_int = self.ledcount_int
            self.lednum_int = led
            self.ledcount_int = ledcount
            self._update_ledtable_activestatus(led, ledcount)
            self._highlight_led(led, ledcount)
            #self._update_preview(_LEDupdate=False)
            

    def led_off(self,_event=None):
    # switch off all LED
        self.ledhighlight = False
        if self.controller.mobaledlib_version == 1:
            message = "#L00 00 00 00 FF\n"
        else:
            message = "#L 00 00 00 00 7FFF\n"
        self.controller.send_to_ARDUINO(message)
        #self.controller.ledtable.clear()
        
    def blinking_on_off(self,_event=None):
    # switch off all LED
        if self.ledhighlight_switch:
            self.ledhighlight_switch = False
            self.blinkoff_button.configure(text="Blinken Ein")
            
        else:
            self.ledhighlight_switch = True
            self.blinkoff_button.configure(text="Blinken Aus")
            
        if self.ledhighlight:
            self._restore_led_colors(self.on_lednum,self.on_ledcount)
        else:
            lednum = self.lednum.get()
            ledcount = self.ledcount.get()
            self._highlight_led(lednum, ledcount)
    
    def start_ARDUINO_program_Run(self):
        result = subprocess.run(self.startfile, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        
        if result.returncode == 0:
            self.arduinoMonitorPage.add_text_to_textwindow("\n"+self.ARDUINO_message2+"\n*******************************************************\n",highlight="OK")
        else:
            self.arduinoMonitorPage.add_text_to_textwindow("\n******** "+self.ARDUINO_message3+" ********\n",highlight="Error")
            self.arduinoMonitorPage.add_text_to_textwindow("\n"+result.stdout,highlight="Error")
            self.arduinoMonitorPage.add_text_to_textwindow("\n*******************************************************\n\n\n",highlight="Error")
    
    def write_stdout_to_text_window(self):
        if self.continue_loop:
            output = self.process.stdout.readline()

            if output != '' and self.continue_loop:
                try:
                    self.arduinoMonitorPage.add_text_to_textwindow(output.decode('utf-8').strip())
                except BaseException as e:
                    logging.debug(e)
                    logging.debug("ERROR: Write_stdout_to_text_window: %s",output)
                    pass            
            
            if self.process.poll() is not None:
                self.continue_loop=False
                self.rc = self.process.poll()
                if self.rc==1:
                    self.arduinoMonitorPage.add_text_to_textwindow("\n******** "+self.ARDUINO_message3+" ********\n",highlight="Error")
                else:
                    self.arduinoMonitorPage.add_text_to_textwindow("\n"+self.ARDUINO_message2+"\n*******************************************************\n",highlight="OK")

        if self.continue_loop:
            self.after(10,self.write_stdout_to_text_window)
 
            
    def start_ARDUINO_program_Popen(self):
        try:
            self.process = subprocess.Popen(self.startfile, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin = subprocess.DEVNULL)
            self.continue_loop=True
            self.write_stdout_to_text_window()
        except BaseException as e:
            logging.error("Exception in start_ARDUINO_program_Popen %s - %s",e,self.startfile[0])
            self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")
            self.arduinoMonitorPage.add_text_to_textwindow("\n* Exception in start_ARDUINO_program_Popen "+ e + "-" + self.startfile[0]+ "\n",highlight="Error")
            self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")

        
        #if result.returncode == 0:
        #    self.arduinoMonitorPage.add_text_to_textwindow("\n"+self.ARDUINO_message2+"\n*******************************************************\n",highlight="OK")
        #else:
        #    self.arduinoMonitorPage.add_text_to_textwindow("\n******** "+self.ARDUINO_message3+" ********\n",highlight="Error")
        #    self.arduinoMonitorPage.add_text_to_textwindow("\n"+result.stdout,highlight="Error")
        #    self.arduinoMonitorPage.add_text_to_textwindow("\n*******************************************************\n\n\n",highlight="Error")

    
    def upload_to_ARDUINO(self,_event=None,arduino_type="LED",init_arduino=False):
    # send effect to ARDUINO
        if self.controller.ARDUINO_status == "Connecting":
            tk.messagebox.showwarning(title="Zum ARDUINO Hochladen", message="PC versucht gerade sich mit dem ARDUINO zu verbinden, bitte warten Sie bis der Vorgang beendet ist!")
            return
        self.controller.disconnect()
        self.controller.set_connectstatusmessage("Kompilieren und Hochladen ...",fg="green")
        
        if arduino_type == "LED":
            self.create_ARDUINO_CMD(init_arduino=init_arduino)
                
        private_startfile = self.getConfigData("startcmdcb")
        
        macrodata = self.controller.MacroDef.data.get("ARDUINOMonitorPage",{})
        
        self.arduinoMonitorPage=self.controller.getFramebyName ("ARDUINOMonitorPage")
        self.arduinoMonitorPage.delete_text_from_textwindow()
        
        file_not_found = True
        
        system_platform = platform.platform()
        
        if not "Windows" in system_platform:
            private_startfile = True
        
        self.ARDUINO_message4=""
        
        if private_startfile == True:
            filename = self.getConfigData("startcmd_filename")
            logging.debug("upload_to_ARDUINO - Individual Filename: %s",filename)
            if filename == " " or filename == "":
                filename = "No Filename provided"
            logging.debug("send to ARDUINO - Platform: %s",platform.platform())
            
            macos = "macOS" in system_platform
            macos_fileending = "/Contents/MacOS/Arduino" 
            if macos:
                logging.debug("This is a MAC")
                if not filename.endswith(macos_fileending):
                    filename = filename + "/Contents/MacOS/Arduino"
                file_not_found = False
            else:
                if os.path.isfile(filename):
                    file_not_found = False
                if file_not_found:
                    self.ARDUINO_message4 = macrodata.get("Message_4","") + filename

        else:
            file_not_found = True
            #check if arduino_debug.exe exists in the program dirs
            Win_ARDUINO_searchlist = macrodata.get("Win_ARDUINOIDE","")
            
            for IDE_filename in Win_ARDUINO_searchlist:
                if os.path.isfile(IDE_filename):
                    file_not_found = False
                    filename = IDE_filename
                    break
            if file_not_found:
                self.ARDUINO_message4 = macrodata.get("Message_4","") + repr(Win_ARDUINO_searchlist)
        logging.debug("upload_to_ARDUINO - Filename: %s",filename)
        self.controller.showFramebyName("ARDUINOMonitorPage")
        self.controller.set_connectstatusmessage("Kompilieren und Hochladen ...",fg="green")
        self.update()
        
        if file_not_found:
            self.arduinoMonitorPage.add_text_to_textwindow("\n*******************************************************\n"+self.ARDUINO_message4+"\n*******************************************************\n")            
        else:
            serport = self.getConfigData("serportname")
            arduinotypenumber = self.getConfigData("ArduinoTypeNumber")
            ArduinoTypeNumber_config_dict = self.get_param_config_dict("ARDUINO Type")
            ArduinotypeList = ArduinoTypeNumber_config_dict["Values2Params"]
            ArduinoType = ArduinotypeList[arduinotypenumber]
            
            self.ARDUINO_message1 = macrodata.get("Message_1","")
            self.ARDUINO_message2 = macrodata.get("Message_2","")
            self.ARDUINO_message3 = macrodata.get("Message_3","")
            
            #h_filedir = os.path.dirname(filename)
            filedir = os.path.dirname(os.path.realpath(__file__))
            h_filedir1 = os.path.dirname(filedir)
            h_filedir = os.path.dirname(h_filedir1)            
            #os.chdir(h_filedir)
            os.chdir(self.controller.mainfile_dir)
            
            #filedirname = os.path.join(h_filedir, filename)
            #if platform.platform == "darwin":
            #    logging.debug("This is a MAC")
            #    filedirname = filename + "/Contents/MacOS/Arduino"
            #else:
            filedirname = filename
            
            if arduino_type=="DCC":
                ino_filename = self.controller.get_macrodef_data("StartPage","InoName_DCC") #"../../examples/23_A.DCC_Interface/23_A.DCC_Interface.ino"
            elif arduino_type=="Selectrix":
                ino_filename = self.controller.get_macrodef_data("StartPage","InoName_SX") #"../../examples/23_A.DCC_Interface/23_A.DCC_Interface.ino"
            elif arduino_type=="LED":
                ino_filename = self.controller.get_macrodef_data("StartPage","InoName_LED") #"LEDs_AutoProg.ino"
            
            if ArduinoType == " ":
                self.startfile = [filedirname,ino_filename,"--upload","--port",serport,"--pref","programmer=arduino:arduinoisp","--pref","build.path=../Arduino_Build_LEDs_AutoProg","--preserve-temp-files"]
            else:
                self.startfile = [filedirname,ino_filename,"--upload","--port",serport,"--board",ArduinoType,"--pref","programmer=arduino:arduinoisp","--pref","build.path=../Arduino_Build_LEDs_AutoProg","--preserve-temp-files"]
            
            logging.debug(repr(self.startfile))
            
            self.arduinoMonitorPage.add_text_to_textwindow("\n\n*******************************************************\n"+self.ARDUINO_message1+"\n*******************************************************\n\n")
            
            if arduino_type=="LED":
                self.arduinoMonitorPage.add_text_to_textwindow("***************************************************************************\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*    Zum                                                                  *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*     PC                    Prog_Generator " + PROG_VERSION+ " by Harold    *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*      \\\\                                                                 *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*       \\\\                                                                *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*    ____\\\\___________________                                            *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  | [_] | | [_] |[oo]    |  Achtung: Es muss der LINKE               *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  Arduino mit dem PC verbunden             *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  sein.                                    *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  | LED | |     |        |                                           *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  | Nano| |     |        |  Wenn alles gut geht, dann wird           *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  hier eine Erfolgsmeldung angezeigt       *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |                                           *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |_____| |_____| [O]    |                                           *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |    [@] [@] [@]          |  Falls Probleme auftreten, dann werden    *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |__________________[:::]__|  die Fehler hier aufgelistet              *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*                                                                         *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("***************************************************************************\n")
            elif arduino_type=="DCC":
                self.arduinoMonitorPage.add_text_to_textwindow("***************************************************************************\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*             Zum                                                         *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*              PC           Prog_Generator " + PROG_VERSION+ " by Harold    *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*              \\\\                                                         *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*               \\\\                                                        *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*    ____________\\\\____________                                           *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  | [_] | | [_] |[oo]    |  Achtung: Es muss der RECHTE              *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  Arduino mit dem PC verbunden             *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  sein.                                    *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | | DCC |        |                                           *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | | Nano|        |  Wenn alles gut geht, dann wird           *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  hier eine Erfolgsmeldung angezeigt       *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |                                           *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |  |_____| |_____| [O]    |                                           *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |    [@] [@] [@]          |  Falls Probleme auftreten, dann werden    *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*   |__________________[:::]__|  die Fehler hier aufgelistet              *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("*                                                                         *\n")
                self.arduinoMonitorPage.add_text_to_textwindow("***************************************************************************\n")                
            else:
                pass
            
            self.controller.showFramebyName("ARDUINOMonitorPage")
            start_with_realtime_logging = True
            use_start_cmd = False
            if use_start_cmd:
                filedir = os.path.dirname(os.path.realpath(__file__))
                h_filedir1 = os.path.dirname(filedir)
                h_filedir = os.path.dirname(h_filedir1)
                filename = "Start_Arduino.cmd"
                
                os.chdir(h_filedir)
                self.startfile = filename
                os.startfile(self.startfile)
            elif start_with_realtime_logging:
                self.after(500, self.start_ARDUINO_program_Popen)
            else:
                self.after(500, self.start_ARDUINO_program_Run)
            
  


        
    def generate_macros(self,init_arduino=False):
        return self.controller.ledeffecttable.generate_macros(init_arduino=init_arduino)

    def create_ARDUINO_CMD(self,init_arduino=False):
        
        h_filedir1 = self.controller.mainfile_dir # os.path.dirname(os.path.realpath(__file__))
        #h_filedir1 = os.path.dirname(filedir)
        h_filedir = os.path.dirname(h_filedir1) # get filedir ..\.. for he location of the LEDs_AutoProg.h file

        filename = "LEDs_AutoProg.h"
        self.filepath = os.path.join(h_filedir, filename)
        max_led_count = self.controller.get_maxLEDcnt()
        
        digital_system = self.controller.get_macroparam_val("ARDUINOConfigPage","MLL_DigitalSystem")

        try:
            with open(self.filepath, "w") as write_file:
                print("// This file contains the DCC and LED definitions.",file=write_file)
                print("//",file=write_file)
                print("// It was automatically generated by the program Prog_Generator_MobaLedLib.xlsm Ver. 3.1.0      by Hardi",file=write_file)
                print("// File creation: 19.01.2020 16:50:22",file=write_file)
                print("// (Attention: The display in the Arduino IDE is not updated if Options/External Editor is disabled)",file=write_file)
                print("",file=write_file)
                print("#ifndef __LEDS_AUTOPROG_H__",file=write_file)
                print("#define __LEDS_AUTOPROG_H__",file=write_file)
                print("",file=write_file)
                print("#ifndef ARDUINO_RASPBERRY_PI_PICO",file=write_file)
                print("#define FASTLED_INTERNAL       // Disable version number message in FastLED library (looks like an error)",file=write_file)
                print("#include <FastLED.h>           // The FastLED library must be installed in addition if you got the error message ""..fatal error: FastLED.h: No such file or directory""",file=write_file)
                print("                               // Arduino IDE: Sketch / Include library / Manage libraries                    Deutsche IDE: Sketch / Bibliothek einbinden / Bibliothek verwalten",file=write_file)
                print("                               //              Type ""FastLED"" in the ""Filter your search..."" field                          ""FastLED"" in das ""Grenzen Sie ihre Suche ein"" Feld eingeben",file=write_file)
                print("                               //              Select the entry and click ""Install""                                         Gefundenen Eintrag auswaehlen und ""Install"" anklicken",file=write_file)
                print("#else",file=write_file)
                print("#include <PicoFastLED.h>       // Juergens minimum version or FastLED for Raspberry Pico",file=write_file)                
                print("#endif",file=write_file)                
                print("",file=write_file)
                print("#include <MobaLedLib.h>",file=write_file)
                                                                
                print("#define START_MSG \"LEDs_AutoProg Ver 1: MobaLedLib_3.1.0 19.01.20 16:50\"",file=write_file)
                print("",file=write_file)
                if digital_system == "Selectrix":
                    print("#define TWO_BUTTONS_PER_ADDRESS 0      // One button is used (Selectrix)",file=write_file)
                else:
                    print("#define TWO_BUTTONS_PER_ADDRESS 1      // Two buttons (Red/Green) are used (DCC/CAN)",file=write_file)
                    
                print("#ifdef NUM_LEDS",file=write_file)
                print("  #warning \"NUM_LEDS\" definition in the main program is replaced by the included \"LEDs_AutoProg.h\" with 20",file=write_file)
                print("  #undef NUM_LEDS",file=write_file)
                print("#endif",file=write_file)
                print("",file=write_file)
                print("#define NUM_LEDS ",max_led_count,"                    // Number of LEDs (Maximal 256 RGB LEDs could be used)",file=write_file)
                print("",file=write_file)
                print("#define LEDS_PER_CHANNEL ',20'",file=write_file)
                print("",file=write_file)
                print("#define RECEIVE_LED_COLOR_PER_RS232",file=write_file)
                
                print("",file=write_file)
                print("// Input channel defines for local inputs and expert users",file=write_file)
                print("",file=write_file)
                print("/*********************/",file=write_file)
               
                print("",file=write_file)
                print("//*******************************************************************",file=write_file)
                print("// *** Configuration array which defines the behavior of the LEDs ***",file=write_file)
                
                macro_str = self.generate_macros(init_arduino=init_arduino)
                print(macro_str,file=write_file)

                print("//*******************************************************************",file=write_file)
                print("",file=write_file)
               
                
                print("// No macros used which are stored to the EEPROM => Disable the ENABLE_STORE_STATUS flag in case it was set in the excel sheet",file=write_file)
                print("#ifdef ENABLE_STORE_STATUS",file=write_file)
                print("    #undef ENABLE_STORE_STATUS",file=write_file)
                print("#endif",file=write_file)
                
                print("",file=write_file)
                print("",file=write_file)
                print("",file=write_file)
                
                print("#endif // __LEDS_AUTOPROG_H__",file=write_file)               
                
 
        except:
            logging.error("Exception in create_ARDUINO_CMD", exc_info=True)
        
    def _update_led(self, lednum, ledcount, red, green, blue, color_hex, effect,macro, name ):
        self._update_ledtable(lednum, ledcount, color_hex, effect, macro, name)
        if self.controller.mobaledlib_version == 1:
            message = "#L" + '{:02x}'.format(lednum) + " " + '{:02x}'.format(red) + " " + '{:02x}'.format(green) + " " + '{:02x}'.format(blue) + " " + '{:02x}'.format(ledcount) + "\n"
        else:
            message = "#L " + '{:02x}'.format(lednum) + " " + '{:02x}'.format(red) + " " + '{:02x}'.format(green) + " " + '{:02x}'.format(blue) + " " + '{:02x}'.format(ledcount) + "\n"
        self.controller.send_to_ARDUINO(message)
        
    def _update_ledtable(self, lednum, ledcount,rgb_hex,effect,macro, name, params = {}):
        
        self.controller.ledeffecttable.update_ledeffecttable(lednum, ledcount,rgb_hex,effect,macro, name, params)
        self._restore_led_colors(lednum,ledcount)
        
    def _update_ledtable_view_key(self, lednum_str):
        label = self.controller.ledeffect_label_list.get(lednum_str,None)
        self.controller.ledeffecttable.update_ledtable_view_key(lednum_str, label)
    
    def set_lednum_count(self,lednum, ledcount,scroll=True):
        self.lednum.set(lednum)
        self.ledcount.set(ledcount)
        self._update_led_num(scroll=scroll)

    def update_ledtable_complete(self):
        for key in self.controller.ledeffecttable.keys():
            self._update_ledtable_view_key(key)

    def _update_ledtable_activestatus(self, lednum, ledcount):
        self.controller.ledeffecttable.update_ledeffecttable_activestatus(lednum, ledcount)
    
    def _restore_led_colors(self, lednum, ledcount):
        if self.ledhighlight: # reset all colors
            self.ledhighlight = False
            for i in range(ledcount):
                lednum_str = '{:03}'.format(self.on_lednum+i)
                keycolor = "#000000" #self._get_color_from_ledtable(lednum_str)
                #keycolor = self._get_color_from_ledtable(lednum_str) 
                self._send_ledcolor_to_ARDUINO(lednum_str,1,keycolor)
                
    def _get_color_from_ledtable(self,lednum):
        lednum = int(lednum)
        lednum_str = '{:03}'.format(lednum)
        keycolor = self.controller.ledeffecttable.getpath(lednum_str+"."+"color","#FFFFFF")
        return keycolor
        
    def _send_ledcolor_to_ARDUINO(self, lednum, ledcount, ledcolor):
        lednum_int = int(lednum)
        # determine real led (lednum /3 and the channel
        ar_lednum=int(lednum_int/3)
        ar_channel = (lednum_int % 3) + 1
        if ar_channel ==1:
            if ledcount == 1:
                message = "#L " + '{:02x}'.format(ar_lednum) + " " + ledcolor[1:3] + " 00 00 01\n"
            elif ledcount == 2:
                message = "#L " + '{:02x}'.format(ar_lednum) + " " + ledcolor[1:3] + " " + ledcolor[3:5] + " 00 01\n"
            else:
                message = "#L " + '{:02x}'.format(ar_lednum) + " " + ledcolor[1:3] + " " + ledcolor[3:5] + " " + ledcolor[5:7] + " " + '{:02x}'.format(int(ledcount/3)) + "\n"
        if ar_channel ==2:
            if ledcount == 1:
                message = "# L" + '{:02x}'.format(ar_lednum) + " 00 " + ledcolor[3:5] + " 00 01\n"
            elif ledcount == 2:
                message = "# L" + '{:02x}'.format(ar_lednum) + " 00" + ledcolor[3:5] + " " + ledcolor[5:7] + " 01\n"
            else:
                message = "# L" + '{:02x}'.format(ar_lednum) + " " + ledcolor[1:3] + " " + ledcolor[3:5] + " " + ledcolor[5:7] + " " + '{:02x}'.format(int(ledcount/3)) + "\n"                
        if ar_channel ==3:
            if ledcount == 1:
                message = "# L" + '{:02x}'.format(ar_lednum) + " 00 00 " + ledcolor[5:7] + " 01\n"
            elif ledcount == 2:
                message = "# L" + '{:02x}'.format(ar_lednum) + " 00 00 " + ledcolor[5:7] + " 01\n"
            else:
                message = "# L" + '{:02x}'.format(ar_lednum) + " " + ledcolor[1:3] + " " + ledcolor[3:5] + " " + ledcolor[5:7] + " " + '{:02x}'.format(int(ledcount/3)) + "\n"                    
        self.controller.send_to_ARDUINO(message)
        time.sleep(ARDUINO_WAITTIME)
            
    def _highlight_led(self,lednum, ledcount):
        if self.ledhighlight_switch:
            if self.ledhighlight: # onblink is already running, change only lednum and ledcount
                # reset all blinking led with their colors
                #for i in range(self.on_ledcount):
                #    lednum_str = '{:03}'.format(self.on_lednum+i)
                #    keycolor = "#000000" #self._get_color_from_ledtable(lednum_str)              
                #    self._send_ledcolor_to_ARDUINO(lednum_str,1,keycolor)
                #    time.sleep(ARDUINO_WAITTIME)
                #set the blinking led to highlight
                self._send_ledcolor_to_ARDUINO(self.on_lednum, self.on_ledcount, "#000000")
                self._send_ledcolor_to_ARDUINO(lednum, ledcount, "#FFFFFF")
                # save current lednum and led count
                self.on_lednum = lednum
                self.on_ledcount = ledcount
                self.on_ledon = True
            else:
                self.ledhighlight = True
                self.on_lednum = lednum
                self.on_ledcount = ledcount
                self.on_ledon = True       
                self.onblink_led()

         
    def onblink_led(self):
        if self.ledhighlight:
            if self.on_ledon:
                self._send_ledcolor_to_ARDUINO(self.on_lednum, self.on_ledcount, "#FFFFFF")
                self.on_ledon = False
                self.after(int(500/BLINKFRQ),self.onblink_led)
            else:
                self._send_ledcolor_to_ARDUINO(self.on_lednum, self.on_ledcount, "#000000")
                self.on_ledon = True
                self.after(int(500/BLINKFRQ),self.onblink_led)
        else:
            #self._send_ledcolor_to_ARDUINO(self.on_lednum, self.on_ledcount, "#000000")
            pass
            
    def switchoff_blink_led(self):
        self.ledhighlight = False
        self._send_ledcolor_to_ARDUINO(self.on_lednum, self.on_ledcount, "#000000")
                
    def get_coltab_macro(self):
        color_str = ""
        for i, key in enumerate(self.controller.palette):
            if color_str != "":
                color_str = color_str + ","
            keycolor = self.controller.palette[key]
            r,g,b = hexa_to_rgb(keycolor)
            color_str = color_str + str(r) + "," + str(g) + "," + str(b)
        macro_str = "Set_ColTab(" + color_str + ")"
        return macro_str
    
    def get_house_macro(self):
        color_str = ""
        for i, key in enumerate(self.controller.palette):
            if color_str != "":
                color_str = color_str + ","
            keycolor = self.controller.palette[key]
            r,g,b = hexa_to_rgb(keycolor)
            color_str = color_str + str(r) + "," + str(g) + "," + str(b)
        macro_str = "Set_ColTab(" + color_str + ")"
        return macro_str    

        # ====================================
    def xgetConfigData(self, key):
        return self.controller.getConfigData(key)
    
    def ledlist_cmd(self, _event):
        """Respond to user click on an ledlist item."""
        
        label = _event.widget
        key = label.key
        #count = 0
        #self.main_tab.set_lednum_count(int(key),1,scroll=False)
        #self.main_tab._update_ledtable_activestatus(int(key),1)
        #self.main_tab._show_macroparams(key)
        #no_of_LED_ch = self.controller.ledeffecttable.determine_no_of_LED_channels_key(key)
        #if no_of_LED_ch == 0: # mimal 1 LED channel needs to be selected
        #    no_of_LED_ch = 1
        #count += no_of_LED_ch
        count = 1 # test 
        self.set_lednum_count(int(key),count,scroll=False)
        self._update_ledtable_activestatus(int(key),1)
        self._show_macroparams(key)        
        
    def ledlist_shift_cmd(self, _event):
        """Respond to user shift click on an ledlist item."""
        
        label = _event.widget
        key = label.key
        key_int = int(key)
        cur_lednum = self.lednum.get()
        count = cur_lednum-key_int
        if count>0:
            new_key = key_int
        else:
            new_key = cur_lednum
            count = -count
        #count += 1
        # add associated channels for the macro
        no_of_LED_ch = self.controller.ledeffecttable.determine_no_of_LED_channels_key(key)
        if no_of_LED_ch == 0: # mimal 1 LED channel needs to be selected
            no_of_LED_ch = 1
        count += no_of_LED_ch
        self.set_lednum_count(new_key,count,scroll=False)
        self._update_ledtable_activestatus(new_key,count)
        self._show_macroparams(key)
        


