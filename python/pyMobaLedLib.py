# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 4.03
# * Author: Harold Linke
# * Date: January 7, 2021
# * Copyright: Harold Linke 2021
# *
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

#------------------------------------------------------------------------------
# CHANGELOG:
# 2020-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2021-01-07 v4.02 HL: - Else:, ByRef check done - first PoC release
# 2021-01-08 V4.03 HL: - added Workbook Save and Load
import sys
import os
import urllib
module_path = os.path.abspath(__file__)  # Full path to the module file
module_directory = os.path.dirname(module_path)  # Directory containing the module
sys.path.append(module_directory)
from vb2py.vbconstants import vbQuestion, vbYesNo, vbYes

import tkinter as tk
from tkinter import ttk,messagebox,filedialog, colorchooser
from mlpyproggen.configfile import ConfigFile
from mlpyproggen.dictFile import readDictFromFile, saveDicttoFile
from mlpyproggen.ConfigurationPage import ConfigurationPage
from mlpyproggen.ARDUINOConfigPage import ARDUINOConfigPage
from mlpyproggen.SerialMonitorPage import SerialMonitorPage, SerialThread
from mlpyproggen.ColorCheckPage import ColorCheckPage
from mlpyproggen.DCC_KeyboardPage import DCCKeyboardPage
from mlpyproggen.Prog_Generator import Prog_GeneratorPage
from mlpyproggen.Pattern_Generator import Pattern_GeneratorPage
import pattgen.MainMenu_Form as MainMenu
from mlpyproggen.ServoTestPage import ServoTestPage1
from mlpyproggen.ServoTestPage2 import ServoTestPage2
from mlpyproggen.VB2PyPage import VB2PYPage
from mlpyproggen.Z21MonitorPage import Z21MonitorPage
from mlpyproggen.ARDUINOMonitorPage import ARDUINOMonitorPage
from mlpyproggen.StartPage import StartPage
from mlpyproggen.SoundCheckPage import SoundCheckPage
from mlpyproggen.tooltip import Tooltip
from mlpyproggen.DefaultConstants import COLORCOR_MAX, CONFIG2PARAMKEYS, DEFAULT_CONFIG, DEFAULT_PARAM,LARGE_FONT, SMALL_FONT, VERY_LARGE_FONT, PROG_VERSION, DATA_VERSION, ProgGen_Min_Data_Version, Pattgen_Min_Data_Version, SIZEFACTOR,\
PARAM_FILENAME, CONFIG_FILENAME, DISCONNECT_FILENAME, CLOSE_FILENAME, FINISH_FILE, PERCENT_BRIGHTNESS, TOOLTIPLIST, SerialIF_teststring1,SerialIF_teststring2, MACRODEF_FILENAME, MACROPARAMDEF_FILENAME,LOG_FILENAME, ARDUINO_WAITTIME, COLORTESTONLY_FILE,BLINKFRQ,DEBUG
from scrolledFrame.ScrolledFrame import ScrolledFrame
from tkcolorpicker.spinbox import Spinbox
from tkcolorpicker.limitvar import LimitVar
from tkcolorpicker.functions import hsv_to_rgb, hexa_to_rgb, rgb_to_hexa, rgb_to_hsv
import platform
import traceback

import ExcelAPI.XLA_Application as P01
from mlpyproggen.tooltip import Tooltip_Canvas

from locale import getdefaultlocale
import os
import serial
import sys
import threading
import queue
import time
import logging
import logging.handlers
import webbrowser
import argparse
import subprocess
import shutil
from datetime import datetime
import proggen.M07_COM_Port_New as M07New
import proggen.M25_Columns as M25
import proggen.M18_Save_Load as M18
import proggen.M37_Inst_Libraries as M37
import proggen.M30_Tools as M30
import proggen.F00_mainbuttons as F00
import proggen.M09_Language as M09

# --- Translation - not used
EN = {}
FR = {}
DE = {"Red": "Rot", "Green": "Grün", "Blue": "Blau",
      "Hue": "Farbton", "Saturation": "Sättigung", "Value": "Helligkeit",
      "Cancel": "Beenden", "Color Chooser": "Farbwähler",
      "Alpha": "Alpha", "Configuration": "Einstellungen",
      "ROOM_COL0": "SetColTab Parameter: ROOM_COL0\nRaumfarbe 0 \nRechte Maustaste für Funktionen",
      "ROOM_COL1": "SetColTab Parameter: ROOM_COL1\nRaumfarbe 1 \nRechte Maustaste für Funktionen",
      "ROOM_COL2": "SetColTab Parameter: ROOM_COL2\nRaumfarbe 2 \nRechte Maustaste für Funktionen",
      "ROOM_COL3": "SetColTab Parameter: ROOM_COL3\nRaumfarbe 3 \nRechte Maustaste für Funktionen",
      "ROOM_COL4": "SetColTab Parameter: ROOM_COL4\nRaumfarbe 4 \nRechte Maustaste für Funktionen",
      "ROOM_COL5": "SetColTab Parameter: ROOM_COL5\nRaumfarbe 5 \nRechte Maustaste für Funktionen",
      "GAS_LIGHT D" : "SetColTab Parameter: GAS_LIGHT D\nSimuliert dunkles Gaslicht \nRechte Maustaste für Funktionen",
      "GAS LIGHT"   : "SetColTab Parameter: GAS LIGHT\nSimuliert Gaslicht \nRechte Maustaste für Funktionen",
      "NEON_LIGHT D": "SetColTab Parameter: NEON_LIGHT D\nSimuliert dunkles Neonlicht \nRechte Maustaste für Funktionen",
      "NEON_LIGHT M": "SetColTab Parameter: NEON_LIGHT M\nSimuliert mittel helles Neonlicht \nRechte Maustaste für Funktionen",
      "NEON_LIGHT"  : "SetColTab Parameter: NEON_LIGHT\nSimuliert Neonlicht \nRechte Maustaste für Funktionen",
      "ROOM_TV0 A"  : "SetColTab Parameter: ROOM_TV0 A\nRaumfarbe A - wenn TV0 aus ist \nRechte Maustaste für Funktionen",
      "ROOM_TV0 B"  : "SetColTab Parameter: ROOM_TV0 B\nRaumfarbe B - wenn TV0 aus ist \nRechte Maustaste für Funktionen",
      "ROOM_TV1 A"  : "SetColTab Parameter: ROOM_TV1 A\nRaumfarbe A - wenn TV1 aus ist \nRechte Maustaste für Funktionen",
      "ROOM_TV1 B"  : "SetColTab Parameter: ROOM_TV1 B\nRaumfarbe B - wenn TV1 aus ist \nRechte Maustaste für Funktionen",
      "SINGLE_LED"  : "SetColTab Parameter: SINGLE_LED \nEinzel LEDs \nRechte Maustaste für Funktionen",
      "SINGLE_LED D": "SetColTab Parameter: SINGLE_LED D\nEinzel LEDs dunkel \nRechte Maustaste für Funktionen"            
      }

try:
    TR = DE
    #if getdefaultlocale()[0][:2] == 'fr':
    #    TR = FR
    #else:
    #    if getdefaultlocale()[0][:2] == 'en':
    #        TR = EN
except ValueError:
    TR = DE

def _T(text):
    """Translate text."""
    return text

# ------------------------------


tabClassList_all = ( StartPage, ARDUINOMonitorPage,Prog_GeneratorPage, Pattern_GeneratorPage, ColorCheckPage, SoundCheckPage, DCCKeyboardPage, ServoTestPage1, ServoTestPage2, Z21MonitorPage, SerialMonitorPage, ARDUINOConfigPage, ConfigurationPage)
tabClassList_all_proggen = ( StartPage, ARDUINOMonitorPage,Prog_GeneratorPage, ColorCheckPage, SoundCheckPage, DCCKeyboardPage, ServoTestPage1, ServoTestPage2, Z21MonitorPage, SerialMonitorPage, ARDUINOConfigPage, ConfigurationPage)
tabClassList_mll_only = ( StartPage, ARDUINOMonitorPage,ColorCheckPage, SoundCheckPage, DCCKeyboardPage, ServoTestPage1, ServoTestPage2, Z21MonitorPage, SerialMonitorPage, ARDUINOConfigPage, ConfigurationPage)
tabClassList_SetColTab = (ColorCheckPage, SerialMonitorPage, ARDUINOConfigPage, ConfigurationPage)

#tabClassList_all = ( StartPage, ColorCheckPage, SoundCheckPage, DCCKeyboardPage, ServoTestPage, Z21MonitorPage, SerialMonitorPage, ARDUINOMonitorPage, ARDUINOConfigPage, ConfigurationPage)


# for compatibility with the "old" startpagenumber in the config file
# if startpagenumber is in this list the corresponding start page is opened, otherwise "ColorCheckPage"
startpageNumber2Name = { 
    "0": "ColorCheckPage",
    "1": "Prog_GeneratorPage",
    "2": "SerialMonitorPage",
    "3": "StartPage"
}

defaultStartPage = "ColorCheckPage"

ThreadEvent = None

# ----------------------------------------------------------------
# Class LEDColorTest
# ----------------------------------------------------------------

class pyMobaLedLibapp(tk.Tk):
    
    # ----------------------------------------------------------------
    # LEDColorTest __init__
    # ----------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        self.arduino = None
        self.mainfile_dir = os.path.dirname(os.path.realpath(__file__))
        caller = COMMAND_LINE_ARG_DICT.get("caller","")
        self.setcoltab_only = False
        caller_setcoltab = (caller == "SetColTab")
        self.colortest_only = COMMAND_LINE_ARG_DICT.get("colortest_only","")== "True"
        self.executetests = COMMAND_LINE_ARG_DICT.get("test","")== "True"
        self.loaddatafile = COMMAND_LINE_ARG_DICT["loaddatafile"]!="False"
        self.logfilename =  COMMAND_LINE_ARG_DICT["logfilename"]
        self.useARDUINO_IDE = COMMAND_LINE_ARG_DICT.get("useARDUINO_IDE", False)
        self.coltab = None
        self.checkcolor_callback = None
        self.ledhighlight = False
        
        self.oldTabName = ""
        
        self.show_colorcheckpage_only = caller_setcoltab
        self.show_setcoltab_save_button = caller_setcoltab or not self.colortest_only
        
        self.queue = queue.Queue(maxsize=100)
        self.readConfigData()
        self.ARDUINO_current_portname = ""
        self.ARDUINO_status = ""
        #self.ledtable = {"000": "#FFFFFF"}
        #self.init_ledgrouptable = {
        #                        "Gruppenname": {
        #                            "Name": "Gruppenname",
        #                            "params": {
        #                                "Group_Name": "Gruppenname",
        #                                "Group_Colour": "#FFFFFF",
        #                                "Group_Distributor": "",
        #                                "Group_Connector": "",
        #                                "Group_Comment": ""
        #                            }
        #                        },
        #                        "Gruppenname2": {
        #                            "Name": "Gruppenname",
        #                            "params": {
        #                                "Group_Name": "Gruppenname2",
        #                                "Group_Colour": "#FFFF00",
        #                                "Group_Distributor": "",
        #                                "Group_Connector": "",
        #                                "Group_Comment": ""
        #                            }
        #                        }                                
        #                    }        
        #self.ledeffecttable = ledeffecttable_class(self.init_ledgrouptable, self)
        #self.ledeffecttable.init_ledeffecttable()
        self.colorpalette = {}
        self.macroparams_value = {}
        #self.ledeffect_label_list = {}
        self.macroparams_var = {"dummy": {}}
        self.persistent_param_dict = {}
        self.macroparam_frame_dict = {}
        self.bind_keys_dict = {}
        self.platform=platform.platform().upper()
        self.buttonlist= []
        self.lednum_int = 0
        self.ledcount_int = 1
        self.max_ledcnt_list = []
        self.LED_baseadress = 0
        self.mobaledlib_version = 0
        self.activeworkbook = None
        
        #self.fontdict={}
        #self.fontdict["FontGeneral"] = ("Verdana", int(8 * self.getConfigData("FontGeneral")/100))
        #self.fontdict["FontTitle"] = ("Verdana", int(12 * self.getConfigData("FontTitle")/100))
        #self.fontdict["FontSpinbox"] = ("Verdana", int(8 * self.getConfigData("FontSpinbox")/100))
        #self.fontdict["FontLabel"] = ("Verdana", int(8 * self.getConfigData("FontLabel")/100))
        #self.fontdict["FontButton"] = ("Verdana", int(8 * self.getConfigData("FontLabel")/100))
        #self.fontdict["FontEntry"] = ("Verdana", int(8 * self.getConfigData("FontLabel")/100))
        #self.fontdict["FontText"] = ("Verdana", int(8 * self.getConfigData("FontLabel")/100))
        #self.fontdict["FontHelp"] = ("Verdana", int(8 * self.getConfigData("FontLabel")/100))
        #self.fontdict["FontScale"] = ("Verdana", int(8 * self.getConfigData("FontScale")/100))
        
        self.fontlabel = self.get_font("FontLabel")
        self.fontspinbox = self.get_font("FontSpinbox")
        self.fonttext = self.get_font("FontText")
        self.fontbutton = self.get_font("FontLabel")
        self.fontentry = self.get_font("FontLabel")
        self.fonttext = self.get_font("FontText")
        
        self.fontpattgen_sizenormal = int(self.getConfigData("FontNormal")/ScaleFactor)
        self.fontpattgen_sizelarge = int(self.getConfigData("FontLarge")/ScaleFactor)
        self.fontpattgen_sizesmall = int (self.getConfigData("FontSmall")/ScaleFactor)
        
        logging.debug("Font sizenormal: %s sizelarge: %s sizesmall: %s",self.fontpattgen_sizenormal,self.fontpattgen_sizelarge, self.fontpattgen_sizesmall)
        
        self.fontpattgen_name = self.getConfigData("FontName")
        self.defaultfontnormal = (self.fontpattgen_name, self.fontpattgen_sizenormal)
        self.defaultfontsmall = (self.fontpattgen_name, self.fontpattgen_sizesmall)
        self.defaultfontlarge = (self.fontpattgen_name, self.fontpattgen_sizelarge)
        self.cor_red = self.getConfigData("led_correction_r")
        self.cor_green = self.getConfigData("led_correction_g")
        self.cor_blue = self.getConfigData("led_correction_b")
        macrodata = self.MacroDef.data.get("StartPage",{})
        
        self.show_pyPrgrammGenerator = self.getConfigData("ShowProgramGenerator")
        self.show_pyPatternGenerator = self.getConfigData("ShowPatternGenerator")
        self.show_hiddentables = self.getConfigData("ShowHiddentables")
        
        self.tempLedeffecttableFilname = macrodata.get("TEMP_LEDEFFECTTABLE_FILENAME","StartPage")
        self.tempworkbookFilname = macrodata.get("TEMP_WORKBOOK_FILENAME","StartPage")

        # Structure:
        # self.serial_port_dict={"COM3": {
        #                         "dcc_address_range": (0,1024),   # the port select in the configuration
        #                         "ARDUINO" : None}
        #                       }
        
        self.serial_port_dict={}
        
        self.currentTabClass = ""
        self.maxLEDcnt = self.getConfigData("MaxLEDcnt")
        self.paramDataChanged = False
        self.palette = {}
        self.connection_startup = False
        self.ProgVersion = PROG_VERSION
        self.DataVersion = DATA_VERSION
        self.ProgGenMinDataVersion = ProgGen_Min_Data_Version
        self.PattGenMinDataVersion = Pattgen_Min_Data_Version
        
        self.tooltip_var_dict = {}

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.report_callback_exception = self.show_tkinter_exception
        self.update()
        #default_font = tk.font.nametofont("TkDefaultFont")
        #default_font.configure(family="Arial", size=11)        
        
        #print(self.getConfigData("pos_x"), self.getConfigData("pos_y"))
        #print(self.getConfigData("win_height"), self.getConfigData("win_width"))
        self.window_height= self.getConfigData("win_height")
        
        if self.window_height<500:
            self.window_height=1080
        self.window_width = self.getConfigData("win_width")
        if self.window_width<500:
            self.window_width=1920
        self.pos_x= self.getConfigData("pos_x")
        self.pos_y = self.getConfigData("pos_y")
        self.lastactive_tabname = self.getConfigData("lastactive_tabname") 
        
        #if self.getConfigData("pos_x") < 1920 and self.getConfigData("pos_y") < 1080:
        #    self.geometry('%dx%d+%d+%d' % (self.window_width,self.window_height,self.getConfigData("pos_x"), self.getConfigData("pos_y")))        

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        logging.debug("Screenwidht: %s Screenheight: %s ScaleFactor: %s",screen_width,screen_height, ScaleFactor)

        if screen_width< 1920:
            SIZEFACTOR_width = screen_width/1280
            self.window_width=screen_width
        
        if screen_height < 1080:
            self.window_height=screen_height
            
        logging.debug("Windowwidth: %s Windowheight: %s",self.window_width,self.window_height)
        logging.debug("pos_x: %s pos_y: %s",self.pos_x,self.pos_y)
        
        if self.getConfigData("pos_x") < screen_width and self.getConfigData("pos_y") < screen_height:
            self.geometry('%dx%d+%d+%d' % (self.window_width,self.window_height,self.pos_x, self.pos_y))
        else:
            self.geometry("%dx%d+0+0" % (self.window_width,self.window_height))

        #geometry = self.winfo_geometry()
        #print(geometry, self.getConfigData("pos_x"), self.getConfigData("pos_y"))        

        tk.Tk.wm_title(self, "MobaLedLib " + PROG_VERSION)

        self.title("MobaLedLib " + PROG_VERSION)
        self.transient(self.master)
        #self.resizable(False, False)
        self.resizable(True,True)
        #self.rowconfigure(1, weight=1)

        self.color = ""
        style = ttk.Style(self)
        style.map("palette.TFrame", relief=[('focus', 'sunken')],
                  bordercolor=[('focus', "#4D4D4D")])
        self.configure(background=style.lookup("TFrame", "background"))
         
        menu = tk.Menu(self)
        self.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="Datei", menu=filemenu)
