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
# 2021-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2022-01-07 v4.02 HL: - Else:, ByRef check done - first PoC release
# 2022-03-13 v4.15 HL: - Update to MLL 3.1.0D


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *
# fromx proggen.M02_Public import *
# fromx proggen.M06_Write_Header_LED2Var import *
# fromx proggen.M06_Write_Header_Sound import *
# fromx proggen.M06_Write_Header_SW import *
# fromx proggen.M08_ARDUINO import *
# fromx proggen.M09_Language import *
# fromx proggen.M09_Select_Macro import *
# fromx proggen.M20_PageEvents_a_Functions import Update_Start_LedNr
# fromx proggen.M25_Columns import *
# fromx proggen.M28_Diverse import *
# fromx proggen.M30_Tools import *
# fromx proggen.M80_Create_Multiplexer import *

# fromx ExcelAPI.X02_Workbook import *
# fromx mlpyproggen.F_UserForm_Header_Created import *

import proggen.M02_Public as M02
import proggen.M02a_Public as M02a
#import proggen.M03_Dialog as M03
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M06b_Read_MLLConfig as M06b
import proggen.M07_COM_Port as M07
import proggen.M07_COM_Port_New as M07New
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M18a_Load_PicoConfig as M18a
import proggen.M25_Columns as M25
#import proggen.M27_Sheet_Icons as M27
import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M38_Extensions as M38
import proggen.M39_Simulator as M39
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Multiplexer as M80
import mlpyproggen.Prog_Generator as PG
import mlpyproggen.ARDUINOMonitorPage as AMP
import pgcommon.G00_common as G00
import  proggen.F00_mainbuttons as F00

import ExcelAPI.XLA_Application as P01
from ExcelAPI.XLC_Excel_Consts import *
import ExcelAPI.XLWF_Worksheetfunction as XLWF

import tkinter as tk

import socket, time

import sys
try:
    import cpip
    cpip_imported = True
    from cpip.core import PpLexer, IncludeHandler
    from cpip.CPIPMain import preprocessFileToOutput    
except:
    cpip_imported = False

import collections

try:
    import requests
    requests_imported = True
except:
    requests_imported = False
    
    
HOUSE_PALETTE_List = ("ROOM_DARK",
                     "ROOM_BRIGHT",
                     "ROOM_WARM_W",
                     "ROOM_RED",
                     "ROOM_D_RED",
                     "ROOM_COL0",
                     "ROOM_COL1",
                     "ROOM_COL2",
                     "ROOM_COL3",
                     "ROOM_COL4",
                     "ROOM_COL5",
                     "ROOM_COL345",
                     "FIRE",
                     "FIRED", 
                     "FIREB",
                     "Reserved1", 
                     "ROOM_CHIMNEY",
                     "ROOM_CHIMNEYD",
                     "ROOM_CHIMNEYB",
                     "ROOM_TV0",
                     "ROOM_TV0_CHIMNEY",
                     "ROOM_TV0_CHIMNEYD",
                     "ROOM_TV0_CHIMNEYB",
                     "ROOM_TV1",
                     "ROOM_TV1_CHIMNEY",
                     "ROOM_TV1_CHIMNEYD",
                     "ROOM_TV1_CHIMNEYB",
                     "GAS_LIGHT",
                     "GAS_LIGHT1",
                     "GAS_LIGHT2", 
                     "GAS_LIGHT3",
                     "GAS_LIGHTD",
                     "GAS_LIGHT1D",
                     "GAS_LIGHT2D",
                     "GAS_LIGHT3D",
                     "NEON_LIGHT", 
                     "NEON_LIGHT1",
                     "NEON_LIGHT2",
                     "NEON_LIGHT3",
                     "NEON_LIGHTD",
                     "NEON_LIGHT1D",
                     "NEON_LIGHT2D",
                     "NEON_LIGHT3D",
                     "NEON_LIGHTM",
                     "NEON_LIGHT1M",
                     "NEON_LIGHT2M",
                     "NEON_LIGHT3M",
                     "NEON_LIGHTL",
                     "NEON_LIGHT1L",
                     "NEON_LIGHT2L",
                     "NEON_LIGHT3L",
                     "NEON_DEF_D",
                     "NEON_DEF1D",
                     "NEON_DEF2D",
                     "NEON_DEF3D",
                     "SINGLE_LED1",
                     "SINGLE_LED2",
                     "SINGLE_LED3",
                     "SINGLE_LED1D",                         
                     "SINGLE_LED2D",                                          
                     "SINGLE_LED3D",                      
                     "SKIP_ROOM", 
                     "CANDLE", #3E
                     "CANDLE1",
                     "CANDLE2",
                     "CANDLE3"
                     )

RAM_Usage_dict = {"FIRE":1,"FIRED":1, "FIREB":1,"ROOM_CHIMNEY":1,"ROOM_CHIMNEYD":1, "ROOM_CHIMNEYB":1, "ROOM_TV0_CHIMNEY":1,"ROOM_TV0_CHIMNEYD":1, "ROOM_TV0_CHIMNEYB":1,"ROOM_TV1_CHIMNEY":1, "ROOM_TV1_CHIMNEYD":1, "ROOM_TV1_CHIMNEYB" :1, "CANDLE": 1}

