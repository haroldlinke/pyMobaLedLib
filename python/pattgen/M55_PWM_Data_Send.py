from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import pattgen.M30_Tools as M30
import pattgen.M57_modCOMM
import ExcelAPI.XLWA_WinAPI as X03
import pattgen.M09_Language
import pattgen.M56_Pattern2Bytes
import pattgen.M58_CRC
import proggen.M07_COM_Port
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M60_Select_LED
import pattgen.M11_To_Prog_Gen
import pattgen.M06_Goto_Graph
import pattgen.Pattern_Generator as PG

""" Send data over the WS281x LED protokol
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Die Daten werden als LED PWM Signale zum Charliplexing Arduino übertragen.

 Da die Erkennung des PWM Signals durch die Interrupts der Charliplexing LEDs stark verrauscht ist
 müssen die Bereiche mit denen ein Wert übertragen wird relativ breit sein.
 Für die Signale verwende ich 20 PWM Werte Abstand. Ein PWM Wert zwischen 36 und 55 wird als "Goto" Nummer 0
 interpretiert, Die "Goto" Nummer 1 entspricht dem Bereich 56 - 75. Dadurch ergeben sich 11 Bereiche.
 Das reicht aber nicht für die Datenübertragung.
 Die Daten sollen ohne feste Zeitabstände gesendet werden. Darum wird eine Methode zur Erkennung benötigt
 wann ein neues Datenpaket bekommt. Dazu wird das höchstwertigste Bit benutzt welches bei jedem Paket seinen
 Wert wechselt.
 Während
 Waiting time between two data nibbles [ms]
 50 is sometime to fast, 100 is working with 256 LED's
 => 100 Byte = 20 Sec (8 Bit Signal has 88 Byte, 1 Bit Signal 40 Byte = 8 Sec)
 24.05.20: Increased delay because of the additional delay in the LEDs_Autoproc for the COM port detection. Old: 300
 Enable the analog input
 Table with analog limits which defines the Goto Nr levels
 Die Folgenden WS... Konstanten waren ursprünglich dafür gedacht, dass die Anzahl der übertragenen Bits
 verändern kann. Das wurde aber nicht konsequent umgesetzt weil die Übertragung von 4 Bit ganz gut passt.
 => Die Konstannten dürfen nicht verändert werden
 Number of used bits per package in Write_As_Bits(). The MarkBit is used in addition
 15 = 0xFF
 16
    0  1  2  3  4  5  6   7   8  9 10 11
---------------------------------------------------
------------------------------------------
-------------------------------------
---------------------------------------------------------------------
--------------------------------------------
----------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------
----------------------------------------
-----------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 2 on False
--------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
--------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------
--------------------------------------------------------------------------------------------
UT------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------
--------------------------------------------------------
--------------------------------------------
-------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------
UT-------------------------------
 Es ist zwei mal passiert, das die Übertragung zum ATTiny abgebrochen wurde.      30.12.19:
 Dabei hört das Flackern der LEDs mitten drinnen auf ?!?
----------------------------------------------------------------------------------------------------------------
UT-------------------------------------------------
--------------------------------------------------------------
UT------------------------------------
--------------------------------------------------------------------------------------------------------------
----------------------------------
----------------------------------------------------------------
-------------------------------
-------------------------------
"""

DEBUG_SEND = False
WaitTime = 100
WaitTime_Start = 1800
WaitTime_Begin = 300
CPX_LED_ASSIGNEMENT = Byte()
CPX_ANALOG_INPUT = Byte()
CPX_ANALOG_LIMMITS = Byte()
CP_HEAD_VERSION = String()
ExpectedResponse = '#?LEDs_AutoProg Ver 1: '
PATTERNT1_T = Byte()
APATTERNT1_T = Byte()
ANALOG_KEYS = 10
Bit_Scale = 7
Bit_Offset = 30
WB_BitCnt = 4
WB_Mask = ( 2 ** WB_BitCnt )  - 1
WB_MarkBit = 2 ** WB_BitCnt
WB_Buffer = Integer()
WB_Remaining = Integer()
WB_HighBit = Boolean()
Enable_Analog_Inputs = Boolean()
Analog_Limmits_Str = String()
CRC_ByteList = vbObjectInitialize(objtype=Byte)
VIESSMN_LED_ASSIGNEMENT = String()
UNIPROG_LED_ASSIGNEMANT = String()
REVERSE_LED_ASSIGNEMENT = String()
BRIGHT6_LED_ASSIGNEMENT = String()

def Set_Used_C_Code_Version(Version):
    global CP_HEAD_VERSION, PATTERNT1_T, APATTERNT1_T, CPX_LED_ASSIGNEMENT, CPX_ANALOG_INPUT, CPX_ANALOG_LIMMITS
    #---------------------------------------------------
    _select42 = Version
    if (_select42 == 1):
        CP_HEAD_VERSION = 'CP1'
        PATTERNT1_T = 10
        APATTERNT1_T = 40
        CPX_LED_ASSIGNEMENT = 140
        CPX_ANALOG_INPUT = 141
        CPX_ANALOG_LIMMITS = 142
    elif (_select42 == 2):
        CP_HEAD_VERSION = 'CP2'
        PATTERNT1_T = 10
        APATTERNT1_T = 74
        CPX_LED_ASSIGNEMENT = 200
        CPX_ANALOG_INPUT = 201
        CPX_ANALOG_LIMMITS = 202
    else:
        X02.MsgBox('Internal Error: Undefined version in \'Set_Used_C_Code_Version()\':' + Version, vbCritical, 'Internal Error')
        M30.EndProg()

def Check_if_C_Code_Version_is_Set():
    #------------------------------------------
    if CPX_ANALOG_INPUT == 0:
        X02.MsgBox('Internal Error: \'Set_Used_C_Code_Version()\' not called ;-(', vbCritical, 'Internal Error')
        M30.EndProg()

