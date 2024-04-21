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
# 12.02.23: Hardi
# List of alias names generated with the "// Define Input(" function

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
import mlpyproggen.Prog_Generator as PG
import ExcelAPI.XLWF_Worksheetfunction as WorksheetFunction
import proggen.clsExtensionParameter

import ExcelAPI.XLA_Application as P01

DstVar_List = String()
MultiSet_DstVar_List = String()
StoreVar_List = String()
MaxUsed_Loc_InCh = Long()
MaxUsed_Loc_InCh_Row = Long()
SwitchA_InpCnt = Long()
SwitchB_InpCnt = Long()
SwitchC_InpCnt = Long()
SwitchD_InpCnt = Long()
SwitchA_InpLst = String()
SwitchB_InpLst = String()
SwitchC_InpLst = String()
SwitchD_InpLst = String()
CLK_Pin_Number = String()
RST_Pin_Number = String()
LDR_Pin_Number = String()
Serial_PinLst = String()
DMX_LedChan = Long()
CTR_Channels_1 = Long()
CTR_Channels_2 = Long()
Channel1InpCnt = Long()
Channel2InpCnt = Long()
CTR_Cha_Name_1 = String()
CTR_Cha_Name_2 = String()
But_Inp_List_1 = String()
But_Inp_List_2 = String()
LED_PINNr_List = String()
Read_LDR = Boolean()
Use_WS2811 = Boolean()
Store_Status_Enabled = Boolean()
Switch_Damping_Fact = String()
USE_ATTiny_CAN_GBM = Boolean()
ATTINY_GBM_CHECK_ERROR = Boolean()
ATTINY_GBM_SW_Filter = String()
Alias_Names_List = String()

def PIN_A3_Is_Used():
    global RST_Pin_Number
    _fn_return_value = False
    #------------------------------------------
    if Channel1InpCnt > 0 and RST_Pin_Number == 'A3':
        _fn_return_value = True
    return _fn_return_value

def Add_Logic_InpVars(LogicExp, r):
    _fn_return_value = False
    Arglist = vbObjectInitialize(objtype=String)

    Arg = Variant()
    #---------------------------------------------------------------------------
    Arglist = M30.SplitEx(LogicExp, True, 'OR', 'AND', 'NOT')
    for Arg in Arglist:
        Arg = Trim(Arg)
        if Arg != '':
            if Valid_Var_Name_and_Skip_InCh_and_Numbers(Arg, r) == False:
                return _fn_return_value
                # Skip special names like '#InCh' and Numbers
    _fn_return_value = True
    return _fn_return_value

def Check_if_all_Variables_in_sequece_of_N_exists(r, N):
    _fn_return_value = False
    TxtLen = 0
    Adr_or_Name = String()
    #----------------------------------------------------------------------------------------------
    Adr_or_Name = Trim(P01.Cells(r, M25.Get_Address_Col()))
    if Adr_or_Name == '':
        P01.Cells(r, M25.Get_Address_Col()).Select()
        P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: In Zeile #1# ist keine Adresse, kein Schalter oder keine Variable eingetragen'), "#1#", str(r)), vbCritical, Replace(M09.Get_Language_Str('Kein Eintrag in \'#1#\' Spalte'), "#1#", M25.Get_Address_String(M02.Header_Row)))
        return _fn_return_value
    if not IsNumeric(Split(Adr_or_Name, ' ')(0)):
        Adr_or_Name = M06.ExpandName(Adr_or_Name)
        Nr,TxtLen = Get_Nr_From_Var(Adr_or_Name, TxtLen)
        if Nr >= 0:
            Name = Left(Adr_or_Name, TxtLen)
            for i in vbForRange(Nr, Nr + N - 1):
                if Valid_Var_Name(Name + str(i), r) == False:
                    return _fn_return_value
                    # At the moment Valid_Var_Name always returns true
    _fn_return_value = True
    return _fn_return_value

def Get_Bin_Inputs(Dec_Cnt):
    _fn_return_value = ""
    #-----------------------------------------------
    if Dec_Cnt <= 0:
        _fn_return_value = - 1
    elif Dec_Cnt <= 1:
        _fn_return_value = 1
    elif Dec_Cnt <= 3:
        _fn_return_value = 2
    elif Dec_Cnt <= 7:
        _fn_return_value = 3
    elif Dec_Cnt <= 15:
        _fn_return_value = 4
    elif Dec_Cnt <= 31:
        _fn_return_value = 5
    elif Dec_Cnt <= 63:
        _fn_return_value = 6
    else:
        _fn_return_value = - 1
    return _fn_return_value

def Check_if_all_Variables_in_sequece_exist(r, Ctr_Name, N_Str):
    _fn_return_value = False
    n = Long()
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
        n = Get_Bin_Inputs(P01.val(N_Str))
        if n <= 0:
            P01.MsgBox(M09.Get_Language_Str('Fehler: Anzahl der binären Zustände ungültig. Die Anzahl muss zwischen 1 und 63 liegen'), vbCritical, M09.Get_Language_Str('Anzahl der binären Zustände ungültig'))
            return _fn_return_value
    else:
        n = P01.val(N_Str)
    _fn_return_value = Check_if_all_Variables_in_sequece_of_N_exists(r, n)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: MacroName - ByVal 
def Add_InpVars(MacroName, Org_Macro, Filled_Macro, r, Org_Macro_Row):
    _fn_return_value = False
    Second_Input_Names = 'InCh R_InCh InReset InCh2'

    Arg_List = vbObjectInitialize(objtype=String)

    Fil_List = vbObjectInitialize(objtype=String)

    ArgNr = Long()

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
    Arg_List = Get_Arguments(Org_Macro)
    Fil_List = Get_Arguments(Filled_Macro)
    _select0 = MacroName
    if (_select0 == 'Logic'):
        if UBound(Fil_List) != 1:
            P01.Cells(r, M25.Config__Col).Select()
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Falsche Parameter Anzahl in \'Logic()\' Ausdruck: \'#1#\''), "#1#", Filled_Macro), vbCritical, M09.Get_Language_Str('Fehler: \'Logic()\' Ausdruck ist ungültig'))
            return _fn_return_value
        _fn_return_value = Add_Logic_InpVars(Fil_List(1), r)
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
                    if Valid_Var_Name_and_Skip_InCh_and_Numbers(Fil_List(ArgNr), r) == False:
                        return _fn_return_value
        if Pos_CounterVar >= 0:
            # Macro like "InCh_to_TmpVar(InCh, InCh_Cnt)"
            if Check_if_all_Variables_in_sequece_exist(r, Arg_List(Pos_CounterVar), Fil_List(Pos_CounterVar)) == False:
                return _fn_return_value
        else:
            # Check if there is a number in column "InCnt" and all arguments have been found
            InCntStr = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH).Cells(Org_Macro_Row, M02.SM_InCnt_COL)
            if InCntStr != '':
                # 14.05.20:
                if IsNumeric(InCntStr):
                    if Det_Cnt != P01.val(InCntStr):
                        # Not all arguments detected
                        # It's a function like: "EntrySignal3_RGB(LED, InCh)"
                        # => Check if all Variable in the sequece exist: <Name>1..<Name><InCntStr>
                        if Check_if_all_Variables_in_sequece_of_N_exists(r, P01.val(InCntStr)) == False:
                            return _fn_return_value
                if IsNumeric(Left(InCntStr, Len(InCntStr) - 1)) and Right(InCntStr, 1) == '?':
                    #ToDo Zusätzliche Überprüfung auf "#InCh+2" wenn 3? in Lib_Macros hinzugefügt wird
                    if Fil_List(2) == '#InCh+1':
                        # 07.06.20:
                        # It's a function which may use two inputs like: "RS_FlipFlop(Test, #InCh, #InCh+1)"
                        # => Check if all Variable in the sequece exist: <Name>1..<Name><InCntStr>
                        if Check_if_all_Variables_in_sequece_of_N_exists(r, P01.val(InCntStr)) == False:
                            return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

def Is_Switch_Var_then_Add_to_Ctr(Var_Name):
    global SwitchA_InpCnt,SwitchB_InpCnt,SwitchC_InpCnt,SwitchD_InpCnt
    _fn_return_value = False
    Nr = Long()
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
        _fn_return_value = 1
    elif (_select1 == - 1):
        P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Die Nummer der Variable \'#1#\' ist ungültig!' + vbCr + vbCr + 'Gültiger Bereich: #2#'), "#1#", Var_Name), '#2#', '1..250'), vbCritical, M09.Get_Language_Str('Fehler: Ungültige Variable'))
        _fn_return_value = - 1
    return _fn_return_value