##Die Verschiedenen Ausgangstypen:
macro_list = {
"END" :                   0, 
"CONST":                 1, #Die ersten Ausgangstypen haben als Parameter eine channel mask mit
"RANDMUX":               2, #der ausgewaehlt wird welche LEDs angestuert werden
"SCHEDULE":              3, #Bei diesen Typen steht InCh an Position 2

"PATTERNT1":          10, #Muster mit einer Zeit fuer alle Zustaende
"PATTERNT2":          11, #Muster mit zwei abwechselnd genutzten Zeiten
"PATTERNT3":          12, #  "        drei     "
"PATTERNT4":          13, 
"PATTERNT5":          14, 
"PATTERNT6":          15, 
"PATTERNT7":          16, 
"PATTERNT8":          17, 
"PATTERNT9":          18, 
"PATTERNT10":         19, 
"PATTERNT11":         20, 
"PATTERNT12":         21, 
"PATTERNT13":         22, 
"PATTERNT14":         23, 
"PATTERNT15":         24, 
"PATTERNT16":         25, 
"PATTERNT17":         26, 
"PATTERNT18":         27, 
"PATTERNT19":         28, 
"PATTERNT20":         29, 
"PATTERNT21":         30, 
"PATTERNT22":         31, 
"PATTERNT23":         32, 
"PATTERNT24":         33, 
"PATTERNT25":         34, 
"PATTERNT26":         35, 
"PATTERNT27":         36, 
"PATTERNT28":         37, 
"PATTERNT29":         38, 
"PATTERNT30":         39, 
"PATTERNT31":         40, 
"PATTERNT32":         41, 
"PATTERNT33":         42, 
"PATTERNT34":         43, 
"PATTERNT35":         44, 
"PATTERNT36":         45, 
"PATTERNT37":         46, 
"PATTERNT38":         47, 
"PATTERNT39":         48, 
"PATTERNT40":         49, 
"PATTERNT41":         50, 
"PATTERNT42":         51, 
"PATTERNT43":         52, 
"PATTERNT44":         53, 
"PATTERNT45":         54, 
"PATTERNT46":         55, 
"PATTERNT47":         56, 
"PATTERNT48":         57, 
"PATTERNT49":         58, 
"PATTERNT50":         59, 
"PATTERNT51":         60, 
"PATTERNT52":         61, 
"PATTERNT53":         62, 
"PATTERNT54":         63, 
"PATTERNT55":         64, 
"PATTERNT56":         65, 
"PATTERNT57":         66, 
"PATTERNT58":         67, 
"PATTERNT59":         68, 
"PATTERNT60":         69, 
"PATTERNT61":         70, 
"PATTERNT62":         71, 
"PATTERNT63":         72, 
"PATTERNT64":         73, 
#LAST_PATTERN":       PATTERNT64_T

"APATTERNT1":         74, #Muster mit einer Zeit fuer alle Zustaende mit analogen Uebergaengen
"APATTERNT2":         75, #Muster mit zwei abwechselnd genutzten Zeiten
"APATTERNT3":         76, # "        drei    "
"APATTERNT4":         77, 
"APATTERNT5":         78, 
"APATTERNT6":         79, 
"APATTERNT7":         80, 
"APATTERNT8":         81, 
"APATTERNT9":         82, 
"APATTERNT10":        83, 
"APATTERNT11":        84, 
"APATTERNT12":        85, 
"APATTERNT13":        86, 
"APATTERNT14":        87, 
"APATTERNT15":        88, 
"APATTERNT16":        89, 
"APATTERNT17":        90, 
"APATTERNT18":        91, 
"APATTERNT19":        92, 
"APATTERNT20":        93, 
"APATTERNT21":        94, 
"APATTERNT22":        95, 
"APATTERNT23":        96, 
"APATTERNT24":        97, 
"APATTERNT25":        98, 
"APATTERNT26":        99, 
"APATTERNT27":        100, 
"APATTERNT28":        101, 
"APATTERNT29":        102, 
"APATTERNT30":        103, 
"APATTERNT31":        104, 
"APATTERNT32":        105, 
"APATTERNT33":        106, 
"APATTERNT34":        107, 
"APATTERNT35":        108, 
"APATTERNT36":        109, 
"APATTERNT37":        110, 
"APATTERNT38":        111, 
"APATTERNT39":        112, 
"APATTERNT40":        113, 
"APATTERNT41":        114, 
"APATTERNT42":        115, 
"APATTERNT43":        116, 
"APATTERNT44":        117, 
"APATTERNT45":        118, 
"APATTERNT46":        119, 
"APATTERNT47":        120, 
"APATTERNT48":        121, 
"APATTERNT49":        122, 
"APATTERNT50":        123, 
"APATTERNT51":        124, 
"APATTERNT52":        125, 
"APATTERNT53":        126, 
"APATTERNT54":        127, 
"APATTERNT55":        128, 
"APATTERNT56":        129, 
"APATTERNT57":        130, 
"APATTERNT58":        131, 
"APATTERNT59":        132, 
"APATTERNT60":        133, 
"APATTERNT61":        134, 
"APATTERNT62":        135, 
"APATTERNT63":        136, 
"APATTERNT64":        137, 

#"LAST_PATTERN": "PATTERNT64_T"

"HOUSET":              138, #Erster Ausgangstyp ohne ChMsk (WITHOUT_CHANNEL_MASK). Hier steht InCh an Position 1. Bei den Typen davor steht InCh an Position 2.
"FIRE":                 139, 
"RANDOM":               140, 
"WELDING_CONT":         141, 
"WELDING":              142, 
"COPYLED":              143, 
"COUNTER":              144, 

"NEW_HSV_GROUP":        170,  #Erster Ausgangstyp ohne InpCh (WITHOUT_INP_CH)
"NEW_LOCAL_VAR":        171,                                                                           #07.11.18:
"USE_GLOBALVAR":        172, 

"INCH_TO_TMPVAR":     173,                                                                           #25.11.18:
"INCH_TO_TMPVAR1":    174,                                                                           #07.05.20:
"BIN_INCH_TO_TMPVAR": 175,                                                                           #18.01.19:
"BIN_INCH_TO_TMPVAR1":176,                                                                           #07.05.20:

"SET_COLTAB":          180, 
                                                                                         #10.01.20:
"SET_TV_TAB":          181, 
                                                                                       #12.01.20:
"SET_DEF_NEON":        182, 

"SET_CANDLETAB":       183,                                                                          #10.06.20:


"LOGIC":                184, 

"EXT_PROC_BASE":        240,    #Makro extensions may use type ids >=l EXT_PROC_BASE":up to 255     #21.10.21: Juergen

#Only used in the Charliplexing modul
"CPX_LED_ASSIGNEMENT":   200,    #Define the LED assignement
"CPX_ANALOG_INPUT":      201,    #Enable the analog input
"CPX_ANALOG_LIMMITS":    202,    #Table with analog limits which defines the Goto Nr levels

"WITHOUT_CHANNEL_MASK": "HOUSE_T", 
"WITHOUT_INP_CH":     "NEW_HSV_GROUP_T"
}


macro_substitue_dict = {"House": [("LED","InCh", "On_Min","On_Limit", "..."), ("HOUSE_T","LED+RAMH","InCh","On_Min","On_Limit","HOUSE_MIN_T","HOUSE_MAX_T","COUNT_VARARGS(__VA_ARGS__)", "__VA_ARGS__")]
                       }

RAM_Counter = 0

def add_RAM_Count(count):
    global RAM_Counter
    RAM_Counter += count
    
def add_2Byte_Value_to_config(current_index, value, config_ary, append=True):
    value = int(value)
    low_val = value % 256
    high_val = int(value/256)
    if append:
        config_ary.append(f"cv{current_index:04}={low_val:02X}\n")
        config_ary.append(f"cv{current_index + 1:04}={high_val:02X}\n")
    else:
        config_ary[current_index+6] = f"cv{current_index:04}={low_val:02X}\n"
        config_ary[current_index+7] = f"cv{current_index + 1:04}={high_val:02X}\n"
    return current_index + 2

def add_1Byte_Value_to_config(current_index, value, config_ary, append=True):
    value = int(value)
    if append:
        config_ary.append(f"cv{current_index:04}={value:02X}\n")
    else:
        config_ary[current_index+6] = f"cv{current_index:04}={value:02X}\n"
    return current_index + 1

def add_2Byte_Value_to_cv(current_index, value, config_ary, append=True):
    value = int(value)
    low_val = value % 256
    high_val = int(value/256) & 0xFF
    if append:
        config_ary.append(f"{low_val:02X}")
        config_ary.append(f"{high_val:02X}")
    else:
        config_ary[current_index-1] = f"{low_val:02X}"
        config_ary[current_index] = f"{high_val:02X}"
    return current_index + 2

def add_1Byte_Value_to_cv(current_index, value, config_ary, append=True):
    value = int(value) & 0xFF
    if append:
        config_ary.append(f"{value:02X}")
    else:
        config_ary[current_index-1] = f"{value:02X}"
    return current_index + 1

def get_inch_no(inch_str):
    if inch_str == "SI_1":
        return 255
    else:
        return 255 # dummy
    
def get_roomtype(roomtype_str):
    roomtype_str = roomtype_str.lstrip()
    add_RAM_Count(RAM_Usage_dict.get(roomtype_str, 0))
    return HOUSE_PALETTE_List.index(roomtype_str)
    
