from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import ExcelAPI.XLC_Excel_Consts as X01
import ExcelAPI.XLWA_WinAPI as X03
import pattgen.M30_Tools as M30

""" M40_ShellAndWait:
 ~~~~~~~~~~~~~~~~~
 Module Description:
 ~~~~~~~~~~~~~~~~~~~
 This module provides a function to call external programs and wait for a certain time.
 In addition the windows style (Hidden, Maximized, Minimized, ...) and the
 "Ctrl Break" behavior could be defined.
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
 Chip Pearson
 http://www.cpearson.com/excel/ShellAndWait.aspx
 This module contains code for the ShellAndWait function that will Shell to a process
 and wait for that process to End before returning to the caller.
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# VB2PY (CheckDirective) VB directive took path 1 on Win64
 28.09.19: New 64 Bit definition (Test für Armins MoBa Rechner)
 https://foren.activevb.de/forum/vba/thread-25588/beitrag-25588/VBA7-Win64-CreateProcess-WaitFo/
'# VB2PY (CheckDirective) VB2PY directive Ignore Text
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
# VB2PY (CheckDirective) VB directive took path 1 on Win64
 28.09.19:
"""

SYNCHRONIZE = 0x100000
# Enumeration 'ShellAndWaitResult'
Success = 0
Failure = 1
Timeout = 2
InvalidParameter = 3
SysWaitAbandoned = 4
UserWaitAbandoned = 5
UserBreak = 6
# Enumeration 'ActionOnBreak'
IgnoreBreak = 0
AbandonWait = 1
PromptUser = 2
TaskId = Long()
STATUS_ABANDONED_WAIT_0 = 0x80
STATUS_WAIT_0 = 0x0
WAIT_ABANDONED = ( STATUS_ABANDONED_WAIT_0 + 0 )
WAIT_OBJECT_0 = ( STATUS_WAIT_0 + 0 )
WAIT_TIMEOUT = 258
WAIT_FAILED = 0xFFFFFFFF
WAIT_INFINITE = - 1

