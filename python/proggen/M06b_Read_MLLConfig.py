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
#import proggen.M07_COM_Port as M07
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

import ExcelAPI.XLA_Application as P01
from ExcelAPI.XLC_Excel_Consts import *
import ExcelAPI.XLWF_Worksheetfunction as XLWF

import tkinter as tk

import sys


picoConfig_ary = []
picoConfig_Descr_str = ""
Lines = vbObjectInitialize(objtype=String)



PM_NORMAL =              0              # Normal mode (Als Platzhalter in Excel)
PM_SEQUENZ_W_RESTART =   1              # Rising edge-triggered unique sequence. A new edge starts with state 0.
PM_SEQUENZ_W_ABORT =     2              # Rising edge-triggered unique sequence. Abort the sequence if new edge is detected during run time.
PM_SEQUENZ_NO_RESTART =  3              # Rising edge-triggered unique sequence. No restart if new edge is detected
PM_SEQUENZ_STOP =        4              # Rising edge-triggered unique sequence. A new edge starts with state 0. If input is turned off the sequence is stopped immediately.
PM_PINGPONG =            5              # Change the direction at the end: 118 bytes
PM_HSV =                 6              # Use HSV values instead of RGB for the channels
PM_RES =                 7              # Reserved mode
PM_MODE_MASK =           0x07           # Defines the number of bits used for the modes (currently 3 => Modes 0..7)

PM_SEQUENCE_W_RESTART =  1              # To be able to use the correct spelling also    07.10.21:
PM_SEQUENCE_W_ABORT =    2
PM_SEQUENCE_NO_RESTART = 3
PM_SEQUENCE_STOP =       4

# Flags for the Pattern function
_PF_XFADE =              0x08           # Special fade mode which starts from the actual brightness value instead of the value of the previous state
PF_NO_SWITCH_OFF =       0x10           # Don't switch of the LEDs if the input is turned off. Useful if several effects use the same LEDs alternated by the input switch.
PF_EASEINOUT =           0x20           # Easing function (Uebergangsfunktion) is used because changes near 0 and 255 are noticed different than in the middle
PF_SLOW =                0x40           # Slow timer (divided by 16) to be able to use longer durations
PF_INVERT_INP =          0x80           # Invert the input switch => Effect is active if the input is 0

# Flags and modes for the Random() and RandMux() function
RM_NORMAL =              0b00000000
RF_SLOW =                0b00000001      # Time base is divided by 16 This Flag is set automatically if the time is > 65535 ms
RF_SEQ =                 0b00000010      # Switch the outputs of the RandMux() function sequential and not random
RF_STAY_ON =             0b00000100      # Flag for the Ranom() function. The Output stays on until the input is turned off. MinOn, MaxOn define how long it stays on.
#                                                # 12.01.20:  For some reasons RF_STAY_ON was equal RF_SEQ
RF_NOT_SAME =            0b00001000      # Prevent, that the same output is used two times in sequence                                           # 13.01.20:

# Flags for the Counter() function
CM_NORMAL =              0              # Normal Counter mode
CF_INV_INPUT =           0b00000001      # Invert Input
CF_INV_ENABLE =          0b00000010      # Input Enable
CF_BINARY =              0b00000100      # Maximal 8 outputs
CF_RESET_LONG =          0b00001000      # Taste Lang = Reset
CF_UP_DOWN =             0b00010000      # Ein RS-FlipFlop kann mit CM_UP_DOWN ohne CF_ROTATE gemacht werden
CF_ROTATE =              0b00100000      # Faengt am Ende wieder von vorne an
CF_PINGPONG =            0b01000000      # Wechselt am Ende die Richtung
CF_SKIP0 =               0b10000000      # Ueberspringt die 0. Die 0 kommt nur bei einem Timeout oder wenn die Taste lange gerueckt wird
CF_RANDOM =             (0b00000001<<8)  # Generate random numbers                                                                               # 07.11.18:
CF_LOCAL_VAR =          (0b00000010<<8)  # Write the result to a local variable which must be created with New_Local_Var() prior
_CF_NO_LEDOUTP =         (0b00000100<<8)  # Disable the LED output (the first DestVar contains the maximal counts-1 (counter => 0 .. n-1) )
CF_ONLY_LOCALVAR =      (CF_LOCAL_VAR|_CF_NO_LEDOUTP)  # Don't write to the LEDs defined with DestVar. The first DestVar contains the number maximal number of the counter-1 (counter => 0 .. n-1).


_CM_RS_FlipFlop1 =       (CF_BINARY|CF_UP_DOWN)               # RS Flip Flop with one output (Edge triggered)
_CM_T_FlipFlop1  =       (CF_BINARY|CF_INV_ENABLE|CF_ROTATE)  # T Flip Flop  with one output
_CM_RS_FlipFlop2 =       (CF_UP_DOWN)                         # RS Flip Flop with two outputs (Edge triggered)
_CM_T_FlipFlopEnable2 =  (CF_ROTATE)                          # T Flip Flop  with two outputs and enable
_CM_T_FlipFlopReset2 =   (CF_ROTATE | CF_INV_ENABLE)          # T Flip Flop  with two outputs and reset

_CF_ROT_SKIP0 =          (CF_ROTATE   | CF_SKIP0)             # Rotate and Skip 0
_CF_P_P_SKIP0 =          (CF_PINGPONG | CF_SKIP0)


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

END_T=                    0
CONST_T=                  1 #// Die ersten Ausgangstypen haben als Parameter eine channel mask mit
RANDMUX_T=                2 #// der ausgewaehlt wird welche LEDs angestuert werden
SCHEDULE_T=               3 #// Bei diesen Typen steht InCh an Position 2

PATTERNT1_T=           10 #// Muster mit einer Zeit fuer alle Zustaende
PATTERNT2_T=           11 #// Muster mit zwei abwechselnd genutzten Zeiten
PATTERNT3_T=           12 #//   "        drei     "
PATTERNT4_T=           13
PATTERNT5_T=           14
PATTERNT6_T=           15
PATTERNT7_T=           16
PATTERNT8_T=           17
PATTERNT9_T=           18
PATTERNT10_T=          19
PATTERNT11_T=          20
PATTERNT12_T=          21
PATTERNT13_T=          22
PATTERNT14_T=          23
PATTERNT15_T=          24
PATTERNT16_T=          25
PATTERNT17_T=          26
PATTERNT18_T=          27
PATTERNT19_T=          28
PATTERNT20_T=          29
PATTERNT21_T=          30
PATTERNT22_T=          31
PATTERNT23_T=          32
PATTERNT24_T=          33
PATTERNT25_T=          34
PATTERNT26_T=          35
PATTERNT27_T=          36
PATTERNT28_T=          37
PATTERNT29_T=          38
PATTERNT30_T=          39
PATTERNT31_T=          40
PATTERNT32_T=          41
PATTERNT33_T=          42
PATTERNT34_T=          43
PATTERNT35_T=          44
PATTERNT36_T=          45
PATTERNT37_T=          46
PATTERNT38_T=          47
PATTERNT39_T=          48
PATTERNT40_T=          49
PATTERNT41_T=          50
PATTERNT42_T=          51
PATTERNT43_T=          52
PATTERNT44_T=          53
PATTERNT45_T=          54
PATTERNT46_T=          55
PATTERNT47_T=          56
PATTERNT48_T=          57
PATTERNT49_T=          58
PATTERNT50_T=          59
PATTERNT51_T=          60
PATTERNT52_T=          61
PATTERNT53_T=          62
PATTERNT54_T=          63
PATTERNT55_T=          64
PATTERNT56_T=          65
PATTERNT57_T=          66
PATTERNT58_T=          67
PATTERNT59_T=          68
PATTERNT60_T=          69
PATTERNT61_T=          70
PATTERNT62_T=          71
PATTERNT63_T=          72
PATTERNT64_T=          73
LAST_PATTERN_T=    PATTERNT64_T

