# -*- coding: utf-8 -*-
#
#         MobaLedCheckColors: Color checker for WS2812 and WS2811 based MobaLedLib
#
#         ServoTestPage
#
# * Version: 1.00
# * Author: Harold Linke
# * Date: December 25th, 2019
# * Copyright: Harold Linke 2019
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
# * MobaLedCheckColors is free software: you can servo_0istribute it and/or modify
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
# * tkcolorpicker is free software: you can servo_0istribute it and/or modify
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

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from tkinter import filedialog
import ExcelAPI.XLA_Application as X02
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcolorpicker.spinbox import Spinbox
from tkcolorpicker.limitvar import LimitVar
from tools.CRCalgorithms import TinyRail_GenerateChecksum, CalculateControlValuewithChecksum, CalculateControlValuewithChecksum_old

from mlpyproggen.DefaultConstants import COLORCOR_MAX, DEFAULT_PALETTE, LARGE_FONT, NORMAL_FONT, SMALL_FONT, VERY_LARGE_FONT, PROG_VERSION, PERCENT_BRIGHTNESS, BLINKFRQ
# fromx mlpyproggen.dictFile import saveDicttoFile, readDictFromFile
import mlpyproggen.dictFile as dictFile
from scrolledFrame.ScrolledFrame import VerticalScrolledFrame,HorizontalScrolledFrame,ScrolledFrame
from locale import getdefaultlocale
import re
import time
import logging
import pattgen.D00_Forms as D00
import mlpyproggen.Pattern_Generator as PG
import ExcelAPI.XLWA_WinAPI as X03
import tools.CRCalgorithms as CRC

PERCENT_BRIGHTNESS = 1  # 1 = Show the brightnes as percent, 0 = Show the brightnes as ">>>"# 03.12.19:

COLORCOR_MAX = 255

ARDUINO_WAITTIME = 0.5

Servo_Scale_Min = 0

Servo_Min = 10

Servo_Stop = 0

Servo_Scale_Max = 255

Servo_delay = 200

# ----------------------------------------------------------------
# Class ServoTestPage
# ----------------------------------------------------------------

