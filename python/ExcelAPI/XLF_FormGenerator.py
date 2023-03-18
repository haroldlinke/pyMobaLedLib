# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
# * Author: Harold Linke
# * Date: January 1st, 2020
# * Copyright: Harold Linke 2020
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 10.03.2020 - Harold Linke - first release
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

from vb2py.vbfunctions import *
# fromx vb2py.vbdebug import *
import tkinter as tk
from tkinter import ttk
import os
import sys
import ExcelAPI.XLW_Workbook as X02
import pattgen.M09_Language as M09


# ##########################################################
# Generate Forms
# ##########################################################

guifactor  = 1.55

class CControl_Template(object):
    
    def __init__(self,TK_widget=None,Dlg=None,Name="",Accelerator="",BackColor="#00000F",BorderColor="#000006",
                 BorderStyle="fmBorderStyleNone",Caption="",Command=None,ControlTipText="",
                 ForeColor="#000012",Height=0,Left=0,Top=0,Type="",Value=0,Visible=True,Width=0):
        self.Dlg=Dlg
        self.Name=Name
        self.Accelerator=Accelerator
        self.BackColor=BackColor
        self.BorderColor=BorderColor
        self.BorderStyle=BorderStyle
        self.Caption=Caption
        self.Command=Command
        self.ControlTipText=ControlTipText
        self.ForeColor=ForeColor
        self.Height=Height
        self.Left=Left
        self.Top=Top
        self.Type=Type
        self.Visible=Visible
        self.Width=Width
        self.list_choices=[]
        self.TKVar=None
        self.TKWidget=None
        self.Controls=[]
        self.Enabled = True
        
    def get_value(self):
        if self.TKVar:
            return self.TKVar.get()
        return None
    
    def set_value(self,value):
        self.TKVar.set(value)
    
    Value = property(get_value, set_value, doc='value of Form')
    
    def get_ListCount(self):
        #print("ListCount")
        return len(self.list_choices)
    def set_ListCount(self,value):
        pass
    ListCount = property(get_ListCount, set_ListCount, doc='value of Form')
    def Clear(self):
        #print("Clear ListBox")
        self.list_choices=[]
        self.TKVar.set(self.list_choices)
    def AddItem(self,value):
        #print("AddItem:",value)
        self.list_choices.append(value)
        self.TKVar.set(self.list_choices)
    def setFocus(self):
        #print("SetFocus:")
        pass
    def Selected(self,nr):
        return self.TKWidget.selection_includes(nr)

    def List(self,nr,col):
        res_line = self.list_choices[nr]
        res_split = str.split(res_line,":")
        return res_split[0]

def ToolTip(widget,text="", key="",button_1=False):
    if text:
        tooltiptext = text
    else:
        tooltiptext = ""
    tooltip_var = None
    try:
        tooltip_var = widget.tooltip
    except:
        tooltip_var = None
        
    if tooltip_var==None:
        tooltip_var=X02.global_controller.ToolTip(widget, text=tooltiptext,button_1=button_1)
        widget.tooltip = tooltip_var
    else:
        tooltip_var.unschedule()
        tooltip_var.hide()
        tooltip_var.update_text(text)            
    return    

