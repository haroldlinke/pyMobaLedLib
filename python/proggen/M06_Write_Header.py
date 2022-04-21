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
#from proggen.M02_Public import *
#from proggen.M06_Write_Header_LED2Var import *
#from proggen.M06_Write_Header_Sound import *
#from proggen.M06_Write_Header_SW import *
#from proggen.M08_ARDUINO import *
#from proggen.M09_Language import *
#from proggen.M09_Select_Macro import *
#from proggen.M20_PageEvents_a_Functions import Update_Start_LedNr
#from proggen.M25_Columns import *
#from proggen.M28_divers import *
#from proggen.M30_Tools import *
#from proggen.M80_Create_Mulitplexer import *

#from ExcelAPI.P01_Workbook import *
#from mlpyproggen.F_UserForm_Header_Created import *

import proggen.M02_Public as M02
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
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M38_Extensions as M38
import proggen.M39_Simulator as M39
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80

import ExcelAPI.P01_Workbook as P01
from ExcelAPI.X01_Excel_Consts import *

""" Todo:

 - Wichtig: Die Schalter müssen auch in den Inputs der Macros erkannt werden sonst werden sie nur dann definiert wenn
   sie in der Adress Spalte stehen
 - Warnung generieren wenn Switch C und D Gleichzeitig verwendet werden und die gleichen Pins verwendet werden für C und D
"""

InChTxt = String()                                      # List of all defined DCC (SX or CAN) input channels in the form: "#defines INCH_DCC_1_ONOFF <Nr>"
Undefined_Input_Var = String()                          # List of all undefined input variables in the first step
Undef_Input_Var_Row = String()

AddrList = vbObjectInitialize(objtype=Long)
LocInChNr = int()
CurrentCounterId = int()
Ext_AddrTxt = String()
ConfigTxt = String()
Err = String()
Channel = int()
LEDNr = int()
AddrComment = String()
Start_Values = String()
Store_ValuesTxt = String()
Store_Val_Written = String()

Start_LED_Channel = vbObjectInitialize((M02.LED_CHANNELS - 1,), Long)
LEDs_per_Channel = vbObjectInitialize((M02.LED_CHANNELS - 1,), Long)
Max_Channels = int()
LEDs_per_ChannelList = String()

DayAndNightTimer = String()

MINLEDs = 20

#-------------------------------------------------------
def Init_HeaderFile_Generation():
#-------------------------------------------------------
    global MINLEDs, LocInChNr, CurrentCounterId, Ext_AddrTxt, Store_ValuesTxt, Store_Val_Written, InChTxt, ConfigTxt, Err, Channel, LEDNr, AddrComment, Start_Values
    global Undefined_Input_Var, DayAndNightTimer, Numleds, Maxchannels, LEDs_per_ChannelList, ReserveLeds, LEDs_per_Channel, Start_LED_Channel,AddrList
    
    
    ReserveLeds = int()

    NumLeds = int()

    Nr = int()
    
    fn_return_value = False
    
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
    
    if M06SW.Init_HeaderFile_Generation_SW() == False:
        return fn_return_value
    
    if M06LED.Init_HeaderFile_Generation_LED2Var() == False:
        return fn_return_value
        # 08.10.20:
        
    if M06Sound.Init_HeaderFile_Generation_Sound() == False:
        return fn_return_value
        # 08.10.21: Juergen
        
    if M38.Init_HeaderFile_Generation_Extension() == False:
        return fn_return_value      
    # 31.01.22: Juergen
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
    fn_return_value = True
    return fn_return_value

#-------------------------------------------------------
def AddressExists(Addr):
#-------------------------------------------------------
    global AddrList
    
    fn_return_value = False
    
    a = Variant()
    #------------------------------------------------------
    # ToDo: Überlappungen prüfen wenn InCnt > 1
    if not M30.IsArrayEmpty(AddrList):
        for a in AddrList:
            if a == Addr:
                fn_return_value = True
                return fn_return_value
        AddrList = vbObjectInitialize((UBound(AddrList) + 1,), int, AddrList)
    else:
        AddrList = vbObjectInitialize((0,), int, AddrList)
    AddrList[UBound(AddrList)] = Addr
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpTyp - ByVal 
#-------------------------------------------------------
def AddressRangeExists(Addr, Cnt, InpTyp):
#-------------------------------------------------------
    InpTypMod = int()

    i = int()
    #-------------------------------------------------------------------------------------
    # If the InpTyp is a button (Red / Green) two virtual adresses are used.
    # One for each button.
    # For OnOff switches one address is used twice
    # To destinguish the two cases the address is multiplied by 2 and 0/1 is added
    #
    fn_return_value = False
    M09.Set_Tast_Txt_Var()
    if (InpTyp == M09.Red_T):
        InpTypMod = 1
    elif (InpTyp == M09.Green_T):
        InpTypMod = 2
    elif (InpTyp == M09.OnOff_T):
        InpTypMod = 3
    elif (InpTyp == M09.Tast_T):
        InpTypMod = 3
    else:
        P01.MsgBox('Internal Error: Unknown InpTyp in AddressRangeExists' + InpTyp, vbCritical,"Error")
        M30.EndProg()
    Ad = Addr
    for i in vbForRange(1, Cnt):
        if InpTypMod & 1:
            if AddressExists(Ad * 2):
                fn_return_value = True
                return fn_return_value
        if InpTypMod & 2:
            if AddressExists(Ad * 2 + 1):
                fn_return_value = True
                return fn_return_value
        if (InpTypMod == 1):
            InpTypMod = 2
        elif (InpTypMod == 2):
            InpTypMod = 1
            Ad = Ad + 1
        elif (InpTypMod == 3):
            Ad = Ad + 1
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Inp_Typ - ByVal 
#-------------------------------------------------------
def Get_Next_Typ(Inp_Typ):
#-------------------------------------------------------
    M09.Set_Tast_Txt_Var()
    if (Inp_Typ == M09.OnOff_T):
        fn_return_value = M09.OnOff_T
    elif (Inp_Typ == M09.Red_T):
        fn_return_value = M09.Green_T
    elif (Inp_Typ == M09.Green_T):
        fn_return_value = M09.Red_T
    elif (Inp_Typ == M09.Tast_T):
        fn_return_value = M09.Tast_T
    else:
        P01.MsgBox('Internal error: Undefined Inp_Typ: \'' + Inp_Typ + '\' in Get_Next_Typ()', vbCritical, 'Internal error in Get_Next_Typ()')
        M30.EndProg()
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Addr - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InTyp - ByVal 
#----------------------------------------------------------------------------------
def Gen_Address_Define_Name(Addr, InTyp):
#----------------------------------------------------------------------------------
    if M25.Page_ID == 'Selectrix':
        fn_return_value = 'INCH_SX_' + str(Int(Addr / 8)) + '_' +  str(( Addr % 8 )  + 1 )+ Replace(Mid(Get_Typ_Const(InTyp), 2, 255), ',', '')
    else:
        fn_return_value = 'INCH_' + M25.Page_ID + '_' + str(Addr) + Replace(Mid(Get_Typ_Const(InTyp), 2, 255), ',', '')
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Addr - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Comment - ByVal 
#----------------------------------------------------------------------------------
def Generate_Define_Line(Addr, Row, Channel, Comment):
#----------------------------------------------------------------------------------
    COMMENT_DEFINE = '   // '

    Name = String()
    
    fn_return_value = ""

    i = int()

    InTyp = String()
    # Generate defines for the input channels for expert users
    InTyp = P01.Cells(Row, M25.Inp_Typ_Col)
    M09.Set_Tast_Txt_Var()
    for i in vbForRange(1, P01.val(P01.Cells(Row, M25.InCnt___Col))):
        #Name = "INCH_" & M25.Page_ID & "_" & Addr & Replace(Mid(Get_Typ_Const(InTyp), 2, 255), ",", "")
        Name = Gen_Address_Define_Name(Addr, InTyp)
        fn_return_value = fn_return_value + '#define ' + M30.AddSpaceToLen(Name, 22) + '  ' + M30.AddSpaceToLen(str(Channel), 4) + COMMENT_DEFINE + Comment + vbCr
        if InTyp != M09.Red_T:
            Addr = Addr + 1
        InTyp = Get_Next_Typ(InTyp)
        Channel = Channel + 1
        Comment = '    "'
    return fn_return_value

