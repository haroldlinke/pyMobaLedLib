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
import re
import json

from tkintertable import TableCanvas,CTShape
import tkinter as tk
from tkinter import ttk
from ExcelAPI.XLC_Excel_Consts import *
from vb2py.vbconstants import *
from vb2py.vbfunctions import *
import time
import datetime

from pathlib import Path

import proggen.M20_PageEvents_a_Functions as M20
import subprocess
import pickle
import proggen.F00_mainbuttons as F00
import proggen.M02_Public as M02
import proggen.M18_Save_Load as M18
import proggen.M25_Columns as M25
import proggen.M37_Inst_Libraries as M37
import proggen.M39_Simulator as M39
import pattgen.DieseArbeitsmappe
import pattgen.M02_Main

try:
    keyboard_Module_imported = False
    import keyboard
    keyboard_Module_imported = True
    logging.debug("Keyboard Module imported")
except:
    logging.debug("Keyboard Module not imported")
    
    #import proggen.M25_Columns as M25
#import proggen.M02_global_variables as M02
#import proggen.M28_divers as M28

pyProgfile_dir = "\\LEDs_AutoProg\\pyProg_Generator_MobaLedLib"

shift_key = False

guifactor  = 1.55

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
    global_controller.update()

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
    Selection = CSelection(ActiveSheet.Cells(row,col),ws=ActiveSheet) #*HL
    return ActiveSheet.Cells(row,col) #*HL

def activate_workbook(workbookname):
    #find workbook
    for workbook in Workbooks:
        if workbook.Name==workbookname:
            set_activeworkbook(workbook)
            return
    return

def set_activeworkbook(p_workbook):
    global ActiveSheet,ActiveWorkbook,Selection,Worksheets
    Debug.Print("Set_activeworkbook:", p_workbook.Name)
    aw_Name="---"
    as_Name="---"
    naw_Name="---"
    nas_Name="---"
    if ActiveWorkbook!=p_workbook:
        
        if ActiveWorkbook:
            aw_Name=ActiveWorkbook.Name
        if ActiveSheet:
            as_Name=ActiveSheet.Name
        if p_workbook:
            naw_Name=p_workbook.Name
            if p_workbook.ActiveSheet:
                nas_Name=p_workbook.ActiveSheet.Name
        #print("Set_activeworkbook:",aw_Name,as_Name,"->",naw_Name, nas_Name)
        if ActiveWorkbook!= None:
            ActiveWorkbook.ActiveSheet = ActiveSheet # save active sheet of current workbook
            ActiveWorkbook.Selection = Selection # save selection in workbook
        ActiveWorkbook = Workbook = p_workbook
        if p_workbook.ActiveSheet == None:
            ActiveSheet = ActiveWorkbook.Sheets(p_workbook.start_sheet)
            p_workbook.ActiveSheet = ActiveSheet
        else:
            ActiveSheet = p_workbook.ActiveSheet
        #print("Set_activeworkbook:",p_workbook.Name, p_workbook.ActiveSheet.Name)
        global_controller = p_workbook.controller
        global_controller.activeworkbook = p_workbook
        if p_workbook.Selection == None:
            Selection = CSelection(None,ws=p_workbook.ActiveSheet)
        else:
            Selection = p_workbook.Selection
        Worksheets = p_workbook.sheets
        p_workbook.controller.bind("<<SheetChange>>",p_workbook.Evt_SheetChange)
        p_workbook.controller.bind("<<SheetSelectionChange>>",p_workbook.Evt_SheetSelectionChange)        
        
        p_workbook.ActiveSheet.Activate()


def create_workbook(frame=None, path=None,pyProgPath=None,workbookName=None,workbookFilename=None,sheetdict=None,start_sheet=None,p_global_controller=None):
    global ActiveSheet,ActiveWorkbook,global_controller
    if p_global_controller:
        global_controller = p_global_controller
    workbook = CWorkbook(frame=frame,path=path,pyProgPath=pyProgPath,workbookName=workbookName,workbookFilename=workbookFilename,sheetdict=sheetdict,start_sheet=start_sheet)
    set_activeworkbook(workbook)
    return workbook
    
def IsError(testval):
    return False

def Cells(row:int, column:int,ws=None):
    if ws == None:
        ws=ActiveSheet
    xlrange = ws.Cells(row,column)
    return xlrange

def Range(cell1=None,cell2=None,ws=None):
    if ws==None:
        ws=ActiveSheet
    if cell1==None:
        return CRange() # dummy for type definition only
    if type(cell1) == str:
        if ":" in cell1: # range as string a:b
            cellsplit = cell1.split(":")
            return Range(cellsplit[0],cellsplit[1])
        named_cell1 = ws.find_RangeName(cell1)
        if cell2 != None:
            if type(cell2) == str:
                named_cell2 = ws.find_RangeName(cell2)
                return CRange(named_cell1,named_cell2,ws=ActiveSheet)
            else:
                return CRange(named_cell1,cell2,ws=ActiveSheet)
        else:
            return CRange(named_cell1,named_cell1,ws=ActiveSheet)
    else:
        if cell2==None:
            cell2=cell1
        return CRange(cell1,cell2,ws=ActiveSheet)

def Sheets(sheetname):
    return ActiveWorkbook.Sheets(sheetname)

def Rows(row=None,ws=None):
    if ws==None:
        ws=ActiveSheet
    if row==None:
        return CRange((1,1),(ws.getLastUsedRow(),1),ws=ws,parent=None,parenttype="Rows")
    else:
        if type(row)==str:
            rowlist=row.split(":")
            return CRange((int(rowlist[0]),1),(int(rowlist[1]),1),ws=ws,parent=None,parenttype="Rows")
        else:
            return CRange((row,1),(row,1),ws=ws,parent=None,parenttype="Rows")
    
    #if ws == None:
    #    ws=ActiveSheet    
    #if type(row)==str:
    #    rows=[]
    #    rowlist=row.split(":")
    #    for row1 in range(int(rowlist[0]),int(rowlist[1])+1):
    #        return CRow(row1)
    #else:
    #    return CRow(row)
        #sheet = ActiveSheet
        #return sheet.MaxRange.Rows[row]
   
def Columns(col:int):
    ws = ActiveSheet
    lastusedrow=ws.LastUsedRow
    startcell=CRange(1,col)
    endcell  =CRange(lastusedrow,col)
    return CRange(startcell,endcell)

def IsEmpty(obj):
    if len(obj)==0:
        return True
    else:
        return False

def val(value):
    valtype=type(value)
    if valtype is CRange:
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
                try:
                    return int(value)
                except:
                    return int(float(value))
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
        return "{0:2d}".format(int(value))
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
    global_controller.set_statusmessage(message)
    global_controller.update()

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
    
    if keyboard_Module_imported:
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
        return False
    else:
        return False


def GetCursorPos():
    pass

def SetCursorPos(x,y):
    pass

def DoEvents():
    #ActiveSheet.table.redraw()
    global_controller.update()

class Worksheet(object):
    """Placeholder for Workheettype"""
    def __init__(self):
        self.Name = "Dummy"