#        filemenu.add_command(label="Farbpalette von Datei lesen", command=self.OpenFile)
#        filemenu.add_command(label="Farbpalette speichern als ...", command=self.SaveFileas)
#        filemenu.add_separator()
        filemenu.add_command(label="MacroWorkbook von Datei lesen", command=self.OpenFileWorkbook)
        filemenu.add_command(label="MacroWorkbook speichern als", command=self.SaveFileWorkbook)
        filemenu.add_separator()
        filemenu.add_command(label="ProgramGenerator: PGF-Datei lesen", command=self.OpenFilePGF)
        filemenu.add_command(label="ProgramGenerator: PGF-Datei speichern", command=self.SaveFilePGF)
        filemenu.add_separator()
        filemenu.add_command(label="PatternGenerator: PCF-Datei lesen", command=self.OpenFilePCF)
        filemenu.add_command(label="PatternGenerator: Alle Seiten als PCF-Datei speichern", command=self.SaveAllFilePCF)
        filemenu.add_command(label="PatternGenerator: Aktuelle Seite als PCF-Datei speichern", command=self.SaveCurSheetFilePCF)
        filemenu.add_separator()                
        filemenu.add_command(label="Beenden und Konfig-Daten speichern", command=self.ExitProg_with_save)
        filemenu.add_command(label="Beenden ohne Konfig-Daten zu speichern", command=self.ExitProg)

        colormenu = tk.Menu(menu)
        menu.add_cascade(label="Farbpalette", menu=colormenu)
        colormenu.add_command(label="letzte Änderung Rückgängig machen [CTRL-Z]", command=self.MenuUndo)
               
        colormenu.add_command(label="von Datei lesen", command=self.OpenFile)
        colormenu.add_command(label="speichern als ...", command=self.SaveFileas)
        colormenu.add_separator()
        colormenu.add_command(label="auf Standard zurücksetzen", command=self.ResetColorPalette)
        
        colormenu = tk.Menu(menu)
        menu.add_cascade(label="Tabelle", menu=colormenu)
        colormenu.add_command(label="Refresh Icons", command=self.MenuRefreshIcons)

        arduinomenu = tk.Menu(menu)
        menu.add_cascade(label="ARDUINO", menu=arduinomenu)
        arduinomenu.add_command(label="Verbinden", command=self.ConnectArduino)
        arduinomenu.add_command(label="Trennen", command=self.DisconnectArduino)
        arduinomenu.add_command(label="Alle LED aus", command=self.SwitchoffallLEDs)
        
        #optionsmenu = tk.Menu(menu)
        #menu.add_cascade(label="Optionen", menu=optionsmenu)
        #optionsmenu.add_command(label="Aktualisiere Bibliothek", command=self.update_library)
        #optionsmenu.add_command(label="Installiere Beta Test", command=self.install_Betatest)
        #optionsmenu.add_command(label="Status der Bibliotheken", command=self.library_status)
        #optionsmenu.add_command(label="Schnelle Bootloader installieren", command=self.install_fast_bootloader)
        
        #patternconfmenu = tk.Menu(menu)
        #menu.add_cascade(label="Pattern Configurator", menu=patternconfmenu)
        #patternconfmenu.add_command(label="Starte Pattern Cofigurator", command=self.start_patternconf)
        #patternconfmenu.add_command(label="Daten an Pattern Conf senden", command=self.send_to_patternconf)
        #patternconfmenu.add_command(label="Daten von Pattern Conf empfangen", command=self.receiver_from_patternconf)
        
        helpmenu = tk.Menu(menu)
        menu.add_cascade(label="Hilfe", menu=helpmenu)
        helpmenu.add_command(label="Hilfe öffnen", command=self.OpenHelp)
        helpmenu.add_command(label="Logfile öffnen", command=self.OpenLogFile)
        helpmenu.add_command(label="Update pyMobaLedLib", command=self.UpdatePyMLL)
        helpmenu.add_command(label="Über...", command=self.About)
        
        testmenu = tk.Menu(menu)
        #menu.add_cascade(label="Test", menu=testmenu)
        testmenu.add_command(label="Excel-Datei importieren", command=self.OpenExcelWorkbook)
        testmenu.add_command(label="Lines of Code", command=self.find_loc)
        
        self.messageframe = ttk.Frame(self)
        
        self.connectstatusmessage = tk.Label(self.messageframe, text='Status:', fg="black",bd=1, relief="sunken", anchor="w")
        self.connectstatusmessage.grid(row=0,column=0,sticky="ew")
        #self.statusmessage.pack(side="bottom", fill="x")
        self.ToolTip(self.connectstatusmessage, text="Zeigt den Status der Verbindung zum ARDUINO an: \nVerbunden - eine Verbindung zum ARDUINO steht\nNicht verbunden - keine Verbindung zum ARDUINO")
        
        self.statusmessage = tk.Label(self.messageframe, text=' ', fg="black",bd=1, relief="sunken", anchor="w")
        self.statusmessage.grid(row=0,column=1,sticky="ew")
        #self.statusmessage.pack(side="bottom", fill="x")
        self.ToolTip(self.statusmessage, text="Zeigt Meldungen und Fehler an")
        
        self.messageframe.grid_columnconfigure(0, weight=1, uniform="group1")
        self.messageframe.grid_columnconfigure(1, weight=1, uniform="group1")
        self.messageframe.grid_rowconfigure(0, weight=1)
        
        self.messageframe.grid(row=1,column=0,sticky="nesw")        
                
        #filemenu.add_command(label="MacroWorkbook speichern als", command=self.SaveFileWorkbook)        

        # --- define container for tabs
        
        #self.scrolledframe = VerticalScrolledFrame(self)
        #self.scrolledframe.pack(side="top", fill="both", expand = True)
        
        #self.container = ttk.Notebook(self.scrolledframe.interior)
        self.shutdown_frame = tk.Frame(self)
        
        shutdown_label = tk.Label(self.shutdown_frame,text="Shutting Down ...",font=VERY_LARGE_FONT)
        shutdown_label.grid(row=0,column=0,sticky="nesw")
        self.shutdown_frame.grid(row=0,column=0,sticky="nesw")
        self.shutdown_frame.grid_columnconfigure(0,weight=1)
        self.shutdown_frame.grid_rowconfigure(0,weight=1)
        
        #************************************
        #* Create Excel Application - parentframe=None, because the workbooks ProgGen and PattConf will have different frames in the notebook
        #************************************
        self.ExcelApplication = P01.CApplication(caption="pyMobaLedLib", Path=self.mainfile_dir, p_global_controller=self)
        
        use_horizontalscroll=True
        use_fullscroll=True
        use_verticalscroll = True
        #if use_verticalscroll:
        #    self.scrolledcontainer = VerticalScrolledFrame(self)
        #if use_horizontalscroll:
        #    self.scrolledcontainer = HorizontalScrolledFrame(self)
        if use_fullscroll:
            self.scrolledcontainer = ScrolledFrame(self)
            
        if use_verticalscroll or use_fullscroll or use_horizontalscroll:
            self.scrolledcontainer.grid(row=0,column=0,rowspan=1,columnspan=2,sticky="nesw")
            self.scrolledcontainer.grid_rowconfigure(0, weight=1)
            self.scrolledcontainer.grid_columnconfigure(0, weight=1)
            maincontainer = tk.Frame(self.scrolledcontainer.interior, width=self.window_width-30, height=self.window_height-30)
            maincontainer.grid(row=0,column=0,columnspan=2,sticky="nesw")
            maincontainer.grid_rowconfigure(0, weight=1)
            maincontainer.grid_columnconfigure(0, weight=1)
            self.container = ttk.Notebook(maincontainer)
        else:
            self.container = ttk.Notebook(self)
            
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.container.grid(row=0,column=0,columnspan=2,sticky="nesw")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.tabdict = dict()
        self.tabdict_frames = dict()
        
        if self.show_colorcheckpage_only:
            tabClassList = tabClassList_SetColTab
        else:
            if self.show_pyPrgrammGenerator:
                tabClassList = tabClassList_all_proggen #all Pages except PatternGenerator
                if self.show_pyPatternGenerator:
                    tabClassList = tabClassList_all # all Pages
            else:
                tabClassList = tabClassList_mll_only #no ProgGen and no PattGen
        
        tabClassList = tabClassList_all #test, always show all pages 
        
        if COMMAND_LINE_ARG_DICT.get("vb2py","")=="True":
            tabClassList += (VB2PYPage, )
        
        for tabClass in tabClassList:
            frame = tabClass(self.container,self)
            tabClassName = frame.tabClassName
            self.tabdict[tabClassName] = frame
            self.container.add(frame, text=frame.tabname)
        
        self.container.insert(10, self.tabdict["ARDUINOMonitorPage"])
        
        self.continueCheckDisconnectFile = True
        self.onCheckDisconnectFile()
        
        self.container.bind("<<NotebookTabChanged>>",self.TabChanged)
        
        # set ProgranGeneraor as aktive workbook.
        P01.Application.setActiveWorkbook("ProgGenerator")
        
        # set final startpagew
        if self.lastactive_tabname == "":
            startpagename = self.getStartPageClassName()
            self.showFramebyName(startpagename)
        else:
            self.showFramebyName(self.lastactive_tabname)
        
        filedir = self.mainfile_dir # os.path.dirname(os.path.realpath(__file__))
        self.update()
        #for wb in P01.Workbooks:
        #    # test 15.4.2024wb.init_workbook()
        #    if self.getConfigData("AutoLoadWorkbooks"):
        #            temp_workbook_filename = os.path.join(filedir,self.tempworkbookFilname+"_"+wb.Name+".json")
        #            #wb.Load(filename=temp_workbook_filename)
        
        self.messageframe = ttk.Frame(self)
        
        self.connectstatusmessage = tk.Label(self.messageframe, text='Status:', fg="black",bd=1, relief="sunken", anchor="w")
        self.connectstatusmessage.grid(row=0,column=0,sticky="ew")
        #self.statusmessage.pack(side="bottom", fill="x")
        self.ToolTip(self.connectstatusmessage, text="Zeigt den Status der Verbindung zum ARDUINO an: \nVerbunden - eine Verbindung zum ARDUINO steht\nNicht verbunden - keine Verbindung zum ARDUINO")
        
        self.statusmessage = tk.Label(self.messageframe, text=' ', fg="black",bd=1, relief="sunken", anchor="w")
        self.statusmessage.grid(row=0,column=1,sticky="ew")
        #self.statusmessage.pack(side="bottom", fill="x")
        self.ToolTip(self.statusmessage, text="Zeigt Meldungen und Fehler an")
        
        self.messageframe.grid_columnconfigure(0, weight=1, uniform="group1")
        self.messageframe.grid_columnconfigure(1, weight=1, uniform="group1")
        self.messageframe.grid_rowconfigure(0, weight=1)
        
        self.messageframe.grid(row=1,column=0,sticky="nesw")
        
        if COMMAND_LINE_ARG_DICT.get("z21simulator","")=="True":
            # start the Z21 simulator
            frame = self.tabdict.get("Z21MonitorPage",None)
            if frame:
                frame.start_process_Z21()
                
        if COMMAND_LINE_ARG_DICT.get("test","")=="True":
            self.executetests = True
        else:
            self.executetests = False
        
        self.arduinoMonitorPage=self.getFramebyName ("ARDUINOMonitorPage")
        
        self.focus_set()
        #self.wait_visibility()

        self.lift()
        self.grab_set()
        
    def show_tkinter_exception(self, exc,val,tb):
        err = traceback.format_exception(exc,val,tb)
        messagestring = ""
        for line in err:
            messagestring+=line
        messagebox.showerror('Exception',messagestring)
        #print("Tkinter Exception:",messagestring)
        logging.debug("Tkinter Exception:\n"+messagestring)
        if DEBUG and not "Error in Dialog" in line:
            raise
        
    def check_data_changed(self):
        if self.activeworkbook != None:
            data_changed = self.activeworkbook.check_Data_Changed()
        else:
            data_changed = False
        return self.paramDataChanged or data_changed

    def get_font(self,fontname):
        font_size = self.getConfigData(fontname)
        if str(font_size) == "":
            return SMALL_FONT
        else:
            return ("Verdana", int(font_size))
        
    def notimplemented(self,command):
        n = tk.messagebox.showinfo(command,
                               "Not implemented yet",
                                parent=self)        

    def SaveFileas(self):
        filepath = filedialog.asksaveasfilename(filetypes=[("Color Palette files","*.clr.json")],defaultextension=".clr.json")
        if filepath:
            frame = self.tabdict["ColorCheckPage"]
            frame.savePalettetoFile(filepath) 

    def SaveFile(self):
        filepath = PARAM_FILENAME
        if filepath:
            frame = self.tabdict["ColorCheckPage"]
            frame.savePalettetoFile(filepath) 

    def OpenFile(self):
        filepath = filedialog.askopenfilename(filetypes=[("Color Palette files","*.clr.json"),("All JSON files","*.json")],defaultextension=".clr.json")
        if filepath:
            frame = self.tabdict["ColorCheckPage"]
            frame.readPalettefromFile(filepath)         

    def SaveFileWorkbook(self):
        self.activeworkbook.Save()

    def OpenFileWorkbook(self):
        self.activeworkbook.Load()
        
    def SaveFilePGF(self):
        M18.Save_Data_to_File()

    def OpenFilePGF(self):
        M18.Load_Data_from_File()
        
    def SaveAllFilePCF(self):
        MainMenu.SaveAllExamplesButton_Click()
        
    def SaveCurSheetFilePCF(self):
        MainMenu.SaveActualExampleButton_Click()

    def OpenFilePCF(self):
        MainMenu.LoadExampleButton_Click()

    def find_loc(self,cd = os.curdir):
        listdir = os.listdir(cd)
        if len(listdir) == 0:
            return 0
        loc = 0;
        files = []
        folders = []
        next_dirs = []
        total_loc=0
        for x in listdir:
            path = os.path.join(cd, x)
            if os.path.isfile(path):
                if x.endswith(".py"):
                    files.append(x)
                    file = open(path, 'r')
                    try:
                        for line in file:
                            if line == '':
                                continue
                            loc += 1
                    except:
                        pass
            elif os.path.isdir(path):
                folders.append(x)
                next_dirs.append(path)
        #print(f'cd: {cd}')
        #print(f'files ({len(files)}): {files}')
        #print(f'dirs: {folders}')
        #print(f'loc: {loc}\n')
        for next_dir in next_dirs:
            loc += self.find_loc(next_dir)
        
        return loc

    def About(self):
        messagebox.showinfo('About',"pyMobaLedLib by Harold"+"\n\n"+ "Version "+ PROG_VERSION)

    def OpenHelp(self):
        self.call_helppage()
        
    def UpdatePyMLL(self):
        self.check_version(exec_update=True)
        
    def OpenLogFile(self):
        logging.debug("Open logfile: %s",self.logfilename)
        dst = self.logfilename + ".tmp.log"     # logfile is locked by logger, open a copy with the os specific viewer
        shutil.copyfile(self.logfilename, dst)
        #subprocess.run(dst, shell=True)
        subprocess.Popen(dst, shell=True)
        
    def OpenExcelWorkbook(self):
        self.activeworkbook.LoadExcelWorkbook()    

    def ResetColorPalette(self):
        frame = self.tabdict["ColorCheckPage"]
        frame.palette_reset_colors()

    def MenuUndo(self,_event=None):
        for key in self.tabdict:
            if hasattr(self.tabdict[key], "MenuUndo"):
                self.tabdict[key].MenuUndo() 
    
    def MenuRedo(self,_event=None):
        for key in self.tabdict:
            self.tabdict[key].MenuRedo()
            
    def MenuRefreshIcons(self):
        self.activeworkbook.refreshicons()

    def ConnectArduino(self):
        self.connect()

    def DisconnectArduino(self):
        self.disconnect()

    def SwitchoffallLEDs(self):
        # switch off all LED
        if self.controller.mobaledlib_version == 1:
            message = "#L00 00 00 00 FF\n"
        else:
            message = "#L 00 00 00 00 7FFF\n"          
        #message = "#L00 00 00 00 FF\n"
        self.send_to_ARDUINO(message)

    def update_library(self):
        M37.Update_MobaLedLib_from_Arduino_and_Restart_Excel()
    
    def install_Betatest(self):
        self.activeworkbook.install_Betatest()
    
    def library_status(self):
        self.activeworkbook.library_status()
    
    def install_fast_bootloader(self):
        self.activeworkbook.install_fast_bootloader()
        
    def start_patternconf(self):
        self.activeworkbook.start_patternconf()
    
    def send_to_patternconf(self):
        self.activeworkbook.send_to_patternconf()
    
    def receiver_from_patternconf(self):
        self.activeworkbook.receiver_from_patternconf()
        
    def ExitProg(self):
        self.cancel()
        
    def ExitProg_with_save(self):
        self.cancel_with_save()    

    def xsaveLEDTabtoFile(self, filepath):
               
        temp_dict = {"ledeffecttable":self.ledeffecttable.get_table(),
                     "ledgrouptable" :self.ledeffecttable.mledgrouptable}
        
        saveDicttoFile(filepath, temp_dict)

    def xreadLEDTabfromFile(self, filepath,tabselection=True):
        temp_dict = readDictFromFile(filepath)
        if temp_dict:
            temp_led_effect_table = temp_dict.get("ledeffecttable",{}) 
            if self.ledeffecttable.keys() != temp_led_effect_table.keys(): # check if the read led list has the corect keys
                logging.debug("Error in led list file %s - %s",filepath,temp_led_effect_table.keys())
                messagebox.showerror("Led List file incorrect format","Led List file could not be opened, incorrect format")
            else:
                self.ledeffecttable.set_table(temp_led_effect_table)
                self.ledeffecttable.mledgrouptable  = temp_dict.get("ledgrouptable",{})
        if tabselection:
            self.current_tab.tabselected()
        
    def save_persistent_params(self):
        for macro in self.persistent_param_dict:
            persistent_param_list = self.persistent_param_dict[macro]
            for paramkey in persistent_param_list:
                self.setConfigData(paramkey, self.get_macroparam_val(macro, paramkey))
            
    # ----------------------------------------------------------------
    #  cancel_with_save
    # ----------------------------------------------------------------
    def cancel_step2_with_save(self):
        logging.debug("Cancel_with_save2")
        self.setConfigData("pos_x", self.winfo_x())
        self.setConfigData("pos_y", self.winfo_y())
        self.setConfigData("lastactive_tabname", self.lastactive_tabname)
        logging.debug("Cancel_Save_Data: pos_x=%s pos_y=%s",self.winfo_x(), self.winfo_y())
        self.save_persistent_params()
        self.SaveConfigData()
        self.SaveParamData()
        filedir = self.mainfile_dir # os.path.dirname(os.path.realpath(__file__))
        #temp_ledeffecttable_filename = os.path.join(filedir,self.tempLedeffecttableFilname)
        #self.saveLEDTabtoFile(temp_ledeffecttable_filename)
        for wb in P01.Workbooks:
            wb.Evt_Workbook_BeforeClose()
            temp_workbook_filename = wb.workbookfilename
            if temp_workbook_filename == None:
                temp_workbook_filename = os.path.join(filedir,self.tempworkbookFilname+"_"+wb.Name+".json")
            wb.Save(filename=temp_workbook_filename)        
        self.close_notification()
        
    def cancel_step2_without_save(self):
        logging.debug("Cancel_without_save2")
        for wb in P01.Workbooks:
            wb.Evt_Workbook_BeforeClose()
        self.close_notification()           

    # ----------------------------------------------------------------
    #  cancel_with_save
    # ----------------------------------------------------------------
    def cancel_with_save(self):
        logging.debug("Cancel_with_save")
        self.set_connectstatusmessage("Closing program...",fg="red")
        self.shutdown_frame.tkraise()
        self.update()        
        self.cancel_step2_with_save()   

        #open(FINISH_FILE, 'a').close()                                       # 03.12.19:
        #self.disconnect()
        #self.continueCheckDisconnectFile = False
        #self.destroy()

    # ----------------------------------------------------------------
    #  cancel_without_save
    # ----------------------------------------------------------------
    def cancel_without_save(self):
        logging.debug("Cancel_without_save")
        self.set_connectstatusmessage("Closing program...",fg="red")
        #i=0
        #for key in self.tabdict:
        #    #self.tabdict[key].cancel()
        #    self.container.tab(i, state="disabled")
        #    i+=1        
        #self.after(500, self.cancel_step2_without_save) # a trick to show the close message before closing
        
        self.shutdown_frame.tkraise()
        self.update()
        self.cancel_step2_without_save()

    # ----------------------------------------------------------------
    #  cancel
    # ----------------------------------------------------------------
    def cancel(self):
        logging.debug("Cancel")
        if self.check_data_changed():
            answer = tk.messagebox.askyesnocancel ('Das Programm wird beendet','Daten wurden verändert. Sollen die Daten gesichert werden?',default='no')
            if answer == None:
                return # no cancelation
            
            if answer:
                self.cancel_with_save() 
            else:
                self.cancel_without_save()
        else:
            self.cancel_without_save()
            
    # ----------------------------------------------------------------
    #  restart program
    # ----------------------------------------------------------------
    def restart(self):
        logging.debug("Restart requested")
        answer = tk.messagebox.askyesnocancel ('Das Programm wird beendet und neu gestartet','Daten wurden verändert. Sollen die Daten gesichert werden?',default='no')
        if answer == None:
            return # no cancelation
        if answer:
            self.cancel_with_save() 
        else:
            self.cancel_without_save()
        #restart program
        logging.debug("Restart")
        logging.debug("sys.executable: %s, sys.argv: %s", sys.executable, repr(sys.argv))
        os.execv(sys.executable, ["python"] + sys.argv)
        
        #############################################


    def close_notification(self):
        logging.debug("Close_notification")
        for key in self.tabdict:
            self.tabdict[key].cancel()
        self.setConfigData("pos_x", self.winfo_x())
        self.setConfigData("pos_y", self.winfo_y())
        if self.ParamData.data == {}: # ParamData is not used, interface is config data. In this case do not save config data - compatibility modus
            self.SaveConfigData()
        try: #create a FINISH_File if possible to show the mobaledlib program that the program finished - ignore any error
            open(FINISH_FILE, 'a').close()                                       # 03.12.19:
        except:
            pass
        self.disconnect()
        self.continueCheckDisconnectFile = False
        logging.debug("Destroy")
        self.destroy()        
        
    # ----------------------------------------------------------------
    # show_frame byName
    # ----------------------------------------------------------------
    def showFramebyName(self, pageName):
        frame = self.tabdict.get(pageName,None)
        if frame == None:
            pageName = "ColorCheckPage"
            frame = self.tabdict.get(pageName,None)
        if pageName == "ColorCheckPage":
            frame._update_cor_rgb()
        self.container.select(self.tabdict[pageName])

    # ----------------------------------------------------------------
    # Event TabChanged
    # ----------------------------------------------------------------
    def TabChanged(self,_event=None):
        self.oldTabName = self.currentTabClass
        if self.oldTabName != "":
            self.oldtab = self.nametowidget(self.oldTabName)
            self.oldtab.tabunselected()
        newtab_name = self.container.select()
        if newtab_name != "":
            newtab = self.nametowidget(newtab_name)
            self.currentTabClass = newtab_name
            self.current_tab = newtab
            self.lastactive_tabname = newtab.tabClassName
            newtab.tabselected()
        logging.debug("TabChanged %s - %s",self.oldTabName,newtab_name)

    # ----------------------------------------------------------------
    # setParamDataChanged
    # ----------------------------------------------------------------        
    def setParamDataChanged(self):
        self.paramDataChanged=True
        
    # ----------------------------------------------------------------
    # startup_system
    # ----------------------------------------------------------------             
    def startup_system(self):
        if True: #self.getConfigData("autoconnect"):
            port_name = self.getConfigData("serportname")
            logging.debug("Portname: "+ str(port_name))
            if P01.checkplatform("Darwin"):
                logging.debug("startup-system: MAC - no NO DEVICE check")
                self.connect()
            else:
                if port_name.upper() == "NO DEVICE" or port_name=="":
                    logging.debug("startup-system: NO DEVICE  handling")
                    macrodata = self.MacroDef.data.get("StartPage")
                    msg_no_device_title = macrodata.get("MSG_NO_DEVICE_title","")
                    msg_no_device = macrodata.get("MSG_NO_DEVICE","")
                    answer = tk.messagebox.askyesnocancel (msg_no_device_title, msg_no_device, default='no')
                    logging.debug("Portname: No DEVICE question - answer:"+ str(answer))
                    if answer == None:
                        return
                    
                    if answer==True:
                        logging.debug("pyMobaLedLib.startup_system: Show_USB_Port_Dialog")
                        ComPortColumn = M25.COMPort_COL
                        ComPort=" "
                        res, ComPort= M07New.Show_USB_Port_Dialog(ComPortColumn, ComPort) 
                        self.setConfigData("serportname",ComPort)
                        #self.showFramebyName("ARDUINOConfigPage")
                        self.connect()
                else:
                    self.connect()
        
    # ----------------------------------------------------------------
    # LEDColorTest connect ARDUINO
    # ----------------------------------------------------------------
    def connect(self,port=None):
        if port == None:
            port = self.getConfigData("serportname")
        logging.debug("connect %s",port)
        self.ARDUINO_message = ""
        timeout_error = False
        read_error =False
        text_string = "ERROR"
        
        if self.arduino and self.arduino.isOpen():
            #if port == self.ARDUINO_current_portname:
            #    return # port already open
            self.disconnect()
            self.set_connectstatusmessage("Nicht Verbunden",fg="black")

        if port.upper()!="NO DEVICE":
            self.set_connectstatusmessage("Versuch sich mit dem ARDUINO am Port "+ port + " zu verbinden ...",fg="red")
            self.update()
            # it is possible that during the update procedure the port was opened already - check again
            if self.arduino and self.arduino.isOpen():
                if port == self.ARDUINO_current_portname:
                    return # port already open            
            try:
                self.ARDUINO_status = "Connecting"
                baudrate = self.getConfigData("baudrate")
                baudrate = 115200
                self.arduino = serial.Serial(port,baudrate=baudrate,timeout=2,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
                logging.debug("connected to: %s Baudrate: %s", self.arduino.portstr,baudrate)
            except BaseException as e:
                logging.debug(e, exc_info=True) 
                #messagebox.showerror("Error connecting to the serial port " + self.getConfigData("serportname"),
                #                     "Serial Interface to ARDUINO could not be opened!\n"
                #                     "\n"
                #                     "Check if the ARDUINO is connected to the correct port\n"
                #                     "or if an other program is using the serial port\n")
                # 
                macrodata = self.MacroDef.data.get("StartPage")
                msg_connect_open_error_title = macrodata.get("connect_open_error_title","")
                msg_connect_open_error = macrodata.get("msg_connect_open_error","")
                msg_connect_open_error = msg_connect_open_error.format(port)
                answer = tk.messagebox.askyesnocancel (msg_connect_open_error_title, msg_connect_open_error, default='no')
                if answer == None:
                    pass 
                if answer:
                    #open ARDUINO Comport Selection
                    ComPortColumn = M25.COMPort_COL
                    ComPort=" "
                    res, ComPort= M07New.Show_USB_Port_Dialog(ComPortColumn, ComPort) 
                    if res:
                        return self.connect(port=ComPort)
                    else:
                        self.arduino = None
                        self.ARDUINO_status = ""
                        self.set_connectstatusmessage("Nicht Verbunden",fg="black")
                        return False                        
                    #self.showFramebyName("ARDUINOConfigPage") 
                else:
                    self.arduino = None
                    self.ARDUINO_status = ""
                    self.set_connectstatusmessage("Nicht Verbunden",fg="black")
                    return False
            # reset ARDUINO
            try:
                #self.arduino.dtr = True
                #time.sleep(0.250)
                #self.arduino.dtr = False
                #time.sleep(1)
                pass
            except:
                logging.debug("Connect: Error Reset ARDUINO!")
            #time.sleep(1)
            self.send_to_ARDUINO("#?\r\n")
            logging.debug ("send #?")
            time.sleep(0.250)            
            no_of_trails = 25
            emptyline_no = 0
            for i in range(no_of_trails):
                try:
                    text=""
                    timeout_error = True
                    text = self.arduino.readline()
                    logging.debug (text)
                    timeout_error = False
                    # check if feedback is from MobaLedLib
                    text_string = str(text.decode('utf-8'))
                    if text_string == "":
                        emptyline_no +=1
                        if emptyline_no>2:
                            read_error = True
                            logging.debug("Connect Error: %s - trial:%s",text_string,i+1)                            
                            break
                    
                    if not SerialIF_teststring1 in text_string:
                        read_error = True
                        logging.debug("Connect Error: %s - trial:%s",text_string,i+1)
                    else:
                        if "MobaLedLib" in text_string:
                            self.mobaledlib_version = 1
                        else:
                            self.mobaledlib_version = 2
                        self.queue.put(text_string)
                        logging.debug("Connect message: %s", text_string)
                        read_error = False
                        break
                except (IOError,UnicodeDecodeError) as e:
                    logging.debug(e)
                    logging.debug("Connect Error:%s",text_string)
                    read_error = True
            self.send_to_ARDUINO("#X\r\n")
            if read_error:         
                messagebox.showerror("Error when reading Arduino answer",
                                     "Wrong answer from ARDUINO:\n"
                                     " '" + str(text_string) + "'\n"
                                     "\n"
                                     "Check if the correct MobaLedLib program is loaded to the arduino.\nYou can upload the MobaLedLib program using the 'send to ARDUINO' Button in the ProgrammGenerator page"
                                     )
                self.set_connectstatusmessage("Nicht Verbunden",fg="black")
                self.arduino = None
                self.ARDUINO_status = ""
                return False                

            if timeout_error:         # 03.12.19: more detailed error message
                messagebox.showerror("Timeout waiting for the Arduino answer",
                                     "ARDUINO is not answering.\n"
                                     "\n"
                                     "Check if the correct program is loaded to the arduino.\n")
                self.set_connectstatusmessage("Nicht Verbunden",fg="black")
                self.arduino = None
                self.ARDUINO_status = ""
                return False
            else:
                self.connection_startup = True
                self.connection_startup_time = 100 # 5 seconds time to send the correct messages
                self.connection_startup_answer = False
                self.ARDUINO_current_portname = port
                
                for key in self.tabdict:
                    self.tabdict[key].connect(port)
                    
                    
                port_dcc_data = self.serial_port_dict.get(str(port),{})
                if port_dcc_data != {}:
                    port_dcc_data["ARDUINO"] = self.arduino
                else:
                    self.serial_port_dict[str(port)] ={"dcc_address_range": (1,9999), 
                                                  "ARDUINO" : self.arduino}
                    logging.info(" %s added to Z21 list",port)
                            
                #self.set_connectstatusmessage("Verbunden mit "+ self.ARDUINO_current_portname + " - Warten auf korrekte Antwort von ARDUINO ...",fg="orange")
                
                self.set_connectstatusmessage("Verbunden mit "+ self.ARDUINO_current_portname + " - EFFECT Mode",fg="green")
                self.connection_startup = False
                self.connection_startup_answer = True
                self.ARDUINO_status = "Connected"                
                return True
            return False
        else:
            return False

    # ----------------------------------------------------------------
    # LEDColorTest connect ARDUINO
    # ----------------------------------------------------------------
    def connect_Z21(self,port,dcc_adress_range):

        logging.debug("connect_Z21 ", port)
        if port == self.getConfigData("serportname"):
            self.disconnect()
            self.ARDUINO_status = ""
        
        arduino = None
        port_dcc_data = self.serial_port_dict.get(port,{})
        if port_dcc_data != {}:
            arduino = port_dcc_data.get("ARDUINO",None)        
            if arduino and arduino.isOpen():
                self.disconnect_Z21(port)
                arduino = None

        timeout_error = False
        read_error =False
        text_string = "ERROR"

        if port!="NO DEVICE" and not arduino:
            try:
                self.ARDUINO_status = "Connecting"
                baudrate = self.getConfigData("baudrate")
                baudrate = 115200
                self.arduino = serial.Serial(port,baudrate=baudrate,timeout=2,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
                logging.debug("connected to: %s Baudrate: %s", self.arduino.portstr,baudrate)                

            except BaseException as e:
                logging.debug(e, exc_info=True) 
                messagebox.showerror("Error connecting to the serial port " + port,
                                     "Serial Interface to ARDUINO could not be opened!\n"
                                     "\n"
                                     "Check if an other program is using the serial port\n"
                                     "This could be the Ardiono IDE/serial monitor or an\n"
                                     "other instance of this program.")
                
                arduino = None
                return False
            
            timeout_error = True
            try:
                text=""
                text = arduino.readline()
                timeout_error = False
                # check if feedback is from MobaLedLib
                text_string = text.decode('utf-8')
                
                if text_string.find(SerialIF_teststring1) == -1:
                    read_error = True
                else:
                    self.queue.put(text_string)
                    logging.info("Connect message: %s", text_string)
            except (IOError,UnicodeDecodeError) as e:
                logging.debug(e)                
                read_error = True
                
            if read_error:         
                messagebox.showerror("Error when reading Arduino answer",
                                     "Wrong answer from ARDUINO:\n"                                  # 02.01.20:  Ausgabe der empfangenen Message. Das Hilft evtl. bei der Fehlersuche
                                     " '" + text_string + "'\n"                                      # 02.01.20:  ToDo: Woher kommt das 'b am Anfang der Meldung? das "\n\r" muss auch nicht angezeigt werden
                                     "\n"
                                     "Check if the correct program is loaded to the arduino.\n"
                                     "It must be compiled with the compiler switch:\n"               # 02.01.20:  Old: "becompiled"
                                     "  #define RECEIVE_LED_COLOR_PER_RS232")
                
                arduino = None
                return False                

            if timeout_error:         # 03.12.19: more detailed error message
                messagebox.showerror("Timeout waiting for the Arduino answer",
                                     "ARDUINO is not answering.\n"
                                     "\n"
                                     "Check if the correct program is loaded to the arduino.\n"
                                     "It must becompiled with the compiler switch:\n"
                                     "  #define RECEIVE_LED_COLOR_PER_RS232")
                
                arduino = None
                return False
            else:
                
                port_dcc_data = self.serial_port_dict.get(port,{})
                if port_dcc_data != {}:
                    port_dcc_data["ARDUINO"] = arduino
                else:
                    self.serial_port_dict[port] ={"dcc_address_range": dcc_adress_range, 
                                                  "ARDUINO" : arduino}
                    logging.info("%s added to list",port)
                    if port == self.getConfigData("serportname"):
                        self.arduino = arduino                
                
                return True
            return False
        else:
            return False

    # ----------------------------------------------------------------
    # LEDColorTest disconnect ARDUINO
    # ----------------------------------------------------------------
    def disconnect_Z21(self,port):
        self.disconnect()
        logging.debug("disconnect Z21 serial port: %s", port)
        arduino = None
        port_dcc_data = self.serial_port_dict.get(port,{})
        if port_dcc_data != {}:
            arduino = port_dcc_data.get("ARDUINO",None)                
            if arduino:
                arduino.close()
                arduino = None
                del self.serial_port_dict[port]
                logging.info("%s deleted from list",port)
        self.stop_process_serial_all()

    # ----------------------------------------------------------------
    # LEDColorTest disconnect ARDUINO
    # ----------------------------------------------------------------
    def disconnect(self):
        logging.debug("disconnect start")
        if self.arduino:
            self.led_off()
            for key in self.tabdict:
                self.tabdict[key].disconnect()
            #message = "#END\n"
            #self.send_to_ARDUINO(message)
            message = "#X\n"
            self.send_to_ARDUINO(message)
            logging.debug("close ARDUINO port %s",self.arduino.portstr)
            time.sleep(10*ARDUINO_WAITTIME)
            self.arduino.close()
            self.arduino = None
            self.ARDUINO_current_portname=""
            self.ARDUINO_status=""
        self.set_connectstatusmessage("Nicht Verbunden",fg="black")
            
    def connect_if_not_connected(self, port=None):
        logging.debug("Connect_if_not_connected")
        if self.arduino:
            if self.arduino.isOpen():
                return True
        return self.connect(port=port)

    def checkconnection(self):
        #logging.debug("Check_connection")
        textmessage = ""
        #self.connection_startup = False
        if self.connection_startup:
            # checks if in the first messages from ARDUINO the string "#Color Test LED" is included
            self.connection_startup_time -= 1 # is called every 100ms
            if self.connection_startup_time == 0:
            
                messagebox.showerror("Error when reading Arduino answer",
                                     "ARDUINO is not answering correctly.\n"
                                    "\n"
                                     "Check if the correct program is loaded to the arduino.\n"
                                     "It must be compiled with the compiler switch:\n"
                                     "  #define RECEIVE_LED_COLOR_PER_RS232")
                self.disconnect()
            else:
                while self.queue.qsize():
                    #print("process_serial: While loop")
                    try:
                        readtext = self.queue.get()
                        date_time = datetime.now()
                        d = date_time.strftime("%H:%M:%S")
                        readtext_str = readtext
                        textmessage = d + "  " + readtext_str
                        if not textmessage.endswith("\n"):
                            textmessage = textmessage +"\n"
                        if SerialIF_teststring2 in textmessage:
                            self.connection_startup = False                           
                            self.set_connectstatusmessage("Verbunden mit "+ self.ARDUINO_current_portname + " - EFFECT Mode",fg="green")
                            dummy,maxLEDcnt_str=readtext_str.split(":")
                            self.ARDUINO_status = "Connected"
                            if maxLEDcnt_str.endswith("\r\n"):
                                maxLEDcnt_str = maxLEDcnt_str[:-2]
                            if str.isdigit(maxLEDcnt_str):
                                maxLEDcnt_int = int(maxLEDcnt_str)
                            else:
                                maxLEDcnt_int = 0
                            if maxLEDcnt_int == 0:
                                paramconfig_dict = self.MacroParamDef.data.get("MaxLEDcnt",{})
                                param_default = paramconfig_dict.get("Default","")
                                maxLEDcnt_int = int(param_default)
                            self.set_maxLEDcnt(maxLEDcnt_int)
                            #self.led_off()                                # 02.01.20:  Disabled because it generates sometimes a "Buffer overrun" on the Arduino
                            #self.led_off()                                #            In addition it doesn't work with out a "#begin"
                            break
                        else:
                            self.set_connectstatusmessage("Verbunden mit "+ self.ARDUINO_current_portname + " - EFFECT Mode",fg="green")
                            self.connection_startup = False
                            self.ARDUINO_status = "Connected"
                            break
                    except BaseException as e:
                        logging.debug(e, exc_info=True) 
                        pass
        return textmessage
    
    def ARDUINO_begin_direct_mode(self):
        if self.arduino and self.arduino.isOpen():
            logging.debug("ARDUINO_Begin_direct_mode")
            if self.mobaledlib_version == 1:
                self.send_to_ARDUINO("#BEGIN\n")
            else:
                self.send_to_ARDUINO("#?\n")
            time.sleep(ARDUINO_WAITTIME)
            self.led_off()
            self.set_connectstatusmessage("Verbunden "+ self.ARDUINO_current_portname + " - DIRECT Mode",fg="green")

    def ARDUINO_end_direct_mode(self):
        if self.arduino and self.arduino.isOpen():
            logging.debug("ARDUINO_End_direct_mode")
            self.set_connectstatusmessage("Verbunden "+ self.ARDUINO_current_portname + " - EFFECT Mode",fg="green")
            if self.mobaledlib_version == 1:
                self.send_to_ARDUINO("#END\n")
            else:
                self.send_to_ARDUINO("#X\n")
        
    def set_connectstatusmessage(self,status_text,fg="black"):
        logging.debug("set_connectstatusmessage: %s",status_text)
        self.connectstatusmessage.configure(text="Status: " + status_text,fg=fg)
        
    def set_statusmessage(self,status_text,fg="black", monitor_message=False):
        logging.debug("set_statusmessage: %s",status_text)
        self.statusmessage.configure(text=status_text,fg=fg)
        if monitor_message:
            self.arduinoMonitorPage.add_text_to_textwindow(status_text)

    def set_ARDUINOmessage(self,status_text,fg="black"):
        logging.debug("set_ARDUINOmessage %s",status_text)
        #self.statusmessage.configure(text=status_text,fg=fg)
        pass

    def send_to_ARDUINO(self, message,arduino=None,comport=None):
        if arduino == None:
            arduino = self.arduino
        if arduino:
            try:
                arduino.write(message.encode())
                logging.debug("Message send to ARDUINO: %s",message)
                time.sleep(2*ARDUINO_WAITTIME)
                self.queue.put( ">> " + str(message))
            except BaseException as e:
                logging.debug("Error write message to ARDUINO %s",message)
                logging.debug(e, exc_info=True) 
    
    def set_maxLEDcnt(self,maxLEDcnt):
        self.maxLEDcnt = maxLEDcnt
        self.setConfigData("maxLEDcount",maxLEDcnt)
        self.set_macroparam_val("ConfigurationPage","MaxLEDcnt",maxLEDcnt)
        
        
    def get_maxLEDcnt(self):
        if self.maxLEDcnt:            
            return self.maxLEDcnt
        else:
            return self.getConfigData("maxLEDcount")
        
    def xinit_ledeffecttable(self):
        self.ledeffecttable.init_ledeffecttable()
 
    def xinit_ledeffecttable_entry(self,keystr):
        self.ledeffecttable.init_entry(keystr)
        
    def xledeffecttable_copy_leds(self,start_int,cnt_int,dest_int):
        self.ledeffecttable.copy_leds(start_int,cnt_int,dest_int)

    def xledeffecttable_init_entries(self,start_int,cnt_int):
        self.ledeffecttable.init_entries(start_int,cnt_int)
            
    def xledeffecttable_move_leds(self,start_int,cnt_int,dest_int):
        self.ledeffecttable.move_leds(start_int,cnt_int,dest_int)
        
    def xledeffecttable_insert_leds(self,start_int,cnt_int):
        self.ledeffecttable.insert_leds(start_int,cnt_int)

    def xledeffecttable_remove_leds(self,remove_start_int,cnt_int):
        self.ledeffecttable.remove_leds(remove_start_int,cnt_int)

                
    # ----------------------------------------------------------------
    # getframebyName
    # ----------------------------------------------------------------
    def getFramebyName (self, pagename):
        return self.tabdict.get(pagename,None)
    
    # ----------------------------------------------------------------
    # getStartPageClassName
    # ----------------------------------------------------------------
    def getStartPageClassName (self):
        startpagename = COMMAND_LINE_ARG_DICT.get("startpagename","")
        if not startpagename in self.tabdict.keys():
            startpagename=""
            logging.debug("Commandline argument --startpage %s wrong. Allowed: %s",startpagename,repr(self.tabdict.keys()))
            
        if startpagename == "":
            startpagenumber = self.getConfigData("startpage")
            startpagename = startpageNumber2Name.get(startpagenumber,self.ConfigData.data.get("startpagename","ColorCheckPage"))
        else:
            self.cl_arg_startpagename = startpagename
        return startpagename
    
    # ----------------------------------------------------------------
    # getStartPageClassIndex
    # ----------------------------------------------------------------
    def getStartPageClassIndex (self):
        startpagenumber = self.getConfigData("startpage")
        startpagename = startpageNumber2Name.get(startpagenumber,self.ConfigData.data.get("startpagename","ColorCheckPage"))
        startpageindex = tabClassName2Index.get(startpagename,"1")
        return startpageindex
    # ----------------------------------------------------------------
    # getTabNameList
    # ----------------------------------------------------------------
    def getTabNameList (self):

        return list(tabClassName2Name.values())
    
    # ----------------------------------------------------------------
    # getStartPageName
    # ----------------------------------------------------------------
    def getStartPageName(self, combolist_index):
        return tabIndex2ClassName.get(str(combolist_index),defaultStartPage)

    def call_helppage(self,event=None):
        #filedir = os.path.dirname(os.path.realpath(__file__))
        #helpfilename = filedir + "//" + HELPPAGE_FILENAME
        macrodata = self.MacroDef.data.get("HelpPage",{})
        helppageurl = macrodata.get("HelpPageURL",)
        webbrowser.open_new_tab(helppageurl)

    def getConfigData(self, key):
        newkey = CONFIG2PARAMKEYS.get(key,key) # translate configdata key into paramdata key
        return self.ParamData.data.get(newkey,self.ConfigData.data.get(key,DEFAULT_CONFIG.get(key,""))) # return Paramdata for the key if available else ConfigData
    
    def getConfigData_multiple(self, configdatakey,paramkey,index):
        value = ""
        index_str = str(index)
        paramkey_dict = self.ConfigData.data.get(paramkey,{})
        if paramkey_dict != {}:
            configdatakey_dict = paramkey_dict.get(index_str,{})
            if configdatakey_dict != {}:
                value = configdatakey_dict.get(configdatakey,"")
        return value

    def correct_led_correction_values(self):
        
        self.cor_red = self.getConfigData("led_correction_r")
        self.cor_green = self.getConfigData("led_correction_g")
        self.cor_blue = self.getConfigData("led_correction_b")
        
        if self.cor_red == 150 and self.cor_green == 119 and self.cor_blue==144:
            # wrong init values from Excel file
            new_led_cor_values_dict = {"led_correction_r": COLORCOR_MAX,
                                       "led_correction_g": int(69*COLORCOR_MAX/100),
                                       "led_correction_b": int(94*COLORCOR_MAX/100)
                                       }

            
            self.ConfigData.data.update(new_led_cor_values_dict)
            self.cor_red = self.getConfigData("led_correction_r")
            self.cor_green = self.getConfigData("led_correction_g")
            self.cor_blue = self.getConfigData("led_correction_b")
            
            
    def readConfigData(self):
        logging.debug("readConfigData")
        filedir = self.mainfile_dir # os.path.dirname(os.path.realpath(__file__))
        
        self.ParamData = ConfigFile(DEFAULT_PARAM, PARAM_FILENAME,filedir=filedir)
        logging.debug("Read Paramdata: %s",repr(self.ParamData.data))
                
        parent_filedir = os.path.dirname(filedir) # get the parent dirname
        # configfile in parent dir
        #self.ConfigData = ConfigFile(DEFAULT_CONFIG, CONFIG_FILENAME,filedir=parent_filedir)
        self.ConfigData = ConfigFile(DEFAULT_CONFIG, CONFIG_FILENAME,filedir=filedir)
        self.ConfigData.data.update(COMMAND_LINE_ARG_DICT) # overwrite configdata mit commandline args
        
        self.correct_led_correction_values()
        
        logging.debug("ReadConfig: %s %s\n\r%s",CONFIG_FILENAME,filedir,repr(self.ConfigData.data))
        
        macrodef_filename_str = MACRODEF_FILENAME
        macroparamdef_filename_str = MACROPARAMDEF_FILENAME
       
        if hasattr(sys, '_MEIPASS'):
            logging.debug('running in a PyInstaller bundle')
        
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
                logging.debug("PyInstaller: sys._MEIPASS: %s",base_path)
                
                filedir = base_path
                
                # PyInstaller installation - macrodef and macroparamdef need to be copied
                
                srcfile = os.path.join(base_path,MACRODEF_FILENAME)
                destfile =  os.path.join(filedir,MACRODEF_FILENAME)
                
                macrodef_filename_str = srcfile
                #shutil.copy2(srcfile,destfile)
                #logging.debug("Copy %s to %s",srcfile,destfile)
                
                srcfile = os.path.join(base_path,MACROPARAMDEF_FILENAME)
                destfile =  os.path.join(filedir,MACROPARAMDEF_FILENAME)
                
                macroparamdef_filename_str = srcfile
                #shutil.copy2(srcfile,destfile)            
                #logging.debug("Copy %s to %s",srcfile,destfile)
                
            except BaseException as e:
                logging.debug("PyInstaller handling Error")
                logging.debug(e, exc_info=True) 
        
        else:
            logging.debug('running in a normal Python process')        
        
        try:
            self.MacroDef = ConfigFile({},MACRODEF_FILENAME,filedir=filedir)
            #logging.info(self.MacroDef.data)
            self.MacroParamDef = ConfigFile({},MACROPARAMDEF_FILENAME,filedir=filedir)
            logging.debug("ReadConfig: %s",repr(self.ConfigData.data))
            #logging.info(self.MacroParamDef.data)
        except BaseException as e:
            logging.debug("PyInstaller handling Error")
            logging.debug(e, exc_info=True) 
        
    def setConfigData(self,key, value):
        if key=="serportname":
            print("setconfigdata:", key,value)
        self.ConfigData.data[key] = value
        
    def setConfigDataDict(self,param_dict):
        self.ConfigData.data.update(param_dict)  
    
    def setParamData(self,key, value):
        if self.ParamData.data:
            self.ParamData.data[key] = value

    def SaveConfigData(self):
        logging.debug("SaveConfigData")
        self.ConfigData.save()
        
    def SaveParamData(self):
        logging.debug("SaveParamData")
        if self.ParamData.data:
            self.ParamData.save()
        
    def led_off(self,_event=None):
    # switch off all LED
        if self.mobaledlib_version == 1:
            message = "#L00 00 00 00 FF\n"
        else:
            message = "#L 00 00 00 00 7FFF\n"
        self.send_to_ARDUINO(message)
        pass
        
    def onCheckDisconnectFile(self):
        # checks every 1 Second if the file DISCONNECT_FILENAME is found.
        # if yes: then disconnect ARDUINO - is used by external program to request a disconnect of the ARDUINO
        #logging.info("onCheckDisconnectFile running")
        if os.path.isfile(DISCONNECT_FILENAME):
            self.led_off()
            message = "#X\n"
            self.send_to_ARDUINO(message)            
            self.disconnect()

            # delete the file to avoid a series of disconnects
            try:
                os.remove(DISCONNECT_FILENAME)
            except BaseException as e:
                logging.debug("ERROR: onCheckDisconnectFile")
                logging.debug(e, exc_info=True) 

        if os.path.isfile(CLOSE_FILENAME):
            self.led_off()
            self.disconnect()
            self.cancel()

            # delete the file to avoid a series of disconnects
            try:
                os.remove(CLOSE_FILENAME)
            except BaseException as e:
                logging.debug("ERROR: onCheckDisconnectFile2")
                logging.debug(e, exc_info=True) 
        
        if self.continueCheckDisconnectFile:
            self.after(1000, self.onCheckDisconnectFile)


    def ToolTip(self, widget,text="", key="",button_1=False):
        if text:
            tooltiptext = text
        else:
            tooltiptext = _T(TOOLTIPLIST.get(key,key))
        tooltip_var = None
        try:
            tooltip_var = widget.tooltip
        except:
            tooltip_var = None
            
        if tooltip_var==None:
            tooltip_var=Tooltip(widget, text=tooltiptext,button_1=button_1)
            widget.tooltip = tooltip_var
        else:
            tooltip_var.unschedule()
            tooltip_var.hide()
            tooltip_var.update_text(text)            
        return

    def addtoclipboard(self,text):
        self.root.clipboard_clear()
        # text to clipboard
        self.root.clipboard_append(text)
        
    def readfromclipboard(self):
        
        return self.root.clipboard_get()        

    def setroot(self, app):
        self.root=app
        
        
    def set_macroparam_var(self, macro, paramkey,variable,persistent=False):
        paramdict = self.macroparams_var.get(macro,{})
        if paramdict == {}:
            self.macroparams_var[macro] = {}
            self.macroparams_var[macro][paramkey] = variable
        else:
            paramdict[paramkey] = variable
        if persistent:
            if self.persistent_param_dict.get(macro,[]) !=[]:
                self.persistent_param_dict[macro] += [paramkey]
            else:
                self.persistent_param_dict[macro] = [paramkey]
            
    def get_macroparam_val(self, macro, paramkey):
        value = ""
        variable = self.macroparams_var[macro][paramkey]
        try:
            var_class = variable.winfo_class()
            if var_class == "TCombobox":
                # value of combobox needs to be translated into a generic value
                current_index = variable.current()
                if current_index == -1: # entry not in list
                    value = variable.get()
                else:
                    if variable.keyvalues !=[]:
                        value_list = variable.keyvalues
                        value = value_list[current_index]
                    else:
                        value=variable.get()
            elif var_class == "Text":
                value = variable.get("1.0",tk.END)            
            else:
                value = variable.get()
        except:
            value = variable.get()
        return value     
            

    def get_macroparam_var_value(self, var,valuedict):
        
        paramconfig_dict = self.MacroParamDef.data.get(var.key,{})
        param_type = paramconfig_dict.get("Type","")
        
        if param_type == "":
            value = var.get()
            param_configname = paramconfig_dict.get("ConfigName",var.key)
            valuedict[param_configname] = value                                        
        elif param_type == "Combo":
            current_index = var.current()
            #if current_index == -1: # entry not in list
            value = var.get()
            #else:
            #    value_list = var.keyvalues
            #    value = value_list[current_index]
            param_configname_list = paramconfig_dict.get("ConfigName",[var.key])
    
            if param_configname_list[0] != "":
                valuedict[param_configname_list[0]] = value
            if param_configname_list[1] != "":
                valuedict[param_configname_list[1]] = current_index
        elif param_type in ["Entry","BigEntry"]:
            value = var.get()
            param_configname = paramconfig_dict.get("ConfigName",var.key)
            valuedict[param_configname] = value
        elif param_type in ["Checkbutton"]:
            param_configname = paramconfig_dict.get("ConfigName",var.key)
            try:
                value = var.get()
                if value==0:
                    valuedict[param_configname] = False
                else:
                    valuedict[param_configname] = True
            except:
                valuedict[param_configname] = False
        return

            
    def get_macroparam_var_values(self, macro):
        valuedictmain = {}
        
        for macrokey in self.macroparams_var:
            valuedict = valuedictmain
            macro_components = macrokey.split(".")
            if macro_components[0] == macro:
                paramdict = self.macroparams_var.get(macrokey,{})
                if len(macro_components) > 1:
                    logging.info(macro_components)
                    valuedict2 = valuedict.get(macro_components[1],None)
                    if valuedict2 == None:
                        valuedict[macro_components[1]]={}
                        valuedict2 = valuedict.get(macro_components[1],None)
                    valuedict3 = valuedict2.get(macro_components[2],None)
                    if valuedict3 == None:
                        valuedict2[macro_components[2]]={}
                        valuedict3 = valuedict2.get(macro_components[2],None)
                    valuedict = valuedict3
                    
                if paramdict != {}:
                    for paramkey in paramdict:
                        var = paramdict.get(paramkey,None)
                        if var != None:
                            self.get_macroparam_var_value(var,valuedict)
        valuedict = valuedictmain
        return valuedict
     
     
    def set_macroparam_val(self, macro, paramkey, value, disable = False):
        if value != None:
            
            macroparams_dict = self.macroparams_var.get(macro,{})
                    
            variable = macroparams_dict.get(paramkey,None)
            if variable:
                if disable:
                    variable.config(state="normal")
                try:
                    var_class = variable.winfo_class()
                except: #limit_var has no winfo_class() function
                    var_class = "Limit_Var"                
    
                if var_class == "TCombobox":
                    # value of combobox needs to be translated into a generic value
                    if isinstance(value,int):
                        current_index = value
                    #else:
                    #    if value !="":
                    #        current_index = variable.keyvalues.index(value)
                    #    else:
                    #        current_index=0
                        value = variable.textvalues[current_index]
                    variable.set(value)
                elif var_class in ["Entry"]:
                    variable.delete(0,tk.END)
                    variable.insert(0,value)
                elif var_class in ["Text"]:
                    variable.delete(0.0,tk.END)
                    variable.insert(0.0,value)                          
                else:          
                    variable.set(value)
                if disable:
                    variable.config(state="disabled")                    
            else:
                pass
            
        return
    
    def set_all_macroparam_val(self, macro, paramvalues):
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
        paramvalues={}
        try:
            for paramkey in self.macroparams_var[macro]:
                value = self.get_macroparam_val(macro,paramkey)
                paramvalues[paramkey] = value
            for paramkey in self.macroparams_var["Group"]:
                value = self.get_macroparam_val("Group",paramkey)
                paramvalues[paramkey] = value            
        except:
            paramvalues = {}
        return paramvalues
    
    def update_color_palette(self,palette):
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
    
    def getConfigDatakey(self,paramkey):
        
        ConfigDatakey = paramkey
        paramconfig_dict = self.MacroParamDef.data.get(paramkey,{})
        param_type = paramconfig_dict.get("Type","")
        
        ConfigDatakey=[]
        
        if param_type == "Combo":
            ConfigDatakeyList = paramconfig_dict.get("ConfigName",[paramkey,paramkey])
            ConfigDatakey = ConfigDatakeyList[1]
            if ConfigDatakey == "":
                ConfigDatakey = ConfigDatakeyList[0]
        else:
            ConfigDatakey = paramconfig_dict.get("ConfigName",paramkey)
        return ConfigDatakey
    
    def update_combobox_valuelist(self,macro,paramkey,valuelist,value=""):
        
        combobox_var = self.macroparams_var[macro][paramkey]
        
        combobox_var ["value"] = valuelist
        if value != "":
            combobox_var.set(value)
            
    def checkcolor(self,_event=None):
        self.showFramebyName("ColorCheckPage")    
    
    def create_macroparam_content(self,parent_frame, macro, macroparams,extratitleline=False,maxcolumns=5, startrow=0, minrow=4, style="MACROPage",generic_methods={},hidecondition=False):
        
        if style =="MACROPage":
        
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
            
        elif style == "CONFIGPage":
            MACROLABELWIDTH = 15*2
            MACRODESCWIDTH = 20*2
            MACRODESCWRAPL = 120*2
            
            PARAMFRAMEWIDTH = 105
            
            PARAMLABELWIDTH = 15
            PARAMLABELWRAPL = 100       
            
            PARAMSPINBOXWIDTH = 6
            PARAMENTRWIDTH = 16
            PARAMCOMBOWIDTH = 16
         
            STICKY = "w"
            ANCHOR = "e"
            
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
            if not paramkey.startswith("!"):
                paramconfig_dict = self.MacroParamDef.data.get(paramkey,{})
                param_min = paramconfig_dict.get("Min",0)
                param_max = paramconfig_dict.get("Max",255)
                param_title = paramconfig_dict.get("Input Text","")
                param_tooltip = paramconfig_dict.get("Hint","")
                param_persistent = (paramconfig_dict.get("Persistent","False") == "True")
                param_configname = paramconfig_dict.get("ConfigName",paramkey)
                param_default = paramconfig_dict.get("Default","")
                param_allow_value_entry = (paramconfig_dict.get("AllowValueEntry","False") == "True")
                param_hide_str = paramconfig_dict.get("Hide","False")
                param_hide = param_hide_str == "True"
                if param_hide_str == "Cond":
                    param_hide = hidecondition
                param_value_change_event = (paramconfig_dict.get("ValueChangeEvent","False") == "True")
                param_value_scrollable = (paramconfig_dict.get("Scrollable","False") == "True")
                param_label_width = int(paramconfig_dict.get("ParamLabelWidth",PARAMLABELWIDTH))
                param_entry_width = int(paramconfig_dict.get("ParamEntryWidth",PARAMENTRWIDTH))
                param_description = paramconfig_dict.get("ParamDescription","")
                
                if param_persistent:
                    configData = self.getConfigData(paramkey)
                    if configData != "":
                        param_default = configData
                param_readonly = (paramconfig_dict.get("ReadOnly","False") == "True")
                param_type = paramconfig_dict.get("Type","")
        
                if param_title == "":
                    param_title = paramkey
                    
                if param_description != "":
                    paramdescriptionlabel = tk.Text(parent_frame, wrap='word', bg=self.cget('bg'), height=0, font=self.fontlabel)
                    paramdescriptionlabel.delete("1.0", "end")
                    paramdescriptionlabel.insert("end", param_description)
                    paramdescriptionlabel.yview("1.0")
                    paramdescriptionlabel.config(state = tk.DISABLED)
                    paramdescriptionlabel.grid(row=row+valuerow, column=column+titlecolumn, columnspan=2, padx=10, pady=10,sticky="ew")
                    column = column + deltacolumn
                    if column > maxcolumns:
                        column = 0
                        row=row+deltarow                    
                    
                    
                if param_type == "": # number value param
                    
                    label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
                    label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                    self.ToolTip(label, text=param_tooltip)
                    if param_max == "":
                        param_max = 255
                    paramvar = LimitVar(param_min, param_max, parent_frame)
                    paramvar.set(param_default)
                    paramvar.key = paramkey
                    
                    if param_value_change_event:
                        s_paramvar = Spinbox(parent_frame, from_=param_min, to=param_max, width=PARAMSPINBOXWIDTH, name='spinbox', textvariable=paramvar,font=self.fontspinbox,command=lambda:self._update_value(macro,paramkey))
                    else:
                        s_paramvar = Spinbox(parent_frame, from_=param_min, to=param_max, width=PARAMSPINBOXWIDTH, name='spinbox', textvariable=paramvar,font=self.fontspinbox)

                    s_paramvar.delete(0, 'end')
                    s_paramvar.insert(0, param_default)
                    s_paramvar.grid(row=row+valuerow, column=column+valuecolumn, padx=2, pady=2, sticky=STICKY)
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
                
                    self.set_macroparam_var(macro, paramkey, paramvar,persistent=param_persistent)
                    
                    column = column + deltacolumn
                    if column > maxcolumns:
                        column = 0
                        row=row+deltarow                    
                    
                elif param_type == "Time": # Time value param
                    
                    label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
                    label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                    self.ToolTip(label, text=param_tooltip)
                    
                    
                    paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH,font=self.fontentry)
                    paramvar.delete(0, 'end')
                    paramvar.insert(0, param_default)
                    paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                    paramvar.key = paramkey
                
                    self.set_macroparam_var(macro, paramkey, paramvar)                
        
                    column = column + deltacolumn
                    if column > maxcolumns:
                        column = 0
                        row=row+deltarow      
                        
                elif param_type == "String": # String value param
                    
                    label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
                    label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                    self.ToolTip(label, text=param_tooltip)
                    
                    
                    paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH,font=self.fontentry)
                         
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
                
                elif param_type == "BigEntry": # Text value param
                    
                    label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,font=self.fontlabel)
                    label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                    self.ToolTip(label, text=param_tooltip)
                    paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH*3,font=self.fontentry)
                    
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
                
                elif param_type == "Text": # Text value param
                    if not param_hide:
                        label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
                        label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                        self.ToolTip(label, text=param_tooltip)
                    
                    number_of_lines = paramconfig_dict.get("Lines","")
                    if number_of_lines == "":
                        number_of_lines = "2"
                        
                    if param_value_scrollable:
                        paramvar = tk.scrolledtext.ScrolledText(parent_frame,bg=self.cget('bg'),width=PARAMENTRWIDTH*5,height=int(number_of_lines),font=self.fonttext)
                    else:
                        paramvar = tk.Text(parent_frame,width=PARAMENTRWIDTH*5,bg=self.cget('bg'),height=int(number_of_lines),font=self.fonttext)
                    
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
                        
                elif param_type == "Checkbutton": # Checkbutton param
                    paramvar = tk.IntVar(value=0)
                    paramvar.key = paramkey
                    if param_default!="":
                        paramvar.set(1)
                    else:                        
                        paramvar.set(0)
                    label=tk.Checkbutton(parent_frame, text=param_title,width=PARAMLABELWIDTH*2,wraplength = PARAMLABELWRAPL*2,anchor="w",variable=paramvar,font=self.fontlabel,onvalue = 1, offvalue = 0)
                    label.grid(row=row+valuerow, column=column, columnspan=2,sticky=STICKY, padx=2, pady=2)
                    self.ToolTip(label, text=param_tooltip)
                                    
                    self.set_macroparam_var(macro, paramkey, paramvar)                
        
                    column = column + deltacolumn
                    if column > maxcolumns:
                        column = 0
                        row=row+deltarow
        
                    
                elif param_type == "Combo": # Combolist param
                    
                    if not param_hide:
                        label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
                        label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                        self.ToolTip(label, text=param_tooltip)
                    
                    if param_allow_value_entry:
                        paramvar = ttk.Combobox(parent_frame, width=PARAMCOMBOWIDTH,font=self.fontlabel)
                    else:                
                        paramvar = ttk.Combobox(parent_frame, state="readonly", width=PARAMCOMBOWIDTH,font=self.fontlabel)
                    combo_value_list = paramconfig_dict.get("KeyValues",paramconfig_dict.get("Values",[]))
                    combo_text_list = paramconfig_dict.get("ValuesText",[])
                    
                    if combo_text_list == []:
                        paramvar["value"] = combo_value_list
                    else:
                        paramvar["value"] = combo_text_list
                        
                    paramvar.current(0) #set the selected view                    
                    
                    if not param_hide:
                        paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                    paramvar.key = paramkey
                    paramvar.keyvalues = combo_value_list
                    paramvar.textvalues = combo_text_list
                
                    self.set_macroparam_var(macro, paramkey, paramvar)               
        
                    column = column + deltacolumn
                    if column > maxcolumns:
                        column = 0
                        row=row+deltarow      
                        
                elif param_type == "GroupCombo": # Combolist param
                    
                    label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
                    label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                    self.ToolTip(label, text=param_tooltip)
                    
                    paramvar = ttk.Combobox(parent_frame, width=PARAMCOMBOWIDTH,postcommand=self.update_GroupComboValues,font=self.fontlabel)
                    combo_value_list = list(self.ledeffecttable.mledgrouptable.keys())
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
                        
                elif param_type == "CX": # Channel value param
                    
                    label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
                    label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                    self.ToolTip(label, text=param_tooltip)
                    
                    paramvar = ttk.Combobox(parent_frame, width=PARAMCOMBOWIDTH,font=self.fontlabel)
                    
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
                
        
                elif param_type == "Multipleparams": # Multiple params
                    logging.info ("%s - %s",macro,param_type)
                    if row >1 or column>0: 
                        row += deltarow
                        column = 0
                    
                    label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
                    label.grid(row=row+titlerow, column=column+titlecolumn, rowspan=2, sticky=STICKY, padx=2, pady=2)
                    self.ToolTip(label, text=param_tooltip)
                    
                    repeat_number = paramconfig_dict.get("Repeat","")
                    
                    if repeat_number == "":
                    
                        multipleparam_frame = ttk.Frame(parent_frame)
                        multipleparam_frame.grid(row=row,column=column+1 ,columnspan=6,sticky='nesw', padx=0, pady=0)
                        
                        multipleparams = paramconfig_dict.get("MultipleParams",[])
                        
                        if multipleparams != []:
                            if style != "CONFIGPage":
                                self.create_macroparam_content(multipleparam_frame,macro, multipleparams,extratitleline=extratitleline,maxcolumns=maxcolumns-1,minrow=0,style=style,generic_methods=generic_methods)
                                separator = ttk.Separator (parent_frame, orient = tk.HORIZONTAL)
                                separator.grid (row = row+2, column = 0, columnspan= 10, padx=2, pady=2, sticky = "ew")
                            else:
                                self.create_macroparam_content(multipleparam_frame,macro, multipleparams,extratitleline=extratitleline,maxcolumns=6,minrow=0,style=style,generic_methods=generic_methods)
                                
               
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
                                self.create_macroparam_content(multipleparam_frame,repeat_macro, multipleparams,extratitleline=extratitleline,maxcolumns=repeat_max_columns,minrow=0,style=style,generic_methods=generic_methods)
                   
                            column = 0
                            row=row+1
                    
                elif param_type == "Color": # Color value param
                    
                    self.colorlabel = tk.Button(parent_frame, text=param_title, width=PARAMLABELWIDTH, height=2, wraplength=PARAMLABELWRAPL,relief="raised", background=param_default,borderwidth=1,command=self.choosecolor,font=self.fontbutton)
                    #label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,bg=param_default,borderwidth=1)
                    self.colorlabel.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                    self.ToolTip(self.colorlabel, text=param_tooltip)
                    
                    paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH,font=self.fontentry)
                    paramvar.delete(0, 'end')
                    paramvar.insert(0, param_default)
                    paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                    paramvar.key = paramkey
                
                    self.set_macroparam_var(macro, paramkey, paramvar)                
        
                    column = column + deltacolumn
                    if column > maxcolumns:
                        column = 0
                        row=row+deltarow
                        
                elif param_type == "ChooseFileName": # parameter AskFileName
                    
                    self.filechooserlabel = tk.Button(parent_frame, text=param_title, width=param_label_width, height=2, padx=2, pady=2, wraplength=PARAMLABELWRAPL,font=self.fontbutton,command=lambda macrokey=macro,paramkey=paramkey: self.choosefilename(macrokey=macrokey,paramkey=paramkey))
                    #label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,bg=param_default,borderwidth=1)
                    self.filechooserlabel.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=10, pady=10)
                    self.ToolTip(self.filechooserlabel, text=param_tooltip)
                    
                    paramvar_strvar = tk.StringVar()
                    paramvar_strvar.set("")
                    paramvar = tk.Entry(parent_frame,width=param_entry_width,font=self.fontentry,textvariable=paramvar_strvar)
                    paramvar.delete(0, 'end')
                    paramvar.insert(0, param_default)
                    paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                    paramvar_strvar.key = paramkey
                    paramvar_strvar.filetypes = paramconfig_dict.get("FileTypes","*")
                    paramvar_strvar.text = param_title
                
                    self.set_macroparam_var(macro, paramkey, paramvar_strvar)                
        
                    column = column + deltacolumn
                    if column > maxcolumns:
                        column = 0
                        row=row+deltarow                
                        
                elif param_type == "Button": # Text value param
                    if not param_hide:
                        number_of_lines = paramconfig_dict.get("Lines","")
                        if number_of_lines == "":
                            number_of_lines = "2"
                        button_function = paramconfig_dict.get("Function","")
                            
                        button=tk.Button(parent_frame, text=param_title,width=param_label_width,height=number_of_lines,wraplength = param_label_width*6,font=self.fontbutton,command=lambda macrokey=macro,button=button_function: self._button_cmd(macrokey=macrokey,button=button))
                        button.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                        self.ToolTip(button, text=param_tooltip)
                        #self.buttonlist.append(self.button)
                        
                        column = column + deltacolumn
                        if column > maxcolumns:
                            column = 0
                            row=row+deltarow
                        
                elif param_type == "ColTab": # Color value param
                    
                    self.coltablabel = tk.Button(parent_frame, text=param_title, width=param_label_width, height=2, wraplength=PARAMLABELWRAPL,relief="raised", borderwidth=1,command=self.checkcolor,font=self.fontbutton)
                    #label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,bg=param_default,borderwidth=1)
                    self.coltablabel.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                    self.ToolTip(self.coltablabel, text=param_tooltip)
                    
                    #paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH)
                    #paramvar.delete(0, 'end')
                    #paramvar.insert(0, param_default)
                    #paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
                    #paramvar.key = paramkey
                
                    #self.set_macroparam_var(macro, paramkey, paramvar)
                    
                    self.create_color_palette(parent_frame)
    
                    column = 0
                    row=row + 4
                        
                elif param_type == "Var": # Combolist param
                    
                    label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,font=self.fontlabel)
                    label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                    self.ToolTip(label, text=param_tooltip)
                    
                    if param_allow_value_entry:
                        paramvar = ttk.Combobox(parent_frame, width=PARAMCOMBOWIDTH,font=self.fontlabel)
                    else:                
                        paramvar = ttk.Combobox(parent_frame, state="readonly", width=PARAMCOMBOWIDTH,font=self.fontlabel)                
                    
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
                elif param_type == "Generic": # call generic function
                    logging.info ("%s - %s",macro,param_type)
                                        
                    generic_widget_frame = ttk.Frame(parent_frame)
                    generic_widget_frame.grid(row=row,column=column ,columnspan=6,sticky='nesw', padx=0, pady=0)
                    
                    generic_method_name = paramconfig_dict.get("GenericMethod","")
                    
                    if generic_method_name != "" and generic_methods != {}:
                        generic_methods[generic_method_name](generic_widget_frame,macro,macroparams)
                    else:
                        raise Exception("Method %s not implemented" % generic_method_name)
                    
                    column = 0
                    row=row+deltarow                    
                        
                    
                
                if param_readonly:
                    paramvar.state = "DISABLED"            
            
            #if (column<maxcolumns+1) and (column>0):
            #    for i in range(column,maxcolumns+1):
            #        label=tk.Label(parent_frame, text=" ",width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
            #        label.grid(row=row,column=i,sticky=STICKY, padx=2, pady=2)
            
            if maxcolumns > 6:        
                seplabel=tk.Label(parent_frame, text="",width=90,height=1)
                seplabel.grid(row=row+2, column=0, columnspan=10,sticky='ew', padx=2, pady=2)
    
    
    def create_macroparam_frame(self,parent_frame, macro, extratitleline=False,maxcolumns=5, startrow=0, minrow=4,style="MACROPage",generic_methods={},hidecondition=False):
        
        MACROLABELWIDTH = 15
        MACRODESCWIDTH = 20
        MACRODESCWRAPL = 120
        BUTTONLABELWIDTH = 10
        
        PARAMFRAMEWIDTH = 105
        
        PARAMLABELWIDTH = 15
        PARAMLABELWRAPL = 100        
        
        PARAMSPINBOXWIDTH = 4
        PARAMENTRWIDTH = 8
        PARAMCOMBOWIDTH = 16
        
        macroparam_frame = ttk.Frame(parent_frame, relief="ridge", borderwidth=1)
        self.macroparam_frame_dict[macro] = macroparam_frame
    
        macrodata = self.MacroDef.data.get(macro,{})
        Macrotitle = macro
        
        Macrolongdescription = macrodata.get("Ausführliche Beschreibung","")
        Macrodescription = macrodata.get("Kurzbeschreibung","")
        
        if Macrolongdescription =="":
            Macrolongdescription = Macrodescription
        macroldlabel = tk.Text(macroparam_frame, wrap='word', bg=self.cget('bg'), borderwidth=2,relief="ridge",width=108,height=5,font=self.fontlabel)
        
        macroldlabel.delete("1.0", "end")
        macroldlabel.insert("end", Macrolongdescription)
        macroldlabel.yview("1.0")
        macroldlabel.config(state = tk.DISABLED)
        
        if style == "MACROPage":
            macroldlabel.grid(row=4, column=0, columnspan=2,padx=0, pady=0,sticky="w")
            macrolabel = tk.Button(macroparam_frame, text=Macrotitle, width=MACROLABELWIDTH, height=2, wraplength=150,relief="raised", background="white",borderwidth=1,command=lambda: self._macro_cmd(macrokey=macro))
            macrolabel.grid(row=1, column=0, sticky="nw", padx=4, pady=4)
            macrolabel.key=macro
            self.ToolTip(macrolabel, text=Macrodescription)
        else:
            macroldlabel.grid(row=0, column=0, columnspan=2,padx=10, pady=10,sticky="we",)
       
        macrotype = macrodata.get("Typ","")
        if macrotype =="ColTab":
            macroparams = []
        else:       
            macroparams = macrodata.get("Params",[])
        
        if macroparams:
            param_frame = ttk.Frame(macroparam_frame) #,borderwidth=1,relief="ridge")
                                  
            self.create_macroparam_content(param_frame,macro, macroparams,extratitleline=extratitleline,maxcolumns=maxcolumns,startrow=startrow,style=style,generic_methods=generic_methods,hidecondition=hidecondition)
    
            param_frame.grid(row=1,column=1,rowspan=2,padx=0, pady=0,sticky="nw")
    
        return macroparam_frame
    
    def get_macrodef_data(self, macro, param):
        macrodata = self.MacroDef.data.get(macro,{})
        if macrodata != {}:
            value = macrodata.get(param,"")
        else:
            value = ""
        return value
        
    
    def determine_filepath(self,filename_key):
        #macrodata = self.MacroDef.data.get("StartPage",{})
        #filename = macrodata.get(filename_key,"")
        filename = self.get_macrodef_data("StartPage",filename_key)
        filedir = self.mainfile_dir
        filepath1 = os.path.join(filedir, filename)
        filepath = os.path.normpath(filepath1)
        return filepath
        
    
    def _button_cmd_old(self, macrokey="",button=""):
        """Respond to user click on a button"""
        logging.debug("Button Pressed: %s - %s",macrokey,button)
        button_command = "self."+button+"()"
        eval(button_command)

    def _button_cmd(self, macrokey="",button=""):
        """Respond to user click on a button"""
        logging.debug("Button Pressed: %s - %s",macrokey,button)
        page_frame = self.getFramebyName(macrokey)
        if page_frame:        
            button_command = "page_frame" + "." +button+"()"
            eval(button_command)
 
        
    def _macro_cmd(self, macrokey=""):
        """Respond to user click on a macro label item in macrolist."""
        
        self.macro = macrokey
        macroparams = self.get_all_macroparam_val(macrokey)
        self.hexa = macroparams.get("Group_Colour","")
        self.group_name_str = self.get_all_group_params()
        self._update_ledtable(self.lednum_int, int(self.ledcount_int),self.hexa,"",macrokey, self.group_name_str, params=macroparams)
        self.update_ledtable_complete()    
    
    def update_GroupComboValues(self):
        
        combo_value_list = list(self.ledeffecttable.mledgrouptable.keys())
        combo_text_list = []
        
        paramvar = self.macroparams_var["Group"]["Group_Name"]
        paramvar["value"] = combo_value_list

        paramvar.keyvalues = combo_value_list
        paramvar.textvalues = combo_text_list
        
    def GroupComboSelected(self,event):
        
        #paramvar = self.macroparams_var["Group"]["Group_Name"]
        paramvar = event.widget
        
        groupname = paramvar.get()
        
        group_dict = self.ledeffecttable.mledgrouptable.get(groupname,{})
        group_param_dict = group_dict.get("params",{})
        if group_param_dict != {}:
            self.set_all_macroparam_val("Group",group_param_dict)
    
    def determine_fg_color(self,hex_str):
        '''
        Input a string without hash sign of RGB hex digits to compute
        complementary contrasting color such as for fonts
        '''
        
        (r, g, b) = (hex_str[1:3], hex_str[3:5], hex_str[5:])
        return '#000000' if 1 - (int(r, 16) * 0.299 + int(g, 16) * 0.587 + int(b, 16) * 0.114) / 255 < 0.5 else '#ffffff'        
   
    
    def setgroupcolor(self,color):
        color_fg = self.determine_fg_color(color)
        self.colorlabel.config(bg=color,fg=color_fg)
        paramvar = self.macroparams_var["Group"]["Group_Colour"]
        paramvar.delete(0, 'end')
        paramvar.insert(0, color)    
    
    def choosecolor(self):
        paramvar = self.macroparams_var["Group"]["Group_Colour"]
        old_color=paramvar.get()        
        color = colorchooser.askcolor(color=old_color)
        
        if color:
            colorhex = color[1]
            self.setgroupcolor(colorhex)    


    def _key_return(self,event=None):
        
        param = event.widget
        self._update_value(param.macro,param.key)
    
        
        #tabframe=self.getFramebyName(macro)
        #if tabframe!=None:
        #    tabframe._update_value(paramkey)


    def _update_value(self,macro,paramkey):
        logging.info("update_value: %s - %s",macro,paramkey)
        tabframe=self.getFramebyName(macro)
        if tabframe!=None:
            tabframe._update_value(paramkey)
            
    def create_color_palette(self, parent_frame):
        
        LABELWIDTH = int(16*SIZEFACTOR)
        
        COLOR_PALLETTE_COLUMNS = 4
        
        # --- palette
        self.colorpalette = self.getConfigData("palette")
        self.colorpalette_labels_dict={}
        palette = self.colorpalette
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
            l.bind("<Button-1>", self.checkcolor)
            self.ToolTip(l, key=key)
            l.bind("<FocusOut>", lambda e: e.widget.configure(relief="raised"))
            #l.pack()
            l.key = key
            l.grid(row=i % COLOR_PALLETTE_COLUMNS, column=i // COLOR_PALLETTE_COLUMNS, padx=2, pady=2)
            
            self.colorpalette_labels_dict[key]=l
            
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
    
    def process_serialx(self):

        #print("process_serial: Start")
        textmessage = self.checkconnection()
        if textmessage:
            #self.text.insert("end", textmessage)
            #self.text.yview("end")
            #self.set_ARDUINOmessage(textmessage)
            pass
        else:
            if self.queue:
                while self.queue.qsize():
                    #print("process_serial: While loop")
                    try:
                        readtext = self.queue.get()
                        date_time = datetime.now()
                        d = date_time.strftime("%H:%M:%S")
                        textmessage = d + "  " + readtext
                        if not textmessage.endswith("\n"):
                            textmessage = textmessage +"\n"
                        #write message into text window
                        #self.text.insert("end", textmessage)
                        #self.text.yview("end")
                        #self.set_ARDUINOmessage(textmessage)
                    except IOError:
                        pass
            
        if self.monitor_serial:
            self.after(100, self.process_serial)

    def start_process_serial_all(self):
        #print("pyMobaLedLib: start_process_serial_all")
        #SerialMonitorPage = self.getFramebyName("SerialMonitorPage")
        #SerialMonitorPage.start_process_serial()
        
        
        if False:
            logging.debug("PyProg-Start_process_serial")
            global ThreadEvent
            ThreadEvent = threading.Event()
            ThreadEvent.set()
            time.sleep(2)
            ThreadEvent.clear()
            self.monitor_serial = True
            SerialMonitorPage = self.getFramebyName("SerialMonitorPage")
            for port in self.serial_port_dict:
                arduino = self.serial_port_dict[port]["ARDUINO"]
                self.thread = SerialThread(self.queue,arduino,p_serialportname=port)
            self.thread.start()
            SerialMonitorPage.process_serial()
            


    def stop_process_serial_all(self):
        logging.debug("Pyprog-Stop_process_serial")
        #print("pyMobaLedLib: stop_process_serial_all")
        SerialMonitorPage = self.getFramebyName("SerialMonitorPage")
        SerialMonitorPage.set_check_RMBUS(value=False)
        global ThreadEvent
        self.monitor_serial = False
        if ThreadEvent:
            ThreadEvent.set()
        #time.sleep(1)
        
        
    def _send_ledcolor_to_ARDUINO(self, lednum, ledcount, ledcolor):
        lednum_int = int(lednum)
        lednum_int += self.LED_baseadress
        if self.mobaledlib_version == 1:
            message="#L"
        else:
            message="#L "
        message = message + '{:02x}'.format(lednum_int) + " " + ledcolor[1:3] + " " + ledcolor[3:5] + " " + ledcolor[5:7] + " " + '{:02x}'.format(ledcount) + "\n"
        self.send_to_ARDUINO(message)
        time.sleep(ARDUINO_WAITTIME)
        
    def led_off(self,_event=None):
    # switch off all LED
        self.ledhighlight = False
        if self.mobaledlib_version == 1:
            message = "#L00 00 00 00 FF\n"
        else:
            message = "#L 00 00 00 00 7FFF\n"
        self.send_to_ARDUINO(message)        
        
    def blinking_on_off(self,lednum,ledcount,seq=False):
    # switch off all LED
        self.LED_flash_sequence=seq
        if self.ledhighlight:
            self.ledhighlight = False
            self.led_off()    
        else:
            self._highlight_led(lednum, ledcount)    
            
    def _highlight_led(self,lednum, ledcount):
        if self.ledhighlight: # onblink is already running, change only lednum and ledcount
            # reset all blinking led with their colors
            #for i in range(self.on_ledcount):
            #    lednum_str = '{:03}'.format(self.on_lednum+i)
            #    self._send_ledcolor_to_ARDUINO(lednum_str,1,self.controller.ledtable.get(lednum_str,"#000000"))
            #    time.sleep(ARDUINO_WAITTIME)
            #set the blinking led to highlight
            self._send_ledcolor_to_ARDUINO(self.on_lednum,self.on_ledcount,"#000000")
            self._send_ledcolor_to_ARDUINO(lednum, ledcount, "#FFFFFF")
            # save current lednum and led count
            self.on_lednum_seq=lednum
            self.on_lednum = lednum
            self.on_ledcount = ledcount
            self.on_ledon = True
        else:
            self.ledhighlight = True
            self.on_lednum_seq=lednum
            self.on_led_doubleflash = True
            self.on_lednum = lednum
            self.on_ledcount = ledcount
            self.on_ledon = True       
            self.onblink_led()

         
    def onblink_led(self):
        if self.ledhighlight:
            lednum=self.on_lednum
            ledcount=self.on_ledcount
            if self.on_ledon:
                if self.LED_flash_sequence and ledcount>1:
                    if self.on_led_doubleflash:
                        self.on_led_doubleflash=False
                    else:
                        self.on_lednum_seq+=1
                    if self.on_lednum_seq>lednum+ledcount-1:
                        self.on_lednum_seq=lednum
                        self.on_led_doubleflash=True
                    lednum = self.on_lednum_seq
                    ledcount=1
                self._send_ledcolor_to_ARDUINO(lednum, ledcount, "#FFFFFF")
                self.on_ledon = False
                self.after(int(500/BLINKFRQ),self.onblink_led)
            else:
                self._send_ledcolor_to_ARDUINO(lednum, ledcount, "#000000")
                self.on_ledon = True
                self.after(int(500/BLINKFRQ),self.onblink_led)
                
    def show_download_status(self, a,b,c):
        '''''Callback function 
        @a:Downloaded data block 
        @b:Block size 
        @c:Size of the remote file 
        '''  
        per=100.0*a*b/c  
        if per>100:  
            per=100  
        #print '%.2f%%' % per          
    
        F00.StatusMsg_UserForm.Set_ActSheet_Label(P01.Format(int(time.time()) - M37.Update_Time, 'hh:mm:ss')+"\n"+str(a*b))

    def Update_pyMobaLedLib(self):
        F00.StatusMsg_UserForm.ShowDialog(M09.Get_Language_Str('Aktualisiere Python MobaLedLib Programm'), '')
        URL= "https://github.com/HaroldLinke/pyMobaLedLib/archive/master.zip"
        try:
            workbookpath = filedir
            workbookpath2 = os.path.dirname(workbookpath)
            workbookpath3 = os.path.dirname(workbookpath2)
            zipfilenamepath = workbookpath3+"/pyMobaLedLib.zip"
            F00.StatusMsg_UserForm.Set_Label("Download Python MobaLedLib Program")
            logging.debug("Update pyMobaLedLib from Github - Lokales Verzeichnis:"+ workbookpath)
            logging.debug("Update pyMobaLedLib from Github -download from Github")
            urllib.request.urlretrieve(URL, zipfilenamepath,self.show_download_status)
            F00.StatusMsg_UserForm.Set_Label("Entpacken Python MobaLedLib Programms")
            logging.debug("Update pyMobaLedLib from Github -unzip file:"+zipfilenamepath+" nach " + workbookpath3)
            M30.UnzipAFile(zipfilenamepath,workbookpath3)
            srcpath = workbookpath3+"/pyMobaLedLib-master/python"
            dstpath = workbookpath #workbookpath3+"/pyMobaLedLib/python"
            if not dstpath.startswith(r"D:\data\doc\GitHub"): # do not copy when destination is development folder
                F00.StatusMsg_UserForm.Set_Label("Kopieren des Python MobaLedLib Programm")
                try:
                    logging.debug("Update pyMobaLedLib from Github -delete folder:"+ workbookpath3+"/LEDs_AutoProg")
                    shutil.rmtree(workbookpath+"/LEDs_AutoProg")
                except BaseException as e:
                    logging.error(e, exc_info=True)
                self.copytree(srcpath,dstpath)
                logging.debug("Update pyMobaLedLib from Github -copy folder:"+ srcpath + " nach " +dstpath)
            if P01.MsgBox(M09.Get_Language_Str(' Python MobaLedLib wurde aktualisiert. Soll neu gestartet werden?'), vbQuestion + vbYesNo, M09.Get_Language_Str('Aktualisieren der Python MobaLedLib')) == vbYes:
                # shutdown and restart
                self.restart()
            
        except BaseException as e:
            logging.error(e, exc_info=True)
            #Debug.Print("Update_MobaLedLib exception:",e)
            P01.MsgBox(M09.Get_Language_Str('Fehler beim Download oder Installieren?'),vbInformation, M09.Get_Language_Str('Aktualisieren der Python MobaLedLib'))
        P01.Unload(F00.StatusMsg_UserForm)
    
    def check_version(self, exec_update=False):
        Version_URL= "https://raw.githubusercontent.com/haroldlinke/pyMobaLedLib/master/python/version.py"
        try:
            response = urllib.request.urlopen(Version_URL)
            version_str = response.read().decode('utf-8')
        except:
            version_str = ""
            
        if version_str != "":
            version_str_split = version_str.split('"')
            version_str = version_str_split[1]
        if not exec_update:
            if version_str != PROG_VERSION:
                answer = tk.messagebox.showinfo ('Neue pyMLL Version','Es gibt eine neue pyMLL Version auf GitHub.\n\nAktuelle Version: '+ PROG_VERSION + "\nNeue Version: "+ version_str + "\n\nBitte die neue Version herunterladen")
        else:
            if version_str != PROG_VERSION:
                answer = tk.messagebox.askyesno ('Neue pyMLL Version','Es gibt eine neue pyMLL Version auf GitHub.\n\nAktuelle Version: '+ PROG_VERSION + "\nNeue Version: "+ version_str + "\n\nSoll die neue Version heruntergeladen werden?")
                if answer == False:
                    return
                else:
                    self.Update_pyMobaLedLib()
            else:
                answer = tk.messagebox.showinfo ('Check pyMLL Version','Es gibt eine keine neue pyMLL Version \n\nAktuelle Version: '+ PROG_VERSION)
        return
     


class SerialThreadx(threading.Thread):
    def __init__(self, p_queue, p_serialport,p_serialportname=""):
        #global serialport
        threading.Thread.__init__(self)
        self.queue = p_queue
        self.serialport = p_serialport
        self.serialport_name = p_serialportname

    def run(self):
        #global serialport
        logging.debug("pyProg-SerialThread started:"+self.serialport_name)
        if self.serialport:

            while not ThreadEvent.is_set() and self.serialport:
                # print("Event:",ThreadEvent.is_set())
                # print("Serialport:", serialport)
                # logging.info("SerialThread while loop")
                #logging.info("SerialThread running")
                try:
                    line = []

                    while True:
                        for c in self.serialport.read():
                            if c.isprintable():
                                line.append(c)
                            else:
                                if c == '\n':
                                    text = line + "\n"
                                    line = []
                                    break
                                else:
                                    line.append("#"+c.hex)
                    
                    #text = self.serialport.readline()
                except:
                    text = ""
                
                if len(text)>0:
                    try:
                        self.queue.put(text.decode('utf-8'))
                    except:
                        pass
                    logging.info("PyProg-SerialThread (%s) got message: %s", self.serialport_name,text)

        logging.debug("PyProg-SerialThread (%s) received event. Exiting", self.serialport_name)


def img_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def check_version(exec_update=False):
    
    Version_URL= "https://raw.githubusercontent.com/haroldlinke/pyMobaLedLib/master/python/version.py"
    try:
        response = urllib.request.urlopen(Version_URL)
        version_str = response.read().decode('utf-8')
    except:
        version_str = ""
        
    if version_str != "":
        version_str_split = version_str.split('"')
        version_str = version_str_split[1]
    if not exec_update:
        if version_str != PROG_VERSION:
            answer = tk.messagebox.showinfo ('Neue pyMLL Version','Es gibt eine neue pyMLL Version auf GitHub.\n\nAktuelle Version: '+ PROG_VERSION + "\nNeue Version: "+ version_str + "\n\nBitte die neue Version herunterladen")
    else:
        if version_str != PROG_VERSION:
            answer = tk.messagebox.askyesno ('Neue pyMLL Version','Es gibt eine neue pyMLL Version auf GitHub.\n\nAktuelle Version: '+ PROG_VERSION + "\nNeue Version: "+ version_str + "\n\nSoll die neue Version heruntergeladen werden?")
            if answer == False:
                return
            else:
                pass
        else:
            answer = tk.messagebox.showinfo ('Check pyMLL Version','Es gibt eine keine neue pyMLL Version \n\nAktuelle Version: '+ PROG_VERSION)
    return
 


#-------------------------------------------

COMMAND_LINE_ARG_DICT = {}

logger=logging.getLogger(__name__)

ScaleFactor = 1

filedir = ""

def main_entry():
    global DEBUG
    global ScaleFactor
    
    global COMMAND_LINE_ARG_DICT
    global filedir
    
    #import wingdbstub
    try:
        import ctypes
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        #print("Scalefactor:", ScaleFactor)
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass
        
    if sys.hexversion < 0x030900F0:
        tk.messagebox.showerror("Wrong Python Version"+sys.version,"You need Python Version > 3.9 to run this Program")
        exit()
    
    COMMAND_LINE_ARG_DICT = {}
    
    parser = argparse.ArgumentParser(description='Generate MLL Programs') #,exit_on_error=False) seems to create a problem in some python versions
    parser.add_argument('--loglevel',choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"],help="Logginglevel to be printed into the logfile")
    parser.add_argument('--logfile',help="Logfilename")
    parser.add_argument('--loaddatafile',choices=["True","False"],help="if <False> the last saved data will no be loaded")
    parser.add_argument('--startpage',choices=['StartPage', 'ColorCheckPage', 'Prog_GeneratorPage', 'SoundCheckPage', 'DCCKeyboardPage', 'ServoTestPage', 'Z21MonitorPage', 'SerialMonitorPage', 'ARDUINOMonitorPage', 'ConfigurationPage'],help="Name of the first page shown after start")
    parser.add_argument('--port',help="Name of the port where the ARDUINO is connected to")
    parser.add_argument('--z21simulator',choices=["True","False"],help="if <True> the Z21simulator will be started automatically")
    parser.add_argument('--caller',choices=["SetColTab",""],help="Only for MLL-ProgrammGenerator: If <SetColTab> only the Colorcheckpage is available and the chnage coltab is returned after closing the program")
    parser.add_argument('--test',choices=["True","False"],help="if <True> test routines are started at start of program")
    parser.add_argument('--vb2py',choices=["True","False"],help="if <True> VB2PYpage is shown - for developers only")
    parser.add_argument('--ARDUINO_IDE',choices=["True", "False"],help="Forces the use of the ARDUINO IDE instead of the Windows batch files")
    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        #print("Argument Error")
        logging.debug ('Catching an argumentError')
    
    logging_format = '%(asctime)s - %(message)s'
    
    filedir = os.path.dirname(os.path.realpath(__file__))
    if args.logfile:
        logfilename1=args.logfile
    else:
        logfilename1=LOG_FILENAME
        
    if logfilename1 == "stdout":
        logfilename=None
    else:
        logfilename = os.path.join(filedir, logfilename1)
    logging_level="DEBUG"
    
    if args.loglevel:
        logging_level = args.loglevel.upper()
        COMMAND_LINE_ARG_DICT["logging_level"]=logging_level
        if logging_level=="DEBUG":
            log_level=logging.DEBUG
            DEBUG=True
        elif logging_level=="INFO":
            log_level=logging.INFO
        elif logging_level=="WARNING":
            log_level=logging.WARNING
        elif logging_level=="ERROR":
            log_level=logging.ERROR
        else:
            log_level=logging.CRITICAL
    else:
        log_level=logging.DEBUG

    logger.setLevel(log_level)
    fh = logging.handlers.RotatingFileHandler(logfilename,maxBytes=1000000,backupCount=3)
    fh.setLevel(log_level)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    logging.basicConfig(format=logging_format, filename=logfilename,filemode="w",level=log_level,datefmt="%H:%M:%S",force=True)

    logger.info("Python Version: %s",sys.version)
    logger.info("MLL Proggenerator started %s", PROG_VERSION)
    logger.info(" Platform: %s",platform.platform())
    logger.info("Parameters; %s", repr(args))
    
    logger.debug("Installationfolder %s",filedir)
    logger.debug("Logging Level: %s Logfilename: %s",logging_level, logfilename)
    
    COMMAND_LINE_ARG_DICT["logfilename"]=logfilename
    if args.startpage:
        COMMAND_LINE_ARG_DICT["startpagename"]=args.startpage
    else:
        COMMAND_LINE_ARG_DICT["startpagename"]="StartPage"
        
    logger.info(" Startpage: %s",COMMAND_LINE_ARG_DICT["startpagename"])        
    if args.port:
        COMMAND_LINE_ARG_DICT["serportname"]=args.port
        
    if args.z21simulator:
        COMMAND_LINE_ARG_DICT["z21simulator"]=args.z21simulator
        
    if args.caller:
        COMMAND_LINE_ARG_DICT["caller"]=args.caller
        if (args.caller == "SetColTab"):
            COMMAND_LINE_ARG_DICT["caller"]= "SetColTab"
            COMMAND_LINE_ARG_DICT["startpagename"]='ColorCheckPage'
            
    if args.loaddatafile:
        COMMAND_LINE_ARG_DICT["loaddatafile"]=args.loaddatafile
    else:
        COMMAND_LINE_ARG_DICT["loaddatafile"]=True
        
    if args.test:
        COMMAND_LINE_ARG_DICT["test"]=args.test
        
    if args.vb2py:
        COMMAND_LINE_ARG_DICT["vb2py"]=args.vb2py
        
    if args.ARDUINO_IDE:
        if args.ARDUINO_IDE == "True":
            COMMAND_LINE_ARG_DICT["useARDUINO_IDE"] = True
        
    # check if colortest only is needed
    try: #check if a COLORTESTONLY_FILE is in the main Dir 
        filedir = os.path.dirname(os.path.realpath(__file__))
        filepath1 = os.path.join(filedir, COLORTESTONLY_FILE)
        open(filepath1, 'r').close()
        colortest_only = True
    except BaseException as e:
        logging.debug(e, exc_info=True) 
        colortest_only = False
        pass
    
    if colortest_only:
        COMMAND_LINE_ARG_DICT["colortest_only"]= "True"
        
    logger.info("Commandline args: %s",repr(COMMAND_LINE_ARG_DICT))
    check_version()
    
    try:
        app = pyMobaLedLibapp()
        tk_version = app.tk.call("info", "patchlevel")
        logging.debug("TK-Version:"+tk_version)
        
        app.setroot(app)
        app.protocol("WM_DELETE_WINDOW", app.cancel)
        app.startup_system()
        app.mainloop()
    
    except BaseException as e:
        logging.error(e, exc_info=True)
        #print(e, exc_info=True)
        pass    
    
    logging.info("Program End")

if __name__ == "__main__":
    main_entry()


