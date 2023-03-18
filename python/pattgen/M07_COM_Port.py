from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M30_Tools as M30
import pattgen.M09_Language
import ExcelAPI.XLW_Workbook as X02
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M07_COM_Port_New
import ExcelAPI.XLWA_WinAPI as X03
import serial.tools.list_ports as portlist
import pattgen.Pattern_Generator as PG

""" Revision History:
 ~~~~~~~~~~~~~~~~~
 30.12.19: - Copied from Prog_Generator
           - Added function ComPortPage() to be able to store the com port in one page for all sheets
 31.12.19: - Improved the Get_USB_Ports() function because the "find" function didn't work on Norberts compuer for some reasons
 27.03.20: - method InitComPort to be able to init the serial communication parameter
 31.03.20: - method InitComPort: also set com timeouts
           - support com ports > COM9
 07.04.20: - Jürgen added functions to detect the connected Arduinos
 04.05.20: - Speed up from 3 sec to 1 sec by
             - Requesting only the Device Signatur
             - Reducing the number of requested bytes in Transact()

# VB2PY (CheckDirective) VB directive took path 1 on VBA7
For 64 Bit Systems
-------------------------------------------------------------------------------
 System Constants
-------------------------------------------------------------------------------
 COMM Functions
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
For 64 Bit Systems

 Creates or opens a communications resource and returns a handle
 that can be used to access the resource.


 Closes an open communications device or file handle.

-------------------------
------------------------------------------
-----------------------------------------------------------
UT------------------------------
-----------------------------------------
---------------------------------------------------------------------------
UT------------------------------------------
-----------------------------------------------------------------------------
-------------------------------------------------------------
------------------------------------------------------------------------------------------------
********************** 07.04.20: New block from Jürgen ***************************
------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------
UT------------------------------------------
UT---------------------
--------------------------------------------------------------------------------------------------------------------------
UT------------------------------------
---------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------
"""

class DCB:
    def __init__(self):
        self.DCBlength = Long()
        self.Baudrate = Long()
        self.fBitFields = Long()
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
        self.dwSize = Long()
        self.wVersion = Integer()
        self.wReserved = Integer()
        self.dcbx = DCB()
        self.dwProviderSubType = Long()
        self.dwProviderOffset = Long()
        self.dwProviderSize = Long()
        self.wcProviderData = Byte()

class COMMTIMEOUTS:
    def __init__(self):
        self.ReadIntervalTimeout = Long()
        self.ReadTotalTimeoutMultiplier = Long()
        self.ReadTotalTimeoutConstant = Long()
        self.WriteTotalTimeoutMultiplier = Long()
        self.WriteTotalTimeoutConstant = Long()

ERROR_IO_INCOMPLETE = 996
ERROR_IO_PENDING = 997
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_ATTRIBUTE_NORMAL = 0x80
FILE_FLAG_OVERLAPPED = 0x40000000
FORMAT_MESSAGE_FROM_SYSTEM = 0x1000
OPEN_EXISTING = 3
COM_SETXOFF = 1
COM_SETXON = 2
COM_SETRTS = 3
COM_CLRRTS = 4
COM_SETDTR = 5
COM_CLRDTR = 6
COM_SETBREAK = 8
COM_CLRBREAK = 9
MS_CTS_ON = 0x10
MS_DSR_ON = 0x20
MS_RING_ON = 0x40
MS_RLSD_ON = 0x80
PURGE_RXABORT = 0x2
PURGE_RXCLEAR = 0x8
PURGE_TXABORT = 0x1
PURGE_TXCLEAR = 0x4
Resp_STK_OK = 0x10
Resp_STK_FAILED = 0x11
Resp_STK_INSYNC = 0x14
Sync_CRC_EOP = 0x20
Cmnd_STK_GET_PARAMETER = 0x41
Cmnd_STK_GET_SYNC = 0x30
STK_READ_SIGN = 0x75
Parm_STK_HW_VER = 0x80
Parm_STK_SW_MAJOR = 0x81
Parm_STK_SW_MINOR = 0x82