def generate_config_line(current_index, line, config_ary):
    linesplit1_ary = line.split("(")
    macro_name = linesplit1_ary[0]
    params_str = linesplit1_ary[1].split(")")[0]
    param_list = params_str.split(",")
    macro_name = macro_name.strip().upper()
    macro_code = macro_list[macro_name]
    #if macro_name.endswith("HouseT"):
    if macro_name == "HOUSET":
        
        macro_len = (len(param_list) + 2)
        current_index = add_1Byte_Value_to_cv(current_index, macro_code, config_ary)         # Macro Code
        current_index = add_2Byte_Value_to_cv(current_index, param_list[0], config_ary)      # first LED 2-bytes
        inch = get_inch_no(param_list[1])
        current_index = add_1Byte_Value_to_cv(current_index, inch, config_ary)               # InCh
        for i in range (2, 6):
            current_index = add_1Byte_Value_to_cv(current_index, param_list[i], config_ary)  # Parameters:min rooms on, max rooms on, min time to change, max time to change
        current_index = add_1Byte_Value_to_cv(current_index, len(param_list)-6, config_ary)  # number of rooms  
        for i in range (6, len(param_list)):
            room_type = get_roomtype(param_list[i])
            current_index = add_1Byte_Value_to_cv(current_index, room_type, config_ary) # Rooms
    elif macro_code in range(10, 74):
         # PATTERNTx
        pass
    elif macro_code in range(74, 138):
         # APATTERNTx
        pass
    elif macro_code == macro_list["FIRE"]:
        pass
    elif macro_code == macro_list["RANDOM"]:
        pass
    elif macro_code == macro_list["WELDING_CONT"]:
        pass
    elif macro_code == macro_list["WELDING"]:
        pass
    elif macro_code == macro_list["COPYLED"]:
        pass
    elif macro_code == macro_list["COUNTER"]:
        pass
    
    elif macro_code == macro_list["NEW_HSV_GROUP"]:
        pass
    elif macro_code == macro_list["NEW_LOCAL_VAR"]:
        pass
    elif macro_code == macro_list["USE_GLOBALVAR"]:
        pass
    
    elif macro_code == macro_list["INCH_TO_TMPVAR"]:
        pass
    elif macro_code == macro_list["INCH_TO_TMPVAR1"]:
        pass
    elif macro_code == macro_list["BIN_INCH_TO_TMPVAR"]: 
        pass
    elif macro_code == macro_list["BIN_INCH_TO_TMPVAR1"]:
        pass
    
    elif macro_code == macro_list["SET_COLTAB"]:
        pass

    elif macro_code == macro_list["SET_TV_TAB"]:
        pass
    elif macro_code == macro_list["SET_DEF_NEON"]:
        pass
    
    elif macro_code == macro_list["SET_CANDLETAB"]:
        pass
    elif macro_code == macro_list["LOGIC"]:
        pass
    return current_index,  macro_len

def generate_cvs(ConfigTxt, LEDsInUse):
    
    input_cfg = ConfigTxt.split("\n")
    # Open the file in write mode ('w') and add some text
    maxLEDcnt = 0
    for i in range (0,len(LEDsInUse)):
        maxLEDcnt+=int(LEDsInUse[i]) 

    config_ary = []
    
    config_ary.append("2B") # // low Gesamtlänge (immer ohne die 16 Bit der Länge selber)\n")
    config_ary.append("00") #  // high ...\n")
    
    # // Allgemeine Parameter, die nur EINMAL vorkommen\n")
    config_ary.append("14") #  // low Anzahl LEDs (im Sinne der MobaLedLib.cpp NICHT FastLED)\n")
    config_ary.append("00") #  // high ...\n")
    config_ary.append("0F") #  // low RAM Bedarf in Bytes\n")
    config_ary.append("00") #  // high ...\n")
    
    #config_ary.append("// Konfiguration der FastLED Controller\n")
    #config_ary.append("// (ein Controller besteht jeweils aus zwei 16Bit words)\n")
    config_ary.append("04") #  // low Länge der Strukturinformationen für FastLED Controller\n")
    config_ary.append("00") #  // high ...\n")
    config_ary.append("00") #  // low FastLED Controller 0 Start-LED Nummer\n")
    config_ary.append("00") #  // high ...\n")
    config_ary.append("14") #  // low FastLED Controller 0 Number of LEDs\n")
    config_ary.append("00") #  // high ...\n")
    
    #config_ary.append("// Ext_Addr für DCC Address Mappings\n")
    #config_ary.append("// (ein Mapping besteht jeweils aus zwei 16Bit words)\n")
    config_ary.append("04") #  // low Länge der Ext_Addr Strukturinformationen\n")
    config_ary.append("00") #  // high ...\n")
    config_ary.append("FF") #  // low DCC AddrAndTyp (0xFF is a default-dummy)\n")
    config_ary.append("FF") #  // high ...           (0xFF is a default-dummy)\n")
    config_ary.append("FF") #  // InCnt (low ffs)    (0xFF is 1 default-dummy)\n")
    config_ary.append("00") #  // high ffs\n")
    
    #config_ary.append("// LED2Var für Eingangsvariablen\n")
    #config_ary.append("// (ein Mapping besteht jeweils aus zwei 16Bit words und zwei bytes, also\n")
    #config_ary.append("// insgesamt 6 byte)\n")
    config_ary.append("06") #  // low Länge der LED2Var_tab Strukturinformationen\n")
    config_ary.append("00") #  // high ...\n")
    config_ary.append("FF") #  // Var_Nr (InCnt) (low ffs) (0xFF is a default-dummy)\n")
    config_ary.append("FF") #  // high ffs                 (0xFF is a default-dummy)\n")
    config_ary.append("FF") #  // LED_Nr (low ffs)         (0xFF is a default-dummy)\n")
    config_ary.append("FF") #  // high ffs                 (0xFF is a default-dummy)\n")
    config_ary.append("FF") #  // Offset_And_Typ           (0xFF is a default-dummy)\n")
    config_ary.append("FF") #  // Value (to compare)       (0xFF is a default-dummy)\n")
    
    #config_ary.append("// ab hier kommt die eingentliche MLL Konfiguration\n")
    #config_ary.append("cv0027=11\n") #   // low Länge des MLL Config[] Chunks\n")
    #config_ary.append("cv0028=00\n") #  // high\n")
    #config_ary.append("cv0029=8A\n") #  // HOUSE_T\n")
    #config_ary.append("cv0030=00\n") #  // low first LED (ESP32 Notation)\n")
    #config_ary.append("cv0031=00\n") #  // high ...      (ESP32 Notation)\n")
    #config_ary.append("cv0032=FF\n") #  // input channel (not used / allways enabled)\n")
    #config_ary.append("cv0033=02\n") #  // min rooms on\n")
    #config_ary.append("cv0034=05\n") #  // max rooms on\n")
    #config_ary.append("cv0035=05\n") #  // min time to change\n")
    #config_ary.append("cv0036=0F\n") #  // max time to change\n")
    #config_ary.append("cv0037=07\n") #  // sieben Räume sind konfiguriert\n")
    #config_ary.append("cv0038=00\n") #  // ROOM_DARK\n")
    #config_ary.append("cv0039=02\n") #  // ROOM_WARM_W\n")
    #config_ary.append("cv0040=23\n") #  // NEON_LIGHT\n")
    #config_ary.append("cv0041=27\n") #  // NEON_LIGHTD\n")
    #config_ary.append("cv0042=1D\n") #  // GAS_LIGHT2\n")
    #config_ary.append("cv0043=3E\n") #  // CANDLE\n")
    #config_ary.append("cv0044=03\n") #  // ROOM_RED\n")
    #config_ary.append("cv0045=00\n") #  // END_T Ende der Konfiguration\n")
    
    
    current_index = 27
    #process lines:
    try:
        macro_len = 0 # reserve space
        macro_len_index = current_index
        current_index = add_2Byte_Value_to_cv(current_index, macro_len, config_ary)        
        for line in input_cfg:
            if line != "":
                #linesplit1_ary = line.split("(")
                #macro = linesplit1_ary[0]
                #params_str = linesplit1_ary[1].split(")")[0]
                #param_list = params_str.split(",")
                
                #if macro.endswith("HouseT"):
                    #macro_len += (len(param_list) + 2)
                    #current_index = add_1Byte_Value_to_cv(current_index, 0x8A, config_ary)
                    #current_index = add_2Byte_Value_to_cv(current_index, param_list[0], config_ary) # first LED
                    #inch = get_inch_no(param_list[1])
                    #current_index = add_1Byte_Value_to_cv(current_index, inch, config_ary) # InCh
                    #for i in range (2, 6):
                        #current_index = add_1Byte_Value_to_cv(current_index, param_list[i], config_ary)
                    #current_index = add_1Byte_Value_to_cv(current_index, len(param_list)-6, config_ary)    
                    #for i in range (6, len(param_list)):
                        #room_no = HOUSE_PALETTE_List.index(param_list[i][1:])
                        #current_index = add_1Byte_Value_to_cv(current_index, room_no, config_ary) # Rooms
                current_index, this_macro_len = generate_config_line(current_index, line, config_ary)
                macro_len += this_macro_len
        current_index = add_1Byte_Value_to_cv(current_index, 0, config_ary) # End Config
        #set length of config part at start of config part
        current_index = add_2Byte_Value_to_cv(macro_len_index, macro_len, config_ary, append=False)
        current_index = add_2Byte_Value_to_cv(3, maxLEDcnt, config_ary, append=False)
        current_index = add_2Byte_Value_to_cv(11, maxLEDcnt, config_ary, append=False)
    
        # set config file length cv0001 and cv0002
        len_config = len(config_ary) + 2
        current_index = add_2Byte_Value_to_cv(1, len_config, config_ary, append=False)
        
        return config_ary
    
    except BaseException as e:
        #print(e)
        logging.debug(e, exc_info=True)        
        return []

