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

#from proggen.M02_Public import *
#from proggen.M06_Write_Header_LED2Var import *
#from proggen.M06_Write_Header_Sound import *
#from proggen.M06_Write_Header_SW import *
#from proggen.M08_ARDUINO import *
#from proggen.M09_Language import *
#from proggen.M09_SelectMacro_Treeview import *
#from proggen.M10_Par_Description import *
#from proggen.M20_PageEvents_a_Functions import *
#from proggen.M25_Columns import *
#from proggen.M27_Sheet_Icons import *
#from proggen.M28_divers import *
#from proggen.M30_Tools import *
#from proggen.M60_CheckColors import *
#from proggen.M80_Create_Mulitplexer import *

#from ExcelAPI.P01_Workbook import *

import proggen.M02_Public as M02
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header as M06
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
#import proggen.M07_COM_Port as M07
#import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_SelectMacro_Treeview as M09SMT
import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80
import proggen.D06_Userform_House as D06
import proggen.D07_Userform_Other as D07

import ExcelAPI.P01_Workbook as P01

from ExcelAPI.X01_Excel_Consts import *


""" - Bei Effekten welche einzelne LEDs ansteuern muss die Adressierung der
   LEDs anders gemacht werden.
 - Die LED Nummer darf nicht immer nach einer Zeile erhöht werden.
 - Wenn danach eine RGB Zeile kommt, dann wird die die Nummer erhöht
 - Es muss auch möglich sein, dass mehrere Zeilen den selben LED Kanal ansprechen
   z.B. bei der Sound Funktion. => Es gibt keine Überprüfung auf doppelte Belegung
 - Mit der "Kommetar" Funktion "End_Single_LEDs"  kann man die Nummer erhöhen kann wenn danach wieder eine
   Funktion kommt welche einzelne LEDs anspricht.
   - Das ist alles zu Kompliziert
   - Es währe besser wenn automatisch die nächste RGB LED Nummer gewählt würde.
   - Nur bei Funktionen wie der Sound Funktion benötigt man einen Befehl zum weiter schalten
 - Pattern Configurator: Startkanal, Anzahl der Kanäle
 - Eintrag in der LEDs Spalte: Andreaskreuz: C1 => 1-2, C2 => 2-3, C3 => 3-4
   hier sollen auch größere Nummern möglich sein 5-6
   Eine größere Startnummer benötigt man dann wenn eine Patternfunktion z.B. 4 LEDs benutzt.
   Dann kann man mit 5-6 die letzten beiden LEDs des zweiten WS2811 ansprechen.
   Das ginge aber auch mit NextLED und 2-3
 Neuer Ansatz:
 - Die LED Kanäle müssen wie beim Haus immer in aufsteigender Reihenfolge angegeben werden
   Wenn eine kleinere Nummer als die Vorangegangene verwendet wird, dann wird damit das nächste
   WS2811 Modul angesprochen.
 - Funktionen wie die Sound Befehle bekommen ein Flag mit dem verhindert wird, das
   das nächste Modul verwendet wird. In der Tabelle kann man das so markieren: "^ C1-2"
   Wenn ein Befehl ausgewählt wurde bei dem die Kanäle mit den vorangegangenen Überlappen,
   Dann wird der User gefragt ob er die gleiche StartLedNr verwenden will wie die vorangegange Zeile.
   Das funktioniert aber nur wenn einzel Adressierte LEDs Verwendet werden (C1-2)
 - Befehle welche die RGB LEDs am Stück und nicht als drei einzelne Kanäle ansprechen sorgen immer
   dafür dass die nächste StartLedNr verwendet wird.

"""

__HeadRow = 3

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Res - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: LEDs - ByRef 
def __Special_ConstrWarnLight(Res, LEDs):
    _ret = ""
    Parts = Variant()

    Param = Variant()

    Ret = String()

    FlashFunct = Boolean()

    LED_Channel = String()
    #--------------------------------------------------------------------------------------------
    # ConstrWarnLight(LED,InCh, LEDcnt, MinBrightness, MaxBrightness, OnT, WaitT, WaitE)
    #          Param: 0   1     2       3              4              5    6      7
    LED_Channel = Split(Res, '$')(1)
    Parts = Split(Replace(Split(Res, '$')(0), ')', ''), '(')
    Param = Split(Parts(1), ',')
    if P01.val(Param(6)) > 0:
        FlashFunct = True
        Ret = 'ConstrWarnLightFlash'
    else:
        Ret = 'ConstrWarnLight'
    Ret = Ret + Trim(Param(2)) + '(' + Trim(Param(0)) + ', ' + Trim(Param(1)) + ', ' + Trim(Param(3)) + ', ' + Trim(Param(4)) + ', ' + Trim(Param(5)) + ', '
    if FlashFunct:
        Ret = Ret + Trim(Param(6)) + ', '
    Ret = Ret + Trim(Param(7)) + ')' + '$' + LED_Channel
    _ret = Ret
    LEDs = 'C1-' + Trim(Param(2))
    return _ret, LEDs