#----------------------------------------------------
def Get_Description(r):
#----------------------------------------------------
    fn_return_value = Trim(P01.Cells(r, M25.Descrip_Col))
    # If Get_Description = "" Then Get_Description = Cells(r, Config__Col) ' 02.03.20: Old: Why should the macro be repeated? It gets verry long if "#define" lines are used
    if fn_return_value == '':
        fn_return_value = 'Excel row ' + str(r)
        # 02.03.20: New
    fn_return_value = Replace(fn_return_value, vbLf, '| ')
    return fn_return_value

#----------------------------------------------------
def Activate_DayAndNightTimer(Cmd):
#----------------------------------------------------
    global DayAndNightTimer #"HL
    
    Args = vbObjectInitialize(objtype=String)

    Period = Double()
    #--------------------------------------------------------
    Args = Split(Trim(Replace(Replace(Cmd, 'DayAndNightTimer(', ''), ')', '')), ',')
    Period = P01.val(Trim(Args(1)))
    DayAndNightTimer = vbCr + '#define DayAndNightTimer_Period    ' + Round(Period * 60 * 1000 / 512, 0) + vbCr
    if Trim(Args(0)) != 'SI_1':
        DayAndNightTimer = DayAndNightTimer + '#define DayAndNightTimer_InCh      ' + Trim(Args(0)) + vbCr
    fn_return_value = True
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cmd - ByVal 
#----------------------------------------------------
def Do_Replace_Sym_Pin_Name(Cmd, PinStr):
#----------------------------------------------------

    MB_LED_Nr_Str_Arr = vbObjectInitialize(objtype=String)

    MB_LED_Pin_Nr_Arr = vbObjectInitialize(objtype=String)

    i = int()
    #----------------------------------------------------------------------------------------
    MB_LED_Nr_Str_Arr = Split(M02.MB_LED_NR_STR, ' ')
    MB_LED_Pin_Nr_Arr = Split(Replace(M02.MB_LED_PIN_NR, '  ', ' '), ' ')
    if UBound(MB_LED_Nr_Str_Arr) != UBound(MB_LED_Pin_Nr_Arr):
        P01.MsgBox('Internal Error: Array hafe different size in \'Do_Replace_Sym_Pin_Name()\'', vbCritical, 'Internal Error')
        M30.EndProg()
    for i in vbForRange(0, UBound(MB_LED_Nr_Str_Arr)):
        if PinStr == MB_LED_Nr_Str_Arr(i):
            fn_return_value = Replace(Cmd, '(' + MB_LED_Nr_Str_Arr(i) + ',', '(' + MB_LED_Pin_Nr_Arr(i) + ',')
            return fn_return_value
    P01.MsgBox('Internal Error: PinStr not found in \'Do_Replace_Sym_Pin_Name()\'', vbCritical, 'Internal Error')
    M30.EndProg()
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cmd - ByRef 
#----------------------------------------------------
def Proc_Special_Functions(Cmd, LEDNr, Channel):
#----------------------------------------------------
    fn_return_value = False
    
    if Left(Cmd, Len('Mainboard_LED(')) == 'Mainboard_LED(':
        PinOrNr = Split(Replace(Cmd, 'Mainboard_LED(', ''), ',')(0)
        if InStr(' ' + M02.MB_LED_NR_STR + ' ', ' ' + PinOrNr + ' ') > 0:
            Replace_Sym_Pin_Name = True
        if ( PinOrNr == '4' or PinOrNr == 'D4' )  and M06SW.PIN_A3_Is_Used():
            P01.MsgBox(M09.Get_Language_Str('Achtung: Die Mainboard LED 4 kann nicht benutzt werden wenn der PIN A3 an anderer Stelle benutzt wird (CAN, SwitchB oder SwitchC).'), vbCritical,M09.Get_Language_Str('Pin A3 ist bereits benutzt'))
            return fn_return_value, Cmd
        if PinOrNr == '13' or PinOrNr == 'D13':
            Cmd = Cmd + vbCr + '  #undef  LED_HEARTBEAT_PIN  /* Use the heartbeat LED at pin A3 */' + vbCr + '  #define LED_HEARTBEAT_PIN A3' + Space(79)
        if Replace_Sym_Pin_Name:
            Cmd = Do_Replace_Sym_Pin_Name(Cmd, PinOrNr)
        Cmd = Replace(Replace(Replace(Cmd, 'Mainboard_LED(', '#define Mainboard_LED'), ',', ' '), ')', '')
    if Left(Cmd, Len('DayAndNightTimer(')) == 'DayAndNightTimer(':
        if not Activate_DayAndNightTimer(Cmd):
            return fn_return_value, Cmd
        Cmd = '// ' + Cmd
    if InStr(Cmd, M02.SF_LED_TO_VAR) > 0:
        fret, Cmd = M06LED.Add_LED2Var_Entry(Cmd, LEDNr)
        if not fret:
            return fn_return_value, Cmd
    if InStr(Cmd, M02.SF_SERIAL_SOUND_PIN) > 0:
        fret, Cmd = M06Sound.Add_SoundPin_Entry(Cmd, LEDNr)
        if not fret:
            return fn_return_value
    fn_return_value = True, Cmd
    return fn_return_value, Cmd

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel_or_define - ByVal 
#----------------------------------------------------
def Generate_Config_Line(LEDNr, Channel_or_define, r, Config_Col, Addr):
#----------------------------------------------------
    
    global LocInChNr
    
    Txt = String()

    Lines = Variant()

    Line = Variant()

    Res = String()

    AddDescription = Boolean()

    Description = String()

    Inc_LocInChNr = False #Boolean()
    #-----------------------------------------------------------------------------------------------------------------------------------
    # ToDo: Add checks like
    # - open/closing braket test
    # - characters after #LED, #InCh
    Txt = P01.Cells(r, Config_Col)
    fn_return_value=""
    if Trim(Txt) == '':
        return fn_return_value
    Lines = Split(Txt, vbLf)
    Description = Get_Description(r)
    AddDescription = Description != ''
    for Line in Lines:
        Comment = ''
        Cmd = ''
        CommentStart = InStr(Line, '//')
        if CommentStart == 0:
            Cmd = Line
        elif CommentStart == 1:
            Comment = Line
        else:
            Cmd = Left(Line, CommentStart)
            Comment = Mid(Line, CommentStart + 1, 1000)
        if LEDNr < 0:
            P01.Cells(r, M25.Config__Col).Select()
            P01.MsgBox(M09.Get_Language_Str('Fehler: Die LED Nummer darf nicht negativ werden. Das kann durch eine falsche Angabe bei einem vorangegangenen "Next_LED" Befehl passieren.'), vbCritical, M09.Get_Language_Str('Fehler: Negative LED Nummer'))
            fn_return_value = '#ERROR#'
            return fn_return_value
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
            fn_return_value = '#ERROR#'
            P01.Cells(r, M25.Config__Col).Select()
            return fn_return_value
        
        if M38.IsExtensionKey(Cmd):
            if not M38.Add_Extension_Entry(Cmd):
                fn_return_value = '#ERROR#'
                P01.Cells(r, M25.Config__Col).Select()
            return fn_return_value        
        
        if P01.Cells(r, M25.LEDs____Col) == M02.SerialChannelPrefix:
            if not M06Sound.CheckSoundChannelDefined(LEDNr):
                fn_return_value = '#ERROR#'
                P01.Cells(r, M25.Config__Col).Select()
                return fn_return_value
            
        if Right(RTrim(Cmd), 1) == '/':
            Add_Backslash_to_End = True
            Cmd = RTrim(Cmd)
            Cmd = Left(Cmd, Len(Cmd) - 1)
        else:
            Add_Backslash_to_End = False
            
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
        Res = Res + Cmd + vbCr
    # Added by Misha 29-03-2020                                             ' 14.06.20: Added from Mishas version
    # Changed by Misha 20-04-2020
    if InStr(Left(Res, InStr(Res, ')')), 'Multiplexer') > 0:
        Res = vbCrLf + M80.Get_Multiplexer_Group(Res, Description, r) + vbCrLf
    # End Changes by Misha
    if Inc_LocInChNr:
        LocInChNr = LocInChNr + P01.val(P01.Cells(r, M25.LocInCh_Col))
        # 18.11.19: Moved down
    fn_return_value = Res
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Inp_Typ - ByVal 
#----------------------------------------------------------------
def Get_Typ_Const(Inp_Typ):
#----------------------------------------------------------------
    M09.Set_Tast_Txt_Var()
    Inp_Typ = str(Inp_Typ)
    if (Inp_Typ == M09.OnOff_T):
        fn_return_value = 'S_ONOFF,'
    elif (Inp_Typ == M09.Red_T):
        fn_return_value = 'B_RED,  '
    elif (Inp_Typ == M09.Green_T):
        fn_return_value = 'B_GREEN,'
    elif (Inp_Typ == M09.Tast_T):
        fn_return_value = 'B_TAST, '
    else:
        P01.MsgBox('Internal error: Undefined Inp_Typ: \'' + str(Inp_Typ) + '\' in Get_Typ_Const()', vbCritical, 'Internal error in Get_Typ_Const()')
        M30.EndProg()
    return fn_return_value

