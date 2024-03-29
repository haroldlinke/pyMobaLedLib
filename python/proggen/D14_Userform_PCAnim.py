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
from vb2py.vbdebug import *
from vb2py.vbconstants import *

import tkinter as tk
from tkinter import ttk

import mlpyproggen.Prog_Generator as PG

import proggen.M02_Public as M02
import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
import proggen.M09_SelectMacro_Treeview as M09SMT
import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80

from ExcelAPI.XLC_Excel_Consts import *
import ExcelAPI.XLW_Workbook as P01

house_button_list_str = 'ROOM_DARK,ROOM_BRIGHT,ROOM_WARM_W,ROOM_RED,ROOM_D_RED,NL,ROOM_COL0,ROOM_COL1,ROOM_COL2,ROOM_COL3,ROOM_COL4,ROOM_COL5,ROOM_COL345,NL,FIRE,FIRED,FIREB,ROOM_CHIMNEY,ROOM_CHIMNEYD,ROOM_CHIMNEYB,NL,ROOM_TV0,ROOM_TV0_CHIMNEY,ROOM_TV0_CHIMNEYD,ROOM_TV0_CHIMNEYB,ROOM_TV1,ROOM_TV1_CHIMNEY,ROOM_TV1_CHIMNEYD,ROOM_TV1_CHIMNEYB,NL,NEON_LIGHT,NEON_LIGHT1,NEON_LIGHT2,NEON_LIGHT3,NEON_LIGHTD,NEON_LIGHT1D,NEON_LIGHT2D,NEON_LIGHT3D,NL,NEON_LIGHTM,NEON_LIGHT1M,NEON_LIGHT2M,NEON_LIGHT3M,NEON_LIGHTL,NEON_LIGHT1L,NEON_LIGHT2L,NEON_LIGHT3L,NL,NEON_DEF_D,NEON_DEF1D,NEON_DEF2D,NEON_DEF3D,CANDLE,CANDLE1,CANDLE2,CANDLE3,NL,SINGLE_LED1,SINGLE_LED2,SINGLE_LED3,SINGLE_LED1D,SINGLE_LED2D,SINGLE_LED3D,NL,GAS_LIGHT,GAS_LIGHT1,GAS_LIGHT2,GAS_LIGHT3,GAS_LIGHTD,GAS_LIGHT1D,GAS_LIGHT2D,GAS_LIGHT3D,NL,SKIP_ROOM,SKIP_ROOM'
gaslights_button_list_str = 'NEON_LIGHT,NEON_LIGHT1,NEON_LIGHT2,NEON_LIGHT3,NEON_LIGHTD,NEON_LIGHT1D,NEON_LIGHT2D,NEON_LIGHT3D,NL,NEON_LIGHTM,NEON_LIGHT1M,NEON_LIGHT2M,NEON_LIGHT3M,NEON_LIGHTL,NEON_LIGHT1L,NEON_LIGHT2L,NEON_LIGHT3L,NL,NEON_DEF_D,NEON_DEF1D,NEON_DEF2D,NEON_DEF3D,CANDLE,CANDLE1,CANDLE2,CANDLE3,NL,SINGLE_LED1,SINGLE_LED2,SINGLE_LED3,SINGLE_LED1D,SINGLE_LED2D,SINGLE_LED3D,NL,GAS_LIGHT,GAS_LIGHT1,GAS_LIGHT2,GAS_LIGHT3,GAS_LIGHTD,GAS_LIGHT1D,GAS_LIGHT2D,GAS_LIGHT3D,NL,SKIP_ROOM,SKIP_ROOM'

class UserForm_PCAnim:
    def __init__(self,MacroName="ServoAnim"):
        self.title = M09.Get_Language_Str('ServoAnim: Animation einer Servobewegung')
        self.Description_Label_txt =  M09.Get_Language_Str('ServoAnim Beschreibung.')
        self.Label_Beleuchtungstypen_txt =  M09.Get_Language_Str("")
        self.Label_NotchangableCol_txt =  M09.Get_Language_Str("")
        self.label4_txt =  M09.Get_Language_Str("")
        self.label5_txt =  M09.Get_Language_Str("")
        self.Label1_ServoAdress_txt =  M09.Get_Language_Str("ServoAdresse")
        self.Label2_Steps_txt =  M09.Get_Language_Str("Anzahl Stufen für Animation")
        self.Used_RGB_LEDs_Label_txt =  M09.Get_Language_Str("")
        self.OnTime_Label_txt = M09.Get_Language_Str("Dauer der Animation beim Einschalten (msec)")
        self.OffTime_Label_txt = M09.Get_Language_Str("Dauer der Animation beim Ausschalten (msec)")
        self.Label9_LED_Channel_txt =  M09.Get_Language_Str("LED Kanal")
        self.Analog_Crossfade_CheckBox_txt = M09.Get_Language_Str("Mit Überblendung")
                
        self.controller = PG.get_global_controller()
        self.IsActive = False
        self.button1_txt =  M09.Get_Language_Str("Abbrechen")
        self.button2_txt =  M09.Get_Language_Str("Ok")
        self.Dist_Nr_R = ""
        self.Conn_Nr_R = ""
        self.res = False
        self.Userform_Res = ""
        
        self.top = tk.Toplevel(self.controller)
        self.top.transient(self.controller)
        
        self.top.grab_set()
        
        self.top.resizable(False, False)  # This code helps to disable windows from resizing
        
        window_height = 900
        window_width = 1400
        
        winfo_x = PG.global_controller.winfo_x()
        winfo_y = PG.global_controller.winfo_y()
        
        screen_width = PG.global_controller.winfo_width()
        screen_height = PG.global_controller.winfo_height()
        
        x_cordinate = winfo_x+int((screen_width/2) - (window_width/2))
        y_cordinate = winfo_y+int((screen_height/2) - (window_height/2))
        
        self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))                 
        
        if len(self.title) > 0: 
            self.top.title(self.title)
        
        self.Description_Label = ttk.Label(self.top, text=self.Description_Label_txt,font=("Tahoma", 11),wraplength=window_width,relief=tk.SUNKEN, borderwidth=1)

        self.Label5_hint_txt = ttk.Label(self.top, text=self.label5_txt,font=("Tahoma", 8),justify="center")
        #self.Label1_MinCnt = ttk.Label(self.top, text=self.Label1_MinCnt_txt,font=("Tahoma", 11))
        #self.Label2_MaxCnt = ttk.Label(self.top, text=self.Label2_MaxCnt_txt,font=("Tahoma", 11))
        
        self.MinCnt_TextBox_svar = tk.StringVar(self.controller)
        self.MinCnt_TextBox_svar.set("1")
        self.MinCnt_TextBox = tk.Entry(self.top,width=4,textvariable=self.MinCnt_TextBox_svar)
        self.MinCnt_Label = ttk.Label(self.top, text=self.Label1_ServoAdress_txt,wraplength=window_width,font=("Tahoma", 11))
        
        self.MaxCnt_TextBox_svar = tk.StringVar(self.controller)
        self.MaxCnt_TextBox_svar.set("255")
        self.MaxCnt_TextBox = tk.Entry(self.top,width=4,textvariable=self.MaxCnt_TextBox_svar)
        self.MaxCnt_Label = ttk.Label(self.top, text=self.Label2_Steps_txt,wraplength=window_width,font=("Tahoma", 11))
        
        self.LED_Channel_TextBox_svar = tk.StringVar(self.controller)
        self.LED_Channel_TextBox_svar.set("1")
        self.LED_Channel_TextBox = tk.Entry(self.top,width=4,textvariable=self.LED_Channel_TextBox_svar)
        self.Label9_LED_Channel = ttk.Label(self.top, text=self.Label9_LED_Channel_txt,wraplength=window_width,font=("Tahoma", 11))
        
        self.Analoge_Crossfade = tk.StringVar(self.controller)
        self.Analoge_Crossfade.set(0)
        self.Analog_Crossfade_CheckBox = tk.Checkbutton(self.top, offvalue=0, onvalue=1, text=self.Analog_Crossfade_CheckBox_txt,variable=self.Analoge_Crossfade)
        
        self.OnTime_TextBox_svar = tk.StringVar(self.controller)
        self.OnTime_TextBox_svar.set("1")
        self.OnTime_TextBox = tk.Entry(self.top,width=4,textvariable=self.OnTime_TextBox_svar)
        self.OnTime_Label = ttk.Label(self.top, text=self.OnTime_Label_txt,wraplength=window_width,font=("Tahoma", 11))
        
        self.OffTime_TextBox_svar = tk.StringVar(self.controller)
        self.OffTime_TextBox_svar.set("255")
        self.OffTime_TextBox = tk.Entry(self.top,width=4,textvariable=self.OffTime_TextBox_svar)
        self.OffTime_Label = ttk.Label(self.top, text=self.OffTime_Label_txt,wraplength=window_width,font=("Tahoma", 11))

        self.Label5_hint_txt.grid(row=3,column=1,columnspan=3,sticky="e",padx=10,pady=10)
            
        self.MinCnt_TextBox.grid(row=6,column=0,columnspan=1,sticky="e",padx=10,pady=10)   
        self.MinCnt_Label.grid(row=6,column=1,columnspan=1,sticky="w",padx=10,pady=10)
        self.MaxCnt_TextBox.grid(row=7,column=0,columnspan=1,sticky="e",padx=10,pady=10)  
        self.MaxCnt_Label.grid(row=7,column=1,columnspan=1,sticky="w",padx=10,pady=10)
        
        self.OnTime_TextBox.grid(row=6,column=3,columnspan=1,sticky="e",padx=10,pady=10)  
        self.OnTime_Label.grid(row=6,column=4,columnspan=1,sticky="w",padx=10,pady=10)
        #self.OffTime_TextBox.grid(row=7,column=3,columnspan=1,sticky="e",padx=10,pady=10)  
        #self.OffTime_Label.grid(row=7,column=4,columnspan=1,sticky="w",padx=10,pady=10)    
        
        self.LED_Channel_TextBox.grid(row=8,column=0,columnspan=1,sticky="e",padx=10,pady=10)
        self.Label9_LED_Channel.grid(row=8,column=1,columnspan=1,sticky="w",padx=10,pady=10)
        self.Analog_Crossfade_CheckBox.grid(row=9,column=1,columnspan=1,sticky="w",padx=10,pady=10)

        self.button_frame = ttk.Frame(self.top)
        
        self.b_cancel = tk.Button(self.button_frame, text=self.button1_txt, command=self.cancel,width=10,font=("Tahoma", 11))
        self.b_ok = tk.Button(self.button_frame, text=self.button2_txt, command=self.ok,width=10,font=("Tahoma", 11))

        self.b_cancel.grid(row=0,column=0,sticky="e",padx=10,pady=10)
        self.b_ok.grid(row=0,column=1,sticky="e",padx=10,pady=10)
        
        self.button_frame.grid(row=10,column=4,sticky="e")
        
        self.top.bind("<Return>", self.ok)
        self.top.bind("<Escape>", self.cancel)                    

        self.__UserForm_Initialize()
        P01.Center_Form(self.top)
        
    def dummy_proc(self, event=None):
        #print(event)
        pass
 
    def ok(self, event=None):
        self.IsActive = False
        self.__OK_Button_Click()
        
        #self.Userform_res = value
        self.top.destroy()
        P01.ActiveSheet.Redraw_table()
        self.res = True
 
    def cancel(self, event=None):
        self.UserForm_res = '<Abort>'
        self.IsActive = False
        self.top.destroy()
        P01.ActiveSheet.Redraw_table()
        self.res = False
        
    def delete_room(self, event=None):
        self.__DelRoom_Button_Click()

    def show(self):
        
        self.IsActive = True
        self.controller.wait_window(self.top)

        return self.res

    def house_button_cmd(self, button_label):
        
        #print("Button clicked ",button_label)
        
        self.__Add_Room(button_label)
    
    def __Debug_Print_LED_Channels():
        o = Variant()
    
        All = String()
        #-------------------------------------
        # Used to generate LED_ChannelsList (Prior the Channel have been stored in the "Tag" of the button, but this is no longer used)
        for o in Me.Controls:
            if Left(o.Name, Len('CommandButton')) == 'CommandButton':
                Txt = ' ' + o.Caption + ':'
                if o.Tag != '':
                    Txt = Txt + o.Tag
                else:
                    Txt = Txt + 'RGB'
                Txt = Txt + '                '
            All = All + Left(Txt, 22)
            if Len(All) > 80:
                Debug.Print(All + '" & _')
                All = '"'
        Debug.Print(All + '" & _')
    
    def __Set_Color_in_y_Range(StartY, EndY, ForeColor):
        c = Variant()
        #--------------------------------------------------------------------------------
        for c in Controls:
            if c.Top >= StartY and c.Top < EndY:
                c.ForeColor = ForeColor
    
    def __Set_Bold_in_y_Range(StartY, EndY, Bold):
        c = Variant()
        #---------------------------------------------------------------------------------
        for c in Controls:
            if c.Top >= StartY and c.Top < EndY:
                c.Font.Bold = Bold
    
    def __CommandButton58_Click():
        __Add_Room(Me.ActiveControl.Caption)
    
    def __CommandButton59_Click():
        __Add_Room(Me.ActiveControl.Caption)
    
    def __CommandButton60_Click():
        __Add_Room(Me.ActiveControl.Caption)
    
    def __CommandButton61_Click():
        __Add_Room(Me.ActiveControl.Caption)
    
    def __IndividualTimes_CheckBox_Click(self):
        #-------------------------------------------
        self.MinTime_TextBox.Enabled = self.Analoge_Crossfade.get()
        self.MaxTime_TextBox.Enabled = self.Analoge_Crossfade.get()
    
    def __LimmitActivInput(self,ct, MinVal, MaxVal):
        #--------------------------------------------------------------------------------
        with_0 = ct
        if not IsNumeric(with_0.Value):
            while Len(with_0.Value) > 0 and not IsNumeric(with_0.Value):
                with_0.Value = M02.DelLast(with_0.Value)
        else:
            if P01.val(with_0.Value) < MinVal:
                with_0.Value = MinVal
            if P01.val(with_0.Value) > MaxVal:
                with_0.Value = MaxVal
            if Round(with_0.Value, 0) != with_0.Value:
                with_0.Value = Round(with_0.Value, 0)
    
    def __LED_Channel_TextBox_Change(self):
        #---------------------------------------
        self.__LimmitActivInput(self.LED_Channel_TextBox_svar.get(), 0, M02.LED_CHANNELS - 1)
    
    def __MinCnt_TextBox_Change(self):
        #----------------------------------
        self.__MinCntChanged = True
        self.__LimmitActivInput(self.MinCnt_TextBox_svar.get(), 0, 127)
    
    def __MaxCnt_TextBox_Change(self):
        #----------------------------------
        self.__MaxCntChanged = True
        self.__LimmitActivInput(self.MaxCnt_TextBox_svar.get(), 1, 255)
    
    def __Get_Calc_MinCnt(self,LEDCnt):
        fn_return_value = None
        #val = int()
        #-------------------------------------------------------
        val = Round(LEDCnt / 3, 0)
        if val < 1:
            val = 1
        if val > 127:
            val = 127
            # 13.01.20:
        fn_return_value = int(val)
        return fn_return_value
    
    def __Get_Calc_MaxCnt(self,LEDCnt):
        fn_return_value = None
        #-------------------------------------------------------
        fn_return_value = int(Round(2 * LEDCnt / 3, 0))
        return fn_return_value
    
    def __Set_MinMaxCnt(self,LEDCnt):
        #----------------------------------------
        # Set MinCnt to 1/3 LEDCnt
        # And MaxCnt to 2/3 LEDCnt
        ## VB2PY (CheckDirective) VB directive took path 1 on 1
        P01.Application.EnableEvents = False
        if not self.__MinCntChanged:
            self.MinCnt_TextBox_svar.set(self.__Get_Calc_MinCnt(LEDCnt))
            self.__MinCntChanged = False
        if not self.__MaxCntChanged:
            self.MaxCnt_TextBox_svar.set(self.__Get_Calc_MaxCnt(LEDCnt))
            self.__MaxCntChanged = False
        P01.Application.EnableEvents = True
    
    def __OnTime_TextBox_Change(self):
        #-----------------------------------
        self.__LimmitActivInput(self.OnTime_TextBox_svar.get(), 0, 100000)
    
    def __OffTime_TextBox_Change(self):
        #-----------------------------------
        self.__LimmitActivInput(self.OffTime_TextBox_svar.get(), 0, 100000)
    
    def __OK_Button_Click(self):
        #Cnt = int()
        #----------------------------

        self.Userform_Res = "// Activation: Binary\n" + "Bin_InCh_to_TmpVar(#InCh, 1.0) \n"
        #APatternT1(#LED,28,SI_LocalVar,3,0,128,0,PM_NORMAL,250,10,1,0,40,1,0,70,1,0,100,1,0,130,1,0,180,1,0,210,1,0,240,1,0,250,1,0,250,1,0,220,1,0,190,1,0,160,1,0,130,1,0,100,1,0,70,1,0,40,1,0,10,1,0  ,0,0,0,0,0,0,0,0,63,128,0,0,0,0,0,0,0,63)
        if self.Analoge_Crossfade.get()=="1":
            self.Userform_Res = self.Userform_Res + "A"
        self.Userform_Res = self.Userform_Res + "PatternT1(#LED,28,SI_LocalVar,3,0,128,0,PM_NORMAL,"
        duration_str =  self.OnTime_TextBox_svar.get()
        count_str = self.MinCnt_TextBox_svar.get() 

        #if self.InpInversBox_svar.get()=="1":
        #    self.Userform_Res = self.Userform_Res + '_Inv'
            # 13.01.20:
        self.Userform_Res = self.Userform_Res + '(#LED, #InCh, '
        if self.__Mode == 'House':
            self.Userform_Res = self.Userform_Res + self.MinCnt_TextBox_svar.get() + ', ' + self.MaxCnt_TextBox_svar.get() + ', '
            if self.Analoge_Crossfade.get()=="1":
                self.Userform_Res = self.Userform_Res + self.OnTime_TextBox_svar.get() + ', ' + self.OffTime_TextBox_svar.get() + ', '
        #self.Userform_Res = self.Userform_Res + self.SelectedRooms_TextBox.get(1.0, tk.END+"-1c") + ')$' + self.LED_Channel_TextBox_svar.get()
        #Store_Pos(Me, HouseForm_Pos)
        #Unload(Me)
    
    def __Abort_Button_Click(self):
        #-------------------------------
        
        self.Userform_Res = ''
        #Store_Pos(Me, HouseForm_Pos)
        #Unload(Me)
    
    def __Count_Used_RGB_Channels(self):
        fn_return_value = None
        Cnt = 0 #int()
    
        #X = Variant()
    
        SingleLED = 0
        #-----------------------------------------
        # Single LEDs (Connected to a WS2811) are counted as one LED as long as they are in
        # assending order.
        # 1 2 3 = one RGB LED
        # 1 1 1 = three RGB LEDs
        for X in Split(self.__LED_CntList, ' '):
            if X == 'RGB':
                if SingleLED == 0:
                    Cnt = Cnt + 1
                else:
                    Cnt = Cnt + 2
                    SingleLED = 0
            elif X != '':
                if P01.val(X) <= SingleLED:
                    Cnt = Cnt + 1
                SingleLED = P01.val(X)
        if SingleLED > 0:
            Cnt = Cnt + 1
        fn_return_value = Cnt
        return fn_return_value
    
    def __Count_Rooms(self):
        fn_return_value = None
        Cnt = 0
        
        #-----------------------------
        selroom=self.SelectedRooms_TextBox.get(1.0, tk.END+"-1c") #*HL
        if selroom != '':
            Cnt = UBound(Split(selroom, ',')) + 1 #*HL
        fn_return_value = Cnt
        return fn_return_value
    
    def __Set_Fokus_To_Selected_Rooms_to_Show_Cursor(self):
        #-------------------------------------------------------
        self.SelectedRooms_TextBox.focus_set()
    
    def __Set_RoomCount(self,Cnt):
        #-------------------------------------
        self.RoomCnt_Label.configure(text=M09.Get_Language_Str('Anzahl: ') + str(Cnt))
        self.Used_RGB_LEDs_Label.configure(text=M09.Get_Language_Str('RGB LED Kanäle: ') + str(self.__Count_Used_RGB_Channels()))
        self.__Set_MinMaxCnt(Cnt)
        self.__Set_Fokus_To_Selected_Rooms_to_Show_Cursor()

    
    def __SelectedRooms_TextBox_Click(self):
        Debug.Print('Textbox' + SelectedRooms_TextBox.SelStart)
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Button - ByVal 
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: X - ByVal 
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Y - ByVal 
    def __SelectedRooms_TextBox_MouseDown(self, Button, Shift, X, Y):
        #---------------------------------------------------------------------------------------------------------------------------------
        with_1 = self.SelectedRooms_TextBox
        for Word in Split(with_1.Text, ','):
            ChrCnt = Len(Txt) + 0.5 + Len(Word) / 2
            if with_1.SelStart < ChrCnt:
                with_1.SelStart = Len(Txt)
                return
            Txt = Txt + Word + ','
        with_1.SelStart = Len(with_1.Text)
    
    def __Correct_Selection(self,direction=" -1 chars"):
        
        fn_return_value = False
        #-----------------------------------
        
        curpos = self.SelectedRooms_TextBox.index(tk.INSERT)
        
        #if SelectedRooms_TextBox.SelLength > 0:
        #    SelectedRooms_TextBox.SelLength = 0
        self.SelectedRooms_TextBox.mark_set(tk.INSERT, curpos + direction)
        
        if direction == " -1 chars":
            loopend = "1.0"
        else:
            loopend = self.SelectedRooms_TextBox.index(tk.END + " -1 chars")

        while curpos !=loopend:
            curchar = self.SelectedRooms_TextBox.get(curpos)
            if curchar == ",":
                self.SelectedRooms_TextBox.mark_set(tk.INSERT, curpos)
                return False
            self.SelectedRooms_TextBox.mark_set(tk.INSERT, curpos + direction) #SelectedRooms_TextBox.SelStart = SelectedRooms_TextBox.SelStart - 1
            curpos = self.SelectedRooms_TextBox.index(tk.INSERT)
        fn_return_value = False
        self.__Set_Fokus_To_Selected_Rooms_to_Show_Cursor()
        return fn_return_value
    
    def __DelRoom_Button_Click(self):
        p = 0 #int()
    
        e = 0 # int()
    
        Txt = "" #String()
        #---------------------------------
        if self.SelectedRooms_TextBox.get(1.0, tk.END+"-1c") == '':
            self.__Set_Fokus_To_Selected_Rooms_to_Show_Cursor()
            return
        curpos1 = self.SelectedRooms_TextBox.index(tk.INSERT)
        
        curchar = self.SelectedRooms_TextBox.get(curpos1)
        if curchar == ",":
            self.SelectedRooms_TextBox.mark_set(tk.INSERT, curpos1 + "-1c")     
        
        dummy=self.__Correct_Selection()
        curpos2 = self.SelectedRooms_TextBox.index(tk.INSERT)
        self.SelectedRooms_TextBox.mark_set(tk.INSERT, curpos1)
        dummy=self.__Correct_Selection(direction=" +1 chars")
        curpos3 = self.SelectedRooms_TextBox.index(tk.INSERT)
             
        self.SelectedRooms_TextBox.delete(curpos2,curpos3)
        
        Txt = self.SelectedRooms_TextBox.get(1.0, tk.END+"-1c")
                
        self.__LED_CntList = Txt
        self.__Set_RoomCount(self.__Count_Rooms())
    
    def __Get_LED_Channel_from_Name(self,Name):
        fn_return_value = None
        p = 0 #int()
    
        e = 0# int()
        #-------------------------------------------------------------------
        p = InStr(self.__LED_ChannelsList, ' ' + Name + ':')
        if p == 0:
            P01.MsgBox('Internal Error: \'' + Name + '\' not found in \'LED_ChannelsList\'', vbCritical, 'Internal Error')
            sys.exit(0)
        else:
            p = p + 1 + Len(Name) + 1
            e = InStr(p, self.__LED_ChannelsList, ' ')
            fn_return_value = Mid(self.__LED_ChannelsList, p, e - p)
        return fn_return_value
    
    def __Add_Room(self,Caption):
        Cnt = int()
        #--------------------------------------
        Cnt = self.__Count_Rooms()
        if Cnt >= 250:
            P01.MsgBox(M09.Get_Language_Str('Es können keine weiteren Räume hinzugefügt werden'), vbInformation, M09.Get_Language_Str('Maximale Raumanzahl erreicht'))
            self.__Set_Fokus_To_Selected_Rooms_to_Show_Cursor()
            return
        #if self.__Correct_Selection():
        #    return
        self.__LED_CntList = self.__LED_CntList + self.__Get_LED_Channel_from_Name(Caption) + ' '
        txt = self.SelectedRooms_TextBox.get(1.0, tk.END+"-1c")
        #print("Txt:",txt,"Caption:",Caption)
        if self.SelectedRooms_TextBox.get(1.0, tk.END+"-1c") == '':
            self.SelectedRooms_TextBox.insert(tk.END+"-1c", Caption)
        else:
            curchar = self.SelectedRooms_TextBox.get(tk.INSERT)
            #print("curchar:",curchar)
            if curchar == " ":
                self.SelectedRooms_TextBox.insert(tk.INSERT, " " + Caption + ",")
            elif curchar == ",":
                self.SelectedRooms_TextBox.insert(tk.INSERT, ", " + Caption)
            else:
                curpos = self.SelectedRooms_TextBox.index(tk.INSERT)
                wordstart = self.SelectedRooms_TextBox.index(tk.INSERT + " wordstart")
                if curpos == wordstart and curchar != "\n":
                    self.SelectedRooms_TextBox.insert(tk.INSERT, Caption + ", ")
                else:
                    self.SelectedRooms_TextBox.insert(tk.INSERT+" wordend", ", " + Caption)
                
            #p = self.SelectedRooms_TextBox.index(tk.INSERT)
            #end = self.SelectedRooms_TextBox.index(tk.END+"-1c")
            #print("P:",p," end:",end)
            #if p == self.SelectedRooms_TextBox.index(tk.END+"-1c"): # at to end
            #    self.SelectedRooms_TextBox.insert(tk.END, ', ' + Caption)
            #else:
            #    self.SelectedRooms_TextBox.insert(tk.INSERT, ', ' + Caption)
            #*HL SelectedRooms_TextBox.SelStart = p + Len(Caption) + 1
        #curpos = self.SelectedRooms_TextBox.index(tk.END+"-1c")
        #self.SelectedRooms_TextBox.mark_set(tk.INSERT, curpos)
        self.__Set_RoomCount(self.__Count_Rooms())
    
    def __Change_Height(self,factor):
        return
        #X = Byte()
    
        #obj = Control()
        #------------------------------------------
        # Factor 0.85 => 712  (width 1110)
        # factor 0.9  => 745
        Me.Height = ( Me.Height + 5 )  * factor
        for obj in Controls:
            obj.Top = obj.Top * factor
            obj.Height = obj.Height * factor
        Description_Label.Font.Size = Description_Label.Font.Size * factor
        Label_NotchangableCol.Font.Size = Label_NotchangableCol.Font.Size * factor
    
    def __UserForm_Initialize(self):
        #Monitor_Pixel_Cnt_Y = int()
        #--------------------------------
        #Debug.Print vbCr & Me.Name & ": UserForm_Initialize"
        #Monitor_Pixel_Cnt_Y = self.Get_Primary_Monitor_Pixel_Cnt_Y()
        #if Monitor_Pixel_Cnt_Y <= 720:
        #    self.__Change_Height(0.85)
        #elif Monitor_Pixel_Cnt_Y <= 833:
        #    self.__Change_Height(0.9)
        #Change_Language_in_Dialog(Me)
        #Restore_Pos_or_Center_Form(Me, HouseForm_Pos)
        ## VB2PY (CheckDirective) VB directive took path 1 on False
        #self.SelectedRooms_TextBox.insert(tk.INSERT,'ROOM_D_RED, ROOM_COL4, ROOM_CHIMNEYD, ROOM_TV1, NEON_LIGHTD, NEON_LIGHTL, SINGLE_LED2D, GAS_LIGHTD, GAS_LIGHT1D, SINGLE_LED3D, NEON_LIGHT1L, NEON_LIGHT1D, ROOM_TV1_CHIMNEY, ROOM_CHIMNEYB')
        #self.__LED_CntList = '                          RGB         RGB        RGB            RGB       RGB          RGB          2             RGB         1            3             1             1             RGB               RGB       '

        self.b_ok.focus_set() #OK_Button.setFocus()
    
    def __SetMode(self, MacroName):
        #---------------------------------------
        self.__Mode = MacroName
        if (MacroName == 'ServoAnim'):
            pass
        #    self.__Set_Bold_in_y_Range(CommandButton1.Top, CommandButton27.Top, True)
        elif (MacroName == 'LEDAnim'):
            self.top.title(M09.Get_Language_Str('LEDAnim: Animation von LEDs'))
            self.Description_Label.configure(text=M09.Get_Language_Str('LEDAnim Beschreibung'))
            
    def Show_With_Existing_Data(self, MacroName, ConfigLine, LED_Channel, Def_Channel):
        Txt = String()
        #----------------------------------------------------------------------------------------------------------------------
        self.__SetMode(MacroName)
        self.__LED_CntList = ''
        #self.IndividualTimes_CheckBox_svar.set(False)
        self.LED_Channel_TextBox_svar.set(Def_Channel)
        #self.show() #*HL
        if Len(ConfigLine) > Len(MacroName):
            if Left(ConfigLine, Len(MacroName)) == MacroName:
                Parts = Split(Replace(Split(ConfigLine, '(')(1), ')', ''), ',')
                if MacroName == 'House':
                    self.MinCnt_TextBox_svar.set(P01.val(Parts(2)))
                    self.MaxCnt_TextBox_svar.set(P01.val(Parts(3)))
                    if Left(ConfigLine, Len('HouseT')) == 'HouseT':
                        self.MinTime_TextBox_svar.set(P01.val(Parts(4)))
                        self.MaxTime_TextBox_svar.set(P01.val(Parts(5)))
                        self.Analoge_Crossfade.set(True)
                        Nr = 6
                    else:
                        Nr = 4
                else:
                    Nr = 2
                self.LED_Channel_TextBox_svar.set(str(LED_Channel))
        self.show()
    
    # VB2PY (UntranslatedCode) Option Explicit
