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


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

""" Export macros to the Prog_Generator
 ToDo:
 - Abfrage in Get_Prog_Generator_Name() einbauen mit dem man ein anderes Prog_Generator
   Programm anstelle das standards auswählen kann (Name/Verzeichnis)
   Momentan kommt nur eine Meldung das das Programm nicht gefunden wurde
 - Überprüfung der Prog_Generator Version
"""

__Default_Prog_Generator_Name = 'Prog_Generator_MobaLedLib.xlsm'
__Prog_Generator_Name = String()

def __Get_Prog_Generator_Name():
    fn_return_value = None
    #---------------------------------------------------
    # Make sure that the Prog_Generator excel sheet is opened
    # and activated.
    # The function returns the name if it's activated
    # In case of an error "" is returned
    if __Prog_Generator_Name == '':
        if Same_Name_already_open(__Default_Prog_Generator_Name):
            __Prog_Generator_Name = Workbooks(__Default_Prog_Generator_Name).FullName
        else:
            Path = Get_DestDir_All()
            # Check if it exists in the user dir
            FullPath = Path + __Default_Prog_Generator_Name
            if Dir(FullPath) == '':
                # Check if it exists in the lib dir
                Path = Get_SrcDirInLib()
                FullPath = Path + __Default_Prog_Generator_Name
                if Dir(FullPath) == '':
                    MsgBox(Get_Language_Str('Fehler: Das Programm \'') + __Default_Prog_Generator_Name + '\'' + vbCr + Get_Language_Str('existiert nicht im Standard Verzeichnis:') + vbCr + '  \'' + Path + '\'', vbCritical, Get_Language_Str('Fehler ') + __Default_Prog_Generator_Name + Get_Language_Str(' nicht vorhanden'))
                    return fn_return_value
            __Prog_Generator_Name = FullPath
    if Same_Name_already_open(__Prog_Generator_Name):
        Workbooks(FileNameExt(__Prog_Generator_Name)).Activate()
        if Is_Minimized(FileNameExt(__Prog_Generator_Name)) != 0:
            Application.WindowState = xlNormal
    else:
        Workbooks.Open(FileName=__Prog_Generator_Name)
        __Prog_Generator_Name = Workbooks(FileNameExt(__Prog_Generator_Name)).FullName
    fn_return_value = __Prog_Generator_Name
    return fn_return_value

def __Test_Get_Prog_Generator_Name():
    #UT---------------------------------------
    Debug.Print('Get_Prog_Generator_Name=\'' + __Get_Prog_Generator_Name() + '\'')

