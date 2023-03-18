# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 4.02
# * Author: Harold Linke
# * Date: January 7, 2022
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
# 2022-01-07 v4.02 HL: - Else:,ByRef check done - first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

from ExcelAPI.XLC_Excel_Consts import *

import proggen.M02_Public as M02
import proggen.M02a_Public as M02a
import proggen.M06_Write_Header as M06
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
import proggen.M25_Columns as M25
import proggen.M30_Tools as M30
import proggen.M70_Exp_Libraries as M70
import proggen.Prog_Generator as PG
import ExcelAPI.XLWF_Worksheetfunction as WorksheetFunction

import ExcelAPI.XLW_Workbook as P01

__DstVar_List = String()
__MultiSet_DstVar_List = String()
__StoreVar_List = String()
__MaxUsed_Loc_InCh = int()
__MaxUsed_Loc_InCh_Row = int()
SwitchA_InpCnt = int()
SwitchB_InpCnt = int()
SwitchC_InpCnt = int()
SwitchD_InpCnt = int()
SwitchA_InpLst = String()
SwitchB_InpLst = String()
SwitchC_InpLst = String()
SwitchD_InpLst = String()
CLK_Pin_Number = String()
RST_Pin_Number = String()
LDR_Pin_Number = String()
Serial_PinLst = String()
DMX_LedChan = int()
__CTR_Channels_1 = int()
__CTR_Channels_2 = int()
__Channel1InpCnt = int()
__Channel2InpCnt = int()
__CTR_Cha_Name_1 = String()
__CTR_Cha_Name_2 = String()
__But_Inp_List_1 = String()
__But_Inp_List_2 = String()
LED_PINNr_List = String()
Read_LDR = Boolean()
__Use_WS2811 = Boolean()
Store_Status_Enabled = Boolean()
Switch_Damping_Fact = String()

def PIN_A3_Is_Used():
    global RST_Pin_Number
    _ret = False
    #------------------------------------------
    if __Channel1InpCnt > 0 and RST_Pin_Number == 'A3':
        _ret = True
    return _ret

def __Add_Logic_InpVars(LogicExp, r):
    _ret = False
    Arglist = vbObjectInitialize(objtype=String)

    Arg = Variant()
    #---------------------------------------------------------------------------
    Arglist = M30.SplitEx(LogicExp, True, 'OR', 'AND', 'NOT')
    for Arg in Arglist:
        Arg = Trim(Arg)
        if Arg != '':
            if __Valid_Var_Name_and_Skip_InCh_and_Numbers(Arg, r) == False:
                return _ret
                # Skip special names like '#InCh' and Numbers
    _ret = True
    return _ret

def __Check_if_all_Variables_in_sequece_of_N_exists(r, N):
    _ret = False
    TxtLen = 0
    Adr_or_Name = String()
    #----------------------------------------------------------------------------------------------
    Adr_or_Name = Trim(P01.Cells(r, M25.Get_Address_Col()))
    if Adr_or_Name == '':
        P01.Cells(r, M25.Get_Address_Col()).Select()
        P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: In Zeile #1# ist keine Adresse, kein Schalter oder keine Variable eingetragen'), "#1#", str(r)), vbCritical, Replace(M09.Get_Language_Str('Kein Eintrag in \'#1#\' Spalte'), "#1#", M25.Get_Address_String(M02.Header_Row)))
        return _ret
    if not IsNumeric(Split(Adr_or_Name, ' ')(0)):
        Nr,TxtLen = __Get_Nr_From_Var(Adr_or_Name, TxtLen)
        if Nr >= 0:
            Name = Left(Adr_or_Name, TxtLen)
            for i in vbForRange(Nr, Nr + N - 1):
                if Valid_Var_Name(Name + i, r) == False:
                    return _ret
                    # At the moment Valid_Var_Name always returns true
    _ret = True
    return _ret

def __Get_Bin_Inputs(Dec_Cnt):
    _ret = ""
    #-----------------------------------------------
    if Dec_Cnt <= 0:
        _ret = - 1
    elif Dec_Cnt <= 1:
        _ret = 1
    elif Dec_Cnt <= 3:
        _ret = 2
    elif Dec_Cnt <= 7:
        _ret = 3
    elif Dec_Cnt <= 15:
        _ret = 4
    elif Dec_Cnt <= 31:
        _ret = 5
    elif Dec_Cnt <= 63:
        _ret = 6
    else:
        _ret = - 1
    return _ret

def __Check_if_all_Variables_in_sequece_exist(r, Ctr_Name, N_Str):
    _ret = False
    N = int()
    #------------------------------------------------------------------------------------------------------------------
    # Is called if a macro of those is checked
    # - InCh_to_TmpVar(InCh, InCh_Cnt)
    # - Charlie_Buttons(LED, InCh, States)
    # - Charlie_Binary(LED, InCh, BinStates)
    # InCh could be a DCC Variable, a Switch or an "Array" variable.
    # In the last two cases it has to be checked if all required variables exist.
    # Example: InCh_to_TmpVar(SwitchA3, 3)
    # => SwitchA3, SwitchA4, SwitchA5 must be defined
    if Ctr_Name == 'BinStates':
        N = __Get_Bin_Inputs(P01.val(N_Str))
        if N <= 0:
            P01.MsgBox(M09.Get_Language_Str('Fehler: Anzahl der binären Zustände ungültig. Die Anzahl muss zwischen 1 und 63 liegen'), vbCritical, M09.Get_Language_Str('Anzahl der binären Zustände ungültig'))
            return _ret
    else:
        N = P01.val(N_Str)
    _ret = __Check_if_all_Variables_in_sequece_of_N_exists(r, N)
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: MacroName - ByVal 
def __Add_InpVars(MacroName, Org_Macro, Filled_Macro, r, Org_Macro_Row):
    _ret = False
    Second_Input_Names = 'InCh R_InCh InReset InCh2'

    Arg_List = vbObjectInitialize(objtype=String)

    Fil_List = vbObjectInitialize(objtype=String)

    ArgNr = int()

    Name = Variant()

    Arg = String()
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Die benutzten Schalter Eingänge müssen aus den Parametern der Makros gelesen werden
    # Die Eingänge können an verschiedenen Stellen benutzt werden
    # - Logic:
    # - Zwei Eingänge z.B. "RS_FlipFlop(DstVar, InCh, R_InCh)"
    #   Hier gibt es verschiedene mögliche Kandidaten: "R_InCh InReset"
    # - Es gibt auch "versteckte" Eingänge bei Makros wie "InCh_to_TmpVar(InCh, InCh_Cnt)"
    #   Diese sind in Spalte "InCh" mit "n", "States", "BinStates", "2", "3", "4"
    #
    # Examples:
    # - Logic(TestOr, #InCh OR #InCh+1 OR SwitchA4)              O.K.
    # - RS_FlipFlopTimeout(FlipFlop, #InCh+1, #InCh, 30 Sek)     O.K.    Hier muss man das +1 von Hand vertauschen wenn die "Rot= Reset" sein soll
    # - RS_FlipFlopTimeout(FlipFlop, #InCh, SwitchA5, 30 Sek)    O.K.
    # - RS_FlipFlopTimeout(FlipFlop, #InCh, SI_0, 30 Sek)        O.K.
    # - EntrySignal3_RGB(LED, InCh)                              O.K.
    # - InCh_to_TmpVar(InCh, InCh_Cnt)                           O.K.
    # - Charlie_Buttons(LED, InCh, States)                       O.K.
    # - Charlie_Binary(LED, InCh, BinStates)                     O.K.
    Arg_List = __Get_Arguments(Org_Macro)
    Fil_List = __Get_Arguments(Filled_Macro)
    _select0 = MacroName
    if (_select0 == 'Logic'):
        if UBound(Fil_List) != 1:
            P01.Cells(r, M25.Config__Col).Select()
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Falsche Parameter Anzahl in \'Logic()\' Ausdruck: \'#1#\''), "#1#", Filled_Macro), vbCritical, M09.Get_Language_Str('Fehler: \'Logic()\' Ausdruck ist ungültig'))
            return _ret
        _ret = __Add_Logic_InpVars(Fil_List(1), r)
    else:
        Det_Cnt = 0
        Pos_CounterVar = - 1
        Pos_InCh = - 1
        for ArgNr in vbForRange(0, UBound(Arg_List)):
            Arg = Arg_List(ArgNr)
            if Arg == 'InCh_Cnt' or Arg == 'States' or Arg == 'BinStates':
                Pos_CounterVar = ArgNr
            if Arg == 'InCh':
                Pos_InCh = ArgNr
            for Name in Split(Second_Input_Names, ' '):
                if Arg == Name:
                    Det_Cnt = Det_Cnt + 1
                    if __Valid_Var_Name_and_Skip_InCh_and_Numbers(Fil_List(ArgNr), r) == False:
                        return _ret
        if Pos_CounterVar >= 0:
            if __Check_if_all_Variables_in_sequece_exist(r, Arg_List(Pos_CounterVar), Fil_List(Pos_CounterVar)) == False:
                return _ret
        else:
            # Check if there is a number in column "InCnt" and all arguments have been found
            InCntStr = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH).Cells(Org_Macro_Row, M02.SM_InCnt_COL)
            if InCntStr != '':
                if IsNumeric(InCntStr):
                    if Det_Cnt != P01.val(InCntStr):
                        # It's a function like: "EntrySignal3_RGB(LED, InCh)"
                        # => Check if all Variable in the sequece exist: <Name>1..<Name><InCntStr>
                        if __Check_if_all_Variables_in_sequece_of_N_exists(r, P01.val(InCntStr)) == False:
                            return _ret
                if IsNumeric(Left(InCntStr, Len(InCntStr) - 1)) and Right(InCntStr, 1) == '?':
                    #ToDo Zusätzliche Überprüfung auf "#InCh+2" wenn 3? in Lib_Macros hinzugefügt wird
                    if Fil_List(2) == '#InCh+1':
                        # It's a function which may use two inputs like: "RS_FlipFlop(Test, #InCh, #InCh+1)"
                        # => Check if all Variable in the sequece exist: <Name>1..<Name><InCntStr>
                        if __Check_if_all_Variables_in_sequece_of_N_exists(r, P01.val(InCntStr)) == False:
                            return _ret
    _ret = True
    return _ret