def First_Scan_of_Data_Rows():
    
    global Switch_Damping_Fact, DMX_LedChan,Read_LDR,Store_Status_Enabled,Use_WS2811, SwitchA_InpLst, SwitchB_InpLst, SwitchC_InpLst, SwitchD_InpLst, CLK_Pin_Number, RST_Pin_Number, LDR_Pin_Number, LED_PINNr_List, DMX_LedChan,Read_LDR, USE_ATTiny_CAN_GBM
    
    _fn_return_value = False
    r = Long()

    Var_COL = Long()
    # 04.04.20:
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
            if Is_Switch_Var_then_Add_to_Ctr(Var_Name) == - 1:
                P01.Cells(r, Var_COL).Select()
                return _fn_return_value
            Config_Entry = P01.Cells(r, M25.Config__Col)
            if Trim(Config_Entry) != '':
                for line in Split(Config_Entry, vbLf):
                    line = Trim(line)
                    fret, SwitchA_InpLst = Set_PinNrLst_if_Matching(line, '// Set_SwitchA_InpLst(', SwitchA_InpLst, 'A', 5)
                    if fret == False:
                        return _fn_return_value
                    fret, SwitchB_InpLst = Set_PinNrLst_if_Matching(line, '// Set_SwitchB_InpLst(', SwitchB_InpLst, 'I', 12) 
                    if fret == False:
                        return _fn_return_value
                    fret, SwitchC_InpLst = Set_PinNrLst_if_Matching(line, '// Set_SwitchC_InpLst(', SwitchC_InpLst, 'I', 12)
                    if fret == False:
                        return _fn_return_value
                    fret, SwitchD_InpLst = Set_PinNrLst_if_Matching(line, '// Set_SwitchD_InpLst(', SwitchD_InpLst, 'Pu', 12)
                    if fret == False:
                        return _fn_return_value
                    fret, CLK_Pin_Number = Set_PinNrLst_if_Matching(line, '// Set_CLK_Pin_Number(', CLK_Pin_Number, 'O', 1)
                    if fret == False:
                        return _fn_return_value
                    fret, RST_Pin_Number = Set_PinNrLst_if_Matching(line, '// Set_RST_Pin_Number(', RST_Pin_Number, 'O', 1)
                    if fret == False:
                        return _fn_return_value
                    fret, LDR_Pin_Number = Set_PinNrLst_if_Matching(line, '// Set_LDR_Pin_Number(', LDR_Pin_Number, 'A', 1)
                    if fret == False:
                        return _fn_return_value
                    fret, LED_PINNr_List = Set_PinNrLst_if_Matching(line, '// Set_LED_OutpPinLst(', LED_PINNr_List, 'OV', M02.LED_CHANNELS)  # 18.02.22 Juergen Virtual Channel
                    if fret == False:
                        return _fn_return_value
                    # 18.02.22 Juergen Virtual Channel
                    if line == '// Use_DMX512()':
                        # 19.01.21 Juergen
                        DMX_LedChan = P01.val(P01.Cells(r, M25.LED_Cha_Col))
                    if line == '#define READ_LDR':
                        Read_LDR = True
                    if Left(line, Len('#define SWITCH_DAMPING_FACT')) == '#define SWITCH_DAMPING_FACT':
                        Switch_Damping_Fact = line
                    if line == '#define USE_WS2811':
                        Use_WS2811 = True
                        # 19.01.21 Juergen
                    if line == '#define ENABLE_STORE_STATUS':
                        Store_Status_Enabled = True
                        #    "
                    if line == '#define USE_ATTiny_CAN_GBM':
                        USE_ATTiny_CAN_GBM = True   # Must be located at the beginning of the configuration
                        # 12.02.23: Hardi                    
                    if Add_Inp_and_DstVars(line, r) == False:
                        return _fn_return_value
                        # Add the destination variable to DstVar_List
    _fn_return_value = True
    return _fn_return_value

def Test():
    Debug.Print(Replace('Aber    Hallo', '  ', ' '))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sw_List - ByVal 
def Check_one_Switch_Lists_for_SPI_Pins(Sw_List):
    _fn_return_value = False
    Pin = Variant()
    #---------------------------------------------------------------------------------------
    Sw_List = ' ' + Sw_List + ' '
    for Pin in Split('10 11 12', ' '):
        if InStr(Sw_List, ' ' + Pin + ' ') > 0:
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Der Arduino Pin \'#1#\' kann nicht als Ein- oder Ausgang werden wenn ' + 'DCC oder Selectrix Daten per SPI Bus gelesen werden. Es muss ein anderer Anschluss verwendet ' + 'werden oder die SPI Kommunikation in der \'Config\' Seite deaktiviert werden.' + vbLf + 'Achtung: Die beiden Arduinos müssen dann per RS232 verbunden sein.'), "#1#", Pin), vbCritical, 'Fehler: Ungültiger Arduino Pin erkannt')
            return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

def Check_Switch_Lists_for_SPI_Pins():
    global SwitchA_InpCnt, SwitchB_InpCnt, SwitchC_InpCnt, SwitchD_InpCnt,SwitchA_InpLst,SwitchB_InpLst,SwitchC_InpLst,SwitchD_InpLst
    _fn_return_value = False
    #-----------------------------------------------------------
    if SwitchA_InpCnt > 0:
        if Check_one_Switch_Lists_for_SPI_Pins(SwitchA_InpLst) == False:
            return _fn_return_value
    if SwitchB_InpCnt > 0:
        if Check_one_Switch_Lists_for_SPI_Pins(SwitchB_InpLst) == False:
            return _fn_return_value
    if SwitchC_InpCnt > 0:
        if Check_one_Switch_Lists_for_SPI_Pins(SwitchC_InpLst) == False:
            return _fn_return_value
    if SwitchD_InpCnt > 0:
        if Check_one_Switch_Lists_for_SPI_Pins(SwitchD_InpLst) == False:
            return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Dest_InpLst - ByRef 
def Set_PinNrLst_if_Matching(line, Name, Dest_InpLst, PinTyp, MaxCnt):
    _fn_return_value = False
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
        if PinTyp == 'I' or PinTyp == 'O' or PinTyp == 'OV' or PinTyp == 'Pu':
            # 18.02.22: Juergen add virtual Channel
            SPI_Pins = M30.Get_Current_Platform_String('SPI_Pins')
            # ~08.10.21: Juergen: New function to handle the valid pins. Prior this was handled here
    ValidPins = M30.Get_Current_Platform_String(PinTyp + '_Pins', True)
    # ~08.10.21: Juergen:    "
    ValidPins = SPI_Pins + ValidPins
    if Left(line, Len(Name)) == Name:
        p = InStr(line, ')')
        if p == 0:
            # VB2PY (UntranslatedCode) GoTo PrintError
            #P01.MsgBox(Replace(M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern in Zeile:' + vbCr + '  \'#1#\''), "#1#", line), vbCritical, M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern'))
            #return _fn_return_value, Dest_InpLst            
            pass
        NrStr = Mid(line, 1 + Len(Name), p - 1 - Len(Name))
        NrStr = Trim(Replace(NrStr, ',', ' '))
        NrStr = Replace(NrStr, '  ', ' ')
        if NrStr == '':
            # VB2PY (UntranslatedCode) GoTo PrintError
            #P01.MsgBox(Replace(M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern in Zeile:' + vbCr + '  \'#1#\''), "#1#", line), vbCritical, M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern'))
            #return _fn_return_value, Dest_InpLst            
            pass
        NrArr = Split(NrStr, ' ')
        if UBound(NrArr) + 1 > MaxCnt:
            # VB2PY (UntranslatedCode) GoTo PrintError
            #P01.MsgBox(Replace(M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern in Zeile:' + vbCr + '  \'#1#\''), "#1#", line), vbCritical, M09.Get_Language_Str('Fehler beim Lesen der Pin Nummern'))
            #return _fn_return_value, Dest_InpLst            
            pass
        # Check if valid pins names / numbers are used
        NrStr = ''
        for OnePin in NrArr:
            if InStr(ValidPins, ' ' + M30.AliasToPin(OnePin) + ' ') == 0:
                P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Der Pin \'#1#\' ist nicht gültig im' + vbCr + '  \'#2#\' Befehl'), "#1#", OnePin), '#2#', Replace(line, '// ', '')), vbCritical, M09.Get_Language_Str('Ungültige Arduino Pin Nummer'))
                return _fn_return_value, Dest_InpLst
            # Check Duplicate Pins , not for virtual PIN 'V' - virtual pin may be used multiple times
            if OnePin != M09.Virtual_Channel_T:
                #p = InStr(" " & line & " ", " " & AliasToPin(OnePin) & " ")
                # 14.10.21: Juergen, 16.05.20: Added space around OnePin (Problem: 2 ... 12)
                p = InStr(' ' + Replace(Replace(line, '(', ' '), ')', ' ') + ' ', ' ' + OnePin + ' ')
                # 17.02.22: Juergen, fix a bug
                if InStr(p + 1, ' ' + line + ' ', ' ' + OnePin + ' ') > 0:
                    P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Der Pin \'#1#\' wird mehrfach verwendet im' + vbCr + '  \'#2#\' Befehl'), "#1#", OnePin), '#2#', Replace(line, '// ', '')), vbCritical, M09.Get_Language_Str('Mehrfach verwendeter Arduino Pin'))
                    return _fn_return_value, Dest_InpLst
                if NrStr != '':
                    NrStr = NrStr + ' '
            # 14.10.21: Juergen
            NrStr = NrStr + M30.AliasToPin(OnePin)
            # build a new list with logical names mapped to physical pins
        Dest_InpLst = NrStr
    _fn_return_value = True
    if NrStr != '':
        Debug.Print('Set_PinNrLst_if_Matching(' + Name + '=' + NrStr + ')')
        # Debug
    return _fn_return_value, Dest_InpLst
    

def Get_Arguments(line):
    _fn_return_value = ""
    Arguments = String()

    Parts = vbObjectInitialize(objtype=String)

    i = Long()

    p = Long()
    #---------------------------------------------------------
    if InStr(line, '(') == 0:
        P01.MsgBox('Error: Opening bracket not found in \'' + line + '\'', vbCritical, 'Internal Error')
        return _fn_return_value
    Arguments = Split(line, '(')(1)
    p = InStrRev(Arguments, ')')
    if p == 0:
        P01.MsgBox('Error: Closing bracket not found in \'' + line + '\'', vbCritical, 'Internal Error')
        return _fn_return_value
    Arguments = Left(Arguments, p - 1)
    Parts = Split(Arguments, ',')
    for i in vbForRange(0, UBound(Parts)):
        Parts[i] = Trim(Parts(i))
    _fn_return_value = Parts
    return _fn_return_value

def Test_Get_Arguments():
    Res = vbObjectInitialize(objtype=String)
    #UT-----------------------------
    Res = Get_Arguments('Test( A, b, c)')

