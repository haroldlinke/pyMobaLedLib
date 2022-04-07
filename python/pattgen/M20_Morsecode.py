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

""" This Modul has been written by Lorenz
 with some smal modifications by Hardi
 Revision History:
 ~~~~~~~~~~~~~~~~~
 17.10.19: - Speed Up
 19.10.19: - Suport for special codes like {SOS}
           - Error checks
 22.11.19: - Replaced the most cell adresses by public constants
             The Morse code specific cells M2..P5 have not been replaced
 ToDo:
 - Use the public constants: FirstLEDTabRANGE, ...
------------------------------------------------------
UT------------
-------------------------------
---------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------
--------------------------------------------------------------------------------
UT----------------------------------
----------------------------
"""


def __Add_Kursive_Text(r, Txt):
    Parts = vbObjectInitialize(objtype=String)
    #------------------------------------------------------
    Parts = Split(Get_Language_Str(Txt), '#')
    if UBound(Parts) != 2:
        MsgBox('Error: In the Language sheet. The text \'' + Txt + '\' must contain the startposition and the length of the cursive part', vbCritical, 'Internal Error')
        r = Txt
    else:
        r = Parts(2)
        r.Characters[Start= Val(Parts(0)), Length= Val(Parts(1))].Font.FontStyle = 'Italic'

def __Test_Bold():
    #UT------------
    # Attention: Place the cursor to the destination cell for the test
    __Add_Kursive_Text(ActiveCell, '7#3#Dauer Dit in ms')

def Make_Morsecode_Init():
    Oldupdating = Boolean()

    OldEvents = Boolean()
    #-------------------------------
    # Ist called when the sheet is copied with the "Neues Blatt" button or loaded from a file
    Oldupdating = Application.ScreenUpdating
    OldEvents = Application.EnableEvents
    Application.ScreenUpdating = False
    Application.EnableEvents = False
    Range['M2'] = Get_Language_Str('Morsetext')
    __Add_Kursive_Text(Range('M3'), '7#3#Dauer Dit in ms')
    Range['M4'] = Get_Language_Str('Spruchanfang/-ende senden')
    Range['M5'] = Get_Language_Str('Nach dem Erstellen vorführen')
    Range['M5'].HorizontalAlignment = xlRight
    Range['N2'] = Get_Language_Str('{SOS} Rettet Hardi')
    Range['N3'] = '240'
    Range['N4'] = Get_Language_Str('Nein')
    Range['N5'] = Get_Language_Str('Ja')
    Range['N2:N5'].Interior.Color = 65535
    Range['O2:P2'].Interior.Color = 65535
    __Hide_Second_Pic()
    Application.ScreenUpdating = Oldupdating
    Application.EnableEvents = OldEvents
    #Button_Init_Proc_Finished = True                                                         ' 05.01.22: Juergen call init function synchronous
    ##If VBA6 Then                                                                              ' 05.01.22: Juergen call init function synchronous
    #  Debug.Print "Button_Init_Proc_Finished=" & Button_Init_Proc_Finished
    #  DoEvents
    ##End If

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Zellcounter - ByRef 
def __One_Char(Zeichencode, Zellcounter, Morsezeichen):
    Zaehlerincode = Integer()

    c = String()
    #---------------------------------------------------------------------------------------------------
    c = Chr(Zeichencode)
    for Zaehlerincode in vbForRange(1, Len(Morsezeichen(Zeichencode))):
        select_0 = Mid(Morsezeichen(Zeichencode), Zaehlerincode, 1)
        if (select_0 == '·'):
            Cells[LEDsTAB_R + 0, Zellcounter].Value = 'X'
            Cells[LEDsTAB_R + 2, Zellcounter].Value = '.'
            Cells[LEDsTAB_R + 1, Zellcounter].Value = c
            Zellcounter = Zellcounter + 1
        elif (select_0 == '-'):
            Range[Cells(LEDsTAB_R + 0, Zellcounter), Cells(LEDsTAB_R + 0, Zellcounter + 2)].Value = 'X'
            Range[Cells(LEDsTAB_R + 2, Zellcounter), Cells(LEDsTAB_R + 2, Zellcounter + 2)].Value = '-'
            Range[Cells(LEDsTAB_R + 1, Zellcounter), Cells(LEDsTAB_R + 1, Zellcounter + 2)].Value = c
            Zellcounter = Zellcounter + 3
        elif (select_0 == '_') or (select_0 == ' '):
            Zellcounter = Zellcounter + 1
        else:
            MsgBox('Wrong character in \'Morsezeichen(' + Zeichencode + ')\'', vbCritical, 'Interner Fehler')

def Make_Morsecode():
    Zaehler = Double()

    Zeichencode = Integer()

    Morsezeichen = vbObjectInitialize(((1, 255),), String)

    Morsecode = String()

    Ditdauer = Double()

    Spruchanfangende = String()

    Zellcounter = Long()

    WrongChar = String()
    #------------------------------------------------------------------------------------------------------------------------------------
    #Dim Zaehlerincode As Integer
    Application.EnableEvents = False
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    # Morsetable corresponding to ASCII codes
    Morsezeichen[32] = '_'
    # Additional codes from https://de.wikipedia.org/wiki/Morsezeichen#@-Zeichen  19.10.19: Hardi
    # How to handle special signals ?
    Morsezeichen[Asc('À')] = '· - - · -'
    Morsezeichen[Asc('Å')] = '· - - · -'
    Morsezeichen[Asc('Ä')] = '· - · -'
    Morsezeichen[Asc('È')] = '· - · · -'
    Morsezeichen[Asc('É')] = '· · - · ·'
    Morsezeichen[Asc('Ö')] = '- - - ·'
    Morsezeichen[Asc('Ü')] = '· · - -'
    # ??       "- - - -" CH
    Morsezeichen[Asc('ß')] = '· · · - - · ·'
    Morsezeichen[Asc('Ñ')] = '- - · - -'
    Morsezeichen[Asc('.')] = '· - · - · -'
    Morsezeichen[Asc(',')] = '- - · · - -'
    Morsezeichen[Asc(':')] = '- - - · · ·'
    Morsezeichen[Asc(';')] = '- · - · - ·'
    Morsezeichen[Asc('?')] = '· · - - · ·'
    Morsezeichen[Asc('-')] = '- · · · · -'
    Morsezeichen[Asc('_')] = '· · - - · -'
    Morsezeichen[Asc('(')] = '- · - - ·'
    Morsezeichen[Asc(')')] = '- · - - · -'
    Morsezeichen[Asc('\'')] = '· - - - - ·'
    Morsezeichen[Asc('=')] = '- · · · -'
    Morsezeichen[Asc('+')] = '· - · - ·'
    Morsezeichen[Asc('/')] = '- · · - ·'
    Morsezeichen[Asc('@')] = '· - - · - ·'
    Morsezeichen[48] = '-_-_-_-_-'
    Morsezeichen[49] = '·_-_-_-_-'
    Morsezeichen[50] = '·_·_-_-_-'
    Morsezeichen[51] = '·_·_·_-_-'
    Morsezeichen[52] = '·_·_·_·_-'
    Morsezeichen[53] = '·_·_·_·_·'
    Morsezeichen[54] = '-_·_·_·_·'
    Morsezeichen[55] = '-_-_·_·_·'
    Morsezeichen[56] = '-_-_-_·_·'
    Morsezeichen[57] = '-_-_-_-_·'
    Morsezeichen[65] = '·_-'
    Morsezeichen[66] = '-_·_·_·'
    Morsezeichen[67] = '-_·_-_·'
    Morsezeichen[68] = '-_·_·'
    Morsezeichen[69] = '·'
    Morsezeichen[70] = '·_·_-_·'
    Morsezeichen[71] = '-_-_·'
    Morsezeichen[72] = '·_·_·_·'
    Morsezeichen[73] = '·_·'
    Morsezeichen[74] = '·_-_-_-'
    Morsezeichen[75] = '-_·_-'
    Morsezeichen[76] = '·_-_·_·'
    Morsezeichen[77] = '-_-'
    Morsezeichen[78] = '-_·'
    Morsezeichen[79] = '-_-_-'
    Morsezeichen[80] = '·_-_-_·'
    Morsezeichen[81] = '-_-_·_-'
    Morsezeichen[82] = '·_-_·'
    Morsezeichen[83] = '·_·_·'
    Morsezeichen[84] = '-'
    Morsezeichen[85] = '·_·_-'
    Morsezeichen[86] = '·_·_·_-'
    Morsezeichen[87] = '·_-_-'
    Morsezeichen[88] = '-_·_·_-'
    Morsezeichen[89] = '-_·_-_-'
    Morsezeichen[90] = '-_-_·_·'
    Zellcounter = Dauer_Col1
    Morsecode = Cells(2, 14).Value
    Ditdauer = Cells(3, 14).Value
    Spruchanfangende = Cells(4, 14).Value
    if Spruchanfangende == Get_Language_Str('Ja'):
        Morsecode = 'KA ' + Morsecode + 'AR'
    Range(Dauer_Rng).ClearContents()
    Range(LEDs__TAB).ClearContents()
    Range(GoTo_RNG).ClearContents()
    Morsecode = UCase(Morsecode)
    Cells[Dauer_Row, Zellcounter].Value = Ditdauer
    for Zaehler in vbForRange(1, Len(Morsecode)):
        c = Mid(Morsecode, Zaehler, 1)
        Zeichencode = Asc(c)
        if c != '{' and Morsezeichen(Zeichencode) == '':
            if InStr(WrongChar, c) == 0:
                WrongChar = WrongChar + c + ' '
        if c == '{':
            Parts = Split(Mid(Morsecode, Zaehler), '}')
            select_1 = Mid(Parts(0), 2)
            if (select_1 == 'KA') or (select_1 == 'BT') or (select_1 == 'AR') or (select_1 == 'VE') or (select_1 == 'SK') or (select_1 == 'SOS') or (select_1 == 'HH') or (select_1 == 'OE') or (select_1 == 'SZ') or (select_1 == 'AAA') or (select_1 == 'MIM') or (select_1 == 'OS') or (select_1 == 'NNN') or (select_1 == 'IMI') or (select_1 == 'BA') or (select_1 == 'UK') or (select_1 == 'KN') or (select_1 == 'KK') or (select_1 == 'JN') or (select_1 == 'BT') or (select_1 == 'AR') or (select_1 == 'DN') or (select_1 == 'AC'):
                for ix in vbForRange(2, Len(Parts(0))):
                    __One_Char(Asc(Mid(Parts(0), ix, 1)), Zellcounter, Morsezeichen)
                    Zellcounter = Zellcounter + 1
            else:
                MsgBox(Get_Language_Str('Unbekanntes Spezial Signal \'') + Parts(0) + '}\'', vbCritical, Get_Language_Str('Unbekanntes Signal'))
            Zaehler = Zaehler + Len(Parts(0)) + 1
        else:
            ## VB2PY (CheckDirective) VB directive took path 1 on 1
            __One_Char(Zeichencode, Zellcounter, Morsezeichen)
        Zellcounter = Zellcounter + 3
    Zellcounter = Zellcounter - 3
    Cells[LEDsTAB_R + 0, Zellcounter] = '.'
    if WrongChar != '':
        MsgBox(Get_Language_Str('Achtung die folgenden Zeichen existieren nicht im Morse Alphabet:') + vbCr + '  ' + WrongChar + vbCr + Get_Language_Str('Die Zeichen wurden weggelassen'), vbCritical, Get_Language_Str('Falsche Zeichen erkannt'))
    if Zellcounter > 148 + 5:
        MsgBox(Get_Language_Str('Der Morsecode ist zu lang (') + Zellcounter - 5 + Get_Language_Str('). Maximal 148 Abschnitte sind möglich.'), vbInformation, Get_Language_Str('Morsecode zu lang'))
        # Problem: Der Range mit dem die Macros "CalculatePattern", ... aufgerufen werden ist nicht größer
        #          damit die Berechnung bei anderen sheets nicht zu lange dauert.
        #          => Erst mal muss diese Länge reichen.
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    ActiveSheet.Calculate()
    if Cells(5, 14).Value == Get_Language_Str('Ja') or Cells(5, 14).Value == 'Ja':
        __Simulate_MorseCode(Ditdauer, Zellcounter)

def __Find_Second_Pic():
    fn_return_value = None
    o = Variant()

    Nr = Integer()
    #--------------------------------------------
    for o in ActiveSheet.Shapes:
        #If o.Type <> msoComment Then o.Select ' Debug
        if (o.Type == msoPicture) or (o.Type == msoLinkedPicture):
            if o.Name != 'MainMenu':
                Nr = Nr + 1
                if Nr == 2:
                    fn_return_value = o
                    return fn_return_value
    fn_return_value = None
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Ditdauer - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Zellcounter - ByVal 
def __Simulate_MorseCode(Ditdauer, Zellcounter):
    Led_An = Variant()

    i = Integer()

    Zaehler = Long()

    StartActCell = Long()
    #--------------------------------------------------------------------------------
    Led_An = __Find_Second_Pic()
    Application.Cursor = xlWait
    for Zaehler in vbForRange(LEDsTAB_C, Zellcounter):
        if Cells(LEDsTAB_R, Zaehler).Value == 'X':
            if StartActCell == 0:
                StartActCell = Zaehler
            Cells[LEDsTAB_R + 1, Zaehler].Interior.ColorIndex = 6
        else:
            if StartActCell > 0:
                Range[Cells(LEDsTAB_R + 1, StartActCell), Cells(LEDsTAB_R + 1, Zaehler)].Interior.ColorIndex = 2
                StartActCell = 0
        Led_An.Visible = ( Cells(LEDsTAB_R, Zaehler).Value == 'X' ) 
        ActiveSheet.Calculate()
        DoEvents()
        Sleep(Ditdauer)
    #Cells(LEDsTAB_R+1, Zaehler - 1).Interior.ColorIndex = 2
    if StartActCell > 0:
        Range[Cells(LEDsTAB_R + 1, StartActCell), Cells(LEDsTAB_R + 1, Zaehler)].Interior.ColorIndex = 2
    Led_An.Visible = False
    Application.Cursor = xlDefault

def __Test_Simulate_MorseCode():
    #UT----------------------------------
    __Simulate_MorseCode(240, 30)

def __Hide_Second_Pic():
    Led_An = Variant()
    #----------------------------
    Led_An = __Find_Second_Pic()
    if Led_An is None:
        MsgBox(Get_Language_Str('Fehler die Bilder wurden nicht geladen. Bitte sicherstellen, dass sie in der \'MLL_pcf\' Datei VOR dem Button (msoFormControl) stehen.'), vbCritical, Get_Language_Str('Fehler in Beispiel Datei'))
    else:
        Led_An.Visible = False

# VB2PY (UntranslatedCode) Option Explicit