def __Is_Switch_Var_then_Add_to_Ctr(Var_Name):
    _ret = False
    Nr = int()
    #-------------------------------------------------------------------------
    _select1, Nr = Is_in_Nr_String(Var_Name, 'Switch?', 1, 250, Nr)
    if (_select1 == 1):
        _select2 = Left(Var_Name, Len('Switch?'))
        if (_select2 == 'SwitchA'):
            if Nr > SwitchA_InpCnt:
                SwitchA_InpCnt = Nr
        elif (_select2 == 'SwitchB'):
            if Nr > SwitchB_InpCnt:
                SwitchB_InpCnt = Nr
        elif (_select2 == 'SwitchC'):
            if Nr > SwitchC_InpCnt:
                SwitchC_InpCnt = Nr
        elif (_select2 == 'SwitchD'):
            if Nr > SwitchD_InpCnt:
                SwitchD_InpCnt = Nr
        else:
            Debug.Print('Unsupported variable \'' + Var_Name + '\' in \'First_Scan_of_Data_Rows()\'')
        _ret = 1
    elif (_select1 == - 1):
        P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Die Nummer der Variable \'#1#\' ist ungültig!' + vbCr + vbCr + 'Gültiger Bereich: #2#'), "#1#", Var_Name), '#2#', '1..250'), vbCritical, M09.Get_Language_Str('Fehler: Ungültige Variable'))
        _ret = - 1
    return _ret

def __First_Scan_of_Data_Rows():
    
    global Switch_Damping_Fact, DMX_LedChan,Read_LDR,Store_Status_Enabled,__Use_WS2811, SwitchA_InpLst, SwitchB_InpLst, SwitchC_InpLst, SwitchD_InpLst, CLK_Pin_Number, RST_Pin_Number, LDR_Pin_Number, LED_PINNr_List, DMX_LedChan,Read_LDR
    
    _ret = False
    r = int()

    Var_COL = int()
    #----------------------------------------------------
    # Set the global variables if the corrosponding entries are found
    # - in the Var_Col:
    #     "Switch?<Nr>"
    # - in then Config__Col:
    #     "// Set_Switch?_InpLst("
    #     "DstVar*"
    #     "#define READ_LDR"
    #
    Var_COL = M25.Get_Address_Col()
    Switch_Damping_Fact = ''
    for r in vbForRange(M02.FirstDat_Row, M30.LastUsedRow()):
        P01.set_statusmessage(M09.Get_Language_Str("Headerfile wird erstellt. 1st round - Macrozeile: "+str(r)))
        if not P01.Rows(r).EntireRow.Hidden and P01.Cells(r, M02.Enable_Col) != '':
            Var_Name = P01.Cells(r, Var_COL)
            if __Is_Switch_Var_then_Add_to_Ctr(Var_Name) == - 1:
                P01.Cells(r, Var_COL).Select()
                return _ret
            Config_Entry = P01.Cells(r, M25.Config__Col)
            if Trim(Config_Entry) != '':
                for Line in Split(Config_Entry, vbLf):
                    Line = Trim(Line)
                    fret, SwitchA_InpLst = Set_PinNrLst_if_Matching(Line, '// Set_SwitchA_InpLst(', SwitchA_InpLst, 'A', 5)
                    if fret == False:
                        return _ret
                    fret, SwitchB_InpLst = Set_PinNrLst_if_Matching(Line, '// Set_SwitchB_InpLst(', SwitchB_InpLst, 'I', 12) 
                    if fret == False:
                        return _ret
                    fret, SwitchC_InpLst = Set_PinNrLst_if_Matching(Line, '// Set_SwitchC_InpLst(', SwitchC_InpLst, 'I', 12)
                    if fret == False:
                        return _ret
                    fret, SwitchD_InpLst = Set_PinNrLst_if_Matching(Line, '// Set_SwitchD_InpLst(', SwitchD_InpLst, 'Pu', 12)
                    if fret == False:
                        return _ret
                    fret, CLK_Pin_Number = Set_PinNrLst_if_Matching(Line, '// Set_CLK_Pin_Number(', CLK_Pin_Number, 'O', 1)
                    if fret == False:
                        return _ret
                    fret, RST_Pin_Number = Set_PinNrLst_if_Matching(Line, '// Set_RST_Pin_Number(', RST_Pin_Number, 'O', 1)
                    if fret == False:
                        return _ret
                    fret, LDR_Pin_Number = Set_PinNrLst_if_Matching(Line, '// Set_LDR_Pin_Number(', LDR_Pin_Number, 'A', 1)
                    if fret == False:
                        return _ret
                    fret, LED_PINNr_List = Set_PinNrLst_if_Matching(Line, '// Set_LED_OutpPinLst(', LED_PINNr_List, 'OV', M02.LED_CHANNELS)  # 18.02.22 Juergen Virtual Channel
                    if fret == False:
                        return _ret
                    if Line == '// Use_DMX512()':
                        DMX_LedChan = P01.val(P01.Cells(r, M25.LED_Cha_Col))
                    if Line == '#define READ_LDR':
                        Read_LDR = True
                    if Left(Line, Len('#define SWITCH_DAMPING_FACT')) == '#define SWITCH_DAMPING_FACT':
                        Switch_Damping_Fact = Line
                    if Line == '#define USE_WS2811':
                        __Use_WS2811 = True
                        # 19.01.21 Juergen
                    if Line == '#define ENABLE_STORE_STATUS':
                        Store_Status_Enabled = True
                        #    "
                    if Add_Inp_and_DstVars(Line, r) == False:
                        return _ret
                        # Add the destination variable to DstVar_List
    _ret = True
    return _ret

def __Test():
    Debug.Print(Replace('Aber    Hallo', '  ', ' '))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sw_List - ByVal 
def __Check_one_Switch_Lists_for_SPI_Pins(Sw_List):
    _ret = False
    Pin = Variant()
    #---------------------------------------------------------------------------------------
    Sw_List = ' ' + Sw_List + ' '
    for Pin in Split('10 11 12', ' '):
        if InStr(Sw_List, ' ' + Pin + ' ') > 0:
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Der Arduino Pin \'#1#\' kann nicht als Ein- oder Ausgang werden wenn ' + 'DCC oder Selectrix Daten per SPI Bus gelesen werden. Es muss ein anderer Anschluss verwendet ' + 'werden oder die SPI Kommunikation in der \'Config\' Seite deaktiviert werden.' + vbLf + 'Achtung: Die beiden Arduinos müssen dann per RS232 verbunden sein.'), "#1#", Pin), vbCritical, 'Fehler: Ungültiger Arduino Pin erkannt')
            return _ret
    _ret = True
    return _ret