def ShellAndWait(ShellCommand, TimeOutSeconds, ShellWindowState, BreakKey):
    global TaskId
    _fn_return_value = None
    TimeOutMs = Long()

    WaitRes = Long()

    ms = Long()

    MsgRes = VbMsgBoxResult()

    SaveCancelKey = XlEnableCancelKey()

    ElapsedTime = Long()

    Quit = Boolean()

    ProcHandle = Long()

    ERR_BREAK_KEY = 18

    DEFAULT_POLL_INTERVAL = 500
    #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # ShellAndWait
    #
    # This function calls Shell and passes to it the command text in ShellCommand. The function
    # then waits for TimeOutSeconds (in Seconds) to expire.
    #
    #   Parameters:
    #       ShellCommand
    #           is the command text to pass to the Shell function.
    #
    #       TimeOutSeconds Hardi: Changed type to double (Old: Long)
    #
    #       TimeOutMs
    #           is the number of milliseconds to wait for the shell'd program to wait. If the
    #           shell'd program terminates before TimeOutMs has expired, the function returns
    #           ShellAndWaitResult.Success = 0. If TimeOutMs expires before the shell'd program
    #           terminates, the return value is ShellAndWaitResult.TimeOut = 2.
    #
    #       ShellWindowState
    #           is an item in VbAppWinStyle specifying the window state for the shell'd program.
    #
    #       BreakKey
    #           is an item in ActionOnBreak indicating how to handle the application's cancel key
    #           (Ctrl Break). If BreakKey is ActionOnBreak.AbandonWait and the user cancels, the
    #           wait is abandoned and the result is ShellAndWaitResult.UserWaitAbandoned = 5.
    #           If BreakKey is ActionOnBreak.IgnoreBreak, the cancel key is ignored. If
    #           BreakKey is ActionOnBreak.PromptUser, the user is given a ?Continue? message. If the
    #           user selects "do not continue", the function returns ShellAndWaitResult.UserBreak = 6.
    #           If the user selects "continue", the wait is continued.
    #
    #   Return values:
    #            ShellAndWaitResult.Success = 0
    #               indicates the the process completed successfully.
    #            ShellAndWaitResult.Failure = 1
    #               indicates that the Wait operation failed due to a Windows error.
    #            ShellAndWaitResult.TimeOut = 2
    #               indicates that the TimeOutMs interval timed out the Wait.
    #            ShellAndWaitResult.InvalidParameter = 3
    #               indicates that an invalid value was passed to the procedure.
    #            ShellAndWaitResult.SysWaitAbandoned = 4
    #               indicates that the system abandoned the wait.
    #            ShellAndWaitResult.UserWaitAbandoned = 5
    #               indicates that the user abandoned the wait via the cancel key (Ctrl+Break).
    #               This happens only if BreakKey is set to ActionOnBreak.AbandonWait.
    #            ShellAndWaitResult.UserBreak = 6
    #               indicates that the user broke out of the wait after being prompted with
    #               a ?Continue message. This happens only if BreakKey is set to
    #               ActionOnBreak.PromptUser.
    #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ## VB2PY (CheckDirective) VB directive took path 1 on Win64
    # 28.09.19:
    if Trim(ShellCommand) == vbNullString:
        _fn_return_value = ShellAndWaitResult.InvalidParameter
        return _fn_return_value
    TimeOutMs = 1000 * TimeOutSeconds
    if TimeOutMs < 0:
        _fn_return_value = ShellAndWaitResult.InvalidParameter
        return _fn_return_value
    elif TimeOutMs == 0:
        ms = WAIT_INFINITE
    else:
        ms = TimeOutMs
    _select63 = BreakKey
    if (_select63 == AbandonWait) or (_select63 == IgnoreBreak) or (_select63 == PromptUser):
        # valid
        pass
    else:
        _fn_return_value = ShellAndWaitResult.InvalidParameter
        return _fn_return_value
    _select64 = ShellWindowState
    if (_select64 == vbHide) or (_select64 == vbMaximizedFocus) or (_select64 == vbMinimizedFocus) or (_select64 == vbMinimizedNoFocus) or (_select64 == vbNormalFocus) or (_select64 == vbNormalNoFocus):
        # valid
        pass
    else:
        _fn_return_value = ShellAndWaitResult.InvalidParameter
        return _fn_return_value
    # VB2PY (UntranslatedCode) On Error Resume Next
    Err.Clear()
    TaskId = X02.Shell(ShellCommand, ShellWindowState)
    if ( Err.Number != 0 )  or  ( TaskId == 0 ) :
        _fn_return_value = ShellAndWaitResult.Failure
        return _fn_return_value
    ProcHandle = OpenProcess(SYNCHRONIZE, False, TaskId)
    if ProcHandle == 0:
        _fn_return_value = ShellAndWaitResult.Failure
        return _fn_return_value
    # VB2PY (UntranslatedCode) On Error GoTo ErrH
    SaveCancelKey = X02.Application.EnableCancelKey
    X02.Application.EnableCancelKey = X01.xlErrorHandler
    WaitRes = X03.WaitForSingleObject(ProcHandle, DEFAULT_POLL_INTERVAL)
    while not (WaitRes == WAIT_OBJECT_0):
        X02.DoEvents()
        _select65 = WaitRes
        if (_select65 == WAIT_ABANDONED):
            # Windows abandoned the wait
            _fn_return_value = ShellAndWaitResult.SysWaitAbandoned
            break
        elif (_select65 == WAIT_OBJECT_0):
            # Successful completion
            _fn_return_value = ShellAndWaitResult.Success
            break
        elif (_select65 == WAIT_FAILED):
            # attach failed
            _fn_return_value = ShellAndWaitResult.Failure
            break
        elif (_select65 == WAIT_TIMEOUT):
            # Wait timed out. Here, this time out is on DEFAULT_POLL_INTERVAL.
            # See if ElapsedTime is greater than the user specified wait
            # time out. If we have exceed that, get out with a TimeOut status.
            # Otherwise, reissue as wait and continue.
            ElapsedTime = ElapsedTime + DEFAULT_POLL_INTERVAL
            if ms > 0:
                # user specified timeout
                if ElapsedTime > ms:
                    _fn_return_value = ShellAndWaitResult.Timeout
                    break
                else:
                    # user defined timeout has not expired.
                    pass
            else:
                # infinite wait -- do nothing
                pass
            # reissue the Wait on ProcHandle
            WaitRes = X03.WaitForSingleObject(ProcHandle, DEFAULT_POLL_INTERVAL)
        else:
            # unknown result, assume failure
            _fn_return_value = ShellAndWaitResult.Failure
            break
            Quit = True
    X03.CloseHandle(ProcHandle)
    X02.Application.EnableCancelKey = SaveCancelKey
    return _fn_return_value
    Debug.Print('ErrH: Cancel: ' + X02.Application.EnableCancelKey)
    if Err.Number == ERR_BREAK_KEY:
        if BreakKey == ActionOnBreak.AbandonWait:
            X03.CloseHandle(ProcHandle)
            _fn_return_value = ShellAndWaitResult.UserWaitAbandoned
            X02.Application.EnableCancelKey = SaveCancelKey
            return _fn_return_value
        elif BreakKey == ActionOnBreak.IgnoreBreak:
            Err.Clear()
            # VB2PY (UntranslatedCode) Resume
        elif BreakKey == ActionOnBreak.PromptUser:
            MsgRes = M30.MsgBoxMov('User Process Break.' + vbCrLf + 'Continue to wait?', vbYesNo)
            if MsgRes == vbNo:
                X03.CloseHandle(ProcHandle)
                _fn_return_value = ShellAndWaitResult.UserBreak
                X02.Application.EnableCancelKey = SaveCancelKey
            else:
                Err.Clear()
                # VB2PY (UntranslatedCode) Resume Next
        else:
            X03.CloseHandle(ProcHandle)
            X02.Application.EnableCancelKey = SaveCancelKey
            _fn_return_value = ShellAndWaitResult.Failure
    else:
        # some other error. assume failure
        X03.CloseHandle(ProcHandle)
        _fn_return_value = ShellAndWaitResult.Failure
    X02.Application.EnableCancelKey = SaveCancelKey
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Option Compare Text
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function WaitForSingleObject Lib "kernel32" (ByVal hHandle As LongPtr, ByVal dwMilliseconds As LongLong) As LongLong
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function OpenProcess Lib "kernel32" (ByVal dwDesiredAccess As Long, ByVal bInheritHandle As Long, ByVal dwProcessId As Long) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function CloseHandle Lib "kernel32" (ByVal hObject As Long) As Long