def __Test_Special_ConstrWarnLight():
    Res = String()

    LEDs = String()
    #UT---------------------------------------
    # ConstrWarnLight(LED,InCh, LEDcnt, MinBrightness, MaxBrightness, OnT, WaitT, WaitE)
    Res = 'ConstrWarnLight(#LED,#InCh, 6, 20, 255, 100 ms, 0 ms, 300 ms)'
    Res, LEDs = __Special_ConstrWarnLight(Res, LEDs)
    Debug.Print(Res + 'LEDs:' + LEDs)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Macro - ByVal 
def __Proc_General_With_Other_Par(Macro, Description, LedChannels, Show_Channel, LED_Channel, Def_Channel):
    _ret = ""
    Parts = Variant()

    Res = String()

    Param = Variant()
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if Macro == '':
        return _ret
    Parts = Split(Replace(Macro, ')', ''), '(')
    Param = Split(Parts(1), ',')
    # IF statement added by Misha 18-4-2020                                   ' 14.06.20: Added from Mishas version
    if Left(Macro, Len('Multiplexer')) == 'Multiplexer':
        UserForm_Create_Multiplexer = D07.UserForm_Other() #*HL dummy - multiplexer not implemented
        UserForm_Create_Multiplexer.Show_UserForm_Other(Parts(1), Parts(0), Description, LedChannels)
    else:
        UserForm_Other = D07.UserForm_Other()
        UserForm_Other.Show_UserForm_Other(Parts(1), Parts(0), Description, LedChannels, Show_Channel, LED_Channel, Def_Channel)
    # End IF statement added by Misha 18-4-2020
    _ret = UserForm_Other.UserForm_Res
    return _ret

def __Get_NamedPar(SearchName, MacroWithNames, FilledMacro):
    _ret = ""
    Names = Variant()

    Values = Variant()

    i = int()
    #-------------------------------------------------------------------------------------------------------------
    Names = Split(Replace(Split(MacroWithNames, '(')(1), ')', ''), ',')
    Values = Split(Replace(Split(FilledMacro, '(')(1), ')', ''), ',')
    for i in vbForRange(0, UBound(Names)):
        if Trim(Names(i)) == SearchName:
            _ret = Trim(Values(i))
            return _ret
    return _ret

