# -*- coding: utf-8 -*-
#
#         MobaLedCheckColors: Color checker for WS2812 and WS2811 based MobaLedLib
#
#         DefaultData
#
# * Version: 2.25
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
# * V2.00 11-04-2020 - Harold Linke - update with pyPrgramGenerator
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


PROG_VERSION ="3.1.0.008 17.04.2022"
hexversion = 0x03010001
LARGE_FONT= ("Verdana", 12)
VERY_LARGE_FONT = ("Verdana", 14)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)
Very_SMALL_FONT= ("Verdana", 6)

MAC_Version = False #True

COLORCOR_MAX = 255

SIZEFACTOR = 1 # 720/1280

# colorwheel view
DELTA_H = 270
INVERT_WHEEL = True

# filenames
# all filenames are relativ to the location of the main program pyProg_generator_MobaLedLib.py

LOG_FILENAME = 'logfile.log'
PARAM_FILENAME = 'MobaLedTest_param.json'
CONFIG_FILENAME = '../../MobaLedTest_config.json'
MACRODEF_FILENAME = 'MobaLedTest_macrodef.json'
MACROPARAMDEF_FILENAME = 'MobaLedTest_macroparamdef.json'
DISCONNECT_FILENAME = 'MobaLedTest_disconnect.txt'
CLOSE_FILENAME = 'MobaLedTest_close.txt'
TEMP_LEDEFFECTTABLE_FILENAME = "temp_ledeffect_table.json"

InoName_DCC = "23_A.DCC_Interface.ino"
InoName__SX = "23_A.Selectrix_Interface.ino"

Ino_Dir_LED = "LEDs_AutoProg/"
InoName_LED = "LEDs_AutoProg.ino"

FINISH_FILE = "Finished.txt"                                                 # 03.12.19:
COLORTESTONLY_FILE = "ColorTestOnly.txt"

SerialIF_teststring1 = "LEDs_AutoProg"
SerialIF_teststring2 = "#Color Test LED"

PERCENT_BRIGHTNESS = 1  # 1 = Show the brightnes as percent, 0 = Show the brightnes as ">>>"# 03.12.19:

DEFAULT_PALETTE = {
                    "ROOM_COL0"   : "#0F0D03",
                    "ROOM_COL1"   : "#162C1B",
                    "ROOM_COL2"   : "#9B4905",
                    "ROOM_COL3"   : "#271201",
                    "ROOM_COL4"   : "#1E0000",
                    "ROOM_COL5"   : "#4F2707",
                    "GAS_LIGHT D" : "#323232",
                    "GAS LIGHT"   : "#FFFFFF",
                    "NEON_LIGHT D": "#14141B",
                    "NEON_LIGHT M": "#464650",
                    "NEON_LIGHT"  : "#F5F5FF",
                    "ROOM_TV0 A"  : "#323214",
                    "ROOM_TV0 B"  : "#46461E",
                    "ROOM_TV1 A"  : "#323208",
                    "ROOM_TV1 B"  : "#323208",
                    "SINGLE_LED"  : "#FFFFFF",
                    "SINGLE_LED D": "#323232"
                    }