def generate_config_file(ConfigTxt, LEDsInUse):
    filename =  M08.GetWorkbookPath() + '/' + M02.Ino_Dir_LED + "LEDs_CONFIG.txt"
    #print(ConfigTxt)
    input_cfg = ConfigTxt.split("\n")
    # Open the file in write mode ('w') and add some text
    maxLEDcnt = 0
    for i in range (0,len(LEDsInUse)):
        maxLEDcnt+=int(LEDsInUse[i]) 

    cv_ary = generate_cvs(ConfigTxt, LEDsInUse)
    
    config_ary = []
    config_ary.append("#start\n")
    config_ary.append("#RailMail-WS2811\n")
    config_ary.append("#Firmware-Version=2.0.9\n")
    config_ary.append("#Serial-Number=Pico1-000400000003\n")
    config_ary.append("#Ethernet-MAC-Adresse=28:CD:C1:04:A5:C5\n")
    config_ary.append("#IP-Adress=192.168.188.45\n")
    config_ary.append("#Section=MLL-Configuration\n")
    
    for i in range(0, len(cv_ary)):
        config_ary.append(f"cv{i + 1:04}={cv_ary[i]}\n")
        
    config_ary.append("#finish\n")
    
    with open(filename, 'w') as file:
        for i in range(0, len(config_ary)):
            file.write(config_ary[i])
    
    return filename


def generate_config_file2(ConfigTxt, LEDsInUse):
    filename =  M08.GetWorkbookPath() + '/' + M02.Ino_Dir_LED + "LEDs_CONFIG.txt"
    #print(ConfigTxt)
    input_cfg = ConfigTxt.split("\n")
    # Open the file in write mode ('w') and add some text
    maxLEDcnt = 0
    for i in range (0,len(LEDsInUse)):
        maxLEDcnt+=int(LEDsInUse[i]) 

    config_ary = []
    
    config_ary.append("#start\n")
    config_ary.append("#RailMail-WS2811\n")
    config_ary.append("#Firmware-Version=2.0.9\n")
    config_ary.append("#Serial-Number=Pico1-000400000003\n")
    config_ary.append("#Ethernet-MAC-Adresse=28:CD:C1:04:A5:C5\n")
    config_ary.append("#IP-Adress=192.168.188.45\n")
    config_ary.append("#Section=MLL-Configuration\n")
    config_ary.append("cv0001=2B\n") # // low Gesamtlänge (immer ohne die 16 Bit der Länge selber)\n")
    config_ary.append("cv0002=00\n") #  // high ...\n")
    
    # // Allgemeine Parameter, die nur EINMAL vorkommen\n")
    config_ary.append("cv0003=14\n") #  // low Anzahl LEDs (im Sinne der MobaLedLib.cpp NICHT FastLED)\n")
    config_ary.append("cv0004=00\n") #  // high ...\n")
    config_ary.append("cv0005=0F\n") #  // low RAM Bedarf in Bytes\n")
    config_ary.append("cv0006=00\n") #  // high ...\n")
    
    # Konfiguration der FastLED Controller
    # ein Controller besteht jeweils aus zwei 16Bit words
    config_ary.append("cv0007=04\n") #  // low Länge der Strukturinformationen für FastLED Controller\n")
    config_ary.append("cv0008=00\n") #  // high ...\n")
    config_ary.append("cv0009=00\n") #  // low FastLED Controller 0 Start-LED Nummer\n")
    config_ary.append("cv0010=00\n") #  // high ...\n")
    config_ary.append("cv0011=14\n") #  // low FastLED Controller 0 Number of LEDs\n")
    config_ary.append("cv0012=00\n") #  // high ...\n")
    
    #Ext_Addr für DCC Address Mappings
    #ein Mapping besteht jeweils aus zwei 16Bit words)
    config_ary.append("cv0013=04\n") #  // low Länge der Ext_Addr Strukturinformationen\n")
    config_ary.append("cv0014=00\n") #  // high ...\n")
    config_ary.append("cv0015=FF\n") #  // low DCC AddrAndTyp (0xFF is a default-dummy)\n")
    config_ary.append("cv0016=FF\n") #  // high ...           (0xFF is a default-dummy)\n")
    config_ary.append("cv0017=FF\n") #  // InCnt (low ffs)    (0xFF is 1 default-dummy)\n")
    config_ary.append("cv0018=00\n") #  // high ffs\n")
    
    #LED2Var für Eingangsvariablen
    #ein Mapping besteht jeweils aus zwei 16Bit words und zwei bytes, also
    #insgesamt 6 byte)
    config_ary.append("cv0019=06\n") #  // low Länge der LED2Var_tab Strukturinformationen\n")
    config_ary.append("cv0020=00\n") #  // high ...\n")
    config_ary.append("cv0021=FF\n") #  // Var_Nr (InCnt) (low ffs) (0xFF is a default-dummy)\n")
    config_ary.append("cv0022=FF\n") #  // high ffs                 (0xFF is a default-dummy)\n")
    config_ary.append("cv0023=FF\n") #  // LED_Nr (low ffs)         (0xFF is a default-dummy)\n")
    config_ary.append("cv0024=FF\n") #  // high ffs                 (0xFF is a default-dummy)\n")
    config_ary.append("cv0025=FF\n") #  // Offset_And_Typ           (0xFF is a default-dummy)\n")
    config_ary.append("cv0026=FF\n") #  // Value (to compare)       (0xFF is a default-dummy)\n")
    
    #config_ary.append("// ab hier kommt die eigentliche MLL Konfiguration\n")
    #config_ary.append("cv0027=11\n") #   // low Länge des MLL Config[] Chunks\n")
    #config_ary.append("cv0028=00\n") #  // high\n")
    #config_ary.append("cv0029=8A\n") #  // HOUSE_T\n")
    #config_ary.append("cv0030=00\n") #  // low first LED (ESP32 Notation)\n")
    #config_ary.append("cv0031=00\n") #  // high ...      (ESP32 Notation)\n")
    #config_ary.append("cv0032=FF\n") #  // input channel (not used / allways enabled)\n")
    #config_ary.append("cv0033=02\n") #  // min rooms on\n")
    #config_ary.append("cv0034=05\n") #  // max rooms on\n")
    #config_ary.append("cv0035=05\n") #  // min time to change\n")
    #config_ary.append("cv0036=0F\n") #  // max time to change\n")
    #config_ary.append("cv0037=07\n") #  // sieben Räume sind konfiguriert\n")
    #config_ary.append("cv0038=00\n") #  // ROOM_DARK\n")
    #config_ary.append("cv0039=02\n") #  // ROOM_WARM_W\n")
    #config_ary.append("cv0040=23\n") #  // NEON_LIGHT\n")
    #config_ary.append("cv0041=27\n") #  // NEON_LIGHTD\n")
    #config_ary.append("cv0042=1D\n") #  // GAS_LIGHT2\n")
    #config_ary.append("cv0043=3E\n") #  // CANDLE\n")
    #config_ary.append("cv0044=03\n") #  // ROOM_RED\n")
    #config_ary.append("cv0045=00\n") #  // END_T Ende der Konfiguration\n")
    
    
    current_index = 27
    #process lines:
    try:
        macro_len = 0 # reserve space
        macro_len_index = current_index
        current_index = add_2Byte_Value_to_config(current_index, macro_len, config_ary)        
        for line in input_cfg:
            if line != "":
                linesplit1_ary = line.split("(")
                macro = linesplit1_ary[0]
                params_str = linesplit1_ary[1].split(")")[0]
                param_list = params_str.split(",")
                
                if macro.endswith("HouseT"):
                    macro_len += (len(param_list) + 2)
                    current_index = add_1Byte_Value_to_config(current_index, 0x8A, config_ary)
                    current_index = add_2Byte_Value_to_config(current_index, param_list[0], config_ary) # first LED
                    inch = get_inch_no(param_list[1])
                    current_index = add_1Byte_Value_to_config(current_index, inch, config_ary) # InCh
                    for i in range (2, 6):
                        current_index = add_1Byte_Value_to_config(current_index, param_list[i], config_ary)
                    current_index = add_1Byte_Value_to_config(current_index, len(param_list)-6, config_ary)    
                    for i in range (6, len(param_list)):
                        room_no = HOUSE_PALETTE_List.index(param_list[i][1:])
                        current_index = add_1Byte_Value_to_config(current_index, room_no, config_ary) # Rooms
        current_index = add_1Byte_Value_to_config(current_index, 0, config_ary) # End Config
        #set length of config part at start of config part
        current_index = add_2Byte_Value_to_config(macro_len_index, macro_len, config_ary, append=False)
        current_index = add_2Byte_Value_to_config(3, maxLEDcnt, config_ary, append=False)
        current_index = add_2Byte_Value_to_config(11, maxLEDcnt, config_ary, append=False)
    except BaseException as e:
        #print(e)
        logging.debug(e, exc_info=True)   
    
    # set config file length cv0001 and cv0002
    len_config = len(config_ary) - 9
    current_index = add_2Byte_Value_to_config(1, len_config, config_ary, append=False)
    config_ary.append("#finish\n")
    
    with open(filename, 'w') as file:
        for i in range(0, len(config_ary)):
            file.write(config_ary[i])
    
    return filename