def Get_Matching_Arg(Org_Macro, line, DestVarName):
    _fn_return_value = ""
    Org_Args = vbObjectInitialize(objtype=String)

    Act_Args = vbObjectInitialize(objtype=String)
    #------------------------------------------------------------------------------------------------------
    # Return the argument in "Line" which matches DestVarName in Org_Macro
    Org_Args = Get_Arguments(Org_Macro)
    if M30.isInitialised(Org_Args):
        Act_Args = Get_Arguments(line)
        if M30.isInitialised(Act_Args):
            if UBound(Act_Args) >= UBound(Org_Args):
                # Org_Args may contain ... => the number of Act_Args may be greater
                new_i=-1 #*HL simulation of loopvar change
                for i in vbForRange(0, UBound(Org_Args)):
                    if i>new_i:
                        if Org_Args(i) == DestVarName:
                            _select3 = DestVarName
                            if (_select3 == '...') or (_select3 == 'OutList'):
                                while i <= UBound(Act_Args):
                                    _fn_return_value = _fn_return_value + Act_Args(i) + ','
                                    new_i = i + 1
                                _fn_return_value = M30.DelLast(_fn_return_value)
                            else:
                                _fn_return_value = Act_Args(i)
                            _fn_return_value = M06.ExpandName(_fn_return_value)
                            return _fn_return_value
    P01.MsgBox(Replace(M09.Get_Language_Str('Fehler bei der Erkennung der Zielvariable in Makro \'#1#\''), "#1#", line), vbCritical, M09.Get_Language_Str('Fehler: Zielvariable wurde nicht gefunden'))
    return _fn_return_value

def Test_Get_Matching_Arg():
    #UT--------------------------------
    Debug.Print(Get_Matching_Arg('Random(        DstVar, InCh, RandMode, MinTime, MaxTime, MinOn, MaxOn)', 'Random( OutA, 1, 2, 3, 4, 5, 6)', 'DstVar'))
    Debug.Print(Get_Matching_Arg('Counter(       CtrMode, InCh, Enable, TimeOut, ...)', 'Counter(12, #InCh, Enable, TimeOut, OutA, OutB, OutB)', '...'))
    Debug.Print(Get_Matching_Arg('RandMux(       DstVar1, DstVarN, InCh, RandMode, MinTime, MaxTime)', 'RandMux( Out1, Out10, InCh, RandMode, MinTime, MaxTime)', 'DstVarN'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: VarName - ByVal 
def Add_Variable_to_DstVar_List(VarName):
    global DstVar_List,MultiSet_DstVar_List
    
    _fn_return_value = False
    Check = String()
    #-------------------------------------------------------------------------------
    Check = ' ' + VarName + ' '
    if InStr(DstVar_List, Check) == 0:
        DstVar_List = DstVar_List + VarName + ' '
    else:
        if InStr(MultiSet_DstVar_List, Check) == 0:
            MultiSet_DstVar_List = MultiSet_DstVar_List + VarName + ' '
    _fn_return_value = True
    return _fn_return_value

def Add_Matching_Arg_to_DstVars(Org_Macro, line, DestVarName):
    _fn_return_value = False
    Arg = String()
    #------------------------------------------------------------------------------------------------------------------
    # Locate DestVarName in Org_Macro and add the corrosponding
    # argument to the global string DstVar_List
    # Example:
    #   MonoFlop(DstVar, InCh, Duration)
    #   RS_FlipFlop2(DstVar1, DstVar2, InCh, R_InCh)             Called 2 times
    Arg = Get_Matching_Arg(Org_Macro, line, DestVarName)
    if Arg != '':
        if Arg == '#LocInCh':
            # 20.06.20: Prevent problems with the random goto activation: Random(#LocInCh, #InCh, RM_NORMAL, 5 Sek,  10 Sek, 1 ms, 1 ms)
            _fn_return_value = True
        else:
            _fn_return_value = Add_Variable_to_DstVar_List(Arg)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: VarName - ByVal 
def Add_Variable_to_StoreVar_List(VarName):
    global StoreVar_List
    _fn_return_value = False
    Check = String()
    # 01.05.20: Jürgen
    #--------------------------------------------------------------------------------
    Check = ' ' + VarName + ' '
    if InStr(StoreVar_List, Check) == 0:
        StoreVar_List = StoreVar_List + VarName + ' '
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: VarName - ByVal 
def StoreVar_List_Present(VarName):
    _fn_return_value = False
    Check = String()
    # 01.05.20: Jürgen
    #------------------------------------------------------------------------
    Check = ' ' + VarName + ' '
    _fn_return_value = InStr(StoreVar_List, Check) != 0
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: TxtLen - ByRef 
def Get_Nr_From_Var(Name, TxtLen):
    _fn_return_value = 0
    p = Long()
    # 27.12.20:
    #-----------------------------------------------------------------------------
    _fn_return_value = - 1
    p = Len(Name)
    while p > 0 and InStr('0123456789', Mid(Name, p, 1)) > 0:
        p = p - 1
    if p > 0:
        p = p + 1
        TxtLen = p - 1
        if IsNumeric(Mid(Name, p)):
            _fn_return_value = P01.val(Mid(Name, p))
        else:
            _fn_return_value = - 2
    return _fn_return_value,TxtLen

def Add_N2_Arg_to_DstVars(Org_Macro, line):
    _fn_return_value = False
    Arg1 = String()

    ArgN = String()

    TxtLen1 = Long()

    TxtLenN = Long()
    #-------------------------------------------------------------------------------------
    # Example: RandMux(DstVar1, DstVarN, InCh, RandMode, MinTime, MaxTime)
    Arg1 = Get_Matching_Arg(Org_Macro, line, 'DstVar1')
    if Arg1 != '':
        ArgN = Get_Matching_Arg(Org_Macro, line, 'DstVarN')
        if ArgN != '':
            StartNr,TxtLen1 = Get_Nr_From_Var(Arg1, TxtLen1)
            if StartNr < 0:
                return _fn_return_value
            EndNr, TxtLenN = Get_Nr_From_Var(ArgN, TxtLenN)
            if EndNr < 0:
                return _fn_return_value
            if TxtLen1 != TxtLenN or Left(Arg1, TxtLen1) != Left(ArgN, TxtLenN):
                return _fn_return_value
            for i in vbForRange(StartNr, EndNr):
                if Add_Variable_to_DstVar_List(Left(Arg1, TxtLen1) + str(i)) == False:
                    return _fn_return_value
            _fn_return_value = True
    return _fn_return_value

def Add_VarArgCnt_to_DstVars(Org_Macro, line):
    _fn_return_value = False
    Arg = String()
    #----------------------------------------------------------------------------------------
    # Example: Counter(CtrMode, InCh, Enable, TimeOut, ...)
    # 20.06.20:
    if Left(Org_Macro, Len('Counter(')) == 'Counter(':
        # If the LED output is disabled the first DestVar contains the destination
        if InStr(line, 'CF_ONLY_LOCALVAR') > 0:
            # count (Counter => 0 .. n-1)
            _fn_return_value = True
            # => There are no Dest vars ==> We don't have to add them
            return _fn_return_value
    Arg = Get_Matching_Arg(Org_Macro, line, 'OutList')
    # Old: "...")
    if Arg != '':
        for _idx0 in Split(Arg, ','):
            proggen.clsExtensionParameter.Name = _idx0
            if not Add_Variable_to_DstVar_List(proggen.clsExtensionParameter.Name):
                return _fn_return_value
        _fn_return_value = True
    return _fn_return_value

def Add_Cx_to_DstVars(Org_Macro, line, cnt, r):
    _fn_return_value = False
    Arg1 = String()

    TxtLen = Long()
    #---------------------------------------------------------------------------------------------------------
    # Example: PushButton_w_LED_0_2(B_LED, B_LED_Cx, InCh, DstVar1, Rotate, Timeout)
    Arg1 = Get_Matching_Arg(Org_Macro, line, 'DstVar1')
    if Arg1 != '':
        StartNr, TxtLen = Get_Nr_From_Var(Arg1, TxtLen)
        if StartNr < 0:
            P01.MsgBox(Replace(Replace(Replace(M09.Get_Language_Str('Fehler: Die Zielvariable \'#1#\' in Zeile #2# muss eine Zahl am Ende haben ' + 'weil sie Teil einer Sequenz ist.' + vbCr + '  Beispiel: #3#'), "#1#", Arg1), '#2#', r), '#3#', Arg1 + '0'), vbCritical, M09.Get_Language_Str('Fehler: Zielvariable ungültig für Sequenz'))
            return _fn_return_value
        EndNr = StartNr + cnt - 1
        for i in vbForRange(StartNr, EndNr):
            if Add_Variable_to_DstVar_List(Left(Arg1, TxtLen) + str(i)) == False:
                return _fn_return_value
        _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Line - ByVal 
def Add_Inp_and_DstVars(line, r):
    _fn_return_value = ""
    Parts = vbObjectInitialize(objtype=String)

    p = Long()

    Org_Macro_Row = Long()

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
    _fn_return_value = True
    if InStr(line, '(') == 0:
        return _fn_return_value
    Parts = Split(line, '(')
    Arguments = Parts(1)
    p = InStrRev(Arguments, ')')
    if p == 0:
        return _fn_return_value
    if Parts(0) == 'HouseT':
        SearchMacro = 'House'
    else:
        SearchMacro = Parts(0)
    Org_Macro_Row = M09SM.Find_Macro_in_Lib_Macros_Sheet(SearchMacro + '(')
    if Org_Macro_Row == 0:
        Debug.Print('Attention: Macro \'' + line + ' not found in \'' + M02.LIBMACROS_SH + '\'')
        # ToDo: Wie können Zielvariablen in diesen Makros erkannt werden?
    else:
        _with0 = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
        OutCntStr = _with0.Cells(Org_Macro_Row, M02.SM_OutCntCOL)
        Org_Macro = _with0.Cells(Org_Macro_Row, M02.SM_Macro_COL)
        if Add_InpVars(Parts(0), Org_Macro, line, r, Org_Macro_Row) == False:
            _fn_return_value = False
            return _fn_return_value
        _select4 = OutCntStr
        if (_select4 == '') or (_select4 == '0'):
            _fn_return_value = True
            return _fn_return_value
        elif (_select4 == '1'):
            Res = Add_Matching_Arg_to_DstVars(Org_Macro, line, 'DstVar')
            # Ex.: MonoFlop(DstVar, InCh, Duration)
        elif (_select42 == '2'):
            Res = Add_Matching_Arg_to_DstVars(Org_Macro, line, 'DstVar1')
            # Ex.: RS_FlipFlop2(DstVar1, DstVar2, InCh, R_InCh)
            if Res:
                Res = Add_Matching_Arg_to_DstVars(Org_Macro, line, 'DstVar2')
        elif (_select4 == 'n..'):
            Res = Add_VarArgCnt_to_DstVars(Org_Macro, line)
            # Ex.: Counter(CtrMode, InCh, Enable, TimeOut, ...)
        elif (_select4 == 'n2'):
            Res = Add_N2_Arg_to_DstVars(Org_Macro, line)
            # Ex.: RandMux(DstVar1, DstVarN, InCh, RandMode, MinTime, MaxTime)
        else:
            # Other Output Count entries
            if Left(OutCntStr, 1) == 'C':
                # C1, C2, .. Cn                             Ex.: PushButton_w_LED_0_2(B_LED, B_LED_Cx, InCh, DstVar1, Rotate, Timeout)
                if IsNumeric(Mid(OutCntStr, 2)):
                    Res = Add_Cx_to_DstVars(Org_Macro, line, P01.val(Mid(OutCntStr, 2)), r)
            else:
                P01.MsgBox('Internal Error: Undefined OutCnt entry \'' + OutCntStr + '\' in row ' + str(Org_Macro_Row) + ' in sheet \'' + M02.LIBMACROS_SH + '\'', vbCritical, 'Internal Error')
                return _fn_return_value
        if Res == False:
            P01.Cells(r, M25.Config__Col).Select()
            P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler in der Definition der Zielvariable(n): \'#1#\' in Zeile #2#'), "#1#", line), '#2#', r), vbCritical, M09.Get_Language_Str('Fehler in Makro Definition'))
            _fn_return_value = False
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel - ByRef 
def Print_DstVar_List(fp, Channel,Min_Channel):
    global DstVar_List
    
    Var = Variant()
    #-----------------------------------------------------------------
    start_channel = Channel
    
    rm_number = start_channel - Min_Channel #+List_Lenght(DstVar_List)-1
    
    for Var in Split(Trim(DstVar_List), ' '):
        VBFiles.writeText(fp, '#define ' + M30.AddSpaceToLen(Var, 22) + '  ' + M30.AddSpaceToLen(str(Channel), 41) + '// Z21-RM-Rückmelder: Adresse:' + str(int(rm_number/8)+1) + " Eingang:" + str(int(rm_number%8)+1), '\n')
        Channel = Channel + 1
        rm_number = rm_number + 1
        
    return Channel

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Count - ByVal 
def To_Eight(Count):
    _fn_return_value = False
    # 21.03.23 Juergen
    _fn_return_value = Int(( Count + 7 )  / 8) * 8
    return _fn_return_value