def Check_Switch_Lists_for_SPI_Pins():
    _ret = False
    #-----------------------------------------------------------
    if SwitchA_InpCnt > 0:
        if __Check_one_Switch_Lists_for_SPI_Pins(SwitchA_InpLst) == False:
            return _ret
    if SwitchB_InpCnt > 0:
        if __Check_one_Switch_Lists_for_SPI_Pins(SwitchB_InpLst) == False:
            return _ret
    if SwitchC_InpCnt > 0:
        if __Check_one_Switch_Lists_for_SPI_Pins(SwitchC_InpLst) == False:
            return _ret
    if SwitchD_InpCnt > 0:
        if __Check_one_Switch_Lists_for_SPI_Pins(SwitchD_InpLst) == False:
            return _ret
    _ret = True
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Dest_InpLst - ByRef 
def Set_PinNrLst_if_Matching(Line, Name, Dest_InpLst, PinTyp, MaxCnt):
    _ret = False
    NrStr="" #*HL
    ValidPins = String()

    SPI_Pins = String()

    UseA1 = String()
    #--------------------------------------------------------------------------------------------------------------------------------------------------
    # ToDo:
    # - Noch mal prüfen ob alle Pins möglich sind
    #   Evtl. gibt es auch HW Kombinationen welche verhindern dass bestimmte Pins benutzt werden
    #   - A1 kann z.B. dann benutzt werden wenn CAN Benutzt wird oder wenn Kein DCC und Selectrix benutzt ist
    #     Evtl. eine Meldung ausgeben
    #   - Wenn die SPI Kommunikation zum DCC Arduino verwendet wird, dann können die Pins 10, 11, 12 nicht benutzt werden
    # FIX nach Umstellung auf Platform_Parameters                                ' 17.11.21: Juergen
    # beim AM328 sind die SPI Pins nur frei, wenn kein CAN Modul angeschlossen ist
    SPI_Pins = ''
    if M25.Page_ID != 'CAN':
        if PinTyp == 'I' or PinTyp == 'OV' or PinTyp == 'Pu':           # 18.02.22: Juergen add virtual Channel
            SPI_Pins = M30.Get_Current_Platform_String('SPI_Pins')
    ValidPins = M30.Get_Current_Platform_String(PinTyp + '_Pins', True)
    ValidPins = SPI_Pins + ValidPins
    if Left(Line, Len(Name)) == Name:
        p = InStr(Line, ')')
        if p == 0:
            # VB2PY (UntranslatedCode) GoTo PrintError
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern in Zeile:' + vbCr + '  \'#1#\''), "#1#", Line), vbCritical, M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern'))
            return _ret, Dest_InpLst            
            
        NrStr = Mid(Line, 1 + Len(Name), p - 1 - Len(Name))
        NrStr = Trim(Replace(NrStr, ',', ' '))
        NrStr = Replace(NrStr, '  ', ' ')
        if NrStr == '':
            # VB2PY (UntranslatedCode) GoTo PrintError
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern in Zeile:' + vbCr + '  \'#1#\''), "#1#", Line), vbCritical, M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern'))
            return _ret, Dest_InpLst            
           
        NrArr = Split(NrStr, ' ')
        if UBound(NrArr) + 1 > MaxCnt:
            # VB2PY (UntranslatedCode) GoTo PrintError
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern in Zeile:' + vbCr + '  \'#1#\''), "#1#", Line), vbCritical, M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern'))
            return _ret, Dest_InpLst            
            
        # Check if valid pins names / numbers are used
        NrStr = ''
        for OnePin in NrArr:
            if InStr(ValidPins, ' ' + M30.AliasToPin(OnePin) + ' ') == 0:
                P01.MsgBox(M09.Replace(Replace(M09.Get_Language_Str('Fehler: Der Pin \'#1#\' ist nicht gültig im' + vbCr + '  \'#2#\' Befehl'), "#1#", OnePin), '#2#', Replace(Line, '// ', '')), vbCritical, M09.Get_Language_Str('Ungültige Arduino Pin Nummer'))
                return _ret, Dest_InpLst
            # Check Duplicate Pins , not for virtual PIN 'V' - virtual pin may be used multiple times
            if OnePin != M09.Virtual_Channel_T:
                #p = InStr(" " & line & " ", " " & AliasToPin(OnePin) & " ")                     ' 14.10.21: Juergen, 16.05.20: Added space around OnePin (Problem: 2 ... 12)
                p = InStr(' ' + Replace(Replace(Line, '(', ' '), ')', ' ') + ' ', ' ' + OnePin + ' ')  # 17.02.22: Juergen, fix a bug
                if InStr(p + 1, ' ' + Line + ' ', ' ' + OnePin + ' ') > 0:
                    P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Der Pin \'#1#\' wird mehrfach verwendet im' + vbCr + '  \'#2#\' Befehl'), "#1#", OnePin), '#2#', Replace(Line, '// ', '')), vbCritical, M09.Get_Language_Str('Mehrfach verwendeter Arduino Pin'))
                    return _ret, Dest_InpLst
                if NrStr != '':
                    NrStr = NrStr + ' '
                # 14.10.21: Juergen
            NrStr = NrStr + M30.AliasToPin(OnePin)
        Dest_InpLst = NrStr
    _ret = True
    if NrStr != '':
        Debug.Print('Set_PinNrLst_if_Matching(' + Name + '=' + NrStr + ')')
        # Debug
    return _ret, Dest_InpLst
    

def __Get_Arguments(Line):
    _ret = ""
    Arguments = String()

    Parts = vbObjectInitialize(objtype=String)

    i = int()

    p = int()
    #---------------------------------------------------------
    if InStr(Line, '(') == 0:
        P01.MsgBox('Error: Opening bracket not found in \'' + Line + '\'', vbCritical, 'Internal Error')
        return _ret
    Arguments = Split(Line, '(')(1)
    p = InStrRev(Arguments, ')')
    if p == 0:
        P01.MsgBox('Error: Closing bracket not found in \'' + Line + '\'', vbCritical, 'Internal Error')
        return _ret
    Arguments = Left(Arguments, p - 1)
    Parts = Split(Arguments, ',')
    for i in vbForRange(0, UBound(Parts)):
        Parts[i] = Trim(Parts(i))
    _ret = Parts
    return _ret

def __Test_Get_Arguments():
    Res = vbObjectInitialize(objtype=String)
    #UT-----------------------------
    Res = __Get_Arguments('Test( A, b, c)')

def __Get_Matching_Arg(Org_Macro, Line, DestVarName):
    _ret = ""
    Org_Args = vbObjectInitialize(objtype=String)

    Act_Args = vbObjectInitialize(objtype=String)
    #------------------------------------------------------------------------------------------------------
    # Return the argument in "Line" which matches DestVarName in Org_Macro
    Org_Args = __Get_Arguments(Org_Macro)
    if M30.isInitialised(Org_Args):
        Act_Args = __Get_Arguments(Line)
        if M30.isInitialised(Act_Args):
            if UBound(Act_Args) >= UBound(Org_Args):
                for i in vbForRange(0, UBound(Org_Args)):
                    if Org_Args(i) == DestVarName:
                        _select3 = DestVarName
                        if (_select3 == '...') or (_select3 == 'OutList'):
                            while i <= UBound(Act_Args):
                                _ret = __Get_Matching_Arg() + Act_Args(i) + ','
                                i = i + 1
                            _ret = M30.DelLast(__Get_Matching_Arg())
                        else:
                            _ret = Act_Args(i)
                        return _ret
    P01.MsgBox(Replace(M09.Get_Language_Str('Fehler bei der Erkennung der Zielvariable in Makro \'#1#\''), "#1#", Line), vbCritical, M09.Get_Language_Str('Fehler: Zielvariable wurde nicht gefunden'))
    return _ret

