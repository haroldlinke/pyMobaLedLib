from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLWA_WinAPI as X03
import ExcelAPI.XLW_Workbook as X02

"""-------------------------------------------------------------------------------
 modCOMM - Written by: David M. Hitchner

 This VB module is a collection of routines to perform serial port I/O without
 using the Microsoft Comm Control component.  This module uses the Windows API
 to perform the overlapped I/O operations necessary for serial communications.

 The routine can handle up to 50 serial ports which are identified with a
 Port ID.

 All routines (with the exception of CommRead and CommWrite) return an error
 code or 0 if no error occurs.  The routine CommGetError can be used to get
 the complete error message.
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 Public Constants
-------------------------------------------------------------------------------
 Output Control Lines (CommSetLine)
 Input Control Lines  (CommGetLine)
-------------------------------------------------------------------------------
 System Constants
-------------------------------------------------------------------------------
 COMM Functions
 COMM Escape Functions
-------------------------------------------------------------------------------
 System Structures
-------------------------------------------------------------------------------

 The DCB structure defines the control setting for a serial
 communications device.

-------------------------------------------------------------------------------
 System Functions
-------------------------------------------------------------------------------

 Fills a specified DCB structure with values specified in
 a device-control string.

# VB2PY (CheckDirective) VB directive took path 1 on VBA7
 18.01.20:

 Retrieves information about a communications error and reports
 the current status of a communications device. The function is
 called when a communications error occurs, and it clears the
 device's error flag to enable additional input and output
 (I/O) operations.


 Closes an open communications device or file handle.


 Creates or opens a communications resource and returns a handle
 that can be used to access the resource.


 Directs a specified communications device to perform a function.


 Formats a message string such as an error string returned
 by anoher function.


 Retrieves modem control-register values.


 Retrieves the current control settings for a specified
 communications device.


 Retrieves the calling thread's last-error code value.


 Retrieves the results of an overlapped operation on the
 specified file, named pipe, or communications device.


 Discards all characters from the output or input buffer of a
 specified communications resource. It can also terminate
 pending read or write operations on the resource.


 Reads data from a file, starting at the position indicated by the
 file pointer. After the read operation has been completed, the
 file pointer is adjusted by the number of bytes actually read,
 unless the file handle is created with the overlapped attribute.
 If the file handle is created for overlapped input and output
 (I/O), the application must adjust the position of the file pointer
 after the read operation.


 Configures a communications device according to the specifications
 in a device-control block (a DCB structure). The function
 reinitializes all hardware and control settings, but it does not
 empty output or input queues.


 Sets the time-out parameters for all read and write operations on a
 specified communications device.


 Initializes the communications parameters for a specified
 communications device.


 Writes data to a file and is designed for both synchronous and a
 synchronous operation. The function starts writing data to the file
 at the position indicated by the file pointer. After the write
 operation has been completed, the file pointer is adjusted by the
 number of bytes actually written, except when the file is opened with
 FILE_FLAG_OVERLAPPED. If the file handle was created for overlapped
 input and output (I/O), the application must adjust the position of
 the file pointer after the write operation is finished.

-------------------------------------------------------------------------------
 Program Constants
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 Program Structures
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 Program Storage
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 GetSystemMessage - Gets system error text for the specified error code.
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 CommOpen - Opens/Initializes serial port.


 Parameters:
   intPortID   - Port ID used when port was opened.
   strSettings - Communication settings.
                 Example: "baud=9600 parity=N data=8 stop=1"

 Returns:
   Error Code  - 0 = No Error.

----------------------------------------------------------------------------
-----------------------------------------------------------
-------------------------------------------------------------------------------
 CommSet - Modifies the serial port settings.

 Parameters:
   intPortID   - Port ID used when port was opened.
   strSettings - Communication settings.
                 Example: "baud=9600 parity=N data=8 stop=1"

 Returns:
   Error Code  - 0 = No Error.
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 CommClose - Close the serial port.

 Parameters:
   intPortID   - Port ID used when port was opened.

 Returns:
   Error Code  - 0 = No Error.
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 CommFlush - Flush the send and receive serial port buffers.

 Parameters:
   intPortID   - Port ID used when port was opened.

 Returns:
   Error Code  - 0 = No Error.
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 CommRead - Read serial port input buffer.

 Parameters:
   intPortID   - Port ID used when port was opened.
   strData     - Data buffer.
   lngSize     - Maximum number of bytes to be read.

 Returns:
   Error Code  - 0 = No Error.
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 CommWrite - Output data to the serial port.

 Parameters:
   intPortID   - Port ID used when port was opened.
   strData     - Data to be transmitted.

 Returns:
   Error Code  - 0 = No Error.
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 CommGetLine - Get the state of selected serial port control lines.

 Parameters:
   intPortID   - Port ID used when port was opened.
   intLine     - Serial port line. CTS, DSR, RING, RLSD (CD)
   blnState    - Returns state of line (Cleared or Set).

 Returns:
   Error Code  - 0 = No Error.
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 CommSetLine - Set the state of selected serial port control lines.

 Parameters:
   intPortID   - Port ID used when port was opened.
   intLine     - Serial port line. BREAK, DTR, RTS
                 Note: BREAK actually sets or clears a "break" condition on
                 the transmit data line.
   blnState    - Sets the state of line (Cleared or Set).

 Returns:
   Error Code  - 0 = No Error.
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
 CommGetError - Get the last serial port error message.

 Parameters:
   strMessage  - Error message from last serial port error.

 Returns:
   Error Code  - Last serial port error code.
-------------------------------------------------------------------------------
"""

