from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLWA_WinAPI as X03
import ExcelAPI.XLW_Workbook as X02
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.Pattern_Generator as PG

""" Mouse wheel support for list boxes
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


 Program combined from
  https://stackoverflow.com/questions/34911413/mouse-scroll-on-a-listbox
  https://www.ozgrid.com/forum/forum/help-forums/excel-general/128354-mouse-wheel-scroll-userform

 Hier eine weitere Lösung:
  http://www.office-loesung.de/ftopic174250_0_0_asc.php
 Hier wird von Problemen mit 32/64 Bit berichtet
 https://stackoverflow.com/questions/36621795/use-mouse-wheel-in-excel-dynamic-combobox-not-working-on-excel-2010
 Revision History:
 ~~~~~~~~~~~~~~~~~
 28.04.20: - Hopefully saved the MouseHook problem by storing the MouseHook to the worksheet

 Usage:
 ~~~~~~
 - Define the page whre the MouseHook is stored in a public modul:
    Public Const MouseHook_Store_Page = "Start"
 This page is used to store the MouseHook. There must be a named range called "MouseHook".

 Add the following calls to the UserForm code:
 - Call Cleare_Mouse_Hook() when the program is started !!!
 - To the initialisation of the user form:
     HookFormScroll Me, "ListBox"
 Initialize the mouse wheel scroll function

 - When the form is closed:
     UnhookFormScroll
 Deactivate the mouse weel scrol function

 - The following sub is called if the mouse wheel is changed
   It must be copied to the user form and adapted (Remove the #if ...)
# VB2PY (CheckDirective) VB directive took path 2 on False
 Disable this for debugging    29.04.20:
 Enable the Debug messages. The Error messages printed to the Debug window are always shown
 Overview 32 / 64 Bit functions: https://jkp-ads.com/Articles/apideclarations.asp
 https://stackoverflow.com/questions/45324586/using-setwindowshookex-in-excel-2010
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
For 64 Bit Systems
'# VB2PY (CheckDirective) VB2PY directive Ignore Text
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
   MSLLHOOKSTRUCT
   0    pt.X Long
   4    pt.Y Long
   8    mouseData Long  Holds Forward\Backward flag
   12   flags Long
   16   time Long
   20   dwExtraInfo Long
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
-----------------------------------------------------------------------------------------------------------
----------------------------
-----------------------------
------------------------------------------------
-------------------------------------------------
UT------------------
---------------------
----------------------------------------------------------
"""

ENABLE_CRITICAL_EVENTS_MOUSE = True
PRINT_MOUSE_DEBUG = False
HC_ACTION = 0
WH_MOUSE_LL = 14
WM_MOUSEWHEEL = 0x20A
GWL_HINSTANCE = ( - 6 )
nMyControlTypeNONE = 0
nMyControlTypeUSERFORM = 1
nMyControlTypeFRAME = 2
nMyControlTypeCOMBOBOX = 3
nMyControlTypeLISTBOX = 4
mLngMouseHook = LongPtr()
mFormHwnd = LongPtr()
class MouseHook_T:
    def __init__(self):
        self.V = LongPtr()

mbHook = Boolean()
mForm = Object()
mControllName = String()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lParam - ByVal 
def GetMouseData(lParam):
    _fn_return_value = None
    Value = Long()
    # offset of MouseData in MSLLHOOKSTRUCT is 8
    X03.CopyMemory(Value, lParam + 8, 4)
    _fn_return_value = Value
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: nCode - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: wParam - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lParam - ByVal 
def LowLevelMouseProc(nCode, wParam, lParam):
    global mbHook, mLngMouseHook
    _fn_return_value = None
    iDirection = Long()
    #-----------------------------------------------------------------------------------------------------------
    #Avoid XL crashing if RunTime error occurs due to Mouse fast movement
    # VB2PY (UntranslatedCode) On Error Resume Next
    # Unhook & get out in case the application is deactivated
    if mbHook == False and Is_Mouse_Hook_Stored():
        # 28.04.20:
        Debug.Print('!!! Disabling MouseHook after debug break !!!')
        mbHook = True
        mLngMouseHook = Read_Mouse_Hook.V
        UnhookFormScroll()
        return _fn_return_value
    if GetForegroundWindow == mFormHwnd:
        # Hardi
        if ( nCode == HC_ACTION ) :
            if wParam == WM_MOUSEWHEEL:
                iDirection = GetMouseData(lParam)
                mForm.MouseWheel(iDirection)
                # Don't process Default WM_MOUSEWHEEL Window message
                _fn_return_value = True
            return _fn_return_value
    _fn_return_value = CallNextHookEx(0, nCode, wParam, lParam)
    return _fn_return_value

def Save_Mouse_Hook():
    # 28.04.20:
    #----------------------------
    PG.ThisWorkbook.Sheets[M01.MouseHook_Store_Page].Range['MouseHook'] = "" #mLngMouseHook

def Cleare_Mouse_Hook():
    # 28.04.20:
    #-----------------------------
    PG.ThisWorkbook.Sheets[M01.MouseHook_Store_Page].Range['MouseHook'] = ''

def Read_Mouse_Hook():
    _fn_return_value = None
    # 28.04.20:
    #------------------------------------------------
    _fn_return_value.V = PG.ThisWorkbook.Sheets(M01.MouseHook_Store_Page).Range('MouseHook')
    return _fn_return_value

def Is_Mouse_Hook_Stored():
    _fn_return_value = None
    # 28.04.20:
    #-------------------------------------------------
    _fn_return_value = PG.ThisWorkbook.Sheets(M01.MouseHook_Store_Page).Range('MouseHook') != '' and IsNumeric(PG.ThisWorkbook.Sheets(M01.MouseHook_Store_Page).Range('MouseHook'))
    return _fn_return_value

def Test_MH():
    #UT------------------
    Debug.Print(Is_Mouse_Hook_Stored())
    Debug.Print(CLng(Read_Mouse_Hook().V))

def UnhookFormScroll():
    global mLngMouseHook, mFormHwnd, mbHook
    #---------------------
    if PRINT_MOUSE_DEBUG:
        Debug.Print('Mouse: UnhookFormScroll() called mbHook=' + mbHook)
    if mbHook:
        X03.UnhookWindowsHookEx(mLngMouseHook)
        mLngMouseHook = 0
        mFormHwnd = 0
        mbHook = False
        Cleare_Mouse_Hook()
        # 28.04.20:

def HookFormScroll(oForm, ControllName):
    global mForm, mControllName, mFormHwnd, mLngMouseHook, mbHook
    lngAppInst = LongPtr()

    hwndUnderCursor = LongPtr()
    #----------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on ENABLE_CRITICAL_EVENTS_MOUSE
    #'# VB2PY (CheckDirective) VB2PY directive Ignore Text
    #'# VB2PY (CheckDirective) VB2PY directive Ignore Text
    mForm = oForm
    hwndUnderCursor = X03.FindWindow('ThunderDFrame', oForm.Caption)
    if PRINT_MOUSE_DEBUG:
        Debug.Print('Mouse: HookFormScroll() Form window: ' + hwndUnderCursor)
    # Debug
    if mFormHwnd != hwndUnderCursor:
        mControllName = ControllName
        UnhookFormScroll()
        mFormHwnd = hwndUnderCursor
        #'# VB2PY (CheckDirective) VB2PY directive Ignore Text
        if mbHook:
            Debug.Print('!!! Mouse: Mouse was already hooked !!! => Don\'t hook it again ')
        else:
            mLngMouseHook = X03.SetWindowsHookEx(WH_MOUSE_LL, AddressOf(LowLevelMouseProc()), lngAppInst, 0)
            Save_Mouse_Hook()
            # Save the MouseHook to the worksheet to be able to restore it in case the program was aborted
            # 28.04.20:
            mbHook = mLngMouseHook != 0
            if mbHook:
                if PRINT_MOUSE_DEBUG:
                    Debug.Print('Mouse: Form hooked')
            else:
                Debug.Print('!!! Mouse: Error hook !!!')
    else:
        Debug.Print('!!! Mouse: Error mFormHwnd = hwndUnderCursor !!!')
    # ENABLE_CRITICAL_EVENTS_MOUSE

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function FindWindow Lib "user32" Alias "FindWindowA" (ByVal lpClassName As String, ByVal lpWindowName As String) As LongPtr
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function GetForegroundWindow Lib "user32.dll" () As LongPtr
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function UnhookWindowsHookEx Lib "user32" (ByVal hHook As LongPtr) As Long
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function SetWindowsHookEx Lib "user32" Alias "SetWindowsHookExA" (ByVal idHook As Long, ByVal lpFn As LongPtr, ByVal hmod As LongPtr, ByVal dwThreadId As Long) As LongPtr
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function CallNextHookEx Lib "user32" (ByVal hHook As LongPtr, ByVal nCode As Long, ByVal wParam As LongPtr, lParam As Any) As LongPtr
# VB2PY (UntranslatedCode) Private Declare PtrSafe Sub CopyMemory Lib "kernel32" Alias "RtlMoveMemory" (hpvDest As Any, hpvSource As Any, ByVal cbCopy As Long)