APATTERNT1_T=          74 #// Muster mit einer Zeit fuer alle Zustaende mit analogen Uebergaengen
APATTERNT2_T=          75 #// Muster mit zwei abwechselnd genutzten Zeiten
APATTERNT3_T=          76 #//   "        drei    "
APATTERNT4_T=          77
APATTERNT5_T=          78
APATTERNT6_T=          79
APATTERNT7_T=          80
APATTERNT8_T=          81
APATTERNT9_T=          82
APATTERNT10_T=         83
APATTERNT11_T=         84
APATTERNT12_T=         85
APATTERNT13_T=         86
APATTERNT14_T=         87
APATTERNT15_T=         88
APATTERNT16_T=         89
APATTERNT17_T=         90
APATTERNT18_T=         91
APATTERNT19_T=         92
APATTERNT20_T=         93
APATTERNT21_T=         94
APATTERNT22_T=         95
APATTERNT23_T=         96
APATTERNT24_T=         97
APATTERNT25_T=         98
APATTERNT26_T=         99
APATTERNT27_T=         100
APATTERNT28_T=         101
APATTERNT29_T=         102
APATTERNT30_T=         103
APATTERNT31_T=         104
APATTERNT32_T=         105
APATTERNT33_T=         106
APATTERNT34_T=         107
APATTERNT35_T=         108
APATTERNT36_T=         109
APATTERNT37_T=         110
APATTERNT38_T=         111
APATTERNT39_T=         112
APATTERNT40_T=         113
APATTERNT41_T=         114
APATTERNT42_T=         115
APATTERNT43_T=         116
APATTERNT44_T=         117
APATTERNT45_T=         118
APATTERNT46_T=         119
APATTERNT47_T=         120
APATTERNT48_T=         121
APATTERNT49_T=         122
APATTERNT50_T=         123
APATTERNT51_T=         124
APATTERNT52_T=         125
APATTERNT53_T=         126
APATTERNT54_T=         127
APATTERNT55_T=         128
APATTERNT56_T=         129
APATTERNT57_T=         130
APATTERNT58_T=         131
APATTERNT59_T=         132
APATTERNT60_T=         133
APATTERNT61_T=         134
APATTERNT62_T=         135
APATTERNT63_T=         136
APATTERNT64_T=         137

LAST_APATTERN_T= APATTERNT64_T

HOUSE_T=                 138 #// Erster Ausgangstyp ohne ChMsk (WITHOUT_CHANNEL_MASK). Hier steht InCh an Position 1. Bei den Typen davor steht InCh an Position 2.
FIRE_T=                  139
RANDOM_T=                140
WELDING_CONT_T=          141
WELDING_T=               142
COPYLED_T=               143
COUNTER_T=               144

NEW_HSV_GROUP_T=         170  #// Erster Ausgangstyp ohne InpCh (WITHOUT_INP_CH)
NEW_LOCAL_VAR_T=         171  #                                                                         // 07.11.18:
USE_GLOBALVAR_T=         172

#if _USE_INCH_T=RIGGER                                                                                         // 02.06.20: New trigger method from Juergen
INCH_TO_X_VAR_T=       173 #                                                                          // 25.11.18:
BIN_INCH_TO_T=MPVAR_T=  174 #                                                                           // 18.01.19:
#else
INCH_TO_TMPVAR_T=      173 #                                                                          // 25.11.18:
INCH_TO_TMPVAR1_T=     174 #                                                                          // 07.05.20:
BIN_INCH_TO_TMPVAR_T=  175 #                                                                          // 18.01.19:
BIN_INCH_TO_TMPVAR1_T= 176 #                                                                          // 07.05.20:
#endif

#ifdef _NEW_ROOM_COL
SET_COLTAB_T=           180
#endif
#if _USE_SET_T=VTAB                                                                                            // 10.01.20:
SET_TV_TAB_T=           181
#endif

#if _USE_DEF_NEON                                                                                             // 12.01.20:
SET_DEF_NEON_T=         182
#endif

#if _USE_CANDLE
SET_CANDLETAB_T=        183 #                                                                          // 10.06.20:
#endif

LOGIC_T=                 184

EXT_PROC_BASE_T=         240    #// Makro extensions may use type ids >=l EXT_PROC_BASE_T= up to 255     // 21.10.21: Juergen
JUMPR_T = 220
NOOP_T = 255

#// Only used in the Charliplexing modul
CPX_LED_ASSIGNEMENT =    200    #// Define the LED assignement
CPX_ANALOG_INPUT =        201   # // Enable the analog input
CPX_ANALOG_LIMMITS =      202  #  // Table with analog limits which defines the Goto Nr levels

WITHOUT_CHANNEL_MASK = HOUSE_T
WITHOUT_INP_CH =       NEW_HSV_GROUP_T

SI_Enable_Sound =   253  #// Wird auf 1 initialisiert, kann aber vom der Konfigurarion veraendert werden
SI_0 =              254  #// Immer 0
SI_1 =              255  #// Immer 1
SI_LocalVar = SI_0 #// Input fuer Pattern Funktion zum einlesen der Localen Variable. Diese Nummer wird verwendet weil eine Konstante 0 als Eingang keinen Sinn macht


#// - LedCnt (1..3), StCh (0..2)
def _Cx(LedCnt, StCh):
    return (LedCnt + (StCh<<2))

C1 =        _Cx(1,      0)
C2 =         _Cx(1,      1)
C3 =         _Cx(1,      2)
C12 =        _Cx(2,      0)
C23 =        _Cx(2,      1)
C_ALL =      _Cx(3,      0)
C_RED =      C1
C_GREEN =    C2
C_BLUE =     C3
C_WHITE =    C_ALL
C_YELLOW =   C12
C_CYAN =     C23

Cx2str = {
   C1: "C1",
   C2: "C2",
   C3: "C3",
   C12: "C12",
   C23: "C23",
   C_ALL: "C_ALL"
}

#define _Cx2LedCnt(Cx) ((Cx)&0x03)
#define _Cx2StCh(Cx)   (((Cx)>>2)&0x03)


P_INPCHANEL_NO_CM = 1  #// If the funktion has no channel mask
P_INPCHANEL_W_CM =  2  # // If the function has a channel mask
ADD_WORD_OFFSET = 1

P_LEDNR = 0
P_CHANELMSK = (1+ADD_WORD_OFFSET)
P_INPCHANEL = (P_INPCHANEL_W_CM+ADD_WORD_OFFSET)  #// 2

P_CONST_VAL0 = (3+ADD_WORD_OFFSET) # Const
P_CONST_VAL1 = (4+ADD_WORD_OFFSET) #  "

P_DFLASH_PAUSE = (3+ADD_WORD_OFFSET)
P_DFLASH_TON = (4+ADD_WORD_OFFSET)
P_DFLASH_TOFF = (5+ADD_WORD_OFFSET)
P_DFLASH_VAL0= (6+ADD_WORD_OFFSET)
P_DFLASH_VAL1= (7+ADD_WORD_OFFSET)
P_DFLASH_OFF=  (8+ADD_WORD_OFFSET)


P_HOUSE_LED=0
P_HOUSE_INCH=  (P_INPCHANEL_NO_CM+ADD_WORD_OFFSET)   # 1
P_HOUSE_ON_MIN=(2+ADD_WORD_OFFSET)
P_HOUSE_ON_MAX=(3+ADD_WORD_OFFSET)
P_HOUSE_MIN_T= (4+ADD_WORD_OFFSET)
P_HOUSE_MAX_T= (5+ADD_WORD_OFFSET)
P_HOUSE_CNT=(6+ADD_WORD_OFFSET)
P_HOUSE_ROOM_0=(7+ADD_WORD_OFFSET)

P_FIRE_LED0=0
P_FIRE_INCH=(P_INPCHANEL_NO_CM+ADD_WORD_OFFSET)  # 1
P_FIRE_LEDCNT= (2+ADD_WORD_OFFSET)
P_FIRE_BRIGHT= (3+ADD_WORD_OFFSET)

P_BUTTON_LED=  0
P_BUTTON_CHMSK=(1+ADD_WORD_OFFSET)
P_BUTTON_INCH= (P_INPCHANEL_W_CM+ADD_WORD_OFFSET) # 2
P_BUTTON_DURLO=(3+ADD_WORD_OFFSET)
P_BUTTON_DURHI=(4+ADD_WORD_OFFSET)
P_BUTTON_VAL0= (5+ADD_WORD_OFFSET)
P_BUTTON_VAL1= (6+ADD_WORD_OFFSET)

