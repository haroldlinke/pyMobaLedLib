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

# fromx proggen.M02_Public import *
# fromx proggen.M08_ARDUINO import M08.LEDNr_Display_Type
# fromx proggen.M25_Columns import Make_sure_that_Col_Variables_match #,LEDs____Col,LED_Cha_Col,LED_Nr__Col
#import proggen.M25_Columns as M25
#import proggen.M30_Tools as M30
#import proggen.M06_Write_Header as M06
#import proggen.D02_Userform_Select_Typ_DCC as D02
# fromx proggen.M06_Write_Header import Start_LED_Channel

import proggen.M01_Gen_Release_Version as M01
import proggen.M02_Public as M02
import proggen.M02_global_variables as M02GV
#import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
#import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
#import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
import proggen.M32_DCC as M32
#import proggen.M37_Inst_Libraries as M37
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Multiplexer as M80
#import ExcelAPI.P01_Worksheetfunction as WorksheetFunction

import  proggen.F00_mainbuttons as F00

#import proggen.D02_Userform_Select_Typ_DCC as D02

import ExcelAPI.XLA_Application as P01
import mlpyproggen.Prog_Generator as PG

from ExcelAPI.XLC_Excel_Consts import *



#Start_LED_Channel = vbObjectInitialize((M02.LED_CHANNELS - 1,), Long)


""" Update several cells in the DCC and Selectrix sheet by events
 - Set/delete the Enable hook
 - Toggle the Input Typ
 - Calculate the Start LedNr
 - Format new lines
 -
 27.03.20: - add automatic creation of DCC/Selectrix test buttons
 29.03.20: - automatic resize of buttons column
 31.03.20: - add toggle and improve ButtonColor handling
 02.04.20: - limit size of test buttons
           - if multiple test buttons use same address toggle all related buttons
 26.03.21: - speed up ResetTestButtons function

# VB2PY (CheckDirective) VB directive took path 1 on True

"""

Global_Rect_List = vbObjectInitialize(objtype=String)
PriorCell = None  #range() #* HaLi test

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Line - ByVal 
def Get_Parameter_from_Leds_Line(Line, ParNr):
    Parts = Variant()

    Error = Boolean()
    #---------------------------------------------------------------------------------
    if Left(Line, 1) == '^':
        Line = Trim(Mid(Line, 2, 200))
    if Left(Line, 1) != 'C':
        P01.MsgBox(M09.Get_Language_Str('Fehler: LEDs Eintrag muss mit \'C\' beginnen'), vbCritical, M09.Get_Language_Str('Fehler in LEDs Eintrag'))
        M30.EndProg()
    Parts = Split(Mid(Line, 2, 200), '-')
    if UBound(Parts) != 1:
        Error = 1
    elif not IsNumeric(Parts(0)) or not IsNumeric(Parts(1)):
        Error = 1
    if Error:
        P01.MsgBox(M09.Get_Language_Str('Fehler: LEDs Eintrag muss zwei mit \'-\' getrennte Kanäle enthalten'), vbCritical, M09.Get_Language_Str('Fehler in LEDs Eintrag'))
        M30.EndProg()
    partx = Parts[ParNr]
    fn_return_value = P01.val(partx)
    #fn_return_value = P01.val(Parts[ParNr]) #*HL
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Line - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: LastusedChannel - ByRef 
def Update_LastUsedChannel_in_Row(Line, LastusedChannel):
    val = int()
    #---------------------------------------------------------------------------------------------
    Line = Trim(Line)
    val = Get_Parameter_from_Leds_Line(Line, 1)
    if val > LastusedChannel:
        LastusedChannel = val
    return LastusedChannel

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: LastusedChannel - ByRef 
def Update_LastUsedChannel(LEDs, LastusedChannel):
    #--------------------------------------------------------------------------------
    if InStr(LEDs, vbLf):
        for Line in Split(LEDs, vbLf):
            LastusedChannel = Update_LastUsedChannel_in_Row(Line, LastusedChannel)
    else:
        LastusedChannel = Update_LastUsedChannel_in_Row(LEDs, LastusedChannel)
    return LastusedChannel
        

def Get_FirstUsedChannel(LEDs):
    #---------------------------------------------------
    fn_return_value = 0
    if InStr(LEDs, vbLf):
        fn_return_value = 99
        for Line in Split(LEDs, vbLf):
            val = Get_Parameter_from_Leds_Line(Line, 0)
            if val < Get_FirstUsedChannel():
                fn_return_value = val
    else:
        fn_return_value = Get_Parameter_from_Leds_Line(LEDs, 0)
    return fn_return_value

def UsedModules(LEDs):
    d = Double()
    #-------------------------------------------------
    d = LEDs / 3
    if d == Round(d):
        fn_return_value = int(d)
    else:
        fn_return_value = int(Round(d + 0.5, 0))
    return fn_return_value

def Check_IsSingleChannelCmd(LEDs):
    #-------------------------------------------------------
    fn_return_value = InStr(LEDs, 'C') > 0
    return fn_return_value

def Row_is_Achtive(r):
    #---------------------------------------------------
    fn_return_value =  P01.Rows(r).EntireRow.Hidden == False and P01.Cells(r, M02.Enable_Col) != '' and Trim(P01.Cells(r, M25.LEDs____Col)) != ''
    return fn_return_value

def Row_Contains_Address_or_VarName(r):
    #--------------------------------------------------------------------
    if  P01.Rows(r).EntireRow.Hidden == False and P01.Cells(r, M02.Enable_Col) != '':
        Addr_Col = M25.Get_Address_Col()
        if Trim(P01.Cells(r, Addr_Col)) == '':
            return fn_return_value
            # Empty Address
        if IsNumeric(Trim(P01.Cells(r, Addr_Col))):
            # For Variable names this check is not needed
            if  M25.Page_ID == 'Selextrix':
                if Trim(P01.Cells(r, M25.SX_Bitposi_Col)) == '':
                    return fn_return_value
            if Trim(P01.Cells(r, M25.Inp_Typ_Col)) == '':
                return fn_return_value
    fn_return_value = True
    return fn_return_value

def Update_All_Start_LedNr():
    OldScreenupdating = Boolean()

    Sh = Variant()
    #---------------------------
    # 29.12.2023: Juergen - keep active sheet on function exit
    OldScreenupdating = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = False
    for Sh in PG.ThisWorkbook.Sheets():
        if M28.Is_Data_Sheet(Sh):
            Sh.Select()
            Update_Start_LedNr()
    # 29.12.2023: Juergen - keep active sheet on function exit
    P01.Application.ScreenUpdating = OldScreenupdating

def Is_Set_LEDNrMacro(Cmd):
    _fn_return_value = False
    # 15.09.23: Hardi
    #-----------------------------------------------------------
    _fn_return_value = Left(Cmd, Len('// Set_LEDNr(')) == '// Set_LEDNr('
    return _fn_return_value

def Get_LEDNr_from_Set_LEDNrMacro(Cmd):
    _fn_return_value = False
    # 15.09.23: Hardi
    #--------------------------------------------------------------------
    _fn_return_value = P01.val(Mid(Cmd, 1 + Len('// Set_LEDNr(')))
    return _fn_return_value

