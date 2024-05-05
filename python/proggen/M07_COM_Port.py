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
import serial.tools.list_ports as portlist
import logging
import serial

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *


#import proggen.M02_Public as M02
#import ExcelAPI.X02_Workbook as P01
#import proggen.M08_ARDUINO as M08
#import proggen.M09_Language as M09
#import proggen.M25_Columns as M25
#import proggen.M30_Tools as M30
#import mlpyproggen.U01_userform as U01

import proggen.M02_Public as M02
import proggen.M02a_Public as M02a
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header as M06
import proggen.M07_COM_Port_New as M07New
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
#import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
#import proggen.M27_Sheet_Icons as M27
#import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Multiplexer as M80

#import proggen.D08_Select_COM_Port_Userform as D08

import ExcelAPI.XLA_Application as P01
import  proggen.F00_mainbuttons as F00

import mlpyproggen.Prog_Generator as PG


class DCB:
    def __init__(self):
        self.DCBlength = int()
        self.BaudRate = int()
        self.fBitFields = int()
        self.wReserved = Integer()
        self.XonLim = Integer()
        self.XoffLim = Integer()
        self.ByteSize = Byte()
        self.Parity = Byte()
        self.StopBits = Byte()
        self.XonChar = Byte()
        self.XoffChar = Byte()
        self.ErrorChar = Byte()
        self.EofChar = Byte()
        self.EvtChar = Byte()
        self.wReserved1 = Integer()

class COMMCONFIG:
    def __init__(self):
        self.dwSize = int()
        self.wVersion = Integer()
        self.wReserved = Integer()
        self.dcbx = DCB()
        self.dwProviderSubType = int()
        self.dwProviderOffset = int()
        self.dwProviderSize = int()
        self.wcProviderData = Byte()

class COMMTIMEOUTS:
    def __init__(self):
        self.ReadIntervalTimeout = int()
        self.ReadTotalTimeoutMultiplier = int()
        self.ReadTotalTimeoutConstant = int()
        self.WriteTotalTimeoutMultiplier = int()
        self.WriteTotalTimeoutConstant = int()

__ERROR_IO_INCOMPLETE = 996
__ERROR_IO_PENDING = 997
__GENERIC_READ = 0x80000000
__GENERIC_WRITE = 0x40000000
__FILE_ATTRIBUTE_NORMAL = 0x80
__FILE_FLAG_OVERLAPPED = 0x40000000
__FORMAT_MESSAGE_FROM_SYSTEM = 0x1000
__OPEN_EXISTING = 3
__COM_SETXOFF = 1
__COM_SETXON = 2
__COM_SETRTS = 3
__COM_CLRRTS = 4
__COM_SETDTR = 5
__COM_CLRDTR = 6
__COM_SETBREAK = 8
__COM_CLRBREAK = 9
__MS_CTS_ON = 0x10
__MS_DSR_ON = 0x20
__MS_RING_ON = 0x40
__MS_RLSD_ON = 0x80
__PURGE_RXABORT = 0x2
__PURGE_RXCLEAR = 0x8
__PURGE_TXABORT = 0x1
__PURGE_TXCLEAR = 0x4
__Resp_STK_OK = 0x10
__Resp_STK_FAILED = 0x11
__Resp_STK_INSYNC = 0x14
__Sync_CRC_EOP = 0x20
__Cmnd_STK_GET_PARAMETER = 0x41
__Cmnd_STK_GET_SYNC = 0x30
__STK_READ_SIGN = 0x75
__Parm_STK_HW_VER = 0x80
__Parm_STK_SW_MAJOR = 0x81
__Parm_STK_SW_MINOR = 0x82

Resp_STK_OK = b'\x10'
Resp_STK_FAILED = b'\x11'
Resp_STK_INSYNC = b'\x14'
Sync_CRC_EOP = b'\x20'
Cmnd_STK_GET_PARAMETER = b'\x41'
Cmnd_STK_GET_SYNC = b'\x30'
STK_READ_SIGN = b'\x75'
Parm_STK_HW_VER = b'\x80'
Parm_STK_SW_MAJOR = b'\x81'
Parm_STK_SW_MINOR = b'\x82'

CheckCOMPort_Txt = ""
CheckCOMPort = " "#0

def __Test_Get_COM():
    Res = String()

    Line = Variant()
    #-------------------------
    Res = F_shellExec('cmd /c mode')
    for Line in Split(Res, vbCr):
        Debug.Print(Line)