HOUSE_PALETTE = {    "ROOM_DARK"          : "#323232",
                     "ROOM_BRIGHT"        : "#FFFFFF",
                     "ROOM_WARM_W"        : "#934D08",
                     "ROOM_RED"           : "#FF0000",
                     "ROOM_D_RED"         : "#320009",
                     "ROOM_COL0"          : "#0F0D03",
                     "ROOM_COL1"          : "#162C1B",
                     "ROOM_COL2"          : "#9B4905",
                     "ROOM_COL3"          : "#271201",
                     "ROOM_COL4"          : "#1E0000",
                     "ROOM_COL5"          : "#4F2707",
                     "ROOM_COL345"        : "#271201",
                     "FIRE"               : "#000000",
                     "FIRED"              : "#000000",
                     "FIREB"              : "#000000",
                     "ROOM_CHIMNEY"       : "#000000",
                     "ROOM_CHIMNEYD"      : "#000000",
                     "ROOM_CHIMNEYB"      : "#000000",
                     "ROOM_TV0"           : "#323214",
                     "ROOM_TV0_CHIMNEY"   : "#323214",
                     "ROOM_TV0_CHIMNEYD"  : "#323214",
                     "ROOM_TV0_CHIMNEYB"  : "#323214",
                     "ROOM_TV1"           : "#323208",
                     "ROOM_TV1_CHIMNEY"   : "#323208",
                     "ROOM_TV1_CHIMNEYD"  : "#323208",
                     "ROOM_TV1_CHIMNEYB"  : "#323208",
                     "NEON_LIGHT"         : "#F5F5FF",
                     "NEON_LIGHT_SGL"     : "#F5F5FF",
                     "NEON_LIGHT1"        : "#F5F5FF",
                     "NEON_LIGHT2"        : "#F5F5FF",
                     "NEON_LIGHT3"        : "#F5F5FF",
                     "NEON_LIGHTD"        : "#14141B",
                     "NEON_LIGHTD_SGL"    : "#14141B",
                     "NEON_LIGHT1D"       : "#14141B",
                     "NEON_LIGHT2D"       : "#14141B",
                     "NEON_LIGHT3D"       : "#14141B",
                     "NEON_LIGHTM"        : "#464650",
                     "NEON_LIGHTM_SGL"    : "#464650",
                     "NEON_LIGHT1M"       : "#464650",
                     "NEON_LIGHT2M"       : "#464650",
                     "NEON_LIGHT3M"       : "#464650",
                     "NEON_LIGHTL"        : "#464650",
                     "NEON_LIGHTL_SGL"    : "#464650",
                     "NEON_LIGHT1L"       : "#464650",
                     "NEON_LIGHT2L"       : "#464650",
                     "NEON_LIGHT3L"       : "#464650",
                     "NEON_DEF_D"         : "#14141B",
                     "NEON_DEF_D_SGL"     : "#14141B",
                     "NEON_DEF1D"         : "#14141B",
                     "NEON_DEF2D"         : "#14141B",
                     "NEON_DEF3D"         : "#14141B",
                     "LED_SGL"            : "#FFFFFF",
                     "SINGLE_LED1"        : "#FFFFFF",
                     "SINGLE_LED2"        : "#FFFFFF",
                     "SINGLE_LED3"        : "#FFFFFF",
                     "LED_D_SGL"          : "#323232",
                     "SINGLE_LED1D"       : "#323232",                         
                     "SINGLE_LED2D"       : "#323232",                                          
                     "SINGLE_LED3D"       : "#323232",                      
                     "GAS_LIGHT"          : "#FFFFFF",
                     "GAS_LIGHT_SGL"      : "#FFFFFF",
                     "GAS_LIGHT1"         : "#FFFFFF",
                     "GAS_LIGHT2"         : "#FFFFFF",
                     "GAS_LIGHT3"         : "#FFFFFF",
                     "GAS_LIGHTD"         : "#323232",
                     "GAS_LIGHTD_SGL"     : "#323232",
                     "GAS_LIGHT1D"        : "#323232",
                     "GAS_LIGHT2D"        : "#323232",
                     "GAS_LIGHT3D"        : "#323232",
                     "SKIP_ROOM"          : "#000000"                     
                     }

