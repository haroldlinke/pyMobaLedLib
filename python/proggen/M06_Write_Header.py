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
# 2021-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2022-01-07 v4.02 HL: - Else:, ByRef check done - first PoC release
# 2022-03-13 v4.15 HL: - Update to MLL 3.1.0D


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *
# fromx proggen.M02_Public import *
# fromx proggen.M06_Write_Header_LED2Var import *
# fromx proggen.M06_Write_Header_Sound import *
# fromx proggen.M06_Write_Header_SW import *
# fromx proggen.M08_ARDUINO import *
# fromx proggen.M09_Language import *
# fromx proggen.M09_Select_Macro import *
# fromx proggen.M20_PageEvents_a_Functions import Update_Start_LedNr
# fromx proggen.M25_Columns import *
# fromx proggen.M28_Diverse import *
# fromx proggen.M30_Tools import *
# fromx proggen.M80_Create_Multiplexer import *

# fromx ExcelAPI.X02_Workbook import *
# fromx mlpyproggen.F_UserForm_Header_Created import *

import proggen.M02_Public as M02
import proggen.M02a_Public as M02a
#import proggen.M03_Dialog as M03
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
#import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
#import proggen.M27_Sheet_Icons as M27
import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M38_Extensions as M38
import proggen.M39_Simulator as M39
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Multiplexer as M80
import mlpyproggen.Prog_Generator as PG

import ExcelAPI.XLA_Application as P01
from ExcelAPI.XLC_Excel_Consts import *
import ExcelAPI.XLWF_Worksheetfunction as XLWF

""" Todo:

 - Wichtig: Die Schalter müssen auch in den Inputs der Macros erkannt werden sonst werden sie nur dann definiert wenn
   sie in der Adress Spalte stehen
 - Warnung generieren wenn Switch C und D Gleichzeitig verwendet werden und die gleichen Pins verwendet werden für C und D
"""

InChTxt = String()                                      # List of all defined DCC (SX or CAN) input channels in the form: "#defines INCH_DCC_1_ONOFF <Nr>"
Undefined_Input_Var = String()                          # List of all undefined input variables in the first step
Undef_Input_Var_Row = String()

AddrList = vbObjectInitialize(objtype=Long)
LocInChNr = Long()
CurrentCounterId = Long()
Ext_AddrTxt = String()
ConfigTxt = String()
Err = String()
Channel = Long()
LEDNr = Long()
includeCount = Long()
AddrComment = String()
Start_Values = String()
Store_ValuesTxt = String()
Store_Val_Written = String()
MaxLEDNr = vbObjectInitialize((M02.LED_CHANNELS - 1,), Long) # 08.02.23 Juergen (include feature)
IncludeStack = Collection()                 # 10.03.23 Juergen (include feature)

Start_LED_Channel = vbObjectInitialize((M02.LED_CHANNELS - 1,), Long)
LEDs_per_Channel = vbObjectInitialize((M02.LED_CHANNELS - 1,), Long)
Max_Channels = Long()
LEDs_per_ChannelList = String()

DayAndNightTimer = String()

MINLEDs = 20

#-------------------------------------------------------
def Init_HeaderFile_Generation():
#-------------------------------------------------------
    global LocInChNr, CurrentCounterId, Ext_AddrTxt, Store_ValuesTxt, Store_Val_Written, InChTxt, ConfigTxt, Err, Channel, LEDNr, AddrComment, Start_Values, Undefined_Input_Var, DayAndNightTimer, includeCount, Start_LED_Channel, LEDs_per_Channel, Max_Channels, LEDs_per_ChannelList
    _fn_return_value = False
    
    ReserveLeds = Long()

    NumLeds = Long()

    Nr = Long()
    
    Erase(AddrList)
    M25.Make_sure_that_Col_Variables_match()
    LocInChNr = 0
    CurrentCounterId = 0
    Ext_AddrTxt = ''
    Store_ValuesTxt = ''
    Store_Val_Written = ''
    InChTxt = ''
    ConfigTxt = ''
    Err = ''
    Channel = 0
    LEDNr = 0
    AddrComment = ''
    Start_Values = ''
    Undefined_Input_Var = ''
    DayAndNightTimer = ''
    includeCount = 0
    M06SW.ATTINY_GBM_CHECK_ERROR = False                                            # 13.02.23:
    M06SW.USE_ATTiny_CAN_GBM = False
    M06SW.ATTINY_GBM_SW_Filter = ""
    M06SW.Alias_Names_List = ""    
    
    # Fill the array Start_LED_Channel()
    for Nr in vbForRange(0, M02.LED_CHANNELS - 1):
        NumLeds = NumLeds + P01.val(P01.Cells(M02.SH_VARS_ROW, M20.Get_LED_Nr_Column(Nr))) #*HL
    if NumLeds < MINLEDs:
        ReserveLeds = MINLEDs - NumLeds
        NumLeds = MINLEDs
    Start_LED_Channel[0] = 0
    for Nr in vbForRange(0, M02.LED_CHANNELS - 1):
        LEDs_per_Channel[Nr] = P01.val(P01.Cells(M02.SH_VARS_ROW, M20.Get_LED_Nr_Column(Nr))) #*HL
        if Nr == 0 and ReserveLeds > 0:
            LEDs_per_Channel[0] = LEDs_per_Channel(0) + ReserveLeds
            # To be able to test at least 20 LEDs with the color test program ' 26.10.20:
        if Nr > 0:
            Start_LED_Channel[Nr] = Start_LED_Channel(Nr - 1) + LEDs_per_Channel(Nr - 1)
    for Nr in vbForRange(M02.LED_CHANNELS - 1, 0, - 1):
        if LEDs_per_Channel(Nr) > 0:
            Max_Channels = Nr
            break
    LEDs_per_ChannelList = ''
    for Nr in vbForRange(0, Max_Channels):
        LEDs_per_ChannelList = LEDs_per_ChannelList + str(LEDs_per_Channel(Nr)) #*HL
        if Nr != Max_Channels:
            LEDs_per_ChannelList = LEDs_per_ChannelList + ','
    _fn_return_value = True
    return _fn_return_value
#-------------------------------------------------------
def ExpandName(Variablename):
#-------------------------------------------------------
    _fn_return_value = ""
    # 03.03.23 Juergen new function
    if Left(Variablename, 1) == '$':
        #ExpandName = Replace(Variablename, "$", "I" + Trim(Str(includeCount)) + "_")
        _fn_return_value = 'I' + Trim(Str(includeCount)) + '_' + Mid(Variablename, 2)
    else:
        _fn_return_value = Variablename
    return _fn_return_value

#-------------------------------------------------------
def AddressExists(Addr):
#-------------------------------------------------------
    global AddrList
    
    _fn_return_value = False
    
    a = Variant()
    #------------------------------------------------------
    # ToDo: Überlappungen prüfen wenn InCnt > 1
    if not M30.IsArrayEmpty(AddrList):
        for a in AddrList:
            if a == Addr:
                _fn_return_value = True
                return _fn_return_value
        AddrList = vbObjectInitialize((UBound(AddrList) + 1,), int, AddrList)
    else:
        AddrList = vbObjectInitialize((0,), int, AddrList)
    AddrList[UBound(AddrList)] = Addr
    return _fn_return_value

#-------------------------------------------------------
def Clear_MaxLEDNr():
#-------------------------------------------------------
    global MaxLEDNr
    idx = Long()
    for idx in vbForRange(0, M02.LED_CHANNELS - 1):
        MaxLEDNr[idx] = 0

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpTyp - ByVal 
#-------------------------------------------------------
def AddressRangeExists(Addr, cnt, InpTyp):
#-------------------------------------------------------
    _fn_return_value = False
    Ad = Long()
    InpTypMod = Long()

    i = Long()
    #-------------------------------------------------------------------------------------
    # If the InpTyp is a button (Red / Green) two virtual adresses are used.
    # One for each button.
    # For OnOff switches one address is used twice
    # To destinguish the two cases the address is multiplied by 2 and 0/1 is added
    #
    
    M09.Set_Tast_Txt_Var()
    # Set the global variables Red_T, Green_T, ...          06.03.20:
    _select58 = InpTyp
    if (_select58 == M09.Red_T):
        InpTypMod = 1
    elif (_select58 == M09.Green_T):
        InpTypMod = 2
    elif (_select58 == M09.OnOff_T):
        InpTypMod = 3
    elif (_select58 == M09.Tast_T):
        InpTypMod = 3
    else:
        P01.MsgBox('Internal Error: Unknown InpTyp in AddressRangeExists', vbCritical,"Error")
        M30.EndProg()
    Ad = Addr
    for i in vbForRange(1, cnt):
        if InpTypMod & 1:
            if AddressExists(Ad * 2):
                _fn_return_value = True
                return _fn_return_value
        if InpTypMod & 2:
            if AddressExists(Ad * 2 + 1):
                _fn_return_value = True
                return _fn_return_value
        _select59 = InpTypMod
        if (_select59 == 1):
            InpTypMod = 2
        elif (_select59 == 2):
            InpTypMod = 1
            Ad = Ad + 1
        elif (_select59 == 3):
            Ad = Ad + 1
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Inp_Typ - ByVal 
#-------------------------------------------------------
def Get_Next_Typ(Inp_Typ):
#-------------------------------------------------------
    _fn_return_value = ""
    M09.Set_Tast_Txt_Var()
    # Set the global variables Red_T, Green_T, ...          06.03.20:
    _select60 = Inp_Typ    
    if (_select60 == M09.OnOff_T):
        _fn_return_value = M09.OnOff_T
    elif (_select60 == M09.Red_T):
        _fn_return_value = M09.Green_T
    elif (_select60 == M09.Green_T):
        _fn_return_value = M09.Red_T
    elif (_select60 == M09.Tast_T):
        _fn_return_value = M09.Tast_T
    elif (_select60 == 'O_RET_MSG'):
        _fn_return_value = 'O_RET_MSG'
        # 12.02.23:    
    else:
        P01.MsgBox('Internal error: Undefined Inp_Typ: \'' + Inp_Typ + '\' in Get_Next_Typ()', vbCritical, 'Internal error in Get_Next_Typ()')
        M30.EndProg()
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Addr - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InTyp - ByVal 
#----------------------------------------------------------------------------------
def Gen_Address_Define_Name(Addr, InTyp):
#----------------------------------------------------------------------------------
    _fn_return_value = ""
    if M25.Page_ID == 'Selectrix':
        _fn_return_value = 'INCH_SX_' + str(Int(Addr / 8)) + '_' +  str(( Addr % 8 )  + 1 )+ Replace(Mid(Get_Typ_Const(InTyp), 2, 255), ',', '')
    else:
        # 13.02.23: Hardi
        if InTyp == 'O_RET_MSG':
            NrStr = str(Hex(Addr + 0x3000))
            NrStr = Left(NrStr, Len(NrStr) - 1) + '_' + Right(NrStr, 1)
        else:
            NrStr = str(Addr)        
        _fn_return_value = 'INCH_' + M25.Page_ID + '_' + NrStr + Replace(Mid(Get_Typ_Const(InTyp), 2, 255), ',', '')
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Addr - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Comment - ByVal 
#----------------------------------------------------------------------------------
def Generate_Define_Line(Addr, row, Channel, Comment, IsRM):
#----------------------------------------------------------------------------------
    _fn_return_value = ""
    
    COMMENT_DEFINE = '   // '

    Name = String()
    
    i = Long()

    InTyp = String()
    
    MacroName = String()
    
    AliasName = String() 
    # 12.02.23: Hardi: Added IsRM
    
    # Generate defines for the input channels for expert users
    if IsRM:
        # 12.02.23: Hardi
        InTyp = 'O_RET_MSG'
    else:    
        InTyp = P01.Cells(row, M25.Inp_Typ_Col)
    M09.Set_Tast_Txt_Var()
    for i in vbForRange(1, P01.val(P01.Cells(row, M25.InCnt___Col))):
        #Name = "INCH_" & M25.Page_ID & "_" & Addr & Replace(Mid(Get_Typ_Const(InTyp), 2, 255), ",", "")
        Name = Gen_Address_Define_Name(Addr, InTyp)
        _fn_return_value = _fn_return_value + '#define ' + M30.AddSpaceToLen(Name, 22) + '  ' + M30.AddSpaceToLen(str(Channel), 4) + COMMENT_DEFINE + Comment + vbCrLf
        # 21.12.22 replace vbcr with vbcrlf
        if InTyp != M09.Red_T:
            Addr = Addr + 1
        InTyp = Get_Next_Typ(InTyp)
        Channel = Channel + 1
        Comment = '    "'
    # Generate Alias name if "// Define Input(" is used
    # 14.02.23: Hardi
    MacroName = P01.Cells(row, M25.Config__Col)
    if Left(MacroName, Len('// Define Input(')) == '// Define Input(':
        AliasName = Split(Mid(MacroName, Len('// Define Input(') + 1), ')')(0)
        if AliasName != '':
            if M06SW.Alias_Names_List == '':
                M06SW.Alias_Names_List = vbCrLf + '// Alias definitions defined with \'Define Input()\'' + vbCrLf
            M06SW.Alias_Names_List = M06SW.Alias_Names_List + '#define ' + M30.AddSpaceToLen(AliasName, 20) + ' ' + Name + vbCrLf
    
    return _fn_return_value

