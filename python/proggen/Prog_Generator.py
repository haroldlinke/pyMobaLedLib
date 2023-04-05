# -*- coding: utf-8 -*-
#
#         Prog_Generator
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

import time

from vb2py.vbconstants import *

from mlpyproggen.DefaultConstants import ARDUINO_WAITTIME,LARGE_FONT, SMALL_FONT, VERY_LARGE_FONT, PROG_VERSION,ARDUINO_LONG_WAITTIME
# fromx mlpyproggen.configfile import ConfigFile
from locale import getdefaultlocale
# fromx tkintertable import TableCanvas, TableModel
# fromx collections import OrderedDict
from ExcelAPI.XLW_Workbook import create_workbook
import proggen.M02_Public as M02
import proggen.M08_ARDUINO as M08
import proggen.M40_ShellandWait as M40

import ExcelAPI.XLW_Workbook as P01

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
import  proggen.F00_mainbuttons as F00
import proggen.M02_Public as M02
import proggen.M09_Language as M09
import proggen.M07_COM_Port as M07
import proggen.M20_PageEvents_a_Functions as M20
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

def get_global_controller():
    return global_controller

def get_dialog_parent():
    return dialog_parent
ThreadEvent = None

BUTTONLABELWIDTH = 10



start_sheet  = "DCC"
ThisWorkbook = None
            
