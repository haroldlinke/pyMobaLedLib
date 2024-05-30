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
import ExcelAPI.XLA_Application as X02
import proggen.M09_Language as M09
#import pattgen.D00_GlobalProcs as D00
#import tkcolorpicker.spinbox as SB
from scrolledFrame.ScrolledFrame import ScrolledFrame


# ##########################################################
# Generate Forms
# ##########################################################

guifactor  = 1.55
scrolledcontainer = None

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
        self.Init_Value=None

    def get_selection(self):
        sel_list = self.TKWidget.curselection()
        if sel_list == ():
            return 0
        if len(sel_list) == 1:
            return sel_list[0]
        return sel_list
    
    def set_selection(self,value):
        if value != None:
            self.TKWidget.select_clear(0, "end")
            if value != "":
                self.TKWidget.selection_set(value)
                self.TKWidget.activate(value)
    
    Selection = property(get_selection, set_selection, doc='Selected Entry of Listbox')

    def get_value(self):
        if self.TKVar != None:
            return self.TKVar.get()
        else:
            # textbox
            return self.TKWidget.get('1.0', 'end')
        return None
    
    def set_value(self,value):
        if self.TKVar != None:
            self.TKVar.set(value)
        else:
            # textbox
            self.TKWidget.delete('1.0', 'end')
            self.TKWidget.insert('end', value)
    
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
    
    def select(self, value):
        # select page of MultiPage
        self.TKWidget.select(value)
        
    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return("break")

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

def translate_text(text):
    trans = M09.Get_Language_Str(text)
    return trans

def generate_controls(comp_list,parent,dlg,persistent_controls={},format_dict={},defaultfont=("Calibri",10), jump_table={}, window=None):
    gui_factor_label_width = guifactor
    gui_factor_label_height = guifactor
    gui_factor_pos = guifactor
    
    if comp_list != None:
        for component_dict in comp_list:
            compName= component_dict.get("Name","")
            comp=CControl_Template(Dlg=dlg)
            #dlg.Controls.append(comp)
            comp.Name = component_dict.get("Name","")
            comp.Type = component_dict.get("Type","")
            comp.Default = component_dict.get("Default",None)
            comp.Persistent = component_dict.get("Persistent",comp.Default)
            comp.Init_Value = persistent_controls.get(comp.Name,None)
            if not comp.Init_Value:
                comp.Init_Value = component_dict.get("Value",None)
            comp.Caption = translate_text(component_dict.get("Caption",""))
            comp.AlternativeText = component_dict.get("AlternativeText","")
            comp.Font = component_dict.get("Font",defaultfont)
            comp.SpecialEffect = component_dict.get("SpecialEffect","")
            if comp.SpecialEffect == "fmSpecialEffectSunken":
                comp.relief = tk.SUNKEN
            else:
                comp.relief = tk.FLAT
            width = component_dict.get("Width",0)
            height = component_dict.get("Height",0)
            if type(width)==int:
                comp.Width = int(width * gui_factor_label_width)
                comp.Height = int(height * gui_factor_label_height)
            elif type(width) == float:
                comp.Width = int(width)
                comp.Height = int(height)                
            else:
                comp.Width = width
                comp.Height = height
            comp.Wraplength = comp.Width
            comp.Top = int(component_dict.get("Top",0) * gui_factor_pos)
            comp.Left = int(component_dict.get("Left",0) * gui_factor_pos)
            #comp_font = self.fontlabel
            comp.ControlTipText = component_dict.get("ControlTipText","")
            comp.format_dict = format_dict.get(comp.Name,None)
            
            comp.Command = component_dict.get("Command",None)
            if type(comp.Command) == str:
                if comp.Command != "":
                    comp.Command = jump_table.get(comp.Command,None)