#----------------------------------------------------
def Get_Description(r):
#----------------------------------------------------
    _fn_return_value = Trim(P01.Cells(r, M25.Descrip_Col))
    # If Get_Description = "" Then Get_Description = Cells(r, Config__Col) ' 02.03.20: Old: Why should the macro be repeated? It gets verry long if "#define" lines are used
    if _fn_return_value == '':
        _fn_return_value = 'Excel row ' + str(r)
        # 02.03.20: New
    _fn_return_value = Replace(_fn_return_value, vbLf, '| ')
    return _fn_return_value

#----------------------------------------------------
def Activate_DayAndNightTimer(Cmd):
#----------------------------------------------------
    global DayAndNightTimer #"HL
    
    args = vbObjectInitialize(objtype=String)

    Period = Double()
    #--------------------------------------------------------
    args = Split(Trim(Replace(Replace(Cmd, 'DayAndNightTimer(', ''), ')', '')), ',')
    Period = P01.val(Trim(args(1)))
    DayAndNightTimer = vbCrLf + '#define DayAndNightTimer_Period    ' + Round(Period * 60 * 1000 / 512, 0) + vbCrLf
    # 21.12.22 replace vbcr with vbcrlf
    if Trim(args(0)) != 'SI_1':
        DayAndNightTimer = DayAndNightTimer + '#define DayAndNightTimer_InCh      ' + Trim(args(0)) + vbCrLf
        # 21.12.22 replace vbcr with vbcrlf
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cmd - ByVal 
#----------------------------------------------------
def Do_Replace_Sym_Pin_Name(Cmd, PinStr):
#----------------------------------------------------

    MB_LED_Nr_Str_Arr = vbObjectInitialize(objtype=String)

    MB_LED_Pin_Nr_Arr = vbObjectInitialize(objtype=String)

    i = Long()
    #----------------------------------------------------------------------------------------
    MB_LED_Nr_Str_Arr = Split(M02.MB_LED_NR_STR, ' ')
    MB_LED_Pin_Nr_Arr = Split(Replace(M02.MB_LED_PIN_NR, '  ', ' '), ' ')
    if UBound(MB_LED_Nr_Str_Arr) != UBound(MB_LED_Pin_Nr_Arr):
        P01.MsgBox('Internal Error: Array hafe different size in \'Do_Replace_Sym_Pin_Name()\'', vbCritical, 'Internal Error')
        M30.EndProg()
    for i in vbForRange(0, UBound(MB_LED_Nr_Str_Arr)):
        if PinStr == MB_LED_Nr_Str_Arr(i):
            _fn_return_value = Replace(Cmd, '(' + MB_LED_Nr_Str_Arr(i) + ',', '(' + MB_LED_Pin_Nr_Arr(i) + ',')
            return _fn_return_value
    P01.MsgBox('Internal Error: PinStr not found in \'Do_Replace_Sym_Pin_Name()\'', vbCritical, 'Internal Error')
    M30.EndProg()
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cmd - ByRef 
#----------------------------------------------------
def Proc_Special_Functions(Cmd, LEDNr, Channel):
#----------------------------------------------------
    _fn_return_value = False
    
    if Left(Cmd, Len('Mainboard_LED(')) == 'Mainboard_LED(':
        PinOrNr = Split(Replace(Cmd, 'Mainboard_LED(', ''), ',')(0)
        if InStr(' ' + M02.MB_LED_NR_STR + ' ', ' ' + PinOrNr + ' ') > 0:
            Replace_Sym_Pin_Name = True
        if ( PinOrNr == '4' or PinOrNr == 'D4' )  and M06SW.PIN_A3_Is_Used():
            # Problem if the SwitchB or C is used. If the CAN mode is used the Mainboard LED may be used. It will overwrite the HB
            P01.MsgBox(M09.Get_Language_Str('Achtung: Die Mainboard LED 4 kann nicht benutzt werden wenn der PIN A3 an anderer Stelle benutzt wird (CAN, SwitchB oder SwitchC).'), vbCritical,M09.Get_Language_Str('Pin A3 ist bereits benutzt'))
            return _fn_return_value, Cmd
        if PinOrNr == '13' or PinOrNr == 'D13':
            # The heartbeat LED can't be used if Mainboard LED 13 is used. Attention: Don't use the Mainboard LEDs 10-13 together with the CAN
            # 09.10.20:
            Cmd = Cmd + vbCrLf + '  #undef  LED_HEARTBEAT_PIN  /* Use the heartbeat LED at pin A3 */' + vbCrLf + '  #define LED_HEARTBEAT_PIN A3' + Space(79)
            # 21.12.22 replace vbcr with vbcrlf
        if Replace_Sym_Pin_Name:
            Cmd = Do_Replace_Sym_Pin_Name(Cmd, PinOrNr)
        Cmd = Replace(Replace(Replace(Cmd, 'Mainboard_LED(', '#define Mainboard_LED'), ',', ' '), ')', '')
    if Left(Cmd, Len('DayAndNightTimer(')) == 'DayAndNightTimer(':
        if not Activate_DayAndNightTimer(Cmd):
            return _fn_return_value, Cmd
        Cmd = '// ' + Cmd
    if InStr(Cmd, M02.SF_LED_TO_VAR) > 0:
        fret, Cmd = M06LED.Add_LED2Var_Entry(Cmd, LEDNr)
        if not fret:
            return _fn_return_value, Cmd
    if InStr(Cmd, M02.SF_SERIAL_SOUND_PIN) > 0:
        # 08.10.21: Juergen
        fret, Cmd = M06Sound.Add_SoundPin_Entry(Cmd, LEDNr)
        if not fret:
            return _fn_return_value
    _fn_return_value = True, Cmd
    return _fn_return_value, Cmd

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel_or_define - ByVal 
#----------------------------------------------------
def Generate_Config_Line(LEDNr, Channel_or_define, r, Config_Col, Addr):
#----------------------------------------------------
    
    global LocInChNr
    _fn_return_value = ""
    
    Txt = String()

    lines = Variant()

    line = Variant()

    Res = String()

    AddDescription = Boolean()

    Description = String()

    Inc_LocInChNr = False #Boolean()
    #-----------------------------------------------------------------------------------------------------------------------------------
    # ToDo: Add checks like
    # - open/closing braket test
    # - characters after #LED, #InCh
    Txt = P01.Cells(r, Config_Col)
    if Trim(Txt) == '':
        return _fn_return_value
    lines = Split(Txt, vbLf)
    Description = Get_Description(r)
    AddDescription = Description != ''
    for line in lines:
        Comment = ''
        Cmd = ''
        CommentStart = InStr(line, '//')
        if CommentStart == 0:
            Cmd = line
        elif CommentStart == 1:
            Comment = line
        else:
            Cmd = Left(line, CommentStart)
            Comment = Mid(line, CommentStart + 1, 1000)
        # search for macros having $ Args
        if InStr(Cmd, '(') != 0 and InStr(Cmd, '$') != 0:
            # 28.01.24 Juergen
            Arg_List = M06SW.Get_Arguments(Cmd)
            for ArgNr in vbForRange(0, UBound(Arg_List)):
                Arg = Arg_List(ArgNr)
                ExpandArg = ExpandName(Arg)
                if ExpandArg != Arg:
                    Cmd = Replace(Cmd, Arg + ')', ExpandArg + ')')
                    Cmd = Replace(Cmd, Arg + ',', ExpandArg + ',')
        if LEDNr < 0:
            P01.Cells(r, M25.Config__Col).Select()
            P01.MsgBox(M09.Get_Language_Str('Fehler: Die LED Nummer darf nicht negativ werden. Das kann durch eine falsche Angabe bei einem vorangegangenen "Next_LED" Befehl passieren.'), vbCritical, M09.Get_Language_Str('Fehler: Negative LED Nummer'))
            _fn_return_value = '#ERROR#'
            return _fn_return_value
        Cmd = Replace(Cmd, '#LED', str(LEDNr))
        if Addr >= 0 or Addr == - 2:
            Cmd = Replace(Cmd, '#InCh', str(Channel_or_define))
        else:
            Cmd = Replace(Cmd, '#InCh', 'SI_1')
        if InStr(Cmd, '#LocInCh') > 0:
            if P01.Cells(r, M25.LocInCh_Col) == 0:
                P01.MsgBox('Interner Fehler: \'#LocInCh\' wird verwendet aber \'Loc InCh\' ist 0 oder leer in Zeile ' + r, vbCritical, 'Interner Fehler')
                M30.EndProg()
            Cmd = Replace(Cmd, '#LocInCh', 'LOC_INCH' + str(LocInChNr))
            Inc_LocInChNr = True
            # 18.11.19:
            
        fret,Cmd = Proc_Special_Functions(Cmd, LEDNr, Channel_or_define) #*HL
        if fret == False:
            _fn_return_value = '#ERROR#'
            P01.Cells(r, M25.Config__Col).Select()
            return _fn_return_value
        
        if M38.IsExtensionKey(Cmd):
            # 31.01.22: Juergen
            res,Cmd = M38.Add_Extension_Entry(Cmd) #*HL ByRef
            if not res:
                _fn_return_value = '#ERROR#'
                P01.Cells(r, M25.Config__Col).Select()
            return _fn_return_value        
        
        if P01.Cells(r, M25.LEDs____Col) == M02.SerialChannelPrefix:
            # 08.10.20: 08.10.21: Juergen
            if not M06Sound.CheckSoundChannelDefined(LEDNr):
                _fn_return_value = '#ERROR#'
                P01.Cells(r, M25.Config__Col).Select()
                return _fn_return_value
            
        if Right(RTrim(Cmd), 1) == '/':
            Add_Backslash_to_End = True
            Cmd = RTrim(Cmd)
            Cmd = Left(Cmd, Len(Cmd) - 1)
        else:
            Add_Backslash_to_End = False
            # Don't add a '\' to all following lines
            # 02.03.20:
        Cmd = '  ' + Cmd + Comment
        
        if AddDescription:
            Cmd = M30.AddSpaceToLen(Cmd, 109) + ' /* ' + Description
        elif Description != '':
            Cmd = M30.AddSpaceToLen(Cmd, 109) + ' /*     "'
        Cmd = M30.AddSpaceToLen(Cmd, 300) + ' */'
        
        if Add_Backslash_to_End:
            Cmd = Cmd + ' /'
            # 25.11.19:
            
        AddDescription = False
        Res = Res + Cmd + vbCrLf 
        # 21.12.22 replace vbcr with vbcrlf
    # Added by Misha 29-03-2020
    # 14.06.20: Added from Mishas version
    # Changed by Misha 20-04-2020
    if InStr(Left(Res, InStr(Res, ')')), 'Multiplexer') > 0:
        Res = vbCrLf + M80.Get_Multiplexer_Group(Res, Description, r) + vbCrLf 
        # 21.12.22 replace vbcr with vbcrlf
    # End Changes by Misha
    if Inc_LocInChNr:
        LocInChNr = LocInChNr + P01.val(P01.Cells(r, M25.LocInCh_Col))
        # 18.11.19: Moved down
    _fn_return_value = Res
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Inp_Typ - ByVal 
#----------------------------------------------------------------
def Get_Typ_Const(Inp_Typ):
#----------------------------------------------------------------
    _fn_return_value=""
    M09.Set_Tast_Txt_Var()
    _select61 = str(Inp_Typ)
    if (_select61 == M09.OnOff_T):
        _fn_return_value = 'S_ONOFF,'
    elif (_select61 == M09.Red_T):
        _fn_return_value = 'B_RED,  '
    elif (_select61 == M09.Green_T):
        _fn_return_value = 'B_GREEN,'
    elif (_select61 == M09.Tast_T):
        _fn_return_value = 'B_TAST, '
    elif (_select61 == 'O_RET_MSG'):
        _fn_return_value = 'O_RET_MSG,'  # 12.03.23: Hardi    
    else:
        P01.MsgBox('Internal error: Undefined Inp_Typ: \'' + str(Inp_Typ) + '\' in Get_Typ_Const()', vbCritical, 'Internal error in Get_Typ_Const()')
        M30.EndProg()
    return _fn_return_value