def List_Lenght(List):
    _fn_return_value = False
    Var = Variant()
    # 21.03.23 Juergen
    #-----------------------------------------------------------------
    _fn_return_value = 0
    for Var in Split(Trim(List), ' '):
        _fn_return_value = _fn_return_value + 1
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ExpectedName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Nr - ByRef 
def Is_in_Nr_String(Name, ExpectedName, MinNr, MaxNr, Nr):
    _fn_return_value = 0
    SkipCnt = Long()
    #------------------------------------------------------------------------------------------------------------------------------------------
    # Check if "Name" starts with "ExpectedName" and has a tailing number in the range form MinNr to MaxNr
    while Right(ExpectedName, 1) == '?':
        SkipCnt = SkipCnt + 1
        ExpectedName = M30.DelLast(ExpectedName)
    if Left(Name, Len(ExpectedName)) == ExpectedName:
        NrStr = Mid(Name, 1 + Len(ExpectedName) + SkipCnt)
        if IsNumeric(NrStr):
            if Left(NrStr, 1) == '0':
                return _fn_return_value
                # Leading 0 are not allowed because they generate the same number
            WrongChar = '-+.,eE'
            for i in vbForRange(1, Len(WrongChar)):
                if InStr(NrStr, Mid(WrongChar, i, 1)) > 0:
                    return _fn_return_value
            Nr = P01.val(NrStr)
            if Nr >= MinNr and Nr <= MaxNr:
                _fn_return_value = 1
            else:
                _fn_return_value = - 1
                # Exists, but invalide number
    return _fn_return_value, Nr

def Test_Is_in_Nr_String():
    Nr = Long()
    #UT-------------------------------
    Debug.Print('Is_in_Nr_String=' + Is_in_Nr_String('HalloAB13', 'Hallo??', 1, 200, Nr))

def Error_Msg_Varaible_Not_Defined(VarName, r):
    # 03.04.20:
    #-----------------------------------------------------------------------
    P01.Cells(r, M25.Get_Address_Col()).Select()
    P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Die Variable \'#1#\' in Zeile #2# ist nicht definiert'), "#1#", VarName), '#2#', r), vbCritical, M09.Get_Language_Str('Fehler: Undefinierte Variable'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def Valid_Var_Name(Name, row):
    global MaxUsed_Loc_InCh, MaxUsed_Loc_InCh_Row, Undefined_Input_Var, Undef_Input_Var_Row, DstVar_List
    
    _fn_return_value = False
    Std_Names = 'SI_1 SI_0 SI_Enable_Sound #LocInCh'

    Nr = Long()

    Std_N = Variant()
    # 03.04.20:
    #---------------------------------------------------------------------------
    # Check if it's a valid variable (Switch<Nr>, Button<Nr>, INCH_DCC_..., LOC_INCH<Nr>, ...)
    # 20.06.20: Added: "#LocInCh" to prevent problems with the Goto activation Random which uses "Counter(CF_ONLY_LOCALVAR | CF_ROTATE | CF_SKIP0, #LocInCh, #InCh, 0 Sec, 2)"
    _fn_return_value = True
    for Std_N in Split(Std_Names, ' '):
        if Name == Std_N:
            return _fn_return_value
    _select5 = Is_Switch_Var_then_Add_to_Ctr(Name)
    if (_select5 == 1):
        return _fn_return_value
    elif (_select5 == - 1):
        _fn_return_value = False
        P01.Cells(row, M25.Config__Col).Select()
        return _fn_return_value
    if InStr(DstVar_List, ' ' + Name + ' '):
        return _fn_return_value
    if InStr(M06.InChTxt, '#define ' + Name + ' ') > 0:
        return _fn_return_value
    _select6, Nr = Is_in_Nr_String(Name, 'LOC_INCH', 0, 250, Nr)
    if (_select6 == 1):
        # Valid Number
        if Nr > MaxUsed_Loc_InCh:
            MaxUsed_Loc_InCh = Nr
            # The "LOC_INCH" are checked later because they are not generated at this time
            MaxUsed_Loc_InCh_Row = row
        return _fn_return_value
    elif (_select6 == - 1):
        P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Die Nummer der Variable \'#1#\' ist ungültig!' + vbCr + vbCr + 'Gültiger Bereich: #2#'), "#1#", Name), '#2#', '0..250'), vbCritical, M09.Get_Language_Str('Fehler: Ungültige Variable'))
    if USE_ATTiny_CAN_GBM:
        # "#define USE_ATTiny_CAN_GBM" Must be located at the beginning of the configuration
        #  13.02.23: Hardi
        if Left(Name, Len('RM ')) == 'RM ':
            return _fn_return_value
    # Old:
    #  Error_Msg_Varaible_Not_Defined Name, Row
    #  Valid_Var_Name = False
    # Add the undefined input variable to a list which is checked later
    if InStr(M06.Undefined_Input_Var, ' ' + Name + ' ') == 0:
        M06.Undefined_Input_Var = M06.Undefined_Input_Var + Name + ' '
        M06.Undef_Input_Var_Row = M06.Undef_Input_Var_Row + str(row) + ' '
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Arg - ByVal 
def Valid_Var_Name_and_Skip_InCh_and_Numbers(Arg, row):
    _fn_return_value = False
    SubArgList = vbObjectInitialize(objtype=String)

    SubArg = Variant()
    #-----------------------------------------------------------------------------------------------------
    SubArgList = M30.SplitMultiDelims(Arg, ' +-')
    for SubArg in SubArgList:
        if SubArg == '#InCh':
            if M09SM.Get_InCh_Number_w_Err_Msg(Arg) < 0:
                return _fn_return_value
            # Check the whole argumnet to make sure that the equation contains only constants
        else:
            if not IsNumeric(SubArg):
                # Skip special names like '#InCh' and Numbers
                if Valid_Var_Name(SubArg, row) == False:
                    return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Dest - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel - ByRef 
def Create_Loc_InCh_Defines(Dest, Channel, LocInChNr):
    global MaxUsed_Loc_InCh_Row, MaxUsed_Loc_InCh
    
    #-------------------------------------------------------------------------------------------------
    if LocInChNr > 0:
        Dest = Dest + vbCr + '// Local InCh variables' + vbCr
        for i in vbForRange(0, LocInChNr - 1):
            Dest = Dest + M30.AddSpaceToLen('#define LOC_INCH' + str(i), 32) + str(Channel) + vbCr
            Channel = Channel + 1
    if MaxUsed_Loc_InCh >= LocInChNr:
        Error_Msg_Varaible_Not_Defined('LOC_INCH' + MaxUsed_Loc_InCh, MaxUsed_Loc_InCh_Row)
    return Dest, Channel

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Nr - ByRef 
def Print_Keyboard_Defines_for_Type(fp, Name, InpCnt, Nr, Skip_11_16=False, Suppress_Fill=False):
    i = Long()

    ResCnt = Long()
    #-------------------------------------------------------------------------------------------------------------------------------------------
    for i in vbForRange(1, InpCnt):
        VBFiles.writeText(fp, M30.AddSpaceToLen('#define ' + Name + str(i), 32) + str(Nr), '\n')
        if Skip_11_16:
            if ( i - 1 % 16 )  == 9:
                Nr = Nr + 6
            # Skip the IONr 11 and 16 because they are not used for the analog switches, but have to be reserved for MobaLedLib_Copy_to_InpStruct()
        Nr = Nr + 1
    # Es werden immer vielfache von 8 Inp Channels belegt
    if not Suppress_Fill:
        # 21.03.23: Juergen - don't reserve space for SwitchD
        ResCnt = ( 8 -  ( InpCnt % 8 ) )  % 8
        # 02.05.20: Old: (8 - InpCnt) Mod 8
        if ResCnt > 0:
            Nr = Nr + ResCnt
            VBFiles.writeText(fp, '// Reserve channels: ' + str(ResCnt) + ' because MobaLedLib_Copy_to_InpStruct always writes multiple of 8 channels', '\n')
    return Nr

