# -*- coding: utf-8 -*-
#
#         Workbook
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
# 2021-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2022-01-07 v4.02 HL: - Else:, ByRef check done - first PoC release
# 2022-01-08 V4.03 HL: - added Workbook Save and Load
# 2022-04-02 LX4.18 HL: update to MLL V3.1.0F4, removed keyword "exit_on_error" and annotation for global variables
# 2022-04-03 LX4.19 HL: added platformcheck

import logging
import locale
import platform
import pathlib

from tkintertable import TableCanvas, TableModel
import tkinter as tk
from tkinter import ttk
from ExcelAPI.X01_Excel_Consts import *
from vb2py.vbconstants import *
from vb2py.vbfunctions import *
import time
import datetime

from pathlib import Path

#import proggen.M20_PageEvents_a_Functions as M20
import subprocess
import pickle
import proggen.Prog_Generator as PG
import proggen.F00_mainbuttons as F00
import proggen.M02_Public as M02
import proggen.M18_Save_Load as M18
import proggen.M25_Columns as M25
import proggen.M37_Inst_Libraries as M37
import proggen.M39_Simulator as M39

#import proggen.M01_Gen_Release_Version as M01
import keyboard
#import proggen.M25_Columns as M25
#import proggen.M02_global_variables as M02
import proggen.M28_divers as M28

pyProgfile_dir = "\\LEDs_AutoProg\\pyProg_Generator_MobaLedLib"

shift_key = False