HOUSE_PALETTE2COLOR_PALETTE = {
                     "ROOM_DARK"          : "#323232",
                     "ROOM_BRIGHT"        : "#FFFFFF",
                     "ROOM_WARM_W"        : "#934D08",
                     "ROOM_RED"           : "#FF0000",
                     "ROOM_D_RED"         : "#320009",
                     "ROOM_COL0"          : "ROOM_COL0",
                     "ROOM_COL1"          : "ROOM_COL1",
                     "ROOM_COL2"          : "ROOM_COL2",
                     "ROOM_COL3"          : "ROOM_COL3",
                     "ROOM_COL4"          : "ROOM_COL4",
                     "ROOM_COL5"          : "ROOM_COL5",
                     "ROOM_COL345"        : "ROOM_COL3",
                     "FIRE"               : "#000000",
                     "FIRED"              : "#000000",
                     "FIREB"              : "#000000",
                     "ROOM_CHIMNEY"       : "#000000",
                     "ROOM_CHIMNEYD"      : "#000000",
                     "ROOM_CHIMNEYB"      : "#000000",
                     "ROOM_TV0"           : "ROOM_TV0 A",
                     "ROOM_TV0_CHIMNEY"   : "ROOM_TV0 A",
                     "ROOM_TV0_CHIMNEYD"  : "ROOM_TV0 A",
                     "ROOM_TV0_CHIMNEYB"  : "ROOM_TV0 A",
                     "ROOM_TV1"           : "ROOM_TV1 A",
                     "ROOM_TV1_CHIMNEY"   : "ROOM_TV1 A",
                     "ROOM_TV1_CHIMNEYD"  : "ROOM_TV1 A",
                     "ROOM_TV1_CHIMNEYB"  : "ROOM_TV1 A",
                     "NEON_LIGHT"         : "NEON_LIGHT",
                     "NEON_LIGHT_SGL"     : "NEON_LIGHT",
                     "NEON_LIGHT1"        : "NEON_LIGHT",
                     "NEON_LIGHT2"        : "NEON_LIGHT",
                     "NEON_LIGHT3"        : "NEON_LIGHT",
                     "NEON_LIGHTD"        : "NEON_LIGHT D",
                     "NEON_LIGHTD_SGL"    : "NEON_LIGHT D",
                     "NEON_LIGHT1D"       : "NEON_LIGHT D",
                     "NEON_LIGHT2D"       : "NEON_LIGHT D",
                     "NEON_LIGHT3D"       : "NEON_LIGHT D",
                     "NEON_LIGHTM"        : "NEON_LIGHT M",
                     "NEON_LIGHTM_SGL"    : "NEON_LIGHT M",
                     "NEON_LIGHT1M"       : "NEON_LIGHT M",
                     "NEON_LIGHT2M"       : "NEON_LIGHT M",
                     "NEON_LIGHT3M"       : "NEON_LIGHT M",
                     "NEON_LIGHTL_SGL"    : "#464650",
                     "NEON_LIGHTL"        : "#464650",
                     "NEON_LIGHT1L"       : "#464650",
                     "NEON_LIGHT2L"       : "#464650",
                     "NEON_LIGHT3L"       : "#464650",
                     "NEON_DEF_D"         : "NEON_LIGHT D",
                     "NEON_DEF_D_SGL"     : "NEON_LIGHT D",
                     "NEON_DEF1D"         : "NEON_LIGHT D",
                     "NEON_DEF2D"         : "NEON_LIGHT D",
                     "NEON_DEF3D"         : "NEON_LIGHT D",
                     "LED_SGL"            : "SINGLE_LED",
                     "SINGLE_LED1"        : "SINGLE_LED",
                     "SINGLE_LED2"        : "SINGLE_LED",
                     "SINGLE_LED3"        : "SINGLE_LED",
                     "LED_D_SGL"          : "SINGLE_LED D",  
                     "SINGLE_LED1D"       : "SINGLE_LED D",                         
                     "SINGLE_LED2D"       : "SINGLE_LED D",                                          
                     "SINGLE_LED3D"       : "SINGLE_LED D",                      
                     "GAS_LIGHT"          : "GAS LIGHT",
                     "GAS_LIGHT_SGL"      : "GAS LIGHT",
                     "GAS_LIGHT1"         : "GAS LIGHT",
                     "GAS_LIGHT2"         : "GAS LIGHT",
                     "GAS_LIGHT3"         : "GAS LIGHT",
                     "GAS_LIGHTD"         : "GAS_LIGHT D",
                     "GAS_LIGHTD_SGL"     : "GAS_LIGHT D",
                     "GAS_LIGHT1D"        : "GAS_LIGHT D",
                     "GAS_LIGHT2D"        : "GAS_LIGHT D",
                     "GAS_LIGHT3D"        : "GAS_LIGHT D",
                     "SKIP_ROOM"          : "#000000"                     
                     }