def Init_Assignement_Strings():
    global VIESSMN_LED_ASSIGNEMENT, UNIPROG_LED_ASSIGNEMANT, REVERSE_LED_ASSIGNEMENT, BRIGHT6_LED_ASSIGNEMENT
    #-------------------------------------
    if VIESSMN_LED_ASSIGNEMENT == '':
        #    0  1  2  3  4  5  6   7   8  9 10 11
        VIESSMN_LED_ASSIGNEMENT = LED_Assignement(8, 6, 7, 3, 0, 1, 2, 10, 11, 4, 5, 9)
        # Viessmann Multiplex (8 und 9 konnte ich nicht prüfen)
        UNIPROG_LED_ASSIGNEMANT = LED_Assignement(0, 1, 8, 9, 11, 10, 3, 2, 4, 5, 7, 6)
        # LED Numbers see Tiny_UniProg_Sch2.pdf
        REVERSE_LED_ASSIGNEMENT = LED_Assignement(11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
        # Reverse Test Board
        BRIGHT6_LED_ASSIGNEMENT = LED_Assignement(0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5)
        # 6 Bright LEDS: One LED is controlled by two LED channels => The brightness could be doubled

def Write_Com(PortId, Txt):
    _fn_return_value = None
    Size = Long()

    Status = Integer()
    #---------------------------------------------------------------------
    Size = Len(Txt)
    Status = pattgen.M57_modCOMM.CommWrite(PortId, Txt)
    if DEBUG_SEND:
        Debug.Print(' Write_Com: ' + Txt)
    # Debug
    if Status != Size:
        Debug.Print('Error ' + Status + ' in CommWrite')
        # Handle error.
    else:
        _fn_return_value = True
    return _fn_return_value

def Debug_Read_Com(PortId):
    Status = Integer()

    strData = String()
    #--------------------------------------------
    # Read maximum of 64 bytes from serial port.
    Status = pattgen.M57_modCOMM.CommRead(PortId, strData, 64)
    if Status > 0:
        # Process data.
        if DEBUG_SEND:
            Debug.Print(strData)
    elif Status < 0:
        Debug.Print('Error')

def Wait_Until_Arduino_Responds(PortId, WaitMsg, Timeout):
    _fn_return_value = None
    Status = Integer()

    strData = String()

    AllData = String()

    t = Long()

    Cnt = Long()

    DelayTime = 50
    #----------------------------------------------------------------------------------------------------------------
    while t < Timeout:
        Status = pattgen.M57_modCOMM.CommRead(PortId, strData, 64)
        if Status > 0:
            # Process data.
            if Len(strData) > 0:
                AllData = AllData + strData
        elif Status < 0:
            Debug.Print('Error in Wait_Until_Arduino_Responds(): ' + Status)
            return _fn_return_value
        if Len(AllData) > 0 and InStr(AllData, WaitMsg) > 0:
            Cnt = Cnt + 1
            if Cnt >= 2:
                # Wait until the rest is read
                if DEBUG_SEND:
                    Debug.Print('Wait for the Arduino ' + t + ' ms')
                _fn_return_value = AllData
                return _fn_return_value
        t = t + DelayTime
        if t < Timeout:
            X03.Sleep(DelayTime)
    return _fn_return_value

def Open_Port_with_Error_Msg(PortId, withReset):
    _fn_return_value = None
    Status = Long()

    strError = String()
    #----------------------------------------------------------------------
    # Initialize Communications
    Status = pattgen.M57_modCOMM.CommOpen(PortId, 'baud=115200 parity=N data=8 stop=1 dtr=off')
    Debug.Print('CommOpen(' + PortId + ')')
    if Status != 0:
        # Handle error.
        Status = pattgen.M57_modCOMM.CommGetError(strError)
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler beim verbinden mit dem Arduino über COM') + PortId + vbCr + '  ' + strError + vbCr + pattgen.M09_Language.Get_Language_Str('Evtl. ist der Port bereits von einem anderen Programm (Arduino IDE, Farbtest, serieller Monitor) belegt.' + vbCr + 'Falls das Excel Programm vorher mit einer Fehlermeldung abgebrochen wurde, dann kann es sein, ' + 'dass der Port nicht richtig geschlossen wurde. In dem Fall müssen alle Excel Fenster geschlossen werden ;-('), vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler beim öffnen des COM Ports'))
        Close_Port(PortId)
    else:
        if withReset:
            pattgen.M57_modCOMM.CommSetLine(PortId, pattgen.M57_modCOMM.LINE_RTS, True)
            pattgen.M57_modCOMM.CommSetLine(PortId, pattgen.M57_modCOMM.LINE_DTR, True)
        _fn_return_value = True
    return _fn_return_value

def Close_Port(PortId):
    #----------------------------------------
    X03.Sleep(( 100 ))
    # Process remaining characters
    # Reset modem control lines.
    pattgen.M57_modCOMM.CommSetLine(PortId, pattgen.M57_modCOMM.LINE_RTS, False)
    pattgen.M57_modCOMM.CommSetLine(PortId, pattgen.M57_modCOMM.LINE_DTR, False)
    pattgen.M57_modCOMM.CommClose(PortId)
    # Close communications.
    if DEBUG_SEND:
        Debug.Print('Close_Port(' + PortId + ')')

def Scale_Bits(Val):
    _fn_return_value = None
    #-----------------------------------------------------
    _fn_return_value = Val * Bit_Scale + Bit_Offset
    return _fn_return_value

def Send_LED_PWM(PortId, pwm, LedNr, LEDCnt):
    _fn_return_value = None
    Part = Variant()

    LedCntStr = String()

    LeadStr = String()

    TailStr = String()

    LED_PWM = String()
    #--------------------------------------------------------------------------------------------------------
    # Send pwm to all 3 Channels (RGB)
    # 30.01.20: prior only the Green and blue channel was used (Blue LED as status indicator)
    #
    LedCntStr = M30.Hex02(LEDCnt)
    LeadStr = '#L' + M30.Hex02(LedNr)
    # & " 00 "
    LED_PWM = ' ' + M30.Hex02(pwm)
    TailStr = ' ' + LedCntStr + vbLf
    # Blue LED is used as status LED. Replace R10 on the PCB by a LED
    if DEBUG_SEND:
        Debug.Print('PWM=' + pwm + ' ')
    # Debug
    _fn_return_value = Write_Com(PortId, LeadStr + LED_PWM + LED_PWM + LED_PWM + TailStr)
    return _fn_return_value