def generate_controls(comp_list,parent,dlg):
    gui_factor_label_width = guifactor
    gui_factor_label_height = guifactor
    gui_factor_pos = guifactor
    
    if comp_list != None:
        for component_dict in comp_list:
            comp=CControl_Template(Dlg=dlg)
            #dlg.Controls.append(comp)
            comp.Name = component_dict.get("Name","")
            comp.Type = component_dict.get("Type","")
            comp.Persistent = component_dict.get("Persistent",False)
            comp.Caption = M09.Get_Language_Str(component_dict.get("Caption",""))
            comp.AlternativeText = component_dict.get("AlternativeText","")
            width = component_dict.get("Width",0)
            height = component_dict.get("Height",0)
            if type(width)==int:
                comp.Width = int(width * gui_factor_label_width)
                comp.Height = int(height * gui_factor_label_height)
            else:
                comp.Width = width
                comp.Height = height
            comp.Wraplength = 0 # comp.Width-10
            comp.Top = int(component_dict.get("Top",0) * gui_factor_pos)
            comp.Left = int(component_dict.get("Left",0) * gui_factor_pos)
            #comp_font = self.fontlabel
            comp.ControlTipText = component_dict.get("ControlTipText","")
            dlg.AddControl(comp)
            
            if comp.Type == "MultiPage":
                mp_comp_list = component_dict.get("Components",[])
                container = ttk.Notebook(parent)
                container.place(x=comp.Left,y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=container
                for page_dict in mp_comp_list:
                    page=CControl_Template(Dlg=dlg)
                    page.Type = page_dict["Type"]
                    if page.Type == "Page":
                        page.Name = page_dict.get("Name","")
                        page.Caption = M09.Get_Language_Str(page_dict.get("Caption",""))
                        page_frame = tk.Frame(container)
                        container.add(page_frame, text=page.Caption)
                        page.TKWidget=page_frame
                        page_comp = page_dict.get("Components",[])
                        dlg.AddControl(page)
                        generate_controls(page_comp,page_frame,dlg=dlg)
            elif comp.Type == "Label":
                comp.Textalign = component_dict.get("TextAlign","")
                if comp.Textalign == "fmTextAlignLeft":
                    anchor="nw"
                    justify=tk.LEFT
                elif comp.Textalign == "fmTextAlignRight":
                    anchor="ne"
                    justify=tk.RIGHT
                else:
                    anchor="n"
                    justify=tk.CENTER
                label=tk.Label(parent, text=comp.Caption,anchor=anchor, justify=justify,width=comp.Width,height=comp.Height,wraplength = comp.Wraplength) #,font=comp_font)
                label.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=label
                if comp.ControlTipText!="":
                    ToolTip(label, text=comp.ControlTipText)
            elif comp.Type == "CommandButton":
                comp.Command = component_dict.get("Command",None)
                comp.Accelerator = component_dict.get("Accelerator","")
                comp.icon = component_dict.get("IconName","")
                if comp.Accelerator!="":            
                    parent.bind(comp.Accelerator, Command)   
                    
                if comp.icon != "":
                    filename = r"/images/"+comp.icon
                    filedir = os.path.dirname(os.path.realpath(__file__))
                    filedir2 = os.path.dirname(filedir)                    
                    filepath = filedir2 + filename
                    comp.iconImage = tk.PhotoImage(file=filepath)
                    button=tk.Button(parent, text=comp.Caption,command=comp.Command,width=comp.Width,height=comp.Height,wraplength = comp.Wraplength,image=comp.iconImage,anchor="nw")
                else:
                    button=tk.Button(parent, text=comp.Caption,command=comp.Command,width=comp.Width,height=comp.Height,wraplength = comp.Wraplength)
                button.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=button
                if comp.ControlTipText!="":
                    ToolTip(button, text=comp.ControlTipText)
                pass
            elif comp.Type == "CheckBox":
                comp.TKVar = tk.IntVar(value=0)
                setattr(dlg,comp.Name,comp)
                #comp.Command = component_dict.get("Command",None)
                comp.Accelerator = component_dict.get("Accelerator","")
                #if comp.Accelerator!="":
                #    parent.bind(comp.Accelerator, Command)                    
                checkbutton=tk.Checkbutton(parent, text=comp.Caption,width=comp.Width,wraplength = comp.Wraplength,anchor="w",variable=comp.TKVar,onvalue = 1, offvalue = 0)
                checkbutton.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=checkbutton
                if comp.ControlTipText!="":
                    ToolTip(checkbutton, text=comp.ControlTipText)
            elif comp.Type == "ListBox":
                comp.TKVar = tk.StringVar(value=[])
                setattr(dlg,comp.Name,comp)
                #comp.Command = component_dict.get("Command",None)
                #comp.Accelerator = component_dict.get("Accelerator","")
                #if comp.Accelerator!="":
                #    parent.bind(comp.Accelerator, Command)                    
                listbox=tk.Listbox(parent, height=comp.Height, width=comp.Width,listvariable=comp.TKVar)
                listbox.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=listbox
                if comp.ControlTipText!="":
                    ToolTip(listbox, text=comp.ControlTipText)                        
            elif comp.Type == "Frame":
                frame = ttk.LabelFrame(parent,text=comp.Caption,borderwidth=1,relief=tk.RIDGE)
                frame.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=frame
                frame_comp = component_dict.get("Components",[])
                generate_controls(frame_comp,frame,dlg=dlg)
                if comp.ControlTipText!="":
                    ToolTip(frame, text=comp.ControlTipText)                      
            elif comp.Type == "Page":
                mp_comp_list = component_dict["Components"]
                generate_controls(mp_comp_list, parent, dlg=dlg)
            else:
                pass
                   
def generate_form(form_dict,parent,dlg=None,modal=True):
    #create main window
    dlg.Controls=[]
    
    userform_dict = form_dict.get("UserForm",None)
    if userform_dict:
        top = tk.Toplevel(parent)
        top.transient(parent)
        if modal:
            top.grab_set()
        top.resizable(True, True)  # This code helps to disable windows from resizing
        
        window_height = int(userform_dict.get("Height",500)*guifactor)
        window_width = int(userform_dict.get("Width",600)*guifactor)
        
        winfo_x = X02.global_controller.winfo_x()
        winfo_y = X02.global_controller.winfo_y()
        
        screen_width = X02.global_controller.winfo_width()
        screen_height = X02.global_controller.winfo_height()
        
        x_cordinate = winfo_x+int((screen_width/2) - (window_width/2))
        y_cordinate = winfo_y+int((screen_height/2) - (window_height/2))
    
        top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))                 
        #self.top.geometry("+{}+{}".format(x_cordinate, y_cordinate))
        
        window_title = userform_dict.get("Caption","Title")
        
        top.title(M09.Get_Language_Str(window_title))
        
        components = userform_dict.get("Components",None)
        
        generate_controls(components,top,dlg=dlg)
        
        return top
    else:
        return None