def generate_patch_file(input_cfg, CV_adress=0, CV_used=0):
    filename =  M08.GetWorkbookPath() + '/' + M02.Ino_Dir_LED + "LEDs_CONFIG.txt"
    #print(input_cfg)

    config_ary = []
    config_ary.append("#start\n")
    config_ary.append("#RailMail-WS2811\n")
    config_ary.append("#Firmware-Version=2.0.9\n")
    config_ary.append("#Serial-Number=Pico1-000400000003\n")
    config_ary.append("#Ethernet-MAC-Adresse=28:CD:C1:04:A5:C5\n")
    config_ary.append("#IP-Adress=192.168.188.45\n")
    config_ary.append("#Section=MLL-Configuration\n")    
    current_index = CV_adress
    last_CV = CV_adress + CV_used
    inputcfg_split = input_cfg.split("$")
    line = ""
    if len(inputcfg_split) == 3:
        line = inputcfg_split[1]
    elif len(inputcfg_split) == 2:
        line = inputcfg_split[0]
    else:
        line = ""

    if line != "":
        
        linesplit1_ary = line.split("(")
        macro = linesplit1_ary[0]
        params_str = linesplit1_ary[1].split(")")[0]
        param_list = params_str.split(",")
        macronotknown = False
        if macro.endswith("HouseT"):
            macro_len = (len(param_list) + 3)
            if macro_len > CV_used:
                max_params = CV_used - 3
            else:
                max_params = len(param_list)
            
            current_index = add_1Byte_Value_to_config(current_index, 0x8A, config_ary)
            #current_index = add_2Byte_Value_to_config(current_index, param_list[0], config_ary) # first LED
            #inch = get_inch_no(param_list[1])
            #current_index = add_1Byte_Value_to_config(current_index, inch, config_ary) # InCh
            current_index += 3 # do not chnage LED Nr and Inch
            for i in range (2, 6):
                current_index = add_1Byte_Value_to_config(current_index, param_list[i], config_ary)
            current_index = add_1Byte_Value_to_config(current_index, len(param_list)-6, config_ary)
            
            for i in range (6, max_params): #len(param_list)):
                room_no = HOUSE_PALETTE_List.index(param_list[i][1:])
                current_index = add_1Byte_Value_to_config(current_index, room_no, config_ary) # Rooms
        elif macro.endswith("Const"):
            current_index = add_1Byte_Value_to_config(current_index+5, param_list[3], config_ary)
            current_index = add_1Byte_Value_to_config(current_index, param_list[4], config_ary)
        else:
            macronotknown = True
                
        if macronotknown == False and current_index < last_CV:
            for i in range(current_index, last_CV):
                current_index = add_1Byte_Value_to_config(i, 0xFF, config_ary)

    config_ary.append("#finish\n")
    
    with open(filename, 'w') as file:
        for i in range(0, len(config_ary)):
            file.write(config_ary[i])
    
    return filename

import re

def remove_unnecessary_parentheses(expression):
    """Removes parentheses around single values while preserving expression structure."""
    return re.sub(r'\(\s*([0-9a-fxbo]+)\s*\)', r'\1', expression)  # Matches numbers/hex/binary

def convert_ternary(expression):
    """Convert simple ternary expressions manually."""
    while '?' in expression:  # Loop until all ternary expressions are processed
        parts = expression.split('?')  # Split at the first ternary operator
        condition = parts[0].strip('() ')  # Extract condition
        
        true_false_parts = parts[1].split(':', 1)  # Split at first colon
        if len(true_false_parts) != 2:
            break  # Safety check
        
        true_value = true_false_parts[0].strip('() ')
        false_value = true_false_parts[1].strip('() ')
        
        expression = f"({true_value} if {condition} else {false_value})"  # Build Python syntax

    return expression


def evaluate_parentheses(expression):
    """Recursively evaluate the innermost parentheses first."""
    while '(' in expression:  # Loop until no more parentheses
        deepest_expr = re.search(r'\([^()]+\)', expression)  # Find innermost parenthesis
        if not deepest_expr:
            break  # No more matches
        
        inner = deepest_expr.group()  # Extract expression inside parentheses
        processed_inner = convert_ternary(inner[1:-1])  # Remove outer parentheses and process
        processed_value = int(eval(processed_inner))
        processed_value_str = str(processed_value)
        
        expression = expression.replace(inner, processed_value_str)  # Replace in original
    
    return expression