def Send_LED_Dat(PortId, Val, LedNr, LEDCnt):
    _fn_return_value = None
    #---------------------------------------------------------------------------------------------------------
    if DEBUG_SEND:
        Debug.Print('Dat=' +  ( Val and WB_Mask )  + ' (')
        # Debug
        if ( Val and WB_MarkBit )  == WB_MarkBit:
            Debug.Print('1) ')
        else:
            Debug.Print('0) ')
    _fn_return_value = Send_LED_PWM(PortId, Val * 7 + 30, LedNr, LEDCnt)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NextDatFlag - ByRef 
def Toggle(NextDatFlag):
    #--------------------------------------------
    if NextDatFlag == 0:
        NextDatFlag = WB_MarkBit
    else:
        NextDatFlag = 0
    return NextDatFlag #*HL ByRef

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NextDatFlag - ByRef 
def Send_String(PortId, LedNr, LEDCnt, NextDatFlag, Add2CRC, Txt):
    global CRC_ByteList
    _fn_return_value = None
    i = Integer()

    Res = Boolean()
    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    for i in vbForRange(1, Len(Txt)):
        c = Mid(Txt, i, 1)
        if Add2CRC:
            CRC_ByteList[UBound(CRC_ByteList)] = Asc(c)
            CRC_ByteList = vbObjectInitialize((UBound(CRC_ByteList) + 1,), Variant, CRC_ByteList)
            # Allocate space for the next element
            # Debug.Print "Add CRC " & Asc(c)
            # Debug
        if not Send_LED_Dat(PortId, ( Asc(c) and WB_Mask )  + NextDatFlag, LedNr, LEDCnt):
            return _fn_return_value
        NextDatFlag=Toggle(NextDatFlag)
        X03.Sleep(WaitTime)
        if not Send_LED_Dat(PortId, Int(( Asc(c) / WB_MarkBit )) + NextDatFlag, LedNr, LEDCnt):
            return _fn_return_value
        NextDatFlag=Toggle(NextDatFlag)
        X03.Sleep(WaitTime)
    _fn_return_value = True
    return _fn_return_value, NextDatFlag #*HL ByRef

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NextDatFlag - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ByteStr - ByVal 
def Send_ByteString(PortId, LedNr, LEDCnt, NextDatFlag, AddByteCnt, ByteStr, PercentTxt=VBMissingArgument):
    global CRC_ByteList
    _fn_return_value = None
    bStr = Variant()

    ByteCnt = Integer()

    CRCPos = Integer()

    Total = Long()

    Cnt = Long()
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Percent_Msg_UserForm.Set_Status_Label(PercentTxt + '0 %')
    Percent_Msg_UserForm.Show()
    ByteStr = Trim(ByteStr)
    if Right(ByteStr, 1) == ',':
        ByteStr = M30.DelLast(ByteStr)
    ByteCnt = UBound(Split(ByteStr, ',')) + 1 + 2
    # Add 1 because UBound starts with 0, Add 2 for the ByteCnt
    CRCPos = UBound(CRC_ByteList)
    CRC_ByteList = vbObjectInitialize((CRCPos + ByteCnt,), Variant, CRC_ByteList)
    # Allocate space for the CRC data
    if AddByteCnt:
        ByteStr = M30.Long_to_2ByteStr(ByteCnt) + ', ' + ByteStr
    # Add Number of bytes to the start
    Total = UBound(Split(ByteStr, ',')) + 1
    for bStr in Split(ByteStr, ','):
        B = Val(bStr)
        CRC_ByteList[CRCPos] = B
        CRCPos = CRCPos + 1
        if DEBUG_SEND:
            Debug.Print('Add CRC ' + B)
        if not Send_LED_Dat(PortId, ( B and WB_Mask )  + NextDatFlag, LedNr, LEDCnt):
            return _fn_return_value
        NextDatFlag=Toggle(NextDatFlag)
        X03.Sleep(WaitTime)
        if not Send_LED_Dat(PortId, Int(( B / WB_MarkBit )) + NextDatFlag, LedNr, LEDCnt):
            return _fn_return_value
        NextDatFlag=Toggle(NextDatFlag)
        Cnt = Cnt + 1
        Percent_Msg_UserForm.Set_Status_Label(PercentTxt + Round(100 * Cnt / Total, 0) + ' %')
        X03.Sleep(WaitTime)
    _fn_return_value = True
    Percent_Msg_UserForm.Hide()
    return _fn_return_value, NextDatFlag #*HL ByRef

def LA(L1, L2):
    _fn_return_value = None
    #------------------------------------
    _fn_return_value = Trim(str(L1 * 16 + L2)) + ', '
    return _fn_return_value