class CWorkbook(object):
    def __init__(self, frame=None,path=None,pyProgPath=None,workbookName=None, workbookFilename=None, sheetdict=None,init_workbook=None,open_workbook=None,start_sheet=None,controller=None):
        global Workbooks,pyProgfile_dir,Worksheets
        # Row and Columns are 0 based and not 1 based as in Excel
        if controller==None:
            self.controller = global_controller
        else:
            self.controller = controller

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
            self.oldTabName=""
            self.ActiveSheet = None

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
            self.Selection = None
            self.tabid    = 0
            self.Eventdict = sheetdict.get("Events",None)
            for sheetname in self.sheetdict.keys():
                if sheetname != "Events":
                    self.add_sheet(sheetname)
                """
                tabframe = ttk.Frame(self.container,relief="ridge", borderwidth=1)
                act_worksheet = self.new_sheet(sheetname,tabframe)
                tabframe.sheetname = sheetname
                tabframe.sheet = act_worksheet
                self.sheets.append(act_worksheet)
                self.container.add(tabframe, text=sheetname)
                self.tabframedict[sheetname]=act_worksheet
                if not self.showws and not PG.global_controller.show_hiddentables:
                    act_worksheet.Visible(False)
                    #self.container.tab(tabframe,state="hidden")
                self.tabid += 1
                """
            self.container.bind("<<NotebookTabChanged>>",self.TabChanged)
               
        else:
            self.Path = path
            self.tablemodel= None
            self.sheets = None
        self.start_sheet=start_sheet
        
        set_activeworkbook(self)
        self.InitWorkbookFunction=None
        Worksheets = self.sheets
        self.open()
        
    def init_workbook(self):
        set_activeworkbook(self)
        if self.InitWorkbookFunction:
            self.InitWorkbookFunction(self)
        
        #add controls to sheet    
        for sheet in self.sheets:
            sheetname_prop = self.sheetdict.get(sheet.Name)
            controls_dict = sheetname_prop.get("Controls",None)
            if controls_dict:
                sheet.add_controls(controls_dict)
            sheet.table.redraw()
        
        self.controller.bind("<<SheetChange>>",self.Evt_SheetChange)
        self.controller.bind("<<SheetSelectionChange>>",self.Evt_SheetSelectionChange)
        self.controller.bind("<<SheetReturnKey>>",self.Evt_SheetReturnKey)
                    
        self.activate_sheet(self.start_sheet)

        #if self.Name != "PatternWorkbook":
        #    F00.workbook_init(self)

    def open(self):
        pass
        #if self.Name != "PatternWorkbook":
        #    if M28.Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0) == 1: #               ' 04.04.22: Juergen Simulator
        #        M39.OpenSimulator()
        
    def delete_sheet(self,sheetname):
        #remove sheet from all lists:
           
        #self.sheets.append(act_worksheet)
        #self.container.add(tabframe, text=sheetname)
        #self.tabframedict[sheetname]=act_worksheet
        logging.debug("Error: Delete sheet not implemented!!")
        return
        
                
    def add_sheet(self,sheetname,from_sheet=None,After=None):
        tabframe = ttk.Frame(self.container,relief="ridge", borderwidth=1)
        act_worksheet = self.new_sheet(sheetname,tabframe,from_sheet=from_sheet)
        tabframe.sheetname = sheetname
        tabframe.sheet = act_worksheet
        self.sheets.append(act_worksheet)
        self.container.add(tabframe, text=sheetname)
        self.tabframedict[sheetname]=act_worksheet
        
        copyfrom_sheet=self.Sheets(from_sheet)
        
        if copyfrom_sheet:
            act_worksheet.wscalculation_callback = copyfrom_sheet.wscalculation_callback
            act_worksheet.wschanged_callback = copyfrom_sheet.wschanged_callback
            act_worksheet.wsselected_callback = copyfrom_sheet.wsselected_callback
            
            sheetname_prop = self.sheetdict.get(copyfrom_sheet.Name)
            controls_dict = sheetname_prop.get("Controls",None)
            if controls_dict:
                act_worksheet.add_controls(controls_dict)
            act_worksheet.table.redraw()
        
        if not self.showws and not self.controller.show_hiddentables:
            act_worksheet.Visible(False)
            #self.container.tab(tabframe,state="hidden")
        self.tabid += 1
           
    def new_sheet(self,sheetname,tabframe,from_sheet=None):
        if from_sheet==None:
            sheetname_prop = self.sheetdict.get(sheetname)
        else:
            sheetname_prop = self.sheetdict.get(from_sheet)
        sheettype = sheetname_prop.get("SheetType","")
        callback = sheettype in ["Datasheet","Libraries"]
        self.showws = sheettype in ["Datasheet","Config"]
        formating_dict = sheetname_prop.get("Formating",None)
        fieldnames = sheetname_prop.get("Fieldnames",None)
        if type(fieldnames) == str:
            fieldnames = fieldnames.split(";")
        act_worksheet = CWorksheet(sheetname,workbook=self, csv_filepathname=(Path(self.pyProgPath) / sheetname_prop["Filename"]),frame=tabframe,fieldnames=fieldnames,formating_dict=formating_dict,Sheettype=sheettype,callback=callback,tabid=self.tabid)
        return act_worksheet
    
    def activate_sheet(self,sheetname):
        sheet=self.Sheets(sheetname)
        self.container.select(sheet.Tabframe)
            
    def TabChanged(self,_event=None):
        newtab_name = self.container.select()
        if newtab_name != "":
            newtab = self.container.nametowidget(newtab_name)
            sheet_name = newtab.sheetname
            sheet = newtab.sheet
            if sheet:
                sheet.Activate()
                #print("Tabchanged - Sheet activated:",sheet_name)
            
            #newtab.tabselected()
        logging.debug("TabChanged %s - %s",self.oldTabName,newtab_name)        
        
    def Sheets(self,name):
        if self.sheets != None:
            if name == "<<LASTSHEET>>":
                return self.sheets[-1]
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
    
    def SetInitWorkbookFunction(self,func):
        self.InitWorkbookFunction=func
    
    def Activate(self):
        set_activeworkbook(self)
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
        
        
        # Write JSON file
        #with open(filename+".json", 'w', encoding='utf8') as outfile:
        #    json.dump(workbookdata, outfile, ensure_ascii=False, indent=4)        
        
        fd = open(filename,'wb')
        try:
            pickle.dump(workbookdata,fd)
            fd.close()
        except BaseException as e:
            logging.debug(e)            
            logging.debug("Save Workbook Error: "+filename)            
        return
    
    def LoadWorkbook(self,filename):
        fd=open(filename,'rb')
        try:
            workbookdata = pickle.load(fd)
            for sheet in self.sheets:
                data = workbookdata.get(sheet.Name,{})
                if data !={}:
                    sheet.setData(data)
                    sheet.init_data()
                    sheet.tablemodel.resetDataChanged()
        except BaseException as e:
            logging.debug(e)            
            logging.debug("Load Workbook Error"+filename)
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
    
    # ------------------------------------------
    # VBA events
    # ------------------------------------------
    def Noneproc(*args):
        pass
    
    def Call_EventProc(self,eventname):
        if self.Eventdict:
            eventproc = self.Eventdict.get(eventname,None)
            if eventproc:
                return eventproc
            else:
                return self.Noneproc
        else:
            return self.Noneproc
    
    def Evt_Workbook_Open(self):
        # occurs when the workbook is opened
        if Application.EnableEvents:
            self.Call_EventProc("Workbook_Open")()
    
    def Evt_Workbook_BeforeClose(self, event):
        if Application.EnableEvents:
            self.Call_EventProc("Workbook_BeforeClose")(Cancel)
            return Cancel
    
    def Evt_SheetTableUpdate(self,sheet,target):
        # Occurs after the sheet table has been updated.
        if Application.EnableEvents:
            self.Call_EventProc("SheetTableUpdate")(sheet,target)
    
    def Evt_SheetCalculate(self, sheet, target):
        # Occurs after any worksheet is recalculated or after any changed data is plotted on a chart.
        if Application.EnableEvents:
            Application.EnableEvents=False
            self.Call_EventProc("SheetCalculate")(sheet, target)
            Application.EnableEvents=True
    
    def Evt_SheetBeforeDoubleClick(self, sheet,target, cancel):
        # Occurs when any worksheet is double-clicked, before the default double-click action.
        if Application.EnableEvents:
            self.Call_EventProc("SheetBeforeDoubleClick")(sheet, target, cancel)
    
    def Evt_SheetChange(self, event):
        if Application.EnableEvents:
            # Occurs when cells in any worksheet are changed by the user or by an external link.
            row=event.widget.event_row+1
            col=event.widget.event_col+1
            sheet=event.widget.worksheet
            target=CRange(row,col)
            #pattgen.M02_Main.Global_On_Enter_Proc()
            self.Evt_SheetCalculate(sheet,target)
            self.Call_EventProc("SheetChange")(target)
            sheet.Redraw_table()
        
    def Evt_SheetSelectionChange(self,event):
        if Application.EnableEvents:
            # Occurs when cells in any worksheet are changed by the user or by an external link.
            Application.EnableEvents=False
            row=event.widget.event_row+1
            col=event.widget.event_col+1
            sheet=event.widget.worksheet
            target=CRange(row,col)
            #print("Evt_SheetSelectionChange: <<SheetSelectionChange>> "+str(row),","+str(col))
            self.Call_EventProc("SheetSelectionChange")(target)
            Application.EnableEvents=True
        
    def Evt_SheetActivate(self, event):
        # Occurs when cells in any worksheet are changed by the user or by an external link.
        if Application.EnableEvents:
            self.Call_EventProc("SheetActivate")()
        
    def Evt_SheetDeactivate(self, event):
        # Occurs when cells in any worksheet are changed by the user or by an external link.
        if Application.EnableEvents:
            self.Call_EventProc("SheetDectivate")()                
    
    def Evt_NewSheet(self, event):
        # Occurs when a new sheet is created in the workbook.
        if Application.EnableEvents:
            self.Call_EventProc("NewSheet")(sheet)
            
    def Evt_SheetReturnKey(self, event):
        # Occurs when a new sheet is created in the workbook.
        if Application.EnableEvents:
            self.Call_EventProc("SheetReturnKey")()
    
    def Evt_SheetOpen(self, event):
        # Occurs when a new sheet is created in the workbook.
        if Application.EnableEvents:
            self.Call_EventProc("SheetOpen")()
            
    def Synch_Evt_SheetSelectionChange(self,widget):
        if Application.EnableEvents:
            Application.EnableEvents=False
            #print("SynchEvt__SheetSelectionChange: <<SheetSelectionChange>>")
            # Occurs when cells in any worksheet are changed by the user or by an external link.
            row=widget.event_row+1
            col=widget.event_col+1
            sheet=widget.worksheet
            target=CRange(row,col)
            self.Call_EventProc("SheetSelectionChange")(target)
            Application.EnableEvents=True
            
    def Synch_Evt_SheetChange(self, widget):
        if Application.EnableEvents:
            # Occurs when cells in any worksheet are changed by the user or by an external link.
            row=widget.event_row+1
            col=widget.event_col+1
            sheet=widget.worksheet
            target=CRange(row,col,ws=sheet)
            #pattgen.M02_Main.Global_On_Enter_Proc()
            self.Evt_SheetCalculate(sheet,target)
            Debug.Print("Synch_Evt_SheetChange: <<SheetChange>> "+str(row),","+str(col))
            self.Call_EventProc("SheetChange")(target)
            sheet.Redraw_table()
            
    def Synch_Evt_SheetReturnKey(self):
        # Occurs when a new sheet is created in the workbook.
        if Application.EnableEvents:
            self.Call_EventProc("SheetReturnKey")()        
    
class CCellsFind(object):
    def __init__(self,ws=None):
        self.sheet=ws
    
    def Find(self,What="", After=None, LookIn=xlFormulas, LookAt= xlWhole, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False):
       
        cells=self.sheet.Cells()
        if After!=None:
            cells.startrow=After.Row
            cells.startcol=After.Column
                
        for cell in cells:
            cell_val=str(cell.Value)
            if cell_val == What:
                return cell
        return None

