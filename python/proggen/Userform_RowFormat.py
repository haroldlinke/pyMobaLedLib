from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as X02
#import ExcelAPI.XLC_Excel_Consts as X01
#import pattgen.M01_Public_Constants_a_Var as M01
#import pattgen.M09_Language as M09
#import pattgen.M08_Load_Sheet_Data
#import pattgen.M07_Save_Sheet_Data
#import pattgen.M30_Tools as M30
#import pattgen.M65_Special_Modules
#import pattgen.M80_Multiplexer_INI_Handling
import mlpyproggen.Prog_Generator as PG



import tkinter as tk
from tkinter import ttk

import logging

import tkinter as tk
from tkinter import ttk
import mlpyproggen.Prog_Generator as PG
import proggen.M09_Language as M09



class UserForm_RowFormat:
    
    def __init__(self):
        self.title = M09.Get_Language_Str("Zeilen Formatieren")
        self.tabClassName = "RowFormatPage"
        self.label1_txt = M09.Get_Language_Str("Zeile1")
        self.label2_txt = M09.Get_Language_Str("Zeile2")
        #self.label3_txt = "Der Dialog muss dazu nicht beendet werden.Zusätzliche Zeilen können mit der Schaltfläche ""Zeile einfügen"" hinzugefügt werden. Wenn die Zeile bereits Daten enthält, dann werden diese ab der ausgewählten Position vervollständigt. "
        self.controller = PG.get_global_controller()
        self.IsActive = False
        self.button1_txt = M09.Get_Language_Str("Abbrechen")
        self.button2_txt = M09.Get_Language_Str("Ok")
        self.Userform_res = ""
        self.default_font = self.controller.defaultfontnormal
        self.default_fontsmall = self.controller.defaultfontsmall
        self.default_fontlarge = self.controller.defaultfontlarge        
 
 
    def ok(self, event=None):
        self.IsActive = False
        #value = self.TextBox.get("1.0","end-1c")

        self.Userform_res = self.controller.get_macroparam_var_values("RowFormatPage")
        self.top.destroy()
        
 
    def cancel(self, event=None):
        self.Userform_res = '<Abort>'
        self.IsActive = False
        self.top.destroy()
        

    def ShowForm(self, userdata_dict):
        
        self.top = tk.Toplevel(self.controller)
        self.top.transient(self.controller)
        
        #self.TextBox = tk.Text(self.top,height=20,width=40,wrap="word")
        #self.TextBox.insert("end",Txt)
        config_frame = self.controller.create_macroparam_frame(self.top,self.tabClassName, maxcolumns=3,startrow =1,style="CONFIGPage")   
        self.top.resizable(False, False)  # This code helps to disable windows from resizing
        
        
        
        # winfo_x = PG.global_controller.winfo_x()
        # winfo_y = PG.global_controller.winfo_y()
        
        # window_height = self.top.winfo_y() # 800
        # window_width = self.top.winfo_x() #
        
        # screen_width = PG.global_controller.winfo_width()
        # screen_height = PG.global_controller.winfo_height()
        
        # x_cordinate = winfo_x+int((screen_width/2) - (window_width/2))
        # y_cordinate = winfo_y+int((screen_height/2) - (window_height/2))
                
        #self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))     
        
        if len(self.title) > 0: self.top.title(self.title)
        #self.label1 = ttk.Label(self.top, text=self.label1_txt,wraplength=window_width/10-20,font=self.default_font)
        #self.label2 = ttk.Label(self.top, text=self.label2_txt,wraplength=window_width/20,font=self.default_font,foreground="#0000FF")
        #self.label3 = ttk.Label(self.top, text=self.label3_txt,wraplength=window_width,font=("Tahoma", 11))
        #self.label1.grid(row=0,column=0,columnspan=1,sticky="nesw",padx=10,pady=10)
        #self.label3.grid(row=2,column=0,columnspan=3,sticky="nesw",padx=10,pady=10)
        config_frame.grid(row=1,column=0,sticky="nesw",padx=10,pady=10)
        
        #self.label2.grid(row=2,column=0,columnspan=1,rowspan=1,sticky="nesw",padx=10,pady=10)

        self.top.bind("<Return>", self.ok)
        self.top.bind("<Escape>", self.cancel)
        self.button_frame = ttk.Frame(self.top)
        
        self.b_cancel = tk.Button(self.button_frame, text=self.button1_txt, command=self.cancel,width=10,font=self.default_font)
        self.b_ok = tk.Button(self.button_frame, text=self.button2_txt, command=self.ok,width=10,font=self.default_font)

        self.b_cancel.grid(row=0,column=0,sticky="e",padx=10,pady=10)
        self.b_ok.grid(row=0,column=1,sticky="e",padx=10,pady=10)
        
        self.button_frame.grid(row=3,column=0,sticky="e",padx=10,pady=1)
        
        self.IsActive = True
        self.top.wait_visibility()
        self.top.takefocus = True
        self.top.focus_set()
        self.top.focus_force()
        self.top.grab_set()
        #self.TextBox.focus_set()
        self.controller.wait_window(self.top)


        return self.Userform_res
        