def LED_Assignement(L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12):
    _fn_return_value = None
    #--------------------------------------------------------------------------------------------
    Check_if_C_Code_Version_is_Set()
    _fn_return_value = CPX_LED_ASSIGNEMENT + ', ' + LA(L1, L2) + LA(L3, L4) + LA(L5, L6) + LA(L7, L8) + LA(L9, L10) + LA(L11, L12) + ' '
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NextDatFlag - ByRef 
def Send_Pattern_Test(PortId, LedNr, LEDCnt, NextDatFlag, Mode):
    _fn_return_value = None
    ByteStr = String()
    #UT------------------------------------------------------------------------------------------------------------------------------------------
    Check_if_C_Code_Version_is_Set()
    _select43 = Left(Mode, 1)
    if (_select43 == 'H'):
        ByteStr = pattgen.M56_Pattern2Bytes.Convert_PatternStr_to_ByteStr('XPatternT11(0,128,SI_LocalVar,4,0,255,0,0,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,500 ms,200 ms,32,64,80,160,42,2  ,0,63,128,63,128,63,128,64,0,0,1)')
        # KS_Hauptsignal_Zs3_Zs1
    elif (_select43 == 'V'):
        ByteStr = pattgen.M56_Pattern2Bytes.Convert_PatternStr_to_ByteStr('XPatternT1(0,32,SI_LocalVar,11,0,128,0,0,300 ms,0,96,0,0,4,5,0,26,0,64,104,0,0,128,64,1,0,0  ,0,127,128,63,128,63,192,63,129,128,63,129,130)')
        # Viessm_4751
    elif (_select43 == 'T'):
        ByteStr = pattgen.M56_Pattern2Bytes.Convert_PatternStr_to_ByteStr('PatternT1(0,128,SI_LocalVar,12,0,128,0,0,1 Sek,1,32,0,4,128,0,16,0,2,64,0,8,0,1,32,0,4,192,0,0  ,63,191,191,191,191,191,191,191,191,191,192,1,0)')
        # Test LED Nr
    elif (_select43 == 'P'):
        ByteStr = pattgen.M56_Pattern2Bytes.Convert_PatternStr_to_ByteStr('PatternT4(0,0,SI_1,6,0,255,0,PF_NO_SWITCH_OFF,2 Sec,1 Sec,10 Sec,3 Sec,201,194,40,73,22,70)')
        #     // RGB_AmpelX
    elif (_select43 == 'L'):
        ByteStr = pattgen.M56_Pattern2Bytes.Convert_PatternStr_to_ByteStr('APatternT2(0,4,SI_1,12,0,255,0,0,100 ms,200 ms,3,0,0,3,0,0,12,0,0,12,0,0,48,0,0,48,0,0,192,0,0,192,0,0,0,3,0,0,3,0,0,12,0,0,12,0,0,48,0,0,48,0,0,192,0,0,192,0,0,0,3,0,0,3,0,0,12,0,0,12,0,0,48,0,0,48,0,0,192,0,0,192,0,0,0,0,0,0,0,0,0,0,0,0)')
        #     // ConstrWarnLight
    elif (_select43 == 'W'):
        ByteStr = pattgen.M56_Pattern2Bytes.Convert_PatternStr_to_ByteStr('APatternT1(0,128,SI_1,2,0,128,0,PM_NORMAL,1 Sek,9)')
        #     // Wechselblinker
    elif (_select43 == 'B'):
        ByteStr = pattgen.M56_Pattern2Bytes.Convert_PatternStr_to_ByteStr('APatternT2(0,4,SI_1,12,0,255,0,0,100 ms,200 ms,3,48,0,3,48,0,12,192,0,12,192,0,48,0,3,48,0,3,192,0,0,192,0,0,0,3,0,0,3,0,0,12,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)')
        # 3 Bright and 3 Normal LEDs
    else:
        X02.MsgBox('Error: Unknown Mode \'' + Mode + '\' in Send_Pattern_Test()', vbCritical, 'Internal Error')
        return _fn_return_value
    if Enable_Analog_Inputs:
        ByteStr = CPX_ANALOG_INPUT + ', ' + ByteStr
    else:
        if Analog_Limmits_Str != '':
            ByteStr = Analog_Limmits_Str + ByteStr
    Init_Assignement_Strings()
    if Len(Mode) > 1:
        _select44 = Mid(Mode, 2, 1)
        if (_select44 == 'V'):
            ByteStr = VIESSMN_LED_ASSIGNEMENT + ByteStr
        elif (_select44 == 'R'):
            ByteStr = REVERSE_LED_ASSIGNEMENT + ByteStr
        elif (_select44 == 'U'):
            ByteStr = UNIPROG_LED_ASSIGNEMANT + ByteStr
        elif (_select44 == 'B'):
            ByteStr = BRIGHT6_LED_ASSIGNEMENT + ByteStr
    #ByteStr = "1, 2, "
    ByteStr = ByteStr + '0'
    # Add EndCfg
    _fn_return_value, NextDatFlag = Send_ByteString(PortId, LedNr, LEDCnt, NextDatFlag, True, ByteStr)
    return _fn_return_value, NextDatFlag #*HL ByRef

def Conv_Analog_Limmits_to_ByteStr(Param):
    _fn_return_value = None
    Res = String()

    Limmits = vbObjectInitialize(objtype=String)

    Lim = Variant()

    Cnt = Long()
    #-------------------------------------------------------------------------
    Check_if_C_Code_Version_is_Set()
    Res = CPX_ANALOG_LIMMITS + ', '
    Limmits = Split(Param, ',')
    for Lim in Limmits:
        Cnt = Cnt + 1
        Lim = Trim(Lim)
        if not IsNumeric(Lim):
            X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Ungültige analoge Schwelle \'') + Lim + pattgen.M09_Language.Get_Language_Str('\' erkannt. '), vbCritical, pattgen.M09_Language.Get_Language_Str('Ungültige analoge Schwelle'))
            return _fn_return_value
        if Cnt <= ANALOG_KEYS:
            V = Val(Lim)
            Hi = Int(V / 256)
            lo = V % 256
            Res = Res + lo + ', ' + Hi + ', '
    if UBound(Limmits) + 1 > ANALOG_KEYS:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Es wurden zu viele analoge Schwellen angegeben. Nur die ersten ') + ANALOG_KEYS + pattgen.M09_Language.Get_Language_Str(' werden verwendet'), vbInformation, pattgen.M09_Language.Get_Language_Str('Zu viele analoge Schwellen'))
    if UBound(Limmits) + 1 < ANALOG_KEYS:
        #MsgBox "Not enough limmits given. The remaining " & ANALOG_KEYS - Cnt & " limmits are filled with 0", vbInformation
        while Cnt < ANALOG_KEYS:
            Res = Res + '0, 0, '
            Cnt = Cnt + 1
    _fn_return_value = Res
    return _fn_return_value