class ServoTestPage2(tk.Frame):

    # ----------------------------------------------------------------
    # ServoTestPage __init__
    # ----------------------------------------------------------------

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.tabClassName = "ServoTestPage2"
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.fontlabel = self.controller.get_font("FontLabel")
        self.fontspinbox = self.controller.get_font("FontSpinbox")
        self.fonttext = self.controller.get_font("FontText")
        self.fontbutton = self.controller.get_font("FontLabel")
        self.fontentry = self.controller.get_font("FontEntry")
        self.fonttext = self.controller.get_font("FontText")
        self.fontscale = self.controller.get_font("FontScale")
        self.fonttitle = self.controller.get_font("FontTitle")

        macrodata = self.controller.MacroDef.data.get(self.tabClassName,{})
        self.tabname = macrodata.get("MTabName",self.tabClassName)
        self.title = macrodata.get("Title",self.tabClassName)

        #button1_text = macrodata.get("Button_1",self.tabClassName)
        #button2_text = macrodata.get("Button_2",self.tabClassName)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        self.frame=ttk.Frame(self,relief="ridge", borderwidth=1)
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)

        self.scroll_main_frame = ScrolledFrame(self.frame)
        self.scroll_main_frame.grid_columnconfigure(0,weight=1)
        self.scroll_main_frame.grid_rowconfigure(0,weight=1)

        self.main_frame = ttk.Frame(self.scroll_main_frame.interior, relief="flat", borderwidth=0)
        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(2,weight=1)

        title_frame = ttk.Frame(self.main_frame, relief="flat", borderwidth=0)

        label = ttk.Label(title_frame, text=self.title, font=self.fonttitle)
        label.pack(padx=5,pady=(5,5))

        config_frame = self.controller.create_macroparam_frame(self.main_frame,self.tabClassName, maxcolumns=4,startrow =1,style="CONFIGPage")

        self.on_lednum = 0

        led = self.getConfigData("lastLed")

        serport = controller.arduino

        self.tab_frame = ttk.Frame(self.main_frame,borderwidth=0,relief="flat")

        #direct control frame for servos
        direct_control_frame = ttk.Frame(self.tab_frame,relief="flat", borderwidth=0)

        servo_direct_position_frame = ttk.Frame(direct_control_frame, relief="flat", borderwidth=0)
        servo_direct_position_frame.grid(row=0, column=0, padx=0, pady=0,sticky="")

        #dc_label1 = ttk.Label(servo_direct_position_frame, text='Servo Direct Control').grid(row=0, column=0, sticky='w', padx=4, pady=4)

        servo_direct_position_frame.columnconfigure(0, weight=1)

        self.buttonEnter=tk.Label(servo_direct_position_frame, text="ENTER",width=15,height=4,fg="black",relief="raised",font=self.fontbutton)

        self.controller.ToolTip(self.buttonEnter, text="Enter")
        self.buttonEnter.bind("<ButtonRelease-1>",lambda event: self.servo_prog_label_released(event=event,code=0))
        self.buttonEnter.bind("<Button-1>",lambda event: self.servo_prog_label_pressed(event=event,code=0))

        self.buttonProgramServo=ttk.Button(servo_direct_position_frame, text="Servo-Attiny Programmieren", command=self.servo_program_button, style='my.TButton')

        self.controller.ToolTip(self.buttonProgramServo, text="Servo Programm mit Programmieradapter auf den Servo hochladen")

        self.buttonProgramServodirect=ttk.Button(servo_direct_position_frame, text="Attiny Direkt Programmieren", command=self.servo_program_direct_button, style='my.TButton')

        self.controller.ToolTip(self.buttonProgramServodirect, text="Servo Programm OHNE Programmieradapter direkt auf den Attiny hochladen")
        #self.buttonEnter.bind("<ButtonRelease-1>",lambda event: self.servo_prog_label_released(event=event,code=0))
        #self.buttonEnter.bind("<Button-1>",lambda event: self.servo_prog_label_pressed(event=event,code=0))


        self.progress_var = tk.IntVar()
        self.progress_var.set(0)
        self.progress_bar = ttk.Progressbar(servo_direct_position_frame, orient="horizontal", length=440, mode="determinate", variable=self.progress_var)
        
        self.progress_message_var = tk.StringVar()
        self.progress_message_var.set("")
        self.progress_message = tk.Label(servo_direct_position_frame, textvariable=self.progress_message_var, width=80,height=3)

        self.servo_pos_var = tk.DoubleVar()
        self.servo_pos_var.set(0)
        #self.servo_scale = ttk.Scale( servo_direct_position_frame, variable = self.servo_pos_var,command=self._update_servo_position,from_=0,to=220,orient=tk.HORIZONTAL,length=440)
        self.servo_scale = tk.Scale( servo_direct_position_frame, variable = self.servo_pos_var,command=self._update_servo_position,from_=Servo_Scale_Min,to=Servo_Scale_Max,orient=tk.HORIZONTAL,length=440,label="Servo position",tickinterval=20,font=self.fontscale)

        self.controller.ToolTip(self.servo_scale, text="Position of Servo 0..255\nAnklicken zum Aktivieren der Tasten:\n[Right]/[Left]\n - single step\n[CTRL-Right]/[CTRL-Left]\n - long step\n[Pos1]/[Ende}\n - Anfang/Ende\n"+
                                "\nKlicken auf dem Sliderfeld:\n<Linke Taste>\n - single step vorwärts/rückwärts\n<Rechte Taste>\n - spring zum angeklickten Wert\n<CTRL Linke Taste>\n - springe zum Anfang/Ende")
        self.servo_scale.focus_set()
        self.servo_scale.bind("<Button-1>", self.servo_scale_focus_set)
        self.servo_position = 0
        self.enter_pressed = False
        self.servo_programm_step_1 = False
        self.servo_continue_update_status = False
        self.servo_set_mode_normal = False
        self.servo_refresh_delay = 150

        servo_program_frame =ttk.Frame(self.tab_frame,relief="flat", borderwidth=0,width=500)

        # ------------- SERVO Pos
        s = ttk.Style()
        s.configure('my.TButton', font=self.fontbutton)

        self.servo_scale.grid(row=0,column=1,sticky="")
        self.buttonEnter.grid(row=0,column=0,sticky="",padx=20, pady=10)
        self.buttonProgramServo.grid(row=0,column=2,sticky="",padx=20, pady=10)
        self.buttonProgramServodirect.grid(row=1,column=2,sticky="",padx=20, pady=10)
        self.progress_bar.grid(row=1,column=1,sticky="",padx=20, pady=10)
        self.progress_message.grid(row=2,column=1,sticky="",padx=20, pady=10)


        # --- placement
        self.frame.grid(row=0,column=0)
        self.scroll_main_frame.grid(row=0,column=0,sticky="nesw")
        # scroll_main_frame
        self.main_frame.grid(row=0,column=0)
        # main_frame
        title_frame.grid(row=0, column=0, pady=5, padx=5)
        config_frame.grid(row=1, column=0, pady=5, padx=5)
        self.tab_frame.grid(row=2, column=0, pady=0, padx=5)

        self.main_frame.columnconfigure(0,weight=1)

        # tab_frame
        direct_control_frame.grid(row=1, rowspan=1, column=0, pady=0, padx=5, sticky="")
        servo_program_frame.grid(row=2, column=0, pady=0, padx=5,sticky="ew")

        self.tab_frame.grid_columnconfigure(0,weight=1)

        self.tab_frame.grid_rowconfigure(3,weight=1)

        # --- bindings
        #self.controller.bind("<Control-Right>",self.s_servo_address.invoke_buttonup)
        #self.controller.bind("<Control-Left>",self.s_servo_address.invoke_buttondown)
        #self.controller.bind("<Control-Up>",self.s_servo_channel.invoke_buttonup)
        #self.controller.bind("<Control-Down>",self.s_servo_channel.invoke_buttondown)
        self.controller.bind("<F1>",self.controller.call_helppage)
        self.controller.bind("<Alt-F4>",self.cancel)
        self.controller.bind("<Control-o>",self.led_off)


    def cancel(self,_event=None):
        try:
            pass
        except:
            pass

    def tabselected(self):
        logging.debug("Tabselected: %s",self.tabname)
        #self.controller.currentTabClass = self.tabClassName
        #self.controller.send_to_ARDUINO("#BEGIN")
        #time.sleep(ARDUINO_WAITTIME)
        #self.controller.connect()
        self.controller.ARDUINO_begin_direct_mode()
        #self.controller.bind("<Control-Down>",self.s_servo_address.invoke_buttonup)
        #self.controller.bind("<Control-Up>",self.s_servo_address.invoke_buttondown)
        #self.controller.bind("<Control-Right>",self.s_servo_channel.invoke_buttonup)
        #self.controller.bind("<Control-Left>",self.s_servo_channel.invoke_buttondown)

        self.controller.bind("<F1>",self.controller.call_helppage)
        self.controller.bind("<Alt-F4>",self.cancel)
        self.servo_continue_update_status = True
        self.servo_status_loop()

    def tabunselected(self):
        logging.debug("Tabunselected: %s",self.tabname)
        #self.controller.send_to_ARDUINO("#END")
        #time.sleep(ARDUINO_WAITTIME)
        self.controller.ARDUINO_end_direct_mode()

        self.servo_continue_update_status = False

        logging.info(self.tabname)
        pass

    def getConfigData(self, key):
        return self.controller.getConfigData(key)

    def readConfigData(self):
        self.controller.readConfigData()

    def setConfigData(self,key, value):
        self.controller.setConfigData(key, value)

    def setParamData(self,key, value):
        self.controller.setParamData(key, value)

    def connect(self,port):
        pass

    def disconnect(self):
        pass


    def servo_scale_focus_set(self,event=None):
        self.servo_scale.focus_set()

    def _update_servo_channel(self, servo_address, servo_control, position):
        #if servo_control == 0:
        self._update_servos(servo_address, position, servo_control, 0)
        #elif servo_control == 1:
        #    self._update_servos(servo_address, 1, position, 1)
        #else:
        #    self._update_servos(servo_address, 1, 1, position)

    def _update_servo_position(self, position):
        position_int=int(position)
        self.servo_position = position_int

        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_control = int(self.controller.get_macroparam_val(self.tabClassName, "ServoControl"))
        #if servo_control in [1, 2, 3]:

            #self._update_servo_channel(servo_address, servo_control, position_int)

    def led_off(self,_event=None):
    # switch off all LED
        self.ledhighlight = False
        if self.controller.mobaledlib_version == 1:
            message = "#L00 00 00 00 FF\n"
        else:
            message = "#L 00 00 00 00 7FFF\n"
        self.controller.send_to_ARDUINO(message)
        #self.controller.ledtable.clear()

    def servo_program_button(self,event=None,code=0):
    # send code to Servo
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        D00.MainMenu_Form.Show(page1=1, page2=3, AttinyAdress=servo_address)

    def get_high_byte(self, value):
        # Shift the value 8 bits to the right to get the high byte
        high_byte = (value >> 8) & 0xFF
        return high_byte

    def get_low_byte(self, value):
        # Mask the value with 0xFF to get the low byte
        low_byte = value & 0xFF
        return low_byte

    # Control commands for Attiny bootloader
    #--------------------------------------------------------------------------------------------------------------
    #|     | CRC-4 nach ITU | ENTER-Bit | Command 0..7 | 2. Byte Modulo | 3. Byte reserved | 4.-24. Byte HEX-Data |
    #--------------------------------------------------------------------------------------------------------------
    #| Bit |        7 6 5 4 |         3 |        2 1 0 |                |                  |                      |
    #--------------------------------------------------------------------------------------------------------------
    #|     |        0 0 0 0 |         0 |        0 0 0 |         unused |           unused |               unused | idle, nothing to do
    #--------------------------------------------------------------------------------------------------------------
    #|     |        invalid |         X |        X X X | not applicable |   not applicable |       not applicable | failure on WS2811 Bus
    #--------------------------------------------------------------------------------------------------------------
    #|     |          valid |   first 1 |        0 0 1 |    modulo (*1) |                0 |   HEX-File-Data (*2) | TRANSFER Update File first block/line
    #--------------------------------------------------------------------------------------------------------------
    #|     |          valid |  follow 0 |        0 0 1 |    modulo (*1) |                0 |   HEX-File-Data (*2) | TRANSFER Update File following blocks/lines
    #--------------------------------------------------------------------------------------------------------------
    #|     |          valid |         0 |        0 1 1 |  LEDs-zero-low |   LEDs-zero-high |                all 0 | prerequisite: shift WS2811 Status-LED pos
    #--------------------------------------------------------------------------------------------------------------
    #|     |          valid |         1 |        0 1 1 |  LEDs-zero-low |   LEDs-zero-high |                all 0 | execute: memorize WS2811 Status-LED pos (*3)
    #--------------------------------------------------------------------------------------------------------------


    def send_21bytes_to_Attiny(self, servo_address, command, byte2, byte3, bytestring, first_line=False):
        # changes the 21 bytes following the servo_adress in the MLL-WS2812-stream
        # servo_address: RGB-LED number of the servo in the MLL-Stream
        # bytestring: 24 bytes to upload to Attiny
        # first_line: the first hex-line has to be marked as first=True

        #reset command to 0000 to allow sending of the 21 bytes before flashing them into the Attiny EEPROM
        self.send_command_to_attiny(servo_address, command=0, byte2=0, byte3=0, enter=False, start_CRC4=0, gen_CRC4=0)
        #X03.Sleep(100)
        #crc4 = 0
        crc4 = TinyRail_GenerateChecksum( controlValue=command, positionValueHigh=byte2, positionValueLow=0, start_CRC4=0)
        bytenum = 0
        blen = len(bytestring)
        curr_address = servo_address + 1 # bytes werden hinter dem Kommando geschrieben.
        for i in range(21):
            if bytenum == 0:
                if i < blen:
                    dbyte1 = bytestring[i]
                else:
                    dbyte1 = 0
                crc4 =  CRC.CalcCrc4( crc4, dbyte1, 8)
                bytenum = 1
            elif bytenum == 1:
                if i < blen:
                    dbyte2 = bytestring[i]
                else:
                    dbyte2 = 0
                crc4 =  CRC.CalcCrc4( crc4, dbyte2, 8)
                bytenum = 2
            elif bytenum == 2:
                if i < blen:
                    dbyte3 = bytestring[i]
                else:
                    dbyte3 = 0
                crc4 =  CRC.CalcCrc4( crc4, dbyte3, 8)
                bytenum = 0
                self.send_command_to_attiny(curr_address, command=dbyte1, byte2=dbyte2, byte3=dbyte3, enter=False, gen_CRC4=False)
                curr_address += 1

        # all bytes send, update command for uploading

        newCommand = ( crc4 & 0x0F) << 4 | ( command & 0x0F)
        self.send_command_to_attiny(servo_address, command=newCommand, byte2=byte2, byte3=0, enter=first_line, start_CRC4=0, gen_CRC4=False)
        self.send_command_to_attiny(servo_address, command=newCommand, byte2=byte2, byte3=0, enter=first_line, start_CRC4=0, gen_CRC4=False)
        self.send_command_to_attiny(servo_address, command=newCommand, byte2=byte2, byte3=0, enter=first_line, start_CRC4=0, gen_CRC4=False)

    def update_upload_info(self):

        delta = len(self.controller.serial_writebuffer) - self.controller.serial_writebuffer_idx

        if len(self.controller.serial_writebuffer) > 0:
            delta_percent = self.controller.serial_writebuffer_idx * 100 / len(self.controller.serial_writebuffer)
        else:
            delta_percent = 0
        self.progress_var.set(delta_percent)
        if self.controller.serial_writebuffer_idx >= len(self.controller.serial_writebuffer):
            self.upload_complete = True
            self.progress_message_var.set("Hochladen zum Attiny beendet")
            self.buttonProgramServodirect.config(text = "Attiny direkt Programmieren")
        else:
            
            self.controller.after(1000, self.update_upload_info)


    def Upload_firmware_direkt(self, hexfile_name="", AttinyAdress=None):
        print("Upload Firmware direkt:", hexfile_name, AttinyAdress)
        logging.debug("Upload Firmware direkt: "+ hexfile_name, AttinyAdress)
        self.progress_message_var.set("Hochladen zum Attiny gestartet")
        
        self.buttonProgramServodirect.config(text = "Abbrechen")
        
        PG.ThisWorkbook.Activate()
        WorkDir = PG.ThisWorkbook.Path + "/hex-files"

        if Dir(WorkDir + "/"+ hexfile_name) == '':
            # ask for filename - makefile or hexfile_name

            filenameandpath = filedialog.askopenfilename(filetypes=[("hex-File","*.blthex")], initialdir=WorkDir)
            if not filenameandpath:
                return
            if not os.path.exists(filenameandpath):
                #print ('file does not exist')
                return
            filepath,filename = os.path.split(filenameandpath)
            WorkDir = filepath
            hexfile_name = filename
            if Dir(WorkDir + "/"+ hexfile_name) == '':
                return

        X02.ChDrive(WorkDir)
        ChDir(WorkDir)

        # Read the .hex file and convert each line to binary
        with open(hexfile_name, 'r') as hex_file:
            lines = hex_file.readlines()

            logging.debug("Upload Firmware direkt - file opened: "+ hexfile_name, AttinyAdress)
            self.controller.send_to_ARDUINO_init_buffer()
            self.servo_continue_update_status = False

            hexline_nr = 0
            len_lines = len(lines)
            first = True # marks first line
            modulo = 0
            while hexline_nr < len_lines and self.continue_upload:
                print("Block-Nr:", hexline_nr)
                logging.debug("Upload Firmware direkt - send hex line: "+ str(hexline_nr))
                hex_line = lines[hexline_nr]
                hex_line2 = hex_line[1:len(hex_line)-1]
                bytestring = bytes.fromhex(hex_line2)
                bytestring = bytestring.ljust(21, b'\x00')
                blen = len(bytestring)

                self.send_21bytes_to_Attiny(AttinyAdress, 1, modulo, 0, bytestring, first_line=first)

                first = False
                hexline_nr += 1
                modulo += 1
                modulo = modulo % 256
            # setze alles wiederr auf 0

            self.send_21bytes_to_Attiny(AttinyAdress, 0, 0, 0, b'', first_line=first)

            self.upload_complete = False
            self.controller.after(1000, self.update_upload_info)


    def servo_program_direct_button(self,event=None,code=0):
    # send code to Servo
        
        if self.buttonProgramServodirect.cget("text") == "Abbrechen":
            self.continue_upload = False
            self.controller.send_to_ARDUINO_init_buffer()
            return
        self.continue_upload = True
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_status_led_address = self.controller.get_macroparam_val(self.tabClassName, "ServoStatusLEDAddress")
        ok_button = D00.UserForm_Attiny_direct_program.Show_Dialog(AttinyAdress=servo_address, StatusLEDAdress=servo_status_led_address)
        if ok_button:
            #set status LED address
            enter_bootloader = True # D00.UserForm_Attiny_direct_program.Enter_Bootloader_CheckBox.Value
            set_status_led = True # D00.UserForm_Attiny_direct_program.Set_Status_LED_CheckBox.Value
            upload_hex_file = True # D00.UserForm_Attiny_direct_program.Upload_Hex_File_CheckBox.Value

            if enter_bootloader:
                # enter bootloader
                self.send_command_to_attiny(servo_address, command=7, byte2=0x01, byte3=0xC9)
                X03.Sleep(100)
                self.send_command_to_attiny(servo_address, command=7, byte2=0x01, byte3=0xC9, enter=True)
                X03.Sleep(100)
                # bootloader entered

            if servo_status_led_address:
            # set status LED pos
                if servo_status_led_address != 0:
                    delta_servo_status_led_address = servo_status_led_address - servo_address # only delta is needed
                    if delta_servo_status_led_address <= 0:
                        delta_servo_status_led_address = 0
                else:
                    delta_servo_status_led_address = 0

                delta_servo_status_led_address_high = self.get_high_byte(delta_servo_status_led_address)
                delta_servo_status_led_address_low = self.get_low_byte(delta_servo_status_led_address)
                #self.send_command_to_attiny(servo_address, command=5, byte2=delta_servo_status_led_address_low, byte3=delta_servo_status_led_address_high)
                self.send_21bytes_to_Attiny(servo_address, 3, delta_servo_status_led_address_low, delta_servo_status_led_address_high, b'', first=False)
                X03.Sleep(100)
                self.send_21bytes_to_Attiny(servo_address, 3, delta_servo_status_led_address_low, delta_servo_status_led_address_high, b'', first=True)
                X03.Sleep(100)

            if upload_hex_file:
                self.Upload_firmware_direkt(AttinyAdress=servo_address)



    def servo_status_loop(self, event=None):
        self.servo_update_status()
        if self.servo_continue_update_status:
            self.after(Servo_delay, self.servo_status_loop)

    def servo_update_status(self):
        global Servo_delay
        servo_address = self.controller.get_macroparam_val(self.tabClassName, "ServoAddress")
        servo_control = int(self.controller.get_macroparam_val(self.tabClassName, "ServoControl"))
        servo_position = self.servo_position
        servo_use_old_crc = int(self.controller.get_macroparam_val(self.tabClassName, "ServoCRCold"))
        if servo_use_old_crc: #
            Servo_delay = 40
        else:
            Servo_delay = 50

        enter_pressed = self.enter_pressed
        #print("Servo status update", self.servo_position, servo_control, enter_pressed)
        if servo_control == 1: # normal position
            self._update_servos(servo_address,servo_position,servo_control,0)
        elif servo_control == 2 : # normal endpos training
            if enter_pressed:
                servo_control += 8 # set input bit
            self._update_servos(servo_address,servo_position,servo_control,0)
        elif servo_control == 3 : # wide endpos training
            if enter_pressed:
                servo_control += 8 # set input bit
            self._update_servos(servo_address,servo_position,servo_control,0)
        elif servo_control == 4 : # prog max speed
            if enter_pressed:
                servo_control += 8 # set input bit
                self.servo_set_mode_normal = True
            self._update_servos(servo_address,servo_position,servo_control,0x9A)
        elif servo_control == 5 : # Toggle invers
            if enter_pressed:
                self._update_servos(servo_address,1,12,0x15)
                self.servo_set_mode_normal = True
            else:
                self._update_servos(servo_address,1,4,0x15)
        elif servo_control == 6 : # Reset servo
            if enter_pressed:
                self._update_servos(servo_address,0xE9,13,0x8A)
                self.servo_set_mode_normal = True
            else:
                self._update_servos(servo_address,0xE9,5,0x8A)
        elif servo_control == 7 : # reset all factory defaults
            if enter_pressed:
                self._update_servos(servo_address,0x16,13,0x75)
                self.servo_set_mode_normal = True
            else:
                self._update_servos(servo_address,0x16,5,0x75)
        elif servo_control == 8 : # reset last position
            if enter_pressed:
                self._update_servos(servo_address,0x5A,13,0x9E)
                self.servo_set_mode_normal = True
            else:
                self._update_servos(servo_address,0x5A,5,0x9E)

    def servo_prog_label_pressed(self,event=None,code=0):
    # send <Enter> to Servo
        event.widget.config(relief="sunken")
        self.enter_pressed = True
        servo_control = int(self.controller.get_macroparam_val(self.tabClassName, "ServoControl"))
        if servo_control == 2 or servo_control == 3: # programming in progress
            if self.servo_programm_step_1:
                event.widget.config(text="Enter")
                self.servo_programm_step_1 = False
                self.servo_set_mode_normal = True
                # self.controller.set_macroparam_val(self.tabClassName, "ServoControl", 0)
            else:
                event.widget.config(text="2nd Step")
                self.servo_programm_step_1 = True

    def servo_prog_label_released(self,event=None,code=100):
    # send <Enter> released to servo
        event.widget.config(relief="raised")
        self.enter_pressed = False
        if self.servo_set_mode_normal:
            self.servo_set_mode_normal = False
            self.controller.set_macroparam_val(self.tabClassName, "ServoControl", 0)

    def send_command_to_attiny(self, servo_address, command=0, byte2=0, byte3=0, enter=False, start_CRC4=0,gen_CRC4=True ):
        if enter:
            command += 8
        self._update_servos(servo_address,byte2,command,byte3, start_CRC4=start_CRC4, gen_CRC4=gen_CRC4)



    def _update_servos(self, lednum, positionValueHigh, controlValue, positionValueLow, start_CRC4=0, gen_CRC4=True):
        #servo_use_old_crc = int(self.controller.get_macroparam_val(self.tabClassName, "ServoCRCold"))
        if gen_CRC4:

            #if servo_use_old_crc:
            #    newcontrolValue =  CalculateControlValuewithChecksum_old (controlValue, positionValueHigh, positionValueLow)
            #else:
            newcontrolValue =  CalculateControlValuewithChecksum (controlValue, positionValueHigh, positionValueLow, start_CRC4=start_CRC4)
        else:
            newcontrolValue = controlValue
        if self.controller.mobaledlib_version == 1:
            message = "#L" + '{:02x}'.format(lednum) + " " + '{:02x}'.format(positionValueHigh) + " " + '{:02x}'.format(newcontrolValue) + " " + '{:02x}'.format(positionValueLow) + " " + '{:02x}'.format(1) + "\n"
        else:
            message = "#L " + '{:02x}'.format(lednum) + " " + '{:02x}'.format(positionValueHigh) + " " + '{:02x}'.format(newcontrolValue) + " " + '{:02x}'.format(positionValueLow) + " " + '{:04x}'.format(1) + "\n"
        self.controller.send_to_ARDUINO(message)
        #time.sleep(0.2)