#----------------------------------------------------------------
def Add_to_Err(r, Txt):
#----------------------------------------------------------------
    global Err #*HL
    
    if Err == '':
        r.Select()
        # Marc the first error location
    Err = Err + Txt + vbCr
    Debug.Print("Add_to_Err:" + Err)

#--------------------------------------------------------------------------------------------
def Add_Start_Value_Line(r, Mask, Pos, Description):
    global Start_Values, Channel
#--------------------------------------------------------------------------------------------
    Start_Values = Start_Values + M30.AddSpaceToLen('  MobaLedLib.Set_Input(' + str(Channel + Pos) + ', 1);', 109) + ' // ' + Description + vbCr

#--------------------------------------------------------------------------------------------
def Create_Start_Value_Entry(r):
#--------------------------------------------------------------------------------------------
    sv = int()

    i = int()

    Mask = int()

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
#--------------------------------------------------------------------------------------------
def Create_Header_Entry(r, AddrStr):
#--------------------------------------------------------------------------------------------
    global LEDNr,ConfigTxt,Ext_AddrTxt,Start_Values,InChTxt, Channel, AddrComment, Store_Val_Written, Store_ValuesTxt
    ADDR_BORDER = '           { '

    COMMENT_START = '      // '

    STORE_BORDER = '           { '

    Comment = String()

    AddrTxt_Line = String()

    Inp_Typ = String()

    InCnt = int()

    Channel_or_define = String()

    Addr = int()

    LEDs_Channel = int()

    LEDs = String()

    ErrorMessage = String()

    ErrorTitle = String()

    Res = String()

    storeStatusType = Integer()

    TextLine = String()
    
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
    if IsNumeric(AddrStr):
        Addr = P01.val(AddrStr)
    else:
        Addr = - 2
        Channel_or_define = AddrStr
    if Addr >= 0:
        Inp_TypR = P01.Cells(r, M25.Inp_Typ_Col)
        M20.Complete_Typ(Inp_TypR, True)
        if Inp_TypR == '':
            return fn_return_value
        if AddressRangeExists(Addr, InCnt, Inp_TypR):
            Channel_or_define = Gen_Address_Define_Name(Addr, Inp_TypR)
            if InStr(InChTxt, Channel_or_define) == 0:
                Add_to_Err(P01.Cells(r, M25.Inp_Typ_Col), M09.Get_Language_Str('Die Adresse \'') + str(Addr) + M09.Get_Language_Str('\' in Zeile ') + str(r) + M09.Get_Language_Str(' wird bereits mit einem anderen Typ benutzt.'))
            Addr = - 2
        else:
            Channel_or_define = Channel
    ## VB2PY (CheckDirective) VB directive took path 1 on True
    LEDs_Channel = P01.val(P01.Cells(r, M25.LED_Cha_Col))
    LEDs = P01.Cells(r, M25.LEDs____Col)
    if Trim(LEDs) == M02.SerialChannelPrefix:
        if LEDs_Channel < 0 or LEDs_Channel >= M02.SERIAL_CHANNELS:
            ErrorMessage = Replace(Replace(M09.Get_Language_Str('Fehler: Der \'Sound Kanal\' in Zeile #1# ist ungültig.' + vbCr + 'Es sind die Sound Kanäle 0-#2# erlaubt.'), "#1#", r), '#2#', Str(M02.SERIAL_CHANNELS - 1))
            ErrorTitle = M09.Get_Language_Str('Ungültiger Sound Kanal')
    else:
        if LEDs_Channel < 0 or LEDs_Channel >= M02.LED_CHANNELS:
            ErrorMessage = Replace(Replace(M09.Get_Language_Str('Fehler: Der \'LED Kanal\' in Zeile #1# ist ungültig.' + vbCr + 'Es sind die Led Kanäle 0-#2# erlaubt.'), "#1#", r), '#2#', Str(M02.LED_CHANNELS - 1))
            ErrorTitle = M09.Get_Language_Str('Ungültiger LED Channel')
    if ErrorMessage != '':
        #OldEvents = Application.EnableEvents
        #Application.EnableEvents = False
        P01.Cells(r, M25.LED_Cha_Col).Select()
        #Application.EnableEvents = OldEvents
        P01.MsgBox(ErrorMessage, vbCritical, ErrorTitle)
        return fn_return_value
    LEDNr = M20.Get_LED_Nr(LEDNr, r, LEDs_Channel)
    # Entry for the configuration array which contains the macros
    Res = Generate_Config_Line(LEDNr, Channel_or_define, r, M25.Config__Col, Addr)
    if Res == '#ERROR#':
        return fn_return_value
    ConfigTxt = ConfigTxt + Res
    #begin change 01.05.20: Jürgen
    select_variable_ = GetMacroStoreType(r)
    if (select_variable_ == M02.MST_CTR_NONE) or (select_variable_ == M02.MST_CTR_ON) or (select_variable_ == M02.MST_CTR_OFF):
        CurrentCounterId = CurrentCounterId + 1
    storeStatusType = Check_And_Get_Store_Status(r, Addr, Inp_TypR, Channel_or_define)
    if storeStatusType < M02.MST_None:
        return fn_return_value
    if storeStatusType > M02.MST_None:
        # get lastet translated name of channel
        if not Inp_TypR is None and Addr >= 0:
            Channel_or_define = Gen_Address_Define_Name(Addr, Inp_TypR)
        if storeStatusType == M02.SST_S_ONOFF or storeStatusType == M02.SST_TRIGGER:
            # avoid duplicate entries
            if ( InStr(Store_Val_Written, ' ' + Channel_or_define + ' ') )  == 0:
                if storeStatusType == M02.SST_S_ONOFF:
                    TextLine = STORE_BORDER + 'IS_TOGGLE + '
                else:
                    TextLine = STORE_BORDER + 'IS_PULSE  + '
                TextLine = TextLine + M30.AddSpaceToLen(InCnt, 2) + ', '
                TextLine = TextLine + M30.AddSpaceToLen(Channel_or_define, 20) + '},'
                TextLine = TextLine + COMMENT_START + Comment
                Store_ValuesTxt = Store_ValuesTxt + TextLine + vbCr
                Store_Val_Written = Store_Val_Written + ' ' + Channel_or_define + ' '
    if storeStatusType == M02.SST_COUNTER_ON:
        # diese Variante würde nur ein Byte pro Counter verwenden,
        # allerdings is der zusätzliche code zum Behandeln der zusätlzichen Liste
        # in den häufigsten Fällen größer als jene Bytes, die man mit dieser Variante einsparen könnte
        #TextLine = TextLine & AddSpaceToLen(CurrentCounterId, 4) & "},"
        #TextLine = TextLine & COMMENT_START & Comment
        #Store_CountersTxt = Store_CountersTxt & TextLine & vbCr
        TextLine = STORE_BORDER + 'IS_COUNTER    , '
        TextLine = TextLine + M30.AddSpaceToLen('COUNTER_ID ' + CurrentCounterId, 20) + '},'
        TextLine = TextLine + COMMENT_START + Comment
        Store_ValuesTxt = Store_ValuesTxt + TextLine + vbCr
    #end change 01.05.20: Jürgen
    if Addr >= 0:
        # Defines for expert users and duplicate adresses
        InChTxt = InChTxt + Generate_Define_Line(Addr, r, Channel, Comment)
        # Definition of the array with the external adresses for DCC, Selecrix and CAN
        AddrTxt_Line = ADDR_BORDER + M30.AddSpaceToLen(Addr, 5)
        AddrTxt_Line = AddrTxt_Line + '+ ' + Get_Typ_Const(Inp_TypR) + ' ' + M30.AddSpaceToLen(InCnt, 2) + '},'
        Ext_AddrTxt = Ext_AddrTxt + AddrTxt_Line + COMMENT_START
        if AddrComment != '':
            Ext_AddrTxt = Ext_AddrTxt + M30.AddSpaceToLen(AddrComment, 10)
        Ext_AddrTxt = Ext_AddrTxt + Comment + vbCr
        Create_Start_Value_Entry(r)
        # Calculate the next input channel number
        if P01.Cells(r, M25.InCnt___Col).Value != '':
            if not IsNumeric(P01.Cells(r, M25.InCnt___Col).Value) or P01.val(P01.Cells(r, M25.InCnt___Col).Value) < 0 or P01.val(P01.Cells(r, M25.InCnt___Col).Value) > 100:
                P01.Cells(r, M25.InCnt___Col).Select()
                P01.MsgBox(M09.Get_Language_Str('Fehler: Eintrag \'') + P01.Cells(r, M25.InCnt___Col).Value + M09.Get_Language_Str('\' in InCnt Spalte ist ungültig'), vbCritical, M09.Get_Language_Str('Falscher InCnt Eintrag'))
                M30.EndProg()
            else:
                Channel = Channel + P01.val(P01.Cells(r, M25.InCnt___Col).Value)
    fn_return_value = True
    return fn_return_value

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
    fn_return_value = M02.SST_NONE
    fn_return_value = Get_Store_Status(r, Addr, Inp_TypR, Channel_or_define)
    if (fn_return_value == M02.SST_COUNTER_OFF):
        # user forces status store to on
        if P01.Cells(r, M25.Start_V_Col).Value == M02.AUTOSTORE_ON:
            fn_return_value = M02.SST_COUNTER_ON
        return fn_return_value
    elif (fn_return_value == M02.SST_COUNTER_ON):
        if P01.Cells(r, M25.Start_V_Col).Value == M02.AUTOSTORE_OFF or  ( P01.Cells(r, M25.Start_V_Col).Value != '' and IsNumeric(P01.Cells(r, M25.Start_V_Col).Value) ) :
            fn_return_value = M02.SST_COUNTER_OFF
            # 01.05.20: Added from Mail: or IsNumeric(.value)
        return fn_return_value
    elif (fn_return_value == M02.SST_S_ONOFF) or (fn_return_value == M02.SST_TRIGGER):
        if P01.Cells(r, M25.Start_V_Col).Value == M02.AUTOSTORE_OFF or  ( P01.Cells(r, M25.Start_V_Col).Value != '' and IsNumeric(P01.Cells(r, M25.Start_V_Col).Value) ) :
            fn_return_value = M02.SST_NONE
            # 01.05.20: Added from Mail: or IsNumeric(.value)
        return fn_return_value
    # user is not allow to force status store for functions that don't support this
    if P01.Cells(r, M25.Start_V_Col).Value == M02.AUTOSTORE_ON:
        P01.Cells(r, M25.Start_V_Col).Select()
        P01.MsgBox(M09.Get_Language_Str('Fehler: Eintrag \'') + P01.Cells(r, M25.Start_V_Col).Value + M09.Get_Language_Str('\' in Startwert Spalte ist ungültig'), vbCritical, 'Statusspeicherung für diese Funktion nicht möglich')
        fn_return_value = - 1
    return fn_return_value
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
        fn_return_value = M02.SST_NONE
        return fn_return_value
    fn_return_value = GetOnOffStoreType(r, Addr, Inp_TypR, Channel_or_define)
    return fn_return_value

