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

""" Send data over the WS281x LED protokol
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Die Daten werden als LED PWM Signale zum Charliplexing Arduino übertragen.

 Da die Erkennung des PWM Signals durch die Interrupts der Charliplexing LEDs stark verrauscht ist
 müssen die Bereiche mit denen ein Wert übertragen wird relativ breit sein.
 Für die Signale verwende ich 20 PWM Werte Abstand. Ein PWM Wert zwischen 36 und 55 wird als "Goto" Nummer 0
 interpretiert, Die "Goto" Nummer 1 entspricht dem Bereich 56 - 75. Dadurch ergeben sich 11 Bereiche.
 Das reicht aber nicht für die Datenübertragung.
 Die Daten sollen ohne feste Zeitabstände gesendet werden. Darum wird eine Methode zur Erkennung benötigt
 wann ein neues Datenpaket bekommt. Dazu wird das höchstwertigste Bit benutzt welches bei jedem Paket seinen
 Wert wechselt.
 Während
 50 is sometime to fast, 100 is working with 256 LED's
 => 100 Byte = 20 Sec (8 Bit Signal has 88 Byte, 1 Bit Signal 40 Byte = 8 Sec)
 Die Folgenden WS... Konstanten waren ursprünglich dafür gedacht, dass die Anzahl der übertragenen Bits
 verändern kann. Das wurde aber nicht konsequent umgesetzt weil die Übertragung von 4 Bit ganz gut passt.
 => Die Konstannten dürfen nicht verändert werden
    0  1  2  3  4  5  6   7   8  9 10 11
---------------------------------------------------
------------------------------------------
-------------------------------------
---------------------------------------------------------------------
--------------------------------------------
----------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------
----------------------------------------
-----------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on False
---------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
--------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------
--------------------------------------------------------------------------------------------
UT------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------
--------------------------------------------------------
--------------------------------------------
-------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------
UT-------------------------------
 Es ist zwei mal passiert, das die Übertragung zum ATTiny abgebrochen wurde.      30.12.19:
 Dabei hört das Flackern der LEDs mitten drinnen auf ?!?
----------------------------------------------------------------------------------------------------------------
UT-------------------------------------------------
--------------------------------------------------------------
UT------------------------------------
--------------------------------------------------------------------------------------------------------------
----------------------------------
----------------------------------------------------------------
-------------------------------
-------------------------------
"""

__DEBUG_SEND = False
__WaitTime = 100
__WaitTime_Start = 1800
__WaitTime_Begin = 300
__CPX_LED_ASSIGNEMENT = Byte()
__CPX_ANALOG_INPUT = Byte()
__CPX_ANALOG_LIMMITS = Byte()
__CP_HEAD_VERSION = String()
__ExpectedResponse = '#?LEDs_AutoProg Ver 1: '
PATTERNT1_T = Byte()
APATTERNT1_T = Byte()
__ANALOG_KEYS = 10
__Bit_Scale = 7
__Bit_Offset = 30
__WB_BitCnt = 4
__WB_Mask = ( 2 ** __WB_BitCnt )  - 1
__WB_MarkBit = 2 ** __WB_BitCnt
__WB_Buffer = Integer()
__WB_Remaining = Integer()
__WB_HighBit = Boolean()
__Enable_Analog_Inputs = Boolean()
__Analog_Limmits_Str = String()
__CRC_ByteList = vbObjectInitialize(objtype=Byte)
__VIESSMN_LED_ASSIGNEMENT = String()
__UNIPROG_LED_ASSIGNEMANT = String()
__REVERSE_LED_ASSIGNEMENT = String()
__BRIGHT6_LED_ASSIGNEMENT = String()

def __Set_Used_C_Code_Version(Version):
    #---------------------------------------------------
    if (Version == 1):
        __CP_HEAD_VERSION = 'CP1'
        PATTERNT1_T = 10
        APATTERNT1_T = 40
        __CPX_LED_ASSIGNEMENT = 140
        __CPX_ANALOG_INPUT = 141
        __CPX_ANALOG_LIMMITS = 142
    elif (Version == 2):
        __CP_HEAD_VERSION = 'CP2'
        PATTERNT1_T = 10
        APATTERNT1_T = 74
        __CPX_LED_ASSIGNEMENT = 200
        __CPX_ANALOG_INPUT = 201
        __CPX_ANALOG_LIMMITS = 202
    else:
        MsgBox('Internal Error: Undefined version in \'Set_Used_C_Code_Version()\':' + Version, vbCritical, 'Internal Error')
        EndProg()

def Check_if_C_Code_Version_is_Set():
    #------------------------------------------
    if __CPX_ANALOG_INPUT == 0:
        MsgBox('Internal Error: \'Set_Used_C_Code_Version()\' not called ;-(', vbCritical, 'Internal Error')
        EndProg()