P_PATERN_LED=  0
P_PATERN_NSTRU=(1+ADD_WORD_OFFSET)
P_PATERN_INCH= (P_INPCHANEL_W_CM+ADD_WORD_OFFSET) # 2
P_PATERN_ENABLE=  (3+ADD_WORD_OFFSET)
P_PATERN_LEDS= (4+ADD_WORD_OFFSET)  #  -+
P_PATERN_VAL0= (5+ADD_WORD_OFFSET)  #=+  Attention: LEDs, Val0, Val1, Off are read at once.
P_PATERN_VAL1= (6+ADD_WORD_OFFSET)  #=+  => Don't change the sequence of the parameters
P_PATERN_OFF=  (7+ADD_WORD_OFFSET)  #  -+
P_PATERN_MODE= (8+ADD_WORD_OFFSET)
P_PATERN_T1_L= (9+ADD_WORD_OFFSET)
P_PATERN_T1_H= (10+ADD_WORD_OFFSET)

 #Random(= DestVar, Inp, MinTime, MaxTime, MinOn, MaxOn) RANDOM_T,  DestVar, Inp, _T2B(MinTime), _T2B(MaxTime), _T2B(MinOn), _T2B(MaxOn),
 #RandMux(=DestVar1, DestVarN, Inp, MinTime, MaxTime)= RANDMUX_T, DestVar1, DestVarN, Inp, _T2B(MinTime), _T2B(MaxTime),

P_RANDOM_DSTVAR=  0
P_RANDOM_INP=  P_INPCHANEL_NO_CM   # 1
P_RANDOM_MODE= 2
P_RANDOM_MINTIME_L=  3
P_RANDOM_MINTIME_H=  4
P_RANDOM_MAXTIME_L=  5  # must be direct after P_RANDOM_MINTIME_H
P_RANDOM_MAXTIME_H=  6
P_RANDOM_MINON_L= 7
P_RANDOM_MINON_H= 8
P_RANDOM_MAXON_L= 9  # must be direct after P_RANDOM_MINON_H
P_RANDOM_MAXON_H= 10
EP_RANDOM_INCREMENT= 11 # Insert additional parameters before

P_RANDMUX_DSTVAR1=0
P_RANDMUX_DSTVARN=1
P_RANDMUX_INP= (P_INPCHANEL_W_CM) # 2
P_RANDMUX_MODE=(3)
P_RANDMUX_MINTIME_L= (4)
P_RANDMUX_MINTIME_H= (5)
P_RANDMUX_MAXTIME_L= (6)  # must be direct after P_RANDMUX_MINTIME_H
P_RANDMUX_MAXTIME_H= (7)
EP_RANDMUX_INCREMENT=(8)  # Insert additional parameters before

P_WELDING_LED= 0
P_WELDING_INP= (1+ADD_WORD_OFFSET)
EP_WELDING_INCREMENT=(2+ADD_WORD_OFFSET)  # Insert additional parameters before

P_COPYLED_CNT=  0
P_COPYLED_LED=  1
P_COPYLED_INP=  (2+ADD_WORD_OFFSET)
P_COPYLED_SRCLED=  (3+ADD_WORD_OFFSET)
EP_COPYLED_INCREMENT = (4+ADD_WORD_OFFSET*2)

P_SCHEDULE_DSTVAR1 =     0
P_SCHEDULE_DSTVARN =     1
P_SCHEDULE_INCH =        2
P_SCHEDULE_START =       3
P_SCHEDULE_END =         4
EP_SCHEDULE_INCREMENT =  5    #// Insert additional parameters before

P_COUNT_MODE_L=         0
P_COUNT_MODE_H =         1
P_COUNT_INP =            2
P_COUNT_ENABLE =         3
P_COUNT_TIMEOUT_L =      4
P_COUNT_TIMEOUT_H =      5
P_COUNT_DEST_COUNT =     6
P_COUNT_FIRST_DEST =     7

# // Callback types for Callback_t                                                                              // 01.05.20:
CT_CHANNEL_CHANGED = 0
CT_COUNTER_CHANGED = 1
CT_COUNTER_INITIAL = 2

PT_INACTIVE = 255

ROOM_COL_CNT =   17   # // Number of user defined colors for the room lights (Attention: If changed the program has to be adapted at several positions)  06.09.19:  Old 15

S_ONOFF = 0
B_RED = 1<<14
B_GREEN = 2<<14
O_RET_MSG = 3<<14    # Return messages (Rueckmelder)
B_TAST = B_RED

class MobaLedLib_C:
    
    def __init__(self):
        self.Trigger20fps = 0
        self.leds = 0
        self.Num_Leds = 0
    
    
        self.cp = 0 #          // Pointer to the Config[]            //  2 Byte

    #//--------------------------------------------
    def Is_Pattern(self, Type):
    #//--------------------------------------------
    #// return  0             if it's no pattern
    #//         PATTERNT1_T   if it's a digital pattern
    #//        APATTERNT1_T   for analog pattern or XPatternT
    #{
        if (Type >= PATTERNT1_T and Type <= LAST_PATTERN_T):  return PATTERNT1_T
        elif (Type >= APATTERNT1_T and Type <= LAST_APATTERN_T): return APATTERNT1_T
        return 0;

    def Inc_cp(self, Type):
        pass

    def IncCP_House(self):
        self.cp += P_HOUSE_ROOM_0 + pgm_read_byte_near(self.cp+P_HOUSE_CNT);
    
    def IncCP_Const(self):
        self.cp += (5 + ADD_WORD_OFFSET)
        
    def IncCP_Fire(self):
        self.cp += 4 + ADD_WORD_OFFSET
    
    def IncCP_Set_ColTab(self): self.cp += ROOM_COL_CNT*3
            #bool             Cmp_Room_Col(CRGB *lp, uint8_t ColorNr);
            #uint8_t          Get_Room_Col1(uint8_t ColorNr, uint8_t Channel);
            #void             Copy_Room_Col(CRGB *Dst, uint8_t ColorNr);
            #void             Copy_Single_Room_Col(CRGB *Dst, uint8_t Channel, uint8_t ColorNr);                        // 06.09.19:

    def IncCP_Set_CandleTab(self):
        self.cp += 9 # sizeof(Candle_Dat_T)

    def IncCP_Set_TV_Tab(self):
        self.cp += 12
        
    def IncCP_Set_Def_Neon(self):
        self.cp += 4
        
    def IncCP_Pattern(self, TimeCnt):
        BitMaskCnt = pgm_read_word_near(self.cp+P_PATERN_T1_L + 2*TimeCnt)
        self.cp += P_PATERN_T1_L + 2*TimeCnt + BitMaskCnt + 2;
        if self.cp > len(picoConfig_ary) - 1:
            self.cp = len(picoConfig_ary) - 1
    
    def IncCP_Logic(self):
        self.cp += pgm_read_byte_near(self.cp+1) + 2;
    
    def IncCP_New_HSV_Group(self): pass
    def IncCP_New_Local_Var(self): pass
    
    def IncCP_Use_GlobalVar(self):
        self.cp+= 1
        
    def IncCP_InCh_to_X_Var(self):
        self.cp+=2
        
    def IncCP_Random(self):
        self.cp += EP_RANDOM_INCREMENT
        
    def IncCP_RandMux(self):
        self.cp += EP_RANDMUX_INCREMENT
        
    def IncCP_Welding(self):
        self.cp += EP_WELDING_INCREMENT
        
    def IncCP_CopyLED(self):
        self.cp += EP_COPYLED_INCREMENT
        
    def IncCP_Schedule(self):
        self.cp += EP_SCHEDULE_INCREMENT
        
    def IncCP_Counter(self):
        self.cp += P_COUNT_FIRST_DEST + pgm_read_byte_near(self.cp+P_COUNT_DEST_COUNT);
        
    def IncCP_Jump(self):
        self.cp += pgm_read_word_near(self.cp+1)
        
    def IncCP_Noop(self):
        pass 


pMobaLedLib = MobaLedLib_C()
current_cp = 0
next_cp = 0
expected_next_led_nr = 0
config_strcuture_ary = []
max_InCh = 0

def pgm_read_byte_near(pointer):
    return picoConfig_ary[pointer]

def pgm_read_word_near(pointer):
    return picoConfig_ary[pointer] + picoConfig_ary[pointer+1] *256 

def pgm_read_led_nr(pointer):
    try:
        return picoConfig_ary[pointer] + picoConfig_ary[pointer+1] *256
    except BaseException as e:
        logging.debug(e, exc_info=True)

def pgm_read_dword_near(pointer):
    return picoConfig_ary[pointer] + picoConfig_ary[pointer+1] *256 + picoConfig_ary[pointer+2] *256 *256 + picoConfig_ary[pointer+3] *256 *256 * 256 