LINE_BREAK = 1
LINE_DTR = 2
LINE_RTS = 3
LINE_CTS = 0x10
LINE_DSR = 0x20
LINE_RING = 0x40
LINE_RLSD = 0x80
LINE_CD = 0x80
ERROR_IO_INCOMPLETE = 996
ERROR_IO_PENDING = 997
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_ATTRIBUTE_NORMAL = 0x80
FILE_FLAG_OVERLAPPED = 0x40000000
FORMAT_MESSAGE_FROM_SYSTEM = 0x1000
OPEN_EXISTING = 3
MS_CTS_ON = 0x10
MS_DSR_ON = 0x20
MS_RING_ON = 0x40
MS_RLSD_ON = 0x80
PURGE_RXABORT = 0x2
PURGE_RXCLEAR = 0x8
PURGE_TXABORT = 0x1
PURGE_TXCLEAR = 0x4
CLRBREAK = 9
CLRDTR = 6
CLRRTS = 4
SETBREAK = 8
SETDTR = 5
SETRTS = 3
class COMSTAT:
    def __init__(self):
        self.fBitFields = Long()
        self.cbInQue = Long()
        self.cbOutQue = Long()

class COMMTIMEOUTS:
    def __init__(self):
        self.ReadIntervalTimeout = Long()
        self.ReadTotalTimeoutMultiplier = Long()
        self.ReadTotalTimeoutConstant = Long()
        self.WriteTotalTimeoutMultiplier = Long()
        self.WriteTotalTimeoutConstant = Long()

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

class OVERLAPPED:
    def __init__(self):
        self.Internal = Long()
        self.InternalHigh = Long()
        self.offset = Long()
        self.OffsetHigh = Long()
        self.hEvent = Long()

class SECURITY_ATTRIBUTES:
    def __init__(self):
        self.nLength = Long()
        self.lpSecurityDescriptor = Long()
        self.bInheritHandle = Long()

MAX_PORTS = 50
class COMM_ERROR:
    def __init__(self):
        self.lngErrorCode = Long()
        self.strFunction = String()
        self.strErrorMessage = String()

class COMM_PORT:
    def __init__(self):
        self.lngHandle = Long()
        self.blnPortOpen = Boolean()
        self.udtDCB = DCB()

udtCommOverlap = OVERLAPPED()
udtCommError = COMM_ERROR()
udtPorts = vbObjectInitialize(((1, MAX_PORTS),), COMM_PORT)

def GetSystemMessage(lngErrorCode):
    _fn_return_value = None
    intPos = Integer()

    strMessage = String()

    strMsgBuff = FixedString(256)
    FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM, 0, lngErrorCode, 0, strMsgBuff, 255, 0)
    intPos = InStr(1, strMsgBuff, vbNullChar)
    if intPos > 0:
        strMessage = Trim(Left(strMsgBuff, intPos - 1))
    else:
        strMessage = Trim(strMsgBuff)
    _fn_return_value = strMessage
    return _fn_return_value