def convert_ternary(expression):
    """Convert ternary expressions to Python-compatible format."""
    pattern = r'([^?]+)\s*\?\s*([^:]+)\s*:\s*([^)]+)'  # Detect ternary structure
    return re.sub(pattern, r'(\2 if \1 else \3)', expression)  # Replace ternary

def evaluate_expression(expression):
    try:
        processed_expr = evaluate_parentheses(expression)  # First, resolve parentheses
        final_expr = convert_ternary(processed_expr)  # Convert ternary operators
        return eval(final_expr)
    except BaseException as e:
        logging.debug("ERROR - expression evaluation:", e, "\n", expression)
        return "0"

RAMused = 0

def generate_config_table_part(tu_string, startstring, endstring, determine_RAMusage=False):
    global RAMused
    configtbl_start = startstring
    configtbl_end = endstring
    
    # Find the start and end positions
    start_idx = tu_string.find(configtbl_start)
    end_idx = tu_string.find(configtbl_end, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        configtbl_part = tu_string[start_idx + len(configtbl_start) : end_idx].strip()
    else:
        #print("No match found.")
        return []
    configtbl_part = configtbl_part.replace("\\\n", "")

    
    counter_teststring = "+1 + __COUNTER__ - __COUNTER__"
    #count__counter = configtbl_part.count("__COUNTER__")
    RAMused = configtbl_part.count(counter_teststring) + 13 # Number of __Counter__ / 2  + a Char-buffer [1][13]
    #if RAMused != count__counter / 2:
    #    print("RAMUsed:", RAMused, " __counter__:", count__counter)
    configtbl_part_cleaned = configtbl_part.replace(counter_teststring, "")
    
    #print("Modified text:", configtbl_part_cleaned, " RAM:", RAMused)
    
    cv_table_part = []
    
    table_lines = configtbl_part_cleaned.split("\n")
    current_index = 0
    current_index = add_2Byte_Value_to_cv(current_index, 0, cv_table_part) # length of table, will be replace later
    
    
    length = 0
    openbrackets = 0
    
    for line in table_lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        if line == "{":
            openbrackets += 1
            continue
        if line == "}":
            openbrackets -= 1
            if openbrackets == 0:
                break
            else:
                continue
        if line.startswith("{"):
            openbrackets += 1
            line[0] = " "
        if line.endswith("}"):
            openbrackets -= 1
            line = line[:-1]
        if line.endswith("};"):
            openbrackets -= 1
            line = line[:-2]
        if line != "":
            line = line.replace("(uint32_t)", "")
            line = line.replace("L", "")
            line = line.replace("u", "")
            line = line.replace("&&", " and ")
            line_parts = line.split(",")
            for value in line_parts:
                if value != "":
                    new_value = evaluate_expression(value)
                    current_index = add_1Byte_Value_to_cv(current_index, new_value, cv_table_part)
                    length += 1
        if openbrackets == 0:
            break
            
        current_index = add_2Byte_Value_to_cv(1, length, cv_table_part, append=False) # length of table
    
    return cv_table_part

start_values_table = {}

def generate_start_values_tbl(tu_string, startstring, endstring):
    global start_values_table
    
    start_values_table = {}
    configtbl_start = startstring
    configtbl_end = endstring
    
    # Find the start and end positions
    start_idx = tu_string.find(configtbl_start)
    end_idx = tu_string.find(configtbl_end, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        configtbl_part = tu_string[start_idx + len(configtbl_start) : end_idx].strip()
    else:
        #print("No match found.")
        configtbl_part = "255,255"
    configtbl_part = configtbl_part.replace("\\\n", "")
    table_lines = configtbl_part.split("\n")
    
    for line in table_lines:
        idx =  line.find("MobaLedLib.Set_Input(")
        if idx != -1:
            line_split = line.split("(")
            values = line_split[1][:-2]
            values_split = values.split(",")
            key = int(values_split[0].strip())
            value = int(values_split[1].strip())
            start_values_table[key] = value
    #print(repr(start_values_table))

    

def generate_config_table_part_Ext_Addr(tu_string, startstring, endstring):
    
    configtbl_start = startstring
    configtbl_end = endstring
    
    # Find the start and end positions
    start_idx = tu_string.find(configtbl_start)
    end_idx = tu_string.find(configtbl_end, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        configtbl_part = tu_string[start_idx + len(configtbl_start) : end_idx].strip()
    else:
        #print("No match found.")
        configtbl_part = "255,255"
    configtbl_part = configtbl_part.replace("\\\n", "")
    table_lines = configtbl_part.split("\n")
    current_index = 0
    cv_table_part = []
    current_index = add_2Byte_Value_to_cv(current_index, 0, cv_table_part) # length of table, will be replace later
    
    length = 0
    openbrackets = 0
    table_idx = 0
    total_incnt_idx = 0
    for line in table_lines:
        line = line.strip()
        if line == "{":
            openbrackets += 1
            continue
        if line == "}":
            openbrackets -= 1
            if openbrackets == 0:
                break
            else:
                continue
        if line.startswith("{"):
            openbrackets += 1
            line = line[1:]
        close_idx = line.find("}")
        if close_idx != -1:
            openbrackets -= 1
            line = line[:close_idx]
            if openbrackets == 0:
                break
        line = line.replace("(uint16_t)", "")
        line_parts = line.split(",")
        if len(line_parts) == 2:
            adress = evaluate_expression(line_parts[0])
            incnt =  int(line_parts[1])
            incnt_orig = incnt
            for i in range(0, incnt):
                start_value = start_values_table.get(i+total_incnt_idx, None)
                if start_value != None:
                    if start_value == 1:
                        incnt |= (1 << 15) | (1 << 14 - i)
            total_incnt_idx += incnt_orig
            current_index = add_2Byte_Value_to_cv(current_index, adress, cv_table_part)
            current_index = add_2Byte_Value_to_cv(current_index, incnt, cv_table_part)
            length += 4
            table_idx += 1
            
    current_index = add_2Byte_Value_to_cv(1, length, cv_table_part, append=False) # length of table
    
    return cv_table_part

def generate_config_table_part_LED2Var(tu_string, startstring, endstring):
    
    configtbl_start = startstring
    configtbl_end = endstring
    
    # Find the start and end positions
    start_idx = tu_string.find(configtbl_start)
    end_idx = tu_string.find(configtbl_end, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        configtbl_part = tu_string[start_idx + len(configtbl_start) : end_idx].strip()
    else:
        #print("No match found.")
        configtbl_part = "255,255,255,255" # dummy table
    configtbl_part = configtbl_part.replace("\\\n", "")
    table_lines = configtbl_part.split("\n")
    cv_table_part = []
    current_index = 0
    current_index = add_2Byte_Value_to_cv(current_index, 0, cv_table_part) # length of table, will be replace later
   
    length = 0
    openbrackets = 0
    
    for line in table_lines:
        line = line.strip()
        
        if line == "{":
            openbrackets += 1
            continue
        if line == "}":
            openbrackets -= 1
            if openbrackets == 0:
                break
            else:
                continue
        if line.startswith("{"):
            openbrackets += 1
            line = line[1:]
        close_idx = line.find("}")
        if close_idx != -1:
            openbrackets -= 1
            line = line[:close_idx]
            if openbrackets == 0:
                break
        line = line.replace("(uint16_t)", "")
        line_parts = line.split(",")
        if len(line_parts) == 4:
            adress = evaluate_expression(line_parts[0])
            current_index = add_2Byte_Value_to_cv(current_index, adress, cv_table_part) # adress
            current_index = add_2Byte_Value_to_cv(current_index, int(line_parts[1]), cv_table_part) # var_Nr
            offset_and_type =  evaluate_expression(line_parts[2])
            current_index = add_1Byte_Value_to_cv(current_index, offset_and_type, cv_table_part) # offset and type
            current_index = add_1Byte_Value_to_cv(current_index, int(line_parts[3]), cv_table_part) # value           
            length += 6
            
        current_index = add_2Byte_Value_to_cv(1, length, cv_table_part, append=False) # length of table
                    
    
    return cv_table_part

def generate_config_table_part_init(LEDsInUse):
    
    anzahl_controller = 1 # len(LEDsInUse)
    maxLEDcnt = 0
    
    for i in range (0,len(LEDsInUse)):
        val = int(LEDsInUse[i])
        if val != 0:
            maxLEDcnt+=val
            anzahl_controller = i + 1

    config_ary = []
    current_index = 0
    config_ary.append("00") #  // low Gesamtlänge (immer ohne die 16 Bit der Länge selber)\n")
    config_ary.append("00") #  // high ...\n")
    
    # // Allgemeine Parameter, die nur EINMAL vorkommen\n")
    #config_ary.append("00") #  // low Anzahl LEDs (im Sinne der MobaLedLib.cpp NICHT FastLED)\n")
    #config_ary.append("00") #  // high ...\n")
    current_index = add_2Byte_Value_to_cv(current_index, maxLEDcnt, config_ary)
    
    config_ary.append("00") #  // low RAM Bedarf in Bytes\n")
    config_ary.append("00") #  // high ...\n")
    
    #config_ary.append("// Konfiguration der FastLED Controller\n")
    #config_ary.append("// (ein Controller besteht jeweils aus zwei 16Bit words)\n")
    
    
    #config_ary.append("04") #  // low Länge der Strukturinformationen für FastLED Controller\n")
    #config_ary.append("00") #  // high ...\n")
    #config_ary.append("00") #  // low FastLED Controller 0 Start-LED Nummer\n")
    #config_ary.append("00") #  // high ...\n")
    #config_ary.append("14") #  // low FastLED Controller 0 Number of LEDs\n")
    #config_ary.append("00") #  // high ...\n")
    
    controllerInfo_Len = 4 * anzahl_controller
    current_index = add_2Byte_Value_to_cv(current_index, controllerInfo_Len, config_ary)
    #write controller info per controller
    current_ledNr = 0
    for i in range(0, anzahl_controller):
        anzahlLED = LEDsInUse[i]
        current_index = add_2Byte_Value_to_cv(current_index, current_ledNr, config_ary)
        current_index = add_2Byte_Value_to_cv(current_index, anzahlLED, config_ary)
        current_ledNr += anzahlLED
         
    return config_ary
    
    #except BaseException as e:
    #    print(e)
    #    return []

config_ary = []
config_structure_orig = {0: ""}

def generate_config_file_test(LEDsInUse):
    global config_ary, start_values_table
    try:
        LEDS_per_Channel_start = "#define LEDS_PER_CHANNEL"
        
        # Paths
        LEDs_AutoProg_Filename = M08.GetWorkbookPath() + '/' + M02.Ino_Dir_LED + M02.Include_FileName
        ConfigFileDir = M08.GetWorkbookPath() + '/' + "LEDs_AutoConfig/"
        ConfigFilename = ConfigFileDir + "LEDs_AutoConfig.txt"
        IncludeFileDir = ConfigFileDir + "include_dir"
        
        
        myH = IncludeHandler.CppIncludeStdOs(
                theUsrDirs=[IncludeFileDir,],
                theSysDirs=[IncludeFileDir,],
                )
        
        AMP.PageInstance.add_text_to_textwindow("\n*Analyse LEDs_AutoProg.h file*\n")
        AMP.PageInstance.update()
        
        myLex = PpLexer.PpLexer(LEDs_AutoProg_Filename, myH)
        tu_string = ""
        for tok in myLex.ppTokens(minWs=True):
            tu_string += tok.t
            #print(tok.t, end=' ')
            
        #print(tu_string)
        
        if LEDsInUse == None:
            LEDsInUse[0] = 20
            
        #if LEDsInUse == None or LEDsInUse[0] < 20:
        #    LEDsInUse[0] = 20
        
        configtbl_start = "const PROGMEM unsigned char Config[] ="
        configtbl_end = "void Set_Start_Values(MobaLedLib_C &MobaLedLib)"
        
        ## Find the start and end positions
        #start_idx = tu_string.find(configtbl_start)
        #end_idx = tu_string.find(configtbl_end, start_idx)
        
        #if start_idx != -1 and end_idx != -1:
            #configtbl_part = tu_string[start_idx + len(configtbl_start) : end_idx].strip()
        #else:
            #print("No match found.")
        #configtbl_part = configtbl_part.replace("\\\n")

        #counter_teststring = "+1 + __COUNTER__ - __COUNTER__"
        #RAMused = configtbl_part.count(counter_teststring)
        #configtbl_part_cleaned = configtbl_part.replace(counter_teststring, "")
        
        #print("Modified text:", configtbl_part_cleaned, " RAM:", RAMused)
        
        AMP.PageInstance.add_text_to_textwindow("\n*Generate Configuration*\n")
        AMP.PageInstance.update()
        
        generate_start_values_tbl(tu_string, "void Set_Start_Values(MobaLedLib_C &MobaLedLib)", "}")
        
        cv_part_ini = generate_config_table_part_init(LEDsInUse)
        
        cv_part_Ext_Addr = generate_config_table_part_Ext_Addr(tu_string, "const PROGMEM Ext_Addr_T Ext_Addr[] =", "const PROGMEM unsigned char Config[] =")
        
        cv_part_LED2VAR_Tab = generate_config_table_part_LED2Var(tu_string, "const PROGMEM LED2Var_Tab_T LED2Var_Tab[] =", "const PROGMEM unsigned char Config[] =")
        
        cv_part_Config = generate_config_table_part(tu_string, configtbl_start, configtbl_end)
                
        # put all parts together:
     
        config_ary = []
        config_ary.append("#start\n")
        config_ary.append("#RailMail-WS2811\n")
        config_ary.append("#Firmware-Version=2.0.9\n")
        config_ary.append("#Serial-Number=Pico1-000400000003\n")
        config_ary.append("#Ethernet-MAC-Adresse=28:CD:C1:04:A5:C5\n")
        config_ary.append("#IP-Adress=192.168.188.45\n")
        config_ary.append("#Section=MLL-Configuration\n")
        
        cv_nr = 1
    
        for i in range(0, len(cv_part_ini)):
            config_ary.append(f"cv{cv_nr:04}={cv_part_ini[i]}\n")
            cv_nr += 1
            
        for i in range(0, len(cv_part_Ext_Addr)):
            config_ary.append(f"cv{cv_nr:04}={cv_part_Ext_Addr[i]}\n")
            cv_nr += 1
            
        for i in range(0, len(cv_part_LED2VAR_Tab)):
            config_ary.append(f"cv{cv_nr:04}={cv_part_LED2VAR_Tab[i]}\n")
            cv_nr += 1
            
        for i in range(0, len(cv_part_Config)):
            config_ary.append(f"cv{cv_nr:04}={cv_part_Config[i]}\n")
            cv_nr += 1
            
        config_ary.append("#finish\n")
        
        # set config file length cv0001 and cv0002
        len_config = len(config_ary) - 10
        current_index = add_2Byte_Value_to_cv(1, len_config, cv_part_ini, append=False)
        current_index = add_2Byte_Value_to_cv(3, RAMused, cv_part_ini, append=False)
        
        config_ary[7] = f"cv0001={cv_part_ini[0]}\n"
        config_ary[8] = f"cv0002={cv_part_ini[1]}\n"
        
        config_ary[11] = f"cv0005={cv_part_ini[2]}\n"
        config_ary[12] = f"cv0006={cv_part_ini[3]}\n"         
    
        with open(ConfigFilename, 'w') as file:
            for i in range(0, len(config_ary)):
                file.write(config_ary[i])
    
        return ConfigFilename
        
    except BaseException as e:
        #print(e)
        logging.debug(e, exc_info=True)   

    return ConfigFilename


def upload_to_PICO(pico_ip, file_path):
    pico_ip = pico_ip[3:]
    url = f'http://{pico_ip}/'  # Replace with your Pico's IP
    files = {'file': open(file_path, 'rb')}
    try:
        AMP.PageInstance.add_text_to_textwindow("\n*Send Configuration File to PICO*\n")
        AMP.PageInstance.add_text_to_textwindow("\n*url: "+url+ "                *\n")
        AMP.PageInstance.add_text_to_textwindow("\n*File: "+file_path+ " *\n")
        AMP.PageInstance.add_text_to_textwindow("\n* Start upload *\n")
        AMP.PageInstance.update()
        uploadurl = url + "extensionbackup"
        response = requests.post(uploadurl, files=files, timeout=PG.IPUploadTimeout)
        if response.status_code == 200:
            #print("File uploaded successfully!")
            AMP.PageInstance.add_text_to_textwindow(f"\n* Upload sucessfull -  RAM used: {RAMused} *\n")
            AMP.PageInstance.add_text_to_textwindow("\n* Execute Activation*\n")
            AMP.PageInstance.update()
            time.sleep(2)
            activate_url = url + "extensionuse"
            response = requests.get(activate_url, timeout=5)
            if response.status_code == 200:
                AMP.PageInstance.add_text_to_textwindow("\n* Activation sucessfull *\n")
                fn_return_value = True
            else:
                AMP.PageInstance.add_text_to_textwindow(f"\n* Activation failed {response.status_code} - {response.text}*\n")
                fn_return_value = False
        else:
            #print(f"Failed to upload: {response.status_code} - {response.text}")
            AMP.PageInstance.add_text_to_textwindow(f"Failed to upload: {response.status_code} - {response.text}")
            fn_return_value = False
    except Exception as e:
        #print(f"Error: {e}")
        AMP.PageInstance.add_text_to_textwindow(f"ERROR: {e}")
        fn_return_value = False
    return fn_return_value
        
def download_from_Pico():
    pico_ip = P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL)
    
    if not pico_ip.startswith("IP:"):
        ipadress = PG.global_controller.getConfigData("serportname")
        if ipadress.startswith("IP:"):
            ipadress = ipadress[3:]
        ipadress = G00.InputBox("Enter IP-Adresse", "WLAN-PICO", Default=ipadress)
        ComPortColumn = M25.COMPort_COL
        if ipadress != "":
            pico_ip = "IP:" + ipadress
            P01.CellDict[M02.SH_VARS_ROW, ComPortColumn] = "IP:" + ipadress
            PG.global_controller.setConfigData("serportname", "IP:" + ipadress)
    if pico_ip.startswith("IP:"):
        try:
            F00.StatusMsg_UserForm.ShowDialog(M09.Get_Language_Str('Download Konfiguration'), M09.Get_Language_Str('Download Konfiguration'))
            pico_ip = pico_ip[3:]
            url = f'http://{pico_ip}/'  # Replace with your Pico's IP
            download_url = url + "extensionsave"
            response = requests.get(download_url, timeout=5)
            # Define the file path where you want to save it
            #print(repr(response.headers))
            header_disposition_str = response.headers["Content-Disposition"]
            #print (header_disposition_str)
            
            #print(response.content)
            ConfigFileDir = M08.GetWorkbookPath() + '/' + "LEDs_AutoConfig/"
            file_path = ConfigFileDir + "LEDs_AutoConfig.dl.txt"  
            
            # Save the response content to a file
            with open(file_path, "wb") as file:
                file.write(response.content)
                
            controller = PG.get_global_controller()
            
            picoconfig_lines = response.content.decode("utf-8").split("\r\n")
            picoconfig_lines.insert(0, "#Header:" + str(header_disposition_str) + "\r\n")
            
            lines = M06b.convert_picoconfig_to_pgf(picoconfig_lines)
            
            Name = "PicoConfig"
            ToActiveSheet = True
            
            result = M18a.__Read_PGF_from_String_V1and2(lines, Name, ToActiveSheet)
            P01.Unload(F00.StatusMsg_UserForm)
        except BaseException as e:
            logging.debug(e, exc_info=True)   
            #print(e)
            
def init_config_structure_orig():
    global config_structure_orig
    config_structure_orig = {0: ""}
     
def set_config_structure_orig(LEDnr, Macro_line_str, Excel_row):
    macro_line_split = Macro_line_str.split("(")
    if len(macro_line_split) > 1:
        macro_str = macro_line_split[0].replace(" ", "")
    else:
        macro_str = ""
    
    config_structure_orig[LEDnr] = [macro_str, Excel_row]
    #print("set_config_structure_orig:", LEDnr, Macro_line_str)
    
def is_ip_responsive(ip, port=80, timeout=1):
    if ip.startswith("IP:"):
        ip = ip[3:]
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False

def create_MLLconfig_and_upload_to_PICO(pico_ip, ConfigTxT, LEDsInUse, ComPortColumn=5):
    global config_ary
    
    fn_return_value = False
    Retry = True
    while Retry:
        Retry = False
    
        if not is_ip_responsive(pico_ip):
            Msg = M09.Get_Language_Str('Fehler: Es ist kein Gerät mit der IP Adresse #1# angeschlossen.')
            Msg = Replace(Msg, "#1#", str(pico_ip)) + vbCr + vbCr + M09.Get_Language_Str('Wollen sie es noch mal mit einem anderen Arduino oder einer anderen IP-Adresse versuchen?') + vbCr + vbCr + M09.Get_Language_Str('Mit \'Nein\' wird die Meldung ignoriert und versucht den Arduino trotzdem zu programmieren.')
            select_variable_ = P01.MsgBox(Msg, vbYesNoCancel + vbQuestion, M09.Get_Language_Str('Fehler bei der Überprüfung des angeschlossenen Arduinos'))
            if (select_variable_ == vbYes):
                Retry = True
                fn_return_value = M07New.USB_Port_Dialog(ComPortColumn)
                if not fn_return_value:
                    return fn_return_value
            elif (select_variable_ == vbCancel):
                return fn_return_value
            elif (select_variable_ == vbNo):
                pass
        
    AMP.PageInstance.add_text_to_textwindow("\n*****************************************************\n")
    AMP.PageInstance.add_text_to_textwindow("\n*Generate Configuration File*\n")
    AMP.PageInstance.update()
    
    file_path = generate_config_file_test(LEDsInUse)
    
    config_structure = M06b.convert_picoconfig_to_structure(config_ary)
    
    #print(repr(config_structure))
    #print(repr(config_structure_orig))
    
    for cfg_line in config_structure:
        orig_line_ary = config_structure_orig.get(int(cfg_line[0]), "")
        if cfg_line[1].startswith(orig_line_ary[0]):
            excel_row = orig_line_ary[1]
            CV_Adress = cfg_line[2]
            CV_used = cfg_line[3]
            InCh_ptr = cfg_line[4] 
            
            P01.CellDict[excel_row, M25.Config__Col+6] = CV_Adress 
            P01.CellDict[excel_row, M25.Config__Col+7] = CV_used
            P01.CellDict[excel_row, M25.Config__Col+8] = InCh_ptr
    
    #file_path = generate_config_file(ConfigTxT, LEDsInUse)
    fn_return_value = upload_to_PICO(pico_ip, file_path)
    return fn_return_value


# VB2PY (UntranslatedCode) Option Explicit
