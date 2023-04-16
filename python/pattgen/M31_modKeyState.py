from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLWA_WinAPI as X03
import ExcelAPI.XLW_Workbook as X02

"""'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
 modKeyState
 By Chip Pearson, www.cpearson.com, chip@cpearson.com
 This module contains functions for testing the state of the SHIFT, ALT, and CTRL
 keys.

 http://www.cpearson.com/excel/keytest.aspx
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''
 Declaration of GetKeyState API function. This
 tests the state of a specified key.
'''''''''''''''''''''''''''''''''''''''''''''''''''
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
For 64 Bit Systems
 19.10.19:
'''''''''''''''''''''''''''''''''''''''''
 This constant is used in a bit-wise AND
 operation with the result of GetKeyState
 to determine if the specified key is
 down.
'''''''''''''''''''''''''''''''''''''''''
 decimal -128
''''''''''''''''''''''''''''''''''''''''
 KEY CONSTANTS. Values taken
 from VC++ 6.0 WinUser.h file.
''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''
 The following four constants simply
 provide other names, CTRL and ALT,
 for CONTROL and MENU. "CTRL" and
 "ALT" are more familiar than
 "CONTROL" and "MENU". These constants
 provide no additional functionality.
 They simply provide more familiar
 names.
''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''
 The following constants are used to specify,
 when testing CTRL, ALT, or SHIFT, whether
 the Left key, the Right key, either the
 Left OR Right, or BOTH the Left AND Right
 key is down.

 By default, the key-test procedures make
 no distinction between the Left and Right
 keys.
'''''''''''''''''''''''''''''''''''''''''''
 Note: Bit-wise AND of LeftKey and RightKey
 Note: Bit-wise OR of LeftKey and RightKey
UT---------------
UT-------------------
"""

KEY_MASK = 0xFF80
VK_LSHIFT = 0xA0
VK_RSHIFT = 0xA1
VK_LCONTROL = 0xA2
VK_RCONTROL = 0xA3
VK_LMENU = 0xA4
VK_RMENU = 0xA5
VK_LALT = VK_LMENU
VK_RALT = VK_RMENU
VK_LCTRL = VK_LCONTROL
VK_RCTRL = VK_RCONTROL
BothLeftAndRightKeys = 0
LeftKey = 1
RightKey = 2
LeftKeyOrRightKey = 3

def IsShiftKeyDown(LeftOrRightKey=LeftKeyOrRightKey):
    _fn_return_value = None
    Res = Long()
    #'''''''''''''''''''''''''''''''''''''''''''''''
    # IsShiftKeyDown
    # Returns TRUE or FALSE indicating whether the
    # SHIFT key is down.
    #
    # If LeftOrRightKey is omitted or LeftKeyOrRightKey,
    # the function return TRUE if either the left or the
    # right SHIFT key is down. If LeftKeyOrRightKey is
    # LeftKey, then only the Left SHIFT key is tested.
    # If LeftKeyOrRightKey is RightKey, only the Right
    # SHIFT key is tested. If LeftOrRightKey is
    # BothLeftAndRightKeys, the codes tests whether
    # both the Left and Right keys are down. The default
    # is to test for either Left or Right, making no
    # distiction between Left and Right.
    #'''''''''''''''''''''''''''''''''''''''''''''''
    _select21 = LeftOrRightKey
    if (_select21 == LeftKey):
        Res = X03.GetKeyState(VK_LSHIFT) and KEY_MASK
    elif (_select21 == RightKey):
        Res = X03.GetKeyState(VK_RSHIFT) and KEY_MASK
    elif (_select21 == BothLeftAndRightKeys):
        Res = ( X03.GetKeyState(VK_LSHIFT) and X03.GetKeyState(VK_RSHIFT) and KEY_MASK )
    else:
        Res = X03.GetKeyState(vbKeyShift) and KEY_MASK
    _fn_return_value = CBool(Res)
    return _fn_return_value