class CWorksheet(object):
    
    def __init__(self,Name,tablemodel=None,workbook=None,csv_filepathname=None,frame=None,fieldnames=None,formating_dict=None,Sheettype="",callback=False,tabid=0):
        
        sheetdict_popmenu = {"DCC":
                             { "LED blinken Ein/Aus":self.LED_flash,
                               "LED nacheinander blinken Ein/Aus":self.LED_flash_seq
                             }
                            }

        screen_width = 1920
        screen_height = 1080       
        self.controller = workbook.controller
        self.rightclickactiondict = sheetdict_popmenu.get(Name,{})
        self.width = screen_width-120
        self.height = screen_height-350
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
        self.wsRowdict = {}
        self.EnableCalculation=True
        self.tabid = tabid
        if tablemodel:
            self.tablemodel = tablemodel
            self.table = TableCanvas(frame, tablename=Name, model=tablemodel,width=self.width,height=self.height,scrollregion=(0,0,self.width,self.height),rightclickactions=self.rightclickactiondict,worksheet=self)
        else:
            if csv_filepathname:
                #self.tablemodel = TableModel()
                self.table = TableCanvas(frame, tablename=Name, model=None,width=self.width,height=self.height,scrollregion=(0,0,self.width,self.height),rightclickactions=self.rightclickactiondict,worksheet=self)
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
        #*HL dummy for testing
        self.CellsFind=CCellsFind(ws=self)
        self.Controls = []
        self.Controls_Dict = {}
        self.persistent_controls_dict = {}
        self.RangeDict = CRangeDict()
        
    def init_data(self):
        if self.wsInitDataFunction:
            self.wsInitDataFunction(self)
        #F00.worksheet_init(self)
        self.DataChanged=False
        
    def update_table_properties(self):
        self.LastUsedRow_val = self.tablemodel.getLastUsedRow()+1
        self.LastUsedColumn_val = self.tablemodel.getColumnCount()
        self.UsedRange_val = CRange((1,1) , (self.LastUsedRow_val,self.LastUsedColumn_val),ws=self)
        self.MaxRange_val  = CRange((1,1) , (self.LastUsedRow_val,self.LastUsedColumn_val),ws=self)
        #self.Rectangles = CRectangles()
        self.AutoFilterMode = False
        self.searchcache = {}
        self.Shapes = CShapeList(self)
        self.CellDict = CCellDict(ws=self)
        self.End_val = self.LastUsedColumn_val
        
    def Calculate(self):
        self.EventWScalculate()
        
    def Delete(self):
        self.Workbook.delete_sheet(self.Name)
        
    def add_controls(self,controls_dict):
        for control_key in controls_dict.keys():
            form_def = controls_dict[control_key]
            Left = form_def.get("Left",None)
            Top = form_def.get("Top",None)
            Row=form_def.get("Row",None)
            Col=form_def.get("Col",None)
            Width = form_def["Width"]
            Height = form_def["Height"]
            Name = form_def["Name"]
            controls_def= form_def
            self.Shapes.AddShape(msoOLEControlObject, Left, Top, Width, Height, Row=Row, Col=Col, Fill=0, text="", name=Name,control_dict=controls_def)
            
    def AddControl(self,control):
        self.Controls.append(control)
        self.Controls_Dict[control.Name]=control

    def set_control_val(self, control,value,disable=False):
        if value != None:
            if hasattr(control,"TKVar"):
                variable = control.TKVar
                if variable:
                    if disable:
                        variable.config(state="normal") # we need to set the state to "normal" to be able to set values
                    try:
                        var_class = variable.winfo_class()
                    except: #limit_var has no winfo_class() function
                        var_class = "Limit_Var"                
                    if var_class == "TCombobox":
                        # value of combobox needs to be translated into a generic value
                        if isinstance(value,int):
                            current_index = value
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
            
    def get_control_val(self, control):
        value = ""
        variable = control.TKVar
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
        
    def SavePersistentControls(self):
        for control in self.Controls:
            if control.Persistent:
                self.persistent_controls_dict[control.Name]=self.get_control_val(control)
    
    def SetPersistentControls(self):
        for control in self.Controls:
            if control.Persistent:
                self.set_control_val(control,self.persistent_controls_dict[control.Name])
        
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
        global_controller.blinking_on_off(lednum,ledcount)
            
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
            global_controller.blinking_on_off(lednum,ledcount,seq=True)    
        
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
            Application.caller = value1[0]
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
    
    LastUsedColumn = property(get_LastUsedColumn, set_LastUsedColumn, doc='Last used column')
    End = property(get_LastUsedColumn, set_LastUsedColumn, doc='Last used column')

    def get_UsedRange(self):
        self.UsedRange_val = CRange((0,0) , (self.get_LastUsedRow(),self.LastUsedColumn_val),ws=self)
        return self.UsedRange_val
    
    def set_UsedRange(self,value):
        self.UsedRange_val = value
               
    UsedRange = property(get_UsedRange, set_UsedRange, doc='used range')
    MaxRange  = property(get_UsedRange, set_UsedRange, doc='used range')
    
    def get_Shape(self,shapename):
        for Shape in self.Shapes:
            if Shape.Name == shapename:
                return Shape
        return None
           
    def Cells(self,row=None, col=None):
        if row==None and col==None:
            return self.get_UsedRange()
        return CRange(row,col,ws=self)
    
    def Rows(self,row):
        try:
            return self.wsRowdict[row]
        except:
            self.wsRowdict[row] = CRow(row)
            return self.wsRowdict[row]
    
    def get_cellvalue_direct(self,sheet,row,col):
        tablemodel = sheet.tablemodel
        max_cols = tablemodel.getColumnCount()
        if col <= max_cols:
            value = tablemodel.getValueAt(row-1,col-1)
        else:
            value = ""
        return value
    
    def find_RangeName(self,rangestr,ws=None):
        # returns CRange with row and column of the Named_range
        if ws==None:
            ws  = ActiveSheet
        #check for Cell Names eg. "E5", "AB12"
        pattern=re.compile("([A-Z]+)(\d+)")
        m = re.match(pattern,rangestr)
        if m!=None:
            #print(rangestr,"->",m.groups())
            m_list = m.groups(0)
            col_str = m_list[0]
            named_range_col = 0
            for char in col_str:
                index = ord(char)-ord("A")+1
                named_range_col = named_range_col*26+index
            row_str = m_list[1]
            named_range_row = int(row_str)
            resultcell = CRange(self.Cells(named_range_row,named_range_col))
            return resultcell
        
        LSh = ws.Workbook.Sheets("Named_Ranges")
        _row = LSh.find_in_col_ret_row(rangestr,1,cache=True)        
        if _row != None:
            named_range_sheetname= self.get_cellvalue_direct(LSh,_row,2)
            named_range_sheet = ws.Workbook.Sheets(named_range_sheetname)
            named_range_col = int(self.get_cellvalue_direct(LSh,_row,3))
            named_range_row = int(self.get_cellvalue_direct(LSh,_row,4))
            resultcell = CRange(self.Cells(named_range_row,named_range_col),value=self.get_cellvalue_direct(ws, named_range_row,named_range_col))
            return resultcell
        else:
            return None

    def Range(self,cell1,cell2=None,ws=None):
        if ws==None:
            ws=self        
        return CRange(cell1,cell2,ws=ws)
        
    def Range_set(self,rangestr,value):
        oldflag = Application.EnableEvents
        Application.EnableEvents=False
        named_cell = self.find_RangeName(rangestr)
        named_cell.Value = value
        Application.EnableEvents = oldflag
    
    def Unprotect(self,Password=""):
        self.ProtectContents = False
        
    def Protect(self, DrawingObjects=True, Contents=True, Scenarios=True, AllowFormattingCells=True, AllowInsertingHyperlinks=True):
        self.ProtectContents = True
        return
        
    def Columns(col:int):
        #print("Columns",col)
        return CColumn(col)
    
    def EnableDisableAllButtons(self,value):
        return
    
    def SetChangedCallback(self,callback):
        self.wschanged_callback = callback
        
    def SetSelectedCallback(self,callback):
        self.wsselected_callback = callback
        
    def SetCalculationCallback(self,callback):
        self.wscalculation_callback = callback
        
    def SetInitDataFunction(self,func):
        self.wsInitDataFunction = func
        
    def EventWScalculate(self):
        if self.wscalculation_callback:
            self.wscalculation_callback(self)
       
    def EventWSchanged(self, changedcell):
        if self.wschanged_callback and Application.EnableEvents:
            if Application.EnableCalculation and self.EnableCalculation and Application.Calculation == xlCalculationAutomatic:
                Application.EnableEvents=False
                self.wsselected_callback(changedcell)
                self.wscalculation_callback(self,cell=changedcell) # Calc_Worksheet(self)
                self.wschanged_callback(changedcell)
                Application.EnableEvents=True
                self.Redraw_table()
            
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
        global ActiveSheet,ActiveWorkbook
        #print("Worksheet.Activate",self.Workbook.Name, self.Name)
        set_activeworkbook(self.Workbook)
        ActiveSheet = self
        ActiveWorkbook = self.Workbook
        self.Workbook.ActiveSheet=self
#        self.Workbook.ActiveSheet =self
        self.table.do_bindings()
        if self.Workbook.Name=="ProgGenerator":
            Port=Cells(M02.SH_VARS_ROW, M25.COMPort_COL)
            if F00.port_is_available(Port):    
                self.controller.setConfigData("serportname",Port)
        return

    def Copy(self,SheetName=None,After=None):
        self.Workbook.add_sheet(SheetName,from_sheet=self.Name,After=After)
        
        pass
    
    def do_bindings(self):
        #print("do bindings")
        self.table.do_bindings()
        
    def remove_bindings(self):
        #print("remove bindings")
        self.table.remove_bindings()
    
    def Select(self):
        global ActiveSheet,Selection
        ActiveSheet = self
        #print("Worksheet.Select",self.Workbook.Name, self.Name)
        self.Workbook.ActiveSheet = self
        Selection=self.Workbook.Selection
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
        self.SavePersistentControls()
        data["Persistent_Controls"]=self.persistent_controls_dict
        return data
    
    def setData(self,data):
        self.tablemodel.createEmptyModel()
        self.tablemodel.setupModel(data)
        self.persistent_controls_dict=data.get("Persistent_Controls",{})
        self.SetPersistentControls()
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
        self.controller.update()
        
    def check_Data_Changed(self):
        return self.DataChanged or self.tablemodel.checkDataChanged()
    
    def add_new_attr(self,attr):
        setattr(self,attr,attr)
        
    def add_UI_object(self,ui_object_name,UI_object):
        setattr(self,ui_object_name, UI_object)
        
    def get_selection(self):
        
        return 
    
    def set_selection(self, value):
        ActiveSheet.get_selection().Value=value
    
    Selection = property(get_selection, set_selection, doc='Selection')             
 
class CFreeForm(object):
    def __init__(self, EditingType, X1, Y1):
        self.nodelist=[(X1,Y1)]
        self.EditingType=EditingType
        self.Left=X1
        self.Top=Y1
        self.SegmentType = None
        
    def AddNodes(self,SegmentType, EditingType, X2, Y2, *args):
        self.SegmentType = SegmentType
        self.EditingType = EditingType
        point=(X2,Y2)
        self.nodelist.append(point)
        get_xval=True
        for val in args:
            if get_xval:
                x=val
                get_xval=False
            else:
                y=val
                point=(x,y)
                self.nodelist.append(point)
                get_xval=True
        
    def ConvertToShape(self):
        name="Freeform"
        shape=CShape(name, msoFreeform, self.Left, self.Top, None, None,Fillcolor=-1,nodelist=self.nodelist,zorder=0,segmenttype=self.SegmentType,editingtype=self.EditingType)
        return shape
        