def Update_Start_LedNr(FirstRun=True):
    _fn_return_value = False
    OldEvents = Boolean()

    #display_Type = int()

    #Row = Variant()
    
    value = P01.getvalue(3,12)

    LEDNr = vbObjectInitialize((M02.LED_CHANNELS,), Long)

    LastusedChannel = vbObjectInitialize((M02.LED_CHANNELS,), Long)
    
    LEDs_Channel = 0
    
    col = Long()

    r = Long()

    Nr = Long()
    #------------------------------
    # Update the Start LedNr in all used rows
    OldEvents =  P01.Application.EnableEvents
    display_Type = M08.LEDNr_Display_Type()
    if FirstRun:
        P01.Application.EnableEvents = False
        # Prevent recursive calls ic cells are changed
        # 26.04.20:  # 03.04.21 Juergen - try to find out if only the main LED Channel is in use
        Max_LEDs_Channel = 0   # 10.03.2023 Juergen include feature
        M06.IncludeStack = Collection()
        M06.IncludeStack.Add(( P01.ActiveSheet.Name ))
        M06.Clear_MaxLEDNr()    
    M25.Make_sure_that_Col_Variables_match()
    # 03.04.21 Juergen - try to find out if only the main LED Channel is in use
    for row in P01.ActiveSheet.UsedRange_Rows():
        # ToDo: Hier könnte man einen Eigenen Range definieren der erst ab der FirstDat_Row beginnt. Dann könnte die abfrage "If r >= FirstDat_Row Then" entfallen
        r = row.Row
        #*HL P01.set_statusmessage(M09.Get_Language_Str("Headerfile wird erstellt. Max LEDs Channel: "+str(r)))
        if r >= M02.FirstDat_Row:
            if Row_is_Achtive(r):
                if P01.val(P01.Cells(r, M25.LED_Cha_Col)) > Max_LEDs_Channel:
                    Max_LEDs_Channel = P01.val(P01.Cells(r, M25.LED_Cha_Col))
    for row in P01.ActiveSheet.UsedRange_Rows():
        # ToDo: Hier könnte man einen Eigenen Range definieren der erst ab der FirstDat_Row beginnt. Dann könnte die abfrage "If r >= FirstDat_Row Then" entfallen
        r = row.Row
        #P01.set_statusmessage(M09.Get_Language_Str("Headerfile wird erstellt. Update Start LED: "+str(r)))
        #print("Update Start LED: Row=",r)
        if r >= M02.FirstDat_Row:
            if Row_is_Achtive(r):
                LEDs_Channel = P01.val(P01.Cells(r, M25.LED_Cha_Col))
                LEDs = Trim(P01.Cells(r, M25.LEDs____Col))
                IsSingleChannelCmd = Check_IsSingleChannelCmd(LEDs)
                # Check if the privious lines adress single channels
                if LastusedChannel(LEDs_Channel) > 0:
                    if IsSingleChannelCmd:
                        if Left(LEDs, 1) == '^':
                            LastusedChannel[LEDs_Channel] = 0
                        if Get_FirstUsedChannel(LEDs) <= LastusedChannel(LEDs_Channel):
                            LEDNr[LEDs_Channel] = LEDNr(LEDs_Channel) + UsedModules(LastusedChannel(LEDs_Channel))
                            LastusedChannel[LEDs_Channel] = 0
                    else:
                        # Last lines have been single channel lines, but the actual line adresses full RGB LEDs
                        LEDNr[LEDs_Channel] = LEDNr(LEDs_Channel) + UsedModules(LastusedChannel(LEDs_Channel))
                        LastusedChannel[LEDs_Channel] = 0
                Clear_LED_Nr_Columns(r, M25.LED_Nr__Col)
                if LEDs == M02.SerialChannelPrefix:
                    # 07.10.21: Jürgen Serial Channel
                    #NewValue = '\'' + M02.SerialChannelPrefix + str(LEDs_Channel) **HLI remove "'" 
                    NewValue = M02.SerialChannelPrefix + str(LEDs_Channel)
                else:
                    if Max_LEDs_Channel > 0 and display_Type == 1:
                        #NewValue = '\'' + LEDs_Channel + '-' + str(LEDNr(LEDs_Channel)) **HLI remove "'" 
                        NewValue = str(LEDs_Channel) + '-' + str(LEDNr(LEDs_Channel))
                    else:
                        NewValue = str(LEDNr(LEDs_Channel))
                if P01.Cells(r, M25.LED_Nr__Col).Value == '' or P01.Cells(r, M25.LED_Nr__Col).Value != NewValue:
                    P01.Cells(r, M25.LED_Nr__Col).Value = NewValue
                    #print("New Value: ",r,NewValue)
                if IsSingleChannelCmd:
                    LastusedChannel[LEDs_Channel] = Update_LastUsedChannel(LEDs, LastusedChannel(LEDs_Channel))
                    if LastusedChannel(LEDs_Channel) > 3:
                        # Wenn mehrere einzelne LEDs verwendet werden welche nicht in ein WS2811 Modul passen  ' 06.06.20:
                        # Beispiel: Drei aufeinanderfolgende "Herz_BiRelais()" Zeilen
                        #           Das zweite Herz_BiRelais() Belegt den blauen Kanal und den Roten des nächsten WS2811
                        #           Darum muss LastusedChannel auf 1 gesetzt und LEDNr um 1 erhöht werden
                        IncLEDNr = LastusedChannel(LEDs_Channel) // 3
                        LastusedChannel[LEDs_Channel] = LastusedChannel(LEDs_Channel) % 3
                        LEDNr[LEDs_Channel] = LEDNr(LEDs_Channel) + IncLEDNr
                else:
                    # 20.04.23: Hardi: Additional Max calc
                    CellLinesS = M30.CellLinesSum("") #proggen.clsExtensionMacro.LEDs)
                    if CellLinesS < 0:
                        if LEDNr(LEDs_Channel) > M06.MaxLEDNr(LEDs_Channel):
                            M06.MaxLEDNr[LEDs_Channel] = LEDNr(LEDs_Channel)
                        # Calc the correct maximum in case the line substracts leds: Next_LED(-1) 20.04.23: Hardi:
                    LEDNr[LEDs_Channel] = LEDNr(LEDs_Channel) + M30.CellLinesSum(LEDs)
                    # If the cell consists of several lines the sum is calculated
                Cmd = Trim(P01.Cells(r, M25.Config__Col))
                # 15.09.23: Hardi: New command Set_LEDNr
                if Is_Set_LEDNrMacro(Cmd):
                    New_LEDNr = Get_LEDNr_from_Set_LEDNrMacro(Cmd)
                    LEDs_Channel = P01.val(P01.Cells(r, M25.LED_Cha_Col))
                    P01.CellDict[r, M25.LEDs____Col] = New_LEDNr - LEDNr(LEDs_Channel)
                    LEDNr[LEDs_Channel] = New_LEDNr
            else:
                #Dim cmd As String
                Cmd = Trim(P01.Cells(r, M25.Config__Col))
                if P01.Rows(r).EntireRow.Hidden == False and P01.Cells(r, M02.Enable_Col) != '' and M06.IsIncludeMacro(Cmd):
                    SheetName=""
                    addressOffset = 0
                    res, SheetName, addressOffset = M06.GetIncludeArgs(Cmd, SheetName, addressOffset)
                    if M06.CheckIncludeSheet(SheetName, r):
                        for idx in vbForRange(0, M02.LED_CHANNELS - 1):
                            col = Get_LED_Nr_Column(idx)
                            LEDNr[idx] = LEDNr(idx) + PG.ThisWorkbook.Worksheets(SheetName).Cells(M02.SH_VARS_ROW, col)
                            if LEDNr(idx) > M06.MaxLEDNr(idx):
                                M06.MaxLEDNr[idx] = LEDNr(idx)
                            # 19.01.21:
                else:                
                    # Row is not activ
                    Clear_LED_Nr_Columns(r)
        if LEDNr(LEDs_Channel) > M06.MaxLEDNr(LEDs_Channel):
            M06.MaxLEDNr[LEDs_Channel] = LEDNr(LEDs_Channel)
            # 19.01.21:
    # Write the Last LED number to row 1 (SH_VARS_ROW)
    for Nr in vbForRange(0, M02.LED_CHANNELS - 1):
        Col = Get_LED_Nr_Column(Nr)
        M06.MaxLEDNr[Nr] = M06.MaxLEDNr(Nr) + UsedModules(LastusedChannel(Nr))
        P01.CellDict[M02.SH_VARS_ROW, Col] = M06.MaxLEDNr(Nr)
    P01.Application.EnableEvents = OldEvents
    _fn_return_value = M06.MaxLEDNr
    Clear_Formula_Errors()
    return _fn_return_value