def Test_ResCnt():
    InpCnt = Long()

    ResCnt = Long()
    #UT----------------------
    # Test for the problem above
    Debug.Print('i Ok  Err')
    for InpCnt in vbForRange(0, 24):
        ResCnt = ( 8 -  ( InpCnt % 8 ) )  % 8
        Debug.Print(Left(str(InpCnt) + '   ', 3) + Left(str(ResCnt) + '   ', 3) +  ( 8 - str(InpCnt) )  % 8)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel - ByRef 
def Make_sure_that_Channel_is_divisible_by_4(Channel):
    #--------------------------------------------------------------------------
    if Channel % 4 != 0:
        # Attention: Channel number must be divisible by 4 for Copy_Bits_to_InpStructArray()
        Channel = Channel + 4 - Channel % 4
    return Channel

def Print_MacroLine(fp, MinLen, Txt):
    # 05.01.23: Hardi
    #------------------------------------------------------------------------
    VBFiles.writeText(fp, M30.AddSpaceToLen(Txt, MinLen) + ' \\', '\n')

def Add_Set_Input_Loop_for_Keys(fp, Keys_Array_Nr):
    MinLen = 70
    # 05.01.23: Hardi
    #-------------------------------------------------------------------------------
    # New method of storing the keys which is used if Store_ValuesTxt_Used is active ("ENABLE_STORE_STATUS" defined)
    # It replaces the function "MobaLedLib_Copy_to_InpStruct"
    # Pro/Con
    # + Use the same function "MobaLedLib.Set_Input()" for all inputs
    # - This method uses more cpu time (Not checked how much)
    Print_MacroLine(fp, MinLen, '  uint8_t channel' + str(Keys_Array_Nr) + ' = START_SWITCHES_' + str(Keys_Array_Nr) + ';')
    # 27.04.23: Juergen fix bug with if both Switch B and C are used
    Print_MacroLine(fp, MinLen, '  for (int j=0;j<KEYS_ARRAY_BYTE_SIZE_' + str(Keys_Array_Nr) + ';j++)')
    Print_MacroLine(fp, MinLen, '    {')
    Print_MacroLine(fp, MinLen, '    uint8_t tmp = Keys_Array_' + str(Keys_Array_Nr) + '[j];')
    Print_MacroLine(fp, MinLen, '    for (int i=0;i<8;i++)')
    Print_MacroLine(fp, MinLen, '      {')
    Print_MacroLine(fp, MinLen, '      MobaLedLib.Set_Input(channel' + str(Keys_Array_Nr) + '++, tmp & 0x01);')
    # 27.04.23: Juergen fix bug with if both Switch B and C are used
    Print_MacroLine(fp, MinLen, '      tmp = tmp >> 1;')
    Print_MacroLine(fp, MinLen, '      }')
    Print_MacroLine(fp, MinLen, '    }')


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Channel - ByRef 
def Write_Switches_Header_File_Part_A(fp, Channel):
    global DstVar_List, SwitchA_InpCnt, SwitchB_InpCnt, SwitchC_InpCnt, SwitchD_InpCnt, SwitchA_InpLst, SwitchB_InpLst, SwitchC_InpLst, SwitchD_InpLst, Switch_Damping_Fact, CLK_Pin_Number, RST_Pin_Number
    
    _fn_return_value = False
    Ana_But_Pin_Array = vbObjectInitialize(objtype=String)

    ACh = Long()

    Used_AButton_Channels = Long()

    Start_AButtons = Long()

    Min_Channel = Long()

    dmxDefines = String()
    
    DMX_Pin_Number = "" #*HL
    #-------------------------------------------------------------------------------------------------
    # #If USE_SWITCH_AND_LED_ARRAY Then
    # 04.11.20:
    #    Print #fp, "#define USE_SWITCH_AND_LED_ARRAY 1    // Enable the new function which handles the SwitchD and the Mainboard LEDs in the ino file"
    # #Else
    #    Print #fp, "#define USE_SWITCH_AND_LED_ARRAY 0"
    #    If Get_BoardTyp() = "ESP32" Then
    # 04.11.20:
    #        MsgBox "Internal error: The compiler switch 'USE_SWITCH_AND_LED_ARRAY' must be defined if the ESP32 is used", vbCritical, "Internal error"
    #        'EndProg
    #     End If
    #  #End If
    #  Print #fp, ""
    Min_Channel = 99999999
    # 27.04.23: Juergen start with an invalid value
    if SwitchA_InpCnt > 0 or Read_LDR:
        Ana_But_Pin_Array = Split(SwitchA_InpLst, ' ')
        if SwitchA_InpCnt >  ( UBound(Ana_But_Pin_Array) + 1 )  * 10:
            P01.MsgBox(M09.Get_Language_Str('Fehler: Es wurden mehr analoge Taster verwendet als möglich sind. ' + 'Es müssen weitere analoge Eingänge zum einlesen definiert werden.' + vbCr + 'Das wird mit dem Befehl \'Set_SwitchA_InpLst()\' in der Makro Spalte gemacht.'), vbCritical, M09.Get_Language_Str('Fehler: Nicht genügend analoge Eingänge zum einlesen der Taster definiert'))
            return _fn_return_value, Channel
        
        VBFiles.writeText(fp, '#ifndef CONFIG_ONLY', '\n')
        VBFiles.writeText(fp, '//*** Analog switches ***', '\n')
        VBFiles.writeText(fp, '', '\n')
        if M02a.Get_BoardTyp() == 'AM328':
            if M70.Make_Sure_that_AnalogScanner_Library_Exists() == False:
                return _fn_return_value, Channel
            VBFiles.writeText(fp, '#include <AnalogScanner.h>   // Interrupt driven analog reading library. The library has to be installed manually from https://github.com/merose/AnalogScanner', '\n')
            VBFiles.writeText(fp, 'AnalogScanner scanner;       // Creates an instance of the analog pin scanner.', '\n')
        elif M02a.Get_BoardTyp() == 'ESP32':
            VBFiles.writeText(fp, '#include "AnalogScannerESP32.h"   ', '\n')
            VBFiles.writeText(fp, 'AnalogScannerESP32 scanner;       // Creates an instance of the analog pin scanner.', '\n')
        VBFiles.writeText(fp, '', '\n')
        if SwitchA_InpCnt > 0:
            VBFiles.writeText(fp, '#include <Analog_Buttons10.h>', '\n')
            Used_AButton_Channels = WorksheetFunction.RoundUp(SwitchA_InpCnt / 10, 0)
            for ACh in vbForRange(1, Used_AButton_Channels):
                VBFiles.writeText(fp, 'Analog_Buttons10_C AButtons' + str(ACh) + '(' + str(Ana_But_Pin_Array(ACh - 1)) + ');', '\n')
            VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
        if Switch_Damping_Fact != '':
            # 04.11.21:
            VBFiles.writeText(fp, Switch_Damping_Fact, '\n')
            VBFiles.writeText(fp, '', '\n')
        if Read_LDR:
            VBFiles.writeText(fp, '#include "Read_LDR.h"     // Darkness sensor', '\n')
            VBFiles.writeText(fp, '', '\n')
            
        VBFiles.writeText(fp, '#endif //CONFIG_ONLY', '\n')
            
        Channel = Make_sure_that_Channel_is_divisible_by_4(Channel)
        Start_AButtons = Channel
        TmpChannel = Channel
        Min_Channel = WorksheetFunction.Min(Min_Channel, Channel)
        TmpChannel = Print_Keyboard_Defines_for_Type(fp, 'SwitchA', SwitchA_InpCnt, TmpChannel, Skip_11_16=True)
        VBFiles.writeText(fp, '#define START_SWITCHES_A  ' + M30.AddSpaceToLen(str(Channel), 41) + '// Define the start number for the first analog switch', '\n')# 21.03.23 Juergen
        Channel = Channel + Used_AButton_Channels * 16
        # multiply by 16 because the Copy_Bits_to_InpStructArray() always fills bytes
        VBFiles.writeText(fp, '', '\n')
    # SwitchA_InpCnt > 0 Or Read_LDR
    if Channel1InpCnt > 0:
        VBFiles.writeText(fp, '//*** Digital switches ***', '\n')
        VBFiles.writeText(fp, '', '\n')
        # Generate the #define Switch... statements
        Channel =Make_sure_that_Channel_is_divisible_by_4(Channel)
        StartSwitches1 = Channel
        Min_Channel = WorksheetFunction.Min(Min_Channel, Channel)
        if Channel1InpCnt > 0:
            Channel = Print_Keyboard_Defines_for_Type(fp, CTR_Cha_Name_1, Channel1InpCnt, Channel)
        Channel=Make_sure_that_Channel_is_divisible_by_4(Channel)
        StartSwitches2 = Channel
        Min_Channel = WorksheetFunction.Min(Min_Channel, Channel)
        if Channel2InpCnt > 0:
            Channel = Print_Keyboard_Defines_for_Type(fp, CTR_Cha_Name_2, Channel2InpCnt, Channel)
        VBFiles.writeText(fp, '', '\n')
    if SwitchD_InpCnt >  ( UBound(Split(SwitchD_InpLst, ' ')) + 1 ) :
        # 04.11.20: Moved out of the following if because SwitchD_InpCnt should also be checked if USE_SWITCH_AND_LED_ARRAY is enabled
        # Todo: Activate the corrosponding cell. Therefore a list has to be generated where each switch is used the first time
        P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Es wurden mehr SwitchD Schalter verwendet als Pins definiert sind. ' + 'Es müssen weitere Eingänge zum einlesen definiert werden.' + vbCr + 'Das wird mit dem Befehl \'Set_SwitchD_InpLst()\' in der Makro Spalte gemacht.' + vbCr + 'Letzter möglicher Schalter: \'SwitchD#1#\''), "#1#", UBound(Split(SwitchD_InpLst, ' ')) + 1), vbCritical, M09.Get_Language_Str('Fehler: Nicht genügend Eingänge zum einlesen der Schalter definiert'))
        return _fn_return_value, Channel
    if SwitchD_InpCnt > 0:
        VBFiles.writeText(fp, '//*** Direct connected switches ***', '\n')
        VBFiles.writeText(fp, '', '\n')
        Min_Channel = WorksheetFunction.Min(Min_Channel, Channel)
        VBFiles.writeText(fp, '#define START_SWITCHES_D  ' + M30.AddSpaceToLen(str(Channel), 41) + '// Define the start number for the first mainboard switch', '\n') 
        # 21.03.23 Juergen
        Channel = Print_Keyboard_Defines_for_Type(fp, 'SwitchD', SwitchD_InpCnt, Channel, Suppress_Fill=True)
        VBFiles.writeText(fp, '', '\n')
    if DstVar_List != ' ':
        # #defines for the Output variables
        Min_Channel = WorksheetFunction.Min(Min_Channel, Channel)
        VBFiles.writeText(fp, '//*** Output Channels ***', '\n')
        VBFiles.writeText(fp, '#define START_VARIABLES   ' + M30.AddSpaceToLen(str(Channel), 41) + '// Define the start number for the variables.', '\n')
        Channel = Print_DstVar_List(fp, Channel,Min_Channel)
        VBFiles.writeText(fp, '', '\n')
    if SwitchD_InpCnt > 0:
        VBFiles.writeText(fp, 'const PROGMEM uint8_t SwitchD_Pins[] = ' + M30.AddSpaceToLen('{ ' + Replace(SwitchD_InpLst, ' ', ',') + ' };', 28) + '// Array of pins which read switches \'D\'', '\n')
        VBFiles.writeText(fp, '#define SWITCH_D_INP_CNT sizeof(SwitchD_Pins)', '\n')
        VBFiles.writeText(fp, '', '\n')
    if Channel1InpCnt > 0:
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '#define CTR_CHANNELS_1    ' + M30.AddSpaceToLen(str(CTR_Channels_1), 41) + '// Number of used counter channels for keyboard 1. Up to 10 if one CD4017 is used, up to 18 if two CD4017 are used, ...', '\n')
        VBFiles.writeText(fp, '#define CTR_CHANNELS_2    ' + M30.AddSpaceToLen(str(CTR_Channels_2), 41) + '// Number of used counter channels for keyboard 2. Up to 10 if one CD4017 is used, up to 18 if two CD4017 are used, ...', '\n')
        VBFiles.writeText(fp, '#define BUTTON_INP_LIST_1 ' + M30.AddSpaceToLen(Replace(But_Inp_List_1, ' ', ','), 41) + '// Comma separated list of the button input pins', '\n')
        VBFiles.writeText(fp, '#define BUTTON_INP_LIST_2 ' + M30.AddSpaceToLen(Replace(But_Inp_List_2, ' ', ','), 41) + '// Comma separated list of the button input pins', '\n')
        VBFiles.writeText(fp, '#define CLK_PIN           ' + M30.AddSpaceToLen(str(CLK_Pin_Number), 41) + '// Pin number used for the CD4017 clock', '\n')
        VBFiles.writeText(fp, '#define RESET_PIN         ' + M30.AddSpaceToLen(str(RST_Pin_Number), 41) + '// Pin number used for the CD4017 reset', '\n')
        VBFiles.writeText(fp, '', '\n')
        
        VBFiles.writeText(fp, '#ifndef CONFIG_ONLY', '\n')
        VBFiles.writeText(fp, '#include <Keys_4017.h>                                             // Keyboard library which uses the CD4017 counter to save Arduino pins. Attention: The pins (CLK_PIN, ...) must be defined prior.', '\n')
        VBFiles.writeText(fp, '#endif', '\n')
        
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '#define START_SWITCHES_1  ' + M30.AddSpaceToLen(StartSwitches1, 41) + '// Define the start number for the first keyboard.', '\n')
        VBFiles.writeText(fp, '#define START_SWITCHES_2  ' + M30.AddSpaceToLen(StartSwitches2, 41) + '// Define the start number for the second keyboard.', '\n')
        #VBFiles.writeText(fp, '#define START_SWITCHES_B  ' + M30.AddSpaceToLen(StartSwitches1, 41) + '// Define the start number for the first keyboard.', '\n') # 21.03.23 Juergen
        VBFiles.writeText(fp, '#define START_SWITCHES_' + Right(CTR_Cha_Name_1, 1) + '  ' + M30.AddSpaceToLen(StartSwitches1, 41) + '// Define the start number for the first keyboard.', '\n')
    if Channel2InpCnt > 0:
        VBFiles.writeText(fp, '#define START_SWITCHES_' + Right(CTR_Cha_Name_2, 1) + '  ' + M30.AddSpaceToLen(StartSwitches2, 41) + '// Define the start number for the second keyboard.', '\n')
             
        #VBFiles.writeText(fp, '#define START_SWITCHES_C  ' + M30.AddSpaceToLen(StartSwitches2, 41) + '// Define the start number for the second keyboard.', '\n') # 21.03.23 Juergen
    VBFiles.writeText(fp, '', '\n')
    # 21.03.23 Juergen write also TOTAL_...
    if Min_Channel != 99999999:
        VBFiles.writeText(fp, '#define START_SEND_INPUTS ' + M30.AddSpaceToLen(Min_Channel, 41) + '// Start address of all switches/variables', '\n')
        VBFiles.writeText(fp, '#define TOTAL_SEND_INPUTS ' + M30.AddSpaceToLen(To_Eight(Used_AButton_Channels * 16) + To_Eight(CTR_Channels_1 * List_Lenght(But_Inp_List_1)) + To_Eight(CTR_Channels_2 * List_Lenght(But_Inp_List_2)) + SwitchD_InpCnt + List_Lenght(DstVar_List), 41) + '// Number of used switches/variables', '\n')
    
    VBFiles.writeText(fp, '#define TOTAL_SWITCHES_A  ' + M30.AddSpaceToLen(To_Eight(Used_AButton_Channels * 16), 41) + '// Number of used inputs for analog keyboard', '\n')
    if Right(CTR_Cha_Name_1, 1) == 'B':
        VBFiles.writeText(fp, '#define TOTAL_SWITCHES_B  ' + M30.AddSpaceToLen(To_Eight(CTR_Channels_1 * List_Lenght(But_Inp_List_1)), 41) + '// Number of used inputs for keyboard 1', '\n')
        VBFiles.writeText(fp, '#define TOTAL_SWITCHES_C  ' + M30.AddSpaceToLen(To_Eight(CTR_Channels_2 * List_Lenght(But_Inp_List_2)), 41) + '// Number of used inputs for keyboard 2', '\n')
    else:
        # channels are changed in the case
        VBFiles.writeText(fp, '#define TOTAL_SWITCHES_B  ' + M30.AddSpaceToLen(0, 41) + '// Number of used inputs for keyboard 1', '\n')
        VBFiles.writeText(fp, '#define TOTAL_SWITCHES_C  ' + M30.AddSpaceToLen(To_Eight(CTR_Channels_1 * List_Lenght(But_Inp_List_1)), 41) + '// Number of used inputs for keyboard 2', '\n')
    
    VBFiles.writeText(fp, '#define TOTAL_SWITCHES_D  ' + M30.AddSpaceToLen(SwitchD_InpCnt, 41) + '// Number of used inputs for main board switches', '\n')
    VBFiles.writeText(fp, '#define TOTAL_VARIABLES   ' + M30.AddSpaceToLen(List_Lenght(DstVar_List), 41) + '// Number of used variables', '\n')
    # 19.01.21 Juergen      
    if True:
        # FastLED initialisation                                                
        # 26.04.20:
        LED_PINNr_Arr = Split(LED_PINNr_List, ' ')
        VBFiles.writeText(fp, '/*********************/', '\n')
        VBFiles.writeText(fp, '#define SETUP_FASTLED()                                                      \\', '\n')
        VBFiles.writeText(fp, '/*********************/                                                      \\', '\n')
        cnt = 0 #*HL
        for LEDCh in vbForRange(0, M02.LED_CHANNELS - 1):
            if M06.LEDs_per_Channel(LEDCh) > 0:
                ExpOutPins = LEDCh
                if LEDCh <= UBound(LED_PINNr_Arr):
                    if LEDCh != DMX_LedChan:
                        if LED_PINNr_Arr(LEDCh) != M09.Virtual_Channel_T:   
                            #   18.02.22 Juergen Virtual Channel
                            # Generate: CLEDController& controller0 = FastLED.addLeds<NEOPIXEL,  6 >(leds+   0, 200); \"
                            if Use_WS2811:
                                # 19.01.21 Juergen
                                VBFiles.writeText(fp, '  CLEDController& controller' + str(LEDCh) + ' = FastLED.addLeds<WS2811, ' + M30.AddSpaceToLenLeft(LED_PINNr_Arr(LEDCh), 2) + ', RGB>(leds+' + M30.AddSpaceToLenLeft(str(cnt), 3) + ',' + M30.AddSpaceToLenLeft(str(M06.LEDs_per_Channel(LEDCh)), 3) + '); \\', '\n')
                                # 19.01.21 Juergen
                            else:
                                VBFiles.writeText(fp, '  CLEDController& controller' + str(LEDCh) + ' = FastLED.addLeds<NEOPIXEL, ' + M30.AddSpaceToLenLeft(LED_PINNr_Arr(LEDCh), 2) + '>(leds+' + M30.AddSpaceToLenLeft(str(cnt), 3) + ',' + M30.AddSpaceToLenLeft(str(M06.LEDs_per_Channel(LEDCh)), 3) + '); \\', '\n')
                    else:
                        # 19.01.21 Juergen
                        dmxDefines = '#define DMX_LED_OFFSET ' + str(cnt) + vbCrLf + '#define DMX_CHANNEL_COUNT ' + str(M06.LEDs_per_Channel(LEDCh) * 3)
                        DMX_Pin_Number = LED_PINNr_Arr(LEDCh)
                        if ( M06.LEDs_per_Channel(LEDCh) > 100 ) :
                            P01.MsgBox(M09.Get_Language_Str('Fehler: Das DMX Senden ist auf 100 Leds (300 DMX Kanäle) limitiert.'), vbCritical, P01.ActiveSheet.Name)
                            return _fn_return_value, Channel
            cnt = cnt + M06.LEDs_per_Channel(LEDCh)
        if ExpOutPins > UBound(LED_PINNr_Arr):
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Es sind nicht genügend Ausgangs Pins zur Ansteuerung der LEDs vorhanden. ' + 'Die LED Pins müssen mit dem Befehl "Set_LED_OutpPinLst()" definiert werden.' + vbCr + 'Es müssen #1# Arduino Ausgänge definiert sein.'), "#1#", str(ExpOutPins + 1)), vbCritical, M09.Get_Language_Str('Mehr LED Gruppen verwendet als LED Ausgangspins definiert'))
            return _fn_return_value, Channel
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
    if SwitchA_InpCnt > 0 or Read_LDR or Channel1InpCnt > 0 or SwitchD_InpCnt > 0:
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
            
            VBFiles.writeText(fp, '#endif', '\n')
            VBFiles.writeText(fp, '', '\n')
        if Channel1InpCnt > 0:
            VBFiles.writeText(fp, '#ifndef CONFIG_ONLY', '\n')
            VBFiles.writeText(fp, '  Keys_4017_Setup(); // Initialize the keyboard scanning process', '\n')
            VBFiles.writeText(fp, '#endif', '\n')
            
        if SwitchD_InpCnt > 0:
            VBFiles.writeText(fp, '', '\n')
            VBFiles.writeText(fp, '  for (uint8_t i = 0; i < SWITCH_D_INP_CNT; i++)', '\n')
            VBFiles.writeText(fp, '    pinMode(pgm_read_byte_near(&SwitchD_Pins[i]), INPUT_PULLUP);', '\n')
        VBFiles.writeText(fp, '}', '\n')
        VBFiles.writeText(fp, '', '\n')
    # Generate the "Additional_Loop_Proc()"
    if SwitchA_InpCnt > 0 or Channel1InpCnt > 0 or SwitchD_InpCnt > 0:
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
                # add 16 because 2 Bytes add 16 channels
        if M06.Store_ValuesTxt_Used:
            # 05.01.23: Hardi
            if Channel1InpCnt > 0:
                Add_Set_Input_Loop_for_Keys(fp, 1)
            if Channel2InpCnt > 0:
                Add_Set_Input_Loop_for_Keys(fp, 2)
        else:
            if Channel1InpCnt > 0:        
                VBFiles.writeText(fp, '  MobaLedLib_Copy_to_InpStruct(Keys_Array_1, KEYS_ARRAY_BYTE_SIZE_1, START_SWITCHES_1);  \\', '\n')
            if Channel2InpCnt > 0:
                VBFiles.writeText(fp, '  MobaLedLib_Copy_to_InpStruct(Keys_Array_2, KEYS_ARRAY_BYTE_SIZE_2, START_SWITCHES_2);  \\', '\n')
        if SwitchD_InpCnt > 0:
            VBFiles.writeText(fp, '  for (uint8_t i = 0; i < ' + str(SwitchD_InpCnt) + '; i++) \\', '\n')
            VBFiles.writeText(fp, '      MobaLedLib.Set_Input(SwitchD1 + i, !digitalRead(pgm_read_byte_near(&SwitchD_Pins[i])));\\', '\n')
        VBFiles.writeText(fp, '}', '\n')
    _fn_return_value = True
    return _fn_return_value, Channel

