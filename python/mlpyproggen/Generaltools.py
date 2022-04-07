# -*- coding: utf-8 -*-
#
#         MobaLedCheckColors: Color checker for WS2812 and WS2811 based MobaLedLib
#
#         DefaultData
#
# * Version: 1.25
# * Author: Harold Linke
# * Date: January 04th, 2020
# * Copyright: Harold Linke 2020
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

def set_macroparam_var(self, macro, paramkey,variable):
    paramdict = self.controller.macroparams_var.get(macro,{})
    if paramdict == {}:
        self.controller.macroparams_var[macro] = {}
        self.controller.macroparams_var[macro][paramkey] = variable
    else:
        paramdict[paramkey] = variable

def create_macroparam_content(self,parent_frame, macro, macroparams,extratitleline=False,maxcolumns=5, startrow=0, minrow=4):
    
    MACROLABELWIDTH = 15
    MACRODESCWIDTH = 20
    MACRODESCWRAPL = 120
    
    PARAMFRAMEWIDTH = 105
    
    PARAMLABELWIDTH = 15
    PARAMLABELWRAPL = 100        
    
    PARAMSPINBOXWIDTH = 6
    PARAMENTRWIDTH = 16
    PARAMCOMBOWIDTH = 16
    
    STICKY = "nw"
    
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
        paramconfig_dict = self.get_param_config_dict(paramkey)
        param_min = paramconfig_dict.get("Min",0)
        param_max = paramconfig_dict.get("Max",255)
        param_title = paramconfig_dict.get("Input Text","")
        param_tooltip = paramconfig_dict.get("Hint","")
        param_default = paramconfig_dict.get("Default","")
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
            
            s_paramvar = Spinbox(parent_frame, from_=param_min, to=param_max, width=PARAMSPINBOXWIDTH, name='spinbox', textvariable=paramvar)
            s_paramvar.delete(0, 'end')
            s_paramvar.insert(0, param_default)
            s_paramvar.grid(row=row+valuerow, column=column+valuecolumn, padx=2, pady=2)
            s_paramvar.key = paramkey
        
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
            paramvar.delete(0, 'end')
            paramvar.insert(0, param_default)
            paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
            paramvar.key = paramkey
        
            self.set_macroparam_var(macro, paramkey, paramvar)                

            column = column + deltacolumn
            if column > maxcolumns:
                column = 0
                row=row+deltarow
        
        if param_type == "Text": # Text value param
            
            label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
            label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
            self.controller.ToolTip(label, text=param_tooltip)
            
            
            paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH*3)
            paramvar.delete(0, 'end')
            paramvar.insert(0, param_default)
            paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
            paramvar.key = paramkey
        
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
            combo_value_list = list(self.controller.ledgrouptable.keys())
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
            logging.debug  (macro,param_type)
            if row >1 or column>0: 
                row += deltarow
                column = 0
            
            label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
            label.grid(row=row+titlerow, column=column+titlecolumn, rowspan=2, sticky=STICKY, padx=2, pady=2)
            self.controller.ToolTip(label, text=param_tooltip)                
            
            multipleparam_frame = ttk.Frame(parent_frame)
            multipleparam_frame.grid(row=row,column=column+1 ,columnspan=6,sticky='nesw', padx=0, pady=0)
            
            multipleparams = paramconfig_dict.get("MultipleParams",[])
            
            if multipleparams != []:
                self.create_macroparam_content(multipleparam_frame,macro, multipleparams,extratitleline=True,maxcolumns=maxcolumns-1,minrow=0)
                
            separator = ttk.Separator (parent_frame, orient = tk.HORIZONTAL)
            separator.grid (row = row+2, column = 0, columnspan= 10, padx=2, pady=2, sticky = "ew")
   
            column = column + deltacolumn
            column = 0
            row=row+3
            
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
    
    if (column<maxcolumns+1) and (column>0):
        for i in range(column,maxcolumns+1):
            label=tk.Label(parent_frame, text=" ",width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL)
            label.grid(row=row,column=i,sticky=STICKY, padx=2, pady=2)
    
    if maxcolumns > 5:        
        seplabel=tk.Label(parent_frame, text="",width=90,height=1)
        seplabel.grid(row=row+2, column=0, columnspan=10,sticky='ew', padx=2, pady=2)
            

def create_macroparam_frame(self,parent_frame, macro):
    
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

    macrodata = self.controller.MacroDef.data.get(macro,{})
    Macrotitle = macro
    
    Macrolongdescription = macrodata.get("Ausführliche Beschreibung","")
    Macrodescription = macrodata.get("Kurzbeschreibung","")
    
    if Macrolongdescription =="":
        Macrolongdescription = Macrodescription
    macroldlabel = scrolledtext.ScrolledText(macroparam_frame, wrap='word', bg=self.cget('bg'), borderwidth=2,relief="ridge",width=108,height=5)
    macroldlabel.grid(row=0, column=0, columnspan=2,padx=0, pady=0,sticky="w")
    macroldlabel.delete("1.0", "end")
    macroldlabel.insert("end", Macrolongdescription)
    macroldlabel.yview("1.0")
    macroldlabel.state = "DISABLED"
                   
    macrolabel = tk.Button(macroparam_frame, text=Macrotitle, width=MACROLABELWIDTH, height=2, wraplength=150,relief="raised", background="white",borderwidth=1,command=lambda: self._macro_cmd(macrokey=macro))
    macrolabel.grid(row=1, column=0, sticky="nw", padx=4, pady=4)
    macrolabel.key=macro
    self.controller.ToolTip(macrolabel, text=Macrodescription)
    
    """in_button_cnt_str = macrodata.get("InCnt","0")
    if str.isdigit(in_button_cnt_str):
        in_button_cnt = int(in_button_cnt_str)
    else:
        in_button_cnt = 0
    
    if in_button_cnt > 0:
        inbuttoncolorlist = macrodata.get("ButtonColor",["green","red","yellow"]) 
        inbuttontextlist = macrodata.get("ButtonText",["On","Off","xx"]) 
        in_button_frame =  ttk.Frame(macroparam_frame, relief="ridge", borderwidth=1)
        in_button_frame.grid(row=2, column=0, sticky="nesw", padx=4, pady=4)
    
        for i in range(0,in_button_cnt): # create switch buttons
            
            row = i
            index = int(i/2)
                           
            inbuttoncolor1 = inbuttoncolorlist[index]
            inbuttontext1 = inbuttontextlist[index]
            
            inbuttonlabel1 = tk.Button(in_button_frame, text=inbuttontext1, width=BUTTONLABELWIDTH, height=1, relief="raised", background=inbuttoncolor1,borderwidth=1,command=lambda: self._button_cmd(macrokey=macro,button=i*2))
            inbuttonlabel1.grid(row=row, column=0, sticky="n", padx=4, pady=4)
            inbuttonlabel1.button=i*2
            self.controller.ToolTip(inbuttonlabel1, text="{} Button {}".format(macro,i*2))
            
            inbuttoncolor2 = inbuttoncolorlist[index+1]
            inbuttontext2 = inbuttontextlist[index+1]                
            inbuttonlabel2 = tk.Button(in_button_frame, text=inbuttontext2, width=BUTTONLABELWIDTH, height=1, relief="raised", background=inbuttoncolor2,borderwidth=1,command=lambda: self._button_cmd(macrokey=macro,button=i*2+1))
            inbuttonlabel2.grid(row=row, column=1, sticky="n", padx=4, pady=4)
            inbuttonlabel2.button=i*2+1
            self.controller.ToolTip(inbuttonlabel1, text="{} Button {}".format(macro,i*2+1))
           
    """       
   
    macrotype = macrodata.get("Typ","")
    if macrotype =="ColTab":
        macroparams = []
    else:       
        macroparams = macrodata.get("Params",[])
    
    if macroparams:
        param_frame = ttk.Frame(macroparam_frame) #,borderwidth=1,relief="ridge")
                              
        self.create_macroparam_content(param_frame,macro, macroparams,extratitleline=True)

        param_frame.grid(row=1,column=1,rowspan=2,padx=0, pady=0,sticky="nw")

    return macroparam_frame