def __Test_Get_Matching_Arg():
    #UT--------------------------------
    Debug.Print(__Get_Matching_Arg('Random(        DstVar, InCh, RandMode, MinTime, MaxTime, MinOn, MaxOn)', 'Random( OutA, 1, 2, 3, 4, 5, 6)', 'DstVar'))
    Debug.Print(__Get_Matching_Arg('Counter(       CtrMode, InCh, Enable, TimeOut, ...)', 'Counter(12, #InCh, Enable, TimeOut, OutA, OutB, OutB)', '...'))
    Debug.Print(__Get_Matching_Arg('RandMux(       DstVar1, DstVarN, InCh, RandMode, MinTime, MaxTime)', 'RandMux( Out1, Out10, InCh, RandMode, MinTime, MaxTime)', 'DstVarN'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: VarName - ByVal 
def Add_Variable_to_DstVar_List(VarName):
    global __DstVar_List
    
    _ret = False
    Check = String()
    #-------------------------------------------------------------------------------
    Check = ' ' + VarName + ' '
    if InStr(__DstVar_List, Check) == 0:
        __DstVar_List = __DstVar_List + VarName + ' '
    else:
        if InStr(__MultiSet_DstVar_List, Check) == 0:
            __MultiSet_DstVar_List = __MultiSet_DstVar_List + VarName + ' '
    _ret = True
    return _ret

def __Add_Matching_Arg_to_DstVars(Org_Macro, Line, DestVarName):
    _ret = False
    Arg = String()
    #------------------------------------------------------------------------------------------------------------------
    # Locate DestVarName in Org_Macro and add the corrosponding
    # argument to the global string DstVar_List
    # Example:
    #   MonoFlop(DstVar, InCh, Duration)
    #   RS_FlipFlop2(DstVar1, DstVar2, InCh, R_InCh)             Called 2 times
    Arg = __Get_Matching_Arg(Org_Macro, Line, DestVarName)
    if Arg != '':
        if Arg == '#LocInCh':
            _ret = True
        else:
            _ret = Add_Variable_to_DstVar_List(Arg)
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: VarName - ByVal 
def Add_Variable_to_StoreVar_List(VarName):
    _ret = False
    Check = String()
    #--------------------------------------------------------------------------------
    Check = ' ' + VarName + ' '
    if InStr(__StoreVar_List, Check) == 0:
        __StoreVar_List = __StoreVar_List + VarName + ' '
    _ret = True
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: VarName - ByVal 
def StoreVar_List_Present(VarName):
    _ret = False
    Check = String()
    #------------------------------------------------------------------------
    Check = ' ' + VarName + ' '
    _ret = InStr(__StoreVar_List, Check) != 0
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: TxtLen - ByRef 
def __Get_Nr_From_Var(Name, TxtLen):
    _ret = 0
    p = int()
    #-----------------------------------------------------------------------------
    _ret = - 1
    p = Len(Name)
    while p > 0 and InStr('0123456789', Mid(Name, p, 1)) > 0:
        p = p - 1
    if p > 0:
        p = p + 1
        TxtLen = p - 1
        if IsNumeric(Mid(Name, p)):
            _ret = P01.val(Mid(Name, p))
        else:
            _ret = - 2
    return _ret,TxtLen

def __Add_N2_Arg_to_DstVars(Org_Macro, Line):
    _ret = False
    Arg1 = String()

    ArgN = String()

    TxtLen1 = int()

    TxtLenN = int()
    #-------------------------------------------------------------------------------------
    # Example: RandMux(DstVar1, DstVarN, InCh, RandMode, MinTime, MaxTime)
    Arg1 = __Get_Matching_Arg(Org_Macro, Line, 'DstVar1')
    if Arg1 != '':
        ArgN = __Get_Matching_Arg(Org_Macro, Line, 'DstVarN')
        if ArgN != '':
            StartNr,TxtLen1 = __Get_Nr_From_Var(Arg1, TxtLen1)
            if StartNr < 0:
                return _ret
            EndNr, TxtLenN = __Get_Nr_From_Var(ArgN, TxtLenN)
            if EndNr < 0:
                return _ret
            if TxtLen1 != TxtLenN or Left(Arg1, TxtLen1) != Left(ArgN, TxtLenN):
                return _ret
            for i in vbForRange(StartNr, EndNr):
                if Add_Variable_to_DstVar_List(Left(Arg1, TxtLen1) + str(i)) == False:
                    return _ret
            _ret = True
    return _ret

def __Add_VarArgCnt_to_DstVars(Org_Macro, Line):
    _ret = False
    Arg = String()
    #----------------------------------------------------------------------------------------
    # Example: Counter(CtrMode, InCh, Enable, TimeOut, ...)
    # 20.06.20:
    if Left(Org_Macro, Len('Counter(')) == 'Counter(':
        if InStr(Line, 'CF_ONLY_LOCALVAR') > 0:
            _ret = True
            return _ret
    Arg = __Get_Matching_Arg(Org_Macro, Line, 'OutList')
    if Arg != '':
        for Name in Split(Arg, ','):
            if not Add_Variable_to_DstVar_List(Name):
                return _ret
        _ret = True
    return _ret

def __Add_Cx_to_DstVars(Org_Macro, Line, Cnt, r):
    _ret = False
    Arg1 = String()

    TxtLen = int()
    #---------------------------------------------------------------------------------------------------------
    # Example: PushButton_w_LED_0_2(B_LED, B_LED_Cx, InCh, DstVar1, Rotate, Timeout)
    Arg1 = __Get_Matching_Arg(Org_Macro, Line, 'DstVar1')
    if Arg1 != '':
        StartNr, TxtLen = __Get_Nr_From_Var(Arg1, TxtLen)
        if StartNr < 0:
            P01.MsgBox(Replace(Replace(Replace(M09.Get_Language_Str('Fehler: Die Zielvariable \'#1#\' in Zeile #2# muss eine Zahl am Ende haben ' + 'weil sie Teil einer Sequenz ist.' + vbCr + '  Beispiel: #3#'), "#1#", Arg1), '#2#', r), '#3#', Arg1 + '0'), vbCritical, M09.Get_Language_Str('Fehler: Zielvariable ungültig für Sequenz'))
            return _ret
        EndNr = StartNr + Cnt - 1
        for i in vbForRange(StartNr, EndNr):
            if Add_Variable_to_DstVar_List(Left(Arg1, TxtLen) + i) == False:
                return _ret
        _ret = True
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Line - ByVal 
def Add_Inp_and_DstVars(Line, r):
    _ret = ""
    Parts = vbObjectInitialize(objtype=String)

    p = int()

    Org_Macro_Row = int()

    Arguments = String()

    Res = Boolean()

    SearchMacro = String()
    #------------------------------------------------------------------------------
    # Following types of macros are defined which generate DstVar's (One example per typ)
    #
    #  1   Logic(           DstVar, ...)                                         o.k.
    #  2   MonoFlop2(       DstVar1, DstVar2, InCh, Duration)                    o.k.
    #  n…  Counter(         CtrMode, InCh, Enable, TimeOut, ...)                 o.k.
    #  n2  RandMux(DstVar1, DstVarN, InCh, RandMode, MinTime, MaxTime)           o.k.
    #
    _ret = True
    if InStr(Line, '(') == 0:
        return _ret
    Parts = Split(Line, '(')
    Arguments = Parts(1)
    p = InStrRev(Arguments, ')')
    if p == 0:
        return _ret
    if Parts(0) == 'HouseT':
        SearchMacro = 'House'
    else:
        SearchMacro = Parts(0)
    Org_Macro_Row = M09SM.Find_Macro_in_Lib_Macros_Sheet(SearchMacro + '(')
    if Org_Macro_Row == 0:
        Debug.Print('Attention: Macro \'' + Line + ' not found in \'' + M02.LIBMACROS_SH + '\'')
        # ToDo: Wie können Zielvariablen in diesen Makros erkannt werden?
    else:
        _with0 = P01.Sheets(M02.LIBMACROS_SH)
        OutCntStr = _with0.Cells(Org_Macro_Row, M02.SM_OutCntCOL)
        Org_Macro = _with0.Cells(Org_Macro_Row, M02.SM_Macro_COL)
        if __Add_InpVars(Parts(0), Org_Macro, Line, r, Org_Macro_Row) == False:
            _ret = False
            return _ret
        _select4 = OutCntStr
        if (_select4 == '') or (_select4 == '0'):
            _ret = True
            return _ret
        elif (_select4 == '1'):
            Res = __Add_Matching_Arg_to_DstVars(Org_Macro, Line, 'DstVar')
        elif (_select4 == '2'):
            Res = __Add_Matching_Arg_to_DstVars(Org_Macro, Line, 'DstVar1')
            if Res:
                Res = __Add_Matching_Arg_to_DstVars(Org_Macro, Line, 'DstVar2')
        elif (_select4 == 'n..'):
            Res = __Add_VarArgCnt_to_DstVars(Org_Macro, Line)
        elif (_select4 == 'n2'):
            Res = __Add_N2_Arg_to_DstVars(Org_Macro, Line)
        else:
            if Left(OutCntStr, 1) == 'C':
                if IsNumeric(Mid(OutCntStr, 2)):
                    Res = __Add_Cx_to_DstVars(Org_Macro, Line, P01.val(Mid(OutCntStr, 2)), r)
            else:
                P01.MsgBox('Internal Error: Undefined OutCnt entry \'' + OutCntStr + '\' in row ' + str(Org_Macro_Row) + ' in sheet \'' + M02.LIBMACROS_SH + '\'', vbCritical, 'Internal Error')
                return _ret
        if Res == False:
            P01.Cells(r, M25.Config__Col).Select()
            P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler in der Definition der Zielvariable(n): \'#1#\' in Zeile #2#'), "#1#", Line), '#2#', r), vbCritical, M09.Get_Language_Str('Fehler in Makro Definition'))
            _ret = False
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel - ByRef 
def Print_DstVar_List(fp, Channel):
    global __DstVar_List
    
    Var = Variant()
    #-----------------------------------------------------------------
    for Var in Split(Trim(__DstVar_List), ' '):
        VBFiles.writeText(fp, '#define ' + M30.AddSpaceToLen(Var, 22) + '  ' + str(Channel), '\n')
        Channel = Channel + 1
    return Channel

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ExpectedName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Nr - ByRef 
def Is_in_Nr_String(Name, ExpectedName, MinNr, MaxNr, Nr):
    _ret = False
    SkipCnt = int()
    #------------------------------------------------------------------------------------------------------------------------------------------
    # Check if "Name" starts with "ExpectedName" and has a tailing number in the range form MinNr to MaxNr
    while Right(ExpectedName, 1) == '?':
        SkipCnt = SkipCnt + 1
        ExpectedName = M30.DelLast(ExpectedName)
    if Left(Name, Len(ExpectedName)) == ExpectedName:
        NrStr = Mid(Name, 1 + Len(ExpectedName) + SkipCnt)
        if IsNumeric(NrStr):
            if Left(NrStr, 1) == '0':
                return _ret
                # Leading 0 are not allowed because they generate the same number
            WrongChar = '-+.,eE'
            for i in vbForRange(1, Len(WrongChar)):
                if InStr(NrStr, Mid(WrongChar, i, 1)) > 0:
                    return _ret
            Nr = P01.val(NrStr)
            if Nr >= MinNr and Nr <= MaxNr:
                _ret = 1
            else:
                _ret = - 1
    return _ret, Nr

def __Test_Is_in_Nr_String():
    Nr = int()
    #UT-------------------------------
    Debug.Print('Is_in_Nr_String=' + Is_in_Nr_String('HalloAB13', 'Hallo??', 1, 200, Nr))

