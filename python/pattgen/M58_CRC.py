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


import proggen.Prog_Generator as PG

import ExcelAPI.P01_Workbook as P01

from ExcelAPI.X01_Excel_Consts import *


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

""" https://foren.activevb.de/archiv/vba/thread-24525/beitrag-24974/Re-CRC-in-VBA/
-------------- Helper-Functions for Lookup-Table-Generation ----------------------
"""


def Crc6(B):
    fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        __CreateLookupTable(crcTab, 6, True, 0x6B)
    CRC = 63
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( CRC // 256 )
    fn_return_value = CRC ^ 63
    return fn_return_value

def Crc16(B):
    fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        __CreateLookupTable(crcTab, 16, True, 0x8005)
    CRC = 0
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( CRC // 256 )
    fn_return_value = CRC
    return fn_return_value

def Crc16_ModBus(B):
    fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        __CreateLookupTable(crcTab, 16, True, 0x8005)
    CRC = 0xFFFF
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( CRC // 256 )
    fn_return_value = CRC
    return fn_return_value

def Crc16_USB(B):
    fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        __CreateLookupTable(crcTab, 16, True, 0x8005)
    CRC = 0xFFFF
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( CRC // 256 )
    fn_return_value = CRC ^ 0xFFFF
    return fn_return_value

def Crc16_CCITT(B):
    fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        __CreateLookupTable(crcTab, 16, False, 0x1021)
    CRC = 0xFFFF
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = ( crcTab(( ( CRC // 256 )  ^ B(i) )  and 0xFF) ^  ( CRC * 256 ) )  and 0xFFFF
    fn_return_value = CRC
    return fn_return_value

def Crc16_CCITT_XModem(B):
    fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        __CreateLookupTable(crcTab, 16, False, 0x1021)
    CRC = 0
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = ( crcTab(( ( CRC // 256 )  ^ B(i) )  and 0xFF) ^  ( CRC * 256 ) )  and 0xFFFF
    fn_return_value = CRC
    return fn_return_value

def Crc16_CCITT_Kermit(B):
    fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        __CreateLookupTable(crcTab, 16, True, 0x1021)
    CRC = 0
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( CRC // 256 )
    fn_return_value = CRC // 256 + 256 *  ( CRC and 0xFF ) 
    return fn_return_value

def Crc32(B):
    fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        __CreateLookupTable(crcTab, 32, True, 0x4C11DB7)
    CRC = 0xFFFFFFFF
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( ( ( CRC and 0xFFFFFF00 )  // 0x100 )  and 0xFFFFFF )
    fn_return_value = CRC ^ 0xFFFFFFFF
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: BitLen - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Reflected - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Poly - ByVal 
def __CreateLookupTable(crcTab, BitLen, Reflected, Poly):
    r = Long()

    i = Long()

    V = Long()

    BM = Long()
    if BitLen == 32:
        BM = 0x80000000
    else:
        BM = 2 **  ( BitLen - 1 )
    for V in vbForRange(0, UBound(crcTab)):
        r = V
        if Reflected:
            r = __Reflect(V, IIf(BitLen < 8, BitLen, 8))
        if BitLen > 8:
            r = __SHL(r, BitLen - 8)
        for i in vbForRange(0, IIf(BitLen < 8, BitLen, 8) - 1):
            if r and BM:
                r = __SHL(r, 1) ^ Poly
            else:
                r = __SHL(r, 1)
        if Reflected:
            r = __Reflect(r, BitLen)
        if BitLen == 32:
            crcTab[V] = r
        else:
            crcTab[V] = r and CLng(2 ** BitLen - 1)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: V - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Bits - ByVal 
def __Reflect(V, Bits):
    fn_return_value = None
    i = Long()

    m = Long()
    fn_return_value = V
    for i in vbForRange(0, Bits - 1):
        if ( Bits - i - 1 )  == 31:
            m = 0x80000000
        else:
            m = 2 **  ( Bits - i - 1 )
        fn_return_value = IIf(V and 1, __Reflect() or m, __Reflect() and not m)
        V = __SHR(V, 1)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Value - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Bits - ByVal 
def __SHL(Value, Bits):
    fn_return_value = None
    m = Long()
    if Bits == 0:
        fn_return_value = Value
        return fn_return_value
    m = 2 **  ( 31 - Bits )
    fn_return_value = ( Value and  ( m - 1 ) )  * 2 ** Bits or IIf(Value and m, 0x80000000, 0)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Value - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Bits - ByVal 
@staticmethod
def __SHR(Value, Bits):
    fn_return_value = None
    if Value > 0:
        fn_return_value = Value // 2 ** Bits
        return fn_return_value
    fn_return_value = ( ( Value and not 0x80000000 )  // 2 ** Bits )  or 2 **  ( 31 - Bits )
    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