def DPRINTF_MLL_P(text, writemacro=False):
    global picoConfig_Descr_str
    text = "Line:" + vbTab + vbTab + vbTab + vbTab + vbTab + vbTab + vbTab + vbTab + vbTab + "//" + text + "\n"
    logging.debug(text)
    if writemacro:
        picoConfig_Descr_str += text
    
def WriteMacroLine(macro, LedNr, InCh, Type, num_used_Led_str=None, ChanMsk=None, Act=True, num_used_led=None, CV_Adress=None, CV_used=None):
    global picoConfig_Descr_str, expected_next_led_nr, config_strcuture_ary, max_InCh
    if ChanMsk != None:
        _Cx2LedCnt = ((ChanMsk)&0x03)
        _Cx2StCh = (((ChanMsk)>>2)&0x03)
        startLed = _Cx2StCh + 1
        num_used_Led_str = "C{}-{}".format(startLed, _Cx2StCh+_Cx2LedCnt)
        num_used_led = 1
    
    if num_used_Led_str==None:
        #num_used_led = 0 #determine_num_of_LEDs(LedNr, Type)
        num_used_Led_str = "" #{}".format(num_used_led)
    
    InChCnt_str = "0"
    InChType = ""
    if InCh == 255:
        InCh_str = ""
    elif InCh ==  SI_LocalVar:
        InCh_str = "SI_LocalVar"
    elif InCh < len(ext_addr_list):
        ext_addr_value = ext_addr_list[InCh]
        ext_addr = ext_addr_value[0] & 0x3FFF
        InChCnt = ext_addr_value[1]
        InCh_str = "{}".format(ext_addr)
        InChCnt_str = "{}".format(InChCnt)
        InChType_val = ext_addr_value[0] & 0xC000
        if InChType_val == S_ONOFF:
            InChType = "AnAus"
        elif InChType_val == B_RED:
            InChType = "Rot"
        elif InChType_val == B_GREEN:
            InChType = "Grün"
        else:
            InChType = "AnAus"
    else:
        InCh_str = "_V" + str(InCh)
        if InCh > max_InCh:
            max_InCh = InCh
    if Act:
        act_str = "Act"
    else:
        act_str = ""
        
    if CV_Adress != None:
        CV_adress_str = str(CV_Adress)
    else:
        CV_adress_str = ""
    if CV_used != None:
        CV_used_str = str(CV_used)
    else:
        CV_used_str = ""    
    if num_used_led != None and expected_next_led_nr != LedNr:
        # add (next_LED_Macro)
        deltaLED = LedNr - expected_next_led_nr
        nextmacro = "// Next_LED({})".format(deltaLED) 
        text = "Line:" + vbTab + act_str + vbTab + vbTab+ vbTab + vbTab + vbTab + vbTab + vbTab + vbTab + nextmacro + vbTab + str(expected_next_led_nr) + vbTab + str(deltaLED) + vbTab + InChCnt_str + vbTab + "0"+ vbTab + "0\n"
        logging.debug(text)
        picoConfig_Descr_str += text
        
    text = "Line:" + vbTab + act_str + vbTab + vbTab+ InCh_str + vbTab + InChType + vbTab + vbTab + vbTab + vbTab + vbTab + macro + vbTab + str(LedNr) + vbTab + num_used_Led_str + vbTab + InChCnt_str + vbTab + "0"+ vbTab + "0"+ vbTab + CV_adress_str + vbTab + CV_used_str + vbTab + str(InCh) +"\n"
    
    logging.debug(text)
    picoConfig_Descr_str += text
    config_strcuture_ary.append([str(LedNr), macro, CV_adress_str, CV_used_str, InCh])
    if not macro.startswith("//"):
        # check Led2Var
        led2var_entry = led2var_list.get(LedNr, None)
        if led2var_entry != None:
            varnr = led2var_entry[0]
            varnr_str = "_V" + str(varnr)
            offset = led2var_entry[1]
            type_str = led2var_entry[2]
            value = led2var_entry[3]
            macro = "LED_to_Var({}, {},{}, {})".format(varnr_str, offset, type_str, value)
            text = "Line:" + vbTab + act_str + vbTab + vbTab+ vbTab + vbTab + vbTab + vbTab + vbTab + vbTab + macro + vbTab + vbTab + vbTab + "0" + vbTab + "0"+ vbTab + "0"+ "\n"
            picoConfig_Descr_str += text
            config_strcuture_ary.append([str(LedNr), macro, CV_adress_str, CV_used_str, InCh])
        led2var_list[LedNr] = None
        
    if num_used_led != None:
        expected_next_led_nr = LedNr + num_used_led
    
def writeMacroLine2(macroName, LedNr = 0, InCh=255, Type=None, InCh_Pos=None, Var_Pos = None, donotwritemacro=False):
    global picoConfig_Descr_str, next_cp, current_cp
    #current CP points to Type - if InCh_Pos == 0 then InCh is the byte behind the Type-byte
    next_cp = pMobaLedLib.cp
    remaining_bytes_str = generate_remaining_bytes(current_cp, next_cp, 0, hex=True)
    tmp_macro = "//Type:{}".format(Type) + remaining_bytes_str 
    WriteMacroLine(tmp_macro, 0, 255, Type=Type, Act=False) # write Hex-Values found
    if donotwritemacro:
        return
    if InCh_Pos != None:
        InCh = pgm_read_byte_near(current_cp+1+InCh_Pos)
        remaining_bytes_str = generate_remaining_bytes(current_cp, current_cp+1+InCh_Pos, 0, hex=False, Var_Pos=Var_Pos) + ",#InCh" + generate_remaining_bytes(current_cp, next_cp, InCh_Pos+1, hex=False, Var_Pos=Var_Pos)
    else:
        remaining_bytes_str = generate_remaining_bytes(current_cp, next_cp, 0, hex=False, Var_Pos=Var_Pos)
    macro = macroName + remaining_bytes_str
    WriteMacroLine(macro, LedNr, InCh, Type)
    
def PSTR(text):
    return text

def generate_remaining_bytes(current_macro_cp, next_macro_cp, last_cp_used, hex=True, Var_Pos=None):
    try:
        byte_str = ""
        for i in range(current_macro_cp+last_cp_used+1, next_macro_cp):
            readbyte = pgm_read_byte_near(i)
            if hex:
                byte_str += ",0x{:02X}".format(readbyte)
            else:
                if Var_Pos == None:
                    byte_str += ",{}".format(readbyte)
                else:
                    if (i - current_cp - 1) in Var_Pos:
                        byte_str += ",_V{}".format(readbyte)
                    else:
                        byte_str += ",{}".format(readbyte)
        return byte_str
    except BaseException as e:
        print (e)
        return byte_str


def gotoNextMacro():
    LedNr = None
    End = False
    cp = pMobaLedLib.cp
    Type = pgm_read_byte_near(cp)
    cp += 1
    pMobaLedLib.cp = cp

    if Type == CONST_T:
        LedNr   = pgm_read_led_nr( cp + P_LEDNR);
        pMobaLedLib.IncCP_Const();
    elif Type == HOUSE_T :
        LedNr  = pgm_read_led_nr( cp + P_HOUSE_LED);
        pMobaLedLib.IncCP_House();
    elif Type == FIRE_T :
        LedNr    = pgm_read_led_nr( cp + P_FIRE_LED0);
        pMobaLedLib.IncCP_Fire();
    elif Type == SET_COLTAB_T:
        pMobaLedLib.IncCP_Set_ColTab()
    elif Type == SET_CANDLETAB_T:
        pMobaLedLib.IncCP_Set_CandleTab()
    elif Type == SET_TV_TAB_T :
        pMobaLedLib.IncCP_Set_TV_Tab()
    elif Type == SET_DEF_NEON_T:
        pMobaLedLib.IncCP_Set_Def_Neon()
    elif Type == NEW_HSV_GROUP_T :
        pMobaLedLib.IncCP_New_HSV_Group();
    elif Type == NEW_LOCAL_VAR_T      :
        pMobaLedLib.IncCP_New_Local_Var()
    elif Type == USE_GLOBALVAR_T      :
        pMobaLedLib.IncCP_Use_GlobalVar()
    elif Type == INCH_TO_X_VAR_T      :
        pMobaLedLib.IncCP_InCh_to_X_Var()
    elif Type == BIN_INCH_TO_TMPVAR_T :
        pMobaLedLib.IncCP_InCh_to_X_Var()
    elif Type == INCH_TO_TMPVAR_T     :
        pMobaLedLib.IncCP_InCh_to_X_Var()
    elif Type == INCH_TO_TMPVAR1_T    :
        pMobaLedLib.IncCP_InCh_to_X_Var()
    elif Type == BIN_INCH_TO_TMPVAR_T :
        pMobaLedLib.IncCP_InCh_to_X_Var()
    elif Type == BIN_INCH_TO_TMPVAR1_T:
        pMobaLedLib.IncCP_InCh_to_X_Var()
    elif Type == LOGIC_T              :
        pMobaLedLib.IncCP_Logic()
    elif Type == RANDOM_T             :
        pMobaLedLib.IncCP_Random()
    elif Type == RANDMUX_T            :
        pMobaLedLib.IncCP_RandMux()
    elif Type == WELDING_CONT_T       :
        pMobaLedLib.IncCP_Welding()
    elif Type == WELDING_T            :
        pMobaLedLib.IncCP_Welding()
    elif Type == COPYLED_T            :
        pMobaLedLib.IncCP_CopyLED()
    elif Type == SCHEDULE_T           :
        pMobaLedLib.IncCP_Schedule()
    elif Type == COUNTER_T            :
        pMobaLedLib.IncCP_Counter()
    elif Type == END_T :
        End = True;
    else:
        pt = pMobaLedLib.Is_Pattern( Type)
        if ( pt):
            TimeCnt    = Type - pt + 1;
            LedNr       = pgm_read_led_nr( cp + P_PATERN_LED);
            pMobaLedLib.IncCP_Pattern( TimeCnt);
        else:
            pass # type not known - should not happen
    return LedNr, End
        