class Prog_GeneratorPage(tk.Frame):
    def __init__(self, parent, controller):
        global global_tablemodel, ThisWorkbook
        global dialog_parent
        dialog_parent = self
        self.tabClassName = "ProgGeneratorPage"
        tk.Frame.__init__(self,parent)
        self.controller = controller
        set_global_controller(controller)
        self.default_font        = self.controller.defaultfontnormal
        self.default_boldfont    = (self.default_font[0],self.default_font[1],"bold")
        self.default_smallfont   = self.controller.defaultfontsmall
        
        datasheet_fieldnames = "A;Aktiv;Filter;Adresse oder Name;Typ;Start-\nwert;Beschreibung;Verteiler-\nNummer;Stecker\nNummer;Icon;Name;Beleuchtung, Sound, oder andere Effekte;Start LedNr;LEDs;InCnt;Loc InCh;LED\nSound\nKanal;Comment"
        datasheet_formating = { "HideCells" : ((0,1),(0,2),(0,3),(0,5),(0,7),(0,12),(0,13),(0,14),(0,15),(0,16),(1,"*")),
                                "ProtectedCells"  : ((0,0),(1,0),("*",12),("*",13),("*",14),("*",15),("*",16)),
                                "left_click_callertype": "cell",
                                "FontColor"       : { "1": {
                                                            "font"     : self.default_smallfont,
                                                            "fg"       : "#FFFF00",
                                                            "bg"       : "#0000FF",
                                                            "Cells"    : ((0,"*"),(1,"*"))
                                                            },
                                                      "2": {
                                                            "font"     : ("Wingdings",10),
                                                            "fg"       : "#000000",
                                                            "bg"       : "#FFFFFF",
                                                            "Cells"    : (("*",1),)
                                                            },                                                          
                                                    "default": {
                                                           "font"     : self.default_font,
                                                           "fg"       : "#000000",
                                                           "bg"       : "#FFFFFF",
                                                           "Cells"    : (("*","*"),)
                                                           }
                                        }
                            }
                                
        sheetdict_PROGGEN={"DCC":
                    {"Name":"DCC",
                     "Filename"  : "csv/DCC.csv",
                     "Fieldnames": datasheet_fieldnames,
                     "Formating" : datasheet_formating,
                     "SheetType" : "Datasheet"
                     },
                   "Selectrix":
                    {"Name":"Selectrix",
                     "Filename"  : "csv/Selectrix.csv",
                     "Fieldnames": "A;Aktiv;Filter;Channel oder\nName[0..99];Bitposition\n[1..8];Typ;Start-\nwert;Beschreibung;Verteiler-\nNummer;Stecker\nNummer;Icon;Name;Beleuchtung, Sound, oder andere Effekte;Start LedNr;LEDs;InCnt;Loc InCh;LED\nSound\nKanal;Comment",
                     "Formating" : datasheet_formating,
                     "SheetType" : "Datasheet"
                     },
                   "CAN":
                    {"Name":"CAN",
                     "Filename"  : "csv/CAN.csv",
                     "Fieldnames": datasheet_fieldnames,
                     "Formating" : datasheet_formating,
                     "SheetType" : "Datasheet"
                     },
                   "Examples":
                    {"Name":"Examples",
                     "Filename"  : "csv/Examples.csv",
                     "Fieldnames": datasheet_fieldnames,
                     "Formating" : datasheet_formating,
                     "SheetType" : "Datasheet"
                     },
                   "Config":
                    {"Name":"Config",
                     "Filename":"csv/Config.csv",
                     "Fieldnames": "A;B;C;D",
                     "SheetType" : "Config",
                     "Formating" : { "HideCells"       : (("*",3),),
                                    "ProtectedCells"  : ( ("*",1),("*",3)),
                                    "FontColor"       : { "1": {
                                                                "font"     : self.default_font ,
                                                                "fg"       : "#0000FF",
                                                                "bg"       : "#FFFFFF",
                                                                "Cells"    : ((0,"*"),)
                                                                },
                                                        "default": {
                                                               "font"     : self.default_font ,
                                                               "fg"       : "#000000",
                                                               "bg"       : "#FFFFFF",
                                                               "Cells"    : (("*","*"),)
                                                               }
                                                        }
                                    }
                    },
                   "Languages":
                    {"Name":"Languages",
                     "Filename":"csv/Languages.csv",
                     "Fieldnames": "A;B;C;D;E;F;G;H;I"
                    },
                   "Lib_Macros":
                    {"Name":"Lib_Macros",
                     "Filename":"csv/Lib_Macros.csv",
                     "Fieldnames": "A;B;C;D;E;F;G;H;I;J;K;L;M;N;O;P;Q;R;S;T;U;V;W;X;Y;Z;AA;AB;AC;AD;AE;AF;AG;AH;AI;AJ;AK;AL;AM;AN;AO;AP;AQ;AR;AS"
                    },
                   "Libraries":
                    {"Name":"Libraries",
                     "SheetType" : "Libraries",
                     "Filename":"csv/Libraries.csv",
                     "Fieldnames": "A;B;C;D;E;F;G;H;I;J",
                     "Formating" : {"ProtectedCells"  : ((0,"*"),(1,"*"),(2,"*"),(3,"*"),(4,"*"),(5,"*"),(6,"*"),(7,"*")),
                                    "FontColor"       : { "1": {
                                                                "font"     : self.default_font ,
                                                                "fg"       : "#FFFF00",
                                                                "bg"       : "#0000FF",
                                                                "Cells"    : ((6,"*"),)
                                                                },
                                                        "default": {
                                                               "font"     : self.default_font ,
                                                               "fg"       : "#000000",
                                                               "bg"       : "#FFFFFF",
                                                               "Cells"    : (("*","*"),)
                                                               }
                                                        },
                                    "left_click_callertype": "cell"
                                    }
                    },
                   "Par_Description":
                    {"Name":"Par_Description",
                     "Filename":"csv/Par_Description.csv",
                      "Fieldnames": "A;B;C;D;E;F;G;H;I;J;K"
                    },
                   "Platform_Parameters":
                    {"Name":"Platform_Parameters",
                     "Filename":"csv/Platform_Parameters.csv",
                     "Fieldnames": "A;B;C;D;E"
                    },
                   "Named_Ranges":
                    {"Name":"Named_Ranges",
                     "Filename":"csv/Named_Ranges.csv",
                     "Fieldnames": "A;B;C;D"
                    },
                   "Events": {"Workbook_Open"          : None,
                              "Workbook_BeforeClose"   : None,
                              "SheetActivate"          : None,
                              "SheetDeactivate"        : None,
                              "SheetTableUpdate"       : None,
                              "SheetCalculate"         : None,
                              "SheetBeforeDoubleClick" : None,
                              "SheetChange"            : M20.Global_Worksheet_Change,
                              "SheetSelectionChange"   : None,
                              "SheetReturnKey"         : None,
                              "NewSheet"               : None
                   }           
                }        
        
        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName)
        self.Start_Compile_Time = 0
        
        #button1_text = macrodata.get("Button_1",self.tabClassName)
        #button2_text = macrodata.get("Button_2",self.tabClassName)
        
        #self.fontlabel = self.controller.get_font("FontLabel")
        #self.fontspinbox = self.controller.get_font("FontSpinbox")
        #self.fonttext = self.controller.get_font("FontText")
        #self.fontbutton = self.controller.get_font("FontLabel")
        #self.fontentry = self.controller.get_font("FontEntry")
        self.fonttext = self.controller.get_font("FontText")
        #self.fontscale = self.controller.get_font("FontScale")
        self.fonttitle = self.controller.get_font("FontTitle")        
        
        #self.grid_columnconfigure(0,weight=1)
        #self.grid_rowconfigure(0,weight=1)
        
        self.frame=ttk.Frame(self,relief="ridge", borderwidth=2)
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)
        #self.frame.columnconfigure(0,weight=1)
        #self.frame.rowconfigure(0,weight=1)            
        
        #self.scroll_main_frame = ScrolledFrame(self.frame)
        #self.scroll_main_frame.grid_columnconfigure(0,weight=1)
        #self.scroll_main_frame.grid_rowconfigure(0,weight=1)
        
        #self.main_frame = ttk.Frame(self.scroll_main_frame.interior, relief="ridge", borderwidth=2)
        #self.main_frame.grid_columnconfigure(0,weight=1)
        #self.main_frame.grid_rowconfigure(2,weight=1)         

        
        #config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=1,startrow =1,style="CONFIGPage")        

        self.parent = parent
        
        title_frame = ttk.Frame(self.frame, relief="ridge", borderwidth=2)
        self.info_frame  = ttk.Frame(self.frame, borderwidth=0)
        self.button_frame = ttk.Frame(self.frame, borderwidth=0)
        self.workbook_frame = ttk.Frame(self.frame, relief="ridge", borderwidth=2)
        filedir = os.path.dirname(os.path.realpath(__file__))
        filedir2 = os.path.dirname(filedir)
        filedir3 = os.path.dirname(filedir2)
        filedir4 = os.path.dirname(filedir3)
        self.filedir5 = os.path.dirname(filedir4)
        self.workbook_frame.rowconfigure(0,weight=1)
        self.workbook_frame.columnconfigure(0,weight=1)
        #self.workbook_frame.grid_rowconfigure(0,weight=1)
        #self.workbook_frame.grid_columnconfigure(0,weight=1)
        
        self.workbook_width = self.controller.window_width-120
        self.workbook_height = self.controller.window_height-420
        self.workbook = create_workbook(frame=self.workbook_frame,path=filedir2, pyProgPath=filedir2, workbookName="ProgGenerator", sheetdict=sheetdict_PROGGEN,start_sheet=start_sheet,p_global_controller=global_controller,width=self.workbook_width,height=self.workbook_height)
        ThisWorkbook=self.workbook
        
        for sheet in self.workbook.sheets:
            sheet.SetChangedCallback(wschangedcallback)
            sheet.SetSelectedCallback(wsselectedcallback)
            sheet.SetCalculationCallback(wscalculationcallback)
            sheet.SetInitDataFunction(F00.worksheet_init)
           
        self.workbook.SetInitWorkbookFunction(F00.workbook_init)
                
        # Tabframe
        self.frame.grid(row=0,column=0,sticky="nesw")

        label = ttk.Label(title_frame, text=self.title, font=self.fonttitle)
        label.pack(padx=5,pady=(5,5))
        
        # create buttonlist
        self.create_button_list()
        
        self.infotext = M02.Prog_Version
        
        infolabel = ttk.Label(self.info_frame, text=self.infotext, font=self.fonttext)
        infolabel.grid(row=0, column=0, sticky="n",pady=(10, 10), padx=10)
        
        title_frame.grid(row=0, column=0, sticky="n",pady=(10, 10), padx=10)
        self.button_frame.grid(row=1, column=0, sticky="nw",pady=(10, 10), padx=10)
        self.info_frame.grid(row=1,column=1,sticky="nw",pady=(10, 10), padx=10)
        self.workbook_frame.grid(row=2,column=0,columnspan=2,sticky="nesw",pady=(10, 10), padx=10)
    
        #config_frame.grid(row=1, columnspan=2, pady=(20, 30), padx=10)        
        #in_button_frame.grid(row=2, column=0, sticky="n", padx=4, pady=4)
        
        for sheet in self.workbook.sheets:
            sheet.tablemodel.resetDataChanged()
        
        self.workbook.activate_sheet(start_sheet)
            
        
        
        # ----------------------------------------------------------------
        # Standardprocedures for every tabpage
        # ----------------------------------------------------------------

    def tabselected(self):
        #self.controller.currentTabClass = self.tabClassName
        logging.debug("Tabselected: %s",self.tabname)
        P01.Application.setActiveWorkbook(self.workbook.Name)
        for sheet in self.workbook.sheets:
            if self.controller.getConfigData("ShowHiddentables"):
                sheet.Visible(True)
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

    def connect(self):
        pass

    def disconnect(self):
        pass
    
    # ----------------------------------------------------------------
    # End of Standardprocedures for every tabpage
    # ---------------------------------------------------------------- 
    

        
    def create_button_list(self):
        
        button_list=(
                        {"Icon_name": "Btn_Dialog.png",
                         "command"  : F00.Dialog_Button_Click,
                         "text"     : "Dialog",
                         "padx"     : 20,
                         "tooltip"  : "Dialog aufrufen"},
                        {"Icon_name": "Btn_Send_to_ARDUINO.png",
                         "command"  : F00.Arduino_Button_Click,
                         "shift_command": F00.Arduino_Button_Shift_Click,
                         "text"     : "Z. Arduino\nschicken",
                         "padx"     : 20,
                         "tooltip"  : "ARDUINO aufrufen"},
                        {"Icon_name": "Btn_Insert_Row.png",
                         "command"  : F00.Insert_Button_Click,
                         "text"     : "Zeile\neinfügen",
                         "padx"     : 10,
                         "tooltip"  : "Zeile\neinfügen"},
                        {"Icon_name": "Btn_Delete_Row.png",
                         "command"  : F00.Del_Button_Click,
                         "text"     : "Lösche\nZeilen",
                         "padx"     : 10,
                         "tooltip"  : "Zeile löschen"},
                        {"Icon_name": "Btn_Move_Row.png",
                         "command"  : F00.Move_Button_Click,
                         "text"     : "Verschiebe\nZeilen",
                         "padx"     : 10,
                         "tooltip"  : "Zeile verschieben"},
                        {"Icon_name": "Btn_Copy_Row.png",
                         "command"  : F00.Copy_Button_Click,
                         "text"     : "Kopiere\nZeilen",
                         "padx"     : 10,
                         "tooltip"  : "Zeile kopieren"},
                        {"Icon_name": "Btn_Hide_Unhide.png",
                         "command"  : F00.Hide_Button_Click,
                         "text"     : "Aus- oder\nEinblenden",
                         "padx"     : 20,
                         "tooltip"  : "Zeile verstecken/einblenden"},
                        {"Icon_name": "Btn_Unhide_all.png",
                         "command"  : F00.UnHideAll_Button_Click,
                         "text"     : "Alle\nEinblenden",
                         "padx"     : 20,
                         "tooltip"  : "Alle versteckten Zeilen einblenden"},
                        {"Icon_name": "Btn_Delete_Table.png",
                         "command"  : F00.ClearSheet_Button_Click,
                         "text"     : "Lösche\nTabelle",
                         "padx"     : 10,
                         "tooltip"  : "Tabelle löschen"},
                        {"Icon_name": "Btn_Options.png",
                         "command"  : F00.Options_Button_Click,
                         "text"     : "Optionen",
                         "padx"     : 20,
                         "tooltip"  : "Optionen anzeigen"},
                        {"Icon_name": "Btn_Help.png",
                         "command"  : F00.Help_Button_Click,
                         "text"     : "Hilfe",
                         "padx"     : 20,
                         "tooltip"  : "Hilfe aufrufenn"}                        
                    )
        
        filedir = os.path.dirname(os.path.realpath(__file__))
        self.filedir2 = os.path.dirname(filedir)
        
        self.icon_dict = {}
        
        for button_desc in button_list:
            self.create_button(button_desc)
            
    def create_button(self, button_desc):
        filename = r"/images/"+button_desc["Icon_name"]
        filepath = self.filedir2 + filename
        self.icon_dict[button_desc["Icon_name"]] = tk.PhotoImage(file=filepath)
        button_text = M09.Get_Language_Str(button_desc["text"])
        button=tk.Button(self.button_frame, text=button_text, image=self.icon_dict[button_desc["Icon_name"]], command=button_desc["command"]) #,compound="center")
        shift_command = button_desc.get("shift_command",None)
        if shift_command:
            button=tk.Button(self.button_frame, text=button_text, image=self.icon_dict[button_desc["Icon_name"]]) #,compound="center")
            button.bind("<Button-1>", button_desc["command"])
            button.bind("<Shift-Button-1>", shift_command)
        else:
            button=tk.Button(self.button_frame, text=button_text, image=self.icon_dict[button_desc["Icon_name"]], command=button_desc["command"]) #,compound="center")
        
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
            #print(P01.Format(int(time.time()), 'hh:mm:ss')," write_stdout-start")
    
            if output != '' and self.continue_loop:
                try:
                    self.arduinoMonitorPage.add_text_to_textwindow(output.decode('utf-8').strip())
                except BaseException as e:
                    logging.debug(e)
                    logging.debug("ERROR: Write_stdout_to_text_window: %s",output)
                    
                    pass            
            
            if self.process.poll() is not None:
                self.continue_loop=False
                M08.Stop_Compile_Time_Display()
                self.rc = self.process.poll()
                if self.rc==1:
                    self.arduinoMonitorPage.add_text_to_textwindow("\n******** "+self.ARDUINO_message3+" ********\n",highlight="Error")
                    error_flag=True
                else:
                    self.arduinoMonitorPage.add_text_to_textwindow("\n"+self.ARDUINO_message2+"\n*******************************************************\n",highlight="OK")
                    error_flag=False
                ResFile = 'Start_Arduino_Result.txt'    
                if P01.Dir(ResFile) != '':
                    error_flag = True
                self.upload_to_ARDUINO_end(error_flag)
                
        #print(P01.Format(int(time.time()), 'hh:mm:ss')," write_stdout-end")
    
        if self.continue_loop:
            self.after(50,self.write_stdout_to_text_window)
            
    def EndProg(self):
        #-------------------
        # Is called in case of an fatal error
        # Normaly this function should not be called because the
        # global variables and dialog positions are cleared.
        #ShowHourGlassCursor(False)
        P01.Application.EnableEvents = True
        P01.Application.ScreenUpdating = True
        sys.exit(0)
        
    def Update_Compile_Time(self, Start=False):
        #---------------------------------------------------------
        #global Start_Compile_Time
        # Is called by OnTime
        print(P01.Format(int(time.time()), 'hh:mm:ss')," write_update_compile_time")
        if self.Start_Compile_Time != 0 or Start:
            if Start:
                self.Start_Compile_Time = int(time.time())
                F00.StatusMsg_UserForm.Set_ActSheet_Label(P01.Format(int(time.time()) - self.Start_Compile_Time, 'hh:mm:ss'))
            else:
                F00.StatusMsg_UserForm.Set_ActSheet_Label(P01.Format(int(time.time()) - self.Start_Compile_Time, 'hh:mm:ss'))
            P01.Application.OnTime(1000, self.Update_Compile_Time)
    
        
    def Stop_Compile_Time_Display(self):
        #--------------------------------------
        global Start_Compile_Time
        self.upload_duration = int(time.time()) - self.Start_Compile_Time
        self.Start_Compile_Time = 0
        P01.Unload(F00.StatusMsg_UserForm)
        
    def ClearStatusbar(self):
        #--------------------------
        # Is called by onTime to clear the status bar after a while
        P01.set_statusmessage("")
    
        
    def Show_Status_for_a_while(self, Txt, Duration=r'00:00:15'):
        #-------------------------------------------------------------------------------------------
        P01.set_statusmessage(Txt)
        if Txt != r'':
            P01.Application.OnTime(15000, self.ClearStatusbar)
        else:
            P01.Application.OnTime(15000, self.ClearStatusbar)    
            
    def upload_to_ARDUINO_end(self,error_flag):
        pass
        if error_flag:
            self.Stop_Compile_Time_Display()
            P01.MsgBox(M09.Get_Language_Str('Es ist ein Fehler aufgetreten ;-(' + vbCr + vbCr + 'Zur Fehlersuche kann man die letzten Änderungen wieder rückgängig machen und es noch mal versuchen. ' + vbCr + vbCr + 'Kommunikationsprobleme erkennt man an dieser Meldung: ' + vbCr + '   avrdude: ser_open(): can\'t open device "\\\\.\\COM') + '":' + vbCr + M09.Get_Language_Str('   Das System kann die angegebene Datei nicht finden.' + vbCr + 'In diesem Fall müssen die Verbindungen überprüft und der Arduino durch einen neuen ersetzt werden.' + vbCr + vbCr + 'Der Fehler kann auch auftreten wenn der DCC/Selextrix Arduino noch nicht programmiert wurde.' + vbCr + 'Am besten man steckt den rechten Arduino erst dann ein wenn er benötigt wird.' + vbCr + vbCr + 'Wenn der Fehler nicht zu finden ist und immer wieder auftritt, dann kann ein Screenshot des ' + 'vorangegangenen Bildschirms (Nach oben scrollen so dass die erste Meldung nach dem Arduino Bild zu sehen ist) ' + 'zusammen mit dem Excel Programm und einer ausführlichen Beschreibung an ' + vbCr + '  MobaLedLib@gmx.de' + vbCr + 'geschickt werden.'), vbInformation, M09.Get_Language_Str('Fehler beim Hochladen des Programms'))
            #self.EndProg()
        else:
            self.Stop_Compile_Time_Display()
            #Debug.Print('Compile and upload duration: ' + P01.Format(P01.Time() - Start, 'hh:mm:ss'))
            self.Show_Status_for_a_while(M09.Get_Language_Str('Programm erfolgreich hochgeladen. Kompilieren und Hochladen dauerte ') + P01.Format(self.upload_duration, 'hh:mm:ss'), '00:02:00')
    
    def start_ARDUINO_program_cmd(self,startfile,arduino_type="LED"):
        self.Update_Compile_Time(Start=True)
        macrodata = self.controller.MacroDef.data.get("ARDUINOMonitorPage",{})
        self.ARDUINO_message1 = macrodata.get("Message_1","")
        self.ARDUINO_message2 = macrodata.get("Message_2","")
        self.ARDUINO_message3 = macrodata.get("Message_3","")        
        self.arduinoMonitorPage=self.controller.getFramebyName ("ARDUINOMonitorPage")
        self.arduinoMonitorPage.delete_text_from_textwindow()
        
        logging.debug(repr(startfile))
        
        self.arduinoMonitorPage.add_text_to_textwindow("\n\n*******************************************************\n"+self.ARDUINO_message1+"\n*******************************************************\n\n")
        
        if arduino_type=="LED":
            self.arduinoMonitorPage.add_text_to_textwindow("***************************************************************************\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*    Zum                                                                  *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*     PC             PythonProg_Generator " + PROG_VERSION+ " by Harold    *\n")
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
            self.arduinoMonitorPage.add_text_to_textwindow("*              PC     PythonProg_Generator " + PROG_VERSION+ " by Harold    *\n")
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
        
        self.execute_shell_cmd(startfile,"Upload started")
        self.Stop_Compile_Time_Display()
        return 
    
        try:
            self.process = subprocess.Popen(startfile, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin = subprocess.DEVNULL,shell=True)
            self.continue_loop=True
            self.write_stdout_to_text_window()
        except BaseException as e:
            #logging.error("Exception in start_ARDUINO_program_Popen %s - %s",e,self.startfile[0])
            self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")
            self.arduinoMonitorPage.add_text_to_textwindow("\n* Exception in start_ARDUINO_program_Popen "+ e + "-" + self.startfile[0]+ "\n",highlight="Error")
            self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")    
    
    def terminate_process(self,event=None):
        self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")
        self.arduinoMonitorPage.add_text_to_textwindow("\n* Program Terminated by User\n",highlight="Error")
        self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")
        self.process.terminate()
    
    def execute_shell_cmd(self,cmd_str,message1):
        
        self.arduinoMonitorPage=self.controller.getFramebyName ("ARDUINOMonitorPage")
        self.arduinoMonitorPage.delete_text_from_textwindow()
        self.controller.bind("c",self.terminate_process)
        
        logging.debug("execute_shell_cmd:"+cmd_str)
        
        self.arduinoMonitorPage.add_text_to_textwindow("\n\n*******************************************************\n"+ message1 +"\n*******************************************************\n\n")
        
        self.controller.showFramebyName("ARDUINOMonitorPage")
        self.arduinoMonitorPage.update()
        
        try:
            self.process = subprocess.Popen(cmd_str, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin = subprocess.DEVNULL,shell=True)
            self.continue_loop=True
        
            # Poll process.stdout to show stdout live
            while True:
                output = self.process.stdout.readline()
                if self.process.poll() is not None:
                    logging.debug("shell ended")
                    #print("shell ended")
                    break
                if output:
                    self.arduinoMonitorPage.add_text_to_textwindow(str(output)+"\n")
                    self.arduinoMonitorPage.update()
    
            rc = self.process.returncode
            
            self.arduinoMonitorPage.update()
            
            if rc != 0:
                self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")
                return M40.Failure
            else:
                self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="OK")
                return M40.Success
        
        except subprocess.TimeoutExpired:
            #self.Stop_Compile_Time_Display()
            #P01.Unload(F00.StatusMsg_UserForm)
            return M40.Timeout
        except BaseException as e:
            #self.Stop_Compile_Time_Display()
            #P01.Unload(F00.StatusMsg_UserForm)
            logging.debug("execute_shell_cmd:"+e)
            #logging.error("Exception in start_ARDUINO_program_Popen %s - %s",e,self.startfile[0])
            self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")
            self.arduinoMonitorPage.add_text_to_textwindow("\n* Exception in start_ARDUINO_program_Popen "+ e + "-" + "\n",highlight="Error")
            self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")            
        
        return rc
            
    def start_ARDUINO_program_Popen(self):
        self.Update_Compile_Time(Start=True)
        try:
            self.process = subprocess.Popen(self.startfile, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin = subprocess.DEVNULL,shell=True)
            self.continue_loop=True
            self.write_stdout_to_text_window()
        except BaseException as e:
            #logging.error("Exception in start_ARDUINO_program_Popen %s - %s",e,self.startfile[0])
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
            if P01.checkplatform("Darwin"): # Mac
            #if macos:
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
    
    

def wschangedcallback(changedcell):
    
    #print ("wschangedcallback ",changedcell.Row,":",changedcell.Column)
    M20.Global_Worksheet_Change(changedcell)
    
def wsselectedcallback(changedcell):
    
    #print ("wsselectedcallback ",changedcell.Row,":",changedcell.Column)
    M20.Global_Worksheet_SelectionChange(changedcell)
    
def wscalculationcallback(worksheet,cell=None):
   pass
    