def __Error_Msg_Varaible_Not_Defined(VarName, r):
    #-----------------------------------------------------------------------
    P01.Cells(r, M25.Get_Address_Col()).Select()
    P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Die Variable \'#1#\' in Zeile #2# ist nicht definiert'), "#1#", VarName), '#2#', r), vbCritical, M09.Get_Language_Str('Fehler: Undefinierte Variable'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def Valid_Var_Name(Name, Row):
    global __MaxUsed_Loc_InCh, __MaxUsed_Loc_InCh_Row, Undefined_Input_Var, Undef_Input_Var_Row, __DstVar_List
    
    _ret = False
    Std_Names = 'SI_1 SI_0 SI_Enable_Sound #LocInCh'

    Nr = int()

    Std_N = Variant()
    #---------------------------------------------------------------------------
    # Check if it's a valid variable (Switch<Nr>, Button<Nr>, INCH_DCC_..., LOC_INCH<Nr>, ...)
    _ret = True
    for Std_N in Split(Std_Names, ' '):
        if Name == Std_N:
            return _ret
    _select5 = __Is_Switch_Var_then_Add_to_Ctr(Name)
    if (_select5 == 1):
        return _ret
    elif (_select5 == - 1):
        _ret = False
        P01.Cells(Row, M25.Config__Col).Select()
        return _ret
    if InStr(__DstVar_List, ' ' + Name + ' '):
        return _ret
    if InStr(M06.InChTxt, '#define ' + Name + ' ') > 0:
        return _ret
    _select6, Nr = Is_in_Nr_String(Name, 'LOC_INCH', 0, 250, Nr)
    if (_select6 == 1):
        if Nr > __MaxUsed_Loc_InCh:
            __MaxUsed_Loc_InCh = Nr
            __MaxUsed_Loc_InCh_Row = Row
        return _ret
    elif (_select6 == - 1):
        P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Die Nummer der Variable \'#1#\' ist ungültig!' + vbCr + vbCr + 'Gültiger Bereich: #2#'), "#1#", Name), '#2#', '0..250'), vbCritical, M09.Get_Language_Str('Fehler: Ungültige Variable'))
    # Old:
    #  Error_Msg_Varaible_Not_Defined Name, Row
    #  Valid_Var_Name = False
    # Add the undefined input variable to a list which is checked later
    if InStr(Undefined_Input_Var, ' ' + Name + ' ') == 0:
        Undefined_Input_Var = Undefined_Input_Var + Name + ' '
        Undef_Input_Var_Row = Undef_Input_Var_Row + str(Row) + ' '
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Arg - ByVal 
def __Valid_Var_Name_and_Skip_InCh_and_Numbers(Arg, Row):
    _ret = False
    SubArgList = vbObjectInitialize(objtype=String)

    SubArg = Variant()
    #-----------------------------------------------------------------------------------------------------
    SubArgList = M30.SplitMultiDelims(Arg, ' +-')
    for SubArg in SubArgList:
        if SubArg == '#InCh':
            if M09SM.Get_InCh_Number_w_Err_Msg(Arg) < 0:
                return _ret
                # Check the whole argumnet to make sure that the equation contains only constants
        else:
            if not IsNumeric(SubArg):
                if Valid_Var_Name(SubArg, Row) == False:
                    return _ret
    _ret = True
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Dest - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel - ByRef 
def Create_Loc_InCh_Defines(Dest, Channel, LocInChNr):
    global __MaxUsed_Loc_InCh_Row, __MaxUsed_Loc_InCh
    
    #-------------------------------------------------------------------------------------------------
    if LocInChNr > 0:
        Dest = Dest + vbCr + '// Local InCh variables' + vbCr
        for i in vbForRange(0, LocInChNr - 1):
            Dest = Dest + M30.AddSpaceToLen('#define LOC_INCH' + str(i), 32) + str(Channel) + vbCr
            Channel = Channel + 1
    if __MaxUsed_Loc_InCh >= LocInChNr:
        __Error_Msg_Varaible_Not_Defined('LOC_INCH' + __MaxUsed_Loc_InCh, __MaxUsed_Loc_InCh_Row)
    return Dest, Channel

        

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Nr - ByRef 
def __Print_Keyboard_Defines_for_Type(fp, Name, InpCnt, Nr, Skip_11_16=False):
    i = int()

    ResCnt = int()
    #-------------------------------------------------------------------------------------------------------------------------------------------
    for i in vbForRange(1, InpCnt):
        VBFiles.writeText(fp, M30.AddSpaceToLen('#define ' + Name + str(i), 32) + str(Nr), '\n')
        if Skip_11_16:
            if ( i - 1 % 16 )  == 9:
                Nr = Nr + 6
                # Skip the IONr 11 and 16 because they are not used for the analog switches, but have to be reserved for MobaLedLib_Copy_to_InpStruct()
        Nr = Nr + 1
    # Es werden immer vielfache von 8 Inp Channels belegt
    ResCnt = ( 8 -  ( InpCnt % 8 ) )  % 8
    if ResCnt > 0:
        Nr = Nr + ResCnt
        VBFiles.writeText(fp, '// Reserve channels: ' + ResCnt + ' because MobaLedLib_Copy_to_InpStruct always writes multiple of 8 channels', '\n')
    
    return Nr

def __Test_ResCnt():
    InpCnt = int()

    ResCnt = int()
    #UT----------------------
    # Test for the problem above
    Debug.Print('i Ok  Err')
    for InpCnt in vbForRange(0, 24):
        ResCnt = ( 8 -  ( InpCnt % 8 ) )  % 8
        Debug.Print(Left(InpCnt + '   ', 3) + Left(ResCnt + '   ', 3) +  ( 8 - InpCnt )  % 8)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel - ByRef 