def Proc_Parameter_Analog_Inputs():
    _fn_return_value = None
    Ana_Inp = String()
    #--------------------------------------------------------
    Check_if_C_Code_Version_is_Set()
    Ana_Inp = Trim(X02.Range('Analog_Inputs'))
    if Ana_Inp == '':
        return _fn_return_value
    if InStr(Ana_Inp, ',') > 0:
        Res = Conv_Analog_Limmits_to_ByteStr(Ana_Inp)
        if Res == '':
            _fn_return_value = 'ERROR'
            return _fn_return_value
        _fn_return_value = Res
    else:
        # Only one parameter
        if Val(Ana_Inp) > 0:
            _fn_return_value = CPX_ANALOG_INPUT + ', '
            return _fn_return_value
    return _fn_return_value

def Set_Analog_Input(Param):
    global Analog_Limmits_Str, Enable_Analog_Inputs
    #--------------------------------------------
    # Enable the Analog input
    # If Param is empty the global variable Enable_Analog_Inputs is set
    # otherwite the parameter string is parsed for up to 10 limmits
    # which are written to the global variable Analog_Limmits_Str
    if Len(Param) > 0:
        Analog_Limmits_Str = Conv_Analog_Limmits_to_ByteStr(Param)
        Enable_Analog_Inputs = False
    else:
        Enable_Analog_Inputs = True

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NextDatFlag - ByRef 
def Send_CRC(PortId, LedNr, LEDCnt, NextDatFlag):
    _fn_return_value = None
    #-------------------------------------------------------------------------------------------------------------------
    if UBound(CRC_ByteList) > 0:
        CRC_ByteList = vbObjectInitialize((UBound(CRC_ByteList) - 1,), Variant, CRC_ByteList)
        # Remove the last unused element
        CRC = pattgen.M58_CRC.Crc16_ModBus(CRC_ByteList)
        if DEBUG_SEND:
            Debug.Print('CRC calculated over all \'Send_String()\' calls except the the header: ' + Hex(CRC))
        _fn_return_value, NextDatFlag = Send_ByteString(PortId, LedNr, LEDCnt, NextDatFlag, False, M30.Long_to_2ByteStr(CRC), 'CRC ')
    else:
        _fn_return_value = True
    return _fn_return_value, NextDatFlag #*HL ByRef

def Get_Goto_pwm(GotoNr):
    _fn_return_value = None
    pwm = Byte()
    #---------------------------------------------------------
    _select45 = GotoNr
    if (_select45 == 0):
        pwm = 15
    elif (_select45 == 1):
        pwm = 35
    elif (_select45 == 2):
        pwm = 55
    elif (_select45 == 3):
        pwm = 75
    elif (_select45 == 4):
        pwm = 95
    elif (_select45 == 5):
        pwm = 115
    elif (_select45 == 6):
        pwm = 135
    elif (_select45 == 7):
        pwm = 155
    elif (_select45 == 8):
        pwm = 175
    elif (_select45 == 9):
        pwm = 195
    elif (_select45 == 10):
        pwm = 215
    else:
        X02.MsgBox('Internal Error in Get_Goto_pwm(): Wrong GotoNr: ' + GotoNr, vbCritical, 'Internel Error)')
        pwm = 0
    _fn_return_value = pwm
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: NrStr - ByVal 
def Send_Goto(PortId, LedNr, LEDCnt, NrStr):
    _fn_return_value = None
    #-------------------------------------------------------------------------------------------------------------------
    _fn_return_value = Send_LED_PWM(PortId, Get_Goto_pwm(Val(NrStr)), LedNr, LEDCnt)
    return _fn_return_value

def Open_Port_With_Error_Msg_and_get_LastLED(PortId):
    _fn_return_value = None
    Cnt = Integer()

    BootMsg = String()

    LastLEDNr = Long()
    #----------------------------------------------------------------------------------
    _fn_return_value = - 1
    if not Open_Port_with_Error_Msg(PortId, False):
        return _fn_return_value
    Percent_Msg_UserForm.Set_Status_Label(pattgen.M09_Language.Get_Language_Str('Öffne Verbindung...'))
    Percent_Msg_UserForm.Show()
    for Cnt in vbForRange(1, 5):
        if not Write_Com(PortId, '#?' + vbLf):
            # VB2PY (UntranslatedCode) GoTo ErrorHand
            pass
        # write the question message
        BootMsg = '***Timeout***'
        BootMsg = Wait_Until_Arduino_Responds(PortId, ExpectedResponse, 1000)
        # Wait until the Arduino reponds
        if BootMsg != '***Timeout***' and BootMsg != '':
            break
    if BootMsg == '***Timeout***':
        Percent_Msg_UserForm.Hide()
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Der Adruino reagiert nicht'), vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler beim zugriff auf den Arduino an COM') + PortId)
        GoTo(ErrorHand)
    pattgen.M57_modCOMM.CommFlush(PortId)
    Debug.Print(BootMsg)
    LastLEDNr = 0
    if BootMsg != '':
        List = Split(BootMsg, ',')
        if UBound(List) >= 1 and InStr(List(0), ExpectedResponse) >= 0:
            for Idx in vbForRange(1, UBound(List)):
                LastLEDNr = LastLEDNr + Val(List(Idx))
    if LastLEDNr <= 0:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Auf dem Arduino ist nicht das richtige Programm installiert.' + vbCr + 'Der Arduino muss mit dem Excel Programm \'Prog_Generator\' konfiguriert werden.' + 'Dabei muss der \'LED Farbtest Mode\' im \'Config\' Blatt aktiviert sein.' + vbCr + vbCr + 'Meldung von Arduino:') + vbCr + BootMsg, vbCritical, pattgen.M09_Language.Get_Language_Str('Falsches Programm auf dem Arduino installiert'))
        GoTo(ErrorHand)
    Write_Com(PortId, '#L 0 0 0 0 FFFF' + vbLf)
    _fn_return_value = LastLEDNr
    Percent_Msg_UserForm.Hide()
    return _fn_return_value
    Percent_Msg_UserForm.Hide()
    End_Test_and_Close(PortId)
    return _fn_return_value