def getLedNr_for_Macro(cp, Type):
    if Type == CONST_T:
        LedNr = pgm_read_led_nr( cp + P_LEDNR);
    elif Type == HOUSE_T :
        LedNr = pgm_read_led_nr( cp + P_HOUSE_LED);
    elif Type == FIRE_T :
        LedNr = pgm_read_led_nr( cp + P_FIRE_LED0);
    else:
        pt = pMobaLedLib.Is_Pattern( Type)
        if ( pt):
            LedNr = pgm_read_led_nr( cp + P_PATERN_LED)
        else:
            LedNr = None
    return LedNr

    
def searchNextLedNr(Type):
    cp = pMobaLedLib.cp # save pointer to current macro.Type
    Type = pgm_read_byte_near(cp)
    tmp_cp = cp + 1
    LedNr = getLedNr_for_Macro(tmp_cp, Type)
    if LedNr != None:
        return LedNr
    finished = False
    ledfound = False
    while not ledfound and not finished:
        LedNr, finished = gotoNextMacro()
        if LedNr != None:
            ledfound = True
    pMobaLedLib.cp = cp # restore pointer
    return LedNr
    
def determine_num_of_LEDs(LedNr, Type):
    nextLedNr = searchNextLedNr(Type)
    if nextLedNr != None:
        return nextLedNr - LedNr
    else:
        max_anzahl_led = pgm_read_word_near(2) 
        return max_anzahl_led - LedNr

__LED_ChannelsList = (' ROOM_DARK:RGB         ROOM_BRIGHT:RGB       ROOM_WARM_W:RGB       ROOM_RED:RGB         ' +
                           ' ROOM_D_RED:RGB        ROOM_COL0:RGB         ROOM_COL1:RGB         ROOM_COL2:RGB        ' +
                           ' ROOM_COL3:RGB         ROOM_COL4:RGB         ROOM_COL5:RGB         ROOM_COL345:RGB      ' +
                           ' FIRE:RGB              FIRED:RGB             FIREB:RGB             ROOM_CHIMNEY:RGB     ' +
                           ' ROOM_CHIMNEYD:RGB     ROOM_CHIMNEYB:RGB     ROOM_TV0:RGB          ROOM_TV0_CHIMNEY:RGB ' +
                           ' ROOM_TV0_CHIMNEYD:RGB ROOM_TV0_CHIMNEYB:RGB ROOM_TV1:RGB          ROOM_TV1_CHIMNEY:RGB ' +
                           ' ROOM_TV1_CHIMNEYD:RGB ROOM_TV1_CHIMNEYB:RGB NEON_LIGHT:RGB        NEON_LIGHT1:1        ' +
                           ' NEON_LIGHT2:2         NEON_LIGHT3:3         NEON_LIGHTD:RGB       NEON_LIGHT1D:1       ' + 
                           ' NEON_LIGHT2D:2        NEON_LIGHT3D:3        NEON_LIGHT3M:3        NEON_LIGHTM:RGB      ' +
                           ' NEON_LIGHT1M:1        NEON_LIGHT2M:2        NEON_LIGHT3L:3        NEON_LIGHTL:RGB      ' +
                           ' NEON_LIGHT1L:1        NEON_LIGHT2L:2        SINGLE_LED1:1         SINGLE_LED2:2        ' +
                           ' NEON_DEF_D:RGB        NEON_DEF1D:1          NEON_DEF2D:2          NEON_DEF3D:3         ' +
                           ' SINGLE_LED3:3         GAS_LIGHT3D:3         GAS_LIGHT1:1          GAS_LIGHT:RGB        ' +
                           ' CANDLE:RGB            CANDLE1:1             CANDLE2:2             CANDLE3:3            ' +
                           ' GAS_LIGHT2:2          GAS_LIGHT3:3          GAS_LIGHTD:RGB        GAS_LIGHT1D:1        ' +
                           ' GAS_LIGHT2D:2         SKIP_ROOM:RGB         SKIP_ROOM:RGB         SKIP_ROOM:RGB        ' +
                           ' SKIP_ROOM:RGB         SKIP_ROOM:RGB         SKIP_ROOM:RGB         SKIP_ROOM:RGB        ' +
                           ' SKIP_ROOM:RGB         SKIP_ROOM:RGB         SKIP_ROOM:RGB         SKIP_ROOM:RGB        ' +
                           ' SKIP_ROOM:RGB         SINGLE_LED1D:1        SINGLE_LED2D:2        SINGLE_LED3D:3       ' +
                           ' SINGLE_LED3D:3        SINGLE_LED3D:3        SINGLE_LED3D:3')


    
def Get_LED_Channel_from_Name(Name):
    fn_return_value = None
    p = 0 #int()

    e = 0# int()
    #-------------------------------------------------------------------
    p = InStr(__LED_ChannelsList, ' ' + Name + ':')
    if p == 0:
        P01.MsgBox('Internal Error: \'' + Name + '\' not found in \'LED_ChannelsList\'', vbCritical, 'Internal Error')
        sys.exit(0)
    else:
        p = p + 1 + Len(Name) + 1
        e = InStr(p, __LED_ChannelsList, ' ')
        fn_return_value = Mid(__LED_ChannelsList, p, e - p)
    return fn_return_value

def Count_Used_RGB_Channels(room_list_str): # for House-Macro
    fn_return_value = None
    Cnt = 0 #int()
    room_list = room_list_str.split(",")
    LED_CntList = ""
    
    for room in room_list:
        if room != "":
            LED_CntList = LED_CntList + Get_LED_Channel_from_Name(room) + ' '

    SingleLED = 0
    #-----------------------------------------
    # Single LEDs (Connected to a WS2811) are counted as one LED as long as they are in
    # assending order.
    # 1 2 3 = one RGB LED
    # 1 1 1 = three RGB LEDs
    for X in LED_CntList.split(' '):
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
    

