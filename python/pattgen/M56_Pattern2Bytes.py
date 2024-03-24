from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M30_Tools as M30
import pattgen.M55_PWM_Data_Send

""" Convert a Pattern string to a byte array
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 XPatternT11(#LED,128,SI_LocalVar,4,0,128,0,0,500 ms,500 ms,500 ms,500 ms,500 ms,500 ms,500 ms,500 ms,200 ms,500 ms,200 ms,32,64,80,160,42,2  ,0,63,128,63,128,63,128,64,0,0,1)
 List of replacements for converting the pattern Macro
 Each entry has two parts separated by '>'
 The Entries are separated by ','
 This config Array:
   MobaLedLib_Configuration()
    {
    // KS_Hauptsignal_Zs3_Zs1
    XPatternT11(0,128,SI_LocalVar,4,0,255,0,0,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,32,64,80,160,42,2  ,0,63,128,63,128,63,128,64,0,0,1)     // KS_Hauptsignal_Zs3_Zs1
    EndCfg // End of the configuration
    }
 Is stored as this byte sequence
 50, 0, 128, 254, 255, 4, 0, 255, 0, 8, 200, 0, 244, 1, 200, 0, 244, 1, 200, 0, 244, 1, 200, 0, 244, 1, 200, 0, 244, 1, 200, 0, 17, 0, 32, 64, 80, 160, 42, 2, 0, 63, 128, 63, 128, 63, 128, 64, 0, 0, 1, 0,
 Ram Usage:
 ~~~~~~~~~~
 PatternTx():   5 Byte,             Typ: 10-39
 APatternT1():  7 Byte,             Typ: 40-69
 XPatternT1():  7+LedCnt Byte+LEDs, Typ: 40-69 and Mode contains "_PF_XFADE"
-----------------------------------
--------------------------------------------------------------------
UT---------------------------
-------------------------------------------------------------------------------
------------------------------------------------------
UT----------------------------
---------------------------------------------------------------------
-----------------------------------------------
"""

ReplaceList = 'SI_LocalVar > 254, SI_0 > 254, SI_1 > 255, ) > ,'

def ExitError(Txt):
    #-----------------------------------
    Debug.Print(Txt)
    M30.EndProg()

def Get_Mode_Nr(Par, XMode):
    _fn_return_value = None
    ModeList = 'PM_NORMAL              = 0,' + 'PM_SEQUENZ_W_RESTART   = 1,' + 'PM_SEQUENZ_W_ABORT     = 2,' + 'PM_SEQUENZ_NO_RESTART  = 3,' + 'PM_SEQUENZ_STOP        = 4,' + 'PM_PINGPONG            = 5,' + 'PM_HSV                 = 6,' + 'PM_RES                 = 7,' + '_PF_XFADE              = &H08,' + 'PF_NO_SWITCH_OFF       = &H10,' + 'PF_EASEINOUT           = &H20,' + 'PF_SLOW                = &H40,' + 'PF_INVERT_INP          = &H80,' + '0X                     = &H,' + '0x                     = &H'

    ModePair = Variant()

    ConvPar = String()

    Res = Byte()

    NrStr = Variant()
    #--------------------------------------------------------------------
    ConvPar = Par
    for ModePair in Split(ModeList, ','):
        Parts = Split(ModePair, '=')
        ConvPar = Replace(ConvPar, Trim(Parts(0)), Trim(Parts(1)))
    for NrStr in Split(ConvPar, '|'):
        NrStr = Trim(NrStr)
        if not IsNumeric(NrStr):
            ExitError('Wrong entry \'' + NrStr + '\' in Mode Sting \'' + Par + '\'')
        Res = Res or Val(NrStr)
    if XMode:
        Res = Res or 0x8
    _fn_return_value = Res
    return _fn_return_value

def Test_Get_Mode_Nr():
    #UT---------------------------
    Debug.Print(Hex(Get_Mode_Nr('PM_SEQUENZ_W_RESTART|PF_NO_SWITCH_OFF|0x40', True)))

def Get_Enable_Input(PatternName, Parm):
    _fn_return_value = None
    #-------------------------------------------------------------------------------
    _select50 = Parm
    if (_select50 == 'SI_Enable_Sound'):
        _fn_return_value = 253
    else:
        # Is it a number
        if IsNumeric(Parm):
            _fn_return_value = Val(Parm)
        else:
            ExitError('Unknown Enable input \'' + Parm + '\'')
    return _fn_return_value

def Convert_Time(Parm):
    _fn_return_value = None
    ms = Long()
    #------------------------------------------------------
    ms = M30.Convert_TimeStr_to_ms(Parm)
    if ms < 0:
        ExitError('Error converting the time \'' + Parm + '\'')
    else:
        if ms >= 65536:
            ExitError('Fehler die Zeit \'' + Parm + '\' ist zu groß')
        _fn_return_value = M30.Long_to_2ByteStr(ms)
    return _fn_return_value

def Test_Convert_Time():
    #UT----------------------------
    Debug.Print(Convert_Time('500 ms'))
    # 244, 1
    #Debug.Print Convert_Time("200 ms")
    # 200, 0