SingleEffectHandling_Tbl = {
    "NEON_LIGHT_SGL"     : "NEON_LIGHT{}",
    "NEON_LIGHT1"        : "NEON_LIGHT{}",
    "NEON_LIGHT2"        : "NEON_LIGHT{}",
    "NEON_LIGHT3"        : "NEON_LIGHT{}",
    "NEON_LIGHTD_SGL"    : "NEON_LIGHT{}D",
    "NEON_LIGHT1D"       : "NEON_LIGHT{}D",
    "NEON_LIGHT2D"       : "NEON_LIGHT{}D",
    "NEON_LIGHT3D"       : "NEON_LIGHT{}D",
    "NEON_LIGHTM_SGL"    : "NEON_LIGHT{}M",
    "NEON_LIGHT1M"       : "NEON_LIGHT{}M",
    "NEON_LIGHT2M"       : "NEON_LIGHT{}M",
    "NEON_LIGHT3M"       : "NEON_LIGHT{}M",
    "NEON_LIGHTL_SGL"    : "NEON_LIGHT{}L",
    "NEON_LIGHT1L"       : "NEON_LIGHT{}L",
    "NEON_LIGHT2L"       : "NEON_LIGHT{}L",
    "NEON_LIGHT3L"       : "NEON_LIGHT{}L",
    "NEON_DEF_D_SGL"     : "NEON_DEF{}D",
    "NEON_DEF1D"         : "NEON_DEF{}D",
    "NEON_DEF2D"         : "NEON_DEF{}D",
    "NEON_DEF3D"         : "NEON_DEF{}D",
    "LED_SGL"            : "SINGLE_LED{}",
    "SINGLE_LED1"        : "SINGLE_LED{}",
    "SINGLE_LED2"        : "SINGLE_LED{}",
    "SINGLE_LED3"        : "SINGLE_LED{}",
    "LED_D_SGL"          : "SINGLE_LED{}D",  
    "SINGLE_LED1D"       : "SINGLE_LED{}D",                         
    "SINGLE_LED2D"       : "SINGLE_LED{}D",                                          
    "SINGLE_LED3D"       : "SINGLE_LED{}D",
    "GAS_LIGHT_SGL"      : "GAS_LIGHT{}",
    "GAS_LIGHT1"         : "GAS_LIGHT{}",
    "GAS_LIGHT2"         : "GAS_LIGHT{}",
    "GAS_LIGHT3"         : "GAS_LIGHT{}",
    "GAS_LIGHTD_SGL"     : "GAS_LIGHT{}D",
    "GAS_LIGHTD"         : "GAS_LIGHT{}D",
    "GAS_LIGHT1D"        : "GAS_LIGHT{}D",
    "GAS_LIGHT2D"        : "GAS_LIGHT{}D",
    "GAS_LIGHT3D"        : "GAS_LIGHT{}D",
    "C1"                 : "C{}",
    "C2"                 : "C{}",
    "C3"                 : "C{}",
    "C_auto"             : "C{}"
    }


SETMACRO_LIST = ["Set_ColTab", "Set_TV_COL1", "Set_TV_COL2", "Set_TV_BW1", "Set_TV_BW2", "Set_Def_Neon"]
SWITCHMACROLIST = ["DCC-switch","CAN-switch", "ARDUINO Port", "Variable"]

