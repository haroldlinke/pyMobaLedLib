# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
# * Author: Harold Linke
# * Date: January 1st, 2020
# * Copyright: Harold Linke 2020
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 10.03.2020 - Harold Linke - first release
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


def SetCommState(hCommDev,lpDCB):
    pass

def GetCommState(nCid, lpDCB):
    pass

def BuildCommDCB(lpDef, lpDCB):
    pass

def SetCommTimeouts(hFile, lpCommTimeouts):
    pass

def GetCommTimeouts(hFile, lpCommTimeouts):
    pass

def EscapeCommFunction(hFile, dwFunc):
    pass

def PurgeComm(hFile, dwFlags):
    pass
def GetDefaultCommConfig(lpszName, lpCC, lpdwSize ):
    pass

def CreateFile(lpFileName,ing,dwDesiredAccess,dwShareMode,SecurityAttributes,dwCreationDisposition,dwFlagsAndAttributes,hTemplateFile):
    pass

def CloseHandle(hObject):
    pass

def WriteFile(hFile,Buffer,nNumberOfBytesToWrite,lpNumberOfBytesWritten,lpOverlapped):
    pass

def ReadFile(hFile,Buffer,nNumberOfBytesToRead,lpNumberOfBytesRead,lpOverlapped):
    pass

def Sleep(dwMilliseconds):
    pass

def GetAsyncKeyState(vKey):
    pass

def SetForegroundWindow(hWnd):
    pass

def IsIconic(hWnd):
    pass

def AccessibleObjectFromWindow(hWnd,dwId,riid,ppvObject):
    pass

def FindWindowExA(hwndParent,hwndChildAfter,lpszClas,lpszWindow):
    pass

def WideCharToMultiByte( CodePage,dwFlags,lpWideCharStr,cchWideChar,lpMultiByteStr,cbMultiByte,lpDefaultChar,lpUsedDefaultChar):
    pass
def MultiByteToWideChar(CodePage,dwFlags,lpMultiByteStr,cchMultiByte,lpWideCharStr,cchWideChar):
    pass

def GetKeyState(nVirtKey):
    return False
    pass

def FindWindow (lpClassName,lpWindowName):
    pass

def UnhookWindowsHookEx(hHook):
    pass

def SetWindowsHookEx(idHook,lpFn,hmod,dwThreadId):
    pass

def CopyMemory(hpvDest,hpvSourcey,cbCopy):
    pass

def WaitForSingleObject(hHandle,dwMilliseconds):
    pass

def CloseHandle(hObject):
    pass

def GlobalUnlock(hMem):
    pass

def GlobalLock(hMem):
    pass

def GlobalAlloc(wFlags,dwBytes):
    pass

def CloseClipboard():
    pass

def EmptyClipboard():
    pass

def lstrcpy(lpString1,lpString2):
    pass

def SetClipboardData(wFormat,hMem):
    pass

def GetPrivateProfileString(lpApplicationName,lpKeyName,lpDefault,lpReturnedString,nSize,lpFileName):
    pass

def WritePrivateProfileString (lpApplicationName,lpKeyName,lpString,lpFileName):
    pass

def GetPrivateProfileInt(lpApplicationName,lpKeyName,nDefault,lpFileName):
    pass

def GetPrivateProfileSection(lpAppName,lpReturnedString,nSize,lpFileName):
    pass

def GetPrivateProfileSectionNames(lpSectionNames,nSize,lpFileName):
    pass

def WritePrivateProfileSection(lpAppName,lpString,lpFileName):
    pass