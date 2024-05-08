# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 4.02
# * Author: Harold Linke
# * Date: January 7, 2021
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
# 2021-01-07 v4.02 HL: - Else: check done, first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

import tkinter as tk
from tkinter import ttk
import urllib
from mlpyproggen.tooltip import Tooltip
from tkcolorpicker.spinbox import Spinbox
from tkcolorpicker.limitvar import LimitVar



import proggen.M02_Public as M02
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header as M06
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M08_Install_FastBootLoader as M08IN
#import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
import proggen.M17_Import_old_Data as M17
import proggen.M18_Save_Load as M18
#import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Multiplexer as M80

import proggen.F00_mainbuttons as F00

from ExcelAPI.XLC_Excel_Consts import *
import ExcelAPI.XLA_Application as P01
import mlpyproggen.Prog_Generator as PG
import proggen.M09_Language as M09

import logging

from vb2py.vbfunctions import *
from vb2py.vbdebug import *


__Disable_Set_Arduino_Typ = Boolean()

class CUserForm_Options:
    
    def __init__(self):
        self.controller = PG.get_global_controller()
        self.IsActive = False
        self.button1_txt = "Abbrechen"
        self.button2_txt = "Ok"
        self.res = False
        self.UserForm_Res = ""
        #self.__UserForm_Initialize()
        self.Controls={}
        self.rb_res = {"_R": tk.IntVar(),
                       "_L": tk.IntVar()}
        self.__Disable_Set_Arduino_Typ = True
        
        self.radiobuttons = {"Nano_Normal_L": {"text":M09.Get_Language_Str("Nano Normal (old Bootloader)"), "value": 1,"board": M02.BOARD_NANO_OLD},
                             "Nano_New_L"   : {"text":M09.Get_Language_Str("Nano (neue Version)"), "value": 2,"board": M02.BOARD_NANO_NEW},
                             "Nano_Full_L"  : {"text":M09.Get_Language_Str("Nano (Full memory)"), "value": 3,"board": M02.BOARD_NANO_FULL},
                             "Uno_L"        : {"text":M09.Get_Language_Str("Uno"), "value": 4,"board": M02.BOARD_UNO_NORM},
                             "Board_IDE_L"  : {"text":M09.Get_Language_Str("Typ von Arduino IDE benutzen"), "value": 5,"board": ''},
                             "ESP32_L"      : {"text":M09.Get_Language_Str("ESP32 Wroom"), "value": 6,"board": M02.BOARD_ESP32},
                             "Pico_L"       : {"text":M09.Get_Language_Str("Raspberry Pico (Experimental)"), "value": 7,"board": M02.BOARD_PICO},
                             "Nano_Normal_R": {"text":M09.Get_Language_Str("Nano Normal (old Bootloader)"), "value": 1,"board": M02.BOARD_NANO_OLD},
                             "Nano_New_R"   : {"text":M09.Get_Language_Str("Nano (neue Version)"), "value": 2,"board":  M02.BOARD_NANO_NEW},
                             "Nano_Full_R"  : {"text":M09.Get_Language_Str("Nano (Full memory)"), "value": 3,"board": M02.BOARD_NANO_FULL},
                             "Uno_R"        : {"text":M09.Get_Language_Str("Uno"), "value": 4,"board": M02.BOARD_UNO_NORM},
                             "Board_IDE_R"  : {"text":M09.Get_Language_Str("Typ von Arduino IDE benutzen"), "value": 5,"board": ''},
                             }
        
        self.boardlist = ("dummy",M02.BOARD_NANO_OLD, M02.BOARD_NANO_NEW, M02.BOARD_NANO_FULL, M02.BOARD_UNO_NORM,'', M02.BOARD_ESP32, M02.BOARD_PICO)
        
        self.defaultboard = 7
        
        #*HL Center_Form(Me)                

    
    def __Close_Button_Click(self):
        #-------------------------------
        self.Hide()
        board=self.radiobutton_to_board(True)
        self.Change_Board(True, board)        
    
    def __ColorTest_Button_Click(self):
        #-----------------------------------
        self.Hide()
        #Open_MobaLedCheckColors('')
    
    def __Detect_LED_Port_Button_Click(self):
        #-----------------------------------------
        self.Hide()
        board=self.radiobutton_to_board(True)
        self.Change_Board(True, board)
        
        M07.Detect_Com_Port_and_Save_Result(False)
        self.Show()
    
    def __Detect_Right_Port_Button_Click(self):
        #-------------------------------------------
        self.Hide()
        board=self.radiobutton_to_board(False)
        self.Change_Board(False, board)        
        M07.Detect_Com_Port_and_Save_Result(True)
        self.Show()
    
    def __FastBootloader_Button_Click(self):
        #----------------------------------------
        self.Hide()
        M08IN.Install_FastBootloader()
    
    def __HardiForum_Button_Click(self):
        #------------------------------------
        self.Hide()
        if P01.MsgBox(M09.Get_Language_Str('Öffnet das Profil von Hardi im Stummi Forum.' + vbCr + vbCr + 'Dort findet man, wenn man im Forum angemeldet ist, einen Link zur ' + 'Email Adresse des Autors zum senden einer E-Mail oder PN.' + vbCr + vbCr + 'Alternativ kann auch eine Mail an \'MobaLedlib@gmx.de\' geschickt werden wenn ' + 'es Fragen oder Anregungen zu dem Programm oder zur MobaLedLib gibt.'), vbOKCancel, M09.Get_Language_Str('Profil des Autors öffnen')) == vbOK:
            P01.Shell('Explorer "https://www.stummiforum.de/u26419_Hardi.html"')
    
    def __Pattern_Config_Button_Click(self):
        #----------------------------------------
        self.Hide()
        #Start_Pattern_Configurator()
    
    def __ProInstall_Button_Click(self):
        #------------------------------------
        M08.Ask_to_Upload_and_Compile_and_Upload_Prog_to_Right_Arduino()
    
    def __Nano_Normal_L_Click(self):
        self.Change_Board(True, M02.BOARD_NANO_OLD)
    
    def __Nano_New_L_Click(self):
        self.Change_Board(True, M02.BOARD_NANO_NEW)
    
    def __Nano_Full_L_Click(self):
        self.Change_Board(True, M02.BOARD_NANO_FULL)
    
    def __Uno_L_Click(self):
        self.Change_Board(True, M02.BOARD_UNO_NORM)
    
    def __Board_IDE_L_Click(self):
        self.Change_Board(True, '')
    
    def __ESP32_L_Click(self):
        self.Change_Board(True, M02.BOARD_ESP32)
        self.Autodetect_Typ_L_CheckBox.Value = False
    
    def __Pico_L_Click(self):
        self.Change_Board(True, M02.BOARD_PICO)
        self.Autodetect_Typ_L_CheckBox.Value = False
    
    def __Nano_Normal_R_Click(self):
        self.Change_Board(False, M02.BOARD_NANO_OLD)
    
    def __Nano_New_R_Click(self):
        self.Change_Board(False, M02.BOARD_NANO_NEW)
    
    def __Nano_Full_R_Click(self):
        self.Change_Board(False, M02.BOARD_NANO_FULL)
    
    def __Uno_R_Click(self):
        self.Change_Board(False, M02.BOARD_UNO_NORM)
    
    def __Board_IDE_R_Click(self):
        self.Change_Board(False, '')
    
    def __Autodetect_Typ_L_CheckBox_Click(self):
        self.__Change_Autodetect(True)
        self.Check_Board (self.Autodetect_Typ_L_CheckBox_var.get())
    
    def __Autodetect_Typ_R_CheckBox_Click(self):
        self.__Change_Autodetect(False)
    
    def Change_Board(self,LeftArduino, NewBrd):
        #----------------------------------------------------------------
        if self.__Disable_Set_Arduino_Typ:
            return
        M28.Change_Board_Typ(LeftArduino, NewBrd)
        
    def Check_Board(self,AutodetectChecked):
        #----------------------------------------------------
        if AutodetectChecked:
            buttonvalue = self.rb_res["_L"].get()
            if buttonvalue in range (4,7):
            #if ESP32_L or Pico_L or Uni_L or Board_IDE_L:
                # change back to Nano
                #self.Nano_New_L = True
                self.rb_res["_L"].set(2)
    
    def __Change_Autodetect(self,LeftArduino):
        
        Col = Long()
        #----------------------------------------------------
        if LeftArduino:
            Col = M25.BUILDOP_COL
            self.__Set_Autodetect_Value(Col, self.Autodetect_Typ_L_CheckBox_var.get())
        else:
            Col = M25.BUILDOpRCOL
            self.__Set_Autodetect_Value(Col, self.Autodetect_Typ_R_CheckBox_var.get()) #Controls('Autodetect_Typ_R_CheckBox'))
    
    def __Set_Autodetect_Value(self,BuildOpt_Col, Value):
        #--------------------------------------------------------------------------
        with_0 = P01.Cells(M02.SH_VARS_ROW, BuildOpt_Col)
        if Value:
            if InStr(with_0.Value, M02.AUTODETECT_STR) == 0:
                with_0.Value = M02.AUTODETECT_STR + ' ' + Trim(with_0.Value)
        else:
            with_0.Value = M30.Replace_Multi_Space(Trim(Replace(with_0.Value, M02.AUTODETECT_STR, '')))
    
    def __Get_Arduino_Typ(self,LeftArduino):
        Side = String()
    
        Col = Integer()
    
        BuildOpt = String()
        #---------------------------------------------------
        #BuildOpt = P01.Cells(M02.SH_VARS_ROW, Col)
        #self.Controls['Autodetect_Typ_' + Side + '_CheckBox'] = ( InStr(BuildOpt, M02.AUTODETECT_STR) > 0 )        
        if LeftArduino:
            Col = M25.BUILDOP_COL
            Side = 'L'
            BuildOpt = P01.Cells(M02.SH_VARS_ROW, Col)
            self.Autodetect_Typ_L_CheckBox_var.set(InStr(str(BuildOpt), M02.AUTODETECT_STR) > 0)
        else:
            Col = M25.BUILDOpRCOL
            Side = 'R'
            BuildOpt = P01.Cells(M02.SH_VARS_ROW, Col)
            self.Autodetect_Typ_R_CheckBox_var.set(InStr(str(BuildOpt), M02.AUTODETECT_STR) > 0)
        if InStr(str(BuildOpt), M02.BOARD_NANO_OLD) > 0:
            self.Controls['Nano_Normal_' + Side].Value = True
            return
        if InStr(str(BuildOpt), M02.BOARD_NANO_FULL) > 0:
            self.Controls['Nano_Full_' + Side].Value = True
            return
            # 28.10.20:
        if InStr(str(BuildOpt), M02.BOARD_NANO_NEW) > 0:
            self.Controls['Nano_New_' + Side].Value = True
            return
        if InStr(str(BuildOpt), M02.BOARD_UNO_NORM) > 0:
            self.Controls['Uno_' + Side].Value = True
            return
        if InStr(str(BuildOpt), M02.BOARD_NANO_EVERY) > 0:
            return
            # currently no option in GUI, but that's ok, as ATMEGA4809 is currently unsupported 28.10.20: Jürgen
        if InStr(str(BuildOpt), M02.BOARD_ESP32) > 0 and Side == 'L' and M37.ESP32_Lib_Installed():
            self.Controls['ESP32_L'].Value = True
            return
            # 11.11.20:
        if InStr(str(BuildOpt), M02.BOARD_PICO) > 0 and Side == 'L' and M37.PICO_Lib_Installed():
            self.Controls['PICO_L'].Value = True
            return
            # 18.04.21: Juergen
        if InStr(str(BuildOpt), '--board ') > 0:
            self.Controls['Nano_Normal_' + Side].Value = False
            self.Controls['Nano_New_' + Side].Value = False
            self.Controls['Uno_' + Side].Value = False
            self.Controls['Board_IDE_' + Side].Value = False
            if Side == 'L':
                self.Controls['ESP32_L'].Value = False
            if Side == 'L':
                self.Controls['PICO_L'].Value = False
            P01.MsgBox(M09.Get_Language_Str('Unbekannte Board Option: ') + vbCr + BuildOpt, vbInformation, M09.Get_Language_Str('Unbekanntes Board'))
        self.Controls['Board_IDE_' + Side].Value = True
    
    def __Test_Get_Arduino_Typ(self):
        #UT-------------------------------
        self.__Get_Arduino_Typ(True)
    
    def __Import_Button_Click(self):
        #--------------------------------
        self.Hide()
        M17.Import_from_Old_Version()
    
    def __Save_Button_Click(self):
        #------------------------------
        self.Hide()
        M18.Save_Data_to_File()
    
    def __Load_Button_Click(self):
        #------------------------------
        M18.Load_Data_from_File()
    
    def __Copy_Page_Button_Click(self):
        #-----------------------------------
        self.Hide()
        M18.Copy_from_Sheet_to_Sheet()
    
    def __Update_to_Arduino_Button_Click(self):
        #-------------------------------------------
        self.Hide()
        M37.Update_MobaLedLib_from_Arduino_and_Restart_Excel()
        
        
    def copytree(self, src, dst, symlinks=False, ignore=None):
        names = os.listdir(src)
        if ignore is not None:
            ignored_names = ignore(src, names)
        else:
            ignored_names = set()
            
        if not os.path.exists(dst):
            os.makedirs(dst)
            
        errors = []
        for name in names:
            if name in ignored_names:
                continue
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            try:
                if symlinks and os.path.islink(srcname):
                    linkto = os.readlink(srcname)
                    os.symlink(linkto, dstname)
                elif os.path.isdir(srcname):
                    self.copytree(srcname, dstname, symlinks, ignore)
                else:
                    shutil.copy2(srcname, dstname)
                # XXX What about devices, sockets etc.?
            except (IOError, os.error) as why:
                errors.append((srcname, dstname, str(why)))
            # catch the Error from the recursive copytree so that we can
            # continue with other files
            except BaseException as err:
                errors.extend(err.args[0])
        try:
            shutil.copystat(src, dst)
        except WindowsError:
            # can't copy file access times on Windows
            pass
        except OSError as why:
            errors.extend((src, dst, str(why)))
        if errors:
            raise Error(errors) 
        
    def show_download_status(self,a,b,c):
        
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
        
    def __Update_pyMobaLedLib_Button_Click(self):
        self.Hide()
        if P01.MsgBox(M09.Get_Language_Str('Soll die Python MobaLedLib aktualisiert werden?'), vbQuestion + vbYesNo, M09.Get_Language_Str('Aktualisieren der Python MobaLedLib')) != vbYes:
            return
        F00.StatusMsg_UserForm.ShowDialog(M09.Get_Language_Str('Aktualisiere Python MobaLedLib Programm'), '')
        URL= "https://github.com/HaroldLinke/pyMobaLedLib/archive/master.zip"
        try:
            
            workbookpath = PG.ThisWorkbook.Path
            workbookpath2 = os.path.dirname(workbookpath)
            workbookpath3 = os.path.dirname(workbookpath2)
            zipfilenamepath = workbookpath3+"/pyMobaLedLib.zip"
            F00.StatusMsg_UserForm.Set_Label("Download Python MobaLedLib Programm")
            urllib.request.urlretrieve(URL, zipfilenamepath,self.show_download_status)
            
            F00.StatusMsg_UserForm.Set_Label("Entpacken Python MobaLedLib Programm")
            M30.UnzipAFile(zipfilenamepath,workbookpath3)
            srcpath = workbookpath3+"/pyMobaLedLib-master/python"
            dstpath = workbookpath3+"/pyMobaLedLib/python"
            if not dstpath.startswith(r"D:\data\doc\GitHub"): # do not copy when destination is development folder
                F00.StatusMsg_UserForm.Set_Label("Kopieren des Python MobaLedLib Programm")
                self.copytree(srcpath,dstpath)
            
            
            if P01.MsgBox(M09.Get_Language_Str(' Python MobaLedLib wurde aktualisiert. Soll neu gestartet werden?'), vbQuestion + vbYesNo, M09.Get_Language_Str('Aktualisieren der Python MobaLedLib')) == vbYes:
                # shutdown and restart
                PG.global_controller.restart()
            
        except BaseException as e:
            Debug.Print("Update_MobaLedLib exception:",e)
            P01.MsgBox(M09.Get_Language_Str('Fehler beim Download oder Installieren?'),vbInformation, M09.Get_Language_Str('Aktualisieren der Python MobaLedLib'))
   
        P01.Unload(F00.StatusMsg_UserForm)
        
        
    
    def __Update_Beta_Button_Click(self):
        #-------------------------------------
        self.Hide()
        M37.Update_MobaLedLib_from_Beta_and_Restart_Excel()
    
    def __Show_Lib_and_Board_Page_Button_Click(self):
        #-------------------------------------------------
        self.Hide()
        with_1 = PG.ThisWorkbook.Sheets(M02.LIBRARYS__SH)
        with_1.Visible = True
        with_1.Select()
        
    def Button_Setup(self,button_frame,Text,Command,Accelerator,Row=0,label_text="",state=tk.NORMAL):
        Text = Trim(Text)
        Button = tk.Button(button_frame, text=Text, command=Command,width=20,height=2,font=("Tahoma", 8),state=state)
        Button.grid(row=Row,column=0,sticky="n",padx=10,pady=10)
        
        if Accelerator!="":            
            button_frame.bind(Accelerator, Command)
        
        if label_text!="":
            label = ttk.Label(button_frame, text=M09.Get_Language_Str(label_text),wraplength=300,font=("Tahoma", 11))
            label.grid(row=Row,column=1,sticky="NESW")            
        return
        
        
    def create_arduinopage(self,frame,LeftArduino):
        
        self.right_frame=tk.Frame(frame,relief=tk.RIDGE)
        
        if LeftArduino:
            self.Button_Setup(frame,M09.Get_Language_Str("USB Port erkennen"),self.__Detect_LED_Port_Button_Click,"U",Row=0)
            #self.Button_Setup(M09.Get_Language_Str("Version lesen"),self.CommandButton4_,"U",Row=2)
            side="_L"
            self.Autodetect_Typ_L_CheckBox_var = tk.IntVar(master=self.top)
            self.Autodetect_Typ_L_CheckBox_var.set(0)
            self.Autodetect_Typ_L_CheckBox = tk.Checkbutton(self.right_frame, text=M09.Get_Language_Str("Automatisch erkennen"),width=30,wraplength = 200,anchor="w",variable=self.Autodetect_Typ_L_CheckBox_var,font=("Tahoma", 8),onvalue = 1, offvalue = 0, command=self.__Autodetect_Typ_L_CheckBox_Click)
            self.Autodetect_Typ_L_CheckBox.grid(row=0, column=0,sticky="nw", padx=2, pady=2)                    
        else:
            side="_R"
            self.Button_Setup(frame,M09.Get_Language_Str("USB Port erkennen"),self.__Detect_Right_Port_Button_Click,"U",Row=0)
            self.Button_Setup(frame,M09.Get_Language_Str("Prog. Installieren"),self.__ProInstall_Button_Click,"U",Row=2)    
            self.Autodetect_Typ_R_CheckBox_var = tk.IntVar(master=self.top)
            self.Autodetect_Typ_R_CheckBox_var.set(0)
            self.Autodetect_Typ_R_CheckBox = tk.Checkbutton(self.right_frame, text=M09.Get_Language_Str("Automatisch erkennen"),width=30,wraplength = 200,anchor="w",variable=self.Autodetect_Typ_R_CheckBox_var,font=("Tahoma", 8),onvalue = 1, offvalue = 0, command=self.__Autodetect_Typ_R_CheckBox_Click)
            self.Autodetect_Typ_R_CheckBox.grid(row=0, column=0,sticky="nw", padx=2, pady=2)                  
        
        for rb in self.radiobuttons.keys():
            rb_text = self.radiobuttons[rb]["text"]
            if rb.endswith(side):
                try:
                    
                    if rb.startswith("ESP32"):
                        if not M37.ESP32_Lib_Installed():
                            continue
                    if rb_text.startswith("Pico"):
                        if not M37.PICO_Lib_Installed():
                            continue
                except BaseException as e:
                    logging.error(e, exc_info=True)
         
                rbutton=tk.Radiobutton(self.right_frame, text=rb_text, variable=self.rb_res.get(side), value=self.radiobuttons[rb]["value"])
                row = self.radiobuttons[rb]["value"]
                if row > 3:
                    row+=1
                rbutton.grid(row=row,column=0,sticky="nw",padx=10,pady=0)
                self.radiobuttons[rb]["button"]=rbutton
                self.Controls[rb]=P01.CControl(False)
                
        self.right_frame.grid(row=0,column=1)
        
        subtitle_txt = M09.Get_Language_Str("Für andere Hauptplatine")
        self.subtitle_Label = ttk.Label(self.right_frame, text=subtitle_txt,font=("Tahoma", 8),width=40,wraplength=350,relief=tk.FLAT, borderwidth=1)
        self.subtitle_Label.grid(row=4,column=0,sticky="w",padx=10,pady=0)
   
    def __UserForm_Initialize(self, first_page_only=False):
        #--------------------------------
        # Is called once to initialice the form
        #Debug.Print vbCr & Me.Name & ": UserForm_Initialize"
        #Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        
        self.top = tk.Toplevel(self.controller)
        self.top.transient(self.controller)

        self.top.grab_set()
        
        self.top.resizable(True, True)  # This code helps to disable windows from resizing
        
        window_height = 500
        window_width = 600
        
        winfo_x = PG.global_controller.winfo_x()
        winfo_y = PG.global_controller.winfo_y()
        
        screen_width = PG.global_controller.winfo_width()
        screen_height = PG.global_controller.winfo_height()
        
        x_cordinate = winfo_x+int((screen_width/2) - (window_width/2))
        y_cordinate = winfo_y+int((screen_height/2) - (window_height/2))
        
        #self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))                 
        self.top.geometry("+{}+{}".format(x_cordinate, y_cordinate))                   
        
        self.top.title(M09.Get_Language_Str("Optionen und spezielle Funktionien")) 
         
        self.container = ttk.Notebook(self.top)
        self.container.grid(row=0,column=0,sticky="nesw")
        
        self.tabdict = {}
        LED_Arduino_frame = tk.Frame(self.container)
        LED_Arduino_frame_Name = "LED Arduino"
        self.tabdict[LED_Arduino_frame_Name] = LED_Arduino_frame
        self.container.add(LED_Arduino_frame, text=LED_Arduino_frame_Name)
        
        self.create_arduinopage(LED_Arduino_frame, True)
        
        if not first_page_only:
            if  M25.Page_ID != 'CAN':
                DCC_Arduino_frame = tk.Frame(self.container)
                DCC_Arduino_frame_Name = M25.Page_ID + ' Arduino'
                self.tabdict[DCC_Arduino_frame_Name] = DCC_Arduino_frame
                self.container.add(DCC_Arduino_frame, text=DCC_Arduino_frame_Name)
                self.create_arduinopage(DCC_Arduino_frame, False)
            
            File_frame = tk.Frame(self.container)
            File_frame_Name = M09.Get_Language_Str("Dateien")
            self.tabdict[File_frame_Name] = File_frame
            self.container.add(File_frame, text=File_frame_Name)
        
            self.Button_Setup(File_frame,M09.Get_Language_Str("Importieren v. altem Prog."),self.__Import_Button_Click,"I",Row=0,state=tk.DISABLED)
            self.Button_Setup(File_frame,M09.Get_Language_Str("Speichern in Datei"),self.__Save_Button_Click,"S",Row=1)
            self.Button_Setup(File_frame,M09.Get_Language_Str("Laden aus Datei"),self.__Load_Button_Click,"L",Row=2)
            self.Button_Setup(File_frame,M09.Get_Language_Str("Kopiere von Seite zu Seite"),self.__Copy_Page_Button_Click,"K",Row=3,state=tk.DISABLED)
            
            self.label5 = ttk.Label(File_frame, text=M09.Get_Language_Str("Speichern und Laden einzelner oder mehrerer Seiten"),wraplength=window_width/2-20,font=("Tahoma", 11))
            self.label6 = ttk.Label(File_frame, text=M09.Get_Language_Str("Mit den Knöpfen links können die Daten der aktuellen Seite gespeichert und wieder geladen werden."),wraplength=window_width/2-20,font=("Tahoma", 8))
            self.label5.grid(row=0,column=1)
            self.label6.grid(row=1,column=1,rowspan=3)
            
            Update_frame = tk.Frame(self.container)
            Update_frame_Name = M09.Get_Language_Str("Update")
            self.tabdict[Update_frame_Name] = Update_frame
            self.container.add(Update_frame, text=Update_frame_Name)
            
            self.Button_Setup(Update_frame,M09.Get_Language_Str("Aktualisiere Bibliotheke"),self.__Update_to_Arduino_Button_Click,"",Row=0,label_text="Aktualisiert die MobaLedLib auf den offiziellen freigegebenen Stand welcher in der Arduino IDE verfügbar ist.")
            self.Button_Setup(Update_frame,M09.Get_Language_Str("Installiere Beta Test"),self.__Update_Beta_Button_Click,"",Row=1,label_text="Installiert die Beta Test Version der MobaLedLib Bibliothek.\n(Nur für Experten)")
            self.Button_Setup(Update_frame,M09.Get_Language_Str("Status der Bibliotheken"),self.__Show_Lib_and_Board_Page_Button_Click,"",Row=2,label_text="Zeigt den Status aller installierten Bibliotheken und Boards an.")
            self.Button_Setup(Update_frame,M09.Get_Language_Str("Aktualisiere pyMobLedLib"),self.__Update_pyMobaLedLib_Button_Click,"",Row=3,label_text="Aktualisiert pyMobaLedLib auf die neueste Version.")
                           
            Bootloader_frame = tk.Frame(self.container)
            Bootloader_frame_Name = M09.Get_Language_Str("Bootloader")
            self.tabdict[Bootloader_frame_Name] = Bootloader_frame
            self.container.add(Bootloader_frame, text=Bootloader_frame_Name)
            
            self.Button_Setup(Bootloader_frame,M09.Get_Language_Str("Schnellen Bootloader"),self.__FastBootloader_Button_Click,"",Row=0,label_text="Installiert den schnellen Bootloader auf dem linken Arduino.")
            
        
        self.lower_Button_frame = tk.Frame(self.top)
        self.lower_Button_frame.grid(row=2,column=0)
        
        self.Button_Setup(self.lower_Button_frame,M09.Get_Language_Str("Mail an Hardi"),self.__HardiForum_Button_Click,"H",Row=0)
        
        self.Button_Setup(self.lower_Button_frame,M09.Get_Language_Str("Schließen"),self.__Close_Button_Click,"S",Row=1)
                       
        
                
    def UserForm_Activate(self, first_page_only=False):
        #------------------------------
        # Is called every time when the form is shown
        M25.Make_sure_that_Col_Variables_match()
        
        #self.ESP32_L = ESP32_Lib_Installed()                                   ' 11.11.20:
        #self.Pico_L = PICO_Lib_Installed()                                    ' 18.04.21: Juergen
        #self.Uno_L = True
        #self.Board_IDE_L = True
        
        
        self.__Disable_Set_Arduino_Typ = True
        self.__Get_Arduino_Typ(True)
        if not first_page_only:
            self.__Get_Arduino_Typ(False)
        self.__Disable_Set_Arduino_Typ = False
        
    def Hide(self):
        self.top.destroy()
        
    def control_to_radiobutton(self):
        for rb in self.radiobuttons.keys():
            control = self.Controls.get(rb,P01.CControl(False))
            if control.Value==True:
                rb_var=self.rb_res.get(rb[-2:])
                rb_var.set(self.radiobuttons[rb]["value"])
                
    def radiobutton_to_board(self,leftarduino):
        if leftarduino:
            buttonvalue = self.rb_res["_L"].get()
        else:
            buttonvalue = self.rb_res["_R"].get()
        return self.boardlist[buttonvalue]
        
    def Show(self, first_page_only=False):
        self.IsActive = True
        M25.Make_sure_that_Col_Variables_match()
        self.__UserForm_Initialize(first_page_only=first_page_only)
        self.UserForm_Activate(first_page_only=first_page_only)
        self.control_to_radiobutton()
     
        self.controller.wait_window(self.top)
        
    
    # VB2PY (UntranslatedCode) Option Explicit