#--------------------------------------------------------------------------------------------
def GetMacroStoreType(r):
#--------------------------------------------------------------------------------------------
    return GetMacroStoreTypeLine(P01.Cells(r, M25.Config__Col))

#--------------------------------------------------------------------------------------------
def GetMacroStoreTypeLine(Config_Entry):
#--------------------------------------------------------------------------------------------
    Org_Macro_Row = int()

    Parts = vbObjectInitialize(objtype=String)

    p = int()

    OutCntStr = String()

    Org_Macro = String()

    Org_Arguments = String()
    #---------------------------------------------------
    fn_return_value = M02.MST_None
    #Config_Entry = P01.Cells(r, M25.Config__Col)
    if Trim(Config_Entry) == '':
        return fn_return_value
        # no macro assigned
    Parts = Split(Config_Entry, vbLf)
    if ( LBound(Parts) != UBound(Parts) ) :
        fn_return_value = GetMultilineMacroStoreType(Parts)
        return fn_return_value
        # multi line macros don't allow store    
    Parts = Split(Config_Entry, vbCr)
    if ( LBound(Parts) != UBound(Parts) ) :
        fn_return_value = GetMultilineMacroStoreType(Parts)
        return fn_return_value
        # multi line macros don't allow store
    Parts = Split(Config_Entry, '(')
    if Trim(Parts(0)) == '':
        return fn_return_value
        # no macro assigned
    Org_Macro_Row = M09SM.Find_Macro_in_Lib_Macros_Sheet(Parts(0) + '(')
    if Org_Macro_Row == 0:
        return fn_return_value
        # macro not found
    fn_return_value = P01.val(P01.Sheets(M02.LIBMACROS_SH).Cells(Org_Macro_Row, M02.SM_Type__COL))
    return fn_return_value

