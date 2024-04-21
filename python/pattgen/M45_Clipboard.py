from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLWA_WinAPI as X03
import ExcelAPI.XLA_Application as X02

""" https://www.spreadsheet1.com/how-to-copy-strings-to-clipboard-using-excel-vba.html
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
# VB2PY (CheckDirective) VB directive took path 1 on Win64
 18.12.19:
-----------------------------------------------------------------
UT---------------------------------
"""

GHND = 0x42
CF_TEXT = 1
MAXSIZE = 4096

def ClipBoard_SetData(sPutToClip):
    _fn_return_value = None
    hGlobalMemory = LongPtr()

    lpGlobalMemory = LongPtr()

    hClipMemory = LongLong()

    x = Long()
    #-----------------------------------------------------------------
    # www.msdn.microsoft.com/en-us/library/office/ff192913.aspx
    ## VB2PY (CheckDirective) VB directive took path 1 on Win64
    # 18.12.19:
    # VB2PY (UntranslatedCode) On Error GoTo ExitWithError_
    # Allocate moveable global memory
    hGlobalMemory = X03.GlobalAlloc(GHND, Len(sPutToClip) + 1)
    # Lock the block to get a far pointer to this memory
    lpGlobalMemory = X03.GlobalLock(hGlobalMemory)
    # Copy the string to this global memory
    lpGlobalMemory = X03.lstrcpy(lpGlobalMemory, sPutToClip)
    # Unlock the memory
    if X03.GlobalUnlock(hGlobalMemory) != 0:
        X02.MsgBox('Memory location could not be unlocked. Clipboard copy aborted', vbCritical, 'API Clipboard Copy')
        GoTo(ExitWithError_)
    # Open the Clipboard to copy data to
    if OpenClipboard(0) == 0:
        X02.MsgBox('Clipboard could not be opened. Copy aborted!', vbCritical, 'API Clipboard Copy')
        GoTo(ExitWithError_)
    # Clear the Clipboard
    x = X03.EmptyClipboard()
    # Copy the data to the Clipboard
    hClipMemory = X03.SetClipboardData(CF_TEXT, hGlobalMemory)
    _fn_return_value = True
    if X03.CloseClipboard() == 0:
        X02.MsgBox('Clipboard could not be closed!', vbCritical, 'API Clipboard Copy')
    return _fn_return_value
    # VB2PY (UntranslatedCode) On Error Resume Next
    if Err.Number > 0:
        X02.MsgBox('Clipboard error: ' + Err.Description, vbCritical, 'API Clipboard Copy')
    _fn_return_value = False
    return _fn_return_value

def Test_ClipBoard_SetData():
    #UT---------------------------------
    ClipBoard_SetData('Hallo Armin')

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Declare PtrSafe Function GlobalUnlock Lib "kernel32" (ByVal hMem As LongPtr) As LongPtr
# VB2PY (UntranslatedCode) Declare PtrSafe Function GlobalLock Lib "kernel32" (ByVal hMem As LongPtr) As LongPtr
# VB2PY (UntranslatedCode) Declare PtrSafe Function GlobalAlloc Lib "kernel32" (ByVal wFlags As LongPtr, ByVal dwBytes As LongPtr) As LongPtr
# VB2PY (UntranslatedCode) Declare PtrSafe Function CloseClipboard Lib "user32" () As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function OpenClipboard Lib "user32" (ByVal hWnd As LongPtr) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function EmptyClipboard Lib "user32" () As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function lstrcpy Lib "kernel32" (ByVal lpString1 As Any, ByVal lpString2 As Any) As Long
# VB2PY (UntranslatedCode) Declare PtrSafe Function SetClipboardData Lib "user32" (ByVal wFormat As LongPtr, ByVal hMem As LongPtr) As Long