def Write_LowProrityLoop_Header_File(fp):
    _fn_return_value = False
    if Serial_PinLst != '':
        VBFiles.writeText(fp, '/*****************************/', '\n')
        VBFiles.writeText(fp, '#define Additional_Loop_Proc2() \\', '\n')
        VBFiles.writeText(fp, '/*****************************/ \\', '\n')
        # This function is called in every loop, on ESP32 in the alternate loop (not time critical)
        VBFiles.writeText(fp, '{                               \\', '\n')
        if Serial_PinLst != '':
            VBFiles.writeText(fp, '   soundProcessor.process();\\', '\n')
            # 02.11.2021: Juergen add support of multiple sound module types
        VBFiles.writeText(fp, '}', '\n')
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpLst1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpLst2 - ByVal 
def No_Duplicates_in_two_InpLists(Letter1, Letter2_or_Name, InpLst1, InpLst2, Set_Funct2='Set_LED_OutpPinLst()'):
    _fn_return_value = False
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
            return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpLst1 - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpLst2 - ByVal 
def No_Duplicates_in_two_Lists(Pin2, InpLst1, InpLst2, Set_Funct2='Set_LED_OutpPinLst()'):
    _fn_return_value = False
    Pin = Variant()
    #-----------------------------------------------------------------------------------------------------------------------------------------
    # Retutn True if no duplicates are detected
    InpLst2 = ' ' + InpLst2 + ' '
    for Pin in Split(InpLst1, ' '):
        if InStr(InpLst2, ' ' + Pin + ' ') > 0:
            P01.MsgBox(Replace(Replace(Replace(M09.Get_Language_Str('Fehler: Der Pin \'#1#\' in \'#3#\' wird bereits als \'#2#\' Pin benutzt.' + vbCr + 'Der Pin kann nicht mehrfach benutzt werden.'), "#1#", Pin), '#2#', Pin2), '#3#', Set_Funct2), vbCritical, 'Fehler: Doppelte Benutzung eines Pins')
            return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