#----------------------------------------------------------------
def Add_to_Err(r, Txt):
#----------------------------------------------------------------
    global Err
    
    if Err == '':
        r.Select()
        # Marc the first error location
    Err = Err + Txt + vbCr

#--------------------------------------------------------------------------------------------
def Add_Start_Value_Line(r, Mask, Pos, Description):
    global Start_Values, Channel
#--------------------------------------------------------------------------------------------
    Start_Values = Start_Values + M30.AddSpaceToLen('  MobaLedLib.Set_Input(' + str(Channel + Pos) + ', 1);', 109) + ' // ' + Description + vbCrLf 
    # 21.12.22 replace vbcr with vbcrlf

#--------------------------------------------------------------------------------------------
def Create_Start_Value_Entry(r):
#--------------------------------------------------------------------------------------------
    sv = Long()

    i = Long()

    Mask = Long()

    Description = String()
    #----------------------------------------------
    # Fill the global string "Start_Values"
    sv = P01.val(P01.Cells(r, M25.Start_V_Col))
    if sv == 0:
        return
    if sv < 0:
        Add_to_Err(P01.Cells(r, M25.Start_V_Col), M09.Get_Language_Str('Negativer Startwert in Zeile ') + r)
    Description = Get_Description(r)
    Mask = 1
    for i in vbForRange(0, P01.val(P01.Cells(r, M25.InCnt___Col)) - 1):
        if ( sv & Mask )  > 0:
            Add_Start_Value_Line(r, Mask, i, Description)
            Description = '   "'
        Mask = Mask * 2
    if sv > Mask - 1:
        Add_to_Err(P01.Cells(r, M25.Start_V_Col), M09.Get_Language_Str('Startwert in Zeile ') + str(r) + M09.Get_Language_Str(' ist zu groß. Maximal möglicher Wert: ') + str(Mask - 1))


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: AddrStr - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: LEDsInUse - ByRef 
#--------------------------------------------------------------------------------------------
def Create_Header_Entry(r, AddrStr, IsRM, LEDOffset, LEDsInUse, MaxLEDNrInSheet):
#--------------------------------------------------------------------------------------------
    global LEDNr, ConfigTxt, CurrentCounterId, Store_ValuesTxt, Store_Val_Written, InChTxt, Ext_AddrTxt, Channel,Start_Values,AddrComment, Channel
    
    _fn_return_value = False
    ADDR_BORDER = '           { '

    COMMENT_START = '      // '

    STORE_BORDER = '           { '

    Comment = String()

    AddrTxt_Line = String()

    Inp_Typ = String()

    InCnt = Long()

    Channel_or_define = String()

    Addr = Long()

    LEDs_Channel = Long()

    LEDs = String()

    ErrorMessage = String()

    ErrorTitle = String()

    Res = String()

    storeStatusType = Integer()

    TextLine = String()
    
    LEDCnt = Long()
    
    Inp_TypR = None
    #-----------------------------------------------------------------------------------
    # Fills the global strings
    # - "ConfigTxt":    Configuration array "MobaLedLib_Configuration()"
    # - "Ext_AddrTxt":  addresses for DCC, Selextrix or CAN: (Array Ext_Addr[])
    # - "Start_Values": Initial values for DCC, Selextrix or CAN
    # - "InChTxt":      defines like "#defines INCH_DCC_1_ONOFF " for expert user
    # Calculate "Channel" = the next input channel number
    Comment = Get_Description(r)
    InCnt = P01.val(P01.Cells(r, M25.InCnt___Col))
    # 08.10.21: avoid error is cell is empty
    if IsNumeric(AddrStr):
        Addr = P01.val(AddrStr)
    else:
        Addr = - 2
        # it's a variable
        Channel_or_define = AddrStr
    if Addr >= 0:
        Inp_TypR = P01.Cells(r, M25.Inp_Typ_Col)
        if IsRM == False:  
            # 12.02.23: Hardi        
            M20.Complete_Typ(Inp_TypR, True)
            # Check Inp_Typ. If not valid call the dialog
            if Inp_TypR == '':
                return _fn_return_value
            Inp_Typ = Inp_TypR
            # 12.02.23: Hardi
        else:
            M09.Set_Tast_Txt_Var()
            # Set the global variables Red_T, Green_T, ...
            # 12.02.23: Hardi
            Inp_Typ = M09.OnOff_T
            # 12.02.23: Hardi
            
        if AddressRangeExists(Addr, InCnt, Inp_Typ):
            # 12.02.23: Old: Inp_TypR
            Channel_or_define = Gen_Address_Define_Name(Addr, Inp_Typ)
            # 12.02.23: Old: Inp_TypR
            if InStr(InChTxt, Channel_or_define) == 0:
                Add_to_Err(P01.Cells(r, M25.Inp_Typ_Col), M09.Get_Language_Str('Die Adresse \'') + str(Addr) + M09.Get_Language_Str('\' in Zeile ') + str(r) + M09.Get_Language_Str(' wird bereits mit einem anderen Typ benutzt.'))
            Addr = - 2
        else:
            Channel_or_define = Channel
    ## VB2PY (CheckDirective) VB directive took path 1 on True
    # 26.04.20:
    # 10.08.21: Juergen add sound channel
    LEDs_Channel = P01.val(P01.Cells(r, M25.LED_Cha_Col))
    LEDs = P01.Cells(r, M25.LEDs____Col)
    if Trim(LEDs) == M02.SerialChannelPrefix:
        # 10.08.21: Juergen add sound channel
        if LEDs_Channel < 0 or LEDs_Channel >= M02.SERIAL_CHANNELS:
            ErrorMessage = Replace(Replace(M09.Get_Language_Str('Fehler: Der \'Sound Kanal\' in Zeile #1# ist ungültig.' + vbCr + 'Es sind die Sound Kanäle 0-#2# erlaubt.'), "#1#", r), '#2#', Str(M02.SERIAL_CHANNELS - 1))
            ErrorTitle = M09.Get_Language_Str('Ungültiger Sound Kanal')
    else:
        if LEDs_Channel < 0 or LEDs_Channel >= M02.LED_CHANNELS:
            ErrorMessage = Replace(Replace(M09.Get_Language_Str('Fehler: Der \'LED Kanal\' in Zeile #1# ist ungültig.' + vbCr + 'Es sind die Led Kanäle 0-#2# erlaubt.'), "#1#", r), '#2#', Str(M02.LED_CHANNELS - 1))
            ErrorTitle = M09.Get_Language_Str('Ungültiger LED Channel')
    if ErrorMessage != '':
        OldEvents = P01.Application.EnableEvents
        P01.Application.EnableEvents = False
        P01.Cells(r, M25.LED_Cha_Col).Select()
        P01.Application.EnableEvents = OldEvents
        P01.MsgBox(ErrorMessage, vbCritical, ErrorTitle)
        return _fn_return_value
    LEDNr = M20.Get_LED_Nr(LEDNr, r, LEDs_Channel)
    # Entry for the configuration array which contains the macros
    Res = Generate_Config_Line(LEDNr + LEDOffset[LEDs_Channel], Channel_or_define, r, M25.Config__Col, Addr) 
    # 17.04.23 Juergen
    if Res == '#ERROR#':
        return _fn_return_value
    ConfigTxt = ConfigTxt + Res
    #begin change 01.05.20: Jürgen
    _select62 = GetMacroStoreType(r)
    if (_select62 == M02.MST_CTR_NONE) or (_select62 == M02.MST_CTR_ON) or (_select62 == M02.MST_CTR_OFF):
        CurrentCounterId = CurrentCounterId + 1
    if IsRM:
        # 12.02.23: Hardi
        storeStatusType = M02.SST_S_ONOFF  
        # Eigentlich muss der Status nicht gespeichert werden
    else:    
        storeStatusType = Check_And_Get_Store_Status(r, Addr, Inp_TypR, Channel_or_define) 
        #ERROR? Inp_TypR might be Inp_Typ
    if storeStatusType < M02.MST_None:
        return _fn_return_value
    if IsRM:
        Inp_Typ = 'O_RET_MSG'
        # Very dirty
        # 12.02.23: Hardi
        # ToDo: Kann nur dann aktiviert werden wenn zusätzlich eine Zubehör Adresse empfangen wird
        #       Wenn die Zeile nicht aktiviert ist, dann wird das Store_Values[] array angelegt
        #       Das ist zunächst nicht schlimm solange "#define ENABLE_STORE_STATUS()" nicht verwendet wird
        #       Es gefällt mir aber nicht dass, wenn es benutzt wird, die Rückmelder im EEPROM gespeichert werden.
        storeStatusType = M02.SST_DISABLED    
    
    if storeStatusType > M02.MST_None:
        # get lastet translated name of channel
        if not Inp_TypR is None and Addr >= 0:
            Channel_or_define = Gen_Address_Define_Name(Addr, Inp_Typ)
        # 12.02.23: Old: Inp_TypR ToDo: Braucht man das "Not Inp_TypR Is Nothing" überhaupt
        if storeStatusType == M02.SST_S_ONOFF or storeStatusType == M02.SST_TRIGGER:
            # avoid duplicate entries
            if ( InStr(Store_Val_Written, ' ' + Channel_or_define + ' ') )  == 0:
                if storeStatusType == M02.SST_S_ONOFF:
                    TextLine = STORE_BORDER + 'IS_TOGGLE + '
                else:
                    TextLine = STORE_BORDER + 'IS_PULSE  + '
                    
                if InCnt > 63:
                    # 05.01.23: Hardi
                    P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Die Anzahl der zu speichernden Eingänge in Zeile #1# ist zu groß (> 63)'), '#1#', r), vbCritical, M09.Get_Language_Str('Fehler: Anzahl der Eingänge zu groß'))
            
                TextLine = TextLine + M30.AddSpaceToLen(str(InCnt), 2) + ', '
                TextLine = TextLine + M30.AddSpaceToLen(Channel_or_define, 20) + '},'
                TextLine = TextLine + COMMENT_START + Comment
                Store_ValuesTxt = Store_ValuesTxt + TextLine + vbCrLf
                # 21.12.22 replace vbcr with vbcrlf
                Store_Val_Written = Store_Val_Written + ' ' + Channel_or_define + ' '
                #end change 01.05.20: Jürgen
    if storeStatusType == M02.SST_COUNTER_ON:
        # diese Variante würde nur ein Byte pro Counter verwenden,
        # allerdings is der zusätzliche code zum Behandeln der zusätlzichen Liste
        # in den häufigsten Fällen größer als jene Bytes, die man mit dieser Variante einsparen könnte
        #TextLine = TextLine & AddSpaceToLen(CurrentCounterId, 4) & "},"
        #TextLine = TextLine & COMMENT_START & Comment
        #Store_CountersTxt = Store_CountersTxt & TextLine & vbCrLf
        TextLine = STORE_BORDER + 'IS_COUNTER    , '
        TextLine = TextLine + M30.AddSpaceToLen('COUNTER_ID ' + str(CurrentCounterId), 20) + '},'
        TextLine = TextLine + COMMENT_START + Comment
        Store_ValuesTxt = Store_ValuesTxt + TextLine + vbCrLf
        # 21.12.22 replace vbcr with vbcrlf
    #end change 01.05.20: Jürgen
    if Addr >= 0:
        # Defines for expert users and duplicate adresses
        InChTxt = InChTxt + Generate_Define_Line(Addr, r, Channel, Comment, IsRM)
        # Definition of the array with the external adresses for DCC, Selecrix and CAN
        AddrTxt_Line = ADDR_BORDER + M30.AddSpaceToLen(str(Addr), 5)
        #AddrTxt_Line = AddrTxt_Line + '+ ' + Get_Typ_Const(Inp_TypR) + ' ' + M30.AddSpaceToLen(InCnt, 2) + '},'
        AddrTxt_Line = AddrTxt_Line + '+ ' + M30.AddSpaceToLen(Get_Typ_Const(Inp_Typ), 11) + M30.AddSpaceToLen(str(InCnt), 2) + '},'
        # 13.02.23: Hardi: Added AddSpaceToLen(..11)
        Ext_AddrTxt = Ext_AddrTxt + AddrTxt_Line + COMMENT_START
        if AddrComment != '':
            Ext_AddrTxt = Ext_AddrTxt + M30.AddSpaceToLen(AddrComment, 10)
        Ext_AddrTxt = Ext_AddrTxt + Comment + vbCrLf
        # 21.12.22 replace vbcr with vbcrlf
        Create_Start_Value_Entry(r)
        # Calculate the next input channel number
        _with109 = P01.Cells(r, M25.InCnt___Col)
        if _with109.Value != '':
            if not IsNumeric(_with109.Value) or P01.val(_with109.Value) < 0 or P01.val(_with109.Value) > 100:
                _with109.Select()
                P01.MsgBox(M09.Get_Language_Str('Fehler: Eintrag \'') + _with109.Value + M09.Get_Language_Str('\' in InCnt Spalte ist ungültig'), vbCritical, M09.Get_Language_Str('Falscher InCnt Eintrag'))
                M30.EndProg()
            else:
                Channel = Channel + int(_with109.Value)
                # ToDo: Unterstützung für mehrere Zeilen in einer Zelle ?
    _fn_return_value = True
    # 20.10.23 Juergen: Fix 'Fehler bei der Funktion "include"  #10763'
    if P01.Cells(r, M25.LED_Nr__Col) != '':
        # has the line a LEdNr?
        # 03.03.23 Juergen: include feature
        if M20.Check_IsSingleChannelCmd(LEDs):
            if M20.Get_Parameter_from_Leds_Line(LEDs, 1) > 3:
                LEDCnt = 2
            else:
                LEDCnt = 1
        else:
            LEDCnt = M30.CellLinesSum(LEDs)
        if LEDNr > MaxLEDNrInSheet(LEDs_Channel):
            LEDsInUse[LEDs_Channel] = LEDsInUse(LEDs_Channel) +  ( LEDNr - Start_LED_Channel(LEDs_Channel) - MaxLEDNrInSheet(LEDs_Channel) )  + LEDCnt - 1
            MaxLEDNrInSheet[LEDs_Channel] = LEDNr - Start_LED_Channel(LEDs_Channel) + LEDCnt - 1
    return _fn_return_value