def MLL_AnalyzeMLLConfigChunk( cp, length):
    global current_cp, max_InCh
    startCp = cp
    End = False
    max_InCh = 0
    while not End:
        current_cp = cp
        Type = pgm_read_byte_near(cp)
        cp += 1
        pMobaLedLib.cp = cp  # pMobaLedLib.cp points to byte behind Type = LEDNr if Macro has LedNr
        #pMobaLedLib.Inc_cp(Type)
        #DPRINTF_MLL_P( PSTR("Type %3d:"), Type);
        DPRINTF_MLL_P("Type{}:".format(Type))
        #DPRINTF_MLL_P("\n");
        #pMobaLedLib.cp = cp;
        if Type == CONST_T:
            LedNr   = pgm_read_led_nr( cp + P_LEDNR);
            ChanMsk = pgm_read_byte_near( cp + P_CHANELMSK);
            InCh    = pgm_read_byte_near( cp + P_INPCHANEL);
            Val0    = pgm_read_byte_near( cp + P_CONST_VAL0);
            Val1    = pgm_read_byte_near( cp + P_CONST_VAL1);
            DPRINTF_MLL_P("- CONST_T, LedNr:{}, ChanMsk:0x{:02X}, InCh:{}, Val0:{}, Val1:{}".format(LedNr, ChanMsk, InCh, Val0, Val1))
            pMobaLedLib.IncCP_Const(); #pMobaLedLib.cp points to start of next Macro = Type
            used_CV = pMobaLedLib.cp - current_cp
            #WriteMacroLine("CONST_T,_CHKL(#LED),{},#InCh,{},{}".format(ChanMsk, Val0, Val1), LedNr, InCh, Type, ChanMsk=ChanMsk, CV_Adress=current_cp+1, CV_used=used_CV)
            ChanMsk_str = Cx2str.get(ChanMsk, "CError")
            WriteMacroLine("Const(#LED,{},#InCh,{},{})".format(ChanMsk_str, Val0, Val1), LedNr, InCh, Type, ChanMsk=ChanMsk, CV_Adress=current_cp+1, CV_used=used_CV)
        elif Type == HOUSE_T :
            LedNr  = pgm_read_led_nr( cp + P_HOUSE_LED);
            InCh   = pgm_read_byte_near( cp + P_HOUSE_INCH);
            On_Min = pgm_read_byte_near( cp + P_HOUSE_ON_MIN);
            On_Max = pgm_read_byte_near( cp + P_HOUSE_ON_MAX);
            Min_T  = pgm_read_byte_near( cp + P_HOUSE_MIN_T);
            Max_T  = pgm_read_byte_near( cp + P_HOUSE_MAX_T);
            R_cnt  = pgm_read_byte_near( cp + P_HOUSE_CNT);
            pMobaLedLib.IncCP_House();
            DPRINTF_MLL_P( "- HOUSE_T, LedNr:{}, InCh:{}, OnMin:{}, OnMax:{}, MinT:{}, MaxT:{}, RoomCnt:{}\n".format( LedNr, InCh, On_Min, On_Max, Min_T, Max_T, R_cnt))
            macro ="HouseT(#LED, #InCh, {}, {}, {}, {}".format(On_Min, On_Max, Min_T, Max_T)
            room_list_str = ""
            for i in range(0, R_cnt):
                roomtype = pgm_read_byte_near( cp + P_HOUSE_CNT+1+i)
                roomtype_str = HOUSE_PALETTE_List[roomtype]
                macro += "," + roomtype_str
                room_list_str += "," + roomtype_str
            macro += ")"
            
            used_led_cnt = Count_Used_RGB_Channels(room_list_str)
            used_led_cnt_str = "{}".format(used_led_cnt)
            used_CV = pMobaLedLib.cp - current_cp
            WriteMacroLine(macro, LedNr, InCh, Type, num_used_Led_str=used_led_cnt_str, num_used_led=used_led_cnt, CV_Adress=current_cp+1, CV_used=used_CV)
        elif Type == FIRE_T :
            Led0    = pgm_read_led_nr( cp + P_FIRE_LED0);
            InCh    = pgm_read_byte_near( cp + P_FIRE_INCH);
            LED_cnt = pgm_read_byte_near( cp + P_FIRE_LEDCNT);
            Bright  = pgm_read_byte_near( cp + P_FIRE_BRIGHT);
            pMobaLedLib.IncCP_Fire();
            #DPRINTF_MLL_P( PSTR( "- FIRE_T Led0:%d, LED_cnt:%d, InCh:%d, Bright:%d\n"), Led0, LED_cnt, InCh, Bright);
            DPRINTF_MLL_P( "- FIRE_T Led0:{}, LED_cnt:{}, InCh:{}, Bright:{}\n".format(Led0, LED_cnt, InCh, Bright));
            WriteMacroLine("FIRE_T,_CHKL(#LED)+RAM1+RAMN({}),#InCh,{},{}".format(LED_cnt, LED_cnt, Bright), LedNr, InCh, Type,num_used_Led_str="{}".format(LED_cnt), num_used_led=LED_cnt)
        elif Type == SET_COLTAB_T:
            pMobaLedLib.IncCP_Set_ColTab()
            writeMacroLine2("SET_COLTAB_T", Type=Type)
        elif Type == SET_CANDLETAB_T:
            pMobaLedLib.IncCP_Set_CandleTab()
            writeMacroLine2("SET_CANDLETAB_T", Type=Type)
        elif Type == SET_TV_TAB_T :
            InCh = pgm_read_byte_near( cp + P_INPCHANEL_NO_CM)
            pMobaLedLib.IncCP_Set_TV_Tab()
            writeMacroLine2("SET_TV_TAB_T", Type=Type, InCh_Pos=0)
        elif Type == SET_DEF_NEON_T:
            InCh = pgm_read_byte_near( cp + P_INPCHANEL_NO_CM);
            pMobaLedLib.IncCP_Set_Def_Neon()
            writeMacroLine2("SET_DEF_NEON_T", Type=Type, InCh_Pos=0)
        elif Type == NEW_HSV_GROUP_T :
            DPRINTF_MLL_P( PSTR( "- NEW_HSV_GROUP_T\n"));
            pMobaLedLib.IncCP_New_HSV_Group();
            writeMacroLine2("NEW_HSV_GROUP_T", Type=Type)
        elif Type == NEW_LOCAL_VAR_T      :
            pMobaLedLib.IncCP_New_Local_Var()
            writeMacroLine2("NEW_LOCAL_VAR_T", Type=Type)
        elif Type == USE_GLOBALVAR_T      :
            pMobaLedLib.IncCP_Use_GlobalVar()
            writeMacroLine2("USE_GLOBALVAR_T", Type=Type)
        elif Type == INCH_TO_X_VAR_T      :
            pMobaLedLib.IncCP_InCh_to_X_Var()
            writeMacroLine2("INCH_TO_X_VAR_T", Type=Type, InCh_Pos=0)
        elif Type == BIN_INCH_TO_TMPVAR_T :
            pMobaLedLib.IncCP_InCh_to_X_Var()
            writeMacroLine2("BIN_INCH_TO_TMPVAR_T", Type=Type, InCh_Pos=0)
        elif Type == INCH_TO_TMPVAR_T     :
            pMobaLedLib.IncCP_InCh_to_X_Var()
            writeMacroLine2("BIN_INCH_TO_TMPVAR_T", Type=Type, InCh_Pos=0)
        elif Type == INCH_TO_TMPVAR1_T    :
            pMobaLedLib.IncCP_InCh_to_X_Var()
            writeMacroLine2("INCH_TO_TMPVAR_T", Type=Type, InCh_Pos=0)
        elif Type == BIN_INCH_TO_TMPVAR_T :
            pMobaLedLib.IncCP_InCh_to_X_Var()
            writeMacroLine2("BIN_INCH_TO_TMPVAR_T", Type=Type, InCh_Pos=0)
        elif Type == BIN_INCH_TO_TMPVAR1_T:
            pMobaLedLib.IncCP_InCh_to_X_Var()
            writeMacroLine2("BIN_INCH_TO_TMPVAR1_T", Type=Type, InCh_Pos=0)
        elif Type == LOGIC_T              :
            pMobaLedLib.IncCP_Logic()
            writeMacroLine2("LOGIC_T", Type=Type, Var_Pos=[0])
        elif Type == RANDOM_T             :
            pMobaLedLib.IncCP_Random()
            writeMacroLine2("RANDOM_T", Type=Type, InCh_Pos=1, Var_Pos=[0])
        elif Type == RANDMUX_T            :
            pMobaLedLib.IncCP_RandMux()
            writeMacroLine2("RANDMUX_T", Type=Type, InCh_Pos=2, Var_Pos=[0, 1])
        elif Type == WELDING_CONT_T       :
            pMobaLedLib.IncCP_Welding()
            writeMacroLine2("WELDING_CONT_T", Type=Type, InCh_Pos=1)
        elif Type == WELDING_T            :
            pMobaLedLib.IncCP_Welding()
            writeMacroLine2("WELDING_T", Type=Type, InCh_Pos=1)
        elif Type == COPYLED_T            :
            pMobaLedLib.IncCP_CopyLED()
            writeMacroLine2("COPYLED_T", Type=Type)
        elif Type == SCHEDULE_T           :
            pMobaLedLib.IncCP_Schedule()
            writeMacroLine2("SCHEDULE_T", Type=Type, Var_Pos=[0, 1])
        elif Type == COUNTER_T            :
            pMobaLedLib.IncCP_Counter()
            writeMacroLine2("COUNTER_T", Type=Type, InCh_Pos=1)
        elif Type == END_T :
            DPRINTF_MLL_P( PSTR( "- END_T\n"));
            End = True;
        elif Type == JUMPR_T:
            pMobaLedLib.IncCP_Jump()
            writeMacroLine2("JUMP_T", Type=Type, donotwritemacro=True)
        elif Type == NOOP_T:
            pMobaLedLib.IncCP_Noop()
            writeMacroLine2("NOOP_T", Type=Type, donotwritemacro=True)
        else: # handle pattern
            pt = pMobaLedLib.Is_Pattern( Type)
            if ( pt):
                TimeCnt    = Type - pt + 1;
                Led0       = pgm_read_led_nr( cp + P_PATERN_LED);
                NStru      = pgm_read_byte_near( cp + P_PATERN_NSTRU);
                InCh       = pgm_read_byte_near( cp + P_PATERN_INCH);
                Enable     = pgm_read_byte_near( cp + P_PATERN_ENABLE);
                #u32        = pgm_read_dword_near( cp + P_PATERN_LEDS); # typedef struct {uint8_t LEDs;uint8_t Val0;uint8_t Val1;uint8_t Off;} Par_t;
                p_LEDs = pgm_read_byte_near( cp + P_PATERN_LEDS)
                p_Val0 = pgm_read_byte_near( cp + P_PATERN_LEDS + 1)
                p_Val1 = pgm_read_byte_near( cp + P_PATERN_LEDS + 2)
                p_Off = pgm_read_byte_near( cp + P_PATERN_LEDS + 3)
                ModeAFlag  = pgm_read_byte_near( cp + P_PATERN_MODE)
                
                time_str = ""
                for i in range(0, TimeCnt):
                    T =  pgm_read_word_near( cp + P_PATERN_T1_L+2*i)
                    time_str += ",{}".format(T)

                if pt >= APATTERNT1_T:
                    patterntype = "A"
                else:
                    patterntype = " "
                    
                pMobaLedLib.IncCP_Pattern( TimeCnt);
                
                next_cp = pMobaLedLib.cp
                
                remaining_bytes_str = generate_remaining_bytes(current_cp, next_cp, P_PATERN_MODE, hex=True)
                
                #DPRINTF_MLL_P( PSTR( "- %cPATTERNT%d_T, Led0:%d, NStru:0x%02X, InCh:%d, Enab:0x%02X, LEDs:%d, Val0:0x%02X, Val1:0x%02X, Off:%d, Mode:0x%02X\n"),
                               #patterntype, TimeCnt,
                               #Led0, NStru, InCh, Enable, p.LEDs, p.Val0, p.Val1, p.Off, ModeAFlag);
                DPRINTF_MLL_P( "- {}PATTERNT{}_T, Led0:{}, NStru:0x{:02X}, InCh:{}, Enab:0x{:02X}, LEDs:{}, Val0:0x{:02X}, Val1:0x{:02X}, Off:{}, Mode:0x{:02X}, Bytes: {}\n".format(
                               patterntype, TimeCnt, Led0, NStru, InCh, Enable, p_LEDs, p_Val0, p_Val1, p_Off, ModeAFlag, remaining_bytes_str))

                remaining_bytes_str = generate_remaining_bytes(current_cp, next_cp, P_PATERN_INCH+1, hex=False)
                if p_Off & _PF_XFADE:
                    macro ="{}PATTERNT{}_T,_CHKL(#LED)+RAM7+RAMN({}),{},#InCh{}".format(patterntype, TimeCnt, p_LEDs, NStru, remaining_bytes_str)
                else:
                    macro ="{}PATTERNT{}_T,_CHKL(#LED)+RAM7,{},#InCh{}".format(patterntype, TimeCnt, NStru, remaining_bytes_str)
                num_used_LEDs = int((p_LEDs-1)/3)+1 
                num_used_LEDs_str = "C1-{}".format(p_LEDs)
                WriteMacroLine(macro, Led0, InCh, Type, num_used_Led_str=num_used_LEDs_str, num_used_led=num_used_LEDs)
            else:
                pass # type not known - should not happen
                
        cp = pMobaLedLib.cp;

    DPRINTF_MLL_P( "cp used len {}\n".format(cp-startCp));
    