def __Copy_Pattern_Macro_Callback(OK_Pressed, SendToArduino, GoBack):
    Macro_Line = String()

    p = Long()

    MacroTxt = String()

    LEDs = String()

    InCnt = Integer()

    LocInCh = Integer()

    Comment = String()

    Activation_Macro = String()

    Kanaele = Long()

    Startkanal = Long()

    Prog_Gen_Name = String()

    Makro_Name = String()

    Old_Comment = String()

    Comment_Range = Range()
    #----------------------------------------------------------------------------------------------------------
    # This Macro is called when the destination sheet and row in the Prog_Generator workbook is selected
    if not OK_Pressed:
        ThisWorkbook.Activate()
        return
    Macro_Line = ThisWorkbook.ActiveSheet.Range('Macro_Range')
    p = InStr(Macro_Line, ')')
    if p == 0:
        MsgBox(Get_Language_Str('Fehler in Makro Zeile: Klammer zu fehlt'), vbCritical, Get_Language_Str('Interner Macro Fehler'))
        return
    p = p + 1
    while Mid(Macro_Line, p, 1) == ' ':
        p = p + 1
    InCnt = 1
    LocInCh = 0
    if not Get_Additional_Goto_Activation_Macro(Activation_Macro, InCnt, LocInCh):
        return
        # Add macros like InCh_to_TmpVar()
    MacroTxt = Activation_Macro + Replace(Replace(Mid(Macro_Line, p), '(LED,', '(#LED,'), ',InCh,', ',#InCh,')
    Kanaele = ThisWorkbook.ActiveSheet.Range('Kanaele')
    Startkanal = ThisWorkbook.ActiveSheet.Range('Startkanal')
    if Kanaele % 3 == 0 and Startkanal == 0:
        LEDs = Kanaele / 3
    else:
        LEDs = 'C' + Startkanal + 1 + '-' + Startkanal + Kanaele
    Prog_Gen_Name = FileNameExt(__Get_Prog_Generator_Name())
    Makro_Name = ThisWorkbook.ActiveSheet.Range('Makro_Name') + FROM_PAT_CONFIG_TXT
    Comment_Range = Run(Prog_Gen_Name + '!Get_Description_Range_from_Act_Row')
    # Wenn Bereits ein Kommentar vorhanden ist, dieser aber nicht dem Makro namen entspricht und
    # nicht mit "(pc)" endet, dann wird gefragt ob der Kommentar überschrieben werden soll
    if Trim(Comment_Range.Value) != '' and Comment_Range.Value != Makro_Name and Right(Comment_Range.Value, Len(FROM_PAT_CONFIG_TXT)) != FROM_PAT_CONFIG_TXT:
        Comment_Range.Select()
        if vbNo == MsgBox(Get_Language_Str('Soll die bestehende Beschreibung durch') + vbCr + '  \'' + Makro_Name + Get_Language_Str('\' ersetzt werden?'), vbQuestion + vbYesNo + vbDefaultButton2, Get_Language_Str('Bestehende Beschreibung ersetzen?')):
            Makro_Name = ''
    Comment = Makro_Name
    Run(Prog_Gen_Name + '!Write_Macro_to_Act_Row', MacroTxt, LEDs, CStr(InCnt), CStr(LocInCh), Comment, False)
    if SendToArduino:
        Run(Prog_Gen_Name + '!Create_HeaderFile')
    if GoBack:
        ThisWorkbook.Activate()

def __Check_Duration_Row():
    fn_return_value = None
    #-----------------------------------------------
    # Check if the duration row is filled correcly
    ## VB2PY (CheckDirective) VB directive took path 1 on True
    if InStr(Range(ErgebnisRng), '!') > 0:
        Parts = Split(Range(ErgebnisRng), ',')
        for Nr in vbForRange(StartNr, UBound(Parts) - 1):
            if Left(Parts(Nr), 1) == '!':
                Col = Nr - StartNr + Dauer_Col1
                Application.ScreenUpdating = True
                Cells(Dauer_Row, Col).Select()
                select_0 = Left(Parts(Nr), 6)
                if (select_0 == '!Error'):
                    MsgBox(Get_Language_Str('Fehler in der markierten Spalte der Dauer Tabelle!' + vbCr + '  Ungültiger Eintrag: \'') + Replace(Mid(Parts(Nr), Len('!Error') + 2), '/16', '') + '\'' + vbCr + vbCr + Get_Language_Str('Folgende Bedingungen müssen erfüllt sein:' + vbCr + ' -Der Eintrag muss kleiner als 17 Minuten sein' + vbCr + ' -Es dürfen nur folgende Einheiten benutzt werden:' + vbCr + '   Min, Sek, Sec, sek, sec, Ms, ms' + vbCr + ' -Zwischen Zahl und Einheit muss ein Leerzeichen stehen'), vbCritical, Get_Language_Str('Fehler in \'Dauer\' Tabelle'))
                elif (select_0 == '!Empty'):
                    MsgBox(Get_Language_Str('Fehler: In der Dauer Tabelle dürfen keine Lücken sein' + vbCr + vbCr + 'Es müssen nicht alle Spalten der \'Dauer\' Tabelle ausgefüllt ' + 'werden. Bei Fehlenden Einträgen werden die Zeiten aus dem Anfang der ' + 'Tabelle gelesen.'), vbCritical, Get_Language_Str('Lücke in der Dauer Tabelle entdeckt'))
                else:
                    MsgBox(Get_Language_Str('Unbekannter Fehler in der \'Dauer\' Spalte'), vbCritical, Get_Language_Str('Internal Error:'))
    else:
        fn_return_value = True
    return fn_return_value