def __Make_sure_that_Channel_is_divisible_by_4(Channel):
    #--------------------------------------------------------------------------
    if Channel % 4 != 0:
        Channel = Channel + 4 - Channel % 4
    return Channel

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel - ByRef 
def Write_Switches_Header_File_Part_A(fp, Channel):
    global __DstVar_List, SwitchA_InpCnt, SwitchB_InpCnt, SwitchC_InpCnt, SwitchD_InpCnt, SwitchA_InpLst, SwitchB_InpLst, SwitchC_InpLst, SwitchD_InpLst, Switch_Damping_Fact, CLK_Pin_Number, RST_Pin_Number
    
    _ret = False
    Ana_But_Pin_Array = vbObjectInitialize(objtype=String)

    ACh = int()

    Used_AButton_Channels = int()

    Start_AButtons = int()

    dmxDefines = String()
    DMX_Pin_Number = "" #*HL
    #-------------------------------------------------------------------------------------------------
    # #If USE_SWITCH_AND_LED_ARRAY Then                                         ' 04.11.20:
    #    Print #fp, "#define USE_SWITCH_AND_LED_ARRAY 1    // Enable the new function which handles the SwitchD and the Mainboard LEDs in the ino file"
    # #Else
    #    Print #fp, "#define USE_SWITCH_AND_LED_ARRAY 0"
    #    If Get_BoardTyp() = "ESP32" Then                                       ' 04.11.20:
    #        MsgBox "Internal error: The compiler switch 'USE_SWITCH_AND_LED_ARRAY' must be defined if the ESP32 is used", vbCritical, "Internal error"
    #        'EndProg
    #     End If
    #  #End If
    #  Print #fp, ""
    if SwitchA_InpCnt > 0 or Read_LDR:
        Ana_But_Pin_Array = Split(SwitchA_InpLst, ' ')
        if SwitchA_InpCnt >  ( UBound(Ana_But_Pin_Array) + 1 )  * 10:
            P01.MsgBox(M09.Get_Language_Str('Fehler: Es wurden mehr analoge Taster verwendet als möglich sind. ' + 'Es müssen weitere analoge Eingänge zum einlesen definiert werden.' + vbCr + 'Das wird mit dem Befehl \'Set_SwitchA_InpLst()\' in der Makro Spalte gemacht.'), vbCritical, M09.Get_Language_Str('Fehler: Nicht genügend analoge Eingänge zum einlesen der Taster definiert'))
            return _ret, Channel
        
        VBFiles.writeText(fp, '#ifndef CONFIG_ONLY', '\n')
        VBFiles.writeText(fp, '//*** Analog switches ***', '\n')
        VBFiles.writeText(fp, '', '\n')
        if M02a.Get_BoardTyp() == 'AM328':
            if M70.Make_Sure_that_AnalogScanner_Library_Exists() == False:
                return _ret, Channel
            VBFiles.writeText(fp, '#include <AnalogScanner.h>   // Interrupt driven analog reading library. The library has to be installed manually from https://github.com/merose/AnalogScanner', '\n')
            VBFiles.writeText(fp, 'AnalogScanner scanner;       // Creates an instance of the analog pin scanner.', '\n')
        elif M02a.Get_BoardTyp() == 'ESP32':
            VBFiles.writeText(fp, '#include "AnalogScannerESP32.h"   ', '\n')
            VBFiles.writeText(fp, 'AnalogScannerESP32 scanner;       // Creates an instance of the analog pin scanner.', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '#include <Analog_Buttons10.h>', '\n')
        Used_AButton_Channels = WorksheetFunction.RoundUp(SwitchA_InpCnt / 10, 0)
        for ACh in vbForRange(1, Used_AButton_Channels):
            VBFiles.writeText(fp, 'Analog_Buttons10_C AButtons' + ACh + '(' + Ana_But_Pin_Array(ACh - 1) + ');', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
        if Switch_Damping_Fact != '':
            VBFiles.writeText(fp, Switch_Damping_Fact, '\n')
            VBFiles.writeText(fp, '', '\n')
        if Read_LDR:
            VBFiles.writeText(fp, '#include "Read_LDR.h"     // Darkness sensor', '\n')
            VBFiles.writeText(fp, '', '\n')
            
        VBFiles.writeText(fp, '#endif //CONFIG_ONLY', '\n')
            
        Channel = __Make_sure_that_Channel_is_divisible_by_4(Channel)
        Start_AButtons = Channel
        TmpChannel = Channel
        TmpChannel = __Print_Keyboard_Defines_for_Type(fp, 'SwitchA', SwitchA_InpCnt, TmpChannel, Skip_11_16=True)
        Channel = Channel + Used_AButton_Channels * 16
        VBFiles.writeText(fp, '', '\n')
    if __Channel1InpCnt > 0:
        VBFiles.writeText(fp, '//*** Digital switches ***', '\n')
        VBFiles.writeText(fp, '', '\n')
        # Generate the #define Switch... statements
        Channel =__Make_sure_that_Channel_is_divisible_by_4(Channel)
        StartSwitches1 = Channel
        if __Channel1InpCnt > 0:
            Channel = __Print_Keyboard_Defines_for_Type(fp, __CTR_Cha_Name_1, __Channel1InpCnt, Channel)
        Channel =__Make_sure_that_Channel_is_divisible_by_4(Channel)
        StartSwitches2 = Channel
        if __Channel2InpCnt > 0:
            Channel = __Print_Keyboard_Defines_for_Type(fp, __CTR_Cha_Name_2, __Channel2InpCnt, Channel)
        VBFiles.writeText(fp, '', '\n')
    if SwitchD_InpCnt >  ( UBound(Split(SwitchD_InpLst, ' ')) + 1 ) :
        # Todo: Activate the corrosponding cell. Therefore a list has to be generated where each switch is used the first time
        P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Es wurden mehr SwitchD Schalter verwendet als Pins definiert sind. ' + 'Es müssen weitere Eingänge zum einlesen definiert werden.' + vbCr + 'Das wird mit dem Befehl \'Set_SwitchD_InpLst()\' in der Makro Spalte gemacht.' + vbCr + 'Letzter möglicher Schalter: \'SwitchD#1#\''), "#1#", UBound(Split(SwitchD_InpLst, ' ')) + 1), vbCritical, M09.Get_Language_Str('Fehler: Nicht genügend Eingänge zum einlesen der Schalter definiert'))
        return _ret, Channel
    if SwitchD_InpCnt > 0:
        VBFiles.writeText(fp, '//*** Direct connected switches ***', '\n')
        VBFiles.writeText(fp, '', '\n')
        Channel = __Print_Keyboard_Defines_for_Type(fp, 'SwitchD', SwitchD_InpCnt, Channel)
        VBFiles.writeText(fp, '', '\n')
    if __DstVar_List != ' ':
        VBFiles.writeText(fp, '//*** Output Channels ***', '\n')
        Channel = Print_DstVar_List(fp, Channel)
        VBFiles.writeText(fp, '', '\n')
    if SwitchD_InpCnt > 0:
        VBFiles.writeText(fp, 'const PROGMEM uint8_t SwitchD_Pins[] = ' + M30.AddSpaceToLen('{ ' + Replace(SwitchD_InpLst, ' ', ',') + ' };', 28) + '// Array of pins which read switches \'D\'', '\n')
        VBFiles.writeText(fp, '#define SWITCH_D_INP_CNT sizeof(SwitchD_Pins)', '\n')
        VBFiles.writeText(fp, '', '\n')
    if __Channel1InpCnt > 0:
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '#define CTR_CHANNELS_1    ' + M30.AddSpaceToLen(__CTR_Channels_1, 41) + '// Number of used counter channels for keyboard 1. Up to 10 if one CD4017 is used, up to 18 if two CD4017 are used, ...', '\n')
        VBFiles.writeText(fp, '#define CTR_CHANNELS_2    ' + M30.AddSpaceToLen(__CTR_Channels_2, 41) + '// Number of used counter channels for keyboard 2. Up to 10 if one CD4017 is used, up to 18 if two CD4017 are used, ...', '\n')
        VBFiles.writeText(fp, '#define BUTTON_INP_LIST_1 ' + M30.AddSpaceToLen(Replace(__But_Inp_List_1, ' ', ','), 41) + '// Comma separated list of the button input pins', '\n')
        VBFiles.writeText(fp, '#define BUTTON_INP_LIST_2 ' + M30.AddSpaceToLen(Replace(__But_Inp_List_2, ' ', ','), 41) + '// Comma separated list of the button input pins', '\n')
        VBFiles.writeText(fp, '#define CLK_PIN           ' + M30.AddSpaceToLen(CLK_Pin_Number, 41) + '// Pin number used for the CD4017 clock', '\n')
        VBFiles.writeText(fp, '#define RESET_PIN         ' + M30.AddSpaceToLen(RST_Pin_Number, 41) + '// Pin number used for the CD4017 reset', '\n')
        VBFiles.writeText(fp, '', '\n')
        
        VBFiles.writeText(fp, '#ifndef CONFIG_ONLY', '\n')
        VBFiles.writeText(fp, '#include <Keys_4017.h>                                             // Keyboard library which uses the CD4017 counter to save Arduino pins. Attention: The pins (CLK_PIN, ...) must be defined prior.', '\n')
        VBFiles.writeText(fp, '#endif //CONFIG_ONLY', '\n')
        
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '#define START_SWITCHES_1  ' + M30.AddSpaceToLen(StartSwitches1, 41) + '// Define the start number for the first keyboard.', '\n')
        VBFiles.writeText(fp, '#define START_SWITCHES_2  ' + M30.AddSpaceToLen(StartSwitches2, 41) + '// Define the start number for the second keyboard.', '\n')
        VBFiles.writeText(fp, '', '\n')
    if True:
        # FastLED initialisation                                                ' 26.04.20:
        LED_PINNr_Arr = Split(LED_PINNr_List, ' ')
        VBFiles.writeText(fp, '/*********************/', '\n')
        VBFiles.writeText(fp, '#define SETUP_FASTLED()                                                      \\', '\n')
        VBFiles.writeText(fp, '/*********************/                                                      \\', '\n')
        Cnt = 0 #*HL
        for LEDCh in vbForRange(0, M02.LED_CHANNELS - 1):
            if M06.LEDs_per_Channel(LEDCh) > 0:
                ExpOutPins = LEDCh
                if LEDCh <= UBound(LED_PINNr_Arr):
                    if LEDCh != DMX_LedChan:
                        if LED_PINNr_Arr(LEDCh) != M09.Virtual_Channel_T:   #   18.02.22 Juergen Virtual Channel
                            # Generate: CLEDController& controller0 = FastLED.addLeds<NEOPIXEL,  6 >(leds+   0, 200); \"
                            if __Use_WS2811:
                                VBFiles.writeText(fp, '  CLEDController& controller' + str(LEDCh) + ' = FastLED.addLeds<WS2811, ' + M30.AddSpaceToLenLeft(LED_PINNr_Arr(LEDCh), 2) + ', RGB>(leds+' + M30.AddSpaceToLenLeft(str(Cnt), 3) + ',' + M30.AddSpaceToLenLeft(str(M06.LEDs_per_Channel(LEDCh)), 3) + '); \\', '\n')
                            else:
                                VBFiles.writeText(fp, '  CLEDController& controller' + str(LEDCh) + ' = FastLED.addLeds<NEOPIXEL, ' + M30.AddSpaceToLenLeft(LED_PINNr_Arr(LEDCh), 2) + '>(leds+' + M30.AddSpaceToLenLeft(str(Cnt), 3) + ',' + M30.AddSpaceToLenLeft(str(M06.LEDs_per_Channel(LEDCh)), 3) + '); \\', '\n')
                    else:
                        dmxDefines = '#define DMX_LED_OFFSET ' + str(Cnt) + vbCrLf + '#define DMX_CHANNEL_COUNT ' + str(M06.LEDs_per_Channel(LEDCh) * 3)
                        DMX_Pin_Number = LED_PINNr_Arr(LEDCh)
                        if ( M06.LEDs_per_Channel(LEDCh) > 100 ) :
                            P01.MsgBox(M09.Get_Language_Str('Fehler: Das DMX Senden ist auf 100 Leds (300 DMX Kanäle) limitiert.'), vbCritical, P01.ActiveSheet.Name)
                            return _ret, Channel
            Cnt = Cnt + M06.LEDs_per_Channel(LEDCh)
        if ExpOutPins > UBound(LED_PINNr_Arr):
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Es sind nicht genügend Ausgangs Pins zur Ansteuerung der LEDs vorhanden. ' + 'Die LED Pins müssen mit dem Befehl "Set_LED_OutpPinLst()" definiert werden.' + vbCr + 'Es müssen #1# Arduino Ausgänge definiert sein.'), "#1#", str(ExpOutPins + 1)), vbCritical, M09.Get_Language_Str('Mehr LED Gruppen verwendet als LED Ausgangspins definiert'))
            return _ret, Channel
        VBFiles.writeText(fp, '                                                                             \\', '\n')
        for LEDCh in vbForRange(0, M02.LED_CHANNELS - 1):
            if M06.LEDs_per_Channel(LEDCh) > 0 and LEDCh <= UBound(LED_PINNr_Arr) and  ( LEDCh != DMX_LedChan ) :
                if LED_PINNr_Arr(LEDCh) != M09.Virtual_Channel_T:   #  ' 18.02.22 Juergen Virtual Channel
                    VBFiles.writeText(fp, '  controller' + str(LEDCh) + '.clearLeds(256);                                                \\', '\n')
        VBFiles.writeText(fp, '  FastLED.setDither(DISABLE_DITHER);       // avoid sending slightly modified brightness values', '\n')
        VBFiles.writeText(fp, '/*End*/', '\n')
        VBFiles.writeText(fp, '', '\n')
        if DMX_Pin_Number != '' and dmxDefines != '':
            VBFiles.writeText(fp, '#include "DmxInterface.h"     // DMX512 Interface', '\n')
            VBFiles.writeText(fp, '#define USE_DMX_PIN ' + str(DMX_Pin_Number), '\n')
            VBFiles.writeText(fp, dmxDefines, '\n')
            VBFiles.writeText(fp, 'DMXInterface dmxInterface;', '\n')
    # Additional Setup proc
    if SwitchA_InpCnt > 0 or Read_LDR or __Channel1InpCnt > 0 or SwitchD_InpCnt > 0:
        VBFiles.writeText(fp, '#define USE_ADDITIONAL_SETUP_PROC                                  // Activate the usage of the Additional_Setup_Proc()', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '//--------------------------', '\n')
        VBFiles.writeText(fp, 'void Additional_Setup_Proc()', '\n')
        VBFiles.writeText(fp, '//--------------------------', '\n')
        VBFiles.writeText(fp, '{', '\n')
        PinList=""
        
        if SwitchA_InpCnt > 0 or Read_LDR:
            
            VBFiles.writeText(fp, '#ifndef CONFIG_ONLY', '\n')
            if SwitchA_InpCnt > 0:
                PinList = Replace(Trim(SwitchA_InpLst), ' ', ',') + ','
            if Read_LDR:
                PinList = PinList + LDR_Pin_Number + ','
            PinList = M30.DelLast(PinList)
            VBFiles.writeText(fp, '  int scanOrder[] = {' + PinList + '};', '\n')
            VBFiles.writeText(fp, '  const int SCAN_COUNT = sizeof(scanOrder) / sizeof(scanOrder[0]);', '\n')
            if M02a.Get_BoardTyp() == 'AM328':
                VBFiles.writeText(fp, '', '\n')
                if Read_LDR:
                    VBFiles.writeText(fp, '  Init_DarknessSensor(' + str(LDR_Pin_Number) + ', 50, SCAN_COUNT); // Attention: The analogRead() function can\'t be used together with the darkness sensor !', '\n')
                    VBFiles.writeText(fp, '  scanner.setCallback(' + str(LDR_Pin_Number) + ', Darkness_Detection_Callback);', '\n')
                VBFiles.writeText(fp, '  scanner.setScanOrder(SCAN_COUNT, scanOrder);', '\n')
                VBFiles.writeText(fp, '  scanner.beginScanning();', '\n')
            elif M02a.Get_BoardTyp() == 'ESP32':
                VBFiles.writeText(fp, '  scanner.setScanPins(SCAN_COUNT, scanOrder);', '\n')
                if Read_LDR:
                    VBFiles.writeText(fp, '  Init_DarknessSensor(' + str(LDR_Pin_Number) + ', 50, 50); // Attention: The analogRead() function can\'t be used together with the darkness sensor !', '\n')
                    VBFiles.writeText(fp, '  scanner.setCallback(' + str(LDR_Pin_Number) + ', Darkness_Detection_Callback);', '\n')
            
            VBFiles.writeText(fp, '#endif //CONFIG_ONLY', '\n')
            
        if __Channel1InpCnt > 0:
            VBFiles.writeText(fp, '#ifndef CONFIG_ONLY', '\n')
            VBFiles.writeText(fp, '  Keys_4017_Setup(); // Initialize the keyboard scanning process', '\n')
            VBFiles.writeText(fp, '#endif //CONFIG_ONLY', '\n')
            
        if SwitchD_InpCnt > 0:
            VBFiles.writeText(fp, '', '\n')
            VBFiles.writeText(fp, '  for (uint8_t i = 0; i < SWITCH_D_INP_CNT; i++)', '\n')
            VBFiles.writeText(fp, '    pinMode(pgm_read_byte_near(&SwitchD_Pins[i]), INPUT_PULLUP);', '\n')
        VBFiles.writeText(fp, '}', '\n')
        VBFiles.writeText(fp, '', '\n')
    # Generate the "Additional_Loop_Proc()"
    if SwitchA_InpCnt > 0 or __Channel1InpCnt > 0 or SwitchD_InpCnt > 0:
        VBFiles.writeText(fp, '/****************************/', '\n')
        VBFiles.writeText(fp, '#define Additional_Loop_Proc() \\', '\n')
        VBFiles.writeText(fp, '/****************************/ \\', '\n')
        VBFiles.writeText(fp, '{                              \\', '\n')
        if SwitchA_InpCnt > 0:
            Act_Start_AButtons = Start_AButtons
            VBFiles.writeText(fp, '  uint16_t Button;             \\', '\n')
            for ACh in vbForRange(1, Used_AButton_Channels):
                VBFiles.writeText(fp, M30.AddSpaceToLen('  Button = AButtons' + str(ACh) + '.Get(); MobaLedLib_Copy_to_InpStruct((uint8_t*)&Button, 2, ' + str(Act_Start_AButtons) + ');', 89) + '\\', '\n')
                Act_Start_AButtons = Act_Start_AButtons + 16
        if __Channel1InpCnt > 0:
            VBFiles.writeText(fp, '  MobaLedLib_Copy_to_InpStruct(Keys_Array_1, KEYS_ARRAY_BYTE_SIZE_1, START_SWITCHES_1);  \\', '\n')
        if __Channel2InpCnt > 0:
            VBFiles.writeText(fp, '  MobaLedLib_Copy_to_InpStruct(Keys_Array_2, KEYS_ARRAY_BYTE_SIZE_2, START_SWITCHES_2);  \\', '\n')
        if SwitchD_InpCnt > 0:
            VBFiles.writeText(fp, '  for (uint8_t i = 0; i < ' + str(SwitchD_InpCnt) + '; i++) \\', '\n')
            VBFiles.writeText(fp, '      MobaLedLib.Set_Input(SwitchD1 + i, !digitalRead(pgm_read_byte_near(&SwitchD_Pins[i])));\\', '\n')
        VBFiles.writeText(fp, '}', '\n')
    _ret = True
    return _ret, Channel