#--------------------------------------------------------------------------------------------
def GetMultilineMacroStoreType(lines):
#--------------------------------------------------------------------------------------------
    fn_return_value = None
    line = Variant()
    #---------------------------------------------------
    # find the first macro have a defined store type
    # otherwise 0 = undefined
    fn_return_value = M02.MST_None
    for line in lines:
        s = line
        fn_return_value = GetMacroStoreTypeLine(s)
        if fn_return_value != M02.MST_None:
            return fn_return_value
    return fn_return_value


#--------------------------------------------------------------------------------------------
def GetOnOffStoreType(r, Addr, Inp_TypR, Channel_or_define):
#--------------------------------------------------------------------------------------------
    TypConst = String()
    fn_return_value = M02.SST_NONE
    if not Inp_TypR is None:
        if Inp_TypR != '':
            TypConst = Get_Typ_Const(Inp_TypR)
            if Addr >= 0:
                Channel_or_define = Gen_Address_Define_Name(Addr, Inp_TypR)
    else:
        TypConst = ''
    if Channel_or_define == '':
        return fn_return_value
    # or all functions having Adress
    if Addr >= 0 and TypConst == 'S_ONOFF,':
        fn_return_value = M02.SST_S_ONOFF
        return fn_return_value
    value = str(P01.Cells(r, M25.InCnt___Col))
    if  P01.Cells(r, M25.LED_Nr__Col) != '' and  value !='':
        if int(value) > 1:
            fn_return_value = M02.SST_TRIGGER
            return fn_return_value
    return fn_return_value