def CommOpen(intPortID, strSettings):
    global udtPorts
    _fn_return_value = None
    lngStatus = Long()

    udtCommTimeOuts = COMMTIMEOUTS()

    COMStr = String()
    #----------------------------------------------------------------------------
    if intPortID > 4:
        COMStr = '\\\\.\\COM'
        # 16.12.19: Hardi
    else:
        COMStr = 'COM'
    COMStr = COMStr + intPortID
    # VB2PY (UntranslatedCode) On Error GoTo Routine_Error
    # See if port already in use.
    if udtPorts(intPortID).blnPortOpen:
        lngStatus = - 1
        _with56 = udtCommError
        _with56.lngErrorCode = lngStatus
        _with56.strFunction = 'CommOpen'
        _with56.strErrorMessage = 'Port in use.'
        GoTo(Routine_Exit)
    # Open serial port.
    udtPorts[intPortID].lngHandle = X03.CreateFile(COMStr, GENERIC_READ or GENERIC_WRITE, 0, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0)
    if udtPorts(intPortID).lngHandle == - 1:
        lngStatus = SetCommError('CommOpen (CreateFile)')
        GoTo(Routine_Exit)
    udtPorts[intPortID].blnPortOpen = True
    # Setup device buffers (1K each).
    lngStatus = SetupComm(udtPorts(intPortID).lngHandle, 1024, 1024)
    if lngStatus == 0:
        lngStatus = SetCommError('CommOpen (SetupComm)')
        GoTo(Routine_Exit)
    # Purge buffers.
    lngStatus = X03.PurgeComm(udtPorts(intPortID).lngHandle, PURGE_TXABORT or PURGE_RXABORT or PURGE_TXCLEAR or PURGE_RXCLEAR)
    if lngStatus == 0:
        lngStatus = SetCommError('CommOpen (PurgeComm)')
        GoTo(Routine_Exit)
    # Set serial port timeouts.
    _with57 = udtCommTimeOuts
    _with57.ReadIntervalTimeout = - 1
    _with57.ReadTotalTimeoutMultiplier = 0
    _with57.ReadTotalTimeoutConstant = 1000
    _with57.WriteTotalTimeoutMultiplier = 0
    _with57.WriteTotalTimeoutMultiplier = 1000
    lngStatus = X03.SetCommTimeouts(udtPorts(intPortID).lngHandle, udtCommTimeOuts)
    if lngStatus == 0:
        lngStatus = SetCommError('CommOpen (SetCommTimeouts)')
        GoTo(Routine_Exit)
    # Get the current state (DCB).
    lngStatus = X03.GetCommState(udtPorts(intPortID).lngHandle, udtPorts(intPortID).udtDCB)
    if lngStatus == 0:
        lngStatus = SetCommError('CommOpen (GetCommState)')
        GoTo(Routine_Exit)
    # Modify the DCB to reflect the desired settings.
    lngStatus = X03.BuildCommDCB(strSettings, udtPorts(intPortID).udtDCB)
    if lngStatus == 0:
        lngStatus = SetCommError('CommOpen (BuildCommDCB)')
        GoTo(Routine_Exit)
    # Set the new state.
    lngStatus = X03.SetCommState(udtPorts(intPortID).lngHandle, udtPorts(intPortID).udtDCB)
    if lngStatus == 0:
        lngStatus = SetCommError('CommOpen (SetCommState)')
        GoTo(Routine_Exit)
    lngStatus = 0
    _fn_return_value = lngStatus
    return _fn_return_value
    lngStatus = Err.Number
    _with58 = udtCommError
    _with58.lngErrorCode = lngStatus
    _with58.strFunction = 'CommOpen'
    _with58.strErrorMessage = Err.Description
    # VB2PY (UntranslatedCode) Resume Routine_Exit
    return _fn_return_value

def SetCommError(strFunction):
    _fn_return_value = None
    #-----------------------------------------------------------
    _with59 = udtCommError
    _with59.lngErrorCode = Err.LastDllError
    _with59.strFunction = strFunction
    _with59.strErrorMessage = GetSystemMessage(_with59.lngErrorCode)
    _fn_return_value = _with59.lngErrorCode
    return _fn_return_value

def SetCommErrorEx(strFunction, lngHnd):
    _fn_return_value = None
    lngErrorFlags = Long()

    udtCommStat = COMSTAT()
    _with60 = udtCommError
    _with60.lngErrorCode = GetLastError
    _with60.strFunction = strFunction
    _with60.strErrorMessage = GetSystemMessage(_with60.lngErrorCode)
    ClearCommError(lngHnd, lngErrorFlags, udtCommStat)
    _with60.strErrorMessage = _with60.strErrorMessage + '  COMM Error Flags = ' + Hex(lngErrorFlags)
    _fn_return_value = _with60.lngErrorCode
    return _fn_return_value