#--------------------------------------------------------------------------------------------
def Check_And_Get_Store_Status(r, Addr, Inp_TypR, Channel_or_define):
#--------------------------------------------------------------------------------------------
    # return
    # -1 for error
    # 0 for Store Status not enabled
    # 1 for Counter with status, Default on
    # 2 for Counter with status, Default off
    # 3 for Channel S_ONOFF
    # 4 for Channel TRIGGER
    _fn_return_value = M02.SST_NONE
    _with110 = P01.Cells(r, M25.Start_V_Col)
    _fn_return_value = Get_Store_Status(r, Addr, Inp_TypR, Channel_or_define)
    _select63 = _fn_return_value
    if (_select63 == M02.SST_COUNTER_OFF):
        # user forces status store to on
        if _with110.Value == M02.AUTOSTORE_ON:
            _fn_return_value = M02.SST_COUNTER_ON
        return _fn_return_value
    elif (_select63 == M02.SST_COUNTER_ON):
        if _with110.Value == M02.AUTOSTORE_OFF or  ( _with110.Value != '' and IsNumeric(_with110.Value) ) :
            _fn_return_value = M02.SST_COUNTER_OFF
            # 01.05.20: Added from Mail: or IsNumeric(.value)
        return _fn_return_value
    elif (_select63 == M02.SST_S_ONOFF) or (_select63 == M02.SST_TRIGGER):
        if _with110.Value == M02.AUTOSTORE_OFF or  (_with110.Value != '' and IsNumeric(_with110.Value) ) :
            _fn_return_value = M02.SST_NONE
            # 01.05.20: Added from Mail: or IsNumeric(.value)
        return _fn_return_value
    # user is not allow to force status store for functions that don't support this
    if _with110.Value == M02.AUTOSTORE_ON:
        _with110.Select()
        P01.MsgBox(M09.Get_Language_Str('Fehler: Eintrag \'') + _with110.Value + M09.Get_Language_Str('\' in Startwert Spalte ist ungültig'), vbCritical, 'Statusspeicherung für diese Funktion nicht möglich')
        _fn_return_value = - 1
    return _fn_return_value
#--------------------------------------------------------------------------------------------
def Get_Store_Status(r, Addr, Inp_TypR, Channel_or_define):
#--------------------------------------------------------------------------------------------
    # return
    # -1 for error
    # 0 for Store Status not enabled
    # 1 for Counter with status, Default on
    # 2 for Counter with status, Default off
    # 3 for Channel S_ONOFF
    # 4 for Channel TRIGGER
    fn_return_value = M02.SST_NONE
    storeType = GetMacroStoreType(r)
    if storeType == M02.MST_CTR_OFF:
        fn_return_value = M02.SST_COUNTER_OFF
        return fn_return_value
    if storeType == M02.MST_CTR_ON:
        fn_return_value = M02.SST_COUNTER_ON
        return fn_return_value
    if storeType == M02.MST_PREVENT_STORE:
        # 01.05.20: From Mail
        fn_return_value = M02.SST_NONE
        return fn_return_value
    fn_return_value = GetOnOffStoreType(r, Addr, Inp_TypR, Channel_or_define)
    return fn_return_value

#--------------------------------------------------------------------------------------------
def GetMacroStoreType(r):
#--------------------------------------------------------------------------------------------
    # 17.12.21: Jürgen Split into single line and multi line implementation
    return GetMacroStoreTypeLine(P01.Cells(r, M25.Config__Col))

#--------------------------------------------------------------------------------------------
def GetMacroStoreTypeLine(Config_Entry):
#--------------------------------------------------------------------------------------------
    Org_Macro_Row = Long()

    Parts = vbObjectInitialize(objtype=String)

    p = Long()

    OutCntStr = String()

    Org_Macro = String()

    Org_Arguments = String()
    #---------------------------------------------------
    _fn_return_value = M02.MST_None
    # 01.05.20: From Mail Old: GetMacroStoreType = 0
    if Trim(Config_Entry) == '':
        return _fn_return_value
    # no macro assigned
    Parts = Split(Config_Entry, vbLf)
    if ( LBound(Parts) != UBound(Parts) ) :
        _fn_return_value = GetMultilineMacroStoreType(Parts)
        return _fn_return_value 
    Parts = Split(Config_Entry, vbCr)
    if ( LBound(Parts) != UBound(Parts) ) :
        _fn_return_value = GetMultilineMacroStoreType(Parts)
        return _fn_return_value
    Parts = Split(Config_Entry, '(')
    if Trim(Parts(0)) == '':
        return _fn_return_value
    # no macro assigned
    Org_Macro_Row = M09SM.Find_Macro_in_Lib_Macros_Sheet(Parts(0) + '(')
    if Org_Macro_Row == 0:
        return _fn_return_value
    # macro not found
    _with112 = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
    _fn_return_value = P01.val(_with112.Cells(Org_Macro_Row, M02.SM_Type__COL))
    # 01.05.20: From Mail Old: GetMacroStoreType = Val(.Cells(Org_Macro_Row, SM_CountrCOL))
    return _fn_return_value