#--------------------------------------------------------------------------------------------
def Create_HeaderFile(CreateFilesOnly = False): #20.12.21: Jürgen add CreateFilesOnly for programatically generation of header files
#--------------------------------------------------------------------------------------------
    global AddrComment
    
    Ctrl_Pressed = Boolean()

    r = int()

    sx = Boolean()

    SX_Ch = int()
    #-----------------------------
    # Is called if the "Z. Arduino schicken" button is pressed
    P01.set_statusmessage(M09.Get_Language_Str("Headerfile wird erstellt"))
    fn_return_value=False
    
    M30.Check_Version()
    M20.Update_Start_LedNr()
    M30.Clear_Platform_Parameter_Cache()
    #removed by HaLi 9.12.2021
    #Ctrl_Pressed = GetAsyncKeyState(VK_CONTROL) != 0
    #if Ctrl_Pressed:
    #    UserForm_Header_Created.DontShowAgain = False
    
    M25.Make_sure_that_Col_Variables_match()
    P01.set_statusmessage(M09.Get_Language_Str("Headerfile wird erstellt. Init Headerfile Generation"))
    
    if not Init_HeaderFile_Generation():
        return fn_return_value
    
    # 04.03.22 Juergen: If shift key is pressed to configuration is sent to the simulator only, also if Autostart Option 3  = simulatorOnly
    shift_pressed = P01.GetAsyncKeyState(P01.__VK_SHIFT)
    print("Shift_pressed:",shift_pressed)
    
    # 17.03.22 Juergen: shift key is reverses simualtor option
    #SimulatorOnly = Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0) = 3 and GetAsyncKeyState(VK_SHIFT) = 0
    SimulatorOnly = M28.Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0) == 3 and shift_pressed
        
    if not SimulatorOnly:
        SimulatorOnly = M28.Get_Num_Config_Var_Range("SimAutostart", 0, 3, 0) != 3 and shift_pressed
      
    #If SimulatorOnly And CreateFilesOnly = False And Get_BoardTyp() = "AM328" Then    
    
    if SimulatorOnly and CreateFilesOnly == False and M02.Get_BoardTyp() == 'AM328':
        Debug.Print(" go to UploadToSimulator")
        fn_return_value = M39.UploadToSimulator(True)
        return fn_return_value

    sx = M25.Page_ID == 'Selectrix'
    for r in vbForRange(M02.FirstDat_Row, M30.LastUsedRow()): #*HL
        if not P01.Rows(r).EntireRow.Hidden and P01.Cells(r, M02.Enable_Col) != '':
            P01.set_statusmessage(M09.Get_Language_Str("Headerfile wird erstellt. 2nd round - Macrozeile: "+str(r)))
            Addr = - 1
            if M25.Address_starts_with_a_Number(r):
                if sx:
                    Bit_P = P01.Cells(r, M25.SX_Bitposi_Col)
                    if Bit_P != '' and P01.val(P01.Cells(r, M25.InCnt___Col)) > 0:
                        if P01.Cells(r, M25.SX_Channel_Col) != '':
                            SX_Ch = M25.Get_First_Number_of_Range(r, M25.SX_Channel_Col)
                            # ToDo: SX_Ch wird nur dann aktualisiert wenn Bit pos vorhanden ist und InCnt > 0. Ist das gut ?
                        if SX_Ch >= 0 and SX_Ch <= 99:
                            if Bit_P >= 1 and Bit_P <= 8:
                                Addr = SX_Ch * 8 + Bit_P - 1
                                AddrComment = 'SX ' + M30.AddSpaceToLenLeft(SX_Ch, 2) + ',' + Bit_P + ': '
                            else:
                                Add_to_Err(P01.Cells(r, M25.SX_Bitposi_Col), 'Wrong bitpos " & bp & " in row ' + r)
                        else:
                            Add_to_Err(P01.Cells(r, M25.SX_Channel_Col), 'Wrong SX channel in row ' + r)
                else:
                    if M25.Page_ID == 'DCC':
                        MaxAddr = 10240
                    else:
                        MaxAddr = 65535
                    Addr = M25.Get_First_Number_of_Range(r, M25.DCC_or_CAN_Add_Col)
                    if Addr == '' or P01.val(P01.Cells(r, M25.InCnt___Col)) <= 0:
                        if Addr != '':
                            Add_to_Err(P01.Cells(r, M25.DCC_or_CAN_Add_Col), M09.Get_Language_Str('Die Ausgewählte Funktion in Zeile ') + str(r) + M09.Get_Language_Str(' ist immer aktiv und kann nicht über DCC oder CAN geschaltet werden.'))
                        Addr = - 1
                    elif Addr >= 1 and Addr <= MaxAddr:
                        # Valid adress range
                        pass
                    else:
                        Add_to_Err(P01.Cells(r, M25.DCC_or_CAN_Add_Col), M09.Get_Language_Str('Die Adresse \'') + Replace(P01.Cells(r, M25.DCC_or_CAN_Add_Col), vbLf, ' ') + M09.Get_Language_Str('\' in Zeile ') + str(r) + M09.Get_Language_Str(' ist ungültig.'))
            else:
                VarName = M25.Get_Address_String(r)
                if VarName != '':
                    if not M06SW.Valid_Var_Name(VarName, r):
                        return fn_return_value
                    Addr = VarName
            if not Create_Header_Entry(r, Addr):
                return fn_return_value
    if M06SW.Check_Detected_Variables() == False:
        return fn_return_value
    if M37.CheckArduinoHomeDir()==False: # 02.12.21: Juergen see forum post #7085
        return fn_return_value
    fn_return_value = Write_Header_File_and_Upload_to_Arduino(CreateFilesOnly) # 20.12.21: Jürgen return result of called function
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Txt - ByRef 
def DelTailingEmptyLines(Txt):
    #----------------------------------------------------
    while Right(Txt, 2) == vbCr + vbCr:
        Txt = Left(Txt, Len(Txt) - 1)
    return Txt

def Ext_AddrTxt_Used():
    global Ext_AddrTxt
    
    #--------------------------------------------
    # Check if DCC, SX or CAN is used
    fn_return_value = ( Ext_AddrTxt != '' )
    return fn_return_value

def Store_ValuesTxt_Used():
    global Store_ValuesTxt
    
    #--------------------------------------------
    fn_return_value = ( Store_ValuesTxt != '' )
    return fn_return_value