def IsControlKeyDown(LeftOrRightKey=LeftKeyOrRightKey):
    _fn_return_value = None
    Res = Long()
    #'''''''''''''''''''''''''''''''''''''''''''''''
    # IsControlKeyDown
    # Returns TRUE or FALSE indicating whether the
    # CTRL key is down.
    #
    # If LeftOrRightKey is omitted or LeftKeyOrRightKey,
    # the function return TRUE if either the left or the
    # right CTRL key is down. If LeftKeyOrRightKey is
    # LeftKey, then only the Left CTRL key is tested.
    # If LeftKeyOrRightKey is RightKey, only the Right
    # CTRL key is tested. If LeftOrRightKey is
    # BothLeftAndRightKeys, the codes tests whether
    # both the Left and Right keys are down. The default
    # is to test for either Left or Right, making no
    # distiction between Left and Right.
    #'''''''''''''''''''''''''''''''''''''''''''''''
    _select22 = LeftOrRightKey
    if (_select22 == LeftKey):
        Res = X03.GetKeyState(VK_LCTRL) and KEY_MASK
    elif (_select22 == RightKey):
        Res = X03.GetKeyState(VK_RCTRL) and KEY_MASK
    elif (_select22 == BothLeftAndRightKeys):
        Res = ( X03.GetKeyState(VK_LCTRL) and X03.GetKeyState(VK_RCTRL) and KEY_MASK )
    else:
        Res = X03.GetKeyState(vbKeyControl) and KEY_MASK
    _fn_return_value = CBool(Res)
    return _fn_return_value

def IsAltKeyDown(LeftOrRightKey=LeftKeyOrRightKey):
    _fn_return_value = None
    Res = Long()
    #'''''''''''''''''''''''''''''''''''''''''''''''
    # IsAltKeyDown
    # Returns TRUE or FALSE indicating whether the
    # ALT key is down.
    #
    # If LeftOrRightKey is omitted or LeftKeyOrRightKey,
    # the function return TRUE if either the left or the
    # right ALT key is down. If LeftKeyOrRightKey is
    # LeftKey, then only the Left ALT key is tested.
    # If LeftKeyOrRightKey is RightKey, only the Right
    # ALT key is tested. If LeftOrRightKey is
    # BothLeftAndRightKeys, the codes tests whether
    # both the Left and Right keys are down. The default
    # is to test for either Left or Right, making no
    # distiction between Left and Right.
    #'''''''''''''''''''''''''''''''''''''''''''''''
    _select23 = LeftOrRightKey
    if (_select23 == LeftKey):
        Res = X03.GetKeyState(VK_LALT) and KEY_MASK
    elif (_select23 == RightKey):
        Res = X03.GetKeyState(VK_RALT) and KEY_MASK
    elif (_select23 == BothLeftAndRightKeys):
        Res = ( X03.GetKeyState(VK_LALT) and X03.GetKeyState(VK_RALT) and KEY_MASK )
    else:
        Res = X03.GetKeyState(vbKeyMenu) and KEY_MASK
    _fn_return_value = CBool(Res)
    return _fn_return_value

def Test():
    #UT---------------
    #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Test
    # This is a procedrue to test and demonstrate the Key-State
    # functions above. Since you can't run a macro in the VBA
    # Editor if the SHIFT, ALT, or CTRL key is down, this procedure
    # uses OnTime to execute the ProcTest test procedure. OnTime
    # will call ProcTest two seconds after running this Test
    # procedure. Immediately after executing Test, press the
    # key(s) (Left/Right SHIFT, ALT, or CTRL) you want to test
    # for. The procedure called by OnTime, ProcTest, displays the
    # status of the Left/Right SHIFT, ALT, and CTRL keys.
    #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    X02.Application.OnTime(X02.Now + TimeSerial(0, 0, 2), 'ProcTest', VBGetMissingArgument(X02.Application.OnTime, 2), True)

def ProcTest():
    #UT-------------------
    #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # ProcTest
    # This procedure simply displays the status of the Left adn Right
    # SHIFT, ALT, and CTRL keys.
    #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Debug.Print('SHIFT KEY: ', 'LEFT: ' + CStr(IsShiftKeyDown(LeftKey)), 'RIGHT: ' + CStr(IsShiftKeyDown(RightKey)), 'EITHER: ' + CStr(IsShiftKeyDown(LeftKeyOrRightKey)), 'BOTH:   ' + CStr(IsShiftKeyDown(BothLeftAndRightKeys)))
    Debug.Print('ALT KEY:   ', 'LEFT: ' + CStr(IsAltKeyDown(LeftKey)), 'RIGHT: ' + CStr(IsAltKeyDown(RightKey)), 'EITHER: ' + CStr(IsAltKeyDown(LeftKeyOrRightKey)), 'BOTH:   ' + CStr(IsAltKeyDown(BothLeftAndRightKeys)))
    Debug.Print('CTRL KEY:   ', 'LEFT: ' + CStr(IsControlKeyDown(LeftKey)), 'RIGHT: ' + CStr(IsControlKeyDown(RightKey)), 'EITHER: ' + CStr(IsControlKeyDown(LeftKeyOrRightKey)), 'BOTH:   ' + CStr(IsControlKeyDown(BothLeftAndRightKeys)))

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Option Compare Text
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function GetKeyState Lib "user32" (ByVal nVirtKey As Long) As Integer