#                    if comp.Command == None:
#                        comp.Command = D00.globalprocs.get(comp.Command,None)
                else:
                    # test standard command "Name_clicked"
                    command_str = comp.Name + "_Click"
                    if hasattr(dlg, command_str):
                        comp.Command = getattr(dlg, command_str)
                    else:
                        comp.Command = None
            comp.Accelerator = component_dict.get("Accelerator","")
            comp.icon = component_dict.get("IconName","")            
            
            dlg.AddControl(comp)
            
            #****************************************************
            #* MultiPage
            #****************************************************
            if comp.Type == "MultiPage":
                mp_comp_list = component_dict.get("Components",[])
                container = ttk.Notebook(parent)
                container.place(x=comp.Left,y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=container
                setattr(dlg,comp.Name,comp)
                for page_dict in mp_comp_list:
                    page=CControl_Template(Dlg=dlg)
                    page.Type = page_dict["Type"]
                    if page.Type == "Page":
                        page.Name = page_dict.get("Name","")
                        page.Caption = translate_text(page_dict.get("Caption",""))
                        page_frame = tk.Frame(container)
                        container.add(page_frame, text=page.Caption)
                        page.TKWidget=page_frame
                        page_comp = page_dict.get("Components",[])
                        dlg.AddControl(page)
                        generate_controls(page_comp,page_frame,dlg=dlg, jump_table=jump_table, defaultfont=defaultfont)
            #****************************************************
            #* Label
            #****************************************************                        
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
                comp.TKVar = tk.StringVar(value=comp.Caption)
                label=tk.Label(parent, textvariable=comp.TKVar, anchor=anchor, justify=justify,width=comp.Width,height=comp.Height,wraplength = comp.Wraplength,font=comp.Font, relief=comp.relief) #,font=comp_font)
                label.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=label
                setattr(dlg,comp.Name,comp)
                if comp.ControlTipText!="":
                    ToolTip(label, text=comp.ControlTipText)
            #****************************************************
            #* Image
            #****************************************************                        
            elif comp.Type == "Image":
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
                comp.icon = component_dict.get("IconName","")
                if comp.icon != "":
                    filename = r"/images/"+comp.icon
                    filedir = os.path.dirname(os.path.realpath(__file__))
                    filedir2 = os.path.dirname(filedir)
                    filepath = filedir2 + filename
                    comp.iconImage = tk.PhotoImage(file=filepath)
                label=tk.Label(parent, text=comp.Caption,anchor=anchor, image=comp.iconImage, justify=justify,width=comp.Width,height=comp.Height,wraplength = comp.Wraplength,font=comp.Font, relief=comp.relief) #,font=comp_font)
                label.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=label
                setattr(dlg,comp.Name,comp)
                if comp.ControlTipText!="":
                    ToolTip(label, text=comp.ControlTipText)                    
            #****************************************************
            #* CommandButton
            #****************************************************                   
            elif comp.Type == "CommandButton":
                if comp.Accelerator!="":
                    if window:
                        window.bind(comp.Accelerator, comp.Command)
                if comp.icon != "":
                    filename = r"/images/"+comp.icon
                    filedir = os.path.dirname(os.path.realpath(__file__))
                    filedir2 = os.path.dirname(filedir)                    
                    filepath = filedir2 + filename
                    comp.iconImage = tk.PhotoImage(file=filepath)
                    button=tk.Button(parent, text=comp.Caption,command=comp.Command,width=comp.Width,height=comp.Height,wraplength = comp.Wraplength,image=comp.iconImage,font=comp.Font)
                else:
                    button=tk.Button(parent, text=comp.Caption,command=comp.Command,width=comp.Width,height=comp.Height,wraplength = comp.Wraplength, font=comp.Font)
                button.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=button
                setattr(dlg,comp.Name,comp)
                if comp.ControlTipText!="":
                    ToolTip(button, text=comp.ControlTipText)
                pass
            #****************************************************
            #*CheckBox
            #****************************************************                   
            elif comp.Type == "CheckBox":
                if comp.Init_Value:
                    init_value=comp.Init_Value
                else:
                    init_value=0
                comp.TKVar = tk.IntVar(value=init_value)
                setattr(dlg,comp.Name,comp)
                #comp.Command = component_dict.get("Command",None)
                comp.Accelerator = component_dict.get("Accelerator","")
                #if comp.Accelerator!="":
                #    parent.bind(comp.Accelerator, Command)                    
                checkbutton=tk.Checkbutton(parent, text=comp.Caption,width=comp.Width,wraplength = comp.Wraplength,anchor="w",variable=comp.TKVar,onvalue = 1, offvalue = 0,font=comp.Font)
                checkbutton.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=checkbutton
                if comp.ControlTipText!="":
                    ToolTip(checkbutton, text=comp.ControlTipText)
        
            #****************************************************
            #* TextBox
            #****************************************************                   
            elif comp.Type == "TextBox":
                textbox=tk.Text(parent, width=comp.Width,height=comp.Height,wrap= tk.WORD,font=comp.Font,relief=comp.relief)
                if comp.Caption != None:
                    textbox.insert("1.0",comp.Caption)
                charformat_dict = component_dict.get("CharFormat",None)
                if charformat_dict==None:
                    charformat_dict=comp.format_dict # shape individual formats
                if charformat_dict:
                    for index in charformat_dict.keys():
                        startidx = index[0]
                        endidx = index[1]
                        if type(startidx)==int:
                            endidx  = "1.0+"+str(startidx+endidx-2)+"c"
                            startidx= "1.0+"+str(startidx-1)+"c"
                        tagname = "tag"+str(startidx)+str(endidx)
                        textbox.tag_add(tagname, startidx,endidx)
                        charformat=charformat_dict.get(index,None)
                        if type(charformat)==tuple: # old version
                            textbox.tag_config(tagname, font=charformat)
                        else:
                            if charformat:
                                if charformat.Font:
                                    font=textbox.cget("font")+" "+charformat.Font
                                    textbox.tag_config(tagname, font=font)
                                if charformat.ForeGround:
                                    textbox.tag_config(tagname, foreground=charformat.ForeGround)
                #textbox.config(state=tk.DISABLED)
                textbox.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                setattr(dlg,comp.Name,comp)
                comp.TKWidget=textbox
                if comp.ControlTipText!="":
                    ToolTip(textbox, text=comp.ControlTipText)

            #****************************************************
            #* NumBox
            #****************************************************                   
            elif comp.Type == "NumBox":
                if comp.Init_Value:
                    init_value=comp.Init_Value
                else:
                    init_value=0
                comp.TKVar = tk.IntVar(value=init_value)
                setattr(dlg,comp.Name,comp)
                numbox=ttk.Spinbox(parent, from_=0,to=65535,textvariable=comp.TKVar, command=comp.Command, width=comp.Width ,font=comp.Font)
                #if comp.Caption != None and comp.Caption != "":
                #    textbox.insert("1.0",comp.Caption)
                numbox.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=numbox
                if comp.ControlTipText!="":
                    ToolTip(numbox, text=comp.ControlTipText)
            #****************************************************
            #* ListBox
            #****************************************************                   
            elif comp.Type == "ListBox":
                if comp.Init_Value:
                    init_value=comp.Init_Value # list of values
                else:
                    init_value=[]                
                comp.TKVar = tk.StringVar(value=init_value)
                setattr(dlg,comp.Name,comp)
                #comp.Command = component_dict.get("Command",None)
                #comp.Accelerator = component_dict.get("Accelerator","")
                #if comp.Accelerator!="":
                #    parent.bind(comp.Accelerator, Command)                    
                listbox=tk.Listbox(parent, height=comp.Height, width=comp.Width,listvariable=comp.TKVar,font=comp.Font,relief=comp.relief, exportselection = 0, selectmode=tk.SINGLE)
                listbox.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=listbox
                comp.Selection = component_dict.get("Selection",None)
                if comp.ControlTipText!="":
                    ToolTip(listbox, text=comp.ControlTipText)
            #****************************************************
            #* Frame
            #****************************************************                   
            elif comp.Type == "Frame":
                frame = ttk.LabelFrame(parent,text=comp.Caption,borderwidth=1,relief=tk.RIDGE)
                frame.place(x=comp.Left, y=comp.Top,width=comp.Width,height=comp.Height)
                comp.TKWidget=frame
                setattr(dlg,comp.Name,comp)
                frame_comp = component_dict.get("Components",[])
                generate_controls(frame_comp,frame,dlg=dlg, jump_table=jump_table, defaultfont=defaultfont)
                if comp.ControlTipText!="":
                    ToolTip(frame, text=comp.ControlTipText)
            #****************************************************
            #* Page
            #****************************************************                   
            elif comp.Type == "Page":
                mp_comp_list = component_dict["Components"]
                generate_controls(mp_comp_list, parent, dlg=dlg, jump_table=jump_table)
            else:
                pass
            comp.TKWidget.bind("<Tab>", comp.focus_next_widget)
            
            
def generate_form(form_dict,parent,dlg=None,modal=True, jump_table={}, defaultfont=("Calibri",10)):
    #create main window
    global scrolledcontainer
    dlg.Controls=[]
    
    userform_dict = form_dict.get("UserForm",None)
    if userform_dict:
        top = tk.Toplevel(parent)
        top.transient(parent)
        if modal:
            top.grab_set()
        top.resizable(True, True)  # This code helps to disable windows from resizing
        
        orig_window_height = int(userform_dict.get("Height",500)*guifactor)
        orig_window_width = int(userform_dict.get("Width",600)*guifactor)
        
        winfo_x = X02.global_controller.winfo_x()
        winfo_y = X02.global_controller.winfo_y()
        
        screen_width = X02.global_controller.winfo_width()
        screen_height = X02.global_controller.winfo_height()
        
        if screen_height < orig_window_height:
            window_height = screen_height
        else:
            window_height = orig_window_height
        if screen_width < orig_window_width:
            window_width = screen_width
        else:
            window_width = orig_window_width
        
        x_cordinate = winfo_x+int((screen_width/2) - (window_width/2))
        y_cordinate = winfo_y+int((screen_height/2) - (window_height/2))
    
        top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        #self.top.geometry("+{}+{}".format(x_cordinate, y_cordinate))
        
        window_title = userform_dict.get("Caption","Title")
        
        top.title(translate_text(window_title))
        
        scrolledcontainer = ScrolledFrame(top)
        scrolledcontainer.grid(row=0,column=0, rowspan=1,columnspan=2, sticky="nesw")
        scrolledcontainer.grid_rowconfigure(0, weight=1)
        scrolledcontainer.grid_columnconfigure(0, weight=1)        
        top.grid_rowconfigure(0,weight=1)
        top.grid_columnconfigure(0, weight=1)
        
        components = userform_dict.get("Components",None)
        
        container = tk.Frame(scrolledcontainer.interior, width=orig_window_width-30, height=orig_window_height-30)
        container.grid(row=0,column=0,columnspan=2,sticky="nesw")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        generate_controls(components,container,dlg=dlg, jump_table=jump_table, defaultfont=defaultfont, window=top)
        
        return top
    else:
        return None