def my_eeprom_read_word(addr):
    return pgm_read_word_near(addr)

def my_eeprom_read_byte(addr):
    return pgm_read_byte_near(addr)


sizeof_unsigned_short =  2 # sizeof(unsigned_short)

MAX_FAST_LED_CONTROLLER = 10

controller_List = []

ext_addr_list = []

#Led2Var_Type_list =  ("T_EQUAL_THEN","T_NOT_EQUAL_THEN", "T_LESS_THEN","T_GREATER_THAN", "T_BIN_MASK", "T_NOT_BIN_MASK")
Led2Var_Type2Str_list =  ("=","!=", "<",">", "&", "!&")
led2var_list = {}


def MLL_UseConfigInExtensionMemory():
    global pMobaLedLib, controller_List,  ext_addr_list,  expected_next_led_nr, config_strcuture_ary, led2var_list
    
    #unsigned char *extensionUnit  = ( unsigned char *)&pCVextension->dummyExtension;
    extensionUnit = 2
    totalLeds = my_eeprom_read_word(extensionUnit)
    sizeConfig_RAM = my_eeprom_read_word( extensionUnit + sizeof_unsigned_short ) #sizeof_unsigned_short));
    totalFlex      = 0;

    DPRINTF_MLL_P( "mll: use Config LEDS {}, RAM {}\n".format(totalLeds, sizeConfig_RAM));

    mllSuspendLoop = 1;
    
    controller_List = []
    
    ext_addr_list = []
    led2var_list = {}

    #if ( pMyMllLeds)
        #free( pMyMllLeds);
    #pMyMllLeds = ( CRGB *)malloc( totalLeds * sizeof( CRGB));

    #if ( pMyMllConfig_RAM)
        #free( pMyMllConfig_RAM);
    #pMyMllConfig_RAM = ( uint8_t *)malloc( sizeConfig_RAM);

    if (True): #pMyMllLeds && pMyMllConfig_RAM)
    
        #memset( pMyMllLeds, 0, totalLeds * sizeof( CRGB))
        #memset( pMyMllConfig_RAM, 0, sizeConfig_RAM);

        extensionUnit += ( 2 * sizeof_unsigned_short ) #sizeof( short));

        if ( True) : #my_eeprom_read_word(extensionUnit) <= ( my_eeprom_read_word( &pCVextension->lengthExtension) - ( 5 * sizeof_unsigned_short)))
       
            offsetLeds = 0
            expected_next_led_nr = 0
            config_strcuture_ary = []

            #// DPRINTF_MLL_P( PSTR( "mll: use Controller size %d\n"), my_eeprom_read_word( extensionUnit));

            #memset( controllerLeds, 0, sizeof( controllerLeds));

            #for ( uint8_t indexContent = 0; indexContent < my_eeprom_read_word(extensionUnit); indexContent += ( 2 * sizeof_unsigned_short)):
            
            controller_List = []
            
            for indexContent in range(0, my_eeprom_read_word(extensionUnit), 2 * sizeof_unsigned_short):
            
                if ( ( indexContent / ( 2 * sizeof_unsigned_short)) < MAX_FAST_LED_CONTROLLER):
                    firstLed = my_eeprom_read_word( extensionUnit + indexContent + sizeof_unsigned_short)
                    numLeds  = my_eeprom_read_word(  extensionUnit + indexContent + ( 2 * sizeof_unsigned_short))

                    DPRINTF_MLL_P( "mll: use Controller {}, firstLed {}, numLeds {}\n".format(( indexContent / ( 2 * sizeof_unsigned_short)), firstLed, numLeds));

                    DPRINTF_MLL_P("mll: add Controller {}\n".format( indexContent / ( 2 * sizeof_unsigned_short)))
                    
                    controller_List.append([firstLed, numLeds])


            #// advance to next section
            totalFlex += my_eeprom_read_word(extensionUnit)
            extensionUnit += sizeof_unsigned_short + my_eeprom_read_word(extensionUnit);

            if ( True): #my_eeprom_read_word( extensionUnit) <= ( my_eeprom_read_word( &pCVextension->lengthExtension) - ( 4 * sizeof_unsigned_short) - totalFlex))
            
                #// DPRINTF_MLL_P( PSTR( "mll: use Ext_Adr size %d\n"), my_eeprom_read_word( extensionUnit));
                
                # *** Ext_Addr Array

                sizeMyMllExt_Addr = my_eeprom_read_word( extensionUnit);
                if ( True): #pMyMllExt_Addr):
                
                    #free( pMyMllExt_Addr);
                    pMyMllExt_Addr = 0;
                
                #if ( sizeMyMllExt_Addr)
                #    pMyMllExt_Addr = ( Ext_Addr_T *)malloc( sizeMyMllExt_Addr);

                #if ( pMyMllExt_Addr)
                #    memset( pMyMllExt_Addr, 0, sizeMyMllExt_Addr);

                if ( True) : #!sizeMyMllExt_Addr || pMyMllExt_Addr)
                    #for ( uint8_t indexContent = 0; indexContent < my_eeprom_read_word( extensionUnit); indexContent += ( 2 * sizeof_unsigned_short))
                    for indexContent in range(0, my_eeprom_read_word(extensionUnit), 2 * sizeof_unsigned_short):
                        addr  = my_eeprom_read_word( ( extensionUnit + indexContent + sizeof_unsigned_short));
                        inCnt = my_eeprom_read_word( ( extensionUnit + indexContent + ( 2 * sizeof_unsigned_short)));

                        #DPRINTF_MLL_P( PSTR( "mll: use Ext_Addr %d, Addr %d, InCnt %d\n"), ( indexContent / ( 2 * sizeof_unsigned_short)), addr, inCnt);
                        DPRINTF_MLL_P( "mll: use Ext_Addr {}, Addr {}, InCnt {}\n".format(( indexContent / ( 2 * sizeof_unsigned_short)), addr, inCnt))

                        #pMyMllExt_Addr[indexContent/( 2 * sizeof_unsigned_short)].AddrAndTyp = addr;
                        #pMyMllExt_Addr[indexContent/( 2 * sizeof_unsigned_short)].InCnt      = inCnt;
                        
                        ext_addr_list.append([addr, inCnt])
                    
                    #// advance to next section
                    totalFlex += my_eeprom_read_word( extensionUnit);
                    extensionUnit += sizeof_unsigned_short + my_eeprom_read_word( extensionUnit);
                    
                    led2var_list = {}
                    led2var_list[0xFFFF] = [255, 0, "---", 0]

                    if ( True): #my_eeprom_read_word( extensionUnit) <= ( my_eeprom_read_word( &pCVextension->lengthExtension) - ( 5 * sizeof_unsigned_short) - totalFlex))
                    
                        #DPRINTF_MLL_P( PSTR( "mll: use LED2Var16_Tab size %d\n"), my_eeprom_read_word( extensionUnit));
                        DPRINTF_MLL_P("mll: use LED2Var16_Tab size {}\n".format(my_eeprom_read_word( extensionUnit)))

                        #// here starts the genric access via PGM_RED_XXX
                        pStartConfigInEEPROM = extensionUnit + sizeof_unsigned_short

                        pMyMllLED2Var16_Tab  = extensionUnit + sizeof_unsigned_short;
                        sizeMyMllLED2Var_Tab = my_eeprom_read_word( extensionUnit);
                        
                        # LED2VarTab
                        #cv0021=FF // Var_Nr (InCnt) (low ffs) (0xFF is a default-dummy)
                        #cv0022=FF // high ffs                 (0xFF is a default-dummy)
                        #cv0023=FF // LED_Nr (low ffs)         (0xFF is a default-dummy)
                        #cv0024=FF // high ffs                 (0xFF is a default-dummy)
                        #cv0025=FF // Offset_And_Typ           (0xFF is a default-dummy)
                        #cv0026=FF // Value (to compare)       (0xFF is a default-dummy) 
                        tablestart = extensionUnit + 2
                        
                        for indexContent in range(0, my_eeprom_read_word(extensionUnit), 6):
                            Varnr  = my_eeprom_read_word( ( tablestart + indexContent ));
                            LedNr = my_eeprom_read_word( ( tablestart + indexContent + 2));
                            Offset_and_Type = my_eeprom_read_byte( ( tablestart + indexContent + 4));
                            Offset = Offset_and_Type >> 3
                            L2V_Type = Offset & 3
                            L2V_Type_str = Led2Var_Type2Str_list[L2V_Type]
                            Value = my_eeprom_read_byte( ( tablestart + indexContent + 5));
    
                            #DPRINTF_MLL_P( PSTR( "mll: use Ext_Addr %d, Addr %d, InCnt %d\n"), ( indexContent / ( 2 * sizeof_unsigned_short)), addr, inCnt);
                            DPRINTF_MLL_P( "mll: use LED2VAR {}, VarNr {}, LedNr {}, Offset_And_Type {}, Value {}\n".format(( indexContent / ( 2 * sizeof_unsigned_short)), Varnr, LedNr, Offset_and_Type, Value))
    
                            #pMyMllExt_Addr[indexContent/( 2 * sizeof_unsigned_short)].AddrAndTyp = addr;
                            #pMyMllExt_Addr[indexContent/( 2 * sizeof_unsigned_short)].InCnt      = inCnt;
                            
                            led2var_list[LedNr] = [Varnr, Offset, L2V_Type_str, Value]

                        #// advance to next section
                        totalFlex += my_eeprom_read_word( extensionUnit);
                        extensionUnit += sizeof_unsigned_short + my_eeprom_read_word( extensionUnit);

                        if ( True) : #my_eeprom_read_word( extensionUnit) <= ( my_eeprom_read_word( &pCVextension->lengthExtension) - ( 6 * sizeof_unsigned_short) - totalFlex))
                        
                            #DPRINTF_MLL_P( PSTR( "mll: use Config Chunk size %d\n"), my_eeprom_read_word( extensionUnit));
                            DPRINTF_MLL_P( "mll: use Config Chunk size {}\n".format(my_eeprom_read_word( extensionUnit)))
                            

                            #if ( pMobaLedLib)
                            #    delete pMobaLedLib;
                            pMobaLedLib = MobaLedLib_C() #pMyMllLeds, totalLeds, extensionUnit + sizeof_unsigned_short, pMyMllConfig_RAM, sizeConfig_RAM, None, None);
                            
                            pConfigInExtension = extensionUnit + sizeof_unsigned_short;

                            MLL_AnalyzeMLLConfigChunk( extensionUnit + sizeof_unsigned_short, my_eeprom_read_word( extensionUnit));

                            totalMyMllLeds = totalLeds;
                            mllSuspendLoop = 0;