def Write_LowProrityLoop_Header_File(fp):
    _ret = False
    if Serial_PinLst != '':
        VBFiles.writeText(fp, '/*****************************/', '\n')
        VBFiles.writeText(fp, '#define Additional_Loop_Proc2() \\', '\n')
        VBFiles.writeText(fp, '/*****************************/ \\', '\n')
        VBFiles.writeText(fp, '{                               \\', '\n')
        if Serial_PinLst != '':
            VBFiles.writeText(fp, '   soundProcessor.process();\\', '\n')
        VBFiles.writeText(fp, '}', '\n')
    _ret = True
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpLst1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpLst2 - ByVal 
def __No_Duplicates_in_two_InpLists(Letter1, Letter2_or_Name, InpLst1, InpLst2, Set_Funct2='Set_LED_OutpPinLst()'):
    _ret = False
    Pin = Variant()
    #-----------------------------------------------------------------------------------------------------------------------------------------
    # Retutn True if no duplicates are detected
    InpLst2 = ' ' + InpLst2 + ' '
    for Pin in Split(InpLst1, ' '):
        if InStr(InpLst2, ' ' + Pin + ' ') > 0:
            if Len(Letter2_or_Name) == 1:
                P01.MsgBox(Replace(Replace(Replace(M09.Get_Language_Str('Fehler: Der Eingabe Pin \'#1#\' des Arduinos wird als Eingabe in den zwei Schalter Funktionen \'#2#\' und \'#3#\' benutzt.' + vbCr + 'Die beiden Schalter Funktionen können nicht gleichzeitig benutzt werden. Die Pins können mit den Funktionen ' + '\'Set_Switch?_InpLst()\' angepasst werden.' + vbCr + 'Achtung: Dazu muss auch die Hardware angepasst werden!'), "#1#", Pin), '#2#', Letter1), '#3#', Letter2_or_Name), vbCritical, 'Fehler: Doppelte benutzung der Eingangs Pins')
            else:
                P01.MsgBox(Replace(Replace(Replace(Replace(M09.Get_Language_Str('Fehler: Der Eingabe Pin \'#1#\' des Arduinos wird als Eingabe in der Schalter Funktionen \'#2#\' und gleichzeitig ' + 'als #3# Pin benutzt.' + vbCr + 'Die Pins können mit den Funktionen \'Set_Switch?_InpLst()\' und \'#4#\' angepasst werden.' + vbCr + 'Achtung: Dazu muss auch die Hardware angepasst werden!'), "#1#", Pin), '#2#', Letter1), '#3#', Letter2_or_Name), '#4#', Set_Funct2), vbCritical, 'Fehler: Doppelte benutzung der Arduino Pins')
            return _ret
    _ret = True
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpLst1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpLst2 - ByVal 
def No_Duplicates_in_two_Lists(Pin2, InpLst1, InpLst2, Set_Funct2='Set_LED_OutpPinLst()'):
    _ret = False
    Pin = Variant()
    #-----------------------------------------------------------------------------------------------------------------------------------------
    # Retutn True if no duplicates are detected
    InpLst2 = ' ' + InpLst2 + ' '
    for Pin in Split(InpLst1, ' '):
        if InStr(InpLst2, ' ' + Pin + ' ') > 0:
            P01.MsgBox(Replace(Replace(Replace(M09.Get_Language_Str('Fehler: Der Pin \'#1#\' in \'#3#\' wird bereits als \'#2#\' Pin benutzt.' + vbCr + 'Der Pin kann nicht mehrfach benutzt werden.'), "#1#", Pin), '#2#', Pin2), '#3#', Set_Funct2), vbCritical, 'Fehler: Doppelte Benutzung eines Pins')
            return _ret
    _ret = True
    return _ret

def __Test_No_Duplicates_in_two_InpLists():
    #UT------------------------------------------------
    SwitchC_InpLst = '2 7 8 9 10 11 12 A5'
    SwitchD_InpLst = '7 8 9'
    #Debug.Print No_Duplicates_in_two_InpLists("C", "D", SwitchC_InpLst, SwitchD_InpLst)
    LED_PINNr_List = '6 A4 A5'
    Debug.Print(__No_Duplicates_in_two_InpLists('C', 'LED', SwitchC_InpLst, LED_PINNr_List))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpLst1 - ByVal 
def __Check_CLK_a_RST_Pin_Usage(Letter1, InpLst1):
    global RST_Pin_Number, CLK_Pin_Number
    
    _ret = False
    #------------------------------------------------------------------------------------------------
    # Check the RST_Pin_Number together with Letter1
    if SwitchB_InpCnt > 0 or SwitchC_InpCnt > 0:
        if False == __No_Duplicates_in_two_InpLists(Letter1, Replace(M09.Get_Language_Str('#1# Pin für SwitchB oder SwitchC'), "#1#", 'Reset'), InpLst1, RST_Pin_Number, 'Set_RST_Pin_Number()'):
            return _ret
        if False == __No_Duplicates_in_two_InpLists(Letter1, Replace(M09.Get_Language_Str('#1# Pin für SwitchB oder SwitchC'), "#1#", 'Clock'), InpLst1, CLK_Pin_Number, 'Set_CLK_Pin_Number()'):
            return _ret
    _ret = True
    return _ret