def Get_LED_Nr(DefaultLedNr, Row, LED_Channel):
    LEDNr = String()
    #-----------------------------------------------------
    fn_return_value = int(DefaultLedNr)
    LEDNr = P01.Cells(Row, M25.LED_Nr__Col)
    LEDNrstr=str(LEDNr)
    if LEDNrstr != '':
        Pos = InStr(LEDNr, '-')
        if ( Pos < 1 ) :
            if Left(LEDNr, 1) == M02.SerialChannelPrefix:
                fn_return_value = int(P01.val(Mid(LEDNr, 2)))
                return fn_return_value
            fn_return_value = int(LEDNr) + M06.Start_LED_Channel(LED_Channel) #*HL
        else:
            if Left(LEDNr, Pos - 1) == LED_Channel:
                fn_return_value = int(P01.val(Mid(LEDNr, Pos + 1))) + M06.Start_LED_Channel(LED_Channel) #*HL
            else:
                # todo
                pass
    return fn_return_value

def Get_LED_Nr_Column(LED_Channel):
    #-----------------------------------------------------
    if LED_Channel == 0:
        fn_return_value = M25.LED_Nr__Col
    else:
        fn_return_value = M25.LED_TastCol + LED_Channel - 1
    return fn_return_value

def Clear_LED_Nr_Columns(r, ExceptCol=-1):
    Nr = int()
    #---------------------------------------------------------------------
    for Nr in vbForRange(0, M02.LED_CHANNELS - 1):
        Col = Get_LED_Nr_Column(Nr)
        if Col != ExceptCol:
            if Col == M25.LED_Nr__Col:
                if P01.Cells(r, Col).Formula != '=""':
                    P01.Cells(r, Col).Formula = '=""'
                    # 30.04.20: Using the formula ="" to prevent overlapping texts from the left cell
            else:
                if P01.Cells(r, Col).Value != '':
                    P01.Cells(r, Col).Value = ''

def FirstNotFormatedRow(StartRow):
    Row = int()
    fn_return_value = 0
    #-------------------------------------------------------------
    # Find the first row where the Enable_Col doesn't use the font "Wingdings"
    # The search starts with the giveb row and searches upwards.
    # Return 0 if the StartRow is already formated
    if P01.Cells(StartRow, M02.Enable_Col).Font.Name == 'Wingdings':
        return fn_return_value
    Row = StartRow
    while P01.Cells(Row, M02.Enable_Col).Font.Name != 'Wingdings' and Row > M02.FirstDat_Row:
        Row = Row - 1
    fn_return_value = Row
    return fn_return_value

def Format_Cells_to_Row(Row, UpdateAutofilter=True, AllRows=False):
    
    return #*HL
"""
    FirstNFormRow = int()
    #--------------------------------------------------------------------------------------------------------------------
    # Formating the unformated rows
    # - Wingdings in the Enable column and centeres in both directions
    # - For all other columns the horizontal alignement is copied fron the Head line
    #   and the vertical alignement is XlTop
    # - Border lines
    if AllRows:
        FirstNFormRow = M02.FirstDat_Row
    else:
        FirstNFormRow = FirstNotFormatedRow(Row)
    if FirstNFormRow > 0:
        #Debug.Print "Formating rows " & FirstNFormRow & " to " & Row ' Debug
        P01.Range(P01.Cells(FirstNFormRow, M02.Enable_Col), P01.Cells(Row, M02.Enable_Col)).Font.Name = 'Wingdings'
        P01.Range(P01.Cells(FirstNFormRow, M02.Enable_Col), P01.Cells(Row, M02.Enable_Col)).VerticalAlignment = xlCenter
        P01.Range(P01.Cells(FirstNFormRow, M02.Enable_Col), P01.Cells(Row, M02.Enable_Col)).HorizontalAlignment = xlCenter
        for c in vbForRange(M02.Enable_Col + 1, M30.LastColumnDatSheet()):
            #.Select ' Debug
            P01.Range(P01.Cells(FirstNFormRow, c), P01.Cells(Row, c)).HorizontalAlignment = P01.Cells(M02.Header_Row, c).HorizontalAlignment
            P01.Range(P01.Cells(FirstNFormRow, c), P01.Cells(Row, c)).VerticalAlignment = xlTop
            #If C = LEDs____Col Then .NumberFormat = "@" ' Text format to be able to enter "1-2"
            if c == M25.DCC_or_CAN_Add_Col or c == M25.SX_Channel_Col:
                P01.Range(P01.Cells(FirstNFormRow, c), P01.Cells(Row, c)).NumberFormat = '@'
                # Text format to be able to enter "1-2"
            if c == M25.Config__Col:
                P01.Range(P01.Cells(M02.FirstNFormRow, c), P01.Cells(Row, c)).Font.Name = 'Consolas'
            if c == M25.DCC_or_CAN_Add_Col:
                P01.Range(P01.Cells(FirstNFormRow, c), P01.Cells(Row, c)).WrapText = True
            # Gray background
            if (c == M25.Config__Col) or (M25.LED_Nr__Col <= c <= M25.LED_Nr__Col + M02.INTERNAL_COL_CNT - 1):
                P01.Range(P01.Cells(FirstNFormRow, c), P01.Cells(Row, c)).Interior.ThemeColor = xlThemeColorDark1
                P01.Range(P01.Cells(FirstNFormRow, c), P01.Cells(Row, c)).Interior.TintAndShade = - 4.99893185216834E-02
        M30.All_Borderlines(P01.Range(P01.Cells(FirstNFormRow, M02.Enable_Col), P01.Cells(Row, M30.LastColumnDatSheet())))
        if UpdateAutofilter:
            pass #*HL M15.Expand_Filter_to_all_used_Rows()
        #If UpdateAutofilter Then AutofilterAllColumns Row ' Deletes the filter settings ;-(
        """