EFFECT_LED_CHANNELS_LIST = {
            "ROOM_DARK": "1",
            "ROOM_BRIGHT": "1",
            "ROOM_WARM_W": "1",
            "ROOM_RED": "1",
            "ROOM_D_RED": "1",
            "ROOM_COL0": "1",
            "ROOM_COL1": "1",
            "ROOM_COL2": "1",
            "ROOM_COL3": "1",
            "ROOM_COL4": "1",
            "ROOM_COL5": "1",
            "ROOM_COL345": "1",
            "FIRE": "1",
            "FIRED": "1",
            "FIREB": "1",
            "ROOM_CHIMNEY": "1",
            "ROOM_CHIMNEYD": "1",
            "ROOM_CHIMNEYB": "1",
            "ROOM_TV0": "1",
            "ROOM_TV0_CHIMNEY": "1",
            "ROOM_TV0_CHIMNEYD": "1",
            "ROOM_TV0_CHIMNEYB": "1",
            "ROOM_TV1": "1",
            "ROOM_TV1_CHIMNEY": "1",
            "ROOM_TV1_CHIMNEYD": "1",
            "ROOM_TV1_CHIMNEYB": "1",
            "NEON_LIGHT": "1",
            "NEON_LIGHT_SGL": "C1",
            "NEON_LIGHT1": "C1",
            "NEON_LIGHT2": "C2",
            "NEON_LIGHT3": "C3",
            "NEON_LIGHTD": "1",
            "NEON_LIGHTD_SGL": "C1",
            "NEON_LIGHT1D": "C1",
            "NEON_LIGHT2D": "C2",
            "NEON_LIGHT3D": "C3",
            "NEON_LIGHTM": "1",
            "NEON_LIGHTM_SGL": "C1",
            "NEON_LIGHT1M": "C1",
            "NEON_LIGHT2M": "C2",
            "NEON_LIGHT3M": "C3",
            "NEON_LIGHTL": "1",
            "NEON_LIGHTL_SGL": "C1",
            "NEON_LIGHT1L": "C1",
            "NEON_LIGHT2L": "C2",
            "NEON_LIGHT3L": "C3",
            "NEON_DEF_D": "1",
            "NEON_DEFD_SGL": "C1",
            "NEON_DEF1D": "C1",
            "NEON_DEF2D": "C2",
            "NEON_DEF3D": "C3",
            "LED_SGL": "C1",
            "SINGLE_LED1": "C1",
            "SINGLE_LED2": "C2",
            "SINGLE_LED3": "C3",
            "LED_DARK_SGL": "C1",
            "SINGLE_LED1D": "C1",
            "SINGLE_LED2D": "C2",
            "SINGLE_LED3D": "C3",
            "GAS_LIGHT": "1",
            "GAS_LIGHT_SGL": "C1",
            "GAS_LIGHT1": "C1",
            "GAS_LIGHT2": "C2",
            "GAS_LIGHT3": "C3",
            "GAS_LIGHTD": "1",
            "GAS_LIGHTD_SGL": "C1",
            "GAS_LIGHT1D": "C1",
            "GAS_LIGHT2D": "C2",
            "GAS_LIGHT3D": "C3",
            "SKIP_ROOM": "1",
            "C_auto": "1",
            "C_ALL" : "3",
            "C1"    : "1",
            "C2"    : "1",
            "C3"    : "1",
            "C12"   : "2",
            "C23"   : "2",
            "C_RED" : "1",
            "C_GREEN": "1",
            "C_BLUE" : "1",
            "C_WHITE": "3",
            "C_YELLOW": "2",
            "C_CYAN"  : "2",
            "C1-1"    : "1",
            "C1-2"    : "2",
            "C1-3"    : "3",
            "C1-6"    : "6",
            "C1-n"    : "LEDcnt",
            "C2-3"    : "2"
            }