def Test_Send_with_Dialog():
    global WB_HighBit
    LedNr = 1

    LEDCnt = 1

    PortId = Integer()

    EndLoop = Boolean()

    NextDatFlag = Byte()
    #UT-------------------------------
    # Zum Test folgende sind folgende Eingaben zu machen:
    #   S = Start des Programmier mode: Die LEDs flackern wild
    #   C = Addressiere das Charliplexing Modul. Wenn diese Sequenz nicht kommt dann wird der Prog mode abgebrochen
    # eine der Pattern Funktionen P, A, L, W
    # dann mit 'E' Beenden.
    Set_Used_C_Code_Version(2)
    PortId = M07.M07_COM_Port.Get_USB_Port_with_Dialog()
    if PortId <= 0:
        return
    CRC_ByteList = vbObjectInitialize((0,), Variant)
    if Open_Port_With_Error_Msg_and_get_LastLED(PortId) <= 0:
        return
    X03.Sleep(100)
    WB_HighBit = False
    while not EndLoop:
        Inp = X02.InputBox('Eingabe der Befehle' + vbCr + '   S: Start' + vbCr + '   C: Charlieplexing Head' + vbCr + '   H: KS_Hauptsignal_Zs3_Zs1' + vbCr + '   VV: Vissmann 4751' + vbCr + '   P: Ampel' + vbCr + '   L: Lauflicht' + vbCr + '   W: Wechselblinker' + vbCr + '   BB: Bright Lauflicht' + vbCr + '   T: Test LED Numbers' + vbCr + 'Optional LED Asssigment tables could be added to the pattern functions:' + vbCr + '   ?R= Reverse, ?V=Viessmann, ?B= Bright ?U=UniProg' + vbCr + '   E: Send CRC and End' + vbCr + '   G<Nr>: Goto' + vbCr + '   A: Analog inputs (Opt with 10 limmits)' + vbCr + 'Spezialbefehle:' + vbCr + '   0..15 Daten' + vbCr + '   N: Toggle NextDatFlag' + vbCr + '   R<Nr>: Raw PWM number' + vbCr + 'NextDatFlag: ' + NextDatFlag, 'LED PWM Send Test')
        Res = True
        _select46 = Left(UCase(Inp), 1)
        if (_select46 == 'S'):
            Res = Send_LED_PWM(PortId, 235, LedNr, LEDCnt)
            NextDatFlag = 0
            CRC_ByteList = vbObjectInitialize((0,), Variant)
        elif (_select46 == 'E'):
            Res, NextDatFlag = Send_CRC(PortId, LedNr, LEDCnt, NextDatFlag)
            Res = Send_LED_PWM(PortId, 255, LedNr, LEDCnt)
        elif (_select46 == 'R'):
            Res = Send_LED_PWM(PortId, Val(Mid(Inp, 2)), LedNr, LEDCnt)
        elif (_select46 == 'N'):
            NextDatFlag=Toggle(NextDatFlag)
        elif (_select46 == 'C'):
            Res, NextDatFlag = Send_String(PortId, LedNr, LEDCnt, NextDatFlag, False, CP_HEAD_VERSION)
        elif (_select46 == 'H') or (_select46 == 'V') or (_select46 == 'P') or (_select46 == 'L') or (_select46 == 'W') or (_select46 == 'B') or (_select46 == 'T'):
            Res, NextDatFlag = Send_Pattern_Test(PortId, LedNr, LEDCnt, NextDatFlag, UCase(Inp))
        elif (_select46 == ''):
            EndLoop = True
        elif (_select46 == 'G'):
            Res = Send_Goto(PortId, LedNr, LEDCnt, Mid(Inp, 2))
        elif (_select46 == 'A'):
            Set_Analog_Input(Mid(Inp, 2))
        else:
            if Val(Inp) >= 0 and Val(Inp) <= 15:
                Res = Send_LED_Dat(PortId, Val(Inp) + NextDatFlag, LedNr, LEDCnt)
                NextDatFlag=Toggle(NextDatFlag)
            else:
                X02.MsgBox('Wrong Input:' + vbCr + '  \'' + Inp + '\'', vbCritical, 'Test_Send_with_Dialog')
        if not Res:
            X02.MsgBox('Error sending the data', vbCritical, 'Test_Send_with_Dialog')
    End_Test_and_Close(PortId)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ByteStr - ByRef 
def Convert_Numerical_LED_Assignement(LED_Assignement, ByteStr):
    _fn_return_value = None
    List = vbObjectInitialize(objtype=String)

    NrStr = Variant()

    Nr = Long()

    Nibbel = Integer()

    L0 = Integer()
    #----------------------------------------------------------------------------------------------------------------
    Check_if_C_Code_Version_is_Set()
    List = Split(LED_Assignement(), ',')
    if UBound(List) != 11:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Die Anzahl Einträge (') + UBound(List) + 1 + pattgen.M09_Language.Get_Language_Str(') in der LED Zuordnungsliste ist falsch. ' + 'Es müssen genau 12 per Komma getrennte Zahlen angegeben werden. ' + vbCr + 'Jede Zahl beschreibt die LED Nummer welche von der entsprechenden Zeile ' + 'der Mustertabelle angesprochen werden soll. Die erste Zahl steht ' + 'dabei für die erste Zeile, ...'), vbCritical, pattgen.M09_Language.Get_Language_Str('Falsche Anzahl in \'Charliplexing LED Zuordnung\''))
        return _fn_return_value
    ByteStr = ByteStr + CPX_LED_ASSIGNEMENT + ', '
    for NrStr in List:
        NrStr = Trim(NrStr)
        Nr = Val(NrStr)
        if not IsNumeric(NrStr) or Nr < 0 or Nr > 11:
            X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Der Eintrag \'') + NrStr + pattgen.M09_Language.Get_Language_Str('\' in der LED Zuordnungstabele ist keine gültige Zahl.' + vbCr + 'Es sind nur Zahlen zwischen 0 und 11 erlaubt.'), vbCritical, pattgen.M09_Language.Get_Language_Str('Ungültiger Eintrag in \'Charliplexing LED Zuordnung\''))
            return _fn_return_value
        _select47 = Nibbel
        if (_select47 == 0):
            Nibbel = 1
            L0 = Nr
        elif (_select47 == 1):
            Nibbel = 0
            ByteStr = ByteStr + LA(L0, Nr)
    _fn_return_value = True
    return _fn_return_value, ByteStr #*HL ByRef