def Format_All_Rows():
    #---------------------------
    return  #*HL

    M25.Make_sure_that_Col_Variables_match()
    Format_Cells_to_Row(M30.LastUsedRow(), True, True)

def Update_Sum_Func():
    #---------------------------
    # The Sum function in the filter column is used to detect changes in the autofilter
    #  to update the "Start LedNr"
    Debug.Print("Update_Sum_Func called")

    return #*HL
    
    P01.CellDict[M02.SH_VARS_ROW, M25.Filter__Col].FormulaR1C1 = '=SUM(R[1]C:R[' + str(M30.LastUsedRow()) + ']C)'
    

def Col_is_in_Range(c, r):
    #------------------------------------------------------
    fn_return_value = c >= r.Column and c <= r.Column + r.Columns.Count - 1
    return fn_return_value

def Range_is_Empty(r):
    c = Variant()
    #-----------------------------------------------------
    for c in r:
        if c != '':
            return fn_return_value
    fn_return_value = True
    return fn_return_value

def Select_Typ_by_Dialog(Target):
    OldEvents = Boolean()
    #------------------------------------------------------
    if not M25.Address_starts_with_a_Number(Target.Row):
        return
        # 03.02.20:
    OldEvents = P01.Application.EnableEvents
    P01.Application.EnableEvents = False
    Target.Select()
    if M25.Page_ID == 'Selectrix':
        F00.UserForm_Select_Typ_SX.setFocus(Target)
        F00.UserForm_Select_Typ_SX.Show()
        M02GV.Userform_Res = F00.UserForm_Select_Typ_SX.Userform_res
        if F00.UserForm_Select_Typ_SX.Userform_res !="":
            Target.set_value(F00.UserForm_Select_Typ_SX.Userform_res) #*HL        
    else:
        F00.UserForm_Select_Typ_DCC.setFocus(Target)
        F00.UserForm_Select_Typ_DCC.Show()
        M02GV.Userform_Res = F00.UserForm_Select_Typ_DCC.Userform_res
        if F00.UserForm_Select_Typ_DCC.Userform_res !="":
            Target.set_value(F00.UserForm_Select_Typ_DCC.Userform_res) #*HL
    P01.Application.EnableEvents = True
    #*HL if Userform_Res != '':
    #*HL     Target = Userform_Res
    P01.Application.EnableEvents = OldEvents

def Complete_Typ(Target, DialogIfEmpty=False):
    Txt = String()
    #----------------------------------------------------------------------------------------
    M09.Set_Tast_Txt_Var()
    if Len(Target) == 0:
        if DialogIfEmpty:
            Select_Typ_by_Dialog(Target)
        return
    if  M25.Page_ID == 'Selectrix':
        if UCase(Left(Target, 1)) == UCase(Left(M09.Tast_T, 1)):
            Txt = M09.Tast_T
            # ToDo: Language
    else:
        if UCase(Left(Target, 1)) == UCase(Left(M09.Red_T, 1)):
            Txt = M09.Red_T
        if UCase(Left(Target, 1)) == UCase(Left(M09.Green_T, 1)):
            Txt = M09.Green_T
    if UCase(Left(Target, 1)) == UCase(Left(M09.OnOff_T, 1)):
        Txt = M09.OnOff_T
    if Txt != '':
        if Target != Txt:
            Target = Txt
    else:
        # 23.06.20: Speed up (took 45 seconds at a larger configuration with 130 LEDs and a lot od DCC (Harald))
        Select_Typ_by_Dialog(Target)

def AutofilterAllColumns(EndRow):
    return #*HL
    #----------------------------------------------------
    # Activate the autofilter for all columns
    if P01.ActiveSheet.AutoFilterMode:
        P01.Range(P01.Cells(M02.Header_Row, M02.Enable_Col), P01.Cells(EndRow, M30.LastColumnDatSheet())).Cells.AutoFilter() # remove
        P01.Range(P01.Cells(M02.Header_Row, M02.Enable_Col), P01.Cells(EndRow, M30.LastColumnDatSheet())).Cells.AutoFilter() # put back
    else:
        P01.Range(P01.Cells(M02.Header_Row, M02.Enable_Col), P01.Cells(EndRow, M30.LastColumnDatSheet())).Cells.AutoFilter() # first time
    return

def Correct_Autofilter():
    #-------------------------------
    # Call this manualy in case the filter is corrupted
    AutofilterAllColumns(M30.LastUsedRow())

def Clear_Formula_Errors():
    return #*HL
    
    #rngCell = Range()

    #i = int()
    #-------------------------------
    for rngCell in P01.ActiveSheet.Used.Range:
        for i in vbForRange(1, 7):
            rngCell.Errors.Item[i].Ignore = True

def Move_Active_Cell():
    #-----------------------------
    global PriorCell
    # VB2PY (UntranslatedCode) On Error GoTo JustActivete
    if not PriorCell is None:
        if PriorCell.Row == P01.ActiveCell().Row:
            Delta = P01.ActiveCell().Column - PriorCell.Column
            if Abs(Delta) == 1:
                P01.Range(P01.ActiveCell().Address).Offset(0, Delta).Activate()
                return
    P01.Range(P01.ActiveCell().Address).Offset(0, 1).Activate()

def Proc_Typ_Col(Target):
    RefCol = int()
    #----------------------------------------------
    # Open the Typ Dialog if the "DCC Adresse" or "Bitposition" Cell is filled
    # but the "Typ" cell is empty
    if (M25.Page_ID == 'DCC') or (M25.Page_ID == 'CAN') or (M25.Page_ID == 'LNet'):
        RefCol = M25.DCC_or_CAN_Add_Col
    elif (M25.Page_ID == 'Selectrix'):
        RefCol = M25.SX_Bitposi_Col
    else:
        P01.MsgBox('Internal error:',' Unknown M25.Page_ID in \'Proc_Typ_Col\'', vbCritical)
        M30.EndProg()
    if P01.Cells(Target.Row, RefCol) != '' and Target == '':
        Select_Typ_by_Dialog(Target)
        Move_Active_Cell()

def Hide_Unhide_Selected_Rows(Hide):
    OldUppdating = Boolean()

    OldEvents = Boolean()
    #-----------------------------------------------------
    # Is called if rows are hidden or unhiden by event´
    OldUppdating =  P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = False
    OldEvents =  P01.Application.EnableEvents
    P01.Application.EnableEvents = False
    P01.Selection.EntireRow.Hidden = Hide
    Update_Start_LedNr()
    P01.Application.EnableEvents = OldEvents
    P01.Application.ScreenUpdating = OldUppdating