#--------------------------------------------------------------------------------------------
def GetMultilineMacroStoreType(lines):
#--------------------------------------------------------------------------------------------
    _fn_return_value = None
    line = Variant()
    #---------------------------------------------------
    # find the first macro have a defined store type
    # otherwise 0 = undefined
    _fn_return_value = M02.MST_None
    for line in lines:
        s = line
        _fn_return_value = GetMacroStoreTypeLine(s)
        if _fn_return_value != M02.MST_None:
            return _fn_return_value
    return _fn_return_value


#--------------------------------------------------------------------------------------------
def GetOnOffStoreType(r, Addr, Inp_TypR, Channel_or_define):
#--------------------------------------------------------------------------------------------
    TypConst = String()
    _fn_return_value = M02.SST_NONE
    if not Inp_TypR is None:
        if Inp_TypR != '':
            # 11.10.20: Prevent error message it the Userform_Selext_Typ* is aborted with ESC
            TypConst = Get_Typ_Const(Inp_TypR)
            if Addr >= 0:
                Channel_or_define = Gen_Address_Define_Name(Addr, Inp_TypR)
    else:
        TypConst = ''
    if Channel_or_define == '':
        return _fn_return_value
    # or all functions having Adress
    if Addr >= 0 and TypConst == 'S_ONOFF,':
        _fn_return_value = M02.SST_S_ONOFF
        return _fn_return_value
    value = P01.Cells(r, M25.InCnt___Col).Value #HL
    if  P01.Cells(r, M25.LED_Nr__Col) != '' and  value !='':
        if int(value) > 1:
            _fn_return_value = M02.SST_TRIGGER
            return _fn_return_value
    return _fn_return_value

def Get_RM_Addr(VarName, r):
    _fn_return_value = None
    # 12.02.23: Hardi
    #-----------------------------------------------------------------
    # VarName: "RM 300.1"
    _fn_return_value = - 1
    # Error
    if M06SW.USE_ATTiny_CAN_GBM:
        Parts = Split(Mid(VarName, 4), '.')
        if UBound(Parts) != 1:
            # VB2PY (UntranslatedCode) GoTo GenErrMsg
            pass
        Nr = XLWF.CDec('&H' + Parts(0) + Parts(1))
        if Parts(1) >= 8:
            M06SW.ATTINY_GBM_CHECK_ERROR = True
        # Achtung die Adresse kann maximal 3FFF sein (Siehe "#define ADDR_MSK  0x3FFF  // 14 Bits are used for the Address")
        # Damit könnten bis GBM Messages 6FF verarbeitet werde.
        # Zunächst sollen aber 255 GBM Module reichen (Siehe Write_ATTINY_GBM_H_if_used)
        if Nr <= XLWF.CDec('&H3000') or Nr > XLWF.CDec('&H3FFF'):
            # VB2PY (UntranslatedCode) GoTo GenErrMsg
            Add_to_Err(P01.Cells(r, M25.DCC_or_CAN_Add_Col), Replace(M09.Get_Language_Str('Die Rückmelder Adresse #1# ist nicht ungültig'), '#1#', VarName))
            return _fn_return_value
        _fn_return_value = Nr - 0x3000
        # Add to ATTINY_GBM_SW_Filter
        SW_Filter_Byte = '0x' + Right(UCase(Parts(0)), 2) + ', '
        if InStr(M06SW.ATTINY_GBM_SW_Filter, SW_Filter_Byte) == 0:
            M06SW.ATTINY_GBM_SW_Filter = M06SW.ATTINY_GBM_SW_Filter + SW_Filter_Byte
    else:
        Add_to_Err(P01.Cells(r, M25.DCC_or_CAN_Add_Col), M09.Get_Language_Str('Der Rückmelder Typ ist nicht definiert. Dazu muss z.B. die Zeile \'#define USE_ATTiny_CAN_GBM\' in die Konfiguration eingetragen werden'))
    return _fn_return_value

    Add_to_Err(P01.Cells(r, M25.DCC_or_CAN_Add_Col), Replace(M09.Get_Language_Str('Die Rückmelder Adresse #1# ist nicht ungültig'), '#1#', VarName))
    return _fn_return_value

def Write_ATTINY_GBM_H_if_used(fp):
    # 13.02.23: Hardi
    #----------------------------------------------------
    if not M06SW.USE_ATTiny_CAN_GBM:
        return
    if M06SW.ATTINY_GBM_CHECK_ERROR:
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '#define ATTINY_GBM_CHECK_ERROR         // Check the error flags of the Arduino CAN GBM also', '\n')
    if M06SW.ATTINY_GBM_SW_Filter != '':
        # Wenn maximal 4 GBM Module verwendet werden, dann kann man den CAN Filter ganz exakt setzen
        # da der MCP2515 4 Filter für den Message Buffer 1 hat
        # Der Message Buffer 0 wird zum empfangen der 29 Bit Märklin messages genutzt.
        if UBound(Split(M06SW.ATTINY_GBM_SW_Filter, ',')) <= 4:
            VBFiles.writeText(fp, '', '\n')
            VBFiles.writeText(fp, '#define Is_in_ATTINY_GBM_SW_Filter(x) 1 // Dummy macro because the SW filter is not used', '\n')
            VBFiles.writeText(fp, '', '\n')
            Nr = 1
            for ByteStr in Split(M06SW.ATTINY_GBM_SW_Filter, ','):
                ByteStr = Trim(ByteStr)
                if ByteStr != '':
                    VBFiles.writeText(fp, '#define ATTINY_GBM_FILTER' + Nr + Replace(ByteStr, '0x', ' 0x3'), '\n')
                Nr = Nr + 1
        else:
            # Wenn mehr als 4 GBM Module verwendet werden, dann kann man den Filter nicht mehr exakt
            # setzen. Darum wird ein zusätzlicher SW Filter eingebaut. Das erhöht zwar die CPU last,
            # läst sich aber nicht verhindern.
            # Zunächst nehmen wir an, das nur 255 GBM Module = 2040 Belegtmelder vorhanden sind
            # => MsgId 300 - 3FF
            # Dann muss der SW Filter nur das letzte Byte der MsgID prüfen.
            VBFiles.writeText(fp, '', '\n')
            VBFiles.writeText(fp, '// Set message filter to pass all 0x03xx messages', '\n')
            VBFiles.writeText(fp, '#define ATTINY_GBM_MASK_BUFF1     0x1300  // Bits to check', '\n')
            VBFiles.writeText(fp, '#define ATTINY_GBM_FILTER_BUFF1   0x0300', '\n')
            VBFiles.writeText(fp, '', '\n')
            VBFiles.writeText(fp, '#define ATTINY_GBM_SW_FILTER              // Using an additional software CAN filter', '\n')
            VBFiles.writeText(fp, '', '\n')
            VBFiles.writeText(fp, 'const PROGMEM uint8_t ATTINY_GBM_SW_Filter[] =', '\n')
            VBFiles.writeText(fp, '       {', '\n')
            VBFiles.writeText(fp, '       ' + M06SW.ATTINY_GBM_SW_Filter, '\n')
            VBFiles.writeText(fp, '       };', '\n')
            VBFiles.writeText(fp, '', '\n')
            VBFiles.writeText(fp, '//------------------------------------------------', '\n')
            VBFiles.writeText(fp, 'uint8_t Is_in_ATTINY_GBM_SW_Filter(uint32_t MsgId)', '\n')
            VBFiles.writeText(fp, '//------------------------------------------------', '\n')
            VBFiles.writeText(fp, '{', '\n')
            VBFiles.writeText(fp, '  uint8_t MsgID_Byte = MsgId & 0xFF; // Check only the lower byte. The upper byte is always 0x03)', '\n')
            #Print #fp, "  Serial.print(MsgId,HEX); Serial.print("" SW_Filter:""); Serial.print(sizeof(ATTINY_GBM_SW_Filter));Serial.print(""  "");"
            VBFiles.writeText(fp, '  for (const uint8_t *p = (const uint8_t*)ATTINY_GBM_SW_Filter, *e = p + sizeof(ATTINY_GBM_SW_Filter); p < e; )', '\n')
            VBFiles.writeText(fp, '      {', '\n')
            VBFiles.writeText(fp, '      uint8_t b = pgm_read_byte_near(p);', '\n')
            #Print #fp, "      Serial.print(b,HEX); Serial.print("" "");"
            VBFiles.writeText(fp, '      if (MsgID_Byte == b) return 1;', '\n')
            VBFiles.writeText(fp, '      p++;', '\n')
            VBFiles.writeText(fp, '      }', '\n')
            #Print #fp, "  Serial.println("""");"
            VBFiles.writeText(fp, '  return 0;', '\n')
            VBFiles.writeText(fp, '}', '\n')
            VBFiles.writeText(fp, '', '\n')



#--------------------------------------------------------------------------------------------
def Create_HeaderFile(CreateFilesOnly = False): #20.12.21: Jürgen add CreateFilesOnly for programatically generation of header files
#--------------------------------------------------------------------------------------------
    _fn_return_value = False
    Ctrl_Pressed = False
    SimulatorOnly = False
    r = Long()
    
    LED_Offset = vbObjectInitialize((M02.LED_CHANNELS - 1,), Long)

    LEDsInUse = vbObjectInitialize((M02.LED_CHANNELS - 1,), Long)
    # 20.12.21: Jürgen add CreateFilesOnly for programatically generation of header files
    #-----------------------------
    # Is called if the "Z. Arduino schicken" button is pressed
    P01.set_statusmessage(M09.Get_Language_Str("Headerfile wird erstellt"))
    _fn_return_value = False
     # 20.12.21: Jürgen
    M30.Check_Version()
    # 21.11.21: Juergen
    M20.Update_Start_LedNr()
    # 11.10.20: To prevent problems if the calculation was not called before for some reasons
    M30.Clear_Platform_Parameter_Cache()
    # 14.10.2021: Juergen force reload of Platofmr Paramters every time a new header is created
    #removed by HaLi 9.12.2021
    #Ctrl_Pressed = GetAsyncKeyState(VK_CONTROL) != 0
    #if Ctrl_Pressed:
    #    UserForm_Header_Created.DontShowAgain = False
    M25.Make_sure_that_Col_Variables_match()
    #P01.set_statusmessage(M09.Get_Language_Str("Headerfile wird erstellt. Init Headerfile Generation"))
    
    #if not Init_HeaderFile_Generation():
    #    return _fn_return_value
    
    # 04.03.22 Juergen: If shift key is pressed to configuration is sent to the simulator only, also if Autostart Option 3  = simulatorOnly
    shift_pressed = P01.GetAsyncKeyState(P01.__VK_SHIFT)
    Debug.Print("Shift_pressed: %s",shift_pressed)
    
    # 17.03.22 Juergen: shift key is reverses simualtor option
    #SimulatorOnly = Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0) = 3 and GetAsyncKeyState(VK_SHIFT) = 0
    SimulatorOnly = M28.Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0) == 3 and shift_pressed
        
    if not SimulatorOnly:
        SimulatorOnly = M28.Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0) != 3 and shift_pressed
       
    if SimulatorOnly and CreateFilesOnly == False and M02a.Get_BoardTyp() == 'AM328':
        Debug.Print(" go to UploadToSimulator")
        _fn_return_value = M39.UploadToSimulator(True)
        return _fn_return_value
    if not Init_HeaderFile_Generation():
        return _fn_return_value
    if not ProcessSheet(P01.ActiveSheet.Name, True, 0, LED_Offset, LEDsInUse):
        return _fn_return_value
    if M06SW.Check_Detected_Variables() == False:
        return _fn_return_value
    if M37.CheckArduinoHomeDir() == False:
        return _fn_return_value
    # 02.12.21: Juergen see forum post #7085
    _fn_return_value = Write_Header_File_and_Upload_to_Arduino(CreateFilesOnly)
    # 20.12.21: Jürgen return result of called function
    return _fn_return_value