def __Cx_to_LED_Channel(Cx, LedChannels):
    _ret = ""
    #------------------------------------------------------------------------------
    _select0 = Cx
    if (_select0 == 'C_ALL'):
        _ret = '1'
    elif (_select0 == 'C1'):
        _ret = 'C1-' + str(1 + Abs(LedChannels) - 1)
    elif (_select0 == 'C2'):
        _ret = 'C2-' + str(2 + Abs(LedChannels) - 1)
    elif (_select0 == 'C3'):
        _ret = 'C3-' + str(3 + Abs(LedChannels) - 1)
    elif (_select0 == 'C12'):
        _ret = 'C1-2'
    elif (_select0 == 'C23'):
        _ret = 'C2-3'
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Macro - ByVal 
def __Proc_General(LEDs, Macro, Description, LedChannels, LED_Channel, Def_Channel):
    _ret = ""
    Parts = Variant()

    Res = String()

    Param = Variant()
    Res_LED_Channel = ""
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if Macro == '' or Macro == "<Abort>":
        return _ret
    Parts = Split(Replace(Macro, ')', ''), '(')
    if UBound(Parts) == 0:
        Res = Macro
    else:
        Param = Split(Parts(1), ',')
        Res = Parts(0) + '('
        Other=0
        for p in Param:
            p = Trim(p)
            _select1 = p
            if (_select1 == 'LED') or (_select1 == 'B_LED'):
                p = '#LED'
            elif (_select1 == 'InCh'):
                p = '#InCh'
            elif (_select1 == ''):
                pass
            else:
                Other = Other + 1
            Res = Res + p + ', '
        if UBound(Param) >= 0:
            Res = M30.DelLast(M30.DelLast(Res))
        Show_Channel = M10.CHAN_TYPE_NONE
        if Trim(LEDs) != '':
            if Trim(LEDs) == M02.SerialChannelPrefix:
                Show_Channel = M10.CHAN_TYPE_SERIAL
            elif IsNumeric(LEDs):
                if P01.val(LEDs) >= 0:
                    Show_Channel = M10.CHAN_TYPE_LED
                    # 19.01.21: Jürgen: Old ".. <> 0"  07.10.21:Juergen
            else:
                Show_Channel = M10.CHAN_TYPE_LED
        Res = Res + ')'
        if Other > 0 or Show_Channel != M10.CHAN_TYPE_NONE:
            Res = __Proc_General_With_Other_Par(Res, Description, LedChannels, Show_Channel, LED_Channel, Def_Channel)
            if Res == '' or Res =="<Abort>":
                return _ret
            if Parts(0) == 'ConstrWarnLight':
                Res, LEDs = __Special_ConstrWarnLight(Res, LEDs)
                # 18.09.19
            if Left(Parts(0), Len('Multiplexer')) == 'Multiplexer':
                Res = M80.Special_Multiplexer_Ext(Res, LEDs)
                # Added by Misha 2020-03-26 ' 14.06.20: Added from Mishas version
        if InStr(Res, '$') > 0:
            Res_LED_Channel = Split(Res, '$')(1)
            Res = Split(Res, '$')(0)
        if Left(LEDs, Len('LedCnt')) == 'LedCnt':
            LEDs = __Get_NamedPar(LEDs, Macro, Res)
        _select2 = LEDs
        if (_select2 == 'Cx'):
            Par = __Get_NamedPar('Cx', Macro, Res)
            if Par == '':
                Par = __Get_NamedPar('B_LED_Cx', Macro, Res)
                # Used in PushButton_w_LED_BL_0..     ' 13.04.20:
            LEDs = __Cx_to_LED_Channel(Par, LedChannels)
    _ret = LEDs + '$' + Res
    if Res_LED_Channel != '':
        _ret = _ret + '$' + Res_LED_Channel
        # 27.04.20:
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Row - ByRef 
def __Get_PriorLine_LEDs(Row):
    _ret = P01.Cells(M02.FirstDat_Row, M25.LEDs____Col)
    #-----------------------------------------------------
    # Return the LEDs cell of the first enabled row starting with Row
    # Only lines which have an entry in the "LEDs" column are checked
    # Row is set to the detected line
    
    while Row >= M02.FirstDat_Row:
        if M20.Row_is_Achtive(Row):
            _ret = P01.Cells(Row, M25.LEDs____Col)
            return _ret, Row
        Row = Row - 1
    return _ret, Row #*HL

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: FilledMacro - ByVal 
def __Get_From_Input_Var(Macro, FilledMacro, ParName):
    _ret = ""
    Par = String()
    #-----------------------------------------------------------------------------------------------------------
    Par = __Get_NamedPar(ParName, Macro, FilledMacro)
    if Par == '':
        P01.MsgBox('Interner Fehler in Get_From_Input_Var()', vbCritical, 'Interner Fehler')
        M30.EndProg()
    _ret = Par
    return _ret