class CShapeList(object):
    def __init__(self,ws=None):
        if ws==None:
            ws=ActiveSheet
        self.ws = ws
        self.ws.tablemodel.shapelist = list()
        self.currentshape=None
        self.currentidx = 0
       
    def convTShape2CShape(self,tshape):
        cshape=CShape(tshape.Name, tshape.Shapetype, tshape.Left, tshape.Top, tshape.Width, tshape.Height, tshape.Fillcolor, tshape.Text, Row=tshape.Row, Col=tshape.Col, AlternativeText=tshape.AlternativeText,orientation=msoTextOrientationHorizontal, ws=self.ws,tshape=tshape,)
        return cshape
    
    def getShape(self,index):
        if type(index)==int:
            if index <= len(self.ws.tablemodel.shapelist):
                shape = self.convTShape2CShape(self.ws.tablemodel.shapelist[index-1])
            else:
                shape=None
        else:
            shape=self.ws.get_Shape(index) # by name
        return shape
    
    def getlist(self):
        return self.ws.tablemodel.shapelist
        
    def AddShape(self, shapetype, Left, Top, Width, Height, Row=None, Col=None, Fill=0,text="",name="",control_dict=None):
        shape=None
        if shapetype == msoShapeRectangle:
            shape=CShape(name, shapetype, Left, Top, Width, Height, Fill, ws=self.ws)
        elif shapetype == msoShapeOval:
            shape=CShape(name, shapetype, Left, Top, Width, Height, Fill, ws=self.ws)
        elif shapetype == msoTextBox:
            shape=CShape(name, shapetype, Left, Top, Width, Height, Fill, Text=text,ws=self.ws)
        elif shapetype == msoOLEControlObject:
            shape=CShape(name, shapetype, Left, Top, Width, Height, Fill,ws=self.ws, Row=Row, Col=Col, control_dict=control_dict)
        return shape # self.convTShape2CShape(shape)

    def AddLabel(self, TextOrientation=msoTextOrientationHorizontal, Left=0, Top=0 , Width=0, Height=0):
        shape=self.ws.table.addLabel( TextOrientation, Left, Top, Width, Height)
        return self.convTShape2CShape(shape)
    
    def AddConnector(self, ConType, BeginX, BeginY, EndX, EndY):
        Left=BeginX
        Top=BeginY
        Width=EndX-BeginX
        Height=EndY-BeginY
        shape=self.ws.table.addConnector( ConType, Left, Top, Width, Height)
        return self.convTShape2CShape(shape)
        
    
    def AddPicture(self, PicName, linktofile=False, savewithdocument=True, Left=0 , Top=0 , Width=0, Height=0):
        shape=self.ws.table.addPicture( PicName, Left, Top, Width, Height)
        return self.convTShape2CShape(shape)
    
    def BuildFreeform(self, EditingType, X1, Y1):

        return CFreeForm(EditingType,X1,Y1)
        
    def Delete(self,shape):
        self.ws.table.deleteshape(shape)
        #if type(shape)==int:
        #    del self.tablemodel.shapelist[shape-1]
        #else:
        #    self.tablemodel.shapelist.remove(shape)
        
    def Count(self):
        return len(self.ws.tablemodel.shapelist)
    
    def Range(self,input_array):
        searchname = str(input_array)
        searchname = searchname[2:-2] # remove []
        for Shape in self:
            if Shape.Name == searchname:
                return Shape
        return None
        
    
    def __iter__(self):
    #returning __iter__ object
        self.currentidx = 1
        self.currentshape = self.getShape(self.currentidx)
        self.stopiteration=False
        return self
    
    def __next__(self):
        self.currentshape = self.getShape(self.currentidx)
        if self.stopiteration or self.currentshape==None:
            raise StopIteration 
        self.currentidx += 1
        if self.currentidx > len(self.ws.tablemodel.shapelist):
            self.stopiteration=True       
        return self.currentshape

class CRangeList(list):
    def __init__(self, *args):
        list.__init__(self,*args)
        
    def get_count(self):
        return len(self)
    
    def set_count(self,range):
        pass        
            
    Count = property(get_count, set_count, doc='number of rows included in range')     
        
class CRange(str):
    def __new__(cls,t1=None,t2=None,ws=None,value="",parenttype="",parent=None):
        if ws==None:
            ws=ActiveSheet
            
        if t2==None:
            if t1==None: #only type definition, only dummy needed
                return
        #print("Range:",t1,t2)
        if type(t1)==int and type(t2)==int:
            start=(t1,t2)
            end=(t1,t2)
        elif type(t1) == CRange:
            #t1=t1.start
            start=t1.start
            if t2==None:
                end=t1.end
            elif type(t2) ==CRange:
                end=t2.start
            else:
                Debug.Print("CRange-Error t2 wrong type:"+repr(t2))
        elif type(t1)== str:
            if IsNumeric(t1):
                t1=int(t1)
            elif ":" in t1: # range as string a:b
                cellsplit = t1.split(":")
                temprng=CRange(cellsplit[0],cellsplit[1])
                start= temprng.start
                end  = temprng.end
                
            else:
                named_cell1 = ws.find_RangeName(t1,ws=ws)
                if named_cell1 == None:
                    logging.debug("Named Range not found:", t1)
                    start=(1,1)
                    end=(1,1)
                else:
                    if t2 != None:
                        if type(t2) == str:
                            named_cell2 = ws.find_RangeName(t2)
                            temprng=CRange(named_cell1,named_cell2,ws=ws)
                            start= temprng.start
                            end  = temprng.end
                            
                        else:
                            temprng = CRange(named_cell1,t2,ws=ws)
                            start= temprng.start
                            end  = temprng.end
                    else:
                        start=named_cell1.start
                        end  =named_cell1.end
        else: 
            if type(t1)==int and type(t2)!=int:
                #error return (t1,t1)
                start=(t1,t1)
                end=(t1,t1)
            else: # t1 is a tuple (row,col)
                start=t1
                end  =t1
        if t2!=None:
            if type(t2)==CRange:
                end=t2.end
            elif type(t2)==str:
                if IsNumeric(t2):
                    t2=int(t2)
                    start=(t1,t2)
                    end=(t1,t2)
                else:
                    logging.debug("Error-CRANGE-Type T2: %s",repr(t2))
            elif type(t2)!=int:
                end = t2
            else:
                start=(t1,t2)
                end=(t1,t2)
        row=start[0]
        col=start[1]
        max_cols = ws.tablemodel.getColumnCount()
        max_rows = ws.tablemodel.getRowCount()
        if col < max_cols and row < max_rows:
            value = ws.tablemodel.getValueAt(row-1,col-1)
        else:
            value = ""
        obj=str.__new__(cls,value)
        obj.ws = ws
        obj.Worksheet = obj.ws
        if parent==None:
            obj.Parent = obj.ws
        else:
            obj.Parent=parent
        obj.Interior = CInterior(parent=obj)
        obj.DisplayFormat = CDisplayFormat(parent=obj)
        obj.HasFormula = False
        obj.WrapText=False
        obj.Orientation=xlHorizontal           
        obj.start = start
        obj.end   = end
        obj.Formula=""
        obj.ParentType=parenttype
        obj.iter_start=None
        obj.currentcell=obj.start
        #self.rowrange = (self.start[0],self.end[0])
        #self.colrange = (self.start[1],self.end[1])
        #self.Address=self.start
        #self.Rows=[]
        #self.Columns = []
        #self.Cells = CCells(self.rowrange,self.colrange,ws=ws)
        obj.CountLarge = (obj.end[0]-obj.start[0]+1)*(obj.end[1]-obj.start[1]+1)
        obj.Font = CFont("Arial",10)

        return obj
        #    x1,y1,x2,y2 = self.ws.table.getCellCoords(self.Row-1,self.Column-1)
        #    self.Height=y2-y1
        #    self.Width=x2-x1
        #    self.Top=y1
        #    self.Left=x1
        #    self.Interior = CInterior(self.Cells,p_range=self)

    # Attributes
    def dummy(self,value):
        pass
    
    def get_address(self):
        return self.start
    def set_address(self,range):
        pass
    Address = property(get_address, set_address, doc='adress of first cell in range')
    
    
    def set_cells(self,rowlist):
        pass

    def get_cells(self):
        if self.Parent.ParentType=="Columns":
            startrow=self.Parent.Parent.start[0]
            lastrow =self.Parent.Parent.end[0]
            column = self.start[1]
            return CRange((startrow,column),(lastrow,column),parent=self,ws=self.ws)
        else:
            logging.debug("get_cells-Error")
      
    Cells = property(get_cells, set_cells, doc='rows included in range')   

    def get_column(self):
        #row = CRow(self.start[0])
        return self.start[1]
    def set_column(self,range):
        pass 
    Column = property(get_column, set_column, doc='row of first cell in range')

    def set_columns(self,rowlist):
        pass
    
    def get_columns(self):
        return CRange((self.start[0],self.start[1]),(self.start[0],self.end[1]),ws=self.ws,parent=self,parenttype="Columns")
   
    Columns = property(get_columns, set_columns, doc='Columns in Range')
    
    def get_columnwidth(self):
        colname=self.ws.tablemodel.getColumnName(self.start[1]-1)
        width=self.ws.tablemodel.columnwidths[colname]
        return width
    
    def set_columnwidth(self, width):
        for col in range(self.start[1],self.end[1]+1):
            colname=self.ws.tablemodel.getColumnName(col-1)
            self.ws.tablemodel.columnwidths[colname] = width
        return
    ColumnWidth = property(get_columnwidth, set_columnwidth, doc='ColumnWidth of CRange')

    def get_count(self):
        return (self.end[0]-self.start[0]+1)*(self.end[1]-self.start[1]+1)
    def set_count(self,p_range):
        pass         
    Count = property(get_count, set_count, doc='number of cells in range')
      
    def get_entirecolumn(self):
        entirecolumn = CRange((1,self.start[1]),(self._get_LastRow(),self.end[1]),parenttype="EntireColumn")
        return entirecolumn
    def set_entirecolumn(self,param):
        pass
    EntireColumn = property(get_entirecolumn, set_entirecolumn, doc='entirecolumn of range')

    def get_entirerow(self):
        entirerow = CRange((self.start[0],1),(self.end[0],self._get_LastColumn()),parenttype="EntireRow")
        return entirerow
    def set_entirerow(self,param):
        pass
    EntireRow = property(get_entirerow, set_entirerow, doc='entirerow of range')

    def _Height(self):
        x1,y1,x2,y2 = self.ws.table.getCellCoords(self.Row-1,self.Column-1)
        return (y2-y1)
    Height  = property(_Height, dummy, doc='Height of cell')
    
    def get_Hidden(self):
        if self.ParentType=="EntireRow":
            return self.start[0]-1 in ActiveSheet.table.model.hiderowslist
        elif self.ParentType=="EntireColumn":
            return False
        else:
            return False
        
    def _set_hiderow(self,row,newval):
        if newval==True:
            if not row-1 in ActiveSheet.table.model.hiderowslist:
                ActiveSheet.table.model.hiderowslist.append(row-1)
                ActiveSheet.Redraw_table()
        else:
            if row-1 in ActiveSheet.table.model.hiderowslist:
                ActiveSheet.table.model.hiderowslist.remove(row-1)
                ActiveSheet.Redraw_table()
                
    def _set_hidecolumn(self,col,newval):
        if newval==True:
            if not col-1 in ActiveSheet.table.model.hidecolslist:
                ActiveSheet.table.model.hidecolslist.append(col-1)
                ActiveSheet.Redraw_table()
        else:
            if col-1 in ActiveSheet.table.model.hidecolslist:
                ActiveSheet.table.model.hidecolslist.remove(col-1)
                ActiveSheet.Redraw_table()    

    def set_Hidden(self,hide):
        if self.ParentType=="EntireRow":
            for row in range(self.start[0],self.end[0]+1):
                self._set_hiderow(row,hide)            
        elif self.ParentType=="EntireColumn":
            for col in range(self.start[1],self.end[1]+1):
                    self._set_hidecolumn(col,hide)
        else:
            return False
    Hidden = property(get_Hidden, set_Hidden, doc='hidden attribute of range')

    def _Left(self):
        x1,y1,x2,y2 = self.ws.table.getCellCoords(self.Row-1,self.Column-1)
        return x1    
    Left = property(_Left, dummy, doc='Left coordinates of cell')
    
    def get_row(self):
        return self.start[0]
    def set_row(self,range):
        pass
    Row = property(get_row, set_row, doc='row of first cell in range')

    def get_rows(self):
        return CRange((self.start[0],self.start[1]),(self.end[0],self.start[1]),ws=self.ws,parent=self,parenttype="Rows")
    def set_rows(self,rowlist):
        pass
    Rows = property(get_rows, set_rows, doc='rows included in range')
    
    def set_columns(self,rowlist):
        pass
    def get_columns(self):
        return CRange((self.start[0],self.start[1]),(self.start[0],self.end[1]),ws=self.ws,parent=self,parenttype="Columns")
    Columns = property(get_columns, set_columns, doc='Columns in Range')    
    
    def get_text(self):
        return self.get_value()
    def set_text(self,value):
        self.set_value(value)
    Text = property(get_text, set_text, doc='value of Textvalue of Range')
    
    def _Top(self):
        x1,y1,x2,y2 = self.ws.table.getCellCoords(self.Row-1,self.Column-1)
        return y1
    Top  = property(_Top, dummy, doc='Top coordinates of cell')
  
    def get_value(self):
        row=self.start[0]
        col=self.start[1]
        if self.ws.tablemodel == None:
            self.ws.tablemodel = ActiveSheet.tablemodel
        max_cols = self.ws.tablemodel.getColumnCount()
        max_rows = self.ws.tablemodel.getRowCount()
        if col < max_cols and row < max_rows:
            value = self.ws.tablemodel.getValueAt(row-1,col-1)
        else:
            value = ""
        return value         

    def set_value(self,value):
        row=self.start[0]
        col=self.start[1]        
        if self.ws.tablemodel == None:
            self.ws.tablemodel = ActiveSheet.tablemodel
        if row <=self.ws.tablemodel.getRowCount() and col <=self.ws.tablemodel.getColumnCount():
            curval = self.ws.tablemodel.getValueAt(row-1, col-1)
            if curval != value:
                self.ws.tablemodel.setValueAt(value, row-1, col-1)
                self.ws.table.event_row=row-1
                self.ws.table.event_col=col-1
                self.ws.Workbook.Synch_Evt_SheetChange(self.ws.table)
    Value = property(get_value, set_value, doc='value of first Cell in Range')
    
    def _Width(self):
        x1,y1,x2,y2 = self.ws.table.getCellCoords(self.Row-1,self.Column-1)
        return x2-x1
    Width = property(_Width, dummy, doc='Width of cell')
        

