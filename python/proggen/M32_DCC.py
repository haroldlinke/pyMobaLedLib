# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
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

import ExcelAPI.XLW_Workbook as P01
import ExcelAPI.XLWA_WinAPI as XLWA

import proggen.M02_Public as M02
#import proggen.M02_global_variables as M02GV
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header as M06
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
#import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
#import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
import proggen.M39_Simulator as M39
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80
import proggen.F00_mainbuttons as F00

import mlpyproggen.Prog_Generator as PG

""" https://wellsr.com/vba/2019/excel/vba-playsound-to-play-system-sounds-and-wav-files/
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
-------------------------------------------------------------------------
"""

""" Revision History:
 ~~~~~~~~~~~~~~~~~
 27.03.20: - Initial release: Handle DCCSend button actions and send DCC accessory commands to receiver arduino
 31.03.20: - add toggle button actions
 02.04.20: - add optional output of serial messages from receiver arduino
           - if multiple test buttons use same address toggle all related buttons
 17.04.20: - add option to use hardware handshake when communicating with LED Arduino to speed up communication
 18.04.21: - move serial port specific code to M07_COM_Port
-------------------------------------------------------------------------------------------------
"""


def DCCSend():
    callerName = String()

    #Target = Excel.Range()

    Button = Object()

    Addr = Integer()

    Direction = Byte()
    # VB2PY (UntranslatedCode) On Error Resume Next
    Button = P01.ActiveSheet.Shapes.getShape(P01.Application.caller)
    if Button==None:
        logging.debug("Button not found "+P01.Application.caller )
        return
    callerName = Button.Name
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if callerName == '':
        return
    if M02.DEBUG_DCCSEND:
        Debug.Print(P01.Format(Time, 'hh.mm.ss') + ' click on button ' + callerName)
    #Debug.Print callerName ' Debug
    Addr = P01.val(Mid(callerName, 2, 4))
    Addr = Addr - P01.val(M28.Get_String_Config_Var('DCC_Offset'))
    Direction = P01.val(Mid(callerName, 7, 2))
    if SendDCCAccessoryCommand(Addr, Direction):
        
        for Button in P01.ActiveSheet.Shapes:
            #Debug.Print Button.Name
            if Button.Name == callerName and Button.AlternativeText != '':
                Tmp = Button.Name
                if M02.DEBUG_DCCSEND:
                    Debug.Print(P01.Format(Time, 'hh.mm.ss') + ' change from' + vbCrLf + Button.Name + ' to' + vbCrLf + Button.AlternativeText)
                Button.Name = Button.AlternativeText
                Button.AlternativeText = Tmp
                #*HLButton.TextFrame2.TextRange.Text = Mid(Button.Name, 13, 1)
                Button.TextFrame2.TextRange.Text = Mid(Button.Name, 13, 1)
                Button.Fill.ForeColor.rgb = M20.GetButtonColor(P01.val(Mid(Button.Name, 10, 2)))
                Button.updateShape()
    M39.SendToSimulator(Addr, Direction)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Addr - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Direction - ByVal 
#-------------------------------------------------------------------------------------------------
def SendDCCAccessoryCommand(Addr, Direction):
#-------------------------------------------------------------------------------------------------
    fn_return_value = False
    ComPort = Integer()

    Output_Buffer = String()

    UseHardwareHandshake = Boolean()
    
    # to be able to use the hardware handshake the Arduino Nano module must be modified
    # connect A1 pin to pin 9 (CTS) of the CH340 chip
    # now you may use hardware handshake using CTR flow control
    UseHardwareHandshake = False
    M25.Make_sure_that_Col_Variables_match()
    
    #if M39.IsSimulatorActive and P01.val(M07.ComPortPage().Cells(M02.SH_VARS_ROW, M25.COMPort_COL)) <= 0:
    if M39.IsSimulatorActive and F00.port_is_busy(M07.ComPortPage().Cells(M02.SH_VARS_ROW, M25.COMPort_COL)):
        fn_return_value = True
        return fn_return_value
    if M07.Check_USB_Port_with_Dialog(M25.COMPort_COL) == False:
        return fn_return_value
        # 04.05.20: Added exit (Prior Check_USB_Port_with_Dialog ends the program in case of an error)
    if ( Addr < 1 or Addr > 9999 ) :
        P01.MsgBox(M09.Get_Language_Str('Die Adresse muss im Bereich 1 bis 9999 liegen'), vbCritical, M09.Get_Language_Str('Fehler: Decoder senden fehlgeschlagen'))
        return fn_return_value
    ComPort = P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL)
    Output_Buffer = '@' + Left(str(Addr) + '   ', 4) + ' ' + Left(str(Direction) + ' ', 2) + ' 01' + Chr(10)
    send_command_to_ARDUINO(Output_Buffer,comport=ComPort)
    fn_return_value=True    
    if not fn_return_value:
        _fn_return_value = False
        return _fn_return_value
    if M28.Get_Num_Config_Var('GEN_BUTTON_RELEASE_COM') > 0:
        # 09.04.23: Juergen, don't simulate release if legacy mode is selected
        while 1:
            if P01.GetAsyncKeyState(0x1) == 0:
                break
            # 13.12.22: wait until button is released
            XLWA.Sleep(10)
            if not (True):
                break
        Output_Buffer = '@' + Left(Addr + '   ', 4) + ' ' + Left(Direction + ' ', 2) + ' 00' + Chr(10)
        # 13.12.22: Also send the release    
        send_command_to_ARDUINO(Output_Buffer,comport=ComPort)
        fn_return_value=True
    
    #fn_return_value = M07.SendMLLCommand(ComPort, Output_Buffer, UseHardwareHandshake, M02.DEBUG_DCCSEND)
    fn_return_value=True

    #fn_return_value = M07.SendMLLCommand(ComPort, Output_Buffer, UseHardwareHandshake, M02.DEBUG_DCCSEND)
    return fn_return_value

def send_command_to_ARDUINO(command,comport=None):
    PG.global_controller.connect_if_not_connected()
    for c in command:
        PG.global_controller.send_to_ARDUINO(c,comport=comport)
        #time.sleep(0.01)
    c = chr(10)
    PG.global_controller.send_to_ARDUINO(c,comport=comport)    

# VB2PY (UntranslatedCode) Option Explicit