def Write_Header_File_and_Upload_to_Arduino(CreateFilesOnly=False): #20.12.21: Jürgen add CreateFilesOnly for programatically generation of header files
    global Err, Ext_AddrTxt, Store_ValuesTxt, InChTxt, LocInChNr, Channel, ConfigTxt, LEDs_per_ChannelList, Start_Values
    
    NumLeds = int()

    Nr = int()

    MaxLed = int()

    Name = String()

    ShortPath = String()

    p = int()

    fp = Integer()

    House_Min_T = String()

    House_Max_T = String()

    Color_Test_Mode = String()
    #----------------------------------------------------
    fn_return_value = False
    Err=""
    MaxLed = M30.Get_Current_Platform_Int('MaxLed')
    for Nr in vbForRange(0, M02.LED_CHANNELS - 1):
        NumLeds = NumLeds + P01.val(P01.Cells(M02.SH_VARS_ROW, M20.Get_LED_Nr_Column(Nr))) #*HL
    if NumLeds < MINLEDs:
        NumLeds = MINLEDs
    if NumLeds > MaxLed:
        Err = Err + M09.Get_Language_Str('Maximale LED Anzahl überschritten: ') + str(NumLeds) + vbCr + M09.Get_Language_Str('Es sind maximal #1# RGB LEDs möglich') + vbCr
    else:
        Err = Replace(Err, "#1#", str(MaxLed))
    if Err != '':
        P01.MsgBox(Err + vbCr + vbCr + M09.Get_Language_Str('Ein neues Header file wurde nicht generiert!'), vbCritical, M09.Get_Language_Str('Es sind Fehler aufgetreten'))
        return fn_return_value
    Name = P01.ThisWorkbook.Path + '/' + M02.Ino_Dir_LED + M02.Include_FileName
    Debug.Print("Write_Header - Filename:"+Name)
    Ext_AddrTxt=DelTailingEmptyLines(Ext_AddrTxt)
    Store_ValuesTxt=DelTailingEmptyLines(Store_ValuesTxt)
    InChTxt=DelTailingEmptyLines(InChTxt)
    InChTxt, Channel = M06SW.Create_Loc_InCh_Defines(InChTxt, Channel, LocInChNr)
    p = InStrRev(P01.ThisWorkbook.Path, '/')
    if p == 0:
        p = InStrRev(P01.ThisWorkbook.Path, '/')
    if p > 0:
        pass #ShortPath = Mid(P01.ThisWorkbook.Path, p + 1, 255) + ' '
    ShortPath = "Ver_"+ M02.Lib_Version_Nr+" "
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    #try:
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '// This file contains the ' + M25.Page_ID + ' and LED definitions.', '\n')
    VBFiles.writeText(fp, '//', '\n')
    VBFiles.writeText(fp, '// It was automatically generated by the program ' + P01.ThisWorkbook.Name + ' ' + M02.Prog_Version + '      by Hardi', '\n')
    VBFiles.writeText(fp, '// File creation: ' + P01.Date_str() + ' ' + P01.Time_str(), '\n')
    VBFiles.writeText(fp, '// (Attention: The display in the Arduino IDE is not updated if Options/External Editor is disabled)', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#ifndef __LEDS_AUTOPROG_H__', '\n')
    VBFiles.writeText(fp, '#define __LEDS_AUTOPROG_H__', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#ifndef CONFIG_ONLY', '\n')                            # 04.03.22 Juergen: add Simulator feature
    VBFiles.writeText(fp, '#ifndef ARDUINO_RASPBERRY_PI_PICO', '\n')
    VBFiles.writeText(fp, '#define FASTLED_INTERNAL       // Disable version number message in FastLED library (looks like an error)', '\n')
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
    #VBFiles.writeText(fp, '#define START_MSG "LEDs_AutoProg Ver 1: ' + '"', '\n')
    VBFiles.writeText(fp, '', '\n')
    if M25.Page_ID == 'Selectrix':
        VBFiles.writeText(fp, '#define USE_SX_INTERFACE               // enable Selectrix protocol on single CPU mainboards', '\n') # 06.12.2021 Juergen add SX for ESP
    else:
        VBFiles.writeText(fp, '#define TWO_BUTTONS_PER_ADDRESS 1      // Two buttons (Red/Green) are used (DCC/CAN)', '\n')
    VBFiles.writeText(fp, '#ifdef NUM_LEDS', '\n')
    VBFiles.writeText(fp, '  #warning "\'NUM_LEDS\' definition in the main program is replaced by the included \'' + M30.FileNameExt(Name) + '\' with ' + str(NumLeds) + '"', '\n')
    VBFiles.writeText(fp, '  #undef NUM_LEDS', '\n')
    VBFiles.writeText(fp, '#endif', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#define NUM_LEDS ' + M30.AddSpaceToLen(str(NumLeds), 22) + '// Number of LEDs (Maximal 256 RGB LEDs could be used)', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#define LEDS_PER_CHANNEL ",' + str(LEDs_per_ChannelList) + '"', '\n')
    # Set HOUSE_MIN_T and HOUSE_MAX_T
    House_Min_T = M28.Get_String_Config_Var('MinTime_House')
    if House_Min_T != '':
        VBFiles.writeText(fp, '#undef  HOUSE_MIN_T', '\n')
        VBFiles.writeText(fp, '#define HOUSE_MIN_T  ' + str(P01.val(House_Min_T)), '\n')
    else:
        House_Min_T = 50
    House_Max_T = M28.Get_String_Config_Var('MaxTime_House')
    if House_Max_T != '':
        VBFiles.writeText(fp, '#undef  HOUSE_MAX_T', '\n')
        VBFiles.writeText(fp, '#define HOUSE_MAX_T ' + str(P01.val(House_Max_T)), '\n')
    else:
        House_Max_T = 150
    if P01.val(House_Min_T) > P01.val(House_Max_T) or P01.val(House_Max_T) == 0:
        P01.Sheets(M02.ConfigSheet).Select()
        #P01.Range('MinTime_House').Select()
        #Sleep(100)
        P01.MsgBox(M09.Get_Language_Str('Fehler auf der \'Config\' Seite:' + vbCr + 'Die \'Minimale Zeit bis zur nächsten Änderung\' muss kleiner ' + 'oder gleich groß wie die Maximale Zeit sein.' + vbCr + 'Achtung: Wenn nichts eingegeben ist werden die Standard Werte vom 50/150 verwendet. ' + 'Dadurch kann es ebenfalls zu einem Konflikt kommen.'), vbCritical, M09.Get_Language_Str('Falsche Zeiten für die House() Funktion'))
        M30.EndProg()
    VBFiles.writeText(fp, '', '\n')
    Color_Test_Mode = M28.Get_String_Config_Var('Color_Test_Mode')
    select_variable_ = Left(UCase(Color_Test_Mode), 1)
    if True: #*HL (select_variable_ == 'J') or (select_variable_ == 'Y') or (select_variable_ == '1'):
        VBFiles.writeText(fp, '#define RECEIVE_LED_COLOR_PER_RS232' + vbCr, '\n')
    if M28.Get_Bool_Config_Var('USE_SPI_Communication') or M25.Page_ID == 'CAN':
        if M28.Get_Bool_Config_Var('USE_SPI_Communication'):
            VBFiles.writeText(fp, '#define USE_SPI_COM                    // Use the SPI bus for the communication in addition to the RS232 if J13 is closed. If no DCC commands are configured the A1 pin of the DCC Arduino is disabled', '\n')
        if M06SW.PIN_A3_Is_Used():
            VBFiles.writeText(fp, '#define LED_HEARTBEAT_PIN -1           // Disable the heartbeat pin because it\'s used for the SwitchB or SwitchC', '\n')
        else:
            VBFiles.writeText(fp, '#define LED_HEARTBEAT_PIN A3           // Don\'t use the internal heartbeat LED because the D13 pins between LED and DCC arduin are connected together', '\n')
    if Ext_AddrTxt_Used():
        if M28.Get_Bool_Config_Var('USE_SPI_Communication'):
            if M06SW.Check_Switch_Lists_for_SPI_Pins() == False:
                VBFiles.closeFile(fp)
                return fn_return_value
        VBFiles.writeText(fp, '#define USE_EXT_ADDR', '\n')
        if InStr(M02.Prog_for_Right_Ardu, ' ' + M25.Page_ID + ' ') > 0:
            VBFiles.writeText(fp, '#define USE_RS232_OR_SPI_AS_INPUT      // Use the RS232 or SPI Input to read DCC/SX commands from the second Arduino and from the PC (The SPI is only used if enabled with USE_SPI_COM)', '\n')
        #    If Get_Bool_Config_Var("USE_SPI_Communication") Then                    ' 14.05.20:
        #       Print #fp, "#define USE_SPI_COM                    // Use the SPI bus for the communication in addition to the RS232 if J13 is closed"
        #    End If
        # Set DCC Offset                                                        ' 26.09.19:
        
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
        VBFiles.writeText(fp, '#define B_RESERVE (uint16_t)(3<<14)    // Not used at the moment', '\n')
        VBFiles.writeText(fp, '#define B_TAST    B_RED', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'typedef struct', '\n')
        VBFiles.writeText(fp, '    {', '\n')
        VBFiles.writeText(fp, '    uint16_t AddrAndTyp; // Addr range: 0..16383. The upper two bytes are used for the type', '\n')
        VBFiles.writeText(fp, '    uint8_t  InCnt;', '\n')
        VBFiles.writeText(fp, '    } __attribute__ ((packed)) Ext_Addr_T;', '\n')
        VBFiles.writeText(fp, '', '\n')
        
        VBFiles.writeText(fp, '// Definition of external adresses', '\n')
        VBFiles.writeText(fp, '#ifdef CONFIG_ONLY', '\n')
        VBFiles.writeText(fp, 'const Ext_Addr_T Ext_Addr[] __attribute__ ((section (".MLLAddressConfig"))) =', '\n')
        VBFiles.writeText(fp, '#else', '\n')
        VBFiles.writeText(fp, 'const PROGMEM Ext_Addr_T Ext_Addr[] =', '\n')
        VBFiles.writeText(fp, '#endif', '\n')
        VBFiles.writeText(fp, '         { // Addr & Typ    InCnt', '\n')
        
        #VBFiles.writeText(fp, '// Definition of external adresses' + vbCr + 'const PROGMEM Ext_Addr_T Ext_Addr[] =' + vbCr + '         { // Addr & Typ    InCnt', '\n')
        VBFiles.writeText(fp, Ext_AddrTxt)
        VBFiles.writeText(fp, '         };', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '// Input channel defines for local inputs and expert users', '\n')
    VBFiles.writeText(fp, InChTxt, '\n')
    VBFiles.writeText(fp, '', '\n')
    
    fret, Channel = M06SW.Write_Switches_Header_File_Part_A(fp, Channel)
    if fret == False:
        VBFiles.closeFile(fp)
        return fn_return_value
    
    if M06SW.Write_LowProrityLoop_Header_File(fp) == False:
        VBFiles.closeFile(fp)
        return fn_return_value
    
    if M06LED.Write_Header_File_LED2Var(fp) == False:
        VBFiles.closeFile(fp)
        return fn_return_value
    # 15.10.21: Juergen split creation of sound extensions to ensure that preprocessor defines are corretly compiled
    if M06Sound.Write_Header_File_Sound_Before_Config(fp) == False:
        VBFiles.closeFile(fp)
        return fn_return_value
    
    if M38.Write_Header_File_Extension_Before_Config(fp) == False:
        VBFiles.closeFile(fp)
        return fn_return_value    
    
    VBFiles.writeText(fp, DayAndNightTimer, '\n')
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
    VBFiles.writeText(fp, '//---------------------------------------------', '\n')
    VBFiles.writeText(fp, 'void Set_Start_Values(MobaLedLib_C &MobaLedLib)', '\n')
    VBFiles.writeText(fp, '//---------------------------------------------', '\n')
    VBFiles.writeText(fp, '{', '\n')
    VBFiles.writeText(fp, Start_Values)
    VBFiles.writeText(fp, '}', '\n')
    VBFiles.writeText(fp, '', '\n')
    #begin change 01.05.20: Jürgen
    if Store_ValuesTxt_Used():
        #Print #fp, "#define ENABLE_STORE_STATUS"                               ' 01.05.20: disabled in Mail from Juergen
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '// if function returns TRUE the calling loop stops', '\n')
        VBFiles.writeText(fp, 'typedef bool(*HandleValue_t) (uint8_t CallbackType, uint8_t ValueId, uint8_t* Value, uint16_t EEPromAddr, uint8_t TargetValueId, uint8_t Options);', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '#define InCnt_MSK  0x0007  // 3 Bits are used for the InCnt', '\n')
        VBFiles.writeText(fp, '#define IS_COUNTER (uint8_t)0x80', '\n')
        VBFiles.writeText(fp, '#define IS_PULSE   (uint8_t)0x40', '\n')
        VBFiles.writeText(fp, '#define IS_TOGGLE  (uint8_t)0x00', '\n')
        VBFiles.writeText(fp, '#define COUNTER_ID', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, 'typedef struct', '\n')
        VBFiles.writeText(fp, '    {', '\n')
        VBFiles.writeText(fp, '    uint8_t TypAndInCnt; // Type bit 7, InCnt bits 0..3, reserved 0 bits 4..6', '\n')
        VBFiles.writeText(fp, '    uint8_t Channel;', '\n')
        VBFiles.writeText(fp, '    } __attribute__ ((packed)) Store_Channel_T;', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '// Definition of channels and counters that need to store state in EEProm' + vbCr + 'const PROGMEM Store_Channel_T Store_Values[] =' + vbCr + '         { // Mode + InCnt , Channel', '\n')
        VBFiles.writeText(fp, Store_ValuesTxt)
        VBFiles.writeText(fp, '         };', '\n')
        VBFiles.writeText(fp, '', '\n')
    else:
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '// No macros used which are stored to the EEPROM => Disable the ENABLE_STORE_STATUS flag in case it was set in the excel sheet', '\n')
        VBFiles.writeText(fp, '#ifdef ENABLE_STORE_STATUS', '\n')
        VBFiles.writeText(fp, '  #undef ENABLE_STORE_STATUS', '\n')
        VBFiles.writeText(fp, '#endif', '\n')
        VBFiles.writeText(fp, '', '\n')
    #end change 19.04.20 Jürgen
    
    VBFiles.writeText(fp, '#ifndef CONFIG_ONLY', '\n') # 04.03.22 Juergen: add Simulator feature
  
    # 15.10.21: Juergen move creation of onboard sound code after the configuration struture to ensue that #defines from ProgGenerator are effective
    if M06Sound.Write_Header_File_Sound_After_Config(fp) == False:
        VBFiles.closeFile(fp)
        return fn_return_value
    
    """ 31.01.22: Juergen add extension support"""
    
    
    if M38.Write_Header_File_Extension_After_Config(fp) == False:
        VBFiles.closeFile(fp)
        return fn_return_value
    
    VBFiles.writeText(fp, '#endif // CONFIG_ONLY', '\n')    
    
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '#endif // __LEDS_AUTOPROG_H__', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if Channel - 1 > 250:
        P01.MsgBox(M09.Get_Language_Str('Fehler: Die Anzahl der verwendeten Eingangskanäle ist zu groß!' + vbCr + 'Es sind maximal 250 verfügbar. Die Konfiguration enthält aber ') + str(Channel - 1) + '.' + vbCr + vbCr + M09.Get_Language_Str('Die Eingangskanäle werden zum einlesen von DCC, Selectrix und CAN Daten benutzt. ' + vbCr + 'Außerdem werden sie als interne Zwischenspeicher benötigt.'), vbCritical, M09.Get_Language_Str('Anzahl der InCh Variablen überschritten'))
        M30.EndProg()
    if ConfigTxt == '':
        P01.MsgBox(M09.Get_Language_Str('Achtung: Es ist keine einzige Zeile in der Spalte "Beleuchtung, Sound, oder andere Effekte" aktiv!' + vbCr + '=> Das Programm wird keine LEDs ansteuern'), vbCritical, M09.Get_Language_Str('Achtung: Die Konfiguration ist leer'))
        #*HLUserForm_Header_Created.DontShowAgain = False
    P01.Application.StatusBar = Time + M09.Get_Language_Str(': Header Datei \'') + Name + M09.Get_Language_Str('\' wurde erzeugt')
    #Show_Status_for_a_while Time & Get_Language_Str(": Header Datei '") & Name & Get_Language_Str("' wurde erzeugt")
    #*HL if CreateFilesOnly == False and UserForm_Header_Created.DontShowAgain == False:
    #*HL    UserForm_Header_Created.FileName = Name
    #*HL    UserForm_Header_Created.Show()
    M08.Compile_and_Upload_LED_Prog_to_Arduino(CreateFilesOnly)
    M20.ResetTestButtons(M06SW.Store_Status_Enabled)
    fn_return_value = True
    return fn_return_value
    #except:
    #    # Attention: This could also be an error some where else in the code
    P01.MsgBox(M09.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Header Datei'))
    VBFiles.closeFile(fp)

# VB2PY (UntranslatedCode) Option Explicit