def No_Duplicates_in_InpLists():
    _ret = False
    #-----------------------------------------------------
    if SwitchA_InpCnt > 0:
        if SwitchB_InpCnt > 0:
            if __No_Duplicates_in_two_InpLists('A', 'B', SwitchA_InpLst, SwitchB_InpLst) == False:
                return _ret
        if SwitchC_InpCnt > 0:
            if __No_Duplicates_in_two_InpLists('A', 'C', SwitchA_InpLst, SwitchC_InpLst) == False:
                return _ret
        if SwitchD_InpCnt > 0:
            if __No_Duplicates_in_two_InpLists('A', 'D', SwitchA_InpLst, SwitchD_InpLst) == False:
                return _ret
        if __No_Duplicates_in_two_InpLists('A', 'LED', SwitchA_InpLst, LED_PINNr_List) == False:
            return _ret
        if Read_LDR:
            if __No_Duplicates_in_two_InpLists('A', 'LDR', SwitchA_InpLst, LDR_Pin_Number, 'Set_LDR_Pin_Number()') == False:
                return _ret
        if __Check_CLK_a_RST_Pin_Usage('A', SwitchA_InpLst) == False:
            return _ret
            # 04.11.20:
        if __No_Duplicates_in_two_InpLists('A', 'SOUND', SwitchA_InpLst, Serial_PinLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _ret
            # 08.10.21: Juergen
    if SwitchB_InpCnt > 0:
        if SwitchC_InpCnt > 0:
            if __No_Duplicates_in_two_InpLists('B', 'C', SwitchB_InpLst, SwitchC_InpLst) == False:
                return _ret
        if SwitchD_InpCnt > 0:
            if __No_Duplicates_in_two_InpLists('B', 'D', SwitchB_InpLst, SwitchD_InpLst) == False:
                return _ret
        if __No_Duplicates_in_two_InpLists('B', 'LED', SwitchB_InpLst, LED_PINNr_List) == False:
            return _ret
        if Read_LDR:
            if __No_Duplicates_in_two_InpLists('B', 'LDR', SwitchB_InpLst, LDR_Pin_Number, 'Set_LDR_Pin_Number()') == False:
                return _ret
        if __Check_CLK_a_RST_Pin_Usage('B', SwitchB_InpLst) == False:
            return _ret
            # 04.11.20:
        if __No_Duplicates_in_two_InpLists('B', 'SOUND', SwitchA_InpLst, Serial_PinLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _ret
            # 08.10.21: Juergen
    if SwitchC_InpCnt > 0:
        if SwitchD_InpCnt > 0:
            if __No_Duplicates_in_two_InpLists('C', 'D', SwitchC_InpLst, SwitchD_InpLst) == False:
                return _ret
        if __No_Duplicates_in_two_InpLists('C', 'LED', SwitchC_InpLst, LED_PINNr_List) == False:
            return _ret
        if Read_LDR:
            if __No_Duplicates_in_two_InpLists('C', 'LDR', SwitchC_InpLst, LDR_Pin_Number, 'Set_LDR_Pin_Number()') == False:
                return _ret
        if __Check_CLK_a_RST_Pin_Usage('C', SwitchC_InpLst) == False:
            return _ret
            # 04.11.20:
        if __No_Duplicates_in_two_InpLists('C', 'SOUND', SwitchA_InpLst, Serial_PinLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _ret
            # 08.10.21: Juergen
    if SwitchD_InpCnt > 0:
        if __No_Duplicates_in_two_InpLists('D', 'LED', SwitchD_InpLst, LED_PINNr_List) == False:
            return _ret
        if Read_LDR:
            if __No_Duplicates_in_two_InpLists('D', 'LDR', SwitchD_InpLst, LDR_Pin_Number, 'Set_LDR_Pin_Number()') == False:
                return _ret
        if __Check_CLK_a_RST_Pin_Usage('D', SwitchD_InpLst) == False:
            return _ret
            # 04.11.20:
        if __No_Duplicates_in_two_InpLists('D', 'SOUND', SwitchA_InpLst, Serial_PinLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _ret
            # 08.10.21: Juergen
    _ret = True
    return _ret

def Init_HeaderFile_Generation_SW():
    
    global  __MaxUsed_Loc_InCh, Read_LDR, Store_Status_Enabled, __Use_WS2811, SwitchA_InpCnt, SwitchB_InpCnt,SwitchC_InpCnt
    global SwitchD_InpCnt,DMX_LedChan,Serial_PinLst,LED_PINNr_List,LDR_Pin_Number,SwitchA_InpLst,SwitchB_InpLst,SwitchC_InpLst,SwitchD_InpLst,CLK_Pin_Number,RST_Pin_Number,__DstVar_List, __MultiSet_DstVar_List
    global  __CTR_Channels_1, __CTR_Channels_2, __But_Inp_List_1,__But_Inp_List_2, __Channel1InpCnt, __Channel2InpCnt,__CTR_Cha_Name_1,__CTR_Cha_Name_2
    _ret = False
    #---------------------------------------------------------
    __MaxUsed_Loc_InCh = - 1
    Read_LDR = False
    Store_Status_Enabled = False
    __Use_WS2811 = False
    # The following variables are read from the data lines
    SwitchA_InpCnt = 0
    SwitchB_InpCnt = 0
    SwitchC_InpCnt = 0
    SwitchD_InpCnt = 0
    DMX_LedChan = - 1
    Serial_PinLst = ''
    LED_PINNr_List = M30.Get_Current_Platform_String('LED_Pins')
    LDR_Pin_Number = M30.Get_Current_Platform_String('LDR_Pin')
    SwitchA_InpLst = M30.Get_Current_Platform_String('SwitchA_Pins')
    SwitchB_InpLst = M30.Get_Current_Platform_String('SwitchB_Pins')
    SwitchC_InpLst = M30.Get_Current_Platform_String('SwitchC_Pins')
    SwitchD_InpLst = M30.Get_Current_Platform_String('SwitchD_Pins')
    CLK_Pin_Number = M30.Get_Current_Platform_String('CLK_Pin')
    RST_Pin_Number = M30.Get_Current_Platform_String('RST_Pin')
    __DstVar_List = ' '
    __MultiSet_DstVar_List = ' '
    if not __First_Scan_of_Data_Rows():
        return _ret
        # Scan the data rows and fill the variables above if the corrosponding functions are used in the Config__Col
    if __MultiSet_DstVar_List != ' ':
        if P01.MsgBox(M09.Get_Language_Str('Achtung: Die folgenden Zielvariablen werden mehrfach gesetzt:') + vbCr + __MultiSet_DstVar_List + vbCr + M09.Get_Language_Str('Senden zum Arduino abbrechen?'), vbQuestion + vbYesNo, M09.Get_Language_Str('Warnung: Mehrfach benutzte Zielvariablen')) == vbYes:
            return _ret
    if No_Duplicates_in_InpLists() == False:
        return _ret
    __CTR_Channels_1 = 0
    __CTR_Channels_2 = 0
    __But_Inp_List_1 = 'Unused'
    __But_Inp_List_2 = 'Unused'
    __Channel1InpCnt = 0
    __Channel2InpCnt = 0
    if SwitchB_InpCnt > 0 and SwitchC_InpCnt > 0:
        __CTR_Cha_Name_1 = 'SwitchB'
        __CTR_Cha_Name_2 = 'SwitchC'
        __CTR_Channels_1 = WorksheetFunction.RoundUp(SwitchB_InpCnt /  ( UBound(Split(SwitchB_InpLst, ' ')) + 1 ), 0)
        __CTR_Channels_2 = WorksheetFunction.RoundUp(SwitchC_InpCnt /  ( UBound(Split(SwitchC_InpLst, ' ')) + 1 ), 0)
        __But_Inp_List_1 = SwitchB_InpLst
        __But_Inp_List_2 = SwitchC_InpLst
        __Channel1InpCnt = SwitchB_InpCnt
        __Channel2InpCnt = SwitchC_InpCnt
    elif SwitchB_InpCnt > 0:
        __CTR_Cha_Name_1 = 'SwitchB'
        __CTR_Cha_Name_2 = 'Unused'
        __CTR_Channels_1 = WorksheetFunction.RoundUp(SwitchB_InpCnt /  ( UBound(Split(SwitchB_InpLst, ' ')) + 1 ), 0)
        __But_Inp_List_1 = SwitchB_InpLst
        __Channel1InpCnt = SwitchB_InpCnt
    elif SwitchC_InpCnt > 0:
        __CTR_Cha_Name_1 = 'SwitchC'
        __CTR_Cha_Name_2 = 'Unused'
        __CTR_Channels_1 = WorksheetFunction.RoundUp(SwitchC_InpCnt /  ( UBound(Split(SwitchC_InpLst, ' ')) + 1 ), 0)
        __But_Inp_List_1 = SwitchC_InpLst
        __Channel1InpCnt = SwitchC_InpCnt
    _ret = True
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def __Find_and_Select_Name(Name, UndefNr):
    UndefRow = int()
    #----------------------------------------------------------------------
    UndefRow = Split(Undef_Input_Var_Row, ' ')(UndefNr)
    P01.Cells(UndefRow, M25.Get_Address_Col()).Select()
    # VB2PY (UntranslatedCode) On Error Resume Next
    P01.Rows(UndefRow).Find(What= Name, LookIn= xlValues, LookAt= xlPart, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False).Activate()
    # VB2PY (UntranslatedCode) On Error GoTo 0

def Check_Detected_Variables():
    global __DstVar_List
    
    _ret = False
    #----------------------------------------------------
    # Check undefined input variables
    # ToDo:
    #  - Check unused or double written desination variables
    #  - Variablen müssen geschrieben werden bevor sie gelesen werden sonst wird eine Änderung nicht erkannt.
    #    Das ist eigentlich klar => In die Doku
    #
    M06.Undefined_Input_Var = Trim(M06.Undefined_Input_Var)
    if M06.Undefined_Input_Var != '':
        for UnDefVar in Split(M06.Undefined_Input_Var, ' '):
            Found = ( InStr(M06.InChTxt, ' ' + UnDefVar + ' ') != 0 )                
            if not Found:
                Found = ( InStr(__DstVar_List, UnDefVar) != 0 )
            if not Found and UnDefVar == '[Multiplexer]':
                Found = True
                # Added by Misha 30-5-2020.  ' 14.06.20: Added from Mishas version
            if not Found:
                __Find_and_Select_Name(UnDefVar, UndefNr)
                P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Die Variable \'#1#\' wird als Eingang benutzt, wird aber nirgendwo gesetzt.'), "#1#", UnDefVar), vbCritical, M09.Get_Language_Str('Fehler: Undefinierter Zustand eine Eingangsvariablen'))
                return _ret
            UndefNr = UndefNr + 1
    _ret = True
    return _ret

# VB2PY (UntranslatedCode) Option Explicit