def __Get_USB_Ports():
    fn_return_value = None
    Res = String()

    Lines = Variant()

    Line = Variant()

    p = int()

    ResStr = String()

    Cnt = int()

    ResSplit = Variant()

    ResArray = vbObjectInitialize(objtype=Long)

    i = int()
    #------------------------------------------
    # The function returns an long array with COM numbers
    # COM-10 is allways added because otherwise the array may be empty if no other com port is detected
    # The "find" function dosen't work on Norberts computer => Therefore it's replaced by an own find algo
    Res = M30.F_shellExec('cmd /c mode')
    # Achtung: Der Mode Befehl schickt einen Reset zu allen Ports
    if Res == '':
        # No COM port available ?
        P01.MsgBox(M09.Get_Language_Str('Fehler: Das Abfragen der COM Ports ist fehlgeschlagen ;-('), vbCritical, M09.Get_Language_Str('Fehler beim abfragen der COM Ports'))
        M30.EndProg()
    Res = Replace(Res, ':', '')
    ResStr = '-10 '
    for Line in Split(Res, vbCr):
        p = InStr(Line, 'COM')
        if p > 0:
            ResStr = ResStr + Trim(Mid(Line, p + Len('COM'), 255)) + ' '
            Cnt = Cnt + 1
    ResStr = M30.DelLast(ResStr)
    ResSplit = Split(ResStr, ' ')
    ResArray = vbObjectInitialize((Cnt,), Variant)
    for i in vbForRange(0, Cnt):
        ResArray[i] = P01.val(ResSplit(i))
    fn_return_value = ResArray
    return fn_return_value

def Detect_Com_Port_and_Save_Result(Right):
    ComPortColumn = int()

    BuildOptColumn = int()

    Pic_ID = String()

    Port = int()
    #-----------------------------------------------------------
    if Right:
        ComPortColumn = M25.COMPrtR_COL
        Pic_ID = 'DCC'
        BuildOptColumn = M25.BUILDOpRCOL
    else:
        ComPortColumn = M25.COMPort_COL
        Pic_ID = 'LED'
        BuildOptColumn = M25.BUILDOP_COL
    Port = M07New.Detect_Com_Port(Right, Pic_ID)
    #if Port > 0:
    if F00.port_is_available(Port):    
        P01.CellDict[M02.SH_VARS_ROW, ComPortColumn] = Port
        PG.global_controller.setConfigData("serportname",Port)
        F00.StatusMsg_UserForm.Set_Label(M09.Get_Language_Str('Überprüfe den Arduino Typ'))
        # 30.10.20:
        F00.StatusMsg_UserForm.Show()
        
        BuildOptions = ""
        DeviceSignature = 0        
        Fn_res, BuildOptions, DeviceSignature = M08.Check_If_Arduino_could_be_programmed_and_set_Board_type(ComPortColumn, BuildOptColumn, BuildOptions, DeviceSignature) #*HL Buildoption and devicesignature are return values
        P01.Unload(F00.StatusMsg_UserForm)

def __TestDetect_Com_Port():
    #UT------------------------------
    M07New.Detect_Com_Port(False, 'LED')

def ComPortPage():
    fn_return_value = None
    # 30.12.19:
    #-----------------------------------------
    if M02.ComPortfromOnePage != '':
        fn_return_value = PG.ThisWorkbook.Sheets(M02.ComPortfromOnePage)
    else:
        fn_return_value = P01.ActiveSheet
    return fn_return_value

def Check_USB_Port_with_Dialog(ComPortColumn):
    fn_return_value = False
    #---------------------------------------------------------------------------
    #if P01.val(ComPortPage().Cells(M02.SH_VARS_ROW, ComPortColumn)) <= 0:
    if not F00.port_is_available(ComPortPage().Cells(M02.SH_VARS_ROW, ComPortColumn)):
        fn_return_value = M07New.USB_Port_Dialog(ComPortColumn)
        # 04.05.20: Prior Check_USB_Port_with_Dialog ends the program in case of an error
    else:
        fn_return_value = True
    return fn_return_value

def __Test_Check_USB_Port_with_Dialog():
    # 30.12.19:
    #UT------------------------------------------
    M25.Make_sure_that_Col_Variables_match()
    Debug.Print(Check_USB_Port_with_Dialog(M25.COMPort_COL))
    # Left Arduino
    #Debug.Print Check_USB_Port_with_Dialog(COMPrtR_COL)   ' Right Arduino
    # Right Arduino
    #Debug.Print Check_USB_Port_with_Dialog(COMPrtT_COL)   ' Tiny_Uniprog
    # Tiny_Uniprog

def Get_USB_Port_with_Dialog(right=VBMissingArgument):
    _fn_return_value = False
    ComPortColumn = Long()
    # 30.12.19:
    #-----------------------------------------------------------------------------
    if Right:
        ComPortColumn = M25.COMPrtR_COL
    else:
        ComPortColumn = M25.COMPort_COL
    with_0 = ComPortPage().Cells(M02.SH_VARS_ROW, ComPortColumn)
    if not F00.port_is_available(with_0.Value):
    #*HL if P01.val(with_0.Value) <= 0:
        if M07New.USB_Port_Dialog(ComPortColumn) == False:
            fn_return_value = - 1
            return fn_return_value
    #fn_return_value = P01.val(with_0.Value)
    fn_return_value = with_0.Value
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Port - ByVal 
def InitComPort(Port, Settings):
    #-------------------------------------------------------------
    if NativeInitComPort(Port, Settings, 100):
        return
    # if previous method failed use command shell and mode command to set serial options
    F_shellRun('cmd /c mode com' + Port + ' ' + Settings, 0, True)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Port - ByVal 