def Test_No_Duplicates_in_two_InpLists():
    global SwitchC_InpLst, SwitchD_InpLst, LED_PINNr_List
    #UT------------------------------------------------
    SwitchC_InpLst = '2 7 8 9 10 11 12 A5'
    SwitchD_InpLst = '7 8 9'
    #Debug.Print No_Duplicates_in_two_InpLists("C", "D", SwitchC_InpLst, SwitchD_InpLst)
    LED_PINNr_List = '6 A4 A5'
    Debug.Print(No_Duplicates_in_two_InpLists('C', 'LED', SwitchC_InpLst, LED_PINNr_List))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpLst1 - ByVal 
def Check_CLK_a_RST_Pin_Usage(Letter1, InpLst1):
    global RST_Pin_Number, CLK_Pin_Number, SwitchB_InpCnt, SwitchC_InpCnt
    
    _fn_return_value = False
    #------------------------------------------------------------------------------------------------
    # Check the RST_Pin_Number together with Letter1
    if SwitchB_InpCnt > 0 or SwitchC_InpCnt > 0:
        if False == No_Duplicates_in_two_InpLists(Letter1, Replace(M09.Get_Language_Str('#1# Pin für SwitchB oder SwitchC'), "#1#", 'Reset'), InpLst1, RST_Pin_Number, 'Set_RST_Pin_Number()'):
            return _fn_return_value
        if False == No_Duplicates_in_two_InpLists(Letter1, Replace(M09.Get_Language_Str('#1# Pin für SwitchB oder SwitchC'), "#1#", 'Clock'), InpLst1, CLK_Pin_Number, 'Set_CLK_Pin_Number()'):
            return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

