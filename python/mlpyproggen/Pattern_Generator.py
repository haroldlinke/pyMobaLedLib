# -*- coding: utf-8 -*-
#
#         Pattern_Generator
#
# * Version: 4.03
# * Author: Harold Linke
# * Date: January 8, 2022
# * Copyright: Harold Linke 2021
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
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
# * along with this program.  if not, see <http://www.gnu.org/licenses/>.
# *
# *
# ***************************************************************************

#------------------------------------------------------------------------------
# CHANGELOG:
# 2020-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2021-01-07 v4.02 HL: - Else:, ByRef check done - first PoC release
# 2021-01-08 V4.03 HL: - added Workbook Save and Load

import tkinter as tk
from tkinter import ttk,messagebox

from mlpyproggen.DefaultConstants import ARDUINO_WAITTIME,LARGE_FONT, SMALL_FONT, VERY_LARGE_FONT, PROG_VERSION,ARDUINO_LONG_WAITTIME
# fromx mlpyproggen.configfile import ConfigFile
from locale import getdefaultlocale
# fromx tkintertable import TableCanvas, TableModel
# fromx collections import OrderedDict
# fromx ExcelAPI.X02_Workbook import create_workbook
import pattgen.M02_Main as M02
import pattgen.M80_Multiplexer_INI_Handling as M80
import pattgen.M08_Load_Sheet_Data as M08
import pattgen.M03_Analog_Trend as M03
import pattgen.M65_Special_Modules as M65
import pattgen.M16_Add_Del_Columns as M16
from ExcelAPI.P01_Worksheetcalc import Calc_Worksheet
import pattgen.DieseArbeitsmappe as AM
import pattgen.Tabelle9 as T09
import pattgen.D00_Forms as D00
#import pattgen.D00_GlobalProcs as D00GP
import pattgen.M20_Morsecode as M20
import pattgen.M02_Main as M02
import pattgen.Tabelle9 as PAT09
#import ExcelAPI.XLA_Application as XLW

import os
#import serial
#import sys
#import threading
import subprocess
#import queue
#import time
import logging
import platform
# fromx scrolledFrame.ScrolledFrame import VerticalScrolledFrame,HorizontalScrolledFrame,ScrolledFrame
# fromx proggen.M06_Write_Header import Create_HeaderFile
# fromx ExcelAPI.X02_Workbook import global_tablemodel

# fromx datetime import datetime
# fromx mlpyproggen.T01_exceltable import get_globaltabelmodel
#import  proggen.F00_mainbuttons as F00
#import proggen.M20_PageEvents_a_Functions as M20
import ExcelAPI.XLA_Application as X02
#import proggen.D08_Select_COM_Port_Userform as D08


# --- Translation - not used
EN = {}
FR = {"Red": "Rouge", "Green": "Vert", "Blue": "Bleu",
      "Hue": "Teinte", "Saturation": "Saturation", "Value": "Valeur",
      "Cancel": "Annuler", "Color Chooser": "Sélecteur de couleur",
      "Alpha": "Alpha"}
DE = {"Red": "Rot", "Green": "Grün", "Blue": "Blau",
      "Hue": "Farbton", "Saturation": "Sättigung", "Value": "Helligkeit",
      "Cancel": "Beenden", "Color Chooser": "Farbwähler",
      "Alpha": "Alpha", "Configuration": "Einstellungen"}

try:
    TR = DE
    #if getdefaultlocale()[0][:2] == 'fr':
    #    TR = FR
    #else:
    #    if getdefaultlocale()[0][:2] == 'de':
    #        TR = DE
except ValueError or TypeError:
    TR = EN

def _(text):
    """Translate text."""
    return TR.get(text, text)

global_controller = None
dialog_parent = None

def set_global_controller(controller):
    global global_controller
    global_controller=controller
    X02.global_controller = controller

def get_global_controller():
    return global_controller

def get_dialog_parent():
    return dialog_parent

def Del_Col_Button_Click():
    M16.Del_Columns_from_Pattern()
    X02.ActiveSheet.Redraw_table()

def Add_Col_Button_Click():
    M16.Add_Columns_to_Pattern()
    X02.ActiveSheet.Redraw_table()
    
def button_testen_cmd():
    X02.Application.Caller="Test_Leds_M99O01"
    M80.Button_Pressed()
    
def button_aktualisieren_cmd():
    X02.Application.Caller="Update"
    X02.ActiveSheet.EventWSchanged(X02.Cells(5,5))
    #M03.Update_Grafik()
    
def button_newsheet_cmd():
    M08.New_Sheet()
    
def button_Neuberechnen_cmd():
    X02.ActiveSheet.EventWSchanged(X02.ActiveCell())
    #Global_Worksheet_Change(P01.ActiveCell())

ThreadEvent = None

BUTTONLABELWIDTH = 10

start_sheet = "Main"