CheckCOMPort_Txt = ""
CheckCOMPort = ""

def Test_Get_COM():
    Res = String()

    Line = Variant()
    #-------------------------
    Res = M30.F_shellExec('cmd /c mode')
    for Line in Split(Res, vbCr):
        Debug.Print(Line)

def Get_USB_Ports():
    _fn_return_value = None
    Res = String()

    Lines = Variant()

    Line = Variant()

    p = Long()

    ResStr = String()

    Cnt = Long()

    ResSplit = Variant()

    ResArray = vbObjectInitialize(objtype=Long)

    i = Long()
    #------------------------------------------
    # The function returns an long array with COM numbers
    # COM-10 is allways added because otherwise the array may be empty if no other com port is detected
    # The "find" function dosen't work on Norberts computer => Therefore it's replaced by an own find algo
    Res = M30.F_shellExec('cmd /c mode')
    # Achtung: Der Mode Befehl schickt einen Reset zu allen Ports
    if Res == '':
        # No COM port available ?
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Das Abfragen der COM Ports ist fehlgeschlagen ;-('), vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler beim abfragen der COM Ports'))
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
        ResArray[i] = Val(ResSplit(i))
    _fn_return_value = ResArray
    return _fn_return_value

def Detect_Com_Port_and_Save_Result(Right):
    ComPortColumn = Long()

    Pic_ID = String()

    Port = Long()
    #-----------------------------------------------------------
    if Right:
        ComPortColumn = M01.COMPrtR_COL
        Pic_ID = 'DCC'
    else:
        ComPortColumn = M01.COMPort_COL
        Pic_ID = 'LED'
    Port = pattgen.M07_COM_Port_New.Detect_Com_Port(Right, Pic_ID)
    if Port > 0:
        X02.CellDict[M01.SH_VARS_ROW, ComPortColumn] = Port

def TestDetect_Com_Port():
    #UT------------------------------
    pattgen.M07_COM_Port_New.Detect_Com_Port(False, 'LED')

def ComPortPage():
    _fn_return_value = None
    # 30.12.19:
    #-----------------------------------------
    if M01.ComPortfromOnePage != '':
        _fn_return_value = PG.ThisWorkbook.Sheets(M01.ComPortfromOnePage)
    else:
        _fn_return_value = X02.ActiveSheet
    return _fn_return_value

def Check_USB_Port_with_Dialog(ComPortColumn):
    _fn_return_value = None
    #---------------------------------------------------------------------------
    if Val(ComPortPage().Cells(M01.SH_VARS_ROW, ComPortColumn)) <= 0:
        _fn_return_value = pattgen.M07_COM_Port_New.USB_Port_Dialog(ComPortColumn)
        # 04.05.20: Prior Check_USB_Port_with_Dialog ends the program in case of an error
    else:
        _fn_return_value = True
    return _fn_return_value

def Test_Check_USB_Port_with_Dialog():
    # 30.12.19:
    #UT------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
    pass

def Get_USB_Port_with_Dialog(Right=VBMissingArgument):
    _fn_return_value = None
    ComPortColumn = Long()
    # 30.12.19:
    #-----------------------------------------------------------------------------
    if Right:
        ComPortColumn = M01.COMPrtR_COL
    else:
        ComPortColumn = M01.COMPort_COL
    _with69 = ComPortPage().Cells(M01.SH_VARS_ROW, ComPortColumn)
    if Val(_with69.Value) <= 0:
        if pattgen.M07_COM_Port_New.USB_Port_Dialog(ComPortColumn) == False:
            _fn_return_value = - 1
            return _fn_return_value
    _fn_return_value = Val(_with69.Value)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Port - ByVal 