def No_Duplicates_in_InpLists():
    global SwitchA_InpCnt, SwitchB_InpCnt, SwitchC_InpCnt, SwitchD_InpCnt,SwitchA_InpLst,SwitchB_InpLst,SwitchC_InpLst,SwitchD_InpLst, LED_PINNr_List, LDR_Pin_Number, Serial_PinLst
     
    _fn_return_value = False
    #-----------------------------------------------------
    if SwitchA_InpCnt > 0:
        if SwitchB_InpCnt > 0:
            if No_Duplicates_in_two_InpLists('A', 'B', SwitchA_InpLst, SwitchB_InpLst) == False:
                return _fn_return_value
        if SwitchC_InpCnt > 0:
            if No_Duplicates_in_two_InpLists('A', 'C', SwitchA_InpLst, SwitchC_InpLst) == False:
                return _fn_return_value
        if SwitchD_InpCnt > 0:
            if No_Duplicates_in_two_InpLists('A', 'D', SwitchA_InpLst, SwitchD_InpLst) == False:
                return _fn_return_value
        if No_Duplicates_in_two_InpLists('A', 'LED', SwitchA_InpLst, LED_PINNr_List) == False:
            return _fn_return_value
        if Read_LDR:
            if No_Duplicates_in_two_InpLists('A', 'LDR', SwitchA_InpLst, LDR_Pin_Number, 'Set_LDR_Pin_Number()') == False:
                return _fn_return_value
        if Check_CLK_a_RST_Pin_Usage('A', SwitchA_InpLst) == False:
            return _fn_return_value
            # 04.11.20:
        if No_Duplicates_in_two_InpLists('A', 'SOUND', SwitchA_InpLst, Serial_PinLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _fn_return_value
            # 08.10.21: Juergen
    if SwitchB_InpCnt > 0:
        if SwitchC_InpCnt > 0:
            if No_Duplicates_in_two_InpLists('B', 'C', SwitchB_InpLst, SwitchC_InpLst) == False:
                return _fn_return_value
        if SwitchD_InpCnt > 0:
            if No_Duplicates_in_two_InpLists('B', 'D', SwitchB_InpLst, SwitchD_InpLst) == False:
                return _fn_return_value
        if No_Duplicates_in_two_InpLists('B', 'LED', SwitchB_InpLst, LED_PINNr_List) == False:
            return _fn_return_value
        if Read_LDR:
            if No_Duplicates_in_two_InpLists('B', 'LDR', SwitchB_InpLst, LDR_Pin_Number, 'Set_LDR_Pin_Number()') == False:
                return _fn_return_value
        if Check_CLK_a_RST_Pin_Usage('B', SwitchB_InpLst) == False:
            return _fn_return_value
            # 04.11.20:
        if No_Duplicates_in_two_InpLists('B', 'SOUND', SwitchA_InpLst, Serial_PinLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _fn_return_value
            # 08.10.21: Juergen
    if SwitchC_InpCnt > 0:
        if SwitchD_InpCnt > 0:
            if No_Duplicates_in_two_InpLists('C', 'D', SwitchC_InpLst, SwitchD_InpLst) == False:
                return _fn_return_value
        if No_Duplicates_in_two_InpLists('C', 'LED', SwitchC_InpLst, LED_PINNr_List) == False:
            return _fn_return_value
        if Read_LDR:
            if No_Duplicates_in_two_InpLists('C', 'LDR', SwitchC_InpLst, LDR_Pin_Number, 'Set_LDR_Pin_Number()') == False:
                return _fn_return_value
        if Check_CLK_a_RST_Pin_Usage('C', SwitchC_InpLst) == False:
            return _fn_return_value
            # 04.11.20:
        if No_Duplicates_in_two_InpLists('C', 'SOUND', SwitchA_InpLst, Serial_PinLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _fn_return_value
            # 08.10.21: Juergen
    if SwitchD_InpCnt > 0:
        if No_Duplicates_in_two_InpLists('D', 'LED', SwitchD_InpLst, LED_PINNr_List) == False:
            return _fn_return_value
        if Read_LDR:
            if No_Duplicates_in_two_InpLists('D', 'LDR', SwitchD_InpLst, LDR_Pin_Number, 'Set_LDR_Pin_Number()') == False:
                return _fn_return_value
        if Check_CLK_a_RST_Pin_Usage('D', SwitchD_InpLst) == False:
            return _fn_return_value
            # 04.11.20:
        if No_Duplicates_in_two_InpLists('D', 'SOUND', SwitchA_InpLst, Serial_PinLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _fn_return_value
            # 08.10.21: Juergen
    _fn_return_value = True
    return _fn_return_value

def Init_HeaderFile_Generation_SW(firstRun):
    
    global  MaxUsed_Loc_InCh, Read_LDR, Store_Status_Enabled, Use_WS2811, SwitchA_InpCnt, SwitchB_InpCnt,SwitchC_InpCnt
    global SwitchD_InpCnt,DMX_LedChan,Serial_PinLst,LED_PINNr_List,LDR_Pin_Number,SwitchA_InpLst,SwitchB_InpLst,SwitchC_InpLst,SwitchD_InpLst,CLK_Pin_Number,RST_Pin_Number,DstVar_List, MultiSet_DstVar_List
    global  CTR_Channels_1, CTR_Channels_2, But_Inp_List_1,But_Inp_List_2, Channel1InpCnt, Channel2InpCnt,CTR_Cha_Name_1,CTR_Cha_Name_2
    _fn_return_value = False
    #---------------------------------------------------------
    if ( firstRun ) :
        MaxUsed_Loc_InCh = - 1
        Read_LDR = False
        Store_Status_Enabled = False
        Use_WS2811 = False
        # The following variables are read from the data lines
        SwitchA_InpCnt = 0
        # Number of switch imputs for channel A (A=Analog push buttons) Maximal switch number is detected for this and the next two lines.
        SwitchB_InpCnt = 0
        # Number of switch imputs for channel B (B=Border:  push buttons (or switches) around the border of the layout
        SwitchC_InpCnt = 0
        # Number of switch imputs for channel C (C=Console: switches (or push buttons) in the console (Weichenstellpult)
        SwitchD_InpCnt = 0
        # Number of switch imputs for channel D (D=Direct:  switches (or push buttons) connected direct to the main board
        DMX_LedChan = - 1
        # 19.01.21 Juergen
        Serial_PinLst = ''
         # 08.10.21 Juergen add Serial Sound feature, by default no serial sound
        LED_PINNr_List = M30.Get_Current_Platform_String('LED_Pins')
        # ~08.10.21: Juergen: New function to handle the valid pins. Prior this was handled here
        LDR_Pin_Number = M30.Get_Current_Platform_String('LDR_Pin')
        SwitchA_InpLst = M30.Get_Current_Platform_String('SwitchA_Pins')
        SwitchB_InpLst = M30.Get_Current_Platform_String('SwitchB_Pins')
        SwitchC_InpLst = M30.Get_Current_Platform_String('SwitchC_Pins')
        SwitchD_InpLst = M30.Get_Current_Platform_String('SwitchD_Pins')
        CLK_Pin_Number = M30.Get_Current_Platform_String('CLK_Pin')
        RST_Pin_Number = M30.Get_Current_Platform_String('RST_Pin')
        DstVar_List = ' '
        MultiSet_DstVar_List = ' '
    if not First_Scan_of_Data_Rows():
        return _fn_return_value
        # Scan the data rows and fill the variables above if the corrosponding functions are used in the Config__Col
    if MultiSet_DstVar_List != ' ':
        if P01.MsgBox(M09.Get_Language_Str('Achtung: Die folgenden Zielvariablen werden mehrfach gesetzt:') + vbCr + MultiSet_DstVar_List + vbCr + M09.Get_Language_Str('Senden zum Arduino abbrechen?'), vbQuestion + vbYesNo, M09.Get_Language_Str('Warnung: Mehrfach benutzte Zielvariablen')) == vbYes:
            return _fn_return_value
    if No_Duplicates_in_InpLists() == False:
        return _fn_return_value
    if firstRun:
        CTR_Channels_1 = 0
        CTR_Channels_2 = 0
        But_Inp_List_1 = 'Unused'
        But_Inp_List_2 = 'Unused'
        Channel1InpCnt = 0
        Channel2InpCnt = 0
    if SwitchB_InpCnt > 0 and SwitchC_InpCnt > 0:
        CTR_Cha_Name_1 = 'SwitchB'
        CTR_Cha_Name_2 = 'SwitchC'
        CTR_Channels_1 = WorksheetFunction.RoundUp(SwitchB_InpCnt /  ( UBound(Split(SwitchB_InpLst, ' ')) + 1 ), 0)
        CTR_Channels_2 = WorksheetFunction.RoundUp(SwitchC_InpCnt /  ( UBound(Split(SwitchC_InpLst, ' ')) + 1 ), 0)
        But_Inp_List_1 = SwitchB_InpLst
        But_Inp_List_2 = SwitchC_InpLst
        Channel1InpCnt = SwitchB_InpCnt
        Channel2InpCnt = SwitchC_InpCnt
    elif SwitchB_InpCnt > 0:
        CTR_Cha_Name_1 = 'SwitchB'
        CTR_Cha_Name_2 = 'Unused'
        CTR_Channels_1 = WorksheetFunction.RoundUp(SwitchB_InpCnt /  ( UBound(Split(SwitchB_InpLst, ' ')) + 1 ), 0)
        But_Inp_List_1 = SwitchB_InpLst
        Channel1InpCnt = SwitchB_InpCnt
    elif SwitchC_InpCnt > 0:
        CTR_Cha_Name_1 = 'SwitchC'
        CTR_Cha_Name_2 = 'Unused'
        CTR_Channels_1 = WorksheetFunction.RoundUp(SwitchC_InpCnt /  ( UBound(Split(SwitchC_InpLst, ' ')) + 1 ), 0)
        But_Inp_List_1 = SwitchC_InpLst
        Channel1InpCnt = SwitchC_InpCnt
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def Find_and_Select_Name(Name, UndefNr):
    UndefRow = Long()
    #----------------------------------------------------------------------
    UndefRow = int(Split(M06.Undef_Input_Var_Row, ' ')(UndefNr))
    P01.Cells(UndefRow, M25.Get_Address_Col()).Select()
    # VB2PY (UntranslatedCode) On Error Resume Next
    try:
        P01.Rows(UndefRow).Find(What= Name, LookIn= xlValues, LookAt= xlPart, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False).Activate()
    except:
        pass
    # VB2PY (UntranslatedCode) On Error GoTo 0
    
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def Find_Alias_Name_In_Sheet(Name):
    _fn_return_value = None
    Res = Long()

    row = Long()

    #-------------------------------------------------------------------------
    row = M02.FirstDat_Row
    while 1:
        r = P01.Range(P01.Cells(row, M25.Config__Col), P01.Cells(M30.LastUsedRow(), M25.Config__Col))
        Res = M30.FastFind('// Define Input(' + Name + ')', r)
        if Res == 0:
            return _fn_return_value
        row = row + Res - 1
        if not P01.Rows(row).EntireRow.Hidden and P01.Cells(row, M02.Enable_Col) != '':
            _fn_return_value = True
            return _fn_return_value
        row = row + 1
        if not (True):
            break
    return _fn_return_value

def Check_Detected_Variables():
    global DstVar_List
    
    _fn_return_value = False
    UndefNr = 0
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
            # 24.04.20: Search also in the list of DCC,SX,CAN defines
            if not Found:
                Found = ( InStr(DstVar_List, UnDefVar) != 0 )
            if not Found and UnDefVar == '[Multiplexer]':
                Found = True
                # Added by Misha 30-5-2020.
                # 14.06.20: Added from Mishas version
            if not Found:
                Found = Find_Alias_Name_In_Sheet(UnDefVar)            
            if not Found:
                Find_and_Select_Name(UnDefVar, UndefNr)
                P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Die Variable \'#1#\' wird als Eingang benutzt, wird aber nirgendwo gesetzt.'), "#1#", UnDefVar), vbCritical, M09.Get_Language_Str('Fehler: Undefinierter Zustand eine Eingangsvariablen'))
                return _fn_return_value
            UndefNr = UndefNr + 1
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