datasheet_fieldnames = "A;Aktiv;Filter;Adresse oder Name;Typ;Start-\nwert;Beschreibung;Verteiler-\nNummer;Stecker\nNummer;Icon;Name;Beleuchtung, Sound, oder andere Effekte;Start LedNr;LEDs;InCnt;Loc InCh;LED\nSound\nKanal;Comment"
datasheet_formating = { "HideCells" : ((0,1),(0,2),(0,3),(0,5),(0,7),(0,12),(0,13),(0,14),(0,15),(0,16),(1,"*")),
                        "ProtectedCells"  : ((0,0),(1,0),("*",12),("*",13),("*",14),("*",15),("*",16)),
                        "left_click_callertype": "cell",
                        "FontColor"       : { "1": {
                                                    "font"     : ("Arial",8),
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
                                                   "font"     : ("Arial",10),
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
                                                        "font"     : ("Arial",10),
                                                        "fg"       : "#0000FF",
                                                        "bg"       : "#FFFFFF",
                                                        "Cells"    : ((0,"*"),)
                                                        },
                                                "default": {
                                                       "font"     : ("Arial",10),
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
                                                        "font"     : ("Arial",10),
                                                        "fg"       : "#FFFF00",
                                                        "bg"       : "#0000FF",
                                                        "Cells"    : ((6,"*"),)
                                                        },
                                                "default": {
                                                       "font"     : ("Arial",10),
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
            }
        }

sheetdict_PatternGEN={"Main":
            {"Name":"Main",
             "Filename"  : "csv/PA_main.csv",
             "Fieldnames": "A;B;C;D;E;F;G;H;I;J;K;L;M;N;O;P;Q;R;S;T;U;V;W;X;Y;Z;AA;AB;AC;AD;AE;AF;AG;AH;AI;AJ;AK;AL;AM;AN;AO;AP;AQ;AR;AS",
             "Formating" : {"HideCells"       : ((0,0),),
                            "HideRows"        : (12,15,16,17,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46),
                            "ProtectedCells"  : ( ("*",0),("*",1),("*",2),("*",3)),
                            "GridList"        : (((27,4),(27,63)),((48,3),(50,63))),
                            "ColumnWidth"     : (5,17,1,8,22,7),
                            "ColumnAlignment" : {3:"e",},
                            "RowHeight"       : 20,
                            "FontColor"       : { "1": {
                                                        "font"     : ("Arial",9),
                                                        "fg"       : "#000000",
                                                        "bg"       : "#FFFF00",
                                                        "Cells"    : ((1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(10,4),(11,4),(12,4),(13,4),(14,4),(15,4),(21,4))
                                                        },
                                                "default": {
                                                       "font"     : ("Arial",9),
                                                       "fg"       : "#000000",
                                                       "bg"       : "#FFFFFF",
                                                       "Cells"    : (("*","*"),)
                                                       }
                                                }
                            },
             "SheetType" : "Datasheet"
             },
           "PA_Languages":
            {"Name":"Languages",
             "Filename"  : "csv/PA_Languages.csv",
             "Fieldnames": "A;B;C;D;E;F",
             "Formating" : {}
             },
           "PA_Goto_Activation_Entries":
            {"Name":"Goto_Activation_Entries",
             "Filename"  : "csv/PA_Goto_Activation_Entries.csv",
             "Fieldnames": "A;B;C;D;E;F",
             "Formating" : {},
             },
           "PA_Special_Mode_Dlg":
            {"Name":"Special_Mode_Dlg",
             "Filename"  : "csv/PA_Special_Mode_Dlg.csv",
             "Fieldnames": "A;B;C;D;E;F",
             "Formating" : {},
             },
           "PA_Par_Description":
            {"Name":"Par_Description",
             "Filename":"csv/PA_Par_Description.csv",
              "Fieldnames": "A;B;C;D;E;F;G;H;I;J;K"
            },
           "Named_Ranges":
            {"Name":"Named_Ranges",
             "Filename":"csv/Named_Ranges.csv",
             "Fieldnames": "A;B;C;D"
            }
        }

def checkplatform(checkstr):
    teststr = platform.system()
    logging.debug("Checkplatform: "+teststr+"-"+checkstr)
    return teststr==checkstr

def get_home_dir():
    logging.debug("get_home_dir")
    homedir = pathlib.Path.home()
    logging.debug("HomeDir:"+homedir)
    return homedir

def Dir(filepath,dummy=None):
    if os.path.isfile(filepath):
        return filepath
    else:
        if os.path.isdir(filepath):
            return filepath
        else:
            return ""
        

def Date_str():
    return Date()

def Time_str():
    t = datetime.datetime.now()
    return t.strftime("%X")

def Center_Form(form):
    return

def Shell(cmd):
    Run(cmd)

def updateWindow():
    PG.global_controller.update()

def TimeValue(Duration):
    return str(Duration)

def getvalue(row,column):
    value=ActiveSheet.tablemodel.getValueAt(row-1,column-1)
    #print("P01.getvalue:",row,column,value)
    return value

def ActiveCell():
    global Selection
    table = ActiveSheet.table
    row = table.getSelectedRow()+1
    col = table.getSelectedColumn()+1
    Selection = CSelection(ActiveSheet.Cells(row,col)) #*HL
    return ActiveSheet.Cells(row,col) #*HL

def set_activeworkbook(workbook):
    global ThisWorkbook,ActiveSheet,ActiveWorkbook
    ActiveWorkbook = Workbook = ThisWorkbook = workbook
    ActiveSheet = ActiveWorkbook.Sheets("DCC")
    PG.global_controller.activeworkbook = workbook
    
def create_workbook(frame=None, path=None,pyProgPath=None,workbookName=None,workbookFilename=None,sheetdict=sheetdict_PROGGEN):
    global ThisWorkbook,ActiveSheet,ActiveWorkbook
    workbook = ThisWorkbook = CWorkbook(frame=frame,path=path,pyProgPath=pyProgPath,workbookName=workbookName,workbookFilename=workbookFilename,sheetdict=sheetdict)
    set_activeworkbook(workbook)
    return workbook
    
def IsError(testval):
    return False

def Cells(row:int, column:int,ws=None):
    if ws == None:
        ws=ActiveSheet
    cell = ws.Cells(row,column)
    return cell

def Range(cell1,cell2):
    return CRange(cell1,cell2,ws=ActiveSheet)

def Sheets(sheetname):
    return ActiveWorkbook.Sheets(sheetname)

def Rows(row):
    sheet = ActiveSheet
    if type(row)==str:
        rows=[]
        rowlist=row.split(":")
        for row1 in range(int(rowlist[0]),int(rowlist[1])+1):
            return CRow(row1)
    else:
        return CRow(row)
        #sheet = ActiveSheet
        #return sheet.MaxRange.Rows[row]
   
def Columns(col:int):
    sheet = ActiveSheet
    return sheet.MaxRange.Columns[col]

def IsEmpty(obj):
    if len(obj)==0:
        return True
    else:
        return False

def val(value):
    valtype=type(value)
    if valtype is CCell:
        cellvalue = value.get_value()
        if cellvalue != "":
            if IsNumeric(cellvalue):
                return int(cellvalue)
            else:
                return 0
        else:
            return 0
    elif valtype is str:
        if value != "":
            if IsNumeric(value):
                return int(value)
            else:
                return 0
        else:
            return 0
    return int(value)

def VarType(obj):
    valtype=type(obj)
    if valtype is str:
        return vbString
    else:
        return None
def Unload(UserForm):
    UserForm.destroy()

def ChDrive(srcdir):
    #print("ChDrive:", srcdir)
    
    if checkplatform=="Windows":
        drive = srcdir[0:2]
        os.chdir(drive)
    return

def Format(value,formatstring):
    if formatstring == "hh:mm:ss":
        time_val = time.gmtime(value)
        return time.strftime("%H:%M:%S",time_val)
    elif formatstring == "hh:mm":
        if type(value)==str:
            return value[:5]
        else:
            time_val = time.gmtime(value)
            return time.strftime("%H:%M",time_val)

    elif formatstring == "0000":
        return "{0:4d}".format(value)
    
    elif formatstring == "00":
        return "{0:2d}".format(value)
    elif formatstring == "dd.mm.yy":
        return value[:2]+"."+value[3:5]+"."+value[6:]
    else:
        pass
    
    return str(value) # no formating implemented yet


def MsgBox(ErrorMessage:str, msg_type:int, ErrorTitle:str):
    if msg_type == vbQuestion + vbYesNoCancel or msg_type == vbYesNoCancel:
        res=tk.messagebox.askyesnocancel(title=ErrorTitle, message=ErrorMessage)
        if res == None:
            return vbCancel
        if res:
            return vbYes
        else:
            return vbNo
    elif msg_type == vbQuestion + vbYesNo or msg_type == vbYesNo:
        res=tk.messagebox.askyesno(title=ErrorTitle, message=ErrorMessage)
        if res == None:
            return vbCancel
        if res:
            return vbYes
        else:
            return vbNo        
    elif msg_type == vbOKCancel:
        res=tk.messagebox.askokcancel(title=ErrorTitle, message=ErrorMessage)
        if res == None:
            return vbCancel
        if res:
            return vbOK
        else:
            return vbCancel
    elif msg_type == vbOKOnly:
        res=tk.messagebox.showinfo(title=ErrorTitle, message=ErrorMessage)
        
    elif msg_type == vbInformation:
        res=tk.messagebox.showinfo(title=ErrorTitle, message=ErrorMessage)
        
    elif msg_type == vbCritical:
        res=tk.messagebox.showerror(title=ErrorTitle, message=ErrorMessage)
        
    elif msg_type == vbCritical + vbYesNo:
        res=tk.messagebox.askyesno(title=ErrorTitle, message=ErrorMessage)
        if res == None:
            return vbCancel
        if res:
            return vbYes
        else:
            return vbNo
    else:
        logging.debug("P01_MSGBox: Unknown Messagetype:"+str(msg_type))
        res=tk.messagebox.askyesnocancel(title=ErrorTitle, message=ErrorMessage)
        if res == None:
            return vbCancel
        if res:
            return vbYes
        
    return vbNo

def InputBox(Message:str, Title:str, Default=None):
    #res = tk.simpledialog.askstring(Title,Message,initialvalue=Default,parent=PG.dialog_parent)
    
    F00.Userform_SimpleInput.Show(Message,Title,Default)
    res = F00.Userform_SimpleInput.UserForm_res
    if res == None:
        res=""
    return res

def Time():
    return time.time()

def Date():
    x = datetime.datetime.now()
    return x.strftime("%x")

def Run(cmd):
    subprocess.run(cmd,shell=True)
    
def set_statusmessage(message):
    PG.global_controller.set_statusmessage(message)
    PG.global_controller.update()

__VK_LBUTTON = 0x1
__VK_RBUTTON = 0x2
__VK_MBUTTON = 0x4
__VK_UP = 0x26
__VK_DOWN = 0x28
__VK_RETURN = 0xD
__VK_ESCAPE = 0x1B
__VK_CONTROL = 0x11
__VK_SHIFT = 0x10

def GetAsyncKeyState(key):
    global shift_key
    if key==__VK_UP:
        return keyboard.is_pressed("up")
    if key==__VK_DOWN:
        return keyboard.is_pressed("down")
    if key==__VK_RETURN:
        return keyboard.is_pressed("enter")
    if key==__VK_ESCAPE:   
        return keyboard.is_pressed("escape")
    if key==__VK_CONTROL:   
        return keyboard.is_pressed("crtl")
    if key==__VK_SHIFT:
        Debug.Print("Check Shift Key")
        fn_return_value = shift_key #or keyboard.is_pressed("shift")
        shift_key=False
        return fn_return_value
    return


def GetCursorPos():
    pass

def SetCursorPos(x,y):
    pass

def DoEvents():
    pass


class CWorkbook:
    def __init__(self, frame=None,path=None,pyProgPath=None,workbookName=None, workbookFilename=None, sheetdict=sheetdict_PROGGEN,init_workbook=None,open_workbook=None):
        global Workbooks,ThisWorkbook,pyProgfile_dir
        # Row and Columns are 0 based and not 1 based as in Excel

        if workbookName:
            self.Name = workbookName
        else:
            self.Name = "PyProgramWorkbook"
        Workbooks.append(self)
        if frame != None:
            self.Path = path
            self.pyProgPath = pyProgPath
            self.master = frame
            self.init_workbook_proc=init_workbook
            self.open_workbook_proc = open_workbook
            self.tabframedict = {}

            self.FullName = workbookFilename
            style = ttk.Style(frame)
            style.configure('downtab.TNotebook', tabposition='sw')
            self.container = ttk.Notebook(frame, style="downtab.TNotebook")
            
            self.container.grid_rowconfigure(0,weight=1)
            self.container.grid_columnconfigure(0,weight=1)                 

            self.container.grid(row=0,column=0,columnspan=2,sticky="nesw")
            self.tabdict = dict()
            self.tabdict_frames = dict()
            self.sheets = list()
            self.sheetdict = sheetdict
            self.tabid = 0
            for sheetname in self.sheetdict.keys():
                tabframe = ttk.Frame(self.container,relief="ridge", borderwidth=1)
                worksheet = self.new_sheet(sheetname,tabframe)
                tabframe.sheetname = sheetname
                tabframe.sheet = worksheet
                self.sheets.append(worksheet)
                self.container.add(tabframe, text=sheetname)
                self.tabframedict[sheetname]=worksheet
                if not self.showws and not PG.global_controller.show_hiddentables:
                    worksheet.Visible(False)
                    #self.container.tab(tabframe,state="hidden")
                self.tabid += 1
                    
            self.container.bind("<<NotebookTabChanged>>",self.TabChanged)
               
        else:
            self.Path = path
            self.tablemodel= None
            self.sheets = None
        ThisWorkbook = self
        self.open()
        
    def init_workbook(self):
        F00.workbook_init(self)

    def open(self):
        if M28.Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0) == 1: #               ' 04.04.22: Juergen Simulator
            M39.OpenSimulator()
           
    def new_sheet(self,sheetname,tabframe):
        sheetname_prop = self.sheetdict.get(sheetname)
        sheettype = sheetname_prop.get("SheetType","")
        callback = sheettype in ["Datasheet","Libraries"]
        self.showws = sheettype in ["Datasheet","Config"]
        formating_dict = sheetname_prop.get("Formating",None)
        fieldnames = sheetname_prop.get("Fieldnames",None)
        if type(fieldnames) == str:
            fieldnames = fieldnames.split(";")
        worksheet = CWorksheet(sheetname,workbook=self, csv_filepathname=(Path(self.pyProgPath) / sheetname_prop["Filename"]),frame=tabframe,fieldnames=fieldnames,formating_dict=formating_dict,Sheettype=sheettype,callback=callback,tabid=self.tabid)
        return worksheet

            
    def TabChanged(self,_event=None):
        newtab_name = self.container.select()
        if newtab_name != "":
            newtab = self.container.nametowidget(newtab_name)
            sheet_name = newtab.sheetname
            sheet = newtab.sheet
            if sheet:
                sheet.Activate()
                #print("Sheet activated:",sheet_name)
            
            #newtab.tabselected()
        #logging.debug("TabChanged %s - %s",self.oldTabName,newtab_name)        
        
    def Sheets(self,name):
        if self.sheets != None:
            for sheet in self.sheets:
                if sheet.Name == name:
                    return sheet
        return None
    
    def Worksheets(self,name):
        if self.sheets != None:
            for sheet in self.sheets:
                if sheet.Name == name:
                    return sheet
        return None
    
    def Activate(self):
        return
    
    def notimplemented(self,command):
        n = tk.messagebox.showinfo(command,
                               "Not implemented yet",
                                parent=self.master)
    
    def Save(self,filename=None):
        if filename == None:
            filename = tk.filedialog.asksaveasfilename(parent=self.master,
                                                        defaultextension='.table',
                                                        #initialdir=os.getcwd(),
                                                        filetypes=[("pickle","*.table"),
                                                          ("All files","*.*")])
        if filename:
            self.SaveWorkbook(filename)
        return
    
    def Load(self,filename=None):
        """load from a file"""

        if filename == None:
            filename = tk.filedialog.askopenfilename(parent=self.master,
                                                      defaultextension='.table',
                                                      #initialdir=os.getcwd(),
                                                      filetypes=[("pickle","*.table"),
                                                        ("All files","*.*")])
        if not os.path.exists(filename):
            #print ('file does not exist')
            return
        if filename:
            self.LoadWorkbook(filename)
        return
    
    def SavePGF(self,filename=None):
        M18.Save_Data_to_File()
        return
    
    def LoadPGF(self,filename=None):
        """load PGF from a file"""
        M18.Load_Data_from_File()
        return       
    
    def SaveWorkbook(self,filename,allsheets=False):
        workbookdata = {}
        for sheet in self.sheets:
            if sheet.Datasheet or sheet.Configsheet or allsheets:
                sheetdata = sheet.getData()
                workbookdata[sheet.Name] = sheetdata
        
        fd = open(filename,'wb')
        pickle.dump(workbookdata,fd)
        fd.close()
        return
    
    def LoadWorkbook(self,filename):
        fd=open(filename,'rb')
        workbookdata = pickle.load(fd)

        for sheet in self.sheets:
            data = workbookdata.get(sheet.Name,{})
            if data !={}:
                sheet.setData(data)
                sheet.init_data()
                sheet.tablemodel.resetDataChanged()
        return
    
    def update_library(self):
        #self.notimplemented("update_library")
        M37.Update_MobaLedLib_from_Arduino_and_Restart_Excel()
    
    def install_Betatest(self):
        self.notimplemented("install_Betatest")
    
    def library_status(self):
        self.notimplemented("library_status")
        
    
    def install_fast_bootloader(self):
        self.notimplemented("install_fast_bootloader")
        
    def start_patternconf(self):
        self.notimplemented("start_patternconf")
    
    def send_to_patternconf(self):
        self.notimplemented("send_to_patternconf")
    
    def receiver_from_patternconf(self):
        self.notimplemented("receiver_from_patternconf")
        
    def check_Data_Changed(self):
        for sheet in self.sheets:
            if sheet.check_Data_Changed():
                return True
        return False
        
        

class CWorksheet:
    
    def __init__(self,Name,tablemodel=None,workbook=None,csv_filepathname=None,frame=None,fieldnames=None,formating_dict=None,Sheettype="",callback=False,tabid=0):
        
        sheetdict_popmenu = {"DCC":
                             { "LED blinken Ein/Aus":self.LED_flash,
                               "LED nacheinander blinken Ein/Aus":self.LED_flash_seq
                             }
                            }
        
        #controller = PG.get_global_controller()
        #screen_width = controller.winfo_screenwidth()
        #screen_height = controller.winfo_screenheight()
        #pos_x = controller.winfo_x()
        #pos_y = controller.winfo_y()
        #root = tk.Tk()
        #root.update_idletasks()
        #root.geometry("+"+str(pos_x)+"+"+str(pos_y))
        #root.attributes('-fullscreen', True)
        #root.state('iconic')
        #geometry = root.winfo_geometry()
        #print(geometry)
        screen_width = 1920 #root.winfo_screenwidth()
        screen_height = 1080 #root.winfo_screenheight()        
        #root.destroy()
        self.rightclickactiondict = sheetdict_popmenu.get(Name,{})
        self.width = screen_width-120
        self.height = screen_height-450
        self.Workbook = workbook
        self.ProtectContents = False
        self.Datasheet = Sheettype == "Datasheet"
        self.Configsheet = Sheettype == "Config"
        self.csv_filepathname = csv_filepathname
        self.fieldnames = fieldnames
        self.formating_dict = formating_dict
        self.Name = Name
        self.shape_clicked = False
        self.Tabframe = frame
        self.DataChanged=False
        self.tabid = tabid
        if tablemodel:
            self.tablemodel = tablemodel
            self.table = TableCanvas(frame, tablename=Name, model=tablemodel,width=self.width,height=self.height,scrollregion=(0,0,self.width,self.height),rightclickactions=self.rightclickactiondict)
        else:
            if csv_filepathname:
                #self.tablemodel = TableModel()
                self.table = TableCanvas(frame, tablename=Name, model=None,width=self.width,height=self.height,scrollregion=(0,0,self.width,self.height),rightclickactions=self.rightclickactiondict)
                self.table.importCSV(filename=self.csv_filepathname, sep=';',fieldnames=self.fieldnames)
                self.tablemodel = self.table.getModel()
                if callback:
                    self.table.set_left_click_callback(self.left_click_callback)
            else:
                return
        if self.formating_dict:
            self.tablemodel.nodisplay = self.formating_dict.get("HideCells",[])
            self.tablemodel.hiderowslist = self.formating_dict.get("HideRows",[])
            self.tablemodel.protected_cells = self.formating_dict.get("ProtectedCells",[])
            self.tablemodel.format_cells = self.formating_dict.get("FontColor",{})
            self.tablemodel.gridlist = self.formating_dict.get("GridList",[])
            self.tablemodel.ColumnAlignment = self.formating_dict.get("ColumnAlignment",{})
            colsizelist = self.formating_dict.get("ColumnWidth",[])
            self.table.resizecolumns(colsizelist)
            rowheight=self.formating_dict.get("RowHeight",30)
            self.table.setRowHeight(rowheight)
            self.table.left_click_callertype=self.formating_dict.get("left_click_callertype",None)
        self.table.show()
        self.update_table_properties()
        self.DataChanged=False
        
    def init_data(self):
        F00.worksheet_init(self)
        self.DataChanged=False
        
    def update_table_properties(self):
        self.LastUsedRow_val = self.tablemodel.getLastUsedRow()+1
        self.LastUsedColumn_val = self.tablemodel.getColumnCount()
        self.UsedRange_val = CRange((0,0) , (self.LastUsedRow_val,self.LastUsedColumn_val),ws=self)
        self.MaxRange_val  = CRange((0,0) , (self.LastUsedRow_val,self.LastUsedColumn_val),ws=self)
        #self.Rectangles = CRectangles()
        self.AutoFilterMode = False
        self.searchcache = {}
        self.Shapes = CShapeList(self.tablemodel)
        self.CellDict = CCellDict(ws=self)
        self.End_val = self.LastUsedColumn_val
        
    def LED_flash(self,row,col):
        #print("LED Flash:",row,col)
        lednum_str = Cells(row+1,13)
        if lednum_str == "":
            lednum_str = Cells(row,13) # take LED num from previous line
            if lednum_str.isnumeric():
                lednum = int(lednum_str)
                ledcount_str = Cells(row,14)
                if ledcount_str.isnumeric():
                    ledcount=int(ledcount_str)
                else:
                    ledcount = 1
                lednum = lednum+ledcount+1 # next LED after current
                ledcount = 1
        else:
            if lednum_str.isnumeric():
                lednum = int(lednum_str)
                ledcount_str = Cells(row+1,14)
                if ledcount_str.isnumeric():
                    ledcount=int(ledcount_str)
                else:
                    ledcount = 1
            else:
                return
            
        PG.global_controller.blinking_on_off(lednum,ledcount)
            
    def LED_flash_seq(self,row,col):
        #print("LED Flash_seq:",row,col)
        lednum_str = Cells(row+1,13)
        if lednum_str.isnumeric():
            lednum = int(lednum_str)
            ledcount_str = Cells(row+1,14)
            if ledcount_str.isnumeric():
                ledcount=int(ledcount_str)
            else:
                ledcount = 1
            
            PG.global_controller.blinking_on_off(lednum,ledcount,seq=True)    
        
    def left_click_callback(self,value1,value2,callertype="cell"):
        
        if callertype=="cell":
            if self.shape_clicked:
                self.shape_clicked=False
                return False
            row=value1
            col=value2
            #print("Left_Click_Call_Back:",row,col)
            if col == 1:  # aktive column
                cell = self.Cells(row+1,col+1)
                if cell.Value == "":
                    cell.Value = chr(252)
                else:
                    cell.Value= ""
                self.Redraw_table()
                return False
            else:
                return True
        elif callertype=="canvas":
            #print("Leftclick-Canvas",value1)
            #callingshape = self.Shapes.shapelist[int(value1[0])]
            Application.caller = int(value1[0])
            if Application.canvas_leftclickcmd!=None:
                Application.canvas_leftclickcmd()
                self.shape_clicked = True # avoid cell maked as clicked
                return False
        
    def EnableMousePosition(self):
        pass
    
    def addrow_if_needed(self,row=None):
        if row==None:
            row = self.table.getSelectedRow()
        if row==self.tablemodel.getRowCount():
            self.addrow_after_current_row()
        
    def addrow_after_current_row(self,copy=False):
        cur_row = self.table.getSelectedRow()
        num_rows = len(self.table.get_selectedRecordNames())
        if num_rows==0:
            num_rows = 1
        copyfromrow=None
        if copy:
            copyfromrow = cur_row
        self.table.addRows(num=num_rows,atrow=cur_row,copyfromrow=copyfromrow)
    
    def deleterows(self):
        self.table.deleteRow()
        
    def moveRows(self): #,sc_rowlist,destrow):
        self.table.Flag_move=True
        #print("Move started")
        return
    
    def UsedRange_Rows(self):
        rowlist=[]
        for row in range(1,self.get_LastUsedRow()+1):
            rowlist.append(CRow(row))
        return rowlist
        
    def get_LastUsedRow(self):
        self.LastUsedRow_val = self.tablemodel.getLastUsedRow()+1 #self.tablemodel.getRowCount()
        return self.LastUsedRow_val
    
    def set_LastUsedRow(self,value):
        self.LastUsedRow_val = value
        self.tablemodel.setLastUsedRow(value-1)
    
    LastUsedRow = property(get_LastUsedRow, set_LastUsedRow, doc='Last used row')
    
    def get_LastUsedColumn(self):
        self.LastUsedColumn_val = self.tablemodel.getColumnCount()
        return self.LastUsedColumn_val
    
    def set_LastUsedColumn(self,value):
        self.LastUsedColumn_val= value
    
    LastUsedColumn = property(get_LastUsedColumn, set_LastUsedColumn, doc='Last used row')
    End = property(get_LastUsedColumn, set_LastUsedColumn, doc='Last used row')

    def get_UsedRange(self):
        self.UsedRange_val = CRange((0,0) , (self.get_LastUsedRow(),self.LastUsedColumn_val),ws=self)
        return self.UsedRange_val
    
    def set_UsedRange(self,value):
        self.UsedRange_val = value
               
    UsedRange = property(get_UsedRange, set_UsedRange, doc='used range')
    MaxRange  = property(get_UsedRange, set_UsedRange, doc='used range')
           
    def Cells(self,row, col):
        #print("Cells", self.Name, row, col)
        if row <=self.tablemodel.getRowCount() and col <=self.tablemodel.getColumnCount():
            cell = CCell(self.tablemodel.getCellRecord(row-1, col-1),row=row,column=col,tablemodel=self.tablemodel,parent=self,Sheet=self)
        else:
            cell=CCell("",row=row,column=col,tablemodel=self.tablemodel,parent=self,Sheet=self)
        #cell.set_tablemodel(self.tablemodel)
        #cell.set_row(row)
        #cell.set_column(col)
        #cell.set_parent(self)
        #cell.set_sheet(self)
        return cell
    
    def get_cellvalue_direct(self,sheet,row,col):
        tablemodel = sheet.tablemodel
        max_cols = tablemodel.getColumnCount()
        if col <= max_cols:
            value = tablemodel.getValueAt(row-1,col-1)
        else:
            value = ""
        return value
    
    def find_RangeName(self,rangestr):
        # returns CCell with row and column of the Named_range
        LSh = ThisWorkbook.Sheets("Named_Ranges")
    
        _row = LSh.find_in_col_ret_row(rangestr,1,cache=True)
        if _row != None:
            named_range_sheetname= self.get_cellvalue_direct(LSh,_row,2)
            named_range_sheet = ThisWorkbook.Sheets(named_range_sheetname)
            named_range_col = int(self.get_cellvalue_direct(LSh,_row,3))
            named_range_row = int(self.get_cellvalue_direct(LSh,_row,4))
            cell = CCell("")
            cell.set_tablemodel(named_range_sheet.tablemodel)
            cell.set_column(named_range_col)
            cell.set_row(named_range_row)
            cell.set_sheet(named_range_sheet)
            return cell
        else:
            return None
    
    def Range(self,cell1,cell2=None):
        #print("Range,cell1,cell2,ws=self")
        if type(cell1) == str:
            named_cell = self.find_RangeName(cell1)
            return named_cell
        else:
            return CRange((cell1.Row,cell1.Column),(cell2.Row,cell2.Column),ws=self)
        
    def Range_set(self,rangestr,value):
        oldflag = Application.EnableEvents
        Application.EnableEvents=False
        named_cell = self.find_RangeName(rangestr)
        named_cell.Value = value
        Application.EnableEvents = oldflag
    
    def Unprotect(self):
        self.ProtectContents = False
        
    def Protect(self, DrawingObjects=True, Contents=True, Scenarios=True, AllowFormattingCells=True, AllowInsertingHyperlinks=True):
        self.ProtectContents = True
        return
        
    def Columns(col:int):
        #print("Columns",col)
        return None
    
    def EnableDisableAllButtons(self,value):
        return
    
    def SetChangedCallback(self,callback):
        self.wschanged_callback = callback
        
    def SetSelectedCallback(self,callback):
        self.wsselected_callback = callback
        
    def EventWSchanged(self, changedcell):
        if self.wschanged_callback and Application.EnableEvents:
            self.wschanged_callback(changedcell)
            
    def EventWSselected(self, selectedcell):
        if self.wsselected_callback and Application.EnableEvents:
            self.wsselected_callback(selectedcell)
            
    def Redraw_table(self,do_bindings=False):
        self.table.redraw()
        if do_bindings:
            #print("Redraw_Table - do bindings")
            self.do_bindings()
        
    def set_value_in_cell(self,row,column,newval):
        cell = self.Cells(row, column)
        cell.Value=newval
        
        """
        colname = self.tablemodel.getColumnName(column-1)
        #coltype = tablemodel.columntypes[colname]
        name = self.tablemodel.getRecName(row-1)
        if colname in self.tablemodel.data[name]:
            if self.tablemodel.data[name][colname] != newval:
                self.tablemodel.data[name][colname] = newval
                if Application.EnableEvents:
                    print("Workbook contents changed")
                    ActiveSheet.EventWSchanged(self)
        """
        
    def create_search_colcache(self,searchcol):
        colcontent = self.tablemodel.getColCells(searchcol-1)
        row = 1
        self.searchcache[searchcol]={}
        searchcol_dict = self.searchcache[searchcol]
        for col in colcontent:
            if len(col)>50:
                col=col[:50]
            searchcol_dict[col]=row
            row=row+1
        return
        
    def find_in_col_ret_col_val(self,searchtext, searchcol, resultcol,cache=True):
        
        if cache:
            colcache = self.searchcache.get(searchcol,None)
            if not colcache:
                self.create_search_colcache(searchcol)
                colcache = self.searchcache.get(searchcol,None)
            if len(searchtext)>50:
                searchtext=searchtext[:50]
            res_row = colcache.get(searchtext,None)
            if not res_row:
                return None # searchtext not found
            else:
                return self.tablemodel.getCellRecord(res_row-1, resultcol-1)
        else:
            pass
        return None
    
    def find_in_col_ret_row(self,searchtext, searchcol, cache=True):
        
        if cache:
            colcache = self.searchcache.get(searchcol,None)
            if not colcache:
                self.create_search_colcache(searchcol)
                colcache = self.searchcache.get(searchcol,None)
            res_row = colcache.get(searchtext,None)
            if not res_row:
                return None # searchtext not found
            else:
                return res_row
        return None    
                
    def find_in_col_set_col_val(self,searchtext, searchcol, setcol,setval,cache=False):
        if cache:
            colcache = self.searchcache.get(searchcol,None)
            if not colcache:
                self.create_search_colcache(searchcol)
                colcache = self.searchcache.get(searchcol,None)
            res_row = colcache.get(searchtext,None)
            if not res_row:
                return None # searchtext not found
            else:
                self.set_value_in_cell(res_row, setcol, setval)
                return True
        else:
            pass
        return None
    
    def Activate(self):
        global ActiveSheet
        ActiveSheet = self
        self.table.do_bindings()
        Port=Cells(M02.SH_VARS_ROW, M25.COMPort_COL)
        if F00.port_is_available(Port):    
            PG.global_controller.setConfigData("serportname",Port)        
        return
    
    def do_bindings(self):
        #print("do bindings")
        self.table.do_bindings()
        
    def remove_bindings(self):
        #print("remove bindings")
        self.table.remove_bindings()
    
    def Select(self):
        global ActiveSheet
        ActiveSheet = self
        self.Workbook.container.select(self.tabid)
        return
    
    def Visible(self,value):
        if value==True:
            self.Workbook.container.tab(self.tabid,state="normal")
            #self.Workbook.container.add(self)
        else:
            self.Workbook.container.tab(self.tabid,state="disable")
            self.Workbook.container.hide(self.tabid)
        
        return    
    def getData(self):
        data = self.tablemodel.getData()
        return data
    
    def setData(self,data):
        self.tablemodel.createEmptyModel()
        self.tablemodel.setupModel(data)
        self.table.redrawTable()
        
    def getSelectedRow(self):
        selectedRow=self.table.getSelectedRow()+1
        return selectedRow
    
    def clearSheet(self):
        self.table.clearData(question=False)
        self.table.importCSV(filename=self.csv_filepathname, sep=';',fieldnames=self.fieldnames)
        self.tablemodel = self.table.getModel()
        if self.formating_dict:
            self.tablemodel.nodisplay = self.formating_dict.get("HideCells",[])
            self.tablemodel.hiderowslist = self.formating_dict.get("HideRows",[])
            self.tablemodel.protected_cells = self.formating_dict.get("ProtectedCells",[])
            self.tablemodel.format_cells = self.formating_dict.get("FontColor",{})
        #self.table.redraw()
        self.update_table_properties()
        self.Activate()
        
    def check_Data_Changed(self):
        return self.DataChanged or self.tablemodel.checkDataChanged()

class CShapeList(object):
    def __init__(self,model=None):
        self.tablemodel = model
        self.tablemodel.shapelist = list()
       
        
    def getShape(self,index):
        shape = self.tablemodel.shapelist[index-1]
        return shape
    
    def getlist(self):
        return self.tablemodel.shapelist
        
    def AddShape(self, name, shapetype, Left, Top, Width, Height, Fill,text=""):
        shape=None
        if shapetype == msoShapeRectangle:
            shape=ActiveSheet.table.addShape(name, "rect", Left, Top, Width, Height, Fill)
        elif shapetype == msoTextBox:
            shape=ActiveSheet.table.addShape(name, "rect", Left, Top, Width, Height, Fill,text=text)
        return shape
        
    def Delete(self,shape):
        ActiveSheet.table.deleteshape(shape)
        #if type(shape)==int:
        #    del self.tablemodel.shapelist[shape-1]
        #else:
        #    self.tablemodel.shapelist.remove(shape)
        
    def Count(self):
        return len(self.tablemodel.shapelist)

        
class CRange:
    def __init__(self,t1,t2,ws=None):
        self.ws=ws
        #print("Range:",t1,t2)
        if type(t1)==CCell:
            t1=(t1.Row,t1.Column)
        if type(t2)==CCell:
            t2=(t2.Row,t2.Column)
        self.start=[t1[0],t1[1]]
        self.end=[t2[0],t2[1]]
        #self.Rows=[]
        #self.Columns = []
        #self.Cells = []
        self.CountLarge = (t2[0]-t1[0]+1)*(t2[1]-t1[1]+1)
        self.Font = CFont("Arial",10)
        self.currentcell=self.start
                
    def Find(self,What="", LookIn=xlFormulas, LookAt= xlWhole, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False):
        for cell in self.Cells:
            if cell.Value == What:
                return cell
            
    def Offset(self, offset_row, offset_col):
        for cell in self.Cells:
            cell.offset(offset_row,offset_col)
        return self
    
    def Activate(self):
        for cell in self.Cells:
            cell.Activate()
            
    def get_rows(self):
        rowlist = []
        for rownumber in range(self.start[0],self.end[0]+1):
            rowlist.append(CRow(rownumber))
        return rowlist
    
    def set_rows(self,rowlist):
        pass
    
    def get_columns(self):
        collist = []
        for colnumber in range(self.start[1],self.end[1]+1):
            collist.append(CColumn(colnumber))
        return collist        
    
    def set_cells(self,rowlist):
        pass 
    
    def get_cells(self):
        cellist = []
        for colnumber in range(self.start[1],self.end[1]+1):
            for rownumber in range(self.start[0],self.end[0]+1):
                cellist.append(Cells(rownumber,colnumber,ws=self.ws))
        return cellist        
    
    def set_columns(self,rowlist):
        pass      
            
    Rows = property(get_rows, set_rows, doc='rows included in range')
    
    Columns = property(get_columns, set_columns, doc='rows included in range')
      
    Cells = property(get_cells, set_cells, doc='rows included in range')
        
    def __iter__(self):
    #returning __iter__ object
        self.currentcell = self.start
        return self
    
    def __next__(self):
        nextcell = Cells(self.currentcell[0],self.currentcell[1])
        self.currentcell[1]+=1
        if self.currentcell[1]>self.end[1]:
            self.currentcell[0]+=1
            if self.currentcell[0] > self.end[0]:
                raise StopIteration
        return nextcell
            
class CRectangles(object):
    def __init__(self):
        self.rlist = []
        self.Count=0
        
    def add(self,rectangle):
        self.rlist.append(rectangle)
        self.Count+=1
        
    def delete(self,i):
        self.rlist.remove(i)
        self.Count-=1
        

        
    #def __init__(self,rowrange,colrange):
    #    self.Rows=list()
    #    for i in range(rowrange[0],rowrange[1]):
    #        self.Rows.append(CRow(i))
    #    self.Columns=list()
    #    for i in range(colrange[0],colrange[1]):
    #        self.Columns.append(CRow(i))
    
class CRectangle(object):
    
    def __init__(self,row=0,col=0,i=0,onaction=""):
        self.OnAction = onaction
        self.TopLeftCell = CCell("")
        self.TopLeftCell.Row = row
        self.TopLeftCell.Column = col
        self.index = i
        pass
    
    def Delete(self):
        super().delete(self.index)
        pass
    
class CSelection:
    def __init__(self,cell):
        #self.EntireRow = CEntireRow(cell.Row)
        self.EntireColumn = CEntireColumn(cell.Column)
        self.Characters = ""
        self.selectedRows = []
        self.Cells = []
        
    def EntireRow(self):
        self.selectedRows = []
        for row in ActiveSheet.table.multiplerowlist:
            self.selectedRows.append(row+1)
        if self.selectedRows==[]:
            self.selectedRows=[ActiveSheet.table.getSelectedRow()+1]
        return self.selectedRows
    
    def Rows(self):
        selectedrows = self.EntireRow()
        selectedcrows = []
        for row in selectedrows:
            selectedcrows.append(CRow(row))
        return selectedcrows

class CRow:
    def __init__(self,rownumber):
        self.Row = rownumber
        self.EntireRow = CEntireRow(rownumber)
        self.Hidden_value = False
        
    def Select(self):
        ActiveSheet.table.gotoCell(self.Row-1,0)
        return    
        
        
    def set_Hidden(self, newval):
        self.Hidden_value = newval
        if newval==True:
            ActiveSheet.table.model.hiderowslist.append(self.Row-1)
        else:
            ActiveSheet.table.model.hiderowslist.remove(self.Row-1)
    
    def get_Hidden(self):
        return self.Row-1 in ActiveSheet.table.model.hiderowslist
        
    Hidden = property(get_Hidden, set_Hidden, doc='Hiddenvalue of CRow')
        
        

        
class CEntireRow:
    def __init__(self,rownumber):
        self.Rownumber = rownumber
        self.Hidden_value = False
        
    def set_Hidden(self, newval):
        self.Hidden_value = newval
        if newval==True:
            if not self.Rownumber-1 in ActiveSheet.table.model.hiderowslist:
                ActiveSheet.table.model.hiderowslist.append(self.Rownumber-1)
                ActiveSheet.Redraw_table()
        else:
            if self.Rownumber-1 in ActiveSheet.table.model.hiderowslist:
                ActiveSheet.table.model.hiderowslist.remove(self.Rownumber-1)
                ActiveSheet.Redraw_table()
    
    def get_Hidden(self):
        return self.Rownumber-1 in ActiveSheet.table.model.hiderowslist
        
    Hidden = property(get_Hidden, set_Hidden, doc='Hiddenvalue of CRow')        
        

        
class CColumn:
    def __init__(self,colnumber):
        self.Column=colnumber
        self.EntireColumn = CEntireColumn(colnumber)
        self.columnwidth = 5
        self.Hidden = False
        
        
    def get_columnwidth(self):
        return self.columnwidth
    
    def set_columnwidth(self, value):
        self.columnwidth = value
        ActiveSheet.table.resizeColumn(self.Column-1,value)
        
        
    ColumnWidth = property(get_columnwidth, set_columnwidth, doc='Column Width')
        
class CEntireColumn:
    def __init__(self,colnumber):
        self.Columnnumber = colnumber
        self.Hidden = False
    
    
class CCell(str):
    def __new__(cls,value,row=-1,column=-1,tablemodel=None,parent=None,Sheet=None):
        obj=str.__new__(cls,value)
        obj.Orientation = 0
        obj.Row = row
        obj.Column = column
        obj.Formula = ""
        obj.tablemodel = tablemodel
        obj.CountLarge = 1
        obj.Parent = parent
        obj.Address = (obj.Row,obj.Column)
        obj.Comment = None
        obj.Font = CFont("Arial",10)
        obj.HorizontalAlignment = xlCenter
        if Sheet==None:
            obj.Sheet = ActiveSheet
        else:
            obj.Sheet = Sheet
        obj.Text = value
        obj.Value = value
        obj.EntireRow = CEntireRow(obj.Row)
        return obj
        
    def __str__(self):
        return str(self.get_value())
    
    def __repr__(self):
        return str(self.get_value())
    
    def get_value(self):
        if self.Row != -1:
            if self.tablemodel == None:
                self.tablemodel = ActiveSheet.tablemodel
            max_cols = self.tablemodel.getColumnCount()
            if self.Column < max_cols:
                value = self.tablemodel.getValueAt(self.Row-1,self.Column-1)
            else:
                value = ""
        return value # self.__value
    
    def set_row(self,row):
        if row > self.tablemodel.getRowCount():
            logging.debug("Set_row - Error - out of range: "+str(row))
            self.tablemodel.autoAddRows(numrows=row-self.tablemodel.getRowCount())
        self.Row = row
        self.Address = (self.Row,self.Column)            
        
    def set_column(self,column):
        self.Column=column
        self.Address = (self.Row,self.Column)
    
    def set_value(self, newval):
        if self.Sheet != None:
            if self.Row != -1:
                #print("Set_value",self.Row, self.Column,newval,self.Sheet.Name)
                if self.tablemodel == None:
                    self.tablemodel = ActiveSheet.tablemodel
                if self.Row <=self.tablemodel.getRowCount() and self.Column <=self.tablemodel.getColumnCount():
                    curval = self.tablemodel.getValueAt(self.Row-1, self.Column-1)
                    if curval != newval:
                        self.tablemodel.setValueAt(newval, self.Row-1, self.Column-1)
                        #self.Sheet.setDataChanged()
                        if type(newval) != str:
                            Debug.Print("Type not str",newval)
                        if Application.EnableEvents:
                            #print("Workbook contents changed:",)
                            ActiveSheet.EventWSchanged(self)
                                #M20.Global_Worksheet_Change(self)
                
    def set_tablemodel(self,tablemodel):
        self.tablemodel = tablemodel
        
    def set_sheet(self,sheet):
        self.Sheet=sheet
    
    def set_parent(self,parent):
        self.Parent = parent
        
    def check_if_empty_row(self):
        if self.tablemodel == None:
            self.tablemodel = ActiveSheet.tablemodel        
        cols = self.tablemodel.getColumnCount()
        r=self.Row-1
        for c in range(0,cols):
            #absr = self.get_AbsoluteRow(r)
            val = self.tablemodel.getValueAt(r,c)
            if val != None and val != '':
                return False
        return True
    
    def Offset(self, offset_row, offset_col):
        self.Row    = self.Row + offset_row
        self.Column = self.Column + offset_col
        ActiveSheet.table.gotoCell(self.Row-1,self.Column-1)
        return ActiveCell()
    
    def Select(self):
        ActiveSheet.table.gotoCell(self.Row-1,self.Column-1)
        ActiveSheet.EventWSselected(self)
        return
    
    def AutoFilter(self):
        print("Autofilter")
        
    def Activate(self):
        self.Parent.table.gotoCell(self.Row,self.Column)
        
    def Left(self):
        x1,y1,x2,y2 = ActiveSheet.table.getCellCoords(self.Row-1,self.Column-1)
        return x1
    
    def Top(self):
        x1,y1,x2,y2 = ActiveSheet.table.getCellCoords(self.Row-1,self.Column-1)
        return y1
    
    def Width(self):
        x1,y1,x2,y2 = ActiveSheet.table.getCellCoords(self.Row-1,self.Column-1)
        return x2-x1
    
    def Height(self):
        x1,y1,x2,y2 = ActiveSheet.table.getCellCoords(self.Row-1,self.Column-1)
        return y2-y1
    
    def ClearContents(self):
        self.set_value("")
    
    Value = property(get_value, set_value, doc='value of CCell')
    Text = property(get_value, set_value, doc='value of CCell')
    
class CCellDict():
    def __init__ (self,ws=None):
        #data = {}
        self.ws = ws
        
    def __getitem__(self, k):
        #print("Getitem",k)
        return Cells(k[0],k[1],ws=self.ws)
        
    def __setitem__(self,k,value):
        ccell = Cells(k[0],k[1],ws=self.ws)
        #print("Setitem",k, value,ccell.Sheet.Name)
        ccell.set_value(value)

        
class CWorksheetFunction:
    def __init__(self):
        pass
    def RoundUp(v1,v2):
        #print("RoundUp")
        if v2 == 0:
            if v1 == int(v1):
                return v1
            else:
                return int(v1 + 1)
        else:
            return "Error"
        
class CApplication:
    def __init__(self):
        self.StatusBar = ""
        self.EnableEvents = True
        self.ScreenUpdating = True
        self.Top = 0
        self.Left = 0
        self.Width = 1000 #*HL
        self.Height = 500 #*HL
        self.Version = "15"
        self.WindowState = 0
        self.caller=0
        self.canvas_leftclickcmd=None
        self.LanguageSettings = CLanguageSettings()
        self.hWnd = 0
        
    def set_canvas_leftclickcmd(self,cmd):
        self.canvas_leftclickcmd=cmd
        
        
    def OnTime(self,time,cmd):
        #print("Application OnTime:",time,cmd)
        PG.global_controller.after(time,cmd)
        return
    
    def RoundUp(v1,v2):
        #print("RoundUp")
        if v2 == 0:
            if v1 == int(v1):
                return v1
            else:
                return int(v1 + 1)
        else:
            return "Error"
        

    def GetSaveAsFilename(self,InitialFileName="", fileFilter="", Title="" ):
        filefilter_list = fileFilter.split(",")
        filepath = tk.filedialog.asksaveasfilename(filetypes=[filefilter_list],defaultextension=".MLL_pgf",title=Title,initialfile=InitialFileName)
        return filepath
    
    def GetOpenFilename(self,InitialFileName="", fileFilter="", Title="" ):
        filefilter_list = fileFilter.split(",")
        filepath = tk.filedialog.askopenfilename(filetypes=[filefilter_list],defaultextension=".MLL_pgf",title=Title,initialfile=InitialFileName)
        return filepath
    
    def setActiveWorkbook(self,workbookName):
        global ThisWorkbook,ActiveWorkbook
        for wb in Workbooks:
            if wb.Name == workbookName:
                set_activeworkbook(wb)
                break
    
    def Quit(self):
        pass
    
locale2msoid={"de":msoLanguageIDGerman,
              "en":msoLanguageIDEnglishUK,
              "nl":msoLanguageIDDutch,
              "fr":msoLanguageIDFrench,
              "it":msoLanguageIDItalian,
              "es":msoLanguageIDSpanish,
              "da":msoLanguageIDDanish
              }
msoid_list = ("de","en","nl","fr","it","es","da")

class CLanguageSettings:
    def __init__(self):
        id = -1
        
    def LanguageID(self,id):
        if id == msoLanguageIDUI:
            lngconfstr = PG.global_controller.getConfigData("language")
            if lngconfstr == "":
                lngconfnum=0
            else:
                lngconfnum= int(lngconfstr)
            if lngconfnum==0:
                loc = locale.getdefaultlocale()
                locstr=loc[0]
                if locstr != None:
                    locstr=loc[0][:2]
                else:
                    locstr="de"
                msoid = locale2msoid.get(locstr,msoLanguageIDEnglishUK)
                return msoid
            else:
                msoid = locale2msoid.get(msoid_list[lngconfnum-1],msoLanguageIDEnglishUK)
                return msoid
        else:
            return msoLanguageIDEnglishUK
        
class CFont:
    def __init__(self,name,size):
        self.Name = name
        self.Size = size
        
class CActiveWindow:
    def __init__(self):
        Zoom = 100
        ScrollColumn = 1
        self.SelectedSheets={}
        self.SelectedSheets["Count"]=1        
        
class SoundLines:
    def __init__(self):
        self.dict = {}
        self.Count = 0
        self.keys = []
    
    def Exists(self,Channel:int):
        pass
    
    def Add(Channel, Pin_playerClass):
        pass
    
class CButton:
    def __init__(self,name):
        self.Name=name
        self.AlternativeText = ""
        self.TextFrame2 = ""
        self.Fill = (0,0,0)

        
class CControl:
    def __init__(self,value):
        self.Value=value

        
def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'


# global variables

ActiveWorkbook = None # :CWorkbook
 
ActiveSheet = None #:CWorksheet

#WorksheetFunction = CWorksheetFunction()

Application = CApplication() #:CApplication

CellDict = CCellDict() # :CCellDict

Selection = CSelection(CCell(""))

Workbooks =[]

ActiveWindow = CActiveWindow()

#Date = "1.1.2022"
#Time = "12:00"


Now = 0