def CheckIncludeSheet(SheetName, row):
    _fn_return_value = None
    item = Variant()
    # 10.03.23 Juergen - include feature
    _fn_return_value = M30.WorksheetExists(SheetName)
    if not _fn_return_value:
        P01.MsgBox(M09.Get_Language_Str('Es wurde versucht, ein Blatt einzubinden, welches nicht existiert. Der Blattname lautet: \'') + P01.ActiveSheet.Name + ' -> ' + SheetName + '\'' + M09.Get_Language_Str('\' in Zeile ') + row, vbCritical, M09.Get_Language_Str('Fehler beim Einbinden eines Blattes'))
        return _fn_return_value
    for item in IncludeStack:
        if UCase(item) == UCase(SheetName):
            P01.MsgBox(M09.Get_Language_Str('Beim Einbinden eines Blattes wurde ein Zirkelbezug festgestellt. Der Blattname lautet: \'') + P01.ActiveSheet.Name + ' -> ' + SheetName + '\'' + M09.Get_Language_Str('\' in Zeile ') + row, vbCritical, M09.Get_Language_Str('Fehler beim Einbinden eines Blattes'))
            _fn_return_value = False
            return _fn_return_value
    if M25.Page_ID != P01.ThisWorkbook.Worksheets(SheetName).Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL).Value:
        P01.MsgBox(M09.Get_Language_Str('Das Einbinden eines Blattes mit einem unterschiedlichen Steuerungstyps ist nicht möglich: Der Blattname lautet: \'') + P01.ActiveSheet.Name + ' -> ' + SheetName + '\'' + M09.Get_Language_Str('\' in Zeile ') + Row + ' ' + P01.ThisWorkbook.Worksheets(SheetName).Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL).Value, vbCritical, M09.Get_Language_Str('Fehler beim Einbinden eines Blattes'))
        _fn_return_value = False
        return _fn_return_value
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: LEDsInUse - ByRef 
def ProcessSheet(SheetName, firstSheet, addressOffset, LEDsOffset, LEDsInUse):
    _fn_return_value = None
    r = Long()
    sx = Boolean()
    MaxLEDNrInSheet = vbObjectInitialize((M02.LED_CHANNELS - 1,), Integer)
    _fn_return_value = False
    # 20.10.23: Juergen fix #10763
    for idx in vbForRange(0, M02.LED_CHANNELS - 1):
        MaxLEDNrInSheet[idx] = - 1
    if not M30.WorksheetExists(SheetName):
        return _fn_return_value
    PG.ThisWorkbook.Worksheets(SheetName).Activate()
    M25.Make_sure_that_Col_Variables_match()
    if M06SW.Init_HeaderFile_Generation_SW(firstSheet) == False:
        return _fn_return_value
    if M06LED.Init_HeaderFile_Generation_LED2Var(firstSheet) == False:
        return _fn_return_value
    # 08.10.20:
    if M06Sound.Init_HeaderFile_Generation_Sound(firstSheet) == False:
        return _fn_return_value
    # 08.10.21: Juergen
    if M38.Init_HeaderFile_Generation_Extension(firstSheet) == False:
        return _fn_return_value
    # 31.01.22: Juergen    
    sx = M25.Page_ID == 'Selectrix'
    for r in vbForRange(M02.FirstDat_Row, M30.LastUsedRow()): #*HL
        if not ProcessLine(r, sx, addressOffset, LEDsOffset, LEDsInUse, MaxLEDNrInSheet):
            return _fn_return_value
    _fn_return_value = True
    return _fn_return_value
    
def IsIncludeMacro(Cmd):
    _fn_return_value = None
    SheetName = String()

    addressOffset = Long()
    SheetName=""
    addressOffset = 0
    _fn_return_value, SheetName, addressOffset = GetIncludeArgs(Cmd,SheetName, addressOffset)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SheetName - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: addressOffset - ByRef 
def GetIncludeArgs(Cmd, SheetName, addressOffset):

    _fn_return_value = None
    if Left(Cmd, 8) == 'include(':
        args = Split(Mid(Cmd, 9, Len(Cmd) - 9), ',')
        #todo error handling
        if UBound(args) - LBound(args) == 1:
            if Len(args(0)) > 0 and IsNumeric(args(1)):
                SheetName = args(0)
                addressOffset = P01.val(args(1))
                _fn_return_value = True
                return _fn_return_value, SheetName, addressOffset
    _fn_return_value = False
    return _fn_return_value, SheetName, addressOffset

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: LEDsInUse - ByRef 
def ProcessLine(r, sx, addressOffset, LEDsOffset, LEDsInUse, MaxLEDNrInSheet):
    global includeCount, AddrComment, IsRM
    
    oldOffset = {}
    newOffset = {}
    SheetName = ""
    Offset = 0
    _fn_return_value = False        
    if not P01.Rows(r).EntireRow.Hidden and P01.Cells(r, M02.Enable_Col) != '':
        P01.set_statusmessage(M09.Get_Language_Str("Headerfile wird erstellt. 2nd round - Macrozeile: "+str(r)), monitor_message=True)
        
        Cmd = Trim(P01.Cells(r, M25.Config__Col))
        if IsIncludeMacro(Cmd):
            res, SheetName, Offset=GetIncludeArgs(Cmd, SheetName, Offset)
            for idx in vbForRange(0, M02.LED_CHANNELS - 1):
                oldOffset[idx] = LEDsOffset(idx)
                newOffset[idx] = LEDsOffset(idx) + LEDsInUse(idx)
            _fn_return_value = CheckIncludeSheet(SheetName, r)
            if _fn_return_value:
                currentSheet = P01.ActiveSheet.Name
                IncludeStack.Add(( SheetName ))
                P01.Application.ScreenUpdating = False
                _fn_return_value = ProcessSheet(SheetName, False, addressOffset + Offset, newOffset, LEDsInUse)
                includeCount = includeCount + 1
                PG.ThisWorkbook.Worksheets(currentSheet).Activate()
                P01.Application.ScreenUpdating = True
                IncludeStack.Remove(( IncludeStack.Count() ))
            return _fn_return_value
        Addr = - 1
        IsRM = False
        # 12.02.23: Hardi        
        if M25.Address_starts_with_a_Number(r):
            if sx: 
                # *** Selectrix ***
                Bit_P = P01.Cells(r, M25.SX_Bitposi_Col)
                if Bit_P != '' and P01.val(P01.Cells(r, M25.InCnt___Col)) > 0:
                    if P01.Cells(r, M25.SX_Channel_Col) != '':
                        SX_Ch = M25.Get_First_Number_of_Range(r, M25.SX_Channel_Col)
                        # ToDo: SX_Ch wird nur dann aktualisiert wenn Bit pos vorhanden ist und InCnt > 0. Ist das gut ?
                    if SX_Ch >= 0 and SX_Ch <= 99:
                        if int(Bit_P) >= 1 and int(Bit_P) <= 8:
                            Addr = SX_Ch * 8 + int(Bit_P) - 1
                            Addr = Addr + addressOffset
                            AddrComment = 'SX ' + M30.AddSpaceToLenLeft(SX_Ch, 2) + ',' + str(Bit_P) + ': '
                        else:
                            Add_to_Err(P01.Cells(r, M25.SX_Bitposi_Col), 'Wrong bitpos " & bp & " in row ' + str(r))
                    else:
                        Add_to_Err(P01.Cells(r, M25.SX_Channel_Col), 'Wrong SX channel in row ' + str(r))
            else:
                # *** DCC, LNet or CAN ***
                if M25.Page_ID == 'DCC':
                    MaxAddr = 10240
                    # Attention some stations only support adresses up to 9999 => Don't generate a warning. The central station will generate an error
                elif M25.Page_ID == 'LNet':
                    # 24.04.23: Juergen
                    MaxAddr = 2048
                else:
                    MaxAddr = 65535
                    # 2048? MS2 only 320 ?
                Addr = M25.Get_First_Number_of_Range(r, M25.DCC_or_CAN_Add_Col)
                if Addr == '' or P01.val(P01.Cells(r, M25.InCnt___Col)) <= 0:
                    if Addr != '':
                        Add_to_Err(P01.Cells(r, M25.DCC_or_CAN_Add_Col), M09.Get_Language_Str('Die Ausgewählte Funktion in Zeile ') + str(r) + M09.Get_Language_Str(' ist immer aktiv und kann nicht über DCC, LNet oder CAN geschaltet werden.'))
                    Addr = - 1
                    # No address given of InCnt <= 0 or empty
                elif Addr >= 1 and Addr + addressOffset <= MaxAddr:
                    # Valid adress range
                    Addr = Addr + addressOffset
                else:
                    Add_to_Err(P01.Cells(r, M25.DCC_or_CAN_Add_Col), M09.Get_Language_Str('Die Adresse \'') + Replace(P01.Cells(r, M25.DCC_or_CAN_Add_Col), vbLf, ' ') + M09.Get_Language_Str('\' in Zeile ') + str(r) + M09.Get_Language_Str(' ist ungültig.'))
        else:
            # Address or selectrix channel entry doesn't start with a number
            # 03.04.20:
            VarName = M25.Get_Address_String(r)
            if VarName != '':
                if Left(VarName, Len('RM ')) == 'RM ':
                    # Rückmelder Adresse
                    # 12.02.23:
                    Addr = Get_RM_Addr(VarName, r)
                    IsRM = True
                else:                
                    if not M06SW.Valid_Var_Name(VarName, r):
                        return _fn_return_value
                    Addr = VarName
        if not Create_Header_Entry(r, Addr, IsRM, LEDsOffset, LEDsInUse, MaxLEDNrInSheet):
            _fn_return_value = False
            return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByRef 
def DelTailingEmptyLines(Txt):
    #----------------------------------------------------
    while Right(Txt, 4) == vbCrLf + vbCrLf:
        # 21.12.22 replace vbcr with vbcrlf
        Txt = Left(Txt, Len(Txt) - 3)    
    while Right(Txt, 2) == vbCr + vbCr:
        Txt = Left(Txt, Len(Txt) - 1)
    return Txt

def Ext_AddrTxt_Used():
    global Ext_AddrTxt
    
    #--------------------------------------------
    # Check if DCC, SX or CAN is used
    _fn_return_value = ( Ext_AddrTxt != '' )
    return _fn_return_value

def Store_ValuesTxt_Used():
    global Store_ValuesTxt
    
    #--------------------------------------------
    _fn_return_value = ( Store_ValuesTxt != '' )
    return _fn_return_value

