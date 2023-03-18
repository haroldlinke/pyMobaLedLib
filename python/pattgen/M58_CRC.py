from vb2py.vbfunctions import *
from vb2py.vbdebug import *

""" https://foren.activevb.de/archiv/vba/thread-24525/beitrag-24974/Re-CRC-in-VBA/
-------------- Helper-Functions for Lookup-Table-Generation ----------------------
"""


def Crc6(B):
    _fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        CreateLookupTable(crcTab, 6, True, 0x6B)
    CRC = 63
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( CRC // 256 )
    _fn_return_value = CRC ^ 63
    return _fn_return_value

def Crc16(B):
    _fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        CreateLookupTable(crcTab, 16, True, 0x8005)
    CRC = 0
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( CRC // 256 )
    _fn_return_value = CRC
    return _fn_return_value

def Crc16_ModBus(B):
    _fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        CreateLookupTable(crcTab, 16, True, 0x8005)
    CRC = 0xFFFF
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( CRC // 256 )
    _fn_return_value = CRC
    return _fn_return_value

def Crc16_USB(B):
    _fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        CreateLookupTable(crcTab, 16, True, 0x8005)
    CRC = 0xFFFF
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( CRC // 256 )
    _fn_return_value = CRC ^ 0xFFFF
    return _fn_return_value

def Crc16_CCITT(B):
    _fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        CreateLookupTable(crcTab, 16, False, 0x1021)
    CRC = 0xFFFF
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = ( crcTab(( ( CRC // 256 )  ^ B(i) )  and 0xFF) ^  ( CRC * 256 ) )  and 0xFFFF
    _fn_return_value = CRC
    return _fn_return_value

def Crc16_CCITT_XModem(B):
    _fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        CreateLookupTable(crcTab, 16, False, 0x1021)
    CRC = 0
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = ( crcTab(( ( CRC // 256 )  ^ B(i) )  and 0xFF) ^  ( CRC * 256 ) )  and 0xFFFF
    _fn_return_value = CRC
    return _fn_return_value

def Crc16_CCITT_Kermit(B):
    _fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        CreateLookupTable(crcTab, 16, True, 0x1021)
    CRC = 0
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( CRC // 256 )
    _fn_return_value = CRC // 256 + 256 *  ( CRC and 0xFF ) 
    return _fn_return_value

def Crc32(B):
    _fn_return_value = None
    i = Long()

    CRC = Long()

    crcTab = vbObjectInitialize(((0, 255),), Long)
    if crcTab(1) == 0:
        CreateLookupTable(crcTab, 32, True, 0x4C11DB7)
    CRC = 0xFFFFFFFF
    for i in vbForRange(LBound(B), UBound(B)):
        CRC = crcTab(( CRC ^ B(i) )  and 0xFF) ^  ( ( ( CRC and 0xFFFFFF00 )  // 0x100 )  and 0xFFFFFF )
    _fn_return_value = CRC ^ 0xFFFFFFFF
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: BitLen - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Reflected - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Poly - ByVal 
def CreateLookupTable(crcTab, BitLen, Reflected, Poly):
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
            r = Reflect(V, IIf(BitLen < 8, BitLen, 8))
        if BitLen > 8:
            r = SHL(r, BitLen - 8)
        for i in vbForRange(0, IIf(BitLen < 8, BitLen, 8) - 1):
            if r and BM:
                r = SHL(r, 1) ^ Poly
            else:
                r = SHL(r, 1)
        if Reflected:
            r = Reflect(r, BitLen)
        if BitLen == 32:
            crcTab[V] = r
        else:
            crcTab[V] = r and CLng(2 ** BitLen - 1)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: V - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Bits - ByVal 
def Reflect(V, Bits):
    _fn_return_value = None
    i = Long()

    m = Long()
    _fn_return_value = V
    for i in vbForRange(0, Bits - 1):
        if ( Bits - i - 1 )  == 31:
            m = 0x80000000
        else:
            m = 2 **  ( Bits - i - 1 )
        _fn_return_value = IIf(V and 1, Reflect() or m, Reflect() and not m)
        V = SHR(V, 1)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Value - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Bits - ByVal 
def SHL(Value, Bits):
    _fn_return_value = None
    m = Long()
    if Bits == 0:
        _fn_return_value = Value
        return _fn_return_value
    m = 2 **  ( 31 - Bits )
    _fn_return_value = ( Value and  ( m - 1 ) )  * 2 ** Bits or IIf(Value and m, 0x80000000, 0)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Value - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Bits - ByVal 
@staticmethod
def SHR(Value, Bits):
    _fn_return_value = None
    if Value > 0:
        _fn_return_value = Value // 2 ** Bits
        return _fn_return_value
    _fn_return_value = ( ( Value and not 0x80000000 )  // 2 ** Bits )  or 2 **  ( 31 - Bits )
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