def NativeInitComPort(Port, Settings, readTimeout):
    fn_return_value = None
    DCB = DCB()

    Result = Variant()

    handle = int()
    #------------------------------------------------------------------------------------------------
    handle = 0
    Result = 0
    # VB2PY (UntranslatedCode) On Error GoTo NativeError
    handle = CreateFile('\\\\.\\COM' + Port, 0, 0, 0, __OPEN_EXISTING, __FILE_ATTRIBUTE_NORMAL, 0)
    if handle > 0:
        Result = BuildCommDCB(Settings, DCB)
        if Result == 1:
            Result = SetCommState(handle, DCB)
        if Result == 1:
            if GetCommTimeouts(handle, cts) == 1:
                cts.ReadIntervalTimeout = readTimeout
                cts.ReadTotalTimeoutConstant = readTimeout
                cts.ReadTotalTimeoutMultiplier = 0
                SetCommTimeouts(handle, cts)
                fn_return_value = True
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if handle > 0:
        CloseHandle(( handle ))
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ResNames - ByRef 
def EnumComPorts_old(Show_Unknown, ResNames, PrintDebug=True):
    fn_return_value = None
    Ports = vbObjectInitialize((50,), Byte)

    NumberOfPorts = Byte()

    Names = vbObjectInitialize((50,), String)

    CountOnly = Boolean()

    objItem = Variant()

    ESP_Inst = Boolean()

    PICO_Inst = Boolean()

    Result = vbObjectInitialize(objtype=Byte)
    #------------------------------------------------------------------------------------------------------------------------------
    # Generate a list of COM ports which have
    # "CH340" or "Arduino" in there name
    # Doesn't check if the COM Port is used by an other program
    CountOnly = True
    NumberOfPorts = 0
    ESP_Inst = ( M02a.Get_BoardTyp() == 'ESP32' )
    PICO_Inst = ( M02a.Get_BoardTyp() == 'PICO' )
    for objItem in GetObject('winmgmts:\\\\.\\root\\CIMV2').ExecQuery('SELECT * FROM Win32_PnPEntity WHERE ClassGuid="{4d36e978-e325-11ce-bfc1-08002be10318}"', VBGetMissingArgument(GetObject.ExecQuery, 1), 48):
        if Show_Unknown or ( ESP_Inst == False and PICO_Inst == False and  (InStr(objItem.Caption, 'CH340') > 0 or InStr(objItem.Caption, 'Arduino') > 0 or InStr(objItem.Caption, 'USB Serial Port') > 0 ) ) or ( ESP_Inst == True and InStr(objItem.Caption, 'Silicon Labs CP210x') > 0 )  or  ( PICO_Inst == True and InStr(objItem.Path_.Path, 'USB\\\\VID_2E8A&PID_000A\\') > 0 ):
            # 10.11.20: Added: "Silicon Labs CP210x" for the ESP32  02.05.20: Added: "USB Serial Port" for original Nano (Frank)
            # 21.04.21: Added: "Silicon Labs CP210x" for the PICO
            if PrintDebug:
                Debug.Print(objItem.Caption)
            idx1 = InStr(objItem.Caption, '(COM')
            if idx1 > 0:
                idx2 = InStr(idx1 + 3, objItem.Caption, ')')
                if idx2 > 0:
                    portNumber = P01.val(Mid(objItem.Caption, idx1 + 4, idx2 - idx1 - 4))
                    Ports[NumberOfPorts] = portNumber
                    Names[NumberOfPorts] = objItem.Caption
                    NumberOfPorts = NumberOfPorts + 1
                    if NumberOfPorts >= UBound(Ports):
                        break
        else:
            Debug.Print('Other device (Not added to result): ' + objItem.Caption)
            # Example: "Silicon Labs CP210x USB to UART Bridge (COM10)"
    if NumberOfPorts > 0:
        Result = vbObjectInitialize((NumberOfPorts - 1,), Variant)
        ResNames = vbObjectInitialize((NumberOfPorts - 1,), Variant)
        for idx1 in vbForRange(0, NumberOfPorts - 1):
            Result[idx1] = Ports(idx1)
        M30.Array_BubbleSort(Result)
        # Sort the Ports
        # find the matching names
        for idx1 in vbForRange(0, NumberOfPorts - 1):
            for idx2 in vbForRange(0, NumberOfPorts - 1):
                if Result(idx1) == Ports(idx2):
                    ResNames[idx1] = Names(idx2)
                    break
        fn_return_value = Result
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ResNames - ByRef 
def EnumComPorts(Show_Unknown, ResNames, PrintDebug=True):
    Ports = vbObjectInitialize((50,), Byte)
    ESP_Inst = ( M02a.Get_BoardTyp() == 'ESP32' )
    PICO_Inst = ( M02a.Get_BoardTyp() == 'PICO' )

    temp_comports_list = portlist.comports(include_links=False)
    
    Debug.Print("EnumComPorts:"+repr(temp_comports_list))

    NumberOfPorts = len(temp_comports_list)
    Ports = [] #vbObjectInitialize((NumberOfPorts - 1,), Variant)
    ResNames = [] #vbObjectInitialize((NumberOfPorts - 1,), Variant)    
    idx=0
    for comport in temp_comports_list:
        Debug.Print("EnumComPorts:"+repr(comport.description)+" "+repr(comport.device))
        # if Show_Unknown or ( ESP_Inst == False and PICO_Inst == False and  (InStr(comport.description, 'CH340') > 0 or InStr(comport.description, 'Arduino') > 0 or InStr(comport.description, 'USB Serial Port') > 0 or InStr(comport.description, 'USB2.0-Ser') > 0  or InStr(comport.description, 'tty') > 0 ) ) or ( ESP_Inst == True and InStr(comport.description, 'Silicon Labs CP210x') > 0 )  or  ( PICO_Inst == True and InStr(comport.description, 'USB\\\\VID_2E8A&PID_000A\\') > 0 ):
        if Show_Unknown or ( ESP_Inst == False and PICO_Inst == False and  (InStr(comport.description, 'CH340') > 0 or InStr(comport.description, 'Arduino') > 0 or InStr(comport.description, 'USB Serial Port') > 0 or InStr(comport.description, 'USB2.0-Ser') > 0  or InStr(comport.description, 'tty') > 0 ) ) or ( InStr(comport.description, 'Silicon Labs CP210x') > 0 )  or  ( PICO_Inst == True and InStr(comport.description, 'USB\\\\VID_2E8A&PID_000A\\') > 0 ):
            Ports.append(comport.device)
            ResNames.append(comport.description)
            idx=idx+1

    fn_return_value = Ports
    return fn_return_value, ResNames

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PortNr - ByVal 
def Check_If_Port_is_Available(PortNr):
    Debug.Print("Check_If_Port_is_Available:"+PortNr)
    fn_return_value = None
    Ports = vbObjectInitialize(objtype=Byte)

    ResNames = vbObjectInitialize(objtype=String)
    #--------------------------------------------------------------------------
    Ports, ResNames = EnumComPorts(False, ResNames)
    fn_return_value = M30.Is_Contained_in_Array(PortNr, Ports)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PortNr - ByVal 