EFFECT_LED_STARTLED_LIST = {
            "ROOM_DARK": "1",
            "ROOM_BRIGHT": "1",
            "ROOM_WARM_W": "1",
            "ROOM_RED": "1",
            "ROOM_D_RED": "1",
            "ROOM_COL0": "1",
            "ROOM_COL1": "1",
            "ROOM_COL2": "1",
            "ROOM_COL3": "1",
            "ROOM_COL4": "1",
            "ROOM_COL5": "1",
            "ROOM_COL345": "1",
            "FIRE": "1",
            "FIRED": "1",
            "FIREB": "1",
            "ROOM_CHIMNEY": "1",
            "ROOM_CHIMNEYD": "1",
            "ROOM_CHIMNEYB": "1",
            "ROOM_TV0": "1",
            "ROOM_TV0_CHIMNEY": "1",
            "ROOM_TV0_CHIMNEYD": "1",
            "ROOM_TV0_CHIMNEYB": "1",
            "ROOM_TV1": "1",
            "ROOM_TV1_CHIMNEY": "1",
            "ROOM_TV1_CHIMNEYD": "1",
            "ROOM_TV1_CHIMNEYB": "1",
            "NEON_LIGHT": "1",
            "NEON_LIGHT_SGL": "",
            "NEON_LIGHT1": "1",
            "NEON_LIGHT2": "2",
            "NEON_LIGHT3": "3",
            "NEON_LIGHTD": "1",
            "NEON_LIGHTD_SGL": "",
            "NEON_LIGHT1D": "1",
            "NEON_LIGHT2D": "2",
            "NEON_LIGHT3D": "3",
            "NEON_LIGHTM": "1",
            "NEON_LIGHTM_SGL": "",
            "NEON_LIGHT1M": "1",
            "NEON_LIGHT2M": "2",
            "NEON_LIGHT3M": "3",
            "NEON_LIGHTL": "1",
            "NEON_LIGHTL_SGL": "",
            "NEON_LIGHT1L": "1",
            "NEON_LIGHT2L": "2",
            "NEON_LIGHT3L": "3",
            "NEON_DEF_D": "1",
            "NEON_DEFD_SGL": "",
            "NEON_DEF1D": "1",
            "NEON_DEF2D": "2",
            "NEON_DEF3D": "3",
            "LED_SGL": "",
            "SINGLE_LED1": "1",
            "SINGLE_LED2": "2",
            "SINGLE_LED3": "3",
            "LED_DARK_SGL": "",
            "SINGLE_LED1D": "1",
            "SINGLE_LED2D": "2",
            "SINGLE_LED3D": "3",
            "GAS_LIGHT": "1",
            "GAS_LIGHT_SGL": "",
            "GAS_LIGHT1": "1",
            "GAS_LIGHT2": "2",
            "GAS_LIGHT3": "3",
            "GAS_LIGHTD": "1",
            "GAS_LIGHTD_SGL": "",
            "GAS_LIGHT1D": "1",
            "GAS_LIGHT2D": "2",
            "GAS_LIGHT3D": "3",
            "SKIP_ROOM": "1",
            "C_auto": "",
            "C_ALL" : "1",
            "C1"    : "1",
            "C2"    : "2",
            "C3"    : "3",
            "C12"   : "1",
            "C23"   : "2",
            "C_RED" : "1",
            "C_GREEN": "2",
            "C_BLUE" : "3",
            "C_WHITE": "1",
            "C_YELLOW": "2",
            "C_CYAN"  : "1",
            "C1-1"    : "1",
            "C1-2"    : "1",
            "C1-3"    : "1",
            "C1-6"    : "1",
            "C1-n"    : "1",
            "C2-3"    : "2"
            }

  

CONST_PALETTE = {}

GASLIGHTS_PALETTE = {                     
                     "NEON_LIGHT"         : "NEON_LIGHT",
                     "NEON_LIGHT_SGL"     : "NEON_LIGHT",
                     "NEON_LIGHT1"        : "NEON_LIGHT",
                     "NEON_LIGHT2"        : "NEON_LIGHT",
                     "NEON_LIGHT3"        : "NEON_LIGHT",
                     "NEON_LIGHTD"        : "NEON_LIGHT D",
                     "NEON_LIGHTD_SGL"    : "NEON_LIGHT D",
                     "NEON_LIGHT1D"       : "NEON_LIGHT D",
                     "NEON_LIGHT2D"       : "NEON_LIGHT D",
                     "NEON_LIGHT3D"       : "NEON_LIGHT D",
                     "NEON_LIGHTM"        : "NEON_LIGHT M",
                     "NEON_LIGHTM_SGL"    : "NEON_LIGHT M",
                     "NEON_LIGHT1M"       : "NEON_LIGHT M",
                     "NEON_LIGHT2M"       : "NEON_LIGHT M",
                     "NEON_LIGHT3M"       : "NEON_LIGHT M",
                     "NEON_LIGHTL"        : "#464650",
                     "NEON_LIGHTL_SGL"    : "#464650",
                     "NEON_LIGHT1L"       : "#464650",
                     "NEON_LIGHT2L"       : "#464650",
                     "NEON_LIGHT3L"       : "#464650",
                     "NEON_DEF_D"         : "NEON_LIGHT D",
                     "NEON_DEF_D_SGL"     : "NEON_LIGHT D",
                     "NEON_DEF1D"         : "NEON_LIGHT D",
                     "NEON_DEF2D"         : "NEON_LIGHT D",
                     "NEON_DEF3D"         : "NEON_LIGHT D",
                     "GAS_LIGHT"          : "GAS LIGHT",
                     "GAS_LIGHT_SGL"      : "GAS LIGHT",
                     "GAS_LIGHT1"         : "GAS LIGHT",
                     "GAS_LIGHT2"         : "GAS LIGHT",
                     "GAS_LIGHT3"         : "GAS LIGHT",
                     "GAS_LIGHTD"         : "GAS_LIGHT D",
                     "GAS_LIGHTD_SGL"     : "GAS_LIGHT D",
                     "GAS_LIGHT1D"        : "GAS_LIGHT D",
                     "GAS_LIGHT2D"        : "GAS_LIGHT D",
                     "GAS_LIGHT3D"        : "GAS_LIGHT D"
                     }