# Methods
    def Activate(self):
        for cell in self:
            row=cell.Row
            col=cell.Column
            self.ws.table.setSelectedRow(row)
            self.ws.table.setSelectedCol(col)
        
    def CellsFct(self,row,column):
        return CRange(row,column, ws=self.ws)    
    

    def ClearContents(self):
        for cell in self:
            cell.Value=""
            
    def Copy(self,dst):
        #calculate offset for copy
        offset_row = dst.Row-self.start[0]
        offset_col = dst.Column-self.start[1]
        if offset_col>0:
            for row in range(self.end[0],self.start[0]-1,-1):
                for col in range(self.end[1],self.start[1]-1,-1):
                    cell=CRange(row,col,ws=self.ws)
                    cell.offset(offset_row,offset_col).Value=cell.Value
        else:
            for row in range(self.start[0],self.end[0]+1):
                for col in range(self.start[1],self.end[1]+1):
                    cell=CRange(row,col,ws=self.ws)
                    cell.offset(offset_row,offset_col).Value=cell.Value            
            
    def End(self,param):
        row=self.start[0]
        column=self.start[1]
        if param==xlToRight:
            column=-1
            for cell in self:
                if cell.Value!="":
                    if cell.Column>column:
                        column=cell.Column
            if column==-1:
                column = self.end[1]+2 #I do not knbow if this is correct, but the column must be higher than end +1 to show that the row is empty
        elif param==xlUp:
            logging.debug("End -xlToUp")
            
        elif param==xlDown:
            logging.debug("End -xlDown")
        else: # xlToLeft
            logging.debug("End -xlToLeft")
        return CRange(row,column)    
                
    def Find(self,What="", after=None, LookIn=xlFormulas, LookAt= xlWhole, SearchOrder=xlByRows, SearchDirection=xlNext, MatchCase= True, SearchFormat= False):
        if after!=None:
            self.iter_start = after.start
        else:
            self.iter_start = None
        for cell in self:
            cell_val=str(cell.Value)
            if cell_val == What:
                return cell
            
    def Offset(self, offset_row, offset_col):
        return self.offset(offset_row, offset_col)    
            
    def offset(self, offset_row, offset_col):
        #newrowrange=(self.rowrange[0]+offset_row,self.rowrange[1]+offset_row)
        #newcolrange=(self.colrange[0]+offset_col,self.colrange[1]+offset_col)
        newstart=(self.start[0]++offset_row,self.start[1]+offset_col)
        newend=(self.end[0]++offset_row,self.end[1]+offset_col)
        new_range=CRange(newstart,newend,ws=self.ws)
        return new_range
    
    def Select(self):
        self.ws.table.setSelectedCells(self.start[0]-1, self.end[0]-1,self.start[1]-1,self.end[1]-1)
        
    def check_if_empty_row(self):
        if self.ws.tablemodel == None:
            self.ws.tablemodel = ActiveSheet.tablemodel        
        cols = self.ws.tablemodel.getColumnCount()
        r=self.Row-1
        for c in range(0,cols):
            #absr = self.get_AbsoluteRow(r)
            val = self.ws.tablemodel.getValueAt(r,c)
            if val != None and val != '':
                return False
        return True    

#python substitute function
        
    def __iter__(self):
    #returning __iter__ object
        if self.iter_start!=None:
            self.currentcell = self.iter_start
        else:
            self.currentcell = self.start
        self.stopiteration=False
        return self
    
    def __next__(self):
        currentresult = CRange(self.ws.Cells(self.currentcell[0],self.currentcell[1]),parent=self,ws=self.ws)
        if self.stopiteration:
            raise StopIteration
        currentcell_col=self.currentcell[1]
        currentcell_row=self.currentcell[0]
        currentcell_col+=1
        if currentcell_col>self.end[1]: 
            currentcell_row+=1
            currentcell_col = self.start[1]
            if currentcell_row > self.end[0]:
                self.stopiteration=True
        self.currentcell = (currentcell_row,currentcell_col)
        return currentresult
    
    def __eq__(self,other):
        if type(other) == int:
            value=self.get_value()
            if type(value)==int:
                intvalue=value
                fn_return_value=(intvalue==other)
            else:
                if value.isnumeric():
                    intvalue=int(value)
                    fn_return_value=(intvalue==other)
                else:
                    fn_return_value=False
            return fn_return_value
        else:
            value=self.get_value()
            strvalue=str(value)
            strother=str(other)    
            fn_return_value=(strvalue==strother)
            return fn_return_value            

    def __lt__(self,other):
        if type(other) == int:
            value=self.get_value()
            if type(value)==int:
                intvalue=value
                fn_return_value=(intvalue<other)
            else:
                if value.isnumeric():
                    intvalue=int(value)
                    fn_return_value=(intvalue<other)
                else:
                    fn_return_value=False
            return fn_return_value
        value=str(self)
        fn_return_value=(value<other)
        return fn_return_value
        
    def __gt__(self,other):
        if type(other) == int:
            value=self.get_value()
            if type(value)==int:
                intvalue=value
                fn_return_value=(intvalue>other)
            else:
                if value.isnumeric():
                    intvalue=int(value)
                    fn_return_value=(intvalue>other)
                else:
                    fn_return_value=False
            return fn_return_value
        value=str(self)
        fn_return_value=(value>other)
        return fn_return_value
    
    def __le__(self,other):
        if type(other) == int:
            value=self.get_value()
            if type(value)==int:
                intvalue=value
                fn_return_value=(intvalue<=other)
            else:
                if value.isnumeric():
                    intvalue=int(value)
                    fn_return_value=(intvalue<=other)
                else:
                    fn_return_value=False
            return fn_return_value

        value=str(self)
        fn_return_value=(value<=other)
        return fn_return_value
        
    def __ge__(self,other):
        if type(other) == int:
            value=self.get_value()
            if type(value)==int:
                intvalue=value
                fn_return_value=(intvalue>=other)
            else:
                if value.isnumeric():
                    intvalue=int(value)
                    fn_return_value=(intvalue>=other)
                else:
                    fn_return_value=False
            return fn_return_value

        value=str(self)
        fn_return_value=(value>=other)
        return fn_return_value    
        
        
    def __int__(self):
        value=self.get_value()
        return int(value)
    
    def __str__(self):
        value=self.get_value()
        return str(value)
    
    def __pow__(self, other):
        value = str(self)
        if value.isnumeric():
            intvalue=int(value)
            return intvalue ** other
        else:
            return 1
    
    def __rpow__(self, other):
        value = str(self)
        if value.isnumeric():
            intvalue=int(value)
            return other ** intvalue
        else:
            return other
        
    def __add__(self,other):
        value = str(self)
        if not isinstance(other,str):
            if value.isnumeric():
                intvalue=int(value)
                return other + intvalue
            else:
                return other
        else:
            return str(self) + str(other)
        
    def __radd__(self,other):
        value = str(self)
        if not isinstance(other,str):
            if value.isnumeric():
                intvalue=int(value)
                return other + intvalue
            else:
                return other
        else:
            return str(other) + value
        
    def __sub__(self,other):
        value = str(self)
        if value.isnumeric():
            intvalue=int(value)
            return intvalue - other
        else:
            return -other
        
    def __rsub__(self,other):
        value = str(self)
        if value.isnumeric():
            intvalue=int(value)
            return  other -intvalue
        else:
            return other
        
    def __mul__(self,other):
        value = str(self)
        if value.isnumeric():
            intvalue=int(value)
            return intvalue * other
        else:
            return other
        
    def __rmul__(self,other):
        value = str(self)
        if value.isnumeric():
            intvalue=int(value)
            return intvalue * other
        else:
            return other