class Pattern_GeneratorPage(tk.Frame):
    def __init__(self, parent, controller):
        global global_tablemodel, ThisWorkbook
        global dialog_parent
        dialog_parent = self
        self.tabClassName = "PatternConfiguratorPage"
        tk.Frame.__init__(self,parent)
        self.controller = controller
        set_global_controller(controller)
        self.controller.set_statusmessage("Erstelle PatternConfigurator Seite ...",fg="green")
        self.Application = controller.ExcelApplication
        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        
        self.default_font        = self.controller.defaultfontnormal
        self.default_boldfont    = (self.default_font[0],self.default_font[1],"bold")
        self.default_smallfont   = self.controller.defaultfontsmall
        
        globalprocs= {"Make_Morsecode_Init"                    : M20.Make_Morsecode_Init,
                      "Make_Morsecode"                         : M20.Make_Morsecode,
                      "Add_Col_Button_Click"                   : Add_Col_Button_Click,
                      "Del_Col_Button_Click"                   : Del_Col_Button_Click,
                      "M02.Main_Menu"                          : M02.Main_Menu,
                      "PAT09.Import_from_ProgGen_Button_Click" : PAT09.Import_from_ProgGen_Button_Click,
                      "PAT09.Prog_Generator_Button_Click"      : PAT09.Prog_Generator_Button_Click,
                      "PAT09.InsertPicture_Button_Click"       : PAT09.InsertPicture_Button_Click,
                      "button_testen_cmd"                      : button_testen_cmd,
                      "button_aktualisieren_cmd"               : button_aktualisieren_cmd,
                      "button_newsheet_cmd"                    : button_newsheet_cmd}
        
        
        sheetdict_sheetevents = {"Activate": T09.Worksheet_Activate,
                                 "Calculate": None,
                                 "Change": T09.Worksheet_Change,
                                 "Deactivate": T09.Worksheet_Deactivate,
                                 "DoubleClick": AM.Workbook_SheetBeforeDoubleClick,
                                 "SelectionChange": T09.Worksheet_SelectionChange,
                                 "Redraw" : M02.worksheet_redraw,
                                 "ReturnKey" : M02.Global_On_Enter_Proc,
                                }
        
        workbook_events = {"Open": self.Workbook_Open,
                           "NewSheet": None,
                           "BeforeSave": None,
                           "BeforeClose": AM.Workbook_BeforeClose,
                           "SheetBeforeDoubleClick": AM.Workbook_SheetBeforeDoubleClick,
                        }
                   
        sheetdict_PatternGEN={"Main":
                    {"Name":"Main",
                     "Filename"  : "csv/PA_Main.csv",
                     "Fieldnames": "A;B;C;D;E;F;G;H;I;J;K;L;M;N;O;P;Q;R;S;T;U;V;W;X;Y;Z;AA;AB;AC;AD;AE;AF;AG;AH;AI;AJ;AK;AL;AM;AN;AO;AP;AQ;AR;AS;AT;AU;AV;AW;AX,AY;AZ;BA;BB;BC;BD;BE;BF;BG;BH;BI;BJ;BK;BL;BM;BN;BO;BP;BQ;BR;BS;BT;BU;BV;BW;BX,BY;BZ",
                     "Formating" : {"HideCells"       : (("A1"), ),
                                    "HideRows"        : [12,15,16,17,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,46],
                                    #"HideRows"        : [],
                                    "ProtectedCells"  : (("A:D"), ),
                                    "GridList"        : {"1": ((28,4),(28,63)),
                                                         "2": ((49,4),(51,63)),
                                                         "3": ((2, 5), (15, 5)), 
                                                         "4": ((47, 4), (47, 63)),
                                                         },
                                    "GridFormat"      : {"fg": "#808080",
                                                         "show_horizontal_grid": False,
                                                         "show_vertical_grid": False,
                                                         },                                    
                                    "ColumnWidth"     : (40,136,8,64,176,56,56,56,56,56,56,56,56,56),  #(5,17,1,8,22,7),
                                    "ColumnAlignment" : {"ex": ("D"), 
                                                         "wx": ("E", "F")
                                                         }, 
                                    "RowHeight"       : 20,
                                    "FontColor"       : { "1": {
                                                                "font"     : self.default_font,
                                                                "fg"       : "#000000",
                                                                "bg"       : "#FFFF00",
                                                                "Cells"    : ("E2:E15", "E22",) #"F28:BQ28", "D50:BQ60")
                                                                },
                                                        "default": {
                                                               "font"     : self.default_font,
                                                               "fg"       : "#000000",
                                                               "bg"       : "#FFFFFF"
                                                               }
                                                        }
                                    },
                     "SheetType" : "Datasheet",
                     "SaveShapes": True,
                     "RefreshShapesafterLoad": True,
                     "Events" : sheetdict_sheetevents,
                     "Controls" :  { "Default":{ "Components" : [{"Name":"Default",
                                                                  "Accelerator":"",
                                                                  "BackColor":"#00000F",
                                                                  "BorderColor":"#000006",
                                                                  "BorderStyle":"fmBorderStyleNone",
                                                                  "IconName":"",
                                                                  "Caption":"",
                                                                  "Command": None ,
                                                                  "ControlTipText":"",
                                                                  "ForeColor":"#000012",
                                                                  "Height":12,
                                                                  "Left":0,
                                                                  "Top":0,
                                                                  "Type":"",
                                                                  "Visible":True,
                                                                  "Width":12,
                                                                  "AlternativeText":"",
                                                                  "Font" : self.default_font,
                                                                  "CharFormat":{("1.0","1.end"): self.default_boldfont}}
                                                                 ]},
                                     "Form1": { "Name"           : "RGB_LED_CheckBox",
                                                "AlternativeText":"Add_Del_Button",
                                                "BackColor"     : "#FFFFFF",
                                                "BorderColor"   : "#000012",
                                                "Caption"       : "",
                                                "Height"        : 14,
                                                "Left"          : None,
                                                "Col"           : 5,
                                                "Top"           : None,
                                                "Row"           : 48,
                                                "Type"          : "FormWindow",
                                                "Visible"       : True,
                                                "Width"         : 140,
                                                "Components"    : [{"Name":"Add_Col","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                    "Caption":"+",
                                                                    "Command": "Add_Col_Button_Click" ,"ControlTipText":"","ForeColor":"#000012","Height":12,"Left":0,"Top":1,"Type":"CommandButton","Visible":True,"Width":12,"AlternativeText":"Add_Del_Button"},
                                                                   {"Name":"Del_Button","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                    "Caption":"-",
                                                                    "Command": "Del_Col_Button_Click","ControlTipText":"","ForeColor":"#000012","Height":12,"Left":14,"Top":1,"Type":"CommandButton","Visible":True,"Width":12,"AlternativeText":"Add_Del_Button"},
                                                                   {"Name":"RGB_LED_CheckBox","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","Persistent":True,
                                                                    "Caption":"RGB LED",
                                                                    "ControlTipText":"","ForeColor":"#000012","Height":12,"Left":28,"Top":1,"Type":"CheckBox","Visible":True,"Width":100,"AlternativeText":"Add_Del_Button"},
                                                                 ]},
                                    "Form2": {  "Name"          : "Options_Button",
                                                "BackColor"     : "#FFFFFF",
                                                "BorderColor"   : "#000012",
                                                "Caption"       : "",
                                                "Height"        : "50",
                                                "Left"          : None,
                                                "Col"           : 1,
                                                "Top"           : None,
                                                "Row"           : 1,
                                                "Type"          : "FormWindow",
                                                "Visible"       : True,
                                                "Width"         : "50",
                                                "Components"    : [{"Name":"Options","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","IconName":"Btn_PA_Options.png",
                                                                    "Caption":"Options",
                                                                    "Command": "M02.Main_Menu" ,"ControlTipText":"Optionen","ForeColor":"#000012","Height":"50","Left":0,"Top":0,"Type":"CommandButton","Visible":True,"Width":"50"},
                                                                  ]},
                                    "Form3": {  "Name"          : "Import",
                                                "BackColor"     : "#FFFFFF",
                                                "BorderColor"   : "#000012",
                                                "Caption"       : "",
                                                "Height"        : "50",
                                                 "Left"          : None,
                                                "Col"           : 2,
                                                "Top"           : None,
                                                "Row"           : 23,                                        
                                                "Type"          : "FormWindow",
                                                "Visible"       : True,
                                                "Width"         : "50",
                                                "Components"    : [{"Name":"Import","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","IconName":"Btn_PA_Import_from_Prog_Gen.png",
                                                                    "Caption":"Import from ProgGen",
                                                                    "Command": "PAT09.Import_from_ProgGen_Button_Click" ,"ControlTipText":"Optionen","ForeColor":"#000012","Height":"50","Left":0,"Top":0,"Type":"CommandButton","Visible":True,"Width":"50"},
                                                                  ]},
                                    "Form4": {  "Name"          : "Export",
                                                "BackColor"     : "#FFFFFF",
                                                "BorderColor"   : "#000012",
                                                "Caption"       : "",
                                                "Height"        : "50",
                                                "Left"          : None,
                                                "Col"           : 2,
                                                "Top"           : None,
                                                "Row"           : 49,
                                                "Type"          : "FormWindow",
                                                "Visible"       : True,
                                                "Width"         : "50",
                                                "Components"    : [{"Name":"Export","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","IconName":"Btn_PA_Prog_Gen.png",
                                                                    "Caption":"Export zu ProgGen",
                                                                    "Command": "PAT09.Prog_Generator_Button_Click" ,"ControlTipText":"Export zu ProgGen","ForeColor":"#000012","Height":"50","Left":0,"Top":0,"Type":"CommandButton","Visible":True,"Width":"50"},
                                                                  ]},
                                    "Form5": {  "Name"          : "Insert",
                                                "BackColor"     : "#FFFFFF",
                                                "BorderColor"   : "#000012",
                                                "Caption"       : "",
                                                "Height"        : "50",
                                                "Left"          : None,
                                                "Col"           : 2,
                                                "Top"           : None,
                                                "Row"           : 56,                                        
                                                "Type"          : "FormWindow",
                                                "Visible"       : True,
                                                "Width"         : "50",
                                                "Components"    : [{"Name":"Insert","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","IconName":"Btn_PA_insert_image.png",
                                                                    "Caption":"Bild einfügen",
                                                                    "Command": "PAT09.InsertPicture_Button_Click" ,"ControlTipText":"Bild einfügen","ForeColor":"#000012","Height":"50","Left":0,"Top":0,"Type":"CommandButton","Visible":True,"Width":"50"},
                                                                  ]},
                                    "Form6": {  "Name"          : "Test_Leds_M99O01",
                                                "BackColor"     : "#FFFFFF",
                                                "BorderColor"   : "#000012",
                                                "Caption"       : "",
                                                "Height"        : 24,
                                                "Left"          : None,
                                                "Col"           : 9,
                                                "Top"           : None,
                                                "Row"           : 14,                                        
                                                "Type"          : "FormWindow",
                                                "Visible"       : True,
                                                "Width"         : 74,
                                                "Components"    : [{"Name":"Test_Leds_M99O01","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","IconName":"",
                                                                    "Caption":"Test Pattern",
                                                                    "Command": "button_testen_cmd" ,"ControlTipText":"Pattern Testen","ForeColor":"#000012","Height":20,"Left":2,"Top":2,"Type":"CommandButton","Visible":True,"Width":70},
                                                                  ]},
                                    "Form7": {  "Name"          : "ReCalc",
                                                "BackColor"     : "#FFFFFF",
                                                "BorderColor"   : "#000012",
                                                "Caption"       : "",
                                                "Height"        : 24,
                                                "Left"          : None,
                                                "Col"           : 6,
                                                "Top"           : None,
                                                "Row"           : 14,                                        
                                                "Type"          : "FormWindow",
                                                "Visible"       : True,
                                                "Width"         : 74,
                                                "Components"    : [{"Name":"ReCalc","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","IconName":"",
                                                                    "Caption":"Aktualisieren",
                                                                    "Command": "button_aktualisieren_cmd" ,"ControlTipText":"Grafik aktualisieren und Neuberechnen","ForeColor":"#000012","Height":20,"Left":2,"Top":2,"Type":"CommandButton","Visible":True,"Width":70},
                                                                  ]},
                                    "Form8": {  "Name"          : "New_Sheet",
                                                "BackColor"     : "#FFFFFF",
                                                "BorderColor"   : "#000012",
                                                "Caption"       : "",
                                                "Height"        : 24,
                                                "Left"          : None,
                                                "Col"           : 6,
                                                "Top"           : None,
                                                "Row"           : 1,                                        
                                                "Type"          : "FormWindow",
                                                "Visible"       : True,
                                                "Width"         : 74,
                                                "Components"    : [{"Name":"New_Sheet","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","IconName":"",
                                                                    "Caption":"Neues Blatt",
                                                                    "Command": "button_newsheet_cmd" ,"ControlTipText":"Ein neues Blatt hinzufügen","ForeColor":"#000012","Height":20,"Left":2,"Top":2,"Type":"CommandButton","Visible":True,"Width":70},
                                                                  ]},
                                    "Form9": {  "Name"          : "TextBox1",
                                                "BackColor"     : "#FFFFFF",
                                                "BorderColor"   : "#000012",
                                                "Caption"       : "",
                                                "Height"        : 148,
                                                "Left"          : None,
                                                "Col"           : 12,
                                                "Top"           : None,
                                                "Row"           : 1,
                                                "Type"          : "FormWindow",
                                                "Visible"       : True,
                                                "Width"         : 600,
                                                "Components"    : [{"Name":"Text_Box1","BackColor":"#00000F",
                                                                    "Caption": "Mit diesem Blatt kann die Konfiguration eines LED Musters erstellt werden.\nDie Gelb hinterlegten Felder und die Tabellen können verändert werden.\nDie Spalten der Tabelle beschreiben einen Abschnitt des Musters welches für eine bestimmte Zeit angezeigt wird. Die Dauer wird in der ersten Tabelle eingetragen."+
                                                                               "Die Zeiten können in Minuten ('Min') oder Sekunden ('Sec'= angegeben werden. Wird keine Einheit angegeben dann ist die Zeitangabe in Millisekunden ('ms').\n"+
                                                                               "Achtung zwischen Zahl und Einheit muss ein Leerzeichen stehen und die Groß- und Kleinschreibung muss exakt stimmen. Wenn Spalten die gleiche Anzeigedauer haben, dann sollte die Zeit nur in den ersten Spalten angegeben werden zur Minimierung des Speicherverbrauchs. Die Folgenden Zeilen können als Formel Angegeben werden damit man sieht wie lange der Abschnitt dauert. Im Beispiel unten ist das bei den Spalten 4 bis 8 gemacht.\n"+
                                                                               "In der zweiten Tabelle wird mit einem x markiert welche LED in dem Abschnitt leuchten soll. Wenn mehrere Helligkeiststufen benutzt werden, dann wird die Helligkeit als Zahl eingetragen. Die Anzahl der Abschnitte wird automatisch anhand der eingetragenen Markierungen bestimmt. Wenn am Ende leere Abschnitte verwendet werden sollen, dann muss in die letzte Spalte ein Punkt eingefügt werden.",
                                                                    "ForeColor":"#000012","Height":148,"Left":0,"Top":0,"Type":"TextBox","Visible":True,"Width":600}, # ,"CharFormat":{("1.0","1.end"): self.default_boldfont}},
                                                                  ]},                                           
                                }
                     },
                     "PG-Temp": {
                        "Name":"PG-Temp",
                                             "Filename"  : "csv/PA_Main.csv",
                                             "Fieldnames": "A;B;C;D;E;F;G;H;I;J;K;L;M;N;O;P;Q;R;S;T;U;V;W;X;Y;Z;AA;AB;AC;AD;AE;AF;AG;AH;AI;AJ;AK;AL;AM;AN;AO;AP;AQ;AR;AS;AT;AU;AV;AW;AX,AY;AZ;BA;BB;BC;BD;BE;BF;BG;BH;BI;BJ;BK;BL;BM;BN;BO;BP;BQ;BR;BS;BT;BU;BV;BW;BX,BY;BZ",
                                             "Events" : sheetdict_sheetevents,
                                             "Formating" : {"HideCells"       : (("A1"), ),
                                                            "HideRows"        : [12,15,16,17,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,46],
                                                            #"HideRows"        : [],
                                                            "ProtectedCells"  : (("A:D"), ),
                                                            "GridList"        : {"1": ((28,4),(28,63)),
                                                                                 "2": ((49,4),(51,63)),
                                                                                 "3": ((2, 5), (15, 5)),
                                                                                 },
                                                            "GridFormat"      : {"fg": "#808080",
                                                                                 "show_horizontal_grid": False,
                                                                                 "show_vertical_grid": False,
                                                                                 },                                                             
                                                            "ColumnWidth"     : (40,136,8,64,176,56,56,56,56,56,56,56,56,56),  #(5,17,1,8,22,7),
                                                            "ColumnAlignment" : {"ex": ("D"), 
                                                                                 "wx": ("E", "F")
                                                                                 }, 
                                                            "RowHeight"       : 20,
                                                            "FontColor"       : { "1": {
                                                                                        "font"     : self.default_font,
                                                                                        "fg"       : "#000000",
                                                                                        "bg"       : "#FFFF00",
                                                                                        "Cells"    : ("E2:E15", "E22")
                                                                                        },
                                                                                "default": {
                                                                                       "font"     : self.default_font,
                                                                                       "fg"       : "#000000",
                                                                                       "bg"       : "#FFFFFF"
                                                                                       }
                                                                                }
                                                            },
                                             "SheetType" : "Datasheet",
                                             "SaveShapes": False,
                                             "RefreshShapesafterLoad": True,
                                             "Controls" :  { "Default":{ "Components" : [{"Name":"Default",
                                                                                          "Accelerator":"",
                                                                                          "BackColor":"#00000F",
                                                                                          "BorderColor":"#000006",
                                                                                          "BorderStyle":"fmBorderStyleNone",
                                                                                          "IconName":"",
                                                                                          "Caption":"",
                                                                                          "Command": None ,
                                                                                          "ControlTipText":"",
                                                                                          "ForeColor":"#000012",
                                                                                          "Height":12,
                                                                                          "Left":0,
                                                                                          "Top":0,
                                                                                          "Type":"",
                                                                                          "Visible":True,
                                                                                          "Width":12,
                                                                                          "AlternativeText":"",
                                                                                          "Font" : self.default_font,
                                                                                          "CharFormat":{("1.0","1.end"): self.default_boldfont}}
                                                                                         ]},
                                                             "Form1": { "Name"           : "RGB_LED_CheckBox",
                                                                        "AlternativeText":"Add_Del_Button",
                                                                        "BackColor"     : "#FFFFFF",
                                                                        "BorderColor"   : "#000012",
                                                                        "Caption"       : "",
                                                                        "Height"        : 12,
                                                                        "Left"          : None,
                                                                        "Col"           : 5,
                                                                        "Top"           : None,
                                                                        "Row"           : 48,
                                                                        "Type"          : "FormWindow",
                                                                        "Visible"       : True,
                                                                        "Width"         : 100,
                                                                        "Components"    : [{"Name":"Add_Col","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                                            "Caption":"+",
                                                                                            "Command": "Add_Col_Button_Click" ,"ControlTipText":"","ForeColor":"#000012","Height":12,"Left":0,"Top":1,"Type":"CommandButton","Visible":True,"Width":12,"AlternativeText":"Add_Del_Button"},
                                                                                           {"Name":"Del_Button","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                                            "Caption":"-",
                                                                                            "Command": "Del_Col_Button_Click","ControlTipText":"","ForeColor":"#000012","Height":12,"Left":14,"Top":1,"Type":"CommandButton","Visible":True,"Width":12,"AlternativeText":"Add_Del_Button"},
                                                                                           {"Name":"RGB_LED_CheckBox","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","Persistent":True,
                                                                                            "Caption":"RGB LED",
                                                                                            "ControlTipText":"","ForeColor":"#000012","Height":12,"Left":28,"Top":1,"Type":"CheckBox","Visible":True,"Width":60,"AlternativeText":"Add_Del_Button"},
                                                                                         ]},
                                                            "Form4": {  "Name"          : "Export",
                                                                        "BackColor"     : "#FFFFFF",
                                                                        "BorderColor"   : "#000012",
                                                                        "Caption"       : "",
                                                                        "Height"        : "50",
                                                                        "Left"          : None,
                                                                        "Col"           : 2,
                                                                        "Top"           : None,
                                                                        "Row"           : 49,
                                                                        "Type"          : "FormWindow",
                                                                        "Visible"       : True,
                                                                        "Width"         : "50",
                                                                        "Components"    : [{"Name":"Export","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","IconName":"Btn_PA_Prog_Gen.png",
                                                                                            "Caption":"Zurück zum ProgrammGenerator",
                                                                                            "Command": "PAT09.Prog_Generator_Button_Click" ,"ControlTipText":"Zurück zum ProgrammGenerator","ForeColor":"#000012","Height":"50","Left":0,"Top":0,"Type":"CommandButton","Visible":True,"Width":"50"},
                                                                                          ]},
                                                            "Form6": {  "Name"          : "Test_Leds_M99O01",
                                                                        "BackColor"     : "#FFFFFF",
                                                                        "BorderColor"   : "#000012",
                                                                        "Caption"       : "",
                                                                        "Height"        : 24,
                                                                        "Left"          : None,
                                                                        "Col"           : 9,
                                                                        "Top"           : None,
                                                                        "Row"           : 14,                                        
                                                                        "Type"          : "FormWindow",
                                                                        "Visible"       : True,
                                                                        "Width"         : 74,
                                                                        "Components"    : [{"Name":"Test_Leds_M99O01","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","IconName":"",
                                                                                            "Caption":"Test Pattern",
                                                                                            "Command": "button_testen_cmd" ,"ControlTipText":"Pattern Testen","ForeColor":"#000012","Height":20,"Left":2,"Top":2,"Type":"CommandButton","Visible":True,"Width":70},
                                                                                          ]},
                                                            "Form7": {  "Name"          : "ReCalc",
                                                                        "BackColor"     : "#FFFFFF",
                                                                        "BorderColor"   : "#000012",
                                                                        "Caption"       : "",
                                                                        "Height"        : 24,
                                                                        "Left"          : None,
                                                                        "Col"           : 6,
                                                                        "Top"           : None,
                                                                        "Row"           : 14,                                        
                                                                        "Type"          : "FormWindow",
                                                                        "Visible"       : True,
                                                                        "Width"         : 74,
                                                                        "Components"    : [{"Name":"ReCalc","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone","IconName":"",
                                                                                            "Caption":"Aktualisieren",
                                                                                            "Command": "button_aktualisieren_cmd" ,"ControlTipText":"Grafik aktualisieren und Neuberechnen","ForeColor":"#000012","Height":20,"Left":2,"Top":2,"Type":"CommandButton","Visible":True,"Width":70},
                                                                                          ]},
                                                            "Form9": {  "Name"          : "TextBox1",
                                                                        "BackColor"     : "#FFFFFF",
                                                                        "BorderColor"   : "#000012",
                                                                        "Caption"       : "",
                                                                        "Height"        : 148,
                                                                        "Left"          : None,
                                                                        "Col"           : 12,
                                                                        "Top"           : None,
                                                                        "Row"           : 1,
                                                                        "Type"          : "FormWindow",
                                                                        "Visible"       : True,
                                                                        "Width"         : 600,
                                                                        "Components"    : [{"Name":"Text_Box1","BackColor":"#00000F",
                                                                                            "Caption": "Mit diesem Blatt kann die Konfiguration eines LED Musters, übernommen vom Programm-Generator, bearbeitet werden.\nDie Gelb hinterlegten Felder und die Tabellen können verändert werden.\nDie Spalten der Tabelle beschreiben einen Abschnitt des Musters welches für eine bestimmte Zeit angezeigt wird. Die Dauer wird in der ersten Tabelle eingetragen."+
                                                                                                       "Die Zeiten können in Minuten ('Min') oder Sekunden ('Sec'= angegeben werden. Wird keine Einheit angegeben dann ist die Zeitangabe in Millisekunden ('ms').\n"+
                                                                                                       "Achtung zwischen Zahl und Einheit muss ein Leerzeichen stehen und die Groß- und Kleinschreibung muss exakt stimmen. Wenn Spalten die gleiche Anzeigedauer haben, dann sollte die Zeit nur in den ersten Spalten angegeben werden zur Minimierung des Speicherverbrauchs. Die Folgenden Zeilen können als Formel Angegeben werden damit man sieht wie lange der Abschnitt dauert. Im Beispiel unten ist das bei den Spalten 4 bis 8 gemacht.\n"+
                                                                                                       "In der zweiten Tabelle wird mit einem x markiert welche LED in dem Abschnitt leuchten soll. Wenn mehrere Helligkeiststufen benutzt werden, dann wird die Helligkeit als Zahl eingetragen. Die Anzahl der Abschnitte wird automatisch anhand der eingetragenen Markierungen bestimmt. Wenn am Ende leere Abschnitte verwendet werden sollen, dann muss in die letzte Spalte ein Punkt eingefügt werden.\n" +
                                                                                                       "Zurück zum ProgrammGenerator gelangt man mit dem -ProgrammGenerator-Button. Die Änderungen werden dann automatisch übernomen.",
                                                                                            "ForeColor":"#000012","Height":148,"Left":0,"Top":0,"Type":"TextBox","Visible":True,"Width":600}, #"CharFormat":{("1.0","1.end"): self.default_boldfont}},
                                                                                          ]},
                                                            }
                        },                    
                    "Languages":
                      {"Name":"Languages",
                       "Filename"  : "csv/PA_Languages.csv",
                       "Fieldnames": "A;B;C;D;E;F",
                       "Formating" : {}
                       },                             
                   "Goto_Activation_Entries":
                    {"Name":"Goto_Activation_Entries",
                     "Filename"  : "csv/PA_Goto_Activation_Entries.csv",
                     "Fieldnames": "A;B;C;D;E;F;G;H;I;J;K;L;M;N;O;P;Q;R;S;T;U;V;W;X;Y;Z",
                     "Formating" : {},
                     },
                   "Special_Mode_Dlg":
                    {"Name":"Special_Mode_Dlg",
                     "Filename"  : "csv/PA_Special_Mode_Dlg.csv",
                     "Fieldnames": "A;B;C;D;E;F",
                     "Formating" : {},
                     },
                   "Par_Description":
                    {"Name":"Par_Description",
                     "Filename":"csv/PA_Par_Description.csv",
                      "Fieldnames": "A;B;C;D;E;F;G;H;I;J;K"
                    },
                   "Named_Ranges":
                    {"Name":"Named_Ranges",
                     "Filename":"csv/PA_Named_Ranges.csv",
                     "Fieldnames": "A;B;C;D"
                    },
                }
        
        workbook_dict = {"Name": "PatternWorkbook",
                         "Events": workbook_events,
                         "SheetDict" : sheetdict_PatternGEN, 
                         "JumpTable" : globalprocs,
                         }        
                
        
        
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName + " (Betatest)")
        
        #button1_text = macrodata.get("Button_1",self.tabClassName)
        #button2_text = macrodata.get("Button_2",self.tabClassName)
        
        #self.fontlabel = self.controller.get_font("FontLabel")
        #self.fontspinbox = self.controller.get_font("FontSpinbox")
        #self.fonttext = self.controller.get_font("FontText")
        #self.fontbutton = self.controller.get_font("FontLabel")
        #self.fontentry = self.controller.get_font("FontEntry")
        #self.fonttext = self.controller.get_font("FontText")
        #self.fontscale = self.controller.get_font("FontScale")
        self.fonttitle = self.controller.get_font("FontTitle")        
        
        #self.grid_columnconfigure(0,weight=1)
        #self.grid_rowconfigure(0,weight=1)
        
        self.frame=ttk.Frame(self,relief="ridge", borderwidth=2)
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)        
        
        #self.scroll_main_frame = ScrolledFrame(self.frame)
        #self.scroll_main_frame.grid_columnconfigure(0,weight=1)
        #self.scroll_main_frame.grid_rowconfigure(0,weight=1)
        
        #self.main_frame = ttk.Frame(self.scroll_main_frame.interior, relief="ridge", borderwidth=2)
        #self.main_frame.grid_columnconfigure(0,weight=1)
        #self.main_frame.grid_rowconfigure(2,weight=1)         

        
        #config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=1,startrow =1,style="CONFIGPage")        

        self.parent = parent
        
        title_frame = ttk.Frame(self.frame, relief="ridge", borderwidth=0)
        self.button_frame = ttk.Frame(self.frame, borderwidth=0)
        self.workbook_frame = ttk.Frame(self.frame, relief="ridge", borderwidth=2)
        filedir = os.path.dirname(os.path.realpath(__file__))
        self.filedir2 = os.path.dirname(filedir)
        self.workbook_frame.rowconfigure(0,weight=1)
        self.workbook_frame.columnconfigure(0,weight=1)
        X02.Application.EnableEvents=True
        self.workbook_width = self.controller.window_width-120
        self.workbook_height = self.controller.window_height-240
        #self.workbook = X02.create_workbook(frame=self.workbook_frame,path=self.filedir2,pyProgPath=self.filedir2,sheetdict=sheetdict_PatternGEN,workbookName="PatternWorkbook",start_sheet=start_sheet,p_global_controller=self.controller,width=self.workbook_width,height=self.workbook_height)
        self.workbookname = "PatternWorkbook"
        self.tempworkbookFilname = self.controller.tempworkbookFilname
        temp_workbook_filename = os.path.join(self.filedir2,self.tempworkbookFilname+"_"+self.workbookname+".json")        
        
        #************************************************
        #* Open Workbook PatternWorkbook
        #************************************************        
        self.workbook = self.Application.Workbooks.Open(
            ParentFrame=self.workbook_frame,
            FileName=temp_workbook_filename,
            path=self.filedir2,
            pyProgPath=self.filedir2,
            workbookName=self.workbookname,
            InitWorkBookFunction=None,
            macro_caller=self, 
            workbookdict=workbook_dict,
            start_sheet=start_sheet,
            controller=global_controller,
            width=self.workbook_width,
            height=self.workbook_height)
        
        for sheet in self.workbook.sheets:
            sheet.SetChangedCallback(wschangedcallback)
            sheet.SetSelectedCallback(wsselectedcallback)
            sheet.SetCalculationCallback(wscalculationcallback)
            sheet.SetInitDataFunction(SheetInitDataProc)
        
        self.workbook.SetInitWorkbookFunction(None)
                
        # Tabframe
        self.frame.grid(row=0,column=0,sticky="nesw")

        label = ttk.Label(title_frame, text=self.title, font=self.fonttitle)
        label.pack(padx=5,pady=(5,5))
        
        # create buttonlist
        #self.create_button_list()
        
        title_frame.grid(row=0, column=0, sticky="n") #,pady=(10, 10), padx=10)
        #self.button_frame.grid(row=1, column=0, sticky="nw",pady=(10, 10), padx=10)
        self.workbook_frame.grid(row=1,column=0,sticky="nesw")#,pady=(10, 10), padx=10)
    
        #config_frame.grid(row=1, columnspan=2, pady=(20, 30), padx=10)        
        #in_button_frame.grid(row=2, column=0, sticky="n", padx=4, pady=4)
        
        for sheet in self.workbook.sheets:
            pass #test sheet.tablemodel.resetDataChanged()
            
        #D00.init_UserForms()

        self.workbook.activate_sheet(start_sheet)
        
        X02.Application.EnableEvents=True
        
        # ----------------------------------------------------------------
        # Standardprocedures for every tabpage
        # ----------------------------------------------------------------

    def tabselected(self):
        #self.controller.currentTabClass = self.tabClassName
        logging.debug("Tabselected: %s",self.tabname)
        X02.Application.setActiveWorkbook(self.workbook.Name)
        #self.controller.send_to_ARDUINO("#END")
        #time.sleep(ARDUINO_WAITTIME)        
        pass
    
    def tabunselected(self):
        logging.debug("Tabunselected: %s",self.tabname)
        #self.controller.send_to_ARDUINO("#BEGIN")
        #time.sleep(ARDUINO_WAITTIME)            
        pass
    
    def TabChanged(self,_event=None):
        logging.debug("Tabchanged: %s",self.tabname)
        pass
    
    def cancel(self,_event=None):
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

    def connect(self,port):
        pass

    def disconnect(self):
        pass
    
    def create_button_list(self):
        button_list=(
                        {"Icon_name": "",
                         "Text"     : "Grafik Aktualisieren",
                         "command"  : self.button_aktualisieren_cmd,
                         "padx"     : 10,
                         "tooltip"  : "Aktualisieren"},
                        {"Icon_name": "",
                         "Text"     : "Neuberechnen",
                         "command"  : self.button_Neuberechnen_cmd,
                         "padx"     : 10,
                         "tooltip"  : "Neuberechnen"},                        
                        {"Icon_name": "",
                         "Text"     : "Testen",
                         "command"  : self.button_testen_cmd,
                         "padx"     : 10,
                         "tooltip"  : "Testen"},
                    )
        
        filedir = os.path.dirname(os.path.realpath(__file__))
        self.filedir2 = os.path.dirname(filedir)
        
        self.icon_dict = {}
        
        for button_desc in button_list:
            self.create_button(button_desc)
            
    def button_testen_cmd(self):
        X02.Application.Caller="Test_Leds_M99O01"
        M80.Button_Pressed()
        
    def button_aktualisieren_cmd(self):
        X02.Application.Caller="Update"
        M03.Update_Grafik()
        
    def button_Neuberechnen_cmd(self):
        X02.ActiveSheet.EventWSchanged(X02.ActiveCell())
        #Global_Worksheet_Change(P01.ActiveCell())
        
    def prog_Attiny(self):
        M65.Prog_Tiny_UniProg()
            
    def create_button(self, button_desc):
        if button_desc["Icon_name"] != "":
            filename = r"/images/"+button_desc["Icon_name"]
            filepath = self.filedir2 + filename
            self.icon_dict[button_desc["Icon_name"]] = tk.PhotoImage(file=filepath)
            button=ttk.Button(self.button_frame, text="Dialog", image=self.icon_dict[button_desc["Icon_name"]], command=button_desc["command"])
        else:
            button=ttk.Button(self.button_frame, text=button_desc["Text"], command=button_desc["command"])
        button.pack( side="left",padx=button_desc["padx"])
        self.controller.ToolTip(button, text=button_desc["tooltip"])
    
    def get_param_config_dict(self, paramkey):
        paramconfig_dict = self.controller.MacroParamDef.data.get(paramkey,{})
        return paramconfig_dict    
    
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
                    logging.debug(e, exc_info=True) 
                    logging.debug("ERROR: PatternConfiguratorPage - Write_stdout_to_text_window: %s",output)
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
            logging.error("PatternConfiguratorPage - Exception in start_ARDUINO_program_Popen %s - %s",e,self.startfile[0])
            self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")
            self.arduinoMonitorPage.add_text_to_textwindow("\n* Exception in start_ARDUINO_program_Popen "+ e + "-" + self.startfile[0]+ "\n",highlight="Error")
            self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")
    
    def upload_to_ARDUINO(self,_event=None,arduino_type="LED",init_arduino=False):
    # send effect to ARDUINO
        if self.controller.ARDUINO_status == "Connecting":
            tk.messagebox.showwarning(title="Zum ARDUINO Hochladen", message="PC versucht gerade sich mit dem ARDUINO zu verbinden, bitte warten Sie bis der Vorgang beendet ist!")
            return
        self.controller.disconnect()
        self.controller.set_connectstatusmessage("Kompilieren und Hochladen ...",fg="green")
        
        #if arduino_type == "LED":
        #    self.create_ARDUINO_CMD(init_arduino=init_arduino)
                
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

    def checkcolor(self,ColorTable,callback=None):
        self.controller.coltab = ColorTable
        self.controller.checkcolor_callback = callback
        self.controller.showFramebyName("ColorCheckPage")
        
    def get_ThisWorkbook(self):
        global ThisWorkbook
        return ThisWorkbook
    def set_ThisWorkbook(self, value):
        global ThisWorkbook
        ThisWorkbook = value
    ThisWorkbook = property(fget=get_ThisWorkbook, fset=set_ThisWorkbook, doc="ThisWorkbook")

    def Workbook_Open(self):
        D00.init_UserForms()
        AM.Workbook_Open()

# ----------------------------------------------------------------
# Callback procedures
# ---------------------------------------------------------------- 

def wschangedcallback(changedcell):    
    #print ("wschangedcallback ",changedcell.Row,":",changedcell.Column)
    M02.Global_Worksheet_Change(changedcell)
    
def wsselectedcallback(changedcell):
    
    #print ("wsselectedcallback ",changedcell.Row,":",changedcell.Column)
    M02.Global_Worksheet_SelectionChange(changedcell)    
   
def wscalculationcallback(worksheet,cell=None):
    Calc_Worksheet(worksheet,cell=cell)
    
def SheetInitDataProc(sheet):
    Target=X02.CRange(5,5,ws=sheet)
    M02.Global_Worksheet_Change(Target)
    sheet.Redraw_table()
    
    
    
ThisWorkbook=None