def Test_Convert_Numerical_LED_Assignement():
    ByteStr = String()
    #UT-------------------------------------------------
    Debug.Print('Res= ' + Convert_Numerical_LED_Assignement('0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11', ByteStr))
    Debug.Print('ByteStr = \'' + ByteStr + '\'')

def Find_LED_Assignement(Name):
    _fn_return_value = None
    Row = Long()

    Col = Long()

    EmptyCnt = Long()

    Numbers = String()

    NL = vbObjectInitialize(objtype=String)
    #--------------------------------------------------------------
    _with54 = X02.Sheets(M01.SPECIAL_MODEDLG_SH)
    _with55 = _with54.Range('LED_Assignm_Head')
    Row = _with55.Row + 1
    Col = _with55.Column
    while 1:
        _select48 = Trim(_with54.Cells(Row, Col))
        if (_select48 == Name):
            Numbers = _with54.Cells(Row, _with54.Range('LED_Assignement_Head').Column)
            NL = Split(Replace(Numbers, ' ', ''), ',')
            if UBound(NL) != 11:
                _with54.Cells(Row, _with54.Range('LED_Assignement_Head').Column).Select()
                X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Die LED Zuordnung in Sheet \'') + _with54.Name +  ( '\' Zeile ' )  + Row + pattgen.M09_Language.Get_Language_Str(' enthält nicht genau 12 Werte'), vbCritical, pattgen.M09_Language.Get_Language_Str('Interner Fehler'))
                return _fn_return_value
            _fn_return_value = LED_Assignement(NL(0), NL(1), NL(2), NL(3), NL(4), NL(5), NL(6), NL(7), NL(8), NL(9), NL(10), NL(11))
            return _fn_return_value
        elif (_select48 == ''):
            EmptyCnt = EmptyCnt + 1
            if EmptyCnt > 2:
                return _fn_return_value
        Row = Row + 1
        if not (True):
            break
    return _fn_return_value

def Test_Find_LED_Assignement():
    #UT------------------------------------
    Debug.Print(Find_LED_Assignement('Reverse'))

def Send_to_ATTiny(PortId, LedNr, LED_Assignement_Str, Analog_Inputs):
    global WB_HighBit
    LEDCnt = 1

    Special_Mode = String()

    MaxTimes = Long()

    UsedTimes = Long()

    LastLEDNr = Long()

    NextDatFlag = Byte()

    ByteStr = String()

    Res = String()
    #--------------------------------------------------------------------------------------------------------------
    # PortId
    # Ex. 1, 2, 3, 4 ... 50 for COM1 - COM4... COM50
    # 16.10.20:
    Special_Mode = PG.ThisWorkbook.ActiveSheet.Range('Special_Mode')
    if Special_Mode == 'Charlieplexing':
        if not pattgen.M60_Select_LED.Select_Special_Mode():
            return
    _select49 = PG.ThisWorkbook.ActiveSheet.Range('Special_Mode')
    if (_select49 == 'Charlieplexing V2'):
        Set_Used_C_Code_Version(2)
        MaxTimes = 64
    elif (_select49 == 'Charlieplexing V1'):
        Set_Used_C_Code_Version(1)
        MaxTimes = 23
        # There is an error in the old version which limmits the size evenif 30 entries should be possible
    else:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Error: Invalid Charlieplexing mode entered'), vbCritical, 'Invalid Charlieplexing mode detected')
        PG.ThisWorkbook.ActiveSheet.Range('Special_Mode').Select()
    UsedTimes = Val(Mid(X02.Range('Start'), InStr(X02.Range('Start'), 'PatternT') + Len('PatternT')))
    if UsedTimes > MaxTimes:
        X02.MsgBox(Replace(Replace(pattgen.M09_Language.Get_Language_Str('Fehler: Zu viele Zeiten in der \'Dauer\' Zeile verwendet. ' + 'Es sind maximal #1# Zeiten bei Version \'#2#\' möglich'), '#1#', MaxTimes), '#2#', X02.Range('Special_Mode')), vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler: Zu viele Zeiten benutzt'))
        return
    if X02.Range('FlashUsage') >= 500:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Der EEPROM Speicher des ATTinys ist zu klein für diese riesige Konfiguration ;-(' + vbCr + 'Tip: \'Bits pro Wert\' oder die Anzahl der Zeiten verringern'), vbCritical, pattgen.M09_Language.Get_Language_Str('Konfiguration passt nicht in EEPROM'))
        return
    if X02.Range('Kanaele') > 12:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Es können maximal 12 LEDs mit dem Charlieplexing Modul angesteuert werden'), vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler: Zu viele LED Kanäle benutzt'))
        return
    if pattgen.M11_To_Prog_Gen.Check_Table_before_Copy(False) == False:
        return
    LastLEDNr = Open_Port_With_Error_Msg_and_get_LastLED(PortId)
    if LastLEDNr <= 0:
        # VB2PY (UntranslatedCode) GoTo ErrorHand
        pass
    if LedNr < 0 or LedNr >= LastLEDNr:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Falsche RGB LED Modul Nummer: ') + LedNr + '.' + vbCr + pattgen.M09_Language.Get_Language_Str('Die Modul Nummer muss zwischen 0 und ') + LastLEDNr - 1 + pattgen.M09_Language.Get_Language_Str(' liegen.' + vbCr + vbCr + 'Die maximal mögliche Modul Nummer wird von der auf dem Arduino installierten Konfiguration ' + 'bestimmt. Es können nur so viele LEDs angesprochen werden wie im \'Prog_Generator\' angegeben ' + 'wurden. Wenn sich das Modul an einer noch nicht eingetragenen Position befindet, dann ' + 'kann der Befehl \'Reserve LEDs\' im \'Prog_Generator\' benutzt werden damit zusätzliche ' + 'LEDs angesprochen werden können.'), vbCritical, pattgen.M09_Language.Get_Language_Str('RGB LED Nummer des Moduls ist falsch'))
        GoTo(ErrorHand)
    WB_HighBit = False
    Init_Assignement_Strings()
    if not Send_LED_PWM(PortId, 235, LedNr, LEDCnt):
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        pass
    # Sent Start
    CRC_ByteList = vbObjectInitialize((0,), Variant)
    X03.Sleep(WaitTime_Start)
    Percent_Msg_UserForm.Set_Status_Label(pattgen.M09_Language.Get_Language_Str('Sende Kennung...'))
    res, NextDatFlag = Send_String(PortId, LedNr, LEDCnt, NextDatFlag, False, CP_HEAD_VERSION)
    if not res:
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        pass
    LED_Assignement_Str = Trim(LED_Assignement_Str)
    if LED_Assignement_Str != '':
        if IsNumeric(Left(LED_Assignement_Str, 1)):
            res, ByteStr = Convert_Numerical_LED_Assignement(LED_Assignement_Str, ByteStr)
            if  res == False:
                # VB2PY (UntranslatedCode) GoTo ErrorHand
                pass
        else:
            ByteStr = Find_LED_Assignement(LED_Assignement_Str)
            if ByteStr == '':
                X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Die LED Zuordnung \'') + LED_Assignement_Str + pattgen.M09_Language.Get_Language_Str('\' ist unbekannt'), vbCritical, pattgen.M09_Language.Get_Language_Str('Unbekannte LED Zuordnung'))
                GoTo(ErrorHand)
    Res = Proc_Parameter_Analog_Inputs()
    if Res == 'ERROR':
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        pass
    ByteStr = ByteStr + Res
    ByteStr = ByteStr + pattgen.M56_Pattern2Bytes.Convert_PatternStr_to_ByteStr(X02.Range(M01.ErgebnisRng))
    ByteStr = ByteStr + '0'
    # Add EndCfg
    res, NextDatFlag = Send_ByteString(PortId, LedNr, LEDCnt, NextDatFlag, True, ByteStr)
    if not res:
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        pass
    # Send the data to the ATTiny
    res, NextDatFlag = Send_CRC(PortId, LedNr, LEDCnt, NextDatFlag)
    if not res:
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        pass
    # Send the CRC
    if not Send_LED_PWM(PortId, 255, LedNr, LEDCnt):
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        pass
    if pattgen.M06_Goto_Graph.Goto_Mode_is_Active():
        Test_GotoNr_Form.Show_Dialog(PortId, LedNr)
    Percent_Msg_UserForm.Hide()
    End_Test_and_Close(PortId)
    return
    Percent_Msg_UserForm.Hide()
    End_Test_and_Close(PortId)
    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler bei der Datenübertragung zum ATTiny'), vbCritical, pattgen.M09_Language.Get_Language_Str('Datenübertragungsfehler'))
    Percent_Msg_UserForm.Hide()