def InitComPort(Port, Settings):
    #-------------------------------------------------------------
    if NativeInitComPort(Port, Settings, 100):
        return
    # if previous method failed use command shell and mode command to set serial options
    M30.F_shellRun('cmd /c mode com' + Port + ' ' + Settings, 0, True)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Port - ByVal 
def NativeInitComPort(Port, Settings, readTimeout):
    _fn_return_value = None
    DCB = DCB()

    Result = Variant()

    Handle = Long()
    #------------------------------------------------------------------------------------------------
    Handle = 0
    Result = 0
    # VB2PY (UntranslatedCode) On Error GoTo NativeError
    Handle = X03.CreateFile('\\\\.\\COM' + Port, 0, 0, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0)
    if Handle > 0:
        Result = X03.BuildCommDCB(Settings, DCB)
        if Result == 1:
            Result = X03.SetCommState(Handle, DCB)
        if Result == 1:
            if X03.GetCommTimeouts(Handle, cts) == 1:
                cts.ReadIntervalTimeout = readTimeout
                cts.ReadTotalTimeoutConstant = readTimeout
                cts.ReadTotalTimeoutMultiplier = 0
                X03.SetCommTimeouts(Handle, cts)
                _fn_return_value = True
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if Handle > 0:
        X03.CloseHandle(( Handle ))
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ResNames - ByRef 
def EnumComPorts(Show_Unknown, ResNames, PrintDebug=True):
    Ports = vbObjectInitialize((50,), Byte)
    ESP_Inst = False #( M02a.Get_BoardTyp() == 'ESP32' )
    PICO_Inst = False #( M02a.Get_BoardTyp() == 'PICO' )

    temp_comports_list = portlist.comports(include_links=False)
    
    Debug.Print("EnumComPorts:"+repr(temp_comports_list))

    NumberOfPorts = len(temp_comports_list)
    Ports = [] #vbObjectInitialize((NumberOfPorts - 1,), Variant)
    ResNames = [] #vbObjectInitialize((NumberOfPorts - 1,), Variant)    
    idx=0
    for comport in temp_comports_list:
        Debug.Print("EnumComPorts:"+repr(comport.description)+" "+repr(comport.device))
        if Show_Unknown or ( ESP_Inst == False and PICO_Inst == False and  (InStr(comport.description, 'CH340') > 0 or InStr(comport.description, 'Arduino') > 0 or InStr(comport.description, 'USB Serial Port') > 0 or InStr(comport.description, 'USB2.0-Ser') > 0  or InStr(comport.description, 'tty') > 0 ) ) or ( ESP_Inst == True and InStr(comport.description, 'Silicon Labs CP210x') > 0 )  or  ( PICO_Inst == True and InStr(comport.description, 'USB\\\\VID_2E8A&PID_000A\\') > 0 ):
            Ports.append(comport.device)
            ResNames.append(comport.description)
            idx=idx+1

    fn_return_value = Ports
    return fn_return_value, ResNames

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ResNames - ByRef 
def EnumComPorts_old(Show_Unknown, ResNames, PrintDebug=True):
    _fn_return_value = None
    Ports = vbObjectInitialize((50,), Byte)

    NumberOfPorts = Byte()

    Names = vbObjectInitialize((50,), String)

    CountOnly = Boolean()

    objItem = Variant()

    Result = vbObjectInitialize(objtype=Byte)
    #------------------------------------------------------------------------------------------------------------------------------
    # Generate a list of COM ports which have
    # "CH340" or "Arduino" in there name
    # Doesn't check if the COM Port is used by an other program
    CountOnly = True
    NumberOfPorts = 0
    for objItem in GetObject('winmgmts:\\\\.\\root\\CIMV2').ExecQuery('SELECT * FROM Win32_PnPEntity WHERE ClassGuid="{4d36e978-e325-11ce-bfc1-08002be10318}"', VBGetMissingArgument(GetObject.ExecQuery, 1), 48):
        if Show_Unknown or InStr(objItem.Caption, 'CH340') > 0 or InStr(objItem.Caption, 'Arduino') > 0 or InStr(objItem.Caption, 'USB Serial Port') > 0 or InStr(objItem.Caption, 'Silicon Labs CP210x') > 0:
            # 09.04.21: Juergen Added ESP32
            if PrintDebug:
                Debug.Print(objItem.Caption)
            idx1 = InStr(objItem.Caption, '(COM')
            if idx1 > 0:
                idx2 = InStr(idx1 + 3, objItem.Caption, ')')
                if idx2 > 0:
                    portNumber = Val(Mid(objItem.Caption, idx1 + 4, idx2 - idx1 - 4))
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
        _fn_return_value = Result
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PortNr - ByVal 
def Check_If_Port_is_Available(PortNr):
    _fn_return_value = None
    Ports = vbObjectInitialize(objtype=Byte)

    ResNames = vbObjectInitialize(objtype=String)
    #--------------------------------------------------------------------------
    Ports = EnumComPorts(False, ResNames)
    _fn_return_value = M30.Is_Contained_in_Array(PortNr, Ports)
    return _fn_return_value

