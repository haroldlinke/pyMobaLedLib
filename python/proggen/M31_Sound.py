# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
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

import ExcelAPI.XLA_Application as P01

import proggen.M02_Public as M02
#import proggen.M02_global_variables as M02GV
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header as M06
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
#import proggen.M07_COM_Port as M07
#import proggen.M08_ARDUINO as M08
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
import proggen.M80_Create_Multiplexer as M80

import mlpyproggen.Prog_Generator as PG

""" https://wellsr.com/vba/2019/excel/vba-playsound-to-play-system-sounds-and-wav-files/
# VB2PY (CheckDirective) VB directive took path 1 on VBA7
-------------------------------------------------------------------------
"""

__SND_SYNC = 0x0
__SND_ASYNC = 0x1
__SND_NODEFAULT = 0x2
__SND_NOSTOP = 0x10
__SND_ALIAS = 0x10000
__SND_FILENAME = 0x20000

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ThisSound='Beep' - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ThisValue=VBMissingArgument - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ThisCount=1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Wait=False - ByVal 
def BeepThis2(ThisSound='Beep', ThisValue=VBMissingArgument, ThisCount=1, Wait=False):
    return #*HL
    fn_return_value = None
    sPath = String()
    flags = int()
    sMedia = '\\Media\\'
    if IsMissing(ThisValue):
        ThisValue = ThisSound
    fn_return_value = ThisValue
    if ThisCount > 1:
        Wait = True
    flags = __SND_ALIAS
    sPath = StrConv(ThisSound, vbProperCase)
    if (sPath == 'Beep'):
        Beep()
        # ignore ThisCount and Wait
        return fn_return_value
    elif (sPath == 'Asterisk') or (sPath == 'Exclamation') or (sPath == 'Hand') or (sPath == 'Notification') or (sPath == 'Question'):
        sPath = 'System' + sPath
    elif (sPath == 'Connect') or (sPath == 'Disconnect') or (sPath == 'Fail'):
        sPath = 'Device' + sPath
    elif (sPath == 'Mail') or (sPath == 'Reminder'):
        sPath = 'Notification.' + sPath
    elif (sPath == 'Text'):
        sPath = 'Notification.SMS'
    elif (sPath == 'Message'):
        sPath = 'Notification.IM'
    elif (sPath == 'Fax'):
        sPath = 'FaxBeep'
    elif (sPath == 'Select'):
        sPath = 'CCSelect'
    elif (sPath == 'Error'):
        sPath = 'AppGPFault'
    elif (sPath == 'Close') or (sPath == 'Maximize') or (sPath == 'Minimize') or (sPath == 'Open'):
        # ok
        pass
    elif (sPath == 'Default'):
        sPath = '.' + sPath
    elif (sPath == 'Chimes') or (sPath == 'Chord') or (sPath == 'Ding') or (sPath == 'Notify') or (sPath == 'Recycle') or (sPath == 'Ringout') or (sPath == 'Tada'):
        sPath = Environ('SystemRoot') + sMedia + sPath + '.wav'
        flags = __SND_FILENAME
    else:
        if LCase(Right(ThisSound, 4)) != '.wav':
            ThisSound = ThisSound + '.wav'
        sPath = ThisSound
        if Dir(sPath) == '':
            # file is not in working directory
            sPath = P01.ActiveWorkbook.Path + '/' + ThisSound
            if Dir(sPath) == '':
                sPath = Environ('SystemRoot') + sMedia + ThisSound
        flags = __SND_FILENAME
    flags = flags + IIf(Wait, __SND_SYNC, __SND_ASYNC)
    while ThisCount > 0:
        # skip if ThisCount < 1
        PlaySound(sPath, 0, flags)
        # if error, .Default sound will play
        ThisCount = ThisCount - 1
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ThisSound='Beep' - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ThisValue=VBMissingArgument - ByVal 
def BeepThis1(ThisSound='Beep', ThisValue=VBMissingArgument):
    fn_return_value = None
    #-------------------------------------------------------------------------
    if IsMissing(ThisValue):
        ThisValue = ThisSound
    fn_return_value = ThisValue
    Beep()
    return fn_return_value

def __Test_BeepThis1():
    #BeepThis2 "Default"
    #BeepThis2 "Asterisk"
    #BeepThis2 "Fax"
    BeepThis2('Windows Information Bar.wav', VBGetMissingArgument(BeepThis2(), 1), VBGetMissingArgument(BeepThis2(), 2), True)

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Public Declare PtrSafe Function PlaySound Lib "winmm.dll" Alias "PlaySoundA" (ByVal lpszName As String, ByVal hModule As LongPtr, ByVal dwFlags As Long) As Long