def __Test():
    Debug.Print(Evaluate('1+3'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Arg - ByVal 
def Get_InCh_Number_w_Err_Msg(Arg):
    _ret = 0
    Nr = int()
    #----------------------------------------------------------------------
    Nr = 0
    # VB2PY (UntranslatedCode) On Error GoTo ErrMsg
    Nr = P01.val(Replace(Arg, '#InCh', '0')) #*HL
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if Nr < 0:
        # VB2PY (UntranslatedCode) GoTo ErrMsg
        pass
    _ret = Nr
    return _ret
    P01.MsgBox(M09.Get_Language_Str('Fehler im Logischen Ausdruck. Es darf nur eine konstante positive Zahl zu \'#InCh\' addiert werden'), vbCritical, M09.Get_Language_Str('Fehler in Logic() Funktion'))
    _ret = - 1
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Statement - ByVal 
def __Get_Number_of_used_InCh_in_Par(Statement, Mode):
    _ret = 0
    Arglist = vbObjectInitialize(objtype=String)

    Arg = Variant()

    Nr = int()

    MaxNr = int()
    #------------------------------------------------------------------------------------------------------
    # Gets the maximal number of "#InCh" which is used in an logic expression if Mode = "Logic":
    # The example
    #    Logic(TestOr, #InCh OR #InCh+1 OR SwitchA4)
    # will return 2
    #
    # If Mode = "Comma" the staremet is a list of parameters separated by ","
    #
    Statement = Trim(Statement)
    if Right(Statement, 1) == ')':
        Statement = Trim(M30.DelLast(Statement))
    _select3 = Mode
    if (_select3 == 'Logic'):
        Arglist = M30.SplitEx(Statement, True, 'OR', 'AND', 'NOT')
    elif (_select3 == 'Comma'):
        Arglist = M30.SplitEx(Statement, True, ',')
    else:
        P01.MsgBox('Internal Error: Unknown Mode \'' + Mode + '\' in \'Get_Number_of_used_InCh_in_Par()\'', vbCritical, 'Internal Error')
        return _ret
    if M30.isInitialised(Arglist):
        for Arg in Arglist:
            if InStr(Arg, '#InCh') > 0:
                Nr = Get_InCh_Number_w_Err_Msg(Arg)
                ## VB2PY (CheckDirective) VB directive took path 1 on 0
                # VB2PY (UntranslatedCode) On Error GoTo ErrMsg
                Nr = eval(Replace(Arg, '#InCh', '0'))
                # VB2PY (UntranslatedCode) On Error GoTo 0
                if Nr < 0:
                    # VB2PY (UntranslatedCode) GoTo ErrMsg
                    pass
                if Nr < 0:
                    return _ret
                if Nr > MaxNr:
                    MaxNr = Nr
        _ret = MaxNr + 1
    return _ret

def __Test_Get_Number_of_used_InCh_in_Par():
    #UT----------------------------------------------
    Debug.Print(__Get_Number_of_used_InCh_in_Par(' NOT #InCh)', 'Logic'))
    Debug.Print(__Get_Number_of_used_InCh_in_Par('#InCh OR #InCh+1 OR SwitchA4', 'Logic'))
    Debug.Print(__Get_Number_of_used_InCh_in_Par('#InCh OR #InCh+2 OR SwitchA4', 'Logic'))
    Debug.Print(__Get_Number_of_used_InCh_in_Par('#InCh AND Bedigung1 OR #InCh AND Bedingung2', 'Logic'))
    Debug.Print(__Get_Number_of_used_InCh_in_Par('#InCh + Bedigung1 + 7', 'Logic'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: X - ByVal 
def __Get_BinSize(X):
    _ret = 0
    #---------------------------------------------------------
    # Number of binary bits necessary for x different P01.values
    _ret = P01.Application.RoundUp(Log(X) / Log(2), 0)
    return _ret

def SelectMacros():
    _ret = ""
    OldUpdating = Boolean()
    #----------------------------------------
    OldUpdating = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = False
    _ret = __SelectMacros_Sub()
    P01.Application.ScreenUpdating = OldUpdating
    return _ret

def Add_Icon_and_Name(SelRow, DstRow, Sh=None, NameOnly=False):
    #-------------------------------------------------------------------------------------------------------------------
    # SelRow: Row in the Lib_Macros sheet
    if M25.LanName_Col > 0 and SelRow > 0:
        _with0 = P01.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
        if Sh is None:
            Sh = P01.ActiveSheet
        LanName = Get_Language_Text(SelRow, M02.SM_LName_COL, M09.Get_ExcelLanguage())
        if LanName == '':
            LanName = _with0.Cells(SelRow, M02.SM_Name__COL)
            # Normal non language specific name if the entry ha no language name yet
        OldEvents = P01.Application.EnableEvents
        P01.Application.EnableEvents = False
        #*HL Sh.CellDict[DstRow, M25.LanName_Col] = LanName
        P01.CellDict[DstRow, M25.LanName_Col] = LanName #*HL
        
        P01.Application.EnableEvents = OldEvents
        if NameOnly == False:
            M27.Del_one_Icon_in_IconCol(DstRow, Sh)
            PicNamesArr = Split(_with0.Cells(SelRow, M02.SM_Pic_N_COL).Value, '|')
            if UBound(PicNamesArr) > 0:
                PicName = Trim(PicNamesArr(UBound(PicNamesArr)))
                M27.Add_Icon(PicName, DstRow, Sh)

def __SelectMacros_Sub():
    _ret = False
    Res="" #*HL
    OldEvents = Boolean()

    ActMacro = String()
    #---------------------------------------------
    M25.Make_sure_that_Col_Variables_match()
    _with1 = P01.ActiveCell()
    if _with1.Row < M02.FirstDat_Row:
        P01.MsgBox(M09.Get_Language_Str('Zur Auswahl des (Beleuchtungs-)Effekts muss eine Zeile in der' + vbCr + 'Tabelle ausgewählt sein bevor der Dialog Knopf betätigt wird.'), vbInformation, M09.Get_Language_Str('Falsche Zielposition ausgewählt'))
        return _ret
    OldEvents = P01.Application.EnableEvents
    P01.Application.EnableEvents = False
    P01.Cells(P01.ActiveCell().Row, M25.Config__Col).Select()
    P01.Application.EnableEvents = OldEvents
    #if M28.Get_String_Config_Var('Use_TreeView_for_Macros') == '':
    #    if P01.MsgBox(M09.Get_Language_Str('Soll die neue Baumansicht zur Auswahl der Makros verwendet werden oder weiter ' + 'mit dem alten Listenbasierten Dialog gearbeitet werden?' + vbCr + '  Ja = Neue Baumansicht' + vbCr + '  Nein = Alte Listenansicht' + vbCr + '(Das kann nachträglich auf der \'Config\' Seite geändert werden)'), vbQuestion + vbYesNo, M09.Get_Language_Str('Welcher Makro Auswahl Dialog soll verwendet werden?')) == vbYes:
    M28.Set_String_Config_Var('Use_TreeView_for_Macros', '1')
    #    else:
    #        M28.Set_String_Config_Var('Use_TreeView_for_Macros', '0')
    ActMacro = Replace(Trim(P01.Cells(P01.ActiveCell().Row, M25.Config__Col).Value), 'HouseT(', 'House(')
    if True: # M28.Get_Bool_Config_Var('Use_TreeView_for_Macros'): #standard list not supported
        Sort_for_TreeView_based_Makro()
        SelectMacro_Res = M09SMT.SelectMacro_TreeView(ActMacro)
    else:
        # Problem: Wenn der Dialog an der Stelle geöffnet wird an der sich die Maus befindet, dann wird das Element an der Maus Position augewählt ;-(
        # Hab noch keine Idee wie ich das beheben kann. Die folgenden Zeilen helfen nicht
        #  Sleep 1500 ' Wait until the mouse is released
        #  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
        #  cancel = True in Proc_DoubleCkick()
        pass
        
        #*HL Sort_for_List_based_Makro()
        #*HL SelectMacros_Form.Show_SelectMacros_Form(LIBMACROS_SH, ActMacro)
       
    if SelectMacro_Res != '':
        ActLanguage = M09.Get_ExcelLanguage()
        MacroName = Split(SelectMacro_Res, ',')(0)
        SelRow = int(Split(SelectMacro_Res, ',')(1))
        _with2 = P01.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
        DlgTyp = _with2.Cells(SelRow, M02.SM_Typ___COL)
        LEDs = _with2.Cells(SelRow, M02.SM_LEDS__COL)
        Macro = _with2.Cells(SelRow, M02.SM_Macro_COL)
        LedChannels = P01.val(_with2.Cells(SelRow, M02.SM_SngLEDCOL))
        Def_Channel = P01.val(_with2.Cells(SelRow, M02.SM_DefCh_COL))
        Act_Channel = P01.val(P01.Cells(P01.ActiveCell().Row, M25.LED_Cha_Col))
        Description = Replace(Get_Language_Text(SelRow, M02.SM_DetailCOL, ActLanguage), '|', vbLf)
        if Description == '':
            Description = Get_Language_Text(SelRow, M02.SM_ShrtD_COL, ActLanguage)
            # 21.10.21: Old: Description = .Cells(SelRow, SM_ShrtD_COL + ActLanguage * DeltaCol_Lib_Macro_Lang)  ' 24.02.20:    "
        _select4 = DlgTyp
        if (_select4 == 'House'):
            UserForm_House = D06.UserForm_House(MacroName=MacroName)
            UserForm_House.Show_With_Existing_Data(MacroName, P01.Cells(P01.ActiveCell().Row, M25.Config__Col), Act_Channel, Def_Channel)
            Res = UserForm_House.Userform_Res
        elif (_select4 == 'ColTab'):
            #Calculate
            M60.Open_MobaLedCheckColors_and_Insert_Set_ColTab_Macro()
            return _ret
        elif (_select4 in ("EX.Constructor", "EX.Macro")):   # 31.01.22: Juergen add extensions
            Res = __Proc_General(LEDs, Macro, Description, LedChannels, Act_Channel, Def_Channel) # Empty typ
            return _ret        
        
        
        elif (_select4 == ''):
            Res = __Proc_General(LEDs, Macro, Description, LedChannels, Act_Channel, Def_Channel)
        else:
            P01.MsgBox('Unknown Dialog Typ \'' + DlgTyp + '\'', vbCritical, 'Program Error: SelectMacros_Sub')
            
            
        if Res != '':
            # If Left(Res, Len("$#define")) = "$#define" Then Res = Replace(Replace(Res, "(", "   "), ")", "") ' Remove the brackets     ' 14.01.20: ' 04.11.21: Commented because the bracets are necessary to parse the argument if the macro should be changed
            Parts = Split(Res, '$')
            DstRow = P01.ActiveCell().Row
            LEDs = Parts(0)
            if UBound(Parts) >= 2:
                LED_Channel = Parts(2)
            else:
                LED_Channel = ''
            if M20.Check_IsSingleChannelCmd(LEDs):
                if DstRow > M02.FirstDat_Row: #*HL
                    PriorLine = DstRow - 1
                    PriorLineLEDs, PriorLine =__Get_PriorLine_LEDs(PriorLine) #*HL
                    if PriorLineLEDs:
                        PriorLeds = Trim(Replace(PriorLineLEDs, '^', ''))
                    else:
                        PriorLeds = ""
                    PriorChan = P01.val(P01.Cells(PriorLine, M25.LED_Cha_Col))
                    if M20.Check_IsSingleChannelCmd(PriorLeds):
                        if PriorLeds == LEDs and PriorChan == P01.val(LED_Channel):
                            Answ = P01.MsgBox(Replace(M09.Get_Language_Str('Achtung: Die LED Kanäle sind gleich wie der vorangegangenen Zeile (#1#)!' + vbCr + 'Das kann zu ungewollten Effekten führen.' + vbCr + 'Bei Funktionen welche einen Kanal nur kurzzeitig ansteuern kann das sinnvoll sein.' + vbCr + 'Ein Beispiel dafür ist die Ansteuerung von Sound Modulen. Hier steuern mehrere Tasten ' + 'den gleichen Kanal mit unterschiedlichen Werten an. Je nach abzuspielendem Sound wird ' + 'eine andere \'Helligkeit\' gesendet. Da die Tasten werden aber nicht gleichzeitig betätigt ' + 'werden ist das unproblematisch.' + vbCr + vbCr + 'Soll der neue Befehl die gleiche LED Adressieren wie der Vorangegangene Befehl?'), "#1#", str(PriorLine)), vbQuestion + vbYesNoCancel, M09.Get_Language_Str('Überlappende Kanäle entdeckt'))
                            _select5 = Answ
                            if (_select5 == vbYes):
                                LEDs = '^ ' + LEDs
                            elif (_select5 == vbCancel):
                                return _ret
            OldEvents1 = P01.Application.EnableEvents
            P01.Application.EnableEvents = False
            P01.CellDict[DstRow, M25.LED_Cha_Col] = LED_Channel
            P01.CellDict[DstRow, M25.LEDs____Col] = LEDs
            P01.Application.EnableEvents = OldEvents1
            P01.CellDict[DstRow, M25.Config__Col] = Parts(1)
            Add_Icon_and_Name(SelRow, DstRow)
            _select6 = _with2.Cells(SelRow, M02.SM_InCnt_COL)
            if (_select6 == 'n'):
                InCnt = __Get_From_Input_Var(Macro, Parts(1), 'InCh_Cnt')
            elif (_select6 == 'States'):
                InCnt = __Get_From_Input_Var(Macro, Parts(1), 'States')
            elif (_select6 == 'BinStates'):
                InCnt = __Get_BinSize(__Get_From_Input_Var(Macro, Parts(1), 'BinStates'))
            elif (_select6 == 'Logic'):
                InCnt = __Get_Number_of_used_InCh_in_Par(Split(Parts(1), ',')(1), 'Logic')
            elif (_select6 == '2?'):
                InCnt = __Get_Number_of_used_InCh_in_Par(Split(Parts(1), '(')(1), 'Comma')
                if InCnt == 0:
                    InCnt = 2
            else:
                InCnt = P01.val(_with2.Cells(SelRow, M02.SM_InCnt_COL))
            P01.Application.EnableEvents = False
            P01.CellDict[DstRow, M25.InCnt___Col] = InCnt
            M20.Complete_Addr_Column_with_InCnt(DstRow)
            M20.Format_Cells_to_Row(DstRow + M02.SPARE_ROWS)
            P01.Application.EnableEvents = OldEvents1
            # Special Checks                                                   ' 16.11.20:
            if UBound(Parts) > 1:
                MacroName = Split(Parts(1), '(')(0)
                _select7 = MacroName
                if (_select7 == 'BlueLight1') or (_select7 == 'BlueLight2') or (_select7 == 'Leuchtfeuer'):
                    if InStr(Parts(1), ' C_ALL,') > 0:
                        P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Das Makro \'#1#\' kann nur mit einer oder zwei LEDs benutzt werden.'), "#1#", MacroName), vbCritical, M09.Get_Language_Str('Fehler: Makro kann nicht mit 3 LEDs benutzt werden'))
                        ActiveCell = Replace(Parts(1), ' C_ALL, ', ' C12, ')
                        P01.CellDict[DstRow, M25.LEDs____Col] = 'C1-2'
            # Changed by Misha 18-4-2020                                       ' 14.06.20: Added from Mishas version
            Parts = Split(Res, ',')
            if Left(MacroName, Len('Multiplexer')) == 'Multiplexer':  # mulitplexer not supported yet
                P01.CellDict[DstRow, M25.LocInCh_Col] = M80.Count_Ones(P01.val(Parts(5))) + 1
                # 10.02.21: 20210206 Misha, Added + 1 because there is an zero pattern added.
                P01.CellDict[ActiveCell.Row, M25.DCC_or_CAN_Add_Col].Value = Userform_Res_Address
            else:
                P01.CellDict[DstRow, M25.LocInCh_Col] = P01.val(_with2.Cells(SelRow, M02.SM_LocInCCOL))
            # End Changed by Misha 18-4-2020
            P01.CellDict[DstRow, M02.Enable_Col] = ChrW(M02.Hook_CHAR)
            M20.Update_TestButtons(DstRow)
            M20.Update_Start_LedNr()
            _ret = True
    if Res != '':
        NextRow = P01.ActiveCell().Row + 1
        #while P01.Cells(NextRow, 1).EntireRow.Hidden:
        #    NextRow = NextRow + 1
        __Move_Cursor_to_visible_Macro_Cell(NextRow)
    else:
        __Move_Cursor_to_visible_Macro_Cell(P01.ActiveCell().Row)
    return _ret

def __Move_Cursor_to_visible_Macro_Cell(Row):
    OldEvents = Boolean()
    #---------------------------------------------------------
    OldEvents = P01.Application.EnableEvents
    P01.Application.EnableEvents = False
    #if P01.Cells(Row, M25.Config__Col).EntireColumn.Hidden:
    #    if P01.Cells(Row, M25.LanName_Col).EntireColumn.Hidden:
    #        P01.Cells(Row, M25.MacIcon_Col).Select()
    #    else:
    #        P01.Cells(Row, M25.LanName_Col).Select()
    #else:
    P01.Cells(Row, M25.Config__Col).Select()
    P01.Application.EnableEvents = OldEvents

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Str - ByVal 
def Find_Macro_in_Lib_Macros_Sheet(Str):
    _ret = 0
    #r = Range()

    #c = Range()
    #---------------------------------------------------------------------------
    _with3 = P01.Sheets(M02.LIBMACROS_SH)
    Str = Replace(Str, 'HouseT(', 'House(')
    if InStr(Str, '(') > 0:
        Str = Split(Str, '(')(0) + '('
        if Str[:3]=="// ":
            Str=Str[3:]
    r = _with3.Range(_with3.Cells(M02.SM_DIALOGDATA_ROW1, M02.SM_Name__COL), _with3.Cells(M30.LastUsedRowIn(P01.ThisWorkbook.Sheets(M02.LIBMACROS_SH)), M02.SM_Name__COL))
    for c in r.Rows: #*HL
        # Find the line
        if _with3.Cells(c.Row, M02.SM_FindN_COL) != '':
            ## VB2PY (CheckDirective) VB directive took path 1 on True
            #           Why did the old function use the InStr function ?
            if Str == _with3.Cells(c.Row, M02.SM_FindN_COL):
                _ret = c.Row
                return _ret
    return _ret

def __Test_Find_Macro_in_Lib_Macros_Sheet():
    #UT----------------------------------------------
    Debug.Print(Find_Macro_in_Lib_Macros_Sheet('Logic('))
    Debug.Print(Find_Macro_in_Lib_Macros_Sheet('Const('))

def __Change_Links_to_Absolute_In_Col(Sh, Col):
    c = Variant()
    #------------------------------------------------------------------------
    _with4 = Sh
    for c in _with4.Range(_with4.Cells(__HeadRow + 1, Col), _with4.Cells(M30.LastUsedRowIn(Sh), Col)):
        if c.Formula != '' + Left(c.Formula, 1) == '=':
            c.Formula = P01.Application.ConvertFormula(c.Formula, xlA1, xlA1, xlAbsolute)

def __Change_Links_to_Absolute():
    Sh = P01.CWorksheet()

    Col = int()

    c = Variant()
    #-------------------------------------
    # This function must be called before sorting the lines. Otherwise the links get corrupted
    Sh = P01.ActiveWorkbook.Worksheets(M02.LIBMACROS_SH)
    _with5 = Sh
    __Change_Links_to_Absolute_In_Col(Sh, M02.SM_Pic_N_COL)
    for Col in vbForRange(M02.SM_Group_COL, M30.LastUsedColumnIn(Sh), M02.DeltaCol_Lib_Macro_Lang):
        __Change_Links_to_Absolute_In_Col(Sh, Col)

def __Sort_by_Column(Col, SortFlag):
    #OldUpdating = Boolean()

    #Sh = P01.Worksheet()
    #----------------------------------------------------------
    if True: #P01.ThisWorkbook.Worksheets(M02.LIBMACROS_SH).Range('SortByTreeView').Value == SortFlag:
        return
    OldUpdating = P01.Application.ScreenUpdating
    P01.Application.ScreenUpdating = False
    # Change_Links_to_Absolute                                              ' 20.10.21: Links are not used anymore because they also create problems if absolute links are used when the lines are sorted ;-(
    Sh = P01.ActiveWorkbook.Worksheets(M02.LIBMACROS_SH)
    _with6 = Sh
    _with6.Sort.SortFields.Clear()
    _with6.Sort.SortFields.Add(key=_with6.Range(_with6.Cells(__HeadRow, Col), _with6.Cells(M30.LastUsedRowIn(Sh), Col)), SortOn=xlSortOnValues, Order=xlAscending, DataOption=xlSortNormal)
    _with6.Sort.SetRange(_with6.Range(_with6.Cells(__HeadRow + 1, 1), _with6.Cells(M30.LastUsedRowIn(Sh), M30.LastUsedColumnIn(Sh))))
    _with7 = _with6.Sort
    _with7.Header = xlNo
    _with7.MatchCase = False
    _with7.Orientation = xlTopToBottom
    _with7.SortMethod = xlPinYin
    _with7.Apply()
    P01.ThisWorkbook.Worksheets[M02.LIBMACROS_SH].Range['SortByTreeView'].Value = SortFlag
    P01.Application.ScreenUpdating = OldUpdating

def Sort_for_List_based_Makro():
    #-------------------------------------
    __Sort_by_Column(M02.SM_ListS_COL, 'L')

def Sort_for_TreeView_based_Makro():
    #-----------------------------------------
    __Sort_by_Column(M02.SM_TreeS_COL, 'T')

def Get_Language_Text(Row, FirstCol, ActLanguage):
    _ret = ""
    #Sh = Worksheet()

    #Txt = String()
    #-------------------------------------------------------------------------------------------------
    # Get the language specific text
    # If the requested text is not available use the englich or german text
    Sh = P01.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
    _with8 = Sh
    Txt = _with8.Cells(Row, FirstCol + ActLanguage * M02.DeltaCol_Lib_Macro_Lang).Value
    if Txt == '' and ActLanguage > 1:
        Txt = _with8.Cells(Row, FirstCol + 1 * M02.DeltaCol_Lib_Macro_Lang).Value
        # Use the english name
    if Txt == '' and ActLanguage > 0:
        Txt = _with8.Cells(Row, FirstCol + 0 * M02.DeltaCol_Lib_Macro_Lang).Value
        # Use the german name
    _ret = Txt
    return _ret

# VB2PY (UntranslatedCode) Option Explicit