DEFAULT_EFFECTPALETTE = {
                    "House"       : HOUSE_PALETTE,
                    "Const"       : CONST_PALETTE,
                    "GasLights"   : GASLIGHTS_PALETTE
                    }

DEFAULT_CONFIG = {
                    "serportnumber": 0,
                    "serportname": "No Device",
                    "baudrate": 115200,         # baudrate, possible values: 50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200
                    "maxLEDcount": 255,
                    "lastLedCount": 1,
                    "lastLed": 0,
                    "pos_x": 10,
                    "pos_y": 10,
                    "colorview": 1,
                    "startpage": -1,
                    "startpagename" : "StartPage",
                    "led_correction_r": COLORCOR_MAX,
                    "led_correction_g": int(69*COLORCOR_MAX/100),
                    "led_correction_b": int(94*COLORCOR_MAX/100),
                    "use_led_correction": True,
                    "old_color": "#FFFFFF",
                    "palette": DEFAULT_PALETTE,
                    "effectpalette" : DEFAULT_EFFECTPALETTE,
                    "old_effect"    : "ROOM_DARK",
                    "group_name"    : "Group001",
                    "autoconnect": False,
                    "lastSound": 0,
                    "lastSoundImpuls": 200,
                    "startcmdcb": False,
                    "startcmd_filename": " ",
                    "ArduinoTypeName": "Nano/Uno (neu)",
                    "ArduinoTypeNumber": 1,
                    "Z21Data": {
                        "0": {
                            "serportname": "NO DEVICE",
                            "dcc_start": 1,
                            "dcc_end": 9999
                        },
                        "1": {
                            "serportname": "NO DEVICE",
                            "dcc_start": 1,
                            "dcc_end": 9999
                        },
                        "2": {
                            "serportname": "NO DEVICE",
                            "dcc_start": 1,
                            "dcc_end": 9999
                        }
                    },
                    "lastservo_channel": 1,
                    "DCC BaseAddress": 100,
                    "ServoAddress": 0,
                    "ServoChannel": 0,
                    "SoundAddress": 0,
                    "SoundImpulsLength": 200,
                    "Sound_RED": 8,
                    "Sound_GREEN": 3,
                    "Sound_BLUE": 6,
                    "baudratenumber": 0,
                    "ARDUINOMessage": 0,
                    "Autoconnect": 0,
                    "ARDUINOShowAll": True,
                    "ARDUINOTakeOver": True,
                    "UseZ21Data": False,
                    "ARDUINOBlink": False,
                    "MLLDigSysName": "None",
                    "MLLDigSysNumber": 0,
                    "Baudrate": 115200,
                    "FontTitle": "12",
                    "FontLabel": "8",
                    "FontSpinbox": "8",
                    "FontScale" : "8",
                    "RMbusTimer": "0",
                    "ShowProgramGenerator": 1,
                    "ShowPatternGenerator": 0,
                    "ShowHiddentables": 0,
                    "AutoLoadWorkbooks":1,
                    "UseCOM_Port_UserForm":0,
                    "languagename": "Auto",
                    "language": 0
                }

DEFAULT_PARAM = {}

CONFIG2PARAMKEYS = {
                    "old_color"   :"color",
                    "lastLed"     :"Lednum",
                    "lastLedCount":"LedCount", 
                    "serportname" :"comport",
                    "palette"     :"coltab", 
                    }

TOOLTIPLIST = {
                   "Alte Farbe": "Alte Farbe",
                   "Aktuelle Farbe": "Aktuelle Farbe",
                   "ColorWheel":"Farbton und Sättigung auswählen durch Mausklick"
                   }
                   

BLINKFRQ     = 2 # Blinkfrequenz in Hz

ARDUINO_WAITTIME = 0.02  # Wartezeit zwischen 2 Kommandos in Sekunden 
ARDUINO_LONG_WAITTIME = 0.5