def Check_If_Port_is_Available_And_Get_Name(PortNr):
    Debug.Print("Check_If_Port_is_Available_And_Get_Name:"+PortNr)
    fn_return_value = ""
    Ports = vbObjectInitialize(objtype=Byte)

    ResNames = vbObjectInitialize(objtype=String)

    Res = int()
    #--------------------------------------------------------------------------------------
    Ports,ResNames = EnumComPorts(False, ResNames)
    Res = M30.Get_Position_In_Array(PortNr, Ports)
    if Res >= 0:
        fn_return_value = ResNames[Res]
    return fn_return_value

def __Test_Check_If_Port_is_Available():
    #UT------------------------------------------
    Debug.Print(Check_If_Port_is_Available(3))

def __TestDetect():
    Ports = vbObjectInitialize(objtype=Byte)

    Start = Variant()

    SWMajorVersion = Byte()

    SWMinorVersion = Byte()

    HWVersion = Byte()

    DeviceSignatur = int()

    BaudRate = int()

    i = Integer()

    ComPort = Variant()

    ComPorts = vbObjectInitialize(objtype=Byte)

    Names = vbObjectInitialize(objtype=String)

    Ub = int()
    #UT---------------------
    Start = Time
    ComPorts, Names = EnumComPorts(False, Names)
    # VB2PY (UntranslatedCode) On Error GoTo IsEmpty
    Ub = UBound(ComPorts)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    for ComPort in ComPorts:
        for i in vbForRange(1, 2):
            if i == 1:
                BaudRate = 57600
            else:
                BaudRate = 115200
            Debug.Print('Trying COM' + ComPort + ' with Baudrate ' + BaudRate)
            select_0, DeviceSignatur = DetectArduino(ComPort, BaudRate, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur)
            if (select_0 == 1):
                Debug.Print('  Serial Port     : COM' + ComPort)
                Debug.Print('  Serial Baudrate : ' + BaudRate)
                Debug.Print('  Hardware Version: ' + HWVersion)
                Debug.Print('  Firmware Version: ' + SWMajorVersion + '.' + SWMinorVersion)
                Debug.Print('  Device signature: ')
                if DeviceSignatur == 2004239:
                    Debug.Print('ATMega328 ')
                if DeviceSignatur == 0x1E9651:
                    Debug.Print('ATMega4809 ')
                    # 28.10.20: Jürgen
                Debug.Print('0x' + Right('00000' + Hex(DeviceSignatur), 6) + vbCr)
                break
            elif (select_0 == 0):
                pass
            else:
                break
    Debug.Print('End')
    Debug.Print('Check duration: ' + Format(Time - Start, 'hh:mm:ss'))
    return
    P01.MsgBox('No Arduino detected')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DeviceSignatur - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: FirmwareVer - ByRef 