def Convert_PatternStr_to_ByteStr(Txt):
    _fn_return_value = None
    PatternName = String()

    PMode = String()

    Res = String()

    PatternPos = Integer()

    FirstTypNr = Integer()

    TimeCnt = Integer()

    HasEnableInp = Boolean()

    ParamsStr = String()

    GotoMode = Boolean()

    CommentPos = Integer()

    Params = vbObjectInitialize(objtype=String)

    Nr = Integer()

    PModeNr = Integer()

    LEDs = Integer()

    Mode = Byte()
    #---------------------------------------------------------------------
    # Convert a pattern string to a string of byte numbers
    # Example:
    #    XPatternT11(0,128,SI_LocalVar,4,0,255,0,0,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,32,64,80,160,42,2  ,0,63,128,63,128,63,128,64,0,0,1)
    # =>
    #    50, 0, 128, 254, 255, 4, 0, 255, 0, 8, 200, 0, 244, 1, 200, 0, 244, 1, 200, 0, 244, 1, 200, 0, 244, 1, 200, 0, 244, 1, 200, 0, 17, 0, 32, 64, 80, 160, 42, 2  , 0, 63, 128, 63, 128, 63, 128, 64, 0, 0, 1,
    #
    pattgen.M55_PWM_Data_Send.Check_if_C_Code_Version_is_Set()
    PatternName = Split(Txt, '(')(0)
    PatternPos = InStr(PatternName, 'PatternT')
    if PatternPos == 0:
        ExitError('PatternName \'' + PatternName + '\' doesn\'t contain the word \'Pattern\'')
    _select51 = Left(PatternName, 1)
    if (_select51 == 'X'):
        PMode = 'X'
        FirstTypNr = pattgen.M55_PWM_Data_Send.APATTERNT1_T
        # #define APATTERNT1_T  40  Flag "_PF_XFADE" is set if XPattern is used
    elif (_select51 == 'A'):
        PMode = 'A'
        FirstTypNr = pattgen.M55_PWM_Data_Send.APATTERNT1_T
        # #define APATTERNT1_T  40
    elif (_select51 == 'P'):
        PMode = 'P'
        FirstTypNr = pattgen.M55_PWM_Data_Send.PATTERNT1_T
        # #define  PATTERNT1_T  10
    else:
        ExitError('Unknown Pattern Typ: \'' + PatternName + '\'')
    # Byte 1
    HasEnableInp = InStr(PatternName, 'PatternTE') > 0
    if HasEnableInp:
        TimeCnt = Val(Mid(PatternName, PatternPos + Len('PatternTE')))
    else:
        TimeCnt = Val(Mid(PatternName, PatternPos + Len('PatternT')))
    if TimeCnt == 0:
        ExitError('Fehler beim Einlesen der Zeitabschnitte von \'' + PatternName + '\'')
    Res = Res + FirstTypNr + TimeCnt - 1 + ', '
    ParamsStr = Split(Txt, '(')(1)
    GotoMode = InStr(ParamsStr, 'SI_LocalVar') > 0
    ParamsStr = M30.Replace_Const(ParamsStr, ReplaceList, ',', '>')
    # Replace string like "SI_LocalVar", "ms", ...
    CommentPos = InStr(ParamsStr, '//')
    if CommentPos > 0:
        ParamsStr = Trim(Left(ParamsStr, CommentPos - 1))
    Params = Split(ParamsStr, ',')
    # Copy the first 7 parameter (If "PatternTE" copy 8)
    # 0    1      2     (3)   3     4     5     6     7
    # LED, NStru, InCh, SI_1, LEDs, Val0, Val1, Off, Mode|_PF_XFADE,_T2B(T1),_W2B(COUNT_VARARGS(__VA_ARGS__)), __VA_ARGS__,
    Res = Res + '0, '
    # First RGB LED must always be 0 otherwise the Charliplexing module cashes and the EEPROM has to be deleted
    # 05.06.20:
    Nr = 1
    if InStr(PatternName, 'PatternTE') > 0:
        PModeNr = 8
    else:
        PModeNr = 7
    while Nr < PModeNr:
        if Nr == 3:
            if InStr(PatternName, 'PatternTE') > 0:
                Res = Res + Get_Enable_Input(PatternName, Trim(Params(Nr))) + ', '
                Nr = Nr + 1
            else:
                Res = Res + '255, '
                # SI_1 = 255
            LEDs = Val(Params(Nr))
        Res = Res + Params(Nr) + ', '
        Nr = Nr + 1
    # Mode
    Mode = Get_Mode_Nr(Params(Nr), PMode == 'X')
    Res = Res + Mode + ', '
    Nr = Nr + 1
    # Time parameter
    for Nr in vbForRange(Nr, Nr + TimeCnt - 1):
        Res = Res + Convert_Time(Params(Nr)) + ', '
    Nr +=1 #*HL Loopvariable adapation to VBA behavior
    Res = Res + M30.Long_to_2ByteStr(UBound(Params) + 1 - Nr) + ', '
    # Number of remaining parameters
    # copy the remaining parameter (Data bytes and Goto Tab)
    while Nr <= UBound(Params):
        Res = Res + Params(Nr) + ', '
        Nr = Nr + 1
    _fn_return_value = Res
    return _fn_return_value

def Test_Convert_PatternStr_to_ByteStr():
    #-----------------------------------------------
    Debug.Print(Convert_PatternStr_to_ByteStr('XPatternT11(0,128,SI_LocalVar,4,0,255,0,0,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,32,64,80,160,42,2  ,0,63,128,63,128,63,128,64,0,0,1)'))
    #Debug.Print Convert_PatternStr_to_ByteStr("XPatternTE11(0,128,SI_LocalVar,SI_1,4,0,255,0,0,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,32,64,80,160,42,2  ,0,63,128,63,128,63,128,64,0,0,1)")

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Option Compare Binary
