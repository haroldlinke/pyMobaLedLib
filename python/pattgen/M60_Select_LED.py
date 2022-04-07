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
# 2021-01-07 v4.02 HL: - Else:, ByRef check done, first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *


import proggen.Prog_Generator as PG

import ExcelAPI.P01_Workbook as P01

from ExcelAPI.X01_Excel_Consts import *


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

"""----------------------
-----------------------------------------
 Auswahl der LED Adresse:
 ~~~~~~~~~~~~~~~~~~~~~~~~
 - Charliplexing Signal
   - Blauer Kanal blinkt. Die LED ist aber unter der Platte
     => Problem wenn kein Goto verwendet wird
   - Grüner Kanal wechselt zwischen Goto 0, Goto 1
   - Roter Kanal blinkt auch
 - Sound JQ6500
   - Rot = Sound
   - Blau und Grün sind LEDs
 - Sound MP3-TF-16P
   - Rot & Grün = Sound
   - Blau = LED oder ATTiny
 => Für alle 3 Varianten
    - Blau Blinken
    - Grün Wechsel zwischen
--------------------------------------------------------------
--------------------------
-----------------------------------------------
-----------------------------------------------------
----------------------------------
UT----------------------------------------------------
"""

__Next_Fash_LED_Time = Double()
__LED_Flash_PortId = Integer()
__LED_Flash_Pattern = vbObjectInitialize(objtype=String)
__LED_Flash_Cnt = Integer()
__Act_LED_Pattern = Integer()
__LED_Flash_Nr = Integer()
__LED_Flash_Act = Boolean()

def __Flash_LED():
    #----------------------
    if __LED_Flash_Act:
        Cmd = '#L' + Hex02(__LED_Flash_Nr) + __LED_Flash_Pattern(__Act_LED_Pattern)
        Debug.Print('Flash_LED ' + __LED_Flash_Nr + '  ' + Cmd)
        if __LED_Flash_PortId > 0:
            if not Write_Com(__LED_Flash_PortId, Cmd):
                return
        __Act_LED_Pattern = __Act_LED_Pattern + 1
        if __Act_LED_Pattern >= __LED_Flash_Cnt:
            __Act_LED_Pattern = 0
        __Next_Fash_LED_Time = 1000 #Now + TimeSerial(0, 0, 1)
        # Here is a dscription how to ude windows calls, but this seames to be critical:
        #  http://www.cpearson.com/excel/OnTime.aspx
        P01.Application.OnTime(__Next_Fash_LED_Time, __Flash_LED)

def Set_Flash_LED(LedNr):
    global __Act_LED_Pattern, __LED_Flash_Nr
    Old_LED = Integer()

    Cmd = String()
    #-----------------------------------------
    P01.Application.EnableEvents = False
    Old_LED = __LED_Flash_Nr
    __Act_LED_Pattern = 0
    __LED_Flash_Nr = LedNr
    P01.Application.EnableEvents = True
    if __LED_Flash_Act and __LED_Flash_PortId > 0:
        Cmd = '#L' + Hex02(Old_LED) + ' 00 00 00 01' + vbLf
        Write_Com(__LED_Flash_PortId, Cmd)
        Sleep(20)
    Cmd = '#L' + Hex02(__LED_Flash_Nr) + __LED_Flash_Pattern(0)
    if __LED_Flash_PortId > 0:
        if not Write_Com(__LED_Flash_PortId, Cmd):
            return
        Sleep(20)

def Start_Flash_LED(PortId, LedNr):
    #--------------------------------------------------------------
    if not __LED_Flash_Act:
        __LED_Flash_PortId = PortId
        __LED_Flash_Nr = LedNr
        __LED_Flash_Act = True
        __Act_LED_Pattern = 0
        if __LED_Flash_Cnt == 0:
            __LED_Flash_Cnt = 2
            __LED_Flash_Pattern = vbObjectInitialize((__LED_Flash_Cnt,), Variant)
            #         Red                            Green                    Blue Cnt
            __LED_Flash_Pattern[0] = ' ' + Hex02(Get_Goto_pwm(0)) + ' ' + Hex02(Get_Goto_pwm(1)) + ' FF 01' + vbLf
            __LED_Flash_Pattern[1] = ' ' + Hex02(Get_Goto_pwm(1)) + ' ' + Hex02(Get_Goto_pwm(0)) + ' 00 01' + vbLf
        P01.Application.OnTime(1000, 'Flash_LED')

def Stop_Flash_LED():
    #--------------------------
    if __LED_Flash_Act:
        __LED_Flash_Act = False
        # VB2PY (UntranslatedCode) On Error Resume Next
        P01.Application.OnTime(1000, 'Flash_LED', Schedule=False)
        # VB2PY (UntranslatedCode) On Error GoTo 0
        Sleep(100)
        Debug.Print('Stop_Flash_LED ' + __LED_Flash_Nr)
        if __LED_Flash_PortId > 0:
            Cmd = '#L' + Hex02(__LED_Flash_Nr) + ' 00 00 00 01' + vbLf
            Write_Com(__LED_Flash_PortId, Cmd)
            Sleep(20)

def Select_Special_Mode():
    fn_return_value = None
    Res = String()
    #-----------------------------------------------
    Res = Select_from_Sheet_Form.Show_Form(SPECIAL_MODEDLG_SH, Get_Language_Str('Auswahl der Spezial Modes'), Get_Language_Str('Spezial Mode'), Get_Language_Str('Mit dem Pattern_Configurator können spezielle Module konfiguriert werden.' + vbCr + 'Die Muster werden in diesem Fall direkt zu dem entsprechenden Modul geschickt. Dort wird die Konfiguration dann autark abgearbeitet.'), oDialog_Dat_ROW1= Sheets(SPECIAL_MODEDLG_SH).Range('Special_Mode_Head').Row + 1, oMiddleWinCOL= 6)
    if Res != '':
        Range['Special_Mode'].Value = Split(Res, ',')(0)
        fn_return_value = True
    return fn_return_value

def Select_LED_Address_Dialog():
    fn_return_value = None
    PortId = Integer()
    #-----------------------------------------------------
    fn_return_value = - 1
    PortId = Get_USB_Port_with_Dialog()
    if PortId > 0:
        LastLEDNr = Open_Port_With_Error_Msg_and_get_LastLED(PortId)
        if LastLEDNr <= 0:
            return fn_return_value
        fn_return_value = Select_LED_Address.ShowForm(PortId, LastLEDNr - 1)
        Debug.Print('Select_LED_Address_Dialog = ' + Select_LED_Address_Dialog())
    End_Test_and_Close(PortId)
    return fn_return_value

def Get_LED_Address_Dialog():
    Res = Integer()
    #----------------------------------
    Res = Select_LED_Address_Dialog()
    if Res >= 0:
        Range['RGB_Modul_Nr'] = Res

def __Test_Without_LED_Write_Select_LED_Address():
    #UT----------------------------------------------------
    Debug.Print(Select_LED_Address.ShowForm(0, 10))

# VB2PY (UntranslatedCode) Option Explicit