def myHideRows_Event():
    #----------------------------
    # Is called on event if rows are hidden
    # Must be enabled in Workbook_Open() which is located in "DieseArbeismappe"
    Hide_Unhide_Selected_Rows(True)

def myUnhideRows_Event():
    #------------------------------
    # Is called on event if rows are shown
    # Must be enabled in Workbook_Open() which is located in "DieseArbeismappe"
    Hide_Unhide_Selected_Rows(False)

def Option_Dialog(first_page_only=False):
    #-------------------------
    M30.Check_Version()
    F00.UserForm_Options.Show(first_page_only=first_page_only)

def ClearSheet():
    #----------------------
    # if M30.MsgBoxMov(M09.Get_Language_Str('Wollen Sie alle Einträge dieser Seite löschen?'), vbQuestion + vbYesNo, M09.Get_Language_Str('Seite Löschen?')) == vbYes:
    res = M30.MsgBoxMov(M09.Get_Language_Str('Wollen Sie  diese Seite komplett löschen?\nja - die Seite wird entfernt\nnein - nur der Inhalt der Seite wird gelöscht\nAbbrechen - es wird nichts gelöscht '), vbQuestion + vbYesNoCancel, M09.Get_Language_Str('Seite Löschen?'))
    if res == vbYes:
        # remove sheet
        P01.ActiveSheet.Delete()
    
    elif res == vbNo:
        P01.ActiveSheet.clearSheet()
        __set_column_width(P01.ActiveSheet)
    else:
        pass
        """
        OldUppdating =  P01.Application.ScreenUpdating
        P01.Application.ScreenUpdating = False
        OldEvents =  P01.Application.EnableEvents
        P01.Application.EnableEvents = False
        M25.Make_sure_that_Col_Variables_match()
        P01.Rows(M02.FirstDat_Row + ':' + M30.LastUsedRow()).ClearContents()
        P01.RowDict[M02.FirstDat_Row + ':' + M30.LastUsedRow()].Hidden = False
        P01.Rows('33:' + M30.LastUsedRow()).Delete(Shift=xlUp)
        P01.Cells(M02.FirstDat_Row, 1).Activate()
        P01.Application.GoTo(P01.ActiveCell(), True)
        ResetTestButtons(False)
        #*HL Del_Icons_in_IconCol()
        P01.Application.EnableEvents = OldEvents
        P01.Application.ScreenUpdating = OldUppdating
        """
        
        
def __set_column_width(sheet):
    M01.set_columnwidth(sheet)

def Show_Help():
    #---------------------
    P01.Application.EnableEvents = True
    ## VB2PY (CheckDirective) VB directive took path 1 on 1
    
    #P01.Shell('Explorer https://wiki.mobaledlib.de/anleitungen/spezial/programmgenerator')
    PG.global_controller.call_helppage()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cancel - ByRef 
def Proc_DoubleCkick(Sh, Target, Cancel):
    #----------------------------------------------------------------------------------------------
    M25.Make_sure_that_Col_Variables_match(Sh)
    if M28.Is_Data_Sheet(P01.ActiveSheet):
        if Target.Row >= M02.FirstDat_Row:
            if (Target.Column == M25.MacIcon_Col) or (Target.Column == M25.LanName_Col) or (Target.Column == M25.Config__Col):
                Cancel = True
                M09SM.SelectMacros()
            elif (Target.Column == M25.Inp_Typ_Col):
                Cancel = True
                Select_Typ_by_Dialog(Target)

def Arduino_Button_StartPage():
    #------------------------------------
    UserForm_Protokoll_Auswahl.Show()