def __Init_Assignement_Strings():
    #-------------------------------------
    if __VIESSMN_LED_ASSIGNEMENT == '':
        __VIESSMN_LED_ASSIGNEMENT = __LED_Assignement(8, 6, 7, 3, 0, 1, 2, 10, 11, 4, 5, 9)
        __UNIPROG_LED_ASSIGNEMANT = __LED_Assignement(0, 1, 8, 9, 11, 10, 3, 2, 4, 5, 7, 6)
        __REVERSE_LED_ASSIGNEMENT = __LED_Assignement(11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
        __BRIGHT6_LED_ASSIGNEMENT = __LED_Assignement(0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5)

def Write_Com(PortId, Txt):
    fn_return_value = None
    Size = Long()

    Status = Integer()
    #---------------------------------------------------------------------
    Size = Len(Txt)
    Status = CommWrite(PortId, Txt)
    if __DEBUG_SEND:
        Debug.Print(' Write_Com: ' + Txt)
        # Debug
    if Status != Size:
        Debug.Print('Error ' + Status + ' in CommWrite')
    else:
        fn_return_value = True
    return fn_return_value

def __Debug_Read_Com(PortId):
    Status = Integer()

    strData = String()
    #--------------------------------------------
    # Read maximum of 64 bytes from serial port.
    Status = CommRead(PortId, strData, 64)
    if Status > 0:
        # Process data.
        if __DEBUG_SEND:
            Debug.Print(strData)
    elif Status < 0:
        Debug.Print('Error')

def __Wait_Until_Arduino_Responds(PortId, WaitMsg, Timeout):
    fn_return_value = None
    Status = Integer()

    strData = String()

    AllData = String()

    t = Long()

    Cnt = Long()

    DelayTime = 50
    #----------------------------------------------------------------------------------------------------------------
    while t < Timeout:
        Status = CommRead(PortId, strData, 64)
        if Status > 0:
            # Process data.
            if Len(strData) > 0:
                AllData = AllData + strData
        elif Status < 0:
            Debug.Print('Error in Wait_Until_Arduino_Responds(): ' + Status)
            return fn_return_value
        if Len(AllData) > 0 and InStr(AllData, WaitMsg) > 0:
            Cnt = Cnt + 1
            if Cnt >= 2:
                if __DEBUG_SEND:
                    Debug.Print('Wait for the Arduino ' + t + ' ms')
                fn_return_value = AllData
                return fn_return_value
        t = t + DelayTime
        if t < Timeout:
            Sleep(DelayTime)
    return fn_return_value

def __Open_Port_with_Error_Msg(PortId, withReset):
    fn_return_value = None
    Status = Long()

    strError = String()
    #----------------------------------------------------------------------
    # Initialize Communications
    Status = CommOpen(PortId, 'baud=115200 parity=N data=8 stop=1 dtr=off')
    Debug.Print('CommOpen(' + PortId + ')')
    if Status != 0:
        # Handle error.
        Status = CommGetError(strError)
        MsgBox(Get_Language_Str('Fehler beim verbinden mit dem Arduino über COM') + PortId + vbCr + '  ' + strError + vbCr + Get_Language_Str('Evtl. ist der Port bereits von einem anderen Programm (Arduino IDE, Farbtest, serieller Monitor) belegt.' + vbCr + 'Falls das Excel Programm vorher mit einer Fehlermeldung abgebrochen wurde, dann kann es sein, ' + 'dass der Port nicht richtig geschlossen wurde. In dem Fall müssen alle Excel Fenster geschlossen werden ;-('), vbCritical, Get_Language_Str('Fehler beim öffnen des COM Ports'))
        Close_Port(PortId)
    else:
        if withReset:
            CommSetLine(PortId, LINE_RTS, True)
            CommSetLine(PortId, LINE_DTR, True)
        fn_return_value = True
    return fn_return_value

def Close_Port(PortId):
    #----------------------------------------
    Sleep(( 100 ) )
    # Reset modem control lines.
    CommSetLine(PortId, LINE_RTS, False)
    CommSetLine(PortId, LINE_DTR, False)
    CommClose(PortId)
    if __DEBUG_SEND:
        Debug.Print('Close_Port(' + PortId + ')')

def __Scale_Bits(Val):
    fn_return_value = None
    #-----------------------------------------------------
    fn_return_value = Val * __Bit_Scale + __Bit_Offset
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Val - ByVal 
def __Write_As_Bits(PortId, Val, LeadStr, TailStr, Waitms):
    fn_return_value = None
    SendDat = Integer()
    #---------------------------------------------------------------------------------------------------------------------------------------
    # Attention: This function must be called with val = -1 at the end to
    # write remaining bits in case WB_BitCnt is not fitting into a byte.
    if Val == - 1:
        if __WB_Remaining == 0:
            return fn_return_value
        __WB_Remaining = __WB_BitCnt
        Debug.Print('Remaining data:')
    else:
        __WB_Buffer = __WB_Buffer + Val * 2 ** __WB_Remaining
        __WB_Remaining = __WB_Remaining + 8
        Debug.Print(Hex02(Val) + ':')
    while __WB_Remaining >= __WB_BitCnt:
        SendDat = __WB_Buffer and __WB_Mask
        if __WB_HighBit:
            SendDat = SendDat + __WB_MarkBit
        Debug.Print(' ', Hex02(SendDat))
        if PortId > 0:
            __Debug_Read_Com(PortId)
            if not Write_Com(PortId, LeadStr + Hex02(__Scale_Bits(SendDat)) + TailStr):
                return fn_return_value
            Sleep(Waitms)
        __WB_HighBit = not __WB_HighBit
        __WB_Remaining = __WB_Remaining - __WB_BitCnt
        __WB_Buffer = SHR(__WB_Buffer, __WB_BitCnt)
    Debug.Print('')
    fn_return_value = True
    return fn_return_value

def Send_LED_PWM(PortId, pwm, LedNr, LEDCnt):
    fn_return_value = None
    Part = Variant()

    LedCntStr = String()

    LeadStr = String()

    TailStr = String()

    LED_PWM = String()
    #--------------------------------------------------------------------------------------------------------
    # Send pwm to all 3 Channels (RGB)
    # 30.01.20: prior only the Green and blue channel was used (Blue LED as status indicator)
    #
    LedCntStr = Hex02(LEDCnt)
    LeadStr = '#L' + Hex02(LedNr)
    LED_PWM = ' ' + Hex02(pwm)
    TailStr = ' ' + LedCntStr + vbLf
    if __DEBUG_SEND:
        Debug.Print('PWM=' + pwm + ' ')
        # Debug
    fn_return_value = Write_Com(PortId, LeadStr + LED_PWM + LED_PWM + LED_PWM + TailStr)
    return fn_return_value

def __Send_LED_Dat(PortId, Val, LedNr, LEDCnt):
    fn_return_value = None
    #---------------------------------------------------------------------------------------------------------
    if __DEBUG_SEND:
        Debug.Print('Dat=' +  ( Val and __WB_Mask )  + ' (')
        if ( Val and __WB_MarkBit )  == __WB_MarkBit:
            Debug.Print('1) ')
        else:
            Debug.Print('0) ')
    fn_return_value = Send_LED_PWM(PortId, Val * 7 + 30, LedNr, LEDCnt)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NextDatFlag - ByRef 
def __Toggle(NextDatFlag):
    #--------------------------------------------
    if NextDatFlag == 0:
        NextDatFlag = __WB_MarkBit
    else:
        NextDatFlag = 0

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NextDatFlag - ByRef 
def __Send_String(PortId, LedNr, LEDCnt, NextDatFlag, Add2CRC, Txt):
    fn_return_value = None
    i = Integer()

    Res = Boolean()
    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    for i in vbForRange(1, Len(Txt)):
        c = Mid(Txt, i, 1)
        if Add2CRC:
            __CRC_ByteList[UBound(__CRC_ByteList)] = Asc(c)
            __CRC_ByteList = vbObjectInitialize((UBound(__CRC_ByteList) + 1,), Variant, __CRC_ByteList)
            # Debug.Print "Add CRC " & Asc(c) ' Debug
        if not __Send_LED_Dat(PortId, ( Asc(c) and __WB_Mask )  + NextDatFlag, LedNr, LEDCnt):
            return fn_return_value
        __Toggle(NextDatFlag)
        Sleep(__WaitTime)
        if not __Send_LED_Dat(PortId, Int(( Asc(c) / __WB_MarkBit )) + NextDatFlag, LedNr, LEDCnt):
            return fn_return_value
        __Toggle(NextDatFlag)
        Sleep(__WaitTime)
    fn_return_value = True
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NextDatFlag - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ByteStr - ByVal 
def __Send_ByteString(PortId, LedNr, LEDCnt, NextDatFlag, AddByteCnt, ByteStr, PercentTxt=VBMissingArgument):
    fn_return_value = None
    bStr = Variant()

    ByteCnt = Integer()

    CRCPos = Integer()

    Total = Long()

    Cnt = Long()
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Percent_Msg_UserForm.Set_Status_Label(PercentTxt + '0 %')
    Percent_Msg_UserForm.Show()
    ByteStr = Trim(ByteStr)
    if Right(ByteStr, 1) == ',':
        ByteStr = DelLast(ByteStr)
    ByteCnt = UBound(Split(ByteStr, ',')) + 1 + 2
    CRCPos = UBound(__CRC_ByteList)
    __CRC_ByteList = vbObjectInitialize((CRCPos + ByteCnt,), Variant, __CRC_ByteList)
    if AddByteCnt:
        ByteStr = Long_to_2ByteStr(ByteCnt) + ', ' + ByteStr
        # Add Number of bytes to the start
    Total = UBound(Split(ByteStr, ',')) + 1
    for bStr in Split(ByteStr, ','):
        B = Val(bStr)
        __CRC_ByteList[CRCPos] = B
        CRCPos = CRCPos + 1
        if __DEBUG_SEND:
            Debug.Print('Add CRC ' + B)
        if not __Send_LED_Dat(PortId, ( B and __WB_Mask )  + NextDatFlag, LedNr, LEDCnt):
            return fn_return_value
        __Toggle(NextDatFlag)
        Sleep(__WaitTime)
        if not __Send_LED_Dat(PortId, Int(( B / __WB_MarkBit )) + NextDatFlag, LedNr, LEDCnt):
            return fn_return_value
        __Toggle(NextDatFlag)
        Cnt = Cnt + 1
        Percent_Msg_UserForm.Set_Status_Label(PercentTxt + Round(100 * Cnt / Total, 0) + ' %')
        Sleep(__WaitTime)
    fn_return_value = True
    Percent_Msg_UserForm.Hide()
    return fn_return_value

def __LA(L1, L2):
    fn_return_value = None
    #------------------------------------
    fn_return_value = Trim(str(L1 * 16 + L2)) + ', '
    return fn_return_value

def __LED_Assignement(L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12):
    fn_return_value = None
    #--------------------------------------------------------------------------------------------
    Check_if_C_Code_Version_is_Set()
    fn_return_value = __CPX_LED_ASSIGNEMENT + ', ' + __LA(L1, L2) + __LA(L3, L4) + __LA(L5, L6) + __LA(L7, L8) + __LA(L9, L10) + __LA(L11, L12) + ' '
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NextDatFlag - ByRef 
def __Send_Pattern_Test(PortId, LedNr, LEDCnt, NextDatFlag, Mode):
    fn_return_value = None
    ByteStr = String()
    #UT------------------------------------------------------------------------------------------------------------------------------------------
    Check_if_C_Code_Version_is_Set()
    select_1 = Left(Mode, 1)
    if (select_1 == 'H'):
        ByteStr = Convert_PatternStr_to_ByteStr('XPatternT11(0,128,SI_LocalVar,4,0,255,0,0,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,32,64,80,160,42,2  ,0,63,128,63,128,63,128,64,0,0,1)')
    elif (select_1 == 'V'):
        ByteStr = Convert_PatternStr_to_ByteStr('XPatternT1(0,32,SI_LocalVar,11,0,128,0,0,300 ms,0,96,0,0,4,5,0,26,0,64,104,0,0,128,64,1,0,0  ,0,127,128,63,128,63,192,63,129,128,63,129,130)')
    elif (select_1 == 'T'):
        ByteStr = Convert_PatternStr_to_ByteStr('PatternT1(0,128,SI_LocalVar,12,0,128,0,0,1 Sek,1,32,0,4,128,0,16,0,2,64,0,8,0,1,32,0,4,192,0,0  ,63,191,191,191,191,191,191,191,191,191,192,1,0)')
    elif (select_1 == 'P'):
        ByteStr = Convert_PatternStr_to_ByteStr('PatternT4(0,0,SI_1,6,0,255,0,PF_NO_SWITCH_OFF,2 Sec,1 Sec,10 Sec,3 Sec,201,194,40,73,22,70)')
    elif (select_1 == 'L'):
        ByteStr = Convert_PatternStr_to_ByteStr('APatternT2(0,4,SI_1,12,0,255,0,0,100 ms,200 ms,3,0,0,3,0,0,12,0,0,12,0,0,48,0,0,48,0,0,192,0,0,192,0,0,0,3,0,0,3,0,0,12,0,0,12,0,0,48,0,0,48,0,0,192,0,0,192,0,0,0,3,0,0,3,0,0,12,0,0,12,0,0,48,0,0,48,0,0,192,0,0,192,0,0,0,0,0,0,0,0,0,0,0,0)')
    elif (select_1 == 'W'):
        ByteStr = Convert_PatternStr_to_ByteStr('APatternT1(0,128,SI_1,2,0,128,0,PM_NORMAL,1 Sek,9)')
    elif (select_1 == 'B'):
        ByteStr = Convert_PatternStr_to_ByteStr('APatternT2(0,4,SI_1,12,0,255,0,0,100 ms,200 ms,3,48,0,3,48,0,12,192,0,12,192,0,48,0,3,48,0,3,192,0,0,192,0,0,0,3,0,0,3,0,0,12,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)')
    else:
        MsgBox('Error: Unknown Mode \'' + Mode + '\' in Send_Pattern_Test()', vbCritical, 'Internal Error')
        return fn_return_value
    if __Enable_Analog_Inputs:
        ByteStr = __CPX_ANALOG_INPUT + ', ' + ByteStr
    else:
        if __Analog_Limmits_Str != '':
            ByteStr = __Analog_Limmits_Str + ByteStr
    __Init_Assignement_Strings()
    if Len(Mode) > 1:
        select_2 = Mid(Mode, 2, 1)
        if (select_2 == 'V'):
            ByteStr = __VIESSMN_LED_ASSIGNEMENT + ByteStr
        elif (select_2 == 'R'):
            ByteStr = __REVERSE_LED_ASSIGNEMENT + ByteStr
        elif (select_2 == 'U'):
            ByteStr = __UNIPROG_LED_ASSIGNEMANT + ByteStr
        elif (select_2 == 'B'):
            ByteStr = __BRIGHT6_LED_ASSIGNEMENT + ByteStr
    #ByteStr = "1, 2, "
    ByteStr = ByteStr + '0'
    fn_return_value = __Send_ByteString(PortId, LedNr, LEDCnt, NextDatFlag, True, ByteStr)
    return fn_return_value

def __Conv_Analog_Limmits_to_ByteStr(Param):
    fn_return_value = None
    Res = String()

    Limmits = vbObjectInitialize(objtype=String)

    Lim = Variant()

    Cnt = Long()
    #-------------------------------------------------------------------------
    Check_if_C_Code_Version_is_Set()
    Res = __CPX_ANALOG_LIMMITS + ', '
    Limmits = Split(Param, ',')
    for Lim in Limmits:
        Cnt = Cnt + 1
        Lim = Trim(Lim)
        if not IsNumeric(Lim):
            MsgBox(Get_Language_Str('Fehler: Ungültige analoge Schwelle \'') + Lim + Get_Language_Str('\' erkannt. '), vbCritical, Get_Language_Str('Ungültige analoge Schwelle'))
            return fn_return_value
        if Cnt <= __ANALOG_KEYS:
            V = Val(Lim)
            Hi = Int(V / 256)
            lo = V % 256
            Res = Res + lo + ', ' + Hi + ', '
    if UBound(Limmits) + 1 > __ANALOG_KEYS:
        MsgBox(Get_Language_Str('Es wurden zu viele analoge Schwellen angegeben. Nur die ersten ') + __ANALOG_KEYS + Get_Language_Str(' werden verwendet'), vbInformation, Get_Language_Str('Zu viele analoge Schwellen'))
    if UBound(Limmits) + 1 < __ANALOG_KEYS:
        #MsgBox "Not enough limmits given. The remaining " & ANALOG_KEYS - Cnt & " limmits are filled with 0", vbInformation
        while Cnt < __ANALOG_KEYS:
            Res = Res + '0, 0, '
            Cnt = Cnt + 1
    fn_return_value = Res
    return fn_return_value

def __Proc_Parameter_Analog_Inputs():
    fn_return_value = None
    Ana_Inp = String()
    #--------------------------------------------------------
    Check_if_C_Code_Version_is_Set()
    Ana_Inp = Trim(Range('Analog_Inputs'))
    if Ana_Inp == '':
        return fn_return_value
    if InStr(Ana_Inp, ',') > 0:
        Res = __Conv_Analog_Limmits_to_ByteStr(Ana_Inp)
        if Res == '':
            fn_return_value = 'ERROR'
            return fn_return_value
        fn_return_value = Res
    else:
        if Val(Ana_Inp) > 0:
            fn_return_value = __CPX_ANALOG_INPUT + ', '
            return fn_return_value
    return fn_return_value

def __Set_Analog_Input(Param):
    #--------------------------------------------
    # Enable the Analog input
    # If Param is empty the global variable Enable_Analog_Inputs is set
    # otherwite the parameter string is parsed for up to 10 limmits
    # which are written to the global variable Analog_Limmits_Str
    if Len(Param) > 0:
        __Analog_Limmits_Str = __Conv_Analog_Limmits_to_ByteStr(Param)
        __Enable_Analog_Inputs = False
    else:
        __Enable_Analog_Inputs = True

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NextDatFlag - ByRef 
def __Send_CRC(PortId, LedNr, LEDCnt, NextDatFlag):
    fn_return_value = None
    #-------------------------------------------------------------------------------------------------------------------
    if UBound(__CRC_ByteList) > 0:
        __CRC_ByteList = vbObjectInitialize((UBound(__CRC_ByteList) - 1,), Variant, __CRC_ByteList)
        CRC = Crc16_ModBus(__CRC_ByteList)
        if __DEBUG_SEND:
            Debug.Print('CRC calculated over all \'Send_String()\' calls except the the header: ' + Hex(CRC))
        fn_return_value = __Send_ByteString(PortId, LedNr, LEDCnt, NextDatFlag, False, Long_to_2ByteStr(CRC), 'CRC ')
    else:
        fn_return_value = True
    return fn_return_value

def Get_Goto_pwm(GotoNr):
    fn_return_value = None
    pwm = Byte()
    #---------------------------------------------------------
    if (GotoNr == 0):
        pwm = 15
    elif (GotoNr == 1):
        pwm = 35
    elif (GotoNr == 2):
        pwm = 55
    elif (GotoNr == 3):
        pwm = 75
    elif (GotoNr == 4):
        pwm = 95
    elif (GotoNr == 5):
        pwm = 115
    elif (GotoNr == 6):
        pwm = 135
    elif (GotoNr == 7):
        pwm = 155
    elif (GotoNr == 8):
        pwm = 175
    elif (GotoNr == 9):
        pwm = 195
    elif (GotoNr == 10):
        pwm = 215
    else:
        MsgBox('Internal Error in Get_Goto_pwm(): Wrong GotoNr: ' + GotoNr, vbCritical, 'Internel Error)')
        pwm = 0
    fn_return_value = pwm
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NrStr - ByVal 
def __Send_Goto(PortId, LedNr, LEDCnt, NrStr):
    fn_return_value = None
    #-------------------------------------------------------------------------------------------------------------------
    fn_return_value = Send_LED_PWM(PortId, Get_Goto_pwm(Val(NrStr)), LedNr, LEDCnt)
    return fn_return_value

def Open_Port_With_Error_Msg_and_get_LastLED(PortId):
    fn_return_value = None
    Cnt = Integer()

    BootMsg = String()

    LastLEDNr = Long()
    #----------------------------------------------------------------------------------
    fn_return_value = - 1
    if not __Open_Port_with_Error_Msg(PortId, False):
        return fn_return_value
    Percent_Msg_UserForm.Set_Status_Label(Get_Language_Str('Öffne Verbindung...'))
    Percent_Msg_UserForm.Show()
    for Cnt in vbForRange(1, 5):
        if not Write_Com(PortId, '#?' + vbLf):
            # VB2PY (UntranslatedCode) GoTo ErrorHand
            # write the question message
            pass
        BootMsg = '***Timeout***'
        BootMsg = __Wait_Until_Arduino_Responds(PortId, __ExpectedResponse, 1000)
        if BootMsg != '***Timeout***' and BootMsg != '':
            break
    if BootMsg == '***Timeout***':
        Percent_Msg_UserForm.Hide()
        MsgBox(Get_Language_Str('Fehler: Der Adruino reagiert nicht'), vbCritical, Get_Language_Str('Fehler beim zugriff auf den Arduino an COM') + PortId)
        GoTo(ErrorHand)
    CommFlush(PortId)
    Debug.Print(BootMsg)
    LastLEDNr = 0
    if BootMsg != '':
        List = Split(BootMsg, ',')
        if UBound(List) >= 1 and InStr(List(0), __ExpectedResponse) >= 0:
            for Idx in vbForRange(1, UBound(List)):
                LastLEDNr = LastLEDNr + Val(List(Idx))
    if LastLEDNr <= 0:
        MsgBox(Get_Language_Str('Fehler: Auf dem Arduino ist nicht das richtige Programm installiert.' + vbCr + 'Der Arduino muss mit dem Excel Programm \'Prog_Generator\' konfiguriert werden.' + 'Dabei muss der \'LED Farbtest Mode\' im \'Config\' Blatt aktiviert sein.' + vbCr + vbCr + 'Meldung von Arduino:') + vbCr + BootMsg, vbCritical, Get_Language_Str('Falsches Programm auf dem Arduino installiert'))
        GoTo(ErrorHand)
    Write_Com()(PortId, '#L 0 0 0 0 FFFF' + vbLf)
    fn_return_value = LastLEDNr
    Percent_Msg_UserForm.Hide()
    return fn_return_value
    Percent_Msg_UserForm.Hide()
    End_Test_and_Close(PortId)
    return fn_return_value

def Test_Send_with_Dialog():
    LedNr = 1

    LEDCnt = 1

    PortId = Integer()

    EndLoop = Boolean()

    NextDatFlag = Byte()
    #UT-------------------------------
    # Zum Test folgende sind folgende Eingaben zu machen:
    #   S = Start des Programmier mode: Die LEDs flackern wild
    #   C = Addressiere das Charliplexing Modul. Wenn diese Sequenz nicht kommt dann wird der Prog mode abgebrochen
    # eine der Pattern Funktionen P, A, L, W
    # dann mit 'E' Beenden.
    __Set_Used_C_Code_Version(2)
    PortId = Get_USB_Port_with_Dialog()
    if PortId <= 0:
        return
    __CRC_ByteList = vbObjectInitialize((0,), Variant)
    if Open_Port_With_Error_Msg_and_get_LastLED(PortId) <= 0:
        return
    Sleep(100)
    __WB_HighBit = False
    while not EndLoop:
        Inp = InputBox('Eingabe der Befehle' + vbCr + '   S: Start' + vbCr + '   C: Charlieplexing Head' + vbCr + '   H: KS_Hauptsignal_Zs3_Zs1' + vbCr + '   VV: Vissmann 4751' + vbCr + '   P: Ampel' + vbCr + '   L: Lauflicht' + vbCr + '   W: Wechselblinker' + vbCr + '   BB: Bright Lauflicht' + vbCr + '   T: Test LED Numbers' + vbCr + 'Optional LED Asssigment tables could be added to the pattern functions:' + vbCr + '   ?R= Reverse, ?V=Viessmann, ?B= Bright ?U=UniProg' + vbCr + '   E: Send CRC and End' + vbCr + '   G<Nr>: Goto' + vbCr + '   A: Analog inputs (Opt with 10 limmits)' + vbCr + 'Spezialbefehle:' + vbCr + '   0..15 Daten' + vbCr + '   N: Toggle NextDatFlag' + vbCr + '   R<Nr>: Raw PWM number' + vbCr + 'NextDatFlag: ' + NextDatFlag, 'LED PWM Send Test')
        Res = True
        select_4 = Left(UCase(Inp), 1)
        if (select_4 == 'S'):
            Res = Send_LED_PWM(PortId, 235, LedNr, LEDCnt)
            NextDatFlag = 0
            __CRC_ByteList = vbObjectInitialize((0,), Variant)
        elif (select_4 == 'E'):
            Res = __Send_CRC(PortId, LedNr, LEDCnt, NextDatFlag)
            Res = Send_LED_PWM(PortId, 255, LedNr, LEDCnt)
        elif (select_4 == 'R'):
            Res = Send_LED_PWM(PortId, Val(Mid(Inp, 2)), LedNr, LEDCnt)
        elif (select_4 == 'N'):
            __Toggle(NextDatFlag)
        elif (select_4 == 'C'):
            Res = __Send_String(PortId, LedNr, LEDCnt, NextDatFlag, False, __CP_HEAD_VERSION)
        elif (select_4 == 'H') or (select_4 == 'V') or (select_4 == 'P') or (select_4 == 'L') or (select_4 == 'W') or (select_4 == 'B') or (select_4 == 'T'):
            Res = __Send_Pattern_Test(PortId, LedNr, LEDCnt, NextDatFlag, UCase(Inp))
        elif (select_4 == ''):
            EndLoop = True
        elif (select_4 == 'G'):
            Res = __Send_Goto(PortId, LedNr, LEDCnt, Mid(Inp, 2))
        elif (select_4 == 'A'):
            __Set_Analog_Input(Mid(Inp, 2))
        else:
            if Val(Inp) >= 0 and Val(Inp) <= 15:
                Res = __Send_LED_Dat(PortId, Val(Inp) + NextDatFlag, LedNr, LEDCnt)
                __Toggle(NextDatFlag)
            else:
                MsgBox('Wrong Input:' + vbCr + '  \'' + Inp + '\'', vbCritical, 'Test_Send_with_Dialog')
        if not Res:
            MsgBox('Error sending the data', vbCritical, 'Test_Send_with_Dialog')
    End_Test_and_Close(PortId)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ByteStr - ByRef 
def __Convert_Numerical_LED_Assignement(LED_Assignement, ByteStr):
    fn_return_value = None
    List = vbObjectInitialize(objtype=String)

    NrStr = Variant()

    Nr = Long()

    Nibbel = Integer()

    L0 = Integer()
    #----------------------------------------------------------------------------------------------------------------
    Check_if_C_Code_Version_is_Set()
    List = Split(LED_Assignement(), ',')
    if UBound(List) != 11:
        MsgBox(Get_Language_Str('Fehler: Die Anzahl Einträge (') + UBound(List) + 1 + Get_Language_Str(') in der LED Zuordnungsliste ist falsch. ' + 'Es müssen genau 12 per Komma getrennte Zahlen angegeben werden. ' + vbCr + 'Jede Zahl beschreibt die LED Nummer welche von der entsprechenden Zeile ' + 'der Mustertabelle angesprochen werden soll. Die erste Zahl steht ' + 'dabei für die erste Zeile, ...'), vbCritical, Get_Language_Str('Falsche Anzahl in \'Charliplexing LED Zuordnung\''))
        return fn_return_value
    ByteStr = ByteStr + __CPX_LED_ASSIGNEMENT + ', '
    for NrStr in List:
        NrStr = Trim(NrStr)
        Nr = Val(NrStr)
        if not IsNumeric(NrStr) or Nr < 0 or Nr > 11:
            MsgBox(Get_Language_Str('Fehler: Der Eintrag \'') + NrStr + Get_Language_Str('\' in der LED Zuordnungstabele ist keine gültige Zahl.' + vbCr + 'Es sind nur Zahlen zwischen 0 und 11 erlaubt.'), vbCritical, Get_Language_Str('Ungültiger Eintrag in \'Charliplexing LED Zuordnung\''))
            return fn_return_value
        if (Nibbel == 0):
            Nibbel = 1
            L0 = Nr
        elif (Nibbel == 1):
            Nibbel = 0
            ByteStr = ByteStr + __LA(L0, Nr)
    fn_return_value = True
    return fn_return_value

def __Test_Convert_Numerical_LED_Assignement():
    ByteStr = String()
    #UT-------------------------------------------------
    Debug.Print('Res= ' + __Convert_Numerical_LED_Assignement('0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11', ByteStr))
    Debug.Print('ByteStr = \'' + ByteStr + '\'')

def __Find_LED_Assignement(Name):
    fn_return_value = None
    Row = Long()

    Col = Long()

    EmptyCnt = Long()

    Numbers = String()

    NL = vbObjectInitialize(objtype=String)
    #--------------------------------------------------------------
    with_0 = Sheets(SPECIAL_MODEDLG_SH)
    with_1 = with_0.Range('LED_Assignm_Head')
    Row = with_1.Row + 1
    Col = with_1.Column
    while 1:
        select_6 = Trim(with_0.Cells(Row, Col))
        if (select_6 == Name):
            Numbers = with_0.Cells(Row, with_0.Range('LED_Assignement_Head').Column)
            NL = Split(Replace(Numbers, ' ', ''), ',')
            if UBound(NL) != 11:
                with_0.Cells(Row, with_0.Range('LED_Assignement_Head').Column).Select()
                MsgBox(Get_Language_Str('Fehler: Die LED Zuordnung in Sheet \'') + with_0.Name +  ( '\' Zeile ' )  + Row + Get_Language_Str(' enthält nicht genau 12 Werte'), vbCritical, Get_Language_Str('Interner Fehler'))
                return fn_return_value
            fn_return_value = __LED_Assignement(NL(0), NL(1), NL(2), NL(3), NL(4), NL(5), NL(6), NL(7), NL(8), NL(9), NL(10), NL(11))
            return fn_return_value
        elif (select_6 == ''):
            EmptyCnt = EmptyCnt + 1
            if EmptyCnt > 2:
                return fn_return_value
        Row = Row + 1
        if not (True):
            break
    return fn_return_value

def __Test_Find_LED_Assignement():
    #UT------------------------------------
    Debug.Print(__Find_LED_Assignement('Reverse'))

def Send_to_ATTiny(PortId, LedNr, LED_Assignement, Analog_Inputs):
    LEDCnt = 1

    Special_Mode = String()

    MaxTimes = Long()

    UsedTimes = Long()

    LastLEDNr = Long()

    NextDatFlag = Byte()

    ByteStr = String()

    Res = String()
    #--------------------------------------------------------------------------------------------------------------
    # PortId ' Ex. 1, 2, 3, 4 ... 50 for COM1 - COM4... COM50
    Special_Mode = ThisWorkbook.ActiveSheet.Range('Special_Mode')
    if Special_Mode == 'Charlieplexing':
        if not Select_Special_Mode():
            return
    select_7 = ThisWorkbook.ActiveSheet.Range('Special_Mode')
    if (select_7 == 'Charlieplexing V2'):
        __Set_Used_C_Code_Version(2)
        MaxTimes = 64
    elif (select_7 == 'Charlieplexing V1'):
        __Set_Used_C_Code_Version(1)
        MaxTimes = 23
    else:
        MsgBox(Get_Language_Str('Error: Invalid Charlieplexing mode entered'), vbCritical, 'Invalid Charlieplexing mode detected')
        ThisWorkbook.ActiveSheet.Range('Special_Mode').Select()
    UsedTimes = Val(Mid(Range('Start'), InStr(Range('Start'), 'PatternT') + Len('PatternT')))
    if UsedTimes > MaxTimes:
        MsgBox(Replace(Replace(Get_Language_Str('Fehler: Zu viele Zeiten in der \'Dauer\' Zeile verwendet. ' + 'Es sind maximal #1# Zeiten bei Version \'#2#\' möglich'), '#1#', MaxTimes), '#2#', Range('Special_Mode')), vbCritical, Get_Language_Str('Fehler: Zu viele Zeiten benutzt'))
        return
    if Range('FlashUsage') >= 500:
        MsgBox(Get_Language_Str('Fehler: Der EEPROM Speicher des ATTinys ist zu klein für diese riesige Konfiguration ;-(' + vbCr + 'Tip: \'Bits pro Wert\' oder die Anzahl der Zeiten verringern'), vbCritical, Get_Language_Str('Konfiguration passt nicht in EEPROM'))
        return
    if Range('Kanaele') > 12:
        MsgBox(Get_Language_Str('Fehler: Es können maximal 12 LEDs mit dem Charlieplexing Modul angesteuert werden'), vbCritical, Get_Language_Str('Fehler: Zu viele LED Kanäle benutzt'))
        return
    if Check_Table_before_Copy(False) == False:
        return
    LastLEDNr = Open_Port_With_Error_Msg_and_get_LastLED(PortId)
    if LastLEDNr <= 0:
        # VB2PY (UntranslatedCode) GoTo ErrorHand
        pass
    if LedNr < 0 or LedNr >= LastLEDNr:
        MsgBox(Get_Language_Str('Fehler: Falsche RGB LED Modul Nummer: ') + LedNr + '.' + vbCr + Get_Language_Str('Die Modul Nummer muss zwischen 0 und ') + LastLEDNr - 1 + Get_Language_Str(' liegen.' + vbCr + vbCr + 'Die maximal mögliche Modul Nummer wird von der auf dem Arduino installierten Konfiguration ' + 'bestimmt. Es können nur so viele LEDs angesprochen werden wie im \'Prog_Generator\' angegeben ' + 'wurden. Wenn sich das Modul an einer noch nicht eingetragenen Position befindet, dann ' + 'kann der Befehl \'Reserve LEDs\' im \'Prog_Generator\' benutzt werden damit zusätzliche ' + 'LEDs angesprochen werden können.'), vbCritical, Get_Language_Str('RGB LED Nummer des Moduls ist falsch'))
        GoTo(ErrorHand)
    __WB_HighBit = False
    __Init_Assignement_Strings()
    if not Send_LED_PWM(PortId, 235, LedNr, LEDCnt):
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        # Sent Start
        pass
    __CRC_ByteList = vbObjectInitialize((0,), Variant)
    Sleep(__WaitTime_Start)
    Percent_Msg_UserForm.Set_Status_Label(Get_Language_Str('Sende Kennung...'))
    if not __Send_String(PortId, LedNr, LEDCnt, NextDatFlag, False, __CP_HEAD_VERSION):
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        pass
    LED_Assignement() = Trim(LED_Assignement())
    if LED_Assignement() != '':
        if IsNumeric(Left(LED_Assignement(), 1)):
            if __Convert_Numerical_LED_Assignement(LED_Assignement(), ByteStr) == False:
                # VB2PY (UntranslatedCode) GoTo ErrorHand
                pass
        else:
            ByteStr = __Find_LED_Assignement(LED_Assignement())
            if ByteStr == '':
                MsgBox(Get_Language_Str('Fehler: Die LED Zuordnung \'') + LED_Assignement() + Get_Language_Str('\' ist unbekannt'), vbCritical, Get_Language_Str('Unbekannte LED Zuordnung'))
                GoTo(ErrorHand)
    Res = __Proc_Parameter_Analog_Inputs()
    if Res == 'ERROR':
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        pass
    ByteStr = ByteStr + Res
    ByteStr = ByteStr + Convert_PatternStr_to_ByteStr(Range(ErgebnisRng))
    ByteStr = ByteStr + '0'
    if not __Send_ByteString(PortId, LedNr, LEDCnt, NextDatFlag, True, ByteStr):
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        # Send the data to the ATTiny
        pass
    if not __Send_CRC(PortId, LedNr, LEDCnt, NextDatFlag):
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        # Send the CRC
        pass
    if not Send_LED_PWM(PortId, 255, LedNr, LEDCnt):
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        pass
    if Goto_Mode_is_Active():
        Test_GotoNr_Form.Show_Dialog(PortId, LedNr)
    Percent_Msg_UserForm.Hide()
    End_Test_and_Close(PortId)
    return
    Percent_Msg_UserForm.Hide()
    End_Test_and_Close(PortId)
    MsgBox(Get_Language_Str('Fehler bei der Datenübertragung zum ATTiny'), vbCritical, Get_Language_Str('Datenübertragungsfehler'))
    Percent_Msg_UserForm.Hide()

def LED_Assignement_Dialog():
    Res = String()
    #----------------------------------
    Res = Select_from_Sheet_Form.Show_Form(SPECIAL_MODEDLG_SH, Get_Language_Str('LED Zuordnung definieren'), Get_Language_Str('Auswahl der LED Zuordnung'), Get_Language_Str('Die Zuordnung der Charlieplexing LEDs ist von Hersteller zu Hersteller unterschiedlich. Mit diesem Dialog kann die passende Zuordnung der Muster Zeilen zu den LEDs gewählt werden.'), oDialog_Dat_ROW1= Sheets(SPECIAL_MODEDLG_SH).Range('LED_Assignm_Head').Row + 1, oLowerWin_COL= 3)
    if Res != '':
        Range['CPX_LED_Assignement'] = Split(Res, ',')(0)

def Open_Port_and_Show_Test_GotoNr_Form(PortId):
    LastLEDNr = Long()

    LedNr = Byte()
    #----------------------------------------------------------------
    LastLEDNr = Open_Port_With_Error_Msg_and_get_LastLED(PortId)
    if LastLEDNr <= 0:
        return
    LedNr = Range('RGB_Modul_Nr')
    Test_GotoNr_Form.Show_Dialog(PortId, LedNr)
    End_Test_and_Close(PortId)

def End_Test_and_Close(PortId):
    #-------------------------------
    # VB2PY (UntranslatedCode) On Error Resume Next
    Write_Com()(PortId, '#L 0 0 0 0 32767' + vbLf)
    Sleep(( 100 ))
    Write_Com()(PortId, '#X' + vbLf)
    Close_Port(PortId)
    # VB2PY (UntranslatedCode) On Error GoTo 0

def Send_to_ATTiny_Main():
    Ctrl_Pressed = Boolean()

    PortId = Integer()
    #-------------------------------
    # Is called if the "Zum Modul schicken" Button is pressed
    Ctrl_Pressed = GetAsyncKeyState(VK_CONTROL) != 0
    PortId = Get_USB_Port_with_Dialog()
    if PortId > 0:
        if Range('RGB_Modul_Nr') == '':
            Get_LED_Address_Dialog()
            if Range('RGB_Modul_Nr') == '':
                return
        if Ctrl_Pressed:
            Open_Port_and_Show_Test_GotoNr_Form(PortId)
        else:
            Send_to_ATTiny(PortId, Range('RGB_Modul_Nr'), Range('CPX_LED_ASSIGNEMENT'), Range('Analog_Inputs'))

# VB2PY (UntranslatedCode) Option Explicit