# other functions    
    def upper(self):
        value=str(self)
        return value.upper()
    
# internal functions
    
    def _get_LastRow(self):
        return self.ws.tablemodel.getRowCount()
    
    def _get_LastColumn(self):
        return self.ws.tablemodel.getColumnCount()
    
            
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

    
class CRectangle(object):
    def __init__(self,row=0,col=0,i=0,onaction=""):
        self.OnAction = onaction
        self.TopLeftCell = None
        self.TopLeftCell.Row = row
        self.TopLeftCell.Column = col
        self.index = i
        pass
    
    def Delete(self):
        super().delete(self.index)
        pass
    
class CShapeRange(object):
    def __init__(self,ws=None):
        if ws==None:
            ws=ActiveSheet
        self.ws=ws
        self.shapes=ws.table.getSelectedShapes()
        self.Line=CLine(shape=self.shapes)
        self.Fill=CFill(shape=self.shapes)
        self.ws=ws
        
    def __getitem__(self, k):
        #print("Getitem",k)
        self.shapes=self.ws.table.getSelectedShapes()
        if k-1<len(self.shapes):
            return self.shapes[k-1]
        else:
            return None
         
    def __setitem__(self,k,value):
        self.ws.table.setSelectedShapes(value)
        
    def set_Name(self, newval):
        for shape in self.shapes:
            shape.Name=newval
    
    def get_Name(self):
        return self.shapes[0].Name
        
    Name = property(get_Name, set_Name, doc='ShapeRange-Name')
    
class CColumns(object):
    
    def __init__(self,startcol=None,lastcol=None,parent=None,ws=None):
        self.ws=ws
        if startcol==None:
            self.startcol=parent.start[1]
            self.lastcol =parent.end[1]
        else:
            self.startcol = startcol
            self.lastcol  = lastcol
        self.parent=parent
        self.currentcol = startcol
        self.Column = startcol
        #self.Cells = CRange(self.parent.start[0],self.currentcol),(self.parent.end[0],self.currentcol),parent=self,ws=self.ws)
        
    def get_Count(self):
        return self.lastcol-self.startcol
    
    def set_Count(self,value):
        pass
    
    Count = property(get_Count,set_Count,doc="Selection Count")
    
    #python substitute function
            
    def __iter__(self):
    #returning __iter__ object
        self.currentcol = self.startcol
        self.stopiteration=False
        return self
    
    def __next__(self):
        self.Column = self.currentcol
        currentresult = CRange((self.parent.start[0],self.currentcol),(self.parent.end[0],self.currentcol),parent=self,ws=self.ws)
        if self.stopiteration:
            raise StopIteration
        self.currentcol+=1
        if self.currentcol>self.lastcol: 
            self.stopiteration=True
        return currentresult    
        
   
class CSelection(object):
    def __init__(self,selrange=None,ws=None):
        if ws==None:
            ws=ActiveSheet
        self.ws=ws
        self.selectedrange=selrange
        #self.EntireRow = CEntireRow(cell.Row)
        #self.EntireColumn = CEntireColumn(cell.Column)
        
    def EntireRow(self):
        self.selectedRows = []
        for row in self.ws.table.multiplerowlist:
            self.selectedRows.append(row+1)
        if self.selectedRows==[]:
            self.selectedRows=[self.ws.table.getSelectedRow()+1]
        return self.selectedRows
    
    def Rows(self):
        selectedrows = self.EntireRow()
        selectedcrows = []
        for row in selectedrows:
            selectedcrows.append(CRow(row))
        return selectedcrows
    
    def Select(self):
        pass
    
    def set_ShapeRange(self, newval):
        pass
    
    def get_ShapeRange(self):
        return CShapeRange(ws=self.ws)
        
    ShapeRange = property(get_ShapeRange, set_ShapeRange, doc='ShapeRange')
    
    def set_RowRange(self, newval):
        pass
    
    def get_RowRange(self):
        selectedrows=self.EntireRow()
        if selectedrows != []:
            rowrange=(selectedrows[0],selectedrows[-1]+1)
        return rowrange
   
    rowrange = property(get_RowRange, set_RowRange, doc='RowRange')
    
    ShapeRange = property(get_ShapeRange, set_ShapeRange, doc='ShapeRange')
    
    def set_ColRange(self, newval):
        pass
    
    def get_ColRange(self):
        selectedcol=ActiveSheet.table.getSelectedColumn()
        if selectedcol != -1:
            colrange=(selectedcol,selectedcol+1)
        return colrange
   
    colrange = property(get_ColRange, set_ColRange, doc='ColRange')
    
    def set_Column(self, newval):
        pass
    
    def get_Column(self):
        selectedcol=ActiveSheet.table.getSelectedColumn()+1
        return selectedcol
   
    Column = property(get_Column, set_Column, doc='Column')
    
    def set_Columns(self, newval):
        pass
    
    def get_Columns(self):
        selectedcol=ActiveSheet.table.getSelectedColumn()+1
        return CColumns(selectedcol,selectedcol+1,ws=self.ws,parent=self)
   
    Columns = property(get_Columns, set_Columns, doc='Columns')
    

class CRow(object):
    def __init__(self,rownumber,rowrange=None):
        self.Row = rownumber
        self.Rowrange=rowrange
        self.EntireRow = CEntireRow(rownumber,rowrange)
        self.Hidden_value = False
        self.Top = 0  #*HL
        self.Height = 12 #*HL
        
    def Select(self):
        ActiveSheet.table.gotoCell(self.Row-1,0)
        return
    
    def _set_hiderow(self,row,newval):
        if newval==True:
            if not row-1 in ActiveSheet.table.model.hiderowslist:
                ActiveSheet.table.model.hiderowslist.append(row-1)
        else:
            if row-1 in ActiveSheet.table.model.hiderowslist:
                ActiveSheet.table.model.hiderowslist.remove(row-1)
        ActiveSheet.Redraw_table()
                
    def _set_rowheight(self,row,newval):
        ActiveSheet.table.model.rowheightlist[row-1]=newval
        ActiveSheet.Redraw_table()
        
    def _get_rowheight(self,row):
        return ActiveSheet.table.model.rowheightlist[row-1]
        
    def set_Hidden(self, newval):
        self.Hidden_value = newval
        if self.Rowrange:
            for row in self.Rowrange:
                self._set_hiderow(row,newval)
        else:
            self._set_hiderow(self.Row,newval)    
    
    def get_Hidden(self):
        return self.Row-1 in ActiveSheet.table.model.hiderowslist
        
    Hidden = property(get_Hidden, set_Hidden, doc='Hiddenvalue of CRow')
    
    def set_RowHeight(self, newval):
        newval = newval * xlvp2py_guifactor
        if self.Rowrange:
            for row in self.Rowrange:
                self._set_rowheight(row,newval)
        else:
            self._set_rowheight(self.Row,newval)    
    
    def get_RowHeight(self):
        rowheight = ActiveSheet.table.model.rowheightlist.get(self.Row-1,12)
        rowheight = int(rowheight/xlvp2py_guifactor)
        return rowheight
        
    RowHeight = property(get_RowHeight, set_RowHeight, doc='Hiddenvalue of CRow')
        
    
        
class CEntireRow(object):
    
    def __init__(self,rownumber,colrange=None,ws=None):
        self.Rownumber = rownumber
        self.Hidden_value = False
        self.Colrange=colrange
        self.Columns=CColumns(CRange((self.Rownumber,1),colrange,ws=ws))
        
    def _set_hiderow(self,row,newval):
        if newval==True:
            if not row-1 in ActiveSheet.table.model.hiderowslist:
                ActiveSheet.table.model.hiderowslist.append(row-1)
                ActiveSheet.Redraw_table()
        else:
            if row-1 in ActiveSheet.table.model.hiderowslist:
                ActiveSheet.table.model.hiderowslist.remove(row-1)
                ActiveSheet.Redraw_table()        
        
    def set_Hidden(self, newval):
        self.Hidden_value = newval
        
        if self.Rowrange:
            for row in self.Rowrange:
                self._set_hiderow(row,newval)
        else:
            self._set_hiderow(self.Rownumber,newval)
    
    def get_Hidden(self):
        return self.Rownumber-1 in ActiveSheet.table.model.hiderowslist
        
    Hidden = property(get_Hidden, set_Hidden, doc='Hiddenvalue of CRow')
        

        