def CommSet(intPortID, strSettings):
    _fn_return_value = None
    lngStatus = Long()
    # VB2PY (UntranslatedCode) On Error GoTo Routine_Error
    lngStatus = X03.GetCommState(udtPorts(intPortID).lngHandle, udtPorts(intPortID).udtDCB)
    if lngStatus == 0:
        lngStatus = SetCommError('CommSet (GetCommState)')
        GoTo(Routine_Exit)
    lngStatus = X03.BuildCommDCB(strSettings, udtPorts(intPortID).udtDCB)
    if lngStatus == 0:
        lngStatus = SetCommError('CommSet (BuildCommDCB)')
        GoTo(Routine_Exit)
    lngStatus = X03.SetCommState(udtPorts(intPortID).lngHandle, udtPorts(intPortID).udtDCB)
    if lngStatus == 0:
        lngStatus = SetCommError('CommSet (SetCommState)')
        GoTo(Routine_Exit)
    lngStatus = 0
    _fn_return_value = lngStatus
    return _fn_return_value
    lngStatus = Err.Number
    _with61 = udtCommError
    _with61.lngErrorCode = lngStatus
    _with61.strFunction = 'CommSet'
    _with61.strErrorMessage = Err.Description
    # VB2PY (UntranslatedCode) Resume Routine_Exit
    return _fn_return_value

def CommClose(intPortID):
    global udtPorts
    _fn_return_value = None
    lngStatus = Long()
    # VB2PY (UntranslatedCode) On Error GoTo Routine_Error
    if udtPorts(intPortID).blnPortOpen:
        lngStatus = X03.CloseHandle(udtPorts(intPortID).lngHandle)
        if lngStatus == 0:
            lngStatus = SetCommError('CommClose (CloseHandle)')
            GoTo(Routine_Exit)
        udtPorts[intPortID].blnPortOpen = False
    lngStatus = 0
    _fn_return_value = lngStatus
    return _fn_return_value
    lngStatus = Err.Number
    _with62 = udtCommError
    _with62.lngErrorCode = lngStatus
    _with62.strFunction = 'CommClose'
    _with62.strErrorMessage = Err.Description
    # VB2PY (UntranslatedCode) Resume Routine_Exit
    return _fn_return_value

def CommFlush(intPortID):
    _fn_return_value = None
    lngStatus = Long()
    # VB2PY (UntranslatedCode) On Error GoTo Routine_Error
    lngStatus = X03.PurgeComm(udtPorts(intPortID).lngHandle, PURGE_TXABORT or PURGE_RXABORT or PURGE_TXCLEAR or PURGE_RXCLEAR)
    if lngStatus == 0:
        lngStatus = SetCommError('CommFlush (PurgeComm)')
        GoTo(Routine_Exit)
    lngStatus = 0
    _fn_return_value = lngStatus
    return _fn_return_value
    lngStatus = Err.Number
    _with63 = udtCommError
    _with63.lngErrorCode = lngStatus
    _with63.strFunction = 'CommFlush'
    _with63.strErrorMessage = Err.Description
    # VB2PY (UntranslatedCode) Resume Routine_Exit
    return _fn_return_value

def CommRead(intPortID, strData, lngSize):
    _fn_return_value = None
    lngStatus = Long()

    lngRdSize = Long()

    lngBytesRead = Long()

    lngRdStatus = Long()

    strRdBuffer = FixedString(1024)

    lngErrorFlags = Long()

    udtCommStat = COMSTAT()
    # VB2PY (UntranslatedCode) On Error GoTo Routine_Error
    strData = ''
    lngBytesRead = 0
    X02.DoEvents()
    # Clear any previous errors and get current status.
    lngStatus = ClearCommError(udtPorts(intPortID).lngHandle, lngErrorFlags, udtCommStat)
    if lngStatus == 0:
        lngBytesRead = - 1
        lngStatus = SetCommError('CommRead (ClearCommError)')
        GoTo(Routine_Exit)
    if udtCommStat.cbInQue > 0:
        if udtCommStat.cbInQue > lngSize:
            lngRdSize = udtCommStat.cbInQue
        else:
            lngRdSize = lngSize
    else:
        lngRdSize = 0
    if lngRdSize:
        lngRdStatus = X03.ReadFile(udtPorts(intPortID).lngHandle, strRdBuffer, lngRdSize, lngBytesRead, udtCommOverlap)
        if lngRdStatus == 0:
            lngStatus = GetLastError
            if lngStatus == ERROR_IO_PENDING:
                # Wait for read to complete.
                # This function will timeout according to the
                # COMMTIMEOUTS.ReadTotalTimeoutConstant variable.
                # Every time it times out, check for port errors.
                # Loop until operation is complete.
                while GetOverlappedResult(udtPorts(intPortID).lngHandle, udtCommOverlap, lngBytesRead, True) == 0:
                    lngStatus = GetLastError
                    if lngStatus != ERROR_IO_INCOMPLETE:
                        lngBytesRead = - 1
                        lngStatus = SetCommErrorEx('CommRead (GetOverlappedResult)', udtPorts(intPortID).lngHandle)
                        GoTo(Routine_Exit)
            else:
                # Some other error occurred.
                lngBytesRead = - 1
                lngStatus = SetCommErrorEx('CommRead (ReadFile)', udtPorts(intPortID).lngHandle)
                GoTo(Routine_Exit)
        strData = Left(strRdBuffer, lngBytesRead)
    _fn_return_value = lngBytesRead
    return _fn_return_value
    lngBytesRead = - 1
    lngStatus = Err.Number
    _with64 = udtCommError
    _with64.lngErrorCode = lngStatus
    _with64.strFunction = 'CommRead'
    _with64.strErrorMessage = Err.Description
    # VB2PY (UntranslatedCode) Resume Routine_Exit
    return _fn_return_value