def convert_picoconfig_to_pgf(picoConfig):
    global picoConfig_ary, picoConfig_Descr_str
    picoConfig_ary = []
    picoConfig_Descr_str = ""
    
    
    for line in picoConfig:
        if line.startswith("#"):
            DPRINTF_MLL_P(line, writemacro=True)
        elif line.startswith("cv"):
            picoConfig_ary.append(int(line[7:], 16))
            
    #try:
    MLL_UseConfigInExtensionMemory()
    #except BaseException as e:
    #    print(e)
        
    #    Head:	Program_Generator configuration file	V1.0
    #   Sheet:	Selectrix	Selectrix        
    maxInch_line = "Line:" + vbTab + "Act" + vbTab + vbTab + vbTab + vbTab + vbTab + vbTab + vbTab + vbTab + "//#MaxInchVar="+str(max_InCh) + "\n"
    
    picoConfig_Descr_str = "Head:	Program_Generator configuration file	V1.0\n" +"Sheet:	DCC	Pico_Config\n" + maxInch_line + picoConfig_Descr_str
    Lines = Split(picoConfig_Descr_str, "\n")
    
    # Save the pgf-file to a file
    ConfigFileDir = M08.GetWorkbookPath() + '/' + "LEDs_AutoConfig/"
    file_path = ConfigFileDir + "LEDs_AutoConfig.dl.pgf"
    with open(file_path, "w") as file:
        file.write(picoConfig_Descr_str)
        
    return Lines

def convert_picoconfig_to_structure(picoConfig):
    global picoConfig_ary, picoConfig_Descr_str, config_strcuture_ary
    picoConfig_ary = []
    picoConfig_Descr_str = ""
    config_strcuture_ary = []
    for line in picoConfig:
        if line.startswith("#"):
            DPRINTF_MLL_P(line, writemacro=True)
        elif line.startswith("cv"):
            picoConfig_ary.append(int(line[7:], 16))
            
    #try:
    MLL_UseConfigInExtensionMemory()
    
    return config_strcuture_ary