class CColumn(object):
    def __init__(self,colnumber,rowrange=None):
        self.Column=colnumber
        self.EntireColumn = CEntireColumn(colnumber)
        self.columnwidth = 5
        self.Hidden = False
        self.rowrange=rowrange
        #self.Cells = CRange(rowrange,(colnumber,colnumber))
        
        
    def get_columnwidth(self):
        return self.columnwidth
    
    def set_columnwidth(self, value):
        self.columnwidth = value
        ActiveSheet.table.resizeColumn(self.Column-1,value)
        
    def get_cells(self):
        cell_list=[]
        if self.rowrange:
            for cellrow in self.rowrange:
                cell_list.append(Cells(cellrow,self.Column))
        
        return cell_list
    
    def set_cells(self, value):
        pass
        
        
    ColumnWidth = property(get_columnwidth, set_columnwidth, doc='Column Width')
    
    Cells = property(get_cells, set_cells, doc='Cells in Column')
        
class CEntireColumn(object):
    def __init__(self,colnumber):
        self.Columnnumber = colnumber
        self.Hidden = False
        
class CInterior(object):
    def __init__(self,parent=None):
        self.parent=parent
        
    def get_color(self):
        if self.parent == None:
            return tkcolor2int("#FFFFFF")
        try:
            if type(self.parent) == CRange:
                colorvalue = self.parent.ws.tablemodel.getColorAt(self.parent.start[0]-1,self.parent.start[1]-1)
                if colorvalue==None:
                    colorvalue="#FFFFFF"
                return tkcolor2int(colorvalue)
            else:
                Debug.Print("CInterior Type ERROR")
                return tkcolor2int("#FFFFFF")
        except BaseException as e:
            logging.debug(e)
            return tkcolor2int("#FFFFFF")
    
    def set_color(self, value):
        if self.parent==None:
            return
        if type(value) == int:
            valuestr=int2tkcolor(value)
        elif type(value) == str:
            if value.isnumeric():
                valuestr=int2tkcolor(int(value))
            else:
                valuestr=value
        else:
            valuestr=f'#{value[0]:02x}{value[1]:02x}{value[2]:02x}'
        if type(self.parent) == CRange:
            for cell in self.parent:
                self.parent.ws.tablemodel.setColorAt(cell.start[0]-1,cell.start[1]-1, valuestr)
    Color = property(get_color, set_color, doc='Cell Color')    

class CDisplayFormat(object):
    def __init__(self,parent=None):
        self.parent=parent
        self.Interior = CInterior(parent=parent)
    
class CColor(object):
    def __init__(self,color,shape=None,tablemodel=None,line=None,cell=None,fg=False):
        self.line=line
        self.shape=shape
        self.tablemodel=tablemodel
        self.cell=cell
        self.color = color # int 0xrrggbb
        
    def tkcolor(self):
        return f'#{self.r:02x}{self.g:02x}{self.b:02x}'
    
    def get_rgb(self):
        colorvalue=self.color
        if self.cell!=None:
            colorvalue_str = self.tablemodel.getColorAt(self.cell.Row-1,self.cell.Column-1)
            colorvalue=tkcolor2rgb(colorvalue_str)
            #print("get_rgb:"+self.cell.Name+"-"+colorvalue_str)
        elif self.shape!=None:
            colorvalue=self.color
        return colorvalue
    
    def set_rgb(self, value):
        if type(value) == int:
            valuestr=int2tkcolor(value)
        elif type(value) == str:
            valuestr=value
        else:
            valuestr=f'#{int(value[0]):02x}{int(value[1]):02x}{int(value[2]):02x}'
        if self.cell!=None:
            self.cell.tablemodel.setColorAt(self.cell.Row-1,self.cell.Column-1, valuestr)
            self.rgb_val=valuestr
        if self.shape!=None:
            if type(self.shape)==list:
                if self.shape==[]:
                    shape=None
                else:
                    shape=self.shape[0]
            else:
                shape=self.shape
            if shape!=None:
                if shape.Tshape:
                    if shape.Tshape.rectidx!=0:
                        shape.Tablecanvas.itemconfig(shape.Tshape.rectidx,fill=valuestr)
                    shape.Fillcolor=valuestr
                    shape.Tshape.Fillcolor=valuestr
                    #print("set_rgb:"+self.shape.Name+"-"+valuestr)
                else:
                    logging.debug("set_rgb: Rectidx=0" +str(self.shape)+ "-"+valuestr)
                    pass
            else:
                logging.debug("set_rgb: Shape not found" +str(self.shape)+ "-"+valuestr)                         
        else:
            logging.debug("set_rgb: Shape not found" + "-"+valuestr)                
                
        self.rgb_val=valuestr
        rgb=tkcolor2rgb(valuestr)
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]
        
    rgb = property(get_rgb, set_rgb, doc='Color RGB')

class CLine(object):
    def __init__(self,linecolor=0,shape=None):
        self.Weight = 8
        self.ForeColor = CColor((255,0,0),line=True,shape=shape,fg=True)
        self.BackColor = CColor((255,0,0),line=True,shape=shape,fg=False)
        self.Visible = True
        self.Transparency = 0
        self.shape=shape
        self.EndArrowheadStyle_val= 0
        
    def get_EndArrowheadStyle(self):
        return self.EndArrowheadStyle_val
    
    def set_EndArrowheadStyle(self,newval):
        self.EndArrowheadStyle_val=newval
        if type(self.shape)==list:
            for shape in self.shape:
                shape.EndArrowheadStyle_val=newval
                if shape.Tshape:
                    shape.Tshape.EndArrowheadStyle_val = newval                
        else:
            self.shape.EndArrowheadStyle_val=newval      
            if self.shape.Tshape:
                self.shape.Tshape.EndArrowheadStyle_val = newval
        
    EndArrowheadStyle = property(get_EndArrowheadStyle,set_EndArrowheadStyle,doc="EndArrowheadStyle")
    
    def get_BeginArrowheadStyle(self):
        return self.BeginArrowheadStyle_val
    
    def set_BeginArrowheadStyle(self,newval):
        self.BeginArrowheadStyle_val=newval
        if type(self.shape)==list:
            for shape in self.shape:
                shape.BeginArrowheadStyle_val=newval
                if shape.Tshape:
                    shape.Tshape.BeginArrowheadStyle_val = newval                
        else:
            self.shape.BeginArrowheadStyle_val=newval      
            if self.shape.Tshape:
                self.shape.Tshape.BeginArrowheadStyle_val = newval
        
    BeginArrowheadStyle = property(get_BeginArrowheadStyle,set_BeginArrowheadStyle,doc="BeginArrowheadStyle")    
        
class CFill(object):
    def __init__(self,Fill="",shape=None):
        self.Visible = 1
        self.ForeColor = CColor((0, 0, 0),shape=shape,fg=True)
        self.Transparency_val = 0
        self.shape=shape
                
    def get_transparency(self):
        return self.Transparency_val
    
    def set_transparency(self,newval):
        self.Transparency_val=newval
        if newval >=0.5:
            zorder=1 #to Bottum
        else:
            zorder=0 # toTop
        if type(self.shape)==list:
            for shape in self.shape:
                shape.ZOrder_val=zorder
                if shape.Tshape:
                    shape.Tshape.ZOrder_Val = zorder                
        else:
            self.shape.ZOrder_val=zorder      
            if self.shape.Tshape:
                self.shape.Tshape.ZOrder_Val = zorder
        
    Transparency = property(get_transparency,set_transparency,doc="Transparency")
        
    def Solid(self):
        pass

class CShape(object):
    def __init__(self, name, shapetype, Left, Top, Width=0, Height=0, Fillcolor=0, Text="",Row=None, Col=None, rotation=0,orientation=msoTextOrientationHorizontal,AlternativeText="",ws=None,tshape=None,nodelist=None,control_dict=None,linecolor=0,zorder=0,segmenttype=msoSegmentLine,editingtype=msoEditingAuto):
        filltkcolor=int2tkcolor(Fillcolor)
        linetkcolor=int2tkcolor(linecolor)
        if shapetype==msoOLEControlObject:
            if type(Width)==int:
                Width = Width *1.55
                Height = Height *1.55
        if ws==None:
            ws=ActiveSheet
        if tshape==None:
            tshape=CTShape(name, shapetype, Left, Top, Width, Height, FillTKcolor=filltkcolor, LineTKcolor=linetkcolor,Text=Text,Row=Row, Col=Col,rotation=rotation,orientation=orientation,nodelist=nodelist,tablecanvas=ws.table,control_dict=control_dict,zorder=zorder,segmenttype=segmenttype,editingtype=editingtype)
        self.Tshape=tshape 
        self.Shapetype = shapetype
        if shapetype in (msoShapeRectangle, msoShapeOval):
            self.Type = msoAutoShape
            self.AutoShapeType = shapetype
        else:
            self.Type = shapetype
        self.Tablecanvas=ws.table
        if ws==None:
            ws=ActiveSheet
        self.Worksheet=ws
        self.Tshape=tshape
        self.Name_val=name
        self.rectidx=0
        self.textidx=0
        self.tablename = ws.table.tablename
        self.Left = Left
        self.Active = True
        self.Top = Top
        self.Top_val = None
        self.Width = Width
        self.Height = Height
        self.Row=Row
        self.Col=Col
        self.Rotation = rotation
        self.Visible_val = True
        if Top==None:
            self.TopLeftCell_Row=Row-1
            self.TopLeftCell_Col=Col-1
        else:
            self.TopLeftCell_Row=ws.table.calc_row_from_y(Top)
            self.TopLeftCell_Col=ws.table.calc_col_from_x(Left)
        self.Index = 0
        self.OnAction = ""
        self.ZOrder_val=zorder
        self.Locked = False
        self.TextFrame2 = CTextFrame2(text=Text,shape=self)
        self.AlternativeText = AlternativeText
        self.Fill = CFill(Fillcolor,shape=self)
        self.Line = CLine(linecolor,shape=self)

        #if tshape==None:    # create new tshape
        #    self.Tshape=self.Tablecanvas.addshape(name, shapetype, Left, Top, Width, Height, Fillcolor, Text="",rotation=0,orientation=1,tablecanvas=None)
            
    def updateShape(self,Fill=None,Text=None):
        if Fill:
            fillcolor=Fill.Color
        else:
            fillcolor=None
        alternativeText=self.AlternativeText
        if self.Tshape:
            self.Tshape.updateShape(Fillcolor=fillcolor,Text=Text,AltText=alternativeText)
        
    def Delete(self):
        self.Tablecanvas.deleteshape(self.Tshape)
        pass
    
    def ZOrder(self,zorder):
        self.ZOrder_val=zorder
    
    def set_activeflag(self,value):
        self.Active=value
        
    def get_activeflag(self):
        try:
            return self.Active
        except:
            self.Active=True
        return self.Active
    
    def Select(self):
        global Selection
        #self.Tablecanvas.setSelectedCells(self.TopLeftCell_Row, self.TopLeftCell_Row+1, self.TopLeftCell_Col, self.TopLeftCell_Col+1)
        self.Tablecanvas.setSelectedShapes(self)
        Selection=CSelection(None,ws=self.Worksheet)
        
    def get_visible(self):
        return self.Visible_val
    
    def set_visible(self, value):
        self.Visible_val=value
        self.Tshape.Visible = value
        if value==True:
            pass # redrawshape
        else:
            pass # removeshape

    Visible = property(get_visible, set_visible, doc='Visible Status')
    
    def get_name(self):
        return self.Name_val
    
    def set_name(self, value):
        self.Name_val=value
        self.Tshape.Name=value

    Name = property(get_name, set_name, doc='Shape-Name')

    def get_left(self):
        return self.Left_val
    
    def set_left(self, value):
        self.Left_val=value
        self.Tshape.Left=value

    Left = property(get_left, set_left, doc='Shape-Left')
    
    def get_top(self):
        return self.Top_val
    
    def set_top(self, value):
        self.Top_val=value
        self.Tshape.Top=value

    Top = property(get_top, set_top, doc='Shape-Top')    
    
    def get_TopLeftCell(self):
        TopLeftCell= CRange(self.TopLeftCell_Row,self.TopLeftCell_Col)
        return TopLeftCell
    
    def set_TopLeftCell(self, value):
        pass
    
    TopLeftCell = property(get_TopLeftCell, set_TopLeftCell, doc='Shape-Name')

    
    