def CommWrite(intPortID, strData):
    _fn_return_value = None
    i = Integer()

    lngStatus = Long()

    lngSize = Long()

    lngWrSize = Long()

    lngWrStatus = Long()
    # VB2PY (UntranslatedCode) On Error GoTo Routine_Error
    # Get the length of the data.
    lngSize = Len(strData)
    # Output the data.
    lngWrStatus = X03.WriteFile(udtPorts(intPortID).lngHandle, strData, lngSize, lngWrSize, udtCommOverlap)
    # Note that normally the following code will not execute because the driver
    # caches write operations. Small I/O requests (up to several thousand bytes)
    # will normally be accepted immediately and WriteFile will return true even
    # though an overlapped operation was specified.
    X02.DoEvents()
    if lngWrStatus == 0:
        lngStatus = GetLastError
        if lngStatus == 0:
            GoTo(Routine_Exit)
        elif lngStatus == ERROR_IO_PENDING:
            # We should wait for the completion of the write operation so we know
            # if it worked or not.
            #
            # This is only one way to do this. It might be beneficial to place the
            # writing operation in a separate thread so that blocking on completion
            # will not negatively affect the responsiveness of the UI.
            #
            # If the write takes long enough to complete, this function will timeout
            # according to the CommTimeOuts.WriteTotalTimeoutConstant variable.
            # At that time we can check for errors and then wait some more.
            # Loop until operation is complete.
            while GetOverlappedResult(udtPorts(intPortID).lngHandle, udtCommOverlap, lngWrSize, True) == 0:
                lngStatus = GetLastError
                if lngStatus != ERROR_IO_INCOMPLETE:
                    lngStatus = SetCommErrorEx('CommWrite (GetOverlappedResult)', udtPorts(intPortID).lngHandle)
                    GoTo(Routine_Exit)
        else:
            # Some other error occurred.
            lngWrSize = - 1
            lngStatus = SetCommErrorEx('CommWrite (WriteFile)', udtPorts(intPortID).lngHandle)
            GoTo(Routine_Exit)
    for i in vbForRange(1, 10):
        X02.DoEvents()
    _fn_return_value = lngWrSize
    return _fn_return_value
    lngStatus = Err.Number
    _with65 = udtCommError
    _with65.lngErrorCode = lngStatus
    _with65.strFunction = 'CommWrite'
    _with65.strErrorMessage = Err.Description
    # VB2PY (UntranslatedCode) Resume Routine_Exit
    return _fn_return_value

def CommGetLine(intPortID, intLine, blnState):
    _fn_return_value = None
    lngStatus = Long()

    lngComStatus = Long()

    lngModemStatus = Long()
    # VB2PY (UntranslatedCode) On Error GoTo Routine_Error
    lngStatus = GetCommModemStatus(udtPorts(intPortID).lngHandle, lngModemStatus)
    if lngStatus == 0:
        lngStatus = SetCommError('CommReadCD (GetCommModemStatus)')
        GoTo(Routine_Exit)
    if ( lngModemStatus and intLine ) :
        blnState = True
    else:
        blnState = False
    lngStatus = 0
    _fn_return_value = lngStatus
    return _fn_return_value
    lngStatus = Err.Number
    _with66 = udtCommError
    _with66.lngErrorCode = lngStatus
    _with66.strFunction = 'CommReadCD'
    _with66.strErrorMessage = Err.Description
    # VB2PY (UntranslatedCode) Resume Routine_Exit
    return _fn_return_value