def Get_Arduino_Baudrate(ComPort, Start_Baudrate, DeviceSignatur, FirmwareVer, DebugPrint=False):
    fn_return_value = 0
    SWMajorVersion = Byte()

    SWMinorVersion = Byte()

    HWVersion = Byte()

    BaudRate = int()

    i = Integer()

    Res = int()

    SleepTime = int()
    # 28.10.20: Jürgen: Added: DeviceSignatur  30.10.20: Added: FirmwareVer
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Return  >0: Baudrate 57600/115200
    #          0: if no arduino is detected
    #         -1: can't open com port => used by an other program ?
    #         -2: can't create com port file
    #         -3: can't reset arduino
    if (Start_Baudrate == 1):
        BaudRate = 115200
    elif (Start_Baudrate == 2):
        BaudRate = 57600
    else:
        BaudRate = Start_Baudrate
    if BaudRate != 115200 and BaudRate != 57600:
        BaudRate = 115200
    SleepTime = 20
    for i in vbForRange(1, 8):
        # In case of an error we check each baudrate 4 times because sometimes the Baudrate is not detected if started with the wrong Baudrate   13.10.20: old:  For i = 1 To 6
        if DebugPrint:
            Debug.Print('Trying COM' + str(ComPort) + ' with Baudrate ' + str(BaudRate))
        if 0:
            # Faster
            # 30.10.20: Old: 1 (Seemes to be not much slower)
            Res, DeviceSignatur = DetectArduino(ComPort, BaudRate, DeviceSignatur= DeviceSignatur, SleepTime= SleepTime)
        else:
            Res, DeviceSignatur = DetectArduino(ComPort, BaudRate, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur= DeviceSignatur, SleepTime= SleepTime)
        if (Res == 1):
            # Detected an arduino
            if DebugPrint:
                Debug.Print('  Serial Port     : COM' + str(ComPort))
                Debug.Print('  Serial Baudrate : ' + str(BaudRate))
                Debug.Print('  Hardware Version: ' + str(HWVersion))
                Debug.Print('  Firmware Version: ' + str(SWMajorVersion) + '.' + str(SWMinorVersion))
                Debug.Print('  Device signature: ')
                if DeviceSignatur == 2004239:
                    Debug.Print('ATMega328 ')
                if DeviceSignatur == 0x1E9651:
                    Debug.Print('ATMega4809 ')
                    # 28.10.20: Jürgen
                Debug.Print('0x' + Right('00000' + Hex(DeviceSignatur), 6) + vbCr)
            FirmwareVer = str(SWMajorVersion) + '.' + str(SWMinorVersion)
            fn_return_value = BaudRate
            break
        elif (Res == 0):
            pass
        else:
            fn_return_value = Res
            break
        if BaudRate == 115200:
            BaudRate = 57600
        else:
            BaudRate = 115200
            # Check again with the other baud rate
        if i == 4:
            SleepTime = 150
    return fn_return_value

def __Test_Get_Arduino_Baudrate():
    Start = Variant()

    DeviceSignatur = int()

    FirmwareVer = String()
    #UT------------------------------------
    Start = Time
    #Debug.Print "Get_Arduino_Baudrate=" & Get_Arduino_Baudrate(6, 115200, DeviceSignatur, FirmwareVer, True)
    Debug.Print('Get_Arduino_Baudrate=' + Get_Arduino_Baudrate(6, 57600, DeviceSignatur, FirmwareVer, True))
    #Debug.Print "Get_Arduino_Baudrate=" & Get_Arduino_Baudrate(8, 115200, DeviceSignatur, FirmwareVer, True)  ' Matching Baudrate 3 Sec, Not matching 6 Sek
    Debug.Print('Check duration: ' + Format(Time - Start, 'hh:mm:ss'))
    
def getdeviceinformation():
    logging.debug("getdeviceinformation")
    DeviceSignatur = b''
    HWVersion = b''
    SWMajorVersion  = b''
    SWMinorVersion  = b''
    Data = __transact(STK_READ_SIGN, 5)
    if len(Data)==5:
        if Data[4].to_bytes(1,byteorder="little") == Resp_STK_OK:
            DeviceSignatur = Data[1:4]
            #logging.debug("getdeviceinformation: %s",str(DeviceSignatur))
            if DeviceSignatur == b'\x1E\x95\x0F':
                logging.info("ATMEGA328P")
            else:
                logging.info("Device Signatur: %s",str(DeviceSignatur))
    return False, DeviceSignatur
    