def Write_Header_File_and_Upload_to_Arduino(CreateFilesOnly=False): #20.12.21: Jürgen add CreateFilesOnly for programatically generation of header files
    global Err, Ext_AddrTxt, Store_ValuesTxt, InChTxt, LocInChNr, Channel, ConfigTxt, LEDs_per_ChannelList, Start_Values
    _fn_return_value = False
    
    NumLeds = Long()

    Nr = Long()

    MaxLed = Long()

    Name = String()

    ShortPath = String()

    p = Long()

    fp = Integer()

    House_Min_T = String()

    House_Max_T = String()

    Color_Test_Mode = String()
    # 20.12.21: Jürgen add CreateFilesOnly for programatically generation of header files
    #----------------------------------------------------
    
    Err=""
    MaxLed = M30.Get_Current_Platform_Int('MaxLed')
    for Nr in vbForRange(0, M02.LED_CHANNELS - 1):
        NumLeds = NumLeds + P01.val(P01.Cells(M02.SH_VARS_ROW, M20.Get_LED_Nr_Column(Nr)))
        # 26.04.20: Old: NumLeds = Cells(SH_VARS_ROW, LED_Nr__Col)
    if NumLeds < MINLEDs:
        # To be able to test at least 20 LEDs with the color test program
        # 26.10.20:        
        NumLeds = MINLEDs
    if NumLeds > MaxLed:
        Err = Err + M09.Get_Language_Str('Maximale LED Anzahl überschritten: ') + str(NumLeds) + vbCr + M09.Get_Language_Str('Es sind maximal #1# RGB LEDs möglich') + vbCr
        # Don't check before to be able to temprory add more than 256 LES
        Err = Replace(Err, "#1#", str(MaxLed))
        # 03.04.21 Juergen replace with actual number
    if Err != '':
        P01.MsgBox(Err + vbCr + vbCr + M09.Get_Language_Str('Ein neues Header file wurde nicht generiert!'), vbCritical, M09.Get_Language_Str('Es sind Fehler aufgetreten'))
        return _fn_return_value
    Name = M08.GetWorkbookPath() + '/' + M02.Ino_Dir_LED + M02.Include_FileName
    Debug.Print("Write_Header - Filename:"+Name)
    Ext_AddrTxt=DelTailingEmptyLines(Ext_AddrTxt)
    Store_ValuesTxt=DelTailingEmptyLines(Store_ValuesTxt)
    # 01.05.20: Jürgen
    InChTxt=DelTailingEmptyLines(InChTxt)
    InChTxt, Channel = M06SW.Create_Loc_InCh_Defines(InChTxt, Channel, LocInChNr)
    p = InStrRev(M08.GetWorkbookPath(), '/')
    if p == 0:
        p = InStrRev(M08.GetWorkbookPath(), '/')
    if p > 0:
        ShortPath = Mid(M08.GetWorkbookPath(), p + 1, 255) + ' '
    #ShortPath = "Ver_"+ M02.Lib_Version_Nr+" "
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    #try:
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '// This file contains the ' + M25.Page_ID + ' and LED definitions.', '\n')
    VBFiles.writeText(fp, '//', '\n')
    VBFiles.writeText(fp, '// It was automatically generated by the program ' + PG.ThisWorkbook.Name + ' ' + M02.Prog_Version + '      by Hardi', '\n')
    VBFiles.writeText(fp, '// File creation: ' + P01.Date_str() + ' ' + P01.Time_str(), '\n')
    VBFiles.writeText(fp, '// (Attention: The display in the Arduino IDE is not updated if Options/External Editor is disabled)', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#ifndef __LEDS_AUTOPROG_H__', '\n')
    VBFiles.writeText(fp, '#define __LEDS_AUTOPROG_H__', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#ifndef CONFIG_ONLY', '\n')
    # 04.03.22 Juergen: add Simulator feature
    VBFiles.writeText(fp, '#ifndef ARDUINO_RASPBERRY_PI_PICO', '\n')
    VBFiles.writeText(fp, '#define FASTLED_INTERNAL       // Disable version number message in FastLED library (looks like an error)', '\n')
    # 11.01.20: Added Block
    VBFiles.writeText(fp, '#include <FastLED.h>           // The FastLED library must be installed in addition if you got the error message "..fatal error: FastLED.h: No such file or directory"', '\n')
    VBFiles.writeText(fp, '                               // Arduino IDE: Sketch / Include library / Manage libraries                    Deutsche IDE: Sketch / Bibliothek einbinden / Bibliothek verwalten', '\n')
    VBFiles.writeText(fp, '                               //              Type "FastLED" in the "Filter your search..." field                          "FastLED" in das "Grenzen Sie ihre Suche ein" Feld eingeben', '\n')
    VBFiles.writeText(fp, '                               //              Select the entry and click "Install"                                         Gefundenen Eintrag auswaehlen und "Install" anklicken', '\n')
    VBFiles.writeText(fp, '#else', '\n')
    VBFiles.writeText(fp, '#include <PicoFastLED.h>       // Juergens minimum version or FastLED for Raspberry Pico', '\n')
    VBFiles.writeText(fp, '#endif', '\n')
    VBFiles.writeText(fp, '#endif // CONFIG_ONLY', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#include <MobaLedLib.h>', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#define START_MSG "LEDs_AutoProg Ver 1: ' + ShortPath + P01.Format(P01.Date_str(), 'dd.mm.yy') + ' ' + P01.Format(P01.Time_str(), 'hh:mm') + '"', '\n')
    # The version could be read out in a future version of this tool
    VBFiles.writeText(fp, '', '\n')
    if M25.Page_ID == 'Selectrix':
        VBFiles.writeText(fp, '#define TWO_BUTTONS_PER_ADDRESS 0      // One button is used (Selectrix)', '\n')
        VBFiles.writeText(fp, '#define USE_SX_INTERFACE               // enable Selectrix protocol on single CPU mainboards', '\n')
        # 06.12.2021 Juergen add SX for ESP
    else:
        VBFiles.writeText(fp, '#define TWO_BUTTONS_PER_ADDRESS 1      // Two buttons (Red/Green) are used (DCC/LNet/CAN)', '\n')
    VBFiles.writeText(fp, '#ifdef NUM_LEDS', '\n')
    VBFiles.writeText(fp, '  #warning "\'NUM_LEDS\' definition in the main program is replaced by the included \'' + M30.FileNameExt(Name) + '\' with ' + str(NumLeds) + '"', '\n')
    VBFiles.writeText(fp, '  #undef NUM_LEDS', '\n')
    VBFiles.writeText(fp, '#endif', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#define NUM_LEDS ' + M30.AddSpaceToLen(str(NumLeds), 22) + '// Number of LEDs (Maximal 256 RGB LEDs could be used)', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#define LEDS_PER_CHANNEL ",' + str(LEDs_per_ChannelList) + '"', '\n')
    # 13.03.21 Juergen - for new Farbtest initialisation
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#define USE_PROTOCOL_' + UCase(M25.Page_ID), '\n')
    # 25.04.23 Juergen - defined for currently active protocol
    Write_ATTINY_GBM_H_if_used(fp)
    # 13.02.23: Hardi
    if M06SW.Alias_Names_List != '':
        VBFiles.writeText(fp, M06SW.Alias_Names_List, '\n')
    # 14.02.23: Hardi
    # Set HOUSE_MIN_T and HOUSE_MAX_T
    # 26.09.19:
    House_Min_T = M28.Get_String_Config_Var('MinTime_House')
    if House_Min_T != '':
        VBFiles.writeText(fp, '#undef  HOUSE_MIN_T', '\n')
        VBFiles.writeText(fp, '#define HOUSE_MIN_T  ' + str(P01.val(House_Min_T)), '\n')
    else:
        House_Min_T = 50
        # Default value used in the library
    House_Max_T = M28.Get_String_Config_Var('MaxTime_House')
    if House_Max_T != '':
        VBFiles.writeText(fp, '#undef  HOUSE_MAX_T', '\n')
        VBFiles.writeText(fp, '#define HOUSE_MAX_T ' + str(P01.val(House_Max_T)), '\n')
    else:
        House_Max_T = 150
        # Default value used in the library
    if P01.val(House_Min_T) > P01.val(House_Max_T) or P01.val(House_Max_T) == 0:
        PG.ThisWorkbook.Sheets(M02.ConfigSheet).Select()
        P01.Range('MinTime_House').Select()
        #XLWA.Sleep(100)
        P01.MsgBox(M09.Get_Language_Str('Fehler auf der \'Config\' Seite:' + vbCr + 'Die \'Minimale Zeit bis zur nächsten Änderung\' muss kleiner ' + 'oder gleich groß wie die Maximale Zeit sein.' + vbCr + 'Achtung: Wenn nichts eingegeben ist werden die Standard Werte vom 50/150 verwendet. ' + 'Dadurch kann es ebenfalls zu einem Konflikt kommen.'), vbCritical, M09.Get_Language_Str('Falsche Zeiten für die House() Funktion'))
        M30.EndProg()
    VBFiles.writeText(fp, '', '\n')
    Color_Test_Mode = M28.Get_String_Config_Var('Color_Test_Mode')
    _select64 = Left(UCase(Color_Test_Mode), 1)
    if (_select64 == 'J') or (_select64 == 'Y') or (_select64 == '1'):
        VBFiles.writeText(fp, '#define RECEIVE_LED_COLOR_PER_RS232' + vbCrLf, '\n')
        # 21.12.22 replace vbcr with vbcrlf
    if M28.Get_Bool_Config_Var('USE_SPI_Communication') or M25.Page_ID == 'CAN':
        # 14.05.20: Change the heartbeat LED pin
        # 04.10.20: Added: Page_ID = "CAN"
        if M28.Get_Bool_Config_Var('USE_SPI_Communication'):
            VBFiles.writeText(fp, '#define USE_SPI_COM                    // Use the SPI bus for the communication in addition to the RS232 if J13 is closed. If no DCC commands are configured the A1 pin of the DCC Arduino is disabled', '\n')
        if M06SW.PIN_A3_Is_Used():
            VBFiles.writeText(fp, '#define LED_HEARTBEAT_PIN -1           // Disable the heartbeat pin because it\'s used for the SwitchB or SwitchC', '\n')
        else:
            VBFiles.writeText(fp, '#define LED_HEARTBEAT_PIN A3           // Don\'t use the internal heartbeat LED because the D13 pins between LED and DCC arduin are connected together', '\n')
    if M28.Get_Num_Config_Var('GEN_BUTTON_RELEASE_COM') == 0 or M25.Page_ID == 'SX':
        # 09.04.23: GEN BUTTON RELEASE HANDLING if set to 0 (=legacy) or SX as input
        VBFiles.writeText(fp, '#define GEN_BUTTON_RELEASE', '\n')
    M08.WriteGenButtonReleaseDefine(( fp ))
 
    
    if Ext_AddrTxt_Used():
        if M28.Get_Bool_Config_Var('USE_SPI_Communication'):
            # 16.05.20:
            if M06SW.Check_Switch_Lists_for_SPI_Pins() == False:
                VBFiles.closeFile(fp)
                return _fn_return_value
        VBFiles.writeText(fp, '#define USE_EXT_ADDR', '\n')
        if InStr(M02.Prog_for_Right_Ardu, ' ' + M25.Page_ID + ' ') > 0:
            VBFiles.writeText(fp, '#define USE_RS232_OR_SPI_AS_INPUT      // Use the RS232 or SPI Input to read DCC/SX commands from the second Arduino and from the PC (The SPI is only used if enabled with USE_SPI_COM)', '\n')
        #    If Get_Bool_Config_Var("USE_SPI_Communication") Then
        # 14.05.20:
        #       Print #fp, "#define USE_SPI_COM                    // Use the SPI bus for the communication in addition to the RS232 if J13 is closed"
        #    End If
        # Set DCC Offset
        # 26.09.19:
        
        if M25.Page_ID == 'DCC':
            VBFiles.writeText(fp, '#define ADDR_OFFSET ' + str(P01.val(M28.Get_String_Config_Var('DCC_Offset'))), '\n')
        else:
            VBFiles.writeText(fp, '#define ADDR_OFFSET 0', '\n')
        
        if M25.Page_ID == 'CAN':
            VBFiles.writeText(fp, '#define USE_CAN_AS_INPUT', '\n')
        
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '#define ADDR_MSK  0x3FFF  // 14 Bits are used for the Address', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '#define S_ONOFF   (uint16_t)0', '\n')
        VBFiles.writeText(fp, '#define B_RED     (uint16_t)(1<<14)', '\n')
        VBFiles.writeText(fp, '#define B_GREEN   (uint16_t)(2<<14)', '\n')
        VBFiles.writeText(fp, '#define O_RET_MSG (uint16_t)(3<<14)    // Return messages (Rueckmelder)', '\n')
        #Print #fp, "#define B_RESERVE (uint16_t)(3<<14)    // Not used at the moment"
        VBFiles.writeText(fp, '#define B_TAST    B_RED', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'typedef struct', '\n')
        VBFiles.writeText(fp, '    {', '\n')
        VBFiles.writeText(fp, '    uint16_t AddrAndTyp; // Addr range: 0..16383. The upper two bytes are used for the type', '\n')
        VBFiles.writeText(fp, '    uint8_t  InCnt;', '\n')
        VBFiles.writeText(fp, '    } __attribute__ ((packed)) Ext_Addr_T;', '\n')
        # 05.11.20: Added: __attribute__ ((packed)) to be able to use it on oa 32 Bit platform
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '// Definition of external adresses', '\n')
        VBFiles.writeText(fp, '#ifdef CONFIG_ONLY', '\n')
        # 04.03.22 Juergen: add Simulator feature
        VBFiles.writeText(fp, 'const Ext_Addr_T Ext_Addr[] __attribute__ ((section (".MLLAddressConfig"))) =', '\n')
        VBFiles.writeText(fp, '#else', '\n')
        VBFiles.writeText(fp, 'const PROGMEM Ext_Addr_T Ext_Addr[] =', '\n')
        VBFiles.writeText(fp, '#endif', '\n')
        VBFiles.writeText(fp, '         { // Addr & Typ    InCnt', '\n')
        VBFiles.writeText(fp, Ext_AddrTxt)
        VBFiles.writeText(fp, '         };', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
    # Ext_AddrTxt_Used
    VBFiles.writeText(fp, '// Input channel defines for local inputs and expert users', '\n')
    # 05.10.19: Moved out of the if because the local inputs are also stored here
    VBFiles.writeText(fp, InChTxt, '\n')
    VBFiles.writeText(fp, '', '\n')
    
    fret, Channel = M06SW.Write_Switches_Header_File_Part_A(fp, Channel)
    if fret == False:
        VBFiles.closeFile(fp)
        return _fn_return_value
    if M06SW.Write_LowProrityLoop_Header_File(fp) == False:
        VBFiles.closeFile(fp)
        return _fn_return_value
    if M06LED.Write_Header_File_LED2Var(fp) == False:
        # 08.10.20:
        VBFiles.closeFile(fp)
        return _fn_return_value
    # 15.10.21: Juergen split creation of sound extensions to ensure that preprocessor defines are corretly compiled
    if M06Sound.Write_Header_File_Sound_Before_Config(fp) == False:
        VBFiles.closeFile(fp)
        return _fn_return_value
    # 31.01.22: Juergen add extension support
    if M38.Write_Header_File_Extension_Before_Config(fp) == False:
        VBFiles.closeFile(fp)
        return _fn_return_value
    VBFiles.writeText(fp, DayAndNightTimer, '\n')
    # 07.10.20:
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '//*******************************************************************', '\n')
    VBFiles.writeText(fp, '// *** Configuration array which defines the behavior of the LEDs ***', '\n')
    VBFiles.writeText(fp, 'MobaLedLib_Configuration()', '\n')
    VBFiles.writeText(fp, '  {', '\n')
    VBFiles.writeText(fp, ConfigTxt, '\n')
    VBFiles.writeText(fp, '  EndCfg // End of the configuration', '\n')
    VBFiles.writeText(fp, '  };', '\n')
    VBFiles.writeText(fp, '//*******************************************************************', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#ifndef COPYLED_OFF', '\n')
    # 23.05.23:
    VBFiles.writeText(fp, '#define COPYLED_OFF 0', '\n')
    VBFiles.writeText(fp, '#endif', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#ifndef COPYLED_OFF_ONCE', '\n')
    VBFiles.writeText(fp, '#define COPYLED_OFF_ONCE 1', '\n')
    VBFiles.writeText(fp, '#endif', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '//---------------------------------------------', '\n')
    VBFiles.writeText(fp, 'void Set_Start_Values(MobaLedLib_C &MobaLedLib)', '\n')
    VBFiles.writeText(fp, '//---------------------------------------------', '\n')
    VBFiles.writeText(fp, '{', '\n')
    VBFiles.writeText(fp, Start_Values)
    VBFiles.writeText(fp, '}', '\n')
    VBFiles.writeText(fp, '', '\n')
    #begin change 01.05.20: Jürgen
    if Store_ValuesTxt_Used():
        # 01.05.20: Juergen
        #Print #fp, "#define ENABLE_STORE_STATUS"
        # 01.05.20: disabled in Mail from Juergen
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '// if function returns TRUE the calling loop stops', '\n')
        VBFiles.writeText(fp, 'typedef bool(*HandleValue_t) (uint8_t CallbackType, uint8_t ValueId, uint8_t* Value, uint16_t EEPromAddr, uint8_t TargetValueId, uint8_t Options);', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '#define InCnt_MSK  0x003F  // 6 bits are used for the InCnt, 2 bits for the type ttcc cccc => Max InCnt=63', '\n')
        # 05.01.23: Hardi: Old : InCnt_MSK  0x0007
        VBFiles.writeText(fp, '#define IS_COUNTER (uint8_t)0x80', '\n')
        VBFiles.writeText(fp, '#define IS_PULSE   (uint8_t)0x40', '\n')
        VBFiles.writeText(fp, '#define IS_TOGGLE  (uint8_t)0x00', '\n')
        VBFiles.writeText(fp, '#define COUNTER_ID', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'typedef struct', '\n')
        VBFiles.writeText(fp, '    {', '\n')
        VBFiles.writeText(fp, '    uint8_t TypAndInCnt; // Type bits 7 & 6, InCnt 0..5', '\n')
        # 05.01.23: Hardi: Changed commemt
        VBFiles.writeText(fp, '    uint8_t Channel;', '\n')
        VBFiles.writeText(fp, '    } __attribute__ ((packed)) Store_Channel_T;', '\n')
        # 05.11.20: Added: __attribute__ ((packed)) to be able to use it on oa 32 Bit platform
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '// Definition of channels and counters that need to store state in EEProm' + vbCrLf + 'const PROGMEM Store_Channel_T Store_Values[] =' + vbCrLf + '         { // Mode + InCnt , Channel', '\n')
        # 21.12.22 replace vbcr with vbcrlf
        VBFiles.writeText(fp, Store_ValuesTxt)
        VBFiles.writeText(fp, '         };', '\n')
        VBFiles.writeText(fp, '', '\n')
    else:
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '// No macros used which are stored to the EEPROM => Disable the ENABLE_STORE_STATUS flag in case it was set in the excel sheet', '\n')
        VBFiles.writeText(fp, '#ifdef ENABLE_STORE_STATUS', '\n')
        # 01.05.20: New block in Mail from Juergen
        VBFiles.writeText(fp, '  #undef ENABLE_STORE_STATUS', '\n')
        VBFiles.writeText(fp, '#endif', '\n')
        VBFiles.writeText(fp, '', '\n')
    # Store_ValuesTxt_Used
    #end change 19.04.20 Jürgen
    VBFiles.writeText(fp, '#ifndef CONFIG_ONLY', '\n')
    # 04.03.22 Juergen: add Simulator feature
    # 15.10.21: Juergen move creation of onboard sound code after the configuration struture to ensue that #defines from ProgGenerator are effective
    if M06Sound.Write_Header_File_Sound_After_Config(fp) == False:
        VBFiles.closeFile(fp)
        return _fn_return_value
    # 31.01.22: Juergen add extension support
    if M38.Write_Header_File_Extension_After_Config(fp) == False:
        VBFiles.closeFile(fp)
        return _fn_return_value
    VBFiles.writeText(fp, '#endif // CONFIG_ONLY', '\n')
    # 04.03.22 Juergen: add Simulator feature
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#endif // __LEDS_AUTOPROG_H__', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if Channel - 1 > 250:
        P01.MsgBox(M09.Get_Language_Str('Fehler: Die Anzahl der verwendeten Eingangskanäle ist zu groß!' + vbCr + 'Es sind maximal 250 verfügbar. Die Konfiguration enthält aber ') + str(Channel - 1) + '.' + vbCr + vbCr + M09.Get_Language_Str('Die Eingangskanäle werden zum einlesen von DCC, LNet, Selectrix und CAN Daten benutzt. ' + vbCr + 'Außerdem werden sie als interne Zwischenspeicher benötigt.'), vbCritical, M09.Get_Language_Str('Anzahl der InCh Variablen überschritten'))
        M30.EndProg()
        
    if ConfigTxt == "": #*HL and M38.ExtensionsActiveCount == 0:                       # 17.04.22: Juergen improve empty configuration warning
        P01.MsgBox(M09.Get_Language_Str('Achtung: Es ist keine einzige Zeile in der Spalte "Beleuchtung, Sound, oder andere Effekte" aktiv!' + vbCr + '=> Das Programm wird keine LEDs ansteuern'), vbCritical, M09.Get_Language_Str('Achtung: Die Konfiguration ist leer'))
        #*HLUserForm_Header_Created.DontShowAgain = False
    P01.Application.StatusBar = Time + M09.Get_Language_Str(': Header Datei \'') + Name + M09.Get_Language_Str('\' wurde erzeugt')
    # 14.07.20: Don't use Show_Status_for_a_while because the compile time is shorter with Jürgens new PrivateBuild command
    #Show_Status_for_a_while Time & Get_Language_Str(": Header Datei '") & Name & Get_Language_Str("' wurde erzeugt")
    #*HL if CreateFilesOnly == False and UserForm_Header_Created.DontShowAgain == False:
    #*HL    UserForm_Header_Created.FileName = Name
    #*HL    UserForm_Header_Created.Show()
    M08.Compile_and_Upload_LED_Prog_to_Arduino(CreateFilesOnly)
    M20.ResetTestButtons(M06SW.Store_Status_Enabled)
    _fn_return_value = True
    return _fn_return_value
    #except:
    #    # Attention: This could also be an error some where else in the code
    P01.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Header Datei'))
    VBFiles.closeFile(fp)

# VB2PY (UntranslatedCode) Option Explicit