def Complete_Addr_Column_with_InCnt(r):
    #Target = P01.Range()
    EndAddr = 0

    InCnt = int()
    #----------------------------------------------------
    # Is called by event if the DCC address or the Selectrix chanel is changed
    M09.Set_Tast_Txt_Var()
    Target = P01.Cells(r, M25.DCC_or_CAN_Add_Col + M25.SX_Channel_Col)
    #Debug.Print "Complete_Addr_Column_with_InCnt"
    InCnt = P01.val(P01.Cells(r, M25.InCnt___Col))
    if InCnt > 0:
        Addr = M25.Get_First_Number_of_Range(r, Target.Column)
        if Addr != '' and P01.val(Addr) >= 0:
            SBit_Str = ''
            EBit_Str = ''
            Inp_Typ = P01.Cells(r, M25.Inp_Typ_Col)
            if Inp_Typ != '':
                if M25.Page_ID == 'Selectrix':
                    BitPos = P01.val(P01.Cells(r, M25.SX_Bitposi_Col))
                    if BitPos > 0 and BitPos <= 8:
                        EBit_Pos = BitPos + InCnt - 1
                        EndAddr = Addr + Int(EBit_Pos / 8)
                        if EBit_Pos % 8 == 0:
                            EBit_Str = '.8'
                            EndAddr = EndAddr - 1
                        else:
                            EBit_Str = '.' + str(EBit_Pos % 8)
                        SBit_Str = '.' + str(BitPos)
                else:
                    if Inp_Typ == M09.Red_T or Inp_Typ == M09.Green_T:
                        EndAddr = Addr
                        for i in vbForRange(1, InCnt):
                            Inp_Typ = M06.Get_Next_Typ(Inp_Typ)
                            if Inp_Typ == M09.Red_T and i < InCnt:
                                EndAddr = EndAddr + 1
                    else:
                        EndAddr = Addr + InCnt - 1
            if Addr != EndAddr and EndAddr != 0 or  ( InCnt > 1 and EBit_Str != '' ) :
                Target = str(Addr) + SBit_Str + ' - ' + str(EndAddr) + EBit_Str
            else:
                Target = Addr

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Global_Worksheet_SelectionChange(Target):
    global PriorCell
    #-----------------------------------------------------------------------
    # Is called by event if the worksheet selection has changed
    if Target.CountLarge == 1:
        if Target.Row >= M02.FirstDat_Row and Target.Row <= M30.LastUsedRow():
            M25.Make_sure_that_Col_Variables_match()
            P01.Application.EnableEvents = False
            if M02.DEBUG_CHANGEEVENT:
                #Debug.Print(Format(Time, 'hh.mm.ss') + ' SelectionChange')
                pass
                # Debug
            if (Target.Column == M02.Enable_Col):
                if Target.Value == '':
                    Target.Value = ChrW(M02.Hook_CHAR)
                else:
                    Target.Value = ''
                #BeepThis2('Windows Balloon.wav')
                Update_Start_LedNr()
                P01.ActiveCell().Offset(0, 1).Activate() #P01.Range(P01.ActiveCell.Address).Offset(0, 1).Activate() #*HL
            elif (Target.Column == M25.Inp_Typ_Col):
                Proc_Typ_Col(Target)
            elif (Target.Column == M25.Config__Col):
                if Target == '' and not M30.First_Change_in_Line(Target):
                    M09SM.SelectMacros()
            elif (M25.LED_Nr__Col <= Target.Column <= M25.LED_Nr__Col + M02.INTERNAL_COL_CNT - 1):
                # The LEDs, InCnt, ... columns should not be changed easyly It's only possible if it is selected from the right side
                # VB2PY (UntranslatedCode) On Error Resume Next
                PriorCol = PriorCell.Column
                # VB2PY (UntranslatedCode) On Error GoTo 0
                if PriorCol <= Target.Column:
                    #P01.Range(P01.ActiveCell.Address).Offset(0, M25.LEDs____Col - Target.Column - 1).Activate() #*HL
                    P01.ActiveCell().Offset(0, M25.LEDs____Col - Target.Column - 1).Activate() #*HL
            PriorCell = P01.ActiveCell()
            P01.Application.EnableEvents = True
        elif Target.Row == M02.Header_Row:
            if not Target.Comment is None:
                Target.Comment.Shape.Top = P01.ActiveWindow.Visible.Range.Top
                Target.Comment.Shape.Left = P01.ActiveCell().Left
                #.Visible = True

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
def Global_Worksheet_Change(Target):
    OldUppdating = Boolean()

    OldEvents = Boolean()

    Row = int()
    #--------------------------------------------------------------
    # This function is called if the worksheet is changed.
    # It performs several checks after a user input depending form the column of the changed cell:
    OldUppdating = P01.Application.ScreenUpdating
    OldEvents = P01.Application.EnableEvents
    P01.Application.ScreenUpdating = False
    P01.Application.EnableEvents = False
    M25.Make_sure_that_Col_Variables_match(Switch_back_Target=Target)
    Row = Target.Row
    if Target.CountLarge == 1:
        if Row >= M02.FirstDat_Row:
            if not P01.IsError(Target.Value):
                if Target.Value != '' and M30.First_Change_in_Line(Target):
                    Format_Cells_to_Row(Row + M02.SPARE_ROWS)
                    P01.CellDict[Row, M02.Enable_Col] = ChrW(M02.Hook_CHAR)
            if (Target.Column == M25.LED_Nr__Col) or (Target.Column == M25.LEDs____Col) or (M25.LED_Cha_Col <= Target.Column <= M25.LED_Cha_Col + M02.LED_CHANNELS - 1):
                Update_Start_LedNr()
                Update_TestButtons(Row)
            elif (Target.Column == M25.SX_Bitposi_Col):
                Complete_Addr_Column_with_InCnt(Row)
                Update_TestButtons(Row)
            elif (Target.Column == M25.Inp_Typ_Col):
                Complete_Typ(Target)
                Complete_Addr_Column_with_InCnt(Row)
                Update_TestButtons(Row)
                Update_StartValue(Row)
                if Target == '':
                    M27.Del_Icons(Target)
                    # 22.10.21:
            elif (Target.Column == M25.DCC_or_CAN_Add_Col) or (Target.Column == M25.SX_Channel_Col):
                if M25.Page_ID == 'DCC' or M25.Page_ID == 'LNet':
                    Complete_Addr_Column_with_InCnt(Row)
                    Update_TestButtons(Row)
                    Update_StartValue(Row)
                else:
                    #P01.ActiveCell().Offset(0, 1).Select        #' 15.10.20:
                    pass
            elif (Target.Column == M25.InCnt___Col):
                Complete_Addr_Column_with_InCnt(Row)
                Update_TestButtons(Row)
    else:
        #If Target. P01.Rows(1).P01.Cells.Count <> MAX_COLUMNS And Target.Columns(1).P01.Cells.Count <> MAX_ROWS Then  ' Not a whole row/column because it would take long and we dont wan't to get the hook if lines are deleted
        # Adapt the first row to fit in the data range
        StartRow = Row
        if StartRow < M02.FirstDat_Row:
            StartRow = M02.FirstDat_Row
        # Don't fill in hooks if cells in the enable column should be changed/deleted
        if Target.Columns(1).Cells.Count != M02.MAX_ROWS:
            if Range_is_Empty(Target):
                # Delete the icons                                     ' 22.10.21:
                if Col_is_in_Range(M25.Inp_Typ_Col, Target):
                    if Col_is_in_Range(M25.MacIcon_Col, Target):
                        M27.Del_Icons(P01.Range(P01.Cells(Target.Row, M25.Inp_Typ_Col), P01.Cells(Target.Row + Target. P01.Rows.Count - 1, M25.MacIcon_Col)))
                    else:
                        M27.Del_Icons(P01.Range(P01.Cells(Target.Row, M25.Inp_Typ_Col), P01.Cells(Target.Row + Target. P01.Rows.Count - 1, M25.Inp_Typ_Col)))
                else:
                    if Col_is_in_Range(M25.MacIcon_Col, Target):
                        M27.Del_Icons(P01.Range(P01.Cells(Target.Row, M25.MacIcon_Col), P01.Cells(Target.Row + Target. P01.Rows.Count - 1, M25.MacIcon_Col)))
            else:
                if not Col_is_in_Range(M02.Enable_Col, Target):
                    P01.Range[P01.Cells(StartRow, M02.Enable_Col), P01.Cells(Row + Target. P01.Rows.Count - 1, M02.Enable_Col)] = ChrW(M02.Hook_CHAR)
        # Format new cells at the end
        EndRow = Row + Target.Rows.Count - 1 + M02.SPARE_ROWS
        if EndRow > M30.LastUsedRow() + M02.SPARE_ROWS:
            EndRow = M30.LastUsedRow()
            # Protection if whole columns are deleted
        if EndRow >= M02.FirstDat_Row:
            Format_Cells_to_Row(EndRow)
        Update_Start_LedNr()
        #End If
    if M02.DEBUG_CHANGEEVENT:
        Debug.Print(P01.Format(Time, 'hh.mm.ss') + ' Worksheet_Change ' + Target.CountLarge)
        # Debug
    P01.Application.EnableEvents = OldEvents
    P01.Application.ScreenUpdating = OldUppdating

def Global_Worksheet_Activate():
    #-------------------------------------
    if M02.DEBUG_CHANGEEVENT:
        Debug.Print(P01.ActiveSheet.Name + ' Global_Worksheet_Activate event')