class CCellDict(object):
    def __init__ (self,ws=None):
        #data = {}
        self.ws = ws
        
    def __getitem__(self, k):
        #print("Getitem",k)
        return Cells(k[0],k[1],ws=self.ws)
        
    def __setitem__(self,k,value):
        cell = Cells(k[0],k[1],ws=self.ws)
        cell.set_value(value)
        
class CRowDict(object):
    def __init__ (self,ws=None):
        #data = {}
        self.ws = ws
        
    def __getitem__(self, k):
        #print("Getitem",k)
        if self.ws == None:
            self.ws= ActiveSheet
        return self.ws.Rows(k)
        
    def __setitem__(self,k,value):
        if self.ws == None:
            self.ws= ActiveSheet
        self.ws.RowDict[k] = value
        
        #print("CRowDict.Setitem",k, value)
        
class CRangeDict(object):
    def __init__ (self,ws=None):
        self.ws = ws
        
    def __getitem__(self, k):
        #print("Getitem",k)
        if self.ws == None:
            self.ws= ActiveSheet
        return Range(k)
        
    def __setitem__(self,k,value):
        p_range=Range(k)
        p_range.Value=value
        
class CWorksheetFunction(object):
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
        
    def Power(self, p1,p2):
        return p1 ** p2
    
    def Max(self,*args):
        maxval=0
        for argvalue in args:
            value=val(argvalue)
            if value>maxval:
                maxval=value
        return maxval
        
        
class CApplication(object):
    def __init__(self):
        self.StatusBar = ""
        self.EnableEvents = True
        self.ScreenUpdating = True
        self.EnableCalculation = True
        self.Calculation = xlCalculationAutomatic
        self.Top = 0
        self.Left = 0
        self.Width = 1000 #*HL
        self.Height = 500 #*HL
        self.Version = "15"
        self.WindowState = 0
        self.Caller=""
        self.canvas_leftclickcmd=None
        self.LanguageSettings = CLanguageSettings()
        self.hWnd = 0
        self.WorksheetFunction = CWorksheetFunction()
        
    def set_canvas_leftclickcmd(self,cmd):
        self.canvas_leftclickcmd=cmd
        
        
    def OnTime(self,time,cmd):
        #print("Application OnTime:",time,cmd)
        global_controller.after(time,cmd)
        return
    
    def RoundUp(self,v1,v2):
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
    
    def International(self,param):
        if param == xlDecimalSeparator:
            return ","
        
    def Intersect(self,rng1,rng2):
        
        if type(rng1)==CRange:
            rowrange1 = (rng1.start[0],rng1.end[0])
            colrange1 = (rng1.start[1],rng1.end[1])
        else:
            rowrange1 = rng1.rowrange
            colrange1 = rng1.colrange
            
        if type(rng2)==CRange:
            rowrange2 = (rng2.start[0],rng2.end[0])
            colrange2 = (rng2.start[1],rng2.end[1])
        else:
            rowrange2 = rng2.rowrange
            colrange2 = rng2.colrange        
        
        #get rowrange intersection
        rowintersect=(max(rowrange1[0],rowrange2[0]),
                      min(rowrange1[1],rowrange2[1])+1)
                      
        colintersect=(max(colrange1[0],colrange2[0]),
                      min(colrange1[1],colrange2[1])+1)
        
        newrowrange=None
        if rowintersect[0]<rowintersect[1]:
            newrowrange=rowintersect
            
        newcolrange=None
        if colintersect[0]<colintersect[1]:
            newcolrange=colintersect
            
        if newcolrange !=None and newrowrange!=None:
            return CRange((newrowrange[0],newcolrange[0]),(newrowrange[1],newcolrange[1]))
        else:
            return None

    
    def setActiveWorkbook(self,workbookName):
         
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

class CLanguageSettings(object):
    def __init__(self):
        id = -1
        
    def LanguageID(self,id):
        if id == msoLanguageIDUI:
            lngconfstr = global_controller.getConfigData("language")
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
        
class CFont(object):
    def __init__(self,name="Font",size=8,shapetype=msoTextBox,shape=None):
        self.Name = name
        self.Size = size
        self.Shapetype= shapetype
        self.Color="#000000"
        self.Bold=False
        self.Italic=False
        self.Underline=- 4142
        self.Fill = CFill(self.Color,shape=shape)
        
class CSelectedSheets(object):
    def _init__(self):
        pass
        
class CActiveWindow(object):
    def __init__(self):
        self.Zoom = 100
        self.ScrollColumn = 1
        self.SelectedSheets = {}
        self.SelectedSheets["Count"]=1
        
class SoundLines(object):
    def __init__(self):
        self.dict = {}
        self.Count = 0
        self.keys = []
    
    def Exists(self,Channel:int):
        pass
    
    def Add(Channel, Pin_playerClass):
        pass
    
class CCharacters(object):
    def __init__(self,text="",shape=None):
        self.Shape=shape
        #self.Text = text
        #self.Textrange.Text=text
        
    def get_text(self):
        return self.Shape.Text
    
    def set_text(self, value):
        
        self.Shape.Text=value
        
        if self.Shape.Tshape:
            self.Shape.Tshape.Text=value

    Text = property(get_text, set_text, doc='Character-Text')        

class CTextRange(object):
    def __init__(self,text="",shape=None):
        self.Shape=shape
        self.Characters = CCharacters(text=text,shape=shape)
        #self.Text = text
        self.Font = CFont(shape=shape)
        
    def get_text(self):
        if self.Shape.Tshape:
            text=self.Shape.Tshape.Text
        else:
            if hasattr(self.Shape,"Text"):
                text=self.Shape.Text
            else:
                text=""
        return text
    
    def set_text(self, value):
        
        self.Shape.Text=value
        
        if self.Shape.Tshape:
            self.Shape.Tshape.Text=value

    Text = property(get_text, set_text, doc='Character-Text')             

class CTextFrame2(object):
    def __init__(self,text="",shape=None):
        self.TextRange = CTextRange(text=text,shape=shape)
    
class CButton(object):
    def __init__(self,name,shape=None):
        self.Shape = shape
        self.Name=name
        self.AlternativeText = ""
        self.TextFrame2 = CTextFrame2(shape=shape)
        self.Fill = (0,0,0)

        
class CControl(object):
    def __init__(self,value):
        self.Value=value

        
def rgb2tkcolor(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

def tkcolor2rgb(color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    return (r,g,b)

def tkcolor2int(color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    colorint=(b*256+g)*256+r
    return colorint

def int2tkcolor(colorVal):
    if type(colorVal)==int:
        if colorVal<0:
            _fn_return_value=""
        r=colorVal % 256
        g=(colorVal // 256 )  % 256
        b=colorVal // 65536
        _fn_return_value = f'#{r:02x}{g:02x}{b:02x}'
    else:
        _fn_return_value=colorVal
    return _fn_return_value

def get_global_controller():
    return ActiveWorkbook.controller

# global variables

ActiveWorkbook = None # :CWorkbook
 
ActiveSheet = None #:CWorksheet

#WorksheetFunction = CWorksheetFunction()

Application = CApplication() #:CApplication

CellDict = CCellDict() # alias for Cells[] 

RowDict = CRowDict() # alias for Rows[]

RangeDict = CRangeDict() # alias for Range[]

Workbooks =[]

Worksheets = []

ActiveWindow = CActiveWindow()

global_controller = None

Now = 0

def get_selection(self):
    
    return ActiveSheet.get_selection()

def set_selection(self, value):
    ActiveSheet.get_selection().Value=value
    

Selection = CSelection() #property(get_selection, set_selection, doc='Selection') 

#---------------------------------------
# Event
#---------------------------------------
def Workbook_Open(workbook):
    # Occurs when the workbook is opened.
    pass

def Workbook_Activate(workbook):
    # Occurs when a workbook, worksheet, chart sheet, or embedded chart is activated.
    pass

def Worksheet_Activate(workbook):
    # Occurs when a workbook, worksheet, chart sheet, or embedded chart is activated.
    pass



    