def Check_Table_before_Copy(Send_to_Prog_Gen):
    fn_return_value = None
    #------------------------------------------------------------------------------
    # Performe some checks before the Pattern function is copied to the Prog_Generator
    Draw_All_Arrows()
    if Goto_Start_Points > 1 and Send_to_Prog_Gen:
        if Trim(Range('Goto_Aktivierung')) == '':
            # Todo: Translate
            select_1 = MsgBox(Get_Language_Str('Wenn der Goto Mode aktiv ist, und mehrere Start Spalten vorhanden sind, dann muss eine Aktivierungsmethode ' + 'angegeben werden sonst können die Einsprung Spalten nicht erreicht werden.' + vbCr + vbCr + 'Soll die Methode jetzt definiert weden?'), vbQuestion + vbYesNoCancel, Get_Language_Str('Goto Aktivierung fehlt'))
            if (select_1 == vbYes):
                Select_GotoAct(Goto_Start_Points)
            elif (select_1 == vbCancel):
                return fn_return_value
    if Trim(Range('Makro_Name')) == '' and Send_to_Prog_Gen:
        Range('Makro_Name').Select()
        MsgBox(Get_Language_Str('Es wurde noch kein Makroname eingegeben ;-('), vbInformation, Get_Language_Str('Bitte Makro name eingeben'))
        return fn_return_value
    # Check if the table is filled
    if Range(TableEmptyMsgRng).Value != '':
        Cells(LEDsTAB_R, LEDsTAB_C).Select()
        MsgBox(Get_Language_Str('Die LED Tabelle ist leer. Bitte die Felder mit einem \'x\' markieren in denen die LEDs leuchten sein sollen'), vbCritical, Get_Language_Str('LED Tabelle leer'))
        return fn_return_value
    # Check if the duration row is filled correcly
    if not __Check_Duration_Row():
        return fn_return_value
    fn_return_value = True
    return fn_return_value

def Select_Line_in_Prog_Gen_and_Call_Macro(Get_Dest, Macro_Callback):
    Prog_Gen_Name = String()

    Ver = String()
    #-----------------------------------------------------------------------------------------------
    # Select the destination / source row in the Prog_Generator
    # If Get_Dest is true the destintion line which should be used to insert the Macro is requested
    # if Get_Dest is false the source line for importing the macro is requested
    #
    if Get_Dest:
        if False == Check_Table_before_Copy(True):
            return
    #Prog_Gen_Name = M30.FileNameExt(__Get_Prog_Generator_Name())
    #if Prog_Gen_Name == '':
    #    return
    # VB2PY (UntranslatedCode) On Error GoTo Wrong_Version
    #Ver = Run(Prog_Gen_Name + '!Get_Prog_Version_Nr')
    # VB2PY (UntranslatedCode) On Error GoTo 0
    #if not VersionStr_is_Greater(Exp_Prog_Gen_Version, Ver):
    #    # The dialog has to be located in the Prog_Generator because otherwise the window is not always shown on top of the screen
    Run(Prog_Gen_Name + '!Select_Line_for_Patern_Config_and_Call_Macro', Get_Dest, ThisWorkbook.Name + '!' + Macro_Callback)
    #    return
    #MsgBox(Get_Language_Str('Fehler: Das Prog_Generator Programm hat nicht die richtige Version.' + vbCr + vbCr + 'Es muss mindesten die Version ') + Exp_Prog_Gen_Version + Get_Language_Str(' haben'), vbCritical, Get_Language_Str('Falsche Prog_Generator Version'))

def Select_Destination_for_the_Pattern_Macro_and_Call_Copy():
    #------------------------------------------------------------------
    # Select the destination row in the Prog_Generator and copy the pattern macro into this line
    Select_Line_in_Prog_Gen_and_Call_Macro(True, 'Copy_Pattern_Macro_Callback')

# VB2PY (UntranslatedCode) Option Explicit