def Global_Worksheet_Calculate():
    #--------------------------------------
    # This function is called if a function is entered in the Excel sheet or if data
    # are changed which influece a formula
    if M02.DEBUG_CHANGEEVENT:
        Debug.Print('Global_Worksheet_Calculate()')
        # Debug
    #Update_Start_LedNr                                                      ' 29.04.20: Disabled because I don't understand why it should be called here

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Row - ByVal 
def Update_StartValue(Row):
    storeStatusType = Integer()

    Channel_or_define = String()

    AddrStr = String()

    Addr = int()

    AddrColumn = int()
    
    Inp_TypR = None
    #-----------------------------------------------
    M25.Make_sure_that_Col_Variables_match()
    if ( M25.Page_ID == 'DCC' )  or  ( M25.Page_ID == 'CAN' )  or  ( M25.Page_ID == 'LNet' ) :
        AddrColumn = M25.DCC_or_CAN_Add_Col
    elif  ( M25.Page_ID == 'Selectrix' ) :
        AddrColumn = M25.SX_Channel_Col
    else:
        return
    AddrStr = P01.Cells(Row, AddrColumn)
    if IsNumeric(AddrStr):
        # 03.04.20:
        Addr = P01.val(AddrStr)
    else:
        Addr = - 2
        # it's a variable
        Channel_or_define = AddrStr
    if Addr >= 0:
        Inp_TypR = P01.Cells(Row, M25.Inp_Typ_Col)
        if M25.Page_ID == 'DCC' or M25.Page_ID == 'LNet':
            # 11.10.20: Otherwise the input type is requested before the bit position on the SX page
            Complete_Typ(Inp_TypR, True)
            # Check Inp_Typ. If not valid call the dialog
    else:
        Channel_or_define = AddrStr
    storeStatusType = M06.Get_Store_Status(Row, Addr, Inp_TypR, Channel_or_define)
    if (storeStatusType == M02.SST_COUNTER_OFF):
        return
    elif (storeStatusType == M02.SST_COUNTER_ON):
        return
    elif (storeStatusType == M02.SST_S_ONOFF) or (storeStatusType == M02.SST_TRIGGER):
        return
    else:
        # inform user later, when downloading to arduino
        #If P01.Cells(Row, Start_V_Col) = AUTOSTORE_ON Then P01.Cells(Row, Start_V_Col) = ""          '01.05.20: Commneted in Mail from Jürgen
        return

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Row - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: onValue=0 - ByVal 
def Update_TestButtons(Row, onValue=0, First_Call=True, redraw=False):
    
    global Global_Rect_List
    #objButton = Shape()

    Addr = Variant()

    ButtonPrefix = String()

    isSX = Variant()

    isDCC = Variant()

    incAddress = Variant()

    toggle = Boolean()

    i = Variant()

    InCnt = Variant()

    BitPos = Variant()

    ButtonCount = Variant()

    TextOffset = Variant()

    TextInc = Variant()

    AltTextOffset = Variant()

    Direction = Variant()

    ColorOffset = Variant()

    ColorInc = Variant()

    PixelOffset = Integer()

    TargetColumn = Variant()

    AddrColumn = int()

    OldRect_List = vbObjectInitialize(objtype=Long)

    OldRect_Cnt = int()

    LastRow = int()

    Height = Integer()

    NewCreated = Boolean()

    Used_OldRect = int()
    #-----------------------------------------------
    Debug.Print ("Update_TestButtons(" + str(Row) + ")")
    isSx = M25.Page_ID == 'Selectrix'
    toggle = False
    # 01.08.21: Jürgen bugfix
    # only for the DCC, LNet and Selectrix sheet
    if M25.Page_ID == 'DCC' or M25.Page_ID == 'LNet':
        # 24.04.23: Juergen
        AddrColumn = M25.DCC_or_CAN_Add_Col
    elif isSx:
        AddrColumn = M25.SX_Channel_Col
    else:
        return
    PixelOffset = 35
    PixelOffset = 50 # for tksheet
    # 25.03.21:
    LastRow = M30.LastUsedRow()
    i = 1
    if First_Call and not redraw:
        Global_Rect_List = vbObjectInitialize(((1, LastRow),), str)
        while i <= P01.ActiveSheet.Shapes.Count():
            #  is it a SendButton Shape?
            if P01.ActiveSheet.Shapes.getShape(i).OnAction == 'DCCSend':
                RectRow = P01.ActiveSheet.Shapes.getShape(i).TopLeftCell_Row
                if RectRow <= LastRow:
                    Global_Rect_List[RectRow] = Global_Rect_List(RectRow) + str(i) + ' '
                if P01.ActiveSheet.Shapes.getShape(i).TopLeftCell_Row == Row:
                    #P01.ActiveSheet.Rectangles(i).Delete                   ' 25.03.21:
                    OldRect_List = vbObjectInitialize((OldRect_Cnt,), Variant, OldRect_List)
                    OldRect_List[OldRect_Cnt] = i
                    OldRect_Cnt = OldRect_Cnt + 1
                else:
                    # find orphans
                    Addr = M25.Get_First_Number_of_Range(P01.ActiveSheet.Shapes.getShape(i).TopLeftCell_Row, AddrColumn)
                    if Addr == '':
                        P01.ActiveSheet.Shapes.Delete(i)
                        i = i - 1
            i = i + 1
    else:
        if redraw:
            OldRect_Cnt = 0
        else:
            OldRect_Cnt = 0
            if Global_Rect_List[Row] == '':
                return
            Rect_List_In_Row = Split(Trim(Global_Rect_List(Row)), ' ')
            OldRect_Cnt = UBound(Rect_List_In_Row) + 1
            OldRect_List = vbObjectInitialize((OldRect_Cnt - 1,), Variant)
            for i in vbForRange(0, OldRect_Cnt - 1):
                OldRect_List[i] = CLng(Rect_List_In_Row(i))
    InCnt = P01.val(P01.Cells(Row, M25.InCnt___Col))
    #print("UpdateTestButton Row:",Row," Col:",M25.InCnt___Col," InCnt:",InCnt)
    if InCnt < 1:
        return
    ButtonCount = 1 * InCnt
    Direction = 1
    # start with "R"=0 or "G"=1
    ColorOffset = 0
    # red
    ColorInc = 1
    # take next color for next address
    TextInc = 1
    M25.Make_sure_that_Col_Variables_match()
    M09.Set_Tast_Txt_Var()
    # Set the global variables Red_T, Green_T, ...
    # 03.04.20:
    Addr = M25.Get_First_Number_of_Range(Row, AddrColumn)
    #print("UpdateTestButton Row:",Row," Col:",AddrColumn," Addr:",Addr)
    if Addr == '' or P01.val(Addr) < 0:
        return
    # 04.05.20: Added: Or Val(Addr) < 0 to fix problems with the error returned by Get_First_Number_of_Range() (Mail from Jürgen)
    if isSx:
        if P01.Cells(Row, M25.SX_Bitposi_Col) != '':
            BitPos = int(P01.Cells(Row, M25.SX_Bitposi_Col))
        if ( BitPos < 1 or BitPos > 8 ) :
            return
        Addr = Addr * 8 +  ( BitPos - 1 )
        TargetColumn = M25.Inp_Typ_Col
        # 11.10.20: Old:  SX_Bitposi_Col  Warum diese Spalte ?
        TextOffset = BitPos
        # starts with bitoffset
        AltTextOffset = BitPos
        # starts with bitoffset
        select_variable_ = P01.Cells(Row, M25.Inp_Typ_Col) #*HL.Text
        if (select_variable_ == M09.Tast_T):
            incAddress = True
            if InCnt == 1:
                # sx buttons are always yellow
                ColorOffset = ColorOffset + 2
        elif (select_variable_ == M09.OnOff_T):
            toggle = True
            ColorInc = 0
            incAddress = True
            ColorOffset = ColorOffset + 1
        else:
            return
            # 11.10.20:
    else:
        TargetColumn = M25.Inp_Typ_Col
        TextOffset = 1
        # starts with this number for button text
        AltTextOffset = 2
        select_variable_ = P01.Cells(Row, M25.Inp_Typ_Col)  #*HL
        if (select_variable_ == M09.Red_T):
            Direction = 0
        elif (select_variable_ == M09.Green_T):
            #incAddress = True                              ' 07.05.20: Disabled to be able to start with "Green". Otherwise the second, third, ... button will be shifted by one
            ColorOffset = ColorOffset + 1
        elif (select_variable_ == M09.OnOff_T):
            toggle = True
            incAddress = True
            TextOffset = 0
            AltTextOffset = TextOffset + 1
            TextInc = 0
            ColorInc = False
        if InCnt > 1:
            TextOffset = 0
            AltTextOffset = 1
    Height = P01.Cells(Row, TargetColumn).Height
    if Height > 26: #13
        Height = 26 
    # increase minimum column size if needed
    #*HLi = 1 + PixelOffset + ButtonCount * Height
    #*HLif P01.Cells(Row, TargetColumn).Width < i:
    #*HL    factor = P01.Cells(Row, TargetColumn).Width / P01.Columns(TargetColumn).ColumnWidth
    #*HL    P01.Range[P01.Cells(1, TargetColumn), P01.Cells(1, TargetColumn)].ColumnWidth = WorksheetFunction.RoundUp(i / factor, 1)
    if toggle:
        ButtonPrefix = 'B'
    else:
        ButtonPrefix = 'S'
    # 25.04.23: Juergen button or switch
    for i in vbForRange(1, ButtonCount):
        if Used_OldRect < OldRect_Cnt:
            objButton = P01.ActiveSheet.Shapes.getlist()[OldRect_List(Used_OldRect)-1]
            Used_OldRect = Used_OldRect + 1
        else:
            #*HLobjButton = P01.ActiveSheet.Shapes.AddShape(msoShapeRectangle, Row, TargetColumn, 0, 0, 0, 0)
            NewCreated = True
        # 19.01.21: Jürgen
        isSetToOn = False
        # 26.03.21: Jürgen, otherwise lines with more than one toggle button are displayed wrong
        if toggle:
            if ( onValue &  ( 2 **  ( i - 1 ) ) )  != 0:
                isSetToOn = True
        objButton_Name = ButtonPrefix + P01.Format(Addr, '0000') + '-' + P01.Format(Direction, '00') + '-' + P01.Format(ColorOffset, '00') + '-' + str(TextOffset)
        if NewCreated:
            objButton_Left = P01.Cells(Row, TargetColumn).Left + PixelOffset +  ( i - 1 )  * Height
            objButton_Top = P01.Cells(Row, TargetColumn).Top + 1
            objButton_Height = Height - 2
            objButton_Width = Height - 2
            objButton = P01.ActiveSheet.Shapes.AddShape(msoShapeRectangle, objButton_Left, objButton_Top, objButton_Height, objButton_Width, Fill="#FF0000", name=objButton_Name)
        
        if P01.Cells(Row, M25.Inp_Typ_Col).Text == M09.OnOff_T:
            if objButton.TextFrame2.TextRange.Text != str(TextOffset):
                objButton.TextFrame2.TextRange.Text = str(TextOffset)
        else:
            if objButton.TextFrame2.TextRange.Text != ' ':
                objButton.TextFrame2.TextRange.Text = ' '
                # No text because it's confusing if 0/1 is used for OnOff switches
        if NewCreated:
            objButton.OnAction = 'DCCSend'
            #objButton.DrawingObject.Border.Color = rgb(0, 0, 0)
            #objButton.TextFrame2.Text.Range.ParagraphFormat.Alignment = msoAlignCenter
        objButton.Fill.ForeColor.rgb = GetButtonColor(ColorOffset)
        if toggle:
            altText = ButtonPrefix + P01.Format(Addr, '0000') + '-' + P01.Format(1 - Direction, '00') + '-' + P01.Format(ColorOffset + 1, '00') + '-' + str(AltTextOffset)
            if isSetToOn:
                objButton.AlternativeText = objButton.Name
                objButton.Name = altText
                #*HLobjButton.TextFrame2.Text.Range.Text = Mid(objButton.Name, 13, 1)
                objButton.TextFrame2.TextRange.Text = Mid(objButton.Name, 13, 1)
                #*HLobjButton.Fill.ForeColor.rgb = GetButtonColor(P01.val(Mid(objButton.Name, 10, 2)))
                objButton.Fill.ForeColor.rgb = GetButtonColor(P01.val(Mid(objButton.Name, 10, 2)))
            else:
                objButton.AlternativeText = altText
        else:
            objButton.AlternativeText = ''
        TextOffset = TextOffset + TextInc
        AltTextOffset = AltTextOffset + TextInc
        if incAddress:
            Addr = Addr + 1
        else:
            if ( Direction == 1 ) :
                Addr = Addr + 1
                Direction = 0
            else:
                Direction = 1
        ColorOffset = ValidateColorIndex(ColorOffset + ColorInc)
        objButton.updateShape()
    for i in vbForRange(Used_OldRect, OldRect_Cnt - 1):
        P01.ActiveSheet.Shapes.Delete(OldRect_List(i))