def DetectArduino(port,baudrate, HWVersion=255, SWMajorVersion=255, SWMinorVersion=255, DeviceSignatur=- 1, Trials=3, PrintDebug=True, SleepTime=20):
    global Cmnd_STK_GET_SYNC, CheckCOMPort_Txt
    # protocol see application note 1AVR061 here http://ww1.microchip.com/downloads/en/Appnotes/doc2525.pdf
    # Result:  1: O.K
    #          0: Give up after n trials => if no arduino is detected
    #         -1: can't open com port
    #         -2: can't close and assign port
    #         -3: can't reset arduino
    fn_return_value=0
    
    No_of_trials = Trials
    logging.debug ("M07.detect_arduino: %s",port)
    no_port=None
    try: # close the port if it is open and reopen it with DTR = False
        if PG.global_controller.arduino and PG.global_controller.arduino.is_open:
            PG.global_controller.arduino.close()
        # hack for Mac
        if P01.checkplatform("Darwin"):
            logging.debug("Hack for Mac: Set baudrate to 19200")
            baudrate=19200

        PG.global_controller.arduino = serial.Serial(no_port,baudrate=baudrate,timeout=0.2,write_timeout=1,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
        logging.info("Serial-params: " + repr(PG.global_controller.arduino))
    except BaseException as e:
        logging.debug(e, exc_info=True) 
        logging.debug("M07.detect_arduino: Error assigning port")
        return -2, None
    if type(port)==int:
        port_str="COM"+str(port)
    else:
        port_str = port
    PG.global_controller.arduino.port = port_str
    PG.global_controller.arduino.dtr = False
    try:
        PG.global_controller.arduino.open()
    except BaseException as e:
        logging.debug("M07.detect_arduino: Error opening  port "+port_str)
        logging.debug(e, exc_info=True) 
        return -1, None           
    try:
        PG.global_controller.arduino.dtr = True
        time.sleep(0.250)
        PG.global_controller.arduino.dtr = False
    except BaseException as e:
        logging.debug(e, exc_info=True)                 
        logging.debug("M07.detect_arduino: Error, reset ARDUINO")
        return -3, None

    # now get in sync
    message = Cmnd_STK_GET_SYNC
    
    fn_return_value = 0
    
    if not(Left(CheckCOMPort_Txt, 18) == 'Arduino NANO Every'):
        fn_return_value = 1
        DeviceSignatur = 2004561
        HWVersion = 1
        SWMajorVersion = 1
        SWMinorVersion = 7
        if baudrate == 115200:
            fn_return_value = 1
        else:
            fn_return_value = 0
    else:
        for i in range (No_of_trials):
            message = __transact(Cmnd_STK_GET_SYNC,2)
            
            if message == Resp_STK_INSYNC + Resp_STK_OK:
                DeviceSignatur = b''
                HWVersion = b''
                SWMajorVersion  = b''
                SWMinorVersion  = b''            
                res,devicesignatur = getdeviceinformation()
                if res==True:
                    fn_return_value=1
                    PG.global_controller.arduino.close()
                    return fn_return_value, devicesignatur
        if fn_return_value != 1:
            logging.debug("Give up after %s trials",No_of_trials)
    return fn_return_value, None

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Port - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: BaudRate - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: HWVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMajorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMinorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DeviceSignatur=- 1 - ByRef 
def DetectArduino_old(Port, BaudRate, HWVersion=255, SWMajorVersion=255, SWMinorVersion=255, DeviceSignatur=- 1, Trials=3, PrintDebug=True, SleepTime=20):
    fn_return_value = None
    handle = int()

    i = Integer()

    Result = Boolean()
    #---------------------------------------------------------------------------
    # protocol see application note 1AVR061 here http://ww1.microchip.com/downloads/en/Appnotes/doc2525.pdf
    # Result:  1: O.K
    #          0: Give up after n trials => if no arduino is detected
    #         -1: can't open com port
    #         -2: can't create com port file
    #         -3: can't reset arduino
    
    return 1 #*HL

    handle = 0
    fn_return_value = 0
    if PrintDebug:
        Debug.Print('SleepTime=' + str(SleepTime))
    if not NativeInitComPort(Port, 'BAUD=' + BaudRate + ' PARITY=N DATA=8 STOP=1 dtr=off', 500):
        if PrintDebug:
            Debug.Print('can\'t open com port')
        fn_return_value = - 1
        return fn_return_value
    # VB2PY (UntranslatedCode) On Error GoTo NativeError
    handle = CreateFile('\\\\.\\COM' + str(Port), __GENERIC_READ or __GENERIC_WRITE, 0, 0, __OPEN_EXISTING, __FILE_ATTRIBUTE_NORMAL, 0)
    if handle <= 0:
        if PrintDebug:
            Debug.Print('can\'t create com port file')
        fn_return_value = - 2
        return fn_return_value
    #if PrintDebug then Debug.Print "reset arduino"
    Result = EscapeCommFunction(handle, __COM_SETDTR)
    if Result:
        DoEvents()
        Sleep(( SleepTime )      )
        # Bei einem meiner Arduinos funktioniert die Erkennung nicht zuverlässig mit 10 ms.    13.10.20:
        # Mit 150ms geht es gut. Aber nur dann wenn die Konfiguration groß ist
        # (Mainboard Test: "MB Test 1 DCC" 66 LEDs)
        # Bei einer kleinen Konfiguration mit nur 2 LEDs geht es aber nicht mit 150 ms.
        # Dann müssen 20 ms verwendet werden
        # => Ich habe eine umschaltung der Wartetzeit in Get_Arduino_Baudrate() eingebaut.
        #    Jetzt werden jeweils zwei versoche mit jeder Baudrate mit 20 ms gemacht und
        #    danach 2 mit 150 ms.
        #    Damit scheint es zu Funktionieren. Getestet mit 2 verschiedenen Arduinos.
        #    Zwei mit neuem BL und einer mit altem BL.
        #  - Zusätzlich habe ic "Trials" von 5 auf 3 reduziert weil ich beobachtet habe,
        #    dass der Arduino entweder beim ersten oder zweiten Versuch erkannt wird
        #    oder gar nicht erkannt wird.
        Result = EscapeCommFunction(handle, __COM_CLRDTR)
    if Result == False:
        if PrintDebug:
            Debug.Print('can\'t reset arduino')
            # I never get this message ?
        CloseHandle(( handle ))
        fn_return_value = - 3
        return fn_return_value
    DoEvents()
    if Left(CheckCOMPort_Txt, 18) == 'Arduino NANO Every':
        fn_return_value = 1
        DeviceSignatur = 2004561
        HWVersion = 1
        SWMajorVersion = 1
        SWMinorVersion = 7
        if BaudRate == 115200:
            fn_return_value = 1
        else:
            fn_return_value = 0
    else:
        for i in vbForRange(1, Trials):
            message = __Transact(handle, Chr(__Cmnd_STK_GET_SYNC), 2)
            if UBound(message) == 1:
                if message(0) == __Resp_STK_INSYNC and message(1) == __Resp_STK_OK:
                    #if PrintDebug then Debug.Print "in sync with arduino"
                    if __GetDeviceInformation(handle, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur):
                        fn_return_value = 1
                        if PrintDebug:
                            Debug.Print('Detected after ' + i + ' trials')
                        break
                    #Exit For                                                           ' 13.10.20: Old position
    if DetectArduino() != 1:
        if PrintDebug:
            Debug.Print('Give up after ' + Trials + ' trials')
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if handle > 0:
        CloseHandle(( handle ))
    return fn_return_value

def __transact(bytemessage,nNumberOfBytesToRead=10):
    
    bytemessage += Sync_CRC_EOP
    # write message to serport
    nbytes_written = PG.global_controller.arduino.write(bytemessage)
    if nbytes_written != len(bytemessage):
        logging.debug("ERROR write to ARDUINO")
        return b''
    no_of_trials=10
    for i in range (no_of_trials):
        # read from serport nNumberOfBytesToRead
        read_data = PG.global_controller.arduino.read(size=nNumberOfBytesToRead)
        #logging.debug("transact: %s",read_data)
        if (read_data[:1] == Resp_STK_INSYNC and read_data[-1:] == Resp_STK_OK) or read_data[-1:] == Resp_STK_FAILED:
        # return response
            #logging.debug("transact data_ok: %s",read_data)
            return read_data
    return b''

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: handle - ByVal 
def __Transact_old(handle, message, nNumberOfBytesToRead=10):
    fn_return_value = None
    CbWritten = Variant()

    CbRead = Variant()

    ToSend = Variant()

    j = int()

    Buffer = vbObjectInitialize(objtype=Byte)

    Response = vbObjectInitialize(((0, 9),), Byte)

    EmptyResp = vbObjectInitialize((0,), Byte)

    Rc = int()
    #-----------------------------------------------------------------------------------------------------------------------
    message = message + Chr(__Sync_CRC_EOP)
    ToSend = Len(message)
    Buffer = vbObjectInitialize((ToSend,), Variant)
    for j in vbForRange(0, ToSend - 1):
        Buffer[j] = Asc(Mid(message, j + 1, 1))
    #Debug.Print "nNumberOfBytesToRead = 10"
    #nNumberOfBytesToRead = 10
    PurgeComm(handle, __PURGE_TXABORT or __PURGE_RXABORT or __PURGE_TXCLEAR or __PURGE_RXCLEAR)
    if WriteFile(handle, Buffer(0), ToSend, CbWritten, 0) == 0:
        return fn_return_value
    if CbWritten != ToSend:
        return fn_return_value
    fn_return_value = EmptyResp
    while 1:
        Rc = ReadFile(handle, Response(0), nNumberOfBytesToRead, CbRead, 0)
        if Rc == 0 or CbRead < 1:
            return fn_return_value
        DoEvents()
        if Response(0) == __Resp_STK_INSYNC and Response(CbRead - 1) == __Resp_STK_OK or Response(CbRead - 1) == __Resp_STK_FAILED:
            resp = vbObjectInitialize(((0, CbRead - 1),), Variant)
            for j in vbForRange(0, CbRead - 1):
                resp[j] = Response(j)
            fn_return_value = resp
            return fn_return_value
        #Debug.Print "invalid packet"
        return fn_return_value
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: handle - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: HWVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMajorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMinorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DeviceSignatur=- 1 - ByRef 
def __GetDeviceInformation(handle, HWVersion=255, SWMajorVersion=255, SWMinorVersion=255, DeviceSignatur=- 1):
    fn_return_value = None
    data = vbObjectInitialize(objtype=Byte)

    Tmp = int()
    #--------------------------------------------------------------------------------------------------------------------
    # Added option to speed up by not requesting all values                     ' 04.05.20:
    # 1 sec instead of 3 if only the DeviceSignatur is requested
    # Attention: At least one value has to be requested
    fn_return_value = False
    if DeviceSignatur != - 1:
        data = __Transact(handle, Chr(__STK_READ_SIGN), 5)
        if UBound(data) != 4:
            return fn_return_value
        if data(4) != __Resp_STK_OK:
            return fn_return_value
        Tmp = data(1)
        DeviceSignatur = Tmp * 65536
        Tmp = data(2)
        DeviceSignatur = DeviceSignatur + Tmp * 256
        Tmp = data(3)
        DeviceSignatur = DeviceSignatur + Tmp
    if HWVersion != 255:
        data = __Transact(handle, Chr(__Cmnd_STK_GET_PARAMETER) + Chr(__Parm_STK_HW_VER), 3)
        if UBound(data) != 2:
            return fn_return_value
        if data(2) != __Resp_STK_OK:
            return fn_return_value
        HWVersion = data(1)
    if SWMinorVersion != 255:
        data = __Transact(handle, Chr(__Cmnd_STK_GET_PARAMETER) + Chr(__Parm_STK_SW_MAJOR), 3)
        if UBound(data) != 2:
            return fn_return_value
        if data(2) != __Resp_STK_OK:
            return fn_return_value
        SWMajorVersion = data(1)
    if SWMinorVersion != 255:
        data = __Transact(handle, Chr(__Cmnd_STK_GET_PARAMETER) + Chr(__Parm_STK_SW_MINOR), 3)
        if UBound(data) != 2:
            return fn_return_value
        if data(2) != __Resp_STK_OK:
            return fn_return_value
        SWMinorVersion = data(1)
    fn_return_value = True
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort - ByVal 
def SendMLLCommand(ComPort, message, UseHardwareHandshake, ShowResult):
    fn_return_value = False
    handle = int()

    CbWritten = Variant()

    CbRead = int()

    t = Variant()

    Repeat = Integer()

    by = Byte()

    Msg = String()
    # VB2PY (UntranslatedCode) On Error GoTo serialError
    if UseHardwareHandshake:
        InitComPort(ComPort, 'BAUD=115200 PARITY=N DATA=8 STOP=1 dtr=off octs=on')
    else:
        if M02a.Get_BoardTyp() != 'PICO':
            InitComPort(ComPort, 'BAUD=115200 PARITY=N DATA=8 STOP=1 dtr=off octs=off')
        else:
            InitComPort(ComPort, 'BAUD=115200 PARITY=N DATA=8 STOP=1 dtr=on octs=off')
    UseHardwareHandshake = M30.Get_Current_Platform_Bool('UseHardwareHandshake')
    handle = CreateFile('\\\\.\\COM' + ComPort, __GENERIC_READ or __GENERIC_WRITE, 0, 0, __OPEN_EXISTING, __FILE_ATTRIBUTE_NORMAL, 0)
    if handle < 0:
        Err.Raise(1, VBGetMissingArgument(Err.Raise, 1), '')
    if M02a.Get_BoardTyp() == 'PICO':
        EscapeCommFunction(handle, __COM_SETDTR)
    if UseHardwareHandshake:
        Repeat = 1
    else:
        Repeat = 2
        # 03.04.20: Old: to 10
    if DEBUG_DCCSEND:
        Debug.Print(Format(Time, 'hh.mm.ss') + ' sending ' + Repeat + ' times to receiver: \'' + message + '\'')
        # Debug
    # The interrupts in the Arduino are locked while the LEDs are updatet
    # => To avoid loosing bits maximal one byte could be send over the RS232 while the interrupts are locked
    # The delay is calculated by:
    # 0.9 + 0.35us + 0.3 us = 1.55us / Bit
    # 24 Bit / LED
    # Resttime > 50 us
    # 256 LEDs => Delay 10 ms
    # Send duration 11 * 10 ms = 110 ms
    while Repeat > 0:
        Repeat = Repeat - 1
        for t in vbForRange(1, Len(message)):
            by = Asc(Mid(message, t, 1))
            WriteFile(handle, by, 1, CbWritten, 0)
            if UseHardwareHandshake == False:
                Sleep(10)()
                # 03.04.20: Added delay
    # write response(s) to the debug output
    if 1 & ShowResult:
        while 1:
            by = 0
            if ReadFile(handle, by, 1, CbRead, 0):
                Msg = Msg + Chr(by)
            if not (by > 0):
                break
        if Len(Msg) > 0:
            Debug.Print(Format(Time, 'hh.mm.ss') + ' Response from Arduino:       \'' + Replace(Msg, vbLf, '\\n') + '\'')
    #Close #1
    if handle > 0:
        CloseHandle(( handle ))
    fn_return_value = True
    return fn_return_value
    if handle > 0:
        CloseHandle(( handle ))
    Msg = Err.Description
    if DEBUG_DCCSEND:
        Debug.Print(Format(Time, 'hh.mm.ss') + ' send to receiver failed with ' + Msg)
    MsgBox(Get_Language_Str('Fehler beim senden an die serielle Schnittstelle COM') + ComPort + ':' + vbCr + '  \'' + Get_Language_Str(Msg) + '\'' + vbCr + Get_Language_Str('Eventuell ist der serielle Monitor noch offen'), vbCritical, Get_Language_Str('Fehler: Decoder senden fehlgeschlagen'))
    # VB2PY (UntranslatedCode) On Error GoTo 0
    fn_return_value = False
    return fn_return_value