def Test_Check_If_Port_is_Available():
    #UT------------------------------------------
    Debug.Print(Check_If_Port_is_Available(8))

def TestDetect():
    Ports = vbObjectInitialize(objtype=Byte)

    Start = Variant()

    SWMajorVersion = Byte()

    SWMinorVersion = Byte()

    HWVersion = Byte()

    DeviceSignatur = Long()

    Baudrate = Long()

    i = Integer()

    ComPort = Variant()

    ComPorts = vbObjectInitialize(objtype=Byte)

    Names = vbObjectInitialize(objtype=String)

    Ub = Long()
    #UT---------------------
    Start = X02.Time
    ComPorts = EnumComPorts(False, Names)
    # VB2PY (UntranslatedCode) On Error GoTo IsEmpty
    Ub = UBound(ComPorts)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    for ComPort in ComPorts:
        for i in vbForRange(1, 2):
            if i == 1:
                Baudrate = 57600
            else:
                Baudrate = 115200
            Debug.Print('Trying COM' + ComPort + ' with Baudrate ' + Baudrate)
            _select52 = DetectArduino(ComPort, Baudrate, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur)
            if (_select52 == 1):
                Debug.Print('  Serial Port     : COM' + ComPort)
                Debug.Print('  Serial Baudrate : ' + Baudrate)
                Debug.Print('  Hardware Version: ' + HWVersion)
                Debug.Print('  Firmware Version: ' + SWMajorVersion + '.' + SWMinorVersion)
                Debug.Print('  Device signature: ')
                if DeviceSignatur == 2004239:
                    Debug.Print('ATMega328 ')
                Debug.Print('0x' + Right('00000' + Hex(DeviceSignatur), 6) + vbCr)
                break
            elif (_select52 == 0):
                # Retry with other baud rate
                pass
            else:
                break
    Debug.Print('End')
    Debug.Print('Check duaration: ' + X02.Format(X02.Time - Start, 'hh:mm:ss'))
    return
    X02.MsgBox('No Arduino detected')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort - ByVal 
def Get_Arduino_Baudrate(ComPort, Start_Baudrate, DebugPrint=VBMissingArgument):
    _fn_return_value = None
    SWMajorVersion = Byte()

    SWMinorVersion = Byte()

    HWVersion = Byte()

    DeviceSignatur = Long()

    Baudrate = Long()

    i = Integer()

    Res = Long()
    #--------------------------------------------------------------------------------------------------------------------------
    # Return  >0: Baudrate 57600/115200
    #          0: if no arduino is detected
    #         -1: can't open com port => used by an other program ?
    #         -2: can't create com port file
    #         -3: can't reset arduino
    _select53 = Start_Baudrate
    if (_select53 == 1):
        Baudrate = 115200
    elif (_select53 == 2):
        Baudrate = 57600
    else:
        Baudrate = Start_Baudrate
    if Baudrate != 115200 and Baudrate != 57600:
        Baudrate = 115200
    for i in vbForRange(1, 6):
        # In case of an error we check each baudrate 3 times because sometimes the Baudrate is not detected if started with the wrong Baudrate
        if DebugPrint:
            Debug.Print('Trying COM' + ComPort + ' with Baudrate ' + Baudrate)
        if 1:
            # Faster
            Res = DetectArduino(ComPort, Baudrate, DeviceSignatur= DeviceSignatur)
        else:
            Res = DetectArduino(ComPort, Baudrate, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur= DeviceSignatur)
        _select54 = Res
        if (_select54 == 1):
            # Detected an arduino
            if DebugPrint:
                Debug.Print('  Serial Port     : COM' + ComPort)
                Debug.Print('  Serial Baudrate : ' + Baudrate)
                Debug.Print('  Hardware Version: ' + HWVersion)
                Debug.Print('  Firmware Version: ' + SWMajorVersion + '.' + SWMinorVersion)
                Debug.Print('  Device signature: ')
                if DeviceSignatur == 2004239:
                    Debug.Print('ATMega328 ')
                Debug.Print('0x' + Right('00000' + Hex(DeviceSignatur), 6) + vbCr)
            _fn_return_value = Baudrate
            break
        elif (_select54 == 0):
            # Retry with other baud rate
            pass
        else:
            _fn_return_value = Res
            break
        if Baudrate == 115200:
            Baudrate = 57600
        else:
            Baudrate = 115200
        # Check again with the other baud rate
    return _fn_return_value

def Test_Get_Arduino_Baudrate():
    Start = Variant()
    #UT------------------------------------
    Start = X02.Time
    #Debug.Print "Get_Arduino_Baudrate=" & Get_Arduino_Baudrate(6, 115200, True)
    #Debug.Print "Get_Arduino_Baudrate=" & Get_Arduino_Baudrate(11, 57600, True)
    # Matching Baudrate 3 Sec, Not matching 6 Sek
    Debug.Print('Get_Arduino_Baudrate=' + Get_Arduino_Baudrate(3, 115200, True))
    # Matching Baudrate 3 Sec, Not matching 6 Sek
    Debug.Print('Check duaration: ' + X02.Format(X02.Time - Start, 'hh:mm:ss'))

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
        logging.debug(e)
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
        logging.debug(e)       
        return -1, None           
    try:
        PG.global_controller.arduino.dtr = True
        time.sleep(0.250)
        PG.global_controller.arduino.dtr = False
    except BaseException as e:
        logging.debug(e)                 
        logging.debug("Error, reset ARDUINO")
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
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Baudrate - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: HWVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMajorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMinorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DeviceSignatur=- 1 - ByRef 
def DetectArduino_old (Port, Baudrate, HWVersion=255, SWMajorVersion=255, SWMinorVersion=255, DeviceSignatur=- 1, Trials=5, PrintDebug=True):
    _fn_return_value = None
    Handle = Long()

    i = Integer()

    Result = Boolean()

    message = vbObjectInitialize(objtype=Byte)
    #---------------------------------------------------------------------------
    # protocol see application note 1AVR061 here http://ww1.microchip.com/downloads/en/Appnotes/doc2525.pdf
    # Result:  1: O.K
    #          0: Give up after n trials => if no arduino is detected
    #         -1: can't open com port
    #         -2: can't create com port file
    #         -3: can't reset arduino
    Handle = 0
    _fn_return_value = 0
    if not NativeInitComPort(Port, 'BAUD=' + str(Baudrate) + ' PARITY=N DATA=8 STOP=1 dtr=off', 500):
        if PrintDebug:
            Debug.Print('can\'t open com port')
        _fn_return_value = - 1
        return _fn_return_value
    # VB2PY (UntranslatedCode) On Error GoTo NativeError
    Handle = X03.CreateFile('\\\\.\\COM' + Port, GENERIC_READ or GENERIC_WRITE, 0, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0)
    if Handle <= 0:
        if PrintDebug:
            Debug.Print('can\'t create com port file')
        _fn_return_value = - 2
        return _fn_return_value
    #if PrintDebug then Debug.Print "reset arduino"
    Result = X03.EscapeCommFunction(Handle, COM_SETDTR)
    if Result:
        X02.DoEvents()
        X03.Sleep(( 10 ))
        Result = X03.EscapeCommFunction(Handle, COM_CLRDTR)
    if Result == False:
        if PrintDebug:
            Debug.Print('can\'t reset arduino')
        # I never get this message ?
        X03.CloseHandle(( Handle ))
        _fn_return_value = - 3
        return _fn_return_value
    X02.DoEvents()
    #now get in sync
    for i in vbForRange(1, Trials):
        message = Transact(Handle, Chr(Cmnd_STK_GET_SYNC), 2)
        if UBound(message) == 1:
            if message(0) == Resp_STK_INSYNC and message(1) == Resp_STK_OK:
                #if PrintDebug then Debug.Print "in sync with arduino"
                if GetDeviceInformation(Handle, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur):
                    _fn_return_value = 1
                break
    if i >= Trials:
        #If PrintDebug Then Debug.Print "Give up after " & Trials & " trials"
        pass
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if Handle > 0:
        X03.CloseHandle(( Handle ))
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Handle - ByVal 
def Transact(Handle, message, nNumberOfBytesToRead=10):
    _fn_return_value = None
    CbWritten = Variant()

    CbRead = Variant()

    ToSend = Variant()

    j = Long()

    Buffer = vbObjectInitialize(objtype=Byte)

    Response = vbObjectInitialize(((0, 9),), Byte)

    EmptyResp = vbObjectInitialize((0,), Byte)

    Rc = Long()
    #-----------------------------------------------------------------------------------------------------------------------
    message = message + Chr(Sync_CRC_EOP)
    ToSend = Len(message)
    Buffer = vbObjectInitialize((ToSend,), Variant)
    for j in vbForRange(0, ToSend - 1):
        Buffer[j] = Asc(Mid(message, j + 1, 1))
    #Debug.Print "nNumberOfBytesToRead = 10"
    #nNumberOfBytesToRead = 10
    X03.PurgeComm(Handle, PURGE_TXABORT or PURGE_RXABORT or PURGE_TXCLEAR or PURGE_RXCLEAR)
    if X03.WriteFile(Handle, Buffer(0), ToSend, CbWritten, 0) == 0:
        return _fn_return_value
    if CbWritten != ToSend:
        return _fn_return_value
    _fn_return_value = EmptyResp
    while 1:
        Rc = X03.ReadFile(Handle, Response(0), nNumberOfBytesToRead, CbRead, 0)
        # Slow
        if Rc == 0 or CbRead < 1:
            return _fn_return_value
        X02.DoEvents()
        if Response(0) == Resp_STK_INSYNC and Response(CbRead - 1) == Resp_STK_OK or Response(CbRead - 1) == Resp_STK_FAILED:
            resp = vbObjectInitialize(((0, CbRead - 1),), Variant)
            for j in vbForRange(0, CbRead - 1):
                resp[j] = Response(j)
            _fn_return_value = resp
            return _fn_return_value
        #Debug.Print "invalid packet"
        return _fn_return_value
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Handle - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: HWVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMajorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SWMinorVersion=255 - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DeviceSignatur=- 1 - ByRef 
def GetDeviceInformation(Handle, HWVersion=255, SWMajorVersion=255, SWMinorVersion=255, DeviceSignatur=- 1):
    _fn_return_value = None
    Data = vbObjectInitialize(objtype=Byte)

    tmp = Long()
    #--------------------------------------------------------------------------------------------------------------------
    # Added option to speed up by not requesting all values
    # 04.05.20:
    # 1 sec instead of 3 if only the DeviceSignatur is requested
    # Attention: At least one value has to be requested
    _fn_return_value = False
    if DeviceSignatur != - 1:
        Data = Transact(Handle, Chr(STK_READ_SIGN), 5)
        if UBound(Data) != 4:
            return _fn_return_value
        if Data(4) != Resp_STK_OK:
            return _fn_return_value
        tmp = Data(1)
        DeviceSignatur = tmp * 65536
        tmp = Data(2)
        DeviceSignatur = DeviceSignatur + tmp * 256
        tmp = Data(3)
        DeviceSignatur = DeviceSignatur + tmp
    if HWVersion != 255:
        Data = Transact(Handle, Chr(Cmnd_STK_GET_PARAMETER) + Chr(Parm_STK_HW_VER), 3)
        if UBound(Data) != 2:
            return _fn_return_value
        if Data(2) != Resp_STK_OK:
            return _fn_return_value
        HWVersion = Data(1)
    if SWMinorVersion != 255:
        Data = Transact(Handle, Chr(Cmnd_STK_GET_PARAMETER) + Chr(Parm_STK_SW_MAJOR), 3)
        if UBound(Data) != 2:
            return _fn_return_value
        if Data(2) != Resp_STK_OK:
            return _fn_return_value
        SWMajorVersion = Data(1)
    if SWMinorVersion != 255:
        Data = Transact(Handle, Chr(Cmnd_STK_GET_PARAMETER) + Chr(Parm_STK_SW_MINOR), 3)
        if UBound(Data) != 2:
            return _fn_return_value
        if Data(2) != Resp_STK_OK:
            return _fn_return_value
        SWMinorVersion = Data(1)
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function SetCommState Lib "kernel32.dll" (ByVal hCommDev As Long, ByRef lpDCB As DCB) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function GetCommState Lib "kernel32.dll" (ByVal nCid As Long, ByRef lpDCB As DCB) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function BuildCommDCB Lib "kernel32.dll" Alias "BuildCommDCBA" (ByVal lpDef As String, ByRef lpDCB As DCB) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function SetCommTimeouts Lib "kernel32" (ByVal hFile As Long, lpCommTimeouts As COMMTIMEOUTS) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function GetCommTimeouts Lib "kernel32.dll" (ByVal hFile As Long, ByRef lpCommTimeouts As COMMTIMEOUTS) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function EscapeCommFunction Lib "kernel32.dll" (ByVal hFile As Long, ByVal dwFunc As Long) As Boolean
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function PurgeComm Lib "kernel32" (ByVal hFile As Long, ByVal dwFlags As Long) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function GetDefaultCommConfig Lib "kernel32" Alias "GetDefaultCommConfigA" (ByVal lpszName As String, _\nlpCC As COMMCONFIG, lpdwSize As Long) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function CreateFile Lib "kernel32" Alias "CreateFileA" _\n(ByVal lpFileName As String, ByVal dwDesiredAccess As Long, _\nByVal dwShareMode As Long, lpSecurityAttributes As Any, _\nByVal dwCreationDisposition As Long, ByVal dwFlagsAndAttributes As Long, _\nByVal hTemplateFile As Long) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function CloseHandle Lib "kernel32" (ByVal hObject As Long) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function WriteFile Lib "kernel32.dll" (ByVal hFile As Long, _\nByRef Buffer As Any, ByVal nNumberOfBytesToWrite As Long, _\nByRef lpNumberOfBytesWritten As Long, ByVal lpOverlapped As Long) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function ReadFile Lib "kernel32.dll" (ByVal hFile As Long, _\nByRef Buffer As Any, ByVal nNumberOfBytesToRead As Long, _\nByRef lpNumberOfBytesRead As Long, ByVal lpOverlapped As Long) As Long