def CommSetLine(intPortID, intLine, blnState):
    _fn_return_value = None
    lngStatus = Long()

    lngNewState = Long()
    # VB2PY (UntranslatedCode) On Error GoTo Routine_Error
    if intLine == LINE_BREAK:
        if blnState:
            lngNewState = SETBREAK
        else:
            lngNewState = CLRBREAK
    elif intLine == LINE_DTR:
        if blnState:
            lngNewState = SETDTR
        else:
            lngNewState = CLRDTR
    elif intLine == LINE_RTS:
        if blnState:
            lngNewState = SETRTS
        else:
            lngNewState = CLRRTS
    lngStatus = X03.EscapeCommFunction(udtPorts(intPortID).lngHandle, lngNewState)
    if lngStatus == 0:
        lngStatus = SetCommError('CommSetLine (EscapeCommFunction)')
        GoTo(Routine_Exit)
    lngStatus = 0
    _fn_return_value = lngStatus
    return _fn_return_value
    lngStatus = Err.Number
    _with67 = udtCommError
    _with67.lngErrorCode = lngStatus
    _with67.strFunction = 'CommSetLine'
    _with67.strErrorMessage = Err.Description
    # VB2PY (UntranslatedCode) Resume Routine_Exit
    return _fn_return_value

def CommGetError(strMessage):
    _fn_return_value = None
    _with68 = udtCommError
    _fn_return_value = _with68.lngErrorCode
    strMessage = 'Error (' + CStr(_with68.lngErrorCode) + '): ' + _with68.strFunction + ' - ' + _with68.strErrorMessage
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Declare PtrSafe Function BuildCommDCB Lib "kernel32" Alias "BuildCommDCBA" _\n(ByVal lpDef As String, lpDCB As DCB) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function ClearCommError Lib "kernel32" _\n(ByVal hFile As Long, lpErrors As Long, lpStat As COMSTAT) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function CloseHandle Lib "kernel32" (ByVal hObject As Long) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function CreateFile Lib "kernel32" Alias "CreateFileA" _\n(ByVal lpFileName As String, ByVal dwDesiredAccess As Long, _\nByVal dwShareMode As Long, lpSecurityAttributes As Any, _\nByVal dwCreationDisposition As Long, ByVal dwFlagsAndAttributes As Long, _\nByVal hTemplateFile As Long) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function EscapeCommFunction Lib "kernel32" _\n(ByVal nCid As Long, ByVal nFunc As Long) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function FormatMessage Lib "kernel32" Alias "FormatMessageA" _\n(ByVal dwFlags As Long, lpSource As Any, ByVal dwMessageId As Long, _\nByVal dwLanguageId As Long, ByVal lpBuffer As String, ByVal nSize As Long, _\nArguments As Long) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetCommModemStatus Lib "kernel32" _\n(ByVal hFile As Long, lpModemStat As Long) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetCommState Lib "kernel32" _\n(ByVal nCid As Long, lpDCB As DCB) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetLastError Lib "kernel32" () As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function GetOverlappedResult Lib "kernel32" _\n(ByVal hFile As Long, lpOverlapped As OVERLAPPED, _\nlpNumberOfBytesTransferred As Long, ByVal bWait As Long) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function PurgeComm Lib "kernel32" _\n(ByVal hFile As Long, ByVal dwFlags As Long) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function ReadFile Lib "kernel32" _\n(ByVal hFile As Long, ByVal lpBuffer As String, _\nByVal nNumberOfBytesToRead As Long, ByRef lpNumberOfBytesRead As Long, _\nlpOverlapped As OVERLAPPED) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function SetCommState Lib "kernel32" _\n(ByVal hCommDev As Long, lpDCB As DCB) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function SetCommTimeouts Lib "kernel32" _\n(ByVal hFile As Long, lpCommTimeouts As COMMTIMEOUTS) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function SetupComm Lib "kernel32" _\n(ByVal hFile As Long, ByVal dwInQueue As Long, ByVal dwOutQueue As Long) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function WriteFile Lib "kernel32" _\n(ByVal hFile As Long, ByVal lpBuffer As String, _\nByVal nNumberOfBytesToWrite As Long, lpNumberOfBytesWritten As Long, _\nlpOverlapped As OVERLAPPED) As Long