def LED_Assignement_Dialog():
    Res = String()
    #----------------------------------
    Res = Select_from_Sheet_Form.Show_Form(M01.SPECIAL_MODEDLG_SH, pattgen.M09_Language.Get_Language_Str('LED Zuordnung definieren'), pattgen.M09_Language.Get_Language_Str('Auswahl der LED Zuordnung'), pattgen.M09_Language.Get_Language_Str('Die Zuordnung der Charlieplexing LEDs ist von Hersteller zu Hersteller unterschiedlich. Mit diesem Dialog kann die passende Zuordnung der Muster Zeilen zu den LEDs gewählt werden.'), oDialog_Dat_ROW1= X02.Sheets(M01.SPECIAL_MODEDLG_SH).Range('LED_Assignm_Head').Row + 1, oLowerWin_COL= 3)
    if Res != '':
        X02.RangeDict['CPX_LED_Assignement'] = Split(Res, ',')(0)

def Open_Port_and_Show_Test_GotoNr_Form(PortId):
    LastLEDNr = Long()

    LedNr = Byte()
    #----------------------------------------------------------------
    LastLEDNr = Open_Port_With_Error_Msg_and_get_LastLED(PortId)
    if LastLEDNr <= 0:
        return
    LedNr = X02.Range('RGB_Modul_Nr')
    Test_GotoNr_Form.Show_Dialog(PortId, LedNr)
    End_Test_and_Close(PortId)

def End_Test_and_Close(PortId):
    #-------------------------------
    # VB2PY (UntranslatedCode) On Error Resume Next
    Write_Com(PortId, '#L 0 0 0 0 32767' + vbLf)
    X03.Sleep(( 100 ))
    Write_Com(PortId, '#X' + vbLf)
    Close_Port(PortId)
    # VB2PY (UntranslatedCode) On Error GoTo 0

def Send_to_ATTiny_Main():
    Ctrl_Pressed = Boolean()

    PortId = Integer()
    #-------------------------------
    # Is called if the "Zum Modul schicken" Button is pressed
    Ctrl_Pressed = X03.GetAsyncKeyState(M30.VK_CONTROL) != 0
    # Following function must be declared: Public Declare Function GetAsyncKeyState Lib "user32" (ByVal vKey As Long) As Integer
    PortId = M07.M07_COM_Port.Get_USB_Port_with_Dialog()
    if PortId > 0:
        if X02.Range('RGB_Modul_Nr') == '':
            pattgen.M60_Select_LED.Get_LED_Address_Dialog()
            if X02.Range('RGB_Modul_Nr') == '':
                return
        if Ctrl_Pressed:
            Open_Port_and_Show_Test_GotoNr_Form(PortId)
        else:
            Send_to_ATTiny(PortId, X02.Range('RGB_Modul_Nr'), X02.Range('CPX_LED_ASSIGNEMENT'), X02.Range('Analog_Inputs'))

# VB2PY (UntranslatedCode) Option Explicit