def ResetTestButtons(keepStatus):
    
    Row = Variant()

    First_Call = Boolean()
    #----------------------------------------------------
    # resets the on/off state of DCC buttons
    # trigger buttons are not affected
    #
    # sets button to on if StartValue > 0
    # sets button to off if StartValue = 0
    # if stats P01.value not set and keepStatus = false set button to off
    # otherwise keep current on/off state
    #
    First_Call = True
    for Row in vbForRange(M02.FirstDat_Row, M30.LastUsedRow()):
        if P01.Cells(Row, M25.Start_V_Col) != '':
            sv = P01.val(P01.Cells(Row, M25.Start_V_Col))
            Update_TestButtons(Row, sv, First_Call)
            First_Call = False
        else:
            if keepStatus == False:
                Update_TestButtons(Row, First_Call=First_Call)
                First_Call = False

def Test_ResetTestButtons():
    Start = Double()
    #UT--------------------------------
    # Org: 12- 13 Sek
    Global_Rect_List = vbObjectInitialize((0,), Variant)
    P01.Application.ScreenUpdating = False
    Make_sure_that_Col_Variables_match()
    Start_ms_Timer()
    Start = Now
    ResetTestButtons(False)
    Debug.Print(Now + ' Duration: ' + Format(Now - Start, 'hh:mm:ss') + ' Millis:' + Get_ms_Duration())

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Index - ByVal 
def GetButtonColor(Index):
    #----------------------------------------------------------
    if (Index == 0):
        fn_return_value = P01.rgb2tkcolor(255, 128, 128)
    elif (Index == 1):
        fn_return_value = P01.rgb2tkcolor(128, 255, 128)
    elif (Index == 2):
        fn_return_value = P01.rgb2tkcolor(255, 255, 128)
    else:
        fn_return_value = P01.rgb2tkcolor(255, 255, 255)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Index - ByVal 
def ValidateColorIndex(Index):
    #------------------------------------------------------
    # currently color 0..3 are P01.valid
    fn_return_value = Index % 4
    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit

