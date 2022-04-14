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
# 2022-01-07 v4.02 HL: - Else:, ByRef check done - first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *


import proggen.D01_Userform_DialogGuide1 as D01
import proggen.D03_Userform_Description as D03
import proggen.D04_Userform_Connector as D04

import proggen.Prog_Generator as PG

#import proggen.M02_Public as M02
import proggen.M02_global_variables as M02GV
import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
import proggen.M09_SelectMacro_Treeview as M09SMT
import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80
import proggen.F00_mainbuttons as F00

from ExcelAPI.X01_Excel_Consts import *
import ExcelAPI.P01_Workbook as P01


""" Dialog guided input
 - Kurze Erklärung am Anfang
   mit Auswahl der Zeile.
   Wenn bereits Daten in der Zeile sind, dann wird mit der ausgewählten Spalte weitergemacht
 - Abfrage ob der Effekt von DCC gesteuert werden soll.
   - Adresse
"""

__Ask_Input_NextRow = Boolean()
__Input_NextRow = Boolean()

def Dialog_Guided_Input():
    global __Ask_Input_NextRow, __Input_NextRow
    #-------------------------------
    M25.Make_sure_that_Col_Variables_match()
    if M30.First_Change_in_Line(P01.ActiveCell()):
        F00.UserForm_DialogGuide1.Show()
        #while UserForm_DialogGuide1.IsActive:
        #    DoEvents()
        #if DialogGuideRes == vbAbort:
        if F00.UserForm_DialogGuide1.res == vbAbort:
            P01.ActiveSheet.Redraw_table()
            return
        #for i in vbForRange(1, 5):
        #    DoEvents()
        #    Sleep(50)
        P01.ActiveSheet.remove_bindings()
        while 1:
            __Input_NextRow = False
            __Ask_Input_NextRow = True
            P01.ActiveSheet.Redraw_table()            
            Ask_External_Control()
            if __Input_NextRow:
                Debug.Print('ToDo: Prüfen of die nächste Zeile leer ist und geg. eine Zeile einfügen')
            if not (__Input_NextRow):
                P01.ActiveSheet.Redraw_table(do_bindings=True)
                break
    else:
        P01.ActiveSheet.remove_bindings()
        __Ask_Input_NextRow = False
        ActiveCell = P01.ActiveCell()
        r = ActiveCell.Row
        if (ActiveCell.Column == M25.DCC_or_CAN_Add_Col) or (ActiveCell.Column == M25.SX_Channel_Col):
            if M25.SX_Bitposi_Col > 0:
                SX_DataAvailable = P01.Cells(r, M25.SX_Bitposi_Col) != ''
            if P01.Cells(r, M25.DCC_or_CAN_Add_Col + M25.SX_Channel_Col) == '' and not SX_DataAvailable:
                Ask_External_Control()
            else:
                Input_Address()
        elif (ActiveCell.Column == M25.Inp_Typ_Col):
            Input_Typ()
        elif (ActiveCell.Column == M25.SX_Bitposi_Col):
            Input_BitPos()
        elif (ActiveCell.Column == M25.Start_V_Col):
            Input_Start_Val()
        elif (ActiveCell.Column == M25.Descrip_Col):
            Input_Description()
        elif (ActiveCell.Column == M25.Dist_Nr_Col) or (ActiveCell.Column == M25.Conn_Nr_Col):
            Input_Connector()
        elif (ActiveCell.Column == M25.Config__Col) or (ActiveCell.Column == M25.MacIcon_Col) or (ActiveCell.Column == M25.LanName_Col):
            M09SM.SelectMacros()
        else:
            if ActiveCell.Column > M25.Config__Col:
                P01.MsgBox(M09.Get_Language_Str('Die ausgewählte Spalte sollte nur von erfahrenen Benutzern verändert werden.' + vbCr + 'Es existiert keine Dialog gestützte Eingabe.'), vbInformation, M09.Get_Language_Str('Spalte sollte nur von Experten verändert werden'))
            else:
                P01.MsgBox(M09.Get_Language_Str('Für die Ausgewählte Spalte existiert noch kein Dialog'), vbInformation, M09.Get_Language_Str('Kein Dialog vorhanden'))
    
    P01.ActiveSheet.Redraw_table(do_bindings=True)
    return
    

def Ask_External_Control():
    #--------------------------------
    M25.Make_sure_that_Col_Variables_match()
    select_1 = P01.MsgBox(M09.Get_Language_Str('Soll die LED Gruppe über ') + M25.Page_ID + M09.Get_Language_Str(' gesteuert werden?' + vbCr + vbCr + '  Ja:     Der Effekt kann über eine Zentrale geschaltet werden.' + vbCr + '           Im Folgenden wird die Adresse zur Steuerung der' + vbCr + '           Funktion abgefragt. Das ist z.B. bei einem Haus oder' + vbCr + '           einem Signal sinnvoll.' + vbCr + '  Nein: Der Effekt ist dauerhaft aktiv. Das kann man z.B. bei' + vbCr + '           einer Ampel auswählen. Die Steuerung über ') + M25.Page_ID + vbCr + M09.Get_Language_Str('           kann auch nachträglich aktiviert werden.'), vbQuestion + vbYesNoCancel, M09.Get_Language_Str('Steuerung über ') + M25.Page_ID + '?')
    if (select_1 == vbYes):
        Input_Address()
    elif (select_1 == vbNo):
        Input_Description()
    elif (select_1 == vbCancel):
        return

def Input_Address():
    Txt = String()

    This_Addr_Channel = String()

    Addr_Channel = String()

    MinVal = int()

    MaxVal = int()

    Adresses_Channels = String()

    Inp = String()

    Valid = Boolean()
    #-------------------------
    if M25.Page_ID == 'Selectrix':
        Txt = M09.Get_Language_Str(' Kanal eingeben')
        This_Addr_Channel = M09.Get_Language_Str('Der Kanal')
        Addr_Channel = M09.Get_Language_Str('Kanal')
        MinVal = 0
        MaxVal = 99
        Adresses_Channels = M09.Get_Language_Str('Kanäle')
    else:
        Txt = M09.Get_Language_Str(' Adresse eingeben')
        This_Addr_Channel = M09.Get_Language_Str('Die Adresse')
        Addr_Channel = M09.Get_Language_Str('Adresse')
        MinVal = 1
        MaxVal = 10240
        Adresses_Channels = M09.Get_Language_Str('Adressen')
    if M25.Page_ID == 'CAN':
        MaxVal = 65535
        MinVal = 1 #*HL
        # ??
    Inp = M25.Get_First_Number_of_Range(P01.ActiveCell().Row, M25.DCC_or_CAN_Add_Col + M25.SX_Channel_Col)
    while 1:
        Inp = P01.InputBox(M09.Get_Language_Str('Bitte ') + M25.Page_ID + Txt + ' [' + str(MinVal) + '..' + str(MaxVal) + ']' + vbCr + vbCr + This_Addr_Channel + M09.Get_Language_Str(' muss bei der Zentrale zur Steuerung der Funktion angegeben werden.' + vbCr + vbCr + 'Achtung: Bei manchen Funktionen werden mehrere ') + Adresses_Channels + M09.Get_Language_Str(' belegt. ' + 'Das Programm ergänzt den Bereich automatisch (Beispiel: 23 - 24)' + vbCr + 'Es muss nur der Startwert ohne \'- 24\' eingegeben werden.') + vbCr + vbCr + M25.Page_ID + ' ' + Addr_Channel + ': ', M25.Page_ID + Txt, Default= Inp)
        Debug.Print ("Res='" + Inp + "'") # Debug
        if InStr(Inp, '-') > 1:
            Inp = Left(Inp, InStr(Inp, '-'))
        if IsNumeric(Inp):
            Valid = P01.val(Inp) >= MinVal and P01.val(Inp) <= MaxVal # and Int(Inp) == Inp
        if Inp != '' and not Valid:
            M31.BeepThis2('Windows Balloon.wav')
            M30.Show_Status_for_a_while(M09.Get_Language_Str('Falsche Eingabe. ') + This_Addr_Channel + M09.Get_Language_Str(' muss zwischen ') + str(MinVal) + M09.Get_Language_Str(' und ') + str(MaxVal) + M09.Get_Language_Str(' liegen. '))
        if Inp == '' or Valid:
            break
    M30.Show_Status_for_a_while('')
    if Valid:
        with_0 = P01.Cells(P01.ActiveCell().Row, M25.DCC_or_CAN_Add_Col + M25.SX_Channel_Col)
        with_0.Value = P01.val(Inp)
        P01.Application.EnableEvents = False
        with_0.Offset(0, 1).Select()
        P01.Application.EnableEvents = True
        if (M25.Page_ID == 'Selectrix'):
            Input_BitPos()
        elif (M25.Page_ID == 'CAN'):
            Input_Typ()
        elif (M25.Page_ID == 'DCC'):
            P01.Cells(P01.ActiveCell().Row, M25.Inp_Typ_Col).Offset(0, 1).Select()
            Input_Start_Val()
        else:
            P01.MsgBox('Internal error in \'Input_Address()\': Unknown Page_ID \'' + M25.Page_ID + '\'', vbCritical, 'Internal Error')

def Input_BitPos():
    Inp = String()

    Valid = Boolean()
    #------------------------
    Inp = P01.Cells(P01.ActiveCell().Row, M25.SX_Bitposi_Col)
    while 1:
        Inp = P01.InputBox(M09.Get_Language_Str('Bitte die Bitposition eingeben [1..8]' + vbCr + vbCr + 'Die Bitposition muss bei der Zentrale zur Steuerung der Funktion angegeben werden.' + vbCr + 'Achtung: Bei manchen Funktionen werden mehrere Bits belegt. Die Eingabe definiert das erste benutzte Bit.' + vbCr + vbCr + 'Bitposition: '), M25.Page_ID + M09.Get_Language_Str('Bitposition eingeben'), Inp)
        #Debug.Print "Res='" & Inp & "'" ' Debug
        if IsNumeric(Inp):
            Valid = P01.val(Inp) >= 1 and P01.val(Inp) <= 8 #*HL and Int(Inp) == Inp
        if Inp != '' and not Valid:
            M31.BeepThis2('Windows Balloon.wav')
            M30.Show_Status_for_a_while(M09.Get_Language_Str('Falsche Eingabe. Die Bitposition muss zwischen 1 und 8 liegen. '))
        if Inp == '' or Valid:
            break
    if Valid:
        with_1 = P01.Cells(P01.ActiveCell().Row, M25.SX_Bitposi_Col)
        with_1.Value = P01.val(Inp)
        P01.Application.EnableEvents = False
        with_1.Offset(0, 1).Select()
        P01.Application.EnableEvents = True
        Input_Typ()

def Input_Typ():
    #---------------------
    M20.Select_Typ_by_Dialog(P01.ActiveCell())
    if M02GV.Userform_Res != '':
        P01.Cells(P01.ActiveCell().Row, M25.Inp_Typ_Col).Offset(0, 1).Select()
        Input_Start_Val()

def Input_Start_Val():
    MinVal = 1

    MaxVal = 255

    Valid = Boolean()

    Inp = Variant()
    #---------------------------
    #Debug.Print "Inp_Typ_Col=" & Inp_Typ_Col
    Inp = P01.ActiveCell()
    while 1:
        Inp = P01.InputBox(M09.Get_Language_Str('Startwert des Eingangs eingeben' + vbCr + vbCr + 'Der Startwert bestimmt das Verhalten nach dem Einschalten in Verbindung mit DCC, ' + 'CAN oder Selectrix. ' + vbCr + 'Normalerweise sind die Funktionen beim Start deaktiviert. ' + 'Erst wenn der erste ') + M25.Page_ID + M09.Get_Language_Str(' Einschaltbefehl von der Zentrale kommt wird ' + 'die Zeile aktiviert. ' + vbCr + 'Wenn eine bestimmte Funktion bereits beim Einschalten der ' + 'Anlage einen definierten Wert haben soll kann das über den ' + 'Startwert vorgegeben werden. Die meisten Funktionen haben einen Eingang mit dem sie ' + 'Ein- oder Ausgeschaltet werden. Hier wird eine 1 zum Einschalten angegeben.' + vbCr + 'Bei Funktionen mit mehreren Eingängen (z.B. Signale) ist der Wert ist Bitkodiert. ' + 'Hier wird der erste Eingang mit einer 1, zweite Eingang mit einer 2 und der dritte Eingang ' + 'mit einer 4 aktiviert.' + vbCr + vbCr + 'Startwert:  (Keine Eingabe wenn nicht benötigt)'), M09.Get_Language_Str('Definition des Startwerts'), Inp)
        if IsNumeric(Inp):
            Valid = P01.val(Inp) >= MinVal and P01.val(Inp) <= MaxVal #*HL and Int(Inp) == val(Inp)
        if Inp != '' and not Valid:
            M31.BeepThis2('Windows Balloon.wav')
            M30.Show_Status_for_a_while(M09.Get_Language_Str('Falsche Eingabe. ') + Inp + M09.Get_Language_Str(' muss zwischen ') + str(MinVal) + M09.Get_Language_Str(' und ') + str(MaxVal) + M09.Get_Language_Str(' liegen. '))
        if Inp == '' or Valid:
            break
    P01.ActiveCell().Value = Inp
    M30.Show_Status_for_a_while('')
    P01.ActiveCell().Offset(0, 1).Select()
    Input_Description()

def Input_Description():
    Res = String()
    #-----------------------------
    
    
    #UserForm_Description.setFocus(Target)
    Res = F00.UserForm_Description.ShowForm(P01.ActiveCell().Value)
    if Res != '<Abort>':
        with_2 = P01.Cells(P01.ActiveCell().Row, M25.Descrip_Col)
        with_2.Value = Res
        with_2.Offset(0, 1).Select()
        Input_Connector()

def Input_Connector():
    global __Input_NextRow, __Ask_Input_NextRow

    #---------------------------
    r = P01.ActiveCell().Row
    
    if F00.UserForm_Connector.Start(P01.Cells(r, M25.Dist_Nr_Col), P01.Cells(r, M25.Conn_Nr_Col)):
        P01.Application.EnableEvents = False
        P01.Cells(r, M25.Conn_Nr_Col + 1).Select()
        P01.Application.EnableEvents = True
        if P01.MsgBox(M09.Get_Language_Str('Im folgenden Dialog wird die Funktion ausgewählt welche mit dieser Zeile verknüpft ist. ' + 'Je nach Funktion müssen weitere Parameter angegeben werden.'), vbOKCancel, M09.Get_Language_Str('Fast geschafft')) == vbOK:
            Debug.Print('Start SelectMacros() from Input_Connector')
            if M09SM.SelectMacros():
                if __Ask_Input_NextRow:
                    __Ask_Input_NextRow = False
                    P01.Cells(r + 1, M25.DCC_or_CAN_Add_Col + M25.SX_Channel_Col).Select()
                    if P01.MsgBox(M09.Get_Language_Str('Eingabe einer weiteren Zeile?'), vbYesNo + vbQuestion, M09.Get_Language_Str('Nächste Zeile Eingeben')) == vbYes:
                        __Input_NextRow = True

# VB2PY (UntranslatedCode) Option Explicit