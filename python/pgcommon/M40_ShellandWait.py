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
# fromx vb2py.vbdebug import *
from vb2py.vbconstants import *

#import proggen.Prog_Generator as PG
import subprocess

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
 https://foren.activevb.de/forum/vba/thread-25588/beitrag-25588/VBA7-Win64-CreateProcess-WaitFo/
"""

__SYNCHRONIZE = 0x100000
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
__STATUS_ABANDONED_WAIT_0 = 0x80
__STATUS_WAIT_0 = 0x0
__WAIT_ABANDONED = ( __STATUS_ABANDONED_WAIT_0 + 0 )
__WAIT_OBJECT_0 = ( __STATUS_WAIT_0 + 0 )
__WAIT_TIMEOUT = 258
__WAIT_FAILED = 0xFFFFFFFF
__WAIT_INFINITE = - 1

def ShellAndWait(ShellCommand, TimeOutSeconds, ShellWindowState, BreakKey):
    fn_return_value = None

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
    if Trim(ShellCommand) == vbNullString:
        fn_return_value = InvalidParameter
        return fn_return_value

    if TimeOutSeconds < 0:
        fn_return_value = InvalidParameter
        return fn_return_value

    if (BreakKey == AbandonWait) or (BreakKey == IgnoreBreak) or (BreakKey == PromptUser):
        # valid
        pass
    else:
        fn_return_value = InvalidParameter
        return fn_return_value
    if (ShellWindowState == vbHide) or (ShellWindowState == vbMaximizedFocus) or (ShellWindowState == vbMinimizedFocus) or (ShellWindowState == vbMinimizedNoFocus) or (ShellWindowState == vbNormalFocus) or (ShellWindowState == vbNormalNoFocus):
        # valid
        pass
    else:
        fn_return_value = InvalidParameter
        return fn_return_value
    # VB2PY (UntranslatedCode) On Error Resume Next
    try:
        
        if TimeOutSeconds == 0:
            process = subprocess.run(ShellCommand,shell=False)
        else:
            process = subprocess.run(ShellCommand,timeout=TimeOutSeconds,shell=False)
            
        errornumber = process.returncode
        
        if errornumber != 0:
            return Failure
        else:
            return Success
    except subprocess.TimeoutExpired:
        return Timeout
    
    except Exception as error:
        print(error)
        return Failure
        
        
    
    """
    #Err.Clear()
    
    
    TaskId = Shell(ShellCommand, ShellWindowState)
    if ( Err.Number != 0 )  or  ( TaskId == 0 ) :
        fn_return_value = Failure
        return fn_return_value
    ProcHandle = OpenProcess(__SYNCHRONIZE, False, TaskId)
    if ProcHandle == 0:
        fn_return_value = Failure
        return fn_return_value
    # VB2PY (UntranslatedCode) On Error GoTo errH
    SaveCancelKey = Application.EnableCancelKey
    Application.EnableCancelKey = xlErrorHandler
    WaitRes = WaitForSingleObject(ProcHandle, DEFAULT_POLL_INTERVAL)
    while not (WaitRes == __WAIT_OBJECT_0):
        DoEvents()
        if (WaitRes == __WAIT_ABANDONED):
            # Windows abandoned the wait
            fn_return_value = SysWaitAbandoned
            break
        elif (WaitRes == __WAIT_OBJECT_0):
            # Successful completion
            fn_return_value = Success
            break
        elif (WaitRes == __WAIT_FAILED):
            # attach failed
            fn_return_value = Failure
            break
        elif (WaitRes == __WAIT_TIMEOUT):
            # Wait timed out. Here, this time out is on DEFAULT_POLL_INTERVAL.
            # See if ElapsedTime is greater than the user specified wait
            # time out. If we have exceed that, get out with a TimeOut status.
            # Otherwise, reissue as wait and continue.
            ElapsedTime = ElapsedTime + DEFAULT_POLL_INTERVAL
            if ms > 0:
                # user specified timeout
                if ElapsedTime > ms:
                    fn_return_value = Timeout
                    break
                else:
                    # user defined timeout has not expired.
                    pass
            else:
                # infinite wait -- do nothing
                pass
            # reissue the Wait on ProcHandle
            WaitRes = WaitForSingleObject(ProcHandle, DEFAULT_POLL_INTERVAL)
        else:
            # unknown result, assume failure
            fn_return_value = Failure
            break
            Quit = True
    CloseHandle(ProcHandle)
    Application.EnableCancelKey = SaveCancelKey
    return fn_return_value

    Debug.Print('ErrH: Cancel: ' + Application.EnableCancelKey)
    if Err.Number == ERR_BREAK_KEY:
        if BreakKey == ActionOnBreak.AbandonWait:
            CloseHandle(ProcHandle)
            fn_return_value = ShellAndWaitResult.UserWaitAbandoned
            Application.EnableCancelKey = SaveCancelKey
            return fn_return_value
        elif BreakKey == ActionOnBreak.IgnoreBreak:
            Err.Clear()
            # VB2PY (UntranslatedCode) Resume
        elif BreakKey == ActionOnBreak.PromptUser:
            MsgRes = MsgBoxMov('User Process Break.' + vbCrLf + 'Continue to wait?', vbYesNo)
            if MsgRes == vbNo:
                CloseHandle(ProcHandle)
                fn_return_value = ShellAndWaitResult.UserBreak
                Application.EnableCancelKey = SaveCancelKey
            else:
                Err.Clear()
                # VB2PY (UntranslatedCode) Resume Next
        else:
            CloseHandle(ProcHandle)
            Application.EnableCancelKey = SaveCancelKey
            fn_return_value = ShellAndWaitResult.Failure
    else:
        # some other error. assume failure
        CloseHandle(ProcHandle)
        fn_return_value = ShellAndWaitResult.Failure
    Application.EnableCancelKey = SaveCancelKey
    return fn_return_value
    """

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Option Compare Text
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function WaitForSingleObject Lib "kernel32" (ByVal hHandle As LongPtr, ByVal dwMilliseconds As LongLong) As LongLong

## VB2PY (CheckDirective) VB directive took path 1 on VBA7
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function OpenProcess Lib "kernel32" (ByVal dwDesiredAccess As Long, ByVal bInheritHandle As Long, ByVal dwProcessId As Long) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function CloseHandle Lib "kernel32" (ByVal hObject As Long) As Long
## VB2PY (CheckDirective) VB directive took path 1 on Win64
